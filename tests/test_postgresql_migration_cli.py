from __future__ import annotations

import json

from core import postgresql_migration as pg
from core import storage_ops
from core.storage_common import StorageOperationError


def test_storage_ops_postgresql_commands(tmp_path, monkeypatch, capsys):
    bundle = tmp_path / "bundle"
    receipts = tmp_path / "receipts"
    calls = []

    def import_inactive(bundle_arg, receipts_arg, **kwargs):
        calls.append(("import", bundle_arg, receipts_arg, kwargs))
        return {"status": "PASS", "active": False}

    def verify_inactive(bundle_arg, **kwargs):
        calls.append(("verify", bundle_arg, kwargs))
        return {"status": "PASS", "active": False}

    monkeypatch.setattr(
        storage_ops,
        "import_logical_export_to_postgresql",
        import_inactive,
    )
    monkeypatch.setattr(
        storage_ops,
        "verify_postgresql_import",
        verify_inactive,
    )

    assert storage_ops.main(
        [
            "import-postgresql-inactive",
            str(bundle),
            "--target-schema",
            "velantrim_inactive_test",
            "--receipts",
            str(receipts),
            "--dsn-env",
            "VELANTRIM_TEST_DSN",
        ]
    ) == 0
    assert storage_ops.main(
        [
            "verify-postgresql-inactive",
            str(bundle),
            "--target-schema",
            "velantrim_inactive_test",
            "--allow-insecure-local-test",
        ]
    ) == 0
    assert calls[0] == (
        "import",
        bundle,
        receipts,
        {
            "target_schema": "velantrim_inactive_test",
            "dsn_env": "VELANTRIM_TEST_DSN",
            "require_tls": True,
            "allow_insecure_test_connection": False,
        },
    )
    assert calls[1] == (
        "verify",
        bundle,
        {
            "target_schema": "velantrim_inactive_test",
            "dsn_env": pg.DEFAULT_DSN_ENV,
            "require_tls": False,
            "allow_insecure_test_connection": True,
        },
    )
    outputs = capsys.readouterr().out.strip().splitlines()
    assert len(outputs) == 2
    assert all(json.loads(line)["active"] is False for line in outputs)


def test_storage_ops_postgresql_failure_is_redacted(tmp_path, monkeypatch, capsys):
    def fail(*_args, **_kwargs):
        raise StorageOperationError("safe operator failure")

    monkeypatch.setattr(storage_ops, "verify_postgresql_import", fail)
    assert storage_ops.main(
        [
            "verify-postgresql-inactive",
            str(tmp_path / "bundle"),
            "--target-schema",
            "velantrim_inactive_test",
        ]
    ) == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "schema_version": 1,
        "status": "FAIL",
        "error": "safe operator failure",
    }
