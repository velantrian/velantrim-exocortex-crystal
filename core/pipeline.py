# core/pipeline.py
# Velantrim ExoCortex — Core Pipeline
# v8.7.0-sprint2
#
# Principle: Graph = Truth · LLM = Language · Memory = Physiology
# Pipeline: Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer
#
# Retrieval — vector-based (cosine of embeddings) over the seed corpus + recall from L3.
# The answer — a pluggable Generator (extractive by default, optional LLM). L3 — a pluggable
# backend (auto→LadybugDB / mock / neo4j). Full L0–L6 architecture:
# docs/Velantrim_V8_Crystal_Sprint1_toc.md
#
# TODO (next):
#   - ESM: full transition matrix + automatic Supported/Hypothesized
#   - First-class episodic nodes (Person/Place/Time) instead of edge props
# (Done: HybridRetriever graph-walk over vector-recall — see _graph_walk below.)

import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from core.trace import build_trace, promote_trace, format_trace
from core.memory import (
    store_fact, get_fact, transition_esm, SUBJECTIVE_CLAIM_TYPES,
)
from core.queue import get_outbox_queue
from core.l3_graph import get_l3_graph
from core.embedding import get_embedder, cosine, assert_compatible_embedder
from core.generation import get_generator
from core import metrics, adaptation

logger = logging.getLogger(__name__)

# ─── RETRIEVAL CORPUS (source for retrieve, not L3) ──────────────────────────
# Issue #65: demo seed facts are opt-in only (VELANTRIM_DEMO_SEED=1).
# The production pipeline starts with an empty corpus; all facts must enter
# through ingest() / velantrim learn and pass the normal TruthGate path.
# A direct MERGE into L3 bypassing the TruthGate is an architectural bug.

def _load_demo_seed():
    """Return demo seed facts when VELANTRIM_DEMO_SEED=1, else empty list.

    Called inside retrieve() so the env flag is evaluated at query time, not at
    module import time. This keeps the production default (no seed) working even
    when tests monkeypatch the env var after the module has been imported.
    """
    import os
    if os.environ.get("VELANTRIM_DEMO_SEED", "0") == "1":
        from core.demo_seed import DEMO_FACTS
        return DEMO_FACTS
    return []


# ─── RETRIEVAL (vector / semantic) ────────────────────────────────────────────
# Cosine similarity of embeddings over TWO sources:
#   1) demo seed corpus (opt-in via VELANTRIM_DEMO_SEED=1) — curated reference facts;
#   2) the L3 canon — what the system has already learned and run through the gates.
# Recall from L3 closes the loop "learned → remembered → recalled": facts accepted
# via ingest()/pipeline become available for the answer. Dedup by id.
# The embedder is pluggable (core/embedding.py): default HashingEmbedder, sbert optional.
# Hybrid: vector-recall + multi-hop graph-walk (spreading activation / HippoRAG-lite).

# Cutoff threshold for noise from hash collisions: below this — not relevant.
_RETRIEVAL_MIN_SIM = 0.05
# Activation damping per graph-walk hop (PageRank propagation).
_GRAPH_WALK_DECAY = 0.5
# Graph-walk depth (number of hops from vector hits).
_GRAPH_WALK_HOPS = 2
# Activation propagation weights by edge type. Truth-maintenance edges do NOT
# carry relevance: a fact is not "more relevant" because it is refuted
# (CONTRADICTS) or because it is replaced (SUPERSEDED_BY) — otherwise graph-walk would lift
# exactly the refuted/obsolete. Episodic association (CO_OCCURRED) and any
# unknown types propagate normally (default weight 1.0).
_WALK_EDGE_WEIGHTS = {
    "CONTRADICTS": 0.0,
    "SUPERSEDED_BY": 0.0,
}
_WALK_DEFAULT_EDGE_WEIGHT = 1.0


