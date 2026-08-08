# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Current verified baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`

## ✅ Delivered baseline

Crystal includes the trust/evidence/query/storage lifecycle baseline plus:

- deterministic bounded-streaming SQLite logical export and verification;
- optional lazy PostgreSQL driver path;
- PostgreSQL 16 / pgvector 0.8.2 preflight;
- serializable import into a new inactive schema;
- independent exact-state equivalence and non-secret receipts;
- 2078 tests, 9756 statements, 100% coverage and 9/9 permanent CI;
- 1/1 real PostgreSQL/pgvector integration job.

## ✅ Completed — issues #331 and #332

PR #335 completed bounded logical migration. PR #337 completed only the first PostgreSQL
phase:

```text
verified bundle
→ PostgreSQL preflight
→ inactive target import
→ independent exact-state equivalence
→ receipts
```

The target remains `active=false`, cannot serve normal reads/writes and is not registered in
ordinary runtime composition. No activation, cutover, rollback, dual-write or automatic
switching was added.

## P1 — Exact-vs-ANN retrieval evaluation

- exact pgvector search as the reference;
- versioned HNSW/IVFFlat evaluation corpus;
- recall@k, filtered recall, latency, index size and rebuild evidence;
- ANN indexes remain rebuildable, non-authoritative projections.

## P1 — Explicit cutover and rollback proof

- source/target fencing;
- immutable cutover receipt;
- crash-window and partial-failure tests;
- explicit rollback receipt and expiry policy;
- no reachability-based backend selection.

## P1 — PostgreSQL server lifecycle and security

- least-privilege migration/read/runtime roles;
- TLS certificate and credential rotation;
- backup/restore/upgrade drills and retention;
- pooling, timeout/retry, observability and operator cleanup policy;
- no certification or distributed exactly-once overclaim.

## P2/P3 — Release evidence and Reader Core research

- reproducible artifacts, checksums, SBOM and dependency/action pinning;
- source-linked Reader Core prototype only upstream of Guardian/TruthGate.

**No grant award** or budget change is claimed. Active PostgreSQL runtime selection,
automatic switching, production multi-tenancy, universal truth, zero hallucinations and
legal certification remain out of scope.