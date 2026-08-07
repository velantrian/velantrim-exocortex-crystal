# core/storage_restore.py
# No-clobber restore to inactive SQLite targets.

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.backend_profiles import StorageProfileError, storage_profile_path
from core.storage_backup import verify_backup
from core.storage_common import (
    StorageOperationError,
    _bundle_paths,
    _copy_new_file,
    _json_bytes,
    _load_profile,
    _profile_payload_for_sqlite,
    _resolve_operator_path,
    _sha256_bytes,
    _sha256_file,
    _sqlite_metrics,
    _utc_now,
    _write_new_bytes,
    _write_new_json,
)


def restore_backup(
    bundle_dir: Path | str,
    *,
    target_database: Path | str,
    target_profile: Path | str,
) -> dict[str, Any]:
    """Restore a verified bundle to new, inactive database/profile targets."""

    verified = verify_backup(bundle_dir)
    bundle = _resolve_operator_path(bundle_dir, "backup bundle")
    bundle_db, _, bundle_receipt = _bundle_paths(bundle)
    target_db = _resolve_operator_path(target_database, "restore database target")
    target_profile_file = _resolve_operator_path(
        target_profile, "restore profile target"
    )
    try:
        active_profile = storage_profile_path()
    except StorageProfileError as exc:
        raise StorageOperationError(str(exc)) from exc
    if target_profile_file == active_profile:
        raise StorageOperationError(
            "restore target profile must not be the active storage profile"
        )
    restore_receipt_file = target_profile_file.with_name(
        f"{target_profile_file.name}.restore-receipt.json"
    )
    targets = (target_db, target_profile_file, restore_receipt_file)
    for target in targets:
        if target.exists() or target.is_symlink():
            raise StorageOperationError(f"restore target already exists: {target}")
    if len(set(targets)) != len(targets):
        raise StorageOperationError(
            "restore database, profile and receipt targets must differ"
        )

    created: list[Path] = []
    try:
        _copy_new_file(bundle_db, target_db)
        created.append(target_db)
        restored_metrics = _sqlite_metrics(target_db)
        if restored_metrics["counts"] != verified["sqlite"]["counts"]:
            raise StorageOperationError(
                "restored SQLite table counts differ from backup"
            )
        if _sha256_file(target_db) != verified["receipt"]["database_sha256"]:
            raise StorageOperationError("restored SQLite SHA-256 differs from backup")

        profile = _profile_payload_for_sqlite(target_db)
        profile_bytes = _json_bytes(profile)
        receipt = {
            "schema_version": 1,
            "operation": "sqlite_restore",
            "created_at": _utc_now(),
            "source_bundle": str(bundle),
            "source_receipt_sha256": _sha256_file(bundle_receipt),
            "source_database_sha256": verified["receipt"]["database_sha256"],
            "target_database_path": str(target_db),
            "target_database_sha256": _sha256_file(target_db),
            "target_profile_path": str(target_profile_file),
            "target_profile_sha256": _sha256_bytes(profile_bytes),
            "target_locator_sha256": profile["locator_sha256"],
            "sqlite": restored_metrics,
            "activation": "candidate_profile_only",
        }
        _write_new_json(restore_receipt_file, receipt)
        created.append(restore_receipt_file)
        _write_new_bytes(target_profile_file, profile_bytes)
        created.append(target_profile_file)
        validated = _load_profile(target_profile_file)
        if validated != profile:
            raise StorageOperationError(
                "restored profile validation changed its content"
            )
        if _sha256_file(target_profile_file) != receipt["target_profile_sha256"]:
            raise StorageOperationError("restored profile SHA-256 mismatch")
        return {
            "schema_version": 1,
            "status": "PASS",
            "operation": "restore",
            "target_database": str(target_db),
            "target_profile": str(target_profile_file),
            "restore_receipt": str(restore_receipt_file),
            "receipt": receipt,
        }
    except Exception as exc:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        if isinstance(exc, OSError):
            raise StorageOperationError(f"cannot restore backup: {exc}") from exc
        raise
