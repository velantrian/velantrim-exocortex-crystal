# core/storage_lock.py
# Read-only lock inspection and guarded explicit stale-lock recovery.

from __future__ import annotations

import hashlib
import os
import stat
import time
from pathlib import Path
from typing import Any, Optional

from core.backend_profiles import storage_profile_path
from core.storage_common import (
    StorageOperationError,
    _fsync_directory,
    _load_profile,
    _resolve,
    _sqlite_locator,
)


def _lock_snapshot(lock_file: Path) -> Optional[dict[str, Any]]:
    """Read one lock identity without following a symlink replacement."""

    try:
        before = lock_file.lstat()
    except FileNotFoundError:
        return None
    regular = stat.S_ISREG(before.st_mode)
    base = {
        "present": True,
        "regular_file": regular,
        "size": before.st_size,
        "mtime_ns": before.st_mtime_ns,
        "age_seconds": max(0.0, time.time() - before.st_mtime),
        "device": before.st_dev,
        "inode": before.st_ino,
        "sha256": None,
    }
    if not regular:
        return {**base, "status": "FAIL", "error": "lock is not a regular file"}

    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(lock_file, flags)
    except FileNotFoundError:
        return None
    except OSError as exc:
        return {**base, "status": "FAIL", "error": f"cannot open lock safely: {exc}"}
    try:
        current = os.fstat(fd)
        stable = (
            current.st_dev == before.st_dev
            and current.st_ino == before.st_ino
            and stat.S_ISREG(current.st_mode)
        )
        if not stable:
            return {
                **base,
                "status": "FAIL",
                "error": "lock identity changed while it was inspected",
            }
        digest = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        return {**base, "status": "WARN", "sha256": digest.hexdigest()}
    except OSError as exc:
        return {**base, "status": "FAIL", "error": f"cannot read lock safely: {exc}"}
    finally:
        os.close(fd)


def lock_report(*, profile_path: Optional[Path | str] = None) -> dict[str, Any]:
    """Return immutable metadata needed for guarded explicit lock recovery."""

    profile_file = (
        _resolve(profile_path) if profile_path is not None else storage_profile_path()
    )
    lock_file = profile_file.with_name(f"{profile_file.name}.lock")
    snapshot = _lock_snapshot(lock_file)
    if snapshot is None:
        return {
            "schema_version": 1,
            "status": "PASS",
            "profile_path": str(profile_file),
            "lock_path": str(lock_file),
            "present": False,
        }
    return {
        "schema_version": 1,
        "profile_path": str(profile_file),
        "lock_path": str(lock_file),
        **snapshot,
    }


def _same_lock_identity(
    left: dict[str, Any], right: dict[str, Any]
) -> bool:
    identity = ("device", "inode", "size", "mtime_ns", "sha256")
    return all(left.get(key) == right.get(key) for key in identity)


def _path_matches_open_file(path: Path, fd: int) -> bool:
    """Return whether a path still names the regular file held by *fd*."""

    try:
        current = path.lstat()
        opened = os.fstat(fd)
    except OSError:
        return False
    return (
        current.st_dev == opened.st_dev
        and current.st_ino == opened.st_ino
        and stat.S_ISREG(current.st_mode)
        and stat.S_ISREG(opened.st_mode)
    )


