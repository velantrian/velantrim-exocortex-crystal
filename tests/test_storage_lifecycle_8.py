"""Restore hardening follow-up to G-01 (PR #508): active locator, WAL, UTF-8.

All data is synthetic SQLite under tmp_path. Negative cases assert the reason
for the refusal, not just the exit code, and the exact state of the files.
"""

from __future__ import annotations

import subprocess
import sys

from tests.storage_lifecycle_support import (
    Path, _create_db, _refresh_completion, _write_profile, backup, common,
    hashlib, json, ops, os, pytest, restore, shutil, sqlite3, store,
)

REPO = Path(__file__).resolve().parents[1]
ACTIVE_ENV = "VELANTRIM_STORAGE_PROFILE_PATH"


def _state(root: Path) -> dict[str, str]:
    """Relative path -> content hash (or 'dir') for everything under root."""
    return {
        str(path.relative_to(root)): (
            "dir" if path.is_dir() else hashlib.sha256(path.read_bytes()).hexdigest()
        )
        for path in sorted(root.rglob("*"))
    }


def _cli(args: list[str], active_profile: Path) -> subprocess.CompletedProcess:
    """Run the real operator CLI in a child process with a minimal environment."""
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONPATH": str(REPO),
        ACTIVE_ENV: str(active_profile),
        "HOME": str(active_profile.parent),
    }
    return subprocess.run(
        [sys.executable, "-m", "core.storage_ops", *args],
        capture_output=True, text=True, env=env, cwd=REPO, timeout=120, check=False,
    )


def _fail_json(stdout: str) -> dict:
    """Exactly one JSON object with status FAIL on stdout."""
    lines = [line for line in stdout.splitlines() if line.strip()]
    assert len(lines) == 1
    report = json.loads(lines[0])
    assert report["status"] == "FAIL"
    return report


def _restore_args(bundle: Path, db: Path, prof: Path, receipt: Path | None = None) -> list[str]:
    args = ["restore", str(bundle), "--target-database", str(db), "--target-profile", str(prof)]
    if receipt is not None:
        args += ["--receipt", str(receipt)]
    return args


@pytest.fixture
def backed_up(store, tmp_path, monkeypatch):
    profile, db = store
    monkeypatch.setenv(ACTIVE_ENV, str(profile))
    bundle = tmp_path / "bundle"
    backup.create_backup(bundle, profile_path=profile)
    return profile, db, bundle


def _rehash(bundle: Path) -> None:
    """Refresh receipt hash/size and completion marker after editing the snapshot."""
    snapshot = bundle / common.BUNDLE_DATABASE
    receipt_file = bundle / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_file.read_text())
    receipt["database_sha256"] = common._sha256_file(snapshot)
    receipt["database_size"] = snapshot.stat().st_size
    receipt_file.write_text(json.dumps(receipt))
    _refresh_completion(bundle)


def _legacy_wal_bundle(bundle: Path) -> None:
    """Turn a new bundle into what PR #508-era backups produced: WAL header,
    empty -wal and a -shm index beside the snapshot."""
    snapshot = bundle / common.BUNDLE_DATABASE
    conn = sqlite3.connect(snapshot)
    assert conn.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
    conn.close()
    assert snapshot.read_bytes()[18:20] == b"\x02\x02"
    (bundle / "storage.sqlite3-wal").write_bytes(b"")
    (bundle / "storage.sqlite3-shm").write_bytes(b"\0" * 32768)
    _rehash(bundle)


# --------------------------------------------------------------------- R-01 / R-02
@pytest.mark.parametrize("suffix", ["", "-wal", "-shm", "-journal"])
@pytest.mark.parametrize("output", ["database", "profile", "receipt"])
def test_r01_r02_restore_refuses_active_locator_when_database_file_is_missing(
    backed_up, tmp_path, capsys, output: str, suffix: str
) -> None:
    profile, db, bundle = backed_up
    db.unlink()  # active profile still points here, but the file is gone
    conflict = Path(str(db.resolve()) + suffix)
    fresh = tmp_path / "fresh"
    db_t, prof_t, receipt_t = fresh / "l3.db", fresh / "c.json", fresh / "r.json"
    if output == "database":
        db_t = conflict
    elif output == "profile":
        prof_t = conflict
    else:
        receipt_t = conflict
    profile_before = profile.read_bytes()

    assert ops.main(_restore_args(bundle, db_t, prof_t, receipt_t if output == "receipt" else None)) == 2

    report = _fail_json(capsys.readouterr().out)
    assert "active storage database" in report["error"]
    assert not conflict.exists() and not fresh.exists()
    assert profile.read_bytes() == profile_before


