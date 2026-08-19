from __future__ import annotations

import pytest

from core import embedding, pipeline
from core.l3_graph import MockL3Graph, SqliteL3Graph
from core.retrieval_config import RetrievalConfig


class _BoundedGraph:
    def __init__(self, edges):
        self._fp = None
        self.edges = list(edges)
        self.calls = []
        self.nodes = {
            "seed": {
                "fact_id": "seed", "claim": "seed", "source": "src",
                "confidence": 1.0, "epistemic_state": "Validated",
                "truth_status": "VERIFIED", "source_status": "EXTERNAL",
                "restricted": False,
            },
            "assoc-a": {
                "fact_id": "assoc-a", "claim": "assoc a", "source": "src",
                "confidence": 1.0, "epistemic_state": "Validated",
                "truth_status": "VERIFIED", "source_status": "EXTERNAL",
                "restricted": False,
            },
            "assoc-b": {
                "fact_id": "assoc-b", "claim": "assoc b", "source": "src",
                "confidence": 1.0, "epistemic_state": "Validated",
                "truth_status": "VERIFIED", "source_status": "EXTERNAL",
                "restricted": False,
            },
            "sep": {
                "fact_id": "sep", "claim": "separated", "source": "src",
                "confidence": 1.0, "epistemic_state": "Validated",
                "truth_status": "VERIFIED", "source_status": "EXTERNAL",
                "restricted": False,
            },
            "deep": {
                "fact_id": "deep", "claim": "deep", "source": "src",
                "confidence": 1.0, "epistemic_state": "Validated",
                "truth_status": "VERIFIED", "source_status": "EXTERNAL",
                "restricted": False,
            },
        }

    def embedder_fingerprint(self):
        return self._fp

    def set_embedder_fingerprint(self, value):
        self._fp = value

    def vector_search(self, _query_vector, k=5):
        node = dict(self.nodes["seed"])
        node["_relevance"] = 1.0
        return [node][:k]

    def get_edges(self, fact_id, rel_type=None, limit=None):
        self.calls.append((fact_id, rel_type, limit))
        out = [
            dict(edge) for edge in self.edges
            if edge["source"] == fact_id
            and (rel_type is None or edge["rel_type"] == rel_type)
        ]
        out.sort(key=lambda edge: (edge["rel_type"], edge["target"]))
        if limit is not None:
            out = out[:limit]
        return [{
            "rel_type": edge["rel_type"],
            "target": edge["target"],
            "props": {},
        } for edge in out]

    def get_fact(self, fact_id):
        node = self.nodes.get(fact_id)
        return dict(node) if node is not None else None


def _cfg(**overrides):
    values = dict(
        k=3, min_similarity=0.0, graph_walk_hops=2, graph_walk_decay=0.5,
        graph_walk_edges_per_node=32, graph_walk_frontier_limit=128,
        graph_walk_candidate_limit=256, significance_weight=0.5,
    )
    values.update(overrides)
    return RetrievalConfig(**values)


def test_graph_walk_is_default_deny_and_passes_backend_limit(monkeypatch):
    graph = _BoundedGraph([
        {"source": "seed", "rel_type": "SEPARATED_FROM", "target": "sep"},
        {"source": "seed", "rel_type": "CO_OCCURRED", "target": "assoc-b"},
        {"source": "seed", "rel_type": "CO_OCCURRED", "target": "assoc-a"},
    ])
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    embedding.reset_embedder()
    monkeypatch.setattr(pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setattr(
        pipeline, "get_retrieval_config",
        lambda: _cfg(graph_walk_hops=1, graph_walk_edges_per_node=1),
    )

    result = pipeline.retrieve("seed", k=3)
    ids = {item["id"] for item in result}

    assert "seed" in ids
    assert "assoc-a" in ids
    assert "assoc-b" not in ids
    assert "sep" not in ids
    assert graph.calls == [("seed", "CO_OCCURRED", 1)]


def test_graph_walk_frontier_and_candidate_limits_are_independent(monkeypatch):
    graph = _BoundedGraph([
        {"source": "seed", "rel_type": "CO_OCCURRED", "target": "assoc-a"},
        {"source": "seed", "rel_type": "CO_OCCURRED", "target": "assoc-b"},
        {"source": "assoc-a", "rel_type": "CO_OCCURRED", "target": "deep"},
    ])
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    embedding.reset_embedder()
    monkeypatch.setattr(pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setattr(
        pipeline, "get_retrieval_config",
        lambda: _cfg(
            graph_walk_hops=2, graph_walk_frontier_limit=1,
            graph_walk_candidate_limit=1,
        ),
    )

    result = pipeline.retrieve("seed", k=5)
    graph_ids = [item["id"] for item in result if item["origin"] == "graph"]

    assert graph_ids == ["assoc-a"]
    assert "deep" not in graph_ids


def test_mock_get_edges_is_deterministic_and_bounded():
    graph = MockL3Graph()
    graph.add_edge("a", "CO_OCCURRED", "z")
    graph.add_edge("a", "CO_OCCURRED", "b")
    graph.add_edge("a", "CO_OCCURRED", "m")

    assert [e["target"] for e in graph.get_edges("a", "CO_OCCURRED", limit=2)] == ["b", "m"]
    with pytest.raises(ValueError):
        graph.get_edges("a", limit=-1)


def test_sqlite_get_edges_applies_order_and_limit():
    graph = SqliteL3Graph(":memory:")
    try:
        graph.add_edge("a", "CO_OCCURRED", "z")
        graph.add_edge("a", "CO_OCCURRED", "b")
        graph.add_edge("a", "CO_OCCURRED", "m")
        assert [e["target"] for e in graph.get_edges("a", "CO_OCCURRED", limit=2)] == ["b", "m"]
    finally:
        graph.close()


def test_retrieval_config_rejects_unbounded_graph_limits():
    with pytest.raises(ValueError):
        _cfg(graph_walk_edges_per_node=257)
    with pytest.raises(ValueError):
        _cfg(graph_walk_frontier_limit=2049)
    with pytest.raises(ValueError):
        _cfg(graph_walk_candidate_limit=4097)


def test_graph_walk_stops_after_relation_budget_is_exhausted(monkeypatch):
    graph = _BoundedGraph([
        {"source": "seed", "rel_type": "A_TEST_REL", "target": "assoc-a"},
        {"source": "seed", "rel_type": "Z_TEST_REL", "target": "assoc-b"},
    ])
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    embedding.reset_embedder()
    monkeypatch.setattr(pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setattr(
        pipeline, "get_retrieval_config",
        lambda: _cfg(graph_walk_hops=1, graph_walk_edges_per_node=1),
    )
    monkeypatch.setattr(
        pipeline, "_WALK_EDGE_WEIGHTS",
        {"A_TEST_REL": 1.0, "Z_TEST_REL": 1.0},
    )

    result = pipeline.retrieve("seed", k=3)

    assert "assoc-a" in {item["id"] for item in result}
    assert "assoc-b" not in {item["id"] for item in result}
    assert graph.calls == [("seed", "A_TEST_REL", 1)]
