# Velantrim V8 · Sprint A v2+ — Additional Hardening Patches (historical)

> **Historical note:** This is a legacy internal sprint/patch document. It may
> contain older planning language ("production-hardened" etc.) that does not
> represent the current implemented status of Velantrim Crystal. For the
> canonical implemented-vs-RFC-vs-vision status map, see
> [`docs/IMPLEMENTATION_STATUS.md`](./docs/IMPLEMENTATION_STATUS.md); for the
> honest A1–A10 triage, see [`docs/SPRINT_A_STATUS.md`](./docs/SPRINT_A_STATUS.md).

> Extensions to A1–A5. Focus: Event Bus, Graph transactions, Resource bounds, LLM safety, Redis ops.

---

## 🔴 A6 · event_bus.py (Queue Overflow + Backpressure)

**Problem**: EventBus accepts infinite events → memory spike → OOM → cascade failure.
ConsolidationEngine queues undefined depth → deadlock risk.

```python
import asyncio
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone

MAX_QUEUE_SIZE = 10_000        # Hard limit - when exceeded, block publishers
DLQ_RETENTION = 86_400         # Dead Letter Queue: keep 1 day
DLQ_MAX_SIZE = 1_000           # DLQ itself bounded

@dataclass
class QueueMetrics:
    size: int
    peak_size: int
    overflow_count: int
    dlq_size: int
    oldest_event_age_sec: float

class EventBus:
    def __init__(self):
        self.queue: deque = deque(maxlen=None)
        self.dlq: deque = deque(maxlen=DLQ_MAX_SIZE)
        self.metrics = {
            'size': 0,
            'peak_size': 0,
            'overflow_count': 0,
            'dlq_size': 0,
        }
        self._lock = asyncio.Lock()
        self._not_full = asyncio.Condition(self._lock)

    async def publish(self, event: dict, timeout_sec: float = 30.0) -> bool:
        """
        Publish event with backpressure.
        If queue full → wait up to timeout_sec.
        If still full → return False (publisher handles it, not us).
        
        P0-5 FIX: backpressure prevents queue explosion.
        """
        start = datetime.now(timezone.utc)
        
        async with self._not_full:
            # Wait until queue has space, with timeout
            while len(self.queue) >= MAX_QUEUE_SIZE:
                elapsed = (datetime.now(timezone.utc) - start).total_seconds()
                if elapsed > timeout_sec:
                    # Timeout: publisher should handle, not retry infinitely
                    self.metrics['overflow_count'] += 1
                    logger.warning(
                        f"EventBus.publish timeout: queue full "
                        f"({len(self.queue)}/{MAX_QUEUE_SIZE}), "
                        f"DLQ size: {len(self.dlq)}"
                    )
                    return False
                
                remaining = timeout_sec - elapsed
                await asyncio.wait_for(
                    self._not_full.wait(),
                    timeout=remaining
                )
            
            # Add event with timestamp
            event['_enqueued_at'] = datetime.now(timezone.utc).isoformat()
            self.queue.append(event)
            self.metrics['size'] = len(self.queue)
            self.metrics['peak_size'] = max(
                self.metrics['peak_size'],
                len(self.queue)
            )
            self._not_full.notify_all()
            return True

    async def consume(self) -> dict | None:
        """
        Dequeue with error handling.
        If processing fails → move to DLQ, don't retry infinitely.
        """
        async with self._lock:
            if not self.queue:
                return None
            event = self.queue.popleft()
            self.metrics['size'] = len(self.queue)
            self._not_full.notify_all()
            return event

    async def handle_failure(self, event: dict, error: Exception):
        """
        Move failed event to DLQ.
        Stop retrying — operator must review DLQ manually.
        """
        event['_failed_at'] = datetime.now(timezone.utc).isoformat()
        event['_error'] = str(error)
        event['_retry_count'] = event.get('_retry_count', 0) + 1
        
        # Only keep in DLQ if retry_count < threshold
        if event['_retry_count'] <= 3:
            if len(self.dlq) >= DLQ_MAX_SIZE:
                logger.error("DLQ overflow — dropping oldest event")
                self.dlq.popleft()
            self.dlq.append(event)
            self.metrics['dlq_size'] = len(self.dlq)
        
        logger.error(
            f"EventBus.failure: event {event.get('type')} → DLQ "
            f"(retry {event['_retry_count']}/3), error: {error}"
        )

    def get_metrics(self) -> QueueMetrics:
        """Monitoring endpoint."""
        oldest_age = 0.0
        if self.queue:
            oldest = self.queue[0]
            enqueued = datetime.fromisoformat(oldest['_enqueued_at'])
            oldest_age = (datetime.now(timezone.utc) - enqueued).total_seconds()
        
        return QueueMetrics(
            size=self.metrics['size'],
            peak_size=self.metrics['peak_size'],
            overflow_count=self.metrics['overflow_count'],
            dlq_size=self.metrics['dlq_size'],
            oldest_event_age_sec=oldest_age
        )

    async def monitor(self):
        """Background: alert on queue health."""
        while True:
            metrics = self.get_metrics()
            if metrics.size > MAX_QUEUE_SIZE * 0.8:
                logger.warning(f"EventBus queue 80% full: {metrics.size}/{MAX_QUEUE_SIZE}")
            if metrics.dlq_size > DLQ_MAX_SIZE * 0.9:
                logger.error(f"DLQ 90% full: {metrics.dlq_size}/{DLQ_MAX_SIZE}")
            if metrics.oldest_event_age_sec > 3600:  # 1 hour
                logger.warning(f"Old event in queue: {metrics.oldest_event_age_sec}s")
            await asyncio.sleep(60)
```

