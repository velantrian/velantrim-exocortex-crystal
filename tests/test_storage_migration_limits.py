from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path

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


def _store(tmp_path: Path) -> tuple[Path, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
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
    for fact_id in ("a", "b"):
        connection.execute(
            "INSERT INTO nodes VALUES (?,?)",
            (fact_id, json.dumps({"fact_id": fact_id, "claim": fact_id})),
        )
    connection.commit()
    connection.close()
    profile.write_text(json.dumps(_profile_payload(db), sort_keys=True) + "\n")
    return profile, db


def _bundle(tmp_path: Path) -> Path:
    profile, _ = _store(tmp_path)
    bundle = tmp_path / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)
    return bundle


def _load(path: Path):
    return json.loads(path.read_text())


def _dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _refresh(bundle: Path) -> None:
    complete = _load(bundle / m.MIGRATION_COMPLETE)
    complete["manifest_sha256"] = m._sha256_file(bundle / m.MIGRATION_MANIFEST)
    _dump(bundle / m.MIGRATION_COMPLETE, complete)


def test_export_rejects_source_and_record_count_over_limits(tmp_path, monkeypatch):
    profile, db = _store(tmp_path / "source")
    monkeypatch.setattr(m, "MAX_SOURCE_SQLITE_BYTES", db.stat().st_size - 1)
    with pytest.raises(StorageOperationError, match="local-first export limit"):
        m.export_sqlite_logical(tmp_path / "source" / "bundle", profile_path=profile)

    monkeypatch.setattr(m, "MAX_SOURCE_SQLITE_BYTES", 64 * 1024 * 1024)
    profile, _ = _store(tmp_path / "count")
    monkeypatch.setattr(m, "MAX_RECORDS_PER_DATASET", 1)
    with pytest.raises(StorageOperationError, match="record local-first export limit"):
        m.export_sqlite_logical(tmp_path / "count" / "bundle", profile_path=profile)


def test_profile_and_control_file_limits(tmp_path, monkeypatch):
    profile, _ = _store(tmp_path / "profile")
    monkeypatch.setattr(m, "MAX_CONTROL_FILE_BYTES", 1)
    with pytest.raises(StorageOperationError, match="control-file resource limit"):
        m.export_sqlite_logical(tmp_path / "profile" / "bundle", profile_path=profile)

    path = tmp_path / "payload"
    path.write_bytes(b"xx")
    with pytest.raises(StorageOperationError, match="resource limit"):
        m._read_regular_bytes(path, "payload", max_bytes=1)


def test_safe_reader_rechecks_open_size_and_growth(tmp_path, monkeypatch):
    path = tmp_path / "payload"
    path.write_bytes(b"x")
    real_fstat = m.os.fstat
    calls = {"count": 0}

    def larger_after_open(fd):
        value = real_fstat(fd)
        calls["count"] += 1
        if calls["count"] == 1:
            values = list(value)
            values[6] = 2
            return os.stat_result(values)
        return value

    monkeypatch.setattr(m.os, "fstat", larger_after_open)
    with pytest.raises(StorageOperationError, match="resource limit"):
        m._read_regular_bytes(path, "payload", max_bytes=1)

    monkeypatch.setattr(m.os, "fstat", real_fstat)
    monkeypatch.setattr(m.os, "read", lambda _fd, _size: b"xx")
    with pytest.raises(StorageOperationError, match="resource limit"):
        m._read_regular_bytes(path, "payload", max_bytes=1)


def test_write_dataset_enforces_limits(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "MAX_RECORD_BYTES", 4)
    with pytest.raises(StorageOperationError, match="record exceeds"):
        m._write_dataset(tmp_path / "record", [{"key": "long", "value": None}])

    monkeypatch.setattr(m, "MAX_RECORD_BYTES", 1024)
    monkeypatch.setattr(m, "MAX_RECORDS_PER_DATASET", 1)
    with pytest.raises(StorageOperationError, match="record-count"):
        m._write_dataset(
            tmp_path / "count",
            [{"key": "a", "value": None}, {"key": "b", "value": None}],
        )

    monkeypatch.setattr(m, "MAX_RECORDS_PER_DATASET", 10)
    monkeypatch.setattr(m, "MAX_DATASET_BYTES", 1)
    with pytest.raises(StorageOperationError, match="byte limit"):
        m._write_dataset(tmp_path / "bytes", [{"key": "a", "value": None}])


def test_export_and_verify_enforce_aggregate_and_manifest_limits(
    tmp_path, monkeypatch
):
    profile, _ = _store(tmp_path / "aggregate-export")
    monkeypatch.setattr(m, "MAX_BUNDLE_DATA_BYTES", 1)
    with pytest.raises(StorageOperationError, match="aggregate data"):
        m.export_sqlite_logical(
            tmp_path / "aggregate-export" / "bundle", profile_path=profile
        )

    monkeypatch.setattr(m, "MAX_BUNDLE_DATA_BYTES", 384 * 1024 * 1024)
    bundle = _bundle(tmp_path / "verify-records")
    monkeypatch.setattr(m, "MAX_RECORDS_PER_DATASET", 1)
    with pytest.raises(StorageOperationError, match="record resource limits"):
        m.verify_logical_export(bundle)

    monkeypatch.setattr(m, "MAX_RECORDS_PER_DATASET", 200_000)
    bundle = _bundle(tmp_path / "verify-bytes")
    manifest = _load(bundle / m.MIGRATION_MANIFEST)
    manifest["datasets"]["nodes"]["bytes"] = m.MAX_DATASET_BYTES + 1
    _dump(bundle / m.MIGRATION_MANIFEST, manifest)
    _refresh(bundle)
    with pytest.raises(StorageOperationError, match="byte resource limits"):
        m.verify_logical_export(bundle)

    bundle = _bundle(tmp_path / "verify-aggregate")
    monkeypatch.setattr(m, "MAX_BUNDLE_DATA_BYTES", 1)
    with pytest.raises(StorageOperationError, match="aggregate resource limits"):
        m.verify_logical_export(bundle)


def test_read_dataset_rejects_oversized_record(tmp_path, monkeypatch):
    bundle = _bundle(tmp_path)
    monkeypatch.setattr(m, "MAX_RECORD_BYTES", 1)
    with pytest.raises(StorageOperationError, match="record-size resource limit"):
        m.verify_logical_export(bundle)


def test_read_dataset_enforces_record_count_during_parse(tmp_path, monkeypatch):
    bundle = _bundle(tmp_path)
    manifest = _load(bundle / m.MIGRATION_MANIFEST)
    monkeypatch.setattr(m, "MAX_RECORDS_PER_DATASET", 1)
    with pytest.raises(StorageOperationError, match="record-count resource limit"):
        m._read_dataset(
            bundle / m.DATASET_FILES["nodes"],
            "nodes",
            manifest["datasets"]["nodes"],
        )


def test_dataset_count_reports_query_failure():
    class Bad:
        def execute(self, _query):
            raise sqlite3.OperationalError("bad")

    with pytest.raises(StorageOperationError, match="cannot count SQLite dataset"):
        m._dataset_count(Bad(), "nodes")
