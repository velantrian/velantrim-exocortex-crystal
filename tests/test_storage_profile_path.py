"""Regression test for the default durable storage-profile location."""

from core.backend_profiles import PROFILE_PATH_ENV, storage_profile_path


def test_default_profile_path_is_stable_across_working_directories(
    monkeypatch, tmp_path
):
    home = tmp_path / "home"
    first_cwd = tmp_path / "first"
    second_cwd = tmp_path / "second"
    home.mkdir()
    first_cwd.mkdir()
    second_cwd.mkdir()

    monkeypatch.delenv(PROFILE_PATH_ENV, raising=False)
    monkeypatch.setenv("HOME", str(home))

    monkeypatch.chdir(first_cwd)
    first = storage_profile_path()
    monkeypatch.chdir(second_cwd)
    second = storage_profile_path()

    expected = home / ".velantrim" / "velantrim-storage-profile.json"
    assert first == expected
    assert second == expected
