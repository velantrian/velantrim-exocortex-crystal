from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from core import postgresql_migration as pg
from core.storage_common import StorageOperationError


class Result:
    def __init__(self, *, one=None, batches=None):
        self.one = one
        self.batches = list(batches or [])

    def fetchone(self):
        return self.one

    def fetchmany(self, _size):
        return self.batches.pop(0) if self.batches else []


class PreflightConnection:
    def __init__(
        self,
        *,
        tls=True,
        recovery=False,
        create_allowed=True,
        read_only=False,
        schema_exists=False,
        postgres=160012,
        pgvector="0.8.2",
    ):
        self.tls = tls
        self.recovery = recovery
        self.create_allowed = create_allowed
        self.read_only = read_only
        self.schema_exists = schema_exists
        self.postgres = postgres
        self.pgvector = pgvector
        self.queries = []

    def execute(self, query, params=()):
        self.queries.append((query, tuple(params)))
        if "current_database()" in query:
            return Result(one=("crystal", "migration_role", self.postgres, "16.12"))
        if "pg_extension" in query:
            return Result(one=(self.pgvector,))
        if "pg_stat_ssl" in query:
            return Result(one=(self.tls,))
        if "pg_is_in_recovery" in query:
            return Result(one=(self.recovery,))
        if "has_database_privilege" in query:
            return Result(one=(self.create_allowed, self.read_only))
        if "pg_namespace" in query:
            return Result(one=(self.schema_exists,))
        raise AssertionError(query)


class FakeCursor:
    def __init__(self, *, batches=None, rowcount=1, fail_execute=None, fail_many=False):
        self.batches = list(batches or [])
        self.rowcount = rowcount
        self.fail_execute = fail_execute
        self.fail_many = fail_many
        self.executed = []
        self.many = []
        self.closed = False

    def execute(self, query, params=()):
        self.executed.append((query, tuple(params)))
        if self.fail_execute and self.fail_execute in query:
            raise RuntimeError("database details must not leak")
        return self

    def executemany(self, query, rows):
        if self.fail_many:
            raise RuntimeError("secret row failure")
        copied = list(rows)
        self.many.append((query, copied))
        return self

    def fetchmany(self, _size):
        if self.fail_execute == "fetch":
            raise RuntimeError("fetch details")
        return self.batches.pop(0) if self.batches else []

    def close(self):
        self.closed = True


class FakeConnection(PreflightConnection):
    def __init__(self, *, cursor=None, **kwargs):
        super().__init__(**kwargs)
        self._cursor = cursor or FakeCursor()
        self.commits = 0
        self.rollbacks = 0
        self.closed = False

    def execute(self, query, params=()):
        if query == "SET TRANSACTION READ ONLY":
            self.queries.append((query, tuple(params)))
            return Result(one=(True,))
        if "import_control" in query and query.startswith("SELECT operation_id"):
            return Result(one=("op", "VERIFIED", False, "a" * 64, "b" * 64, 2))
        return super().execute(query, params)

    def cursor(self):
        return self._cursor

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1

    def close(self):
        self.closed = True


