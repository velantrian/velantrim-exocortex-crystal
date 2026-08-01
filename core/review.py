# core/review.py
# Velantrim ExoCortex — Curator Review Queue (grant WP2)
#
# Import sessions and dry-run preview make bulk import safer. The curator review
# queue closes the human-in-the-loop: every stored claim that did not reach L3
# remains Observed in L1 and surfaces here for an accountable decision.
#
# Curator actions:
#   approve(fact_id)          → promote a clean ready item;
#   resolve_conflict(...)     → apply an explicit contradiction disposition;
#   reject(fact_id)           → Observed → Collapsed;
#   approve(..., force=True)  → explicit audited override of a blocked gate.
#
# A conflict is never a normal approve. Detection creates an immutable,
# content-free ContradictionReport; a curator must select COEXIST,
# CONTEXTUALIZE or SUPERSEDE with an explicit actor and reason.

import uuid
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from core import audit, contradiction, immune, metrics
from core.conflict_decision import apply_conflict_decision
from core.contradiction_report import ConflictDisposition, ContradictionReport
from core.l3_graph import get_l3_graph
from core.memory import (
    get_all_facts,
    get_fact,
    transition_esm,
    update_fact,
    save_review_session,
    list_review_sessions,
    get_review_session,
)
from core.pipeline import _l3_payload, _truth_status_for, guardian, truth_gate
from core.reconcile import find_conflicts

_PENDING_STATE = "Observed"


# ─── Queue inspection ─────────────────────────────────────────────────────────

_RESTRICTED_STUB = {"restricted": True, "reason": "RESTRICTED_BY_POLICY"}


def _summary(fact: Dict[str, Any]) -> Dict[str, Any]:
    """A compact curator view; restricted content is returned as a stub."""
    if fact.get("restricted"):
        return {"fact_id": fact["fact_id"], **_RESTRICTED_STUB}
    return {
        "fact_id": fact["fact_id"],
        "claim": fact.get("claim"),
        "claim_type": fact.get("claim_type"),
        "source": fact.get("source"),
        "source_status": fact.get("source_status"),
        "confidence": fact.get("confidence"),
        "created_at": fact.get("created_at"),
    }


def _summary_with_diagnosis(fact: Dict[str, Any]) -> Dict[str, Any]:
    """_summary() plus a fresh diagnosis, except for restricted facts."""
    summary = _summary(fact)
    if fact.get("restricted"):
        summary["diagnosis"] = {
            "verdict": "restricted",
            "reason": "RESTRICTED_BY_POLICY",
        }
        return summary
    summary["diagnosis"] = _diagnose(fact)
    return summary


def pending(
    limit: Optional[int] = None,
    claim_type: Optional[str] = None,
    diagnose: bool = False,
) -> List[Dict[str, Any]]:
    """List Observed facts, oldest first, with optional type/limit/diagnosis."""
    items = get_all_facts(_PENDING_STATE)
    if claim_type is not None:
        items = [
            fact
            for fact in items
            if not fact.get("restricted") and fact.get("claim_type") == claim_type
        ]
    items.sort(key=lambda fact: (fact.get("created_at") or "", fact.get("fact_id", "")))
    if limit is not None:
        items = items[:limit]
    if not diagnose:
        return [_summary(fact) for fact in items]
    return [_summary_with_diagnosis(fact) for fact in items]


def _build_contradiction_report(fact: Dict[str, Any]) -> Optional[ContradictionReport]:
    """Return a content-free immutable report for current WORLD_FACT conflicts."""
    if fact.get("claim_type", "WORLD_FACT") != "WORLD_FACT":
        return None
    candidates = find_conflicts(fact.get("claim", ""), fact_id=fact["fact_id"])
    contradictions = [
        candidate
        for candidate in candidates
        if candidate.get("kind") == contradiction.CONTRADICTION
    ]
    if not contradictions:
        return None
    return ContradictionReport.from_candidates(
        candidate_fact_id=fact["fact_id"], candidates=contradictions
    )


