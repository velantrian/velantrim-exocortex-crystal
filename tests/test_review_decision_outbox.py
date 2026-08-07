"""Crash-window and replay tests for issue #315 curator decisions."""
from __future__ import annotations

import pytest

from core import audit, review
from core.compliance import restrict_processing
from core.erasure import erase_fact
from core.l3_graph import get_l3_graph, reset_l3_graph
from core.memory import get_fact, store_fact, update_fact
from core.review_decision_store import (
    get_review_decision,
    make_decision_id,
    stage_review_decision,
)
from core.review_projection import project_review_decision


def _pending(fid: str, claim: str = "Neon is a noble gas") -> str:
    store_fact(
        {
            "fact_id": fid,
            "claim": claim,
            "source": "review-outbox-test",
            "confidence": 0.9,
            "epistemic_state": "Observed",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "significance": 0.5,
        }
    )
    return fid


def _validated(fid: str, claim: str) -> str:
    store_fact(
        {
            "fact_id": fid,
            "claim": claim,
            "source": "review-outbox-test",
            "confidence": 0.9,
            "epistemic_state": "Validated",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "significance": 0.5,
        }
    )
    return fid


def test_l3_failure_leaves_durable_decision_and_retryable_projection(monkeypatch):
    fid = _pending("decision:approve-failure")
    graph = get_l3_graph()
    real_merge = graph.merge_fact

    def fail_merge(_payload):
        raise RuntimeError("synthetic L3 outage")

    monkeypatch.setattr(graph, "merge_fact", fail_merge)
    result = review.approve(fid, actor="alice")

    assert result["approved"] is True
    assert result["decision_recorded"] is True
    assert result["projection_status"] == "failed"
    assert result["projection_completed"] is False
    assert get_fact(fid)["epistemic_state"] == "Validated"
    decision = get_review_decision(result["decision_id"])
    assert decision["projection_status"] == "failed"
    assert any(
        event["event"] == "review_approve" and event["fact_id"] == fid
        for event in audit.audit_log()
    )

    monkeypatch.setattr(graph, "merge_fact", real_merge)
    drained = review.drain_projections()
    assert drained["completed"] == 1
    assert get_l3_graph().get_fact(fid) is not None
    assert get_review_decision(result["decision_id"])["projection_status"] == "completed"


def test_pending_projection_survives_graph_reset_restart(monkeypatch):
    fid = _pending("decision:restart")
    graph = get_l3_graph()
    monkeypatch.setattr(
        graph, "merge_fact", lambda _payload: (_ for _ in ()).throw(RuntimeError("down"))
    )
    result = review.approve(fid, actor="alice")
    assert result["projection_status"] == "failed"

    reset_l3_graph()
    drained = review.drain_projections()
    assert drained["completed"] == 1
    assert get_l3_graph().get_fact(fid) is not None


def test_audit_failure_rolls_back_state_and_decision(monkeypatch):
    from core import review_decision_store

    fid = _pending("decision:audit-rollback")
    before = list(audit.audit_log())

    def fail_audit(*_args, **_kwargs):
        raise RuntimeError("synthetic audit failure")

    monkeypatch.setattr(review_decision_store, "_append_audit_event_conn", fail_audit)
    with pytest.raises(RuntimeError, match="audit failure"):
        review.approve(fid, actor="alice")

    assert get_fact(fid)["epistemic_state"] == "Observed"
    assert audit.audit_log() == before
    assert review.projection_report()["counts"]["pending"] == 0