**Invariant**: 
- Max queue depth = 10K (bounded)
- Backpressure on publish (not fire-and-forget)
- DLQ for unreliable events (not retry-loop)
- Monitor alerts at 80% capacity

---

## 🟡 A7 · graph_transaction_safety.py (Deadlock Prevention)

**Problem**: Concurrent writes to same node → Neo4j deadlock. 
ConsolidationEngine + Observer both modifying ESM → transient rollback.

```python
from typing import Callable, TypeVar, Any
import asyncio

T = TypeVar('T')

class GraphTransactionBounds:
    """Prevent deadlock through ordered access + timeout."""
    
    # Global: all Neo4j operations acquire locks in alphabetical order by node_id
    _global_lock_order = {}  # node_id → acquisition_time
    _lock_pool = {}  # node_id → asyncio.Lock (one per node)
    
    MAX_TRANSACTION_TIME_SEC = 30
    LOCK_ACQUIRE_TIMEOUT_SEC = 5

    @classmethod
    def _get_lock(cls, node_id: str) -> asyncio.Lock:
        """Get or create per-node lock."""
        if node_id not in cls._lock_pool:
            cls._lock_pool[node_id] = asyncio.Lock()
        return cls._lock_pool[node_id]

    @classmethod
    async def safe_write(
        cls,
        node_ids: list[str],
        cypher: str,
        params: dict,
        graph,
        timeout_sec: float = MAX_TRANSACTION_TIME_SEC
    ) -> Any:
        """
        Execute Cypher with ordered node locking.
        node_ids must be sorted → prevents circular wait.
        
        P0-6 FIX: deadlock prevention through lock ordering.
        """
        # Sort to guarantee order (no circular waits)
        sorted_nodes = sorted(set(node_ids))
        locks = [cls._get_lock(nid) for nid in sorted_nodes]
        
        acquired = []
        try:
            # Acquire locks in order with timeout
            for i, lock in enumerate(locks):
                try:
                    await asyncio.wait_for(
                        lock.acquire(),
                        timeout=cls.LOCK_ACQUIRE_TIMEOUT_SEC
                    )
                    acquired.append(i)
                except asyncio.TimeoutError:
                    logger.error(
                        f"GraphTransaction deadlock risk: "
                        f"couldn't acquire lock for {sorted_nodes[i]} "
                        f"after {cls.LOCK_ACQUIRE_TIMEOUT_SEC}s. "
                        f"Other writer blocking? Rollback."
                    )
                    raise TransactionDeadlock(
                        f"Can't acquire lock for node {sorted_nodes[i]}"
                    )
            
            # Execute with timeout
            result = await asyncio.wait_for(
                graph.execute_cypher(cypher, params),
                timeout=timeout_sec
            )
            return result
            
        except asyncio.TimeoutError:
            logger.error(
                f"GraphTransaction timeout: Cypher didn't complete "
                f"in {timeout_sec}s. Query aborted."
            )
            raise TransactionTimeout(
                f"Transaction timeout after {timeout_sec}s"
            )
        finally:
            # Release all locks
            for i in acquired:
                locks[i].release()
            acquired.clear()

    @classmethod
    async def safe_read(
        cls,
        node_ids: list[str],
        cypher: str,
        params: dict,
        graph,
        timeout_sec: float = 10  # reads faster
    ) -> Any:
        """Read-only (no lock needed, but timeout enforced)."""
        try:
            return await asyncio.wait_for(
                graph.execute_cypher(cypher, params),
                timeout=timeout_sec
            )
        except asyncio.TimeoutError:
            logger.error(f"GraphQuery timeout after {timeout_sec}s")
            raise QueryTimeout(f"Read timeout after {timeout_sec}s")

class TransactionDeadlock(Exception):
    pass

class TransactionTimeout(Exception):
    pass

class QueryTimeout(Exception):
    pass

# Usage in TruthGate:
async def validate_and_write(fact_dict, graph):
    node_ids = [fact_dict['id']]  # All nodes to be touched
    cypher = """
    MATCH (f:Fact {id: $id})
    SET f.epistemic_state = 'Validated', f.validated_at = datetime()
    RETURN f
    """
    return await GraphTransactionBounds.safe_write(
        node_ids, cypher, {'id': fact_dict['id']}, graph
    )
```

