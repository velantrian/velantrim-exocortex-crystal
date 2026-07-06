# core/imports.py
# Velantrim ExoCortex — Import Sessions & Dry-run Review (grant WP2)
#
# External ingestion (core/knowledge.py) routes a corpus through the TruthGate.
# WP2 makes that safe for institutions importing curated corpora:
#
#   - DRY RUN: predict what an import WOULD do — accept / duplicate / block /
#     conflict — WITHOUT writing anything to the canon (no L0/L1/L3, no evidence).
#   - IMPORT SESSIONS: every real import gets a session id; the facts it accepts
#     are recorded so the whole batch can be reviewed, restricted or erased
#     together (a librarian can pull a bad corpus back out in one call).
#
# The dry run reuses the SAME validators as the live path (classify → immune
# pre-screen → Guardian → TruthGate → conflict check), so the preview matches the
# real decision — it just never persists.

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Iterable

from core import memory, knowledge, immune, contradiction
from core.path_safety import resolve_safe_path
from core.ingest import classify_claim, _fact_id
from core.pipeline import guardian, truth_gate
from core.reconcile import find_conflicts
from core.compliance import restrict_processing
from core.erasure import erase_fact


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ─── Dry-run prediction (no writes) ───────────────────────────────────────────

def predict_claim(
    claim: str, *, source: str = "external", source_status: str = knowledge.EXTERNAL,
    claim_type: Optional[str] = None, confidence: float = 0.6,
    significance: float = 0.5,
) -> Dict[str, Any]:
    """
    Predict the verdict for a single claim WITHOUT persisting anything.
    Verdicts: accept | duplicate | blocked | conflict.
    """
    claim = (claim or "").strip()
    if not claim:
        return {"claim": claim, "verdict": "blocked", "reason": "empty claim"}

    ct, classified = classify_claim(claim)
    if claim_type is not None:
        ct = claim_type
    ss = source_status or classified
    fid = _fact_id(claim)

    # Already-Validated exact duplicate → the live path records an occurrence
    # (frequency only; no reinforce, no confidence change) — see ingest dedup.
    prior = memory.get_fact(fid)
    if prior is not None and prior.get("epistemic_state") == "Validated":
        return {"claim": claim, "verdict": "duplicate", "fact_id": fid,
                "claim_type": ct}

    fact = {
        "fact_id": fid, "claim": claim, "source": source, "confidence": confidence,
        "epistemic_state": "Observed", "claim_type": ct, "source_status": ss,
        "significance": significance,
    }
    pre = immune.screen(claim, fact_id=fid, check_canon=False)
    if pre["verdict"] == immune.BLOCK:
        return {"claim": claim, "verdict": "blocked",
                "reason": f"Immune: {pre.get('reason', '')}"}

    facts_pack = {"facts": [fact], "query": claim, "total": 1}
    trace = [{"fact_id": fid, "source": source, "origin": "dry-run",
              "epistemic_state": "Observed", "confidence": confidence}]
    ok, reason = guardian(facts_pack, trace)
    if ok:
        ok, reason = truth_gate(facts_pack)
    if not ok:
        return {"claim": claim, "verdict": "blocked", "reason": reason}

    conflicts = find_conflicts(claim, fact_id=fid) if ct == "WORLD_FACT" else []
    contradictions = [c for c in conflicts
                      if c["kind"] == contradiction.CONTRADICTION]
    if contradictions:
        return {"claim": claim, "verdict": "conflict", "claim_type": ct,
                "conflicts": [c["fact_id"] for c in contradictions]}
    return {"claim": claim, "verdict": "accept", "claim_type": ct}


def _summarise(items: List[Dict[str, Any]], *, source: str) -> Dict[str, Any]:
    counts = {"accept": 0, "duplicate": 0, "blocked": 0, "conflict": 0}
    for it in items:
        counts[it["verdict"]] = counts.get(it["verdict"], 0) + 1
    return {
        "dry_run": True, "source": source, "total": len(items),
        "would_accept": counts["accept"], "would_duplicate": counts["duplicate"],
        "would_block": counts["blocked"], "conflicts": counts["conflict"],
        "items": items,
    }