def verified_bundle(tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    manifest = {
        "schema_version": 1,
        "bundle_type": "velantrim-l3-logical-export",
        "source": {
            "backend": "sqlite",
            "profile_schema_version": 1,
            "profile_sha256": "1" * 64,
            "locator_sha256": "2" * 64,
            "sqlite_schema_version": 1,
            "sqlite_user_version": 7,
        },
        "datasets": {
            name: {"file": filename, "records": 0, "bytes": 0, "sha256": hashlib.sha256(b"").hexdigest()}
            for name, filename in pg.DATASET_FILES.items()
        },
        "vector_dimension": 2,
        "authority": {
            "physical_l3_equals_strict_canon": False,
            "migration_bundle_is_claim_evidence": False,
            "automatic_activation": False,
        },
    }
    (bundle / pg.MIGRATION_MANIFEST).write_text(json.dumps(manifest))
    for filename in pg.DATASET_FILES.values():
        (bundle / filename).write_bytes(b"")
    return bundle, manifest


def test_versions_driver_schema_and_environment(monkeypatch):
    assert pg._version_tuple("3.3.4", "x") == (3, 3, 4)
    assert pg._version_tuple("0.8", "x") == (0, 8, 0)
    for value in (None, "", "broken"):
        with pytest.raises(StorageOperationError):
            pg._version_tuple(value, "x")

    monkeypatch.setattr(pg.importlib, "import_module", lambda _name: SimpleNamespace(__version__="3.3.4"))
    assert pg._load_psycopg().__version__ == "3.3.4"
    monkeypatch.setattr(pg.importlib, "import_module", lambda _name: SimpleNamespace(__version__="3.2.1"))
    with pytest.raises(StorageOperationError, match="unsupported Psycopg"):
        pg._load_psycopg()
    monkeypatch.setattr(pg.importlib, "import_module", lambda _name: (_ for _ in ()).throw(ImportError()))
    with pytest.raises(StorageOperationError, match="optional dependency"):
        pg._load_psycopg()

    assert pg._target_schema("velantrim_inactive_test") == "velantrim_inactive_test"
    assert pg._quoted_schema("velantrim_inactive_test") == '"velantrim_inactive_test"'
    for value in ("public", "velantrim_inactive_UPPER", 1):
        with pytest.raises(StorageOperationError, match="target schema"):
            pg._target_schema(value)

    monkeypatch.setenv("VELANTRIM_TEST_DSN", "postgresql://hidden")
    assert pg._dsn_from_environment("VELANTRIM_TEST_DSN") == "postgresql://hidden"
    with pytest.raises(StorageOperationError, match="name is invalid"):
        pg._dsn_from_environment("bad-name")
    monkeypatch.delenv("VELANTRIM_MISSING", raising=False)
    with pytest.raises(StorageOperationError, match="not set"):
        pg._dsn_from_environment("VELANTRIM_MISSING")


def test_database_failure_connect_and_fetch():
    error = RuntimeError("secret")
    error.sqlstate = "40001"
    assert "40001" in str(pg._database_failure("query", error))
    assert "secret" not in str(pg._database_failure("query", error))
    assert "SQLSTATE" not in str(pg._database_failure("query", RuntimeError()))

    class Driver:
        def connect(self, *args, **kwargs):
            assert kwargs["connect_timeout"] == 10
            return "connected"

    assert pg._connect(Driver(), "secret", autocommit=True) == "connected"

    class BrokenDriver:
        def connect(self, *_args, **_kwargs):
            raise RuntimeError("dsn secret")

    with pytest.raises(StorageOperationError, match="connection failed") as caught:
        pg._connect(BrokenDriver(), "secret", autocommit=False)
    assert "dsn secret" not in str(caught.value)

    assert pg._fetch_one(PreflightConnection(), "SELECT current_database(), current_user, current_setting('server_version_num')::integer, current_setting('server_version')")[:2] == ("crystal", "migration_role")

    class Missing:
        def execute(self, *_args):
            return Result(one=None)

    with pytest.raises(StorageOperationError, match="returned no row"):
        pg._fetch_one(Missing(), "x")

    class Broken:
        def execute(self, *_args):
            raise RuntimeError("secret")

    with pytest.raises(StorageOperationError, match="preflight query failed"):
        pg._fetch_one(Broken(), "x")


def test_preflight_success_and_failures():
    result = pg._preflight(
        PreflightConnection(),
        driver_version="3.3.4",
        target_schema="velantrim_inactive_test",
        require_tls=True,
        allow_insecure_test_connection=False,
        require_absent_schema=True,
        require_writable=True,
    )
    assert result["active"] is False
    assert len(result["target_identity_sha256"]) == 64
    assert pg._target_identity(result) == result["target_identity_sha256"]

    read_result = pg._preflight(
        PreflightConnection(schema_exists=True, create_allowed=False, read_only=True),
        driver_version="3.3.4",
        target_schema="velantrim_inactive_test",
        require_tls=False,
        allow_insecure_test_connection=True,
        require_absent_schema=False,
        require_writable=False,
    )
    assert read_result["tls_policy"] == "explicit-test-plaintext"

    cases = [
        (dict(postgres=150000), "PostgreSQL 16"),
        (dict(pgvector="0.8.1"), "pgvector 0.8.2"),
        (dict(tls=False), "TLS is required"),
        (dict(recovery=True), "in recovery"),
        (dict(create_allowed=False), "not writable"),
        (dict(read_only=True), "not writable"),
        (dict(schema_exists=True), "already exists"),
    ]
    for kwargs, message in cases:
        with pytest.raises(StorageOperationError, match=message):
            pg._preflight(
                PreflightConnection(**kwargs),
                driver_version="3.3.4",
                target_schema="velantrim_inactive_test",
                require_tls=True,
                allow_insecure_test_connection=False,
                require_absent_schema=True,
                require_writable=True,
            )
    with pytest.raises(StorageOperationError, match="test-only"):
        pg._preflight(
            PreflightConnection(tls=False),
            driver_version="3.3.4",
            target_schema="velantrim_inactive_test",
            require_tls=False,
            allow_insecure_test_connection=False,
            require_absent_schema=True,
            require_writable=True,
        )
    with pytest.raises(StorageOperationError, match="does not exist"):
        pg._preflight(
            PreflightConnection(schema_exists=False),
            driver_version="3.3.4",
            target_schema="velantrim_inactive_test",
            require_tls=True,
            allow_insecure_test_connection=False,
            require_absent_schema=False,
            require_writable=False,
        )


def test_receipt_manifest_ids_and_ddl(tmp_path, monkeypatch):
    root = pg._receipt_root(tmp_path / "receipts")
    assert root.is_dir()
    with pytest.raises(StorageOperationError, match="already exists"):
        pg._receipt_root(root)
    monkeypatch.setattr(Path, "mkdir", lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("denied")))
    with pytest.raises(StorageOperationError, match="cannot create"):
        pg._receipt_root(tmp_path / "other")

    bundle, manifest = verified_bundle(tmp_path)
    assert pg._load_manifest(bundle)["vector_dimension"] == 2
    operation = pg._operation_id("a" * 64, "b" * 64, "velantrim_inactive_test")
    assert operation == pg._operation_id("a" * 64, "b" * 64, "velantrim_inactive_test")
    assert len(operation) == 64
    ddl = pg._ddl("velantrim_inactive_test", 2)
    assert any("vector(2)" in statement for statement in ddl)
    assert any("active = false" in statement for statement in ddl)
    assert "vector NOT NULL" in "\n".join(pg._ddl("velantrim_inactive_test", None))
    assert set(manifest["datasets"]) == set(pg.DATASET_FILES)