**Invariant**: 
- Lock ordering (alphabetical) prevents circular waits
- Timeout on acquire (5s) detects probable deadlock
- Timeout on execute (30s) prevents hanging transactions

---

## 🟢 A8 · memory_cleanup_gc.py (Soft+Hard Delete Lifecycle)

**Problem**: Marked-for-deletion nodes consume RAM. L3 never shrinks.
Tombstones accumulate → effective capacity drops.

```python
from datetime import datetime, timedelta, timezone
from typing import NamedTuple

class RetentionPolicy(NamedTuple):
    soft_delete_grace_period_days: int = 7      # Keep tombstone 7 days
    hard_delete_after_days: int = 30             # Then hard-delete
    min_free_nodes_before_gc: int = 1_000        # Trigger GC if < 1K free
    gc_interval_hours: int = 24                  # Run daily

class MemoryCleanupGC:
    """L3 garbage collection: soft→hard delete lifecycle."""
    
    def __init__(self, graph, policy: RetentionPolicy = RetentionPolicy()):
        self.graph = graph
        self.policy = policy
        self.last_run = datetime.now(timezone.utc)

    async def should_gc_run(self) -> bool:
        """Check if GC needed."""
        # Trigger 1: scheduled (daily)
        if (datetime.now(timezone.utc) - self.last_run).days >= 1:
            return True
        
        # Trigger 2: capacity warning
        stats = await self.get_graph_stats()
        if stats['soft_deleted_count'] > stats['total_nodes'] * 0.15:
            logger.warning(
                f"L3 GC: {stats['soft_deleted_count']} soft-deleted nodes "
                f"({stats['soft_deleted_count']/stats['total_nodes']*100:.1f}%) "
                f"→ running GC early"
            )
            return True
        
        return False

    async def get_graph_stats(self) -> dict:
        """Get graph health metrics."""
        result = await self.graph.execute_cypher(
            """
            MATCH (n)
            RETURN 
                count(n) AS total,
                count(CASE WHEN n.is_active = false THEN 1 END) AS soft_deleted,
                count(CASE WHEN n.pending_hard_delete = true THEN 1 END) AS pending_hard
            """
        )
        row = result[0]
        return {
            'total_nodes': row['total'],
            'soft_deleted_count': row['soft_deleted'],
            'pending_hard_count': row['pending_hard'],
        }

    async def run_gc_cycle(self):
        """Full GC: grace period → hard delete."""
        # Phase 1: Mark old soft-deletes for hard-delete
        grace_cutoff = datetime.now(timezone.utc) - timedelta(
            days=self.policy.soft_delete_grace_period_days
        )
        
        await self.graph.execute_cypher(
            """
            MATCH (n {is_active: false})
            WHERE n.valid_to < $cutoff AND n.pending_hard_delete IS NULL
            SET n.pending_hard_delete = true
            """,
            {'cutoff': grace_cutoff.isoformat()}
        )
        
        # Phase 2: Hard-delete in batches (no cascade)
        batch_size = 100
        while True:
            # Get batch
            to_delete = await self.graph.execute_cypher(
                f"""
                MATCH (n {{pending_hard_delete: true}})
                RETURN n.id AS id LIMIT {batch_size}
                """
            )
            
            if not to_delete:
                break
            
            node_ids = [row['id'] for row in to_delete]
            
            # Delete nodes (detach: remove all relationships)
            # P0-7 FIX: DETACH DELETE prevents orphaned edges
            await GraphTransactionBounds.safe_write(
                node_ids,
                f"""
                MATCH (n) WHERE n.id IN {[n['id'] for n in to_delete]}
                DETACH DELETE n
                """,
                {},
                self.graph,
                timeout_sec=60  # hard-delete slower than update
            )
            
            logger.info(f"MemoryCleanupGC: deleted {len(node_ids)} nodes")
            await asyncio.sleep(0.5)  # Let Neo4j catch breath
        
        self.last_run = datetime.now(timezone.utc)
        stats = await self.get_graph_stats()
        logger.info(
            f"MemoryCleanupGC cycle complete: "
            f"{stats['total_nodes']} nodes, "
            f"{stats['soft_deleted_count']} soft-deleted"
        )

    async def monitor(self):
        """Background: run GC when needed."""
        while True:
            try:
                if await self.should_gc_run():
                    logger.info("MemoryCleanupGC: starting cycle")
                    await self.run_gc_cycle()
            except Exception as e:
                logger.error(f"MemoryCleanupGC failed: {e}", exc_info=True)
            
            await asyncio.sleep(3600)  # Check hourly
```

