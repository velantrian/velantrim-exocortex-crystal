"""Independent hardening regressions found during PR #319 self-review."""
from __future__ import annotations

import threading

import pytest

from core import audit, review
from core.l3_graph import get_l3_graph
from core.memory import get_fact, store_fact
from core.review_decision_store import stage_review_decision


def _pending(fid: str) -> dict:
    store_fact({
        "fact_id": fid,
        "claim": "A hardening test claim",
        "source": "hardening-test",
        "confidence": 0.9,
        "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
    })
    return get_fact(fid)


def test_direct_journal_rejects_immutable_candidate_and_target():
    with pytest.raises(Exception, match="immutable"):
        stage_review_decision(
            decision_id="review:immutable-candidate",
            fact_id="VALUES_CORE",
            expected_revision=0,
            expected_state="Observed",
            candidate_path=("Validated",),
            event="review_approve",
            audit_detail={"actor": "alice"},
        )

    candidate = _pending("hardening:candidate")
    result = stage_review_decision(
        decision_id="review:immutable-target",
        fact_id=candidate["fact_id"],
        expected_revision=candidate["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_supersede",
        audit_detail={"actor": "alice"},
        target_transitions=(
            {
                "fact_id": "RING_ZERO",
                "expected_revision": 0,
                "expected_state": "Validated",
                "path": ("Contradicted",),
            },
        ),
    )
    assert result["ok"] is False
    assert "immutable" in result["reason"]
    assert get_fact(candidate["fact_id"])["epistemic_state"] == "Observed"


def test_idempotency_key_collision_fails_closed():
    first = _pending("hardening:first")
    second = _pending("hardening:second")
    key = "review:collision"
    result = stage_review_decision(
        decision_id=key,
        fact_id=first["fact_id"],
        expected_revision=first["revision"],
        expected_state="Observed",
        candidate_path=("Collapsed",),
        event="review_reject",
        audit_detail={"actor": "alice"},
    )
    assert result["ok"] is True
    collision = stage_review_decision(
        decision_id=key,
        fact_id=second["fact_id"],
        expected_revision=second["revision"],
        expected_state="Observed",
        candidate_path=("Collapsed",),
        event="review_reject",
        audit_detail={"actor": "alice"},
    )
    assert collision["ok"] is False
    assert collision["reason"] == "decision idempotency key collision"
    assert get_fact(second["fact_id"])["epistemic_state"] == "Observed"


def test_backend_exception_message_is_not_persisted(monkeypatch):
    secret = "claim text must not enter projection health"
    fact = _pending("hardening:redaction")
    graph = get_l3_graph()

    def fail(_payload):
        raise RuntimeError(secret)

    monkeypatch.setattr(graph, "merge_fact", fail)
    result = review.approve(fact["fact_id"], actor="alice")
    assert result["projection_status"] == "failed"
    health = review.projection_report()
    assert secret not in str(health)
    assert "projection_backend_failure" in str(health)


def test_journal_serializes_with_normal_audit_appends():
    # This is a behavioral lock-order smoke test: both operations complete and
    # the final chain remains valid under concurrent start.
    fact = _pending("hardening:audit-lock")
    barrier = threading.Barrier(2)
    failures = []

    def ordinary_event():
        try:
            barrier.wait()
            audit.append_event("hardening_concurrent", None, {"kind": "test"})
        except Exception as exc:  # pragma: no cover - asserted below
            failures.append(exc)

    thread = threading.Thread(target=ordinary_event)
    thread.start()
    barrier.wait()
    result = review.reject(fact["fact_id"], actor="alice")
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert failures == []
    assert result["rejected"] is True
    assert audit.verify_audit_log()["ok"] is True
