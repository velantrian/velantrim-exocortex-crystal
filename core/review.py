# core/review.py
# Velantrim ExoCortex — Curator Review Queue (grant WP2)
#
# Import sessions and the dry-run preview (core/imports.py) make a bulk import
# SAFE. The curator review queue closes the human-in-the-loop: every claim that
# was stored but did NOT reach the canon — blocked by a gate, or quarantined
# pending a decision — surfaces here for a librarian to approve or reject.
#
# What "the queue" is, concretely:
#   A fact that passes the gates is transitioned Observed → Validated and merged
#   into the L3 canon. A fact that is blocked stays `Observed` in L1 (pending),
#   never reaching the canon. So the review queue IS the set of Observed facts —
#   no new table, no parallel state machine; it reads the existing ESM.
#
# Curator actions (accountable):
#   approve(fact_id) → re-run the gates; on pass, promote Observed → Validated and
#     merge into L3. A still-blocked item can be promoted only with force=True
#     (an explicit, recorded curator override — truth-first: a human, not a
#     heuristic, overrides the gate, and the override is logged).
#   reject(fact_id)  → transition Observed → Collapsed (logically removed).
#
# Every approve/reject appends a content-free entry to the tamper-evident audit
# chain (core/audit.py), so the canon's human edits are as accountable as its
# erasures (GDPR Art. 5(2) / 24 / 30).

import uuid
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from core import audit, contradiction, immune, metrics
from core.l3_graph import get_l3_graph
from core.memory import (
    get_all_facts, get_fact, transition_esm, update_fact,
    save_review_session, list_review_sessions, get_review_session,
)
from core.pipeline import _l3_payload, _truth_status_for, guardian, truth_gate
from core.reconcile import find_conflicts

_PENDING_STATE = "Observed"


# ─── Queue inspection ─────────────────────────────────────────────────────────

_RESTRICTED_STUB = {"restricted": True, "reason": "RESTRICTED_BY_POLICY"}


def _summary(fact: Dict[str, Any]) -> Dict[str, Any]:
    """A compact, content-light view of a queued fact (the claim is included so a
    curator can actually read it — this is a review surface, not the audit log).

    GDPR Art. 18: a fact under processing restriction returns a redacted stub
    instead — claim/source/source_status/confidence must never surface here."""
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
    """_summary() plus a fresh gate diagnosis — except for a restricted fact,
    which must not be passed through immune/Guardian/TruthGate/find_conflicts
    just to produce one. A restricted verdict is returned instead."""
    summary = _summary(fact)
    if fact.get("restricted"):
        summary["diagnosis"] = {"verdict": "restricted", "reason": "RESTRICTED_BY_POLICY"}
        return summary
    summary["diagnosis"] = _diagnose(fact)
    return summary


def pending(limit: Optional[int] = None,
            claim_type: Optional[str] = None,
            diagnose: bool = False) -> List[Dict[str, Any]]:
    """The review queue: facts stored in L1 but not yet in the canon (Observed),
    oldest first. Optionally filter by `claim_type` and cap with `limit`.

    diagnose=True attaches a fresh gate verdict to every item (the Kanban UI
    sorts cards into Pending/Quarantined by it). Opt-in: it re-runs the live
    gates per item, so it is O(queue) and pricier than the plain listing.
    Restricted items never reach the live gates — see _summary_with_diagnosis().

    GDPR Art. 18: an explicit `claim_type` filter omits restricted facts
    entirely, rather than including them as a redacted stub. A stub's mere
    presence or absence across different `claim_type` values would otherwise
    leak the restricted fact's real claim_type as a side channel — with no
    filter, a restricted fact still appears (redacted) in the plain listing."""
    items = get_all_facts(_PENDING_STATE)
    if claim_type is not None:
        items = [f for f in items
                 if not f.get("restricted") and f.get("claim_type") == claim_type]
    items.sort(key=lambda f: (f.get("created_at") or "", f.get("fact_id", "")))
    if limit is not None:
        items = items[:limit]
    if not diagnose:
        return [_summary(f) for f in items]
    return [_summary_with_diagnosis(f) for f in items]


