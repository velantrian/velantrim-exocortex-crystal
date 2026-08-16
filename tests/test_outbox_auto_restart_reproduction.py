"""Adversarial reproduction/regression for Outbox auto-backend continuity."""

from pathlib import Path

import pytest

from core import queue as queue_mod
from core.queue import (
    QueueProfileError,
    RedisOutboxQueue,
    SqliteOutboxQueue,
    get_outbox_queue,
)


class PersistentFakeRedis:
    """Minimal Redis sorted-set stand-in whose state survives queue resets."""

    def __init__(self) -> None:
        self.z = {}

    def zadd(self, key, mapping):
        self.z.setdefault(key, {}).update(mapping)

    def zrange(self, key, start, end):
        items = sorted(self.z.get(key, {}).items(), key=lambda kv: (kv[1], kv[0]))
        members = [member.encode() for member, _ in items]
        if end == -1:
            end = len(members) - 1
        return members[start : end + 1]

    def zrem(self, key, member):
        self.z.get(key, {}).pop(member, None)

    def ping(self):
        return True


def _profile(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    path = tmp_path / "queue-profile"
    monkeypatch.setenv("VELANTRIM_QUEUE_PROFILE_PATH", str(path))
    monkeypatch.setenv("VELANTRIM_QUEUE_BACKEND", "auto")
    return path


def test_auto_restart_redis_to_sqlite_fails_closed_with_pending_preserved(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A locked Redis queue must not silently switch to empty SQLite after restart."""
    path = _profile(monkeypatch, tmp_path)
    redis_state = PersistentFakeRedis()
    monkeypatch.setattr(queue_mod, "_redis_client", lambda: redis_state)

    first = get_outbox_queue()
    assert isinstance(first, RedisOutboxQueue)
    first.enqueue("redis-before-restart")
    assert first.pending() == ["redis-before-restart"]
    assert path.read_text(encoding="ascii") == "redis\n"

    queue_mod.reset_outbox_queue()

    def redis_unavailable():
        raise RuntimeError("simulated Redis outage after restart")

    monkeypatch.setattr(queue_mod, "_redis_client", redis_unavailable)
    with pytest.raises(RuntimeError, match="simulated Redis outage"):
        get_outbox_queue()

    # The repair obligation remains in its original backend; normal construction
    # refuses to pretend an empty fallback queue is equivalent recovery state.
    assert RedisOutboxQueue(redis_state).pending() == ["redis-before-restart"]
    assert SqliteOutboxQueue().pending() == []


def test_auto_restart_sqlite_to_redis_keeps_locked_sqlite_pending_visible(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A SQLite auto selection remains SQLite even when Redis later appears."""
    path = _profile(monkeypatch, tmp_path)

    def redis_unavailable():
        raise RuntimeError("simulated Redis outage before restart")

    monkeypatch.setattr(queue_mod, "_redis_client", redis_unavailable)
    first = get_outbox_queue()
    assert isinstance(first, SqliteOutboxQueue)
    first.enqueue("sqlite-before-restart")
    assert first.pending() == ["sqlite-before-restart"]
    assert path.read_text(encoding="ascii") == "sqlite\n"

    queue_mod.reset_outbox_queue()
    redis_state = PersistentFakeRedis()
    monkeypatch.setattr(queue_mod, "_redis_client", lambda: redis_state)

    second = get_outbox_queue()
    assert isinstance(second, SqliteOutboxQueue)
    assert second.pending() == ["sqlite-before-restart"]
    assert RedisOutboxQueue(redis_state).pending() == []


def test_programmatic_explicit_auto_does_not_create_persistent_profile(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """One-off inspection preserves the existing uncached explicit-backend contract."""
    path = _profile(monkeypatch, tmp_path)
    monkeypatch.setattr(queue_mod, "_redis_client", lambda: PersistentFakeRedis())
    assert isinstance(get_outbox_queue("auto"), RedisOutboxQueue)
    assert not path.exists()


def test_queue_profile_malformed_and_empty_path_fail_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = _profile(monkeypatch, tmp_path)
    path.write_text("future\n", encoding="ascii")
    with pytest.raises(QueueProfileError, match="sqlite.*redis"):
        queue_mod._load_auto_backend_profile()

    monkeypatch.setenv("VELANTRIM_QUEUE_PROFILE_PATH", " ")
    with pytest.raises(QueueProfileError, match="must not be empty"):
        queue_mod.queue_profile_path()


def test_queue_profile_persistence_is_idempotent_and_rejects_race_mismatch(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = _profile(monkeypatch, tmp_path)
    assert queue_mod._persist_auto_backend_profile("sqlite") == "sqlite"
    assert queue_mod._persist_auto_backend_profile("sqlite") == "sqlite"
    assert path.read_text(encoding="ascii") == "sqlite\n"

    with pytest.raises(QueueProfileError, match="different queue backend"):
        queue_mod._persist_auto_backend_profile("redis")
    with pytest.raises(QueueProfileError, match="unsupported queue backend"):
        queue_mod._persist_auto_backend_profile("future")