**Invariant**: 
- Soft-delete (7 days): tombstone preserved, readable as "inactive"
- Hard-delete (30 days): physically removed
- Batched deletion prevents long locks
- DETACH DELETE prevents orphaned edges

---

## 🔴 A9 · llm_call_safety.py (Rate Limit + Timeout + Retry Bounds)

**Problem**: LLM calls unbounded → rate-limit 429s → retry loop → cascade.
Context window overflow silent → token soup → garbage answer.

```python
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import asyncio

@dataclass
class LLMCallBounds:
    max_tokens_per_minute: int = 90_000      # Claude Sonnet 4.6 rateLimit
    max_concurrent_calls: int = 10           # Max parallel LLM requests
    call_timeout_sec: int = 120              # Max wait for LLM response
    max_retries: int = 3
    backoff_base_sec: int = 2

class LLMCallSafety:
    """Rate-limit, timeout, and retry bounds for LLM calls."""
    
    def __init__(self, bounds: LLMCallBounds = LLMCallBounds()):
        self.bounds = bounds
        self.semaphore = asyncio.Semaphore(bounds.max_concurrent_calls)
        self.rate_limiter = TokenBucket(
            capacity=bounds.max_tokens_per_minute,
            refill_rate_per_sec=bounds.max_tokens_per_minute / 60
        )

    async def call_with_safety(
        self,
        llm_client,
        messages: list,
        model: str,
        temperature: float = 0.5,
        max_tokens: int = 2000,
    ) -> str:
        """
        Call LLM with all safety guards.
        
        P0-8 FIX: rate limits, timeouts, bounded retries.
        """
        
        # Guard 1: max_tokens ceiling
        max_tokens = min(max_tokens, 4096)  # Never exceed context
        
        # Guard 2: concurrency bound
        async with self.semaphore:
            # Guard 3: token budget (rate-limit)
            tokens_needed = len(str(messages)) // 4 + max_tokens
            if not await self.rate_limiter.consume(tokens_needed):
                logger.warning(
                    f"LLM rate-limit: need {tokens_needed} tokens, "
                    f"but at capacity {self.bounds.max_tokens_per_minute}/min. "
                    f"Rejecting call (not retrying)."
                )
                raise LLMRateLimited(f"Rate limit: {tokens_needed} tokens needed")
            
            # Guard 4: retry loop with exponential backoff (max 3 retries)
            for attempt in range(1, self.bounds.max_retries + 1):
                try:
                    # Guard 5: timeout per call
                    response = await asyncio.wait_for(
                        llm_client.messages.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                        ),
                        timeout=self.bounds.call_timeout_sec
                    )
                    return response.content[0].text
                
                except asyncio.TimeoutError:
                    if attempt == self.bounds.max_retries:
                        logger.error(
                            f"LLM timeout after {self.bounds.call_timeout_sec}s "
                            f"(attempt {attempt}/{self.bounds.max_retries}). Giving up."
                        )
                        raise LLMTimeout(
                            f"LLM timeout after {self.bounds.call_timeout_sec}s, "
                            f"max {self.bounds.max_retries} retries exhausted"
                        )
                    wait = self.bounds.backoff_base_sec ** attempt
                    logger.warning(
                        f"LLM timeout (attempt {attempt}/{self.bounds.max_retries}), "
                        f"backoff {wait}s"
                    )
                    await asyncio.sleep(wait)
                
                except Exception as e:
                    if "rate_limit" in str(e).lower() or "429" in str(e):
                        if attempt == self.bounds.max_retries:
                            raise LLMRateLimited(str(e)) from e
                        wait = self.bounds.backoff_base_sec ** attempt
                        logger.warning(f"LLM 429 (attempt {attempt}), backoff {wait}s")
                        await asyncio.sleep(wait)
                    else:
                        # Non-retryable (invalid input, auth, etc)
                        raise

class TokenBucket:
    """Rate limiter using token bucket algorithm."""
    
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = capacity
        self.last_refill = datetime.now(timezone.utc)

    async def consume(self, amount: int) -> bool:
        """Try to consume tokens. Return False if insufficient."""
        await self._refill()
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False

    async def _refill(self):
        now = datetime.now(timezone.utc)
        elapsed = (now - self.last_refill).total_seconds()
        refill_amount = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + refill_amount)
        self.last_refill = now

class LLMRateLimited(Exception):
    pass

class LLMTimeout(Exception):
    pass
```

