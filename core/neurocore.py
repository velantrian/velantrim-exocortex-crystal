# core/neurocore.py
# Velantrim ExoCortex — NeuroCore Plastic Memory Layer (RFC0068, Phase 0)
#
# NeuroCore is a plastic layer that, in later phases, will adapt an SSM model
# (Mamba-3 / RWKV-7 class) DURING a dialogue via a Hebbian update governed by the
# existing decay system:
#
#     s_t = (1 − λ·dt)·s_{t−1} + α · 𝕀(surprise > θ) · (x_t ⊗ k_t)
#
# This module ships **Phase 0 only — a PASSIVE TRACKER**. It computes the norm of
# the would-be weight delta ΔW and logs it; it does NOT apply anything to a model.
#
# Key invariant — I68 (NeuroCoreIsolation):
#   NeuroCore NEVER modifies the L3 graph. Graph = Truth is absolute. On any
#   conflict, L3 wins. This module therefore imports NOTHING from core.l3_graph
#   and writes only to its own observation table (`neurocore_delta_log`).
#
# Deployment phases (only Phase 0 is implemented here):
#   0 — Passive tracker : log ΔW to SQLite; model untouched.            ✅ current
#   1 — Active NLM      : apply updates (after analysing Phase 0 metrics). ⏳ pending
#   2 — Consolidation   : NeuroCore → L3 via TruthGate.                   ⏳ pending
#
# Disabled by default. Enable the passive tracker with VELANTRIM_NEUROCORE=1.
#
# Wiring: pipeline.run() calls observe() once per query (surprise ≈ 1 − top
# retrieval relevance) when VELANTRIM_NEUROCORE=1, so the tracker records real
# ΔW data during normal operation. Strictly Phase 0 — observe() only logs to
# `neurocore_delta_log` and never touches the model or L3 (invariant I68).
# Inspect with `velantrim neurocore-report`.

import math
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

from core import memory, metrics

# ─── Configuration (env-driven, matches the project's flag idiom) ─────────────

_ENV_ENABLED = "VELANTRIM_NEUROCORE"          # master feature-flag (Phase 0 tracker)
_ENV_THETA = "VELANTRIM_NEUROCORE_THETA"      # surprise threshold θ
_ENV_ALPHA = "VELANTRIM_NEUROCORE_ALPHA"      # learning rate α (fixed)

_DEFAULT_THETA = 0.6
_DEFAULT_ALPHA = 0.01

_TRUE = ("1", "true", "yes", "on")


def enabled() -> bool:
    """True only when the Phase 0 passive tracker is explicitly switched on."""
    return os.environ.get(_ENV_ENABLED, "").lower() in _TRUE


def surprise_theta() -> float:
    """θ — NeuroCore observes an update only when surprise > θ."""
    try:
        return float(os.environ.get(_ENV_THETA, _DEFAULT_THETA))
    except ValueError:
        return _DEFAULT_THETA


def alpha() -> float:
    """α — fixed learning rate scaling the (passive) weight delta."""
    try:
        return float(os.environ.get(_ENV_ALPHA, _DEFAULT_ALPHA))
    except ValueError:
        return _DEFAULT_ALPHA


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _l2(vec: Sequence[float]) -> float:
    return math.sqrt(sum(float(v) * float(v) for v in vec))


# ─── Phase 0: passive observation ─────────────────────────────────────────────

def observe(
    surprise_score: float,
    *,
    x: Optional[Sequence[float]] = None,
    k: Optional[Sequence[float]] = None,
    delta_norm: Optional[float] = None,
    domain: str = "default",
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Phase 0 passive tick. NeuroCore would update its plastic state by
    ΔW = α·(x ⊗ k) **only** when surprise > θ. Here we merely compute and log the
    norm of that delta; the model is never touched and the graph is never written.

    The delta norm is ‖α·(x ⊗ k)‖ = α·‖x‖·‖k‖. Provide either the input/context
    vectors `x`/`k`, or a precomputed `delta_norm`.

    Returns a result dict; when disabled or below threshold, nothing is logged.
    """
    if not enabled():
        return {"enabled": False, "logged": False, "reason": "disabled"}

    theta = surprise_theta()
    if surprise_score <= theta:
        # No surprise → NeuroCore does not update (and logs nothing).
        metrics.incr("neurocore.below_threshold")
        return {"enabled": True, "logged": False, "reason": "surprise<=theta",
                "surprise_score": surprise_score, "theta": theta}

    if delta_norm is None:
        if x is None or k is None:
            raise ValueError("observe: provide either delta_norm or both x and k")
        delta_norm = alpha() * _l2(x) * _l2(k)
    delta_norm = float(delta_norm)

    ts = _now()
    with memory._db() as conn:
        conn.execute(
            "INSERT INTO neurocore_delta_log "
            "(timestamp, surprise_score, delta_norm, domain, session_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (ts, float(surprise_score), delta_norm, domain, session_id),
        )
    metrics.incr("neurocore.surprise_events")
    metrics.incr(f"neurocore.domain.{domain}")
    return {
        "enabled": True,
        "logged": True,
        "timestamp": ts,
        "surprise_score": float(surprise_score),
        "delta_norm": delta_norm,
        "domain": domain,
        "session_id": session_id,
    }


def log_entries(limit: int = 100) -> List[Dict[str, Any]]:
    """Most-recent Phase 0 observations (newest first)."""
    with memory._db() as conn:
        rows = conn.execute(
            "SELECT timestamp, surprise_score, delta_norm, domain, session_id "
            "FROM neurocore_delta_log ORDER BY id DESC LIMIT ?",
            (int(limit),),
        ).fetchall()
    return [dict(r) for r in rows]


def report() -> Dict[str, Any]:
    """
    Aggregate Phase 0 telemetry — what NeuroCore *would* have learned. Used to
    decide whether activating Phase 1 is safe (delta stability, surprise volume).
    """
    with memory._db() as conn:
        agg = conn.execute(
            "SELECT COUNT(*) AS n, "
            "       AVG(delta_norm) AS avg_norm, "
            "       MAX(delta_norm) AS max_norm "
            "FROM neurocore_delta_log"
        ).fetchone()
        by_domain = conn.execute(
            "SELECT domain, COUNT(*) AS n FROM neurocore_delta_log "
            "GROUP BY domain ORDER BY n DESC"
        ).fetchall()
    return {
        "enabled": enabled(),
        "phase": 0,
        "theta": surprise_theta(),
        "alpha": alpha(),
        "surprise_events": agg["n"] or 0,
        "avg_delta_norm": agg["avg_norm"] or 0.0,
        "max_delta_norm": agg["max_norm"] or 0.0,
        "by_domain": {r["domain"]: r["n"] for r in by_domain},
    }
