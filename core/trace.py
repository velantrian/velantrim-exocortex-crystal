# core/trace.py
# Velantrim ExoCortex — Trace / Provenance Layer
# v8.7.0-sprint2
#
# Purpose: builds the provenance chain for each fact.
# Principle: Trace → Validation → Answer (not the other way around).
# Each trace element carries the epistemic_state from ESM.
#
# Full architecture: docs/Velantrim_V8_Crystal_Sprint1_toc.md

from typing import List, Dict, Any
from datetime import datetime, timezone
from core.memory import ESM_STATES


# ─── TRACE BUILDER ────────────────────────────────────────────────────────────

def build_trace(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build a trace chain from a list of retrieved facts.

    Each element contains:
      - fact_id:         the fact's identifier
      - source:          source (where the fact came from)
      - origin:          how it was obtained (retrieval / ingestion / volition)
      - epistemic_state: the fact's current ESM state
      - retrieved_at:    the retrieval timestamp

    epistemic_state:
      Observed → the fact was just obtained from retrieval, not yet verified.
      Validated → passed the TruthGate (set in the pipeline after truth_gate()).
      Full list of ESM states: core/memory.py → ESM_STATES.
    """
    trace: List[Dict[str, Any]] = []
    now = datetime.now(timezone.utc).isoformat()

    for item in retrieved:
        fact_id = item.get("id") or item.get("fact_id")
        if not fact_id:
            continue  # skip malformed entries

        trace.append({
            "fact_id":         fact_id,
            "source":          item.get("source", "unknown"),
            "origin":          item.get("origin", "retrieval"),
            "epistemic_state": item.get("epistemic_state", "Observed"),
            "confidence":      round(float(item.get("_score", 0.5)), 4),
            "retrieved_at":    now,
        })

    return trace


def promote_trace(
    trace: List[Dict[str, Any]],
    new_state: str
) -> None:
    """
    Update the epistemic_state of all trace elements after passing the TruthGate.
    Called from the pipeline after truth_gate() → True.
    Mutates the trace elements in-place.

    Example: promote_trace(trace, "Validated")
    """
    if new_state not in ESM_STATES:
        raise ValueError(f"promote_trace: invalid ESM state '{new_state}'")

    now = datetime.now(timezone.utc).isoformat()
    for element in trace:
        element["epistemic_state"] = new_state
        element["promoted_at"] = now


def format_trace(trace: List[Dict[str, Any]]) -> str:
    """
    Human-readable rendering of the trace chain for logs and the answer.
    """
    if not trace:
        return "TRACE: empty"
    lines = ["TRACE:"]
    for i, el in enumerate(trace, 1):
        lines.append(
            f"  [{i}] {el.get('fact_id', '?')} | "
            f"source={el.get('source', '?')} | "
            f"state={el.get('epistemic_state', '?')} | "
            f"confidence={el.get('confidence', '?')}"
        )
    return "\n".join(lines)