def test_r01_real_cli_refuses_active_locator_when_database_file_is_missing(backed_up, tmp_path) -> None:
    profile, db, bundle = backed_up
    db.unlink()
    fresh = tmp_path / "fresh"
    proc = _cli(_restore_args(bundle, db, fresh / "c.json"), profile)
    assert proc.returncode == 2 and proc.stderr == ""
    assert "active storage database" in _fail_json(proc.stdout)["error"]
    assert not db.exists() and not fresh.exists()


# ------------------------------------------------------------------------- R-03
def _tamper(profile: Path, **changes) -> bytes:
    payload = json.loads(profile.read_text())
    payload.update(changes)
    return json.dumps(payload).encode()


@pytest.mark.parametrize(
    "label",
    ["bad_utf8", "bad_json", "root_list", "backend_list", "backend_dict", "backend_null",
     "path_not_string", "locator_checksum"],
)
def test_r03_invalid_active_profile_fails_closed_before_any_output(
    backed_up, tmp_path, capsys, label: str
) -> None:
    profile, db, bundle = backed_up
    good = json.loads(profile.read_text())
    damaged = {
        "bad_utf8": b"\xff\xfe\x00bad",
        "bad_json": b"{",
        "root_list": b"[]",
        "backend_list": _tamper(profile, backend=["sqlite"]),
        "backend_dict": _tamper(profile, backend={"a": 1}),
        "backend_null": _tamper(profile, backend=None),
        "path_not_string": _tamper(profile, configuration={"path": 123}),
        "locator_checksum": _tamper(profile, locator_sha256="0" * 64),
    }[label]
    profile.write_bytes(damaged)
    assert good  # the fixture profile was valid before the damage
    fresh = tmp_path / "fresh"

    assert ops.main(_restore_args(bundle, fresh / "l3.db", fresh / "c.json")) == 2

    assert "storage profile" in _fail_json(capsys.readouterr().out)["error"]
    assert not fresh.exists()


def test_r03_real_cli_invalid_utf8_active_profile_is_machine_readable(backed_up, tmp_path) -> None:
    profile, _, bundle = backed_up
    profile.write_bytes(b"\xff\xfe\x00bad")
    fresh = tmp_path / "fresh"
    proc = _cli(_restore_args(bundle, fresh / "l3.db", fresh / "c.json"), profile)
    assert proc.returncode == 2 and "Traceback" not in proc.stderr
    assert "UnicodeDecodeError" in _fail_json(proc.stdout)["error"]
    assert not fresh.exists()


def test_r03_control_without_active_profile_and_with_neo4j_profile_restores(
    backed_up, tmp_path, monkeypatch, capsys
) -> None:
    profile, db, bundle = backed_up
    # No active profile deployed: nothing is protected, restore proceeds.
    absent = tmp_path / "no-such-profile.json"
    monkeypatch.setenv(ACTIVE_ENV, str(absent))
    first = tmp_path / "first"
    assert ops.main(_restore_args(bundle, first / "l3.db", first / "c.json")) == 0
    capsys.readouterr()
    # A non-file backend (neo4j) has no file locator to protect.
    neo = tmp_path / "neo.json"
    _write_profile(neo, db, backend="neo4j")
    monkeypatch.setenv(ACTIVE_ENV, str(neo))
    second = tmp_path / "second"
    assert ops.main(_restore_args(bundle, second / "l3.db", second / "c.json")) == 0