def test_dataset_sql_rows_flush_and_import(tmp_path, monkeypatch):
    schema = "velantrim_inactive_test"
    for dataset in pg.DATASET_FILES:
        assert schema in pg._dataset_sql(schema, dataset)
    assert pg._row("nodes", {"fact_id": "f", "payload": {"b": 2, "a": 1}}) == ("f", '{"a":1,"b":2}', '{"a":1,"b":2}')
    assert pg._row("vectors", {"fact_id": "f", "vector": [1, 2]}) == ("f", "[1,2]", "[1,2]")
    assert pg._row("edges", {"src": "a", "rel_type": "r", "dst": "b", "props": {}}) == ("a", "r", "b", "{}", "{}")
    assert pg._row("entities", {"entity_id": "e", "kind": None, "label": "E"}) == ("e", None, "E")
    assert pg._row("mentions", {"fact_id": "f", "entity_id": "e", "rel": "M"}) == ("f", "e", "M")
    assert pg._row("meta", {"key": "k", "value": None}) == ("k", None)

    cursor = FakeCursor()
    rows = [(1,), (2,)]
    assert pg._flush(cursor, "SQL", rows) == 2
    assert rows == []
    assert pg._flush(cursor, "SQL", []) == 0
    with pytest.raises(StorageOperationError, match="dataset import failed"):
        pg._flush(FakeCursor(fail_many=True), "SQL", [(1,)])

    records = [{"key": f"k{i}", "value": str(i)} for i in range(3)]
    monkeypatch.setattr(pg, "IMPORT_BATCH_SIZE", 2)

    def feed(_path, _dataset, _metadata):
        consumer = pg._DATASET_CONSUMER.get()
        for record in records:
            consumer(record)
        return [], SimpleNamespace()

    monkeypatch.setattr(pg, "_read_dataset", feed)
    cursor = FakeCursor()
    assert pg._import_dataset(cursor, bundle=tmp_path, target_schema=schema, dataset="meta", metadata={"records": 3}) == 3
    assert [len(batch) for _, batch in cursor.many] == [2, 1]
    with pytest.raises(StorageOperationError, match="count mismatch"):
        pg._import_dataset(FakeCursor(), bundle=tmp_path, target_schema=schema, dataset="meta", metadata={"records": 4})


