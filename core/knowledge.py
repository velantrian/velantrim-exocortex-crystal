# core/knowledge.py
# Velantrim ExoCortex — External Knowledge Ingestion (RFC0063)
#
# The utterance ingestion in core/ingest.py turns a single user message into a
# fact. RFC0063 is the *bulk* counterpart: it imports external knowledge — a text
# file, a JSON/JSONL export, a CSV table, a Markdown document — and routes every
# extracted claim through the SAME Guardian → TruthGate path. Nothing is trusted
# because it came from a file; each claim earns its place in the canon or is
# blocked, exactly like a user's message.
#
# Faithful to the project's principles:
#   - Dependency-free: only stdlib parsers (text / markdown / json / jsonl / csv).
#     Heavier sources (PDF, YAML, Wikidata RDF) are intentionally left to optional
#     adapters so the runtime stays stdlib-only.
#   - physical L3 != strict Canon: imported facts carry source_status = EXTERNAL
#     and the source file as their `source`, preserving explicit provenance.
#   - No alternate entry into Canon — everything still goes through ingest()/TruthGate.

import csv
import hashlib
import io
import json
import os
import re
from typing import Dict, Any, List, Optional, Iterable

from core import ingest as _ingest_mod
from core import metrics, evidence, span_extract
from core.path_safety import resolve_safe_path

EXTERNAL = "EXTERNAL"
_SUPPORTED = (".txt", ".md", ".markdown", ".json", ".jsonl", ".ndjson", ".csv")

# Markdown noise we strip to recover the underlying claim text.
_MD_BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_MD_HEADING = re.compile(r"^\s*#{1,6}\s+")


def _clean_line(line: str) -> str:
    line = line.strip()
    line = _MD_HEADING.sub("", line)
    line = _MD_BULLET.sub("", line)
    return line.strip()


# ─── Claim extraction (dependency-free, per format) ───────────────────────────

def extract_claims(content: str, fmt: str) -> List[Dict[str, Any]]:
    """
    Turn raw `content` of a given format into a list of claim dicts:
    {"claim": str, optional "confidence"/"significance"/"claim_type"}.
    Deterministic and stdlib-only. Unknown formats raise ValueError.
    """
    fmt = fmt.lower().lstrip(".")
    if fmt in ("txt", "text"):
        return [
            {"claim": line}
            for line in (raw_line.strip() for raw_line in content.splitlines())
            if line
        ]
    if fmt in ("md", "markdown"):
        return _extract_markdown(content)
    if fmt == "json":
        return _normalise_records(json.loads(content))
    if fmt in ("jsonl", "ndjson"):
        out: List[Dict[str, Any]] = []
        for line in content.splitlines():
            line = line.strip()
            if line:
                out.extend(_normalise_records(json.loads(line)))
        return out
    if fmt == "csv":
        return _extract_csv(content)
    raise ValueError(f"extract_claims: unsupported format {fmt!r}")


