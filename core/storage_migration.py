# core/storage_migration.py
# Deterministic bounded-memory SQLite logical export and independent verification.

from __future__ import annotations

import contextvars
import hashlib
import json
import math
import os
import shutil
import sqlite3
import stat
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Optional

from core.backend_profiles import (
    DEFAULT_PROFILE_PATH,
    PROFILE_PATH_ENV,
    storage_profile_path,
)
from core.storage_common import (
    StorageOperationError,
    _canonical_json,
    _connect_readonly,
    _load_profile,
    _resolve_operator_path,
    _sha256_file,
    _sqlite_locator,
    _utc_now,
    _write_new_json,
)

MIGRATION_SCHEMA_VERSION = 1
MIGRATION_BUNDLE_TYPE = "velantrim-l3-logical-export"
MIGRATION_MANIFEST = "manifest.json"
MIGRATION_COMPLETE = "complete.json"

# Resource ceilings remain explicit and fail closed. The implementation below no
# longer materializes complete datasets or identifier sets in process memory.
MAX_CONTROL_FILE_BYTES = 1 * 1024 * 1024
MAX_SOURCE_SQLITE_BYTES = 64 * 1024 * 1024
MAX_DATASET_BYTES = 64 * 1024 * 1024
MAX_BUNDLE_DATA_BYTES = 384 * 1024 * 1024
MAX_RECORD_BYTES = 1 * 1024 * 1024
MAX_RECORDS_PER_DATASET = 200_000
MIGRATION_BATCH_SIZE = 512
_DATASET_CONSUMER: contextvars.ContextVar[
    Optional[Callable[[Mapping[str, Any]], None]]
] = contextvars.ContextVar("migration_dataset_consumer", default=None)
MIN_TEMP_FREE_BYTES = 8 * 1024 * 1024
MAX_DANGLING_EXAMPLES = 20

# Final verification snapshots bind both path identity and content. The digest is
# intentionally kept out of filesystem metadata because timestamp precision varies
# across supported filesystems; the max-bytes value preserves the original bounded
# streaming ceiling during the final reread.
FileSnapshot = tuple[os.stat_result, str, int]


@dataclass(frozen=True)
class DirectorySnapshot:
    """Stable directory identity plus a deterministic child-entry inventory."""

    st_dev: int
    st_ino: int
    entries: tuple[tuple[str, int, int, int], ...]

DATASET_FILES = {
    "nodes": "nodes.jsonl",
    "vectors": "vectors.jsonl",
    "edges": "edges.jsonl",
    "entities": "entities.jsonl",
    "mentions": "mentions.jsonl",
    "meta": "meta.jsonl",
}

EXPECTED_COLUMNS = {
    "nodes": ("fact_id", "data"),
    "vectors": ("fact_id", "vec"),
    "edges": ("src", "rel_type", "dst", "props"),
    "entities": ("entity_id", "kind", "label"),
    "mentions": ("fact_id", "entity_id", "rel"),
    "meta": ("key", "value"),
}

AUTHORITY_BOUNDARY = {
    "physical_l3_equals_strict_canon": False,
    "migration_bundle_is_claim_evidence": False,
    "automatic_activation": False,
}


