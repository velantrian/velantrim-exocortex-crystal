# core/query_pipeline.py
# Velantrim ExoCortex — strict read-only query pipeline.
#
# Query is a read operation. It may retrieve and render facts that already exist
# in the L3 graph, but it must never create or update L0/L1 rows, transition ESM,
# drain the L3 outbox, write graph nodes/edges, or trigger research telemetry.

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional

from core import metrics
from core.canonical_view import _normalize_restricted_bit
from core.l3_graph import get_l3_graph
from core.memory import get_fact
from core.pipeline import (
    STORE_STATE_CONFLICT,
    _safe_confidence,
    generate_answer,
    guardian,
    retrieve,
)
from core.retrieval_config import get_retrieval_config
from core.trace import build_trace

_TERMINAL_ESM_STATES = frozenset({"Collapsed", "Contradicted", "Deprecated"})
_QUERY_POLICY = "canonical_read_only"
_DEFAULT_CLAIM_TYPE = "WORLD_FACT"


def _safe_retrieval_score(value: Any) -> float:
    """Return a finite retrieval score for TRACE formatting, else 0.0."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0.0
    try:
        score = float(value)
    except OverflowError:
        return 0.0
    return score if math.isfinite(score) else 0.0


def _public_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{k: v for k, v in fact.items() if not k.startswith("_")} for fact in facts]


def _public_search_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return stable public search rows without leaking private ranking keys."""
    rows: List[Dict[str, Any]] = []
    for fact in facts:
        row = {k: v for k, v in fact.items() if not k.startswith("_")}
        row["score"] = _safe_retrieval_score(fact.get("_score", 0.0))
        rows.append(row)
    return rows


def _blocked(
    reason: str,
    query_text: str,
    *,
    reason_code: str,
    facts: Optional[List[Dict[str, Any]]] = None,
    trace: Optional[List[Dict[str, Any]]] = None,
    episode_requested: bool = False,
) -> Dict[str, Any]:
    metrics.incr("query.blocked")
    result: Dict[str, Any] = {
        "answer": None,
        "error": reason,
        "reason_code": reason_code,
        "query": query_text,
        "facts": _public_facts(facts or []),
        "trace": trace or [],
        "read_only": True,
        "query_policy": _QUERY_POLICY,
    }
    if episode_requested:
        result["episode"] = {
            "recorded": False,
            "reason_code": "read_only_query_does_not_record_episode",
        }
    return result


def _trust_metadata_conflicts(l1: Dict[str, Any], node: Dict[str, Any]) -> bool:
    """True if L1 and L3 genuinely disagree on trust-relevant metadata.

    Both sides are normalized with the SAME defaults and coercion this module
    already applies when it builds the served fact, so that "L3 omits the field
    and therefore takes the default" is not mistaken for a real disagreement.
    Confidence is compared with the tolerance the legacy admission path uses
    (core.pipeline._fact_metadata_conflicts) instead of raw `!=`, so two
    mathematically equal floats cannot fail closed on representation alone.

    A genuine disagreement — including a malformed L3 value that coerces to a
    different number — still conflicts.
    """
    if "confidence" in l1 and not math.isclose(
        _safe_confidence(l1.get("confidence"), 0.0),
        _safe_confidence(node.get("confidence"), 0.0),
        abs_tol=1e-9,
    ):
        return True
    if "claim_type" in l1 and l1.get("claim_type", _DEFAULT_CLAIM_TYPE) != node.get(
        "claim_type", _DEFAULT_CLAIM_TYPE
    ):
        return True
    return bool(
        "source_status" in l1 and l1.get("source_status") != node.get("source_status")
    )


