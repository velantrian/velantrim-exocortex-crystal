"""Defensive-edge coverage for bounded legacy retrieval and explicit reindex."""
from __future__ import annotations

import pytest

from core import query_pipeline
from core.l3_graph import MockL3Graph, SqliteL3Graph
from core.legacy_retrieval import (
    LegacyRetrievalUnavailable,
    _bounded_nodes,
    bounded_legacy_retrieve,
)
from core.reindex_embeddings import reindex_embeddings


def _node(fact_id: str, claim) -> dict:
    return {
        "fact_id": fact_id,
        "claim": claim,
        "source": "bounded-defensive-test",
        "confidence": 0.9,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
    }


def test_bounded_reader_rejects_unsupported_backend_directly():
    with pytest.raises(LegacyRetrievalUnavailable, match="requires_reindex"):
        _bounded_nodes(object(), 3)


def test_bounded_retrieve_validates_k_and_handles_empty_tokens_and_bad_nodes():
    graph = MockL3Graph()
    graph._nodes = {
        "a": {"fact_id": None, "claim": "target phrase"},
        "b": {"fact_id": "b", "claim": None},
        "c": {"fact_id": "c", "claim": "target phrase"},
    }

    for invalid in (True, 0, "1"):
        with pytest.raises(ValueError, match="positive integer"):
            bounded_legacy_retrieve("target", k=invalid, graph=graph)  # type: ignore[arg-type]

    empty = bounded_legacy_retrieve("!!!", k=2, graph=graph)
    assert empty == []
    assert empty.examined == 3

    matched = bounded_legacy_retrieve("target phrase", k=5, graph=graph)
    assert [item["id"] for item in matched] == ["c"]


def test_legacy_metadata_supports_plain_list_compatibility_results():
    metadata = query_pipeline._legacy_metadata(
        [
            {
                "id": "a",
                "origin": "bounded_legacy_lexical",
                "_legacy_candidates_examined": 4,
                "_legacy_candidate_limit": 8,
            },
            {
                "id": "b",
                "origin": "bounded_legacy_lexical",
                "_legacy_candidates_examined": 6,
                "_legacy_candidate_limit": 8,
            },
        ]
    )
    assert metadata == {
        "mode": "bounded_legacy_lexical",
        "candidates_examined": 6,
        "candidate_limit": 8,
        "reindex_recommended": True,
    }


def test_query_marks_generator_none_as_blocked(monkeypatch):
    monkeypatch.setattr(
        query_pipeline,
        "_retrieve_read_only",
        lambda _query: [{"id": "fact:1", "origin": "vector", "_score": 0.9}],
    )
    monkeypatch.setattr(
        query_pipeline,
        "_resolve_retrieval_hits",
        lambda _hits: [
            {
                "fact_id": "fact:1",
                "claim": "Grounded fact",
                "source": "test",
                "epistemic_state": "Validated",
                "_score": 0.9,
            }
        ],
    )
    monkeypatch.setattr(query_pipeline, "guardian", lambda _pack, _trace: (True, "ok"))
    monkeypatch.setattr(query_pipeline, "generate_answer", lambda _pack, _trace: {"answer": None})

    result = query_pipeline.query("grounded question")

    assert result["answer"] is None
    assert result["reason_code"] == "insufficient_strict_canonical_grounding"


def test_sqlite_reindex_skips_empty_claim_and_reports_progress():
    graph = SqliteL3Graph(":memory:")
    try:
        graph.merge_fact(_node("fact:valid", "valid claim"))
        graph.merge_fact(_node("fact:empty", ""))
        with graph._lock, graph._conn:
            graph._conn.execute("DELETE FROM vectors")
            graph._conn.execute("DELETE FROM meta WHERE key = 'embedder_fp'")

        progress = []
        report = reindex_embeddings(graph, batch_size=1, progress=progress.append)

        assert report["processed"] == 1
        assert report["skipped"] == 1
        assert progress[-1] == {"processed": 1, "skipped": 1, "total": 2}
    finally:
        graph.close()
