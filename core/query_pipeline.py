# core/query_pipeline.py
# Velantrim ExoCortex — strict read-only query pipeline.
#
# Query is a read operation. It may retrieve and render facts that already exist
# in the L3 graph, but it must never create/update L0/L1 rows, transition ESM,
# drain an outbox, write graph state, initialise a fingerprint or rebuild vectors.

from __future__ import annotations

import hashlib
import json
import math
import os
from typing import Any, Dict, List, Optional

from core import metrics
from core.embedding import get_embedder
from core.evidence import has_valid_evidence_for_grounding
from core.l3_graph import get_l3_graph
from core.legacy_retrieval import (
    LEGACY_REINDEX_REASON_CODE,
    LegacyRetrievalUnavailable,
    bounded_legacy_retrieve,
)
from core.memory import get_fact
from core.pipeline import generate_answer, guardian, retrieve
from core.retrieval_config import get_retrieval_config
from core.trace import build_trace
from core.trust_snapshot import (
    STORE_STATE_CONFLICT as _STORE_STATE_CONFLICT,
    TrustSnapshot,
)

STORE_STATE_CONFLICT = _STORE_STATE_CONFLICT
_QUERY_POLICY = "canonical_read_only"
_GRANT_PROFILE_ENV = "VELANTRIM_RELEASE_PROFILE"
_GRANT_PROFILE = "grant"
_GRANT_EMBEDDER_REASON = "grant_profile_requires_pinned_embedder"
_EMBEDDER_MISMATCH_FALLBACK = "embedder_mismatch_lexical_fallback"
_EMBEDDER_PROVIDER_FALLBACK = "embedder_provider_unavailable_lexical_fallback"


def _grant_profile_enabled() -> bool:
    return os.environ.get(_GRANT_PROFILE_ENV, "").strip().casefold() == _GRANT_PROFILE


