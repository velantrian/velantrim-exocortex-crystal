"""Tests for core/mosc.py — the advisory claim-type classifier."""
import json

import pytest

from core import audit, mosc
from core.cli import main


def _write_weights(tmp_path, data):
    path = tmp_path / "weights.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return str(path)


# ─── Validation (negative tests) ──────────────────────────────────────────────

def test_invalid_claim_type_in_json_raises(tmp_path, monkeypatch):
    path = _write_weights(tmp_path, {
        "threshold": 0.6, "keywords": {"foo": {"NOT_A_TYPE": 0.7}}})
    monkeypatch.setenv("VELANTRIM_MOSC_PATH", path)
    with pytest.raises(ValueError, match="NOT_A_TYPE"):
        mosc.get_mosc()


@pytest.mark.parametrize("weight", [0.0, -0.5, 1.5, "high", True, None])
def test_weight_out_of_unit_interval_raises(tmp_path, monkeypatch, weight):
    path = _write_weights(tmp_path, {
        "threshold": 0.6, "keywords": {"foo": {"EMOTION": weight}}})
    monkeypatch.setenv("VELANTRIM_MOSC_PATH", path)
    with pytest.raises(ValueError, match="weight"):
        mosc.get_mosc()


@pytest.mark.parametrize("doc", [
    [],                                              # non-object root
    {"keywords": {}},                                # empty keywords
    {"threshold": 0, "keywords": {"a": {"GOAL": 0.7}}},   # bad threshold
    {"threshold": 0.6, "keywords": {" ": {"GOAL": 0.7}}}, # blank keyword
    {"threshold": 0.6, "keywords": {"a": {}}},       # empty mapping
])
def test_structural_problems_raise(tmp_path, monkeypatch, doc):
    path = _write_weights(tmp_path, doc)
    monkeypatch.setenv("VELANTRIM_MOSC_PATH", path)
    with pytest.raises(ValueError):
        mosc.get_mosc()


# ─── Scoring / classification ─────────────────────────────────────────────────

def test_scores_sum_over_matched_keywords():
    m = mosc.get_mosc()
    scores = m.score("I feel afraid and the feeling grows")
    assert scores["EMOTION"] >= 0.7 * 3      # i feel + afraid + feeling


def test_word_boundary_for_single_words_cyrillic_and_latin():
    m = mosc.get_mosc()
    assert m.score("imhotep built pyramids") == {}       # 'imho' bounded
    assert "EMOTION" in m.score("меня мучает тревога")   # cyrillic boundary
    assert m.score("тревогами полна") == {}              # inflected ≠ keyword


def test_phrase_keywords_match_as_substrings():
    m = mosc.get_mosc()
    assert "EMOTION" in m.score("я чувствую усталость")  # stem 'я чувству'


def test_below_threshold_returns_none():
    assert mosc.classify("Water boils at 100 degrees") is None
    assert mosc.classify("") is None


def test_tie_break_is_deterministic(tmp_path, monkeypatch):
    path = _write_weights(tmp_path, {
        "threshold": 0.6,
        "keywords": {"crossroads": {"GOAL": 0.7, "OPINION": 0.7}}})
    monkeypatch.setenv("VELANTRIM_MOSC_PATH", path)
    mosc.reset_mosc()
    # Equal scores → the historical marker order wins (OPINION before GOAL).
    assert mosc.classify("at a crossroads") == "OPINION"


# ─── Advisory boundary ────────────────────────────────────────────────────────

def test_mosc_never_suggests_world_fact_and_gates_unchanged():
    from core.ingest import ingest
    res = ingest("The Danube flows through Vienna")
    assert res["fact"]["claim_type"] == "WORLD_FACT"      # via fallback default
    assert res["fact"]["truth_status"] == "USER_CLAIMED"
    emo = ingest("I feel very tired today")
    assert emo["fact"]["claim_type"] == "EMOTION"         # via MOSC
    assert emo["fact"]["truth_status"] == "SUBJECTIVE"    # same gate rules


