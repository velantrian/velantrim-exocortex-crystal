"""Crash boundaries for the existing CR-04 automatic admission outbox."""
import importlib
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from core import memory, pipeline
from core.l3_graph import get_l3_graph
from core.queue import get_outbox_queue


_CLAIM = "A synthetic durable admission sample about copper and quartz."
_FID = "durable-admission"
_EXIT = 73

_WRITER = r"""
import importlib
import os
import sys
from core import memory, pipeline
from core.l3_graph import get_l3_graph

entrypoint, boundary = sys.argv[1:]
if os.environ.get("CRYSTAL_TEST_REDIS_DOWN") == "1":
    from core import queue
    def unavailable():
        raise ConnectionError("synthetic Redis connection failure")
    queue._redis_client = unavailable
ingestion = importlib.import_module("core.ingest")
fid = "durable-admission"
claim = "A synthetic durable admission sample about copper and quartz."
graph = get_l3_graph()
pipeline.retrieve = lambda *a, **k: [{
    "id": fid, "text": claim, "source": "synthetic", "confidence": 0.9,
    "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
    "significance": 0.5, "_score": 0.9, "epistemic_state": "Observed",
    "origin": "memory",
}]
module = ingestion if entrypoint == "ingest" else pipeline
if boundary == "before_commit":
    real_stage = memory._stage_l3_admission
    def stage_and_die(*args):
        real_stage(*args)
        os._exit(73)
    memory._stage_l3_admission = stage_and_die
elif boundary == "after_commit":
    module._project_l3_admission = lambda *a: os._exit(73)
elif boundary == "after_graph":
    real_merge = graph.merge_fact
    def merge_and_die(payload):
        real_merge(payload)
        os._exit(73)
    graph.merge_fact = merge_and_die
elif boundary == "after_error":
    def fail(_payload):
        raise RuntimeError("synthetic backend outage")
    graph.merge_fact = fail

if entrypoint == "ingest":
    result = ingestion.ingest(claim, fact_id=fid, source="synthetic",
                              confidence=0.9, source_status="EXTERNAL")
    assert result["accepted"] is False
else:
    result = pipeline.run("synthetic")
    assert result["answer"] is None
assert boundary == "after_error"
assert memory._pending_l3_admissions()[0]["fact_id"] == fid
os._exit(73)
"""

_READER = r"""
import os
import sys
from core import memory, pipeline
from core.l3_graph import get_l3_graph
if os.environ.get("CRYSTAL_TEST_REDIS_DOWN") == "1":
    from core import queue
    def unavailable():
        raise ConnectionError("synthetic Redis connection failure")
    queue._redis_client = unavailable
boundary = sys.argv[1]
fid = "durable-admission"
fact = memory.get_fact(fid)
graph = get_l3_graph()
if boundary == "before_commit":
    assert fact["epistemic_state"] == "Observed"
    assert not memory._pending_l3_admissions()
    assert not memory.pending_l3_writes()
    assert graph.get_fact(fid) is None
    assert pipeline.drain_l3_outbox() == 0
else:
    assert fact["epistemic_state"] == "Validated"
    pending = memory._pending_l3_admissions()
    assert len(pending) == 1
    assert pending[0]["fact_id"] == fid
    assert pending[0]["truth_status"] == "VERIFIED"
    assert pending[0]["revision"] == fact["revision"]
    assert memory.pending_l3_writes() == [fid]
    assert (graph.get_fact(fid) is not None) == (boundary == "after_graph")
    def no_new_verdict(*a):
        raise AssertionError("recovery must not compute admission authority")
    pipeline._truth_status_for = no_new_verdict
    real_merge = graph.merge_fact
    writes = []
    def track(payload):
        writes.append(payload)
        real_merge(payload)
    graph.merge_fact = track
    assert pipeline.drain_l3_outbox() == 1
    assert pipeline.drain_l3_outbox() == 0
    assert len(writes) == (0 if boundary == "after_graph" else 1)
    assert graph.get_fact(fid)["truth_status"] == "VERIFIED"
    assert graph.get_fact(fid)["claim"] == fact["claim"]
    assert memory._pending_l3_admissions() == []
    assert memory.pending_l3_writes() == []
"""


