# core/evidence.py
# Velantrim ExoCortex — Evidence Span Store (RFC0063 / grant WP1)
# v8.25.0-sprint5
#
# A canonical fact answers "what do we believe". Evidence spans answer
# "where did it come from": a source URI/file, an optional chunk and character
# span, the source content hash, and the claim hash at attach time.
#
# Design:
#   - Additive: lives in its own `evidence_spans` table; nothing about the fact
#     schema or the existing pipeline changes.
#   - Content-light: the source TEXT is never stored — only SHA-256 hashes — so a
#     receipt can prove a fact maps to an exact source span without re-exposing
#     personal data (mirrors the content-light provenance receipt).
#   - Verifiable: verify_evidence() detects drift — the fact erased, or its claim
#     text changed since the span was attached.
#
# This is the baseline of WP1. Richer span extraction (line/section offsets pulled
# automatically during PDF/Markdown ingestion, dry-run review) remains future work.

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from core import memory


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(text: str) -> str:
    """SHA-256 of text — used for both the claim hash and the source hash."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def attach_evidence(
    fact_id: str,
    source_uri: str,
    *,
    source_kind: str = "external",
    claim: Optional[str] = None,
    chunk_id: Optional[str] = None,
    span_start: Optional[int] = None,
    span_end: Optional[int] = None,
    source_text: Optional[str] = None,
    source_sha256: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Attach a source-span evidence record to a fact.

    `claim` defaults to the fact's current claim (so the span commits to what the
    fact says now). `source_sha256` is taken from `source_text` if not given.
    Returns the stored evidence row. Raises ValueError if the fact does not exist.
    """
    fact = memory.get_fact(fact_id)
    if fact is None:
        raise ValueError(f"attach_evidence: unknown fact_id {fact_id!r}")
    claim_text = claim if claim is not None else fact.get("claim", "")
    if source_sha256 is None and source_text is not None:
        source_sha256 = sha256(source_text)

    row = {
        "evidence_id":   "ev:" + uuid.uuid4().hex[:12],
        "fact_id":       fact_id,
        "source_uri":    source_uri,
        "source_kind":   source_kind,
        "chunk_id":      chunk_id,
        "span_start":    span_start,
        "span_end":      span_end,
        "source_sha256": source_sha256,
        "claim_sha256":  sha256(claim_text),
        "created_at":    _now(),
    }
    with memory._db() as conn:
        conn.execute(
            "INSERT INTO evidence_spans (evidence_id, fact_id, source_uri, "
            "source_kind, chunk_id, span_start, span_end, source_sha256, "
            "claim_sha256, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (row["evidence_id"], row["fact_id"], row["source_uri"],
             row["source_kind"], row["chunk_id"], row["span_start"],
             row["span_end"], row["source_sha256"], row["claim_sha256"],
             row["created_at"]),
        )
    return row


def evidence_for(fact_id: str) -> List[Dict[str, Any]]:
    """All evidence spans attached to a fact (oldest first)."""
    with memory._db() as conn:
        rows = conn.execute(
            "SELECT evidence_id, fact_id, source_uri, source_kind, chunk_id, "
            "span_start, span_end, source_sha256, claim_sha256, created_at "
            "FROM evidence_spans WHERE fact_id = ? ORDER BY created_at",
            (fact_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def verify_evidence(fact_id: str) -> List[Dict[str, Any]]:
    """
    Replay every evidence span for a fact against the current canon.

    Per span status:
      ok        — the fact exists and its claim hash still matches the span;
      modified  — the fact's claim text changed since the span was attached;
      erased    — the fact has a deletion tombstone (Art. 17);
      missing   — the fact is gone with no tombstone.
    """
    fact = memory.get_fact(fact_id)
    tombstoned = {t["fact_id"] for t in memory.get_tombstones()}
    out: List[Dict[str, Any]] = []
    for span in evidence_for(fact_id):
        if fact is None:
            status = "erased" if fact_id in tombstoned else "missing"
        elif sha256(fact.get("claim", "")) != span["claim_sha256"]:
            status = "modified"
        else:
            status = "ok"
        out.append({"evidence_id": span["evidence_id"],
                    "source_uri": span["source_uri"], "status": status})
    return out
