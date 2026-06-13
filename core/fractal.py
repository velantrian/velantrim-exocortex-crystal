# core/fractal.py
# Velantrim ExoCortex — Fractal Memory Layer (RFC0070)
#
# Recursive anchoring across self-similar time scales (SHORT → MEDIUM → LONG →
# CORE), inspired by FractalNet and the brain's short/medium/long-term memory
# hierarchy. The goal is lifelong learning WITHOUT catastrophic forgetting: the
# strongest, most-reinforced knowledge is anchored into deeper, scarcer, better-
# protected scales, where it resists the confidence drift that SleepCycle applies
# to everything else (see core/consolidate.py).
#
# How it integrates with what already exists (no parallel store, no new fact
# table — the canon stays the single source of truth):
#   - Every canonical (Validated) fact already carries significance, confidence
#     and a reinforcement count (metadata['observations'], raised by reconcile.
#     reinforce). From these we compute a deterministic anchor_strength ∈ [0,1].
#   - reanchor() sorts facts by strength into self-similar bands and writes the
#     assigned scale into metadata['fractal_scale'] (which every L3 backend
#     persists). The bands have FRACTAL capacities — base, base/2, base/4, base/8
#     from SHORT to CORE — so the deep scales are scarce; overflow spills DOWN to
#     the next scale (graceful, never deleted).
#   - SleepCycle reads fractal_scale and lengthens the half-life by a per-scale
#     protection factor (CORE is anchored — exempt from decay). A fact with no
#     assigned scale behaves exactly as before, so the layer is inert until
#     reanchor() is run (opt-in, like the immune memory).
#
# Everything is deterministic, dependency-free and explainable.

import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core.memory import get_fact, update_fact
from core.l3_graph import get_l3_graph
from core import metrics

# ─── Scales (self-similar hierarchy, shallow → deep) ──────────────────────────
SHORT = "SHORT"
MEDIUM = "MEDIUM"
LONG = "LONG"
CORE = "CORE"
# Shallow (fast-fading) → deep (anchored). Order matters for spill-down.
SCALES = [SHORT, MEDIUM, LONG, CORE]

# anchor_strength band thresholds (a fact lands in the deepest band it clears).
_BANDS = [(CORE, 0.80), (LONG, 0.55), (MEDIUM, 0.30), (SHORT, 0.0)]

# Fractal capacity divisor per scale: base // 2**level. SHORT is the widest,
# CORE the scarcest — the self-similar halving of the prototype, applied as
# how-many-facts-each-scale-holds rather than as nested blocks.
_CAP_DIVISOR = {SHORT: 1, MEDIUM: 2, LONG: 4, CORE: 8}

# Decay protection: SleepCycle's effective half-life is multiplied by this. CORE
# is exempt entirely (anchored against drift) — see core/consolidate.py.
_PROTECTION = {SHORT: 1.0, MEDIUM: 2.0, LONG: 4.0, CORE: float("inf")}

_ENV_BASE = "VELANTRIM_FRACTAL_BASE"
_DEFAULT_BASE = 1024


def _base_capacity() -> int:
    try:
        return max(1, int(os.environ.get(_ENV_BASE, _DEFAULT_BASE)))
    except ValueError:
        return _DEFAULT_BASE


