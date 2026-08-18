# core/reconcile.py
# Velantrim ExoCortex — Truth Maintenance (reconcile)
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
# future hook. The only auto-operation on an exact claim repeat is occurrence
# tracking (record_occurrence) — it updates frequency metadata only and never
# touches confidence/truth_status/ESM (see ingest exact-dedup). A same- or
# different-source repeat is a frequency signal, NOT independent evidence;
# raising confidence stays an explicit reinforce() decision.

import logging
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from core.memory import get_fact, store_fact, transition_esm, update_fact, l3_secondary_sync_admissible
from core.l3_graph import get_l3_graph
from core.embedding import get_embedder
from core.queue import get_outbox_queue
from core import contradiction

logger = logging.getLogger("velantrim.reconcile")

REL_SUPERSEDED_BY = "SUPERSEDED_BY"
REL_CONTRADICTS = "CONTRADICTS"

# Threshold for "similar, but it is a DIFFERENT fact" → a contradiction/supersession candidate.
_CONFLICT_MIN_SIM = 0.5

# update_fact() CAS-guards on updated_at (#244): a concurrent writer between our
# read and write makes it return False without applying our change. Retry a
# bounded number of times against the fresh state rather than reporting a
# value (confidence/occurrence count) that was never actually persisted.
_CAS_MAX_ATTEMPTS = 3


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sync_l3(fact_id: str) -> Optional[Dict[str, Any]]:
    """Re-merge the fact from SQLite into L3 so the canon reflects the latest state.

    L1 and L3 do not share a transaction: if the L3 backend fails here, the L1
    update has already happened. Mirror the pipeline's self-heal path — enqueue
    the fact in the L3 outbox so drain_l3_outbox() retries the merge later,
    instead of silently losing the sync.

    Guardrail: pre-canonical facts must never enter L3 through this metadata/
    confidence sync path — only TruthGate admission may promote them.
    Contradicted/Deprecated sync only when the node is already in L3.
    """
    fact = get_fact(fact_id)
    if fact is not None and not l3_secondary_sync_admissible(fact):
        return fact
    if fact is not None:
        try:
            get_l3_graph().merge_fact(fact)
        except Exception as e:  # noqa: BLE001 — backend down; keep L1, retry via outbox
            logger.warning("_sync_l3: L3 merge failed for %s (%s); queued for retry",
                           fact_id, type(e).__name__)
            get_outbox_queue().enqueue(fact_id)
    return fact


