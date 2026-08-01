"""Tests for immutable contradiction reports and explicit review decisions."""

from dataclasses import FrozenInstanceError

import pytest

from core import audit, review
from core.conflict_decision import REL_CONTEXTUALIZES
from core.contradiction import CONTRADICTION
from core.contradiction_report import (
    ConflictDisposition,
    ConflictReference,
    ContradictionReport,
)
from core.l3_graph import get_l3_graph
from core.memory import get_fact, store_fact, transition_esm
from core.reconcile import REL_CONTRADICTS, REL_SUPERSEDED_BY


def _validated(fact_id: str, claim: str) -> str:
    store_fact(
        {
            "fact_id": fact_id,
            "claim": claim,
            "source": "reference",
            "confidence": 0.9,
            "epistemic_state": "Observed",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "significance": 0.5,
        }
    )
    assert transition_esm(fact_id, "Validated") is True
    fact = get_fact(fact_id)
    fact["truth_status"] = "VERIFIED"
    get_l3_graph().merge_fact(fact)
    return fact_id


def _pending(fact_id: str, claim: str) -> str:
    store_fact(
        {
            "fact_id": fact_id,
            "claim": claim,
            "source": "candidate-reference",
            "confidence": 0.9,
            "epistemic_state": "Observed",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "significance": 0.5,
        }
    )
    return fact_id


def _conflict_pair(prefix: str = "ctr") -> tuple[str, str]:
    old_id = _validated(
        f"{prefix}:old", "The vaccine is effective against the virus"
    )
    new_id = _pending(
        f"{prefix}:new", "The vaccine is not effective against the virus"
    )
    diagnosis = review.review_item(new_id)["diagnosis"]
    assert diagnosis["verdict"] == "conflict"
    return old_id, new_id


def test_report_is_frozen_deterministic_deduplicated_and_content_free():
    candidates = [
        {
            "fact_id": "old:2",
            "claim": "secret conflicting claim two",
            "similarity": 0.8,
            "kind": CONTRADICTION,
            "signal": "negation",
        },
        {
            "fact_id": "old:1",
            "claim": "secret conflicting claim one",
            "similarity": 0.9,
            "kind": CONTRADICTION,
            "signal": "numeric",
        },
        {
            "fact_id": "old:2",
            "claim": "duplicate retrieval hit",
            "similarity": 0.7,
            "kind": CONTRADICTION,
            "signal": "negation",
        },
    ]

    first = ContradictionReport.from_candidates(
        candidate_fact_id="new:1", candidates=candidates
    )
    second = ContradictionReport.from_candidates(
        candidate_fact_id="new:1", candidates=reversed(candidates)
    )

    assert first.report_id == second.report_id
    assert first.conflict_ids == ("old:1", "old:2")
    assert first.disposition is ConflictDisposition.REVIEW_REQUIRED
    rendered = first.to_dict()
    assert rendered["automatic_winner"] is None
    assert "secret" not in str(rendered)
    assert "claim" not in str(rendered)

    with pytest.raises(FrozenInstanceError):
        first.report_id = "changed"
    with pytest.raises(FrozenInstanceError):
        first.conflicts[0].fact_id = "changed"


def test_report_validation_and_fresh_dicts():
    ref = ConflictReference(
        fact_id="old", kind=CONTRADICTION, signal="negation", similarity=0.8
    )
    report = ContradictionReport(
        report_id="ctr:one", candidate_fact_id="new", conflicts=(ref,)
    )
    first = report.to_dict()
    second = report.to_dict()
    first["conflicts"][0]["fact_id"] = "mutated"
    assert second["conflicts"][0]["fact_id"] == "old"
    assert report.with_disposition("COEXIST").disposition is ConflictDisposition.COEXIST

    with pytest.raises(ValueError, match="at least one"):
        ContradictionReport.from_candidates(candidate_fact_id="new", candidates=[])
    with pytest.raises(ValueError, match="itself"):
        ContradictionReport(
            report_id="ctr:self", candidate_fact_id="new", conflicts=(
                ConflictReference(
                    fact_id="new", kind=CONTRADICTION, signal=None, similarity=1.0
                ),
            )
        )


def test_diagnosis_contains_content_free_report_and_normal_approve_fails_closed():
    old_id, new_id = _conflict_pair("diag")
    item = review.review_item(new_id)
    report = item["diagnosis"]["contradiction_report"]

    assert report["candidate_fact_id"] == new_id
    assert report["conflict_ids"] == [old_id]
    assert report["automatic_winner"] is None
    assert "effective against" not in str(report)

    events_before = len(audit.audit_log())
    result = review.approve(new_id, actor="alice")
    assert result["approved"] is False
    assert result["reason"] == "CONFLICT_DECISION_REQUIRED"
    assert get_fact(new_id)["epistemic_state"] == "Observed"
    assert get_l3_graph().get_fact(new_id) is None
    assert len(audit.audit_log()) == events_before


