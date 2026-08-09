<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Cross-Backend Storage Migration Contract

**Status:** accepted architecture contract; phases 1–6 implemented for the approved physical-L3 bundle, phases 7–9 not implemented  
**Decision issue:** #327  
**SQLite export phase:** issue #331 / PR #335  
**Inactive PostgreSQL import and exact equivalence:** issue #332 / PR #337  
**Ordinary active profile:** SQLite  
**PostgreSQL target:** inactive with `active=false`

## Purpose

Changing a physical storage backend is not a configuration edit. It is a controlled,
auditable transfer of state between independently identified deployments.

This contract does not grant any backend epistemic authority.

```text
backend availability     != migration
profile edit/delete      != migration
import success           != activation
migration receipt        != evidence for a claim
retrieval quality        != exact state equivalence
physical L3              != strict Canon
```

## Authority boundary

Migration moves physical state only. It must not:

- call or emulate TruthGate admission;
- change Guardian decisions;
- promote, demote, verify, invalidate, restrict, erase or resolve a claim;
- select a contradiction winner;
- convert vector similarity into evidence;
- change strict Canon membership except as the identical consequence of preserved state.

The source deployment remains authoritative until a separately reviewed explicit cutover
receipt exists. No cutover receipt exists in the current implementation.

## Phase model

```text
1. preflight                                [implemented]
2. deterministic read-only logical export   [implemented]
3. completed bundle publication             [implemented]
4. independent bundle verification           [implemented]
5. import into a new inactive target         [implemented for PostgreSQL]
6. exact state-equivalence evaluation        [implemented for approved bundle datasets]
7. retrieval-quality evaluation              [not implemented]
8. explicit cutover and fencing              [not implemented]
9. optional explicit rollback                [not implemented]
```

Each phase is independently observable and fail closed. Completion of one phase does not
grant permission to claim another.

## Phase 1 — Preflight

Preflight records bounded non-secret deployment information:

- source backend, schema version, profile identity and locator digest;
- target backend, version, extension and inactive locator identity;
- required optional dependencies;
- source integrity and snapshot capability;
- output or target non-existence;
- migration bundle schema version;
- expected datasets;
- unsupported features or lossy mappings.

For the implemented PostgreSQL target, preflight requires supported PostgreSQL, pgvector and
Psycopg versions, TLS by default, a writable primary, an explicit migration role, a fresh
allowlisted schema and operator-installed pgvector.

It rejects active or existing targets, malformed profiles, unsupported versions, missing
capabilities, unsafe TLS configuration and transformations that cannot preserve required
state.

## Phase 2 — Deterministic read-only logical export

The implemented SQLite exporter:

- opens the source read-only;
- uses a stable snapshot;
- serializes records in deterministic order;
- uses canonical JSON/JSONL;
- preserves identifiers and typed payloads;
- records per-dataset counts, byte sizes and SHA-256 digests;
- binds the source profile identity without credentials;
- publishes completion last;
- leaves the active source and profile unchanged;
- removes handled incomplete output after failure;
- enforces bounded streaming/resource limits.

A database-file backup is not automatically a backend-neutral migration export.

## Approved logical datasets

The current physical-L3 bundle covers:

| Dataset | Required logical content | Deterministic ordering |
|---|---|---|
| `nodes` | `fact_id` plus canonical node payload | `fact_id` |
| `vectors` | `fact_id` plus finite numeric vector | `fact_id` |
| `edges` | source, relation, target and canonical properties | source, relation, target, properties |
| `entities` | entity id, kind and label | entity id |
| `mentions` | fact id, entity id and relation | fact id, entity id, relation |
| `meta` | metadata keys and values, including embedder metadata when present | key |

This is bounded physical-L3 portability, not a complete whole-system migration. L1 facts,
restrictions, review/import sessions, audit checkpoints, receipts, outbox state, encryption
metadata, configuration and other operational domains require explicit inclusion before any
whole-system cutover claim.

## Phase 3 — Completed bundle publication

A valid bundle contains:

- a versioned manifest;
- exactly the declared logical data files;
- canonical deterministic records;
- source identity and non-secret schema metadata;
- per-file counts, bytes and SHA-256;
- a completion marker written last.

Incomplete directories, undeclared files, symlinks, malformed records, count mismatches,
ordering violations and hash mismatches fail closed.

