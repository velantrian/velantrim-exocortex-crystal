<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Storage and Authority Boundaries

**Status date:** 2026-08-08  
**Purpose:** stable architecture contract for storage, migration and epistemic authority.

## 1. Separate identities

```text
storage profile    = deployment identity
physical L3        = multi-status graph state
strict Canon       = trusted read projection
migration bundle   = operation evidence
retrieval score    = ranking signal
model output       = generated text
```

None of these identities automatically implies another. Storage, retrieval, migration and
model output cannot bypass Guardian or TruthGate.

## 2. Durable runtime profile

SQLite is the ordinary active local-first profile. A durable first-run `auto` may select
optional LadybugDB if installed, otherwise SQLite. The chosen backend, schema version and
non-secret locator digest are persisted atomically and reused.

The runtime fails closed on backend, locator or schema conflict. It does not silently switch
to ephemeral Mock. Explicit Mock remains available for development and CI only when no
durable profile exists.

## 3. Physical L3 and strict Canon

Physical L3 can contain accepted, disputed, superseded, restricted, erased or otherwise
non-canonical graph records. Strict Canon is a deny-dominant projection that admits only
records allowed by current evidence and policy.

```text
stored in L3 ≠ trusted answer material
retrieved      ≠ admitted
high score     ≠ evidence
frequent copy  ≠ independent corroboration
```

## 4. SQLite lifecycle

Current verified local-first lifecycle:

```text
active SQLite store
→ backup
→ independent verification
→ inactive restore
→ bounded logical export
→ deterministic bundle verification
```

Inactive restore and logical export preserve state for operations; they do not perform
TruthGate admission or select a different runtime backend.

## 5. Cross-backend migration

The implemented physical-L3 portability phase supports a verified logical bundle and an
optional inactive PostgreSQL/pgvector target:

```text
completed verified bundle
→ PostgreSQL version / pgvector / TLS preflight
→ fresh inactive target schema
→ serializable import
→ independent read-only canonical re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipt
→ active=false
```

This covers bounded physical-L3 state equivalence only. It does not migrate every subsystem
such as L1 operational state, audit logs, outbox state, encryption metadata or configuration.

## 6. Explicitly absent lifecycle stages

Not implemented:

- active PostgreSQL read/write runtime adapter;
- automatic SQLite/PostgreSQL selection or switching;
- source fencing and explicit cutover receipt;
- rollback proof and rollback-expiry policy;
- dual-write;
- accepted exact-vs-ANN production retrieval profile;
- PostgreSQL production backup/restore/upgrade lifecycle;
- production role provisioning, pooling, IdP/multi-tenancy or distributed fencing.

## 7. Secret and privacy boundary

Credentials and credential-bearing DSNs must not enter profiles, bundles, receipts, logs,
issues or Notion. Endpoint identity is represented only through non-secret digests.

Migration and backup create additional copies. Erasure from the active store does not
implicitly erase those copies. Operators need inventory, retention and deletion procedures.

## 8. Authority table

| Event | What it proves | What it does not prove |
|---|---|---|
| record stored in L3 | physical persistence | strict Canon membership |
| retrieval result | candidate relevance | evidence sufficiency |
| backup verified | backup integrity | claim truth |
| inactive restore verified | state equivalence | admission or activation |
| PostgreSQL import succeeds | transactional import | runtime selection |
| exact equivalence receipt | physical bundle equality | production readiness or cutover |
| curator override | explicit governance action | rewritten TruthGate policy |

## 9. Detailed English sources

- [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [Cross-backend migration contract](./architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](./adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
