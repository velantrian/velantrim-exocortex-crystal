# core/mcp_server.py
# Velantrim ExoCortex — minimal, READ-ONLY MCP server (stdio, JSON-RPC 2.0)
#
# Exposes the verifiable memory layer to MCP clients (Claude Desktop, Cursor, any
# MCP-capable agent) over the standard stdio transport — with ZERO third-party
# dependencies (pure Python stdlib), honouring the repo's local-first,
# stdlib-only promise.
#
# Scope: this is the READ-ONLY gateway. Every exposed tool is non-mutating
# (search, observability report, fact lookup, truth-maintenance history,
# conflict candidates, receipt verification). Write/curate tools (ingest,
# validate, supersede, erase) are deliberately NOT registered here. Role-based
# capability gating for write tools is a future roadmap step, not an implemented
# mechanism today.
#
# Enforcement model (what actually protects the canon today): allowlist-based
# read-only registration. Only the tools in READ_ONLY_TOOLS exist, and
# `tools/call` refuses any name that is not in that registry — so a client never
# sees a write tool and a model cannot call one by accident. There is no runtime
# capability/role check; safety comes from the fact that no mutating tool is
# registered at all.
#
# Transport: newline-delimited JSON-RPC 2.0 over stdin/stdout (the MCP stdio
# transport). Run as:
#     python -m core.mcp_server
# Wire into Claude Desktop (claude_desktop_config.json):
#     {"mcpServers": {"velantrim": {"command": "python",
#                                    "args": ["-m", "core.mcp_server"]}}}

from __future__ import annotations

import sys
import json
import logging
from typing import Any, Dict, Optional, Callable

from core import __version__

logger = logging.getLogger("velantrim.mcp")

# Protocol version advertised if the client does not specify one.
_DEFAULT_PROTOCOL = "2024-11-05"
_SERVER_NAME = "velantrim"
# Informational advertised mode label only — NOT an enforcement mechanism.
# Read-only safety is provided by allowlist-based registration (READ_ONLY_TOOLS),
# not by checking this value anywhere. Kept as a public label for clients/imports.
CAPABILITY = "reader"


# ─── Read-only tool implementations ───────────────────────────────────────────
# Each returns a JSON-serialisable object. Heavy imports are done lazily inside
# the function so importing this module stays cheap and a failure in one
# subsystem cannot break the whole server at import time.

def _tool_search(query: str, k: int = 5) -> Any:
    from core.pipeline import retrieve
    hits = retrieve(query, k=int(k))
    return [
        {
            "fact_id": h.get("id"),
            "text": h.get("text"),
            "source": h.get("source"),
            "score": h.get("_score"),
            "epistemic_state": h.get("epistemic_state"),
        }
        for h in hits
    ]


def _tool_memory_report() -> Any:
    from core.observe import memory_report
    return memory_report()


def _tool_get_fact(fact_id: str) -> Any:
    from core.memory import get_fact
    fact = get_fact(fact_id)
    if fact is None:
        return {"found": False, "fact_id": fact_id}
    if fact.get("restricted"):
        # GDPR Art. 18: processing is restricted for this fact. Unlike
        # pipeline.retrieve (which silently excludes restricted nodes from
        # search/graph-walk), a direct by-id lookup must say something — so
        # get_fact refuses with a stable reason code instead of returning the
        # claim text or any other raw stored field.
        return {
            "found": True,
            "fact_id": fact_id,
            "restricted": True,
            "reason": "RESTRICTED_BY_POLICY",
            "message": "Fact is restricted and cannot be returned through MCP get_fact.",
        }
    return {"found": True, **fact}


def _tool_fact_history(fact_id: str) -> Any:
    from core.reconcile import fact_history
    return fact_history(fact_id)


def _tool_find_conflicts(claim: str) -> Any:
    from core.reconcile import find_conflicts
    return find_conflicts(claim)


def _tool_verify_receipt(receipt: Dict[str, Any]) -> Any:
    from core.provenance import verify_receipt
    return verify_receipt(receipt)


# ─── Tool registry (read-only) ────────────────────────────────────────────────

