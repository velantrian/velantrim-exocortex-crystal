# core/storage_backup.py
# Consistent, self-verifying SQLite backup bundles.

from __future__ import annotations

import os
import shutil
import sqlite3
from pathlib import Path
from typing import Any, Mapping, Optional

from core.backend_profiles import storage_profile_path
from core.storage_common import (
    BUNDLE_COMPLETE,
    BUNDLE_DATABASE,
    BUNDLE_PROFILE,
    BUNDLE_RECEIPT,
    BUNDLE_SCHEMA_VERSION,
    StorageOperationError,
    _bundle_paths,
    _json_bytes,
    _load_profile,
    _read_json_object,
    _require_regular_file,
    _resolve,
    _resolve_operator_path,
    _sha256_bytes,
    _sha256_file,
    _sqlite_locator,
    _sqlite_metrics,
    _utc_now,
    _write_new_bytes,
    _write_new_json,
    _connect_readonly,
)


def _verify_backup_contents(bundle: Path) -> dict[str, Any]:
    database_file, profile_file, receipt_file = _bundle_paths(bundle)
    _require_regular_file(database_file, "bundle database")
    _require_regular_file(profile_file, "bundle profile")
    _require_regular_file(receipt_file, "bundle receipt")

    receipt = _read_json_object(receipt_file, "backup receipt")
    if receipt.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        raise StorageOperationError("unsupported backup receipt schema_version")
    if receipt.get("operation") != "sqlite_backup":
        raise StorageOperationError("backup receipt operation must be 'sqlite_backup'")
    if receipt.get("database_file") != BUNDLE_DATABASE:
        raise StorageOperationError("backup receipt database_file is invalid")
    if receipt.get("profile_file") != BUNDLE_PROFILE:
        raise StorageOperationError("backup receipt profile_file is invalid")

    profile = _load_profile(profile_file)
    source_database = _sqlite_locator(profile)
    if receipt.get("source_database_path") != str(source_database):
        raise StorageOperationError("backup source database path does not match profile")
    if receipt.get("source_locator_sha256") != profile.get("locator_sha256"):
        raise StorageOperationError("backup profile locator does not match receipt")
    if receipt.get("database_sha256") != _sha256_file(database_file):
        raise StorageOperationError("backup database SHA-256 mismatch")
    if receipt.get("database_size") != database_file.stat().st_size:
        raise StorageOperationError("backup database size mismatch")
    if receipt.get("profile_sha256") != _sha256_file(profile_file):
        raise StorageOperationError("backup profile SHA-256 mismatch")

    metrics = _sqlite_metrics(database_file)
    recorded_sqlite = receipt.get("sqlite")
    if not isinstance(recorded_sqlite, Mapping):
        raise StorageOperationError("backup receipt SQLite metrics are invalid")
    if recorded_sqlite.get("counts") != metrics["counts"]:
        raise StorageOperationError("backup SQLite table counts do not match receipt")
    if recorded_sqlite.get("user_version") != metrics["user_version"]:
        raise StorageOperationError("backup SQLite user_version does not match receipt")

    return {
        "schema_version": 1,
        "status": "PASS",
        "operation": "verify",
        "bundle": str(bundle),
        "receipt": receipt,
        "sqlite": metrics,
    }


def create_backup(
    output_dir: Path | str,
    *,
    profile_path: Optional[Path | str] = None,
) -> dict[str, Any]:
    """Create a consistent SQLite bundle and publish completion last."""

    profile_file = (
        _resolve(profile_path) if profile_path is not None else storage_profile_path()
    )
    profile = _load_profile(profile_file)
    source_db = _sqlite_locator(profile)
    _require_regular_file(source_db, "source SQLite storage")

    output = _resolve_operator_path(output_dir, "backup output")
    if output.exists() or output.is_symlink():
        raise StorageOperationError(f"backup output already exists: {output}")
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.mkdir(mode=0o700)
    except OSError as exc:
        raise StorageOperationError(f"cannot create backup bundle: {exc}") from exc

    database_file, profile_copy, receipt_file = _bundle_paths(output)
    complete_file = output / BUNDLE_COMPLETE
    success = False
    try:
        source = _connect_readonly(source_db)
        try:
            try:
                destination = sqlite3.connect(database_file)
            except sqlite3.Error as exc:
                raise StorageOperationError(
                    f"cannot create backup database: {exc}"
                ) from exc
            try:
                source.backup(destination)
                destination.commit()
            except sqlite3.Error as exc:
                raise StorageOperationError(f"SQLite backup failed: {exc}") from exc
            finally:
                destination.close()
        finally:
            source.close()

        os.chmod(database_file, 0o600)
        metrics = _sqlite_metrics(database_file)
        profile_bytes = _json_bytes(profile)
        _write_new_bytes(profile_copy, profile_bytes)
        receipt = {
            "schema_version": BUNDLE_SCHEMA_VERSION,
            "operation": "sqlite_backup",
            "created_at": _utc_now(),
            "source_profile_path": str(profile_file),
            "source_database_path": str(source_db),
            "source_locator_sha256": profile["locator_sha256"],
            "database_file": BUNDLE_DATABASE,
            "database_sha256": _sha256_file(database_file),
            "database_size": database_file.stat().st_size,
            "profile_file": BUNDLE_PROFILE,
            "profile_sha256": _sha256_bytes(profile_bytes),
            "sqlite": metrics,
        }
        _write_new_json(receipt_file, receipt)
        report = _verify_backup_contents(output)
        completion = {
            "schema_version": BUNDLE_SCHEMA_VERSION,
            "operation": "sqlite_backup_complete",
            "completed_at": _utc_now(),
            "receipt_file": BUNDLE_RECEIPT,
            "receipt_sha256": _sha256_file(receipt_file),
        }
        _write_new_json(complete_file, completion)
        report = verify_backup(output)
        success = True
        return {
            "schema_version": 1,
            "status": "PASS",
            "operation": "backup",
            "bundle": str(output),
            "receipt": report["receipt"],
            "completion": report["completion"],
        }
    except OSError as exc:
        raise StorageOperationError(f"cannot create backup bundle: {exc}") from exc
    finally:
        if not success:
            shutil.rmtree(output, ignore_errors=True)


def verify_backup(bundle_dir: Path | str) -> dict[str, Any]:
    """Verify completion, hashes, SQLite integrity and recorded table counts."""

    bundle = _resolve_operator_path(bundle_dir, "backup bundle")
    if not bundle.is_dir():
        raise StorageOperationError(f"backup bundle must be a directory: {bundle}")
    completion_file = bundle / BUNDLE_COMPLETE
    _require_regular_file(completion_file, "bundle completion marker")
    completion = _read_json_object(completion_file, "backup completion marker")
    if completion.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        raise StorageOperationError("unsupported backup completion schema_version")
    if completion.get("operation") != "sqlite_backup_complete":
        raise StorageOperationError(
            "backup completion operation must be 'sqlite_backup_complete'"
        )
    if completion.get("receipt_file") != BUNDLE_RECEIPT:
        raise StorageOperationError("backup completion receipt_file is invalid")
    receipt_file = bundle / BUNDLE_RECEIPT
    _require_regular_file(receipt_file, "bundle receipt")
    if completion.get("receipt_sha256") != _sha256_file(receipt_file):
        raise StorageOperationError("backup completion receipt SHA-256 mismatch")
    report = _verify_backup_contents(bundle)
    report["completion"] = completion
    return report
