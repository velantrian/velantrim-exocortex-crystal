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
#     SQLite file as the rest of L0/L1 (table l3_outbox, in core.memory).
#   - RedisOutboxQueue: optional, for multi-process / multi-worker deployments
#     where several pipeline workers share one re-merge queue. Uses a Redis
#     sorted set (score = enqueue time) → ordered + idempotent by fact_id.
#
# Selection:
#   VELANTRIM_QUEUE_BACKEND = auto (default) | sqlite | redis
#   auto → on first environment-selected construction, Redis if the `redis`
#          package is importable AND a server answers PING; otherwise SQLite.
#          That resolved backend family is then persisted in a small local
#          profile so a later process restart cannot silently switch queues and
#          strand already-pending recovery work. A locked Redis outage fails
#          closed rather than falling back to an empty SQLite queue.
#   VELANTRIM_QUEUE_PROFILE_PATH controls the non-secret auto-selection marker.
#
# Programmatic get_outbox_queue(backend=...) remains an uncached one-off path for
# tests/tooling and does not read or mutate the persistent auto-selection marker.

import os
import tempfile
import time
from pathlib import Path
from typing import List, Optional

from core._registry import BackendRegistry
from core.backend_profiles import StorageProfileError, _acquire_profile_lock

QUEUE_PROFILE_PATH_ENV = "VELANTRIM_QUEUE_PROFILE_PATH"
DEFAULT_QUEUE_PROFILE_PATH = "~/.velantrim/velantrim-queue-profile"
_AUTO_BACKENDS = frozenset({"sqlite", "redis"})


class QueueProfileError(StorageProfileError):
    """Raised when the durable queue auto-selection marker is unusable."""


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


def queue_profile_path() -> Path:
    """Return the absolute auto-selection marker path without creating it."""
    raw = os.environ.get(QUEUE_PROFILE_PATH_ENV, DEFAULT_QUEUE_PROFILE_PATH)
    if not raw.strip():
        raise QueueProfileError(f"{QUEUE_PROFILE_PATH_ENV} must not be empty")
    return Path(raw).expanduser().resolve(strict=False)


def _load_auto_backend_profile(path: Optional[Path] = None) -> Optional[str]:
    """Read the locked queue backend family; malformed state fails closed."""
    target = path or queue_profile_path()
    if not target.exists():
        return None
    try:
        backend = target.read_text(encoding="ascii").strip()
    except OSError as exc:
        raise QueueProfileError(
            f"cannot read queue backend profile {target}: {type(exc).__name__}"
        ) from exc
    if backend not in _AUTO_BACKENDS:
        raise QueueProfileError("queue backend profile must contain 'sqlite' or 'redis'")
    return backend


def _persist_auto_backend_profile(backend: str) -> str:
    """Atomically persist the first auto-selected backend, rejecting races."""
    if backend not in _AUTO_BACKENDS:
        raise QueueProfileError(f"unsupported queue backend profile: {backend!r}")

    path = queue_profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(f"{path.name}.lock")
    lock_fd = _acquire_profile_lock(lock_path)
    temp_name: Optional[str] = None
    try:
        os.close(lock_fd)
        existing = _load_auto_backend_profile(path)
        if existing is not None:
            if existing != backend:
                raise QueueProfileError(
                    "another process locked a different queue backend"
                )
            return existing

        fd, temp_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
        with os.fdopen(fd, "w", encoding="ascii") as handle:
            handle.write(f"{backend}\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        temp_name = None
        return backend
    except OSError as exc:
        raise QueueProfileError(
            f"cannot persist queue backend profile {path}: {type(exc).__name__}"
        ) from exc
    finally:
        if temp_name is not None:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:  # pragma: no cover - defensive cleanup race
                pass
        try:
            os.unlink(lock_path)
        except FileNotFoundError:  # pragma: no cover - defensive cleanup race
            pass


def _redis_client():  # pragma: no cover - needs the redis package + a live server
    """Build a Redis client and verify the server is reachable. Raises
    ImportError if the package is missing, or a redis error if PING fails."""
    import redis  # optional dependency — imported lazily
    url = os.environ.get("VELANTRIM_REDIS_URL", "redis://localhost:6379/0")
    client = redis.Redis.from_url(url)
    client.ping()
    return client


def _construct(name: str) -> OutboxQueue:
    """Construct one requested backend without consulting auto-selection state."""
    if name == "sqlite":
        return SqliteOutboxQueue()
    if name == "redis":
        # Explicit/locked Redis: no silent fallback — surface the connection error.
        return RedisOutboxQueue(_redis_client())
    if name == "auto":
        try:
            return RedisOutboxQueue(_redis_client())
        except Exception:
            return SqliteOutboxQueue()
    raise ValueError(
        f"Unknown queue backend: {name!r} (expected auto | sqlite | redis)")


def _make(name: str) -> OutboxQueue:
    """Registry factory. Only environment-selected `auto` owns a durable marker."""
    if name != "auto":
        return _construct(name)

    locked = _load_auto_backend_profile()
    if locked is not None:
        # Do not probe/fallback after restart. If locked Redis is unavailable,
        # _construct('redis') surfaces the failure instead of selecting an empty
        # SQLite queue and making old pending work invisible.
        return _construct(locked)

    candidate = _construct("auto")
    selected = "redis" if isinstance(candidate, RedisOutboxQueue) else "sqlite"
    _persist_auto_backend_profile(selected)
    return candidate


_REGISTRY = BackendRegistry("VELANTRIM_QUEUE_BACKEND", "auto", _make)


def get_outbox_queue(backend: Optional[str] = None) -> OutboxQueue:
    """Return the outbox queue.

    With no argument, use the environment-selected singleton and persist the first
    `auto` backend family across restarts. An explicit `backend=...` is a fresh,
    uncached one-off construction for tests/migration/inspection and deliberately
    bypasses the persistent auto-selection marker.
    """
    if backend is not None:
        return _construct(backend)
    return _REGISTRY.get()


def reset_outbox_queue() -> None:
    """Reset the in-process singleton; persistent auto-selection is retained."""
    _REGISTRY.reset()
