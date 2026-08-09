<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Storage and Authority Boundaries

**Status date:** 2026-08-09  
**Purpose:** stable architecture contract for storage, migration and epistemic authority.  
**Runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`.

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
optional LadybugDB if installed, otherwise SQLite. The chosen backend and non-secret locator
identity are persisted atomically and reused.

The runtime fails closed on backend or locator conflict. It does not silently switch to
ephemeral Mock. Explicit Mock remains available for deliberate development and CI when no
durable profile is being claimed.

Neo4j is an explicit optional remote/server adapter and expands the trust boundary.

## 3. Physical L3 and strict Canon

Physical L3 can contain verified, user-claimed, unverified, hypothetical, subjective,
contested, superseded or restricted records. Erasure removes active-store material under the
implemented erasure contract; independent copies require separate handling.

Strict Canon is a deny-dominant projection that admits only records allowed by current
evidence and policy.

```text
stored in L3 ≠ trusted answer material
retrieved     ≠ admitted
high score    ≠ evidence
frequent copy ≠ independent corroboration
```

## 4. Read and write separation

Public query surfaces route through `core.query_pipeline.query()` and remain read-only with
respect to canonical truth state.

```text
HTTP /ask
CLI ask
MCP search / inspection
→ read-only retrieval
→ trace / answer / bounded refusal
```

Explicit ingest is the admission-capable path:

```text
source-linked candidate
→ Guardian
→ TruthGate
→ operational state + physical L3
→ strict read projection
```

## 5. SQLite lifecycle

Current verified local-first lifecycle:

```text
active SQLite store
→ backup
→ independent verification
→ inactive restore
→ bounded logical export
→ deterministic bundle verification
```

Inactive restore and logical export preserve state for operations. They do not perform
TruthGate admission or select a different runtime backend.

## 6. Cross-backend migration

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

This covers bounded approved physical-L3 datasets only. It does not migrate every subsystem,
including all L1 operational state, audit/outbox state, encryption metadata or deployment
configuration.

## 7. Explicitly absent lifecycle stages

Not implemented:

- active PostgreSQL read/write runtime adapter;
- automatic SQLite/PostgreSQL selection or switching;
- source fencing and explicit cutover receipt;
- rollback proof and rollback-expiry policy;
- dual-write;
- accepted exact-vs-ANN production retrieval profile;
- PostgreSQL production backup/restore/upgrade lifecycle;
- production role provisioning, pooling, IdP/multi-tenancy or distributed fencing.

## 8. Source-grounded document ingestion

Source spans and import-session evidence are implemented baseline. Document records and
candidate claims remain upstream of ordinary Guardian and TruthGate admission.

A dedicated Reader Core for multi-pass reading, coverage maps, exception tracking,
contradiction-aware rereading and document-level synthesis is not implemented.

## 9. Secret and privacy boundary

Credentials and credential-bearing DSNs must not enter profiles, bundles, receipts, logs,
issues or Notion. Endpoint identity is represented through non-secret digests.

Migration and backup create additional copies. Erasure from the active store does not
implicitly erase those copies. Operators need inventory, retention and deletion procedures.

Selected L1 field encryption is not universal encryption.

## 10. Authority table

| Event | What it proves | What it does not prove |
|---|---|---|
| record stored in L3 | physical persistence | strict Canon membership |
| retrieval result | candidate relevance | evidence sufficiency |
| backup verified | backup integrity | claim truth |
| inactive restore verified | restored state integrity | admission or activation |
| PostgreSQL import succeeds | transactional import | runtime selection |
| exact equivalence receipt | approved dataset equality | production readiness or cutover |
| curator override | explicit audited governance action | rewritten TruthGate policy |

## 11. Current non-claims

Crystal does not claim active PostgreSQL runtime, automatic migration, accepted ANN
production quality, cutover, rollback, dual-write, production multi-tenancy, distributed
exactly-once coordination, security/legal/GDPR certification or awarded NLnet funding.

## 12. Detailed English sources

- [Full architecture](./ARCHITECTURE.md)
- [Architecture overview](./ARCHITECTURE_OVERVIEW.md)
- [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [Cross-backend migration contract](./architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](./adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
