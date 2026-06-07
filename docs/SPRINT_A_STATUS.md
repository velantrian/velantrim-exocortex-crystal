# 🩹 Sprint-A Hardening Patches (A1–A10) — Status vs. the Crystal Core

> **Honesty rule.** The Sprint-A patch set in
> [`SPRINT_A_V2_ADDITIONAL_PATCHES.md`](../SPRINT_A_V2_ADDITIONAL_PATCHES.md) was
> written against the **full** Velantrim architecture (an async `EventBus`, a
> Neo4j/Cypher graph in the write path, an `aioredis` connection pool, a live LLM
> on the critical path). The open **Crystal** core is deliberately a smaller,
> dependency-free, synchronous, local-first engine. This document states plainly,
> per patch, whether it is **already satisfied**, **implemented here**, or
> **not applicable** to the Crystal core (it belongs to the heavier Phase‑1 stack).
> Nothing is marked done that is not actually in the code.

| Patch | Concern | Status in the Crystal core | Where |
|------|---------|----------------------------|-------|
| **A1** | Idempotent inserts | ✅ **Already satisfied** | `core/ingest.py` — an exact repeat of a Validated fact reinforces confidence instead of duplicating (content-hash `fact_id`). |
| **A2** | Param injection / strict write contracts | ✅ **Already satisfied** | All SQLite access is parameterised (`core/memory.py`, `core/knowledge.py`); the default L3 is the in-process mock / stdlib SQLite — there is no Cypher string-interpolation surface. |
| **A3** | PII overlap matching | ✅ **Already satisfied** | `core/pii.py` does overlap-safe detection (email/phone/card-Luhn/IPv4/IBAN) with span de-duplication. |
| **A4** | NULL handling in indexed reads | ✅ **N/A by design** | No Cypher `coalesce()` indexing in the default core; Python handles missing fields explicitly. Relevant only to the optional Neo4j backend (Phase 1+). |
| **A5** | Bounded concurrency (similarity) | ✅ **N/A by design** | The core is synchronous; fractal/similarity passes run single-threaded and deterministic. No unbounded parallel fan-out exists to bound. |
| **A6** | EventBus queue overflow / backpressure | ⬜ **N/A — Phase 1 component** | The Crystal core has no `EventBus`. Its async-handoff surface is the **bounded** self-healing outbox (`core/queue.py`, SQLite/Redis), not an unbounded in-memory event queue. |
| **A7** | Neo4j transaction deadlock / lock ordering | ⬜ **N/A — optional Neo4j only** | The default L3 is single-process (mock / on-disk SQLite); there is no concurrent multi-writer Cypher path to deadlock. Lock-ordering applies only when the optional Neo4j backend is enabled (Phase 1+). |
| **A8** | Soft→hard delete lifecycle / GC | ✅ **Partially satisfied** | GDPR Art. 17 erasure already performs **hard** physical deletion across L0/L1/L3 + outbox with content-free tombstones (`core/erasure.py`); the audit log is the accountable record. A scheduled background GC daemon remains future work. |
| **A9** | LLM call safety (rate-limit / timeout / bounded retry) | ✅ **Implemented here** | `core/generation.py` `AnthropicGenerator`: bounded retry with exponential backoff on **transient** failures (429 / timeout / overload), non-transient errors are not retried, output token ceiling, and graceful degradation to the extractive generator. Dependency-free; tested with a stub client. |
| **A10** | aioredis connection pool limits | ⬜ **N/A by design** | The core uses no `aioredis`. The optional Redis queue backend uses a synchronous client behind the swappable `core/queue.py`; the default queue is dependency-free SQLite. |

## Summary

- **Already satisfied by the architecture:** A1, A2, A3 (and A8 in its erasure form).
- **Implemented in this sprint:** **A9** (LLM call safety).
- **Not applicable to the dependency-free core:** A4, A5, A6, A7, A10 — these harden
  the optional Phase‑1 stack (Neo4j write-path, async `EventBus`, `aioredis`) and
  will be wired *if and when* those components are activated, not before.

This is the deliberate trade-off of the open core: fewer moving parts, fewer
failure modes, and no heavy dependencies — so several "production hardening"
patches are simply unnecessary here rather than pending.
