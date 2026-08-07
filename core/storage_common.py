# core/storage_common.py
# Shared fail-closed primitives for SQLite storage lifecycle operations.

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from core.backend_profiles import (
    PROFILE_SCHEMA_VERSION,
    StorageProfileError,
    load_storage_profile,
)

BUNDLE_SCHEMA_VERSION = 1
BUNDLE_DATABASE = "storage.sqlite3"
BUNDLE_PROFILE = "profile.json"
BUNDLE_RECEIPT = "receipt.json"
BUNDLE_COMPLETE = "complete.json"
SQLITE_TABLES = ("nodes", "vectors", "edges", "entities", "mentions", "meta")


class StorageOperationError(RuntimeError):
    """Raised when an operator action cannot prove a safe storage outcome."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _resolve(path: Path | str) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def _resolve_operator_path(path: Path | str, label: str) -> Path:
    raw = Path(path).expanduser()
    if raw.is_symlink():
        raise StorageOperationError(f"{label} must not be a symbolic link: {raw}")
    return raw.resolve(strict=False)


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        return
    try:
        try:
            os.fsync(fd)
        except OSError:
            pass
    finally:
        os.close(fd)


def _write_new_bytes(path: Path, content: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        os.close(fd)
        path.unlink(missing_ok=True)
        raise
    else:
        os.close(fd)
    _fsync_directory(path.parent)


def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _write_new_json(path: Path, payload: Mapping[str, Any]) -> None:
    _write_new_bytes(path, _json_bytes(payload))


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageOperationError(f"cannot read valid {label}: {exc}") from exc
    if not isinstance(payload, dict):
        raise StorageOperationError(f"{label} must be a JSON object")
    return payload


def _copy_new_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with source.open("rb") as src, os.fdopen(fd, "wb", closefd=False) as dst:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
            dst.flush()
            os.fsync(dst.fileno())
    except Exception:
        os.close(fd)
        target.unlink(missing_ok=True)
        raise
    else:
        os.close(fd)
    _fsync_directory(target.parent)


def _load_profile(path: Path) -> dict[str, Any]:
    try:
        profile = load_storage_profile(path, required=True)
    except StorageProfileError as exc:
        raise StorageOperationError(str(exc)) from exc
    if profile is None:  # defensive: required=True must never return None
        raise StorageOperationError(f"storage profile not found: {path}")
    return profile


def _sqlite_locator(profile: Mapping[str, Any]) -> Path:
    if profile.get("backend") != "sqlite":
        raise StorageOperationError(
            "this operation supports only a locked SQLite profile; "
            f"found {profile.get('backend')!r}"
        )
    configuration = profile.get("configuration")
    if not isinstance(configuration, Mapping):
        raise StorageOperationError("SQLite profile configuration is invalid")
    raw = configuration.get("path")
    if not isinstance(raw, str) or raw in {"", ":memory:"}:
        raise StorageOperationError("SQLite profile must point to a durable file")
    return _resolve(raw)


def _connect_readonly(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise StorageOperationError(f"SQLite storage file does not exist: {path}")
    try:
        connection = sqlite3.connect(f"{path.as_uri()}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        raise StorageOperationError(f"cannot open SQLite storage read-only: {exc}") from exc
    connection.row_factory = sqlite3.Row
    return connection


def _sqlite_metrics(path: Path) -> dict[str, Any]:
    connection = _connect_readonly(path)
    try:
        integrity_rows = [row[0] for row in connection.execute("PRAGMA integrity_check")]
        if integrity_rows != ["ok"]:
            raise StorageOperationError(
                "SQLite integrity_check failed: " + "; ".join(map(str, integrity_rows))
            )
        present = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        missing = [table for table in SQLITE_TABLES if table not in present]
        if missing:
            raise StorageOperationError(
                "SQLite storage is missing required tables: " + ", ".join(missing)
            )
        counts = {
            table: int(
                connection.execute(
                    f'SELECT COUNT(*) FROM "{table}"'  # nosec B608 -- hardcoded table tuple
                ).fetchone()[0]
            )
            for table in SQLITE_TABLES
        }
        return {
            "integrity_check": "ok",
            "counts": counts,
            "page_count": int(connection.execute("PRAGMA page_count").fetchone()[0]),
            "freelist_count": int(
                connection.execute("PRAGMA freelist_count").fetchone()[0]
            ),
            "user_version": int(connection.execute("PRAGMA user_version").fetchone()[0]),
        }
    except sqlite3.Error as exc:
        raise StorageOperationError(f"cannot inspect SQLite storage: {exc}") from exc
    finally:
        connection.close()


def _profile_payload_for_sqlite(path: Path) -> dict[str, Any]:
    configuration = {"path": str(_resolve(path))}
    locator_payload = {"backend": "sqlite", "configuration": configuration}
    return {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "profile": "l3",
        "backend": "sqlite",
        "durable": True,
        "configuration": configuration,
        "locator_sha256": _sha256_bytes(
            _canonical_json(locator_payload).encode("utf-8")
        ),
    }


def _bundle_paths(bundle: Path) -> tuple[Path, Path, Path]:
    return (
        bundle / BUNDLE_DATABASE,
        bundle / BUNDLE_PROFILE,
        bundle / BUNDLE_RECEIPT,
    )


def _require_regular_file(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise StorageOperationError(f"{label} must be a regular file: {path}")
