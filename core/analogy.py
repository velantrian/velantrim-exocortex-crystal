# core/analogy.py
# Velantrim ExoCortex — Analogy Graph, Semantic Bridge Engine, CREATIVE mode (RFC0067 v2.0)
# v8.21.0-sprint4
#
# "Creative intelligence." Before RFC0067 the system had no explicit map of
# metaphors and could not build semantic bridges between distant domains. This
# module adds three things, all dependency-free and deterministic:
#
#   1. Analogy Graph — explicit associative edges between nodes:
#        METAPHOR_OF  (directional: "a is a metaphor of b")
#        ANALOGOUS_TO (symmetric:   "a is analogous to b")
#      These are ASSOCIATIONS, not truth claims. They are edges, never :Fact —
#      so Graph = Truth is untouched (an analogy can be wild without lying about
#      the world, exactly like CONTRADICTS/SEPARATED_FROM edges).
#
#   2. Semantic Bridge Engine — find a *bridge* between two nodes WITHOUT an LLM:
#      a shared relational neighbour, a shared emergent concept, or an explicit
#      analogy edge. suggest_analogies() ranks structurally-similar nodes (shared
#      neighbourhood) as analogy CANDIDATES for review — the spec's
#      "suggested_analogies → manual audit" path, at zero tokens.
#
#   3. CREATIVE mode (Adaptive Decoder) — creative_temperature() yields a value in
#      [0.6, 0.85] for an LLM decoder, and creative_associations() surfaces the
#      analogy/bridge layer. Crucially, the FACTS a caller answers from stay
#      Validated-only (this module never fabricates or mutates facts): creativity
#      in framing, accuracy in substance.

import os
from typing import Dict, Any, List, Optional, Set

from core.l3_graph import get_l3_graph
from core import metrics, concept

REL_METAPHOR_OF = "METAPHOR_OF"
REL_ANALOGOUS_TO = "ANALOGOUS_TO"
_KINDS = (REL_METAPHOR_OF, REL_ANALOGOUS_TO)

_ENV_TEMP_MIN = "VELANTRIM_CREATIVE_TEMP_MIN"
_ENV_TEMP_MAX = "VELANTRIM_CREATIVE_TEMP_MAX"


