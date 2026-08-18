# core/concept.py
# Velantrim ExoCortex — Concept Emergence (RFC0066)
#
# "Cells that fire together, wire together." Facts recalled together already get
# CO_OCCURRED episodic edges (pipeline._link_episode) — the Hebbian substrate.
# This module reads that co-activation signal and lets ProtoConcepts EMERGE:
# clusters of facts that keep being recalled together become a named concept node
# in the canon, with MEMBER_OF links from each member fact.
#
# Design (faithful to the rest of the system):
#   - Emergent, not imposed. Concepts are COMPUTED from the live co-activation
#     graph (deterministic union-find over CO_OCCURRED weights), so they always
#     reflect the current recall reality — no stale concept store to reconcile.
#   - Hebbian weight = how many times two facts co-occurred (each co-recall adds a
#     CO_OCCURRED edge). A pair must fire together at least `min_weight` times to
#     wire together; a cluster needs at least `min_size` facts to be a concept.
#   - Materialisation reuses existing graph primitives: a ProtoConcept is an
#     entity of kind CONCEPT (merge_entity) and members are linked via
#     link_fact_to_entity(..., rel=MEMBER_OF). Backend-agnostic, idempotent.
#   - Dependency-free and deterministic; emerge_concepts() never touches fact
#     truth (no ESM change, no confidence edit) — concepts sit ALONGSIDE the canon.

import os
from typing import Dict, Any, List, Optional, Tuple

from core.memory import get_fact
from core.l3_graph import get_l3_graph
from core.trust_snapshot import TrustSnapshot
from core import metrics

CONCEPT_KIND = "CONCEPT"
REL_MEMBER_OF = "MEMBER_OF"
_EPISODE_REL = "CO_OCCURRED"  # written by pipeline._link_episode

_ENV_MIN_WEIGHT = "VELANTRIM_CONCEPT_MIN_WEIGHT"   # co-occurrences to wire (default 2)
_ENV_MIN_SIZE = "VELANTRIM_CONCEPT_MIN_SIZE"       # facts to form a concept (default 2)


def _envi(name: str, default: int) -> int:
    try:
        return max(1, int(os.environ.get(name, default)))
    except ValueError:
        return default


def _min_weight() -> int:
    return _envi(_ENV_MIN_WEIGHT, 2)


def _min_size() -> int:
    return _envi(_ENV_MIN_SIZE, 2)


def _concept_eligible_fact_ids(graph) -> set[str]:
    """Deny-dominant eligible facts for concept clustering.

    Concept emergence may write entity/membership projections, so a non-admitted,
    restricted, terminal, or store-conflicted fact must not shape a cluster.
    This mirrors the read boundary without importing the retrieval pipeline.
    """
    eligible: set[str] = set()
    for node in graph.all_facts():
        fact_id = node.get("fact_id")
        if not isinstance(fact_id, str) or not fact_id:
            continue
        snapshot = TrustSnapshot.from_records(
            fact_id=fact_id, l3=node, l1=get_fact(fact_id), retrieval_score=0.0
        )
        if snapshot.epistemic_state == "Validated" and snapshot.restricted is False:
            eligible.add(fact_id)
    return eligible


def hebbian_weights() -> Dict[Tuple[str, str], int]:
    """
    Undirected Hebbian co-activation weights between canonical facts.

    weight(a, b) = number of times a and b were recalled together (CO_OCCURRED
    edges). Symmetric; keyed by the ordered tuple (min, max) so each pair appears
    once.
    """
    graph = get_l3_graph()
    # A co-recall writes both directed edges a→b and b→a. Tally the directed
    # counts first, then fold each undirected pair to the max of its two
    # directions. This is robust even if only one direction is present (no
    # halving, so odd counts are never lost), and matches the symmetric case.
    directed: Dict[Tuple[str, str], int] = {}
    eligible = _concept_eligible_fact_ids(graph)
    for a in sorted(eligible):
        for edge in graph.get_edges(a, _EPISODE_REL):
            b = edge["target"]
            if a == b or b not in eligible:
                continue
            directed[(a, b)] = directed.get((a, b), 0) + 1
    weights: Dict[Tuple[str, str], int] = {}
    for (a, b), count in directed.items():
        key = (a, b) if a <= b else (b, a)
        weights[key] = max(weights.get(key, 0), count)
    return weights