def test_replay_is_idempotent_for_nodes_and_edges():
    candidate = _pending("decision:edge-candidate", "The marker is blue")
    target = _validated("decision:edge-target", "The marker is red")
    fact = get_fact(candidate)
    decision_id = make_decision_id(
        event="review_conflict_coexist",
        fact_id=candidate,
        expected_revision=fact["revision"],
        actor="alice",
        reason="both contexts remain",
        target_ids=(target,),
    )

    staged = stage_review_decision(
        decision_id=decision_id,
        fact_id=candidate,
        expected_revision=fact["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_coexist",
        audit_detail={"actor": "alice", "reason": "both contexts remain"},
        projection_builder=lambda _partial: {
            "kind": "test",
            "participants": [
                {
                    "fact_id": candidate,
                    "required_state": "Validated",
                    "merge": True,
                    "truth_status": "VERIFIED",
                },
                {
                    "fact_id": target,
                    "required_state": "Validated",
                    "merge": False,
                },
            ],
            "edges": [
                {
                    "src": candidate,
                    "rel_type": "CONTRADICTS",
                    "dst": target,
                    "props": {"decision_id": decision_id},
                }
            ],
        },
    )
    assert staged["ok"] is True
    assert project_review_decision(decision_id)["projection_status"] == "completed"
    assert project_review_decision(decision_id)["idempotent"] is True
    edges = get_l3_graph().get_edges(candidate, "CONTRADICTS")
    assert len(edges) == 1


def test_restriction_before_retry_blocks_without_resurrection(monkeypatch):
    fid = _pending("decision:restricted-retry")
    graph = get_l3_graph()
    real_merge = graph.merge_fact
    monkeypatch.setattr(
        graph, "merge_fact", lambda _payload: (_ for _ in ()).throw(RuntimeError("down"))
    )
    result = review.approve(fid, actor="alice")
    assert result["projection_status"] == "failed"

    restrict_processing(fid, reason="dispute")
    monkeypatch.setattr(graph, "merge_fact", real_merge)
    drained = review.drain_projections()
    assert drained["blocked"] == 1
    assert get_l3_graph().get_fact(fid) is None
    assert "restricted" in get_review_decision(result["decision_id"])["last_error"]


def test_erasure_before_retry_blocks_without_resurrection(monkeypatch):
    fid = _pending("decision:erased-retry")
    graph = get_l3_graph()
    real_merge = graph.merge_fact
    monkeypatch.setattr(
        graph, "merge_fact", lambda _payload: (_ for _ in ()).throw(RuntimeError("down"))
    )
    result = review.approve(fid, actor="alice")
    assert result["projection_status"] == "failed"

    erase_fact(fid, reason="gdpr_request")
    monkeypatch.setattr(graph, "merge_fact", real_merge)
    drained = review.drain_projections()
    assert drained["blocked"] == 1
    assert get_l3_graph().get_fact(fid) is None
    assert "erased" in get_review_decision(result["decision_id"])["last_error"]


def test_partial_target_race_is_durable_and_explicit():
    candidate = _pending("decision:partial-candidate", "Version two is current")
    target = _validated("decision:partial-target", "Version one is current")
    candidate_fact = get_fact(candidate)
    target_fact = get_fact(target)
    assert update_fact(target, significance=0.8) is True

    decision_id = make_decision_id(
        event="review_conflict_supersede",
        fact_id=candidate,
        expected_revision=candidate_fact["revision"],
        actor="alice",
        reason="new source",
        target_ids=(target,),
    )
    staged = stage_review_decision(
        decision_id=decision_id,
        fact_id=candidate,
        expected_revision=candidate_fact["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_supersede",
        audit_detail={"actor": "alice", "reason": "new source"},
        projection_builder=lambda partial: {
            "kind": "partial-test",
            "participants": [
                {
                    "fact_id": candidate,
                    "required_state": "Validated",
                    "merge": True,
                    "truth_status": "VERIFIED",
                },
                {
                    "fact_id": target,
                    "required_state": None,
                    "merge": False,
                },
            ],
            "edges": [
                {
                    "src": candidate,
                    "rel_type": "CONTRADICTS",
                    "dst": target,
                    "props": {"partial_supersede": target in partial},
                }
            ],
        },
        target_transitions=(
            {
                "fact_id": target,
                "expected_revision": target_fact["revision"],
                "expected_state": "Validated",
                "path": ("Contradicted", "Deprecated"),
            },
        ),
        allow_partial_targets=True,
    )
    assert staged["ok"] is True
    assert staged["payload"]["partial_target_ids"] == [target]
    assert get_fact(candidate)["epistemic_state"] == "Validated"
    assert get_fact(target)["epistemic_state"] == "Validated"
    assert project_review_decision(decision_id)["projection_status"] == "completed"
    assert get_l3_graph().get_edges(candidate, "CONTRADICTS")


def test_operator_health_is_content_light(monkeypatch):
    claim = "Sensitive claim must never enter operator projection status"
    fid = _pending("decision:health-redaction", claim)
    graph = get_l3_graph()
    monkeypatch.setattr(
        graph, "merge_fact", lambda _payload: (_ for _ in ()).throw(RuntimeError("down"))
    )
    review.approve(fid, actor="alice")

    status = review.projection_report()
    assert status["counts"]["failed"] == 1
    assert claim not in str(status)
    assert "source" not in str(status).lower()


def test_duplicate_stage_returns_existing_record():
    fid = _pending("decision:duplicate")
    fact = get_fact(fid)
    decision_id = make_decision_id(
        event="review_reject",
        fact_id=fid,
        expected_revision=fact["revision"],
        actor="alice",
        reason="duplicate",
    )
    kwargs = dict(
        decision_id=decision_id,
        fact_id=fid,
        expected_revision=fact["revision"],
        expected_state="Observed",
        candidate_path=("Collapsed",),
        event="review_reject",
        audit_detail={"actor": "alice", "reason": "duplicate"},
    )
    first = stage_review_decision(**kwargs)
    second = stage_review_decision(**kwargs)
    assert first["created"] is True
    assert second["created"] is False
    assert second["decision_id"] == decision_id
    assert len([e for e in audit.audit_log() if e["event"] == "review_reject"]) == 1


def test_stage_fails_closed_for_missing_restricted_and_invalid_state():
    missing = stage_review_decision(
        decision_id="review:missing",
        fact_id="missing",
        expected_revision=0,
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_approve",
        audit_detail={"actor": "alice"},
    )
    assert missing["ok"] is False and "no longer exists" in missing["reason"]

    restricted_id = _pending("decision:stage-restricted")
    restrict_processing(restricted_id, reason="dispute")
    restricted = get_fact(restricted_id)
    result = stage_review_decision(
        decision_id="review:restricted",
        fact_id=restricted_id,
        expected_revision=restricted["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_approve",
        audit_detail={"actor": "alice"},
    )
    assert result["ok"] is False and result["reason"] == "RESTRICTED_BY_POLICY"

    invalid_id = _pending("decision:invalid-state")
    invalid = get_fact(invalid_id)
    result = stage_review_decision(
        decision_id="review:invalid-state",
        fact_id=invalid_id,
        expected_revision=invalid["revision"],
        expected_state="Observed",
        candidate_path=("NOT_A_STATE",),
        event="review_approve",
        audit_detail={"actor": "alice"},
    )
    assert result["ok"] is False and "invalid ESM target" in result["reason"]


def test_stage_target_missing_or_restricted_is_not_partial():
    candidate = _pending("decision:target-guard")
    fact = get_fact(candidate)
    missing = stage_review_decision(
        decision_id="review:target-missing",
        fact_id=candidate,
        expected_revision=fact["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_supersede",
        audit_detail={"actor": "alice"},
        target_transitions=(
            {
                "fact_id": "absent-target",
                "expected_revision": 0,
                "expected_state": "Validated",
                "path": ("Contradicted", "Deprecated"),
            },
        ),
        allow_partial_targets=True,
    )
    assert missing["ok"] is False and "no longer exists" in missing["reason"]
    assert get_fact(candidate)["epistemic_state"] == "Observed"

    target = _validated("decision:restricted-target", "Old statement")
    restrict_processing(target, reason="dispute")
    target_fact = get_fact(target)
    restricted = stage_review_decision(
        decision_id="review:target-restricted",
        fact_id=candidate,
        expected_revision=fact["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_supersede",
        audit_detail={"actor": "alice"},
        target_transitions=(
            {
                "fact_id": target,
                "expected_revision": target_fact["revision"],
                "expected_state": "Validated",
                "path": ("Contradicted", "Deprecated"),
            },
        ),
        allow_partial_targets=True,
    )
    assert restricted["ok"] is False and "restricted" in restricted["reason"]


def test_projection_missing_decision_and_state_change_block():
    missing = project_review_decision("review:not-found")
    assert missing["projection_status"] == "missing"

    fid = _pending("decision:state-changed")
    graph = get_l3_graph()
    real_merge = graph.merge_fact
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        graph, "merge_fact", lambda _payload: (_ for _ in ()).throw(RuntimeError("down"))
    )
    result = review.approve(fid, actor="alice")
    monkeypatch.setattr(graph, "merge_fact", real_merge)
    assert update_fact(fid, significance=0.7) is True
    assert project_review_decision(result["decision_id"])["projection_status"] == "completed"
    monkeypatch.undo()


def test_projection_blocks_when_required_state_changes(monkeypatch):
    fid = _pending("decision:required-state")
    graph = get_l3_graph()
    real_merge = graph.merge_fact
    monkeypatch.setattr(
        graph, "merge_fact", lambda _payload: (_ for _ in ()).throw(RuntimeError("down"))
    )
    result = review.approve(fid, actor="alice")
    monkeypatch.setattr(graph, "merge_fact", real_merge)
    from core.memory import transition_esm

    assert transition_esm(fid, "Contradicted") is True
    projected = project_review_decision(result["decision_id"])
    assert projected["projection_status"] == "blocked"
    assert "state changed" in projected["reason"]


def test_projection_preserves_existing_target_truth_status():
    candidate = _pending("decision:preserve-candidate", "New version")
    target = _validated("decision:preserve-target", "Old version")
    graph = get_l3_graph()
    graph.merge_fact({**get_fact(target), "truth_status": "CURATOR_OVERRIDE"})
    fact = get_fact(candidate)
    target_fact = get_fact(target)
    decision_id = make_decision_id(
        event="review_conflict_supersede",
        fact_id=candidate,
        expected_revision=fact["revision"],
        actor="alice",
        reason="replace",
        target_ids=(target,),
    )
    staged = stage_review_decision(
        decision_id=decision_id,
        fact_id=candidate,
        expected_revision=fact["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_supersede",
        audit_detail={"actor": "alice", "reason": "replace"},
        projection_builder=lambda _partial: {
            "participants": [
                {
                    "fact_id": candidate,
                    "required_state": "Validated",
                    "merge": True,
                    "truth_status": "VERIFIED",
                },
                {
                    "fact_id": target,
                    "required_state": "Deprecated",
                    "merge": True,
                    "preserve_truth_status": True,
                },
            ],
            "edges": [],
        },
        target_transitions=(
            {
                "fact_id": target,
                "expected_revision": target_fact["revision"],
                "expected_state": "Validated",
                "path": ("Contradicted", "Deprecated"),
            },
        ),
    )
    assert staged["ok"] is True
    assert project_review_decision(decision_id)["projection_status"] == "completed"
    assert graph.get_fact(target)["truth_status"] == "CURATOR_OVERRIDE"


def test_projection_cli_status_and_drain(capsys):
    from core.review_projection import main

    assert main(["status"]) == 0
    status = capsys.readouterr().out
    assert '"counts"' in status
    assert main(["drain", "--limit", "1"]) == 0
    drained = capsys.readouterr().out
    assert '"processed"' in drained


def test_projection_result_validation_and_completed_noop():
    from core.review_decision_store import mark_projection_result

    with pytest.raises(ValueError, match="unsupported"):
        mark_projection_result("missing", status="pending")
    with pytest.raises(KeyError):
        mark_projection_result("missing", status="failed")

    fid = _pending("decision:completed-noop")
    result = review.reject(fid, actor="alice")
    completed = get_review_decision(result["decision_id"])
    same = mark_projection_result(result["decision_id"], status="completed")
    assert same["attempts"] == completed["attempts"] == 0
