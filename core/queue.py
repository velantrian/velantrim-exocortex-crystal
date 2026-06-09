# core/queue.py
# Velantrim ExoCortex — pluggable outbox queue for re-merging facts into L3.
#
# L3 (canon) and SQLite (pending) do not share a transaction. When a merge into
# the graph fails (backend unavailable), the fact stays Validated in SQLite
# without a node in the canon. The outbox makes this self-healing: the failed
# fact is enqueued and idempotently re-merged on the next access (see
# pipeline.drain_l3_outbox).
#
# Two interchangeable backends behind one interface:
#   - SqliteOutboxQueue: the dependency-free default. Persists in the same
#     SQLite file as the rest of L0/L1 (table l3_outbox, in core.memory). It is
#     the 'auto' fallback when Redis is absent — the runtime stays stdlib-only.
#   - RedisOutboxQueue: optional, for multi-process / multi-worker deployments
#     where several pipeline workers share one re-merge queue. Uses a Redis
#     sorted set (score = enqueue time) → ordered + idempotent by fact_id.
#
# Selection mirrors the L3/embedder/generator registries (core/_registry.py):
#   VELANTRIM_QUEUE_BACKEND = auto (default) | sqlite | redis
#   auto → Redis if the `redis` package is importable AND a server answers PING
#          (VELANTRIM_REDIS_URL, default redis://localhost:6379/0); else SQLite.

import os
import time
from typing import List, Optional

from core._registry import BackendRegistry


class OutboxQueue:
    """Interface for the L3 re-merge queue. Implementations must be idempotent
    on enqueue (same fact_id enqueued twice → one pending entry)."""

    def enqueue(self, fact_id: str) -> None:
        raise NotImplementedError

    def pending(self) -> List[str]:
        """fact_ids awaiting re-merge, in enqueue order."""
        raise NotImplementedError

    def clear(self, fact_id: str) -> None:
        """Remove a fact from the queue (after a successful merge or erasure)."""
        raise NotImplementedError


class SqliteOutboxQueue(OutboxQueue):
    """Persistent, dependency-free backend. Delegates to the SQLite outbox in
    core.memory (table l3_outbox), so it shares the L0/L1 database file and
    survives restarts with no native dependencies."""

    def enqueue(self, fact_id: str) -> None:
        from core import memory
        memory.enqueue_l3_write(fact_id)

    def pending(self) -> List[str]:
        from core import memory
        return memory.pending_l3_writes()

    def clear(self, fact_id: str) -> None:
        from core import memory
        memory.clear_l3_write(fact_id)


class RedisOutboxQueue(OutboxQueue):
    """Optional Redis backend (sorted set, score = enqueue epoch). Lets several
    pipeline workers share one re-merge queue. Idempotent: re-enqueuing a
    fact_id updates its score but keeps a single member."""

    KEY = "velantrim:l3_outbox"

    def __init__(self, client) -> None:
        self._r = client

    @staticmethod
    def _decode(member) -> str:
        return member.decode() if isinstance(member, (bytes, bytearray)) else member

    def enqueue(self, fact_id: str) -> None:
        self._r.zadd(self.KEY, {fact_id: time.time()})

    def pending(self) -> List[str]:
        return [self._decode(m) for m in self._r.zrange(self.KEY, 0, -1)]

    def clear(self, fact_id: str) -> None:
        self._r.zrem(self.KEY, fact_id)


def _redis_client():  # pragma: no cover - needs the redis package + a live server
    """Build a Redis client and verify the server is reachable. Raises
    ImportError if the package is missing, or a redis error if PING fails."""
    import redis  # optional dependency — imported lazily
    url = os.environ.get("VELANTRIM_REDIS_URL", "redis://localhost:6379/0")
    client = redis.Redis.from_url(url)
    client.ping()
    return client


def _make(name: str) -> OutboxQueue:
    if name == "sqlite":
        return SqliteOutboxQueue()
    if name == "redis":
        # Explicit request: no silent fallback — surface the configuration error.
        return RedisOutboxQueue(_redis_client())
    if name == "auto":
        # Prefer a shared Redis queue when one is actually available; otherwise
        # fall back to the persistent stdlib SQLite queue (runtime stays
        # dependency-free).
        try:
            return RedisOutboxQueue(_redis_client())
        except Exception:
            return SqliteOutboxQueue()
    raise ValueError(
        f"Unknown queue backend: {name!r} (expected auto | sqlite | redis)")


_REGISTRY = BackendRegistry("VELANTRIM_QUEUE_BACKEND", "auto", _make)


def get_outbox_queue(backend: Optional[str] = None) -> OutboxQueue:
    """Return the outbox-queue singleton. Backend via argument or
    VELANTRIM_QUEUE_BACKEND (auto | sqlite | redis)."""
    return _REGISTRY.get(backend)


def reset_outbox_queue() -> None:
    """Reset the singleton (for tests)."""
    _REGISTRY.reset()
