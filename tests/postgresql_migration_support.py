from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from core import postgresql_migration as pg


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
        host="db.example",
        port=5432,
        database="crystal",
        user="migration_role",
        password="test-password",
    ):
        self.tls = tls
        self.recovery = recovery
        self.create_allowed = create_allowed
        self.read_only = read_only
        self.schema_exists = schema_exists
        self.postgres = postgres
        self.pgvector = pgvector
        self.info = SimpleNamespace(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
        )
        self.queries = []

    def execute(self, query, params=()):
        self.queries.append((query, tuple(params)))
        # This query also contains current_database(); check it first so the
        # fake returns the intended two-column privilege row.
        if "has_database_privilege" in query:
            return Result(one=(self.create_allowed, self.read_only))
        if "current_database()" in query:
            return Result(one=("crystal", "migration_role", self.postgres, "16.12"))
        if "pg_extension" in query:
            return Result(one=(self.pgvector,))
        if "pg_stat_ssl" in query:
            return Result(one=(self.tls,))
        if "pg_is_in_recovery" in query:
            return Result(one=(self.recovery,))
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
    bundle.mkdir(parents=True)
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
            name: {
                "file": filename,
                "records": 0,
                "bytes": 0,
                "sha256": hashlib.sha256(b"").hexdigest(),
            }
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
