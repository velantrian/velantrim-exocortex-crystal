from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from core import storage_migration as m
from core.storage_common import StorageOperationError


def _profile_payload(db: Path) -> dict:
    configuration = {"path": str(db.resolve())}
    canonical = json.dumps(
        {"backend": "sqlite", "configuration": configuration},
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "schema_version": 1,
        "profile": "l3",
        "backend": "sqlite",
        "durable": True,
        "configuration": configuration,
        "locator_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
    }


def _make_store(tmp_path: Path, count: int = 4) -> tuple[Path, Path]:
    db = tmp_path / "l3.db"
    profile = tmp_path / "profile.json"
    connection = sqlite3.connect(db)
    connection.executescript(
        """
        CREATE TABLE nodes(fact_id TEXT PRIMARY KEY,data TEXT NOT NULL);
        CREATE TABLE vectors(fact_id TEXT PRIMARY KEY,vec TEXT NOT NULL);
        CREATE TABLE edges(
            src TEXT NOT NULL,rel_type TEXT NOT NULL,dst TEXT NOT NULL,
            props TEXT NOT NULL DEFAULT '{}',UNIQUE(src,rel_type,dst,props)
        );
        CREATE TABLE entities(entity_id TEXT PRIMARY KEY,kind TEXT,label TEXT);
        CREATE TABLE mentions(
            fact_id TEXT NOT NULL,entity_id TEXT NOT NULL,rel TEXT NOT NULL,
            UNIQUE(fact_id,entity_id,rel)
        );
        CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);
        """
    )
    for index in range(count):
        fact_id = f"f{index:04d}"
        connection.execute(
            "INSERT INTO nodes VALUES (?,?)",
            (fact_id, json.dumps({"fact_id": fact_id, "claim": fact_id})),
        )
    connection.execute("INSERT INTO vectors VALUES (?,?)", ("f0000", "[1,2]"))
    connection.execute(
        "INSERT INTO edges VALUES (?,?,?,?)",
        ("f0000", "LINK", "f0001", '{"z":1,"a":2}'),
    )
    connection.execute("INSERT INTO entities VALUES (?,?,?)", ("e", "kind", "E"))
    connection.execute(
        "INSERT INTO mentions VALUES (?,?,?)", ("f0000", "e", "M")
    )
    connection.execute("INSERT INTO meta VALUES (?,?)", ("k", "v"))
    connection.commit()
    connection.close()
    profile.write_text(json.dumps(_profile_payload(db), sort_keys=True) + "\n")
    return profile, db


class _FakeCursor:
    def __init__(self, batches):
        self.batches = list(batches)
        self.sizes = []

    def fetchmany(self, size):
        self.sizes.append(size)
        return self.batches.pop(0) if self.batches else []


def test_cursor_records_are_batched():
    cursor = _FakeCursor(
        [
            [{"key": "a", "value": None}],
            [{"key": "b", "value": None}],
        ]
    )
    assert list(m._cursor_records(cursor, "meta")) == [
        {"key": "a", "value": None},
        {"key": "b", "value": None},
    ]
    assert cursor.sizes == [m.MIGRATION_BATCH_SIZE] * 3


def test_edge_spool_orders_and_rejects_canonical_duplicates():
    cursor = _FakeCursor(
        [
            [
                {
                    "src": "b",
                    "rel_type": "r",
                    "dst": "c",
                    "props": '{"z":1,"a":2}',
                },
                {"src": "a", "rel_type": "r", "dst": "c", "props": "{}"},
            ]
        ]
    )
    records = list(m._edge_spool_records(cursor))
    assert [record["src"] for record in records] == ["a", "b"]
    assert records[1]["props"] == {"a": 2, "z": 1}

    duplicate = _FakeCursor(
        [
            [
                {
                    "src": "a",
                    "rel_type": "r",
                    "dst": "b",
                    "props": '{"a":1,"b":2}',
                },
                {
                    "src": "a",
                    "rel_type": "r",
                    "dst": "b",
                    "props": '{"b":2,"a":1}',
                },
            ]
        ]
    )
    with pytest.raises(StorageOperationError, match="duplicate canonical"):
        list(m._edge_spool_records(duplicate))


