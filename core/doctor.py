# core/doctor.py
# Read-only deployment diagnostics for Crystal's authority-bearing storage profile.

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

from core.backend_profiles import (
    L3_BACKEND_ENV,
    StorageProfileError,
    load_storage_profile,
    resolve_backend_selection,
    storage_profile_path,
)

_STATUS_CODES = {"PASS": 0, "WARN": 1, "FAIL": 2}


def _check(check_id: str, status: str, message: str, **details: Any) -> dict[str, Any]:
    return {
        "id": check_id,
        "status": status,
        "message": message,
        **details,
    }


def _dependency_available(backend: str) -> bool:
    if backend in {"sqlite", "mock"}:
        return True
    package = {"ladybug": "ladybug", "neo4j": "neo4j"}.get(backend)
    return bool(package and importlib.util.find_spec(package) is not None)


def _overall_status(checks: Sequence[dict[str, Any]]) -> str:
    if any(check["status"] == "FAIL" for check in checks):
        return "FAIL"
    if any(check["status"] == "WARN" for check in checks):
        return "WARN"
    return "PASS"


def doctor_report() -> dict[str, Any]:
    """Inspect configuration and filesystem readiness without opening L3."""

    checks: list[dict[str, Any]] = []
    requested = os.environ.get(L3_BACKEND_ENV, "auto")

    try:
        profile_path = storage_profile_path()
    except StorageProfileError as exc:
        checks.append(_check("profile_path", "FAIL", str(exc)))
        status = _overall_status(checks)
        return {
            "schema_version": 1,
            "status": status,
            "exit_code": _STATUS_CODES[status],
            "requested_backend": requested,
            "profile_path": None,
            "locked_backend": None,
            "checks": checks,
        }

    try:
        profile = load_storage_profile(profile_path)
    except StorageProfileError as exc:
        checks.append(_check("profile_integrity", "FAIL", str(exc)))
        status = _overall_status(checks)
        return {
            "schema_version": 1,
            "status": status,
            "exit_code": _STATUS_CODES[status],
            "requested_backend": requested,
            "profile_path": str(profile_path),
            "locked_backend": None,
            "checks": checks,
        }

    if profile is None:
        message = (
            "explicit Mock backend is ephemeral and intentionally has no durable profile"
            if requested == "mock"
            else "no durable profile exists yet; first successful durable startup will lock it"
        )
        checks.append(_check("profile_presence", "WARN", message))
        status = _overall_status(checks)
        return {
            "schema_version": 1,
            "status": status,
            "exit_code": _STATUS_CODES[status],
            "requested_backend": requested,
            "profile_path": str(profile_path),
            "locked_backend": None,
            "checks": checks,
        }

    locked = str(profile["backend"])
    checks.append(
        _check(
            "profile_integrity",
            "PASS",
            "profile schema and locator checksum are valid",
            locator_sha256=profile["locator_sha256"],
        )
    )

    try:
        selection = resolve_backend_selection(L3_BACKEND_ENV, requested)
    except StorageProfileError as exc:
        checks.append(_check("backend_lock", "FAIL", str(exc)))
    else:
        checks.append(
            _check(
                "backend_lock",
                "PASS",
                f"runtime selection resolves to locked backend "
                f"{selection.effective_name!r}",
            )
        )

    if _dependency_available(locked):
        checks.append(
            _check(
                "backend_dependency",
                "PASS",
                f"backend runtime dependency is available for {locked!r}",
            )
        )
    else:
        checks.append(
            _check(
                "backend_dependency",
                "FAIL",
                f"backend runtime dependency is unavailable for {locked!r}",
            )
        )

    configuration = profile["configuration"]
    if locked in {"sqlite", "ladybug"}:
        data_path = Path(configuration["path"])
        parent = data_path.parent
        if parent.exists() and os.access(parent, os.W_OK):
            checks.append(
                _check(
                    "storage_directory",
                    "PASS",
                    "storage directory exists and is writable",
                    path=str(parent),
                )
            )
        else:
            checks.append(
                _check(
                    "storage_directory",
                    "FAIL",
                    "storage directory is missing or not writable",
                    path=str(parent),
                )
            )

        if data_path.exists():
            checks.append(
                _check(
                    "storage_instance",
                    "PASS",
                    "locked storage instance exists",
                    path=str(data_path),
                )
            )
        else:
            checks.append(
                _check(
                    "storage_instance",
                    "WARN",
                    "locked storage instance does not exist yet",
                    path=str(data_path),
                )
            )
    else:
        checks.append(
            _check(
                "storage_instance",
                "PASS",
                "server locator is locked; connectivity is intentionally not probed",
                uri=configuration["uri"],
                database=configuration["database"],
            )
        )

    status = _overall_status(checks)
    return {
        "schema_version": 1,
        "status": status,
        "exit_code": _STATUS_CODES[status],
        "requested_backend": requested,
        "profile_path": str(profile_path),
        "locked_backend": locked,
        "checks": checks,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Emit one machine-readable report and return PASS/WARN/FAIL as 0/1/2."""

    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments:
        raise SystemExit("velantrim-doctor accepts no arguments")
    report = doctor_report()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return int(report["exit_code"])


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
