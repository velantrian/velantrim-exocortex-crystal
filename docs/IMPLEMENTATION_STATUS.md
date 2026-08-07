# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `f03e24c` / PR #335  
**Exact evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | storage and migration cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented and tested | restore is inactive and never admission |
| SQLite logical export/verify | Implemented and tested | canonical backend-neutral bundle |
| Bounded-streaming logical migration | Implemented and tested | fixed batches, disk-backed sort/reference checks, same-descriptor verification |
| Resource benchmark evidence | Observed | 1,025 and 8,193 synthetic corpora; not a production SLO |
| PostgreSQL/pgvector institutional profile | Proposed | #332; no driver, schema, importer or runtime adapter |
| Inactive PostgreSQL import / exact equivalence | Not implemented | next separately reviewed phase |
| Automatic SQLite/PostgreSQL switching | Forbidden | backend availability is not migration |
| Cutover / rollback / dual-write | Not implemented | later explicit phases only |
| Reader Core / Semantic Reading Layer | Not implemented | candidate layer upstream of normal admission |

## Current storage sequence

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ fixed cursor batches
→ deterministic canonical JSONL
→ disk-backed canonical edge ordering
→ same-descriptor independent verification
→ disk-backed referential integrity
```

Issue #331 is implemented by PR #335. Active limits remain 64 MiB source/dataset, 200,000
records per dataset and 384 MiB aggregate JSONL. The benchmark is evidence for tested
local-first corpora, not arbitrary scale or a production SLO.

Future work:

```text
inactive PostgreSQL/pgvector import (#332)
→ exact state equivalence
→ exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ optional explicit rollback
→ server backup/restore/upgrade lifecycle
```

Crystal does not claim PostgreSQL runtime, automatic migration, production multi-tenancy,
universal truth, zero hallucinations, legal/security certification or consciousness.