def test_target_queries_records_and_evidence():
    schema = "velantrim_inactive_test"
    raw_rows = {
        "nodes": ("f", '{"fact_id":"f"}'),
        "vectors": ("f", "[1,2]"),
        "edges": ("f", "R", "g", "{}"),
        "entities": ("e", None, "E"),
        "mentions": ("f", "e", "M"),
        "meta": ("k", "v"),
    }
    for dataset, raw in raw_rows.items():
        assert schema in pg._target_query(schema, dataset)
        assert isinstance(pg._target_record(dataset, raw), dict)

    cursor = FakeCursor(batches=[[raw_rows["meta"]], []])
    evidence = pg._target_dataset_evidence(cursor, target_schema=schema, dataset="meta")
    expected = b'{"key":"k","value":"v"}\n'
    assert evidence == {"records": 1, "bytes": len(expected), "sha256": hashlib.sha256(expected).hexdigest()}
    with pytest.raises(StorageOperationError, match="equivalence query"):
        pg._target_dataset_evidence(FakeCursor(fail_execute="SELECT"), target_schema=schema, dataset="meta")
    with pytest.raises(StorageOperationError, match="equivalence fetch"):
        pg._target_dataset_evidence(FakeCursor(fail_execute="fetch"), target_schema=schema, dataset="meta")


def test_exact_equivalence_and_control(monkeypatch):
    expected = {"records": 1, "bytes": 2, "sha256": "a" * 64}
    monkeypatch.setattr(pg, "_target_dataset_evidence", lambda *_args, **_kwargs: dict(expected))
    cursor = FakeCursor()
    result = pg._exact_equivalence(cursor, target_schema="velantrim_inactive_test", datasets={"meta": expected}, write_evidence=True)
    assert result["meta"] == expected
    assert any("UPDATE" in query for query, _ in cursor.executed)
    cursor = FakeCursor()
    pg._exact_equivalence(cursor, target_schema="velantrim_inactive_test", datasets={"meta": expected}, write_evidence=False)
    assert cursor.executed == []

    monkeypatch.setattr(pg, "_target_dataset_evidence", lambda *_args, **_kwargs: {"records": 0, "bytes": 0, "sha256": "b" * 64})
    with pytest.raises(StorageOperationError, match="exact-state mismatch"):
        pg._exact_equivalence(FakeCursor(), target_schema="velantrim_inactive_test", datasets={"meta": expected}, write_evidence=False)
    monkeypatch.setattr(pg, "_target_dataset_evidence", lambda *_args, **_kwargs: dict(expected))
    with pytest.raises(StorageOperationError, match="evidence write"):
        pg._exact_equivalence(FakeCursor(fail_execute="UPDATE"), target_schema="velantrim_inactive_test", datasets={"meta": expected}, write_evidence=True)

    connection = FakeConnection()
    assert pg._control_row(connection, "velantrim_inactive_test")[1] == "VERIFIED"


