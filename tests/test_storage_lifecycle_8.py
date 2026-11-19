"""Restore CLI regressions using independent, disposable SQLite fixtures."""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

import pytest

from core import storage_backup as backup
from core import storage_common as common
from core import storage_restore as restore
from tests.storage_lifecycle_support import (
    _create_db,
    _profile_payload,
    _refresh_completion,
    _write_profile,
)

_REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture
def source_bundle(tmp_path: Path) -> tuple[Path, Path, Path]:
    database = tmp_path / "source.db"
    source_profile = tmp_path / "source.json"
    _create_db(database)
    _write_profile(source_profile, database)
    bundle = tmp_path / "backup"
    backup.create_backup(bundle, profile_path=source_profile)
    return source_profile, database, bundle


def _candidate_outputs(tmp_path: Path) -> dict[str, Path]:
    return {
        "--target-database": tmp_path / "candidate.db",
        "--target-profile": tmp_path / "candidate.json",
        "--receipt": tmp_path / "restore.json",
    }


def _run_restore(
    working_directory: Path, bundle: Path, active_profile: Path, outputs: dict[str, Path],
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-m", "core.storage_ops", "restore", str(bundle)]
    for flag, path in outputs.items():
        command.extend([flag, str(path)])
    environment = {name: os.environ[name] for name in ("PATH", "SYSTEMROOT") if name in os.environ}
    environment.update({
        "PYTHONPATH": str(_REPOSITORY),
        "VELANTRIM_STORAGE_PROFILE_PATH": str(active_profile),
    })
    return subprocess.run(
        command, cwd=working_directory, env=environment, text=True, capture_output=True, timeout=20,
    )


def _assert_restore_failed(
    result: subprocess.CompletedProcess[str], working_directory: Path, outputs: dict[str, Path],
) -> str:
    assert result.returncode == 2, (result.stdout, result.stderr)
    report = json.loads(result.stdout)
    assert report["status"] == "FAIL"
    assert report["schema_version"] == 1
    assert isinstance(report["error"], str) and report["error"]
    assert "Traceback" not in result.stderr
    for path in outputs.values():
        full_path = working_directory / path
        assert not full_path.exists() and not full_path.is_symlink(), full_path
    return report["error"]


def _source_artifacts(source: tuple[Path, Path, Path]) -> dict[Path, bytes]:
    profile, database, bundle = source
    return {path: path.read_bytes() for path in [profile, database, *bundle.iterdir()]}


@pytest.mark.parametrize("output", ["--target-database", "--target-profile", "--receipt"])
@pytest.mark.parametrize("suffix", ["", "-wal", "-shm", "-journal"], ids=["db", "wal", "shm", "journal"])
@pytest.mark.parametrize("spelling", ["absolute", "relative", "parent-reference", "directory-link"])
def test_restore_cli_reserves_active_sqlite_paths(
    source_bundle: tuple[Path, Path, Path], tmp_path: Path, output: str, suffix: str, spelling: str,
) -> None:
    _, _, bundle = source_bundle
    active_profile = tmp_path / "configured-active.json"
    active_database = tmp_path / "deployment" / "active.db"
    _write_profile(active_profile, active_database)
    original_profile = active_profile.read_bytes()
    protected = active_database.with_name(active_database.name + suffix)
    assert not active_database.exists() and not protected.exists()
    outputs = _candidate_outputs(tmp_path)
    target = protected
    if spelling == "relative":
        target = protected.relative_to(tmp_path)
    elif spelling == "parent-reference":
        nested = active_database.parent / "nested"
        nested.mkdir(parents=True)
        target = nested / ".." / protected.name
    elif spelling == "directory-link":
        active_database.parent.mkdir()
        alias = tmp_path / "deployment-alias"
        alias.symlink_to(active_database.parent, target_is_directory=True)
        target = alias / protected.name
    outputs[output] = target
    original_source = _source_artifacts(source_bundle)

    result = _run_restore(tmp_path, bundle, active_profile, outputs)

    assert "active SQLite storage path" in _assert_restore_failed(result, tmp_path, outputs)
    assert active_profile.read_bytes() == original_profile
    assert not active_database.exists()
    assert _source_artifacts(source_bundle) == original_source


def test_restore_cli_reserves_active_path_for_default_receipt(
    source_bundle: tuple[Path, Path, Path], tmp_path: Path,
) -> None:
    _, _, bundle = source_bundle
    active_profile = tmp_path / "configured-active.json"
    outputs = _candidate_outputs(tmp_path)
    del outputs["--receipt"]
    candidate_profile = outputs["--target-profile"]
    active_database = candidate_profile.with_name(candidate_profile.name + ".restore-receipt.json")
    _write_profile(active_profile, active_database)
    original_profile = active_profile.read_bytes()
    original_source = _source_artifacts(source_bundle)

    result = _run_restore(tmp_path, bundle, active_profile, outputs)

    assert "active SQLite storage path" in _assert_restore_failed(result, tmp_path, outputs)
    assert not active_database.exists()
    assert active_profile.read_bytes() == original_profile
    assert _source_artifacts(source_bundle) == original_source


def _profile_with_locator(active_database: Path, locator: str) -> dict:
    profile = _profile_payload(active_database)
    configuration = {"path": locator}
    profile["configuration"] = configuration
    canonical = json.dumps(
        {"backend": "sqlite", "configuration": configuration},
        sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    )
    profile["locator_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return profile


def _invalid_active_profile(active_database: Path, problem: str) -> bytes:
    if problem == "utf8":
        return b"\xff"
    if problem == "json":
        return b"{"
    if problem == "root-type":
        return b"[]"
    profile = _profile_payload(active_database)
    if problem == "required-field":
        del profile["configuration"]
    elif problem == "backend-type":
        profile["backend"] = ["sqlite"]
    elif problem == "boolean-version":
        profile["schema_version"] = True
    elif problem == "float-version":
        profile["schema_version"] = float(profile["schema_version"])
    else:
        profile = _profile_with_locator(active_database, "invalid\x00locator.db")
    return json.dumps(profile).encode("utf-8")


@pytest.mark.parametrize("problem", [
    "utf8", "json", "root-type", "required-field", "backend-type", "boolean-version",
    "float-version", "unresolvable-locator",
])
def test_restore_cli_rejects_invalid_active_profile(
    source_bundle: tuple[Path, Path, Path], tmp_path: Path, problem: str,
) -> None:
    _, _, bundle = source_bundle
    active_profile = tmp_path / "configured-active.json"
    active_database = tmp_path / "deployment" / "active.db"
    malformed = _invalid_active_profile(active_database, problem)
    active_profile.write_bytes(malformed)
    original_source = _source_artifacts(source_bundle)
    outputs = _candidate_outputs(tmp_path)

    result = _run_restore(tmp_path, bundle, active_profile, outputs)

    _assert_restore_failed(result, tmp_path, outputs)
    assert active_profile.read_bytes() == malformed
    assert not active_database.exists()
    assert _source_artifacts(source_bundle) == original_source


def test_restore_cli_with_absent_configured_profile_leaves_it_absent(
    source_bundle: tuple[Path, Path, Path], tmp_path: Path,
) -> None:
    _, _, bundle = source_bundle
    active_profile = tmp_path / "configured-active.json"
    outputs = _candidate_outputs(tmp_path)
    original_source = _source_artifacts(source_bundle)

    result = _run_restore(tmp_path, bundle, active_profile, outputs)

    assert result.returncode == 0, (result.stdout, result.stderr)
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert report["receipt"]["activation"] == "candidate_profile_only"
    assert not active_profile.exists()
    assert _source_artifacts(source_bundle) == original_source
    assert all(path.is_file() for path in outputs.values())
    restored = outputs["--target-database"]
    with closing(sqlite3.connect(f"{restored.as_uri()}?mode=ro", uri=True)) as connection:
        assert connection.execute("SELECT fact_id FROM nodes ORDER BY fact_id").fetchall() == [
            ("f0",), ("f1",),
        ]


@pytest.mark.parametrize(("locator", "error"), [
    ("deployment/active.db", "must not be an active SQLite storage path"),
    ("invalid\x00locator.db", "cannot resolve active SQLite storage path"),
    ("file:deployment/active.db", "cannot resolve active SQLite storage path"),
])
def test_restore_library_rejects_conflicting_or_unresolvable_active_locator(
    source_bundle: tuple[Path, Path, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    locator: str, error: str,
) -> None:
    _, _, bundle = source_bundle
    active_profile = tmp_path / "configured-active.json"
    target_database = tmp_path / "deployment" / "active.db"
    active_profile.write_text(
        json.dumps(_profile_with_locator(target_database, locator)), encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(active_profile))
    candidate = tmp_path / "candidate.json"

    with pytest.raises(common.StorageOperationError, match=error):
        restore.restore_backup(bundle, target_database=target_database, target_profile=candidate)
    assert not target_database.exists() and not candidate.exists()


def test_restore_library_reports_active_profile_inspection_failure(
    source_bundle: tuple[Path, Path, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, _, bundle = source_bundle

    def cannot_inspect() -> Path:
        raise OSError("fixture profile inspection failure")

    monkeypatch.setattr(restore, "storage_profile_path", cannot_inspect)
    with pytest.raises(common.StorageOperationError, match="cannot inspect active storage profile"):
        restore.restore_backup(
            bundle, target_database=tmp_path / "candidate.db", target_profile=tmp_path / "candidate.json",
        )


@pytest.mark.parametrize(("artifact", "problem", "error"), [
    (common.BUNDLE_COMPLETE, "utf8", "completion marker"),
    (common.BUNDLE_RECEIPT, "utf8", "backup receipt"),
    (common.BUNDLE_PROFILE, "utf8", "storage profile"),
    (common.BUNDLE_PROFILE, "backend-type", "storage profile backend"),
])
def test_restore_cli_rejects_malformed_artifact_with_matching_hashes(
    source_bundle: tuple[Path, Path, Path], tmp_path: Path,
    artifact: str, problem: str, error: str,
) -> None:
    active_profile, _, bundle = source_bundle
    corrupt = bundle / artifact
    if problem == "utf8":
        modified = b"\xff"
    else:
        profile = json.loads(corrupt.read_text(encoding="utf-8"))
        profile["backend"] = ["sqlite"]
        modified = json.dumps(profile).encode("utf-8")
    corrupt.write_bytes(modified)
    if artifact == common.BUNDLE_PROFILE:
        receipt = bundle / common.BUNDLE_RECEIPT
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        payload["profile_sha256"] = hashlib.sha256(modified).hexdigest()
        receipt.write_text(json.dumps(payload), encoding="utf-8")
    if artifact != common.BUNDLE_COMPLETE:
        _refresh_completion(bundle)
    original_source = _source_artifacts(source_bundle)
    outputs = _candidate_outputs(tmp_path)

    result = _run_restore(tmp_path, bundle, active_profile, outputs)

    assert error in _assert_restore_failed(result, tmp_path, outputs)
    assert _source_artifacts(source_bundle) == original_source


def test_verify_library_wraps_malformed_utf8_as_storage_error(
    source_bundle: tuple[Path, Path, Path],
) -> None:
    _, _, bundle = source_bundle
    (bundle / common.BUNDLE_COMPLETE).write_bytes(b"\xff")

    with pytest.raises(common.StorageOperationError, match="backup completion marker"):
        backup.verify_backup(bundle)


def test_verify_library_rejects_unresolvable_bundle_profile(
    source_bundle: tuple[Path, Path, Path],
) -> None:
    _, database, bundle = source_bundle
    profile = _profile_with_locator(database, "invalid\x00locator.db")
    profile_bytes = json.dumps(profile).encode("utf-8")
    (bundle / common.BUNDLE_PROFILE).write_bytes(profile_bytes)
    receipt = bundle / common.BUNDLE_RECEIPT
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["profile_sha256"] = hashlib.sha256(profile_bytes).hexdigest()
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    _refresh_completion(bundle)

    with pytest.raises(common.StorageOperationError, match="cannot resolve the SQLite storage profile path"):
        backup.verify_backup(bundle)
