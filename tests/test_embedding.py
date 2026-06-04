"""Tests for core/embedding.py — the swappable embedder + cosine."""
import pytest

from core.embedding import (
    EMBED_DIM,
    EmbedderMismatchError,
    HashingEmbedder,
    assert_compatible_embedder,
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
    with pytest.raises(ValueError, match="unknown backend"):
        get_embedder(backend="word2vec")


@pytest.mark.parametrize("exc", [
    ImportError("sentence-transformers not installed"),
    OSError("model download failed (offline)"),  # not just ImportError
])
def test_auto_falls_back_to_hashing_on_any_load_failure(monkeypatch, exc):
    import core.embedding as emb

    def boom(*a, **k):
        raise exc

    monkeypatch.setattr(emb, "SentenceTransformerEmbedder", boom)
    assert isinstance(emb._make("auto"), emb.HashingEmbedder)


def test_sbert_captures_real_semantics():
    """Neural embeddings link 'Sun'~'solar' — which the lexical default cannot."""
    pytest.importorskip("sentence_transformers")
    from core.embedding import SentenceTransformerEmbedder, cosine
    e = SentenceTransformerEmbedder()
    sun_solar = cosine(e.embed("the Sun"), e.embed("solar star in the sky"))
    sun_quantum = cosine(e.embed("the Sun"), e.embed("quantum entanglement"))
    assert sun_solar > 0.3
    assert sun_solar > sun_quantum


# ─── Embedder identity + mismatch guard ───────────────────────────────────────

class _StubEmbedder:
    """A throwaway embedder with a controllable id, for guard tests."""
    def __init__(self, id_):
        self.id = id_

    def embed(self, text):
        return [0.0] * EMBED_DIM


def test_hashing_embedder_exposes_stable_id():
    assert get_embedder("hashing").id == f"hashing-{EMBED_DIM}"


def test_guard_stamps_fingerprint_on_first_use():
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    assert g.embedder_fingerprint() is None
    assert_compatible_embedder(g)                      # first use → stamp
    assert g.embedder_fingerprint() == f"hashing-{EMBED_DIM}"
    assert_compatible_embedder(g)                      # same embedder → no-op


def test_guard_warns_on_embedder_switch(monkeypatch, caplog):
    from core import embedding
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    g.set_embedder_fingerprint("sbert-foo-2048")       # store built with sbert
    monkeypatch.setattr(embedding, "get_embedder",
                        lambda backend=None: _StubEmbedder(f"hashing-{EMBED_DIM}"))
    with caplog.at_level("WARNING"):
        assert_compatible_embedder(g)                  # mismatch → warns, no raise
    assert any("not cosine-comparable" in r.message for r in caplog.records)


def test_guard_raises_in_strict_mode(monkeypatch):
    from core import embedding
    from core.l3_graph import get_l3_graph
    g = get_l3_graph()
    g.set_embedder_fingerprint("sbert-foo-2048")
    monkeypatch.setattr(embedding, "get_embedder",
                        lambda backend=None: _StubEmbedder(f"hashing-{EMBED_DIM}"))
    monkeypatch.setenv("VELANTRIM_EMBEDDER_STRICT", "1")
    with pytest.raises(EmbedderMismatchError):
        assert_compatible_embedder(g)


def test_retrieve_stamps_store_fingerprint():
    from core.pipeline import retrieve
    from core.l3_graph import get_l3_graph
    retrieve("quantum entanglement")
    assert get_l3_graph().embedder_fingerprint() == f"hashing-{EMBED_DIM}"