def test_edge_spool_wraps_sqlite_errors():
    class Broken:
        def fetchmany(self, _size):
            raise sqlite3.OperationalError("broken")

    with pytest.raises(StorageOperationError, match="cannot sort SQLite edges"):
        list(m._edge_spool_records(Broken()))


def test_disk_preflight_failures(tmp_path, monkeypatch):
    monkeypatch.setattr(
        m.shutil,
        "disk_usage",
        lambda _path: SimpleNamespace(free=0),
    )
    with pytest.raises(StorageOperationError, match="insufficient temporary disk"):
        m._require_free_disk(tmp_path, 1, "test")

    monkeypatch.setattr(
        m.shutil,
        "disk_usage",
        lambda _path: (_ for _ in ()).throw(OSError("denied")),
    )
    with pytest.raises(StorageOperationError, match="cannot inspect temporary disk"):
        m._require_free_disk(tmp_path, 1, "test")


def test_verify_streams_datasets_and_uses_consumer(tmp_path, monkeypatch):
    profile, _ = _make_store(tmp_path)
    bundle = tmp_path / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)

    original = m._read_regular_bytes

    def controls_only(path, label, **kwargs):
        assert Path(path).suffix != ".jsonl"
        return original(path, label, **kwargs)

    monkeypatch.setattr(m, "_read_regular_bytes", controls_only)
    result = m.verify_logical_export(bundle)
    assert result["resource_mode"] == "bounded-streaming"

    seen = []
    token = m._DATASET_CONSUMER.set(seen.append)
    try:
        records, _ = m._read_dataset(
            bundle / "nodes.jsonl",
            "nodes",
            json.loads((bundle / m.MIGRATION_MANIFEST).read_text())["datasets"][
                "nodes"
            ],
        )
    finally:
        m._DATASET_CONSUMER.reset(token)
    assert records == []
    assert len(seen) == 4


def test_dataset_stream_detects_descriptor_mutation(tmp_path, monkeypatch):
    profile, _ = _make_store(tmp_path)
    bundle = tmp_path / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)
    metadata = json.loads((bundle / m.MIGRATION_MANIFEST).read_text())["datasets"][
        "nodes"
    ]
    real_fstat = m.os.fstat
    calls = {"count": 0}

    def changed(fd):
        value = real_fstat(fd)
        calls["count"] += 1
        if calls["count"] == 2:
            fields = list(value)
            fields[8] += 1
            return os.stat_result(fields)
        return value

    monkeypatch.setattr(m.os, "fstat", changed)
    with pytest.raises(StorageOperationError, match="changed while it was read"):
        m._read_dataset(bundle / "nodes.jsonl", "nodes", metadata)


def test_verification_index_sqlite_failure_is_wrapped(tmp_path, monkeypatch):
    profile, _ = _make_store(tmp_path)
    bundle = tmp_path / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)

    class Temporary:
        def cleanup(self):
            pass

    class BrokenIndex:
        def execute(self, _query, _params=()):
            raise sqlite3.OperationalError("broken")

        def close(self):
            pass

    monkeypatch.setattr(
        m,
        "_verification_index",
        lambda _parent: (Temporary(), BrokenIndex()),
    )
    with pytest.raises(StorageOperationError, match="verification index"):
        m.verify_logical_export(bundle)


def test_missing_examples_handles_scalar_and_tuple():
    class Result:
        def __init__(self, rows):
            self.rows = rows

        def fetchmany(self, size):
            return self.rows[:size]

    class Connection:
        def __init__(self, rows):
            self.rows = rows

        def execute(self, _query):
            return Result(self.rows)

    assert m._missing_examples(Connection([("a",)]), "x") == ["a"]
    assert m._missing_examples(Connection([("a", "b")]), "x") == [("a", "b")]



