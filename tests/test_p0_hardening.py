"""Regression tests for the P0 cross-audit hardening (Claude / ChatGPT / Grok).

1. VELANTRIM_DB must actually redirect the L1 SQLite store — eval_gate.py and
   docs/DEMO.md set it for isolation, but core/memory.py used to ignore it.
2. reconcile._sync_l3() must not silently lose the L3 sync on a backend
   failure: like the pipeline, it queues the fact in the L3 outbox for retry.
3. consolidate() must survive a "ghost" L3 node whose L1 record was erased —
   merge_fact(None) used to crash the sleep cycle.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Repo root so the subprocess can import `core` regardless of cwd.
_REPO_ROOT = Path(__file__).resolve().parents[1]

from core.consolidate import consolidate
from core.ingest import ingest
from core.l3_graph import get_l3_graph
from core.pipeline import drain_l3_outbox
from core.queue import get_outbox_queue
from core import reconcile


# ─── 1. VELANTRIM_DB isolation ────────────────────────────────────────────────
# SQLITE_PATH is resolved at import time, so these run in a fresh subprocess —
# an in-process importlib.reload would invalidate the module references other
# test files hold (e.g. `from core.memory import _L0`).

_PROBE = (
    "import json, core.memory as m;"
    "m.store_fact({'fact_id': 'envdb1', 'claim': 'redirect', 'source': 't'});"
    "print(json.dumps({'path': m.SQLITE_PATH,"
    " 'claim': m.get_fact('envdb1')['claim']}))"
)


def _run_probe(cwd, extra_env):
    env = {k: v for k, v in os.environ.items() if k != "VELANTRIM_DB"}
    env.update({"VELANTRIM_L3_BACKEND": "mock", "VELANTRIM_EMBEDDER": "hashing",
                "VELANTRIM_GENERATOR": "extractive", **extra_env})
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(_REPO_ROOT) if not existing
        else str(_REPO_ROOT) + os.pathsep + existing
    )
    proc = subprocess.run([sys.executable, "-c", _PROBE], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip().splitlines()[-1])


def test_velantrim_db_env_redirects_l1(tmp_path):
    """With VELANTRIM_DB set, L1 lands at that path and the default
    ./data/velantrim_memory.db is never created."""
    target = tmp_path / "isolated" / "l1.db"
    out = _run_probe(tmp_path, {"VELANTRIM_DB": str(target)})
    assert out["path"] == str(target)
    assert out["claim"] == "redirect"
    assert target.exists()
    assert not (tmp_path / "data" / "velantrim_memory.db").exists()


def test_default_sqlite_path_without_env(tmp_path):
    """Without VELANTRIM_DB the default stays ./data/velantrim_memory.db."""
    out = _run_probe(tmp_path, {})
    assert out["path"] == "./data/velantrim_memory.db"
    assert (tmp_path / "data" / "velantrim_memory.db").exists()


# ─── 2. reconcile._sync_l3 self-heal via outbox ───────────────────────────────

def test_sync_l3_enqueues_on_merge_failure():
    """On an L3 merge failure the fact lands in the outbox and is healed by
    drain_l3_outbox once the backend is back — no exception, no lost sync."""
    res = ingest("Mercury is the closest planet to the Sun",
                 source="astro", confidence=0.9)
    assert res["accepted"]
    fid = res["fact"]["fact_id"]

    graph = get_l3_graph()

    def boom(_fact):
        raise RuntimeError("L3 backend down")

    graph.merge_fact = boom  # instance attribute shadows the class method
    try:
        new_conf = reconcile.reinforce(fid)  # must not raise
        assert new_conf is not None
        assert fid in get_outbox_queue().pending()
    finally:
        del graph.merge_fact  # backend is back

    healed = drain_l3_outbox()
    assert healed >= 1
    assert fid not in get_outbox_queue().pending()


# ─── 3. consolidate survives an erased L1 fact ────────────────────────────────

def test_consolidate_survives_l1_erased_fact():
    """A Validated L3 node whose L1 record is gone must not crash the sleep
    cycle via merge_fact(None)."""
    old = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
    get_l3_graph().merge_fact({
        "fact_id": "ghost1", "claim": "orphan canonical node", "source": "test",
        "confidence": 0.9, "significance": 0.5, "epistemic_state": "Validated",
        "created_at": old, "metadata": {"last_consolidated": old},
    })
    report = consolidate()  # no L1 record for ghost1 — must not raise
    assert "decayed" in report
