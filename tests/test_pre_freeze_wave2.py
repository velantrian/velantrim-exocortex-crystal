from __future__ import annotations

from core import embedding, query_pipeline
from core.l3_graph import MockL3Graph


def _validated_fact(fid: str, claim: str):
    return {
        "fact_id": fid, "claim": claim, "source": "src", "confidence": 1.0,
        "epistemic_state": "Validated", "truth_status": "VERIFIED",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
        "restricted": False,
    }


def test_grant_profile_rejects_auto_embedder(monkeypatch):
    graph = MockL3Graph()
    graph.merge_fact(_validated_fact("f1", "alpha beta"))
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "auto")
    result = query_pipeline.search_result("alpha")
    assert result["results"] == []
    assert result["reason_code"] == "grant_profile_requires_pinned_embedder"


def test_embedder_mismatch_uses_labelled_bounded_lexical_fallback(monkeypatch):
    graph = MockL3Graph()
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    embedding.reset_embedder()
    graph.merge_fact(_validated_fact("f1", "alpha beta"))
    graph.set_embedder_fingerprint("different-space")
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    result = query_pipeline.search_result("alpha")
    assert [row["fact_id"] for row in result["results"]] == ["f1"]
    assert result["retrieval"]["mode"] == "bounded_legacy_lexical"
    assert result["retrieval"]["reason_code"] == "embedder_mismatch_lexical_fallback"
    assert result["retrieval"]["stored_embedder_id"] == "different-space"


def test_pipeline_retrieval_explanation_is_navigation_not_confidence(monkeypatch):
    graph = MockL3Graph()
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    embedding.reset_embedder()
    graph.merge_fact(_validated_fact("seed", "alpha seed"))
    graph.merge_fact(_validated_fact("neighbor", "distant memory"))
    graph.add_edge("seed", "CO_OCCURRED", "neighbor")
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setattr("core.pipeline.get_l3_graph", lambda: graph)
    graph.set_embedder_fingerprint(embedding.get_embedder().id)

    result = query_pipeline.query("alpha")
    assert result["trace"]
    for entry in result["trace"]:
        assert entry["trace_version"] == 2
        assert "retrieval_score" in entry
        assert "confidence" not in entry