def recover_stale_lock(
    *,
    profile_path: Optional[Path | str] = None,
    expected_mtime_ns: int,
    expected_sha256: str,
    min_age_seconds: float = 300.0,
    confirm_no_writer: bool = False,
) -> dict[str, Any]:
    """Quarantine one unchanged legacy empty lock, then release it safely."""

    if not confirm_no_writer:
        raise StorageOperationError("lock recovery requires --confirm-no-writer")
    if min_age_seconds < 0:
        raise StorageOperationError("min_age_seconds must be non-negative")
    initial = lock_report(profile_path=profile_path)
    if not initial["present"]:
        raise StorageOperationError("storage profile lock does not exist")
    if not initial.get("regular_file"):
        raise StorageOperationError("storage profile lock is not a regular file")
    if initial.get("size") != 0:
        raise StorageOperationError(
            "only the current legacy empty lock format can be recovered safely"
        )
    if initial["age_seconds"] < min_age_seconds:
        raise StorageOperationError("storage profile lock is newer than the minimum age")
    if initial["mtime_ns"] != expected_mtime_ns:
        raise StorageOperationError("storage profile lock mtime changed")
    if initial["sha256"] != expected_sha256:
        raise StorageOperationError("storage profile lock SHA-256 changed")

    lock_file = Path(initial["lock_path"])
    recovery_guard = lock_file.with_name(f"{lock_file.name}.recovery")
    quarantine = recovery_guard / "stale.lock"
    try:
        os.mkdir(recovery_guard, 0o700)
    except OSError as exc:
        raise StorageOperationError(
            f"cannot acquire storage lock recovery guard: {exc}"
        ) from exc

    placeholder_fd: Optional[int] = None
    try:
        os.rename(lock_file, quarantine)
        try:
            placeholder_fd = os.open(
                lock_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
            )
        except FileExistsError as exc:
            quarantined = _lock_snapshot(quarantine)
            if quarantined is not None and _same_lock_identity(quarantined, initial):
                quarantine.unlink()
                recovery_guard.rmdir()
            raise StorageOperationError(
                "a new writer acquired the storage profile lock during recovery"
            ) from exc

        os.write(placeholder_fd, b"velantrim-storage-lock-recovery\n")
        os.fsync(placeholder_fd)
        quarantined = _lock_snapshot(quarantine)
        if quarantined is None or not _same_lock_identity(quarantined, initial):
            if not _path_matches_open_file(lock_file, placeholder_fd):
                raise StorageOperationError(
                    "storage recovery placeholder changed during recovery"
                )
            os.close(placeholder_fd)
            placeholder_fd = None
            os.replace(quarantine, lock_file)
            recovery_guard.rmdir()
            _fsync_directory(lock_file.parent)
            raise StorageOperationError("storage profile lock changed during recovery")

        quarantine.unlink()
        if not _path_matches_open_file(lock_file, placeholder_fd):
            raise StorageOperationError(
                "storage recovery placeholder changed during recovery"
            )
        os.close(placeholder_fd)
        placeholder_fd = None
        lock_file.unlink()
        recovery_guard.rmdir()
        _fsync_directory(lock_file.parent)
        identity = ("device", "inode", "size", "mtime_ns", "sha256")
        return {
            "schema_version": 1,
            "status": "PASS",
            "operation": "recover_lock",
            "profile_path": initial["profile_path"],
            "removed_lock": str(lock_file),
            "removed_identity": {key: initial[key] for key in identity},
        }
    except StorageOperationError:
        raise
    except OSError as exc:
        raise StorageOperationError(f"cannot recover storage profile lock: {exc}") from exc
    finally:
        if placeholder_fd is not None:
            try:
                os.close(placeholder_fd)
            except OSError:  # pragma: no cover - defensive descriptor cleanup
                pass
        try:
            recovery_guard.rmdir()
        except OSError:
            pass


def status_report(*, profile_path: Optional[Path | str] = None) -> dict[str, Any]:
    """Report lifecycle readiness without opening or modifying the active database."""

    profile_file = _resolve(profile_path) if profile_path is not None else storage_profile_path()
    lock = lock_report(profile_path=profile_file)
    try:
        profile = _load_profile(profile_file)
        database = _sqlite_locator(profile)
    except StorageOperationError as exc:
        return {
            "schema_version": 1,
            "status": "FAIL",
            "profile_path": str(profile_file),
            "error": str(exc),
            "lock": lock,
        }
    database_exists = database.is_file() and not database.is_symlink()
    if lock["status"] == "FAIL":
        status = "FAIL"
    elif database_exists and not lock["present"]:
        status = "PASS"
    else:
        status = "WARN"
    return {
        "schema_version": 1,
        "status": status,
        "profile_path": str(profile_file),
        "backend": "sqlite",
        "locator_sha256": profile["locator_sha256"],
        "database_path": str(database),
        "database_exists": database_exists,
        "lock": lock,
        "operations": {
            "backup": database_exists,
            "verify": True,
            "restore_to_new_target": True,
            "recover_lock": lock["present"],
            "cross_backend_migration": False,
            "automatic_activation": False,
        },
    }
