from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from core import postgresql_migration as pg
from core.storage_common import StorageOperationError
from tests.postgresql_migration_support import (
    FakeConnection,
    FakeCursor,
    verified_bundle,
)


def high_level_patches(monkeypatch, tmp_path, *, second_manifest=None):
    bundle, manifest = verified_bundle(tmp_path)
    verified = {"manifest_sha256": "a" * 64, "source": manifest["source"]}
    calls = {"verify": 0}

    def verify(_bundle):
        calls["verify"] += 1
        if calls["verify"] > 1 and second_manifest is not None:
            return second_manifest
        return verified

    monkeypatch.setattr(pg, "verify_logical_export", verify)
    monkeypatch.setattr(pg, "_load_manifest", lambda _bundle: manifest)
    monkeypatch.setattr(
        pg,
        "_load_psycopg",
        lambda: SimpleNamespace(__version__="3.3.4"),
    )
    monkeypatch.setattr(pg, "_dsn_from_environment", lambda _name: "hidden")
    monkeypatch.setattr(
        pg,
        "_preflight",
        lambda *_args, **kwargs: {
            "driver": "psycopg",
            "driver_version": "3.3.4",
            "database": "db",
            "role": "role",
            "server_version_num": 160012,
            "server_version": "16.12",
            "pgvector_version": "0.8.2",
            "target_schema": "velantrim_inactive_test",
            "target_schema_exists": kwargs.get("require_absent_schema") is False,
            "tls": True,
            "tls_policy": "required",
            "active": False,
            "target_identity_sha256": "b" * 64,
        },
    )
    monkeypatch.setattr(pg, "_ddl", lambda *_args: ["CREATE SCHEMA"])
    monkeypatch.setattr(
        pg,
        "_import_dataset",
        lambda *_args, **kwargs: kwargs["metadata"]["records"],
    )
    monkeypatch.setattr(
        pg,
        "_exact_equivalence",
        lambda *_args, **_kwargs: {
            name: {
                "records": meta["records"],
                "bytes": meta["bytes"],
                "sha256": meta["sha256"],
            }
            for name, meta in manifest["datasets"].items()
        },
    )
    return bundle, manifest, calls


def test_high_level_import_success(tmp_path, monkeypatch):
    bundle, manifest, calls = high_level_patches(monkeypatch, tmp_path)
    preflight_connection = FakeConnection()
    import_connection = FakeConnection(cursor=FakeCursor(rowcount=1))
    connections = [preflight_connection, import_connection]
    monkeypatch.setattr(
        pg,
        "_connect",
        lambda *_args, **_kwargs: connections.pop(0),
    )
    result = pg.import_logical_export_to_postgresql(
        bundle,
        tmp_path / "receipts",
        target_schema="velantrim_inactive_test",
    )
    assert result["status"] == "PASS" and result["active"] is False
    assert import_connection.commits == 1
    assert calls["verify"] == 2
    complete = json.loads((tmp_path / "receipts" / "complete.json").read_text())
    assert set(complete["receipts"]) == set(pg.RECEIPT_FILES)
    assert "hidden" not in json.dumps(complete)
    assert set(manifest["datasets"]) == set(
        result.get("datasets", manifest["datasets"])
    )


def test_preflight_close_failure_is_redacted(tmp_path, monkeypatch):
    bundle, _, _ = high_level_patches(monkeypatch, tmp_path)

    class BrokenClose(FakeConnection):
        def close(self):
            raise RuntimeError("secret close details")

    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: BrokenClose())
    with pytest.raises(
        StorageOperationError,
        match="preflight connection close failed",
    ) as caught:
        pg.import_logical_export_to_postgresql(
            bundle,
            tmp_path / "receipts-close-failure",
            target_schema="velantrim_inactive_test",
        )
    assert "secret close details" not in str(caught.value)
    failure = json.loads(
        (tmp_path / "receipts-close-failure" / "failure.json").read_text()
    )
    assert failure["status"] == "FAIL"
    assert failure["active"] is False


def test_high_level_import_close_failure_is_ignored_after_success(
    tmp_path,
    monkeypatch,
):
    bundle, _, _ = high_level_patches(monkeypatch, tmp_path)

    class BrokenClose(FakeConnection):
        def close(self):
            raise RuntimeError("close details must not leak")

    connections = [FakeConnection(), BrokenClose()]
    monkeypatch.setattr(
        pg,
        "_connect",
        lambda *_args, **_kwargs: connections.pop(0),
    )
    result = pg.import_logical_export_to_postgresql(
        bundle,
        tmp_path / "receipts",
        target_schema="velantrim_inactive_test",
    )
    assert result["status"] == "PASS"
    assert result["active"] is False


