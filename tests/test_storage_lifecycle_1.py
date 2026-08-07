from tests.storage_lifecycle_support import (
    Path, _copy_bundle, _create_db, _old_empty_lock, _profile_payload,
    _refresh_completion, _write_profile, backup, common, hashlib, io, json,
    lockmod, ops, os, pytest, restore, shutil, sqlite3, stat, store, time,
)

def test_profile_payload_for_sqlite_and_time(tmp_path: Path) -> None:
    payload = common._profile_payload_for_sqlite(tmp_path / "db.sqlite")
    assert payload["backend"] == "sqlite"
    assert payload["configuration"]["path"].endswith("db.sqlite")
    assert len(payload["locator_sha256"]) == 64
    assert common._utc_now().endswith("Z")


def test_fsync_directory_tolerates_open_and_fsync_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    real_open = os.open
    real_dup = os.dup
    monkeypatch.setattr(common.os, "open", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("no")))
    common._fsync_directory(tmp_path)

    monkeypatch.setattr(common.os, "open", real_open)
    fd = real_open(tmp_path, os.O_RDONLY)
    monkeypatch.setattr(common.os, "open", lambda *args, **kwargs: real_dup(fd))
    monkeypatch.setattr(common.os, "fsync", lambda *_: (_ for _ in ()).throw(OSError("unsupported")))
    common._fsync_directory(tmp_path)
    os.close(fd)


def test_write_and_copy_new_files_refuse_overwrite_and_cleanup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "new.bin"
    common._write_new_bytes(target, b"abc")
    assert target.read_bytes() == b"abc"
    with pytest.raises(FileExistsError):
        common._write_new_bytes(target, b"def")

    source = tmp_path / "source.bin"
    source.write_bytes(b"payload")
    copied = tmp_path / "copied.bin"
    common._copy_new_file(source, copied)
    assert copied.read_bytes() == b"payload"
    with pytest.raises(FileExistsError):
        common._copy_new_file(source, copied)

    broken = tmp_path / "broken.bin"
    class BrokenWriter(io.BytesIO):
        def write(self, _value):
            raise OSError("write failed")
    real_fdopen = common.os.fdopen
    monkeypatch.setattr(common.os, "fdopen", lambda *args, **kwargs: BrokenWriter())
    with pytest.raises(OSError, match="write failed"):
        common._write_new_bytes(broken, b"x")
    assert not broken.exists()
    monkeypatch.setattr(common.os, "fdopen", real_fdopen)


def test_load_profile_defensive_none(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(common, "load_storage_profile", lambda *_args, **_kwargs: None)
    with pytest.raises(common.StorageOperationError, match="not found"):
        common._load_profile(tmp_path / "none.json")