def test_dataset_hash_pass_resource_and_io_failures(tmp_path, monkeypatch):
    profile, _ = _make_store(tmp_path)
    bundle = tmp_path / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)
    metadata = json.loads((bundle / m.MIGRATION_MANIFEST).read_text())["datasets"][
        "nodes"
    ]

    monkeypatch.setattr(m, "MAX_DATASET_BYTES", metadata["bytes"])

    real_read = m.os.read
    calls = {"count": 0}

    def oversized(fd, size):
        calls["count"] += 1
        if calls["count"] == 1:
            return b"x" * (m.MAX_DATASET_BYTES + 1)
        return b""

    monkeypatch.setattr(m.os, "read", oversized)
    with pytest.raises(StorageOperationError, match="exceeds byte resource limits"):
        m._read_dataset(bundle / "nodes.jsonl", "nodes", metadata)

    monkeypatch.setattr(m.os, "read", lambda _fd, _size: b"")
    with pytest.raises(StorageOperationError, match="byte-size mismatch"):
        m._read_dataset(bundle / "nodes.jsonl", "nodes", metadata)

    monkeypatch.setattr(
        m.os,
        "read",
        lambda _fd, _size: (_ for _ in ()).throw(OSError("read failed")),
    )
    with pytest.raises(StorageOperationError, match="cannot read nodes"):
        m._read_dataset(bundle / "nodes.jsonl", "nodes", metadata)

    monkeypatch.setattr(m.os, "read", real_read)


def test_dataset_final_descriptor_mutation_is_detected(tmp_path, monkeypatch):
    profile, _ = _make_store(tmp_path)
    bundle = tmp_path / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)
    metadata = json.loads((bundle / m.MIGRATION_MANIFEST).read_text())["datasets"][
        "nodes"
    ]
    real_fstat = m.os.fstat
    calls = {"count": 0}

    def changed(fd):
        value = real_fstat(fd)
        calls["count"] += 1
        if calls["count"] == 3:
            fields = list(value)
            fields[8] += 1
            return os.stat_result(fields)
        return value

    monkeypatch.setattr(m.os, "fstat", changed)
    with pytest.raises(StorageOperationError, match="changed while it was read"):
        m._read_dataset(bundle / "nodes.jsonl", "nodes", metadata)


def test_verification_index_factory_cleans_up_before_connection(tmp_path, monkeypatch):
    root = tmp_path / "temp-before"
    root.mkdir()
    cleaned = {"value": False}

    class Temporary:
        name = str(root)

        def cleanup(self):
            cleaned["value"] = True

    monkeypatch.setattr(m.tempfile, "TemporaryDirectory", lambda **_kwargs: Temporary())
    monkeypatch.setattr(
        m.sqlite3,
        "connect",
        lambda _path: (_ for _ in ()).throw(sqlite3.OperationalError("connect failed")),
    )
    with pytest.raises(
        StorageOperationError, match="cannot create migration verification index"
    ):
        m._verification_index(tmp_path)
    assert cleaned["value"] is True


def test_verification_index_factory_closes_connection_and_cleans_up(
    tmp_path, monkeypatch
):
    root = tmp_path / "temp-after"
    root.mkdir()
    state = {"cleaned": False, "closed": False}

    class Temporary:
        name = str(root)

        def cleanup(self):
            state["cleaned"] = True

    class Connection:
        def executescript(self, _script):
            raise sqlite3.OperationalError("schema failed")

        def close(self):
            state["closed"] = True

    monkeypatch.setattr(m.tempfile, "TemporaryDirectory", lambda **_kwargs: Temporary())
    monkeypatch.setattr(m.sqlite3, "connect", lambda _path: Connection())
    monkeypatch.setattr(m.os, "chmod", lambda _path, _mode: None)
    with pytest.raises(
        StorageOperationError, match="cannot create migration verification index"
    ):
        m._verification_index(tmp_path)
    assert state == {"cleaned": True, "closed": True}