# ------------------------------------------------------------------------- R-04
def test_r04_backup_of_committed_wal_state_is_self_contained_and_restorable(
    backed_up, tmp_path, monkeypatch
) -> None:
    profile, db, _ = backed_up
    live = sqlite3.connect(db)
    try:
        assert live.execute("PRAGMA journal_mode=WAL").fetchone()[0] == "wal"
        live.execute("INSERT INTO meta VALUES('wal_probe', '73')")
        live.commit()
        # Precondition: copying only the main file loses the committed row, even
        # though integrity_check says ok. This is why content must be checked.
        main_only = tmp_path / "main_only.db"
        shutil.copyfile(db, main_only)
        lossy = sqlite3.connect(main_only)
        assert lossy.execute("SELECT COUNT(*) FROM meta WHERE key='wal_probe'").fetchone()[0] == 0
        assert lossy.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        lossy.close()

        bundle = tmp_path / "wal-bundle"
        backup.create_backup(bundle, profile_path=profile)
        assert sorted(p.name for p in bundle.iterdir()) == [
            "complete.json", "profile.json", "receipt.json", "storage.sqlite3",
        ]
        assert (bundle / "storage.sqlite3").read_bytes()[18:20] == b"\x01\x01"
        # Only the live source stays in WAL mode.
        assert live.execute("PRAGMA journal_mode").fetchone()[0] == "wal"

        moved = tmp_path / "moved"
        shutil.copytree(bundle, moved)
        before = _state(moved)
        backup.verify_backup(moved)
        assert _state(moved) == before

        monkeypatch.setenv(ACTIVE_ENV, str(profile))
        target = tmp_path / "restored" / "l3.db"
        restore.restore_backup(moved, target_database=target, target_profile=target.with_suffix(".json"))
    finally:
        live.close()
    check = sqlite3.connect(target)
    assert check.execute("SELECT value FROM meta WHERE key='wal_probe'").fetchone()[0] == "73"
    check.close()
    assert sorted(p.name for p in target.parent.iterdir()) == [
        "l3.db", "l3.json", "l3.json.restore-receipt.json",
    ]
    assert _state(moved) == before


def test_r04_backup_refuses_to_publish_when_snapshot_stays_in_wal_mode(
    store, tmp_path, monkeypatch
) -> None:
    profile, db = store
    real_connect = sqlite3.connect

    class StuckInWal(sqlite3.Connection):
        def execute(self, sql, *args):
            if sql == "PRAGMA journal_mode=DELETE":
                return super().execute("SELECT 'wal'")
            return super().execute(sql, *args)

    def fake_connect(*args, **kwargs):
        # The backup destination is the only plain, keyword-less connect.
        return real_connect(*args, factory=StuckInWal) if not kwargs else real_connect(*args, **kwargs)

    monkeypatch.setattr(sqlite3, "connect", fake_connect)
    bundle = tmp_path / "never-published"
    with pytest.raises(common.StorageOperationError, match="rollback-journal mode"):
        backup.create_backup(bundle, profile_path=profile)
    assert not bundle.exists()


def test_standalone_snapshot_contract_rejects_side_files_and_wal_header(tmp_path) -> None:
    snapshot = tmp_path / "snap.sqlite3"
    conn = sqlite3.connect(snapshot)
    conn.execute("CREATE TABLE t(x)")
    conn.commit()
    conn.close()
    common._require_standalone_snapshot(snapshot)  # valid: one rollback-journal file

    (tmp_path / "snap.sqlite3-shm").write_bytes(b"")
    with pytest.raises(common.StorageOperationError, match="not self-contained"):
        common._require_standalone_snapshot(snapshot)
    (tmp_path / "snap.sqlite3-shm").unlink()

    conn = sqlite3.connect(snapshot)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.close()
    with pytest.raises(common.StorageOperationError, match="rollback-journal mode"):
        common._require_standalone_snapshot(snapshot)


# ------------------------------------------------------------------------- R-05
def test_r05_legacy_wal_header_bundle_is_checked_on_a_copy_not_in_place(
    backed_up, tmp_path, monkeypatch
) -> None:
    profile, _, bundle = backed_up
    _legacy_wal_bundle(bundle)
    before = _state(bundle)
    opened: list[str] = []
    real_connect = sqlite3.connect

    def spy(database, *args, **kwargs):
        opened.append(str(database))
        return real_connect(database, *args, **kwargs)

    chmod_applied = os.geteuid() != 0
    if chmod_applied:  # a non-root OS enforces "no write into the bundle" too
        for path in bundle.iterdir():
            path.chmod(0o444)
        bundle.chmod(0o555)
    monkeypatch.setattr(sqlite3, "connect", spy)
    target = tmp_path / "restored" / "l3.db"
    try:
        backup.verify_backup(bundle)
        restore.restore_backup(bundle, target_database=target, target_profile=target.with_suffix(".json"))
    finally:
        monkeypatch.undo()
        if chmod_applied:
            bundle.chmod(0o755)
            for path in bundle.iterdir():
                path.chmod(0o644)

    assert opened and all(str(bundle) not in name for name in opened)
    assert all(str(target.parent) not in name for name in opened)
    assert _state(bundle) == before
    assert common._sha256_file(target) == common._sha256_file(bundle / "storage.sqlite3")
    assert sorted(p.name for p in target.parent.iterdir()) == [
        "l3.db", "l3.json", "l3.json.restore-receipt.json",
    ]


