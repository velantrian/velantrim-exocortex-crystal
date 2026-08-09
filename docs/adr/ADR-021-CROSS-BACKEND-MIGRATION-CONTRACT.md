<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# ADR-021: Explicit Cross-Backend Migration Contract

- **Status:** Accepted and partially implemented
- **Date:** 2026-08-07
- **Decision issue:** #327
- **SQLite export implementation:** #331 / PR #335
- **Inactive PostgreSQL import and exact equivalence:** #332 / PR #337
- **Active runtime cutover:** not implemented

## Context

Crystal locks the selected durable L3 backend and locator and provides a verified SQLite
backup/restore lifecycle. It also implements bounded deterministic SQLite logical export,
independent bundle verification, inactive PostgreSQL/pgvector import and exact equivalence
for the approved physical-L3 datasets.

Without a separate migration contract, an operator or future adapter could incorrectly treat
profile editing, backend discovery, database copy or successful import as a safe backend
transition.

That would weaken deployment continuity and blur Crystal's distinction between physical
storage and epistemic authority.

## Decision

A backend or locator transition after data exists is a phased migration, not ordinary
configuration.

```text
preflight                                  [implemented]
→ deterministic read-only logical export   [implemented]
→ completed bundle publication             [implemented]
→ independent bundle verification          [implemented]
→ inactive target import                    [implemented for PostgreSQL]
→ exact state equivalence                   [implemented for approved datasets]
→ retrieval-quality evaluation              [not implemented]
→ explicit cutover and fencing              [not implemented]
→ optional explicit rollback                [not implemented]
```

The source remains authoritative until a separately reviewed cutover receipt exists.

Each phase fails closed and produces evidence specific to that operation. Completion of one
phase does not imply activation or completion of a later phase.

Migration receipts prove operation integrity only. They do not prove claim truth, perform
TruthGate admission or grant strict Canon membership.

## Implemented boundary

Current merged baseline:

```text
locked durable SQLite profile
→ backup / verify / inactive restore
→ bounded deterministic logical export
→ independently verified bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ fresh inactive target
→ serializable import
→ independent read-only target re-hash
→ exact count / byte / SHA-256 equivalence
→ active=false
```

The PostgreSQL target is absent from ordinary runtime composition and cannot serve normal
reads or writes.

## Consequences

- editing or deleting the storage profile is not migration;
- backend availability cannot trigger automatic switching after data exists;
- import success cannot activate a target;
- exact state equivalence is a blocking gate independent of retrieval quality;
- approximate indexes remain derived and rebuildable projections;
- no HNSW/IVFFlat index is part of the inactive-import baseline;
- no dual-write, cutover, rollback or active PostgreSQL runtime is implemented;
- SQLite remains the ordinary active local-first profile;
- PostgreSQL/pgvector remains an optional inactive migration/equivalence target;
- future ANN evaluation, cutover, fencing, rollback and server lifecycle require separate
  reviewed implementation PRs.

## Authority boundary

```text
physical L3              != strict Canon
migration bundle         != claim evidence
successful import        != activation
exact equivalence        != retrieval acceptance
PostgreSQL availability  != backend selection
```

Migration must not change Guardian decisions, TruthGate policy, contradiction dispositions,
restriction/erasure state or strict Canon membership except as an identical consequence of
preserved state.

## Rejected alternatives

### Silent capability-based switching

Rejected because installed packages or server reachability can change between restarts and
select a different physical store without proving continuity.

### Profile edit/delete as migration

Rejected because it changes deployment identity without export, import or independent
comparison.

### Direct database-file copy as universal format

Rejected because an engine-specific file is not a backend-neutral logical contract.

### Dual-write first

Rejected because it introduces ordering, fencing, partial-commit and reconciliation
complexity before a deterministic offline path and exact equivalence proof.

### Retrieval benchmark as migration proof

Rejected because recall and latency do not prove authority-bearing state, restrictions,
evidence or audit continuity survived.

### Successful import as activation

Rejected because import integrity does not establish runtime selection, fencing, backup
readiness, rollback safety or production authorization.

## Remaining decisions

Separate future ADRs or amendments are required for:

1. exact-vs-ANN acceptance thresholds;
2. source/target fencing and cutover receipts;
3. rollback window, expiry and crash behavior;
4. PostgreSQL backup/restore/upgrade lifecycle;
5. production roles, secrets, certificates, pooling and retries;
6. multi-process concurrency and observability.

## Related documents

- [Cross-Backend Storage Migration Contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [PostgreSQL Inactive Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL + pgvector Profile RFC](../architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [Durable Storage Profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite Storage Lifecycle](../architecture/SQLITE_STORAGE_LIFECYCLE.md)