def _diagnose(fact: Dict[str, Any]) -> Dict[str, Any]:
    """Re-run live gates and produce blocked/conflict/ready diagnosis."""
    claim = fact.get("claim", "")
    fact_id = fact["fact_id"]

    pre = immune.screen(claim, fact_id=fact_id, check_canon=False)
    if pre["verdict"] == immune.BLOCK:
        return {"verdict": "blocked", "reason": f"Immune: {pre.get('reason', '')}"}

    facts_pack = {"facts": [fact], "query": claim, "total": 1}
    trace = [
        {
            "fact_id": fact_id,
            "source": fact.get("source"),
            "origin": "review",
            "epistemic_state": _PENDING_STATE,
            "confidence": fact.get("confidence"),
        }
    ]
    ok, reason = guardian(facts_pack, trace)
    if ok:
        ok, reason = truth_gate(facts_pack)
    if not ok:
        return {"verdict": "blocked", "reason": reason}

    report = _build_contradiction_report(fact)
    if report is not None:
        return {
            "verdict": "conflict",
            "reason": f"contradicts {len(report.conflicts)} canonical fact(s)",
            "conflicts": list(report.conflict_ids),
            "contradiction_report": report.to_dict(),
            "required_action": "resolve_conflict",
        }
    return {"verdict": "ready", "reason": "passes the gates; awaiting curator approval"}


def review_item(fact_id: str) -> Dict[str, Any]:
    """Full detail for one queued fact with a fresh diagnosis."""
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    return {"found": True, **_summary_with_diagnosis(fact)}


def review_report() -> Dict[str, Any]:
    """Aggregate queue health: total pending and claim-type breakdown."""
    items = get_all_facts(_PENDING_STATE)
    by_type: Dict[str, int] = {}
    for fact in items:
        key = fact.get("claim_type", "UNKNOWN")
        by_type[key] = by_type.get(key, 0) + 1
    return {"pending": len(items), "by_claim_type": by_type}


# ─── Curator decisions (accountable) ──────────────────────────────────────────

_FORCE_REASON_MAX = 500
_CAS_MAX_ATTEMPTS = 3


def approve(
    fact_id: str,
    *,
    actor: Optional[str] = None,
    note: Optional[str] = None,
    force: bool = False,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    """Promote a clean pending fact, or explicitly override a blocked gate.

    A conflict is not accepted here. It remains Observed and returns
    `CONFLICT_DECISION_REQUIRED` plus an immutable ContradictionReport. Call
    resolve_conflict() with an explicit disposition, actor and reason.
    """
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    if fact.get("epistemic_state") != _PENDING_STATE:
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": f"not pending (state={fact.get('epistemic_state')})",
        }
    if fact.get("restricted"):
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "restricted": True,
            "reason": "RESTRICTED_BY_POLICY",
        }

    diagnosis = _diagnose(fact)
    if diagnosis["verdict"] == "conflict":
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": "CONFLICT_DECISION_REQUIRED",
            "diagnosis": diagnosis,
        }

    overridden = False
    if diagnosis["verdict"] == "blocked":
        if not force:
            return {
                "found": True,
                "fact_id": fact_id,
                "approved": False,
                "reason": diagnosis["reason"],
                "diagnosis": diagnosis,
            }
        if not (reason and reason.strip()) or not (actor and actor.strip()):
            return {
                "found": True,
                "fact_id": fact_id,
                "approved": False,
                "reason": "force approval requires a non-empty reason and an explicit actor "
                "(it overrides a blocking diagnosis; no default identity)",
                "diagnosis": diagnosis,
            }
        if len(reason.strip()) > _FORCE_REASON_MAX:
            return {
                "found": True,
                "fact_id": fact_id,
                "approved": False,
                "reason": f"force approval reason exceeds {_FORCE_REASON_MAX} characters",
                "diagnosis": diagnosis,
            }
        overridden = True
    if actor is None or not actor.strip():
        actor = "curator"

    try:
        transitioned = transition_esm(fact_id, "Validated")
    except ValueError:
        transitioned = False
    if not transitioned:
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": "ESM CAS conflict: fact state changed concurrently",
            "diagnosis": diagnosis["verdict"],
        }

    claim_type = fact.get("claim_type", "WORLD_FACT")
    if overridden:
        for _ in range(_CAS_MAX_ATTEMPTS):
            metadata = dict((get_fact(fact_id) or {}).get("metadata") or {})
            metadata.update(
                {
                    "admission_path": "review_force_approve",
                    "override": True,
                    "gate_passed": False,
                    "gate_reason": diagnosis.get("reason"),
                }
            )
            if update_fact(fact_id, metadata=metadata):
                break
        promoted = get_fact(fact_id)
        truth_status = "CURATOR_OVERRIDE"
    else:
        truth_status = _truth_status_for(claim_type, fact.get("source_status"))
        promoted = get_fact(fact_id)
    promoted["truth_status"] = truth_status
    get_l3_graph().merge_fact(_l3_payload(promoted))

    metrics.incr("review.approved")
    if overridden:
        metrics.incr("review.override")
        audit.append_event(
            "review_force_approve",
            fact_id,
            {
                "actor": actor,
                "reason": reason,
                "note": note,
                "diagnosis": diagnosis["verdict"],
                "gate_reason": diagnosis.get("reason"),
            },
        )
        warnings.warn(
            f"Force override: curator '{actor}' approved a blocked fact "
            f"(fact_id={fact_id!r}, diagnosis={diagnosis['verdict']!r}). "
            "This override is recorded in the audit chain.",
            RuntimeWarning,
            stacklevel=2,
        )
    else:
        audit.append_event(
            "review_approve",
            fact_id,
            {
                "actor": actor,
                "note": note,
                "override": False,
                "diagnosis": diagnosis["verdict"],
            },
        )
    return {
        "found": True,
        "fact_id": fact_id,
        "approved": True,
        "override": overridden,
        "epistemic_state": "Validated",
        "truth_status": truth_status,
        "diagnosis": diagnosis["verdict"],
    }


