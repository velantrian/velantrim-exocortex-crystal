"""Tests for core/l3_graph.py — the swappable L3 canonical-graph adapter."""
import pytest

from core.l3_graph import (
    MockL3Graph,
    LadybugL3Graph,
    get_l3_graph,
    reset_l3_graph,
)


# ─── MockL3Graph ──────────────────────────────────────────────────────────────

def test_merge_fact_upserts_without_duplicating():
    g = MockL3Graph()
    g.merge_fact({"fact_id": "a", "claim": "v1", "truth_status": "VERIFIED"})
    g.merge_fact({"fact_id": "a", "claim": "v2"})  # same id → update in place
    assert len(g.all_facts()) == 1
    node = g.get_fact("a")
    assert node["claim"] == "v2"
    assert node["truth_status"] == "VERIFIED"  # earlier field preserved on update


def test_merge_fact_requires_fact_id():
    g = MockL3Graph()
    with pytest.raises(ValueError, match="fact_id"):
        g.merge_fact({"claim": "no id"})


def test_get_fact_returns_copy_not_reference():
    g = MockL3Graph()
    g.merge_fact({"fact_id": "a", "claim": "c"})
    node = g.get_fact("a")
    node["claim"] = "mutated"
    assert g.get_fact("a")["claim"] == "c"  # internal state untouched


def test_get_fact_missing_returns_none():
    assert MockL3Graph().get_fact("ghost") is None


def test_edges_and_neighbors_with_type_filter():
    g = MockL3Graph()
    g.merge_fact({"fact_id": "person", "claim": "X"})
    g.merge_fact({"fact_id": "place", "claim": "Y"})
    g.merge_fact({"fact_id": "feeling", "claim": "anxiety"})
    g.add_edge("person", "AT", "place")
    g.add_edge("person", "FELT", "feeling")
    g.add_edge("person", "AT", "place")  # duplicate edge is ignored
    g.add_edge("place", "NEAR", "feeling")  # edge from another node, must be skipped

    all_neighbors = g.neighbors("person")
    assert {n["fact_id"] for n in all_neighbors} == {"place", "feeling"}

    only_at = g.neighbors("person", rel_type="AT")
    assert [n["fact_id"] for n in only_at] == ["place"]


def test_get_edges_returns_targets_with_props():
    g = MockL3Graph()
    g.merge_fact({"fact_id": "a", "claim": "x"})
    g.merge_fact({"fact_id": "b", "claim": "y"})
    g.add_edge("a", "CO_OCCURRED", "b", {"who": ["user"], "when": "2026-06-01"})
    g.add_edge("a", "AT", "b")

    co = g.get_edges("a", rel_type="CO_OCCURRED")
    assert len(co) == 1
    assert co[0]["target"] == "b"
    assert co[0]["props"] == {"who": ["user"], "when": "2026-06-01"}
    assert len(g.get_edges("a")) == 2          # both rel types, unfiltered
    assert g.get_edges("missing") == []


def test_incoming_edges_mirror_get_edges():
    g = MockL3Graph()
    for fid in ("a", "b", "c"):
        g.merge_fact({"fact_id": fid, "claim": fid})
    g.add_edge("a", "SUPERSEDED_BY", "b", {"at": "t1"})
    g.add_edge("c", "CONTRADICTS", "b", {})

    inc = g.incoming_edges("b")
    assert {(e["rel_type"], e["source"]) for e in inc} == {
        ("SUPERSEDED_BY", "a"), ("CONTRADICTS", "c")}
    assert g.incoming_edges("b", rel_type="CONTRADICTS")[0]["source"] == "c"
    assert g.incoming_edges("a") == []          # nothing points at a


def test_neighbors_skips_dangling_edge_targets():
    g = MockL3Graph()
    g.merge_fact({"fact_id": "src", "claim": "c"})
    g.add_edge("src", "REL", "missing")  # target node never merged
    assert g.neighbors("src") == []


