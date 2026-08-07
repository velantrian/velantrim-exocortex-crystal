"""Regression coverage for reindex equivalence with ordinary L3 vector builds."""

from core.l3_graph import MockL3Graph, SqliteL3Graph
from core.reindex_embeddings import reindex_embeddings


def _node(fact_id: str, claim: str) -> dict:
    return {
        "fact_id": fact_id,
        "claim": claim,
        "source": "reindex-equivalence-test",
        "confidence": 0.9,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
    }


def test_mock_reindex_vectors_truthy_whitespace_claim_like_normal_merge():
    graph = MockL3Graph()
    graph.merge_fact(_node("f:space", "   "))
    assert "f:space" in graph._vectors

    graph._vectors.clear()
    graph._embedder_fp = None
    report = reindex_embeddings(graph)

    assert report["processed"] == 1
    assert report["skipped"] == 0
    assert "f:space" in graph._vectors


def test_sqlite_reindex_vectors_truthy_whitespace_claim_like_normal_merge():
    graph = SqliteL3Graph(":memory:")
    try:
        graph.merge_fact(_node("f:space", "   "))
        with graph._lock:
            before = graph._conn.execute(
                "SELECT COUNT(*) FROM vectors WHERE fact_id = 'f:space'"
            ).fetchone()[0]
        assert before == 1

        with graph._lock, graph._conn:
            graph._conn.execute("DELETE FROM vectors")
            graph._conn.execute("DELETE FROM meta WHERE key = 'embedder_fp'")
        report = reindex_embeddings(graph)

        assert report["processed"] == 1
        assert report["skipped"] == 0
        with graph._lock:
            after = graph._conn.execute(
                "SELECT COUNT(*) FROM vectors WHERE fact_id = 'f:space'"
            ).fetchone()[0]
        assert after == 1
    finally:
        graph.close()