def _resolve_canonical_fact(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Resolve one retrieval hit against existing graph memory without writing.

    L3 supplies stored content and verdict fields. L1 is consulted only as a
    deny-dominant read for a newer terminal ESM state or processing restriction.
    Missing/non-canonical retrieval hits return None and remain outside memory.
    """
    fact_id = item.get("id") or item.get("fact_id")
    if not isinstance(fact_id, str) or not fact_id:
        return None

    node = get_l3_graph().get_fact(fact_id)
    if node is None:
        return None

    state = node.get("epistemic_state")
    l3_restricted = _normalize_restricted_bit(node.get("restricted"))
    restricted: Optional[bool] = l3_restricted

    l1 = get_fact(fact_id)
    if l1 is not None:
        l1_state = l1.get("epistemic_state")
        if l1_state in _TERMINAL_ESM_STATES:
            state = l1_state
        elif l1_state is not None and state != l1_state:
            state = STORE_STATE_CONFLICT

        l1_restricted = _normalize_restricted_bit(l1.get("restricted"))
        if l1_restricted is True or l3_restricted is True:
            restricted = True
        elif l1_restricted is False:
            # Some L3 backends do not persist this bit. A typed L1 false is the
            # existing authoritative fallback used by the legacy pipeline.
            restricted = False

        # A hybrid record assembled from disagreeing trust metadata must fail
        # closed rather than silently preferring one representation.
        if _trust_metadata_conflicts(l1, node):
            state = STORE_STATE_CONFLICT

    fact: Dict[str, Any] = {
        "fact_id": fact_id,
        "claim": node.get("claim"),
        "source": node.get("source"),
        "confidence": _safe_confidence(node.get("confidence"), 0.0),
        "epistemic_state": state,
        "claim_type": node.get("claim_type", _DEFAULT_CLAIM_TYPE),
        "source_status": node.get("source_status"),
        "significance": node.get("significance", 0.5),
        "truth_status": node.get("truth_status"),
        "restricted": restricted,
        "_score": _safe_retrieval_score(
            item.get("_score", item.get("_relevance", 0.0))
        ),
    }
    return fact


_TOKEN_RE = re.compile(r"[a-zA-Zа-яА-ЯёЁ0-9_]{2,}")


def _lexical_tokens(text: Any) -> set[str]:
    if not isinstance(text, str):
        return set()
    return {token.casefold() for token in _TOKEN_RE.findall(text)}


def _retrieve_read_only(query_text: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
    """Retrieve without creating an embedding-space fingerprint.

    The legacy retrieve() stamps an unset fingerprint onto the L3 store. When a
    fingerprint already exists, that check is read-only and the mature hybrid
    retrieval can be reused. For a legacy/uninitialised store, use a bounded
    lexical scan over existing graph nodes instead of mutating store metadata.

    The fingerprint is checked BEFORE any full-store read: on the ordinary
    fingerprinted path retrieve() does its own bounded vector_search, so
    materializing every graph node here would be discarded work that grows
    linearly with the store on every single query.
    """
    limit = get_retrieval_config().k if k is None else k
    graph = get_l3_graph()
    if graph.embedder_fingerprint() is not None:
        return retrieve(query_text, k=limit)

    query_tokens = _lexical_tokens(query_text)
    if not query_tokens:
        return []

    nodes = graph.all_facts()
    if not nodes:
        return []

    ranked: List[Dict[str, Any]] = []
    for node in nodes:
        claim_tokens = _lexical_tokens(node.get("claim"))
        if not claim_tokens:
            continue
        overlap = query_tokens & claim_tokens
        if not overlap:
            continue
        score = len(overlap) / max(1, len(query_tokens | claim_tokens))
        ranked.append(
            {
                "id": node.get("fact_id"),
                "text": node.get("claim", ""),
                "source": node.get("source"),
                "confidence": _safe_confidence(node.get("confidence"), 0.0),
                "claim_type": node.get("claim_type", _DEFAULT_CLAIM_TYPE),
                "source_status": node.get("source_status"),
                "significance": node.get("significance", 0.5),
                "epistemic_state": node.get("epistemic_state"),
                "truth_status": node.get("truth_status"),
                "origin": "canonical_lexical_fallback",
                "_score": round(score, 6),
            }
        )
    ranked.sort(key=lambda item: item["_score"], reverse=True)
    return ranked[:limit]


def _resolve_retrieval_hits(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Resolve ranked candidates to existing graph facts without mutation."""
    facts: List[Dict[str, Any]] = []
    for item in retrieved:
        fact = _resolve_canonical_fact(item)
        if fact is not None:
            facts.append(fact)
    return facts


def search(query_text: str, k: int = 5) -> List[Dict[str, Any]]:
    """Read-only ranked search over facts already present in graph memory.

    This is the public search contract for inspection surfaces such as MCP. It
    does not run answer generation or admission policy, never stores unknown
    retrieval candidates, and excludes processing-restricted rows before any
    claim/source content is returned. Trust/status fields remain explicit so a
    caller cannot mistake physical graph membership for strict grounding.
    """
    if not isinstance(query_text, str) or not query_text.strip():
        raise ValueError("search: empty query")
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("search: k must be a positive integer")

    retrieved = _retrieve_read_only(query_text, k=k)
    facts = [
        fact for fact in _resolve_retrieval_hits(retrieved)
        if fact.get("restricted") is False
    ]
    return _public_search_facts(facts)


def query(
    query_text: str,
    episode: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Answer from already-admitted local memory with zero durable mutation.

    This path deliberately does not call pipeline.build_facts_pack(), TruthGate,
    ESM transition functions, outbox draining, episodic linking, NeuroCore, or
    any ingestion/reconciliation writer. Unknown retrieval rows are not stored;
    they produce a bounded insufficient-evidence result.
    """
    if not isinstance(query_text, str) or not query_text.strip():
        raise ValueError("query: empty query")

    metrics.incr("query.total")
    retrieved = _retrieve_read_only(query_text)
    if not retrieved:
        return _blocked(
            "Retrieval returned 0 results.",
            query_text,
            reason_code="no_local_retrieval_results",
            episode_requested=episode is not None,
        )

    facts = _resolve_retrieval_hits(retrieved)
    if not facts:
        return _blocked(
            "Insufficient grounding: retrieval found no existing graph facts.",
            query_text,
            reason_code="no_canonical_retrieval_results",
            episode_requested=episode is not None,
        )

    trace_input = [
        {
            "id": fact["fact_id"],
            "source": fact.get("source"),
            "origin": "canonical_read",
            "epistemic_state": fact.get("epistemic_state"),
            "_score": fact.get("_score", 0.0),
        }
        for fact in facts
    ]
    facts_pack = {"facts": facts, "query": query_text, "total": len(facts)}
    trace = build_trace(trace_input)
    guardian_ok, guardian_reason = guardian(facts_pack, trace)
    if not guardian_ok:
        return _blocked(
            f"Guardian: {guardian_reason}",
            query_text,
            reason_code="guardian_rejected_canonical_read",
            facts=facts,
            trace=trace,
            episode_requested=episode is not None,
        )

    result = generate_answer(facts_pack, trace)
    result["read_only"] = True
    result["query_policy"] = _QUERY_POLICY
    if episode is not None:
        result["episode"] = {
            "recorded": False,
            "reason_code": "read_only_query_does_not_record_episode",
        }

    if result.get("answer") is None:
        metrics.incr("query.blocked")
        result.setdefault("reason_code", "insufficient_strict_canonical_grounding")
    else:
        metrics.incr("query.answered")
    return result


run_read_only = query

__all__ = ["query", "run_read_only", "search"]