def test_clear_resets_state():
    g = MockL3Graph()
    g.merge_fact({"fact_id": "a", "claim": "c"})
    g.add_edge("a", "R", "a")
    g.clear()
    assert g.all_facts() == []
    assert g.neighbors("a") == []
    assert g.vector_search([1.0]) == []


def test_mock_vector_search_ranks_by_semantic_similarity():
    from core.embedding import get_embedder
    g = MockL3Graph()
    g.merge_fact({"fact_id": "sun", "claim": "Earth revolves around the Sun"})
    g.merge_fact({"fact_id": "brain", "claim": "The human brain has 86 billion neurons"})
    g.merge_fact({"fact_id": "dna", "claim": "DNA encodes genetic information"})

    q = get_embedder().embed("Tell me about the Sun")
    hits = g.vector_search(q, k=2)
    assert hits[0]["fact_id"] == "sun"
    assert hits[0]["_score"] > 0.3
    assert "brain" not in {h["fact_id"] for h in hits}  # no false match


def test_mock_vector_search_ignores_nodes_without_claim():
    g = MockL3Graph()
    g.merge_fact({"fact_id": "noclaim", "source": "s"})  # no claim → no embedding
    assert g.vector_search([0.1] * 8) == []


def test_mock_vector_search_breaks_ties_by_significance():
    """Equal relevance → the more significant memory ranks first (salience)."""
    from core.embedding import get_embedder
    g = MockL3Graph()
    claim = "Earth revolves around the Sun"
    g.merge_fact({"fact_id": "low", "claim": claim, "significance": 0.1})
    g.merge_fact({"fact_id": "high", "claim": claim, "significance": 0.9})

    hits = g.vector_search(get_embedder().embed("Tell me about the Sun"), k=2)
    assert hits[0]["fact_id"] == "high"
    assert hits[0]["_relevance"] == hits[1]["_relevance"]  # same semantic relevance
    assert hits[0]["_score"] > hits[1]["_score"]           # but salience tips it


# ─── factory / singleton ──────────────────────────────────────────────────────

def test_factory_default_is_mock_singleton():
    reset_l3_graph()
    g1 = get_l3_graph()
    g2 = get_l3_graph()
    assert isinstance(g1, MockL3Graph)
    assert g1 is g2  # singleton when no explicit backend requested


def test_factory_explicit_backend_is_not_cached():
    reset_l3_graph()
    default = get_l3_graph()
    explicit = get_l3_graph(backend="mock")
    assert explicit is not default  # explicit request bypasses the singleton
    assert get_l3_graph() is default  # ...and does not replace it


def test_factory_unknown_backend_raises():
    with pytest.raises(ValueError, match="неизвестный backend"):
        get_l3_graph(backend="sqlite3")


def test_auto_falls_back_to_mock_when_ladybug_unavailable(monkeypatch):
    import core.l3_graph as l3
    reset_l3_graph()

    def boom():
        raise RuntimeError("LadybugDB not available")

    monkeypatch.setattr(l3, "LadybugL3Graph", boom)
    assert isinstance(l3._make("auto"), MockL3Graph)


def test_neo4j_backend_requires_driver():
    # neo4j is an optional dependency; without it the slot raises a clear error.
    try:
        import neo4j  # noqa: F401
    except ImportError:
        with pytest.raises(ImportError, match="neo4j"):
            get_l3_graph(backend="neo4j")
    else:
        pytest.skip("neo4j installed; backend needs a live server to verify")


def test_factory_respects_env_var(monkeypatch):
    """The factory must consult VELANTRIM_L3_BACKEND to choose a backend."""
    import core.l3_graph as l3
    reset_l3_graph()
    # Register a throwaway backend so the test needs no native deps.
    monkeypatch.setitem(l3._BACKENDS, "dummy", MockL3Graph)
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "dummy")
    assert isinstance(get_l3_graph(), MockL3Graph)


# ─── LadybugDB backend (optional native dep; skipped where absent) ────────────

@pytest.fixture
def lbug(tmp_path):
    pytest.importorskip("ladybug")
    return LadybugL3Graph(db_path=str(tmp_path / "l3.lbug"))


