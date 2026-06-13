# core/neurogenesis.py
# Velantrim ExoCortex — Neurogenesis-inspired Dynamic Growth (RFC0073)
#
# Adult Hippocampal Neurogenesis (AHN): the mammalian hippocampus keeps minting
# new neurons throughout life. Young neurons are highly PLASTIC (they learn fast),
# they MATURE into stable cells, and they enable PATTERN SEPARATION — keeping
# similar-but-distinct memories from collapsing into one. This is a pillar of
# lifelong learning and resistance to catastrophic forgetting.
#
# Mapped onto Velantrim's canon (no parallel store — facts ARE the neurons):
#   - plasticity(fact): a young fact (recently created) is highly plastic; it
#     matures toward a stable floor over a maturation window. Deterministic from
#     the fact's age (created_at), dependency-free.
#   - pattern separation: when a new fact is vectorally CLOSE to an existing one
#     but not a contradiction (a distinct-but-similar memory), neurogenesis spawns
#     a SEPARATED_FROM edge instead of letting the two blur together. Reuses the
#     conflict candidates ingest already computes; opt-in (VELANTRIM_NEURO_SEPARATION),
#     like auto-contradict, so default behaviour is unchanged.
#   - growth & capacity: growth_report() exposes the AHN stats (young/mature,
#     average plasticity, capacity headroom, a pattern-separation score), and
#     prune_candidates() lists mature+weak, non-anchored facts that could be
#     reclaimed to keep lifelong capacity — advisory only (deletion stays with
#     erasure, GDPR Art. 17). CORE fractal anchors are never prune candidates.
#
# Everything is deterministic, dependency-free and observable.

import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core.memory import get_fact
from core.l3_graph import get_l3_graph
from core import metrics, contradiction

REL_SEPARATED_FROM = "SEPARATED_FROM"

_ENV_PLASTICITY = "VELANTRIM_NEURO_PLASTICITY"      # initial plasticity p0 (default 2.0)
_ENV_MATURATION = "VELANTRIM_NEURO_MATURATION"      # maturation window in days (default 30)
_ENV_YOUNG = "VELANTRIM_NEURO_YOUNG"               # "young" age cutoff in days (default 10)
_ENV_MAX_NODES = "VELANTRIM_NEURO_MAX_NODES"        # capacity ceiling (default 100000)
_ENV_SEPARATION = "VELANTRIM_NEURO_SEPARATION"      # enable pattern separation at ingest
_ENV_SEPARATION_SIM = "VELANTRIM_NEURO_SEPARATION_SIM"  # min similarity to separate (0.85)

_PLASTICITY_FLOOR = 0.5


