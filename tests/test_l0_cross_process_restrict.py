"""GDPR Art. 18 restriction committed by another process must be visible to an
already-running process that cached the fact (separate from #505 erasure).

Real OS processes on isolated temp storage, nothing stubbed:
  C  ``python -m core.cli learn`` imports a synthetic source file (VERIFIED);
  A  a long-running reader caches the fact and reads it through every read API
     available in-process: core.memory.get_fact, MCP get_fact, MCP search,
     query_pipeline.query (strict ask), HTTP POST /ask, GET /review/item/{id},
     GET /evidence/{id} (FastAPI TestClient, no network);
  B  ``python -m core.cli restrict`` (compliance.restrict_processing);
  A  reads again WITHOUT restart; A' is a restarted reader;
  ``python -m core.cli ask`` is checked as a fresh process.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
QUESTION = "Where is the Zorblat Tower?"
NEEDLE = "Quuxville"

_READER = r"""
import json, os, sys
from fastapi.testclient import TestClient
from core import memory
from core.api import create_app
from core.mcp_server import handle_message
from core.query_pipeline import query

client = TestClient(create_app())
auth = {"Authorization": "Bearer " + os.environ["VELANTRIM_API_TOKEN"]}


def tool(name, args):
    reply = handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                            "params": {"name": name, "arguments": args}})
    return json.loads(reply["result"]["content"][0]["text"])


print(json.dumps({"ready": True}), flush=True)
for line in sys.stdin:
    req = json.loads(line)
    fid, question, needle = req["fact_id"], req["question"], req["needle"]
    fact = memory.get_fact(fid)
    mcp = tool("get_fact", {"fact_id": fid})
    hits = tool("search", {"query": question, "k": 5}).get("results") or []
    answer = query(question).get("answer") or ""
    http_answer = client.post("/ask", json={"query": question}, headers=auth).json()
    item = client.get(f"/review/item/{fid}", headers=auth)
    evidence = client.get(f"/evidence/{fid}", headers=auth)
    print(json.dumps({
        "in_l0": fid in memory._L0,
        "get_fact_restricted": None if fact is None else fact["restricted"],
        "mcp_get_fact": mcp,
        "mcp_search_hit": fid in [h.get("fact_id") for h in hits],
        "query_answers": needle in answer,
        "http_ask_answers": needle in (http_answer.get("answer") or ""),
        "http_review_item_status": item.status_code,
        "http_review_item_shows_claim": needle in item.text,
        "http_review_item_verdict": (item.json().get("diagnosis") or {}).get("verdict")
        if item.status_code == 200 else None,
        "http_evidence": evidence.json(),
    }), flush=True)
"""


@pytest.fixture
def env(tmp_path):
    env = dict(os.environ)
    env.update({
        "HOME": str(tmp_path), "PYTHONPATH": str(REPO_ROOT),
        "VELANTRIM_DB": str(tmp_path / "memory.db"),
        "VELANTRIM_L3_BACKEND": "sqlite", "VELANTRIM_L3_PATH": str(tmp_path / "l3.db"),
        "VELANTRIM_STORAGE_PROFILE_PATH": str(tmp_path / "storage-profile.json"),
        "VELANTRIM_EMBEDDER": "hashing", "VELANTRIM_GENERATOR": "extractive",
        "VELANTRIM_QUEUE_BACKEND": "sqlite", "VELANTRIM_DEMO_SEED": "0",
        "VELANTRIM_API_TOKEN": "synthetic-test-token",
    })
    return env


def _run(env, *args):
    return subprocess.run([sys.executable, *args], cwd=env["HOME"], env=env,
                          capture_output=True, text=True, check=True, timeout=120)


class _Reader:
    def __init__(self, env):
        self.proc = subprocess.Popen(
            [sys.executable, "-u", "-c", _READER], cwd=env["HOME"], env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True)
        line = self.proc.stdout.readline()
        assert line, self.proc.stderr.read()
        assert json.loads(line) == {"ready": True}

    def read(self, fact_id):
        self.proc.stdin.write(json.dumps(
            {"fact_id": fact_id, "question": QUESTION, "needle": NEEDLE}) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        assert line, self.proc.stderr.read()
        return json.loads(line)

    def close(self):
        if self.proc.poll() is None:
            self.proc.stdin.close()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:  # pragma: no cover - cleanup only
                self.proc.kill()
                self.proc.wait()
        self.proc.stdout.close()
        self.proc.stderr.close()


@pytest.fixture
def readers():
    started = []

    def start(env):
        started.append(_Reader(env))
        return started[-1]

    yield start
    for reader in started:
        reader.close()


def _assert_restricted_everywhere(obs, fact_id):
    assert obs["get_fact_restricted"] == 1
    assert obs["mcp_get_fact"] == {
        "found": True, "fact_id": fact_id, "restricted": True,
        "reason": "RESTRICTED_BY_POLICY",
        "message": "Fact is restricted and cannot be returned through MCP get_fact.",
    }
    assert obs["mcp_search_hit"] is False
    assert obs["query_answers"] is False
    assert obs["http_ask_answers"] is False
    assert obs["http_review_item_status"] == 200
    assert obs["http_review_item_shows_claim"] is False
    assert obs["http_review_item_verdict"] == "restricted"
    assert obs["http_evidence"] == []


def test_running_reader_sees_restriction_committed_by_other_process(env, readers):
    source = Path(env["HOME"]) / "source.txt"
    source.write_text(f"The Zorblat Tower is in {NEEDLE}.\n")
    _run(env, "-m", "core.cli", "learn", str(source))
    fact_id = json.loads(_run(env, "-c", (
        "import json; from core.memory import _db\n"
        "with _db() as c: print(json.dumps(c.execute("
        "'SELECT fact_id FROM facts').fetchone()[0]))")).stdout)

    reader = readers(env)
    before = reader.read(fact_id)
    assert before["in_l0"] is True and before["get_fact_restricted"] == 0
    assert before["mcp_get_fact"]["claim"].endswith(f"{NEEDLE}.")
    assert before["mcp_search_hit"] and before["query_answers"]
    assert before["http_ask_answers"] and before["http_review_item_shows_claim"]
    assert len(before["http_evidence"]) == 1

    receipt = json.loads(_run(env, "-m", "core.cli", "restrict", fact_id).stdout)
    assert receipt["found"] is True and receipt["restricted"] is True

    for _ in range(2):  # same reader, no restart
        _assert_restricted_everywhere(reader.read(fact_id), fact_id)
    _assert_restricted_everywhere(readers(env).read(fact_id), fact_id)  # restarted

    cli_ask = _run(env, "-m", "core.cli", "ask", QUESTION).stdout  # fresh process
    assert NEEDLE not in cli_ask