class _UnionFind:
    def __init__(self) -> None:
        self._parent: Dict[str, str] = {}

    def find(self, x: str) -> str:
        self._parent.setdefault(x, x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:       # path compression
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            # Deterministic: smaller id becomes the root.
            lo, hi = (ra, rb) if ra <= rb else (rb, ra)
            self._parent[hi] = lo


def detect_concepts(
    *, min_weight: Optional[int] = None, min_size: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Compute the ProtoConcepts that currently emerge from co-activation.

    Union facts whose pair weight ≥ min_weight; every resulting component with
    ≥ min_size facts is a concept. Read-only and deterministic. Each concept:
      concept_id    — "concept:<anchor>" (anchor = most co-activated member)
      anchor        — the central fact_id
      label         — "concept: <anchor claim snippet>"
      members       — sorted member fact_ids
      size          — number of members
      coactivations — total internal co-occurrence weight
    Sorted by size desc, then concept_id.
    """
    mw = min_weight if min_weight is not None else _min_weight()
    ms = min_size if min_size is not None else _min_size()
    weights = hebbian_weights()

    uf = _UnionFind()
    internal_degree: Dict[str, int] = {}
    for (a, b), w in weights.items():
        if w >= mw:
            uf.union(a, b)
            internal_degree[a] = internal_degree.get(a, 0) + w
            internal_degree[b] = internal_degree.get(b, 0) + w

    components: Dict[str, List[str]] = {}
    for node in list(internal_degree.keys()):
        components.setdefault(uf.find(node), []).append(node)

    concepts: List[Dict[str, Any]] = []
    for members in components.values():
        if len(members) < ms:
            continue
        members = sorted(members)
        # Anchor = highest internal co-activation degree; tie-break smallest id.
        anchor = sorted(
            members, key=lambda m: (-internal_degree.get(m, 0), m))[0]
        coact = sum(w for (a, b), w in weights.items()
                    if w >= mw and a in members and b in members)
        concepts.append({
            "concept_id": "concept:" + anchor,
            "anchor": anchor,
            "label": _concept_label(anchor),
            "members": members,
            "size": len(members),
            "coactivations": coact,
        })
    concepts.sort(key=lambda c: (-c["size"], c["concept_id"]))
    return concepts


def _concept_label(anchor: str) -> str:
    fact = get_fact(anchor)
    claim = (fact or {}).get("claim", "") if fact else ""
    snippet = " ".join(claim.split()[:8]) if claim else anchor
    return f"concept: {snippet}" if snippet else f"concept:{anchor}"


def emerge_concepts(
    *, min_weight: Optional[int] = None, min_size: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Materialise the emergent ProtoConcepts into the canon: a CONCEPT entity node
    per concept and a MEMBER_OF link from each member fact. Idempotent (re-running
    upserts the same nodes/links). Never alters fact truth. Returns a summary.
    """
    concepts = detect_concepts(min_weight=min_weight, min_size=min_size)
    graph = get_l3_graph()
    for c in concepts:
        graph.merge_entity(c["concept_id"], CONCEPT_KIND, c["label"])
        for fid in c["members"]:
            graph.link_fact_to_entity(fid, c["concept_id"], rel=REL_MEMBER_OF)
    metrics.incr("concept.emerged")
    return {
        "emerged": len(concepts),
        "concepts": [{"concept_id": c["concept_id"], "label": c["label"],
                      "size": c["size"], "coactivations": c["coactivations"]}
                     for c in concepts],
    }


def concepts_for_fact(
    fact_id: str, *, min_weight: Optional[int] = None,
    min_size: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Concepts the fact is a member of (computed from the live co-activation graph)."""
    return [c for c in detect_concepts(min_weight=min_weight, min_size=min_size)
            if fact_id in c["members"]]


def concept_report(
    *, min_weight: Optional[int] = None, min_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Observable state of concept emergence (deterministic, read-only)."""
    mw = min_weight if min_weight is not None else _min_weight()
    ms = min_size if min_size is not None else _min_size()
    concepts = detect_concepts(min_weight=mw, min_size=ms)
    clustered = sorted({fid for c in concepts for fid in c["members"]})
    return {
        "min_weight": mw,
        "min_size": ms,
        "total_concepts": len(concepts),
        "clustered_facts": len(clustered),
        "concepts": [{"concept_id": c["concept_id"], "label": c["label"],
                      "size": c["size"], "coactivations": c["coactivations"],
                      "members": c["members"]} for c in concepts],
    }
