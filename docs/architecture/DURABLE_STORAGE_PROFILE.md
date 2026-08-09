<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# 🔒 Durable L3 Storage Profile and Doctor

**Status:** IMPLEMENTED / TESTED / MERGED BASELINE  
**Runtime checkpoint:** PR #325 and later status/runtime checkpoints through PR #337  
**Current ordinary profile:** SQLite  
**Authority boundary:** storage profile = deployment identity, not strict Canon authority

## Purpose

Crystal's environment-selected L3 backend must not drift silently between processes or
restarts. A dependency, working directory, path, permission or filesystem change must not
make a deployment select a different physical graph without an explicit migration.

```text
Physical L3 = multi-status storage and retrieval state
Strict Canon = deny-dominant trusted read projection
Storage profile = deployment identity, not epistemic authority
```

## Runtime contract

Environment-selected singleton construction follows:

```text
read VELANTRIM_L3_BACKEND
→ read and validate the durable storage profile
→ reject backend or locator conflicts
→ construct the locked backend
→ verify the constructed backend and non-secret locator
→ cache the process-local singleton
```

First durable startup:

```text
requested sqlite / ladybug / neo4j
→ construct explicitly
→ atomically persist backend + non-secret locator

requested auto
→ try optional LadybugDB
→ otherwise durable SQLite
→ persist the durable winner
→ never silently accept ephemeral Mock
```

A later `auto` request reuses the locked profile. Installed packages or server reachability
must not trigger automatic switching after data exists.

## Profile path and contents

```text
VELANTRIM_STORAGE_PROFILE_PATH
default: ~/.velantrim/velantrim-storage-profile.json
```

The default profile path is anchored in the user's home directory. Local storage locators are
persisted as absolute paths so a later process launched from another working directory reuses
the same physical store.

The profile records only:

- profile schema version;
- backend name;
- durable flag;
- local path, or Neo4j URI and database name;
- SHA-256 of the backend/locator identity.

It never records passwords, tokens, private keys or `NEO4J_PASSWORD`.

## Fail-closed behavior

Crystal raises `StorageProfileError` before caching a backend when:

- the profile is malformed;
- its locator checksum is invalid;
- the requested backend conflicts with the locked backend;
- an explicitly supplied locator conflicts with the locked locator;
- the locked optional dependency is unavailable;
- construction returns a different backend or locator;
- first-run `auto` reaches the in-memory Mock backend;
- first-run `auto` resolves to an ephemeral local locator;
- concurrent initializers select different durable targets.

No automatic migration, copying, dual-write or profile repair occurs.

## Explicit Mock and programmatic instances

`VELANTRIM_L3_BACKEND=mock` remains available for deliberate development and CI when no
durable profile exists. It is explicit and ephemeral and does not create a durable profile.

A programmatic call such as `get_l3_graph(backend="mock")` returns a fresh uncached instance.
This supports tests and deliberate migration/inspection tooling without changing the
environment-selected singleton.

## Read-only diagnostics

```bash
velantrim-doctor
```

The doctor validates profile consistency without opening Canon for writes or repairing state.

| Exit | Status | Meaning |
|---:|---|---|
| `0` | `PASS` | locked configuration is internally consistent |
| `1` | `WARN` | initialization is pending or a bounded non-fatal condition exists |
| `2` | `FAIL` | profile, dependency, backend or locator safety failed |

The doctor:

- validates the profile and checksum;
- compares the requested backend with the lock;
- checks optional package availability;
- checks local directory writability and instance presence;
- reports server locator identity without exposing secrets;
- never writes L3, changes strict Canon or repairs configuration.

## Migration boundary

Changing SQLite, LadybugDB, Neo4j or any future active PostgreSQL profile after data exists
requires a separate explicit migration workflow.

```text
profile edit/delete       != migration
backend availability      != migration
successful import         != activation
exact equivalence receipt != cutover
```

Deleting or editing the profile is not migration.

## Current PostgreSQL boundary

PostgreSQL/pgvector is no longer only a future RFC. The merged baseline implements an
optional, lazy-loaded **inactive import and exact-equivalence target**:

```text
verified logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ fresh inactive schema
→ serializable import
→ independent read-only canonical re-hash
→ exact equivalence
→ active=false
```

The target is absent from ordinary runtime composition and cannot serve normal reads or
writes. This does not add:

- active PostgreSQL runtime selection;
- automatic SQLite/PostgreSQL switching;
- exact-vs-ANN retrieval acceptance;
- cutover, rollback or dual-write;
- PostgreSQL production backup/restore/upgrade lifecycle.

## Grant and certification boundary

This profile is deployment hardening of the local-first foundation. It adds no mandatory
third-party dependency, cloud requirement, new truth owner or production certification.

The NLnet proposal remains submitted / under review / not awarded.

## Related documents

- [Full architecture](../ARCHITECTURE.md)
- [Storage and authority boundaries](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [SQLite storage lifecycle](./SQLITE_STORAGE_LIFECYCLE.md)
- [Cross-backend migration contract](./CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](./POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector profile RFC](./POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
