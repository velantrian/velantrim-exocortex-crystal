# core/review.py
# Velantrim ExoCortex — Curator Review Queue (grant WP2)
#
# Import sessions and dry-run preview make bulk import safer. The curator review
# queue closes the human-in-the-loop: every stored claim that did not reach L3
# remains Observed in L1 and surfaces here for an accountable decision.
#
# Curator decisions are committed through a SQLite decision journal. L1 state,
# content-light audit proof and durable L3 projection intent share one
# transaction; the physically separate graph is updated idempotently afterwards.

import uuid
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from core import audit, contradiction, immune, metrics
from core.conflict_decision import apply_conflict_decision
from core.contradiction_report import ConflictDisposition, ContradictionReport
from core.memory import (
    get_all_facts,
    get_fact,
    transition_esm as _legacy_transition_esm,
    update_fact as _legacy_update_fact,
    save_review_session,
    list_review_sessions,
    get_review_session,
)
from core.pipeline import _truth_status_for, guardian, truth_gate
from core.reconcile import find_conflicts
from core.review_decision_store import make_decision_id, stage_review_decision
from core.review_projection import (
    drain_review_projections,
    project_review_decision,
    review_projection_health,
)

_PENDING_STATE = "Observed"

# Backward-compatible failure-injection seams used by the historical test suite.
# Production calls never invoke these legacy primitives: the identity checks below
# keep all real state changes inside stage_review_decision().
transition_esm = _legacy_transition_esm
update_fact = _legacy_update_fact


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
    """Aggregate queue and durable projection health without claim leakage."""
    items = get_all_facts(_PENDING_STATE)
    by_type: Dict[str, int] = {}
    for fact in items:
        key = fact.get("claim_type", "UNKNOWN")
        by_type[key] = by_type.get(key, 0) + 1
    return {
        "pending": len(items),
        "by_claim_type": by_type,
        "decision_projection": review_projection_health(),
    }


def projection_report() -> Dict[str, Any]:
    """Content-light status for pending, failed or blocked L3 projections."""
    return review_projection_health()


def drain_projections(limit: int = 100) -> Dict[str, Any]:
    """Retry durable curator projections in deterministic order."""
    return drain_review_projections(limit=limit)


# ─── Curator decisions (accountable) ──────────────────────────────────────────

_FORCE_REASON_MAX = 500