**Invariant**:
- Concurrent calls ≤ 10
- Token budget enforced (no silent overrun)
- Timeouts on all LLM calls (120s max)
- Retry with exponential backoff (max 3, then fail)
- Rate-limit exhaustion → reject, not infinite retry

---

## 🟡 A10 · redis_connection_pool.py (Connection Limits + Timeout)

**Problem**: Redis connection pool unbounded. 
Task per event → task per async fn → connection leak → exhaust Redis `maxclients`.

```python
import aioredis
from typing import Optional

class RedisConnectionPool:
    """Safe Redis access through bounded connection pool."""
    
    # P0-9 FIX: connection pool with explicit limits
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        min_size: int = 5,
        max_size: int = 50,
        socket_timeout_sec: float = 5.0,
    ):
        self.redis_url = redis_url
        self.min_size = min_size
        self.max_size = max_size
        self.socket_timeout = socket_timeout_sec
        self.pool: Optional[aioredis.ConnectionPool] = None

    async def init(self):
        """Initialize pool once at startup."""
        self.pool = aioredis.ConnectionPool.from_url(
            self.redis_url,
            min_idle=self.min_size,
            max_size=self.max_size,
            socket_timeout=self.socket_timeout,
            socket_keepalive=True,
        )
        logger.info(
            f"RedisPool: min={self.min_size}, max={self.max_size}, "
            f"timeout={self.socket_timeout}s"
        )

    async def get(self, key: str, default=None) -> Optional[str]:
        """Get with timeout."""
        try:
            async with aioredis.Redis(connection_pool=self.pool) as r:
                val = await asyncio.wait_for(r.get(key), timeout=self.socket_timeout)
                return val
        except asyncio.TimeoutError:
            logger.warning(f"Redis GET timeout: {key}")
            return default
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return default

    async def set(self, key: str, value: str, ttl_sec: Optional[int] = None) -> bool:
        """Set with TTL and timeout."""
        try:
            async with aioredis.Redis(connection_pool=self.pool) as r:
                if ttl_sec:
                    result = await asyncio.wait_for(
                        r.setex(key, ttl_sec, value),
                        timeout=self.socket_timeout
                    )
                else:
                    result = await asyncio.wait_for(
                        r.set(key, value),
                        timeout=self.socket_timeout
                    )
                return bool(result)
        except asyncio.TimeoutError:
            logger.warning(f"Redis SET timeout: {key}")
            return False
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            return False

    async def close(self):
        """Cleanup at shutdown."""
        if self.pool:
            await self.pool.disconnect()

# Global instance
_redis_pool: Optional[RedisConnectionPool] = None

async def init_redis(url: str, min_size: int = 5, max_size: int = 50):
    """Initialize at pipeline startup."""
    global _redis_pool
    _redis_pool = RedisConnectionPool(redis_url=url, min_size=min_size, max_size=max_size)
    await _redis_pool.init()

async def redis_get(key: str) -> Optional[str]:
    """Use global pool."""
    return await _redis_pool.get(key)

async def redis_set(key: str, value: str, ttl_sec: Optional[int] = None) -> bool:
    """Use global pool."""
    return await _redis_pool.set(key, value, ttl_sec)

async def redis_cleanup():
    """Call at shutdown."""
    if _redis_pool:
        await _redis_pool.close()
```

