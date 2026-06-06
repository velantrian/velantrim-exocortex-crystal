# core/pipeline.py
# Velantrim ExoCortex — Core Pipeline
# Principle: Graph = Truth · LLM = Language · Memory = Physiology

import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from core.trace import build_trace, promote_trace, format_trace
from core.memory import (
    store_fact, get_fact, transition_esm, SUBJECTIVE_CLAIM_TYPES,
    enqueue_l3_write, pending_l3_writes, clear_l3_write,
)
from core.l3_graph import get_l3_graph
from core.embedding import get_embedder, cosine, assert_compatible_embedder
from core.generation import get_generator
from core import metrics, adaptation

logger = logging.getLogger(__name__)

DATABASE = [
    {"id": "f1", "text": "Water boils at 100°C at sea level", "source": "physics", "confidence": 0.99},
    {"id": "f2", "text": "Quantum entanglement links particles", "source": "physics", "confidence": 0.85},
    {"id": "f3", "text": "Earth revolves around the Sun", "source": "astronomy", "confidence": 0.99},
    {"id": "f4", "text": "The human brain has ~86 billion neurons", "source": "neuroscience", "confidence": 0.90},
    {"id": "f5", "text": "DNA encodes genetic information", "source": "biology", "confidence": 0.99},
]

_RETRIEVAL_MIN_SIM = 0.05
_GRAPH_WALK_DECAY = 0.5
_GRAPH_WALK_HOPS = 2
_WALK_EDGE_WEIGHTS = {"CONTRADICTS": 0.0, "SUPERSEDED_BY": 0.0}
_WALK_DEFAULT_EDGE_WEIGHT = 1.0
_EPISODE_REL = "CO_OCCURRED"


def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """Hybrid search over seed corpus, L3 vector recall, and graph walk."""
    embedder = get_embedder()
    graph = get_l3_graph()
    assert_compatible_embedder(graph)
    q_vec = embedder.embed(query)
    by_id: Dict[str, Dict[str, Any]] = {}

    def offer(item: Dict[str, Any]) -> None:
        prev = by_id.get(item["id"])
        if prev is None or item["_score"] > prev["_score"]:
            by_id[item["id"]] = item

    for item in DATABASE:
        sim = cosine(q_vec, embedder.embed(item["text"]))
        if sim >= _RETRIEVAL_MIN_SIM:
            offer({**item, "_score": round(sim * item.get("confidence", 1.0), 4),
                   "epistemic_state": "Observed", "origin": "retrieval"})

    def from_node(node: Dict[str, Any], score: float, origin: str) -> Dict[str, Any]:
        return {
            "id": node["fact_id"], "text": node.get("claim", ""),
            "source": node.get("source", "memory"),
            "confidence": node.get("confidence", 1.0),
            "claim_type": node.get("claim_type", "WORLD_FACT"),
            "source_status": node.get("source_status", "DERIVED"),
            "truth_status": node.get("truth_status", "UNVERIFIED"),
            "significance": node.get("significance", 0.5),
            "_score": round(score, 4),
            "epistemic_state": node.get("epistemic_state", "Validated"),
            "origin": origin,
        }

    vector_hits = []
    for node in graph.vector_search(q_vec, k=k):
        sim = node.get("_relevance", 0.0)
        if sim < _RETRIEVAL_MIN_SIM or node.get("restricted"):
            continue
        offer(from_node(node, sim * node.get("confidence", 1.0), "memory"))
        vector_hits.append(node)

    seeds = {hit["fact_id"] for hit in vector_hits}
    graph_score: Dict[str, float] = {}
    node_cache: Dict[str, Dict[str, Any]] = {}
    current = {hit["fact_id"]: hit.get("_relevance", 0.0) * hit.get("confidence", 1.0)
               for hit in vector_hits}
    for _ in range(_GRAPH_WALK_HOPS):
        nxt: Dict[str, float] = {}
        for fid, act in current.items():
            targets = []
            for edge in graph.get_edges(fid):
                weight = _WALK_EDGE_WEIGHTS.get(edge["rel_type"], _WALK_DEFAULT_EDGE_WEIGHT)
                if weight <= 0.0:
                    continue
                node = graph.get_fact(edge["target"])
                if node is None or node.get("epistemic_state") != "Validated" or node.get("restricted"):
                    continue
                targets.append((node, weight))
            total = sum(w for _, w in targets)
            if total <= 0.0:
                continue
            for node, weight in targets:
                nid = node["fact_id"]
                if nid in seeds:
                    continue
                share = act * _GRAPH_WALK_DECAY * (weight / total)
                nxt[nid] = nxt.get(nid, 0.0) + share
                node_cache[nid] = node
        if not nxt:
            break
        for nid, val in nxt.items():
            graph_score[nid] = graph_score.get(nid, 0.0) + val
        current = nxt

    for nid, score in graph_score.items():
        offer(from_node(node_cache[nid], score, "graph"))
    return sorted(by_id.values(), key=lambda x: x["_score"], reverse=True)[:k]


