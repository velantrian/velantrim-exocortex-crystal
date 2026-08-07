# core/postgresql_migration.py
# Optional inactive PostgreSQL/pgvector import and exact-state equivalence.

from __future__ import annotations

import hashlib
import importlib
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

from core.storage_common import (
    StorageOperationError,
    _canonical_json,
    _resolve_operator_path,
    _sha256_file,
    _utc_now,
    _write_new_json,
)
from core.storage_migration import (
    DATASET_FILES,
    MIGRATION_MANIFEST,
    _DATASET_CONSUMER,
    _json_object,
    _read_dataset,
    _read_regular_bytes,
    _strict_json,
    verify_logical_export,
)

POSTGRESQL_IMPORT_SCHEMA_VERSION = 1
POSTGRESQL_IMPORT_TYPE = "velantrim-inactive-postgresql-import"
DEFAULT_DSN_ENV = "VELANTRIM_POSTGRES_DSN"
TARGET_SCHEMA_PREFIX = "velantrim_inactive_"
IMPORT_BATCH_SIZE = 256
SUPPORTED_PSYCOPG_SERIES = (3, 3)
SUPPORTED_POSTGRESQL_MAJOR = 16
SUPPORTED_PGVECTOR_VERSION = (0, 8, 2)
RECEIPT_FILES = ("preflight.json", "import.json", "equivalence.json")
_ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]{0,127}$")
_SCHEMA_NAME = re.compile(r"^velantrim_inactive_[a-z0-9_]{1,42}$")


def _load_psycopg() -> Any:
    try:
        module = importlib.import_module("psycopg")
    except ImportError as exc:
        raise StorageOperationError(
            "PostgreSQL import requires the optional dependency: "
            "pip install 'velantrim-exocortex-crystal[postgresql]'"
        ) from exc
    version = _version_tuple(getattr(module, "__version__", ""), "Psycopg")
    if version[:2] != SUPPORTED_PSYCOPG_SERIES:
        raise StorageOperationError(
            "unsupported Psycopg version; this phase supports Psycopg 3.3.x"
        )
    return module


def _version_tuple(value: Any, label: str) -> tuple[int, ...]:
    if not isinstance(value, str) or not value:
        raise StorageOperationError(f"{label} version is unavailable")
    match = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?", value)
    if match is None:
        raise StorageOperationError(f"{label} version is invalid")
    return tuple(int(part or 0) for part in match.groups())


def _target_schema(value: str) -> str:
    if not isinstance(value, str) or _SCHEMA_NAME.fullmatch(value) is None:
        raise StorageOperationError(
            "target schema must match velantrim_inactive_[a-z0-9_]{1,42}"
        )
    return value


def _quoted_schema(value: str) -> str:
    return f'"{_target_schema(value)}"'


def _dsn_from_environment(name: str) -> str:
    if not isinstance(name, str) or _ENV_NAME.fullmatch(name) is None:
        raise StorageOperationError("DSN environment variable name is invalid")
    value = os.environ.get(name)
    if not value:
        raise StorageOperationError(
            f"PostgreSQL DSN environment variable is not set: {name}"
        )
    return value


def _database_failure(stage: str, exc: BaseException) -> StorageOperationError:
    sqlstate = getattr(exc, "sqlstate", None)
    suffix = f" (SQLSTATE {sqlstate})" if isinstance(sqlstate, str) else ""
    return StorageOperationError(f"PostgreSQL {stage} failed{suffix}")


def _connect(driver: Any, dsn: str, *, autocommit: bool) -> Any:
    try:
        return driver.connect(
            dsn,
            autocommit=autocommit,
            connect_timeout=10,
            application_name="velantrim-inactive-import",
        )
    except Exception as exc:
        raise _database_failure("connection", exc) from exc


def _fetch_one(connection: Any, query: str, params: Iterable[Any] = ()) -> tuple[Any, ...]:
    try:
        row = connection.execute(query, tuple(params)).fetchone()
    except Exception as exc:
        raise _database_failure("preflight query", exc) from exc
    if row is None:
        raise StorageOperationError("PostgreSQL preflight query returned no row")
    return tuple(row)