def _file_identity(value: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _open_regular_fd(
    path: Path,
    label: str,
    *,
    max_bytes: int,
) -> tuple[int, os.stat_result]:
    try:
        before = path.lstat()
    except FileNotFoundError as exc:
        raise StorageOperationError(f"{label} must be a regular file: {path}") from exc
    except OSError as exc:
        raise StorageOperationError(f"cannot inspect {label}: {exc}") from exc
    if not stat.S_ISREG(before.st_mode):
        raise StorageOperationError(f"{label} must be a regular file: {path}")
    if before.st_size > max_bytes:
        raise StorageOperationError(
            f"{label} exceeds the {max_bytes}-byte resource limit"
        )

    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise StorageOperationError(f"cannot open {label} safely: {exc}") from exc
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or (
            opened.st_dev != before.st_dev or opened.st_ino != before.st_ino
        ):
            raise StorageOperationError(f"{label} identity changed while opening")
        if opened.st_size > max_bytes:
            raise StorageOperationError(
                f"{label} exceeds the {max_bytes}-byte resource limit"
            )
        return fd, opened
    except Exception:
        os.close(fd)
        raise


def _read_regular_bytes(
    path: Path,
    label: str,
    *,
    max_bytes: int = MAX_CONTROL_FILE_BYTES,
) -> tuple[bytes, FileSnapshot]:
    """Read one small bounded control file from one stable descriptor."""

    fd, opened = _open_regular_fd(path, label, max_bytes=max_bytes)
    try:
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, min(1024 * 1024, max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise StorageOperationError(
                    f"{label} exceeds the {max_bytes}-byte resource limit"
                )
        after = os.fstat(fd)
        if _file_identity(after) != _file_identity(opened):
            raise StorageOperationError(f"{label} changed while it was read")
        raw = b"".join(chunks)
        if len(raw) != after.st_size:
            raise StorageOperationError(f"{label} byte-size changed while it was read")
        return raw, (after, hashlib.sha256(raw).hexdigest(), max_bytes)
    except StorageOperationError:
        raise
    except OSError as exc:
        raise StorageOperationError(f"cannot read {label} safely: {exc}") from exc
    finally:
        os.close(fd)


def _require_unchanged_file(path: Path, expected: FileSnapshot, label: str) -> None:
    expected_stat, expected_sha256, max_bytes = expected
    expected_identity = _file_identity(expected_stat)
    try:
        current = path.lstat()
    except OSError as exc:
        raise StorageOperationError(f"cannot recheck {label}: {exc}") from exc
    if not stat.S_ISREG(current.st_mode) or _file_identity(current) != expected_identity:
        raise StorageOperationError(f"{label} changed during verification")

    # Reopen without following symlinks and stream the content again. This is the
    # final content-integrity check: same-inode/same-size rewrites are rejected even
    # on filesystems whose observable mtime/ctime resolution is too coarse to show
    # the mutation. The reread stays within the same resource ceiling as the first.
    fd, opened = _open_regular_fd(path, label, max_bytes=max_bytes)
    try:
        if _file_identity(opened) != expected_identity:
            raise StorageOperationError(f"{label} changed during verification")
        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(fd, min(1024 * 1024, max_bytes + 1 - total))
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:  # pragma: no cover - concurrent growth guard
                raise StorageOperationError(f"{label} changed during verification")
            digest.update(chunk)
        after = os.fstat(fd)
        final = path.lstat()
        if (
            _file_identity(after) != expected_identity
            or not stat.S_ISREG(final.st_mode)
            or _file_identity(final) != expected_identity
            or total != after.st_size
            or digest.hexdigest() != expected_sha256
        ):
            raise StorageOperationError(f"{label} changed during verification")
    except StorageOperationError:
        raise
    except OSError as exc:
        raise StorageOperationError(f"cannot recheck {label}: {exc}") from exc
    finally:
        os.close(fd)


def _directory_entry_inventory(
    path: Path, label: str
) -> tuple[tuple[str, int, int, int], ...]:
    """Return a stable, no-follow inventory for immediate directory entries."""

    entries: list[tuple[str, int, int, int]] = []
    try:
        with os.scandir(path) as iterator:
            for entry in iterator:
                try:
                    entry_stat = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    raise StorageOperationError(
                        f"cannot inspect {label} entry {entry.name!r}: {exc}"
                    ) from exc
                entries.append((
                    entry.name,
                    entry_stat.st_dev,
                    entry_stat.st_ino,
                    stat.S_IFMT(entry_stat.st_mode),
                ))
    except StorageOperationError:
        raise
    except OSError as exc:
        raise StorageOperationError(f"cannot enumerate {label}: {exc}") from exc
    entries.sort(key=lambda item: item[0])
    return tuple(entries)


def _directory_identity(path: Path, label: str) -> DirectorySnapshot:
    try:
        value = path.lstat()
    except OSError as exc:
        raise StorageOperationError(f"cannot inspect {label}: {exc}") from exc
    if not stat.S_ISDIR(value.st_mode):
        raise StorageOperationError(f"{label} must be a directory: {path}")
    return DirectorySnapshot(
        st_dev=value.st_dev,
        st_ino=value.st_ino,
        entries=_directory_entry_inventory(path, label),
    )


def _require_unchanged_directory(
    path: Path, expected: DirectorySnapshot, label: str
) -> None:
    current = _directory_identity(path, label)
    if current != expected:
        raise StorageOperationError(f"{label} changed during verification")


def _require_free_disk(path: Path, required: int, label: str) -> None:
    try:
        free = shutil.disk_usage(path).free
    except OSError as exc:
        raise StorageOperationError(
            f"cannot inspect temporary disk for {label}: {exc}"
        ) from exc
    if free < required:
        raise StorageOperationError(
            f"insufficient temporary disk for {label}: required={required}, free={free}"
        )


def _canonical_record_bytes(record: Mapping[str, Any]) -> bytes:
    return (_canonical_json(record) + "\n").encode("utf-8")


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_json(raw: Any, label: str) -> Any:
    if not isinstance(raw, (str, bytes, bytearray)):
        raise StorageOperationError(f"{label} must contain JSON text")
    try:
        return json.loads(
            raw,
            parse_constant=_reject_constant,
            object_pairs_hook=_unique_object,
        )
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        raise StorageOperationError(f"{label} must contain strict JSON") from exc


def _json_object(raw: Any, label: str) -> dict[str, Any]:
    value = _strict_json(raw, label)
    if not isinstance(value, dict):
        raise StorageOperationError(f"{label} must contain a JSON object")
    return value


def _vector_value(value: Any, label: str) -> list[int | float]:
    if not isinstance(value, list) or not value:
        raise StorageOperationError(f"{label} must be a non-empty JSON array")
    for element in value:
        if isinstance(element, bool) or not isinstance(element, (int, float)):
            raise StorageOperationError(f"{label} contains a non-numeric element")
        if not math.isfinite(float(element)):
            raise StorageOperationError(f"{label} contains a non-finite element")
    return value


def _vector(raw: Any, label: str) -> list[int | float]:
    return _vector_value(_strict_json(raw, label), label)


def _table_columns(connection: sqlite3.Connection, table: str) -> tuple[str, ...]:
    try:
        return tuple(
            str(row[1]) for row in connection.execute(f'PRAGMA table_info("{table}")')
        )
    except sqlite3.Error as exc:
        raise StorageOperationError(
            f"cannot inspect SQLite table {table}: {exc}"
        ) from exc


def _require_schema(connection: sqlite3.Connection) -> None:
    for table, expected in EXPECTED_COLUMNS.items():
        actual = _table_columns(connection, table)
        if actual != expected:
            raise StorageOperationError(
                f"SQLite table {table} has unsupported columns: "
                f"expected={expected!r}, actual={actual!r}"
            )


def _node_record(row: sqlite3.Row) -> dict[str, Any]:
    fact_id = row["fact_id"]
    if not _non_empty_string(fact_id):
        raise StorageOperationError("nodes.fact_id must be a non-empty string")
    payload = _json_object(row["data"], f"node {fact_id!r}")
    if payload.get("fact_id") != fact_id:
        raise StorageOperationError(f"node {fact_id!r} payload fact_id mismatch")
    return {"fact_id": fact_id, "payload": payload}


def _vector_record(row: sqlite3.Row) -> dict[str, Any]:
    fact_id = row["fact_id"]
    if not _non_empty_string(fact_id):
        raise StorageOperationError("vectors.fact_id must be a non-empty string")
    return {"fact_id": fact_id, "vector": _vector(row["vec"], f"vector {fact_id!r}")}


def _edge_record(row: sqlite3.Row) -> dict[str, Any]:
    values = (row["src"], row["rel_type"], row["dst"])
    if not all(_non_empty_string(value) for value in values):
        raise StorageOperationError("edge identifiers must be non-empty strings")
    return {
        "src": values[0],
        "rel_type": values[1],
        "dst": values[2],
        "props": _json_object(
            row["props"], f"edge {values[0]!r}/{values[1]!r}/{values[2]!r}"
        ),
    }


def _entity_record(row: sqlite3.Row) -> dict[str, Any]:
    entity_id = row["entity_id"]
    if not _non_empty_string(entity_id):
        raise StorageOperationError("entities.entity_id must be a non-empty string")
    if any(
        row[key] is not None and not isinstance(row[key], str)
        for key in ("kind", "label")
    ):
        raise StorageOperationError("entities.kind/label must be strings or null")
    return {"entity_id": entity_id, "kind": row["kind"], "label": row["label"]}


def _mention_record(row: sqlite3.Row) -> dict[str, Any]:
    values = (row["fact_id"], row["entity_id"], row["rel"])
    if not all(_non_empty_string(value) for value in values):
        raise StorageOperationError("mention identifiers must be non-empty strings")
    return {"fact_id": values[0], "entity_id": values[1], "rel": values[2]}


def _meta_record(row: sqlite3.Row) -> dict[str, Any]:
    key, value = row["key"], row["value"]
    if not _non_empty_string(key):
        raise StorageOperationError("meta.key must be a non-empty string")
    if value is not None and not isinstance(value, str):
        raise StorageOperationError("meta.value must be a string or null")
    return {"key": key, "value": value}


RECORD_BUILDERS: dict[str, Callable[[sqlite3.Row], dict[str, Any]]] = {
    "nodes": _node_record,
    "vectors": _vector_record,
    "edges": _edge_record,
    "entities": _entity_record,
    "mentions": _mention_record,
    "meta": _meta_record,
}

QUERIES = {
    "nodes": "SELECT fact_id, data FROM nodes ORDER BY fact_id",
    "vectors": "SELECT fact_id, vec FROM vectors ORDER BY fact_id",
    "edges": "SELECT src, rel_type, dst, props FROM edges",
    "entities": "SELECT entity_id, kind, label FROM entities ORDER BY entity_id",
    "mentions": (
        "SELECT fact_id, entity_id, rel FROM mentions "
        "ORDER BY fact_id, entity_id, rel"
    ),
    "meta": "SELECT key, value FROM meta ORDER BY key",
}

COUNT_QUERIES = {
    "nodes": "SELECT COUNT(*) FROM nodes",
    "vectors": "SELECT COUNT(*) FROM vectors",
    "edges": "SELECT COUNT(*) FROM edges",
    "entities": "SELECT COUNT(*) FROM entities",
    "mentions": "SELECT COUNT(*) FROM mentions",
    "meta": "SELECT COUNT(*) FROM meta",
}


def _record_key(dataset: str, record: Mapping[str, Any]) -> tuple[Any, ...]:
    if dataset in {"nodes", "vectors"}:
        return (record["fact_id"],)
    if dataset == "edges":
        return (
            record["src"],
            record["rel_type"],
            record["dst"],
            _canonical_json(record["props"]),
        )
    if dataset == "entities":
        return (record["entity_id"],)
    if dataset == "mentions":
        return (record["fact_id"], record["entity_id"], record["rel"])
    return (record["key"],)


def _dataset_count(connection: sqlite3.Connection, dataset: str) -> int:
    try:
        value = int(connection.execute(COUNT_QUERIES[dataset]).fetchone()[0])
    except (sqlite3.Error, TypeError, ValueError) as exc:
        raise StorageOperationError(
            f"cannot count SQLite dataset {dataset}: {exc}"
        ) from exc
    if value > MAX_RECORDS_PER_DATASET:
        raise StorageOperationError(
            f"SQLite dataset {dataset} exceeds the {MAX_RECORDS_PER_DATASET}-record "
            "local-first export limit"
        )
    return value


def _cursor_records(cursor: sqlite3.Cursor, dataset: str) -> Iterator[dict[str, Any]]:
    builder = RECORD_BUILDERS[dataset]
    while True:
        rows = cursor.fetchmany(MIGRATION_BATCH_SIZE)
        if not rows:
            return
        for row in rows:
            yield builder(row)


def _edge_spool_records(cursor: sqlite3.Cursor) -> Iterator[dict[str, Any]]:
    temporary = tempfile.TemporaryDirectory(prefix="velantrim-edge-sort-")
    spool_path = Path(temporary.name) / "edges.sqlite"
    connection: Optional[sqlite3.Connection] = None
    try:
        os.chmod(temporary.name, 0o700)
        connection = sqlite3.connect(spool_path)
        os.chmod(spool_path, 0o600)
        connection.execute("PRAGMA journal_mode=OFF")
        connection.execute("PRAGMA synchronous=OFF")
        connection.execute(
            "CREATE TABLE records("
            "src TEXT NOT NULL, rel_type TEXT NOT NULL, dst TEXT NOT NULL, "
            "props TEXT NOT NULL, line BLOB NOT NULL, "
            "PRIMARY KEY(src, rel_type, dst, props)) WITHOUT ROWID"
        )
        for record in _cursor_records(cursor, "edges"):
            key = _record_key("edges", record)
            line = _canonical_record_bytes(record)
            try:
                connection.execute(
                    "INSERT INTO records VALUES (?,?,?,?,?)",
                    (key[0], key[1], key[2], key[3], line),
                )
            except sqlite3.IntegrityError as exc:
                raise StorageOperationError(
                    "edges contain a duplicate canonical record"
                ) from exc
        connection.commit()
        ordered = connection.execute(
            "SELECT line FROM records ORDER BY src, rel_type, dst, props"
        )
        while True:
            rows = ordered.fetchmany(MIGRATION_BATCH_SIZE)
            if not rows:
                return
            for row in rows:
                yield _strict_json(row[0], "spooled edge record")
    except StorageOperationError:
        raise
    except sqlite3.Error as exc:
        raise StorageOperationError(f"cannot sort SQLite edges: {exc}") from exc
    finally:
        if connection is not None:
            connection.close()
        temporary.cleanup()


def _export_records(
    connection: sqlite3.Connection, dataset: str
) -> Iterable[dict[str, Any]]:
    try:
        cursor = connection.execute(QUERIES[dataset])
    except sqlite3.Error as exc:
        raise StorageOperationError(
            f"cannot export SQLite dataset {dataset}: {exc}"
        ) from exc
    if dataset == "edges":
        return _edge_spool_records(cursor)
    return _cursor_records(cursor, dataset)


def _write_dataset(
    path: Path,
    records: Iterable[Mapping[str, Any]],
    *,
    on_record: Optional[Callable[[Mapping[str, Any]], None]] = None,
) -> dict[str, Any]:
    count = 0
    total = 0
    digest = hashlib.sha256()
    try:
        with path.open("xb") as handle:
            os.chmod(path, 0o600)
            for record in records:
                line = _canonical_record_bytes(record)
                if len(line) > MAX_RECORD_BYTES:
                    raise StorageOperationError(
                        f"migration record exceeds the {MAX_RECORD_BYTES}-byte limit"
                    )
                count += 1
                if count > MAX_RECORDS_PER_DATASET:
                    raise StorageOperationError(
                        "migration dataset exceeds the record-count resource limit"
                    )
                total += len(line)
                if total > MAX_DATASET_BYTES:
                    raise StorageOperationError(
                        f"migration dataset exceeds the {MAX_DATASET_BYTES}-byte limit"
                    )
                if on_record is not None:
                    on_record(record)
                handle.write(line)
                digest.update(line)
            handle.flush()
            os.fsync(handle.fileno())
    except StorageOperationError:
        raise
    except OSError as exc:
        raise StorageOperationError(
            f"cannot write migration dataset {path.name}: {exc}"
        ) from exc
    finally:
        closer = getattr(records, "close", None)
        if callable(closer):
            closer()
    return {
        "file": path.name,
        "records": count,
        "bytes": total,
        "sha256": digest.hexdigest(),
    }


def _profile_path(profile_path: Optional[Path | str]) -> Path:
    if profile_path is not None:
        return _resolve_operator_path(profile_path, "storage profile")
    raw = Path(os.environ.get(PROFILE_PATH_ENV, DEFAULT_PROFILE_PATH)).expanduser()
    if raw.is_symlink():
        raise StorageOperationError(
            f"storage profile must not be a symbolic link: {raw}"
        )
    return storage_profile_path()


def _read_source(
    profile_path: Optional[Path | str],
) -> tuple[Path, dict[str, Any], Path, str]:
    profile_file = _profile_path(profile_path)
    if profile_file.is_symlink() or not profile_file.is_file():
        raise StorageOperationError(
            f"storage profile must be a regular file: {profile_file}"
        )
    profile_size = profile_file.stat().st_size
    if profile_size > MAX_CONTROL_FILE_BYTES:
        raise StorageOperationError(
            "storage profile exceeds the control-file resource limit"
        )
    profile_hash = _sha256_file(profile_file)
    profile = _load_profile(profile_file)
    raw_locator = Path(str(profile["configuration"]["path"])).expanduser()
    if raw_locator.is_symlink():
        raise StorageOperationError(
            f"SQLite storage file must not be a symbolic link: {raw_locator}"
        )
    database = _sqlite_locator(profile)
    if database.is_symlink() or not database.is_file():
        raise StorageOperationError(
            f"SQLite storage file must be a regular file: {database}"
        )
    database_size = database.stat().st_size
    if database_size > MAX_SOURCE_SQLITE_BYTES:
        raise StorageOperationError(
            f"SQLite storage file exceeds the {MAX_SOURCE_SQLITE_BYTES}-byte "
            "local-first export limit"
        )
    return profile_file, profile, database, profile_hash


def _source_manifest(
    connection: sqlite3.Connection,
    profile: Mapping[str, Any],
    profile_hash: str,
) -> dict[str, Any]:
    try:
        integrity = [
            str(row[0]) for row in connection.execute("PRAGMA integrity_check")
        ]
        if integrity != ["ok"]:
            raise StorageOperationError(
                "SQLite integrity_check failed: " + "; ".join(integrity)
            )
        schema_version = int(connection.execute("PRAGMA schema_version").fetchone()[0])
        user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
    except sqlite3.Error as exc:
        raise StorageOperationError(f"cannot inspect SQLite source: {exc}") from exc
    return {
        "backend": "sqlite",
        "profile_schema_version": profile["schema_version"],
        "profile_sha256": profile_hash,
        "locator_sha256": profile["locator_sha256"],
        "sqlite_schema_version": schema_version,
        "sqlite_user_version": user_version,
    }


def export_sqlite_logical(
    output: Path | str,
    *,
    profile_path: Optional[Path | str] = None,
) -> dict[str, Any]:
    """Export a bounded-memory locked SQLite physical L3 logical bundle."""

    target = _resolve_operator_path(output, "migration bundle")
    if target.exists() or target.is_symlink():
        raise StorageOperationError(f"migration bundle already exists: {target}")
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.mkdir(mode=0o700)
    except OSError as exc:
        raise StorageOperationError(f"cannot create migration bundle: {exc}") from exc

    success = False
    try:
        profile_file, profile, database, profile_hash = _read_source(profile_path)
        required_disk = max(
            MIN_TEMP_FREE_BYTES,
            min(MAX_BUNDLE_DATA_BYTES, database.stat().st_size * 4),
        )
        _require_free_disk(target.parent, required_disk, "logical export")
        _require_free_disk(
            Path(tempfile.gettempdir()), required_disk, "edge sort"
        )
        connection = _connect_readonly(database)
        try:
            connection.execute("BEGIN")
            _require_schema(connection)
            source = _source_manifest(connection, profile, profile_hash)
            datasets: dict[str, dict[str, Any]] = {}
            vector_dimension: Optional[int] = None
            total_data_bytes = 0
            for dataset, filename in DATASET_FILES.items():
                _dataset_count(connection, dataset)

                def track_vector(record: Mapping[str, Any]) -> None:
                    nonlocal vector_dimension
                    if dataset != "vectors":
                        return
                    dimension = len(record["vector"])
                    if vector_dimension is None:
                        vector_dimension = dimension
                    elif vector_dimension != dimension:
                        raise StorageOperationError(
                            "vectors have inconsistent dimensions"
                        )

                metadata = _write_dataset(
                    target / filename,
                    _export_records(connection, dataset),
                    on_record=track_vector,
                )
                total_data_bytes += int(metadata["bytes"])
                if total_data_bytes > MAX_BUNDLE_DATA_BYTES:
                    raise StorageOperationError(
                        "migration bundle exceeds the aggregate data resource limit"
                    )
                datasets[dataset] = metadata
            connection.execute("COMMIT")
        except sqlite3.Error as exc:
            raise StorageOperationError(
                f"SQLite export transaction failed: {exc}"
            ) from exc
        finally:
            connection.close()

        if _sha256_file(profile_file) != profile_hash:
            raise StorageOperationError("storage profile changed during logical export")

        manifest = {
            "schema_version": MIGRATION_SCHEMA_VERSION,
            "bundle_type": MIGRATION_BUNDLE_TYPE,
            "source": source,
            "datasets": datasets,
            "vector_dimension": vector_dimension,
            "authority": AUTHORITY_BOUNDARY,
        }
        manifest_path = target / MIGRATION_MANIFEST
        _write_new_json(manifest_path, manifest)
        _write_new_json(
            target / MIGRATION_COMPLETE,
            {
                "schema_version": MIGRATION_SCHEMA_VERSION,
                "bundle_type": MIGRATION_BUNDLE_TYPE,
                "manifest_sha256": _sha256_file(manifest_path),
                "completed_at": _utc_now(),
            },
        )
        verified = verify_logical_export(target)
        success = True
        return {
            "schema_version": MIGRATION_SCHEMA_VERSION,
            "status": "PASS",
            "operation": "export_logical",
            "bundle": str(target),
            "manifest_sha256": verified["manifest_sha256"],
            "datasets": verified["datasets"],
            "vector_dimension": verified["vector_dimension"],
            "resource_mode": "bounded-streaming",
        }
    finally:
        if not success:
            shutil.rmtree(target, ignore_errors=True)


def _require_exact_keys(
    value: Mapping[str, Any], expected: set[str], label: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise StorageOperationError(
            f"{label} keys mismatch: expected={sorted(expected)!r}, "
            f"actual={sorted(actual)!r}"
        )


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise StorageOperationError(f"{label} must be a 64-character SHA-256")
    try:
        int(value, 16)
    except ValueError as exc:
        raise StorageOperationError(f"{label} must be hexadecimal") from exc
    return value


def _validate_record(dataset: str, record: Any) -> Mapping[str, Any]:
    if not isinstance(record, dict):
        raise StorageOperationError(f"{dataset} record must be a JSON object")
    if dataset == "nodes":
        _require_exact_keys(record, {"fact_id", "payload"}, "nodes record")
        if not _non_empty_string(record["fact_id"]) or not isinstance(
            record["payload"], dict
        ):
            raise StorageOperationError("nodes record has invalid fact_id or payload")
        if record["payload"].get("fact_id") != record["fact_id"]:
            raise StorageOperationError("nodes record payload fact_id mismatch")
    elif dataset == "vectors":
        _require_exact_keys(record, {"fact_id", "vector"}, "vectors record")
        if not _non_empty_string(record["fact_id"]):
            raise StorageOperationError("vectors record fact_id is invalid")
        _vector_value(record["vector"], "vectors record vector")
    elif dataset == "edges":
        _require_exact_keys(record, {"src", "rel_type", "dst", "props"}, "edges record")
        if not all(
            _non_empty_string(record[key]) for key in ("src", "rel_type", "dst")
        ):
            raise StorageOperationError("edges record identifiers are invalid")
        if not isinstance(record["props"], dict):
            raise StorageOperationError("edges record props must be an object")
    elif dataset == "entities":
        _require_exact_keys(record, {"entity_id", "kind", "label"}, "entities record")
        if not _non_empty_string(record["entity_id"]):
            raise StorageOperationError("entities record entity_id is invalid")
        if any(
            record[key] is not None and not isinstance(record[key], str)
            for key in ("kind", "label")
        ):
            raise StorageOperationError(
                "entities record kind/label must be string or null"
            )
    elif dataset == "mentions":
        _require_exact_keys(record, {"fact_id", "entity_id", "rel"}, "mentions record")
        if not all(
            _non_empty_string(record[key])
            for key in ("fact_id", "entity_id", "rel")
        ):
            raise StorageOperationError("mentions record identifiers are invalid")
    else:
        _require_exact_keys(record, {"key", "value"}, "meta record")
        if not _non_empty_string(record["key"]):
            raise StorageOperationError("meta record key is invalid")
        if record["value"] is not None and not isinstance(record["value"], str):
            raise StorageOperationError("meta record value must be string or null")
    return record


def _read_dataset(
    path: Path,
    dataset: str,
    expected: Mapping[str, Any],
) -> tuple[list[Mapping[str, Any]], FileSnapshot]:
    if path.name != expected.get("file"):
        raise StorageOperationError(f"{dataset} dataset filename mismatch")
    fd, snapshot = _open_regular_fd(
        path,
        f"{dataset} migration dataset",
        max_bytes=MAX_DATASET_BYTES,
    )
    records: list[Mapping[str, Any]] = []
    consumer = _DATASET_CONSUMER.get()
    expected_sha = _require_sha256(expected.get("sha256"), f"{dataset} sha256")
    try:
        if snapshot.st_size != expected.get("bytes"):
            raise StorageOperationError(f"{dataset} dataset byte-size mismatch")

        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(fd, 64 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_DATASET_BYTES:
                raise StorageOperationError(
                    f"{dataset} dataset exceeds byte resource limits"
                )
            digest.update(chunk)
        hashed = os.fstat(fd)
        if _file_identity(hashed) != _file_identity(snapshot):
            raise StorageOperationError(
                f"{dataset} migration dataset changed while it was read"
            )
        if total != expected.get("bytes"):
            raise StorageOperationError(f"{dataset} dataset byte-size mismatch")
        digest_hex = digest.hexdigest()
        if digest_hex != expected_sha:
            raise StorageOperationError(f"{dataset} dataset SHA-256 mismatch")

        os.lseek(fd, 0, os.SEEK_SET)
        count = 0
        previous: Optional[tuple[Any, ...]] = None
        with os.fdopen(fd, "rb", buffering=64 * 1024, closefd=False) as handle:
            while True:
                line = handle.readline(MAX_RECORD_BYTES + 1)
                if not line:
                    break
                if len(line) > MAX_RECORD_BYTES:
                    raise StorageOperationError(
                        f"{dataset} record exceeds the record-size resource limit"
                    )
                if not line.endswith(b"\n"):
                    raise StorageOperationError(
                        f"{dataset} dataset must end with a newline"
                    )
                count += 1
                if count > MAX_RECORDS_PER_DATASET:
                    raise StorageOperationError(
                        f"{dataset} dataset exceeds the record-count resource limit"
                    )
                record = _validate_record(
                    dataset, _strict_json(line, f"{dataset} record {count}")
                )
                if line != _canonical_record_bytes(record):
                    raise StorageOperationError(
                        f"{dataset} record {count} is not canonical JSON"
                    )
                key = _record_key(dataset, record)
                if previous is not None and key <= previous:
                    raise StorageOperationError(
                        f"{dataset} records are not strictly ordered"
                    )
                previous = key
                if consumer is None:
                    records.append(record)
                else:
                    consumer(record)
        after = os.fstat(fd)
        if _file_identity(after) != _file_identity(snapshot):
            raise StorageOperationError(
                f"{dataset} migration dataset changed while it was read"
            )
        if count != expected.get("records"):
            raise StorageOperationError(
                f"{dataset} dataset record-count mismatch"
            )
        return records, (after, digest_hex, MAX_DATASET_BYTES)
    except StorageOperationError:
        raise
    except OSError as exc:
        raise StorageOperationError(
            f"cannot read {dataset} migration dataset safely: {exc}"
        ) from exc
    finally:
        os.close(fd)


def _valid_completed_at(value: Any) -> bool:
    if not _non_empty_string(value) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def _verification_index(
    parent: Path,
) -> tuple[tempfile.TemporaryDirectory[str], sqlite3.Connection]:
    temporary = tempfile.TemporaryDirectory(
        prefix=".velantrim-migration-verify-",
        dir=parent,
    )
    connection: Optional[sqlite3.Connection] = None
    try:
        os.chmod(temporary.name, 0o700)
        database = Path(temporary.name) / "references.sqlite"
        connection = sqlite3.connect(database)
        os.chmod(database, 0o600)
        connection.executescript(
            """
            PRAGMA journal_mode=OFF;
            PRAGMA synchronous=OFF;
            CREATE TABLE nodes(id TEXT PRIMARY KEY) WITHOUT ROWID;
            CREATE TABLE entities(id TEXT PRIMARY KEY) WITHOUT ROWID;
            CREATE TABLE vectors(
                fact_id TEXT PRIMARY KEY,
                dimension INTEGER NOT NULL
            ) WITHOUT ROWID;
            CREATE TABLE edges(src TEXT NOT NULL, dst TEXT NOT NULL);
            CREATE TABLE mentions(fact_id TEXT NOT NULL, entity_id TEXT NOT NULL);
            """
        )
        return temporary, connection
    except (OSError, sqlite3.Error) as exc:
        if connection is not None:
            connection.close()
        temporary.cleanup()
        raise StorageOperationError(
            f"cannot create migration verification index: {exc}"
        ) from exc


def _missing_examples(
    connection: sqlite3.Connection,
    query: str,
) -> list[Any]:
    return [
        row[0] if len(row) == 1 else tuple(row)
        for row in connection.execute(query).fetchmany(MAX_DANGLING_EXAMPLES)
    ]


def verify_logical_export(bundle: Path | str) -> dict[str, Any]:
    """Verify a logical export with bounded memory and disk-backed reference checks."""

    root = _resolve_operator_path(bundle, "migration bundle")
    root_snapshot = _directory_identity(root, "migration bundle")

    manifest_path = root / MIGRATION_MANIFEST
    complete_path = root / MIGRATION_COMPLETE
    complete_raw, complete_snapshot = _read_regular_bytes(
        complete_path, "migration completion marker"
    )
    complete = _json_object(complete_raw, "migration completion marker")
    _require_exact_keys(
        complete,
        {"schema_version", "bundle_type", "manifest_sha256", "completed_at"},
        "migration completion marker",
    )
    if complete["schema_version"] != MIGRATION_SCHEMA_VERSION:
        raise StorageOperationError("unsupported migration completion schema_version")
    if complete["bundle_type"] != MIGRATION_BUNDLE_TYPE:
        raise StorageOperationError("migration completion bundle_type mismatch")
    if not _valid_completed_at(complete["completed_at"]):
        raise StorageOperationError("migration completion timestamp is invalid")
    manifest_sha = _require_sha256(
        complete["manifest_sha256"], "migration manifest sha256"
    )
    manifest_raw, manifest_snapshot = _read_regular_bytes(
        manifest_path, "migration manifest"
    )
    if hashlib.sha256(manifest_raw).hexdigest() != manifest_sha:
        raise StorageOperationError("migration manifest SHA-256 mismatch")

    manifest = _json_object(manifest_raw, "migration manifest")
    _require_exact_keys(
        manifest,
        {
            "schema_version",
            "bundle_type",
            "source",
            "datasets",
            "vector_dimension",
            "authority",
        },
        "migration manifest",
    )
    if manifest["schema_version"] != MIGRATION_SCHEMA_VERSION:
        raise StorageOperationError("unsupported migration manifest schema_version")
    if manifest["bundle_type"] != MIGRATION_BUNDLE_TYPE:
        raise StorageOperationError("migration manifest bundle_type mismatch")

    source = manifest["source"]
    if not isinstance(source, dict):
        raise StorageOperationError("migration source must be an object")
    _require_exact_keys(
        source,
        {
            "backend",
            "profile_schema_version",
            "profile_sha256",
            "locator_sha256",
            "sqlite_schema_version",
            "sqlite_user_version",
        },
        "migration source",
    )
    if source["backend"] != "sqlite" or source["profile_schema_version"] != 1:
        raise StorageOperationError("migration source backend/profile schema mismatch")
    _require_sha256(source["profile_sha256"], "source profile sha256")
    _require_sha256(source["locator_sha256"], "source locator sha256")
    if any(
        isinstance(source[key], bool) or not isinstance(source[key], int)
        for key in ("sqlite_schema_version", "sqlite_user_version")
    ):
        raise StorageOperationError("migration SQLite versions must be integers")

    if manifest["authority"] != AUTHORITY_BOUNDARY:
        raise StorageOperationError("migration authority boundary mismatch")

    datasets = manifest["datasets"]
    if not isinstance(datasets, dict) or set(datasets) != set(DATASET_FILES):
        raise StorageOperationError("migration dataset set mismatch")
    total_data_bytes = 0
    for name, metadata in datasets.items():
        if not isinstance(metadata, dict):
            raise StorageOperationError(f"{name} dataset metadata must be an object")
        _require_exact_keys(
            metadata, {"file", "records", "bytes", "sha256"}, f"{name} metadata"
        )
        if metadata["file"] != DATASET_FILES[name]:
            raise StorageOperationError(f"{name} dataset declared filename mismatch")
        if any(
            isinstance(metadata[key], bool)
            or not isinstance(metadata[key], int)
            or metadata[key] < 0
            for key in ("records", "bytes")
        ):
            raise StorageOperationError(
                f"{name} dataset counts must be non-negative integers"
            )
        if metadata["records"] > MAX_RECORDS_PER_DATASET:
            raise StorageOperationError(
                f"{name} dataset exceeds record resource limits"
            )
        if metadata["bytes"] > MAX_DATASET_BYTES:
            raise StorageOperationError(f"{name} dataset exceeds byte resource limits")
        total_data_bytes += metadata["bytes"]
    if total_data_bytes > MAX_BUNDLE_DATA_BYTES:
        raise StorageOperationError(
            "migration bundle exceeds aggregate resource limits"
        )

    allowed = {MIGRATION_MANIFEST, MIGRATION_COMPLETE, *DATASET_FILES.values()}
    actual = {path.name for path in root.iterdir()}
    if actual != allowed:
        raise StorageOperationError(
            "migration bundle file set mismatch: "
            f"expected={sorted(allowed)!r}, actual={sorted(actual)!r}"
        )

    _require_free_disk(
        root.parent,
        max(MIN_TEMP_FREE_BYTES, min(total_data_bytes, MAX_BUNDLE_DATA_BYTES)),
        "logical verification",
    )
    temporary, index = _verification_index(root.parent)
    snapshots: dict[str, FileSnapshot] = {}
    actual_dimension: Optional[int] = None

    def consume_vector(record: Mapping[str, Any]) -> None:
        nonlocal actual_dimension
        dimension = len(record["vector"])
        if actual_dimension is None:
            actual_dimension = dimension
        elif actual_dimension != dimension:
            raise StorageOperationError(
                "migration vectors have inconsistent dimensions"
            )
        index.execute(
            "INSERT INTO vectors VALUES (?,?)",
            (record["fact_id"], dimension),
        )

    try:
        index.execute("BEGIN")
        consumers: dict[str, Callable[[Mapping[str, Any]], None]] = {
            "nodes": lambda record: index.execute(
                "INSERT INTO nodes VALUES (?)", (record["fact_id"],)
            ),
            "vectors": consume_vector,
            "edges": lambda record: index.execute(
                "INSERT INTO edges VALUES (?,?)", (record["src"], record["dst"])
            ),
            "entities": lambda record: index.execute(
                "INSERT INTO entities VALUES (?)", (record["entity_id"],)
            ),
            "mentions": lambda record: index.execute(
                "INSERT INTO mentions VALUES (?,?)",
                (record["fact_id"], record["entity_id"]),
            ),
            "meta": lambda _record: None,
        }
        for name, filename in DATASET_FILES.items():
            token = _DATASET_CONSUMER.set(consumers[name])
            try:
                _, snapshots[name] = _read_dataset(
                    root / filename,
                    name,
                    datasets[name],
                )
            finally:
                _DATASET_CONSUMER.reset(token)
        index.commit()

        missing_vectors = _missing_examples(
            index,
            "SELECT v.fact_id FROM vectors v "
            "LEFT JOIN nodes n ON n.id=v.fact_id WHERE n.id IS NULL "
            "ORDER BY v.fact_id",
        )
        missing_edges = _missing_examples(
            index,
            "SELECT e.src,e.dst FROM edges e "
            "LEFT JOIN nodes s ON s.id=e.src "
            "LEFT JOIN nodes d ON d.id=e.dst "
            "WHERE s.id IS NULL OR d.id IS NULL ORDER BY e.src,e.dst",
        )
        missing_mentions = _missing_examples(
            index,
            "SELECT m.fact_id,m.entity_id FROM mentions m "
            "LEFT JOIN nodes n ON n.id=m.fact_id "
            "LEFT JOIN entities e ON e.id=m.entity_id "
            "WHERE n.id IS NULL OR e.id IS NULL "
            "ORDER BY m.fact_id,m.entity_id",
        )
    except StorageOperationError:
        raise
    except sqlite3.Error as exc:
        raise StorageOperationError(
            f"cannot build migration verification index: {exc}"
        ) from exc
    finally:
        index.close()
        temporary.cleanup()

    if missing_vectors or missing_edges or missing_mentions:
        raise StorageOperationError(
            "migration bundle contains dangling references: "
            f"vectors={missing_vectors!r}, edges={missing_edges!r}, "
            f"mentions={missing_mentions!r}"
        )

    vector_dimension = manifest["vector_dimension"]
    if vector_dimension != actual_dimension:
        raise StorageOperationError("migration vector_dimension mismatch")
    if vector_dimension is not None and (
        isinstance(vector_dimension, bool)
        or not isinstance(vector_dimension, int)
        or vector_dimension <= 0
    ):
        raise StorageOperationError(
            "migration vector_dimension must be a positive integer or null"
        )

    _require_unchanged_file(
        complete_path, complete_snapshot, "migration completion marker"
    )
    _require_unchanged_file(manifest_path, manifest_snapshot, "migration manifest")
    for name, filename in DATASET_FILES.items():
        _require_unchanged_file(
            root / filename, snapshots[name], f"{name} migration dataset"
        )
    final_files = {path.name for path in root.iterdir()}
    if final_files != allowed:
        raise StorageOperationError(
            "migration bundle file set changed during verification"
        )
    _require_unchanged_directory(root, root_snapshot, "migration bundle")

    return {
        "schema_version": MIGRATION_SCHEMA_VERSION,
        "status": "PASS",
        "operation": "verify_logical",
        "bundle": str(root),
        "manifest_sha256": manifest_sha,
        "datasets": {
            name: int(metadata["records"]) for name, metadata in datasets.items()
        },
        "vector_dimension": vector_dimension,
        "source": source,
        "resource_mode": "bounded-streaming",
    }