def _diagnose(fact: Dict[str, Any]) -> Dict[str, Any]:
    """Re-run the live gates against a pending fact to explain WHY it is pending.

    Verdicts: blocked (a gate rejects it) | conflict (passes, but clashes with the
    canon) | ready (passes cleanly — awaiting only the curator's approval). Reuses
    the SAME validators as the live ingest path, so the preview matches reality.
    """
    claim = fact.get("claim", "")
    fid = fact["fact_id"]
    ct = fact.get("claim_type", "WORLD_FACT")

    pre = immune.screen(claim, fact_id=fid, check_canon=False)
    if pre["verdict"] == immune.BLOCK:
        return {"verdict": "blocked", "reason": f"Immune: {pre.get('reason', '')}"}

    facts_pack = {"facts": [fact], "query": claim, "total": 1}
    trace = [{"fact_id": fid, "source": fact.get("source"), "origin": "review",
              "epistemic_state": _PENDING_STATE, "confidence": fact.get("confidence")}]
    ok, reason = guardian(facts_pack, trace)
    if ok:
        ok, reason = truth_gate(facts_pack)
    if not ok:
        return {"verdict": "blocked", "reason": reason}

    conflicts = find_conflicts(claim, fact_id=fid) if ct == "WORLD_FACT" else []
    contradictions = [c for c in conflicts
                      if c["kind"] == contradiction.CONTRADICTION]
    if contradictions:
        return {"verdict": "conflict",
                "reason": f"contradicts {len(contradictions)} canonical fact(s)",
                "conflicts": [c["fact_id"] for c in contradictions]}
    return {"verdict": "ready", "reason": "passes the gates; awaiting curator approval"}


def review_item(fact_id: str) -> Dict[str, Any]:
    """Full detail for one queued fact: its summary plus a fresh gate diagnosis.

    GDPR Art. 18: a restricted fact never reaches the live gates — see
    _summary_with_diagnosis()."""
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    return {"found": True, **_summary_with_diagnosis(fact)}


def review_report() -> Dict[str, Any]:
    """Aggregate queue health: total pending and a breakdown by claim_type."""
    items = get_all_facts(_PENDING_STATE)
    by_type: Dict[str, int] = {}
    for f in items:
        key = f.get("claim_type", "UNKNOWN")
        by_type[key] = by_type.get(key, 0) + 1
    return {"pending": len(items), "by_claim_type": by_type}


# ─── Curator decisions (accountable) ──────────────────────────────────────────

_FORCE_REASON_MAX = 500  # accountability text, not an essay — keep audit lean

# update_fact() CAS-guards on updated_at (#244): a concurrent writer between
# our read and write makes it return False without applying the override
# metadata below. Retry a bounded number of times against the fresh state.
_CAS_MAX_ATTEMPTS = 3