## Phase 4 — Independent bundle verification

Verification operates without opening or mutating the source deployment and validates:

- completion marker and manifest schema;
- manifest and file hashes;
- exact allowed file set;
- sizes, counts and canonical encoding;
- deterministic ordering;
- identifier and payload shape;
- finite vector elements and consistent dimensions;
- source profile identity and declared backend;
- cross-record references.

This proves bundle integrity and contract conformance. It does not prove claim truth, target
compatibility, successful import or safe cutover.

## Phase 5 — Inactive PostgreSQL target import

Implemented scope:

```text
verified completed bundle
→ PostgreSQL 16 / pgvector 0.8.2 / Psycopg 3.3.x preflight
→ fresh velantrim_inactive_* schema
→ one SERIALIZABLE transaction
→ canonical dataset import
→ target control state VERIFIED / active=false
→ non-secret receipts
```

The importer:

- requires a new allowlisted inactive schema;
- re-verifies the bundle before commit;
- rolls back handled pre-commit failures;
- does not overwrite or activate the source profile;
- does not register PostgreSQL in ordinary runtime composition;
- never serializes credential-bearing DSNs into artifacts;
- converts database errors to bounded stage and SQLSTATE information.

Successful import is **not activation** and cannot serve public reads or writes.

## Phase 6 — Exact state equivalence

The implemented verifier runs a read-only PostgreSQL transaction and independently re-hashes
target rows in the same canonical dataset order as the source bundle.

Exact equivalence requires matching:

- record count;
- canonical JSONL byte count;
- SHA-256;
- vector dimension;
- bundle manifest identity;
- non-secret target identity;
- target `state=VERIFIED`;
- target `active=false`.

The verifier does not update target evidence. A single mismatch fails the operation.

Exact equivalence proves the approved physical-L3 datasets match the verified bundle. It does
not prove retrieval quality, whole-system continuity, production readiness or permission to
cut over.

## Phase 7 — Retrieval-quality evaluation

Not implemented.

Future acceptance must separately measure:

- exact nearest-neighbour baseline;
- recall@k and filtered recall;
- ranking drift for a versioned corpus;
- latency, memory and index size;
- build/rebuild duration;
- stale or unavailable index behavior.

No HNSW or IVFFlat index is created by the inactive-import phase. Approximate retrieval
cannot waive an exact-state mismatch.

## Phase 8 — Explicit cutover and fencing

Not implemented.

A future cutover requires separately reviewed contracts for:

- verified export, import, exact-equivalence and retrieval receipts;
- explicit operator confirmation;
- source/target read and write fencing;
- target health and backup evidence;
- atomic or fail-closed profile activation;
- immutable cutover receipt binding both identities;
- crash-window and concurrency behavior.

Automatic backend switching after data exists is forbidden.

## Phase 9 — Rollback

Not implemented.

A future rollback design must define:

- rollback window and expiry;
- write freeze/fencing;
- post-cutover target changes;
- source revalidation;
- rollback receipt and audit continuity;
- conditions where rollback is no longer safe.

Rollback must never silently overwrite newer state.

## Security and privacy

- Credentials, tokens, passwords, private keys and credential-bearing DSNs must never enter
  profiles, bundles, receipts, logs, issues or Notion.
- Bundle and receipt paths use fail-closed no-clobber handling.
- Sensitive payloads remain sensitive; migration does not create a public artifact.
- TLS is required by default for PostgreSQL; an insecure local-test flag is test-only.
- Backup and migration create additional copies. Active-store erasure does not erase them
  automatically.
- Encryption and transport protection are deployment controls, not proof of claim truth.

## Current boundary summary

```text
SQLite backup / verify / inactive restore                         [implemented]
bounded logical export / independent verification                 [implemented]
inactive PostgreSQL import / exact approved-dataset equivalence    [implemented]
active PostgreSQL runtime                                         [absent]
ANN acceptance                                                     [absent]
cutover / fencing / rollback / dual-write                         [absent]
```

## Related documents

- [Full architecture](../ARCHITECTURE.md)
- [Storage and authority boundaries](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Durable storage profile](./DURABLE_STORAGE_PROFILE.md)
- [SQLite logical export](./SQLITE_LOGICAL_EXPORT.md)
- [Inactive PostgreSQL import](./POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector profile RFC](./POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
