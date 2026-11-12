"""Regression for #505: a process-local L0 entry must not outlive an erasure
committed by another process against the same L1 database.

Every role runs real Crystal code in its own OS process against an isolated
temporary database: facts are created with ``python -m core.cli ingest``,
erased with ``python -m core.cli erase`` (the documented erase_fact() path)
and read by a long-running reader that keeps its L0 between requests.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from core import memory

REPO_ROOT = Path(__file__).resolve().parents[1]

# Long-running reader: one JSON request per stdin line, one JSON reply per
# stdout line. Its L0 survives between requests, like a server process.
_READER = r"""
import json, sys
from core import memory
from core.mcp_server import handle_message

print(json.dumps({"ready": True}), flush=True)
for line in sys.stdin:
    fact_id = json.loads(line)["fact_id"]
    fact = memory.get_fact(fact_id)
    reply = handle_message({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "get_fact", "arguments": {"fact_id": fact_id}},
    })
    mcp = json.loads(reply["result"]["content"][0]["text"])
    print(json.dumps({
        "claim": None if fact is None else fact["claim"],
        "served_from_l0": fact is not None and memory._L0.get(fact_id) is fact,
        "in_l0": fact_id in memory._L0,
        "mcp_found": mcp["found"],
    }), flush=True)
"""


@pytest.fixture
def crystal_env(tmp_path):
    """Environment that points every child process at isolated temp storage."""
    env = dict(os.environ)
    env.update({
        "HOME": str(tmp_path),
        "PYTHONPATH": str(REPO_ROOT),
        "VELANTRIM_DB": str(tmp_path / "memory.db"),
        "VELANTRIM_L3_BACKEND": "sqlite",
        "VELANTRIM_L3_PATH": str(tmp_path / "l3.db"),
        "VELANTRIM_STORAGE_PROFILE_PATH": str(tmp_path / "storage-profile.json"),
        "VELANTRIM_EMBEDDER": "hashing",
        "VELANTRIM_GENERATOR": "extractive",
        "VELANTRIM_QUEUE_BACKEND": "sqlite",
        "VELANTRIM_DEMO_SEED": "0",
    })
    return env


def _cli(env, *args):
    done = subprocess.run(
        [sys.executable, "-m", "core.cli", *args], cwd=env["HOME"], env=env,
        capture_output=True, text=True, check=True, timeout=60,
    )
    return json.loads(done.stdout.strip().splitlines()[-1])


class _Reader:
    """A separate, long-running reader process with its own L0."""

    def __init__(self, env):
        self.proc = subprocess.Popen(
            [sys.executable, "-u", "-c", _READER], cwd=env["HOME"], env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True,
        )
        assert json.loads(self.proc.stdout.readline()) == {"ready": True}

    def read(self, fact_id):
        self.proc.stdin.write(json.dumps({"fact_id": fact_id}) + "\n")
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
        reader = _Reader(env)
        started.append(reader)
        return reader

    yield start
    for reader in started:
        reader.close()


def test_running_reader_does_not_serve_fact_erased_by_other_process(
    crystal_env, readers
):
    erased_id = _cli(crystal_env, "ingest", "Synthetic 505 fact alpha-quartz")["fact_id"]
    kept_id = _cli(crystal_env, "ingest", "Synthetic 505 fact beta-garnet")["fact_id"]

    reader = readers(crystal_env)
    first = reader.read(erased_id)
    assert first["claim"] == "Synthetic 505 fact alpha-quartz"
    assert first["in_l0"] is True  # the reader has cached the fact
    assert reader.read(kept_id)["in_l0"] is True

    receipt = _cli(crystal_env, "erase", erased_id)  # other process, real path
    assert receipt["erased_now"] is True and receipt["l1_removed"] is True

    # Same reader, no restart: neither get_fact nor MCP get_fact returns it.
    for _ in range(2):
        again = reader.read(erased_id)
        assert again == {"claim": None, "served_from_l0": False,
                         "in_l0": False, "mcp_found": False}

    # A fact that was not erased is still read normally and still from L0.
    kept = reader.read(kept_id)
    assert kept["claim"] == "Synthetic 505 fact beta-garnet"
    assert kept["served_from_l0"] is True and kept["mcp_found"] is True

    # A restarted reader agrees.
    restarted = readers(crystal_env)
    assert restarted.read(erased_id)["claim"] is None
    assert restarted.read(kept_id)["claim"] == "Synthetic 505 fact beta-garnet"


def _this_process_env(crystal_env):
    env = dict(crystal_env)
    env["VELANTRIM_DB"] = memory.SQLITE_PATH  # the DB isolated by conftest
    return env


def test_this_process_l0_is_revalidated_after_other_process_erase(crystal_env):
    env = _this_process_env(crystal_env)
    memory.store_fact({"fact_id": "issue-505", "claim": "synthetic", "source": "test"})
    memory.store_fact({"fact_id": "issue-505-kept", "claim": "kept", "source": "test"})
    assert memory.get_fact("issue-505")["claim"] == "synthetic"
    assert "issue-505" in memory._L0

    assert _cli(env, "erase", "issue-505")["l1_removed"] is True

    assert memory.get_fact("issue-505") is None
    assert memory.get_fact("issue-505") is None
    assert "issue-505" not in memory._L0
    cached = memory._L0["issue-505-kept"]
    assert memory.get_fact("issue-505-kept") is cached  # valid L0 hit served


def test_this_process_l0_is_not_served_for_fact_recreated_after_erase(crystal_env):
    env = _this_process_env(crystal_env)
    memory.store_fact({"fact_id": "issue-505-r", "claim": "old", "source": "test"})
    old = memory.get_fact("issue-505-r")
    assert memory._L0["issue-505-r"] is old

    # Another process erases the fact and then stores a new row under the
    # same fact_id (whether such re-creation should be allowed after an
    # erasure is a separate contract question; only the cache is tested).
    assert _cli(env, "erase", "issue-505-r")["l1_removed"] is True
    subprocess.run(
        [sys.executable, "-c",
         "from core.memory import store_fact; store_fact({'fact_id': "
         "'issue-505-r', 'claim': 'new', 'source': 'test'})"],
        cwd=env["HOME"], env=env, check=True, timeout=60,
    )

    fresh = memory.get_fact("issue-505-r")
    assert fresh["claim"] == "new"
    assert fresh["created_at"] != old["created_at"]
    assert memory._L0["issue-505-r"] is fresh