def dry_run_text(content: str, *, fmt: str = "txt", source: str = "external",
                 source_status: str = knowledge.EXTERNAL) -> Dict[str, Any]:
    """Preview a corpus from in-memory content. Writes nothing."""
    items = [predict_claim(rec.get("claim", ""), source=source,
                           source_status=source_status,
                           claim_type=rec.get("claim_type"),
                           **{k: rec[k] for k in ("confidence", "significance")
                              if rec.get(k) is not None})
             for rec in knowledge.extract_claims(content, fmt)]
    return _summarise(items, source=source)


def dry_run_file(path: str, *, source: Optional[str] = None,
                 fmt: Optional[str] = None) -> Dict[str, Any]:
    """Preview a knowledge file (stdlib or WP4 adapter formats). Writes nothing."""
    safe = resolve_safe_path(path)
    path = str(safe)
    ext = (fmt or os.path.splitext(path)[1]).lower()
    if not ext.startswith("."):
        ext = "." + ext
    src = source or os.path.basename(path)
    if ext in knowledge._SUPPORTED:
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        return dry_run_text(content, fmt=ext.lstrip("."), source=src)
    # Optional WP4 adapter path (yaml / pdf / rdf …).
    from core.adapters import load as _load_adapter
    adapter_fn = _load_adapter(ext.lstrip("."))
    claims = adapter_fn(path)
    items = [predict_claim(rec.get("claim", ""), source=src,
                           source_status=knowledge.EXTERNAL,
                           claim_type=rec.get("claim_type"),
                           **{k: rec[k] for k in ("confidence", "significance")
                              if rec.get(k) is not None})
             for rec in claims]
    return _summarise(items, source=src)


# ─── Real import with a session ───────────────────────────────────────────────

def _record_session(session_id: str, fact_ids: Iterable[str], source: str) -> None:
    ts = _now()
    with memory._db() as conn:
        for fid in fact_ids:
            conn.execute(
                "INSERT OR IGNORE INTO import_sessions "
                "(session_id, fact_id, source, created_at) VALUES (?, ?, ?, ?)",
                (session_id, fid, source, ts))


def import_file(path: str, *, source: Optional[str] = None,
                session_id: Optional[str] = None,
                dry_run: bool = False) -> Dict[str, Any]:
    """
    Import a knowledge file through the TruthGate (writing), recording an import
    session so the batch can later be restricted or erased together. With
    `dry_run=True`, predicts the outcome and writes nothing.
    """
    if dry_run:
        return dry_run_file(path, source=source)
    session_id = session_id or ("imp:" + uuid.uuid4().hex[:12])
    rep = knowledge.ingest_file(path, source=source)
    # Session membership must track only facts THIS import newly created
    # (new_fact_ids), not every accepted hit (rep["fact_ids"] also includes
    # duplicates of pre-existing facts) — otherwise restrict_session()/
    # erase_session() on this batch would act on a fact this batch never
    # created.
    _record_session(session_id, rep["new_fact_ids"], rep["source"])
    rep["session_id"] = session_id
    return rep


def session_facts(session_id: str) -> List[str]:
    """Fact ids accepted under an import session."""
    with memory._db() as conn:
        rows = conn.execute(
            "SELECT fact_id FROM import_sessions WHERE session_id = ? "
            "ORDER BY created_at", (session_id,)).fetchall()
    return [r["fact_id"] for r in rows]


def restrict_session(session_id: str) -> Dict[str, Any]:
    """Art. 18 processing restriction applied to every fact in the session."""
    fids = session_facts(session_id)
    done = sum(1 for fid in fids if restrict_processing(fid).get("found"))
    return {"session_id": session_id, "facts": len(fids), "restricted": done}


def erase_session(session_id: str, *, reason: str = "session_erase") -> Dict[str, Any]:
    """Art. 17 physical erasure applied to every fact in the session."""
    fids = session_facts(session_id)
    done = sum(1 for fid in fids if erase_fact(fid, reason=reason).get("erased_now"))
    return {"session_id": session_id, "facts": len(fids), "erased": done}
