from tests.storage_lifecycle_support import (
    Path, _copy_bundle, _create_db, _old_empty_lock, _profile_payload,
    _refresh_completion, _write_profile, backup, common, hashlib, io, json,
    lockmod, ops, os, pytest, restore, shutil, sqlite3, stat, store, time,
)

def test_backup_verify_restore_happy_path(store: tuple[Path, Path], tmp_path: Path) -> None:
    profile, source_db = store
    bundle = tmp_path / "backup"
    report = backup.create_backup(bundle, profile_path=profile)
    assert report["status"] == "PASS"
    assert report["receipt"]["sqlite"]["counts"]["nodes"] == 2
    assert source_db.exists()

    verified = backup.verify_backup(bundle)
    assert verified["status"] == "PASS"
    assert verified["sqlite"]["user_version"] == 7

    target_db = tmp_path / "restored" / "copy.db"
    target_profile = tmp_path / "restored" / "profile.json"
    restored = restore.restore_backup(
        bundle,
        target_database=target_db,
        target_profile=target_profile,
    )
    assert restored["status"] == "PASS"
    assert target_db.exists()
    assert target_profile.exists()
    receipt = Path(restored["restore_receipt"])
    assert receipt.exists()
    assert common._sqlite_metrics(target_db)["counts"] == verified["sqlite"]["counts"]
    assert json.loads(target_profile.read_text())["configuration"]["path"] == str(target_db.resolve())


def test_backup_rejects_existing_non_sqlite_and_missing_source(store: tuple[Path, Path], tmp_path: Path) -> None:
    profile, db = store
    existing = tmp_path / "exists"
    existing.mkdir()
    with pytest.raises(common.StorageOperationError, match="already exists"):
        backup.create_backup(existing, profile_path=profile)

    ladybug_profile = tmp_path / "ladybug.json"
    _write_profile(ladybug_profile, tmp_path / "ladybug", backend="ladybug")
    with pytest.raises(common.StorageOperationError, match="supports only"):
        backup.create_backup(tmp_path / "ladybug-backup", profile_path=ladybug_profile)

    db.unlink()
    with pytest.raises(common.StorageOperationError, match="regular file"):
        backup.create_backup(tmp_path / "missing-backup", profile_path=profile)


def test_backup_wraps_sqlite_and_publish_errors(store: tuple[Path, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    profile, _ = store
    class BrokenSource:
        def backup(self, _destination):
            raise sqlite3.Error("copy failed")
        def close(self):
            pass
    monkeypatch.setattr(backup, "_connect_readonly", lambda _path: BrokenSource())
    with pytest.raises(common.StorageOperationError, match="backup failed"):
        backup.create_backup(tmp_path / "broken-backup", profile_path=profile)
    assert not (tmp_path / "broken-backup").exists()

    # Restore real helper and force destination creation failure.
    monkeypatch.undo()
    real_connect = backup.sqlite3.connect

    def fail_destination(path, *args, **kwargs):
        if Path(path).name == common.BUNDLE_DATABASE:
            raise sqlite3.Error("destination failed")
        return real_connect(path, *args, **kwargs)

    monkeypatch.setattr(backup.sqlite3, "connect", fail_destination)
    with pytest.raises(common.StorageOperationError, match="backup database"):
        backup.create_backup(tmp_path / "destination-fail", profile_path=profile)
    assert not (tmp_path / "destination-fail").exists()


def test_verify_rejects_bundle_shape_and_receipt_fields(
    store: tuple[Path, Path], tmp_path: Path
) -> None:
    profile, _ = store
    bundle = tmp_path / "base"
    backup.create_backup(bundle, profile_path=profile)

    with pytest.raises(common.StorageOperationError, match="must be a directory"):
        backup.verify_backup(tmp_path / "missing")

    missing = _copy_bundle(bundle, tmp_path, "missing-file")
    (missing / common.BUNDLE_DATABASE).unlink()
    with pytest.raises(common.StorageOperationError, match="regular file"):
        backup.verify_backup(missing)

    invalid_json = _copy_bundle(bundle, tmp_path, "invalid-json")
    (invalid_json / common.BUNDLE_RECEIPT).write_text("{")
    _refresh_completion(invalid_json)
    with pytest.raises(common.StorageOperationError, match="valid backup receipt"):
        backup.verify_backup(invalid_json)

    non_object = _copy_bundle(bundle, tmp_path, "non-object")
    (non_object / common.BUNDLE_RECEIPT).write_text("[]")
    _refresh_completion(non_object)
    with pytest.raises(common.StorageOperationError, match="JSON object"):
        backup.verify_backup(non_object)

    mutations = [
        ("schema_version", 99, "schema_version"),
        ("operation", "other", "operation"),
        ("database_file", "wrong", "database_file"),
        ("profile_file", "wrong", "profile_file"),
    ]
    for index, (key, value, message) in enumerate(mutations):
        altered = _copy_bundle(bundle, tmp_path, f"receipt-{index}")
        receipt_path = altered / common.BUNDLE_RECEIPT
        receipt = json.loads(receipt_path.read_text())
        receipt[key] = value
        receipt_path.write_text(json.dumps(receipt))
        _refresh_completion(altered)
        with pytest.raises(common.StorageOperationError, match=message):
            backup.verify_backup(altered)