def build_facts_pack(retrieved: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
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
            "truth_status": item.get("truth_status", "UNVERIFIED"),
        }
        store_fact(fact)
        fact["_score"] = round(float(item.get("_score", fact["confidence"])), 4)
        facts.append(fact)
    facts.sort(key=lambda x: x["_score"], reverse=True)
    return {"facts": facts, "query": query, "total": len(facts)}


def guardian(facts_pack: Dict[str, Any], trace: List[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
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


def truth_gate(facts_pack: Dict[str, Any], min_confidence: Optional[float] = None) -> tuple[bool, Optional[str]]:
    """Source-aware gate. Passing stores memory; it does not automatically imply VERIFIED truth."""
    if min_confidence is None:
        min_confidence = adaptation.verification_threshold()
    facts = facts_pack.get("facts", [])
    if not facts:
        return False, "No facts to verify"
    for fact in facts:
        if not fact.get("source"):
            return False, f"Fact without source: {fact.get('fact_id')}"
        claim_type = fact.get("claim_type", "WORLD_FACT")
        source_status = fact.get("source_status", "UNKNOWN")
        if claim_type == "WORLD_FACT" and source_status == "LLM_OUTPUT":
            return False, f"LLM_OUTPUT cannot be WORLD_FACT without an independent source: {fact.get('fact_id')}"
        if claim_type in SUBJECTIVE_CLAIM_TYPES:
            continue
        if fact.get("confidence", 0) < min_confidence:
            return False, f"Confidence {fact['confidence']} < threshold {min_confidence}: {fact.get('fact_id')}"
    return True, None


def _truth_status_for(claim_type: str, source_status: Optional[str] = None) -> str:
    """Persistence is not truth; user-reported world claims are USER_CLAIMED."""
    claim_type = claim_type or "WORLD_FACT"
    source_status = source_status or "UNKNOWN"
    if claim_type == "WORLD_FACT":
        if source_status == "USER_REPORTED":
            return "USER_CLAIMED"
        if source_status == "LLM_OUTPUT":
            return "HYPOTHESIS"
        if source_status in {"EXTERNAL", "OBSERVED", "DERIVED"}:
            return "VERIFIED"
        return "UNVERIFIED"
    if claim_type == "INTERPRETATION":
        return "HYPOTHESIS"
    return "SUBJECTIVE"


def _public_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{k: v for k, v in f.items() if not k.startswith("_")} for f in facts]


def generate_answer(facts_pack: Dict[str, Any], trace: List[Dict[str, Any]]) -> Dict[str, Any]:
    validated = [f for f in facts_pack["facts"] if f.get("epistemic_state") in {"Validated", "Supported"}]
    if not validated:
        return {
            "answer": "No validated or supported facts are available for this query.",
            "query": facts_pack.get("query", ""),
            "facts": [],
            "trace": trace,
            "trace_fmt": format_trace(trace),
            "total_facts": 0,
        }
    answer = get_generator().generate(facts_pack.get("query", ""), validated)
    return {"answer": answer, "query": facts_pack.get("query", ""),
            "facts": _public_facts(validated), "trace": trace,
            "trace_fmt": format_trace(trace), "total_facts": len(validated)}


def _entity_refs(episode: Dict[str, Any]) -> List[tuple]:
    refs = []
    for name in (episode.get("who") or []):
        refs.append((f"who:{name}", "person", name))
    where = episode.get("where")
    if where is not None:
        refs.append((f"where:{where}", "place", where))
    return refs


def _link_episode(graph, facts: List[Dict[str, Any]], query: str, episode: Optional[Dict[str, Any]]) -> None:
    ids = [f["fact_id"] for f in facts]
    episode = episode or {}
    for entity_id, kind, label in _entity_refs(episode):
        graph.merge_entity(entity_id, kind, label)
        for fid in ids:
            graph.link_fact_to_entity(fid, entity_id)
    if len(ids) < 2:
        return
    props: Dict[str, Any] = {"query": query, "when": episode.get("when") or datetime.now(timezone.utc).isoformat()}
    for key in ("who", "where", "event"):
        if episode.get(key) is not None:
            props[key] = episode[key]
    for a, b in zip(ids, ids[1:]):
        graph.add_edge(a, _EPISODE_REL, b, props)
        graph.add_edge(b, _EPISODE_REL, a, props)


def recall_episode(fact_id: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for edge in get_l3_graph().get_edges(fact_id, _EPISODE_REL):
        props = edge.get("props", {})
        out.append({"with": edge["target"], "who": props.get("who"),
                    "where": props.get("where"), "when": props.get("when"),
                    "query": props.get("query")})
    return out


def recall_by_entity(*, who: Optional[str] = None, where: Optional[str] = None) -> List[str]:
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
    record = get_fact(fact["fact_id"]) or fact
    return {**record, "truth_status": fact.get("truth_status")}


def drain_l3_outbox(graph=None) -> int:
    graph = graph or get_l3_graph()
    healed = 0
    for fid in pending_l3_writes():
        fact = get_fact(fid)
        if fact is None:
            clear_l3_write(fid)
            continue
        fact["truth_status"] = _truth_status_for(fact.get("claim_type", "WORLD_FACT"), fact.get("source_status"))
        try:
            graph.merge_fact(_l3_payload(fact))
        except Exception as e:  # noqa: BLE001
            logger.warning("drain_l3_outbox: %s is still waiting (%s)", fid, type(e).__name__)
            break
        clear_l3_write(fid)
        healed += 1
    return healed


def run(query: str, episode: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    metrics.incr("query.total")
    drain_l3_outbox()
    retrieved = retrieve(query)
    if not retrieved:
        return _blocked("Retrieval returned 0 results.", query)
    facts_pack = build_facts_pack(retrieved, query)
    trace = build_trace(retrieved)
    ok, reason = guardian(facts_pack, trace)
    if not ok:
        adaptation.record_block()
        return _blocked(f"Guardian: {reason}", query, facts_pack, trace)
    ok, reason = truth_gate(facts_pack)
    if not ok:
        adaptation.record_block()
        return _blocked(f"TruthGate: {reason}", query, facts_pack, trace)

    graph = get_l3_graph()
    try:
        for fact in facts_pack["facts"]:
            if fact.get("epistemic_state") != "Validated":
                transition_esm(fact["fact_id"], "Validated")
                updated = get_fact(fact["fact_id"])
                if updated:
                    fact["epistemic_state"] = updated["epistemic_state"]
            fact["truth_status"] = _truth_status_for(fact.get("claim_type", "WORLD_FACT"), fact.get("source_status"))
            graph.merge_fact(_l3_payload(fact))
        _link_episode(graph, facts_pack["facts"], query, episode)
    except Exception as e:  # noqa: BLE001
        logger.error("L3 promotion failed: %s", e)
        adaptation.record_block()
        for f in facts_pack["facts"]:
            enqueue_l3_write(f["fact_id"])
        return _blocked(f"L3 promotion failed: {e}", query, facts_pack, trace)

    promote_trace(trace, "Validated")
    metrics.incr("query.answered")
    adaptation.record_success()
    return generate_answer(facts_pack, trace)


def _blocked(reason: str, query: str, facts_pack: Optional[Dict] = None,
             trace: Optional[List] = None) -> Dict[str, Any]:
    metrics.incr("query.blocked")
    return {"error": reason, "answer": None, "query": query,
            "facts": _public_facts(facts_pack.get("facts", [])) if facts_pack else [],
            "trace": trace or []}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for q in ["What is quantum entanglement?", "How does DNA work?", "Tell me about the Sun"]:
        print(f"\n{'='*60}\nQUERY: {q}")
        result = run(q)
        print(f"ANSWER: {result.get('answer', 'BLOCKED')}")
        if result.get("error"):
            print(f"ERROR:  {result['error']}")
        if result.get("trace_fmt"):
            print(result["trace_fmt"])