def test_classify_detailed_both_methods():
    d = mosc.classify_detailed("I believe this approach is right")
    assert d["method"] == "mosc"
    assert d["claim_type"] == "OPINION"
    assert d["score"] >= 0.6
    assert "OPINION" in d["matched_categories"]
    f = mosc.classify_detailed("Gold is a chemical element")
    assert f["method"] == "fallback"
    assert f["claim_type"] == "WORLD_FACT"
    assert f["score"] == 0.0


# ─── Audit of operator overrides ──────────────────────────────────────────────

def test_env_override_is_audited_content_free(tmp_path, monkeypatch):
    path = _write_weights(tmp_path, {
        "threshold": 0.6, "keywords": {"deadline": {"GOAL": 0.7}}})
    monkeypatch.setenv("VELANTRIM_MOSC_PATH", path)
    mosc.reset_mosc()
    mosc.get_mosc()
    events = [e for e in audit.audit_log()
              if e["event"] == "mosc_weights_loaded"]
    assert len(events) == 1
    detail = events[0]["detail"]
    assert set(detail) == {"sha256", "source", "keywords", "threshold"}
    assert "deadline" not in json.dumps(detail)   # keyword lists stay out
    assert audit.verify_audit_log()["ok"] is True
    # Re-loading the same file must not append a duplicate event.
    mosc.reset_mosc()
    mosc.get_mosc()
    assert len([e for e in audit.audit_log()
                if e["event"] == "mosc_weights_loaded"]) == 1


def test_changed_override_appends_new_hash(tmp_path, monkeypatch):
    path1 = _write_weights(tmp_path, {
        "threshold": 0.6, "keywords": {"alpha": {"GOAL": 0.7}}})
    monkeypatch.setenv("VELANTRIM_MOSC_PATH", path1)
    mosc.reset_mosc()
    sha1 = mosc.get_mosc().sha256
    path2 = tmp_path / "weights2.json"
    path2.write_text(json.dumps(
        {"threshold": 0.6, "keywords": {"beta": {"GOAL": 0.8}}}),
        encoding="utf-8")
    monkeypatch.setenv("VELANTRIM_MOSC_PATH", str(path2))
    mosc.reset_mosc()
    sha2 = mosc.get_mosc().sha256
    assert sha1 != sha2
    hashes = [e["detail"]["sha256"] for e in audit.audit_log()
              if e["event"] == "mosc_weights_loaded"]
    assert hashes == [sha1, sha2]


def test_package_defaults_are_not_audited():
    mosc.get_mosc()
    assert all(e["event"] != "mosc_weights_loaded" for e in audit.audit_log())


# ─── Packaging / report / CLI ─────────────────────────────────────────────────

def test_default_weights_load_via_package_resources():
    from importlib import resources
    raw = resources.files("core").joinpath(
        "_mosc/claim_keywords.json").read_text(encoding="utf-8")
    assert json.loads(raw)["keywords"]
    rep = mosc.report()
    assert rep["source"] == "package"
    assert len(rep["sha256"]) == 64
    assert rep["keywords"] > 0


def test_cli_mosc_classify(capsys):
    assert main(["mosc-classify", "I think we should refactor"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["method"] == "mosc" and out["claim_type"] == "OPINION"


def test_cli_mosc_report(capsys):
    assert main(["mosc-report"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["source"] == "package" and out["threshold"] == 0.6


def test_regex_fallback_still_classifies_when_mosc_abstains():
    """'i like ... better' is a regex marker with no MOSC keyword: MOSC must
    abstain and the historical fallback must still type it PREFERENCE."""
    from core.ingest import classify_claim
    text = "i like tea better than coffee"
    assert mosc.classify(text) is None
    assert classify_claim(text) == ("PREFERENCE", "USER_REPORTED")