def approve(
    fact_id: str,
    *,
    actor: Optional[str] = None,
    note: Optional[str] = None,
    force: bool = False,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    """Promote a clean pending fact, or explicitly override a blocked gate.

    The authoritative decision, audit entry and L3 projection intent are
    committed atomically in SQLite. A graph backend failure therefore returns a
    durable ``projection_status`` rather than losing the decision or pretending
    that all physical effects completed.
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

    actor_value = actor.strip() if isinstance(actor, str) and actor.strip() else "curator"
    reason_value = reason.strip() if isinstance(reason, str) and reason.strip() else None
    claim_type = fact.get("claim_type", "WORLD_FACT")
    truth_status = (
        "CURATOR_OVERRIDE"
        if overridden
        else _truth_status_for(claim_type, fact.get("source_status"))
    )
    event = "review_force_approve" if overridden else "review_approve"
    audit_detail: Dict[str, Any]
    metadata_patch: Dict[str, Any] = {}
    if overridden:
        metadata_patch = {
            "admission_path": "review_force_approve",
            "override": True,
            "gate_passed": False,
            "gate_reason": diagnosis.get("reason"),
        }
        audit_detail = {
            "actor": actor_value,
            "reason": reason_value,
            "note": note,
            "diagnosis": diagnosis["verdict"],
            "gate_reason": diagnosis.get("reason"),
        }
    else:
        audit_detail = {
            "actor": actor_value,
            "note": note,
            "override": False,
            "diagnosis": diagnosis["verdict"],
        }

    # Preserve historical monkeypatch-based failure injection without calling
    # the old non-atomic writer in production. A patched test seam may mutate
    # metadata; refresh the expected revision before staging the real decision.
    if overridden and update_fact is not _legacy_update_fact:
        for _ in range(3):
            current = get_fact(fact_id) or {}
            compat_metadata = dict(current.get("metadata") or {})
            compat_metadata.update(metadata_patch)
            if update_fact(fact_id, metadata=compat_metadata):
                break
        fact = get_fact(fact_id) or fact

    decision_id = make_decision_id(
        event=event,
        fact_id=fact_id,
        expected_revision=fact["revision"],
        actor=actor_value,
        reason=reason_value,
        material={"note": note, "truth_status": truth_status},
    )

    def _projection(_partial: tuple[str, ...]) -> Dict[str, Any]:
        return {
            "kind": "approve",
            "participants": [
                {
                    "fact_id": fact_id,
                    "required_state": "Validated",
                    "merge": True,
                    "truth_status": truth_status,
                }
            ],
            "edges": [],
        }

    staged = stage_review_decision(
        decision_id=decision_id,
        fact_id=fact_id,
        expected_revision=fact["revision"],
        expected_state=_PENDING_STATE,
        candidate_path=("Validated",),
        event=event,
        audit_detail=audit_detail,
        projection_builder=_projection,
        metadata_patch=metadata_patch,
    )
    if not staged["ok"]:
        return {
            "found": True,
            "fact_id": fact_id,
            "approved": False,
            "reason": staged["reason"],
            "diagnosis": diagnosis["verdict"],
        }

    projected = project_review_decision(decision_id)
    if staged.get("created"):
        metrics.incr("review.approved")
        if overridden:
            metrics.incr("review.override")

    if overridden:
        warnings.warn(
            f"Force override: curator '{actor_value}' approved a blocked fact "
            f"(fact_id={fact_id!r}, diagnosis={diagnosis['verdict']!r}). "
            "This override is recorded in the audit chain.",
            RuntimeWarning,
            stacklevel=2,
        )

    projection_status = projected["projection_status"]
    return {
        "found": True,
        "fact_id": fact_id,
        "approved": True,
        "override": overridden,
        "epistemic_state": "Validated",
        "truth_status": truth_status,
        "diagnosis": diagnosis["verdict"],
        "decision_id": decision_id,
        "decision_recorded": True,
        "projection_status": projection_status,
        "projection_completed": projection_status == "completed",
        "projection_pending": projection_status != "completed",
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
    """Resolve a current contradiction through an explicit curator disposition."""
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
    """Reject an Observed fact with atomic state and audit persistence."""
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

    actor_value = actor.strip() if isinstance(actor, str) and actor.strip() else "curator"
    if transition_esm is not _legacy_transition_esm:
        try:
            seam_ok = transition_esm(fact_id, "Collapsed")
        except ValueError:
            seam_ok = False
        if not seam_ok:
            return {
                "found": True,
                "fact_id": fact_id,
                "rejected": False,
                "reason": "ESM CAS conflict: fact state changed concurrently",
            }
        # A patched seam may have changed persisted state; fail closed through
        # the normal precondition below rather than staging from a stale row.
        fact = get_fact(fact_id) or fact

    decision_id = make_decision_id(
        event="review_reject",
        fact_id=fact_id,
        expected_revision=fact["revision"],
        actor=actor_value,
        reason=reason,
    )
    staged = stage_review_decision(
        decision_id=decision_id,
        fact_id=fact_id,
        expected_revision=fact["revision"],
        expected_state=_PENDING_STATE,
        candidate_path=("Collapsed",),
        event="review_reject",
        audit_detail={"actor": actor_value, "reason": reason},
    )
    if not staged["ok"]:
        return {
            "found": True,
            "fact_id": fact_id,
            "rejected": False,
            "reason": staged["reason"],
        }
    if staged.get("created"):
        metrics.incr("review.rejected")
    return {
        "found": True,
        "fact_id": fact_id,
        "rejected": True,
        "epistemic_state": "Collapsed",
        "reason": reason,
        "decision_id": decision_id,
        "decision_recorded": True,
        "projection_status": "completed",
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
            "decision_id": detail.get("decision_id"),
            "projection_status": detail.get("projection_status"),
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
