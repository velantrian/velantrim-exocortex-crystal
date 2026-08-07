"""Storage-profile locking and fail-closed L3 selection tests."""

import os

import pytest

from core import backend_profiles as profiles
from core.backend_profiles import (
    BackendSelection,
    StorageProfileError,
    finalize_backend_selection,
    load_storage_profile,
    resolve_backend_selection,
    storage_profile_path,
    temporary_environment,
)


def _select_sqlite(monkeypatch, tmp_path):
    import core.l3_graph as l3

    l3.reset_l3_graph()
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "l3.db"))

    def no_ladybug(*args, **kwargs):
        raise RuntimeError("ladybug unavailable")

    monkeypatch.setattr(l3, "LadybugL3Graph", no_ladybug)
    graph = l3.get_l3_graph()
    return l3, graph


def test_auto_selection_is_locked_across_registry_resets(monkeypatch, tmp_path):
    l3, graph = _select_sqlite(monkeypatch, tmp_path)
    assert isinstance(graph, l3.SqliteL3Graph)

    profile = load_storage_profile(required=True)
    assert profile["backend"] == "sqlite"
    assert profile["configuration"]["path"] == str((tmp_path / "l3.db").resolve())

    l3.reset_l3_graph()

    def must_not_probe_ladybug(*args, **kwargs):
        raise AssertionError("locked profile must bypass auto probing")

    monkeypatch.setattr(l3, "LadybugL3Graph", must_not_probe_ladybug)
    restarted = l3.get_l3_graph()
    assert isinstance(restarted, l3.SqliteL3Graph)


def test_locked_backend_rejects_backend_and_locator_drift(monkeypatch, tmp_path):
    l3, _ = _select_sqlite(monkeypatch, tmp_path)
    l3.reset_l3_graph()

    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "ladybug")
    with pytest.raises(StorageProfileError, match="conflicts with locked backend"):
        l3.get_l3_graph()

    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "other.db"))
    with pytest.raises(StorageProfileError, match="L3_PATH conflicts"):
        l3.get_l3_graph()


def test_auto_selection_never_silently_uses_mock(monkeypatch):
    import core.l3_graph as l3

    l3.reset_l3_graph()
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")

    def unavailable(*args, **kwargs):
        raise RuntimeError("backend unavailable")

    monkeypatch.setattr(l3, "LadybugL3Graph", unavailable)
    monkeypatch.setattr(l3, "SqliteL3Graph", unavailable)

    with pytest.raises(StorageProfileError, match="ephemeral Mock"):
        l3.get_l3_graph()
    assert not storage_profile_path().exists()


def test_explicit_mock_remains_available_without_a_profile(monkeypatch):
    import core.l3_graph as l3

    l3.reset_l3_graph()
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "mock")
    assert isinstance(l3.get_l3_graph(), l3.MockL3Graph)
    assert not storage_profile_path().exists()


def test_programmatic_explicit_backend_bypasses_runtime_profile(monkeypatch, tmp_path):
    l3, _ = _select_sqlite(monkeypatch, tmp_path)
    isolated = l3.get_l3_graph(backend="mock")
    assert isinstance(isolated, l3.MockL3Graph)
    assert load_storage_profile(required=True)["backend"] == "sqlite"


def test_malformed_profile_fails_closed(monkeypatch):
    import core.l3_graph as l3

    storage_profile_path().parent.mkdir(parents=True, exist_ok=True)
    storage_profile_path().write_text("{", encoding="utf-8")
    l3.reset_l3_graph()
    with pytest.raises(StorageProfileError, match="cannot read valid"):
        l3.get_l3_graph()


@pytest.mark.parametrize(
    "raw, message",
    [
        ([], "JSON object"),
        ({"schema_version": 2}, "schema_version"),
        ({"schema_version": 1, "profile": "other"}, "profile='l3'"),
        (
            {
                "schema_version": 1,
                "profile": "l3",
                "backend": "mock",
                "durable": True,
                "configuration": {},
                "locator_sha256": "x",
            },
            "durable and supported",
        ),
        (
            {
                "schema_version": 1,
                "profile": "l3",
                "backend": "sqlite",
                "durable": False,
                "configuration": {"path": "/tmp/a"},
                "locator_sha256": "x",
            },
            "durable=true",
        ),
        (
            {
                "schema_version": 1,
                "profile": "l3",
                "backend": "sqlite",
                "durable": True,
                "configuration": "bad",
                "locator_sha256": "x",
            },
            "configuration must be an object",
        ),
        (
            {
                "schema_version": 1,
                "profile": "l3",
                "backend": "sqlite",
                "durable": True,
                "configuration": {"wrong": "x"},
                "locator_sha256": "x",
            },
            "requires one string path",
        ),
        (
            {
                "schema_version": 1,
                "profile": "l3",
                "backend": "sqlite",
                "durable": True,
                "configuration": {"path": ":memory:"},
                "locator_sha256": "x",
            },
            "must be persistent",
        ),
        (
            {
                "schema_version": 1,
                "profile": "l3",
                "backend": "neo4j",
                "durable": True,
                "configuration": {"uri": "", "database": "neo4j"},
                "locator_sha256": "x",
            },
            "requires non-empty uri",
        ),
    ],
)
def test_profile_validation_rejects_invalid_shapes(raw, message):
    with pytest.raises(StorageProfileError, match=message):
        profiles._validate_profile(raw)


