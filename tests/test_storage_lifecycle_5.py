from tests.storage_lifecycle_support import (
    Path, _copy_bundle, _create_db, _old_empty_lock, _profile_payload,
    _refresh_completion, _write_profile, backup, common, hashlib, io, json,
    lockmod, ops, os, pytest, restore, shutil, sqlite3, stat, store, time,
)

def test_verify_completion_marker_contract(
    store: tuple[Path, Path], tmp_path: Path
) -> None:
    profile, _ = store
    bundle = tmp_path / "base-completion"
    backup.create_backup(bundle, profile_path=profile)

    missing = _copy_bundle(bundle, tmp_path, "completion-missing")
    (missing / common.BUNDLE_COMPLETE).unlink()
    with pytest.raises(common.StorageOperationError, match="completion marker"):
        backup.verify_backup(missing)

    invalid = _copy_bundle(bundle, tmp_path, "completion-invalid")
    (invalid / common.BUNDLE_COMPLETE).write_text("{")
    with pytest.raises(common.StorageOperationError, match="valid backup completion"):
        backup.verify_backup(invalid)

    non_object = _copy_bundle(bundle, tmp_path, "completion-non-object")
    (non_object / common.BUNDLE_COMPLETE).write_text("[]")
    with pytest.raises(common.StorageOperationError, match="JSON object"):
        backup.verify_backup(non_object)

    cases = [
        ("schema_version", 99, "schema_version"),
        ("operation", "other", "operation"),
        ("receipt_file", "other.json", "receipt_file"),
    ]
    for index, (key, value, message) in enumerate(cases):
        altered = _copy_bundle(bundle, tmp_path, f"completion-{index}")
        complete_path = altered / common.BUNDLE_COMPLETE
        completion = json.loads(complete_path.read_text())
        completion[key] = value
        complete_path.write_text(json.dumps(completion))
        with pytest.raises(common.StorageOperationError, match=message):
            backup.verify_backup(altered)

    changed_receipt = _copy_bundle(bundle, tmp_path, "completion-hash")
    receipt_path = changed_receipt / common.BUNDLE_RECEIPT
    receipt = json.loads(receipt_path.read_text())
    receipt["created_at"] = "changed"
    receipt_path.write_text(json.dumps(receipt))
    with pytest.raises(common.StorageOperationError, match="receipt SHA-256"):
        backup.verify_backup(changed_receipt)


def test_restore_rejects_existing_or_overlapping_targets(store: tuple[Path, Path], tmp_path: Path) -> None:
    profile, _ = store
    bundle = tmp_path / "bundle"
    backup.create_backup(bundle, profile_path=profile)

    existing_db = tmp_path / "existing.db"
    existing_db.write_text("x")
    with pytest.raises(common.StorageOperationError, match="already exists"):
        restore.restore_backup(bundle, target_database=existing_db, target_profile=tmp_path / "p.json")

    existing_profile = tmp_path / "existing-profile.json"
    existing_profile.write_text("x")
    with pytest.raises(common.StorageOperationError, match="already exists"):
        restore.restore_backup(bundle, target_database=tmp_path / "new.db", target_profile=existing_profile)

    same = tmp_path / "same"
    with pytest.raises(common.StorageOperationError, match="must differ"):
        restore.restore_backup(bundle, target_database=same, target_profile=same)


def test_restore_cleanup_on_copy_metrics_hash_profile_and_write_failures(store: tuple[Path, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    profile, _ = store
    bundle = tmp_path / "bundle"
    backup.create_backup(bundle, profile_path=profile)

    target_db = tmp_path / "case1" / "db"
    target_profile = tmp_path / "case1" / "profile"
    monkeypatch.setattr(restore, "_copy_new_file", lambda *_: (_ for _ in ()).throw(OSError("copy")))
    with pytest.raises(common.StorageOperationError, match="cannot restore"):
        restore.restore_backup(bundle, target_database=target_db, target_profile=target_profile)
    assert not target_db.exists()
    monkeypatch.undo()

    target_db = tmp_path / "case2" / "db"
    target_profile = tmp_path / "case2" / "profile"
    real_metrics = restore._sqlite_metrics
    calls = 0
    def changed_counts(path):
        nonlocal calls
        calls += 1
        metrics = real_metrics(path)
        if calls >= 1:
            metrics["counts"] = dict(metrics["counts"], nodes=999)
        return metrics
    monkeypatch.setattr(restore, "_sqlite_metrics", changed_counts)
    with pytest.raises(common.StorageOperationError, match="table counts"):
        restore.restore_backup(bundle, target_database=target_db, target_profile=target_profile)
    assert not target_db.exists()
    monkeypatch.undo()

    target_db = tmp_path / "case3" / "db"
    target_profile = tmp_path / "case3" / "profile"
    real_sha = restore._sha256_file
    def changed_hash(path):
        if Path(path) == target_db.resolve():
            return "0" * 64
        return real_sha(Path(path))
    monkeypatch.setattr(restore, "_sha256_file", changed_hash)
    with pytest.raises(common.StorageOperationError, match="SHA-256"):
        restore.restore_backup(bundle, target_database=target_db, target_profile=target_profile)
    assert not target_db.exists()
    monkeypatch.undo()

    target_db = tmp_path / "case4" / "db"
    target_profile = tmp_path / "case4" / "profile"
    real_load = restore._load_profile
    def altered_profile(path):
        profile_value = real_load(path)
        if Path(path) == target_profile.resolve():
            return dict(profile_value, durable=False)
        return profile_value
    monkeypatch.setattr(restore, "_load_profile", altered_profile)
    with pytest.raises(common.StorageOperationError, match="validation changed"):
        restore.restore_backup(bundle, target_database=target_db, target_profile=target_profile)
    assert not target_db.exists() and not target_profile.exists()
    monkeypatch.undo()

    target_db = tmp_path / "case5" / "db"
    target_profile = tmp_path / "case5" / "profile"
    real_write = restore._write_new_json
    def fail_receipt(path, payload):
        if str(path).endswith(".restore-receipt.json"):
            raise OSError("receipt")
        return real_write(path, payload)
    monkeypatch.setattr(restore, "_write_new_json", fail_receipt)
    with pytest.raises(common.StorageOperationError, match="cannot restore"):
        restore.restore_backup(bundle, target_database=target_db, target_profile=target_profile)
    assert not target_db.exists() and not target_profile.exists()


def test_restore_rejects_active_profile_and_profile_path_errors(
    store: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile, _ = store
    bundle = tmp_path / "restore-active-bundle"
    backup.create_backup(bundle, profile_path=profile)

    active = tmp_path / "currently-active.json"
    monkeypatch.setattr(restore, "storage_profile_path", lambda: active.resolve())
    with pytest.raises(common.StorageOperationError, match="must not be the active"):
        restore.restore_backup(
            bundle,
            target_database=tmp_path / "active-db.sqlite",
            target_profile=active,
        )

    monkeypatch.setattr(
        restore,
        "storage_profile_path",
        lambda: (_ for _ in ()).throw(restore.StorageProfileError("bad profile path")),
    )
    with pytest.raises(common.StorageOperationError, match="bad profile path"):
        restore.restore_backup(
            bundle,
            target_database=tmp_path / "new-db.sqlite",
            target_profile=tmp_path / "new-profile.json",
        )


