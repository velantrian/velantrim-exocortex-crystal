from dataclasses import replace
from datetime import datetime, timezone

import pytest

from prototypes.research_mode.essence_card import (
    CausalCandidateEdge,
    ConfidenceBreakdown,
    ContradictionRef,
    EssenceCard,
    EssenceCardRevision,
    EssenceCardStatus,
    FieldChange,
    ResearchFailureEvent,
    TERMINAL_STATUSES,
    transition_allowed,
    validate_causal_candidate_edge,
    validate_essence_card,
    validate_research_failure_event,
)


def make_card(status: EssenceCardStatus = EssenceCardStatus.HYPOTHESIS) -> EssenceCard:
    return EssenceCard(
        card_id="ess_test",
        source_event_ids=("evt_1",),
        core_essence="Test essence",
        topic="test",
        status=status,
        confidence=ConfidenceBreakdown(0.72, 0.81, 0.65, 0.78, 0.88, 0.12, "v0.1"),
        stability=0.68,
        novelty=0.45,
        evidence_refs=(),
        contradictions=(),
        supersedes=(),
        superseded_by=None,
        failure_flags=(),
        created_at=datetime.now(timezone.utc),
        last_updated=datetime.now(timezone.utc),
    )


def test_tuples_are_immutable():
    card = make_card()
    with pytest.raises(AttributeError):
        card.evidence_refs.append("new")  # type: ignore[attr-defined]


def test_essence_card_revision_changed_fields_is_immutable():
    revision = EssenceCardRevision(
        revision_id="rev_001",
        card_id="ess_test",
        previous_revision_id=None,
        changed_fields=(
            FieldChange(
                field_name="status",
                old_value="HYPOTHESIS",
                new_value="PATTERN_CANDIDATE",
            ),
        ),
        reason="test",
        actor="system",
        evidence_refs=(),
        created_at=datetime.now(timezone.utc),
    )
    with pytest.raises(AttributeError):
        revision.changed_fields.append(  # type: ignore[attr-defined]
            FieldChange(field_name="test", old_value="a", new_value="b")
        )


def test_terminal_statuses_block_all_transitions():
    for terminal in TERMINAL_STATUSES:
        assert transition_allowed(terminal, EssenceCardStatus.NEEDS_REVIEW) is False


def test_rejected_requires_human_or_policy_and_evidence():
    assert (
        transition_allowed(
            EssenceCardStatus.HYPOTHESIS,
            EssenceCardStatus.REJECTED,
            actor="human",
            evidence_refs=("review_001",),
        )
        is True
    )

    assert (
        transition_allowed(
            EssenceCardStatus.HYPOTHESIS,
            EssenceCardStatus.REJECTED,
            actor="policy",
            evidence_refs=("policy_review_001",),
        )
        is True
    )

    assert (
        transition_allowed(
            EssenceCardStatus.HYPOTHESIS,
            EssenceCardStatus.REJECTED,
            actor="system",
            evidence_refs=("review_001",),
        )
        is False
    )

    assert (
        transition_allowed(
            EssenceCardStatus.HYPOTHESIS,
            EssenceCardStatus.REJECTED,
            actor="human",
            evidence_refs=(),
        )
        is False
    )


def test_superseded_requires_evidence():
    assert (
        transition_allowed(
            EssenceCardStatus.CONFIRMED_PATTERN,
            EssenceCardStatus.SUPERSEDED,
            evidence_refs=("evidence_042",),
        )
        is True
    )

    assert (
        transition_allowed(
            EssenceCardStatus.CONFIRMED_PATTERN,
            EssenceCardStatus.SUPERSEDED,
            evidence_refs=(),
        )
        is False
    )


def test_confirmed_pattern_requires_evidence():
    assert (
        transition_allowed(
            EssenceCardStatus.PATTERN_CANDIDATE,
            EssenceCardStatus.CONFIRMED_PATTERN,
            evidence_refs=("validation_01",),
        )
        is True
    )

    assert (
        transition_allowed(
            EssenceCardStatus.PATTERN_CANDIDATE,
            EssenceCardStatus.CONFIRMED_PATTERN,
            evidence_refs=(),
        )
        is False
    )


def test_principle_candidate_requires_evidence():
    assert (
        transition_allowed(
            EssenceCardStatus.CONFIRMED_PATTERN,
            EssenceCardStatus.PRINCIPLE_CANDIDATE,
            evidence_refs=("strong_evidence",),
        )
        is True
    )

    assert (
        transition_allowed(
            EssenceCardStatus.CONFIRMED_PATTERN,
            EssenceCardStatus.PRINCIPLE_CANDIDATE,
            evidence_refs=(),
        )
        is False
    )


def test_validate_essence_card_rejects_invalid_confidence():
    card = make_card()
    bad_confidence = ConfidenceBreakdown(1.5, 0.8, 0.7, 0.8, 0.9, 0.1, "v0.1")
    bad_card = replace(card, confidence=bad_confidence)

    with pytest.raises(ValueError):
        validate_essence_card(bad_card)


