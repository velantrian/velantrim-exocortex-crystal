"""Tests for immutable contradiction reports and explicit review decisions."""

from dataclasses import FrozenInstanceError

import pytest

from core import audit, review
from core.conflict_decision import REL_CONTEXTUALIZES, apply_conflict_decision
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


def _report(candidate_id: str, old_id: str) -> ContradictionReport:
    return ContradictionReport.from_candidates(
        candidate_fact_id=candidate_id,
        candidates=[
            {
                "fact_id": old_id,
                "similarity": 0.9,
                "kind": CONTRADICTION,
                "signal": "negation",
            }
        ],
    )


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


def test_reference_normalization_and_validation():
    malformed = ConflictReference.from_candidate(
        {
            "fact_id": "old",
            "kind": CONTRADICTION,
            "signal": ["bad"],
            "similarity": float("inf"),
        }
    )
    assert malformed.signal is None
    assert malformed.similarity == 0.0
    assert malformed.to_dict()["fact_id"] == "old"

    bool_score = ConflictReference.from_candidate(
        {
            "fact_id": "old-bool",
            "kind": CONTRADICTION,
            "similarity": True,
        }
    )
    assert bool_score.similarity == 0.0

    with pytest.raises(TypeError, match="mapping"):
        ConflictReference.from_candidate([])
    with pytest.raises(ValueError, match="fact_id"):
        ConflictReference(fact_id=" ", kind=CONTRADICTION, signal=None, similarity=0.1)
    with pytest.raises(ValueError, match="kind"):
        ConflictReference(fact_id="old", kind=" ", signal=None, similarity=0.1)
    with pytest.raises(TypeError, match="signal"):
        ConflictReference(fact_id="old", kind=CONTRADICTION, signal=[], similarity=0.1)
    with pytest.raises(TypeError, match="numeric"):
        ConflictReference(fact_id="old", kind=CONTRADICTION, signal=None, similarity="0.1")
    with pytest.raises(ValueError, match="finite"):
        ConflictReference(fact_id="old", kind=CONTRADICTION, signal=None, similarity=float("nan"))


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
    with pytest.raises(ValueError, match="at least one"):
        ContradictionReport.from_candidates(
            candidate_fact_id="new",
            candidates=[{"fact_id": "new", "kind": CONTRADICTION}],
        )
    with pytest.raises(ValueError, match="report_id"):
        ContradictionReport(report_id=" ", candidate_fact_id="new", conflicts=(ref,))
    with pytest.raises(ValueError, match="candidate_fact_id"):
        ContradictionReport(report_id="ctr:x", candidate_fact_id=" ", conflicts=(ref,))
    with pytest.raises(TypeError, match="immutable tuple"):
        ContradictionReport(report_id="ctr:x", candidate_fact_id="new", conflicts=[ref])
    with pytest.raises(ValueError, match="at least one"):
        ContradictionReport(report_id="ctr:x", candidate_fact_id="new", conflicts=())
    with pytest.raises(ValueError, match="itself"):
        ContradictionReport(
            report_id="ctr:self",
            candidate_fact_id="new",
            conflicts=(
                ConflictReference(
                    fact_id="new", kind=CONTRADICTION, signal=None, similarity=1.0
                ),
            ),
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
        {"disposition": None, "actor": "alice", "reason": "why"},
        {"disposition": "COEXIST", "actor": "alice", "reason": "x" * 501},
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


def test_apply_contract_rejects_mismatch_state_restriction_and_target_errors(monkeypatch):
    old_id, new_id = _conflict_pair("direct")
    fact = get_fact(new_id)
    report = _report(new_id, old_id)

    mismatch = apply_conflict_decision(
        fact={**fact, "fact_id": "other"},
        report=report,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert mismatch["reason"] == "report candidate does not match fact"

    restricted = apply_conflict_decision(
        fact={**fact, "restricted": True},
        report=report,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert restricted["reason"] == "RESTRICTED_BY_POLICY"

    not_pending = apply_conflict_decision(
        fact={**fact, "epistemic_state": "Validated"},
        report=report,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert "not pending" in not_pending["reason"]

    targets_not_allowed = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition="COEXIST",
        actor="alice",
        reason="why",
        target_fact_ids=[old_id],
    )
    assert "does not accept" in targets_not_allowed["reason"]

    invalid_target = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition="SUPERSEDE",
        actor="alice",
        reason="why",
        target_fact_ids=[" "],
    )
    assert "non-blank" in invalid_target["reason"]

    monkeypatch.setattr("core.conflict_decision.get_fact", lambda fid: None if fid == old_id else fact)
    missing_target = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition="SUPERSEDE",
        actor="alice",
        reason="why",
        target_fact_ids=[old_id],
    )
    assert "no longer exists" in missing_target["reason"]


def test_apply_contract_rejects_restricted_or_nonvalidated_target(monkeypatch):
    old_id, new_id = _conflict_pair("target-state")
    fact = get_fact(new_id)
    report = _report(new_id, old_id)
    real_get = get_fact

    def restricted_get(fid):
        value = real_get(fid)
        if fid == old_id:
            return {**value, "restricted": True}
        return value

    monkeypatch.setattr("core.conflict_decision.get_fact", restricted_get)
    restricted = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition="SUPERSEDE",
        actor="alice",
        reason="why",
        target_fact_ids=[old_id],
    )
    assert "restricted" in restricted["reason"]

    def observed_get(fid):
        value = real_get(fid)
        if fid == old_id:
            return {**value, "epistemic_state": "Observed"}
        return value

    monkeypatch.setattr("core.conflict_decision.get_fact", observed_get)
    observed = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition="SUPERSEDE",
        actor="alice",
        reason="why",
        target_fact_ids=[old_id],
    )
    assert "no longer Validated" in observed["reason"]