def _retrieval_config_id() -> str:
    payload = json.dumps(
        get_retrieval_config().to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _mark_legacy_degradation(
    candidates: List[Dict[str, Any]],
    *,
    reason_code: str,
    active_embedder_id: Optional[str],
    stored_embedder_id: Optional[str],
) -> List[Dict[str, Any]]:
    setattr(candidates, "degradation_reason_code", reason_code)
    setattr(candidates, "active_embedder_id", active_embedder_id)
    setattr(candidates, "stored_embedder_id", stored_embedder_id)
    for rank, item in enumerate(candidates, 1):
        item["_retrieval_rank"] = rank
        item["_retrieval_signals"] = ["bounded_legacy_lexical"]
        item["_active_embedder_id"] = active_embedder_id
        item["_stored_embedder_id"] = stored_embedder_id
        item["_retrieval_mode"] = "bounded_legacy_lexical"
    return candidates


def _safe_retrieval_score(value: Any) -> float:
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
    rows: List[Dict[str, Any]] = []
    for fact in facts:
        row = {k: v for k, v in fact.items() if not k.startswith("_")}
        row["score"] = _safe_retrieval_score(fact.get("_score", 0.0))
        rows.append(row)
    return rows


def _legacy_metadata(retrieved: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    # LegacyCandidates carries these attributes even when lexical matching
    # returns zero hits, so degraded mode and work bounds remain observable.
    examined = getattr(retrieved, "examined", None)
    candidate_limit = getattr(retrieved, "candidate_limit", None)
    if isinstance(examined, int) and isinstance(candidate_limit, int):
        metadata: Dict[str, Any] = {
            "mode": "bounded_legacy_lexical",
            "candidates_examined": examined,
            "candidate_limit": candidate_limit,
            "reindex_recommended": True,
        }
        reason_code = getattr(retrieved, "degradation_reason_code", None)
        if isinstance(reason_code, str) and reason_code:
            metadata["reason_code"] = reason_code
        active_id = getattr(retrieved, "active_embedder_id", None)
        stored_id = getattr(retrieved, "stored_embedder_id", None)
        if active_id is not None:
            metadata["active_embedder_id"] = active_id
        if stored_id is not None:
            metadata["stored_embedder_id"] = stored_id
        return metadata
    legacy = [item for item in retrieved if item.get("origin") == "bounded_legacy_lexical"]
    if not legacy:
        return None
    return {
        "mode": "bounded_legacy_lexical",
        "candidates_examined": max(
            int(item.get("_legacy_candidates_examined", 0)) for item in legacy
        ),
        "candidate_limit": max(
            int(item.get("_legacy_candidate_limit", 0)) for item in legacy
        ),
        "reindex_recommended": True,
    }


def _blocked(
    reason: str,
    query_text: str,
    *,
    reason_code: str,
    facts: Optional[List[Dict[str, Any]]] = None,
    trace: Optional[List[Dict[str, Any]]] = None,
    episode_requested: bool = False,
    retrieval: Optional[Dict[str, Any]] = None,
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
    if retrieval is not None:
        result["retrieval"] = retrieval
    if episode_requested:
        result["episode"] = {
            "recorded": False,
            "reason_code": "read_only_query_does_not_record_episode",
        }
    return result


def _resolve_canonical_fact(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    fact_id = item.get("id") or item.get("fact_id")
    if not isinstance(fact_id, str) or not fact_id:
        return None
    node = get_l3_graph().get_fact(fact_id)
    if node is None:
        return None
    snapshot = TrustSnapshot.from_records(
        fact_id=fact_id,
        l3=node,
        l1=get_fact(fact_id),
        retrieval_score=item.get("_score", item.get("_relevance", 0.0)),
    )
    fact = snapshot.to_fact_dict()
    # Retrieval metadata is query-local and never becomes L3/Canon state.
    for key in (
        "_retrieval_rank",
        "_retrieval_signals",
        "_active_embedder_id",
        "_stored_embedder_id",
        "_retrieval_mode",
        "_graph_explanation",
    ):
        if key in item:
            fact[key] = item[key]
    return fact


def _retrieve_read_only(query_text: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
    """Retrieve without silent embedding-space changes or durable mutation."""
    limit = get_retrieval_config().k if k is None else k
    graph = get_l3_graph()
    configured_embedder = os.environ.get("VELANTRIM_EMBEDDER", "auto").strip().casefold() or "auto"
    if _grant_profile_enabled() and configured_embedder == "auto":
        raise LegacyRetrievalUnavailable(
            "grant profile requires an explicit VELANTRIM_EMBEDDER value",
            reason_code=_GRANT_EMBEDDER_REASON,
        )

    stored = graph.embedder_fingerprint()
    if stored is None:
        candidates = bounded_legacy_retrieve(query_text, k=limit, graph=graph)
        return _mark_legacy_degradation(
            candidates,
            reason_code=LEGACY_REINDEX_REASON_CODE,
            active_embedder_id=None,
            stored_embedder_id=None,
        )

    try:
        active = get_embedder().id
    except Exception:
        candidates = bounded_legacy_retrieve(query_text, k=limit, graph=graph)
        return _mark_legacy_degradation(
            candidates,
            reason_code=_EMBEDDER_PROVIDER_FALLBACK,
            active_embedder_id=None,
            stored_embedder_id=stored,
        )

    if active != stored:
        candidates = bounded_legacy_retrieve(query_text, k=limit, graph=graph)
        return _mark_legacy_degradation(
            candidates,
            reason_code=_EMBEDDER_MISMATCH_FALLBACK,
            active_embedder_id=active,
            stored_embedder_id=stored,
        )

    retrieved = retrieve(query_text, k=limit)
    for rank, item in enumerate(retrieved, 1):
        item.setdefault("_retrieval_rank", rank)
        item.setdefault("_active_embedder_id", active)
        item.setdefault("_stored_embedder_id", stored)
        item.setdefault("_retrieval_mode", "admitted_memory_hybrid")
    return retrieved


def _resolve_retrieval_hits(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    facts: List[Dict[str, Any]] = []
    for item in retrieved:
        fact = _resolve_canonical_fact(item)
        if fact is not None:
            facts.append(fact)
    return facts


def search_result(query_text: str, k: int = 5) -> Dict[str, Any]:
    """Structured read-only search result with stable availability reason codes."""
    if not isinstance(query_text, str) or not query_text.strip():
        raise ValueError("search: empty query")
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("search: k must be a positive integer")
    try:
        retrieved = _retrieve_read_only(query_text, k=k)
    except LegacyRetrievalUnavailable as exc:
        return {
            "results": [],
            "error": str(exc),
            "reason_code": exc.reason_code,
            "read_only": True,
            "query_policy": _QUERY_POLICY,
            "retrieval": {
                "mode": "unavailable_legacy_backend",
                "reindex_required": True,
            },
        }
    facts = [
        fact for fact in _resolve_retrieval_hits(retrieved)
        if fact.get("restricted") is False
    ]
    result: Dict[str, Any] = {
        "results": _public_search_facts(facts),
        "reason_code": "ok" if facts else "no_local_retrieval_results",
        "read_only": True,
        "query_policy": _QUERY_POLICY,
    }
    legacy = _legacy_metadata(retrieved)
    if legacy is not None:
        result["retrieval"] = legacy
    return result


def search(query_text: str, k: int = 5) -> List[Dict[str, Any]]:
    """Backward-compatible list-only search wrapper."""
    return search_result(query_text, k=k)["results"]


def query(
    query_text: str,
    episode: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Answer from already-admitted local memory with zero durable mutation."""
    if not isinstance(query_text, str) or not query_text.strip():
        raise ValueError("query: empty query")

    metrics.incr("query.total")
    try:
        retrieved = _retrieve_read_only(query_text)
    except LegacyRetrievalUnavailable as exc:
        return _blocked(
            str(exc),
            query_text,
            reason_code=exc.reason_code,
            episode_requested=episode is not None,
            retrieval={
                "mode": "unavailable_legacy_backend",
                "reindex_required": True,
            },
        )
    legacy = _legacy_metadata(retrieved)
    if not retrieved:
        return _blocked(
            "Retrieval returned 0 results.",
            query_text,
            reason_code="no_local_retrieval_results",
            episode_requested=episode is not None,
            retrieval=legacy,
        )

    facts = _resolve_retrieval_hits(retrieved)
    if not facts:
        return _blocked(
            "Insufficient grounding: retrieval found no existing graph facts.",
            query_text,
            reason_code="no_canonical_retrieval_results",
            episode_requested=episode is not None,
            retrieval=legacy,
        )

    # Current factual authority is derived at read time: a VERIFIED fact may
    # ground a public answer only while it retains at least one valid,
    # replayable evidence span. This reuses the established predicate and does
    # not rewrite historical ESM/provenance when support is later removed.
    verified_before = [f for f in facts if f.get("truth_status") == "VERIFIED"]
    facts = [
        f for f in facts
        if f.get("truth_status") != "VERIFIED"
        or has_valid_evidence_for_grounding(
            f["fact_id"], expected_claim=f.get("claim")
        )
    ]
    if verified_before and not any(f.get("truth_status") == "VERIFIED" for f in facts):
        return _blocked(
            "Insufficient grounding: VERIFIED facts lack valid replayable evidence spans.",
            query_text,
            reason_code="insufficient_grounding_missing_verified_evidence",
            episode_requested=episode is not None,
            retrieval=legacy,
        )

    config_id = _retrieval_config_id()
    trace_input = [
        {
            "id": fact["fact_id"],
            "source": fact.get("source"),
            "origin": "canonical_read",
            "epistemic_state": fact.get("epistemic_state"),
            "_score": fact.get("_score", 0.0),
            "_retrieval_rank": fact.get("_retrieval_rank"),
            "_retrieval_signals": fact.get("_retrieval_signals", []),
            "_active_embedder_id": fact.get("_active_embedder_id"),
            "_stored_embedder_id": fact.get("_stored_embedder_id"),
            "_retrieval_mode": fact.get("_retrieval_mode"),
            "_retrieval_config_id": config_id,
            "_projection_id": _QUERY_POLICY,
            "_graph_explanation": fact.get("_graph_explanation"),
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
            retrieval=legacy,
        )

    result = generate_answer(facts_pack, trace)
    result["read_only"] = True
    result["query_policy"] = _QUERY_POLICY
    if legacy is not None:
        result["retrieval"] = legacy
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

__all__ = [
    "LEGACY_REINDEX_REASON_CODE",
    "query",
    "run_read_only",
    "search",
    "search_result",
]
