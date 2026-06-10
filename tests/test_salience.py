"""Tests for core/salience.py — utterance salience → significance."""
import pytest

from core.ingest import ingest
from core.salience import (
    CAPS, EXCLAMATION, IMPORTANCE_EN, IMPORTANCE_RU, analyze, significance_for,
)


# ─── Scoring rules (Eiti heritage) ────────────────────────────────────────────

def test_plain_text_is_exactly_baseline():
    res = analyze("the cat sat on the mat quietly")
    assert res["salience"] == 1.0
    assert res["markers"] == []
    assert res["significance"] == 0.5      # backward-compat hard requirement


@pytest.mark.parametrize("text,marker,factor", [
    ("this is URGENT business", CAPS, 1.5),
    ("call me back!", EXCLAMATION, 1.3),
    ("это критично для проекта", IMPORTANCE_RU, 1.4),
    ("запомни этот адрес", IMPORTANCE_RU, 1.4),
    ("this is important for the project", IMPORTANCE_EN, 1.4),
    ("remember the deadline", IMPORTANCE_EN, 1.4),
])
def test_single_marker_categories(text, marker, factor):
    res = analyze(text)
    assert res["markers"] == [marker]
    assert res["salience"] == factor


def test_caps_needs_three_consecutive_uppercase():
    assert CAPS not in analyze("OK then")["markers"]
    assert CAPS in analyze("ВАЖНОЕ дело")["markers"]


def test_markers_multiply():
    res = analyze("ВАЖНО: никогда не публикуй ключи! this is critical")
    assert set(res["markers"]) == {CAPS, EXCLAMATION, IMPORTANCE_RU,
                                   IMPORTANCE_EN}
    assert res["salience"] == round(1.5 * 1.3 * 1.4 * 1.4, 4)
    assert res["significance"] == 1.0      # capped by the [.., 1.0] mapping


def test_salience_cap():
    # All four categories: 1.5·1.3·1.4·1.4 = 3.822 < 4.0 — the cap holds.
    assert analyze("NEVER do this! всегда помни, must remember")["salience"] <= 4.0


def test_significance_mapping_bounds():
    assert significance_for("plain text") == 0.5
    assert significance_for("URGENT!") == min(1.0, round(0.5 * 1.5 * 1.3, 4))
    assert 0.5 <= significance_for("anything at all") <= 1.0


def test_empty_text_is_baseline():
    assert analyze("")["significance"] == 0.5


# ─── Ingest integration ───────────────────────────────────────────────────────

def test_ingest_auto_significance_with_explainability_metadata():
    res = ingest("ВАЖНО: сервер падает каждую ночь!")
    fact = res["fact"]
    assert fact["significance"] > 0.5
    meta = fact["metadata"]
    assert meta["significance_source"] == "auto_salience"
    assert meta["salience_score"] > 1.0
    assert set(meta["salience_markers"]) <= {CAPS, EXCLAMATION, IMPORTANCE_RU,
                                             IMPORTANCE_EN}
    # Privacy: categories only — never the matched raw text.
    assert all(m.isupper() and " " not in m for m in meta["salience_markers"])


def test_ingest_plain_text_keeps_legacy_default_and_no_metadata():
    res = ingest("the moon orbits the earth")
    fact = res["fact"]
    assert fact["significance"] == 0.5
    assert "significance_source" not in fact.get("metadata", {})


def test_ingest_explicit_significance_always_wins():
    res = ingest("ВАЖНО: this is critical!", significance=0.1)
    fact = res["fact"]
    assert fact["significance"] == 0.1
    assert "significance_source" not in fact.get("metadata", {})


def test_auto_salience_never_touches_truth_fields():
    """Negative test: salience must not alter confidence/truth_status/ESM."""
    loud = ingest("Mars has two moons, NEVER forget this!")["fact"]
    quiet = ingest("Venus has no moons at all")["fact"]
    assert loud["confidence"] == quiet["confidence"] == 0.6
    assert loud["truth_status"] == quiet["truth_status"]
    assert loud["epistemic_state"] == quiet["epistemic_state"]


def test_anchor_strength_grows_with_auto_significance():
    from core import fractal
    loud = ingest("CRITICAL: backups run nightly, always verify them!")["fact"]
    quiet = ingest("the office plant is a ficus")["fact"]
    assert fractal.anchor_strength(loud) > fractal.anchor_strength(quiet)
