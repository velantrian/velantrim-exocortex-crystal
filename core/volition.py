# core/volition.py
# Velantrim ExoCortex — Memory Volition (RFC0065)
#
# "Memory = Agency." So far memory only stores what it is TOLD (ingest) or what a
# query pulls up (pipeline). Volition gives the canon a will of its own: it can
# write a fact it generated itself, and it can decide which of its memories
# deserve attention and rehearsal.
#
# Two faces, both faithful to "Graph = Truth":
#   - write_voluntary(): the system writes a DERIVED, self-authored fact — but
#     through the SAME Guardian → TruthGate path as everything else. Volition
#     never bypasses the gate; a self-generated claim earns its place or is
#     blocked like any other. The fact is tagged (metadata.volition, trace
#     origin "volition") so a voluntary write is always distinguishable from an
#     external one.
#   - VolitionWorker (volition_cycle): a deterministic survey that ranks the canon
#     by a salience signal (significance · confidence · reinforcement · co-
#     activation) and REHEARSES the most salient memories — refreshing their decay
#     clock so attention slows forgetting. Rehearsal does NOT fabricate evidence
#     (confidence is untouched); it only reflects that the system chose to keep
#     thinking about these facts. Explicit and opt-in, like consolidate().
#
# Deterministic, dependency-free, observable.

import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core.memory import get_fact, update_fact
from core.l3_graph import get_l3_graph
from core import metrics

ORIGIN = "volition"
_EPISODE_REL = "CO_OCCURRED"
_ENV_COACT_NORM = "VELANTRIM_VOLITION_COACT_NORM"  # co-activation saturation point


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _coact_norm() -> float:
    try:
        return max(1.0, float(os.environ.get(_ENV_COACT_NORM, 5.0)))
    except ValueError:
        return 5.0


def _coactivation_degree(fact_id: str) -> int:
    """How many CO_OCCURRED edges this fact has (its recall gregariousness)."""
    return len(get_l3_graph().get_edges(fact_id, _EPISODE_REL))


def volition_salience(fact: Dict[str, Any]) -> float:
    """
    Deterministic salience ∈ [0,1] — how much the system 'wants' to attend to a
    fact. Four explainable drivers:
        0.40·significance + 0.25·confidence + 0.20·reinforcement + 0.15·co-activation
    reinforcement = 1 − 1/observations; co-activation = min(1, degree / norm).
    """
    sig = min(1.0, max(0.0, float(fact.get("significance", 0.5))))
    conf = min(1.0, max(0.0, float(fact.get("confidence", 0.5))))
    meta = fact.get("metadata") or {}
    obs = max(1, int(meta.get("observations", 1)))
    reinforcement = 1.0 - 1.0 / obs
    degree = _coactivation_degree(fact["fact_id"])
    coact = min(1.0, degree / _coact_norm())
    return round(0.40 * sig + 0.25 * conf + 0.20 * reinforcement + 0.15 * coact, 4)


def _validated_records() -> List[Dict[str, Any]]:
    graph = get_l3_graph()
    out: List[Dict[str, Any]] = []
    for node in graph.all_facts():
        if node.get("epistemic_state") != "Validated":
            continue
        out.append(get_fact(node["fact_id"]) or node)
    return out


def write_voluntary(
    claim: str,
    *,
    significance: float = 0.5,
    confidence: float = 0.6,
    claim_type: Optional[str] = None,
    source: str = ORIGIN,
) -> Dict[str, Any]:
    """
    The system voluntarily writes a self-authored fact — through the normal gates.

    Thin wrapper over ingest: same Guardian → TruthGate → L3 path, so a voluntary
    write can be blocked exactly like an external one (truth-first). On acceptance
    the fact is tagged metadata.volition=True and the result carries volition=True.
    """
    from core.ingest import ingest  # lazy: ingest imports many siblings
    result = ingest(claim, source=source, significance=significance,
                    confidence=confidence, claim_type=claim_type)
    result["volition"] = True
    if result.get("accepted") and not result.get("duplicate"):
        fid = result["fact"]["fact_id"]
        current = get_fact(fid)
        if current is not None:
            meta = dict(current.get("metadata") or {})
            meta["volition"] = True
            if update_fact(fid, metadata=meta):
                get_l3_graph().merge_fact(get_fact(fid))
    metrics.incr("volition.write")
    return result


def volition_focus(*, k: int = 5) -> List[Dict[str, Any]]:
    """The system's self-selected attention set: the k most salient canonical
    facts, strongest first (read-only). Compact view: fact_id, claim, salience."""
    scored = [{
        "fact_id": f["fact_id"],
        "claim": f.get("claim", ""),
        "salience": volition_salience(f),
    } for f in _validated_records()]
    scored.sort(key=lambda s: (-s["salience"], s["fact_id"]))
    return scored[:max(0, k)]


def volition_cycle(*, k: int = 5, now: Optional[datetime] = None) -> Dict[str, Any]:
    """
    VolitionWorker pass: rehearse the k most salient memories.

    Rehearsal refreshes each focused fact's decay clock (metadata.last_consolidated
    → now), so the system's chosen attention slows forgetting — without inventing
    corroboration (confidence is left untouched). Returns {'focused': [ids], 'at'}.
    Idempotent at a given instant.
    """
    now = now or _now()
    iso = now.isoformat()
    graph = get_l3_graph()
    focused: List[str] = []
    for item in volition_focus(k=k):
        fid = item["fact_id"]
        current = get_fact(fid)
        if current is None:
            continue
        meta = dict(current.get("metadata") or {})
        meta["last_consolidated"] = iso          # rehearsal resets the decay clock
        meta["volition_rehearsed_at"] = iso
        if update_fact(fid, metadata=meta):
            graph.merge_fact(get_fact(fid))
            focused.append(fid)
    metrics.incr("volition.cycle")
    return {"focused": focused, "at": iso}


def volition_report(*, k: int = 5) -> Dict[str, Any]:
    """Observable volition state: population, voluntary-write count, current focus."""
    records = _validated_records()
    voluntary = sum(1 for f in records if (f.get("metadata") or {}).get("volition"))
    return {
        "total": len(records),
        "voluntary": voluntary,
        "focus": volition_focus(k=k),
    }
