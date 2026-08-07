# Implementation Status: Crystal vs Full Exo-Cortex

**Status date:** 2026-08-07
**Verified runtime checkpoint:** `b0df17a` / PR #325
**Exact test evidence:** [TEST_REPORT.md](../TEST_REPORT.md)
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

English is the authoritative active GitHub documentation language. Localized README files
are frozen snapshots pending a dedicated final translation pass.

## Status vocabulary

- **Implemented** — code exists.
- **Tested** — named tests pass at an exact SHA.
- **Wired** — composed into the intended runtime path.
- **Enabled** — active under the relevant configuration.
- **Observed** — demonstrated in a named runtime.
- **Proposed** — issue/RFC/architecture only.

## Current implementation table

| Component | Status | Current boundary |
|---|---|---|
| Local-first L0/L1 storage | Implemented | in-process cache plus SQLite/WAL operational state |
| Pluggable physical L3 | Implemented baseline | locked durable profile; SQLite baseline plus optional adapters |
| TruthGate / Guardian | Implemented | admission/safety owners; no storage backend may bypass them |
| Strict CanonicalView / TrustSnapshot | Implemented | deny-dominant read projection; physical L3 is not strict Canon |
| Read-only HTTP/CLI/MCP query boundary | Implemented | query paths do not mutate canonical truth state |
| TRACE, receipts and replay | Implemented | proof path; receipt alone is not truth |
| Explicit contradiction decisions | Implemented | `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`; no automatic winner |
| Scoped curator authorization | Implemented baseline | process-local lease; production IdP and distributed fencing external |
| Bounded legacy retrieval / reindex | Implemented | bounded degraded recall and explicit reindex |
| Durable L3 profile lock | Implemented and tested | first durable selection persists across restarts |
| SQLite backup/verify/restore lifecycle | Implemented and tested | restore is inactive/no-clobber and never admission |
| Race-safe legacy stale-lock recovery | Implemented and tested | explicit operator action; not distributed fencing |
| Cross-backend migration architecture | Accepted | phased contract; runtime import/cutover absent |
| SQLite logical migration export/verify | Not implemented yet | approved next narrow runtime slice |
| PostgreSQL/pgvector institutional profile | Proposed | no driver, dependency, schema or runtime adapter |
| Automatic SQLite/PostgreSQL switching | Not implemented / forbidden | backend availability is not migration |
| Reader Core / Semantic Reading Layer | Not implemented | future source-linked candidate layer upstream of admission |

## Current storage sequence

```text
first durable startup
→ persist backend + non-secret locator

SQLite lifecycle
→ online backup
→ independent verification
→ restore to new inactive database/profile
→ separate explicit activation decision

future cross-backend sequence
→ deterministic logical export
→ verify
→ inactive import
→ exact equivalence
→ retrieval evaluation
→ explicit cutover
```

## Non-claims

Crystal does not currently claim PostgreSQL/pgvector support, automatic migration,
dual-write, live cutover, distributed exactly-once behavior, production multi-tenancy,
universal truth detection, zero hallucinations, legal/security certification, Titan, or
consciousness.