def test_apply_contract_handles_candidate_transition_failures(monkeypatch):
    old_id, new_id = _conflict_pair("candidate-race")
    fact = get_fact(new_id)
    report = _report(new_id, old_id)

    monkeypatch.setattr(
        "core.conflict_decision.transition_esm",
        lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("race")),
    )
    raised = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert "CAS conflict" in raised["reason"]

    monkeypatch.setattr("core.conflict_decision.transition_esm", lambda *args, **kwargs: True)
    monkeypatch.setattr("core.conflict_decision.get_fact", lambda *args, **kwargs: None)
    disappeared = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert "disappeared" in disappeared["reason"]


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


def test_candidate_metadata_persistence_retries_and_reports_failure(monkeypatch):
    old_id, new_id = _conflict_pair("metadata-retry")
    real_update = __import__("core.conflict_decision", fromlist=["update_fact"]).update_fact
    calls = {"n": 0}

    def flaky(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return False
        return real_update(*args, **kwargs)

    monkeypatch.setattr("core.conflict_decision.update_fact", flaky)
    result = review.resolve_conflict(
        new_id,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert result["metadata_saved"] is True
    assert calls["n"] == 2
    metadata = get_fact(new_id)["metadata"]
    assert metadata["contradiction_report_id"] == result["report_id"]
    assert metadata["conflict_ids"] == [old_id]

    old2, new2 = _conflict_pair("metadata-fail")
    monkeypatch.setattr("core.conflict_decision.update_fact", lambda *args, **kwargs: False)
    result2 = review.resolve_conflict(
        new2,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert result2["metadata_saved"] is False
    assert old2 in result2["conflict_ids"]


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
    residual = get_l3_graph().get_edges(new_id, REL_CONTRADICTS)
    assert [edge["target"] for edge in residual] == [old_id]
    assert residual[0]["props"]["partial_supersede"] is True
    event = [
        entry for entry in audit.audit_log()
        if entry["event"] == "review_conflict_supersede"
    ][-1]
    assert event["detail"]["partial_target_ids"] == [old_id]


def test_review_resolve_conflict_outer_fail_closed_paths(monkeypatch):
    assert review.resolve_conflict(
        "missing",
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )["found"] is False

    ready = _validated("outer:validated", "Mercury is a planet")
    nonpending = review.resolve_conflict(
        ready,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert "not pending" in nonpending["reason"]

    pending_id = _pending("outer:restricted", "A restricted pending claim")
    real_get = get_fact

    def restricted_get(fid):
        value = real_get(fid)
        return {**value, "restricted": True} if fid == pending_id else value

    monkeypatch.setattr(review, "get_fact", restricted_get)
    restricted = review.resolve_conflict(
        pending_id,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert restricted["reason"] == "RESTRICTED_BY_POLICY"

    monkeypatch.setattr(review, "get_fact", real_get)
    blocked_id = _pending("outer:blocked", "I feel uncertain about tomorrow")
    blocked = review.resolve_conflict(
        blocked_id,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert blocked["approved"] is False
    assert blocked["diagnosis"]["verdict"] in {"blocked", "ready"}

    clean_id = _pending("outer:clean", "Helium is a noble gas")
    no_conflict = review.resolve_conflict(
        clean_id,
        disposition="COEXIST",
        actor="alice",
        reason="why",
    )
    assert no_conflict["reason"] == "NO_CURRENT_CONTRADICTION"
