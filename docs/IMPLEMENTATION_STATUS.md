# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `bbd816c` / PR #337  
**Exact evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | storage and migration cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented and tested | restore is inactive and never admission |
| Bounded-streaming SQLite logical export/verify | Implemented and tested | canonical backend-neutral bundle |
| PostgreSQL optional dependency and preflight | Implemented and tested | explicit extra, lazy load, pinned supported versions |
| Inactive PostgreSQL/pgvector import | Implemented and tested | new inactive schema only; no ordinary reads/writes |
| Exact target-state equivalence | Implemented and tested | approved bundle datasets; independent read-only re-hash |
| Active PostgreSQL runtime adapter | Not implemented | target is not registered in normal runtime composition |
| Automatic SQLite/PostgreSQL switching | Forbidden | availability and import success are not selection |
| Exact-vs-ANN retrieval evaluation | Not implemented | later separately reviewed phase |
| Cutover / rollback / dual-write | Not implemented | explicit later phases only |
| PostgreSQL server lifecycle | Not implemented | backup/restore/upgrade/pooling remain future work |
| Reader Core / Semantic Reading Layer | Not implemented | candidate layer upstream of normal admission |

## Current storage sequence

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

Issues #331 and #332 are implemented by PRs #335 and #337. The default installation remains
pure standard library; PostgreSQL support is an optional operator path. `active=false` is
constrained in the target control state and successful equivalence cannot activate a
backend or change Guardian, TruthGate or strict Canon.

Future work:

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal does not claim an active PostgreSQL runtime backend, automatic migration,
production multi-tenancy, universal truth, zero hallucinations, legal/security
certification or consciousness.