def resolve_conflict(
    fact_id: str,
    *,
    disposition: ConflictDisposition | str,
    actor: Optional[str],
    reason: Optional[str],
    target_fact_ids: Iterable[str] = (),
    expected_report_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve a current contradiction through an explicit curator disposition.

    The report is recomputed immediately before the write. `expected_report_id`
    provides optimistic concurrency: if the conflict set/signals changed since a
    curator viewed it, no decision is applied.
    """
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    if fact.get("epistemic_state") != _PENDING_STATE:
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": f"not pending (state={fact.get('epistemic_state')})",
        }
    if fact.get("restricted"):
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "restricted": True,
            "reason": "RESTRICTED_BY_POLICY",
        }

    diagnosis = _diagnose(fact)
    if diagnosis["verdict"] == "blocked":
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": diagnosis["reason"],
            "diagnosis": diagnosis,
        }
    report = _build_contradiction_report(fact)
    if report is None:
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": "NO_CURRENT_CONTRADICTION",
            "diagnosis": diagnosis,
        }
    if expected_report_id is not None and expected_report_id != report.report_id:
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": "CONTRADICTION_REPORT_CHANGED",
            "report": report.to_dict(),
        }

    result = apply_conflict_decision(
        fact=fact,
        report=report,
        disposition=disposition,
        actor=actor,
        reason=reason,
        target_fact_ids=target_fact_ids,
    )
    return {
        "found": True,
        "fact_id": fact_id,
        "diagnosis": "conflict",
        **result,
    }


def reject(
    fact_id: str,
    *,
    actor: str = "curator",
    reason: str = "curator_rejected",
) -> Dict[str, Any]:
    """Reject an Observed fact: Observed → Collapsed, audited."""
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    if fact.get("epistemic_state") != _PENDING_STATE:
        return {
            "found": True,
            "fact_id": fact_id,
            "rejected": False,
            "reason": f"not pending (state={fact.get('epistemic_state')})",
        }
    if not transition_esm(fact_id, "Collapsed"):
        return {
            "found": True,
            "fact_id": fact_id,
            "rejected": False,
            "reason": "ESM CAS conflict: fact state changed concurrently",
        }
    metrics.incr("review.rejected")
    audit.append_event("review_reject", fact_id, {"actor": actor, "reason": reason})
    return {
        "found": True,
        "fact_id": fact_id,
        "rejected": True,
        "epistemic_state": "Collapsed",
        "reason": reason,
    }


# ─── Resumable review sessions ────────────────────────────────────────────────


def create_session(batch_size: Optional[int] = None) -> Dict[str, Any]:
    """Snapshot the current pending queue into a resumable session."""
    pending_facts = get_all_facts(_PENDING_STATE)
    pending_facts.sort(
        key=lambda fact: (fact.get("created_at") or "", fact.get("fact_id", ""))
    )
    claim_ids = [fact["fact_id"] for fact in pending_facts]
    if batch_size is not None:
        claim_ids = claim_ids[:batch_size]
    now = datetime.now(timezone.utc).isoformat()
    session: Dict[str, Any] = {
        "session_id": str(uuid.uuid4()),
        "status": "pending",
        "batch_size": batch_size,
        "claim_ids": claim_ids,
        "reviewed_ids": [],
        "deferred_ids": [],
        "approved_count": 0,
        "rejected_count": 0,
        "created_at": now,
        "updated_at": now,
    }
    save_review_session(session)
    return session


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    return get_review_session(session_id)


def list_sessions(status: Optional[str] = None) -> List[Dict[str, Any]]:
    return list_review_sessions(status)


def resume_session(session_id: str) -> Dict[str, Any]:
    """Return unresolved Observed items for a session in stable order."""
    session = get_review_session(session_id)
    if session is None:
        return {"found": False, "session_id": session_id}
    if session["status"] == "completed":
        return {
            "found": True,
            "session_id": session_id,
            "status": "completed",
            "pending_items": [],
            "remaining": 0,
        }

    reviewed = set(session["reviewed_ids"])
    unresolved = []
    for fact_id in session["claim_ids"]:
        if fact_id in reviewed:
            continue
        fact = get_fact(fact_id)
        if fact is None or fact.get("epistemic_state") != _PENDING_STATE:
            continue
        unresolved.append(_summary(fact))

    session["status"] = "in_progress"
    save_review_session(session)
    return {
        "found": True,
        "session_id": session_id,
        "status": "in_progress",
        "pending_items": unresolved,
        "remaining": len(unresolved),
    }


def record_session_decision(
    session_id: str, fact_id: str, decision: str
) -> Dict[str, Any]:
    """Record approved/rejected progress after the actual review operation."""
    if decision not in ("approved", "rejected"):
        return {"ok": False, "reason": "decision must be 'approved' or 'rejected'"}
    session = get_review_session(session_id)
    if session is None:
        return {"ok": False, "reason": f"session {session_id!r} not found"}
    if fact_id not in session["reviewed_ids"]:
        session["reviewed_ids"].append(fact_id)
    if decision == "approved":
        session["approved_count"] += 1
    else:
        session["rejected_count"] += 1
    save_review_session(session)
    return {
        "ok": True,
        "session_id": session_id,
        "fact_id": fact_id,
        "decision": decision,
    }


def complete_session(session_id: str) -> Dict[str, Any]:
    session = get_review_session(session_id)
    if session is None:
        return {"ok": False, "reason": f"session {session_id!r} not found"}
    session["status"] = "completed"
    save_review_session(session)
    return {"ok": True, "session_id": session_id, "status": "completed"}


# ─── Decision history (reconstructed from the audit chain) ────────────────────

_DECISION_EVENTS = {
    "review_approve": "approved",
    "review_force_approve": "force_approved",
    "review_reject": "rejected",
    "review_conflict_coexist": "conflict_coexist",
    "review_conflict_contextualize": "conflict_contextualized",
    "review_conflict_supersede": "conflict_superseded",
}


def decisions(
    limit: int = 50, *, include_claim: bool = True
) -> List[Dict[str, Any]]:
    """Curator history, newest first, reconstructed from the audit chain."""
    out: List[Dict[str, Any]] = []
    for entry in reversed(audit.audit_log()):
        decision = _DECISION_EVENTS.get(entry["event"])
        if decision is None:
            continue
        detail = entry["detail"]
        item = {
            "decision": decision,
            "fact_id": entry["fact_id"],
            "ts": entry["ts"],
            "actor": detail.get("actor"),
            "reason": detail.get("reason"),
            "note": detail.get("note"),
            "diagnosis": detail.get("diagnosis"),
        }
        if detail.get("report_id") is not None:
            item.update(
                {
                    "report_id": detail.get("report_id"),
                    "disposition": detail.get("disposition"),
                    "conflict_ids": detail.get("conflict_ids"),
                    "target_ids": detail.get("target_ids"),
                    "partial_target_ids": detail.get("partial_target_ids"),
                }
            )
        if include_claim:
            fact = get_fact(entry["fact_id"]) if entry["fact_id"] else None
            if fact is not None and fact.get("restricted"):
                item["claim"] = None
                item["claim_type"] = None
                item["restricted"] = True
                item["restricted_reason"] = "RESTRICTED_BY_POLICY"
            else:
                item["claim"] = fact.get("claim") if fact else None
                item["claim_type"] = fact.get("claim_type") if fact else None
        out.append(item)
        if len(out) >= limit:
            break
    return out
