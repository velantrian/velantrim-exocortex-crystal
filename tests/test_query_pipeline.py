"""Regression tests for the strict read-only query boundary."""

import asyncio

import pytest


def _graph_snapshot():
    from core.l3_graph import get_l3_graph
    from core.queue import get_outbox_queue

    graph = get_l3_graph()
    return {
        "facts": graph.all_facts(),
        "edges": list(getattr(graph, "_edges", [])),
        "mentions": list(getattr(graph, "_mentions", [])),
        "outbox": list(get_outbox_queue().pending()),
        "embedder_fingerprint": graph.embedder_fingerprint(),
    }


def test_query_reads_existing_canon_without_durable_or_adaptive_mutation():
    from core import adaptation
    from core.ingest import ingest
    from core.memory import get_fact
    from core.query_pipeline import query

    admitted = ingest(
        "Portugal's capital city is Lisbon",
        source="reference",
        source_status="EXTERNAL",
        confidence=0.95,
    )
    assert admitted["accepted"] is True
    fact_id = admitted["fact"]["fact_id"]

    l1_before = get_fact(fact_id)
    graph_before = _graph_snapshot()
    threshold_before = adaptation.verification_threshold()

    result = query("Portugal capital city Lisbon")

    assert result["answer"] is not None
    assert result["read_only"] is True
    assert result["query_policy"] == "canonical_read_only"
    assert get_fact(fact_id) == l1_before
    assert _graph_snapshot() == graph_before
    assert adaptation.verification_threshold() == threshold_before


def test_empty_canon_does_not_ingest_demo_retrieval_or_stamp_embedder():
    from core.l3_graph import get_l3_graph
    from core.memory import get_fact
    from core.query_pipeline import query

    graph = get_l3_graph()
    assert graph.all_facts() == []
    assert graph.embedder_fingerprint() is None

    result = query("quantum entanglement")

    assert result["answer"] is None
    assert result["reason_code"] == "no_local_retrieval_results"
    assert get_fact("f2") is None
    assert graph.all_facts() == []
    assert graph.embedder_fingerprint() is None
    assert _graph_snapshot()["outbox"] == []


def test_query_does_not_drain_existing_outbox_entry():
    from core.memory import enqueue_l3_write, pending_l3_writes
    from core.query_pipeline import query

    enqueue_l3_write("waiting-for-maintenance")
    assert pending_l3_writes() == ["waiting-for-maintenance"]

    result = query("nothing has been admitted yet")

    assert result["answer"] is None
    assert pending_l3_writes() == ["waiting-for-maintenance"]


def test_legacy_canon_without_fingerprint_uses_non_mutating_lexical_fallback():
    from core.l3_graph import get_l3_graph
    from core.query_pipeline import query

    graph = get_l3_graph()
    graph.merge_fact(
        {
            "fact_id": "legacy:lisbon",
            "claim": "Lisbon is the capital of Portugal",
            "source": "legacy-fixture",
            "confidence": 0.95,
            "epistemic_state": "Validated",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "truth_status": "VERIFIED",
            "restricted": False,
        }
    )
    assert graph.embedder_fingerprint() is None
    before = _graph_snapshot()

    result = query("Lisbon capital Portugal")

    assert result["answer"] is not None
    assert result["read_only"] is True
    assert graph.embedder_fingerprint() is None
    assert _graph_snapshot() == before


def test_unknown_retrieval_candidate_is_not_written(monkeypatch):
    from core import query_pipeline
    from core.l3_graph import get_l3_graph
    from core.memory import get_fact

    monkeypatch.setattr(
        query_pipeline,
        "_retrieve_read_only",
        lambda _query: [
            {
                "id": "ghost",
                "text": "An unadmitted retrieval candidate",
                "source": "external",
                "confidence": 0.99,
                "epistemic_state": "Observed",
                "origin": "test",
                "_score": 0.9,
            }
        ],
    )
    before = _graph_snapshot()

    result = query_pipeline.query("unadmitted candidate")

    assert result["answer"] is None
    assert result["reason_code"] == "no_canonical_retrieval_results"
    assert get_fact("ghost") is None
    assert get_l3_graph().get_fact("ghost") is None
    assert _graph_snapshot() == before


def test_episode_context_is_never_recorded_by_query(monkeypatch):
    from core import query_pipeline
    from core.ingest import ingest

    first = ingest(
        "Alpha causes beta in the verified fixture",
        source="fixture-a",
        source_status="EXTERNAL",
        confidence=0.95,
    )["fact"]
    second = ingest(
        "Beta causes gamma in the verified fixture",
        source="fixture-b",
        source_status="EXTERNAL",
        confidence=0.95,
    )["fact"]

    monkeypatch.setattr(
        query_pipeline,
        "_retrieve_read_only",
        lambda _query: [
            {"id": first["fact_id"], "_score": 0.9},
            {"id": second["fact_id"], "_score": 0.8},
        ],
    )
    before = _graph_snapshot()

    result = query_pipeline.query(
        "verified fixture",
        episode={"who": ["user"], "where": "lab", "when": "2026-07-27"},
    )

    assert result["episode"] == {
        "recorded": False,
        "reason_code": "read_only_query_does_not_record_episode",
    }
    assert _graph_snapshot() == before


