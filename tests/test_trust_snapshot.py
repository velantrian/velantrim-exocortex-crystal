"""Tests for core/trust_snapshot.py — immutable read-time trust model."""

from dataclasses import FrozenInstanceError

import pytest

from core.trust_snapshot import (
    DEFAULT_CLAIM_TYPE,
    STORE_STATE_CONFLICT,
    TrustSnapshot,
    normalize_restricted_bit,
)


def _l3(**overrides):
    record = {
        "fact_id": "fact:1",
        "claim": "Lisbon is the capital of Portugal",
        "source": "reference",
        "confidence": 0.9,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
        "significance": 0.7,
    }
    record.update(overrides)
    return record


def _snapshot(l3=None, l1=None, score=0.8):
    record = _l3() if l3 is None else l3
    return TrustSnapshot.from_records(
        fact_id=record["fact_id"],
        l3=record,
        l1=l1,
        retrieval_score=score,
    )


def test_snapshot_is_frozen_slotted_and_does_not_retain_input_mapping():
    l3 = _l3()
    snapshot = _snapshot(l3=l3)

    with pytest.raises(FrozenInstanceError):
        snapshot.truth_status = "UNVERIFIED"
    assert not hasattr(snapshot, "__dict__")

    l3["claim"] = "mutated after construction"
    assert snapshot.claim == "Lisbon is the capital of Portugal"


def test_to_fact_dict_returns_fresh_compatibility_mappings():
    snapshot = _snapshot()

    first = snapshot.to_fact_dict()
    second = snapshot.to_fact_dict()

    assert first == second
    assert first is not second
    first["truth_status"] = "UNVERIFIED"
    assert snapshot.truth_status == "VERIFIED"
    assert second["truth_status"] == "VERIFIED"
    assert first["_store_conflicts"] == ()


def test_l3_is_authoritative_for_content_and_verdict_fields():
    l3 = _l3(claim="Canonical claim", source="canonical-source")
    l1 = {
        **l3,
        "claim": "stale L1 claim",
        "source": "stale-L1-source",
        "truth_status": "UNVERIFIED",
    }

    snapshot = _snapshot(l3=l3, l1=l1)

    assert snapshot.claim == "Canonical claim"
    assert snapshot.source == "canonical-source"
    assert snapshot.truth_status == "VERIFIED"


def test_l1_terminal_state_wins_deny_dominantly():
    snapshot = _snapshot(l1={**_l3(), "epistemic_state": "Contradicted"})

    assert snapshot.epistemic_state == "Contradicted"
    assert snapshot.conflict_fields == ()


@pytest.mark.parametrize("state", ["Collapsed", "Contradicted", "Deprecated"])
def test_each_terminal_l1_state_wins(state):
    snapshot = _snapshot(l1={**_l3(), "epistemic_state": state})
    assert snapshot.epistemic_state == state


def test_nonterminal_esm_drift_fails_closed_with_content_free_category():
    snapshot = _snapshot(l1={**_l3(), "epistemic_state": "Supported"})

    assert snapshot.epistemic_state == STORE_STATE_CONFLICT
    assert snapshot.conflict_fields == ("epistemic_state",)


def test_malformed_non_none_l1_state_fails_closed():
    snapshot = _snapshot(l1={**_l3(), "epistemic_state": ["Validated"]})

    assert snapshot.epistemic_state == STORE_STATE_CONFLICT
    assert snapshot.conflict_fields == ("epistemic_state",)


def test_l1_or_l3_confirmed_restriction_always_wins():
    from_l1 = _snapshot(l1={**_l3(), "restricted": True})
    from_l3 = _snapshot(
        l3=_l3(restricted=True),
        l1={**_l3(), "restricted": False},
    )

    assert from_l1.restricted is True
    assert from_l3.restricted is True


def test_l1_confirmed_false_fills_missing_l3_restriction():
    l3 = _l3()
    del l3["restricted"]

    snapshot = _snapshot(l3=l3, l1={**l3, "restricted": False})

    assert snapshot.restricted is False


def test_both_unknown_restrictions_remain_unknown():
    l3 = _l3()
    del l3["restricted"]
    l1 = dict(l3)

    assert _snapshot(l3=l3, l1=l1).restricted is None


@pytest.mark.parametrize(
    "value,expected",
    [
        (True, True),
        (False, False),
        (1, True),
        (0, False),
        (None, None),
        ("1", None),
        (1.0, None),
        (2, None),
    ],
)
def test_restriction_normalization_is_strict(value, expected):
    assert normalize_restricted_bit(value) is expected


def test_equal_confidence_representations_do_not_conflict():
    snapshot = _snapshot(
        l3=_l3(confidence=0.1 + 0.2),
        l1={**_l3(), "confidence": 0.3},
    )

    assert snapshot.epistemic_state == "Validated"
    assert snapshot.conflict_fields == ()


