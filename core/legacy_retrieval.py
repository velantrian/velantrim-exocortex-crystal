"""Bounded, non-mutating retrieval for L3 stores without a fingerprint.

The ordinary vector path is used whenever an embedder fingerprint exists. This
module exists only for legacy/uninitialised stores and guarantees that Python
materialises and scores no more than an explicit candidate window. It never
creates vectors, writes a fingerprint or changes truth state.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Optional

from core.l3_graph import MockL3Graph, SqliteL3Graph

_TOKEN_RE = re.compile(r"[a-zA-Zа-яА-ЯёЁ0-9_]{2,}")
DEFAULT_LEGACY_CANDIDATE_LIMIT = 256
MIN_LEGACY_CANDIDATE_LIMIT = 1
MAX_LEGACY_CANDIDATE_LIMIT = 4096
_LIMIT_ENV = "VELANTRIM_LEGACY_QUERY_CANDIDATES"
LEGACY_REINDEX_REASON_CODE = "legacy_store_requires_reindex"


class LegacyRetrievalUnavailable(RuntimeError):
    """The backend cannot provide a bounded read for an uninitialised store."""

    def __init__(self, message: str, *, reason_code: str = LEGACY_REINDEX_REASON_CODE):
        super().__init__(message)
        self.reason_code = reason_code


@dataclass(frozen=True)
class LegacyRetrievalStatus:
    supported: bool
    backend: str
    candidate_limit: int
    fingerprint_present: bool
    reason_code: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "supported": self.supported,
            "backend": self.backend,
            "candidate_limit": self.candidate_limit,
            "fingerprint_present": self.fingerprint_present,
            "reason_code": self.reason_code,
        }


def lexical_tokens(text: Any) -> set[str]:
    if not isinstance(text, str):
        return set()
    return {token.casefold() for token in _TOKEN_RE.findall(text)}


def legacy_candidate_limit(value: Optional[int] = None) -> int:
    """Resolve a bounded candidate window from an argument or environment."""
    raw: Any = value
    if raw is None:
        raw = os.environ.get(_LIMIT_ENV, str(DEFAULT_LEGACY_CANDIDATE_LIMIT))
    if isinstance(raw, bool):
        raise ValueError("legacy candidate limit must be an integer")
    try:
        limit = int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("legacy candidate limit must be an integer") from exc
    if not MIN_LEGACY_CANDIDATE_LIMIT <= limit <= MAX_LEGACY_CANDIDATE_LIMIT:
        raise ValueError(
            f"legacy candidate limit must be between {MIN_LEGACY_CANDIDATE_LIMIT} "
            f"and {MAX_LEGACY_CANDIDATE_LIMIT}"
        )
    return limit


def legacy_retrieval_status(graph, *, candidate_limit: Optional[int] = None) -> LegacyRetrievalStatus:
    limit = legacy_candidate_limit(candidate_limit)
    backend = type(graph).__name__
    fingerprint_present = graph.embedder_fingerprint() is not None
    supported = isinstance(graph, (MockL3Graph, SqliteL3Graph))
    return LegacyRetrievalStatus(
        supported=supported,
        backend=backend,
        candidate_limit=limit,
        fingerprint_present=fingerprint_present,
        reason_code=None if supported else LEGACY_REINDEX_REASON_CODE,
    )


def _bounded_nodes(graph, candidate_limit: int) -> list[dict[str, Any]]:
    """Read at most ``candidate_limit`` node payloads without ``all_facts``."""
    if isinstance(graph, MockL3Graph):
        # Mock is an ephemeral test/dev backend. Sorted ids make the bounded
        # window deterministic across repeated calls.
        ids = sorted(graph._nodes)[:candidate_limit]
        return [dict(graph._nodes[fact_id]) for fact_id in ids]

    if isinstance(graph, SqliteL3Graph):
        # nodes.fact_id is the PRIMARY KEY, so SQLite can stop after LIMIT
        # rather than materialising the whole JSON corpus in Python.
        with graph._lock:
            rows = graph._conn.execute(
                "SELECT data FROM nodes ORDER BY fact_id LIMIT ?",
                (candidate_limit,),
            ).fetchall()
        return [json.loads(row["data"]) for row in rows]

    raise LegacyRetrievalUnavailable(
        f"{type(graph).__name__} cannot provide bounded legacy retrieval; "
        "run an explicit embedding reindex before public queries"
    )


def bounded_legacy_retrieve(
    query_text: str,
    *,
    k: int,
    graph,
    candidate_limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Rank a deterministic bounded node window using lexical overlap.

    ``k`` bounds output. ``candidate_limit`` independently bounds the number of
    node payloads materialised and tokenised by this degraded legacy path.
    """
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    limit = legacy_candidate_limit(candidate_limit)
    query_tokens = lexical_tokens(query_text)
    if not query_tokens:
        return []

    nodes = _bounded_nodes(graph, limit)
    ranked: list[dict[str, Any]] = []
    examined = len(nodes)
    for node in nodes:
        fact_id = node.get("fact_id")
        if not isinstance(fact_id, str) or not fact_id:
            continue
        claim_tokens = lexical_tokens(node.get("claim"))
        if not claim_tokens:
            continue
        overlap = query_tokens & claim_tokens
        if not overlap:
            continue
        score = len(overlap) / max(1, len(query_tokens | claim_tokens))
        ranked.append(
            {
                "id": fact_id,
                "origin": "bounded_legacy_lexical",
                "_score": round(score, 6),
                "_legacy_candidates_examined": examined,
                "_legacy_candidate_limit": limit,
            }
        )
    ranked.sort(key=lambda item: (-item["_score"], item["id"]))
    return ranked[:k]


__all__ = [
    "DEFAULT_LEGACY_CANDIDATE_LIMIT",
    "LEGACY_REINDEX_REASON_CODE",
    "LegacyRetrievalStatus",
    "LegacyRetrievalUnavailable",
    "bounded_legacy_retrieve",
    "legacy_candidate_limit",
    "legacy_retrieval_status",
    "lexical_tokens",
]