def test_failure_receipt(tmp_path):
    root = tmp_path / "receipts"
    root.mkdir()
    pg._write_failure(root, "preflight", StorageOperationError("safe failure"))
    payload = json.loads((root / "failure.json").read_text())
    assert payload["status"] == "FAIL" and payload["active"] is False
    pg._write_failure(root, "other", StorageOperationError("ignored"))
    assert json.loads((root / "failure.json").read_text())["stage"] == "preflight"


def high_level_patches(monkeypatch, tmp_path, *, second_manifest=None):
    bundle, manifest = verified_bundle(tmp_path)
    verified = {"manifest_sha256": "a" * 64, "source": manifest["source"]}
    calls = {"verify": 0}

    def verify(_bundle):
        calls["verify"] += 1
        return second_manifest if calls["verify"] > 1 and second_manifest is not None else verified

    monkeypatch.setattr(pg, "verify_logical_export", verify)
    monkeypatch.setattr(pg, "_load_manifest", lambda _bundle: manifest)
    monkeypatch.setattr(pg, "_load_psycopg", lambda: SimpleNamespace(__version__="3.3.4"))
    monkeypatch.setattr(pg, "_dsn_from_environment", lambda _name: "hidden")
    monkeypatch.setattr(pg, "_preflight", lambda *_args, **_kwargs: {
        "driver": "psycopg", "driver_version": "3.3.4", "database": "db", "role": "role",
        "server_version_num": 160012, "server_version": "16.12", "pgvector_version": "0.8.2",
        "target_schema": "velantrim_inactive_test", "target_schema_exists": kwargs.get("require_absent_schema") is False,
        "tls": True, "tls_policy": "required", "active": False, "target_identity_sha256": "b" * 64,
    })
    monkeypatch.setattr(pg, "_ddl", lambda *_args: ["CREATE SCHEMA"])
    monkeypatch.setattr(pg, "_import_dataset", lambda *_args, **kwargs: kwargs["metadata"]["records"])
    monkeypatch.setattr(pg, "_exact_equivalence", lambda *_args, **_kwargs: {name: {"records": meta["records"], "bytes": meta["bytes"], "sha256": meta["sha256"]} for name, meta in manifest["datasets"].items()})
    return bundle, manifest, calls


def test_high_level_import_success(tmp_path, monkeypatch):
    bundle, manifest, calls = high_level_patches(monkeypatch, tmp_path)
    preflight_connection = FakeConnection()
    import_connection = FakeConnection(cursor=FakeCursor(rowcount=1))
    connections = [preflight_connection, import_connection]
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: connections.pop(0))
    result = pg.import_logical_export_to_postgresql(bundle, tmp_path / "receipts", target_schema="velantrim_inactive_test")
    assert result["status"] == "PASS" and result["active"] is False
    assert import_connection.commits == 1
    assert calls["verify"] == 2
    complete = json.loads((tmp_path / "receipts" / "complete.json").read_text())
    assert set(complete["receipts"]) == set(pg.RECEIPT_FILES)
    assert "hidden" not in json.dumps(complete)
    assert set(manifest["datasets"]) == set(result.get("datasets", manifest["datasets"]))