def approve(fact_id: str, *, actor: Optional[str] = None,
            note: Optional[str] = None,
            force: bool = False, reason: Optional[str] = None) -> Dict[str, Any]:
    """
    Promote a pending fact into the canon (a curator's decision).

    Re-runs the gates. A `ready` or `conflict` item is promoted (a conflict is a
    non-destructive advisory — truth-first, we admit and link rather than silently
    drop). A `blocked` item is promoted only with `force=True`: an explicit curator
    override of a blocking diagnosis. Force approval is a trust-boundary
    operation, never a silent action — it requires a non-empty `reason`
    (1–500 chars) AND an EXPLICIT non-empty `actor` (no default identity for an
    override), and is recorded under its own audit event
    (`review_force_approve`, distinct from a normal `review_approve`).
    A normal approve keeps the backward-compatible default actor `curator`.
    Idempotent guard: only an `Observed` fact is a queue item.
    """
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    if fact.get("epistemic_state") != _PENDING_STATE:
        return {"found": True, "fact_id": fact_id, "approved": False,
                "reason": f"not pending (state={fact.get('epistemic_state')})"}

    # GDPR Art. 18: a fact under processing restriction is not actionable from
    # the review path — not even with force=True. Checked before _diagnose()
    # (never pass a restricted claim through immune/Guardian/TruthGate/
    # find_conflicts), before transition_esm() (no ESM promotion), before any
    # L3 merge, and before any success audit event. The correct path to
    # promote it is to lift the restriction first via an explicit compliance
    # action (core.compliance.unrestrict_processing), not approval.
    if fact.get("restricted"):
        return {"found": True, "fact_id": fact_id, "approved": False,
                "restricted": True, "reason": "RESTRICTED_BY_POLICY"}

    diag = _diagnose(fact)
    overridden = False
    if diag["verdict"] == "blocked":
        if not force:
            return {"found": True, "fact_id": fact_id, "approved": False,
                    "reason": diag["reason"], "diagnosis": diag}
        if not (reason and reason.strip()) or not (actor and actor.strip()):
            return {"found": True, "fact_id": fact_id, "approved": False,
                    "reason": "force approval requires a non-empty reason and "
                              "an explicit actor (it overrides a blocking "
                              "diagnosis; no default identity)",
                    "diagnosis": diag}
        if len(reason.strip()) > _FORCE_REASON_MAX:
            return {"found": True, "fact_id": fact_id, "approved": False,
                    "reason": f"force approval reason exceeds "
                              f"{_FORCE_REASON_MAX} characters",
                    "diagnosis": diag}
        overridden = True
    if actor is None or not actor.strip():
        actor = "curator"  # backward-compatible default for non-force approve

    # CAS guard: if the persisted state changed under us (a competing
    # writer/reviewer), transition_esm returns False and evicts the stale L0
    # entry. Abort the approval before any L3 merge / success audit — do not
    # resurrect a concurrently rejected/collapsed fact. Defense-in-depth.
    if not transition_esm(fact_id, "Validated"):
        return {"found": True, "fact_id": fact_id, "approved": False,
                "reason": "ESM CAS conflict: fact state changed concurrently",
                "diagnosis": diag["verdict"]}
    ct = fact.get("claim_type", "WORLD_FACT")
    if overridden:
        # Retry against a fresh read on a CAS miss, so the override markers
        # below are not silently dropped by a concurrent writer racing this
        # update (see #244) — a plain unconditional overwrite is not an
        # option here, since update_fact() itself is CAS-guarded.
        for _ in range(_CAS_MAX_ATTEMPTS):
            meta = dict((get_fact(fact_id) or {}).get("metadata") or {})
            meta.update({
                "admission_path": "review_force_approve",
                "override": True,
                "gate_passed": False,
                "gate_reason": diag.get("reason"),
            })
            if update_fact(fact_id, metadata=meta):
                break
        promoted = get_fact(fact_id)
        truth_status = "CURATOR_OVERRIDE"
    else:
        truth_status = _truth_status_for(ct, fact.get("source_status"))
        promoted = get_fact(fact_id)
    promoted["truth_status"] = truth_status
    get_l3_graph().merge_fact(_l3_payload(promoted))

    metrics.incr("review.approved")
    # Audit detail stays content-free: decision metadata only (actor, reason,
    # note, gate verdict) — the claim text is never duplicated into the chain.
    if overridden:
        metrics.incr("review.override")
        audit.append_event("review_force_approve", fact_id,
                           {"actor": actor, "reason": reason, "note": note,
                            "diagnosis": diag["verdict"],
                            "gate_reason": diag.get("reason")})
        # Emit the warning AFTER the ESM transition and audit append so that
        # PYTHONWARNINGS=error (or warnings.simplefilter('error', RuntimeWarning))
        # cannot prevent the fact from being promoted and recorded.
        warnings.warn(
            f"Force override: curator '{actor}' approved a blocked fact "
            f"(fact_id={fact_id!r}, diagnosis={diag['verdict']!r}). "
            f"This override is recorded in the audit chain.",
            RuntimeWarning,
            stacklevel=2,
        )
    else:
        audit.append_event("review_approve", fact_id,
                           {"actor": actor, "note": note, "override": False,
                            "diagnosis": diag["verdict"]})
    return {"found": True, "fact_id": fact_id, "approved": True,
            "override": overridden, "epistemic_state": "Validated",
            "truth_status": truth_status, "diagnosis": diag["verdict"]}


