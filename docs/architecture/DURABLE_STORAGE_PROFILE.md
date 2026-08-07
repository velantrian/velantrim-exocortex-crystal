# 🔒 Durable L3 Storage Profile and Doctor

**Status:** implemented by the accompanying change; `TESTED` and `VERIFIED_CHECKPOINT`
remain contingent on exact-head CI and merge evidence.

## Purpose

Crystal's environment-selected L3 backend previously evaluated `auto` independently in
each process:

```text
LadybugDB if available
  → otherwise SQLite
  → otherwise in-memory Mock
```

That behavior was convenient for a prototype, but it could make one durable deployment
appear empty after a dependency, working directory, path, permission or filesystem change.
A new process could select a different physical graph without an explicit migration.

This contract makes the deployment choice stable without making a graph node equivalent
to strict Canon.

```text
Physical L3 = multi-status storage and retrieval projection
Strict Canon = deny-dominant trusted read projection
Storage profile = deployment identity, not epistemic authority
```

## Runtime contract

Environment-selected singleton construction now follows:

```text
read VELANTRIM_L3_BACKEND
  → read and validate the durable storage profile
  → reject backend or locator conflicts
  → construct the locked backend
  → verify the constructed backend and non-secret locator
  → cache the process-local singleton
```

On the first durable startup:

```text
requested sqlite / ladybug / neo4j
  → construct explicitly
  → atomically persist backend + non-secret locator

requested auto
  → try LadybugDB
  → otherwise SQLite
  → persist the durable winner
  → never silently accept Mock
```

The profile path is controlled by:

```text
VELANTRIM_STORAGE_PROFILE_PATH
default: ~/.velantrim/velantrim-storage-profile.json
```

The default is anchored in the user's home directory rather than the process working
directory. The first durable startup stores the selected local backend path as an absolute
locator, so a later process launched from another directory reuses the same profile and
physical L3. Deployments that need a system, container or service-specific location should
set `VELANTRIM_STORAGE_PROFILE_PATH` explicitly.

The profile records only:

- schema version;
- backend name;
- durable flag;
- local path, or Neo4j URI and database name;
- SHA-256 of the backend/locator identity.

It never records passwords, tokens or `NEO4J_PASSWORD`.

## Fail-closed behavior

Crystal raises `StorageProfileError` before caching the backend when:

- the profile is malformed;
- its locator checksum is invalid;
- the requested backend conflicts with the locked backend;
- an explicitly supplied locator conflicts with the locked locator;
- the locked optional dependency is unavailable;
- construction returns a different backend or locator;
- first-run `auto` reaches the in-memory Mock backend;
- concurrent initializers select different durable targets.

No automatic migration, copying, dual-write or profile repair occurs.

## Explicit Mock and programmatic instances

`VELANTRIM_L3_BACKEND=mock` remains available for development and CI when no durable
profile exists. It is explicit, ephemeral and does not create a profile.

A programmatic explicit call such as `get_l3_graph(backend="mock")` still returns a fresh,
uncached instance. This supports tests and deliberate migration/inspection tooling without
changing the environment-selected runtime singleton.

## Read-only diagnostics

After installation:

```bash
velantrim-doctor
```

The command emits JSON and exits with:

| Exit | Status | Meaning |
|---:|---|---|
| `0` | `PASS` | locked configuration is internally consistent |
| `1` | `WARN` | initialization is pending or a non-fatal condition exists |
| `2` | `FAIL` | profile, dependency, backend or locator safety failed |

The doctor:

- validates the profile and checksum;
- compares the requested backend with the lock;
- checks optional package availability;
- checks local directory writability and instance presence;
- reports server locator identity without probing the network;
- never opens L3, writes Canon or repairs configuration.

## Migration boundary

Changing SQLite, LadybugDB, Neo4j or any future PostgreSQL profile requires a separate,
explicit migration workflow with dry-run, record/edge/evidence counts, hashes, restriction
and audit verification, rollback evidence and a migration receipt.

Deleting or editing the profile is not a migration.

## PostgreSQL and vector retrieval

This change deliberately adds no PostgreSQL, pgvector or dedicated VectorDB dependency.
Those remain a future institutional deployment RFC. Any such profile must preserve the
same authority, evidence, restriction, erasure, audit and replay invariants and must prove
migration equivalence before adoption.

## Grant boundary

This is deployment hardening of the existing local-first foundation:

- no new cognitive architecture;
- no mandatory third-party dependency;
- no cloud requirement;
- no automatic Canon switch;
- no claim of production certification;
- no change to TruthGate, Guardian or strict Canon membership.

## Cross-backend changes

Changing the locked backend or locator after data exists must follow the
[Cross-Backend Storage Migration Contract](./CROSS_BACKEND_MIGRATION_CONTRACT.md).
Editing or deleting the profile, installing an adapter, or observing server availability
is not migration. The [PostgreSQL + pgvector RFC](./POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
remains proposed and not runtime.