def _envf(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return default


def _envi(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _age_days(fact: Dict[str, Any], now: datetime) -> float:
    """Age of a fact in days from created_at (falling back to last_consolidated /
    updated_at). Unknown age → 0.0 (treated as freshly born)."""
    meta = fact.get("metadata") or {}
    baseline = (fact.get("created_at")
                or meta.get("last_consolidated")
                or fact.get("updated_at"))
    if not baseline:
        return 0.0
    try:
        born = datetime.fromisoformat(baseline)
    except (ValueError, TypeError):
        return 0.0
    return max(0.0, (now - born).total_seconds() / 86400.0)


def plasticity(fact: Dict[str, Any], *, now: Optional[datetime] = None) -> float:
    """
    Learning plasticity of a fact ∈ [floor, p0].

    Young (just created) → p0 (highly plastic); decays linearly to the floor over
    twice the maturation window, then stays at the floor (a stable, mature cell).
        plasticity = clamp(p0 · (1 − age / (2·window)), floor, p0)
    """
    now = now or _now()
    p0 = _envf(_ENV_PLASTICITY, 2.0)
    window = max(1.0, _envf(_ENV_MATURATION, 30.0))
    raw = p0 * (1.0 - _age_days(fact, now) / (2.0 * window))
    return round(max(_PLASTICITY_FLOOR, min(p0, raw)), 4)


def is_young(fact: Dict[str, Any], *, now: Optional[datetime] = None) -> bool:
    """True while a fact is within the 'young', highly-plastic window."""
    now = now or _now()
    return _age_days(fact, now) < _envf(_ENV_YOUNG, 10.0)


def separation_enabled() -> bool:
    """True if pattern separation runs automatically at ingest."""
    return os.environ.get(_ENV_SEPARATION, "").lower() in ("1", "true", "yes", "on")


def _sep_threshold() -> float:
    return _envf(_ENV_SEPARATION_SIM, 0.85)


def separate(
    fact_id: str,
    claim: str,
    *,
    conflicts: Optional[List[Dict[str, Any]]] = None,
    threshold: Optional[float] = None,
) -> List[str]:
    """
    Pattern separation: record SEPARATED_FROM edges from fact_id to canonical
    neighbours that are vectorally close (similarity ≥ threshold) but NOT a
    contradiction — distinct memories that must not blur together.

    Reuses the caller's conflict candidates when given (ingest already computes
    them); otherwise computes them. Returns the neighbour ids separated from.
    """
    thr = threshold if threshold is not None else _sep_threshold()
    if conflicts is None:
        from core.reconcile import find_conflicts  # lazy: avoid import cycle
        conflicts = find_conflicts(claim, fact_id=fact_id)
    neighbours = [
        c for c in conflicts
        if c.get("kind") != contradiction.CONTRADICTION
        and float(c.get("similarity", 0.0)) >= thr
    ]
    if not neighbours:
        return []
    graph = get_l3_graph()
    now = _now().isoformat()
    separated: List[str] = []
    for c in neighbours:
        graph.add_edge(fact_id, REL_SEPARATED_FROM, c["fact_id"],
                       {"at": now, "similarity": float(c.get("similarity", 0.0))})
        separated.append(c["fact_id"])
    metrics.incr("neuro.separated")
    return separated


def _validated_records() -> List[Dict[str, Any]]:
    """Authoritative SQLite records for canonical (Validated) facts."""
    graph = get_l3_graph()
    out: List[Dict[str, Any]] = []
    for node in graph.all_facts():
        if node.get("epistemic_state") != "Validated":
            continue
        out.append(get_fact(node["fact_id"]) or node)
    return out


def growth_report(*, now: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Neurogenesis state over the canon (AHN stats):
      total / young / mature counts, average plasticity, capacity ceiling and
      headroom, at_capacity flag, and a pattern-separation score (fraction of the
      population that is young — more young cells ⇒ better separation capacity).
    """
    now = now or _now()
    records = _validated_records()
    total = len(records)
    young = sum(1 for f in records if is_young(f, now=now))
    avg_plast = (round(sum(plasticity(f, now=now) for f in records) / total, 4)
                 if total else 0.0)
    max_nodes = _envi(_ENV_MAX_NODES, 100000)
    # Pattern separation improves with a healthy young-cell pool (prototype metric:
    # young / (total · 0.3), capped at 1.0).
    sep_score = round(min(1.0, young / (total * 0.3)), 4) if total else 0.0
    return {
        "total": total,
        "young": young,
        "mature": total - young,
        "avg_plasticity": avg_plast,
        "max_nodes": max_nodes,
        "headroom": max(0, max_nodes - total),
        "at_capacity": total >= max_nodes,
        "pattern_separation": sep_score,
    }


def prune_candidates(
    *,
    now: Optional[datetime] = None,
    max_confidence: float = 0.2,
    min_age_days: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Mature, weak, non-anchored facts that could be reclaimed to free capacity
    (advisory only — actual deletion is core.erasure.erase_fact, GDPR Art. 17).

    A candidate is: confidence < max_confidence AND age ≥ min_age_days (default:
    the maturation window) AND not anchored to the CORE fractal scale (CORE
    anchors are protected — see core/fractal.py). Weakest first.
    """
    now = now or _now()
    min_age = (min_age_days if min_age_days is not None
               else _envf(_ENV_MATURATION, 30.0))
    out: List[Dict[str, Any]] = []
    for f in _validated_records():
        if float(f.get("confidence", 1.0)) >= max_confidence:
            continue
        if _age_days(f, now) < min_age:
            continue
        if (f.get("metadata") or {}).get("fractal_scale") == "CORE":
            continue  # protected anchor — never a prune candidate
        out.append({
            "fact_id": f["fact_id"],
            "claim": f.get("claim", ""),
            "confidence": float(f.get("confidence", 0.0)),
            "age_days": round(_age_days(f, now), 2),
        })
    out.sort(key=lambda c: c["confidence"])
    return out
