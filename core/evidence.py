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


def _validate_span(span_start: Optional[int], span_end: Optional[int]) -> None:
    """
    Reject malformed character spans early, so a fact can never present a
    provenance pointer that addresses nothing (or a negative/inverted range).

    Either both offsets are given (a real span) or both are omitted (a
    document/chunk-level reference). A half-open [start, end) range must satisfy
    0 <= start <= end.
    """
    if span_start is None and span_end is None:
        return
    if span_start is None or span_end is None:
        raise ValueError(
            "attach_evidence: span_start and span_end must be given together")
    if not isinstance(span_start, int) or not isinstance(span_end, int):
        raise ValueError("attach_evidence: span offsets must be integers")
    if span_start < 0 or span_end < 0:
        raise ValueError("attach_evidence: span offsets must be non-negative")
    if span_start > span_end:
        raise ValueError(
            f"attach_evidence: invalid span [{span_start}, {span_end})")


def attach_evidence(
    fact_id: str,
    source_uri: str,
    *,
    source_kind: str = "external",
    claim: Optional[str] = None,
    chunk_id: Optional[str] = None,
    section: Optional[str] = None,
    span_start: Optional[int] = None,
    span_end: Optional[int] = None,
    source_text: Optional[str] = None,
    source_sha256: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Attach a source-span evidence record to a fact.

    `claim` defaults to the fact's current claim (so the span commits to what the
    fact says now). `source_sha256` is taken from `source_text` if not given.
    `section` is an optional human-readable location (heading/page/section).
    Returns the stored evidence row. Raises ValueError if the fact does not exist
    or the character span is malformed.
    """
    fact = memory.get_fact(fact_id)
    if fact is None:
        raise ValueError(f"attach_evidence: unknown fact_id {fact_id!r}")
    _validate_span(span_start, span_end)
    claim_text = claim if claim is not None else fact.get("claim", "")
    if source_sha256 is None and source_text is not None:
        source_sha256 = sha256(source_text)

    row = {
        "evidence_id":   "ev:" + uuid.uuid4().hex[:12],
        "fact_id":       fact_id,
        "source_uri":    source_uri,
        "source_kind":   source_kind,
        "chunk_id":      chunk_id,
        "section":       section,
        "span_start":    span_start,
        "span_end":      span_end,
        "source_sha256": source_sha256,
        "claim_sha256":  sha256(claim_text),
        "created_at":    _now(),
    }
    with memory._db() as conn:
        conn.execute(
            "INSERT INTO evidence_spans (evidence_id, fact_id, source_uri, "
            "source_kind, chunk_id, section, span_start, span_end, source_sha256, "
            "claim_sha256, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (row["evidence_id"], row["fact_id"], row["source_uri"],
             row["source_kind"], row["chunk_id"], row["section"],
             row["span_start"], row["span_end"], row["source_sha256"],
             row["claim_sha256"], row["created_at"]),
        )
    return row


def evidence_for(fact_id: str) -> List[Dict[str, Any]]:
    """All evidence spans attached to a fact (oldest first)."""
    with memory._db() as conn:
        rows = conn.execute(
            "SELECT evidence_id, fact_id, source_uri, source_kind, chunk_id, "
            "section, span_start, span_end, source_sha256, claim_sha256, created_at "
            "FROM evidence_spans WHERE fact_id = ? ORDER BY created_at",
            (fact_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def verify_evidence(
    fact_id: str,
    current_sources: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """
    Replay every evidence span for a fact against the current canon.

    Per span status:
      ok            — the fact exists and its claim hash still matches the span;
      modified      — the fact's claim text changed since the span was attached;
      stale_source  — the source content changed since the span was attached
                      (its current SHA-256 no longer matches `source_sha256`);
      erased        — the fact has a deletion tombstone (Art. 17);
      missing       — the fact is gone with no tombstone.

    `current_sources` optionally maps `source_uri` → the source's current text.
    When a span's `source_uri` is present in the map and the span recorded a
    `source_sha256`, the live text is re-hashed; a mismatch is reported as
    `stale_source`. Spans whose source is not supplied are not re-checked.
    """
    fact = memory.get_fact(fact_id)
    tombstoned = {t["fact_id"] for t in memory.get_tombstones()}
    out: List[Dict[str, Any]] = []
    for span in evidence_for(fact_id):
        if fact is None:
            status = "erased" if fact_id in tombstoned else "missing"
        elif sha256(fact.get("claim", "")) != span["claim_sha256"]:
            status = "modified"
        elif _source_is_stale(span, current_sources):
            status = "stale_source"
        else:
            status = "ok"
        out.append({"evidence_id": span["evidence_id"],
                    "source_uri": span["source_uri"], "status": status})
    return out


def _source_is_stale(
    span: Dict[str, Any], current_sources: Optional[Dict[str, str]]
) -> bool:
    """True if the live source text no longer hashes to the sealed source_sha256."""
    if not current_sources:
        return False
    stored = span.get("source_sha256")
    if not stored:
        return False
    uri = span.get("source_uri")
    if uri not in current_sources:
        return False
    return sha256(current_sources[uri]) != stored


# ─── Provenance-coverage guard (#61) ──────────────────────────────────────────
# A high-confidence world claim must be backed by a source. A fact whose
# truth_status is VERIFIED carries the strongest provenance signal the system
# can emit, so it must not stand on zero evidence spans.

def _truth_status_of(fact: Dict[str, Any]) -> str:
    """
    The fact's truth_status. It is not persisted as a column (it is derived at
    pipeline time from claim_type + source_status), so when a stored record does
    not carry it we recompute it from the canonical TruthGate mapping.
    """
    ts = fact.get("truth_status")
    if ts:
        return ts
    from core.pipeline import _truth_status_for  # lazy: avoid import cycle
    return _truth_status_for(
        fact.get("claim_type", "WORLD_FACT"), fact.get("source_status"))


def requires_evidence(fact: Dict[str, Any]) -> bool:
    """True if `fact` makes a high-confidence claim that must carry evidence."""
    return _truth_status_of(fact) == "VERIFIED"


def has_evidence(fact_id: str) -> bool:
    """True if at least one source-span evidence record is attached to the fact."""
    return bool(evidence_for(fact_id))


def provenance_gaps(fact_ids: List[str]) -> List[str]:
    """
    fact_ids that present high-confidence provenance (VERIFIED) without any
    source-span evidence — the records a reviewer should not trust as sourced.
    """
    gaps: List[str] = []
    for fid in fact_ids:
        fact = memory.get_fact(fid)
        if fact is not None and requires_evidence(fact) and not has_evidence(fid):
            gaps.append(fid)
    return gaps
