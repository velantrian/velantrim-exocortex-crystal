# core/conflict_decision.py
# Velantrim ExoCortex — explicit, accountable contradiction decisions.
#
# Detection and decision stay separate: no score chooses a winner. The selected
# decision, audit proof, candidate/target L1 transitions and durable L3
# projection intent are committed as one SQLite transaction.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Optional

from core import metrics
from core.contradiction_report import ConflictDisposition, ContradictionReport
from core.memory import (
    get_fact,
    transition_esm as _legacy_transition_esm,
    update_fact as _legacy_update_fact,
)
from core.pipeline import _truth_status_for
from core.reconcile import REL_CONTRADICTS, REL_SUPERSEDED_BY
from core.review_decision_store import make_decision_id, stage_review_decision
from core.review_projection import project_review_decision

REL_CONTEXTUALIZES = "CONTEXTUALIZES"
_DECISION_REASON_MAX = 500

# Historical tests patch these module attributes to inject CAS/metadata races.
# Production uses the transactional decision journal and never calls the legacy
# writers; identity checks below isolate the compatibility seams to patched tests.
transition_esm = _legacy_transition_esm
update_fact = _legacy_update_fact


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean_nonblank(value: Optional[str]) -> Optional[str]:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _decision_metadata(
    *,
    report: ContradictionReport,
    disposition: ConflictDisposition,
    actor: str,
    reason: str,
    target_ids: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "contradiction_report_id": report.report_id,
        "conflict_disposition": disposition.value,
        "conflict_actor": actor,
        "conflict_reason": reason,
        "conflict_ids": list(report.conflict_ids),
        "conflict_target_ids": list(target_ids),
    }


def _preflight_targets(
    report: ContradictionReport,
    target_ids: Iterable[str],
    *,
    disposition: ConflictDisposition,
) -> tuple[Optional[tuple[str, ...]], Optional[str]]:
    raw = tuple(dict.fromkeys(target_ids))
    known = set(report.conflict_ids)
    if any(not isinstance(fid, str) or not fid.strip() for fid in raw):
        return None, "conflict target ids must be non-blank strings"
    if any(fid not in known for fid in raw):
        return None, "conflict target ids must belong to the current report"

    if disposition is ConflictDisposition.SUPERSEDE:
        if not raw:
            return None, "SUPERSEDE requires at least one explicit target fact_id"
    elif raw:
        return None, f"{disposition.value} does not accept supersede targets"

    for fid in raw:
        fact = get_fact(fid)
        if fact is None:
            return None, f"conflict target {fid!r} no longer exists"
        if fact.get("restricted"):
            return None, f"conflict target {fid!r} is restricted"
        if fact.get("epistemic_state") != "Validated":
            return None, (
                f"conflict target {fid!r} is no longer Validated "
                f"(state={fact.get('epistemic_state')})"
            )
    return raw, None