class _Tool:
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any],
                 handler: Callable[[Dict[str, Any]], Any]):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler

    def manifest(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


def _str_prop(desc: str) -> Dict[str, str]:
    return {"type": "string", "description": desc}


# Registry of the tools available at the read-only ("reader") capability.
READ_ONLY_TOOLS: Dict[str, _Tool] = {}


def _register(tool: _Tool) -> None:
    READ_ONLY_TOOLS[tool.name] = tool


_register(_Tool(
    "search",
    "Read-only semantic + graph search over the canonical memory. Returns ranked "
    "facts. Does not write anything.",
    {
        "type": "object",
        "properties": {
            "query": _str_prop("natural-language query"),
            "k": {"type": "integer", "description": "max results (default 5)"},
        },
        "required": ["query"],
    },
    lambda args: _tool_search(args["query"], args.get("k", 5)),
))

_register(_Tool(
    "memory_report",
    "Read-only observability report over the L3 canonical graph: fact counts by "
    "ESM state / claim type / truth status, edges by type, contradictions and "
    "weak facts.",
    {"type": "object", "properties": {}},
    lambda args: _tool_memory_report(),
))

_register(_Tool(
    "get_fact",
    "Read-only lookup of a single fact by its fact_id.",
    {
        "type": "object",
        "properties": {"fact_id": _str_prop("the fact id")},
        "required": ["fact_id"],
    },
    lambda args: _tool_get_fact(args["fact_id"]),
))

_register(_Tool(
    "fact_history",
    "Read-only truth-maintenance provenance of a fact (superseded_by / supersedes "
    "/ contradicts / contradicted_by).",
    {
        "type": "object",
        "properties": {"fact_id": _str_prop("the fact id")},
        "required": ["fact_id"],
    },
    lambda args: _tool_fact_history(args["fact_id"]),
))

_register(_Tool(
    "find_conflicts",
    "Read-only: list canonical WORLD_FACTs that conflict with a claim. Candidates "
    "are classified CONTRADICTION / REFINEMENT / RELATED. Does not write anything.",
    {
        "type": "object",
        "properties": {"claim": _str_prop("the claim to check against the canon")},
        "required": ["claim"],
    },
    lambda args: _tool_find_conflicts(args["claim"]),
))

_register(_Tool(
    "verify_receipt",
    "Read-only: replay a provenance receipt against the current canon and report "
    "drift (erased / restricted / modified / contradicted).",
    {
        "type": "object",
        "properties": {
            "receipt": {"type": "object",
                        "description": "a receipt object from `velantrim receipt`"},
        },
        "required": ["receipt"],
    },
    lambda args: _tool_verify_receipt(args["receipt"]),
))


# ─── JSON-RPC / MCP message handling ──────────────────────────────────────────

def _result(req_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _error(req_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def handle_message(msg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Handle one JSON-RPC message.

    Returns a response dict, or None for notifications (messages without an id).
    """
    req_id = msg.get("id")
    method = msg.get("method")
    is_notification = "id" not in msg

    if method == "initialize":
        params = msg.get("params") or {}
        protocol = params.get("protocolVersion") or _DEFAULT_PROTOCOL
        return _result(req_id, {
            "protocolVersion": protocol,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": _SERVER_NAME, "version": __version__},
        })

    if method in ("notifications/initialized", "initialized"):
        return None  # client handshake notification — no response

    if method == "ping":
        return _result(req_id, {})

    if method == "tools/list":
        return _result(req_id, {"tools": [t.manifest() for t in READ_ONLY_TOOLS.values()]})

    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        tool = READ_ONLY_TOOLS.get(name)
        if tool is None:
            # Unknown/unavailable tool: report as a tool error, not a protocol error.
            return _result(req_id, {
                "content": [{"type": "text",
                             "text": f"Unknown or unavailable tool: {name!r}"}],
                "isError": True,
            })
        try:
            output = tool.handler(arguments)
            text = json.dumps(output, ensure_ascii=False, indent=2, default=str)
            return _result(req_id, {
                "content": [{"type": "text", "text": text}],
                "isError": False,
            })
        except Exception as exc:  # noqa: BLE001 — surface tool errors, don't crash the server
            logger.exception("tool %s failed", name)
            return _result(req_id, {
                "content": [{"type": "text",
                             "text": f"Error in {name}: {type(exc).__name__}: {exc}"}],
                "isError": True,
            })

    if is_notification:
        return None  # ignore unknown notifications

    return _error(req_id, -32601, f"Method not found: {method}")


def serve(stdin=None, stdout=None) -> None:
    """Run the stdio loop: read newline-delimited JSON-RPC, write responses."""
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            stdout.write(json.dumps(_error(None, -32700, "Parse error")) + "\n")
            stdout.flush()
            continue
        response = handle_message(msg)
        if response is not None:
            stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            stdout.flush()


def main(argv=None) -> int:  # pragma: no cover
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
    serve()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
