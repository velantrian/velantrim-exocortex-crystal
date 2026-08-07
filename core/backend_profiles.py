# core/backend_profiles.py
# Persistent deployment-profile guard for authority-bearing storage selection.

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Mapping, Optional

L3_BACKEND_ENV = "VELANTRIM_L3_BACKEND"
PROFILE_PATH_ENV = "VELANTRIM_STORAGE_PROFILE_PATH"
DEFAULT_PROFILE_PATH = "./data/velantrim-storage-profile.json"
PROFILE_SCHEMA_VERSION = 1

_LOCAL_BACKENDS = {"sqlite", "ladybug"}
_KNOWN_BACKENDS = _LOCAL_BACKENDS | {"neo4j", "mock"}
_INSTANCE_BACKENDS = {
    "SqliteL3Graph": "sqlite",
    "LadybugL3Graph": "ladybug",
    "Neo4jL3Graph": "neo4j",
    "MockL3Graph": "mock",
}


class StorageProfileError(RuntimeError):
    """Raised when a durable storage selection cannot be proved safe."""


@dataclass(frozen=True)
class BackendSelection:
    """Resolved backend request plus any locked non-secret configuration."""

    env_var: str
    requested_name: str
    effective_name: str
    profile_path: Optional[Path]
    profile: Optional[dict[str, Any]]
    environment: Mapping[str, str]


def storage_profile_path() -> Path:
    """Return the absolute deployment-profile path without creating it."""

    raw = os.environ.get(PROFILE_PATH_ENV, DEFAULT_PROFILE_PATH)
    if not raw.strip():
        raise StorageProfileError(f"{PROFILE_PATH_ENV} must not be empty")
    return Path(raw).expanduser().resolve(strict=False)


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _locator_sha256(backend: str, configuration: Mapping[str, str]) -> str:
    payload = {"backend": backend, "configuration": dict(configuration)}
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _configuration_for_backend(backend: str) -> dict[str, str]:
    if backend in _LOCAL_BACKENDS:
        default = (
            "./data/velantrim_l3.db"
            if backend == "sqlite"
            else "./data/velantrim_l3.lbug"
        )
        raw_path = os.environ.get("VELANTRIM_L3_PATH", default)
        if raw_path in {"", ":memory:"}:
            return {"path": raw_path}
        return {"path": str(Path(raw_path).expanduser().resolve(strict=False))}
    if backend == "neo4j":
        return {
            "uri": os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
            "database": os.environ.get("NEO4J_DATABASE", "neo4j"),
        }
    if backend == "mock":
        return {}
    raise StorageProfileError(f"unsupported storage backend: {backend!r}")


def _is_durable(backend: str, configuration: Mapping[str, str]) -> bool:
    if backend in _LOCAL_BACKENDS:
        return configuration.get("path") not in {"", ":memory:", None}
    return backend == "neo4j"


def _build_profile(backend: str, configuration: Mapping[str, str]) -> dict[str, Any]:
    normalized = dict(configuration)
    return {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "profile": "l3",
        "backend": backend,
        "durable": True,
        "configuration": normalized,
        "locator_sha256": _locator_sha256(backend, normalized),
    }


