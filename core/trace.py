# core/trace.py
# Velantrim ExoCortex — Trace / Provenance Layer
#
# Purpose: builds the provenance chain for each fact.
# Principle: Trace → Validation → Answer (not the other way around).
# Each trace element carries the epistemic_state from ESM.
#
# Full architecture: docs/archive/Velantrim_V8_Crystal_Sprint1_toc.md

from typing import List, Dict, Any
from datetime import datetime, timezone
from core.memory import ESM_STATES


# ─── TRACE BUILDER ────────────────────────────────────────────────────────────

def _safe_score(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0.0
    try:
        score = float(value)
    except OverflowError:
        return 0.0
    return score if score == score and score not in (float("inf"), float("-inf")) else 0.0


def build_trace(retrieved: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build TRACE v2: query-local retrieval explanation, never evidence authority."""
    trace: List[Dict[str, Any]] = []
    now = datetime.now(timezone.utc).isoformat()

    for fallback_rank, item in enumerate(retrieved, 1):
        fact_id = item.get("id") or item.get("fact_id")
        if not fact_id:
            continue
        rank = item.get("_retrieval_rank", fallback_rank)
        if isinstance(rank, bool) or not isinstance(rank, int) or rank < 1:
            rank = fallback_rank
        signals = item.get("_retrieval_signals", [])
        if not isinstance(signals, list):
            signals = []
        signals = [signal for signal in signals if isinstance(signal, str) and signal]
        if not signals:
            signals = [str(item.get("origin", "retrieval"))]

        source = item.get("source")
        if not isinstance(source, str) or not source.strip():
            source = "unknown"

        entry: Dict[str, Any] = {
            "trace_version": 2,
            "fact_id": fact_id,
            "source": source,
            "origin": item.get("origin", "retrieval"),
            "epistemic_state": item.get("epistemic_state", "Observed"),
            "retrieval_rank": rank,
            "retrieval_score": round(_safe_score(item.get("_score", 0.0)), 4),
            "retrieval_signals": list(dict.fromkeys(signals)),
            "active_embedder_id": item.get("_active_embedder_id"),
            "stored_embedder_id": item.get("_stored_embedder_id"),
            "retrieval_mode": item.get("_retrieval_mode"),
            "retrieval_config_id": item.get("_retrieval_config_id"),
            "projection_id": item.get("_projection_id"),
            "retrieved_at": now,
        }
        graph_explanation = item.get("_graph_explanation")
        if isinstance(graph_explanation, dict):
            entry["graph_explanation"] = graph_explanation
        trace.append(entry)

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
            f"retrieval_score={el.get('retrieval_score', '?')}"
        )
    return "\n".join(lines)
