# core/postgresql_migration.py
# Endpoint-bound facade for inactive PostgreSQL/pgvector migration operations.

from __future__ import annotations

import hashlib
import sys
from typing import Any, Mapping

from core import postgresql_migration_impl as _impl


def _connection_locator_sha256(connection: Any) -> str:
    """Hash non-secret libpq endpoint metadata without serializing a DSN."""

    try:
        info = connection.info
        host = info.host
        port = int(info.port)
        database = info.dbname
        user = info.user
    except (AttributeError, TypeError, ValueError) as exc:
        raise _impl.StorageOperationError(
            "PostgreSQL non-secret connection metadata is unavailable"
        ) from exc
    if (
        not isinstance(host, str)
        or not host
        or not isinstance(database, str)
        or not database
        or not isinstance(user, str)
        or not user
        or port < 1
        or port > 65535
    ):
        raise _impl.StorageOperationError(
            "PostgreSQL non-secret connection metadata is invalid"
        )
    payload = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
    }
    return hashlib.sha256(
        _impl._canonical_json(payload).encode("utf-8")
    ).hexdigest()


def _target_identity(preflight: Mapping[str, Any]) -> str:
    payload = {
        key: preflight[key]
        for key in (
            "database",
            "role",
            "server_version_num",
            "pgvector_version",
            "target_schema",
            "target_locator_sha256",
            "tls",
            "tls_policy",
        )
    }
    return hashlib.sha256(
        _impl._canonical_json(payload).encode("utf-8")
    ).hexdigest()


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
    database, role, server_version_num, server_version = _impl._fetch_one(
        connection,
        "SELECT current_database(), current_user, "
        "current_setting('server_version_num')::integer, "
        "current_setting('server_version')",
    )
    server_version_num = int(server_version_num)
    if server_version_num // 10000 != _impl.SUPPORTED_POSTGRESQL_MAJOR:
        raise _impl.StorageOperationError(
            "unsupported PostgreSQL server; this phase is tested only on PostgreSQL 16"
        )
    pgvector = _impl._fetch_one(
        connection,
        "SELECT extversion FROM pg_extension WHERE extname = 'vector'",
    )[0]
    if _impl._version_tuple(pgvector, "pgvector") != _impl.SUPPORTED_PGVECTOR_VERSION:
        raise _impl.StorageOperationError(
            "unsupported pgvector extension; this phase requires pgvector 0.8.2"
        )
    tls = bool(
        _impl._fetch_one(
            connection,
            "SELECT COALESCE((SELECT ssl FROM pg_stat_ssl "
            "WHERE pid = pg_backend_pid()), false)",
        )[0]
    )
    if require_tls and not tls:
        raise _impl.StorageOperationError(
            "PostgreSQL TLS is required by the selected policy"
        )
    if not require_tls and not allow_insecure_test_connection:
        raise _impl.StorageOperationError(
            "plaintext PostgreSQL is allowed only with explicit test-only authorization"
        )
    in_recovery = bool(
        _impl._fetch_one(connection, "SELECT pg_is_in_recovery()")[0]
    )
    if in_recovery:
        raise _impl.StorageOperationError("PostgreSQL target is in recovery")
    if require_writable:
        create_allowed, read_only = _impl._fetch_one(
            connection,
            "SELECT has_database_privilege(current_user, current_database(), 'CREATE'), "
            "current_setting('transaction_read_only')::boolean",
        )
        if not bool(create_allowed) or bool(read_only):
            raise _impl.StorageOperationError(
                "PostgreSQL target is not writable by the explicit migration role"
            )
    schema_exists = bool(
        _impl._fetch_one(
            connection,
            "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = %s)",
            (target_schema,),
        )[0]
    )
    if require_absent_schema and schema_exists:
        raise _impl.StorageOperationError(
            f"inactive PostgreSQL target schema already exists: {target_schema}"
        )
    if not require_absent_schema and not schema_exists:
        raise _impl.StorageOperationError(
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
        "target_locator_sha256": _connection_locator_sha256(connection),
        "tls": tls,
        "tls_policy": "required" if require_tls else "explicit-test-plaintext",
        "active": False,
    }
    result["target_identity_sha256"] = _target_identity(result)
    return result


_impl._connection_locator_sha256 = _connection_locator_sha256
_impl._target_identity = _target_identity
_impl._preflight = _preflight
sys.modules[__name__] = _impl