def test_high_level_import_failures(tmp_path, monkeypatch):
    bundle, _, _ = high_level_patches(monkeypatch, tmp_path)
    connection = FakeConnection(cursor=FakeCursor(rowcount=0))
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: connection)
    with pytest.raises(StorageOperationError, match="control update"):
        pg.import_logical_export_to_postgresql(
            bundle,
            tmp_path / "receipts1",
            target_schema="velantrim_inactive_test",
        )
    assert connection.rollbacks == 1
    assert json.loads(
        (tmp_path / "receipts1" / "failure.json").read_text()
    )["active"] is False

    bundle2, _, _ = high_level_patches(
        monkeypatch,
        tmp_path / "two",
        second_manifest={"manifest_sha256": "c" * 64, "source": {}},
    )
    connections2 = [FakeConnection(), FakeConnection()]
    monkeypatch.setattr(
        pg,
        "_connect",
        lambda *_args, **_kwargs: connections2.pop(0),
    )
    with pytest.raises(StorageOperationError, match="changed during"):
        pg.import_logical_export_to_postgresql(
            bundle2,
            tmp_path / "receipts2",
            target_schema="velantrim_inactive_test",
        )

    bundle3, _, _ = high_level_patches(monkeypatch, tmp_path / "three")
    preflight3 = FakeConnection()
    import3 = FakeConnection(cursor=FakeCursor(fail_execute="CREATE SCHEMA"))
    connections3 = [preflight3, import3]
    monkeypatch.setattr(
        pg,
        "_connect",
        lambda *_args, **_kwargs: connections3.pop(0),
    )
    with pytest.raises(StorageOperationError, match="inactive-import failed"):
        pg.import_logical_export_to_postgresql(
            bundle3,
            tmp_path / "receipts3",
            target_schema="velantrim_inactive_test",
        )

    bundle4, _, _ = high_level_patches(monkeypatch, tmp_path / "four")
    monkeypatch.setattr(
        pg,
        "_write_failure",
        lambda *_args: (_ for _ in ()).throw(
            StorageOperationError("write failed")
        ),
    )
    monkeypatch.setattr(
        pg,
        "_connect",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            StorageOperationError("connect failed")
        ),
    )
    with pytest.raises(StorageOperationError, match="connect failed"):
        pg.import_logical_export_to_postgresql(
            bundle4,
            tmp_path / "receipts4",
            target_schema="velantrim_inactive_test",
        )


def test_verify_postgresql_import_success_and_mismatches(tmp_path, monkeypatch):
    bundle, _manifest, calls = high_level_patches(monkeypatch, tmp_path)
    connection = FakeConnection()
    monkeypatch.setattr(pg, "_connect", lambda *_args, **_kwargs: connection)
    monkeypatch.setattr(
        pg,
        "_control_row",
        lambda *_args: (
            "op",
            "VERIFIED",
            False,
            "a" * 64,
            "b" * 64,
            2,
        ),
    )
    result = pg.verify_postgresql_import(
        bundle,
        target_schema="velantrim_inactive_test",
    )
    assert result["exact_state_equivalence"] is True
    assert result["active"] is False
    assert connection.rollbacks == 1
    assert connection.closed is True
    assert calls["verify"] == 2

    variants = [
        (
            ("op", "IMPORTING", False, "a" * 64, "b" * 64, 2),
            "not a verified inactive",
        ),
        (
            ("op", "VERIFIED", True, "a" * 64, "b" * 64, 2),
            "not a verified inactive",
        ),
        (
            ("op", "VERIFIED", False, "c" * 64, "b" * 64, 2),
            "manifest identity",
        ),
        (
            ("op", "VERIFIED", False, "a" * 64, "c" * 64, 2),
            "target identity",
        ),
        (
            ("op", "VERIFIED", False, "a" * 64, "b" * 64, 3),
            "vector dimension",
        ),
    ]
    for index, (control, message) in enumerate(variants):
        bundle_i, _, _ = high_level_patches(
            monkeypatch,
            tmp_path / f"v{index}",
        )
        connection_i = FakeConnection()
        monkeypatch.setattr(
            pg,
            "_connect",
            lambda *_args, _connection=connection_i, **_kwargs: _connection,
        )
        monkeypatch.setattr(
            pg,
            "_control_row",
            lambda *_args, _control=control: _control,
        )
        with pytest.raises(StorageOperationError, match=message):
            pg.verify_postgresql_import(
                bundle_i,
                target_schema="velantrim_inactive_test",
            )

    bundle_bad, _, _ = high_level_patches(
        monkeypatch,
        tmp_path / "bad",
        second_manifest={"manifest_sha256": "c" * 64, "source": {}},
    )
    monkeypatch.setattr(
        pg,
        "_connect",
        lambda *_args, **_kwargs: FakeConnection(),
    )
    monkeypatch.setattr(
        pg,
        "_control_row",
        lambda *_args: (
            "op",
            "VERIFIED",
            False,
            "a" * 64,
            "b" * 64,
            2,
        ),
    )
    with pytest.raises(
        StorageOperationError,
        match="changed during PostgreSQL verification",
    ):
        pg.verify_postgresql_import(
            bundle_bad,
            target_schema="velantrim_inactive_test",
        )


def test_read_only_setup_failure_and_close_failures(tmp_path, monkeypatch):
    bundle, _, _ = high_level_patches(monkeypatch, tmp_path)

    class BrokenReadOnly(FakeConnection):
        def execute(self, query, params=()):
            if query == "SET TRANSACTION READ ONLY":
                raise RuntimeError("secret")
            return super().execute(query, params)

        def close(self):
            raise RuntimeError("close ignored")

    monkeypatch.setattr(
        pg,
        "_connect",
        lambda *_args, **_kwargs: BrokenReadOnly(),
    )
    with pytest.raises(
        StorageOperationError,
        match="read-only verification setup",
    ):
        pg.verify_postgresql_import(
            bundle,
            target_schema="velantrim_inactive_test",
        )