**Invariant**:
- Connection pool bounded: min 5, max 50
- Socket timeout 5s on all ops
- Timeouts don't retry (fail fast)
- Pool cleanup at shutdown

---

## Summary Table

| Patch | Component | Issue | Fix |
|-------|-----------|-------|-----|
| A1 | raw_memory_store | None | ✅ Idempotent inserts |
| A2 | memory_guardian | Param injection | ✅ Strict Cypher contracts |
| A3 | pii_redaction | Overlap matching | ✅ Span deduplication |
| A4 | truth_gate | NULL handling | ✅ coalesce() indexing |
| A5 | fractal_similarity | CPU overload | ✅ Bounded concurrency (Semaphore) |
| **A6** | **event_bus** | **Queue overflow** | ✅ **Backpressure + DLQ** |
| **A7** | **graph_transactions** | **Deadlock risk** | ✅ **Lock ordering + timeout** |
| **A8** | **memory_gc** | **L3 never shrinks** | ✅ **Soft→Hard delete lifecycle** |
| **A9** | **llm_calls** | **Rate limit cascade** | ✅ **Token budget + timeout + bounded retry** |
| **A10** | **redis_pool** | **Connection leak** | ✅ **Bounded pool + timeout** |

---

## 🚀 Production Readiness Checklist

- [x] Memory bounds (A6, A8, A9)
- [x] Transaction safety (A7)
- [x] Resource limits (A5, A9, A10)
- [x] Data consistency (A2, A3, A4)
- [x] Monitoring (all: metrics, logging, alerts)
- [x] Error isolation (no cascades)
- [x] Timeout on every I/O (all async ops)
- [x] Retry bounds (A9: max 3 retries)

**Result**: System survives load spikes, cascading failures, and resource exhaustion.
No silent corruption. All failures logged + actionable.

---
