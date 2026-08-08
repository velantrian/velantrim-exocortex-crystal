from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from core import postgresql_migration as pg
from core.storage_common import StorageOperationError
from tests.postgresql_migration_support import PreflightConnection


def preflight(connection):
    return pg._preflight(
        connection,
        driver_version="3.3.4",
        target_schema="velantrim_inactive_test",
        require_tls=True,
        allow_insecure_test_connection=False,
        require_absent_schema=True,
        require_writable=True,
    )


def test_target_identity_is_bound_to_non_secret_endpoint_metadata():
    first = PreflightConnection(
        host="primary-a.example",
        password="credential-a-must-not-appear",
    )
    second = PreflightConnection(
        host="primary-b.example",
        password="credential-b-must-not-appear",
    )

    first_result = preflight(first)
    second_result = preflight(second)

    assert len(first_result["target_locator_sha256"]) == 64
    assert first_result["target_locator_sha256"] != second_result[
        "target_locator_sha256"
    ]
    assert first_result["target_identity_sha256"] != second_result[
        "target_identity_sha256"
    ]
    serialized = json.dumps(first_result)
    assert "primary-a.example" not in serialized
    assert "credential-a-must-not-appear" not in serialized
    assert "password" not in serialized
    assert pg._target_identity(first_result) == first_result[
        "target_identity_sha256"
    ]


def test_locator_metadata_fail_closed_without_exposing_raw_values():
    with pytest.raises(
        StorageOperationError,
        match="connection metadata is unavailable",
    ) as missing:
        pg._connection_locator_sha256(SimpleNamespace())
    assert "password" not in str(missing.value)

    invalid = PreflightConnection(host="", password="raw-secret")
    with pytest.raises(
        StorageOperationError,
        match="connection metadata is invalid",
    ) as caught:
        pg._connection_locator_sha256(invalid)
    assert "raw-secret" not in str(caught.value)

    invalid_port = PreflightConnection(port=70000)
    with pytest.raises(
        StorageOperationError,
        match="connection metadata is invalid",
    ):
        pg._connection_locator_sha256(invalid_port)


def test_target_identity_fails_closed_without_valid_locator_context():
    result = preflight(PreflightConnection())
    result_without_locator = dict(result)
    result_without_locator.pop("target_locator_sha256")
    with pytest.raises(
        StorageOperationError,
        match="target locator context is unavailable",
    ):
        pg._target_identity(result_without_locator)

    result["target_locator_sha256"] = "short"
    with pytest.raises(
        StorageOperationError,
        match="target locator identity is invalid",
    ):
        pg._target_identity(result)