@pytest.fixture
def child_env(tmp_path):
    env = dict(os.environ)
    env.update({
        "HOME": str(tmp_path),
        "PYTHONPATH": str(Path(__file__).resolve().parents[1]),
        "VELANTRIM_DB": str(tmp_path / "admission.db"),
        "VELANTRIM_L3_BACKEND": "sqlite",
        "VELANTRIM_L3_PATH": str(tmp_path / "graph.db"),
        "VELANTRIM_STORAGE_PROFILE_PATH": str(tmp_path / "storage-profile.json"),
        "VELANTRIM_QUEUE_PROFILE_PATH": str(tmp_path / "queue-profile"),
        "VELANTRIM_QUEUE_BACKEND": "sqlite",
        "VELANTRIM_EMBEDDER": "hashing",
        "VELANTRIM_GENERATOR": "extractive",
        "VELANTRIM_DEMO_SEED": "0",
    })
    return env


def _child(env, script, *args, exit_code=0):
    completed = subprocess.run(
        [sys.executable, "-c", script, *args], env=env, cwd=env["HOME"],
        capture_output=True, text=True, timeout=90,
    )
    assert completed.returncode == exit_code, completed.stdout + completed.stderr


@pytest.mark.parametrize("entrypoint", ["ingest", "run"])
@pytest.mark.parametrize("boundary", [
    "before_commit", "after_commit", "after_error", "after_graph",
])
def test_first_projection_crash_survives_restart(child_env, entrypoint, boundary):
    _child(child_env, _WRITER, entrypoint, boundary, exit_code=_EXIT)
    _child(child_env, _READER, boundary)


def _stage(fid=_FID, claim=_CLAIM, verdict="VERIFIED"):
    original = memory.store_fact({
        "fact_id": fid, "claim": claim, "source": "synthetic", "confidence": 0.9,
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
    }, return_persisted=True)
    promoted = memory.transition_esm_if_unchanged(
        original, "Validated", admission_verdict=verdict,
    )
    assert promoted is not None
    return promoted, memory._l3_admission_identity(promoted, verdict)


def test_locked_redis_outage_does_not_strand_sqlite_admission(monkeypatch, tmp_path):
    from core import queue as queue_mod

    profile = tmp_path / "queue-profile"
    profile.write_text("redis\n", encoding="ascii")
    monkeypatch.setenv("VELANTRIM_QUEUE_BACKEND", "auto")
    monkeypatch.setenv("VELANTRIM_QUEUE_PROFILE_PATH", str(profile))
    connect = Mock(side_effect=ConnectionError("synthetic redis unavailable"))
    monkeypatch.setattr(queue_mod, "_redis_client", connect)
    queue_mod.reset_outbox_queue()
    fact, obligation = _stage()
    assert memory._pending_l3_admissions() == [obligation]
    assert pipeline.drain_l3_outbox() == 1
    assert connect.called
    assert get_l3_graph().get_fact(_FID)["claim"] == fact["claim"]
    assert memory._pending_l3_admissions() == []
    assert memory.pending_l3_writes() == []
    assert pipeline.drain_l3_outbox() == 0
    assert profile.read_text(encoding="ascii") == "redis\n"
    with pytest.raises(ConnectionError):
        get_outbox_queue()


@pytest.mark.parametrize("entrypoint", ["ingest", "run"])
def test_both_entrypoints_stage_before_first_graph_write(monkeypatch, entrypoint):
    ingestion = importlib.import_module("core.ingest")
    graph = get_l3_graph()
    real_merge = graph.merge_fact
    seen = []

    def inspect(payload):
        obligations = memory._pending_l3_admissions()
        assert obligations == [memory._l3_admission_identity(
            payload, payload["truth_status"],
        )]
        assert memory.pending_l3_writes() == [payload["fact_id"]]
        seen.append(payload["fact_id"])
        real_merge(payload)

    monkeypatch.setattr(graph, "merge_fact", inspect)
    if entrypoint == "ingest":
        assert ingestion.ingest(
            _CLAIM, fact_id=_FID, source="synthetic", confidence=0.9,
            source_status="EXTERNAL",
        )["accepted"]
    else:
        monkeypatch.setattr(pipeline, "retrieve", lambda *a, **k: [{
            "id": _FID, "text": _CLAIM, "source": "synthetic", "confidence": 0.9,
            "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
            "significance": 0.5, "_score": 0.9, "epistemic_state": "Observed",
            "origin": "memory",
        }])
        assert pipeline.run("synthetic")["answer"] is not None
    assert seen == [_FID]
    assert memory._pending_l3_admissions() == []
    assert memory.pending_l3_writes() == []


