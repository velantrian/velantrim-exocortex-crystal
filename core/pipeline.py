# core/pipeline.py
# Velantrim ExoCortex — Core Pipeline
#
# Principle: Graph = Truth · LLM = Language · Memory = Physiology
# Pipeline: Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer

import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from core.trace import build_trace, promote_trace, format_trace
from core.memory import (
    store_fact, get_fact, transition_esm, ESM_TRANSITIONS,
)
from core.queue import get_outbox_queue
from core.l3_graph import get_l3_graph
from core.embedding import get_embedder, cosine, assert_compatible_embedder
from core.retrieval_config import get_retrieval_config
from core.generation import get_generator
from core.response_policy import (
    ResponsePolicyInput,
    decide_response_policy,
)
from core import metrics, adaptation

logger = logging.getLogger(__name__)


def _load_demo_seed():
    """Return demo seed facts when VELANTRIM_DEMO_SEED=1, else empty list."""
    import os
    if os.environ.get("VELANTRIM_DEMO_SEED", "0") == "1":
        from core.demo_seed import DEMO_FACTS
        return DEMO_FACTS
    return []


_WALK_EDGE_WEIGHTS = {
    "CONTRADICTS": 0.0,
    "SUPERSEDED_BY": 0.0,
}
_WALK_DEFAULT_EDGE_WEIGHT = 1.0


