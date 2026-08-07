"""Defensive-edge coverage for the crash-consistent review package."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from core import conflict_decision, memory, review, review_decision_store
from core.contradiction_report import ConflictDisposition
from core.review_decision_store import (
    DecisionConflict,
    get_review_decision,
    list_projection_work,
    stage_review_decision,
)
from core.review_projection import (
    ProjectionBlocked,
    _participant_fact,
    project_review_decision,
)


def _fact(fid: str, *, state: str = "Observed") -> dict:
    memory.store_fact(
        {
            "fact_id": fid,
            "claim": f"Defensive edge for {fid}",
            "source": "defensive-edge-test",
            "confidence": 0.9,
            "epistemic_state": state,
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
        }
    )
    return memory.get_fact(fid)


class _Cursor:
    def __init__(self, row):
        self._row = row

    def fetchone(self):
        return self._row


class _SequenceConn:
    def __init__(self, rows):
        self._rows = iter(rows)

    def execute(self, *_args, **_kwargs):
        return _Cursor(next(self._rows))


def test_audit_append_rejects_missing_and_mismatched_checkpoints():
    with pytest.raises(RuntimeError, match="checkpoint missing"):
        review_decision_store._append_audit_event_conn(
            _SequenceConn([{"seq": 1, "entry_hash": "tail"}, None]),
            event="coverage",
            fact_id="fact",
            detail={},
            ts="2026-08-07T00:00:00+00:00",
        )

    with pytest.raises(RuntimeError, match="checkpoint mismatch"):
        review_decision_store._append_audit_event_conn(
            _SequenceConn(
                [
                    {"seq": 1, "entry_hash": "tail"},
                    {"seq": 1, "head_hash": "different"},
                ]
            ),
            event="coverage",
            fact_id="fact",
            detail={},
            ts="2026-08-07T00:00:00+00:00",
        )


def test_decision_validation_rejects_invalid_paths_ids_and_commands():
    with pytest.raises(DecisionConflict, match="invalid ESM target"):
        review_decision_store._validate_path("Observed", ("UNKNOWN",))
    with pytest.raises(DecisionConflict, match="no longer allowed"):
        review_decision_store._validate_path("Collapsed", ("Validated",))
    with pytest.raises(DecisionConflict, match="fact id is invalid"):
        review_decision_store._guard_mutable_fact_id(None, role="candidate")

    with pytest.raises(ValueError, match="decision_id"):
        stage_review_decision(
            decision_id="",
            fact_id="coverage:input",
            expected_revision=0,
            expected_state="Observed",
            candidate_path=(),
            event="review_test",
            audit_detail={},
        )
    with pytest.raises(ValueError, match="event"):
        stage_review_decision(
            decision_id="review:coverage-input",
            fact_id="coverage:input",
            expected_revision=0,
            expected_state="Observed",
            candidate_path=(),
            event="",
            audit_detail={},
        )
    with pytest.raises(ValueError, match="integer"):
        list_projection_work(True)


def test_stage_rejects_candidate_and_target_revision_conflicts():
    candidate = _fact("coverage:revision-candidate")
    result = stage_review_decision(
        decision_id="review:wrong-candidate-revision",
        fact_id=candidate["fact_id"],
        expected_revision=candidate["revision"] + 1,
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_approve",
        audit_detail={},
    )
    assert result["ok"] is False
    assert "revision changed" in result["reason"]

    target = _fact("coverage:revision-target", state="Validated")
    candidate = _fact("coverage:target-candidate")
    result = stage_review_decision(
        decision_id="review:wrong-target-revision",
        fact_id=candidate["fact_id"],
        expected_revision=candidate["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_supersede",
        audit_detail={},
        target_transitions=(
            {
                "fact_id": target["fact_id"],
                "expected_revision": target["revision"] + 1,
                "expected_state": "Validated",
                "path": ("Contradicted",),
            },
        ),
    )
    assert result["ok"] is False
    assert "changed concurrently" in result["reason"]


def test_stage_detects_backend_ignored_candidate_and_target_updates():
    candidate = _fact("coverage:ignored-candidate")
    with memory._db() as conn:
        conn.execute(
            "CREATE TRIGGER ignore_candidate_update BEFORE UPDATE ON facts "
            "WHEN OLD.fact_id = 'coverage:ignored-candidate' "
            "BEGIN SELECT RAISE(IGNORE); END"
        )
    result = stage_review_decision(
        decision_id="review:ignored-candidate",
        fact_id=candidate["fact_id"],
        expected_revision=candidate["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_approve",
        audit_detail={},
    )
    assert result["ok"] is False
    assert "candidate state changed" in result["reason"]

    target = _fact("coverage:ignored-target", state="Validated")
    candidate = _fact("coverage:target-trigger-candidate")
    with memory._db() as conn:
        conn.execute(
            "CREATE TRIGGER ignore_target_update BEFORE UPDATE ON facts "
            "WHEN OLD.fact_id = 'coverage:ignored-target' "
            "BEGIN SELECT RAISE(IGNORE); END"
        )
    result = stage_review_decision(
        decision_id="review:ignored-target",
        fact_id=candidate["fact_id"],
        expected_revision=candidate["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_conflict_supersede",
        audit_detail={},
        target_transitions=(
            {
                "fact_id": target["fact_id"],
                "expected_revision": target["revision"],
                "expected_state": "Validated",
                "path": ("Contradicted",),
            },
        ),
    )
    assert result["ok"] is False
    assert "target" in result["reason"] and "changed concurrently" in result["reason"]
    assert memory.get_fact(candidate["fact_id"])["epistemic_state"] == "Observed"


def test_projection_participant_guards_and_empty_projection_completion():
    with pytest.raises(ProjectionBlocked, match="malformed"):
        _participant_fact({})
    with pytest.raises(ProjectionBlocked, match="immutable"):
        _participant_fact({"fact_id": "VALUES_CORE"})
    with pytest.raises(ProjectionBlocked, match="no longer exists"):
        _participant_fact({"fact_id": "coverage:missing"})

    candidate = _fact("coverage:empty-projection")
    staged = stage_review_decision(
        decision_id="review:empty-projection",
        fact_id=candidate["fact_id"],
        expected_revision=candidate["revision"],
        expected_state="Observed",
        candidate_path=("Collapsed",),
        event="review_reject",
        audit_detail={},
    )
    assert staged["projection_status"] == "completed"
    with memory._db() as conn:
        conn.execute(
            "UPDATE review_decisions SET projection_status = 'pending', completed_at = NULL "
            "WHERE decision_id = ?",
            (staged["decision_id"],),
        )
    projected = project_review_decision(staged["decision_id"])
    assert projected["projection_status"] == "completed"
    assert get_review_decision(staged["decision_id"])["attempts"] == 1


def test_reject_compatibility_seam_and_staging_fail_closed(monkeypatch):
    candidate = _fact("coverage:reject-seam-error")

    def raise_value_error(*_args, **_kwargs):
        raise ValueError("synthetic race")

    monkeypatch.setattr(review, "transition_esm", raise_value_error)
    result = review.reject(candidate["fact_id"], actor="alice")
    assert result["rejected"] is False
    assert "CAS conflict" in result["reason"]

    candidate = _fact("coverage:reject-stage-failure")
    monkeypatch.setattr(review, "transition_esm", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(
        review,
        "stage_review_decision",
        lambda **_kwargs: {"ok": False, "reason": "synthetic staging refusal"},
    )
    result = review.reject(candidate["fact_id"], actor="alice")
    assert result["rejected"] is False
    assert result["reason"] == "synthetic staging refusal"


def _report(candidate_fact_id: str):
    return SimpleNamespace(
        candidate_fact_id=candidate_fact_id,
        report_id="coverage-report",
        conflict_ids=(),
        conflicts=(),
        to_dict=lambda: {"candidate_fact_id": candidate_fact_id},
    )


def test_conflict_decision_handles_vanished_target_and_staging_refusal(monkeypatch):
    candidate = _fact("coverage:conflict-target-vanished")
    monkeypatch.setattr(
        conflict_decision,
        "_preflight_targets",
        lambda *_args, **_kwargs: (("coverage:vanished-target",), None),
    )
    monkeypatch.setattr(conflict_decision, "get_fact", lambda _fact_id: None)
    result = conflict_decision.apply_conflict_decision(
        fact=candidate,
        report=_report(candidate["fact_id"]),
        disposition=ConflictDisposition.SUPERSEDE,
        actor="alice",
        reason="coverage",
        target_fact_ids=("coverage:vanished-target",),
    )
    assert result["applied"] is False
    assert "no longer exists" in result["reason"]

    candidate = _fact("coverage:conflict-stage-refusal")
    monkeypatch.setattr(
        conflict_decision,
        "_preflight_targets",
        lambda *_args, **_kwargs: ((), None),
    )
    monkeypatch.setattr(
        conflict_decision,
        "stage_review_decision",
        lambda **_kwargs: {"ok": False, "reason": "synthetic stage refusal"},
    )
    result = conflict_decision.apply_conflict_decision(
        fact=candidate,
        report=_report(candidate["fact_id"]),
        disposition=ConflictDisposition.COEXIST,
        actor="alice",
        reason="coverage",
    )
    assert result == {"applied": False, "reason": "synthetic stage refusal"}