# ------------------------------------------------------------------------- R-06
@pytest.mark.parametrize("kind", ["wal", "journal", "directory", "symlink"])
def test_r06_bundle_with_unaccounted_journal_is_rejected_and_nothing_changes(
    backed_up, tmp_path, capsys, kind: str
) -> None:
    profile, _, bundle = backed_up
    side = bundle / ("storage.sqlite3-wal" if kind in {"wal", "symlink"} else "storage.sqlite3-journal")
    if kind == "directory":
        side.mkdir()
    elif kind == "symlink":
        (tmp_path / "elsewhere").write_bytes(b"")
        side.symlink_to(tmp_path / "elsewhere")
    else:
        side.write_bytes(b"x" * 64)
    before = _state(bundle)
    fresh = tmp_path / "fresh"

    assert ops.main(_restore_args(bundle, fresh / "l3.db", fresh / "c.json")) == 2

    assert "unaccounted SQLite" in _fail_json(capsys.readouterr().out)["error"]
    assert _state(bundle) == before and not fresh.exists()
    with pytest.raises(common.StorageOperationError, match="unaccounted SQLite"):
        backup.verify_backup(bundle)


# ------------------------------------------------------------------------- R-07
def _target_dir(tmp_path: Path) -> tuple[Path, Path, Path]:
    target_dir = tmp_path / "t"
    target_dir.mkdir()
    (target_dir / "alien.txt").write_bytes(b"keep me")
    return target_dir / "l3.db", target_dir / "c.json", target_dir


def test_r07_rollback_removes_only_attempt_artifacts_after_profile_write_failure(
    backed_up, tmp_path, monkeypatch
) -> None:
    _, _, bundle = backed_up
    db_t, prof_t, target_dir = _target_dir(tmp_path)
    real_write = restore._write_new_bytes

    def fail_profile(path, content, *args):
        if Path(path) == prof_t.resolve():
            raise OSError("disk full")
        return real_write(path, content, *args)

    monkeypatch.setattr(restore, "_write_new_bytes", fail_profile)
    with pytest.raises(common.StorageOperationError, match="cannot restore"):
        restore.restore_backup(bundle, target_database=db_t, target_profile=prof_t)
    # The receipt had already been written: it must be gone, the alien file kept.
    assert sorted(p.name for p in target_dir.iterdir()) == ["alien.txt"]
    assert (target_dir / "alien.txt").read_bytes() == b"keep me"


def test_r07_rollback_after_receipt_write_failure_leaves_no_files(
    backed_up, tmp_path, monkeypatch
) -> None:
    _, _, bundle = backed_up
    db_t, prof_t, target_dir = _target_dir(tmp_path)

    def fail_receipt(path, payload):
        raise OSError("receipt")

    monkeypatch.setattr(restore, "_write_new_json", fail_receipt)
    with pytest.raises(common.StorageOperationError, match="cannot restore"):
        restore.restore_backup(bundle, target_database=db_t, target_profile=prof_t)
    assert sorted(p.name for p in target_dir.iterdir()) == ["alien.txt"]


def test_r07_failed_cleanup_is_reported_not_hidden(backed_up, tmp_path, monkeypatch) -> None:
    _, _, bundle = backed_up
    db_t, prof_t, target_dir = _target_dir(tmp_path)
    real_write = restore._write_new_bytes
    real_unlink = Path.unlink

    def fail_profile(path, content, *args):
        if Path(path) == prof_t.resolve():
            raise OSError("disk full")
        return real_write(path, content, *args)

    def stuck_unlink(self, *args, **kwargs):
        if self == db_t.resolve():
            raise OSError("busy")
        return real_unlink(self, *args, **kwargs)

    monkeypatch.setattr(restore, "_write_new_bytes", fail_profile)
    monkeypatch.setattr(Path, "unlink", stuck_unlink)
    with pytest.raises(common.StorageOperationError, match="cleanup incomplete") as raised:
        restore.restore_backup(bundle, target_database=db_t, target_profile=prof_t)
    monkeypatch.undo()
    assert str(db_t.resolve()) in str(raised.value) and "disk full" in str(raised.value)
    # The other artifact was still removed; only the stuck one remains.
    assert sorted(p.name for p in target_dir.iterdir()) == ["alien.txt", "l3.db"]


