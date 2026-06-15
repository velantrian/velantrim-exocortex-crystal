# core/health.py
# Velantrim ExoCortex — Memory-health diagnostic
#
# A single, read-only diagnostic score derived from the existing memory_report()
# observability snapshot (core/observe.py). It summarises the state of the L3
# canonical graph — average confidence minus penalties for contradicted,
# deprecated and weak-confidence facts.
#
# This is a *diagnostic memory-health* score. It is NOT a truth guarantee,
# NOT a compliance score, and NOT a production-readiness score. There is exactly
# one score; no separate "Epistemic Transparency Score" is introduced.

from typing import Dict, Any

from core.observe import memory_report

_MEANING = "diagnostic memory-health score, not a truth guarantee"


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def health_score() -> Dict[str, Any]:
    """
    One read-only diagnostic memory-health score, derived from memory_report().

    health_score = clamp(
        avg_confidence
        - contradicted_ratio    * 0.30
        - deprecated_ratio       * 0.20
        - weak_confidence_ratio  * 0.20
    )

    Deterministic and read-only: it only reads the L3 observability snapshot and
    never writes to L1/L3 or mutates any state.
    """
    report = memory_report()
    n = report["total_facts"]
    avg_confidence = report["avg_confidence"]

    contradicted_ratio = round(len(report["contradicted"]) / n, 4) if n else 0.0
    deprecated_ratio = round(len(report["deprecated"]) / n, 4) if n else 0.0
    weak_confidence_ratio = round(len(report["weak_confidence"]) / n, 4) if n else 0.0

    score = _clamp(
        avg_confidence
        - contradicted_ratio * 0.30
        - deprecated_ratio * 0.20
        - weak_confidence_ratio * 0.20
    )

    return {
        "health_score": round(score, 4),
        "meaning": _MEANING,
        "components": {
            "total_facts": n,
            "avg_confidence": avg_confidence,
            "contradicted_ratio": contradicted_ratio,
            "deprecated_ratio": deprecated_ratio,
            "weak_confidence_ratio": weak_confidence_ratio,
        },
    }
