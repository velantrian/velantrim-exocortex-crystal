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


def test_ingest_world_fact_is_verified_and_lands_in_l3():
    res = ingest("The Earth orbits the Sun")
    assert res["accepted"] is True
    assert res["fact"]["truth_status"] == "VERIFIED"
    # canonical node is in L3
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
    with pytest.raises(ValueError, match="пустая реплика"):
        ingest("   ")


def test_ingest_exact_repeat_reinforces_confidence():
    """An exact re-assertion is independent evidence → reinforce, not duplicate."""
    first = ingest("Water boils at 100 degrees Celsius")
    assert first["accepted"] and not first.get("reinforced")
    c1 = first["fact"]["confidence"]

    second = ingest("Water boils at 100 degrees Celsius")
    assert second["reinforced"] is True
    assert second["fact"]["confidence"] > c1
    assert second["fact"]["metadata"]["observations"] == 2


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
