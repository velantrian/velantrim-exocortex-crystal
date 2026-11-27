"""Restore rollback and no-clobber regressions on disposable SQLite bundles."""

from __future__ import annotations

import json
import os
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

import pytest

from core import storage_backup as backup
from core import storage_common as common
from core import storage_ops as ops
from core import storage_restore as restore
from tests import storage_lifecycle_support

store = storage_lifecycle_support.store


def _legacy_bundle(root: Path, active_profile: Path) -> Path:
    bundle = root / "bundle"
    backup.create_backup(bundle, profile_path=active_profile)
    snapshot = bundle / common.BUNDLE_DATABASE
    with closing(sqlite3.connect(snapshot)) as connection:
        assert connection.execute("PRAGMA journal_mode=WAL").fetchone() == ("wal",)
    receipt_path = bundle / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_text())
    receipt["database_sha256"] = common._sha256_file(snapshot)
    receipt["database_size"] = snapshot.stat().st_size
    receipt_path.write_text(json.dumps(receipt))
    storage_lifecycle_support._refresh_completion(bundle)
    return bundle


def _run_restore(bundle: Path, database: Path, profile: Path, receipt: Path) -> int:
    return ops.main([
        "restore", str(bundle),
        "--target-database", str(database),
        "--target-profile", str(profile),
        "--receipt", str(receipt),
    ])


def _snapshot(directory: Path) -> dict[Path, bytes | None]:
    return {
        entry.relative_to(directory): None if entry.is_dir() else entry.read_bytes()
        for entry in directory.rglob("*")
    }


@pytest.mark.parametrize("phase", ["inspection", "scratch-copy", "receipt", "profile"])
def test_restore_rolls_back_after_copy_failure_points(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    phase: str,
) -> None:
    active_profile, _ = store
    bundle = _legacy_bundle(tmp_path, active_profile)
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(active_profile))
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(scratch))

    target = tmp_path / "candidate"
    target.mkdir()
    database = target / "l3.db"
    profile = target / "profile.json"
    receipt = target / "receipt.json"
    (target / "other.db-shm").write_bytes(b"operator-owned sidecar for a different file\n")
    initial = _snapshot(tmp_path)

    real_connect = sqlite3.connect
    real_open = os.open
    faults: list[str] = []

    def connect(path, *args, **kwargs):
        if phase == "inspection" and database.is_file():
            faults.append(phase)
            raise sqlite3.OperationalError("test inspection failure")
        return real_connect(path, *args, **kwargs)

    def open_file(path, flags, *args, **kwargs):
        if flags & os.O_CREAT and database.is_file():
            opened = Path(path)
            if phase == "scratch-copy" and opened.is_relative_to(scratch):
                faults.append(phase)
                raise OSError("test scratch-copy failure")
            if phase == "receipt" and opened == receipt:
                faults.append(phase)
                raise OSError("test receipt failure")
            if phase == "profile" and opened == profile:
                assert receipt.is_file()
                faults.append(phase)
                raise OSError("test profile failure")
        return real_open(path, flags, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        patch.setattr(os, "open", open_file)
        code = _run_restore(bundle, database, profile, receipt)

    output = capsys.readouterr()
    assert faults == [phase]
    assert code == 2
    report = json.loads(output.out)
    assert report["status"] == "FAIL"
    assert f"test {phase} failure" in report["error"]
    assert "Traceback" not in output.err
    assert _snapshot(tmp_path) == initial


def test_restore_reports_failed_cleanup_and_continues_rollback(store, tmp_path, monkeypatch):
    active_profile, _ = store
    bundle = _legacy_bundle(tmp_path, active_profile)
    original_bundle = _snapshot(bundle)
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(active_profile))
    database = tmp_path / "candidate.db"
    profile = tmp_path / "candidate.json"
    receipt = tmp_path / "restore.json"
    unlink = Path.unlink

    def fail_profile(_path, _data):
        raise OSError("synthetic profile write failure")

    def deny_receipt_cleanup(path, *args, **kwargs):
        if path == receipt:
            raise PermissionError("synthetic unlink failure")
        return unlink(path, *args, **kwargs)

    monkeypatch.setattr(restore, "_write_new_bytes", fail_profile)
    monkeypatch.setattr(Path, "unlink", deny_receipt_cleanup)
    with pytest.raises(common.StorageOperationError, match="cleanup incomplete") as failure:
        restore.restore_backup(bundle, target_database=database, target_profile=profile,
                               receipt_path=receipt)
    assert "synthetic profile write failure" in str(failure.value)
    assert str(receipt) in str(failure.value)
    assert receipt.exists()
    assert not database.exists()
    assert not profile.exists()
    assert _snapshot(bundle) == original_bundle


