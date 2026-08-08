# core/postgresql_migration.py
# Endpoint-bound facade for inactive PostgreSQL/pgvector migration operations.

from __future__ import annotations

from contextvars import ContextVar
import hashlib
import sys
from typing import Any, Mapping

from core import postgresql_migration_impl as _impl

_CURRENT_PREFLIGHT_CONNECTION: ContextVar[Any | None] = ContextVar(
    "postgresql_preflight_connection",
    default=None,
)
_ORIGINAL_PREFLIGHT = _impl._preflight


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
    locator = preflight.get("target_locator_sha256")
    if locator is None:
        connection = _CURRENT_PREFLIGHT_CONNECTION.get()
        if connection is None:
            raise _impl.StorageOperationError(
                "PostgreSQL target locator context is unavailable"
            )
        locator = _connection_locator_sha256(connection)
        if isinstance(preflight, dict):
            preflight["target_locator_sha256"] = locator
    if not isinstance(locator, str) or len(locator) != 64:
        raise _impl.StorageOperationError(
            "PostgreSQL target locator identity is invalid"
        )
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


def _preflight(connection: Any, **kwargs: Any) -> dict[str, Any]:
    token = _CURRENT_PREFLIGHT_CONNECTION.set(connection)
    try:
        return _ORIGINAL_PREFLIGHT(connection, **kwargs)
    finally:
        _CURRENT_PREFLIGHT_CONNECTION.reset(token)


_impl._connection_locator_sha256 = _connection_locator_sha256
_impl._target_identity = _target_identity
_impl._preflight = _preflight
sys.modules[__name__] = _impl
