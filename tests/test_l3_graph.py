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
        get_l3_graph(backend="neo4j")


def test_factory_respects_env_var(monkeypatch):
    reset_l3_graph()
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "ladybug")
    # ladybug backend is a deliberate stub until the spike lands.
    with pytest.raises(NotImplementedError, match="LadybugDB"):
        get_l3_graph()


# ─── LadybugDB stub ───────────────────────────────────────────────────────────

def test_ladybug_backend_is_not_yet_implemented():
    with pytest.raises(NotImplementedError, match="спайк"):
        LadybugL3Graph()