@pytest.mark.parametrize("suffix", ["", "-wal", "-shm", "-journal"])
def test_restore_preserves_existing_database_or_sidecar(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    suffix: str,
) -> None:
    active_profile, _ = store
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(active_profile))
    bundle = tmp_path / "bundle"
    backup.create_backup(bundle, profile_path=active_profile)
    database = tmp_path / "candidate.db"
    profile = tmp_path / "candidate.json"
    receipt = tmp_path / "restore.json"
    existing = database.with_name(database.name + suffix)
    existing.write_bytes(b"preexisting operator-owned data\x00\xff")
    initial = _snapshot(tmp_path)
    opened_outputs: list[Path] = []
    real_open = os.open

    def open_file(path, flags, *args, **kwargs):
        if flags & os.O_CREAT and Path(path) in {database, profile, receipt}:
            opened_outputs.append(Path(path))
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(os, "open", open_file)

    assert _run_restore(bundle, database, profile, receipt) == 2

    output = capsys.readouterr()
    assert json.loads(output.out)["status"] == "FAIL"
    assert opened_outputs == []
    assert "Traceback" not in output.err
    assert _snapshot(tmp_path) == initial


@pytest.mark.parametrize("suffix", ["-wal", "-shm", "-journal"])
@pytest.mark.parametrize("target_role", ["profile", "receipt"])
def test_restore_rejects_outputs_named_for_candidate_sidecars(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    suffix: str,
    target_role: str,
) -> None:
    active_profile, _ = store
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(active_profile))
    bundle = tmp_path / "bundle"
    backup.create_backup(bundle, profile_path=active_profile)
    database = tmp_path / "candidate.db"
    sidecar = database.with_name(database.name + suffix)
    profile = sidecar if target_role == "profile" else tmp_path / "candidate.json"
    receipt = sidecar if target_role == "receipt" else tmp_path / "restore.json"
    initial = _snapshot(tmp_path)

    assert _run_restore(bundle, database, profile, receipt) == 2

    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "FAIL"
    assert _snapshot(tmp_path) == initial


def test_verify_reports_unreadable_bundle_sidecar(
    store: tuple[Path, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    active_profile, _ = store
    bundle = tmp_path / "bundle"
    backup.create_backup(bundle, profile_path=active_profile)
    before = _snapshot(tmp_path)
    wal = bundle / f"{common.BUNDLE_DATABASE}-wal"
    real_lstat = Path.lstat

    def lstat(path: Path):
        if path == wal:
            raise PermissionError("test sidecar stat failure")
        return real_lstat(path)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "lstat", lstat)
        with pytest.raises(common.StorageOperationError, match="cannot inspect backup SQLite sidecar"):
            backup.verify_backup(bundle)

    assert _snapshot(tmp_path) == before


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("busy", "cannot checkpoint SQLite backup snapshot"),
        ("mode", "did not enter DELETE mode"),
        ("open", "cannot finalize SQLite backup snapshot"),
        ("sidecar", "still has sidecar files"),
    ],
)
def test_backup_finalization_failure_removes_incomplete_bundle(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
    message: str,
) -> None:
    active_profile, _ = store
    before = _snapshot(tmp_path)
    bundle = tmp_path / "bundle"
    snapshot = bundle / common.BUNDLE_DATABASE
    real_connect = sqlite3.connect

    class FinalizationConnection(sqlite3.Connection):
        def execute(self, statement, *args, **kwargs):
            if fault == "busy" and statement == "PRAGMA wal_checkpoint(TRUNCATE)":
                return super().execute("SELECT 1")
            if fault == "mode" and statement == "PRAGMA journal_mode=DELETE":
                return super().execute("SELECT 'wal'")
            return super().execute(statement, *args, **kwargs)

        def close(self):
            super().close()
            if fault == "sidecar":
                snapshot.with_name(snapshot.name + "-journal").touch()

    def connect(path, *args, **kwargs):
        if path == snapshot and snapshot.is_file():
            if fault == "open":
                raise sqlite3.OperationalError("test snapshot finalization open failure")
            return real_connect(path, *args, factory=FinalizationConnection, **kwargs)
        return real_connect(path, *args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", connect)

    with pytest.raises(common.StorageOperationError, match=message):
        backup.create_backup(bundle, profile_path=active_profile)

    assert _snapshot(tmp_path) == before
