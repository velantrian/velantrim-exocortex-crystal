"""Adversarial reproduction for Outbox auto-backend continuity across restart.

These tests intentionally freeze the recovery invariant before any runtime repair:
a pending L3 recovery item created under one automatically selected queue backend
must remain observable after a process-style registry reset if `auto` resolves to
the other supported backend.

If current behavior silently switches between Redis and SQLite without preserving
pending visibility or failing closed, these tests are expected to fail. That
failure is the reproduction evidence; this file does not prescribe a fix.
"""

import pytest

from core import queue as queue_mod
from core.queue import RedisOutboxQueue, SqliteOutboxQueue, get_outbox_queue


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


def test_auto_restart_redis_to_sqlite_keeps_pending_visible(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pending Redis work must not silently disappear when auto later selects SQLite."""

    redis_state = PersistentFakeRedis()
    monkeypatch.setenv("VELANTRIM_QUEUE_BACKEND", "auto")
    monkeypatch.setattr(queue_mod, "_redis_client", lambda: redis_state)

    first = get_outbox_queue()
    assert isinstance(first, RedisOutboxQueue)
    first.enqueue("redis-before-restart")
    assert first.pending() == ["redis-before-restart"]

    # Model a new process: the registry singleton is gone and Redis is now
    # unavailable, so the same supported `auto` configuration resolves again.
    queue_mod.reset_outbox_queue()

    def redis_unavailable():
        raise RuntimeError("simulated Redis outage after restart")

    monkeypatch.setattr(queue_mod, "_redis_client", redis_unavailable)
    second = get_outbox_queue()
    assert isinstance(second, SqliteOutboxQueue)

    # Recovery invariant under test: normal pending/drain observation after the
    # restart must still see the already-persisted repair obligation, or the
    # backend switch must have failed closed before reaching this point.
    assert "redis-before-restart" in second.pending()


def test_auto_restart_sqlite_to_redis_keeps_pending_visible(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pending SQLite work must not silently disappear when auto later selects Redis."""

    monkeypatch.setenv("VELANTRIM_QUEUE_BACKEND", "auto")

    def redis_unavailable():
        raise RuntimeError("simulated Redis outage before restart")

    monkeypatch.setattr(queue_mod, "_redis_client", redis_unavailable)
    first = get_outbox_queue()
    assert isinstance(first, SqliteOutboxQueue)
    first.enqueue("sqlite-before-restart")
    assert first.pending() == ["sqlite-before-restart"]

    # New process, same `auto` configuration, but Redis has become available.
    queue_mod.reset_outbox_queue()
    redis_state = PersistentFakeRedis()
    monkeypatch.setattr(queue_mod, "_redis_client", lambda: redis_state)

    second = get_outbox_queue()
    assert isinstance(second, RedisOutboxQueue)

    # The standard recovery surface must not silently observe an empty backend
    # while the previous durable backend still contains pending work.
    assert "sqlite-before-restart" in second.pending()