def test_ladybug_merge_is_idempotent_upsert(lbug):
    lbug.merge_fact({"fact_id": "f2", "claim": "v1", "source": "physics",
                     "claim_type": "WORLD_FACT", "truth_status": "VERIFIED",
                     "confidence": 0.85, "significance": 0.5})
    lbug.merge_fact({"fact_id": "f2", "claim": "v2"})  # same id → upsert
    facts = lbug.all_facts()
    assert len(facts) == 1
    node = lbug.get_fact("f2")
    assert node["claim"] == "v2"
    assert node["truth_status"] == "VERIFIED"  # untouched field preserved


def test_ladybug_merge_requires_fact_id(lbug):
    with pytest.raises(ValueError, match="fact_id"):
        lbug.merge_fact({"claim": "no id"})


def test_ladybug_get_fact_missing_returns_none(lbug):
    assert lbug.get_fact("ghost") is None


def test_ladybug_metadata_round_trips(lbug):
    lbug.merge_fact({"fact_id": "m1", "claim": "c", "source": "s",
                     "metadata": {"tags": ["a", "b"], "n": 3}})
    assert lbug.get_fact("m1")["metadata"] == {"tags": ["a", "b"], "n": 3}


def test_ladybug_edges_and_neighbors_with_type_filter(lbug):
    for fid in ("person", "place", "feeling"):
        lbug.merge_fact({"fact_id": fid, "claim": fid, "source": "s"})
    lbug.add_edge("person", "AT", "place")
    lbug.add_edge("person", "FELT", "feeling")

    assert {n["fact_id"] for n in lbug.neighbors("person")} == {"place", "feeling"}
    assert [n["fact_id"] for n in lbug.neighbors("person", rel_type="AT")] == ["place"]


def test_ladybug_vector_search_via_native_index(lbug):
    from core.embedding import get_embedder
    lbug.merge_fact({"fact_id": "sun", "claim": "Earth revolves around the Sun",
                     "source": "astronomy"})
    lbug.merge_fact({"fact_id": "dna", "claim": "DNA encodes genetic information",
                     "source": "biology"})

    q = get_embedder().embed("Tell me about the Sun")
    hits = lbug.vector_search(q, k=2)
    assert hits[0]["fact_id"] == "sun"
    assert hits[0]["_score"] > 0.3


def test_ladybug_get_edges_round_trips_props(lbug):
    lbug.merge_fact({"fact_id": "a", "claim": "x", "source": "s"})
    lbug.merge_fact({"fact_id": "b", "claim": "y", "source": "s"})
    lbug.add_edge("a", "CO_OCCURRED", "b", {"who": ["user"], "where": "lab"})

    edges = lbug.get_edges("a", rel_type="CO_OCCURRED")
    assert len(edges) == 1
    assert edges[0]["target"] == "b"
    assert edges[0]["props"] == {"who": ["user"], "where": "lab"}


def test_ladybug_incoming_edges_round_trips(lbug):
    for fid in ("old", "new"):
        lbug.merge_fact({"fact_id": fid, "claim": fid, "source": "s"})
    lbug.add_edge("old", "SUPERSEDED_BY", "new", {"at": "t1"})
    inc = lbug.incoming_edges("new")
    assert len(inc) == 1
    assert inc[0]["source"] == "old"
    assert inc[0]["rel_type"] == "SUPERSEDED_BY"
    assert inc[0]["props"] == {"at": "t1"}


def test_ladybug_vector_search_empty_graph_returns_empty(lbug):
    from core.embedding import EMBED_DIM
    assert lbug.vector_search([0.0] * EMBED_DIM, k=3) == []


def test_ladybug_honors_env_path_for_persistence(monkeypatch, tmp_path):
    pytest.importorskip("ladybug")
    from core.l3_graph import LadybugL3Graph
    db = tmp_path / "persist.lbug"
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(db))

    g = LadybugL3Graph()  # no db_path → resolves from VELANTRIM_L3_PATH
    g.merge_fact({"fact_id": "p1", "claim": "persisted", "source": "s"})
    assert g.get_fact("p1")["claim"] == "persisted"
    assert db.exists()  # written to the configured location