def test_high_level_import_failures(tmp_path, monkeypatch):
    bundle, _, _ = high_level_patches(monkeypatch, tmp_path)
    connection = FakeConnection(cursor=FakeCursor(rowcount=0))
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: connection)
    with pytest.raises(StorageOperationError, match="control update"):
        pg.import_logical_export_to_postgresql(bundle, tmp_path / "receipts1", target_schema="velantrim_inactive_test")
    assert connection.rollbacks == 1
    assert json.loads((tmp_path / "receipts1" / "failure.json").read_text())["active"] is False

    bundle2, _, _ = high_level_patches(monkeypatch, tmp_path / "two", second_manifest={"manifest_sha256": "c" * 64, "source": {}})
    connection2 = FakeConnection()
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: connection2)
    with pytest.raises(StorageOperationError, match="changed during"):
        pg.import_logical_export_to_postgresql(bundle2, tmp_path / "receipts2", target_schema="velantrim_inactive_test")

    bundle3, _, _ = high_level_patches(monkeypatch, tmp_path / "three")
    connection3 = FakeConnection(cursor=FakeCursor(fail_execute="CREATE SCHEMA"))
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: connection3)
    with pytest.raises(StorageOperationError, match="inactive-import failed"):
        pg.import_logical_export_to_postgresql(bundle3, tmp_path / "receipts3", target_schema="velantrim_inactive_test")

    bundle4, _, _ = high_level_patches(monkeypatch, tmp_path / "four")
    monkeypatch.setattr(pg, "_write_failure", lambda *_args: (_ for _ in ()).throw(StorageOperationError("write failed")))
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: (_ for _ in ()).throw(StorageOperationError("connect failed")))
    with pytest.raises(StorageOperationError, match="connect failed"):
        pg.import_logical_export_to_postgresql(bundle4, tmp_path / "receipts4", target_schema="velantrim_inactive_test")


def test_verify_postgresql_import_success_and_mismatches(tmp_path, monkeypatch):
    bundle, manifest, calls = high_level_patches(monkeypatch, tmp_path)
    connection = FakeConnection()
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: connection)
    monkeypatch.setattr(pg, "_control_row", lambda *_args: ("op", "VERIFIED", False, "a" * 64, "b" * 64, 2))
    result = pg.verify_postgresql_import(bundle, target_schema="velantrim_inactive_test")
    assert result["exact_state_equivalence"] is True and result["active"] is False
    assert connection.rollbacks == 1 and connection.closed is True and calls["verify"] == 2

    variants = [
        (("op", "IMPORTING", False, "a" * 64, "b" * 64, 2), "not a verified inactive"),
        (("op", "VERIFIED", True, "a" * 64, "b" * 64, 2), "not a verified inactive"),
        (("op", "VERIFIED", False, "c" * 64, "b" * 64, 2), "manifest identity"),
        (("op", "VERIFIED", False, "a" * 64, "c" * 64, 2), "target identity"),
        (("op", "VERIFIED", False, "a" * 64, "b" * 64, 3), "vector dimension"),
    ]
    for index, (control, message) in enumerate(variants):
        bundle_i, _, _ = high_level_patches(monkeypatch, tmp_path / f"v{index}")
        connection_i = FakeConnection()
        monkeypatch.setattr(pg, "_connect", lambda *_args, _connection=connection_i, **_kwargs: _connection)
        monkeypatch.setattr(pg, "_control_row", lambda *_args, _control=control: _control)
        with pytest.raises(StorageOperationError, match=message):
            pg.verify_postgresql_import(bundle_i, target_schema="velantrim_inactive_test")

    bundle_bad, _, _ = high_level_patches(monkeypatch, tmp_path / "bad", second_manifest={"manifest_sha256": "c" * 64, "source": {}})
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: FakeConnection())
    monkeypatch.setattr(pg, "_control_row", lambda *_args: ("op", "VERIFIED", False, "a" * 64, "b" * 64, 2))
    with pytest.raises(StorageOperationError, match="changed during PostgreSQL verification"):
        pg.verify_postgresql_import(bundle_bad, target_schema="velantrim_inactive_test")


def test_read_only_setup_failure_and_close_failures(tmp_path, monkeypatch):
    bundle, _, _ = high_level_patches(monkeypatch, tmp_path)

    class BrokenReadOnly(FakeConnection):
        def execute(self, query, params=()):
            if query == "SET TRANSACTION READ ONLY":
                raise RuntimeError("secret")
            return super().execute(query, params)

        def close(self):
            raise RuntimeError("close ignored")

    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: BrokenReadOnly())
    with pytest.raises(StorageOperationError, match="read-only verification setup"):
        pg.verify_postgresql_import(bundle, target_schema="velantrim_inactive_test")