# ------------------------------------------------------------------------- R-08
@pytest.mark.parametrize("suffix", ["-wal", "-shm", "-journal"])
def test_r08_occupied_sqlite_side_file_of_target_is_refused_and_preserved(
    backed_up, tmp_path, capsys, suffix: str
) -> None:
    _, _, bundle = backed_up
    db_t, prof_t, target_dir = _target_dir(tmp_path)
    side = Path(str(db_t) + suffix)
    side.write_bytes(b"someone else's data")
    before = _state(target_dir)

    assert ops.main(_restore_args(bundle, db_t, prof_t)) == 2

    assert "already exists" in _fail_json(capsys.readouterr().out)["error"]
    assert _state(target_dir) == before  # nothing created, nothing removed, bytes intact


# ------------------------------------------------------------------------- R-09
def _bad_utf8_bundle(bundle: Path, tmp_path: Path, name: str) -> Path:
    damaged = tmp_path / f"bad-{name}"
    shutil.copytree(bundle, damaged)
    (damaged / name).write_bytes(b"\xff\xfe\x00SECRET-MARKER")
    if name == common.BUNDLE_RECEIPT:
        # complete.json binds the receipt by SHA-256: refresh it so the check
        # reaches the decoding step instead of stopping at the hash mismatch.
        _refresh_completion(damaged)
    return damaged


@pytest.mark.parametrize(
    ("name", "label"),
    [("complete.json", "completion marker"), ("receipt.json", "backup receipt"),
     ("profile.json", "storage profile")],
)
def test_r09_real_cli_invalid_utf8_artifact_is_one_json_fail(backed_up, tmp_path, name, label) -> None:
    profile, _, bundle = backed_up
    damaged = _bad_utf8_bundle(bundle, tmp_path, name)
    before = _state(damaged)
    fresh = tmp_path / "fresh"
    proc = _cli(_restore_args(damaged, fresh / "l3.db", fresh / "c.json"), profile)
    assert proc.returncode == 2 and proc.stderr == "" and "Traceback" not in proc.stderr
    error = _fail_json(proc.stdout)["error"]
    assert label in error and "UnicodeDecodeError" in error
    assert "SECRET-MARKER" not in error and "0xff" not in error  # no artifact content
    assert not fresh.exists() and _state(damaged) == before


@pytest.mark.parametrize("name", ["complete.json", "receipt.json"])
def test_r09_invalid_utf8_artifact_raises_domain_error_in_process(backed_up, tmp_path, name) -> None:
    _, _, bundle = backed_up
    damaged = _bad_utf8_bundle(bundle, tmp_path, name)
    with pytest.raises(common.StorageOperationError, match="UnicodeDecodeError"):
        backup.verify_backup(damaged)


def test_sqlite_inspection_reports_missing_file_and_copy_failures(tmp_path, monkeypatch) -> None:
    with pytest.raises(common.StorageOperationError, match="does not exist"):
        common._sqlite_metrics(tmp_path / "missing.db")
    present = tmp_path / "present.db"
    _create_db(present)

    def broken_copy(*_args, **_kwargs):
        raise OSError("no space")

    monkeypatch.setattr(common.shutil, "copyfile", broken_copy)
    with pytest.raises(common.StorageOperationError, match="cannot inspect SQLite storage: no space"):
        common._sqlite_metrics(present)


# ------------------------------------------------------------------------- R-10
def test_r10_real_cli_end_to_end_restore_reads_data_and_does_not_activate(store, tmp_path) -> None:
    profile, db = store
    active_before = profile.read_bytes()
    bundle = tmp_path / "bundle"
    backed = _cli(["backup", str(bundle)], profile)
    assert backed.returncode == 0, backed.stderr
    target = tmp_path / "restored" / "l3.db"
    candidate = tmp_path / "restored" / "candidate.json"
    proc = _cli(_restore_args(bundle, target, candidate), profile)
    assert proc.returncode == 0 and proc.stderr == ""
    report = json.loads(proc.stdout)
    assert report["status"] == "PASS"
    assert report["receipt"]["activation"] == "candidate_profile_only"
    receipt = json.loads(Path(report["restore_receipt"]).read_text())
    assert receipt["target_database_sha256"] == common._sha256_file(target)

    check = sqlite3.connect(target)
    row = check.execute("SELECT data FROM nodes WHERE fact_id='f1'").fetchone()[0]
    check.close()
    assert json.loads(row)["claim"] == "claim 1"
    # Candidate points at the new file; the active profile and database are untouched.
    assert json.loads(candidate.read_text())["configuration"]["path"] == str(target.resolve())
    assert profile.read_bytes() == active_before
    assert json.loads(profile.read_text())["configuration"]["path"] == str(db.resolve())
    assert sorted(p.name for p in target.parent.iterdir()) == [
        "candidate.json", "candidate.json.restore-receipt.json", "l3.db",
    ]
