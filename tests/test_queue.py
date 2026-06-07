"""Tests for the pluggable L3 re-merge queue (core/queue.py) and the async
entry points (core/aio.py)."""
import asyncio

import pytest

from core import queue as queue_mod
from core.queue import (
    OutboxQueue,
    SqliteOutboxQueue,
    RedisOutboxQueue,
    get_outbox_queue,
)


# ─── A minimal in-memory stand-in for a Redis client ──────────────────────────
# Implements just the sorted-set surface RedisOutboxQueue uses. zrange returns
# bytes members (as a real redis-py client does by default) so the decoding path
# is exercised.
class FakeRedis:
    def __init__(self):
        self.z = {}

    def zadd(self, key, mapping):
        self.z.setdefault(key, {}).update(mapping)  # upsert → idempotent by member

    def zrange(self, key, start, end):
        items = sorted(self.z.get(key, {}).items(), key=lambda kv: (kv[1], kv[0]))
        members = [m.encode() for m, _ in items]
        if end == -1:
            end = len(members) - 1
        return members[start:end + 1]

    def zrem(self, key, member):
        self.z.get(key, {}).pop(member, None)

    def ping(self):
        return True


# ─── SQLite backend (the dependency-free default) ─────────────────────────────

def test_sqlite_backend_enqueue_pending_clear():
    q = get_outbox_queue("sqlite")
    assert isinstance(q, SqliteOutboxQueue)
    assert q.pending() == []
    q.enqueue("a")
    q.enqueue("b")
    assert set(q.pending()) == {"a", "b"}
    q.clear("a")
    assert q.pending() == ["b"]


def test_sqlite_backend_enqueue_is_idempotent():
    q = get_outbox_queue("sqlite")
    q.enqueue("dup")
    q.enqueue("dup")
    assert q.pending() == ["dup"]


def test_sqlite_backend_shares_store_with_memory():
    # The SQLite queue must read/write the same l3_outbox table that core.memory
    # exposes directly (so the pipeline and the low-level API stay consistent).
    from core import memory
    get_outbox_queue("sqlite").enqueue("shared")
    assert "shared" in memory.pending_l3_writes()
    memory.clear_l3_write("shared")
    assert get_outbox_queue("sqlite").pending() == []


# ─── Backend selection ────────────────────────────────────────────────────────

def test_unknown_backend_raises():
    with pytest.raises(ValueError):
        get_outbox_queue("bogus")


def test_auto_falls_back_to_sqlite_when_redis_unavailable(monkeypatch):
    def _boom():
        raise RuntimeError("no redis here")
    monkeypatch.setattr(queue_mod, "_redis_client", _boom)
    q = get_outbox_queue("auto")
    assert isinstance(q, SqliteOutboxQueue)


def test_auto_prefers_redis_when_available(monkeypatch):
    monkeypatch.setattr(queue_mod, "_redis_client", lambda: FakeRedis())
    q = get_outbox_queue("auto")
    assert isinstance(q, RedisOutboxQueue)


def test_explicit_redis_backend_surfaces_errors(monkeypatch):
    # An explicit 'redis' request must NOT silently fall back — it surfaces the
    # misconfiguration instead of hiding a missing server.
    def _boom():
        raise RuntimeError("connection refused")
    monkeypatch.setattr(queue_mod, "_redis_client", _boom)
    with pytest.raises(RuntimeError):
        get_outbox_queue("redis")


# ─── Redis backend behaviour (against the fake client) ────────────────────────

def test_redis_backend_enqueue_pending_clear(monkeypatch):
    monkeypatch.setattr(queue_mod, "_redis_client", lambda: FakeRedis())
    q = get_outbox_queue("redis")
    assert isinstance(q, RedisOutboxQueue)
    q.enqueue("x")
    q.enqueue("y")
    assert set(q.pending()) == {"x", "y"}  # decoded from bytes
    assert all(isinstance(m, str) for m in q.pending())
    q.clear("x")
    assert q.pending() == ["y"]


def test_redis_backend_is_idempotent_and_ordered():
    fake = FakeRedis()
    q = RedisOutboxQueue(fake)
    # Inject controlled scores to assert deterministic enqueue order.
    fake.zadd(q.KEY, {"first": 1.0})
    fake.zadd(q.KEY, {"second": 2.0})
    fake.zadd(q.KEY, {"first": 3.0})  # re-enqueue updates score, single member
    assert q.pending() == ["second", "first"]


def test_outboxqueue_interface_is_abstract():
    base = OutboxQueue()
    for call in (lambda: base.enqueue("a"), base.pending, lambda: base.clear("a")):
        with pytest.raises(NotImplementedError):
            call()


# ─── Async entry points (core/aio.py) ─────────────────────────────────────────

def test_arun_matches_sync_run_on_empty_retrieval():
    from core import pipeline
    from core.aio import arun
    query = "a query that retrieves nothing at all zzz"
    sync = pipeline.run(query)
    asyncv = asyncio.run(arun(query))
    # Blocked response shape: no answer, an error explaining the block.
    assert asyncv["answer"] is None
    assert asyncv["error"] == sync["error"]
    assert asyncv["query"] == query


def test_aingest_writes_a_fact():
    from core.aio import aingest
    result = asyncio.run(aingest("Water boils at 100 degrees Celsius."))
    assert "accepted" in result


def test_adrain_l3_outbox_drops_stale_entries():
    from core.aio import adrain_l3_outbox
    q = get_outbox_queue("sqlite")
    q.enqueue("ghost")                       # never stored in SQLite facts
    healed = asyncio.run(adrain_l3_outbox())
    assert healed == 0                       # nothing to merge
    assert q.pending() == []                 # stale entry pruned
