"""Real cross-process writer races for update_fact() and review.approve().

Companion to the rewritten CAS tests in test_memory.py / test_review.py, which
inject an in-flight snapshot. Here nothing is injected: the caller's own read is
a real L1 read, and the competing write is a real committed write performed by
a separate OS process (same isolated temp database) in the window between that
read and the caller's own write. Only the timing is orchestrated, by running
the other process right after the caller's first read returns.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from core import memory, review
from core.l3_graph import get_l3_graph

REPO_ROOT = Path(__file__).resolve().parents[1]


def _other_process(tmp_path, code):
    env = dict(os.environ)
    env.update({
        "HOME": str(tmp_path), "PYTHONPATH": str(REPO_ROOT),
        "VELANTRIM_DB": memory.SQLITE_PATH, "VELANTRIM_L3_BACKEND": "mock",
        "VELANTRIM_STORAGE_PROFILE_PATH": str(tmp_path / "storage-profile.json"),
        "VELANTRIM_EMBEDDER": "hashing", "VELANTRIM_QUEUE_BACKEND": "sqlite",
        "VELANTRIM_DEMO_SEED": "0",
    })
    done = subprocess.run([sys.executable, "-c", code], cwd=tmp_path, env=env,
                          capture_output=True, text=True, check=True, timeout=60)
    return json.loads(done.stdout.strip().splitlines()[-1])


def _after_first_read(monkeypatch, module, action):
    """Run `action` once, right after `module.get_fact`'s first real read."""
    real_get_fact = module.get_fact
    fired = []

    def get_fact_then_race(fact_id):
        snapshot = real_get_fact(fact_id)
        if not fired:
            fired.append(action())
        return snapshot

    monkeypatch.setattr(module, "get_fact", get_fact_then_race)
    return fired


def test_update_fact_cas_rejects_write_committed_by_other_process(monkeypatch, tmp_path):
    memory.store_fact({"fact_id": "race1", "claim": "v0", "source": "s",
                       "confidence": 0.1})
    fired = _after_first_read(monkeypatch, memory, lambda: _other_process(
        tmp_path,
        "import json; from core.memory import update_fact; "
        "print(json.dumps({'ok': update_fact('race1', confidence=0.5)}))"))

    assert memory.update_fact("race1", confidence=0.9) is False  # CAS miss
    assert fired == [{"ok": True}]
    assert "race1" not in memory._L0  # evicted on the CAS miss
    persisted = memory.get_fact("race1")
    assert persisted["confidence"] == 0.5 and persisted["revision"] == 1
    assert memory.update_fact("race1", confidence=0.9) is True  # fresh retry


def test_approve_aborts_when_other_process_collapses_fact(monkeypatch, tmp_path):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = "cas:race-approve"
    memory.store_fact({
        "fact_id": fid, "claim": "A concurrently collapsed world claim",
        "source": "curator-test", "confidence": 0.9, "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL", "significance": 0.5,
    })
    fired = _after_first_read(monkeypatch, review, lambda: _other_process(
        tmp_path,
        "import json; from core.memory import transition_esm; "
        f"print(json.dumps({{'ok': transition_esm({fid!r}, 'Collapsed')}}))"))

    res = review.approve(fid, actor="alice")
    assert fired == [{"ok": True}]
    assert res["approved"] is False
    assert "CAS conflict" in res["reason"]
    assert get_l3_graph().get_fact(fid) is None
    assert memory.get_fact(fid)["epistemic_state"] == "Collapsed"
