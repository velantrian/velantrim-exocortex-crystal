# ADR-021: Explicit Cross-Backend Migration Contract

- **Status:** Accepted architecture contract
- **Date:** 2026-08-07
- **Issue:** #327
- **Runtime implementation:** only SQLite lifecycle exists; cross-backend import/cutover is not implemented

## Context

Crystal now locks the selected durable L3 backend and locator and provides a verified
SQLite backup/restore lifecycle. Without a separate migration contract, an operator or
future adapter could incorrectly treat profile editing, backend discovery, database copy,
or successful import as a safe backend transition.

That would weaken deployment continuity and could also blur Crystal's central distinction
between physical storage and epistemic authority.

## Decision

A backend or locator transition after data exists is a phased migration, not ordinary
configuration.

The required sequence is:

```text
preflight
→ deterministic read-only logical export
→ completed bundle
→ independent verification
→ inactive target import
→ exact state equivalence
→ retrieval-quality evaluation
→ explicit cutover
→ optional explicit rollback
```

The source remains authoritative until a cutover receipt is created. Each phase fails
closed and produces evidence specific to that operation.

Migration receipts prove operation integrity only. They do not prove claim truth or grant
strict Canon membership.

The first implementation slice is limited to deterministic SQLite logical export and
independent verification.

## Consequences

- editing/deleting the storage profile is not migration;
- backend availability cannot trigger automatic switching after data exists;
- import success cannot activate a target;
- exact state equivalence is a blocking gate independent of vector retrieval quality;
- approximate indexes remain derived/rebuildable projections;
- no dual-write or live cutover is part of the first implementation;
- PostgreSQL/pgvector remains an optional proposed institutional profile;
- the default runtime remains pure standard library and SQLite remains the verified
  baseline;
- future import, cutover and rollback require separate reviewed implementation PRs.

## Rejected alternatives

### Silent capability-based switching

Rejected because installed packages or server reachability can change between restarts and
select a different physical store without proving state continuity.

### Profile edit/delete as migration

Rejected because it changes deployment identity without exporting, importing or comparing
state.

### Direct database-file copy as universal format

Rejected because an engine-specific file is not a backend-neutral logical contract and
cannot be independently imported by another backend.

### Dual-write first

Rejected for the initial implementation because it introduces ordering, fencing, partial
commit and reconciliation complexity before a deterministic offline path exists.

### Retrieval benchmark as migration proof

Rejected because recall/latency does not prove that authority-bearing state, restrictions,
evidence or audit continuity survived.

## Related documents

- [Cross-Backend Storage Migration Contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [PostgreSQL + pgvector Institutional Profile RFC](../architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [Durable Storage Profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite Storage Lifecycle](../architecture/SQLITE_STORAGE_LIFECYCLE.md)
