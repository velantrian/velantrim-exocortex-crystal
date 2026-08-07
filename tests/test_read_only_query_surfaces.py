"""Cross-surface regression tests for the read-only query service."""

import json

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


def _seed_verified(claim="Saturn has prominent rings"):
    from core.ingest import ingest

    result = ingest(
        claim,
        source="reference",
        source_status="EXTERNAL",
        confidence=0.95,
    )
    assert result["accepted"] is True
    return result["fact"]["fact_id"]


def test_public_search_reads_existing_graph_without_stamping_fingerprint():
    from core.l3_graph import get_l3_graph
    from core.memory import store_fact
    from core.query_pipeline import search

    fact = {
        "fact_id": "search:legacy",
        "claim": "Lisbon is the capital of Portugal",
        "source": "legacy-fixture",
        "confidence": 0.95,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
    }
    store_fact(fact)
    graph = get_l3_graph()
    graph.merge_fact(fact)
    assert graph.embedder_fingerprint() is None
    before = _graph_snapshot()

    rows = search("Lisbon capital Portugal", k=3)

    assert rows[0]["fact_id"] == fact["fact_id"]
    assert rows[0]["claim"] == fact["claim"]
    assert rows[0]["truth_status"] == "VERIFIED"
    assert rows[0]["score"] > 0
    assert "_score" not in rows[0]
    assert _graph_snapshot() == before


def test_public_search_excludes_restricted_rows_and_content():
    from core.compliance import restrict_processing
    from core.l3_graph import get_l3_graph
    from core.memory import store_fact
    from core.query_pipeline import search

    fact = {
        "fact_id": "search:restricted",
        "claim": "Private Zephyrstone research note",
        "source": "private-fixture",
        "confidence": 0.95,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
    }
    store_fact(fact)
    get_l3_graph().merge_fact(fact)
    restrict_processing(fact["fact_id"], reason="dispute")
    before = _graph_snapshot()

    rows = search("Zephyrstone research", k=5)

    assert rows == []
    assert "Zephyrstone" not in json.dumps(rows)
    assert _graph_snapshot() == before


@pytest.mark.parametrize("query,k,error", [
    ("   ", 5, "empty query"),
    ("valid", True, "positive integer"),
    ("valid", 0, "positive integer"),
    ("valid", 1.5, "positive integer"),
])
def test_public_search_rejects_invalid_inputs(query, k, error):
    from core.query_pipeline import search

    with pytest.raises(ValueError, match=error):
        search(query, k=k)


def test_public_search_discards_unknown_candidates(monkeypatch):
    from core import query_pipeline
    from core.l3_graph import get_l3_graph
    from core.memory import get_fact

    monkeypatch.setattr(
        query_pipeline,
        "_retrieve_read_only",
        lambda _query, k=None: [{"id": "ghost", "_score": 0.99}],
    )
    before = _graph_snapshot()

    assert query_pipeline.search("ghost", k=1) == []
    assert get_fact("ghost") is None
    assert get_l3_graph().get_fact("ghost") is None
    assert _graph_snapshot() == before


def test_cli_ask_is_read_only(capsys):
    from core.cli import main
    from core.memory import get_fact

    fact_id = _seed_verified()
    l1_before = get_fact(fact_id)
    graph_before = _graph_snapshot()

    rc = main(["ask", "Saturn rings"])

    assert rc == 0
    assert "rings" in capsys.readouterr().out.lower()
    assert get_fact(fact_id) == l1_before
    assert _graph_snapshot() == graph_before


def test_cli_receipt_success_is_read_only(capsys):
    from core.cli import main

    _seed_verified("Mercury is the closest planet to the Sun")
    before = _graph_snapshot()

    rc = main(["receipt", "Mercury closest planet Sun"])

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["citations"]
    assert _graph_snapshot() == before


def test_cli_receipt_failure_is_bounded(capsys):
    from core.cli import main

    rc = main(["receipt", "nothing is stored"])

    assert rc == 1
    payload = json.loads(capsys.readouterr().out)
    assert "error" in payload


def test_cli_query_commands_route_to_public_service(monkeypatch, capsys):
    from core import cli

    calls = []

    def fake_query(text):
        calls.append(text)
        return {
            "answer": "read-only answer",
            "facts": [],
            "trace": [],
            "read_only": True,
            "query_policy": "canonical_read_only",
        }

    monkeypatch.setattr(cli, "query", fake_query)

    assert cli.main(["ask", "first"]) == 0
    assert "read-only answer" in capsys.readouterr().out
    assert cli.main(["receipt", "second"]) == 0
    json.loads(capsys.readouterr().out)
    assert calls == ["first", "second"]


def test_mcp_search_uses_read_only_service_and_preserves_fingerprint(monkeypatch):
    from core import mcp_server, query_pipeline
    from core.l3_graph import get_l3_graph
    from core.memory import store_fact

    fact = {
        "fact_id": "mcp:legacy",
        "claim": "Neptune is an ice giant planet",
        "source": "legacy-fixture",
        "confidence": 0.91,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "restricted": False,
    }
    store_fact(fact)
    graph = get_l3_graph()
    graph.merge_fact(fact)
    assert graph.embedder_fingerprint() is None
    before = _graph_snapshot()
    calls = []
    real_search = query_pipeline.search_result

    def tracked_search(query, k=5):
        calls.append((query, k))
        return real_search(query, k=k)

    monkeypatch.setattr(query_pipeline, "search_result", tracked_search)

    response = mcp_server._tool_search("Neptune ice giant", k=2)

    assert calls == [("Neptune ice giant", 2)]
    assert response["reason_code"] == "ok"
    assert response["read_only"] is True
    assert response["query_policy"] == "canonical_read_only"
    assert response["results"][0]["fact_id"] == fact["fact_id"]
    assert response["results"][0]["truth_status"] == "VERIFIED"
    assert _graph_snapshot() == before
