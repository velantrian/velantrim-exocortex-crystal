"""Tests for core/ingest.py — turning user utterances into typed facts."""
import pytest

from core.ingest import classify_claim, ingest
from core.l3_graph import get_l3_graph
from core.memory import get_fact


@pytest.mark.parametrize("text, expected", [
    ("I feel anxious when I talk to him", "EMOTION"),
    ("Я почувствовал тревогу при разговоре с X", "EMOTION"),
    ("I think this design is wrong", "OPINION"),
    ("По-моему это плохая идея", "OPINION"),
    ("I want to finish the project", "GOAL"),
    ("Я хочу закончить проект", "GOAL"),
    ("I prefer tea over coffee", "PREFERENCE"),
    ("Maybe he was unfriendly", "INTERPRETATION"),
    ("Возможно, он был недоброжелателен", "INTERPRETATION"),
    ("Water boils at 100 degrees", "WORLD_FACT"),
])
def test_classify_claim_detects_modality(text, expected):
    ct, source_status = classify_claim(text)
    assert ct == expected
    assert source_status == "USER_REPORTED"


def test_ingest_emotion_is_validated_but_not_world_fact():
    res = ingest("I feel anxious when I talk to X")
    assert res["accepted"] is True
    f = res["fact"]
    assert f["claim_type"] == "EMOTION"
    assert f["epistemic_state"] == "Validated"   # feeling is real as a feeling
    assert f["truth_status"] == "SUBJECTIVE"      # but not a fact about the world
    assert f["claim_type"] != "WORLD_FACT"


def test_ingest_world_fact_lands_in_l3_as_user_claimed():
    """Issue #63: a user-reported world fact is USER_CLAIMED, not VERIFIED.
    It is stored and reaches L3, but requires external evidence to become VERIFIED."""
    res = ingest("The Earth orbits the Sun")
    assert res["accepted"] is True
    assert res["fact"]["truth_status"] == "USER_CLAIMED"
    # canonical node is in L3 — stored and retrievable, just not VERIFIED
    assert "ing:" in res["fact"]["fact_id"]
    assert get_l3_graph().get_fact(res["fact"]["fact_id"]) is not None


def test_ingest_persists_to_sqlite_even_when_pending():
    res = ingest("I think the sky is green")
    fid = res["fact"]["fact_id"]
    assert get_fact(fid) is not None  # stored in L0/L1 regardless


def test_ingest_explicit_claim_type_overrides_classifier():
    res = ingest("anything", claim_type="OPINION")
    assert res["fact"]["claim_type"] == "OPINION"


def test_ingest_empty_raises():
    with pytest.raises(ValueError, match="empty utterance"):
        ingest("   ")


def test_ingest_exact_repeat_records_occurrence_without_reinforcing():
    """Variant B: an exact repeat is a frequency sighting, NOT independent
    evidence — occurrence metadata updates; confidence/truth_status/ESM do not."""
    from core.l3_graph import get_l3_graph
    first = ingest("Water boils at 100 degrees Celsius")
    assert first["accepted"] and not first.get("duplicate")
    fid = first["fact"]["fact_id"]
    c1 = first["fact"]["confidence"]
    ts1 = get_l3_graph().get_fact(fid).get("truth_status")   # canonical truth_status

    second = ingest("Water boils at 100 degrees Celsius")
    assert second["duplicate"] is True
    assert second["occurrences"] == 2
    f2 = second["fact"]
    assert f2["confidence"] == c1                  # confidence unchanged
    assert f2["epistemic_state"] == "Validated"    # ESM unchanged
    assert f2["metadata"]["occurrences"] == 2
    # Occurrence tracking must NOT touch the evidentiary observations counter.
    assert "observations" not in f2["metadata"]
    assert "fingerprint_sha256" in f2["metadata"]
    # The canonical truth_status in L3 is preserved (the sync does not clobber it).
    assert get_l3_graph().get_fact(fid).get("truth_status") == ts1


def test_ingest_surfaces_conflict_candidates_for_world_facts():
    """A new WORLD_FACT close to existing canon surfaces conflict candidates for
    explicit review — it does NOT auto-contradict."""
    from core.memory import get_fact

    ingest("The capital of Australia is Sydney")
    res = ingest("The capital of Australia is Canberra")
    assert res["accepted"] is True
    assert "conflicts" in res
    assert any("Sydney" in c["claim"] for c in res["conflicts"])
    # both still Validated — detection only surfaces, never auto-marks
    sydney_id = res["conflicts"][0]["fact_id"]
    assert get_fact(sydney_id)["epistemic_state"] == "Validated"


def test_ingest_low_confidence_world_fact_is_blocked():
    # WORLD_FACT below the TruthGate threshold is not accepted into canon.
    res = ingest("Plain statement of fact", confidence=0.0)
    assert res["accepted"] is False
    assert get_l3_graph().get_fact(res["fact"]["fact_id"]) is None