def _validate_profile(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise StorageProfileError("storage profile must be a JSON object")
    if raw.get("schema_version") != PROFILE_SCHEMA_VERSION:
        raise StorageProfileError("unsupported storage profile schema_version")
    if raw.get("profile") != "l3":
        raise StorageProfileError("storage profile must declare profile='l3'")

    backend = raw.get("backend")
    if backend not in _KNOWN_BACKENDS or backend == "mock":
        raise StorageProfileError("storage profile backend must be durable and supported")
    if raw.get("durable") is not True:
        raise StorageProfileError("storage profile must declare durable=true")

    configuration = raw.get("configuration")
    if not isinstance(configuration, dict):
        raise StorageProfileError("storage profile configuration must be an object")
    if backend in _LOCAL_BACKENDS:
        if set(configuration) != {"path"} or not isinstance(
            configuration.get("path"), str
        ):
            raise StorageProfileError("local storage profile requires one string path")
        if not _is_durable(backend, configuration):
            raise StorageProfileError("local storage profile path must be persistent")
    elif set(configuration) != {"uri", "database"} or not all(
        isinstance(configuration.get(key), str) and configuration.get(key)
        for key in ("uri", "database")
    ):
        raise StorageProfileError(
            "neo4j storage profile requires non-empty uri and database"
        )

    expected = _locator_sha256(backend, configuration)
    if raw.get("locator_sha256") != expected:
        raise StorageProfileError("storage profile locator checksum mismatch")
    return {
        "schema_version": PROFILE_SCHEMA_VERSION,
        "profile": "l3",
        "backend": backend,
        "durable": True,
        "configuration": dict(configuration),
        "locator_sha256": expected,
    }


def load_storage_profile(
    path: Optional[Path] = None,
    *,
    required: bool = False,
) -> Optional[dict[str, Any]]:
    """Read and strictly validate a profile; never repair malformed state."""

    target = path or storage_profile_path()
    if not target.exists():
        if required:
            raise StorageProfileError(f"storage profile not found: {target}")
        return None
    try:
        with target.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageProfileError(
            f"cannot read valid storage profile {target}: {type(exc).__name__}"
        ) from exc
    return _validate_profile(raw)


def _assert_environment_compatible(profile: Mapping[str, Any]) -> None:
    backend = str(profile["backend"])
    configuration = profile["configuration"]
    if backend in _LOCAL_BACKENDS and "VELANTRIM_L3_PATH" in os.environ:
        current = _configuration_for_backend(backend)
        if current != configuration:
            raise StorageProfileError(
                "VELANTRIM_L3_PATH conflicts with the locked storage locator"
            )
    if backend == "neo4j":
        for env_name, key in (
            ("NEO4J_URI", "uri"),
            ("NEO4J_DATABASE", "database"),
        ):
            if (
                env_name in os.environ
                and os.environ[env_name] != configuration[key]
            ):
                raise StorageProfileError(
                    f"{env_name} conflicts with the locked storage locator"
                )


def _environment_for_profile(profile: Mapping[str, Any]) -> dict[str, str]:
    backend = str(profile["backend"])
    configuration = profile["configuration"]
    if backend in _LOCAL_BACKENDS:
        return {"VELANTRIM_L3_PATH": str(configuration["path"])}
    if backend == "neo4j":
        return {
            "NEO4J_URI": str(configuration["uri"]),
            "NEO4J_DATABASE": str(configuration["database"]),
        }
    raise StorageProfileError(f"cannot apply profile backend: {backend!r}")


@contextmanager
def temporary_environment(overrides: Mapping[str, str]) -> Iterator[None]:
    """Apply non-secret profile values only for backend construction."""

    missing = object()
    previous: dict[str, object] = {
        key: os.environ.get(key, missing) for key in overrides
    }
    os.environ.update(overrides)
    try:
        yield
    finally:
        for key, value in previous.items():
            if value is missing:
                os.environ.pop(key, None)
            else:
                os.environ[key] = str(value)


def resolve_backend_selection(env_var: str, requested_name: str) -> BackendSelection:
    """Resolve the environment-selected singleton against its durable profile."""

    if env_var != L3_BACKEND_ENV:
        return BackendSelection(
            env_var, requested_name, requested_name, None, None, {}
        )

    path = storage_profile_path()
    profile = load_storage_profile(path)
    if profile is None:
        return BackendSelection(
            env_var, requested_name, requested_name, path, None, {}
        )

    locked = str(profile["backend"])
    _assert_environment_compatible(profile)
    if requested_name not in {"auto", locked}:
        raise StorageProfileError(
            f"{env_var}={requested_name!r} conflicts with locked backend {locked!r}"
        )
    return BackendSelection(
        env_var,
        requested_name,
        locked,
        path,
        profile,
        _environment_for_profile(profile),
    )


def _backend_from_instance(instance: Any) -> str:
    backend = _INSTANCE_BACKENDS.get(type(instance).__name__)
    if backend is None:
        raise StorageProfileError(
            f"cannot identify storage backend instance {type(instance).__name__!r}"
        )
    return backend


def _profiles_equal(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return _canonical_json(left) == _canonical_json(right)


def _acquire_profile_lock(lock_path: Path) -> int:
    for _ in range(100):
        try:
            return os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            time.sleep(0.01)
    raise StorageProfileError(  # pragma: no cover - bounded cross-process timeout
        f"timed out acquiring storage profile lock: {lock_path}"
    )


def _persist_profile_if_absent(
    profile: Mapping[str, Any],
    path: Path,
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(f"{path.name}.lock")
    lock_fd = _acquire_profile_lock(lock_path)
    temp_name: Optional[str] = None
    try:
        os.close(lock_fd)
        existing = load_storage_profile(path)
        if existing is not None:
            if not _profiles_equal(existing, profile):
                raise StorageProfileError(
                    "another process locked a different storage backend or locator"
                )
            return existing

        fd, temp_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=str(path.parent),
        )
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(profile, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        temp_name = None
        return _validate_profile(dict(profile))
    except OSError as exc:
        raise StorageProfileError(
            f"cannot persist storage profile {path}: {type(exc).__name__}"
        ) from exc
    finally:
        if temp_name is not None:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:  # pragma: no cover - defensive cleanup race
                pass
        try:
            os.unlink(lock_path)
        except FileNotFoundError:  # pragma: no cover - defensive cleanup race
            pass


def finalize_backend_selection(
    selection: BackendSelection,
    instance: Any,
) -> Optional[dict[str, Any]]:
    """Verify the constructed backend and persist a first durable selection."""

    if selection.env_var != L3_BACKEND_ENV:
        return None

    actual_backend = _backend_from_instance(instance)
    actual_configuration = _configuration_for_backend(actual_backend)

    if selection.profile is not None:
        if actual_backend != selection.profile["backend"]:
            raise StorageProfileError(
                "constructed backend does not match the locked storage profile"
            )
        if actual_configuration != selection.profile["configuration"]:
            raise StorageProfileError(
                "constructed backend locator does not match the locked storage profile"
            )
        return selection.profile

    if actual_backend == "mock":
        if selection.requested_name == "auto":
            raise StorageProfileError(
                "automatic L3 selection reached the ephemeral Mock backend; "
                "fix durable storage or explicitly select mock for development"
            )
        return None

    if not _is_durable(actual_backend, actual_configuration):
        if selection.requested_name == "auto":
            raise StorageProfileError(
                "automatic L3 selection resolved to an ephemeral storage locator"
            )
        return None

    candidate = _build_profile(actual_backend, actual_configuration)
    if selection.profile_path is None:
        raise StorageProfileError("missing storage profile path")
    return _persist_profile_if_absent(candidate, selection.profile_path)