def reinforce(
    fact_id: str,
    agreement: bool = True,
    *,
    lineage_id: Optional[str] = None,
) -> Optional[float]:
    """
    Reinforce a fact with independent evidence. Returns the new confidence;
    None if the fact does not exist; or the fact's current (unchanged)
    confidence if update_fact()'s CAS guard lost a sustained race across all
    retries (the reinforcement is dropped rather than reporting a confidence
    value that was never actually persisted — see #244).

    agreement=True  → confidence += (1 - confidence) / (obs + 1)  — decaying growth.
    agreement=False → confidence *= obs / (obs + 1)               — decaying decline.
    The observation counter is stored in metadata['observations'].

    ``lineage_id`` identifies the evidence family that caused this explicit
    reinforcement. In the grant profile it is mandatory. Reusing an already
    counted lineage is idempotent: it cannot increase observations or confidence.
    Outside the grant profile a missing lineage remains backward-compatible but
    is recorded as UNKNOWN rather than being represented as independent evidence.
    """
    normalized_lineage = lineage_id.strip() if isinstance(lineage_id, str) and lineage_id.strip() else None
    grant_profile = os.environ.get("VELANTRIM_RELEASE_PROFILE", "").strip().casefold() == "grant"
    if grant_profile and normalized_lineage is None:
        raise ValueError("reinforce: grant profile requires lineage_id")

    for attempt in range(_CAS_MAX_ATTEMPTS):
        fact = get_fact(fact_id)
        if fact is None:
            return None

        meta = dict(fact.get("metadata") or {})
        counted_lineages = {
            value for value in (meta.get("reinforcement_lineages") or [])
            if isinstance(value, str) and value
        }
        if normalized_lineage is not None and normalized_lineage in counted_lineages:
            return float(fact.get("confidence", 0.5))

        obs = int(meta.get("observations", 1))
        conf = float(fact.get("confidence", 0.5))

        if agreement:
            new_conf = round(conf + (1.0 - conf) / (obs + 1), 4)
        else:
            new_conf = round(conf * obs / (obs + 1), 4)

        meta["observations"] = obs + 1
        if normalized_lineage is not None:
            counted_lineages.add(normalized_lineage)
            meta["reinforcement_lineages"] = sorted(counted_lineages)
            meta["last_reinforcement_lineage"] = normalized_lineage
        else:
            meta["reinforcement_lineage_status"] = "UNKNOWN"
        meta["last_consolidated"] = _now()  # reinforcement resets the decay clock
        if update_fact(fact_id, confidence=new_conf, metadata=meta):
            _sync_l3(fact_id)
            return new_conf
        logger.warning(
            "reinforce: update_fact CAS miss for %s (attempt %d/%d), retrying",
            fact_id, attempt + 1, _CAS_MAX_ATTEMPTS)

    # Exhausted retries under sustained contention: drop this reinforcement
    # rather than lie about a confidence value that was never persisted.
    current = get_fact(fact_id)
    return current.get("confidence") if current is not None else None


def record_occurrence(
    fact_id: str,
    *,
    source: Optional[str] = None,
    fingerprint: Optional[str] = None,
) -> Optional[int]:
    """
    Register that identical content was ingested again (an exact-duplicate
    sighting). This is a FREQUENCY signal only: it updates occurrence metadata
    and NEVER changes confidence, truth_status or the ESM state — a repeat is
    not independent evidence. Returns the new occurrence count; None if the
    fact does not exist; or the fact's current (unchanged) occurrence count if
    update_fact()'s CAS guard lost a sustained race across all retries (the
    sighting is dropped rather than reporting a count that was never actually
    persisted — see #244).

    Occurrence bookkeeping is kept deliberately SEPARATE from
    metadata['observations'] (which reinforce() folds into the confidence
    formula) so frequency and evidentiary weight are never conflated:
      occurrences        — int, times this exact content has been seen (≥2 here)
      last_seen          — ISO timestamp of the most recent sighting
      sources_seen       — sorted list of distinct source labels
      fingerprint_sha256 — sha256 of the normalized content (audit)
    """
    for attempt in range(_CAS_MAX_ATTEMPTS):
        fact = get_fact(fact_id)
        if fact is None:
            return None

        meta = dict(fact.get("metadata") or {})
        occurrences = int(meta.get("occurrences", 1)) + 1
        meta["occurrences"] = occurrences
        meta["last_seen"] = _now()
        if fingerprint:
            meta["fingerprint_sha256"] = fingerprint
        seen = set(meta.get("sources_seen") or [])
        if fact.get("source"):
            seen.add(fact["source"])
        if source:
            seen.add(source)
        meta["sources_seen"] = sorted(seen)

        if update_fact(fact_id, metadata=meta):
            # Guardrail: occurrence tracking must never promote a fact into the
            # canon. Sync to L3 ONLY when the fact is already Validated (already
            # in the canon); a non-Validated fact is never merged from here.
            if l3_secondary_sync_admissible(fact):
                _sync_l3(fact_id)
            return occurrences
        logger.warning(
            "record_occurrence: update_fact CAS miss for %s (attempt %d/%d), retrying",
            fact_id, attempt + 1, _CAS_MAX_ATTEMPTS)

    # Exhausted retries under sustained contention: drop this sighting rather
    # than lie about an occurrence count that was never persisted.
    current = get_fact(fact_id)
    if current is None:
        return None
    return int((current.get("metadata") or {}).get("occurrences", 1))