def capacities(base: Optional[int] = None) -> Dict[str, int]:
    """Per-scale capacity = base // 2**level (fractal halving)."""
    base = base if base is not None else _base_capacity()
    return {s: max(1, base // _CAP_DIVISOR[s]) for s in SCALES}


def anchor_strength(fact: Dict[str, Any]) -> float:
    """
    Deterministic anchoring strength ∈ [0,1] for a fact.

    Three explainable, orthogonal drivers — what the system was told matters
    (significance), what it keeps re-confirming (reinforcement), and how sure it
    currently is (confidence):
        0.45·significance + 0.35·reinforcement + 0.20·confidence
    reinforcement = 1 − 1/observations (0 for a single observation, saturating
    toward 1 as independent evidence accumulates).
    """
    sig = min(1.0, max(0.0, float(fact.get("significance", 0.5))))
    conf = min(1.0, max(0.0, float(fact.get("confidence", 0.5))))
    meta = fact.get("metadata") or {}
    obs = max(1, int(meta.get("observations", 1)))
    reinforcement = 1.0 - 1.0 / obs
    return round(0.45 * sig + 0.35 * reinforcement + 0.20 * conf, 4)


def scale_for_strength(strength: float) -> str:
    """The deepest band a strength value clears (before capacity spill-down)."""
    for scale, floor in _BANDS:
        if strength >= floor:
            return scale
    return SHORT


def protection_factor(scale: Optional[str]) -> float:
    """Half-life multiplier for a scale (∞ = anchored, exempt from decay).
    An unknown/unset scale → 1.0, so unanchored facts decay as before."""
    return _PROTECTION.get(scale or SHORT, 1.0)


def is_anchored(scale: Optional[str]) -> bool:
    """True if the scale is exempt from SleepCycle decay (CORE)."""
    return protection_factor(scale) == float("inf")


def _validated_records() -> List[Dict[str, Any]]:
    """Authoritative SQLite records for the canonical (Validated) facts. Falls
    back to the L3 node when no L1 record exists (e.g. recall-only nodes)."""
    graph = get_l3_graph()
    out: List[Dict[str, Any]] = []
    for node in graph.all_facts():
        if node.get("epistemic_state") != "Validated":
            continue
        out.append(get_fact(node["fact_id"]) or node)
    return out


def reanchor(*, base: Optional[int] = None) -> Dict[str, Any]:
    """
    Recompute fractal scales over the canon (recursive anchoring).

    1. Score every Validated fact by anchor_strength.
    2. Place it in the deepest band it clears.
    3. Enforce fractal capacities: a deep scale that overflows spills its WEAKEST
       members down to the next-shallower scale (nothing is deleted).
    4. Persist the assigned scale into metadata['fractal_scale'] and re-merge.

    Returns {'assigned': {scale: count}, 'capacities': {...}, 'reanchored': n,
    'at': iso}. Idempotent: re-running with unchanged facts reassigns the same
    scales and re-writes the same metadata.
    """
    caps = capacities(base)
    # Strongest first, so the strongest facts claim the scarce deep slots before
    # weaker ones — a single, obviously-conserving pass (nothing is dropped).
    scored = sorted(
        ((f, anchor_strength(f)) for f in _validated_records()),
        key=lambda fs: fs[1], reverse=True,
    )
    remaining = dict(caps)
    graph = get_l3_graph()
    now = datetime.now(timezone.utc).isoformat()
    assigned = {s: 0 for s in SCALES}
    reanchored = 0
    for fact, strength in scored:
        # Place at the deepest scale that the strength qualifies for AND still has
        # capacity; otherwise spill toward SHORT. SHORT is the floor (its overflow
        # simply stays SHORT and fades fastest), so a slot is always found.
        idx = SCALES.index(scale_for_strength(strength))
        placed = SHORT
        for j in range(idx, -1, -1):
            if remaining[SCALES[j]] > 0:
                placed = SCALES[j]
                remaining[placed] -= 1
                break
        assigned[placed] += 1
        meta = dict(fact.get("metadata") or {})
        if meta.get("fractal_scale") == placed:
            continue  # already at this scale — no rewrite needed
        meta["fractal_scale"] = placed
        if update_fact(fact["fact_id"], metadata=meta):
            graph.merge_fact(get_fact(fact["fact_id"]))
            reanchored += 1
    metrics.incr("fractal.reanchor")
    return {"assigned": assigned, "capacities": caps,
            "reanchored": reanchored, "at": now}


def anchors(scale: Optional[str] = None) -> List[Dict[str, Any]]:
    """Canonical facts at a given scale (or all scales), strongest first.
    Returns a compact view: fact_id, claim, scale, strength."""
    out: List[Dict[str, Any]] = []
    for f in _validated_records():
        s = (f.get("metadata") or {}).get("fractal_scale")
        if scale is not None and s != scale:
            continue
        out.append({
            "fact_id": f["fact_id"],
            "claim": f.get("claim", ""),
            "scale": s,
            "strength": anchor_strength(f),
        })
    out.sort(key=lambda a: a["strength"], reverse=True)
    return out


def fractal_report(*, base: Optional[int] = None) -> Dict[str, Any]:
    """Observable state of the fractal layer: counts and capacities per scale."""
    caps = capacities(base)
    by_scale = {s: 0 for s in SCALES}
    unanchored = 0
    for f in _validated_records():
        s = (f.get("metadata") or {}).get("fractal_scale")
        if s in by_scale:
            by_scale[s] += 1
        else:
            unanchored += 1
    return {
        "depth": len(SCALES),
        "base": base if base is not None else _base_capacity(),
        "capacities": caps,
        "by_scale": by_scale,
        "unanchored": unanchored,
        "anchored_total": sum(by_scale.values()),
    }
