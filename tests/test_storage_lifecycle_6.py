from tests.storage_lifecycle_support import (
    Path, _copy_bundle, _create_db, _old_empty_lock, _profile_payload,
    _refresh_completion, _write_profile, backup, common, hashlib, io, json,
    lockmod, ops, os, pytest, restore, shutil, sqlite3, stat, store, time,
)

def test_restore_detects_profile_hash_change(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile, _ = store
    bundle = tmp_path / "restore-profile-hash-bundle"
    backup.create_backup(bundle, profile_path=profile)
    target_db = (tmp_path / "hash-target" / "db.sqlite").resolve()
    target_profile = (tmp_path / "hash-target" / "profile.json").resolve()
    real_sha = restore._sha256_file

    def changed_profile_hash(path: Path) -> str:
        resolved = Path(path).resolve()
        if resolved == target_profile:
            return "0" * 64
        return real_sha(Path(path))

    monkeypatch.setattr(restore, "_sha256_file", changed_profile_hash)
    with pytest.raises(common.StorageOperationError, match="profile SHA-256"):
        restore.restore_backup(
            bundle,
            target_database=target_db,
            target_profile=target_profile,
        )
    assert not target_db.exists()
    assert not target_profile.exists()


def test_lock_report_absent_regular_and_symlink(tmp_path: Path) -> None:
    profile = tmp_path / "profile.json"
    absent = lockmod.lock_report(profile_path=profile)
    assert absent["status"] == "PASS" and absent["present"] is False

    lock = tmp_path / "profile.json.lock"
    lock.write_bytes(b"")
    old = time.time() - 10
    os.utime(lock, (old, old))
    regular = lockmod.lock_report(profile_path=profile)
    assert regular["status"] == "WARN"
    assert regular["present"] and regular["regular_file"]
    assert regular["sha256"] == hashlib.sha256(b"").hexdigest()

    lock.write_bytes(b"lock metadata")
    nonempty = lockmod.lock_report(profile_path=profile)
    assert nonempty["sha256"] == hashlib.sha256(b"lock metadata").hexdigest()

    lock.unlink()
    target = tmp_path / "target"
    target.write_text("x")
    lock.symlink_to(target)
    linked = lockmod.lock_report(profile_path=profile)
    assert linked["status"] == "FAIL"
    assert linked["sha256"] is None


def test_recover_lock_happy_path(tmp_path: Path) -> None:
    profile = tmp_path / "profile.json"
    report = _old_empty_lock(profile)
    recovered = lockmod.recover_stale_lock(
        profile_path=profile,
        expected_mtime_ns=report["mtime_ns"],
        expected_sha256=report["sha256"],
        min_age_seconds=300,
        confirm_no_writer=True,
    )
    assert recovered["status"] == "PASS"
    assert not Path(recovered["removed_lock"]).exists()
    assert not Path(str(recovered["removed_lock"]) + ".recovery").exists()


def test_recover_lock_rejections(tmp_path: Path) -> None:
    profile = tmp_path / "profile.json"
    with pytest.raises(common.StorageOperationError, match="confirm"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=1,
            expected_sha256="x",
        )
    with pytest.raises(common.StorageOperationError, match="non-negative"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=1,
            expected_sha256="x",
            min_age_seconds=-1,
            confirm_no_writer=True,
        )
    with pytest.raises(common.StorageOperationError, match="does not exist"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=1,
            expected_sha256="x",
            min_age_seconds=0,
            confirm_no_writer=True,
        )

    lock = profile.with_name(f"{profile.name}.lock")
    target = tmp_path / "target"
    target.write_text("x")
    lock.symlink_to(target)
    with pytest.raises(common.StorageOperationError, match="regular file"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=lock.lstat().st_mtime_ns,
            expected_sha256="x",
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    lock.unlink()

    lock.write_text("metadata")
    report = lockmod.lock_report(profile_path=profile)
    with pytest.raises(common.StorageOperationError, match="legacy empty"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    lock.unlink()

    lock.write_bytes(b"")
    report = lockmod.lock_report(profile_path=profile)
    with pytest.raises(common.StorageOperationError, match="newer"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256=report["sha256"],
            min_age_seconds=999,
            confirm_no_writer=True,
        )
    old = time.time() - 600
    os.utime(lock, (old, old))
    report = lockmod.lock_report(profile_path=profile)
    with pytest.raises(common.StorageOperationError, match="mtime changed"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"] + 1,
            expected_sha256=report["sha256"],
            min_age_seconds=0,
            confirm_no_writer=True,
        )
    with pytest.raises(common.StorageOperationError, match="SHA-256 changed"):
        lockmod.recover_stale_lock(
            profile_path=profile,
            expected_mtime_ns=report["mtime_ns"],
            expected_sha256="0" * 64,
            min_age_seconds=0,
            confirm_no_writer=True,
        )