@pytest.mark.parametrize("change", ["claim", "source", "restriction", "tombstone", "terminal"])
def test_stale_admission_cannot_project_changed_or_denied_fact(change):
    _, obligation = _stage()
    if change == "claim":
        # Explicit SQL models an incompatible newer persisted version without
        # granting ordinary callers permission to rewrite a Validated claim.
        with memory._db() as conn:
            conn.execute(
                "UPDATE facts SET claim = ?, revision = revision + 1 WHERE fact_id = ?",
                (memory.crypto.encrypt("Different synthetic claim"), _FID),
            )
    elif change == "source":
        assert memory.update_fact(_FID, source="new source")
    elif change == "restriction":
        assert memory.set_restricted(_FID, True)
    elif change == "tombstone":
        memory.write_tombstone(_FID, reason="test", actor="test")
    else:
        memory.transition_esm(_FID, "Deprecated")
    assert not memory._project_l3_admission(get_l3_graph(), obligation)
    assert pipeline.drain_l3_outbox() == 0
    assert get_l3_graph().get_fact(_FID) is None
    assert memory._pending_l3_admissions() == [obligation]


@pytest.mark.parametrize("denial", ["restriction", "tombstone"])
def test_guarded_commit_refuses_denied_admission(denial):
    snapshot = memory.store_fact({
        "fact_id": _FID, "claim": _CLAIM, "source": "synthetic",
    }, return_persisted=True)
    if denial == "restriction":
        assert memory.set_restricted(_FID, True)
        snapshot = memory.get_fact(_FID)
    else:
        memory.write_tombstone(_FID, reason="test", actor="test")
    assert memory.transition_esm_if_unchanged(
        snapshot, "Validated", admission_verdict="VERIFIED",
    ) is None
    assert memory._pending_l3_admissions() == []
    assert memory.pending_l3_writes() == []


def test_invalid_automatic_verdict_rolls_back_promotion():
    with pytest.raises(ValueError, match="invalid automatic"):
        _stage(verdict="CURATOR_OVERRIDE")
    assert memory.get_fact(_FID)["epistemic_state"] == "Observed"
    assert memory._pending_l3_admissions() == []
    assert memory.pending_l3_writes() == []


def test_old_obligation_cannot_consume_or_overwrite_new_projection():
    graph = get_l3_graph()
    _, old = _stage()
    # Synthetic replacement under the same ID; not an erasure/re-ingest policy.
    assert memory.delete_fact_l1(_FID)
    new_fact, new = _stage(claim="A different synthetic admitted claim.")
    assert old != new
    assert not memory._project_l3_admission(graph, old)
    assert not memory._project_l3_secondary(graph, get_outbox_queue(), _FID)
    assert memory._pending_l3_admissions() == [new]
    assert graph.get_fact(_FID) is None
    assert memory._project_l3_admission(graph, new)
    latest = graph.get_fact(_FID)
    assert latest["claim"] == new_fact["claim"]
    assert not memory._project_l3_admission(graph, old)
    assert graph.get_fact(_FID) == latest
    assert memory._pending_l3_admissions() == []
    assert memory.pending_l3_writes() == []


def test_older_admission_does_not_touch_newer_graph_node():
    fact, old = _stage()
    graph = get_l3_graph()
    newer = {**fact, "revision": fact["revision"] + 1, "truth_status": "VERIFIED"}
    graph.merge_fact(newer)
    assert not memory._project_l3_admission(graph, old)
    assert graph.get_fact(_FID) == newer
    assert memory._pending_l3_admissions() == [old]