@pytest.mark.parametrize(
    "override,field",
    [
        ({"confidence": 0.1}, "confidence"),
        ({"claim_type": "OPINION"}, "claim_type"),
        ({"source_status": "USER_REPORTED"}, "source_status"),
    ],
)
def test_genuine_trust_metadata_drift_fails_closed(override, field):
    snapshot = _snapshot(l1={**_l3(), **override})

    assert snapshot.epistemic_state == STORE_STATE_CONFLICT
    assert field in snapshot.conflict_fields


def test_multiple_conflicts_are_deduplicated_and_ordered_by_contract():
    snapshot = _snapshot(
        l1={
            **_l3(),
            "epistemic_state": "Supported",
            "confidence": 0.1,
            "claim_type": "OPINION",
            "source_status": "USER_REPORTED",
        }
    )

    assert snapshot.conflict_fields == (
        "epistemic_state",
        "confidence",
        "claim_type",
        "source_status",
    )


def test_missing_l3_claim_type_uses_shared_world_fact_default():
    l3 = _l3()
    del l3["claim_type"]
    l1 = {**l3, "claim_type": DEFAULT_CLAIM_TYPE}

    snapshot = _snapshot(l3=l3, l1=l1)

    assert snapshot.claim_type == DEFAULT_CLAIM_TYPE
    assert snapshot.conflict_fields == ()


def test_missing_l1_trust_fields_do_not_invent_disagreement():
    snapshot = _snapshot(l1={"epistemic_state": "Validated", "restricted": False})

    assert snapshot.epistemic_state == "Validated"
    assert snapshot.conflict_fields == ()


@pytest.mark.parametrize(
    "bad",
    ["0.9", True, None, float("nan"), float("inf"), -0.1, 1.1, 10**1000],
)
def test_malformed_l3_confidence_is_unknown_and_fails_closed(bad):
    snapshot = _snapshot(l3=_l3(confidence=bad))

    assert snapshot.confidence is None
    assert snapshot.epistemic_state == STORE_STATE_CONFLICT
    assert snapshot.conflict_fields == ("confidence",)
    assert snapshot.to_fact_dict()["confidence"] == 0.0


def test_malformed_confidence_with_l1_row_is_a_store_conflict():
    snapshot = _snapshot(
        l3=_l3(confidence="0.9"),
        l1={**_l3(), "confidence": 0.9},
    )

    assert snapshot.confidence is None
    assert snapshot.epistemic_state == STORE_STATE_CONFLICT
    assert snapshot.conflict_fields == ("confidence",)
    assert snapshot.to_fact_dict()["confidence"] == 0.0


@pytest.mark.parametrize("field", ["claim", "source", "epistemic_state", "truth_status"])
def test_malformed_string_fields_become_none_without_stringification(field):
    snapshot = _snapshot(l3=_l3(**{field: ["bad"]}))
    assert getattr(snapshot, field) is None


def test_malformed_claim_type_and_source_status_become_none():
    snapshot = _snapshot(
        l3=_l3(claim_type={"bad": 1}, source_status=["EXTERNAL"])
    )
    assert snapshot.claim_type is None
    assert snapshot.source_status is None


@pytest.mark.parametrize("bad", ["0.9", True, None, float("nan"), 10**1000])
def test_malformed_retrieval_score_becomes_zero(bad):
    assert _snapshot(score=bad).retrieval_score == 0.0


def test_valid_negative_retrieval_score_is_preserved_as_ranking_metadata():
    assert _snapshot(score=-0.25).retrieval_score == -0.25


def test_malformed_significance_uses_neutral_default():
    assert _snapshot(l3=_l3(significance="high")).significance == 0.5


def test_invalid_fact_id_and_record_types_are_rejected():
    with pytest.raises(ValueError, match="fact_id"):
        TrustSnapshot.from_records(fact_id=" ", l3=_l3())
    with pytest.raises(TypeError, match="l3"):
        TrustSnapshot.from_records(fact_id="f", l3=[])
    with pytest.raises(TypeError, match="l1"):
        TrustSnapshot.from_records(fact_id="f", l3=_l3(), l1=[])


def test_direct_constructor_rejects_mutable_conflict_collection():
    with pytest.raises(TypeError, match="immutable tuple"):
        TrustSnapshot(
            fact_id="f",
            claim="c",
            source="s",
            confidence=0.9,
            epistemic_state="Validated",
            claim_type="WORLD_FACT",
            source_status="EXTERNAL",
            truth_status="VERIFIED",
            restricted=False,
            significance=0.5,
            retrieval_score=0.8,
            conflict_fields=[],
        )