def test_validate_research_failure_event_rejects_invalid_severity():
    event = ResearchFailureEvent(
        event_id="fail_001",
        card_id="ess_test",
        failure_flag="premature_principle",
        severity=1.3,
        description="test",
        detected_by="system",
        evidence_refs=(),
        created_at=datetime.now(timezone.utc),
    )

    with pytest.raises(ValueError):
        validate_research_failure_event(event)


def test_validate_causal_candidate_edge_rejects_invalid_strength():
    edge = CausalCandidateEdge(
        edge_id="edge_001",
        source_card_id="ess_1",
        target_card_id="ess_2",
        phrasing="candidate_causal",
        strength=1.4,
        evidence_type="temporal",
        evidence_refs=(),
        created_at=datetime.now(timezone.utc),
    )

    with pytest.raises(ValueError):
        validate_causal_candidate_edge(edge)


# ── Additional coverage cases (keep essence_card.py at 100% under the repo's
# ── --cov-fail-under=100 gate; source files are unchanged from the spec). ──────


def test_validate_essence_card_accepts_valid_card():
    # Exercises every scalar _validate_score line on the success path.
    assert validate_essence_card(make_card()) is None


def test_validate_essence_card_rejects_invalid_contradiction_severity():
    # Drives the `for contradiction in card.contradictions` loop body.
    card = make_card()
    bad_card = replace(
        card,
        contradictions=(
            ContradictionRef(
                target_card_id="ess_other",
                type="negation",
                severity=1.5,
                evidence_ref="ev_1",
            ),
        ),
    )

    with pytest.raises(ValueError):
        validate_essence_card(bad_card)


def test_same_status_transition_is_rejected():
    assert (
        transition_allowed(
            EssenceCardStatus.HYPOTHESIS,
            EssenceCardStatus.HYPOTHESIS,
        )
        is False
    )


def test_transition_to_needs_review_always_allowed():
    assert (
        transition_allowed(
            EssenceCardStatus.HYPOTHESIS,
            EssenceCardStatus.NEEDS_REVIEW,
        )
        is True
    )


def test_forward_progression_transitions():
    assert (
        transition_allowed(
            EssenceCardStatus.RAW_OBSERVATION,
            EssenceCardStatus.HYPOTHESIS,
        )
        is True
    )
    assert (
        transition_allowed(
            EssenceCardStatus.HYPOTHESIS,
            EssenceCardStatus.PATTERN_CANDIDATE,
        )
        is True
    )


def test_needs_review_to_archived_requires_human_or_policy_and_evidence():
    assert (
        transition_allowed(
            EssenceCardStatus.NEEDS_REVIEW,
            EssenceCardStatus.ARCHIVED,
            actor="human",
            evidence_refs=("review_002",),
        )
        is True
    )

    assert (
        transition_allowed(
            EssenceCardStatus.NEEDS_REVIEW,
            EssenceCardStatus.ARCHIVED,
            actor="system",
            evidence_refs=("review_002",),
        )
        is False
    )

    assert (
        transition_allowed(
            EssenceCardStatus.NEEDS_REVIEW,
            EssenceCardStatus.ARCHIVED,
            actor="human",
            evidence_refs=(),
        )
        is False
    )


def test_superseded_to_archived_requires_evidence():
    assert (
        transition_allowed(
            EssenceCardStatus.SUPERSEDED,
            EssenceCardStatus.ARCHIVED,
            evidence_refs=("evidence_099",),
        )
        is True
    )

    assert (
        transition_allowed(
            EssenceCardStatus.SUPERSEDED,
            EssenceCardStatus.ARCHIVED,
            evidence_refs=(),
        )
        is False
    )


def test_unknown_transition_falls_through_to_false():
    assert (
        transition_allowed(
            EssenceCardStatus.RAW_OBSERVATION,
            EssenceCardStatus.CONFIRMED_PATTERN,
        )
        is False
    )


def test_validate_research_failure_event_accepts_valid_severity():
    event = ResearchFailureEvent(
        event_id="fail_002",
        card_id="ess_test",
        failure_flag="weak_evidence",
        severity=0.4,
        description="test",
        detected_by="system",
        evidence_refs=(),
        created_at=datetime.now(timezone.utc),
    )

    assert validate_research_failure_event(event) is None


def test_validate_causal_candidate_edge_accepts_valid_strength():
    edge = CausalCandidateEdge(
        edge_id="edge_002",
        source_card_id="ess_1",
        target_card_id="ess_2",
        phrasing="often_preceded",
        strength=0.6,
        evidence_type="temporal",
        evidence_refs=(),
        created_at=datetime.now(timezone.utc),
    )

    assert validate_causal_candidate_edge(edge) is None