def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Hybrid search: cosine of embeddings over the demo seed corpus (opt-in) and
    the L3 canon, then a multi-hop graph-walk (spreading activation).
    Returns the top-k by score, deduped by id.
    Seed facts arrive as Observed; recall from L3 uses its stored ESM state.
    """
    embedder = get_embedder()
    graph = get_l3_graph()
    # Guard against mixing embedders: we catch an embedder swap on a persistent
    # store (incomparable vectors → broken ranking). The first call stamps it.
    assert_compatible_embedder(graph)
    q_vec = embedder.embed(query)
    by_id: Dict[str, Dict[str, Any]] = {}

    def _offer(item: Dict[str, Any]) -> None:
        # Dedup by id: the same fact may be both in the corpus and in L3.
        prev = by_id.get(item["id"])
        if prev is None or item["_score"] > prev["_score"]:
            by_id[item["id"]] = item

    # Source 1: seed corpus (opt-in demo facts when VELANTRIM_DEMO_SEED=1).
    for item in _load_demo_seed():
        sim = cosine(q_vec, embedder.embed(item["text"]))
        if sim < _RETRIEVAL_MIN_SIM:
            continue
        _offer({
            **item,
            "_score":          round(sim * item.get("confidence", 1.0), 4),
            "epistemic_state": "Observed",
            "origin":          "retrieval",
        })

    def _from_node(node: Dict[str, Any], score: float, origin: str) -> Dict[str, Any]:
        return {
            "id":              node["fact_id"],
            "text":            node.get("claim", ""),
            "source":          node.get("source", "memory"),
            "confidence":      node.get("confidence", 1.0),
            "claim_type":      node.get("claim_type", "WORLD_FACT"),
            "source_status":   node.get("source_status", "DERIVED"),
            "significance":    node.get("significance", 0.5),
            "_score":          round(score, 4),
            "epistemic_state": node.get("epistemic_state", "Validated"),
            "origin":          origin,
        }

    # Source 2: L3 canonical memory (recall of what was learned).
    vector_hits = []
    for node in graph.vector_search(q_vec, k=k):
        sim = node.get("_relevance", 0.0)
        if sim < _RETRIEVAL_MIN_SIM:
            continue
        if node.get("restricted"):
            continue  # GDPR Art. 18: restricted facts do not take part in processing
        _offer(_from_node(node, sim * node.get("confidence", 1.0), "memory"))
        vector_hits.append(node)

    # Source 3: multi-hop graph-walk from vector hits (associative recall).
    # Personalized PageRank (without iterating to convergence): activation flows from
    # vector hits along edges, on each hop multiplied by damping and split among
    # outgoing neighbors proportionally to the edge type's weight (_WALK_EDGE_WEIGHTS:
    # truth-maintenance edges weight 0 — do not propagate). What is reachable via SEVERAL
    # paths is summed — well-connected "hubs" rise. Only Validated nodes
    # propagate and are returned; activation is not poured into seed hits (they have
    # an authoritative vector score). Depth — _GRAPH_WALK_HOPS, damping <1 +
    # the hop limit guarantee convergence without blowing up on cycles.
    seeds = {hit["fact_id"] for hit in vector_hits}
    graph_score: Dict[str, float] = {}
    node_cache: Dict[str, Dict[str, Any]] = {}
    current = {
        hit["fact_id"]: hit.get("_relevance", 0.0) * hit.get("confidence", 1.0)
        for hit in vector_hits
    }
    for _hop in range(_GRAPH_WALK_HOPS):
        nxt: Dict[str, float] = {}
        for fid, act in current.items():
            # Outgoing edges by type → weight; only edges with
            # weight > 0 propagate to Validated nodes. Activation is split proportionally to weights
            # (normalized by their sum), not by raw out-degree — edges with
            # weight 0 do not "eat" a neighbor's share.
            targets = []
            for edge in graph.get_edges(fid):
                weight = _WALK_EDGE_WEIGHTS.get(
                    edge["rel_type"], _WALK_DEFAULT_EDGE_WEIGHT)
                if weight <= 0.0:
                    continue
                node = graph.get_fact(edge["target"])
                if node is None or node.get("epistemic_state") != "Validated":
                    continue
                if node.get("restricted"):
                    continue  # GDPR Art. 18: do not propagate activation to restricted facts
                targets.append((node, weight))
            total_weight = sum(w for _, w in targets)
            if total_weight <= 0.0:
                continue
            for node, weight in targets:
                nid = node["fact_id"]
                if nid in seeds:
                    continue  # do not pour activation into vector hits
                share = act * _GRAPH_WALK_DECAY * (weight / total_weight)
                nxt[nid] = nxt.get(nid, 0.0) + share
                node_cache[nid] = node
        if not nxt:
            break
        for nid, val in nxt.items():
            graph_score[nid] = graph_score.get(nid, 0.0) + val
        current = nxt

    for nid, score in graph_score.items():
        _offer(_from_node(node_cache[nid], score, "graph"))

    return sorted(by_id.values(), key=lambda x: x["_score"], reverse=True)[:k]


# ─── FACTS PACK ───────────────────────────────────────────────────────────────

def build_facts_pack(
    retrieved: List[Dict[str, Any]],
    query: str,
) -> Dict[str, Any]:
    """
    Assemble a FactsPack from the retrieved facts.
    Each fact is stored in L0/L1 memory via store_fact().
    truth_status = UNVERIFIED until passing the TruthGate.
    epistemic_state is taken from retrieve() — the owner of the initial ESM state.
    """
    facts: List[Dict[str, Any]] = []

    for item in retrieved:
        fact_id = item.get("id") or item.get("fact_id")
        if not fact_id:
            continue  # consistent with build_trace: skip entries without an id

        fact = {
            "fact_id":         fact_id,
            "claim":           item["text"],
            "source":          item["source"],
            # confidence — EPISTEMIC confidence (from the source or the L3 canon),
            # not a relevance rank. Previously item["_score"]
            # (similarity × confidence) was written here, and that value traveled via merge_fact
            # into the canon, silently eroding the node's confidence on EVERY recall (sim ≤ 1 →
            # confidence only fell). The relevance rank lives separately, in
            # _score, and does not reach the canon (see _l3_payload).
            "confidence":      round(float(item.get("confidence", item.get("_score", 0.5))), 4),
            "epistemic_state": item["epistemic_state"],  # from retrieve(), not duplicated
            # retrieval facts — claims about the world from an external source.
            "claim_type":      item.get("claim_type", "WORLD_FACT"),
            "source_status":   item.get("source_status", "EXTERNAL"),
            "significance":    item.get("significance", 0.5),
            "truth_status":    "UNVERIFIED",
        }
        # L0/L1 store (store_fact does not persist the transient _score).
        store_fact(fact)
        # _score — the relevance rank, only for ordering the pack; not written
        # to the canon (_l3_payload takes the clean persistent record without _score).
        fact["_score"] = round(float(item.get("_score", fact["confidence"])), 4)
        facts.append(fact)

    # retrieve() already returns facts by descending _score; we rank by relevance
    # (_score), not by confidence — these are different axes.
    facts.sort(key=lambda x: x["_score"], reverse=True)

    return {
        "facts": facts,
        "query": query,
        "total": len(facts),
    }


# ─── GUARDIAN ─────────────────────────────────────────────────────────────────
# Structural check — the last line of defense before the answer.
# 0 tokens · synchronous · Fast Path.

def guardian(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> tuple[bool, Optional[str]]:
    """
    Checks the structural integrity of the FactsPack and Trace.
    Returns (passed: bool, reason: str | None).
    """
    facts = facts_pack.get("facts", [])

    if not facts:
        return False, "FactsPack is empty"
    if not trace:
        return False, "Trace is empty — provenance is missing"
    if len(trace) < len(facts):
        return False, f"Mismatch: {len(facts)} facts, {len(trace)} trace elements"

    for fact in facts:
        if not fact.get("fact_id"):
            return False, f"Fact without fact_id: {fact}"
        if not fact.get("claim"):
            return False, f"Fact without claim: {fact['fact_id']}"
        if not fact.get("source"):
            return False, f"Fact without source: {fact['fact_id']}"
        if fact.get("confidence", 0) <= 0:
            return False, f"Zero confidence: {fact['fact_id']}"

    return True, None


# ─── TRUTH GATE ───────────────────────────────────────────────────────────────
# The only entry into the L3 graph. Bypassing it = an architectural bug.
# TODO Sprint 2: full ESM transition matrix, Laplace confidence.

def truth_gate(
    facts_pack: Dict[str, Any],
    min_confidence: Optional[float] = None,
) -> tuple[bool, Optional[str]]:
    """
    Verifies facts before writing to L3.
    min_confidence=None → adaptive threshold (epigenetic verification, RFC0071):
    after blocks the threshold rises (more defensive), under a healthy flow — it relaxes.
    Returns (passed: bool, reason: str | None).

    Type-aware: the gate does NOT throw out the subjective, but does not let it
    masquerade as a fact about the world.
      - WORLD_FACT      → requires source + confidence ≥ threshold.
      - subjective      → pass without an evidentiary bar (a feeling is real
        (EMOTION, OPINION…)  as a feeling), but will not become WORLD_FACT.
      - LLM_OUTPUT      → cannot be WORLD_FACT by itself.

    Transitioning facts into the Validated ESM state is done by the caller
    (run()) when passed=True. truth_gate() only makes the verification decision.
    """
    if min_confidence is None:
        min_confidence = adaptation.verification_threshold()
    facts = facts_pack.get("facts", [])

    if not facts:
        return False, "No facts to verify"

    for fact in facts:
        if not fact.get("source"):
            return False, f"Fact without source: {fact.get('fact_id')}"

        claim_type = fact.get("claim_type", "WORLD_FACT")

        # An LLM output by itself is not a fact about the external world.
        if claim_type == "WORLD_FACT" and fact.get("source_status") == "LLM_OUTPUT":
            return False, (
                f"LLM_OUTPUT cannot be WORLD_FACT without an independent source: "
                f"{fact.get('fact_id')}"
            )

        # Subjective claims are valid as experience — without an evidentiary bar.
        if claim_type in SUBJECTIVE_CLAIM_TYPES:
            continue

        # WORLD_FACT and INTERPRETATION — require a minimum confidence.
        if fact.get("confidence", 0) < min_confidence:
            return False, (
                f"Confidence {fact['confidence']} < threshold {min_confidence}: "
                f"{fact.get('fact_id')}"
            )

    return True, None


def _truth_status_for(claim_type: str, source_status: Optional[str] = None) -> str:
    """
    Source-aware truth status by claim modality (issue #63).

    WORLD_FACT truth status depends on origin:
      EXTERNAL / DERIVED / OBSERVED  → VERIFIED  (independently sourced knowledge)
      USER_REPORTED                  → USER_CLAIMED (stored as recalled, not yet verified)
      LLM_OUTPUT                     → UNVERIFIED (blocked by truth_gate, but defensive)
      UNKNOWN / None                 → UNVERIFIED

    A user saying "Earth orbits the Sun" is a USER_CLAIMED world claim, not a
    VERIFIED fact — even if it is true. VERIFIED requires an independent external
    source or evidence span.
    """
    if claim_type == "WORLD_FACT":
        if source_status in {"EXTERNAL", "DERIVED", "OBSERVED"}:
            return "VERIFIED"
        if source_status == "USER_REPORTED":
            return "USER_CLAIMED"
        return "UNVERIFIED"
    if claim_type == "INTERPRETATION":
        return "HYPOTHESIS"
    return "SUBJECTIVE"


# ─── GENERATION ───────────────────────────────────────────────────────────────
# The answer is formed by a pluggable Generator (core/generation.py): default — extractive,
# optionally — an LLM (Claude) with the FactsPack in system. The graph remains the source of truth.

def _public_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Strip facts of internal service fields (keys prefixed with '_', e.g.
    the transient _score) before returning to the caller. The relevance rank is
    a retrieval detail, not part of the answer; it also does not reach the canon (see _l3_payload).
    """
    return [{k: v for k, v in f.items() if not k.startswith("_")} for f in facts]


def generate_answer(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate an answer from verified facts via get_generator().
    Default backend extractive (concatenation); LLM — via VELANTRIM_GENERATOR=anthropic.
    """
    validated_facts = [
        f for f in facts_pack["facts"]
        if f.get("epistemic_state") in {"Validated", "Supported"}
    ]
    if not validated_facts:
        # Issue #64: a verifiable memory system must not answer from unvalidated
        # material. No Validated/Supported facts → insufficient grounding → block.
        logger.warning(
            "generate_answer: no Validated/Supported facts — blocking answer "
            "(%d unvalidated fact(s) present but not usable as grounding)",
            len(facts_pack["facts"]),
        )
        return {
            "answer":      None,
            "error":       "insufficient grounding: no Validated or Supported facts available",
            "query":       facts_pack.get("query", ""),
            "facts":       [],
            "trace":       trace,
            "trace_fmt":   format_trace(trace),
            "total_facts": 0,
        }

    answer = get_generator().generate(facts_pack.get("query", ""), validated_facts)

    return {
        "answer":       answer,
        "query":        facts_pack.get("query", ""),
        "facts":        _public_facts(validated_facts),
        "trace":        trace,
        "trace_fmt":    format_trace(trace),
        "total_facts":  len(validated_facts),
    }


# ─── EPISODIC BINDING ─────────────────────────────────────────────────────────
# Episodic memory: "what-where-when-with-whom". Facts recalled together are
# linked in L3 by an undirected pair of CO_OCCURRED edges with the episode context.
# The edges connect already validated nodes — this is not a TruthGate bypass (it guards
# only a fact node's entry into the canon).

_EPISODE_REL = "CO_OCCURRED"


def _entity_refs(episode: Dict[str, Any]) -> List[tuple]:
    """Episode entities → [(entity_id, kind, label)] for who/where."""
    refs = []
    for name in (episode.get("who") or []):
        refs.append((f"who:{name}", "person", name))
    where = episode.get("where")
    if where is not None:
        refs.append((f"where:{where}", "place", where))
    return refs


def _link_episode(
    graph,
    facts: List[Dict[str, Any]],
    query: str,
    episode: Optional[Dict[str, Any]],
) -> None:
    """Link co-recalled facts by an episode: who/where → entity nodes (for any
    number of facts) + a CO_OCCURRED edge between pairs (at least two facts)."""
    ids = [f["fact_id"] for f in facts]
    episode = episode or {}

    # First-class who/where entity nodes: each fact mentions the entity.
    for entity_id, kind, label in _entity_refs(episode):
        graph.merge_entity(entity_id, kind, label)
        for fid in ids:
            graph.link_fact_to_entity(fid, entity_id)

    if len(ids) < 2:
        return  # an episodic edge needs at least two facts

    props: Dict[str, Any] = {
        "query": query,
        "when": episode.get("when") or datetime.now(timezone.utc).isoformat(),
    }
    for key in ("who", "where", "event"):
        if episode.get(key) is not None:
            props[key] = episode[key]

    # A chain of adjacent pairs (not all pairs) — O(n) links, enough for an episode.
    for a, b in zip(ids, ids[1:]):
        graph.add_edge(a, _EPISODE_REL, b, props)
        graph.add_edge(b, _EPISODE_REL, a, props)

    # L1.5 Velum (RFC0016): feed the co-recalled set to the synaptic pre-graph as a
    # fire-and-forget hint. Velum is NOT a source of facts (I3) and must never
    # break the pipeline, so failures are swallowed.
    try:
        from core.velum import get_velum
        get_velum().observe_episode(query, ids)
    except Exception:  # noqa: BLE001 — a hint layer must not affect the canon
        pass


def recall_episode(fact_id: str) -> List[Dict[str, Any]]:
    """
    Episodic recall: with which facts and in what context (who/where/when/
    query) this fact was recalled together. Reads CO_OCCURRED edges — makes
    the episodic data that _link_episode wrote queryable.
    """
    out: List[Dict[str, Any]] = []
    for edge in get_l3_graph().get_edges(fact_id, _EPISODE_REL):
        props = edge.get("props", {})
        out.append({
            "with":  edge["target"],
            "who":   props.get("who"),
            "where": props.get("where"),
            "when":  props.get("when"),
            "query": props.get("query"),
        })
    return out


def recall_by_entity(
    *, who: Optional[str] = None, where: Optional[str] = None,
) -> List[str]:
    """
    Recall by entity: ids of facts mentioning a person/place. A direct reverse
    traversal of first-class entity nodes (facts_for_entity), not an edge scan.
    who/where are combined by union.
    """
    if who is None and where is None:
        return []
    graph = get_l3_graph()
    matched = set()
    if who is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"who:{who}"))
    if where is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"where:{where}"))
    return sorted(matched)


# ─── MAIN PIPELINE ────────────────────────────────────────────────────────────

def _l3_payload(fact: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonical payload for merge_fact: take the PERSISTENT record from L0/L1
    (get_fact) — with created_at / updated_at / metadata — and overlay truth_status
    (it is not among the SQLite columns, it lives only in the canon).

    Why: previously a "bare" in-memory fact without created_at/metadata went to L3, and
    SleepCycle (consolidate) did not find a reference timestamp → decay was NEVER
    applied to freshly ingested nodes until reconcile touched them. The clean
    persistent record fixes this and guarantees that the real confidence reaches the canon,
    not the transient _score (which is not in the record).
    """
    record = get_fact(fact["fact_id"]) or fact
    return {**record, "truth_status": fact.get("truth_status")}


def drain_l3_outbox(graph=None) -> int:
    """
    Re-merge into L3 the facts whose write to the canon previously failed (self-heal).

    L3 and SQLite do not share a transaction: on a merge failure a fact stays Validated in
    SQLite but without a node in the graph (see enqueue in run()). Here we idempotently
    retry the MERGE for the queue and remove the successful ones. If the backend is still
    unavailable — we leave it in the queue and stop trying until next time.
    Returns the number of successfully re-merged facts.
    """
    graph = graph or get_l3_graph()
    queue = get_outbox_queue()
    healed = 0
    for fid in queue.pending():
        fact = get_fact(fid)
        if fact is None:
            queue.clear(fid)  # the fact vanished from SQLite — drop the stale entry
            continue
        fact["truth_status"] = _truth_status_for(fact.get("claim_type", "WORLD_FACT"), fact.get("source_status"))
        try:
            graph.merge_fact(_l3_payload(fact))
        except Exception as e:  # noqa: BLE001 — backend still unavailable, do not lose the queue
            logger.warning(
                "drain_l3_outbox: %s is still waiting (%s)", fid, type(e).__name__)
            break
        queue.clear(fid)
        healed += 1
    return healed


def run(query: str, episode: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    The full Velantrim pipeline:
    Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer

    Principle: Trace → Validation → Answer.
    Not the other way around.

    episode — optional episode context (who / where / when / event):
    facts recalled together are linked in L3 by an episodic edge.
    """
    metrics.incr("query.total")
    # 0. Self-heal: re-merge facts whose write to L3 previously failed (outbox).
    drain_l3_outbox()
    # 1. Retrieval
    retrieved = retrieve(query)
    if not retrieved:
        return _blocked("Retrieval returned 0 results.", query)

    # 2. FactsPack
    facts_pack = build_facts_pack(retrieved, query)

    # 3. Trace
    trace = build_trace(retrieved)

    # 4. Guardian (structural check)
    guardian_ok, guardian_reason = guardian(facts_pack, trace)
    if not guardian_ok:
        adaptation.record_block()   # stress → verification rises (RFC0071)
        return _blocked(f"Guardian: {guardian_reason}", query, facts_pack, trace)

    # 5. TruthGate (verification)
    gate_ok, gate_reason = truth_gate(facts_pack)
    if not gate_ok:
        adaptation.record_block()
        return _blocked(f"TruthGate: {gate_reason}", query, facts_pack, trace)

    # 6. ESM: transition facts and trace to Validated via transition_esm (the only path).
    #    truth_status is set by claim_type: VERIFIED only for WORLD_FACT,
    #    the subjective is validated as experience (Validated), but does not become truth about the world.
    #
    #    Cross-store nuance: SQLite (pending) and L3 (canon) — two stores without a shared
    #    transaction. We catch a write failure to L3 and return _blocked, rather than crash
    #    the pipeline with a traceback. Partial state self-heals: failed
    #    facts are put into the outbox (enqueue_l3_write) and idempotently re-merged on the
    #    next access (drain_l3_outbox, step 0). The source of truth is the graph,
    #    SQLite is just a pending cache.
    graph = get_l3_graph()
    try:
        for fact in facts_pack["facts"]:
            # A recall fact from L3 is already Validated — a repeated transition is not allowed in
            # the ESM matrix, so we only transition the not-yet-validated ones.
            if fact.get("epistemic_state") != "Validated":
                transition_esm(fact["fact_id"], "Validated")
                updated = get_fact(fact["fact_id"])
                if updated:
                    fact["epistemic_state"] = updated["epistemic_state"]
            fact["truth_status"] = _truth_status_for(fact.get("claim_type", "WORLD_FACT"), fact.get("source_status"))
            # The only entry into L3: the canonical MERGE strictly after the TruthGate.
            # We merge the persistent record (created_at/metadata → for SleepCycle),
            # not the transient fact with _score (see _l3_payload).
            graph.merge_fact(_l3_payload(fact))
        # 6b. Episodic binding: facts recalled in one query are linked.
        _link_episode(graph, facts_pack["facts"], query, episode)
    except Exception as e:  # noqa: BLE001 — an L3 failure must not crash the pipeline
        logger.error("L3 promotion failed: %s", e)
        adaptation.record_block()
        # We put the failed facts into the outbox — they will be re-merged on the next access.
        queue = get_outbox_queue()
        for f in facts_pack["facts"]:
            queue.enqueue(f["fact_id"])
        return _blocked(f"L3 promotion failed: {e}", query, facts_pack, trace)

    promote_trace(trace, "Validated")

    # 7. Generate
    metrics.incr("query.answered")
    adaptation.record_success()     # a healthy outcome → the threshold relaxes
    return generate_answer(facts_pack, trace)


def _blocked(
    reason: str,
    query: str,
    facts_pack: Optional[Dict] = None,
    trace: Optional[List] = None,
) -> Dict[str, Any]:
    """Standard response when the pipeline is blocked."""
    metrics.incr("query.blocked")
    return {
        "error":  reason,
        "answer": None,
        "query":  query,
        "facts":  _public_facts(facts_pack.get("facts", [])) if facts_pack else [],
        "trace":  trace or [],
    }


# ─── TEST ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    queries = [
        "What is quantum entanglement?",
        "How does DNA work?",
        "Tell me about the Sun",
    ]
    for q in queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {q}")
        result = run(q)
        print(f"ANSWER: {result.get('answer', 'BLOCKED')}")
        if result.get("error"):
            print(f"ERROR:  {result['error']}")
        if result.get("trace_fmt"):
            print(result["trace_fmt"])
