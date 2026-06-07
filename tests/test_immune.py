"""Tests for the Immune / CRISPR Memory Guard (core/immune.py, RFC0072)."""
import json

import pytest

from core import immune


# ─── CRISPR threat memory: record / list / forget ─────────────────────────────

def test_record_and_list_threat():
    entry = immune.record_threat("The sky is green", threat_type="hallucination")
    assert entry["pattern"] == "the sky is green"      # normalized
    assert entry["severity"] == 1.0
    threats = immune.list_threats()
    assert len(threats) == 1
    assert threats[0]["pattern_id"] == entry["pattern_id"]
    assert threats[0]["threat_type"] == "hallucination"


def test_record_threat_is_idempotent_by_normalized_pattern():
    a = immune.record_threat("The  SKY is   green!")   # punctuation/case/space differ
    b = immune.record_threat("the sky is green")
    assert a["pattern_id"] == b["pattern_id"]
    assert len(immune.list_threats()) == 1


def test_record_threat_clamps_severity_and_rejects_empty():
    assert immune.record_threat("danger here", severity=5.0)["severity"] == 1.0
    assert immune.record_threat("other thing", severity=-2.0)["severity"] == 0.0
    with pytest.raises(ValueError):
        immune.record_threat("   ")


def test_forget_threat():
    e = immune.record_threat("bad pattern to drop")
    assert immune.forget_threat(e["pattern_id"]) is True
    assert immune.list_threats() == []
    assert immune.forget_threat(e["pattern_id"]) is False   # already gone


def test_record_and_forget_are_audited():
    from core.audit import audit_log
    e = immune.record_threat("auditable threat")
    immune.forget_threat(e["pattern_id"])
    events = [r["event"] for r in audit_log()]
    assert "immune_threat_recorded" in events
    assert "immune_threat_forgotten" in events


# ─── Pattern matching ─────────────────────────────────────────────────────────

def test_match_threat_whole_token_containment():
    immune.record_threat("the sky is green")
    hit = immune.match_threat("Actually the sky is green because of magic")
    assert hit is not None and hit["pattern"] == "the sky is green"


def test_match_threat_no_partial_word_match():
    immune.record_threat("cat")
    assert immune.match_threat("I love this category of things") is None  # not 'cat'egory


def test_match_threat_respects_severity_floor(monkeypatch):
    immune.record_threat("low risk phrase", severity=0.3)   # below 0.5 floor
    assert immune.match_threat("a low risk phrase indeed") is None
    monkeypatch.setenv("VELANTRIM_IMMUNE_BLOCK_SEVERITY", "0.2")
    assert immune.match_threat("a low risk phrase indeed") is not None


def test_block_severity_falls_back_on_malformed_env(monkeypatch):
    monkeypatch.setenv("VELANTRIM_IMMUNE_BLOCK_SEVERITY", "not-a-number")
    immune.record_threat("severe enough phrase", severity=1.0)
    assert immune.match_threat("a severe enough phrase here") is not None  # floor → 0.5


# ─── Screening verdicts ───────────────────────────────────────────────────────

def test_screen_admits_when_nothing_matches():
    v = immune.screen("a perfectly novel harmless claim", check_canon=False)
    assert v["verdict"] == immune.ADMIT


def test_screen_blocks_recorded_threat_and_counts_hits():
    immune.record_threat("vaccines cause autism", threat_type="harmful")
    v = immune.screen("the myth that vaccines cause autism persists", check_canon=False)
    assert v["verdict"] == immune.BLOCK
    assert v["threat"]["threat_type"] == "harmful"
    # the hit was registered on the stored entry
    assert immune.list_threats()[0]["hits"] == 1


def _validated_worldfact(claim):
    from core.ingest import ingest
    return ingest(claim)


def test_screen_quarantines_canon_contradiction_by_default(monkeypatch):
    monkeypatch.delenv("VELANTRIM_IMMUNE_STRICT", raising=False)
    _validated_worldfact("Sea levels are rising globally")
    v = immune.screen("Sea levels are falling globally")
    assert v["verdict"] == immune.QUARANTINE
    assert v["contradictions"], "expected a contradiction signal"


def test_screen_blocks_canon_contradiction_in_strict_mode(monkeypatch):
    monkeypatch.setenv("VELANTRIM_IMMUNE_STRICT", "1")
    _validated_worldfact("Sea levels are rising globally")
    v = immune.screen("Sea levels are falling globally")
    assert v["verdict"] == immune.BLOCK


def test_immunity_report():
    immune.record_threat("threat one", threat_type="hallucination")
    immune.record_threat("threat two", threat_type="harmful")
    immune.screen("threat one is here", check_canon=False)  # one hit
    rep = immune.immunity_report()
    assert rep["total_threats"] == 2
    assert rep["total_hits"] == 1
    assert rep["by_type"] == {"hallucination": 1, "harmful": 1}


# ─── Ingest integration ───────────────────────────────────────────────────────

def test_ingest_blocked_by_recorded_threat():
    from core.ingest import ingest
    immune.record_threat("the earth is flat", threat_type="hallucination")
    res = ingest("As everyone knows, the earth is flat")
    assert res["accepted"] is False
    assert res["reason"].startswith("Immune:")
    assert res["immune"]["verdict"] == immune.BLOCK


def test_ingest_contradiction_accepted_by_default(monkeypatch):
    # Truth-first regression: a contradicting WORLD_FACT is admitted & linked, not
    # blocked, unless strict mode is on.
    from core.ingest import ingest
    monkeypatch.delenv("VELANTRIM_IMMUNE_STRICT", raising=False)
    ingest("Global temperatures are increasing")
    res = ingest("Global temperatures are decreasing")
    assert res["accepted"] is True
    assert any(c["kind"] == "CONTRADICTION" for c in res.get("conflicts", []))


def test_ingest_strict_mode_blocks_and_learns(monkeypatch):
    from core.ingest import ingest
    monkeypatch.setenv("VELANTRIM_IMMUNE_STRICT", "1")
    monkeypatch.setenv("VELANTRIM_IMMUNE_LEARN", "1")
    ingest("Global temperatures are increasing")
    blocked = ingest("Global temperatures are decreasing")
    assert blocked["accepted"] is False
    assert "contradicts" in blocked["reason"]
    # adaptive immunity: the blocked claim is now a recorded threat …
    assert any(t["threat_type"] == "contradiction" for t in immune.list_threats())
    # … so a repeat is caught pre-gate by the threat memory.
    again = ingest("Global temperatures are decreasing")
    assert again["accepted"] is False
    assert again["immune"]["verdict"] == immune.BLOCK
    assert again["immune"]["threat"] is not None


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_immune_roundtrip(capsys):
    from core.cli import main

    assert main(["immune-block", "the moon is made of cheese",
                 "--type", "hallucination", "--severity", "0.9"]) == 0
    entry = json.loads(capsys.readouterr().out.strip())
    assert entry["threat_type"] == "hallucination"

    assert main(["immune-check", "clearly the moon is made of cheese"]) == 0
    verdict = json.loads(capsys.readouterr().out.strip())
    assert verdict["verdict"] == "BLOCK"

    assert main(["immune-report"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep["total_threats"] == 1

    assert main(["immune-allow", entry["pattern_id"]]) == 0
    assert json.loads(capsys.readouterr().out.strip())["forgotten"] is True
