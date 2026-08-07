# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-07  
**Verified runtime checkpoint:** `c612c1f` / PR #330  
**Exact evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

English is the authoritative active GitHub documentation language. Localized README files
are frozen snapshots pending a dedicated final reconciliation pass.

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
| Pluggable physical L3 | Implemented baseline | locked durable profile; SQLite verified local-first default |
| TruthGate / Guardian | Implemented | admission/safety owners; storage cannot bypass them |
| Strict CanonicalView / TrustSnapshot | Implemented | deny-dominant projection; physical L3 is not strict Canon |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary query paths do not mutate canonical truth state |
| TRACE, receipts and replay | Implemented | proof path; receipt alone is not truth |
| Explicit contradiction decisions | Implemented | `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`; no automatic winner |
| Scoped curator authorization | Implemented baseline | process-local lease; production IdP/distributed fencing external |
| Bounded legacy retrieval / reindex | Implemented | bounded degraded recall and explicit reindex refusal |
| Durable L3 profile lock | Implemented and tested | durable backend/locator identity persists across restarts |
| SQLite backup/verify/restore lifecycle | Implemented and tested | restore is inactive/no-clobber and never admission |
| Race-safe stale-lock recovery | Implemented and tested | explicit operator action; not distributed fencing |
| SQLite logical export/verify | Implemented and tested | canonical bundle, independent verification, local-first limits |
| Cross-backend migration architecture | Accepted | phased contract; target import/cutover absent |
| Institution-scale streaming migration | Not implemented | issue #331; blocks server-profile migration claims |
| PostgreSQL/pgvector institutional profile | Proposed | issue #332; no driver, dependency, schema or runtime adapter |
| Automatic SQLite/PostgreSQL switching | Forbidden | backend availability is not migration |
| Reader Core / Semantic Reading Layer | Not implemented | future candidate layer upstream of normal admission |

## Current storage sequence

```text
first durable startup
→ persist backend + non-secret locator

SQLite lifecycle
→ online backup
→ independent verification
→ restore to new inactive database/profile

verified logical portability
→ deterministic SQLite export
→ completed canonical bundle
→ independent fail-closed verification
```

Future work, not current runtime:

```text
streaming/incremental migration (#331)
→ inactive PostgreSQL import (#332)
→ exact state equivalence
→ retrieval evaluation
→ explicit cutover
→ optional rollback
```

## Resource boundary

The merged logical export is intentionally bounded:

```text
source SQLite <= 64 MiB
record <= 1 MiB
dataset <= 64 MiB
records per dataset <= 200,000
aggregate JSONL <= 384 MiB
```

These limits bound the current materializing implementation. They do not prove operation
with arbitrarily large stores or institutional-scale workloads.

## Non-claims

Crystal does not currently claim PostgreSQL/pgvector runtime support, automatic migration,
dual-write, live cutover, distributed exactly-once behavior, production multi-tenancy,
universal truth detection, zero hallucinations, legal/security certification, Titan runtime
integration, consciousness or a complete human-like exocortex.
