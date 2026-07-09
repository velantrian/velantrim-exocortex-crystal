"""Tests for the read-only MCP server (core/mcp_server.py).

Exercises the JSON-RPC/MCP handshake, the read-only tool surface, error paths,
and the stdio serve() loop — all on the dependency-free mock backends pinned by
the autouse `isolated_db` fixture.
"""
import io
import json

import pytest

from core import mcp_server, __version__


def _call(method, params=None, req_id=1):
    msg = {"jsonrpc": "2.0", "id": req_id, "method": method}
    if params is not None:
        msg["params"] = params
    return mcp_server.handle_message(msg)


# ─── handshake ────────────────────────────────────────────────────────────────

def test_initialize_reports_server_info():
    resp = _call("initialize", {"protocolVersion": "2025-06-18"})
    assert resp["result"]["serverInfo"] == {"name": "velantrim", "version": __version__}
    # Echoes the client's requested protocol version.
    assert resp["result"]["protocolVersion"] == "2025-06-18"
    assert "tools" in resp["result"]["capabilities"]


def test_initialize_defaults_protocol_when_absent():
    resp = _call("initialize", {})
    assert resp["result"]["protocolVersion"] == mcp_server._DEFAULT_PROTOCOL


def test_initialized_notification_has_no_response():
    # No "id" → a notification → must not produce a response.
    assert mcp_server.handle_message({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_ping():
    assert _call("ping")["result"] == {}


# ─── tools/list ───────────────────────────────────────────────────────────────

def test_tools_list_is_read_only_surface():
    tools = _call("tools/list")["result"]["tools"]
    names = {t["name"] for t in tools}
    assert names == {
        "search", "memory_report", "get_fact",
        "fact_history", "find_conflicts", "verify_receipt",
    }
    # No write/destructive tools are exposed at the reader capability.
    for forbidden in ("ingest", "store_fact", "erase", "supersede", "validate"):
        assert forbidden not in names
    # Every tool has a JSON-Schema inputSchema.
    for t in tools:
        assert t["inputSchema"]["type"] == "object"


# ─── tools/call: each read-only tool runs ─────────────────────────────────────

def test_call_search_returns_hits():
    resp = _call("tools/call", {"name": "search", "arguments": {"query": "water", "k": 3}})
    assert resp["result"]["isError"] is False
    payload = json.loads(resp["result"]["content"][0]["text"])
    assert isinstance(payload, list)


def test_call_memory_report():
    resp = _call("tools/call", {"name": "memory_report", "arguments": {}})
    assert resp["result"]["isError"] is False
    payload = json.loads(resp["result"]["content"][0]["text"])
    assert "total_facts" in payload


def test_call_get_fact_missing_and_present():
    # Missing fact.
    resp = _call("tools/call", {"name": "get_fact", "arguments": {"fact_id": "nope"}})
    assert json.loads(resp["result"]["content"][0]["text"]) == {"found": False, "fact_id": "nope"}
    # Present fact (ingest one first).
    from core.ingest import ingest
    fid = ingest("Water is wet")["fact"]["fact_id"]
    resp = _call("tools/call", {"name": "get_fact", "arguments": {"fact_id": fid}})
    payload = json.loads(resp["result"]["content"][0]["text"])
    assert payload["found"] is True and payload["fact_id"] == fid


def test_mcp_get_fact_unrestricted_preserves_existing_behavior():
    from core.ingest import ingest
    fid = ingest("Grass is green")["fact"]["fact_id"]
    resp = _call("tools/call", {"name": "get_fact", "arguments": {"fact_id": fid}})
    payload = json.loads(resp["result"]["content"][0]["text"])
    assert payload["found"] is True
    assert payload["fact_id"] == fid
    assert payload.get("restricted") in (0, False, None)
    assert payload["claim"] == "Grass is green"


def test_mcp_get_fact_respects_processing_restriction():
    from core.memory import store_fact, get_fact
    from core.l3_graph import get_l3_graph
    from core.compliance import restrict_processing

    fact_id = "mcp_restricted_f1"
    store_fact({"fact_id": fact_id, "claim": "a secret claim", "source": "test",
                "epistemic_state": "Validated"})
    get_l3_graph().merge_fact(get_fact(fact_id))
    restrict_processing(fact_id, reason="dispute")

    resp = _call("tools/call", {"name": "get_fact", "arguments": {"fact_id": fact_id}})
    assert resp["result"]["isError"] is False
    payload = json.loads(resp["result"]["content"][0]["text"])

    assert payload["found"] is True
    assert payload["restricted"] is True
    assert payload["reason"] == "RESTRICTED_BY_POLICY"
    # The raw claim/content must never appear in a restricted response.
    assert "claim" not in payload
    assert "metadata" not in payload
    assert "a secret claim" not in json.dumps(payload)


def test_mcp_search_excludes_restricted_facts():
    from core.memory import store_fact, get_fact
    from core.l3_graph import get_l3_graph
    from core.compliance import restrict_processing
    from core.pipeline import retrieve

    fact_id = "mcp_restricted_search_f1"
    claim = "Zylthorpe hums with quiet indigo static"
    store_fact({"fact_id": fact_id, "claim": claim, "source": "test",
                "epistemic_state": "Validated"})
    get_l3_graph().merge_fact(get_fact(fact_id))
    assert fact_id in [h["id"] for h in retrieve(claim)]

    restrict_processing(fact_id, reason="dispute")

    resp = _call("tools/call", {"name": "search", "arguments": {"query": claim, "k": 5}})
    assert resp["result"]["isError"] is False
    payload = json.loads(resp["result"]["content"][0]["text"])
    assert fact_id not in [h["fact_id"] for h in payload]


def test_call_fact_history_and_find_conflicts():
    h = _call("tools/call", {"name": "fact_history", "arguments": {"fact_id": "x"}})
    assert "superseded_by" in json.loads(h["result"]["content"][0]["text"])
    c = _call("tools/call", {"name": "find_conflicts", "arguments": {"claim": "water boils"}})
    assert isinstance(json.loads(c["result"]["content"][0]["text"]), list)


def test_mcp_find_conflicts_excludes_restricted_facts():
    """GDPR Art. 18: the MCP `find_conflicts` tool must not reveal a
    restricted fact's claim as a conflict candidate."""
    from core.memory import store_fact, transition_esm, get_fact
    from core.l3_graph import get_l3_graph
    from core.compliance import restrict_processing

    fact_id = "mcp_restricted_conflict_f1"
    store_fact({"fact_id": fact_id, "claim": "The capital of Freldania is Sunmere",
                "source": "test", "confidence": 0.9, "claim_type": "WORLD_FACT"})
    transition_esm(fact_id, "Validated")
    get_l3_graph().merge_fact(get_fact(fact_id))
    restrict_processing(fact_id, reason="dispute")

    resp = _call("tools/call", {"name": "find_conflicts",
                                 "arguments": {"claim": "The capital of Freldania is Rivenholt"}})
    assert resp["result"]["isError"] is False
    payload = json.loads(resp["result"]["content"][0]["text"])
    assert fact_id not in [h["fact_id"] for h in payload]
    assert "Sunmere" not in json.dumps(payload)


def test_call_verify_receipt_roundtrips():
    # Build a real receipt, then verify it through the tool.
    from core.pipeline import run
    from core.provenance import build_receipt
    res = run("water")
    if res.get("answer") is not None:
        receipt = build_receipt(res)
        resp = _call("tools/call", {"name": "verify_receipt", "arguments": {"receipt": receipt}})
        assert resp["result"]["isError"] is False
    else:  # pragma: no cover - retrieval is deterministic but stay robust
        resp = _call("tools/call", {"name": "verify_receipt", "arguments": {"receipt": {}}})
        assert "content" in resp["result"]


# ─── error paths ──────────────────────────────────────────────────────────────

def test_call_unknown_tool_is_tool_error():
    resp = _call("tools/call", {"name": "definitely_not_a_tool", "arguments": {}})
    assert resp["result"]["isError"] is True


def test_call_missing_required_arg_is_tool_error():
    # search without the required "query" → handler raises KeyError → isError.
    resp = _call("tools/call", {"name": "search", "arguments": {}})
    assert resp["result"]["isError"] is True


def test_unknown_method_returns_jsonrpc_error():
    resp = _call("does/not/exist")
    assert resp["error"]["code"] == -32601


def test_unknown_notification_is_ignored():
    assert mcp_server.handle_message({"jsonrpc": "2.0", "method": "some/notice"}) is None


# ─── stdio serve() loop ───────────────────────────────────────────────────────

def test_serve_stdio_loop():
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05"}}),
        "",                  # blank line → skipped
        "{ not valid json",  # parse error → JSON-RPC parse error
        json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),  # no response
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
    ]
    out = io.StringIO()
    mcp_server.serve(io.StringIO("\n".join(lines) + "\n"), out)

    responses = [json.loads(l) for l in out.getvalue().splitlines() if l.strip()]
    # initialize(id=1), parse-error(id=None), tools/list(id=2) — notification produced nothing.
    assert len(responses) == 3
    assert responses[0]["id"] == 1 and "result" in responses[0]
    assert responses[1]["error"]["code"] == -32700
    assert responses[2]["id"] == 2 and "tools" in responses[2]["result"]
