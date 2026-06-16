# core/rrf.py
# Velantrim ExoCortex — Reciprocal Rank Fusion (RRF) for retrieval ordering
#
# A pure-stdlib helper that merges several *ranked* candidate lists into one
# ordering without ever comparing their raw scores. Different retrieval signals
# — vector recall, the multi-hop graph-walk, a future lexical/BM25 ranker —
# produce scores on incompatible scales; summing those numbers lets one scale
# dominate by accident. RRF sidesteps this: it reads only each item's *rank*
# (position) within each list, so the inputs need only agree on order, not on
# magnitude.
#
# Formula (Cormack, Clarke & Buettcher, SIGIR 2009): for an item d,
#     score(d) = Σ_r  weight_r · 1 / (k + rank_r(d))
# where rank_r(d) is d's 1-based position in ranking r (best = 1) and items
# absent from a ranking contribute nothing for it. k (default 60) damps the pull
# of the very top ranks; the value is the paper's and is deliberately not tuned
# here.
#
# Boundary (audit constraint, Ring Zero): RRF orders retrieval candidates and
# NOTHING ELSE. It never assigns or changes truth_status, never raises
# confidence, never promotes a fact, and never lets a candidate skip the
# FactsPack, the TruthGate or the Guardian. The fused objects are returned
# untouched. Ordering candidates is a presentation concern, not an epistemic
# one — a fact is not "more true" for ranking highly here.

from typing import (Any, Callable, Dict, Hashable, Iterable, List, Optional,
                    Sequence)

# Canonical RRF constant from the original paper. Larger k flattens the
# advantage of top ranks; smaller k sharpens it.
DEFAULT_K = 60


def rrf_scores(
    rankings: Sequence[Iterable[Any]],
    *,
    k: float = DEFAULT_K,
    key: Optional[Callable[[Any], Hashable]] = None,
    weights: Optional[Sequence[float]] = None,
) -> Dict[Hashable, float]:
    """
    Fused RRF score per item across `rankings` (each ordered best-first).

    `key` extracts a hashable identity from an item (default: the item itself,
    which therefore must be hashable). `weights` scales each ranking's
    contribution (default: all 1.0) and must have one entry per ranking.

    Duplicate semantics — compressed unique ranks: duplicates within a single
    ranking are removed *before* ranks are assigned. An item is scored at its
    first (best) appearance, and each later duplicate of it is skipped so the
    next distinct item takes the next rank. Ranks therefore count distinct
    items, not physical list positions — e.g. ["a", "a", "b"] scores a at
    rank 1 and b at rank 2 (not 3). Rankings are expected to be deduplicated
    upstream anyway; this only makes the behaviour well-defined if they are not.
    (For classic physical-position ranks, pass already-deduplicated lists.)

    Returns {identity: score}; higher is better.
    """
    if k < 0:
        raise ValueError("rrf: k must be >= 0")
    rankings = list(rankings)
    if weights is None:
        weights = [1.0] * len(rankings)
    elif len(weights) != len(rankings):
        raise ValueError("rrf: weights must have one entry per ranking")

    identity = key if key is not None else (lambda item: item)
    scores: Dict[Hashable, float] = {}
    for ranking, weight in zip(rankings, weights):
        seen: set = set()
        rank = 0
        for item in ranking:
            ident = identity(item)
            if ident in seen:
                # Compressed unique-rank: skip the duplicate so the next
                # distinct item takes the next rank (ranks count distinct
                # items, not physical positions). See the docstring.
                continue
            seen.add(ident)
            rank += 1
            scores[ident] = scores.get(ident, 0.0) + weight / (k + rank)
    return scores


def rrf_fuse(
    rankings: Sequence[Iterable[Any]],
    *,
    k: float = DEFAULT_K,
    key: Optional[Callable[[Any], Hashable]] = None,
    weights: Optional[Sequence[float]] = None,
) -> List[Any]:
    """
    Merge `rankings` into a single best-first list, deduplicated by identity.

    The object kept for each identity is the first one encountered (scanning
    rankings in order, items in order), so dict/record candidates keep their
    original payload and are returned unmodified. Ordering is by descending
    fused RRF score; ties keep first-seen order (the sort is stable).
    """
    rankings = list(rankings)
    scores = rrf_scores(rankings, k=k, key=key, weights=weights)
    identity = key if key is not None else (lambda item: item)

    representative: Dict[Hashable, Any] = {}
    order: List[Hashable] = []
    for ranking in rankings:
        for item in ranking:
            ident = identity(item)
            if ident not in representative:
                representative[ident] = item
                order.append(ident)
    # Stable sort by descending score; `order` preserves first-seen for ties.
    order.sort(key=lambda ident: scores[ident], reverse=True)
    return [representative[ident] for ident in order]
