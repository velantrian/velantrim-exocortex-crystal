# core/conflict_decision.py
# Velantrim ExoCortex — explicit, accountable contradiction decisions.
#
# This module applies a curator-selected disposition to an already-gated pending
# WORLD_FACT. Detection and decision stay separate: no score chooses a winner.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Optional

from core import audit, metrics
from core.contradiction_report import ConflictDisposition, ContradictionReport
from core.l3_graph import get_l3_graph
from core.memory import get_fact, transition_esm, update_fact
from core.pipeline import _l3_payload, _truth_status_for
from core.reconcile import REL_CONTRADICTS, REL_SUPERSEDED_BY

REL_CONTEXTUALIZES = "CONTEXTUALIZES"
_DECISION_REASON_MAX = 500
_CAS_MAX_ATTEMPTS = 3


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


def _persist_candidate_metadata(fact_id: str, detail: Mapping[str, Any]) -> bool:
    """CAS-retry content-free decision metadata after candidate promotion."""
    for _ in range(_CAS_MAX_ATTEMPTS):
        current = get_fact(fact_id)
        if current is None:
            return False
        metadata = dict(current.get("metadata") or {})
        metadata.update(detail)
        if update_fact(fact_id, metadata=metadata):
            return True
    return False


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
    fact: Mapping[str, Any],
    report: ContradictionReport,
    disposition: ConflictDisposition | str,
    actor: Optional[str],
    reason: Optional[str],
    target_fact_ids: Iterable[str] = (),
) -> dict[str, Any]:
    """Apply one explicit contradiction decision.

    Supported outcomes:
      - COEXIST: admit the pending fact and add explicit CONTRADICTS edges;
      - CONTEXTUALIZE: admit it and add CONTEXTUALIZES edges, preserving both;
      - SUPERSEDE: admit it, then deprecate selected current facts and link
        SUPERSEDED_BY.

    REVIEW_REQUIRED never mutates. The function re-validates actor, reason,
    target membership and current target state. It never chooses a disposition or
    a target from scores/confidence.
    """
    try:
        selected = ConflictDisposition(disposition)
    except ValueError:
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

    # Promote the candidate first. If a later supersede CAS loses a race, the
    # safe residual is explicit coexistence, never silent deletion of the old
    # fact. A partial result is audited and returned rather than hidden.
    try:
        transitioned = transition_esm(fact_id, "Validated")
    except ValueError:
        transitioned = False
    if not transitioned:
        return {
            "applied": False,
            "reason": "ESM CAS conflict: candidate state changed concurrently",
        }

    promoted = get_fact(fact_id)
    if promoted is None:
        return {"applied": False, "reason": "candidate disappeared after transition"}
    truth_status = _truth_status_for(
        promoted.get("claim_type", "WORLD_FACT"), promoted.get("source_status")
    )
    promoted["truth_status"] = truth_status
    graph = get_l3_graph()
    graph.merge_fact(_l3_payload(promoted))

    detail = _decision_metadata(
        report=report,
        disposition=selected,
        actor=actor_value,
        reason=reason_value,
        target_ids=targets,
    )
    metadata_saved = _persist_candidate_metadata(fact_id, detail)

    edge_props = {
        "at": _now(),
        "report_id": report.report_id,
        "disposition": selected.value,
        "actor": actor_value,
    }
    partial_targets: list[str] = []

    if selected is ConflictDisposition.COEXIST:
        for ref in report.conflicts:
            graph.add_edge(fact_id, REL_CONTRADICTS, ref.fact_id, edge_props)
    elif selected is ConflictDisposition.CONTEXTUALIZE:
        for ref in report.conflicts:
            graph.add_edge(fact_id, REL_CONTEXTUALIZES, ref.fact_id, edge_props)
    else:  # SUPERSEDE
        for target_id in targets:
            try:
                contradicted = transition_esm(target_id, "Contradicted")
                deprecated = contradicted and transition_esm(target_id, "Deprecated")
            except ValueError:
                deprecated = False
            if not deprecated:
                partial_targets.append(target_id)
                continue
            old_l1 = get_fact(target_id)
            old_l3 = graph.get_fact(target_id) or {}
            if old_l1 is not None:
                old_payload = dict(old_l3)
                old_payload.update(_l3_payload(old_l1))
                # Preserve the prior L3 truth-status label for historical
                # inspection while the ESM state makes strict grounding fail.
                if "truth_status" in old_l3:
                    old_payload["truth_status"] = old_l3["truth_status"]
                graph.merge_fact(old_payload)
            graph.add_edge(target_id, REL_SUPERSEDED_BY, fact_id, edge_props)

    event = f"review_conflict_{selected.value.lower()}"
    audit_detail = {
        "actor": actor_value,
        "reason": reason_value,
        "report_id": report.report_id,
        "disposition": selected.value,
        "conflict_ids": list(report.conflict_ids),
        "target_ids": list(targets),
        "metadata_saved": metadata_saved,
        "partial_target_ids": partial_targets,
    }
    audit.append_event(event, fact_id, audit_detail)
    metrics.incr("review.approved")
    metrics.incr("review.conflict_resolved")
    metrics.incr(f"review.conflict.{selected.value.lower()}")

    return {
        "applied": not partial_targets,
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
        "metadata_saved": metadata_saved,
    }


__all__ = ["REL_CONTEXTUALIZES", "apply_conflict_decision"]
