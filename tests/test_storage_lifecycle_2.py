from tests.storage_lifecycle_support import (
    Path, _copy_bundle, _create_db, _old_empty_lock, _profile_payload,
    _refresh_completion, _write_profile, backup, common, hashlib, io, json,
    lockmod, ops, os, pytest, restore, shutil, sqlite3, stat, store, time,
)

def test_sqlite_locator_rejections(tmp_path: Path) -> None:
    with pytest.raises(common.StorageOperationError, match="supports only"):
        common._sqlite_locator({"backend": "ladybug"})
    with pytest.raises(common.StorageOperationError, match="configuration"):
        common._sqlite_locator({"backend": "sqlite", "configuration": None})
    for raw in (None, "", ":memory:"):
        with pytest.raises(common.StorageOperationError, match="durable file"):
            common._sqlite_locator({"backend": "sqlite", "configuration": {"path": raw}})


def test_connect_and_metrics_rejections(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(common.StorageOperationError, match="does not exist"):
        common._connect_readonly(tmp_path / "missing.db")

    bad = tmp_path / "bad.db"
    bad.write_text("not sqlite")
    with pytest.raises(common.StorageOperationError, match="inspect SQLite"):
        common._sqlite_metrics(bad)

    incomplete = tmp_path / "incomplete.db"
    sqlite3.connect(incomplete).close()
    with pytest.raises(common.StorageOperationError, match="missing required tables"):
        common._sqlite_metrics(incomplete)

    db = tmp_path / "valid.db"
    _create_db(db)
    real_connect = common.sqlite3.connect
    monkeypatch.setattr(common.sqlite3, "connect", lambda *_a, **_k: (_ for _ in ()).throw(sqlite3.Error("open failed")))
    with pytest.raises(common.StorageOperationError, match="cannot open"):
        common._connect_readonly(db)
    monkeypatch.setattr(common.sqlite3, "connect", real_connect)


def test_copy_new_file_cleans_target_when_source_read_fails(tmp_path: Path) -> None:
    source_directory = tmp_path / "source-directory"
    source_directory.mkdir()
    target = tmp_path / "target.bin"
    with pytest.raises(IsADirectoryError):
        common._copy_new_file(source_directory, target)
    assert not target.exists()


def test_sqlite_metrics_rejects_failed_integrity_check(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    database = tmp_path / "database.sqlite"
    database.write_bytes(b"placeholder")

    class BrokenIntegrityConnection:
        def execute(self, statement: str):
            assert statement == "PRAGMA integrity_check"
            return [("database disk image is malformed",)]

        def close(self) -> None:
            pass

    monkeypatch.setattr(
        common,
        "_connect_readonly",
        lambda _path: BrokenIntegrityConnection(),
    )
    with pytest.raises(common.StorageOperationError, match="integrity_check failed"):
        common._sqlite_metrics(database)