def _extract_markdown(content: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    in_fence = False
    for raw in content.splitlines():
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or _MD_HEADING.match(raw):
            continue  # skip code blocks and section headings (structure, not claims)
        claim = _clean_line(raw)
        if claim:
            out.append({"claim": claim})
    return out


def _extract_csv(content: str) -> List[Dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(content))
    if not reader.fieldnames or "claim" not in reader.fieldnames:
        raise ValueError("CSV ingestion requires a 'claim' column")
    out: List[Dict[str, Any]] = []
    for row in reader:
        claim = (row.get("claim") or "").strip()
        if not claim:
            continue
        rec: Dict[str, Any] = {"claim": claim}
        for k in ("confidence", "significance"):
            if row.get(k):
                try:
                    rec[k] = float(row[k])
                except ValueError:
                    pass
        if row.get("claim_type"):
            rec["claim_type"] = row["claim_type"].strip()
        out.append(rec)
    return out


def _normalise_records(data: Any) -> List[Dict[str, Any]]:
    """Accept a JSON shape and normalise to claim dicts. Supported:
    "a string" | ["a", "b"] | [{"claim": ...}] | {"claims": [...]}."""
    if isinstance(data, str):
        return [{"claim": data}] if data.strip() else []
    if isinstance(data, dict):
        if "claims" in data:
            return _normalise_records(data["claims"])
        if "claim" in data:
            return [_normalise_record_dict(data)]
        return []
    if isinstance(data, list):
        out: List[Dict[str, Any]] = []
        for item in data:
            out.extend(_normalise_records(item))
        return out
    return []


def _normalise_record_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    rec: Dict[str, Any] = {"claim": str(d["claim"]).strip()}
    for k in ("confidence", "significance", "claim_type"):
        if d.get(k) is not None:
            rec[k] = d[k]
    return rec


# ─── Ingestion ─────────────────────────────────────────────────────────────────

def ingest_claims(
    claims: Iterable[Dict[str, Any]], *, source: str = "external",
    source_status: str = EXTERNAL, source_sha256: Optional[str] = None,
    attach_evidence: bool = True,
    source_content: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Route each extracted claim through ingest() (Guardian → TruthGate → L3), with
    source/source_status set for provenance. Returns an aggregate report.

    When `attach_evidence` is set (default), each newly accepted fact also gets a
    source-span evidence record (WP1) linking it to `source` (+ `source_sha256`).

    When `source_content` is provided, character-level span offsets and the
    nearest Markdown section heading are detected and stored in the evidence
    record (WP1 span extraction). Records that already carry `span_start` /
    `span_end` (e.g. from the PDF adapter) are used as-is.
    """
    accepted = duplicates = blocked = 0
    blocked_reasons: List[Dict[str, str]] = []
    fact_ids: List[str] = []
    new_fact_ids: List[str] = []
    for rec in claims:
        claim = (rec.get("claim") or "").strip()
        if not claim:
            continue
        kwargs: Dict[str, Any] = {"source": source, "source_status": source_status}
        for k in ("confidence", "significance", "claim_type"):
            if rec.get(k) is not None:
                kwargs[k] = rec[k]
        res = _ingest_mod.ingest(claim, **kwargs)
        if res.get("accepted"):
            accepted += 1
            fid = res["fact"]["fact_id"]
            fact_ids.append(fid)
            if res.get("duplicate"):
                duplicates += 1
            else:
                # Only facts newly created by THIS call are this batch's own —
                # a duplicate hit means fid already existed (possibly created
                # by an unrelated, earlier import). Session bookkeeping must
                # track new_fact_ids, not fact_ids, or a later erase_session()/
                # restrict_session() on this batch would act on a fact this
                # batch never created (see core/imports.py _record_session).
                new_fact_ids.append(fid)
                if attach_evidence:
                    # Resolve span offsets: prefer adapter-supplied values, then
                    # detect from source_content, else fall back to doc-level ref.
                    sp_start = rec.get("span_start")
                    sp_end = rec.get("span_end")
                    section = rec.get("section")
                    chunk_id = rec.get("chunk_id")
                    if sp_start is None and source_content is not None:
                        sp_start, sp_end = span_extract.locate_claim(
                            source_content, claim)
                        if sp_start is not None and section is None:
                            section = span_extract.extract_section(
                                source_content, sp_start)
                    evidence.attach_evidence(
                        fid, source, source_kind="file", claim=claim,
                        source_sha256=source_sha256,
                        span_start=sp_start, span_end=sp_end,
                        section=section, chunk_id=chunk_id)
        else:
            blocked += 1
            blocked_reasons.append({"claim": claim, "reason": res.get("reason", "")})
    metrics.incr("knowledge.ingested")
    return {
        "source": source,
        "total": accepted + blocked,
        "accepted": accepted,
        "duplicates": duplicates,
        "blocked": blocked,
        "fact_ids": fact_ids,
        "new_fact_ids": new_fact_ids,
        "blocked_reasons": blocked_reasons,
    }


def ingest_text(
    content: str, *, fmt: str = "txt", source: str = "external",
    source_status: str = EXTERNAL,
) -> Dict[str, Any]:
    """Extract claims from in-memory `content` of `fmt` and ingest them."""
    return ingest_claims(extract_claims(content, fmt),
                         source=source, source_status=source_status,
                         source_sha256=evidence.sha256(content),
                         source_content=content)


def ingest_file(
    path: str, *, source: Optional[str] = None, fmt: Optional[str] = None,
    source_status: str = EXTERNAL,
) -> Dict[str, Any]:
    """
    Import a knowledge file into the canon through the TruthGate.

    Stdlib formats (.txt/.md/.json/.jsonl/.csv) are handled natively.
    Optional-dependency formats (.yaml/.pdf/.ttl/…) are handled by WP4
    adapters auto-loaded from core.adapters when the relevant extra is
    installed. `source` defaults to the file's basename; `fmt` is inferred
    from the extension unless given.     Raises on an unsupported extension.
    """
    safe = resolve_safe_path(path)
    path = str(safe)
    ext = (fmt or os.path.splitext(path)[1]).lower()
    if not ext.startswith("."):
        ext = "." + ext
    src = source or os.path.basename(path)
    if ext in _SUPPORTED:
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        return ingest_text(content, fmt=ext.lstrip("."),
                           source=src, source_status=source_status)
    # Fall back to optional WP4 adapters (yaml / pdf / rdf …).
    # ImportError is re-raised with an install hint; ValueError for truly unknown.
    from core.adapters import load as _load_adapter
    adapter_fn = _load_adapter(ext.lstrip("."))
    claims = adapter_fn(path)
    with open(path, "rb") as fh:
        sha256_hex = hashlib.sha256(fh.read()).hexdigest()
    return ingest_claims(claims, source=src, source_status=source_status,
                         source_sha256=sha256_hex)
