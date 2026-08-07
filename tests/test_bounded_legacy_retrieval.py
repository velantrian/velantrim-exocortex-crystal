"""Bounded no-fingerprint retrieval and explicit reindex tests for #317."""
from __future__ import annotations

import json

import pytest

from core.l3_graph import MockL3Graph, SqliteL3Graph
from core.legacy_retrieval import (
    LEGACY_REINDEX_REASON_CODE,
    LegacyRetrievalUnavailable,
    bounded_legacy_retrieve,
    legacy_candidate_limit,
    legacy_retrieval_status,
    lexical_tokens,
)
from core.reindex_embeddings import (
    ReindexUnsupported,
    main as reindex_main,
    reindex_embeddings,
    reindex_status,
)


def _node(fid: str, claim: str, **overrides):
    node = {
        "fact_id": fid,
        "claim": claim,
        "source": "legacy-test",
        "confidence": 0.9,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
    }
    node.update(overrides)
    return node


def test_candidate_limit_validation(monkeypatch):
    assert legacy_candidate_limit(17) == 17
    monkeypatch.setenv("VELANTRIM_LEGACY_QUERY_CANDIDATES", "9")
    assert legacy_candidate_limit() == 9
    for value in (True, 0, 4097, "bad"):
        with pytest.raises(ValueError, match="candidate limit"):
            legacy_candidate_limit(value)  # type: ignore[arg-type]


def test_tokenizer_is_safe_and_unicode_aware():
    assert lexical_tokens(None) == set()
    assert lexical_tokens("Lisbon Лиссабон 42") == {"lisbon", "лиссабон", "42"}


def test_mock_legacy_path_never_calls_all_facts_and_caps_work(monkeypatch):
    graph = MockL3Graph()
    for index in range(20):
        graph.merge_fact(_node(f"f:{index:03d}", f"topic {index}"))
    graph.merge_fact(_node("f:999", "rare target phrase"))
    monkeypatch.setattr(
        graph,
        "all_facts",
        lambda: pytest.fail("public legacy query must not call all_facts"),
    )

    hits = bounded_legacy_retrieve("topic 3", k=5, graph=graph, candidate_limit=7)
    assert hits
    assert hits.examined == 7
    assert hits.candidate_limit == 7
    assert all(hit["_legacy_candidates_examined"] <= 7 for hit in hits)
    missed = bounded_legacy_retrieve(
        "rare target phrase", k=5, graph=graph, candidate_limit=7
    )
    assert missed == []
    assert missed.examined == 7


def test_sqlite_legacy_path_uses_primary_key_limit_not_all_facts(monkeypatch):
    graph = SqliteL3Graph(":memory:")
    try:
        for index in range(30):
            graph.merge_fact(_node(f"f:{index:03d}", f"bounded topic {index}"))
        monkeypatch.setattr(
            graph,
            "all_facts",
            lambda: pytest.fail("public legacy query must not call all_facts"),
        )
        hits = bounded_legacy_retrieve(
            "bounded topic 4", k=3, graph=graph, candidate_limit=10
        )
        assert hits and hits.examined == 10
    finally:
        graph.close()


def test_empty_legacy_store_is_usable_and_reports_zero_work():
    graph = MockL3Graph()
    result = bounded_legacy_retrieve("anything", k=5, graph=graph)
    assert result == []
    assert result.examined == 0
    status = legacy_retrieval_status(graph).to_dict()
    assert status["supported"] is True
    assert status["fingerprint_present"] is False


def test_unknown_and_malformed_backends_fail_with_stable_reason():
    class Unsupported:
        def embedder_fingerprint(self):
            return None

        def all_facts(self):
            pytest.fail("unsupported backend must not be scanned")

    for graph in (Unsupported(), object()):
        with pytest.raises(LegacyRetrievalUnavailable) as exc:
            bounded_legacy_retrieve("query", k=5, graph=graph)
        assert exc.value.reason_code == LEGACY_REINDEX_REASON_CODE
        assert LEGACY_REINDEX_REASON_CODE in str(exc.value)


def test_query_and_structured_search_surface_stable_reason(monkeypatch):
    from core import query_pipeline

    class Unsupported:
        def embedder_fingerprint(self):
            return None

    graph = Unsupported()
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    answer = query_pipeline.query("legacy query")
    assert answer["reason_code"] == LEGACY_REINDEX_REASON_CODE
    assert answer["read_only"] is True
    assert answer["retrieval"]["reindex_required"] is True

    searched = query_pipeline.search_result("legacy query")
    assert searched["results"] == []
    assert searched["reason_code"] == LEGACY_REINDEX_REASON_CODE
    assert searched["retrieval"]["reindex_required"] is True


def test_bounded_no_hit_still_reports_degraded_work(monkeypatch):
    from core import query_pipeline

    graph = MockL3Graph()
    for index in range(8):
        graph.merge_fact(_node(f"f:{index}", f"topic {index}"))
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    result = query_pipeline.query("unmatched phrase")
    assert result["answer"] is None
    assert result["reason_code"] == "no_local_retrieval_results"
    assert result["retrieval"] == {
        "mode": "bounded_legacy_lexical",
        "candidates_examined": 8,
        "candidate_limit": 256,
        "reindex_recommended": True,
    }


