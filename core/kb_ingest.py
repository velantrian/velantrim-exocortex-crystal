# core/kb_ingest.py
# Velantrim ExoCortex — KB Dry-Run Batch Manifest (grant WP2/WP4 hardening)
#
# An institution wants to preview what would happen if they imported a curated
# knowledge-base corpus before committing any writes. This module accepts a
# batch manifest — a list of claim records or a JSONL/JSON file — and returns
# a structured per-item verdict report WITHOUT writing anything to memory.
#
# Verdicts per item (same as imports.predict_claim):
#   accept    — would pass Guardian + TruthGate and be stored
#   reinforce — an identical claim already exists in canon (idempotent)
#   blocked   — rejected by Immune guard, Guardian, or TruthGate
#   conflict  — passes gates but contradicts one or more canonical facts
#
# This module is a thin batch orchestrator over imports.predict_claim. It adds:
#   - manifest file I/O (JSONL / JSON array)
#   - per-item row normalisation
#   - a compact summary dict
#   - the `kb-ingest` CLI surface

import json
import os
from typing import Any, Dict, List, Optional

from core.imports import predict_claim
from core import knowledge as _kb

_VERDICT_KEYS = ("accept", "reinforce", "blocked", "conflict")


# ─── Batch dry-run ────────────────────────────────────────────────────────────

def dry_run_batch(
    claims: List[Dict[str, Any]],
    *,
    source: str = "kb-manifest",
) -> Dict[str, Any]:
    """Run a dry-run gate prediction over a list of claim records.

    Each record must have a `"claim"` key. Optional keys:
      source_status  (default: EXTERNAL)
      claim_type     (auto-classified if absent)
      confidence     (default: 0.6)
      significance   (default: 0.5)

    Returns a manifest dict with a summary and per-item verdicts. Nothing is
    written to memory — identical behaviour to imports.predict_claim.
    """
    items: List[Dict[str, Any]] = []
    for rec in claims:
        claim_text = (rec.get("claim") or "").strip()
        kwargs: Dict[str, Any] = {"source": rec.get("source", source)}
        if rec.get("source_status"):
            kwargs["source_status"] = rec["source_status"]
        if rec.get("claim_type"):
            kwargs["claim_type"] = rec["claim_type"]
        if rec.get("confidence") is not None:
            kwargs["confidence"] = rec["confidence"]
        if rec.get("significance") is not None:
            kwargs["significance"] = rec["significance"]
        items.append(predict_claim(claim_text, **kwargs))
    return _manifest_result(items, source=source)


def dry_run_manifest_file(path: str, *, source: Optional[str] = None) -> Dict[str, Any]:
    """Read a JSONL or JSON-array manifest file and run a batch dry-run.

    Supported formats:
      - JSONL (.jsonl / .ndjson): one claim record per line
      - JSON array (.json): a top-level list of claim records

    Each record must have a `"claim"` key (see dry_run_batch).
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Manifest file not found: {path!r}")
    src = source or os.path.basename(path)
    ext = os.path.splitext(path)[1].lower()
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    if ext in (".jsonl", ".ndjson"):
        claims = [json.loads(line) for line in content.splitlines() if line.strip()]
    else:
        claims = json.loads(content)
        if not isinstance(claims, list):
            raise ValueError(
                f"JSON manifest must be a top-level array of claim records, "
                f"got {type(claims).__name__}"
            )
    return dry_run_batch(claims, source=src)


# ─── Internal helpers ─────────────────────────────────────────────────────────

def _manifest_result(items: List[Dict[str, Any]], *, source: str) -> Dict[str, Any]:
    counts: Dict[str, int] = {k: 0 for k in _VERDICT_KEYS}
    for it in items:
        v = it.get("verdict", "blocked")
        counts[v] = counts.get(v, 0) + 1
    return {
        "dry_run": True,
        "source": source,
        "total": len(items),
        "would_accept": counts["accept"],
        "would_reinforce": counts["reinforce"],
        "would_block": counts["blocked"],
        "conflicts": counts["conflict"],
        "items": items,
    }
