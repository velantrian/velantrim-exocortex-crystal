"""Regression tests for online WAL backups and legacy WAL-header bundles."""

from contextlib import closing
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
from urllib.parse import unquote, urlsplit

import pytest

from core import storage_backup as backup
from core import storage_common as common
from core import storage_ops as ops
from core import storage_restore as restore
from tests import storage_lifecycle_support

store = storage_lifecycle_support.store


BUNDLE_FILES = {
    common.BUNDLE_DATABASE, common.BUNDLE_PROFILE,
    common.BUNDLE_RECEIPT, common.BUNDLE_COMPLETE,
}
WAL_ONLY_ID = "committed-in-wal"


def _contents(directory: Path) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in directory.iterdir()}


def _node_ids(database: Path) -> set[str]:
    with closing(sqlite3.connect(f"{database.as_uri()}?immutable=1", uri=True)) as db:
        return {row[0] for row in db.execute("SELECT fact_id FROM nodes")}


def _record_sqlite_opens(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    opened: list[Path] = []
    real_connect = sqlite3.connect

    def connect(database, *args, **kwargs):
        name = os.fsdecode(database)
        if name.startswith("file:"):
            name = unquote(urlsplit(name).path)
        if name and name != ":memory:":
            opened.append(Path(name).resolve())
        return real_connect(database, *args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", connect)
    return opened


@pytest.fixture
def legacy_bundle(store: tuple[Path, Path], tmp_path: Path) -> Path:
    profile, _ = store
    bundle = tmp_path / "legacy"
    backup.create_backup(bundle, profile_path=profile)
    database = bundle / common.BUNDLE_DATABASE
    with closing(sqlite3.connect(database)) as db:
        assert db.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
    # A prior-release bundle may contain a WAL-mode main file, with its contents
    # fully checkpointed and the byte hash sealed by the original format.
    assert set(_contents(bundle)) == BUNDLE_FILES
    assert database.read_bytes()[18:20] == b"\x02\x02"
    receipt_path = bundle / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_bytes())
    receipt["database_sha256"] = common._sha256_file(database)
    receipt["database_size"] = database.stat().st_size
    receipt_path.write_bytes(common._json_bytes(receipt))
    storage_lifecycle_support._refresh_completion(bundle)
    return bundle


def test_wal_backup_preserves_uncheckpointed_commit_and_restores_via_cli(
    store: tuple[Path, Path], tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    profile, database = store
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(profile))
    source_profile = profile.read_bytes()
    bundle = tmp_path / "online-backup"
    source_wal = database.with_name(f"{database.name}-wal")
    with closing(sqlite3.connect(database)) as writer:
        assert writer.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
        writer.execute("PRAGMA wal_autocheckpoint=0")
        writer.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
        writer.execute("INSERT INTO nodes VALUES (?, ?)", (WAL_ONLY_ID, "{}"))
        writer.commit()
        assert writer.execute(
            "SELECT fact_id FROM nodes WHERE fact_id=?", (WAL_ONLY_ID,)
        ).fetchone() == (WAL_ONLY_ID,)
        assert source_wal.stat().st_size > 0
        raw_database = tmp_path / "only-main-file.db"
        shutil.copyfile(database, raw_database)
        assert WAL_ONLY_ID not in _node_ids(raw_database)
        original_database = database.read_bytes()
        original_wal = source_wal.read_bytes()

        assert backup.create_backup(bundle, profile_path=profile)["status"] == "PASS"
        after_backup = _contents(bundle)
        assert set(after_backup) == BUNDLE_FILES
        assert after_backup[common.BUNDLE_DATABASE][18:20] == b"\x01\x01"
        verified = backup.verify_backup(bundle)
        assert verified["status"] == "PASS"
        assert verified["sqlite"]["counts"]["nodes"] == 3
        assert WAL_ONLY_ID in _node_ids(bundle / common.BUNDLE_DATABASE)

        target_dir = tmp_path / "candidate"
        candidate = target_dir / "restored.db"
        candidate_profile = target_dir / "candidate.json"
        candidate_receipt = target_dir / "receipt.json"
        assert ops.main([
            "restore", str(bundle), "--target-database", str(candidate),
            "--target-profile", str(candidate_profile), "--receipt", str(candidate_receipt),
        ]) == 0
        result = json.loads(capsys.readouterr().out)
        assert result["status"] == "PASS"
        assert result["receipt"]["activation"] == "candidate_profile_only"
        assert {path.name for path in target_dir.iterdir()} == {
            candidate.name, candidate_profile.name, candidate_receipt.name,
        }
        assert WAL_ONLY_ID in _node_ids(candidate)
        assert _contents(bundle) == after_backup
        assert writer.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        assert database.read_bytes() == original_database
        assert source_wal.read_bytes() == original_wal
        assert profile.read_bytes() == source_profile


@pytest.mark.parametrize("legacy_sidecars", [False, True], ids=["four-files", "old-sidecars"])
def test_legacy_wal_bundle_verifies_without_sqlite_opening_it(
    legacy_bundle: Path, monkeypatch: pytest.MonkeyPatch, legacy_sidecars: bool,
) -> None:
    if legacy_sidecars:
        database = legacy_bundle / common.BUNDLE_DATABASE
        with closing(sqlite3.connect(f"{database.as_uri()}?mode=ro", uri=True)) as db:
            assert db.execute("SELECT COUNT(*) FROM nodes").fetchone() == (2,)
        assert (legacy_bundle / f"{common.BUNDLE_DATABASE}-wal").stat().st_size == 0
        assert (legacy_bundle / f"{common.BUNDLE_DATABASE}-shm").stat().st_size > 0
    before = _contents(legacy_bundle)
    opened = _record_sqlite_opens(monkeypatch)
    verified = backup.verify_backup(legacy_bundle)
    assert verified["status"] == "PASS"
    assert verified["sqlite"]["counts"]["nodes"] == 2
    assert opened and not any(path.is_relative_to(legacy_bundle) for path in opened)
    assert _contents(legacy_bundle) == before


def test_verify_avoids_temp_directory_configured_inside_bundle(
    legacy_bundle: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    before = _contents(legacy_bundle)
    monkeypatch.setenv("TMPDIR", str(legacy_bundle))
    monkeypatch.setattr(tempfile, "tempdir", None)
    open_file = os.open
    make_dir = os.mkdir

    def check_outside(path):
        assert not Path(os.fsdecode(path)).resolve().is_relative_to(legacy_bundle)

    def record_open(path, flags, *args, **kwargs):
        if flags & os.O_CREAT:
            check_outside(path)
        return open_file(path, flags, *args, **kwargs)

    def record_mkdir(path, *args, **kwargs):
        check_outside(path)
        return make_dir(path, *args, **kwargs)

    monkeypatch.setattr(os, "open", record_open)
    monkeypatch.setattr(os, "mkdir", record_mkdir)
    assert backup.verify_backup(legacy_bundle)["status"] == "PASS"
    assert _contents(legacy_bundle) == before


def test_verify_fails_when_no_safe_scratch_is_writable(
    legacy_bundle: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    before = _contents(legacy_bundle)
    monkeypatch.setattr(os, "access", lambda *_args: False)
    with pytest.raises(common.StorageOperationError, match="no writable temporary directory"):
        backup.verify_backup(legacy_bundle)
    assert _contents(legacy_bundle) == before


def test_legacy_wal_bundle_restores_without_mutating_bundle_or_creating_sidecars(
    legacy_bundle: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    before = _contents(legacy_bundle)
    opened = _record_sqlite_opens(monkeypatch)
    target_dir = tmp_path / "candidate"
    target = target_dir / "db"
    profile = target_dir / "profile.json"
    result = restore.restore_backup(legacy_bundle, target_database=target, target_profile=profile)
    assert result["status"] == "PASS"
    assert {path.name for path in target_dir.iterdir()} == {
        target.name, profile.name, Path(result["restore_receipt"]).name,
    }
    assert result["receipt"]["source_database_sha256"] == result["receipt"]["target_database_sha256"]
    assert target.read_bytes() == before[common.BUNDLE_DATABASE]
    assert opened and target not in opened
    assert not any(path.is_relative_to(legacy_bundle) for path in opened)
    assert _contents(legacy_bundle) == before
    assert _node_ids(target) == {"f0", "f1"}


def test_legacy_wal_restore_receipt_failure_leaves_no_candidate_artifacts(
    legacy_bundle: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    before = _contents(legacy_bundle)
    target_dir = tmp_path / "candidate"
    target = target_dir / "db"
    profile = target_dir / "profile.json"
    receipt = target_dir / "receipt.json"
    original_write = restore._write_new_json

    def fail_receipt(path, payload):
        if path == receipt:
            assert target.read_bytes() == before[common.BUNDLE_DATABASE]
            raise OSError("simulated receipt write failure")
        return original_write(path, payload)

    monkeypatch.setattr(restore, "_write_new_json", fail_receipt)
    with pytest.raises(common.StorageOperationError, match="simulated receipt write failure"):
        restore.restore_backup(
            legacy_bundle, target_database=target, target_profile=profile, receipt_path=receipt,
        )
    assert list(target_dir.iterdir()) == []
    assert _contents(legacy_bundle) == before


@pytest.mark.parametrize("operation", ["verify", "restore"])
def test_nonempty_untracked_bundle_wal_fails_without_modifying_input(
    legacy_bundle: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str], operation: str,
) -> None:
    database = legacy_bundle / common.BUNDLE_DATABASE
    wal = database.with_name(f"{database.name}-wal")
    with closing(sqlite3.connect(database)) as writer:
        writer.execute("PRAGMA wal_autocheckpoint=0")
        writer.execute("UPDATE nodes SET data=? WHERE fact_id=?", ("{}", "f1"))
        writer.commit()
        assert wal.stat().st_size > 0
        before = _contents(legacy_bundle)
        target_dir = tmp_path / "candidate"
        args = [operation, str(legacy_bundle)]
        if operation == "restore":
            args += [
                "--target-database", str(target_dir / "db"),
                "--target-profile", str(target_dir / "profile.json"),
            ]
        assert ops.main(args) == 2
        result = json.loads(capsys.readouterr().out)
        assert result["status"] == "FAIL"
        assert "wal" in result["error"].lower()
        assert _contents(legacy_bundle) == before
        assert not target_dir.exists()