def _envf(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return default


# ─── Analogy Graph ────────────────────────────────────────────────────────────

def link_analogy(
    src: str, dst: str, *,
    kind: str = REL_ANALOGOUS_TO, weight: float = 1.0, source: str = "manual",
) -> Dict[str, Any]:
    """
    Record an analogy edge. METAPHOR_OF is directional (src → dst); ANALOGOUS_TO
    is symmetric (both directions written). Idempotent for identical edges.
    Never creates a fact — Graph = Truth is preserved.
    """
    if kind not in _KINDS:
        raise ValueError(f"link_analogy: kind must be one of {_KINDS}, got {kind!r}")
    if src == dst:
        raise ValueError("link_analogy: src and dst must differ")
    w = max(0.0, min(1.0, float(weight)))
    props = {"weight": w, "source": source}
    graph = get_l3_graph()
    graph.add_edge(src, kind, dst, props)
    if kind == REL_ANALOGOUS_TO:
        graph.add_edge(dst, kind, src, props)   # symmetric
    metrics.incr("analogy.linked")
    return {"src": src, "dst": dst, "kind": kind, "weight": w, "source": source}


def analogies_for(
    node_id: str, *, kind: Optional[str] = None, min_weight: float = 0.0,
) -> List[Dict[str, Any]]:
    """Analogy edges leaving a node (target, kind, weight, source), strongest first."""
    kinds = (kind,) if kind else _KINDS
    graph = get_l3_graph()
    out: List[Dict[str, Any]] = []
    for k in kinds:
        for e in graph.get_edges(node_id, k):
            w = float(e.get("props", {}).get("weight", 1.0))
            if w < min_weight:
                continue
            out.append({"target": e["target"], "kind": k, "weight": w,
                        "source": e.get("props", {}).get("source", "manual")})
    out.sort(key=lambda a: (-a["weight"], a["kind"], a["target"]))
    return out


# ─── Structural similarity (the bridge substrate, no LLM) ──────────────────────

def _neighbours(node_id: str) -> Set[str]:
    """All graph nodes directly connected to node_id (any rel, either direction),
    excluding node_id itself."""
    graph = get_l3_graph()
    nb: Set[str] = set()
    for e in graph.get_edges(node_id):
        nb.add(e["target"])
    for e in graph.incoming_edges(node_id):
        nb.add(e["source"])
    nb.discard(node_id)
    return nb


def structural_similarity(a: str, b: str) -> float:
    """Jaccard overlap of two nodes' neighbourhoods ∈ [0,1] — how alike their
    relational structure is (the deterministic analogy signal)."""
    na, nb = _neighbours(a), _neighbours(b)
    if not na or not nb:
        return 0.0
    return round(len(na & nb) / len(na | nb), 4)


def suggest_analogies(
    node_id: str, *, k: int = 5, min_similarity: float = 0.1,
) -> List[Dict[str, Any]]:
    """
    Analogy CANDIDATES for a node: other canonical facts whose relational
    structure overlaps it (similarity ≥ min_similarity), strongest first. These
    are suggestions for review — nothing is written. Zero tokens.
    """
    graph = get_l3_graph()
    out: List[Dict[str, Any]] = []
    for node in graph.all_facts():
        other = node["fact_id"]
        if other == node_id:
            continue
        sim = structural_similarity(node_id, other)
        if sim < min_similarity:
            continue
        shared = sorted(_neighbours(node_id) & _neighbours(other))
        out.append({"node": other, "similarity": sim, "shared": shared})
    out.sort(key=lambda s: (-s["similarity"], s["node"]))
    return out[: max(0, k)]


# ─── Semantic Bridge Engine ────────────────────────────────────────────────────

def find_bridges(a: str, b: str) -> List[Dict[str, Any]]:
    """
    Semantic bridges between two nodes (deterministic, no LLM / no Redis):
      - explicit  : a direct METAPHOR_OF / ANALOGOUS_TO edge a→b
      - shared_neighbour : a node both a and b connect to
      - shared_concept   : an emergent concept (RFC0066) both belong to
    Returns the bridges that explain how two distant ideas connect.
    """
    bridges: List[Dict[str, Any]] = []

    for e in analogies_for(a):
        if e["target"] == b:
            bridges.append({"type": "explicit", "kind": e["kind"], "via": None,
                            "weight": e["weight"]})

    for x in sorted(_neighbours(a) & _neighbours(b)):
        bridges.append({"type": "shared_neighbour", "via": x})

    ca = {c["concept_id"] for c in concept.concepts_for_fact(a)}
    cb = {c["concept_id"] for c in concept.concepts_for_fact(b)}
    for c in sorted(ca & cb):
        bridges.append({"type": "shared_concept", "via": c})

    return bridges


# ─── CREATIVE mode (Adaptive Decoder) ──────────────────────────────────────────

def creative_temperature(novelty: float = 0.5) -> float:
    """
    The CREATIVE-mode sampling temperature for an LLM decoder, in
    [TEMP_MIN, TEMP_MAX] (default 0.6 → 0.85). `novelty` ∈ [0,1] dials within the
    band (0 = most grounded, 1 = most exploratory). Advisory metadata only — the
    dependency-free extractive generator ignores it; an LLM generator can use it.
    """
    lo = _envf(_ENV_TEMP_MIN, 0.6)
    hi = _envf(_ENV_TEMP_MAX, 0.85)
    n = max(0.0, min(1.0, float(novelty)))
    return round(lo + (hi - lo) * n, 4)


def creative_associations(
    node_id: str, *, k: int = 5, novelty: float = 0.5,
) -> Dict[str, Any]:
    """
    The CREATIVE associative layer for a node: explicit analogies + structural
    candidates + a recommended temperature. This NEVER includes or alters facts —
    callers keep answering from Validated facts; analogies only enrich the framing
    (creativity without compromising accuracy).
    """
    return {
        "node": node_id,
        "temperature": creative_temperature(novelty),
        "analogies": analogies_for(node_id),
        "suggested": suggest_analogies(node_id, k=k),
    }
