# core/storage_restore.py
# No-clobber restore to inactive SQLite targets.

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.backend_profiles import (
    StorageProfileError,
    load_storage_profile,
    storage_profile_path,
)
from core.storage_backup import verify_backup
from core.storage_common import (
    StorageOperationError,
    _bundle_paths,
    _copy_new_file,
    _inspection_copy,
    _json_bytes,
    _load_profile,
    _profile_payload_for_sqlite,
    _resolve_operator_path,
    _sha256_bytes,
    _sha256_file,
    _sqlite_metrics,
    _sqlite_sidecars,
    _utc_now,
    _write_new_bytes,
    _write_new_json,
)


def _resolve_active_sqlite_path(path: Path) -> Path:
    try:
        # Non-strict resolution can suppress errors other than a missing file.
        try:
            path.stat()
        except FileNotFoundError:
            pass
        return path.resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        raise StorageOperationError("cannot resolve active SQLite storage path") from exc


def _active_sqlite_paths(locator: str) -> set[Path]:
    # SQLite uses the stored filename directly, relative to the process directory.
    # A file: locator may be interpreted as a URI depending on the SQLite build.
    database = None if locator.startswith("file:") else _resolve_active_sqlite_path(Path(locator))
    if database is None or not database.name:
        raise StorageOperationError("cannot resolve active SQLite storage path from the locator")
    protected = {database}
    for sidecar in _sqlite_sidecars(database):
        protected.update((sidecar, _resolve_active_sqlite_path(sidecar)))
    return protected


def restore_backup(
    bundle_dir: Path | str,
    *,
    target_database: Path | str,
    target_profile: Path | str,
    receipt_path: Path | str | None = None,
) -> dict[str, Any]:
    """Restore a verified bundle to new, inactive database/profile targets."""

    bundle = _resolve_operator_path(bundle_dir, "backup bundle")
    bundle_db, _, _ = _bundle_paths(bundle)
    target_db = _resolve_operator_path(target_database, "restore database target")
    target_profile_file = _resolve_operator_path(
        target_profile, "restore profile target"
    )
    try:
        active_profile = storage_profile_path()
        current_profile = load_storage_profile(active_profile)
    except StorageProfileError as exc:
        raise StorageOperationError(str(exc)) from exc
    except (OSError, RuntimeError, ValueError) as exc:
        raise StorageOperationError(f"cannot inspect active storage profile: {exc}") from exc
    if receipt_path is None:
        restore_receipt_file = target_profile_file.with_name(
            f"{target_profile_file.name}.restore-receipt.json"
        )
    else:
        restore_receipt_file = _resolve_operator_path(
            receipt_path, "restore receipt target"
        )
    targets = (target_db, target_profile_file, restore_receipt_file)
    if active_profile in targets:
        raise StorageOperationError("restore target must not be the active storage profile")
    if current_profile is not None and current_profile["backend"] == "sqlite":
        protected = _active_sqlite_paths(current_profile["configuration"]["path"])
        if protected.intersection(targets):
            raise StorageOperationError("restore target must not be an active SQLite storage path")
    for target in targets:
        if target.exists() or target.is_symlink():
            raise StorageOperationError(f"restore target already exists: {target}")
        if target.is_relative_to(bundle):
            raise StorageOperationError(f"restore target is inside the source backup bundle: {target}")
    if len(set(targets)) != len(targets):
        raise StorageOperationError(
            "restore database, profile and receipt targets must differ"
        )
    for sidecar in _sqlite_sidecars(target_db):
        if sidecar in targets or sidecar.exists() or sidecar.is_symlink():
            raise StorageOperationError(f"restore database sidecar conflicts with an output: {sidecar}")

    verified = verify_backup(bundle)
    created: list[Path] = []
    try:
        _copy_new_file(bundle_db, target_db)
        created.append(target_db)
        with _inspection_copy(target_db, bundle=bundle) as snapshot:
            restored_metrics = _sqlite_metrics(snapshot)
        if restored_metrics["counts"] != verified["sqlite"]["counts"]:
            raise StorageOperationError(
                "restored SQLite table counts differ from backup"
            )
        database_sha256 = _sha256_file(target_db)
        if database_sha256 != verified["receipt"]["database_sha256"]:
            raise StorageOperationError("restored SQLite SHA-256 differs from backup")

        profile = _profile_payload_for_sqlite(target_db)
        profile_bytes = _json_bytes(profile)
        receipt = {
            "schema_version": 1,
            "operation": "sqlite_restore",
            "created_at": _utc_now(),
            "source_bundle": str(bundle),
            "source_receipt_sha256": verified["completion"]["receipt_sha256"],
            "source_database_sha256": verified["receipt"]["database_sha256"],
            "target_database_path": str(target_db),
            "target_database_sha256": database_sha256,
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