def supersede(old_id: str, new_fact: Dict[str, Any], *, enforce_gate: bool = True) -> str:
    """
    A new fact supersedes the old one. Old: Validated → Contradicted → Deprecated
    (+ an old -SUPERSEDED_BY-> new edge). New: stored and Validated.
    Returns the fact_id of the new fact.

    The new fact is a *fresh* claim, so by default it must clear the same
    Guardian + TruthGate path as any other entry into L3 — a supersession is not
    a licence to inject an unvalidated world fact into the canon (Graph = Truth:
    the gate is the only entry). Raises ValueError if the new fact is rejected.
    `enforce_gate=False` is reserved for callers that have already gated the fact.
    """
    new_id = new_fact.get("fact_id")
    if not new_id:
        raise ValueError("supersede: new_fact.fact_id is required")

    store_fact({**new_fact, "epistemic_state": "Observed"})

    if enforce_gate:
        # Lazy import: pipeline does not import reconcile, but keep it local to be safe.
        from core.pipeline import guardian, truth_gate
        staged = get_fact(new_id)
        facts_pack = {"facts": [staged], "query": staged.get("claim", ""), "total": 1}
        trace = [{
            "fact_id": new_id, "source": staged.get("source"),
            "origin": "supersede", "epistemic_state": "Observed",
            "confidence": staged.get("confidence"),
        }]
        ok, reason = guardian(facts_pack, trace)
        if ok:
            ok, reason = truth_gate(facts_pack)
        if not ok:
            raise ValueError(f"supersede: new fact rejected by TruthGate: {reason}")

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

    Each candidate is classified (core/contradiction.py) into kind ∈
    {CONTRADICTION, REFINEMENT, RELATED} with the deciding signal, so the caller
    can tell an opposing claim from a refinement. Still does NOT mark anything
    automatically — embedding similarity is a candidate filter, the classifier a
    high-precision signal; the decision (supersede/contradict) stays with the
    caller. A signal for review, not a verdict.
    """
    graph = get_l3_graph()
    q_vec = get_embedder().embed(claim)
    claim_norm = claim.strip().lower()
    out: List[Dict[str, Any]] = []
    # Overfetch beyond k (mirrors LadybugL3Graph.vector_search's own internal
    # k*3 margin): a restricted candidate can occupy a raw top-k slot and get
    # filtered out below, which would silently hide a real unrestricted
    # conflict that was just outside the raw top-k. We stop once k real
    # candidates have been collected (see the break below).
    for node in graph.vector_search(q_vec, k=max(k * 3, k)):
        candidate_id = node.get("fact_id")
        if candidate_id == fact_id:
            continue
        # Backend-independent restriction check: LadybugL3Graph's `_COLS` is a
        # fixed typed-column list that does not include `restricted`, so its
        # vector_search()/get_fact() nodes never carry the flag even when the
        # underlying fact is restricted. core.memory.get_fact() always has it
        # (facts.restricted persists in L1 SQLite regardless of L3 backend).
        canonical = get_fact(candidate_id) if candidate_id else None
        if canonical is not None and canonical.get("restricted"):
            continue  # GDPR Art. 18: restricted facts do not take part in processing
        if node.get("claim_type", "WORLD_FACT") != "WORLD_FACT":
            continue
        if node.get("epistemic_state") != "Validated":
            continue
        node_claim = node.get("claim", "")
        if node_claim.strip().lower() == claim_norm:
            continue  # a verbatim repeat is a reinforce, not a conflict
        sim = node.get("_relevance", 0.0)
        if sim < threshold:
            continue
        verdict = contradiction.classify(claim, node_claim, similarity=sim)
        out.append({
            "fact_id": node["fact_id"],
            "claim": node_claim,
            "similarity": sim,
            "kind": verdict["kind"],
            "signal": verdict["signal"],
        })
        if len(out) >= k:
            break
    return out