def retrieve(query: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Hybrid search: cosine of embeddings over demo seed facts (opt-in) and
    L3 canon, then a multi-hop graph-walk. Returns top-k by relevance score.
    """
    cfg = get_retrieval_config()
    if k is None:
        k = cfg.k
    min_sim = cfg.min_similarity
    embedder = get_embedder()
    graph = get_l3_graph()
    assert_compatible_embedder(graph)
    q_vec = embedder.embed(query)
    by_id: Dict[str, Dict[str, Any]] = {}

    def _offer(item: Dict[str, Any]) -> None:
        prev = by_id.get(item["id"])
        if prev is None or item["_score"] > prev["_score"]:
            by_id[item["id"]] = item

    for item in _load_demo_seed():
        sim = cosine(q_vec, embedder.embed(item["text"]))
        if sim < min_sim:
            continue
        _offer({
            **item,
            "_score": round(sim * item.get("confidence", 1.0), 4),
            "epistemic_state": "Observed",
            "origin": "retrieval",
        })

    def _from_node(node: Dict[str, Any], score: float, origin: str) -> Dict[str, Any]:
        return {
            "id": node["fact_id"],
            "text": node.get("claim", ""),
            "source": node.get("source", "memory"),
            "confidence": node.get("confidence", 1.0),
            "claim_type": node.get("claim_type", "WORLD_FACT"),
            "source_status": node.get("source_status", "DERIVED"),
            "significance": node.get("significance", 0.5),
            "_score": round(score, 4),
            "epistemic_state": node.get("epistemic_state", "Validated"),
            "origin": origin,
        }

    vector_hits = []
    for node in graph.vector_search(q_vec, k=k):
        sim = node.get("_relevance", 0.0)
        if sim < min_sim:
            continue
        if node.get("restricted"):
            continue
        _offer(_from_node(node, sim * node.get("confidence", 1.0), "memory"))
        vector_hits.append(node)

    seeds = {hit["fact_id"] for hit in vector_hits}
    graph_score: Dict[str, float] = {}
    node_cache: Dict[str, Dict[str, Any]] = {}
    current = {
        hit["fact_id"]: hit.get("_relevance", 0.0) * hit.get("confidence", 1.0)
        for hit in vector_hits
    }
    for _hop in range(cfg.graph_walk_hops):
        nxt: Dict[str, float] = {}
        for fid, act in current.items():
            targets = []
            for edge in graph.get_edges(fid):
                weight = _WALK_EDGE_WEIGHTS.get(
                    edge["rel_type"], _WALK_DEFAULT_EDGE_WEIGHT
                )
                if weight <= 0.0:
                    continue
                node = graph.get_fact(edge["target"])
                if node is None or node.get("epistemic_state") != "Validated":
                    continue
                if node.get("restricted"):
                    continue
                targets.append((node, weight))
            total_weight = sum(w for _, w in targets)
            if total_weight <= 0.0:
                continue
            for node, weight in targets:
                nid = node["fact_id"]
                if nid in seeds:
                    continue
                share = act * cfg.graph_walk_decay * (weight / total_weight)
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


def build_facts_pack(
    retrieved: List[Dict[str, Any]],
    query: str,
) -> Dict[str, Any]:
    """Assemble a FactsPack from retrieved facts and store them in L0/L1."""
    facts: List[Dict[str, Any]] = []

    for item in retrieved:
        fact_id = item.get("id") or item.get("fact_id")
        if not fact_id:
            continue
        fact = {
            "fact_id": fact_id,
            "claim": item["text"],
            "source": item["source"],
            "confidence": round(float(item.get("confidence", item.get("_score", 0.5))), 4),
            "epistemic_state": item["epistemic_state"],
            "claim_type": item.get("claim_type", "WORLD_FACT"),
            "source_status": item.get("source_status", "EXTERNAL"),
            "significance": item.get("significance", 0.5),
            "truth_status": "UNVERIFIED",
        }
        store_fact(fact)
        persisted = get_fact(fact_id)
        if persisted:
            fact["epistemic_state"] = persisted["epistemic_state"]
        fact["_score"] = round(float(item.get("_score", fact["confidence"])), 4)
        facts.append(fact)

    facts.sort(key=lambda x: x["_score"], reverse=True)
    return {
        "facts": facts,
        "query": query,
        "total": len(facts),
    }


def guardian(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> tuple[bool, Optional[str]]:
    """Check structural integrity of the FactsPack and Trace."""
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


from core.truth_gate import truth_gate  # noqa: E402  (re-export, see module contract)


def _truth_status_for(claim_type: str, source_status: Optional[str] = None) -> str:
    """Source-aware truth status by claim modality."""
    if claim_type == "WORLD_FACT":
        if source_status in {"EXTERNAL", "DERIVED", "OBSERVED"}:
            return "VERIFIED"
        if source_status == "USER_REPORTED":
            return "USER_CLAIMED"
        return "UNVERIFIED"
    if claim_type == "INTERPRETATION":
        return "HYPOTHESIS"
    return "SUBJECTIVE"


def _public_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Strip internal service fields before returning facts to callers."""
    return [{k: v for k, v in f.items() if not k.startswith("_")} for f in facts]


def _response_policy_for_fact(fact: Dict[str, Any]) -> Dict[str, Any]:
    """Read-path response_policy metadata for one already-selected fact."""
    decision = decide_response_policy(
        ResponsePolicyInput(
            claim_type=fact.get("claim_type", "WORLD_FACT"),
            source_status=fact.get("source_status", "UNKNOWN"),
            epistemic_state=fact.get("epistemic_state", "Hypothesized"),
            truth_status=fact.get("truth_status"),
            risk_domain=fact.get("risk_domain", "GENERAL"),
            mode_hint=fact.get("mode_hint"),
        )
    )
    return {
        "fact_id": fact.get("fact_id"),
        "action": decision.action,
        "reason": decision.reason,
        "requires_citation": decision.requires_citation,
    }


def _response_policy_for_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build response_policy metadata for selected read-path facts."""
    return [_response_policy_for_fact(f) for f in facts]


def generate_answer(
    facts_pack: Dict[str, Any],
    trace: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Generate an answer from Validated/Supported facts via get_generator()."""
    validated_facts = [
        f for f in facts_pack["facts"]
        if f.get("epistemic_state") in {"Validated", "Supported"}
    ]
    if not validated_facts:
        logger.warning(
            "generate_answer: no Validated/Supported facts — blocking answer "
            "(%d unvalidated fact(s) present but not usable as grounding)",
            len(facts_pack["facts"]),
        )
        return {
            "answer": None,
            "error": "insufficient grounding: no Validated or Supported facts available",
            "query": facts_pack.get("query", ""),
            "facts": [],
            "response_policy": [],
            "trace": trace,
            "trace_fmt": format_trace(trace),
            "total_facts": 0,
        }

    answer = get_generator().generate(facts_pack.get("query", ""), validated_facts)
    response_policy = _response_policy_for_facts(validated_facts)

    return {
        "answer": answer,
        "query": facts_pack.get("query", ""),
        "facts": _public_facts(validated_facts),
        "response_policy": response_policy,
        "trace": trace,
        "trace_fmt": format_trace(trace),
        "total_facts": len(validated_facts),
    }


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
    """Link co-recalled facts by episode context."""
    ids = [f["fact_id"] for f in facts]
    episode = episode or {}

    for entity_id, kind, label in _entity_refs(episode):
        graph.merge_entity(entity_id, kind, label)
        for fid in ids:
            graph.link_fact_to_entity(fid, entity_id)

    if len(ids) < 2:
        return

    props: Dict[str, Any] = {
        "query": query,
        "when": episode.get("when") or datetime.now(timezone.utc).isoformat(),
    }
    for key in ("who", "where", "event"):
        if episode.get(key) is not None:
            props[key] = episode[key]

    for a, b in zip(ids, ids[1:]):
        graph.add_edge(a, _EPISODE_REL, b, props)
        graph.add_edge(b, _EPISODE_REL, a, props)

    try:
        from core.velum import get_velum
        get_velum().observe_episode(query, ids)
    except Exception:  # noqa: BLE001 — a hint layer must not affect the canon
        pass


def recall_episode(fact_id: str) -> List[Dict[str, Any]]:
    """Read episodic CO_OCCURRED edges for one fact."""
    out: List[Dict[str, Any]] = []
    for edge in get_l3_graph().get_edges(fact_id, _EPISODE_REL):
        props = edge.get("props", {})
        out.append({
            "with": edge["target"],
            "who": props.get("who"),
            "where": props.get("where"),
            "when": props.get("when"),
            "query": props.get("query"),
        })
    return out


def recall_by_entity(
    *, who: Optional[str] = None, where: Optional[str] = None,
) -> List[str]:
    """Recall ids of facts mentioning a person/place entity."""
    if who is None and where is None:
        return []
    graph = get_l3_graph()
    matched = set()
    if who is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"who:{who}"))
    if where is not None:
        matched.update(n["fact_id"] for n in graph.facts_for_entity(f"where:{where}"))
    return sorted(matched)


