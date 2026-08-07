from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

import pytest

from core.postgresql_migration import (
    import_logical_export_to_postgresql,
    verify_postgresql_import,
)
from core.storage_migration import export_sqlite_logical
from tests.storage_lifecycle_support import _create_db, _write_profile

DSN = os.environ.get("VELANTRIM_POSTGRES_TEST_DSN")
pytestmark = pytest.mark.skipif(not DSN, reason="PostgreSQL integration DSN not configured")


def test_real_postgresql_pgvector_inactive_import(tmp_path: Path, monkeypatch):
    psycopg = pytest.importorskip("psycopg")
    schema = f"velantrim_inactive_it_{uuid.uuid4().hex[:16]}"
    database = tmp_path / "source.db"
    profile = tmp_path / "profile.json"
    bundle = tmp_path / "bundle"
    receipts = tmp_path / "receipts"
    _create_db(database, rows=4)
    _write_profile(profile, database)
    export_sqlite_logical(bundle, profile_path=profile)

    monkeypatch.setenv("VELANTRIM_POSTGRES_DSN", DSN)
    admin = psycopg.connect(DSN, autocommit=True)
    try:
        admin.execute("CREATE EXTENSION IF NOT EXISTS vector")
        result = import_logical_export_to_postgresql(
            bundle,
            receipts,
            target_schema=schema,
            require_tls=False,
            allow_insecure_test_connection=True,
        )
        assert result["status"] == "PASS"
        assert result["active"] is False
        assert result["exact_state_equivalence"] is True

        verification = verify_postgresql_import(
            bundle,
            target_schema=schema,
            require_tls=False,
            allow_insecure_test_connection=True,
        )
        assert verification["status"] == "PASS"
        assert verification["active"] is False
        assert verification["exact_state_equivalence"] is True
        assert verification["datasets"] == {
            "nodes": {"records": 4, "bytes": verification["datasets"]["nodes"]["bytes"], "sha256": verification["datasets"]["nodes"]["sha256"]},
            "vectors": {"records": 4, "bytes": verification["datasets"]["vectors"]["bytes"], "sha256": verification["datasets"]["vectors"]["sha256"]},
            "edges": {"records": 1, "bytes": verification["datasets"]["edges"]["bytes"], "sha256": verification["datasets"]["edges"]["sha256"]},
            "entities": {"records": 1, "bytes": verification["datasets"]["entities"]["bytes"], "sha256": verification["datasets"]["entities"]["sha256"]},
            "mentions": {"records": 1, "bytes": verification["datasets"]["mentions"]["bytes"], "sha256": verification["datasets"]["mentions"]["sha256"]},
            "meta": {"records": 1, "bytes": verification["datasets"]["meta"]["bytes"], "sha256": verification["datasets"]["meta"]["sha256"]},
        }

        control = admin.execute(
            f'SELECT state,active FROM "{schema}".import_control WHERE singleton=1'
        ).fetchone()
        assert control == ("VERIFIED", False)
        indexes = admin.execute(
            "SELECT indexdef FROM pg_indexes WHERE schemaname=%s ORDER BY indexname",
            (schema,),
        ).fetchall()
        assert all("hnsw" not in row[0].lower() and "ivfflat" not in row[0].lower() for row in indexes)

        for name in ("preflight.json", "import.json", "equivalence.json", "complete.json"):
            payload = json.loads((receipts / name).read_text())
            serialized = json.dumps(payload)
            assert "postgresql://" not in serialized
            assert "crystal-password" not in serialized
            assert payload["active"] is False
    finally:
        try:
            admin.execute(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE')
        finally:
            admin.close()