def _target_identity(preflight: Mapping[str, Any]) -> str:
    payload = {
        key: preflight[key]
        for key in (
            "database",
            "role",
            "server_version_num",
            "pgvector_version",
            "target_schema",
            "tls",
            "tls_policy",
        )
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _preflight(
    connection: Any,
    *,
    driver_version: str,
    target_schema: str,
    require_tls: bool,
    allow_insecure_test_connection: bool,
    require_absent_schema: bool,
    require_writable: bool,
) -> dict[str, Any]:
    database, role, server_version_num, server_version = _fetch_one(
        connection,
        "SELECT current_database(), current_user, "
        "current_setting('server_version_num')::integer, "
        "current_setting('server_version')",
    )
    server_version_num = int(server_version_num)
    if server_version_num // 10000 != SUPPORTED_POSTGRESQL_MAJOR:
        raise StorageOperationError(
            "unsupported PostgreSQL server; this phase is tested only on PostgreSQL 16"
        )
    pgvector = _fetch_one(
        connection,
        "SELECT extversion FROM pg_extension WHERE extname = 'vector'",
    )[0]
    if _version_tuple(pgvector, "pgvector") != SUPPORTED_PGVECTOR_VERSION:
        raise StorageOperationError(
            "unsupported pgvector extension; this phase requires pgvector 0.8.2"
        )
    tls = bool(
        _fetch_one(
            connection,
            "SELECT COALESCE((SELECT ssl FROM pg_stat_ssl "
            "WHERE pid = pg_backend_pid()), false)",
        )[0]
    )
    if require_tls and not tls:
        raise StorageOperationError("PostgreSQL TLS is required by the selected policy")
    if not require_tls and not allow_insecure_test_connection:
        raise StorageOperationError(
            "plaintext PostgreSQL is allowed only with explicit test-only authorization"
        )
    in_recovery = bool(_fetch_one(connection, "SELECT pg_is_in_recovery()")[0])
    if in_recovery:
        raise StorageOperationError("PostgreSQL target is in recovery")
    if require_writable:
        create_allowed, read_only = _fetch_one(
            connection,
            "SELECT has_database_privilege(current_user, current_database(), 'CREATE'), "
            "current_setting('transaction_read_only')::boolean",
        )
        if not bool(create_allowed) or bool(read_only):
            raise StorageOperationError(
                "PostgreSQL target is not writable by the explicit migration role"
            )
    schema_exists = bool(
        _fetch_one(
            connection,
            "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = %s)",
            (target_schema,),
        )[0]
    )
    if require_absent_schema and schema_exists:
        raise StorageOperationError(
            f"inactive PostgreSQL target schema already exists: {target_schema}"
        )
    if not require_absent_schema and not schema_exists:
        raise StorageOperationError(
            f"inactive PostgreSQL target schema does not exist: {target_schema}"
        )
    result = {
        "driver": "psycopg",
        "driver_version": driver_version,
        "database": str(database),
        "role": str(role),
        "server_version_num": server_version_num,
        "server_version": str(server_version),
        "pgvector_version": str(pgvector),
        "target_schema": target_schema,
        "target_schema_exists": schema_exists,
        "tls": tls,
        "tls_policy": "required" if require_tls else "explicit-test-plaintext",
        "active": False,
    }
    result["target_identity_sha256"] = _target_identity(result)
    return result


def _receipt_root(path: Path | str) -> Path:
    target = _resolve_operator_path(path, "PostgreSQL import receipt directory")
    if target.exists() or target.is_symlink():
        raise StorageOperationError(
            f"PostgreSQL import receipt directory already exists: {target}"
        )
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.mkdir(mode=0o700)
    except OSError as exc:
        raise StorageOperationError(
            f"cannot create PostgreSQL import receipt directory: {exc}"
        ) from exc
    return target


def _load_manifest(bundle: Path) -> dict[str, Any]:
    raw, _ = _read_regular_bytes(
        bundle / MIGRATION_MANIFEST,
        "migration manifest",
    )
    return _json_object(raw, "migration manifest")


def _operation_id(
    manifest_sha256: str,
    target_identity_sha256: str,
    target_schema: str,
) -> str:
    payload = f"{manifest_sha256}\n{target_identity_sha256}\n{target_schema}\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _ddl(target_schema: str, vector_dimension: Optional[int]) -> list[str]:
    schema = _quoted_schema(target_schema)
    vector_type = "vector" if vector_dimension is None else f"vector({vector_dimension})"
    return [
        f"CREATE SCHEMA {schema}",
        f"""CREATE TABLE {schema}.import_control(
            singleton smallint PRIMARY KEY CHECK(singleton = 1),
            operation_id text NOT NULL UNIQUE,
            state text NOT NULL CHECK(state IN ('IMPORTING','VERIFIED')),
            active boolean NOT NULL DEFAULT false CHECK(active = false),
            bundle_manifest_sha256 char(64) NOT NULL,
            source_profile_sha256 char(64) NOT NULL,
            source_locator_sha256 char(64) NOT NULL,
            target_identity_sha256 char(64) NOT NULL,
            vector_dimension integer CHECK(vector_dimension IS NULL OR vector_dimension > 0),
            created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
            verified_at timestamptz
        )""",
        f"""CREATE TABLE {schema}.nodes(
            fact_id text PRIMARY KEY,
            payload_json text NOT NULL,
            payload jsonb NOT NULL,
            CHECK(payload = payload_json::jsonb)
        )""",
        f"""CREATE TABLE {schema}.vectors(
            fact_id text PRIMARY KEY REFERENCES {schema}.nodes(fact_id)
                DEFERRABLE INITIALLY DEFERRED,
            embedding {vector_type} NOT NULL,
            embedding_json text NOT NULL,
            CHECK(embedding = embedding_json::vector)
        )""",
        f"""CREATE TABLE {schema}.edges(
            src text NOT NULL REFERENCES {schema}.nodes(fact_id)
                DEFERRABLE INITIALLY DEFERRED,
            rel_type text NOT NULL,
            dst text NOT NULL REFERENCES {schema}.nodes(fact_id)
                DEFERRABLE INITIALLY DEFERRED,
            props_json text NOT NULL,
            props jsonb NOT NULL,
            PRIMARY KEY(src, rel_type, dst, props_json),
            CHECK(props = props_json::jsonb)
        )""",
        f"""CREATE TABLE {schema}.entities(
            entity_id text PRIMARY KEY,
            kind text,
            label text
        )""",
        f"""CREATE TABLE {schema}.mentions(
            fact_id text NOT NULL REFERENCES {schema}.nodes(fact_id)
                DEFERRABLE INITIALLY DEFERRED,
            entity_id text NOT NULL REFERENCES {schema}.entities(entity_id)
                DEFERRABLE INITIALLY DEFERRED,
            rel text NOT NULL,
            PRIMARY KEY(fact_id, entity_id, rel)
        )""",
        f"""CREATE TABLE {schema}.metadata(
            key text PRIMARY KEY,
            value text
        )""",
        f"""CREATE TABLE {schema}.dataset_evidence(
            dataset text PRIMARY KEY,
            expected_records integer NOT NULL CHECK(expected_records >= 0),
            expected_bytes bigint NOT NULL CHECK(expected_bytes >= 0),
            expected_sha256 char(64) NOT NULL,
            actual_records integer,
            actual_bytes bigint,
            actual_sha256 char(64),
            exact_match boolean NOT NULL DEFAULT false
        )""",
    ]


def _dataset_sql(target_schema: str, dataset: str) -> str:
    schema = _quoted_schema(target_schema)
    statements = {
        "nodes": (
            f"INSERT INTO {schema}.nodes(fact_id,payload_json,payload) "
            "VALUES (%s,%s,%s::jsonb)"
        ),
        "vectors": (
            f"INSERT INTO {schema}.vectors(fact_id,embedding,embedding_json) "
            "VALUES (%s,%s::vector,%s)"
        ),
        "edges": (
            f"INSERT INTO {schema}.edges(src,rel_type,dst,props_json,props) "
            "VALUES (%s,%s,%s,%s,%s::jsonb)"
        ),
        "entities": (
            f"INSERT INTO {schema}.entities(entity_id,kind,label) VALUES (%s,%s,%s)"
        ),
        "mentions": (
            f"INSERT INTO {schema}.mentions(fact_id,entity_id,rel) VALUES (%s,%s,%s)"
        ),
        "meta": f"INSERT INTO {schema}.metadata(key,value) VALUES (%s,%s)",
    }
    return statements[dataset]


def _row(dataset: str, record: Mapping[str, Any]) -> tuple[Any, ...]:
    if dataset == "nodes":
        payload = _canonical_json(record["payload"])
        return record["fact_id"], payload, payload
    if dataset == "vectors":
        vector = _canonical_json(record["vector"])
        return record["fact_id"], vector, vector
    if dataset == "edges":
        props = _canonical_json(record["props"])
        return record["src"], record["rel_type"], record["dst"], props, props
    if dataset == "entities":
        return record["entity_id"], record["kind"], record["label"]
    if dataset == "mentions":
        return record["fact_id"], record["entity_id"], record["rel"]
    return record["key"], record["value"]


def _flush(cursor: Any, sql: str, rows: list[tuple[Any, ...]]) -> int:
    if not rows:
        return 0
    try:
        cursor.executemany(sql, rows)
    except Exception as exc:
        raise _database_failure("dataset import", exc) from exc
    count = len(rows)
    rows.clear()
    return count


def _import_dataset(
    cursor: Any,
    *,
    bundle: Path,
    target_schema: str,
    dataset: str,
    metadata: Mapping[str, Any],
) -> int:
    rows: list[tuple[Any, ...]] = []
    imported = 0
    sql = _dataset_sql(target_schema, dataset)

    def consume(record: Mapping[str, Any]) -> None:
        nonlocal imported
        rows.append(_row(dataset, record))
        if len(rows) >= IMPORT_BATCH_SIZE:
            imported += _flush(cursor, sql, rows)

    token = _DATASET_CONSUMER.set(consume)
    try:
        _read_dataset(bundle / DATASET_FILES[dataset], dataset, metadata)
    finally:
        _DATASET_CONSUMER.reset(token)
    imported += _flush(cursor, sql, rows)
    if imported != metadata["records"]:
        raise StorageOperationError(f"PostgreSQL {dataset} import count mismatch")
    return imported


def _target_query(target_schema: str, dataset: str) -> str:
    schema = _quoted_schema(target_schema)
    queries = {
        "nodes": f"SELECT fact_id,payload_json FROM {schema}.nodes ORDER BY fact_id",
        "vectors": (
            f"SELECT fact_id,embedding_json FROM {schema}.vectors ORDER BY fact_id"
        ),
        "edges": (
            f"SELECT src,rel_type,dst,props_json FROM {schema}.edges "
            "ORDER BY src,rel_type,dst,props_json"
        ),
        "entities": (
            f"SELECT entity_id,kind,label FROM {schema}.entities ORDER BY entity_id"
        ),
        "mentions": (
            f"SELECT fact_id,entity_id,rel FROM {schema}.mentions "
            "ORDER BY fact_id,entity_id,rel"
        ),
        "meta": f"SELECT key,value FROM {schema}.metadata ORDER BY key",
    }
    return queries[dataset]


def _target_record(dataset: str, row: tuple[Any, ...]) -> dict[str, Any]:
    if dataset == "nodes":
        return {"fact_id": row[0], "payload": _strict_json(row[1], "target node")}
    if dataset == "vectors":
        return {"fact_id": row[0], "vector": _strict_json(row[1], "target vector")}
    if dataset == "edges":
        return {
            "src": row[0],
            "rel_type": row[1],
            "dst": row[2],
            "props": _strict_json(row[3], "target edge"),
        }
    if dataset == "entities":
        return {"entity_id": row[0], "kind": row[1], "label": row[2]}
    if dataset == "mentions":
        return {"fact_id": row[0], "entity_id": row[1], "rel": row[2]}
    return {"key": row[0], "value": row[1]}


def _target_dataset_evidence(
    cursor: Any,
    *,
    target_schema: str,
    dataset: str,
) -> dict[str, Any]:
    try:
        cursor.execute(_target_query(target_schema, dataset))
    except Exception as exc:
        raise _database_failure("equivalence query", exc) from exc
    digest = hashlib.sha256()
    count = 0
    total = 0
    while True:
        try:
            rows = cursor.fetchmany(IMPORT_BATCH_SIZE)
        except Exception as exc:
            raise _database_failure("equivalence fetch", exc) from exc
        if not rows:
            break
        for raw in rows:
            line = (_canonical_json(_target_record(dataset, tuple(raw))) + "\n").encode(
                "utf-8"
            )
            digest.update(line)
            count += 1
            total += len(line)
    return {"records": count, "bytes": total, "sha256": digest.hexdigest()}


def _exact_equivalence(
    cursor: Any,
    *,
    target_schema: str,
    datasets: Mapping[str, Mapping[str, Any]],
    write_evidence: bool,
) -> dict[str, dict[str, Any]]:
    schema = _quoted_schema(target_schema)
    result: dict[str, dict[str, Any]] = {}
    for dataset, expected in datasets.items():
        actual = _target_dataset_evidence(
            cursor,
            target_schema=target_schema,
            dataset=dataset,
        )
        exact = all(actual[key] == expected[key] for key in ("records", "bytes", "sha256"))
        if write_evidence:
            try:
                cursor.execute(
                    f"UPDATE {schema}.dataset_evidence SET "
                    "actual_records=%s,actual_bytes=%s,actual_sha256=%s,exact_match=%s "
                    "WHERE dataset=%s",
                    (
                        actual["records"],
                        actual["bytes"],
                        actual["sha256"],
                        exact,
                        dataset,
                    ),
                )
            except Exception as exc:
                raise _database_failure("equivalence evidence write", exc) from exc
        if not exact:
            raise StorageOperationError(
                f"PostgreSQL exact-state mismatch for dataset: {dataset}"
            )
        result[dataset] = actual
    return result


def _control_row(connection: Any, target_schema: str) -> tuple[Any, ...]:
    schema = _quoted_schema(target_schema)
    return _fetch_one(
        connection,
        f"SELECT operation_id,state,active,bundle_manifest_sha256,"
        f"target_identity_sha256,vector_dimension FROM {schema}.import_control "
        "WHERE singleton=1",
    )


def _write_failure(root: Path, stage: str, error: StorageOperationError) -> None:
    path = root / "failure.json"
    if path.exists():
        return
    _write_new_json(
        path,
        {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,
            "operation": POSTGRESQL_IMPORT_TYPE,
            "status": "FAIL",
            "stage": stage,
            "error": str(error),
            "active": False,
            "failed_at": _utc_now(),
        },
    )


def import_logical_export_to_postgresql(
    bundle: Path | str,
    receipt_directory: Path | str,
    *,
    target_schema: str,
    dsn_env: str = DEFAULT_DSN_ENV,
    require_tls: bool = True,
    allow_insecure_test_connection: bool = False,
) -> dict[str, Any]:
    """Import a verified bundle into a new inactive PostgreSQL schema."""

    stage = "bundle-verification"
    bundle_path = _resolve_operator_path(bundle, "migration bundle")
    verified = verify_logical_export(bundle_path)
    manifest = _load_manifest(bundle_path)
    schema = _target_schema(target_schema)
    driver = _load_psycopg()
    dsn = _dsn_from_environment(dsn_env)
    root = _receipt_root(receipt_directory)
    connection: Any = None
    try:
        stage = "preflight"
        connection = _connect(driver, dsn, autocommit=True)
        preflight = _preflight(
            connection,
            driver_version=driver.__version__,
            target_schema=schema,
            require_tls=require_tls,
            allow_insecure_test_connection=allow_insecure_test_connection,
            require_absent_schema=True,
            require_writable=True,
        )
        manifest_sha = verified["manifest_sha256"]
        operation_id = _operation_id(
            manifest_sha,
            preflight["target_identity_sha256"],
            schema,
        )
        preflight_receipt = {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,
            "operation": POSTGRESQL_IMPORT_TYPE,
            "status": "PASS",
            "stage": "preflight",
            "operation_id": operation_id,
            "bundle_manifest_sha256": manifest_sha,
            "source": verified["source"],
            "target": preflight,
            "active": False,
            "checked_at": _utc_now(),
        }
        _write_new_json(root / "preflight.json", preflight_receipt)
        connection.close()
        connection = _connect(driver, dsn, autocommit=False)

        stage = "inactive-import"
        datasets = manifest["datasets"]
        vector_dimension = manifest["vector_dimension"]
        target = preflight["target_identity_sha256"]
        quoted = _quoted_schema(schema)
        cursor = connection.cursor()
        try:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            cursor.execute("SET LOCAL lock_timeout = '5s'")
            cursor.execute("SET LOCAL statement_timeout = '120s'")
            for statement in _ddl(schema, vector_dimension):
                cursor.execute(statement)
            cursor.execute(
                f"INSERT INTO {quoted}.import_control("
                "singleton,operation_id,state,active,bundle_manifest_sha256,"
                "source_profile_sha256,source_locator_sha256,target_identity_sha256,"
                "vector_dimension) VALUES (1,%s,'IMPORTING',false,%s,%s,%s,%s,%s)",
                (
                    operation_id,
                    manifest_sha,
                    verified["source"]["profile_sha256"],
                    verified["source"]["locator_sha256"],
                    target,
                    vector_dimension,
                ),
            )
            for dataset, metadata in datasets.items():
                cursor.execute(
                    f"INSERT INTO {quoted}.dataset_evidence("
                    "dataset,expected_records,expected_bytes,expected_sha256) "
                    "VALUES (%s,%s,%s,%s)",
                    (
                        dataset,
                        metadata["records"],
                        metadata["bytes"],
                        metadata["sha256"],
                    ),
                )
                _import_dataset(
                    cursor,
                    bundle=bundle_path,
                    target_schema=schema,
                    dataset=dataset,
                    metadata=metadata,
                )
            stage = "exact-equivalence"
            equivalence = _exact_equivalence(
                cursor,
                target_schema=schema,
                datasets=datasets,
                write_evidence=True,
            )
            cursor.execute(
                f"UPDATE {quoted}.import_control SET state='VERIFIED',"
                "verified_at=clock_timestamp() WHERE singleton=1 AND active=false"
            )
            if getattr(cursor, "rowcount", 1) != 1:
                raise StorageOperationError(
                    "PostgreSQL inactive import control update did not affect one row"
                )
            stage = "source-reverification"
            after = verify_logical_export(bundle_path)
            if after["manifest_sha256"] != manifest_sha:
                raise StorageOperationError(
                    "migration bundle changed during PostgreSQL import"
                )
            stage = "commit"
            connection.commit()
        except StorageOperationError:
            connection.rollback()
            raise
        except Exception as exc:
            connection.rollback()
            raise _database_failure(stage, exc) from exc
        finally:
            cursor.close()

        stage = "receipt-publication"
        import_receipt = {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,
            "operation": POSTGRESQL_IMPORT_TYPE,
            "status": "PASS",
            "stage": "inactive-import",
            "operation_id": operation_id,
            "bundle_manifest_sha256": manifest_sha,
            "target_identity_sha256": target,
            "target_schema": schema,
            "datasets": {
                name: metadata["records"] for name, metadata in datasets.items()
            },
            "active": False,
            "committed_at": _utc_now(),
        }
        equivalence_receipt = {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,
            "operation": POSTGRESQL_IMPORT_TYPE,
            "status": "PASS",
            "stage": "exact-equivalence",
            "operation_id": operation_id,
            "bundle_manifest_sha256": manifest_sha,
            "target_identity_sha256": target,
            "datasets": equivalence,
            "exact_state_equivalence": True,
            "active": False,
            "verified_at": _utc_now(),
        }
        _write_new_json(root / "import.json", import_receipt)
        _write_new_json(root / "equivalence.json", equivalence_receipt)
        _write_new_json(
            root / "complete.json",
            {
                "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,
                "operation": POSTGRESQL_IMPORT_TYPE,
                "status": "PASS",
                "operation_id": operation_id,
                "bundle_manifest_sha256": manifest_sha,
                "target_identity_sha256": target,
                "receipts": {
                    name: _sha256_file(root / name) for name in RECEIPT_FILES
                },
                "active": False,
                "completed_at": _utc_now(),
            },
        )
        return {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,
            "status": "PASS",
            "operation": "import_postgresql_inactive",
            "operation_id": operation_id,
            "bundle": str(bundle_path),
            "receipt_directory": str(root),
            "target_schema": schema,
            "target_identity_sha256": target,
            "exact_state_equivalence": True,
            "active": False,
        }
    except StorageOperationError as exc:
        try:
            _write_failure(root, stage, exc)
        except StorageOperationError:
            pass
        raise
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass


def verify_postgresql_import(
    bundle: Path | str,
    *,
    target_schema: str,
    dsn_env: str = DEFAULT_DSN_ENV,
    require_tls: bool = True,
    allow_insecure_test_connection: bool = False,
) -> dict[str, Any]:
    """Re-verify an existing inactive target without activating it."""

    bundle_path = _resolve_operator_path(bundle, "migration bundle")
    verified = verify_logical_export(bundle_path)
    manifest = _load_manifest(bundle_path)
    schema = _target_schema(target_schema)
    driver = _load_psycopg()
    dsn = _dsn_from_environment(dsn_env)
    connection = _connect(driver, dsn, autocommit=False)
    try:
        try:
            connection.execute("SET TRANSACTION READ ONLY")
        except Exception as exc:
            raise _database_failure("read-only verification setup", exc) from exc
        preflight = _preflight(
            connection,
            driver_version=driver.__version__,
            target_schema=schema,
            require_tls=require_tls,
            allow_insecure_test_connection=allow_insecure_test_connection,
            require_absent_schema=False,
            require_writable=False,
        )
        control = _control_row(connection, schema)
        operation_id, state, active, manifest_sha, target_identity, dimension = control
        if state != "VERIFIED" or bool(active):
            raise StorageOperationError(
                "PostgreSQL target is not a verified inactive import"
            )
        if manifest_sha != verified["manifest_sha256"]:
            raise StorageOperationError(
                "PostgreSQL target bundle manifest identity mismatch"
            )
        if target_identity != preflight["target_identity_sha256"]:
            raise StorageOperationError("PostgreSQL target identity mismatch")
        if dimension != manifest["vector_dimension"]:
            raise StorageOperationError("PostgreSQL target vector dimension mismatch")
        cursor = connection.cursor()
        try:
            equivalence = _exact_equivalence(
                cursor,
                target_schema=schema,
                datasets=manifest["datasets"],
                write_evidence=False,
            )
        finally:
            cursor.close()
        after = verify_logical_export(bundle_path)
        if after["manifest_sha256"] != verified["manifest_sha256"]:
            raise StorageOperationError(
                "migration bundle changed during PostgreSQL verification"
            )
        connection.rollback()
        return {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,
            "status": "PASS",
            "operation": "verify_postgresql_inactive",
            "operation_id": operation_id,
            "bundle": str(bundle_path),
            "target_schema": schema,
            "target_identity_sha256": target_identity,
            "datasets": equivalence,
            "exact_state_equivalence": True,
            "active": False,
        }
    finally:
        try:
            connection.close()
        except Exception:
            pass