def test_bounded_query_does_not_mutate_fingerprint_or_graph(monkeypatch):
    from core import query_pipeline

    graph = MockL3Graph()
    graph.merge_fact(_node("legacy:lisbon", "Lisbon is the capital of Portugal"))
    before = graph.all_facts()
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    result = query_pipeline.query("Lisbon capital Portugal")
    assert result["answer"] is not None
    assert result["retrieval"]["mode"] == "bounded_legacy_lexical"
    assert graph.embedder_fingerprint() is None
    assert graph.all_facts() == before


def test_restricted_record_never_leaks_from_legacy_search(monkeypatch):
    from core import query_pipeline

    graph = MockL3Graph()
    secret = "Sensitive restricted legacy claim"
    graph.merge_fact(_node("legacy:restricted", secret, restricted=True))
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setattr(query_pipeline, "get_fact", lambda _fid: None)
    result = query_pipeline.search_result("restricted legacy")
    assert result["results"] == []
    assert secret not in json.dumps(result)


def test_mock_reindex_preserves_facts_and_enables_fingerprint():
    graph = MockL3Graph()
    graph.merge_fact(_node("f:1", "Lisbon is the capital of Portugal"))
    graph.merge_fact(_node("f:2", "", truth_status="HYPOTHESIS"))
    graph._vectors.clear()
    before = graph.all_facts()
    progress = []
    report = reindex_embeddings(graph, batch_size=1, progress=progress.append)
    assert report["ok"] is True
    assert report["processed"] == 1
    assert report["skipped"] == 1
    assert report["truth_state_changed"] is False
    assert graph.embedder_fingerprint() == report["embedder"]
    assert graph.all_facts() == before
    assert set(graph._vectors) == {"f:1"}
    assert progress[-1]["total"] == 2


def test_mock_reindex_failure_keeps_previous_complete_index(monkeypatch):
    graph = MockL3Graph()
    graph.merge_fact(_node("f:1", "First"))
    graph.set_embedder_fingerprint("old")
    graph._vectors = {"f:1": [1.0]}
    old_vectors = dict(graph._vectors)

    class BrokenEmbedder:
        id = "new"

        def embed(self, _claim):
            raise RuntimeError("synthetic")

    monkeypatch.setattr("core.reindex_embeddings.get_embedder", lambda: BrokenEmbedder())
    with pytest.raises(RuntimeError, match="synthetic"):
        reindex_embeddings(graph)
    assert graph.embedder_fingerprint() == "old"
    assert graph._vectors == old_vectors


def test_sqlite_reindex_preserves_payloads_and_vector_count():
    graph = SqliteL3Graph(":memory:")
    try:
        graph.merge_fact(_node("f:1", "First claim"))
        graph.merge_fact(_node("f:2", "Second claim"))
        with graph._lock, graph._conn:
            graph._conn.execute("DELETE FROM vectors")
            graph._conn.execute("DELETE FROM meta WHERE key = 'embedder_fp'")
        before = graph.all_facts()
        report = reindex_embeddings(graph, batch_size=1)
        assert report["processed"] == 2
        assert graph.all_facts() == before
        assert graph.embedder_fingerprint() == report["embedder"]
        with graph._lock:
            count = graph._conn.execute("SELECT COUNT(*) FROM vectors").fetchone()[0]
        assert count == 2
    finally:
        graph.close()


def test_sqlite_reindex_failure_leaves_fingerprint_absent(monkeypatch):
    graph = SqliteL3Graph(":memory:")
    try:
        graph.merge_fact(_node("f:1", "First claim"))
        graph.set_embedder_fingerprint("old")

        class BrokenEmbedder:
            id = "new"

            def embed(self, _claim):
                raise RuntimeError("synthetic")

        monkeypatch.setattr("core.reindex_embeddings.get_embedder", lambda: BrokenEmbedder())
        with pytest.raises(RuntimeError, match="synthetic"):
            reindex_embeddings(graph)
        assert graph.embedder_fingerprint() is None
    finally:
        graph.close()


def test_reindex_status_and_unsupported_backend():
    graph = MockL3Graph()
    status = reindex_status(graph)
    assert status["reindex_supported"] is True
    assert status["active_fingerprint"] is None

    class Unsupported:
        def embedder_fingerprint(self):
            return None

    with pytest.raises(ReindexUnsupported):
        reindex_embeddings(Unsupported())


def test_reindex_batch_validation_and_cli(monkeypatch, capsys):
    graph = MockL3Graph()
    for value in (True, 0, 10001):
        with pytest.raises(ValueError, match="batch_size"):
            reindex_embeddings(graph, batch_size=value)  # type: ignore[arg-type]

    monkeypatch.setattr("core.reindex_embeddings.get_l3_graph", lambda: graph)
    assert reindex_main(["status"]) == 0
    assert "reindex_supported" in capsys.readouterr().out
    assert reindex_main(["rebuild", "--batch-size", "1"]) == 0
    assert '"ok": true' in capsys.readouterr().out


def test_reindex_cli_reports_unsupported(monkeypatch, capsys):
    class Unsupported:
        def embedder_fingerprint(self):
            return None

    monkeypatch.setattr("core.reindex_embeddings.get_l3_graph", lambda: Unsupported())
    assert reindex_main(["rebuild"]) == 2
    assert '"ok": false' in capsys.readouterr().out