def _l3_payload(fact: Dict[str, Any]) -> Dict[str, Any]:
    """Canonical payload for merge_fact."""
    record = get_fact(fact["fact_id"]) or fact
    return {**record, "truth_status": fact.get("truth_status")}


def drain_l3_outbox(graph=None) -> int:
    """Retry L3 writes whose earlier canonical merge failed."""
    graph = graph or get_l3_graph()
    queue = get_outbox_queue()
    healed = 0
    for fid in queue.pending():
        fact = get_fact(fid)
        if fact is None:
            queue.clear(fid)
            continue
        fact["truth_status"] = _truth_status_for(
            fact.get("claim_type", "WORLD_FACT"), fact.get("source_status")
        )
        try:
            graph.merge_fact(_l3_payload(fact))
        except Exception as e:  # noqa: BLE001 — backend still unavailable
            logger.warning(
                "drain_l3_outbox: %s is still waiting (%s)", fid, type(e).__name__
            )
            break
        queue.clear(fid)
        healed += 1
    return healed


def run(query: str, episode: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Full pipeline: Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer."""
    metrics.incr("query.total")
    drain_l3_outbox()
    retrieved = retrieve(query)

    try:
        from core import neurocore
        if neurocore.enabled():
            top = max((float(f.get("_score", 0.0)) for f in retrieved), default=0.0)
            surprise = round(max(0.0, 1.0 - top), 4)
            neurocore.observe(surprise, delta_norm=surprise, domain="pipeline")
    except Exception:  # noqa: BLE001 — Phase 0 tracker must not affect the canon
        pass

    if not retrieved:
        return _blocked("Retrieval returned 0 results.", query)

    facts_pack = build_facts_pack(retrieved, query)
    trace = build_trace(retrieved)

    guardian_ok, guardian_reason = guardian(facts_pack, trace)
    if not guardian_ok:
        adaptation.record_block()
        return _blocked(f"Guardian: {guardian_reason}", query, facts_pack, trace)

    gate_ok, gate_reason = truth_gate(facts_pack)
    if not gate_ok:
        adaptation.record_block()
        return _blocked(f"TruthGate: {gate_reason}", query, facts_pack, trace)

    graph = get_l3_graph()
    try:
        for fact in facts_pack["facts"]:
            if fact.get("epistemic_state") != "Validated":
                if "Validated" not in ESM_TRANSITIONS.get(
                    fact.get("epistemic_state", "Observed"), set()
                ):
                    continue
                if not transition_esm(fact["fact_id"], "Validated"):
                    continue
                updated = get_fact(fact["fact_id"])
                if updated:
                    fact["epistemic_state"] = updated["epistemic_state"]
            fact["truth_status"] = _truth_status_for(
                fact.get("claim_type", "WORLD_FACT"), fact.get("source_status")
            )
            graph.merge_fact(_l3_payload(fact))
        _link_episode(graph, facts_pack["facts"], query, episode)
    except Exception as e:  # noqa: BLE001 — an L3 failure must not crash the pipeline
        logger.error("L3 promotion failed: %s", e)
        adaptation.record_block()
        queue = get_outbox_queue()
        for f in facts_pack["facts"]:
            queue.enqueue(f["fact_id"])
        return _blocked(f"L3 promotion failed: {e}", query, facts_pack, trace)

    promote_trace(trace, "Validated")
    metrics.incr("query.answered")
    adaptation.record_success()
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
        "error": reason,
        "answer": None,
        "query": query,
        "facts": _public_facts(facts_pack.get("facts", [])) if facts_pack else [],
        "response_policy": [],
        "trace": trace or [],
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    queries = [
        "What is quantum entanglement?",
        "How does DNA work?",
        "Tell me about the Sun",
    ]
    for q in queries:
        print(f"\n{'=' * 60}")
        print(f"QUERY: {q}")
        result = run(q)
        print(f"ANSWER: {result.get('answer', 'BLOCKED')}")
        if result.get("error"):
            print(f"ERROR:  {result['error']}")
        if result.get("trace_fmt"):
            print(result["trace_fmt"])
