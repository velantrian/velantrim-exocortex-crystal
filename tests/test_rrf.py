"""Tests for core/rrf.py — Reciprocal Rank Fusion for retrieval ordering."""
import pytest

from core.rrf import DEFAULT_K, rrf_fuse, rrf_scores


# ─── Core formula ─────────────────────────────────────────────────────────────

def test_single_ranking_preserves_order():
    assert rrf_fuse([["a", "b", "c"]]) == ["a", "b", "c"]


def test_scores_follow_rrf_formula():
    scores = rrf_scores([["a", "b"]], k=10)
    assert scores["a"] == pytest.approx(1 / (10 + 1))
    assert scores["b"] == pytest.approx(1 / (10 + 2))


def test_default_k_is_the_paper_constant():
    assert DEFAULT_K == 60
    assert rrf_scores([["x"]])["x"] == pytest.approx(1 / 61)


def test_agreement_across_rankings_accumulates():
    # 'a' is top in both lists; 'b'/'c' appear once each → 'a' wins clearly.
    scores = rrf_scores([["a", "b"], ["a", "c"]], k=1)
    assert scores["a"] == pytest.approx(1 / 2 + 1 / 2)
    assert scores["b"] == pytest.approx(1 / 3)
    assert scores["c"] == pytest.approx(1 / 3)
    assert rrf_fuse([["a", "b"], ["a", "c"]], k=1)[0] == "a"


def test_consensus_beats_a_single_first_place():
    # 'b' is never #1 but is present in every list; 'a' is #1 once then absent.
    # b: 1/3 + 1/2 + 1/2 = 1.333 ; c: 1/3 + 1/3 = 0.667 ; a: 1/2 = 0.5
    fused = rrf_fuse([["a", "b"], ["b", "c"], ["b", "c"]], k=1)
    assert fused == ["b", "c", "a"]


# ─── Duplicates, weights, key extraction ──────────────────────────────────────

def test_duplicate_within_ranking_uses_best_position():
    # The second 'a' is ignored: 'a' is scored at rank 1, 'b' at rank 2 (not 3).
    scores = rrf_scores([["a", "a", "b"]], k=0)
    assert scores["a"] == pytest.approx(1 / 1)
    assert scores["b"] == pytest.approx(1 / 2)


def test_weights_scale_each_ranking_contribution():
    base = rrf_scores([["a"], ["b"]], k=1)
    assert base["a"] == pytest.approx(base["b"])
    weighted = rrf_scores([["a"], ["b"]], k=1, weights=[3.0, 1.0])
    assert weighted["a"] == pytest.approx(3 * weighted["b"])


def test_key_extractor_groups_records_and_keeps_first_payload():
    r1 = [{"id": "x", "v": 1}, {"id": "y", "v": 2}]
    r2 = [{"id": "x", "v": 9}]
    fused = rrf_fuse([r1, r2], key=lambda d: d["id"])
    assert [d["id"] for d in fused] == ["x", "y"]   # 'x' in both → ranks first
    assert fused[0]["v"] == 1                         # first-seen payload kept


def test_ties_keep_first_seen_order():
    # Equal scores (1/2 each) → stable order: the first-seen item stays first.
    assert rrf_fuse([["a"], ["b"]], k=1) == ["a", "b"]


# ─── Edge cases & validation ──────────────────────────────────────────────────

def test_empty_inputs():
    assert rrf_scores([]) == {}
    assert rrf_fuse([]) == []
    assert rrf_fuse([[], []]) == []


def test_negative_k_is_rejected():
    with pytest.raises(ValueError):
        rrf_scores([["a"]], k=-1)
    with pytest.raises(ValueError):
        rrf_fuse([["a"]], k=-1)


def test_weights_length_must_match_rankings():
    with pytest.raises(ValueError):
        rrf_scores([["a"], ["b"]], weights=[1.0])
    with pytest.raises(ValueError):
        rrf_fuse([["a"], ["b"]], weights=[1.0])


# ─── Boundary invariant (Ring Zero) ───────────────────────────────────────────

def test_fusion_orders_only_and_never_annotates_candidates():
    """RRF reorders; it must not mutate payloads nor inject truth/confidence
    fields. The objects returned are the very same input objects."""
    cands = [{"id": "a", "truth_status": "UNVERIFIED"},
             {"id": "b", "truth_status": "UNVERIFIED"}]
    snapshot = [dict(c) for c in cands]
    fused = rrf_fuse([cands], key=lambda d: d["id"])
    assert cands == snapshot                       # no in-place mutation
    for original, came_back in zip(cands, fused):
        assert came_back is original              # same object handed back
        assert set(came_back) == {"id", "truth_status"}   # nothing injected