def test_profile_validation_rejects_bad_checksum(tmp_path):
    profile = profiles._build_profile("sqlite", {"path": str(tmp_path / "l3.db")})
    profile["locator_sha256"] = "0" * 64
    with pytest.raises(StorageProfileError, match="checksum mismatch"):
        profiles._validate_profile(profile)


def test_profile_helpers_cover_supported_configurations(monkeypatch, tmp_path):
    monkeypatch.setenv("VELANTRIM_L3_PATH", ":memory:")
    assert profiles._configuration_for_backend("sqlite") == {"path": ":memory:"}
    assert not profiles._is_durable("sqlite", {"path": ":memory:"})

    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "graph.lbug"))
    local = profiles._configuration_for_backend("ladybug")
    assert local == {"path": str((tmp_path / "graph.lbug").resolve())}
    assert profiles._is_durable("ladybug", local)

    monkeypatch.setenv("NEO4J_URI", "bolt://db:7687")
    monkeypatch.setenv("NEO4J_DATABASE", "crystal")
    server = profiles._configuration_for_backend("neo4j")
    assert server == {"uri": "bolt://db:7687", "database": "crystal"}
    assert profiles._is_durable("neo4j", server)
    assert profiles._configuration_for_backend("mock") == {}
    assert not profiles._is_durable("mock", {})

    with pytest.raises(StorageProfileError, match="unsupported"):
        profiles._configuration_for_backend("future")


def test_environment_projection_and_restoration(monkeypatch):
    monkeypatch.setenv("NEO4J_URI", "before")
    server_profile = profiles._build_profile(
        "neo4j", {"uri": "bolt://locked:7687", "database": "crystal"}
    )
    overrides = profiles._environment_for_profile(server_profile)
    assert overrides["NEO4J_DATABASE"] == "crystal"

    with temporary_environment(overrides):
        assert os.environ["NEO4J_URI"] == "bolt://locked:7687"
        assert os.environ["NEO4J_DATABASE"] == "crystal"

    assert os.environ["NEO4J_URI"] == "before"
    assert "NEO4J_DATABASE" not in os.environ

    local_profile = profiles._build_profile("sqlite", {"path": "/tmp/locked.db"})
    assert profiles._environment_for_profile(local_profile) == {
        "VELANTRIM_L3_PATH": "/tmp/locked.db"
    }
    with pytest.raises(StorageProfileError, match="cannot apply"):
        profiles._environment_for_profile(
            {"backend": "mock", "configuration": {}}
        )


def test_neo4j_explicit_environment_conflicts_fail_closed(monkeypatch, tmp_path):
    profile = profiles._build_profile(
        "neo4j", {"uri": "bolt://locked:7687", "database": "crystal"}
    )
    profiles._persist_profile_if_absent(profile, storage_profile_path())

    monkeypatch.setenv("NEO4J_URI", "bolt://other:7687")
    with pytest.raises(StorageProfileError, match="NEO4J_URI conflicts"):
        resolve_backend_selection("VELANTRIM_L3_BACKEND", "auto")

    monkeypatch.setenv("NEO4J_URI", "bolt://locked:7687")
    monkeypatch.setenv("NEO4J_DATABASE", "other")
    with pytest.raises(StorageProfileError, match="NEO4J_DATABASE conflicts"):
        resolve_backend_selection("VELANTRIM_L3_BACKEND", "auto")


def test_non_l3_registry_selection_is_pass_through():
    selection = resolve_backend_selection("OTHER_BACKEND", "auto")
    assert selection.effective_name == "auto"
    assert selection.profile_path is None
    assert finalize_backend_selection(selection, object()) is None


def test_unknown_instance_and_missing_profile_path_fail_closed(monkeypatch, tmp_path):
    with pytest.raises(StorageProfileError, match="cannot identify"):
        profiles._backend_from_instance(object())

    class SqliteL3Graph:
        pass

    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "l3.db"))
    selection = BackendSelection(
        "VELANTRIM_L3_BACKEND",
        "sqlite",
        "sqlite",
        None,
        None,
        {},
    )
    with pytest.raises(StorageProfileError, match="missing storage profile path"):
        finalize_backend_selection(selection, SqliteL3Graph())


