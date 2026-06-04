# core/reconcile.py
# Velantrim ExoCortex — Truth Maintenance (reconcile)
# v8.6.0-sprint2
#
# What happens when a new fact meets the existing canon:
#   reinforce()  — repeated independent evidence → confidence rises
#                  (Laplace decay), contradicting evidence → falls. Memory reflects
#                  accumulated reliability, not the last write.
#   supersede()  — a reformulation: the old fact → Deprecated + a
#                  SUPERSEDED_BY edge to the new one (new → Validated). Memory is updated
#                  by versioning, not overwritten blindly.
#   contradict() — the old fact → Contradicted + a CONTRADICTS edge to the source.
#                  (The immune layer from the README.) Does not silently overwrite.
#
# Everything is deterministic and explicit. Auto-detection of semantic contradictions (NLI/LLM)
# is intentionally NOT done here — it would produce false positives; left as a
# future hook. The only auto-operation is reinforce on an exact claim repeat
# (see ingest.ingest), which is safe.

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from core.memory import get_fact, store_fact, transition_esm, update_fact
from core.l3_graph import get_l3_graph
from core.embedding import get_embedder

REL_SUPERSEDED_BY = "SUPERSEDED_BY"
REL_CONTRADICTS = "CONTRADICTS"

# Threshold for "similar, but it is a DIFFERENT fact" → a contradiction/supersession candidate.
_CONFLICT_MIN_SIM = 0.5


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sync_l3(fact_id: str) -> Optional[Dict[str, Any]]:
    """Re-merge the fact from SQLite into L3 so the canon reflects the latest state."""
    fact = get_fact(fact_id)
    if fact is not None:
        get_l3_graph().merge_fact(fact)
    return fact


def reinforce(fact_id: str, agreement: bool = True) -> Optional[float]:
    """
    Reinforce a fact with independent evidence. Returns the new confidence
    (or None if the fact does not exist).

    agreement=True  → confidence += (1 - confidence) / (obs + 1)  — decaying growth.
    agreement=False → confidence *= obs / (obs + 1)               — decaying decline.
    The observation counter is stored in metadata['observations'].
    """
    fact = get_fact(fact_id)
    if fact is None:
        return None

    meta = dict(fact.get("metadata") or {})
    obs = int(meta.get("observations", 1))
    conf = float(fact.get("confidence", 0.5))

    if agreement:
        new_conf = round(conf + (1.0 - conf) / (obs + 1), 4)
    else:
        new_conf = round(conf * obs / (obs + 1), 4)

    meta["observations"] = obs + 1
    meta["last_consolidated"] = _now()  # reinforcement resets the decay clock
    update_fact(fact_id, confidence=new_conf, metadata=meta)
    _sync_l3(fact_id)
    return new_conf


def supersede(old_id: str, new_fact: Dict[str, Any]) -> str:
    """
    A new fact supersedes the old one. Old: Validated → Contradicted → Deprecated
    (+ an old -SUPERSEDED_BY-> new edge). New: stored and Validated.
    Returns the fact_id of the new fact.
    """
    new_id = new_fact.get("fact_id")
    if not new_id:
        raise ValueError("supersede: new_fact.fact_id is required")

    store_fact({**new_fact, "epistemic_state": "Observed"})
    transition_esm(new_id, "Validated")
    _sync_l3(new_id)

    old = get_fact(old_id)
    if old is not None and old.get("epistemic_state") == "Validated":
        # There is no direct Validated→Deprecated in the matrix: we go via Contradicted.
        transition_esm(old_id, "Contradicted")
        transition_esm(old_id, "Deprecated")
        _sync_l3(old_id)

    get_l3_graph().add_edge(old_id, REL_SUPERSEDED_BY, new_id, {"at": _now()})
    return new_id


def contradict(fact_id: str, by_id: str) -> bool:
    """
    Mark a fact as refuted by source by_id: Validated → Contradicted
    (+ a fact -CONTRADICTS-> by edge). Returns True if the state changed.
    """
    fact = get_fact(fact_id)
    changed = False
    if fact is not None and fact.get("epistemic_state") == "Validated":
        transition_esm(fact_id, "Contradicted")
        _sync_l3(fact_id)
        changed = True
    get_l3_graph().add_edge(fact_id, REL_CONTRADICTS, by_id, {"at": _now()})
    return changed


def fact_history(fact_id: str) -> Dict[str, List[str]]:
    """
    Truth provenance of a fact: what it is linked to via truth-maintenance edges.
    Uses incoming and outgoing edges (incoming_edges / get_edges).

    Returns ids:
      superseded_by   — what replaced this fact (outgoing SUPERSEDED_BY)
      supersedes      — which facts it replaced (incoming SUPERSEDED_BY)
      contradicts     — what it refutes (outgoing CONTRADICTS)
      contradicted_by — who refutes it (incoming CONTRADICTS)
    """
    graph = get_l3_graph()
    out = graph.get_edges(fact_id)
    inc = graph.incoming_edges(fact_id)
    return {
        "superseded_by":   [e["target"] for e in out if e["rel_type"] == REL_SUPERSEDED_BY],
        "supersedes":      [e["source"] for e in inc if e["rel_type"] == REL_SUPERSEDED_BY],
        "contradicts":     [e["target"] for e in out if e["rel_type"] == REL_CONTRADICTS],
        "contradicted_by": [e["source"] for e in inc if e["rel_type"] == REL_CONTRADICTS],
    }


def find_conflicts(
    claim: str,
    *,
    fact_id: Optional[str] = None,
    threshold: float = _CONFLICT_MIN_SIM,
    k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Identify conflict CANDIDATES: canonical WORLD_FACTs semantically
    close to claim (≥ threshold), but a different fact and not a verbatim repeat.

    Intentionally does NOT mark anything automatically — embedding similarity does not
    distinguish a "refinement" from a "contradiction". The decision is made by the caller
    via supersede()/contradict(). This is a signal for review, not a verdict.
    """
    graph = get_l3_graph()
    q_vec = get_embedder().embed(claim)
    claim_norm = claim.strip().lower()
    out: List[Dict[str, Any]] = []
    for node in graph.vector_search(q_vec, k=k):
        if node.get("fact_id") == fact_id:
            continue
        if node.get("claim_type", "WORLD_FACT") != "WORLD_FACT":
            continue
        if node.get("epistemic_state") != "Validated":
            continue
        if node.get("claim", "").strip().lower() == claim_norm:
            continue  # a verbatim repeat is a reinforce, not a conflict
        if node.get("_relevance", 0.0) < threshold:
            continue
        out.append({
            "fact_id": node["fact_id"],
            "claim": node.get("claim", ""),
            "similarity": node.get("_relevance", 0.0),
        })
    return out
