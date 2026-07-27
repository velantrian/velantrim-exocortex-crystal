"""Regression tests for the strict read-only query boundary."""

import asyncio


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


def test_query_reads_existing_canon_without_durable_mutation():
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

    result = query("Portugal capital city Lisbon")

    assert result["answer"] is not None
    assert result["read_only"] is True
    assert result["query_policy"] == "canonical_read_only"
    assert get_fact(fact_id) == l1_before
    assert _graph_snapshot() == graph_before


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