def test_async_public_query_entrypoint_uses_read_only_pipeline(monkeypatch):
    from core import aio, query_pipeline

    expected = {
        "answer": "bounded",
        "read_only": True,
        "query_policy": "canonical_read_only",
    }
    calls = []

    def fake_query(query_text, episode=None):
        calls.append((query_text, episode))
        return expected

    monkeypatch.setattr(query_pipeline, "query", fake_query)

    result = asyncio.run(aio.arun("question", {"where": "test"}))

    assert result == expected
    assert calls == [("question", {"where": "test"})]


def test_http_ask_surface_preserves_memory(monkeypatch):
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from core import api
    from core.ingest import ingest
    from core.memory import get_fact

    admitted = ingest(
        "Gold is a chemical element",
        source="reference",
        source_status="EXTERNAL",
        confidence=0.95,
    )
    fact_id = admitted["fact"]["fact_id"]
    l1_before = get_fact(fact_id)
    graph_before = _graph_snapshot()

    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    client = TestClient(api.create_app())
    response = client.post("/ask", json={"query": "tell me about gold"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] is not None
    assert body["read_only"] is True
    assert body["query_policy"] == "canonical_read_only"
    assert get_fact(fact_id) == l1_before
    assert _graph_snapshot() == graph_before


def test_query_helper_defensive_branches(monkeypatch):
    from core import query_pipeline

    assert query_pipeline._safe_retrieval_score("bad") == 0.0
    assert query_pipeline._safe_retrieval_score(10**1000) == 0.0
    assert query_pipeline._safe_retrieval_score(float("nan")) == 0.0
    assert query_pipeline._lexical_tokens(None) == set()
    assert query_pipeline._resolve_canonical_fact({}) is None

    with pytest.raises(ValueError, match="empty query"):
        query_pipeline.query("   ")

    blocked = query_pipeline.query("no canon", episode={"where": "test"})
    assert blocked["episode"]["recorded"] is False


def test_resolve_fails_closed_on_l1_terminal_restriction_and_drift(monkeypatch):
    from core import query_pipeline
    from core.l3_graph import get_l3_graph

    node = {
        "fact_id": "resolve:fixture",
        "claim": "A canonical fixture",
        "source": "fixture",
        "confidence": 0.9,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
    }
    get_l3_graph().merge_fact(node)

    monkeypatch.setattr(
        query_pipeline,
        "get_fact",
        lambda _fid: {
            **node,
            "epistemic_state": "Contradicted",
            "restricted": True,
        },
    )
    terminal = query_pipeline._resolve_canonical_fact({"id": node["fact_id"]})
    assert terminal["epistemic_state"] == "Contradicted"
    assert terminal["restricted"] is True

    monkeypatch.setattr(
        query_pipeline,
        "get_fact",
        lambda _fid: {
            **node,
            "epistemic_state": "Supported",
            "confidence": 0.1,
        },
    )
    drifted = query_pipeline._resolve_canonical_fact({"id": node["fact_id"]})
    assert drifted["epistemic_state"] == query_pipeline.STORE_STATE_CONFLICT


def test_lexical_fallback_skips_empty_and_unrelated_claims(monkeypatch):
    from core import query_pipeline

    class FakeGraph:
        def all_facts(self):
            return [
                {"fact_id": "empty", "claim": None},
                {"fact_id": "other", "claim": "completely unrelated words"},
            ]

        def embedder_fingerprint(self):
            return None

    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: FakeGraph())

    assert query_pipeline._retrieve_read_only("!!!") == []
    assert query_pipeline._retrieve_read_only("target phrase") == []


def test_guardian_rejection_is_bounded(monkeypatch):
    from core import query_pipeline

    monkeypatch.setattr(
        query_pipeline,
        "_retrieve_read_only",
        lambda _query: [{"id": "canonical", "_score": 0.9}],
    )
    monkeypatch.setattr(
        query_pipeline,
        "_resolve_canonical_fact",
        lambda _item: {
            "fact_id": "canonical",
            "claim": "Canonical",
            "source": "fixture",
            "confidence": 0.9,
            "epistemic_state": "Validated",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "truth_status": "VERIFIED",
            "restricted": False,
            "_score": 0.9,
        },
    )
    monkeypatch.setattr(query_pipeline, "guardian", lambda _pack, _trace: (False, "bad"))

    result = query_pipeline.query("canonical")

    assert result["answer"] is None
    assert result["reason_code"] == "guardian_rejected_canonical_read"
