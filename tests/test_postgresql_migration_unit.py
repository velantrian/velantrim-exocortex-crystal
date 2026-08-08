from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from core import postgresql_migration as pg
from core.storage_common import StorageOperationError
from tests.postgresql_migration_support import (
    FakeConnection,
    FakeCursor,
    PreflightConnection,
    Result,
    verified_bundle,
)


def test_versions_driver_schema_and_environment(monkeypatch):
    assert pg._version_tuple("3.3.4", "x") == (3, 3, 4)
    assert pg._version_tuple("0.8", "x") == (0, 8, 0)
    for value in (None, "", "broken"):
        with pytest.raises(StorageOperationError):
            pg._version_tuple(value, "x")

    monkeypatch.setattr(
        pg.importlib,
        "import_module",
        lambda _name: SimpleNamespace(__version__="3.3.4"),
    )
    assert pg._load_psycopg().__version__ == "3.3.4"
    monkeypatch.setattr(
        pg.importlib,
        "import_module",
        lambda _name: SimpleNamespace(__version__="3.2.1"),
    )
    with pytest.raises(StorageOperationError, match="unsupported Psycopg"):
        pg._load_psycopg()
    monkeypatch.setattr(
        pg.importlib,
        "import_module",
        lambda _name: (_ for _ in ()).throw(ImportError()),
    )
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

    query = (
        "SELECT current_database(), current_user, "
        "current_setting('server_version_num')::integer, "
        "current_setting('server_version')"
    )
    assert pg._fetch_one(PreflightConnection(), query)[:2] == (
        "crystal",
        "migration_role",
    )

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

    bundle, manifest = verified_bundle(tmp_path)
    with monkeypatch.context() as patch:
        patch.setattr(
            Path,
            "mkdir",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("denied")),
        )
        with pytest.raises(StorageOperationError, match="cannot create"):
            pg._receipt_root(tmp_path / "other")

    assert pg._load_manifest(bundle)["vector_dimension"] == 2
    operation = pg._operation_id(
        "a" * 64,
        "b" * 64,
        "velantrim_inactive_test",
    )
    assert operation == pg._operation_id(
        "a" * 64,
        "b" * 64,
        "velantrim_inactive_test",
    )
    assert len(operation) == 64
    ddl = pg._ddl("velantrim_inactive_test", 2)
    assert any("vector(2)" in statement for statement in ddl)
    assert any("active = false" in statement for statement in ddl)
    assert "vector NOT NULL" in "\n".join(
        pg._ddl("velantrim_inactive_test", None)
    )
    assert set(manifest["datasets"]) == set(pg.DATASET_FILES)


def test_dataset_sql_rows_flush_and_import(tmp_path, monkeypatch):
    schema = "velantrim_inactive_test"
    for dataset in pg.DATASET_FILES:
        assert schema in pg._dataset_sql(schema, dataset)
    assert pg._row(
        "nodes",
        {"fact_id": "f", "payload": {"b": 2, "a": 1}},
    ) == ("f", '{"a":1,"b":2}', '{"a":1,"b":2}')
    assert pg._row(
        "vectors",
        {"fact_id": "f", "vector": [1, 2]},
    ) == ("f", "[1,2]", "[1,2]")
    assert pg._row(
        "edges",
        {"src": "a", "rel_type": "r", "dst": "b", "props": {}},
    ) == ("a", "r", "b", "{}", "{}")
    assert pg._row(
        "entities",
        {"entity_id": "e", "kind": None, "label": "E"},
    ) == ("e", None, "E")
    assert pg._row(
        "mentions",
        {"fact_id": "f", "entity_id": "e", "rel": "M"},
    ) == ("f", "e", "M")
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
    assert pg._import_dataset(
        cursor,
        bundle=tmp_path,
        target_schema=schema,
        dataset="meta",
        metadata={"records": 3},
    ) == 3
    assert [len(batch) for _, batch in cursor.many] == [2, 1]
    with pytest.raises(StorageOperationError, match="count mismatch"):
        pg._import_dataset(
            FakeCursor(),
            bundle=tmp_path,
            target_schema=schema,
            dataset="meta",
            metadata={"records": 4},
        )


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
    evidence = pg._target_dataset_evidence(
        cursor,
        target_schema=schema,
        dataset="meta",
    )
    expected = b'{"key":"k","value":"v"}\n'
    assert evidence == {
        "records": 1,
        "bytes": len(expected),
        "sha256": hashlib.sha256(expected).hexdigest(),
    }
    with pytest.raises(StorageOperationError, match="equivalence query"):
        pg._target_dataset_evidence(
            FakeCursor(fail_execute="SELECT"),
            target_schema=schema,
            dataset="meta",
        )
    with pytest.raises(StorageOperationError, match="equivalence fetch"):
        pg._target_dataset_evidence(
            FakeCursor(fail_execute="fetch"),
            target_schema=schema,
            dataset="meta",
        )


def test_exact_equivalence_and_control(monkeypatch):
    expected = {"records": 1, "bytes": 2, "sha256": "a" * 64}
    monkeypatch.setattr(
        pg,
        "_target_dataset_evidence",
        lambda *_args, **_kwargs: dict(expected),
    )
    cursor = FakeCursor()
    result = pg._exact_equivalence(
        cursor,
        target_schema="velantrim_inactive_test",
        datasets={"meta": expected},
        write_evidence=True,
    )
    assert result["meta"] == expected
    assert any("UPDATE" in query for query, _ in cursor.executed)
    cursor = FakeCursor()
    pg._exact_equivalence(
        cursor,
        target_schema="velantrim_inactive_test",
        datasets={"meta": expected},
        write_evidence=False,
    )
    assert cursor.executed == []

    monkeypatch.setattr(
        pg,
        "_target_dataset_evidence",
        lambda *_args, **_kwargs: {
            "records": 0,
            "bytes": 0,
            "sha256": "b" * 64,
        },
    )
    with pytest.raises(StorageOperationError, match="exact-state mismatch"):
        pg._exact_equivalence(
            FakeCursor(),
            target_schema="velantrim_inactive_test",
            datasets={"meta": expected},
            write_evidence=False,
        )
    monkeypatch.setattr(
        pg,
        "_target_dataset_evidence",
        lambda *_args, **_kwargs: dict(expected),
    )
    with pytest.raises(StorageOperationError, match="evidence write"):
        pg._exact_equivalence(
            FakeCursor(fail_execute="UPDATE"),
            target_schema="velantrim_inactive_test",
            datasets={"meta": expected},
            write_evidence=True,
        )

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
