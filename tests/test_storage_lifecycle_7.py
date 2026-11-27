from tests.storage_lifecycle_support import (
    Path, _copy_bundle, _create_db, _old_empty_lock, _profile_payload,
    _refresh_completion, _write_profile, backup, common, hashlib, io, json,
    lockmod, ops, os, pytest, restore, shutil, sqlite3, stat, store, time,
)

def test_recover_lock_guard_race_and_unlink_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    profile = tmp_path / "profile.json"
    report = _old_empty_lock(profile)
    guard = Path(report["lock_path"] + ".recovery")
    guard.write_text("busy")
    with pytest.raises(common.StorageOperationError, match="recovery guard"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    guard.unlink()

    real_snapshot = lockmod._lock_snapshot

    def changed_quarantine(path: Path):
        snapshot = real_snapshot(path)
        if path.name == "stale.lock" and snapshot is not None:
            return dict(snapshot, inode=snapshot["inode"] + 1)
        return snapshot

    monkeypatch.setattr(lockmod, "_lock_snapshot", changed_quarantine)
    with pytest.raises(common.StorageOperationError, match="changed during"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    assert Path(report["lock_path"]).exists()
    assert not guard.exists()
    monkeypatch.undo()

    report = lockmod.lock_report(profile_path=profile)
    real_unlink = Path.unlink

    def fail_lock_unlink(self, *args, **kwargs):
        if self == Path(report["lock_path"]):
            raise OSError("unlink failed")
        return real_unlink(self, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", fail_lock_unlink)
    with pytest.raises(common.StorageOperationError, match="cannot recover"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )


def test_recover_lock_does_not_unlink_a_new_writer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    profile = tmp_path / "profile.json"
    report = _old_empty_lock(profile)
    lock = Path(report["lock_path"])
    guard = Path(str(lock) + ".recovery")
    real_open = lockmod.os.open

    def writer_wins(path, flags, mode=0o777):
        if Path(path) == lock and flags & os.O_EXCL:
            writer_fd = real_open(path, flags, mode)
            os.close(writer_fd)
            raise FileExistsError("writer acquired lock")
        return real_open(path, flags, mode)

    monkeypatch.setattr(lockmod.os, "open", writer_wins)
    with pytest.raises(common.StorageOperationError, match="new writer acquired"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    assert lock.exists()
    assert lock.read_bytes() == b""
    assert not guard.exists()



def test_recover_lock_fails_closed_when_placeholder_identity_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    profile = tmp_path / "profile.json"
    report = _old_empty_lock(profile)
    real_snapshot = lockmod._lock_snapshot

    def changed_quarantine(path: Path):
        snapshot = real_snapshot(path)
        if path.name == "stale.lock" and snapshot is not None:
            return dict(snapshot, inode=snapshot["inode"] + 1)
        return snapshot

    monkeypatch.setattr(lockmod, "_lock_snapshot", changed_quarantine)
    monkeypatch.setattr(lockmod, "_path_matches_open_file", lambda *_args: False)
    with pytest.raises(common.StorageOperationError, match="placeholder changed"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    guard = Path(report["lock_path"] + ".recovery")
    assert guard.is_dir()
    assert (guard / "stale.lock").exists()


def test_recover_lock_fails_closed_when_release_placeholder_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    profile = tmp_path / "profile.json"
    report = _old_empty_lock(profile)
    monkeypatch.setattr(lockmod, "_path_matches_open_file", lambda *_args: False)
    with pytest.raises(common.StorageOperationError, match="placeholder changed"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    assert Path(report["lock_path"]).exists()


def test_path_matches_open_file_returns_false_on_stat_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "open-file"
    path.write_text("x")
    fd = os.open(path, os.O_RDONLY)
    try:
        monkeypatch.setattr(Path, "lstat", lambda _self: (_ for _ in ()).throw(OSError("stat failed")))
        assert lockmod._path_matches_open_file(path, fd) is False
    finally:
        os.close(fd)

def test_status_report_pass_warn_and_fail(store: tuple[Path, Path], tmp_path: Path) -> None:
    profile, db = store
    passed = lockmod.status_report(profile_path=profile)
    assert passed["status"] == "PASS"
    assert passed["operations"]["backup"] is True
    assert passed["operations"]["cross_backend_migration"] is False

    db.unlink()
    warned = lockmod.status_report(profile_path=profile)
    assert warned["status"] == "WARN"

    profile.write_text("{}")
    failed = lockmod.status_report(profile_path=profile)
    assert failed["status"] == "FAIL"

    # A non-regular lock is a hard failure even with a valid profile.
    _create_db(db)
    _write_profile(profile, db)
    target = tmp_path / "target"
    target.write_text("x")
    profile.with_name(f"{profile.name}.lock").symlink_to(target)
    failed_lock = lockmod.status_report(profile_path=profile)
    assert failed_lock["status"] == "FAIL"


def test_lock_snapshot_fail_closed_on_open_identity_and_read_races(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    profile = tmp_path / "lock-races.json"
    lock = profile.with_name(f"{profile.name}.lock")
    lock.write_bytes(b"")

    real_open = lockmod.os.open
    monkeypatch.setattr(
        lockmod.os,
        "open",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(FileNotFoundError()),
    )
    vanished = lockmod.lock_report(profile_path=profile)
    assert vanished["status"] == "PASS" and vanished["present"] is False
    monkeypatch.setattr(lockmod.os, "open", real_open)

    monkeypatch.setattr(
        lockmod.os,
        "open",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(PermissionError("denied")),
    )
    denied = lockmod.lock_report(profile_path=profile)
    assert denied["status"] == "FAIL" and "open lock" in denied["error"]
    monkeypatch.setattr(lockmod.os, "open", real_open)

    real_fstat = lockmod.os.fstat

    class ChangedIdentity:
        st_dev = -1
        st_ino = -1
        st_mode = stat.S_IFREG

    monkeypatch.setattr(lockmod.os, "fstat", lambda _fd: ChangedIdentity())
    changed = lockmod.lock_report(profile_path=profile)
    assert changed["status"] == "FAIL" and "identity changed" in changed["error"]
    monkeypatch.setattr(lockmod.os, "fstat", real_fstat)

    monkeypatch.setattr(
        lockmod.os,
        "read",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("read failed")),
    )
    unreadable = lockmod.lock_report(profile_path=profile)
    assert unreadable["status"] == "FAIL" and "read lock" in unreadable["error"]


@pytest.mark.parametrize("custom_receipt", [False, True], ids=["default", "custom"])
def test_restore_cli_writes_receipt(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    custom_receipt: bool,
) -> None:
    active_profile, _ = store
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(active_profile))
    bundle = tmp_path / "backup"
    backup.create_backup(bundle, profile_path=active_profile)
    # A sibling with the same name prefix is outside the source bundle.
    target_db = tmp_path / "backup-restored" / "l3.db"
    target_profile = target_db.with_suffix(".json")
    default_receipt = target_profile.with_name(
        f"{target_profile.name}.restore-receipt.json"
    )
    expected_receipt = default_receipt
    args = [
        "restore", str(bundle), "--target-database", str(target_db),
        "--target-profile", str(target_profile),
    ]
    if custom_receipt:
        monkeypatch.chdir(tmp_path)
        expected_receipt = tmp_path / "receipts" / "restore.json"
        args.extend(["--receipt", "receipts/restore.json"])

    assert ops.main(args) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "PASS"
    assert report["restore_receipt"] == str(expected_receipt)
    receipt = json.loads(expected_receipt.read_text())
    assert receipt == report["receipt"]
    assert receipt["activation"] == "candidate_profile_only"
    assert receipt["target_database_sha256"] == common._sha256_file(target_db)
    assert common._sqlite_metrics(target_db)["counts"]["nodes"] == 2
    assert json.loads(target_profile.read_text())["configuration"]["path"] == str(target_db)
    assert default_receipt.exists() is (not custom_receipt)


@pytest.mark.parametrize("receipt_target", ["existing", "active-profile"])
def test_restore_cli_rejects_unavailable_receipt_target(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    receipt_target: str,
) -> None:
    source_profile, _ = store
    bundle = tmp_path / "backup"
    backup.create_backup(bundle, profile_path=source_profile)
    receipt = tmp_path / "reserved.json"
    target_db = tmp_path / "candidate.db"
    target_profile = tmp_path / "candidate.json"
    if receipt_target == "existing":
        monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(source_profile))
        receipt.write_text("existing receipt")
        expected_error = "restore target already exists"
    else:
        monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", str(receipt))
        expected_error = "active storage profile"

    assert ops.main([
        "restore", str(bundle), "--target-database", str(target_db),
        "--target-profile", str(target_profile), "--receipt", str(receipt),
    ]) == 2
    assert expected_error in json.loads(capsys.readouterr().out)["error"]
    assert not target_db.exists() and not target_profile.exists()
    if receipt_target == "existing":
        assert receipt.read_text() == "existing receipt"
    else:
        assert not receipt.exists()


@pytest.mark.parametrize("existing", [False, True], ids=["dangling", "existing-file"])
def test_restore_cli_rejects_receipt_symlink(
    store: tuple[Path, Path],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    existing: bool,
) -> None:
    profile, _ = store
    bundle = tmp_path / "backup"
    backup.create_backup(bundle, profile_path=profile)
    destination = tmp_path / "destination.json"
    if existing:
        destination.write_text("original content")
    receipt = tmp_path / "receipt.json"
    receipt.symlink_to(destination)
    target_db = tmp_path / "candidate.db"
    target_profile = tmp_path / "candidate.json"

    assert ops.main([
        "restore", str(bundle), "--target-database", str(target_db),
        "--target-profile", str(target_profile), "--receipt", str(receipt),
    ]) == 2
    assert "symbolic link" in json.loads(capsys.readouterr().out)["error"]
    assert not target_db.exists() and not target_profile.exists()
    assert receipt.readlink() == destination
    if existing:
        assert destination.read_text() == "original content"
    else:
        assert not destination.exists()


@pytest.mark.parametrize("receipt_name", ["candidate.db", "candidate.json"])
def test_restore_cli_requires_distinct_receipt_target(
    store: tuple[Path, Path],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    receipt_name: str,
) -> None:
    profile, _ = store
    bundle = tmp_path / "backup"
    backup.create_backup(bundle, profile_path=profile)
    target_db = tmp_path / "candidate.db"
    target_profile = tmp_path / "candidate.json"

    assert ops.main([
        "restore", str(bundle), "--target-database", str(target_db),
        "--target-profile", str(target_profile), "--receipt", str(tmp_path / receipt_name),
    ]) == 2
    assert "targets must differ" in json.loads(capsys.readouterr().out)["error"]
    assert not target_db.exists() and not target_profile.exists()


@pytest.mark.parametrize("target_flag", ["--target-database", "--target-profile", "--receipt"])
def test_restore_cli_keeps_outputs_outside_source_bundle(
    store: tuple[Path, Path],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    target_flag: str,
) -> None:
    profile, _ = store
    bundle = tmp_path / "backup"
    backup.create_backup(bundle, profile_path=profile)
    before = {p.name: p.read_bytes() for p in bundle.iterdir()}
    bundle_alias = tmp_path / "same-backup"
    bundle_alias.symlink_to(bundle, target_is_directory=True)
    targets = {
        "--target-database": tmp_path / "candidate.db",
        "--target-profile": tmp_path / "candidate.json",
        "--receipt": tmp_path / "restore.json",
    }
    targets[target_flag] = bundle_alias / targets[target_flag].name
    args = ["restore", str(bundle)]
    for flag, path in targets.items():
        args.extend([flag, str(path)])

    assert ops.main(args) == 2
    assert "inside the source backup bundle" in json.loads(capsys.readouterr().out)["error"]
    assert all(not path.exists() for path in targets.values())
    assert {p.name: p.read_bytes() for p in bundle.iterdir()} == before


def test_main_dispatch_and_exit_codes(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(ops, "status_report", lambda **_k: {"status": "PASS", "kind": "status"})
    assert ops.main(["status"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "status"

    monkeypatch.setattr(ops, "create_backup", lambda *_a, **_k: {"status": "PASS", "kind": "backup"})
    assert ops.main(["backup", "out"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "backup"

    monkeypatch.setattr(ops, "verify_backup", lambda *_a, **_k: {"status": "PASS", "kind": "verify"})
    assert ops.main(["verify", "bundle"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "verify"

    monkeypatch.setattr(ops, "restore_backup", lambda *_a, **_k: {"status": "PASS", "kind": "restore"})
    assert ops.main(["restore", "bundle", "--target-database", "db", "--target-profile", "profile"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "restore"

    monkeypatch.setattr(ops, "lock_report", lambda **_k: {"status": "WARN", "kind": "inspect"})
    assert ops.main(["inspect-lock"]) == 1
    assert json.loads(capsys.readouterr().out)["kind"] == "inspect"

    monkeypatch.setattr(ops, "recover_stale_lock", lambda **_k: {"status": "PASS", "kind": "recover"})
    assert ops.main(["recover-lock", "--expected-mtime-ns", "1", "--expected-sha256", "x", "--confirm-no-writer"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "recover"

    monkeypatch.setattr(ops, "status_report", lambda **_k: {"status": "WARN"})
    assert ops.main(["status"]) == 1
    capsys.readouterr()

    monkeypatch.setattr(ops, "status_report", lambda **_k: (_ for _ in ()).throw(ops.StorageOperationError("bad")))
    assert ops.main(["status"]) == 2
    failure = json.loads(capsys.readouterr().out)
    assert failure["status"] == "FAIL" and failure["error"] == "bad"
