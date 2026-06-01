"""Tests for core/embedding.py — the swappable embedder + cosine."""
import pytest

from core.embedding import (
    EMBED_DIM,
    HashingEmbedder,
    cosine,
    get_embedder,
    reset_embedder,
)


def test_embed_returns_normalized_vector_of_fixed_dim():
    e = HashingEmbedder()
    v = e.embed("quantum entanglement links particles")
    assert len(v) == EMBED_DIM
    assert cosine(v, v) == pytest.approx(1.0)  # unit vector


def test_embed_is_deterministic_across_calls():
    e = HashingEmbedder()
    assert e.embed("the human brain") == e.embed("the human brain")


def test_stopwords_only_text_is_zero_vector():
    v = HashingEmbedder().embed("the a of to about how")
    assert all(x == 0.0 for x in v)


def test_cosine_orthogonal_and_zero_norm():
    assert cosine([1.0, 0.0], [0.0, 1.0]) == 0.0
    assert cosine([0.0, 0.0], [1.0, 1.0]) == 0.0  # zero norm guarded


def test_related_text_scores_higher_than_unrelated():
    e = HashingEmbedder()
    q = e.embed("Tell me about the Sun")
    sun = cosine(q, e.embed("Earth revolves around the Sun"))
    brain = cosine(q, e.embed("The human brain has 86 billion neurons"))
    assert sun > 0.3
    assert brain < 0.05      # the old stopword/collision false-match is gone
    assert sun > brain


def test_factory_default_singleton_is_hashing():
    reset_embedder()
    e1 = get_embedder()
    assert isinstance(e1, HashingEmbedder)
    assert get_embedder() is e1


def test_factory_explicit_backend_not_cached():
    reset_embedder()
    default = get_embedder()
    explicit = get_embedder(backend="hashing")
    assert explicit is not default
    assert get_embedder() is default


def test_factory_unknown_backend_raises():
    with pytest.raises(ValueError, match="неизвестный backend"):
        get_embedder(backend="word2vec")
