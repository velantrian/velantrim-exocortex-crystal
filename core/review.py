# core/review.py
# Velantrim ExoCortex — Curator Review Queue (grant WP2)
# v8.28.0-sprint6
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

from typing import Any, Dict, List, Optional

from core import audit, contradiction, immune, metrics
from core.l3_graph import get_l3_graph
from core.memory import get_all_facts, get_fact, transition_esm
from core.pipeline import _l3_payload, _truth_status_for, guardian, truth_gate
from core.reconcile import find_conflicts

_PENDING_STATE = "Observed"


# ─── Queue inspection ─────────────────────────────────────────────────────────

def _summary(fact: Dict[str, Any]) -> Dict[str, Any]:
    """A compact, content-light view of a queued fact (the claim is included so a
    curator can actually read it — this is a review surface, not the audit log)."""
    return {
        "fact_id": fact["fact_id"],
        "claim": fact.get("claim"),
        "claim_type": fact.get("claim_type"),
        "source": fact.get("source"),
        "source_status": fact.get("source_status"),
        "confidence": fact.get("confidence"),
        "created_at": fact.get("created_at"),
    }


def pending(limit: Optional[int] = None,
            claim_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """The review queue: facts stored in L1 but not yet in the canon (Observed),
    oldest first. Optionally filter by `claim_type` and cap with `limit`."""
    items = get_all_facts(_PENDING_STATE)
    if claim_type is not None:
        items = [f for f in items if f.get("claim_type") == claim_type]
    items.sort(key=lambda f: (f.get("created_at") or "", f.get("fact_id", "")))
    if limit is not None:
        items = items[:limit]
    return [_summary(f) for f in items]


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
    """Full detail for one queued fact: its summary plus a fresh gate diagnosis."""
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    return {"found": True, **_summary(fact), "diagnosis": _diagnose(fact)}


def review_report() -> Dict[str, Any]:
    """Aggregate queue health: total pending and a breakdown by claim_type."""
    items = get_all_facts(_PENDING_STATE)
    by_type: Dict[str, int] = {}
    for f in items:
        key = f.get("claim_type", "UNKNOWN")
        by_type[key] = by_type.get(key, 0) + 1
    return {"pending": len(items), "by_claim_type": by_type}


# ─── Curator decisions (accountable) ──────────────────────────────────────────

def approve(fact_id: str, *, actor: str = "curator", note: Optional[str] = None,
            force: bool = False) -> Dict[str, Any]:
    """
    Promote a pending fact into the canon (a curator's decision).

    Re-runs the gates. A `ready` or `conflict` item is promoted (a conflict is a
    non-destructive advisory — truth-first, we admit and link rather than silently
    drop). A `blocked` item is promoted only with `force=True`: an explicit curator
    override, recorded as such in the audit chain. Idempotent guard: only an
    `Observed` fact is a queue item.
    """
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    if fact.get("epistemic_state") != _PENDING_STATE:
        return {"found": True, "fact_id": fact_id, "approved": False,
                "reason": f"not pending (state={fact.get('epistemic_state')})"}

    diag = _diagnose(fact)
    overridden = False
    if diag["verdict"] == "blocked":
        if not force:
            return {"found": True, "fact_id": fact_id, "approved": False,
                    "reason": diag["reason"], "diagnosis": diag}
        overridden = True

    transition_esm(fact_id, "Validated")
    ct = fact.get("claim_type", "WORLD_FACT")
    truth_status = _truth_status_for(ct, fact.get("source_status"))
    promoted = get_fact(fact_id)
    promoted["truth_status"] = truth_status
    get_l3_graph().merge_fact(_l3_payload(promoted))

    metrics.incr("review.approved")
    if overridden:
        metrics.incr("review.override")
    audit.append_event("review_approve", fact_id,
                       {"actor": actor, "note": note, "override": overridden,
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

    transition_esm(fact_id, "Collapsed")
    metrics.incr("review.rejected")
    audit.append_event("review_reject", fact_id, {"actor": actor, "reason": reason})
    return {"found": True, "fact_id": fact_id, "rejected": True,
            "epistemic_state": "Collapsed", "reason": reason}