def test_conflict_resolution_requires_actor_reason_and_current_report():
    _, new_id = _conflict_pair("required")
    report_id = review.review_item(new_id)["diagnosis"]["contradiction_report"][
        "report_id"
    ]

    for kwargs in (
        {"disposition": "COEXIST", "actor": None, "reason": "why"},
        {"disposition": "COEXIST", "actor": "alice", "reason": " "},
        {"disposition": "REVIEW_REQUIRED", "actor": "alice", "reason": "wait"},
        {"disposition": "UNKNOWN", "actor": "alice", "reason": "why"},
    ):
        result = review.resolve_conflict(new_id, **kwargs)
        assert result.get("applied") is False
        assert get_fact(new_id)["epistemic_state"] == "Observed"

    stale = review.resolve_conflict(
        new_id,
        disposition="COEXIST",
        actor="alice",
        reason="independent sources disagree",
        expected_report_id=report_id + "stale",
    )
    assert stale["reason"] == "CONTRADICTION_REPORT_CHANGED"
    assert get_fact(new_id)["epistemic_state"] == "Observed"


def test_coexist_promotes_both_and_records_content_free_decision():
    old_id, new_id = _conflict_pair("coexist")
    report_id = review.review_item(new_id)["diagnosis"]["contradiction_report"][
        "report_id"
    ]

    result = review.resolve_conflict(
        new_id,
        disposition="COEXIST",
        actor="alice",
        reason="two independent sources must remain visible",
        expected_report_id=report_id,
    )

    assert result["applied"] is True
    assert result["approved"] is True
    assert result["disposition"] == "COEXIST"
    assert get_fact(old_id)["epistemic_state"] == "Validated"
    assert get_fact(new_id)["epistemic_state"] == "Validated"
    edges = get_l3_graph().get_edges(new_id, REL_CONTRADICTS)
    assert [edge["target"] for edge in edges] == [old_id]
    assert edges[0]["props"]["report_id"] == report_id

    event = [
        entry for entry in audit.audit_log()
        if entry["event"] == "review_conflict_coexist"
    ][-1]
    assert event["detail"]["actor"] == "alice"
    assert event["detail"]["conflict_ids"] == [old_id]
    assert "vaccine" not in str(event["detail"])
    history = review.decisions(limit=1, include_claim=False)[0]
    assert history["decision"] == "conflict_coexist"
    assert history["report_id"] == report_id
    assert "claim" not in history


def test_contextualize_preserves_both_with_distinct_relation():
    old_id, new_id = _conflict_pair("context")
    result = review.resolve_conflict(
        new_id,
        disposition="CONTEXTUALIZE",
        actor="bob",
        reason="claims apply to different study populations",
    )

    assert result["applied"] is True
    assert get_fact(old_id)["epistemic_state"] == "Validated"
    assert get_fact(new_id)["epistemic_state"] == "Validated"
    edges = get_l3_graph().get_edges(new_id, REL_CONTEXTUALIZES)
    assert [edge["target"] for edge in edges] == [old_id]
    assert not get_l3_graph().get_edges(new_id, REL_CONTRADICTS)


def test_supersede_requires_explicit_report_target_and_deprecates_selected_fact():
    old_id, new_id = _conflict_pair("supersede")

    missing = review.resolve_conflict(
        new_id,
        disposition="SUPERSEDE",
        actor="carol",
        reason="newer authoritative source",
    )
    assert missing["applied"] is False
    assert "requires at least one" in missing["reason"]
    assert get_fact(new_id)["epistemic_state"] == "Observed"

    unknown = review.resolve_conflict(
        new_id,
        disposition="SUPERSEDE",
        actor="carol",
        reason="newer authoritative source",
        target_fact_ids=["not-in-report"],
    )
    assert unknown["applied"] is False
    assert "current report" in unknown["reason"]

    result = review.resolve_conflict(
        new_id,
        disposition="SUPERSEDE",
        actor="carol",
        reason="newer authoritative source",
        target_fact_ids=[old_id],
    )
    assert result["applied"] is True
    assert get_fact(new_id)["epistemic_state"] == "Validated"
    assert get_fact(old_id)["epistemic_state"] == "Deprecated"
    edges = get_l3_graph().get_edges(old_id, REL_SUPERSEDED_BY)
    assert [edge["target"] for edge in edges] == [new_id]
    assert edges[0]["props"]["disposition"] == "SUPERSEDE"


def test_supersede_reports_partial_target_race_without_hiding_candidate(monkeypatch):
    old_id, new_id = _conflict_pair("partial")
    real_transition = transition_esm

    def race(fact_id, state):
        if fact_id == old_id and state == "Contradicted":
            return False
        return real_transition(fact_id, state)

    monkeypatch.setattr("core.conflict_decision.transition_esm", race)
    result = review.resolve_conflict(
        new_id,
        disposition="SUPERSEDE",
        actor="dana",
        reason="newer source",
        target_fact_ids=[old_id],
    )

    assert result["approved"] is True
    assert result["applied"] is False
    assert result["partial"] is True
    assert result["partial_target_ids"] == [old_id]
    # Safe residual: explicit coexistence, never silent deletion of the old fact.
    assert get_fact(new_id)["epistemic_state"] == "Validated"
    assert get_fact(old_id)["epistemic_state"] == "Validated"
    event = [
        entry for entry in audit.audit_log()
        if entry["event"] == "review_conflict_supersede"
    ][-1]
    assert event["detail"]["partial_target_ids"] == [old_id]