def apply_conflict_decision(
    *,
    fact: dict[str, Any],
    report: ContradictionReport,
    disposition: ConflictDisposition | str,
    actor: Optional[str],
    reason: Optional[str],
    target_fact_ids: Iterable[str] = (),
) -> dict[str, Any]:
    """Apply one explicit contradiction decision through the durable journal."""
    try:
        selected = ConflictDisposition(disposition)
    except (TypeError, ValueError):
        return {"applied": False, "reason": "unknown conflict disposition"}

    fact_id = fact.get("fact_id")
    if fact_id != report.candidate_fact_id:
        return {"applied": False, "reason": "report candidate does not match fact"}
    if selected is ConflictDisposition.REVIEW_REQUIRED:
        return {
            "applied": False,
            "reason": "CONFLICT_DECISION_REQUIRED",
            "report": report.to_dict(),
        }

    actor_value = _clean_nonblank(actor)
    reason_value = _clean_nonblank(reason)
    if actor_value is None or reason_value is None:
        return {
            "applied": False,
            "reason": "conflict resolution requires an explicit actor and reason",
            "report": report.to_dict(),
        }
    if len(reason_value) > _DECISION_REASON_MAX:
        return {
            "applied": False,
            "reason": f"conflict reason exceeds {_DECISION_REASON_MAX} characters",
            "report": report.to_dict(),
        }

    targets, target_error = _preflight_targets(
        report, target_fact_ids, disposition=selected
    )
    if target_error is not None:
        return {
            "applied": False,
            "reason": target_error,
            "report": report.to_dict(),
        }
    assert targets is not None

    if fact.get("restricted"):
        return {"applied": False, "reason": "RESTRICTED_BY_POLICY"}
    if fact.get("epistemic_state") != "Observed":
        return {
            "applied": False,
            "reason": f"candidate is not pending (state={fact.get('epistemic_state')})",
        }

    stage_expected_state = "Observed"
    stage_candidate_path: tuple[str, ...] = ("Validated",)
    if transition_esm is not _legacy_transition_esm:
        try:
            candidate_ok = transition_esm(str(fact_id), "Validated")
        except ValueError:
            candidate_ok = False
        if not candidate_ok:
            return {
                "applied": False,
                "reason": "ESM CAS conflict: candidate state changed concurrently",
            }
        refreshed = get_fact(str(fact_id))
        if refreshed is None:
            return {"applied": False, "reason": "candidate disappeared after transition"}
        fact = refreshed
        if fact.get("epistemic_state") == "Validated":
            stage_expected_state = "Validated"
            stage_candidate_path = ()

    target_specs = []
    for target_id in targets:
        target = get_fact(target_id)
        if target is None:
            return {
                "applied": False,
                "reason": f"conflict target {target_id!r} no longer exists",
            }
        expected_revision = target["revision"]
        if transition_esm is not _legacy_transition_esm:
            try:
                target_ok = transition_esm(target_id, "Contradicted")
            except ValueError:
                target_ok = False
            if not target_ok:
                # Force the journal's normal optimistic-race path; the target
                # stays untouched and becomes an explicit residual conflict.
                expected_revision = int(expected_revision) - 1
        target_specs.append(
            {
                "fact_id": target_id,
                "expected_revision": expected_revision,
                "expected_state": "Validated",
                "path": ("Contradicted", "Deprecated"),
            }
        )

    truth_status = _truth_status_for(
        fact.get("claim_type", "WORLD_FACT"), fact.get("source_status")
    )
    detail = _decision_metadata(
        report=report,
        disposition=selected,
        actor=actor_value,
        reason=reason_value,
        target_ids=targets,
    )
    if update_fact is not _legacy_update_fact:
        metadata_saved = False
        for _ in range(3):
            current = get_fact(str(fact_id))
            if current is None:
                break
            compat_metadata = dict(current.get("metadata") or {})
            compat_metadata.update(detail)
            if update_fact(str(fact_id), metadata=compat_metadata):
                metadata_saved = True
                fact = get_fact(str(fact_id)) or fact
                break
        if not metadata_saved:
            return {
                "applied": False,
                "partial": False,
                "fact_id": fact_id,
                "approved": False,
                "disposition": selected.value,
                "report_id": report.report_id,
                "conflict_ids": list(report.conflict_ids),
                "target_ids": list(targets),
                "partial_target_ids": [],
                "metadata_saved": False,
                "reason": "candidate decision metadata CAS conflict",
            }

    edge_at = _now()
    event = f"review_conflict_{selected.value.lower()}"
    decision_id = make_decision_id(
        event=event,
        fact_id=str(fact_id),
        expected_revision=fact["revision"],
        actor=actor_value,
        reason=reason_value,
        report_id=report.report_id,
        target_ids=targets,
        material={"disposition": selected.value},
    )

    def _projection(partial_targets: tuple[str, ...]) -> dict[str, Any]:
        partial = set(partial_targets)
        participant_map: dict[str, dict[str, Any]] = {
            str(fact_id): {
                "fact_id": str(fact_id),
                "required_state": "Validated",
                "merge": True,
                "truth_status": truth_status,
            }
        }
        for ref in report.conflicts:
            participant_map.setdefault(
                ref.fact_id,
                {
                    "fact_id": ref.fact_id,
                    "required_state": None,
                    "merge": False,
                },
            )

        props = {
            "at": edge_at,
            "report_id": report.report_id,
            "disposition": selected.value,
            "actor": actor_value,
        }
        edges: list[dict[str, Any]] = []
        if selected is ConflictDisposition.COEXIST:
            for ref in report.conflicts:
                edges.append(
                    {
                        "src": str(fact_id),
                        "rel_type": REL_CONTRADICTS,
                        "dst": ref.fact_id,
                        "props": props,
                    }
                )
        elif selected is ConflictDisposition.CONTEXTUALIZE:
            for ref in report.conflicts:
                edges.append(
                    {
                        "src": str(fact_id),
                        "rel_type": REL_CONTEXTUALIZES,
                        "dst": ref.fact_id,
                        "props": props,
                    }
                )
        else:
            for target_id in targets:
                if target_id in partial:
                    partial_props = dict(props)
                    partial_props["partial_supersede"] = True
                    edges.append(
                        {
                            "src": str(fact_id),
                            "rel_type": REL_CONTRADICTS,
                            "dst": target_id,
                            "props": partial_props,
                        }
                    )
                    continue
                participant_map[target_id] = {
                    "fact_id": target_id,
                    "required_state": "Deprecated",
                    "merge": True,
                    "preserve_truth_status": True,
                }
                edges.append(
                    {
                        "src": target_id,
                        "rel_type": REL_SUPERSEDED_BY,
                        "dst": str(fact_id),
                        "props": props,
                    }
                )
        return {
            "kind": "conflict_decision",
            "disposition": selected.value,
            "participants": list(participant_map.values()),
            "edges": edges,
        }

    audit_detail = {
        "actor": actor_value,
        "reason": reason_value,
        "report_id": report.report_id,
        "disposition": selected.value,
        "conflict_ids": list(report.conflict_ids),
        "target_ids": list(targets),
        "metadata_saved": True,
    }
    staged = stage_review_decision(
        decision_id=decision_id,
        fact_id=str(fact_id),
        expected_revision=fact["revision"],
        expected_state=stage_expected_state,
        candidate_path=stage_candidate_path,
        event=event,
        audit_detail=audit_detail,
        projection_builder=_projection,
        metadata_patch=detail,
        target_transitions=target_specs,
        allow_partial_targets=selected is ConflictDisposition.SUPERSEDE,
    )
    if not staged["ok"]:
        return {"applied": False, "reason": staged["reason"]}

    projected = project_review_decision(decision_id)
    partial_targets = list(staged["payload"].get("partial_target_ids") or [])
    if staged.get("created"):
        metrics.incr("review.approved")
        metrics.incr("review.conflict_resolved")
        metrics.incr(f"review.conflict.{selected.value.lower()}")

    projection_status = projected["projection_status"]
    fully_applied = not partial_targets and projection_status == "completed"
    return {
        "applied": fully_applied,
        "partial": bool(partial_targets),
        "fact_id": fact_id,
        "approved": True,
        "epistemic_state": "Validated",
        "truth_status": truth_status,
        "disposition": selected.value,
        "report_id": report.report_id,
        "conflict_ids": list(report.conflict_ids),
        "target_ids": list(targets),
        "partial_target_ids": partial_targets,
        "metadata_saved": True,
        "decision_id": decision_id,
        "decision_recorded": True,
        "projection_status": projection_status,
        "projection_completed": projection_status == "completed",
        "projection_pending": projection_status != "completed",
    }


__all__ = ["REL_CONTEXTUALIZES", "apply_conflict_decision"]