def test_finalize_rejects_constructed_backend_or_locator_mismatch(
    monkeypatch, tmp_path
):
    class SqliteL3Graph:
        pass

    class LadybugL3Graph:
        pass

    locked_path = str((tmp_path / "locked.db").resolve())
    profile = profiles._build_profile("sqlite", {"path": locked_path})
    selection = BackendSelection(
        "VELANTRIM_L3_BACKEND",
        "auto",
        "sqlite",
        storage_profile_path(),
        profile,
        {"VELANTRIM_L3_PATH": locked_path},
    )

    monkeypatch.setenv("VELANTRIM_L3_PATH", locked_path)
    with pytest.raises(StorageProfileError, match="constructed backend"):
        finalize_backend_selection(selection, LadybugL3Graph())

    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "other.db"))
    with pytest.raises(StorageProfileError, match="constructed backend locator"):
        finalize_backend_selection(selection, SqliteL3Graph())


def test_explicit_ephemeral_sqlite_is_allowed_without_lock(monkeypatch):
    class SqliteL3Graph:
        pass

    monkeypatch.setenv("VELANTRIM_L3_PATH", ":memory:")
    selection = BackendSelection(
        "VELANTRIM_L3_BACKEND",
        "sqlite",
        "sqlite",
        storage_profile_path(),
        None,
        {},
    )
    assert finalize_backend_selection(selection, SqliteL3Graph()) is None


def test_auto_ephemeral_sqlite_fails_closed(monkeypatch):
    class SqliteL3Graph:
        pass

    monkeypatch.setenv("VELANTRIM_L3_PATH", ":memory:")
    selection = BackendSelection(
        "VELANTRIM_L3_BACKEND",
        "auto",
        "auto",
        storage_profile_path(),
        None,
        {},
    )
    with pytest.raises(StorageProfileError, match="ephemeral storage locator"):
        finalize_backend_selection(selection, SqliteL3Graph())


def test_profile_persistence_is_idempotent_and_rejects_race_mismatch(tmp_path):
    path = tmp_path / "profile.json"
    first = profiles._build_profile("sqlite", {"path": str(tmp_path / "one.db")})
    assert profiles._persist_profile_if_absent(first, path) == first
    assert profiles._persist_profile_if_absent(first, path) == first

    second = profiles._build_profile("sqlite", {"path": str(tmp_path / "two.db")})
    with pytest.raises(StorageProfileError, match="another process locked"):
        profiles._persist_profile_if_absent(second, path)


def test_profile_lock_retries_once(monkeypatch, tmp_path):
    real_open = profiles.os.open
    calls = {"count": 0}

    def flaky_open(path, flags, mode=0o777):
        calls["count"] += 1
        if calls["count"] == 1:
            raise FileExistsError
        return real_open(path, flags, mode)

    monkeypatch.setattr(profiles.os, "open", flaky_open)
    monkeypatch.setattr(profiles.time, "sleep", lambda _: None)
    lock_path = tmp_path / "profile.lock"
    fd = profiles._acquire_profile_lock(lock_path)
    os.close(fd)
    lock_path.unlink()
    assert calls["count"] == 2


def test_required_and_unreadable_profiles_fail_closed(tmp_path):
    missing = tmp_path / "missing.json"
    with pytest.raises(StorageProfileError, match="not found"):
        load_storage_profile(missing, required=True)

    directory = tmp_path / "directory"
    directory.mkdir()
    with pytest.raises(StorageProfileError, match="cannot read valid"):
        load_storage_profile(directory)


def test_empty_profile_path_is_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", " ")
    with pytest.raises(StorageProfileError, match="must not be empty"):
        storage_profile_path()


def test_registry_closes_candidate_when_profile_finalization_fails(
    monkeypatch, tmp_path
):
    from core._registry import BackendRegistry

    closed = {"value": False}

    class SqliteL3Graph:
        def close(self):
            closed["value"] = True

    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")
    monkeypatch.setenv("VELANTRIM_L3_PATH", ":memory:")
    registry = BackendRegistry(
        "VELANTRIM_L3_BACKEND",
        "auto",
        lambda name: SqliteL3Graph(),
    )
    with pytest.raises(StorageProfileError, match="ephemeral storage locator"):
        registry.get()
    assert closed["value"]


def test_profile_persistence_cleans_temp_file_on_replace_failure(
    monkeypatch, tmp_path
):
    path = tmp_path / "profile.json"
    profile = profiles._build_profile(
        "sqlite", {"path": str(tmp_path / "l3.db")}
    )

    def fail_replace(source, destination):
        raise OSError("replace failed")

    monkeypatch.setattr(profiles.os, "replace", fail_replace)
    with pytest.raises(StorageProfileError, match="cannot persist storage profile"):
        profiles._persist_profile_if_absent(profile, path)

    assert not path.exists()
    assert not path.with_name(f"{path.name}.lock").exists()
    assert list(tmp_path.glob(f".{path.name}.*.tmp")) == []


def test_registry_reuses_cached_instance_and_reset_swallows_close_error(
    monkeypatch,
):
    from core._registry import BackendRegistry

    class Backend:
        def close(self):
            raise RuntimeError("close failed")

    monkeypatch.setenv("OTHER_BACKEND", "one")
    registry = BackendRegistry("OTHER_BACKEND", "default", lambda name: Backend())
    first = registry.get()
    assert registry.get() is first
    registry.reset()
    assert registry.get() is not first
