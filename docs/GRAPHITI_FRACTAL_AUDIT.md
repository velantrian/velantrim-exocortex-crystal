# Graphiti Fractal Compatibility Audit

**Status:** research audit / RFC note  
**Runtime status:** not implemented in Crystal current core  
**Scope:** documentation only  
**Audience:** reviewers, maintainers, future implementation work  

This document records what can and cannot be safely borrowed from a Graphiti-style temporal/fractal memory system into **Velantrim Exo-Cortex Crystal**.

It is intentionally conservative. Crystal remains a local-first, verifiable memory core. It does not adopt mandatory Graphiti, Neo4j, OpenAI embeddings, autonomous consolidation, or LLM-synthesized facts as runtime behavior.

---

## 1. Crystal boundary

Crystal's identity is unchanged:

- pure-stdlib runtime by default;
- local-first, no mandatory cloud;
- no mandatory Graphiti, Neo4j, OpenAI, Redis, Kafka, or vector DB;
- no silent writes to the canonical graph;
- no LLM output promoted directly into verified L3 facts;
- no write-enabled MCP path into canon;
- all canon writes remain gated by ingest, provenance, TruthGate, Guardian, TRACE, and Receipt semantics.

Graphiti-style systems may inspire **implementation patterns**. They must not become the Crystal truth authority.

---

## 2. High-value patterns to consider

### 2.1 RRF for hybrid retrieval

**Recommended priority:** P0.5 / first implementation PR.

Crystal already uses multiple retrieval signals. Add a pure-Python Reciprocal Rank Fusion helper to combine lexical, vector, and graph-walk rankings without mixing incompatible score scales.

Constraints:

- RRF ranks candidates only.
- RRF must not assign `truth_status`.
- RRF must not bypass FactsPack.
- RRF must not bypass TruthGate or Guardian.

Suggested helper:

```python
def rrf_fuse(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item_id in enumerate(ranking, start=1):
            scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
```

### 2.2 Two-stage ingest dedup

**Recommended priority:** P0.5 / second implementation PR.

Add ingest idempotency before canon insertion:

1. Exact fingerprint: `sha256(normalize(text))`.
2. Optional near-duplicate check if an embedder is available.

Constraints:

- Exact fingerprinting must be stdlib-only.
- Near-duplicate cosine checks must remain optional.
- Re-ingesting the same utterance should not create a duplicate canon node.
- Duplicates should update `last_seen`, `observation_count`, or source occurrence metadata instead.

### 2.3 Bulk node fetch for graph-walk

**Recommended priority:** P0.5 / third implementation PR.

Avoid N+1 lookups during graph traversal. Add a batch method such as:

```python
get_nodes(ids: Iterable[str]) -> dict[str, NodeRecord]
```

Constraints:

- Preserve epistemic metadata: `truth_status`, `claim_type`, `source_ref`, `evidence_ref`, `confidence`.
- Do not return bare content-only nodes.
- Keep graph traversal budgeted.

### 2.4 Latency benchmark harness

**Recommended priority:** P1.

Add a minimal benchmark script for ingest and retrieval.

Metrics to collect:

- retrieve p50 / p95 / p99 latency;
- ingest latency;
- graph nodes visited;
- candidate count;
- FactsPack build time;
- TRACE build time;
- Receipt verification time.

This should be a measurement tool, not an optimization claim.

---

## 3. Medium-term patterns

### 3.1 SQLite outbox and failed events

A safe slow-path foundation can be built without Redis or Kafka.

Recommended minimal schema:

```sql
memory_outbox_events(
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  source_ref TEXT,
  trace_id TEXT,
  created_at TEXT NOT NULL,
  status TEXT NOT NULL,
  retry_count INTEGER NOT NULL DEFAULT 0,
  last_error TEXT
)
```

Rules:

- Outbox events are audit records, not canon writes.
- Slow workers may create candidates, not verified facts.
- Candidates must pass Pending, TruthGate, and Guardian before L3.

### 3.2 Circuit breaker and degraded TRACE

If optional graph/vector/LLM backends fail, Crystal should fail safely and visibly.

Suggested behavior:

- graph backend unavailable -> fallback to BM25;
- record `degraded_mode=true` in TRACE;
- include unavailable components;
- apply a confidence cap when retrieval is degraded;
- never hide backend failure from the audit trail.

### 3.3 Embedding cache

Useful only for optional SentenceTransformer/SBERT paths.

Rules:

- Do not make embeddings mandatory.
- Cache key: `sha256(text) + embedder_tag`.
- Store model tag, vector dimension, and expiry metadata.
- Avoid storing raw text in the cache by default.

### 3.4 Local graph export

A D3/static viewer can help inspect L3, but it must be local-first and privacy-aware.

Default export rules:

- no CDN;
- no outbound calls;
- PII redaction enabled by default;
- `VERIFIED` records only by default;
- pending, evidence spans, and source snippets require explicit flags.

### 3.5 Bi-temporal validity

`valid_from`, `valid_to`, `observed_at`, and `recorded_at` are useful, but this is a schema-level change.

Rules:

- Handle through a separate RFC and migration.
- Do not mix with RRF, dedup, or benchmark PRs.
- Preserve Receipt replay compatibility.

---

## 4. Explicit non-adoptions

Do **not** adopt:

- mandatory Neo4j / Graphiti / OpenAI dependencies;
- Graphiti as Crystal's Core Truth Store;
- LLM-synthesized L3 facts;
- write-enabled MCP tools for canon writes;
- automatic chat-turn persistence as facts;
- autonomous strategy updates;
- deletion of verified truth by decay or archival;
- Graphiti output feeding answers directly without FactsPack and TruthGate.

---

## 5. Safe sidecar model

Graphiti-style temporal memory may later be considered only as an optional sidecar:

```text
event_outbox
-> temporal sidecar
-> ClaimCandidate / EpisodeCandidate
-> Pending
-> TruthGate
-> Guardian
-> optional L3 link
```

It must never become:

```text
Graphiti -> L3 directly
Graphiti -> Answer directly
Graphiti -> TruthGate override
```

---

## 6. Recommended implementation order

1. RRF retrieval fusion.
2. Exact ingest dedup.
3. Batch graph node fetch.
4. Latency benchmark harness.
5. SQLite outbox / failed events.
6. Circuit breaker / degraded TRACE.
7. Optional embedding cache.
8. Local graph export.
9. Bi-temporal validity RFC.
10. Community clustering as navigation only.
11. Optional Neo4j index hardening.
12. Optional Graphiti temporal sidecar only after Crystal core is stable.

---

## 7. Reviewer-safe wording

Use:

> Crystal may adopt selected dependency-free patterns inspired by temporal knowledge-graph memory systems, such as rank fusion, ingest idempotency, batch graph access, benchmarking, and safe slow-path event handling. These patterns do not replace Crystal's TruthGate, provenance, TRACE, Receipt, or local-first guarantees.

Avoid:

> Crystal uses Graphiti.

> Crystal automatically learns from chat memory.

> Crystal stores LLM-extracted facts directly into L3.

> Crystal has autonomous long-term memory consolidation.

---

## 8. Final rule

**Borrow mechanisms. Do not borrow authority.**

Graphiti-style systems can inspire retrieval, consolidation, and observability patterns. They cannot become Crystal's truth source.