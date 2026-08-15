import os
from pathlib import Path

import pytest

from core import ingest as ingest_mod
from core import storage_migration as migration
from core.l3_graph import get_l3_graph
from core.pipeline import drain_l3_outbox
from core.queue import get_outbox_queue
from core.storage_common import StorageOperationError


def test_final_file_recheck_detects_same_size_content_change_with_coarse_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "payload"
    path.write_bytes(b"one")
    _, snapshot = migration._read_regular_bytes(path, "payload")

    path.write_bytes(b"two")

    # Model a filesystem where the verifier cannot observe sub-second mtime/ctime
    # changes. Identity and size therefore look unchanged; the final digest must
    # still catch the same-size content replacement.
    real_identity = migration._file_identity

    def coarse_identity(value):
        device, inode, size, _mtime_ns, _ctime_ns = real_identity(value)
        return device, inode, size, 0, 0

    stat_snapshot, digest, max_bytes = snapshot
    monkeypatch.setattr(migration, "_file_identity", coarse_identity)
    coarse_snapshot = (stat_snapshot, digest, max_bytes)

    with pytest.raises(StorageOperationError, match="changed during verification"):
        migration._require_unchanged_file(path, coarse_snapshot, "payload")


def test_final_file_recheck_detects_identity_race_after_initial_lstat(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "payload"
    path.write_bytes(b"one")
    _, snapshot = migration._read_regular_bytes(path, "payload")

    replacement = tmp_path / "replacement"
    replacement.write_bytes(b"two")
    replacement_stat = replacement.stat()

    def open_replacement(_path, _label, *, max_bytes):
        assert max_bytes == snapshot[2]
        return os.open(replacement, os.O_RDONLY), replacement_stat

    monkeypatch.setattr(migration, "_open_regular_fd", open_replacement)

    with pytest.raises(StorageOperationError, match="changed during verification"):
        migration._require_unchanged_file(path, snapshot, "payload")


def test_final_file_recheck_reports_stream_io_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "payload"
    path.write_bytes(b"one")
    _, snapshot = migration._read_regular_bytes(path, "payload")

    def fail_read(_fd, _size):
        raise OSError("simulated reread failure")

    monkeypatch.setattr(migration.os, "read", fail_read)

    with pytest.raises(StorageOperationError, match="cannot recheck payload"):
        migration._require_unchanged_file(path, snapshot, "payload")


def test_direct_ingest_l3_failure_uses_existing_outbox_and_heals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    graph = get_l3_graph()
    real_merge = graph.merge_fact
    fail_once = {"pending": True}

    def merge_with_one_outage(payload):
        if fail_once["pending"]:
            fail_once["pending"] = False
            raise RuntimeError("simulated L3 outage")
        return real_merge(payload)

    monkeypatch.setattr(graph, "merge_fact", merge_with_one_outage)

    result = ingest_mod.ingest("I feel calm during the simulated outage")
    assert result["accepted"] is False
    assert "L3 promotion failed" in result["reason"]

    fact_id = result["fact"]["fact_id"]
    queue = get_outbox_queue()
    assert fact_id in queue.pending()
    assert graph.get_fact(fact_id) is None

    assert drain_l3_outbox(graph) == 1
    assert graph.get_fact(fact_id) is not None
    assert fact_id not in queue.pending()