def reject(fact_id: str, *, actor: str = "curator",
           reason: str = "curator_rejected") -> Dict[str, Any]:
    """
    Reject a pending fact: transition Observed → Collapsed (logically removed from
    the queue). The fact's row remains for accountability; the decision is recorded
    in the tamper-evident audit chain. Only an `Observed` fact can be rejected.
    """
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    if fact.get("epistemic_state") != _PENDING_STATE:
        return {"found": True, "fact_id": fact_id, "rejected": False,
                "reason": f"not pending (state={fact.get('epistemic_state')})"}

    # CAS guard: if the persisted state changed under us (a competing
    # writer/reviewer), transition_esm returns False and evicts the stale L0
    # entry. Abort before recording a reject-success audit event.
    if not transition_esm(fact_id, "Collapsed"):
        return {"found": True, "fact_id": fact_id, "rejected": False,
                "reason": "ESM CAS conflict: fact state changed concurrently"}
    metrics.incr("review.rejected")
    audit.append_event("review_reject", fact_id, {"actor": actor, "reason": reason})
    return {"found": True, "fact_id": fact_id, "rejected": True,
            "epistemic_state": "Collapsed", "reason": reason}


# ─── Resumable review sessions ────────────────────────────────────────────────

def create_session(batch_size: Optional[int] = None) -> Dict[str, Any]:
    """Snapshot the current pending queue into a resumable session.

    The session captures which fact_ids were pending at creation time so a
    curator can pause and resume without losing their place. No claim text is
    stored — only IDs and progress counters.
    """
    pending_facts = get_all_facts(_PENDING_STATE)
    pending_facts.sort(key=lambda f: (f.get("created_at") or "", f.get("fact_id", "")))
    claim_ids = [f["fact_id"] for f in pending_facts]
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
    """Fetch a session by ID, or None if not found."""
    return get_review_session(session_id)


def list_sessions(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List sessions, newest first. Optionally filter by status."""
    return list_review_sessions(status)


def resume_session(session_id: str) -> Dict[str, Any]:
    """Return the unresolved pending items for a session, in stable order.

    Only fact_ids that are still in `Observed` state AND not yet in
    reviewed_ids are included. This is the core resumability guarantee:
    a curator who pauses mid-batch sees the same unresolved items on return.
    """
    session = get_review_session(session_id)
    if session is None:
        return {"found": False, "session_id": session_id}
    if session["status"] == "completed":
        return {"found": True, "session_id": session_id, "status": "completed",
                "pending_items": [], "remaining": 0}

    reviewed = set(session["reviewed_ids"])
    unresolved = []
    for fid in session["claim_ids"]:
        if fid in reviewed:
            continue
        fact = get_fact(fid)
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


def record_session_decision(session_id: str, fact_id: str,
                            decision: str) -> Dict[str, Any]:
    """Mark a fact as reviewed within a session (after approve/reject is called).

    `decision` must be 'approved' or 'rejected'. Does NOT perform the
    approve/reject itself — callers must call review.approve / review.reject
    first, then record the session progress here.
    """
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
    return {"ok": True, "session_id": session_id, "fact_id": fact_id,
            "decision": decision}


def complete_session(session_id: str) -> Dict[str, Any]:
    """Mark a session as completed."""
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
}


def decisions(limit: int = 50, *,
              include_claim: bool = True) -> List[Dict[str, Any]]:
    """
    Curator decision history, newest first, reconstructed from the audit chain
    (no parallel state store). Each entry carries the content-free audit detail
    (actor/reason/note/verdict); with `include_claim=True` (default, used by the
    review UI) the claim text is re-read from L1 for display — an erased fact
    survives as a decision record with claim=None. With `include_claim=False`
    no memory content is rehydrated at all: the entry stays as content-free as
    the audit chain itself (no `claim`/`claim_type` keys).

    GDPR Art. 18: a fact that is now under processing restriction also gets
    claim=None (mirroring the erased case) plus `restricted=True` and
    `restricted_reason="RESTRICTED_BY_POLICY"` — distinct from the erased case
    (no `restricted` key) and from `reason`, which already holds the curator's
    own decision reason (`entry["detail"]["reason"]`) and must not be clobbered.
    """
    out: List[Dict[str, Any]] = []
    for entry in reversed(audit.audit_log()):
        decision = _DECISION_EVENTS.get(entry["event"])
        if decision is None:
            continue
        item = {
            "decision": decision,
            "fact_id": entry["fact_id"],
            "ts": entry["ts"],
            "actor": entry["detail"].get("actor"),
            "reason": entry["detail"].get("reason"),
            "note": entry["detail"].get("note"),
            "diagnosis": entry["detail"].get("diagnosis"),
        }
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