def test_projection_ack_is_idempotent_and_preserves_newer_queue_entry(monkeypatch):
    fact, obligation = _stage()
    graph = get_l3_graph()
    graph.merge_fact({**fact, "truth_status": "VERIFIED"})
    memory.enqueue_l3_write(_FID)
    with memory._db() as conn:
        conn.execute(
            "UPDATE l3_outbox SET enqueued_at = ? WHERE fact_id = ?",
            ("2099-01-01T00:00:00+00:00", _FID),
        )
    monkeypatch.setattr(graph, "merge_fact", Mock(side_effect=AssertionError("remerge")))
    assert memory._project_l3_admission(graph, obligation)
    assert memory.pending_l3_writes() == [_FID]
    assert memory._pending_l3_admissions() == []
    assert not memory._project_l3_admission(graph, obligation)


def test_secondary_replay_does_not_overwrite_newer_graph():
    fact, obligation = _stage()
    graph = get_l3_graph()
    assert memory._project_l3_admission(graph, obligation)
    newer = {**fact, "revision": fact["revision"] + 1, "truth_status": "VERIFIED"}
    graph.merge_fact(newer)
    memory.enqueue_l3_write(_FID)
    assert pipeline.drain_l3_outbox() == 0
    assert graph.get_fact(_FID) == newer
    assert memory.pending_l3_writes() == [_FID]


def test_secondary_transport_acknowledges_only_current_replay():
    _, obligation = _stage()
    graph = get_l3_graph()
    assert memory._project_l3_admission(graph, obligation)
    external = Mock()
    assert memory._project_l3_secondary(graph, external, _FID)
    external.clear.assert_called_once_with(_FID)


def test_no_local_secondary_entry_is_not_replayed():
    assert memory._pending_l3_admissions() == []
    assert not memory._project_l3_secondary(
        get_l3_graph(), get_outbox_queue(), "missing-local-entry",
    )


@pytest.mark.parametrize("entrypoint", ["ingest", "run"])
def test_restart_recovers_without_redis_notification(child_env, entrypoint):
    child_env["VELANTRIM_QUEUE_BACKEND"] = "auto"
    child_env["CRYSTAL_TEST_REDIS_DOWN"] = "1"
    profile = Path(child_env["VELANTRIM_QUEUE_PROFILE_PATH"])
    profile.write_text("redis\n", encoding="ascii")
    _child(child_env, _WRITER, entrypoint, "after_commit", exit_code=_EXIT)
    _child(child_env, _READER, "after_commit")
    assert profile.read_text(encoding="ascii") == "redis\n"


def test_failed_recovery_keeps_durable_obligation(monkeypatch):
    _, obligation = _stage()
    graph = get_l3_graph()
    with monkeypatch.context() as patch:
        patch.setattr(graph, "merge_fact", Mock(side_effect=RuntimeError("unavailable")))
        assert pipeline.drain_l3_outbox() == 0
    assert memory._pending_l3_admissions() == [obligation]
    assert memory.pending_l3_writes() == [_FID]
    assert pipeline.drain_l3_outbox() == 1
    assert memory._pending_l3_admissions() == []


def test_repeat_ingest_cannot_strand_pending_admission():
    ingestion = importlib.import_module("core.ingest")
    fact, obligation = _stage()
    with pytest.raises(ingestion.IngestError, match="CONCURRENT_STATE_CHANGE"):
        ingestion.ingest(_CLAIM, fact_id=_FID, source="synthetic", confidence=0.9,
                         source_status="EXTERNAL")
    assert memory.get_fact(_FID) == fact
    assert memory._pending_l3_admissions() == [obligation]
    assert pipeline.drain_l3_outbox() == 1


def test_repeated_run_during_backend_failure_does_not_invalidate_intent(monkeypatch):
    fact, obligation = _stage()
    graph = get_l3_graph()
    monkeypatch.setattr(pipeline, "retrieve", lambda *a, **k: [{
        "id": _FID, "text": _CLAIM, "source": "synthetic", "confidence": 0.9,
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
        "significance": 0.5, "_score": 0.9, "epistemic_state": "Observed",
        "origin": "memory",
    }])
    with monkeypatch.context() as patch:
        patch.setattr(graph, "merge_fact", Mock(side_effect=RuntimeError("unavailable")))
        assert pipeline.run("synthetic")["answer"] is None
        assert memory.get_fact(_FID) == fact
        assert memory._pending_l3_admissions() == [obligation]
    assert pipeline.drain_l3_outbox() == 1
    assert memory._pending_l3_admissions() == []