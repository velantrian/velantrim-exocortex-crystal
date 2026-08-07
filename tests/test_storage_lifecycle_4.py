from tests.storage_lifecycle_support import (
    Path, _copy_bundle, _create_db, _old_empty_lock, _profile_payload,
    _refresh_completion, _write_profile, backup, common, hashlib, io, json,
    lockmod, ops, os, pytest, restore, shutil, sqlite3, stat, store, time,
)

def test_verify_rejects_hash_size_locator_and_metrics_mismatch(
    store: tuple[Path, Path], tmp_path: Path
) -> None:
    profile, _ = store
    bundle = tmp_path / "base"
    backup.create_backup(bundle, profile_path=profile)

    cases = [
        ("source_database_path", "/wrong/path", "source database path"),
        ("source_locator_sha256", "0" * 64, "locator"),
        ("database_sha256", "0" * 64, "SHA-256"),
        ("database_size", -1, "size"),
        ("profile_sha256", "0" * 64, "profile SHA"),
    ]
    for index, (key, value, message) in enumerate(cases):
        altered = _copy_bundle(bundle, tmp_path, f"integrity-{index}")
        receipt_path = altered / common.BUNDLE_RECEIPT
        receipt = json.loads(receipt_path.read_text())
        receipt[key] = value
        receipt_path.write_text(json.dumps(receipt))
        _refresh_completion(altered)
        with pytest.raises(common.StorageOperationError, match=message):
            backup.verify_backup(altered)

    metrics_type = _copy_bundle(bundle, tmp_path, "metrics-type")
    receipt_path = metrics_type / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_text())
    receipt["sqlite"] = None
    receipt_path.write_text(json.dumps(receipt))
    _refresh_completion(metrics_type)
    with pytest.raises(common.StorageOperationError, match="metrics"):
        backup.verify_backup(metrics_type)

    counts = _copy_bundle(bundle, tmp_path, "counts")
    receipt_path = counts / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_text())
    receipt["sqlite"]["counts"]["nodes"] += 1
    receipt_path.write_text(json.dumps(receipt))
    _refresh_completion(counts)
    with pytest.raises(common.StorageOperationError, match="table counts"):
        backup.verify_backup(counts)

    user_version = _copy_bundle(bundle, tmp_path, "user-version")
    receipt_path = user_version / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_text())
    receipt["sqlite"]["user_version"] += 1
    receipt_path.write_text(json.dumps(receipt))
    _refresh_completion(user_version)
    with pytest.raises(common.StorageOperationError, match="user_version"):
        backup.verify_backup(user_version)


def test_verify_rejects_invalid_bundle_profile_and_database(
    store: tuple[Path, Path], tmp_path: Path
) -> None:
    profile, _ = store
    bundle = tmp_path / "base"
    backup.create_backup(bundle, profile_path=profile)

    invalid_profile = _copy_bundle(bundle, tmp_path, "invalid-profile")
    profile_path = invalid_profile / common.BUNDLE_PROFILE
    profile_path.write_text("{}")
    receipt_path = invalid_profile / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_text())
    receipt["profile_sha256"] = common._sha256_file(profile_path)
    receipt_path.write_text(json.dumps(receipt))
    _refresh_completion(invalid_profile)
    with pytest.raises(common.StorageOperationError, match="schema_version"):
        backup.verify_backup(invalid_profile)

    broken_db = _copy_bundle(bundle, tmp_path, "broken-db")
    db_path = broken_db / common.BUNDLE_DATABASE
    db_path.write_text("broken")
    receipt_path = broken_db / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_text())
    receipt["database_sha256"] = common._sha256_file(db_path)
    receipt["database_size"] = db_path.stat().st_size
    receipt_path.write_text(json.dumps(receipt))
    _refresh_completion(broken_db)
    with pytest.raises(common.StorageOperationError, match="inspect SQLite"):
        backup.verify_backup(broken_db)


def test_backup_removes_published_bundle_when_self_verification_fails(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile, _ = store
    output = tmp_path / "self-verify-failure"
    monkeypatch.setattr(
        backup,
        "verify_backup",
        lambda _path: (_ for _ in ()).throw(
            common.StorageOperationError("self verification failed")
        ),
    )
    with pytest.raises(common.StorageOperationError, match="self verification"):
        backup.create_backup(output, profile_path=profile)
    assert not output.exists()


def test_backup_rejects_dangling_symlink_and_wraps_creation_or_write_errors(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile, _ = store

    dangling = tmp_path / "dangling"
    dangling.symlink_to(tmp_path / "missing-target", target_is_directory=True)
    with pytest.raises(common.StorageOperationError, match="symbolic link"):
        backup.create_backup(dangling, profile_path=profile)

    blocked_parent = tmp_path / "blocked"
    blocked_parent.write_text("not a directory")
    with pytest.raises(common.StorageOperationError, match="cannot create"):
        backup.create_backup(blocked_parent / "bundle", profile_path=profile)

    output = tmp_path / "chmod-failure"
    monkeypatch.setattr(
        backup.os,
        "chmod",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("chmod failed")),
    )
    with pytest.raises(common.StorageOperationError, match="cannot create"):
        backup.create_backup(output, profile_path=profile)
    assert not output.exists()


