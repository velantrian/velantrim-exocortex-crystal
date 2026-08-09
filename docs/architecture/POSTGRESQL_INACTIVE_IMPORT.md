<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# PostgreSQL/pgvector Inactive Import and Exact Equivalence

**Status:** IMPLEMENTED / TESTED / MERGED BASELINE  
**Issue / PR:** #332 / PR #337  
**Runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Profile:** optional institutional migration target  
**Target state:** `active=false`  
**Tested stack:** PostgreSQL 16 · pgvector 0.8.2 · Psycopg 3.3.x

## Purpose

This phase imports a completed, independently verified SQLite logical bundle into a new,
inactive PostgreSQL schema and proves exact logical equivalence.

It does **not** add a normal PostgreSQL runtime adapter or choose PostgreSQL for public reads
or writes.

```text
verified completed bundle
→ server / version / TLS / role / schema preflight
→ transactional import into velantrim_inactive_*
→ independent target canonical re-hash
→ exact dataset equivalence
→ non-secret receipts
→ active=false
```

## Packaging

The default installation remains pure standard library. PostgreSQL support is explicit:

```bash
pip install 'velantrim-exocortex-crystal[postgresql]'
```

The driver is lazy-loaded only when an explicit PostgreSQL migration command is selected.
Missing or unsupported dependencies fail closed.

Supported first-phase policy:

- Psycopg 3.3.x;
- PostgreSQL major version 16;
- pgvector exactly 0.8.2.

A version-policy change requires separate compatibility evidence.

## Operator commands

```bash
export VELANTRIM_POSTGRES_DSN='postgresql://...'

velantrim-storage import-postgresql-inactive BUNDLE \
  --receipts RECEIPTS \
  --target-schema velantrim_inactive_review_20260809

velantrim-storage verify-postgresql-inactive BUNDLE \
  --target-schema velantrim_inactive_review_20260809
```

The CLI accepts the **name** of the configured DSN environment variable through its explicit
operator contract; credentials are never written into Crystal artifacts.

## Secret boundary

Credentials and credential-bearing DSNs must never be written to:

- storage profiles;
- migration bundles;
- target evidence;
- receipts;
- application logs;
- GitHub issues or pull requests;
- Notion.

Database exceptions are reduced to bounded stage and SQLSTATE information. Raw driver
messages are not exposed as public operation evidence.

Non-secret endpoint identity is bound through a digest of host, port, database and role
metadata. This digest is operation identity, not authentication or authorization.

## Preflight

The implemented preflight requires:

- Psycopg 3.3.x;
- PostgreSQL 16;
- pgvector 0.8.2 already installed by the operator;
- TLS by default;
- an explicit migration role with required database privileges;
- a writable primary, not a recovery/read-only target;
- a fresh schema matching `velantrim_inactive_[a-z0-9_]+`;
- a verified completed source bundle.

Crystal does not silently install extensions, create databases, change roles or fall back to
a different server. Plaintext is available only through an explicit local-test flag and is
not deployment guidance.

## Inactive target contract

The target schema contains:

- `import_control` with `active=false` enforced by SQL constraints;
- nodes with canonical payload text and JSONB consistency checks;
- vectors with canonical JSON text and pgvector equality checks;
- edges, entities, mentions and metadata;
- per-dataset expected and observed count/byte/SHA-256 evidence.

The schema name is not written into Crystal's durable active storage profile. Ordinary
runtime composition does not know how to select it. Import success cannot serve public reads
or writes and cannot alter Guardian, TruthGate, ESM or strict Canon membership.

## Transaction and failure behavior

Schema creation, rows, target evidence and the `VERIFIED` control transition occur in one
SERIALIZABLE PostgreSQL transaction.

Handled pre-commit failures roll back the entire target schema. The source bundle is
re-verified before commit so the imported source identity cannot change unnoticed.

Receipts use a new no-clobber directory:

```text
preflight.json
import.json
equivalence.json
complete.json   # written last
```

A failure receipt cannot look like successful completion. A commit or post-commit publication
uncertainty requires independent `verify-postgresql-inactive`; it never activates the target.

## Exact equivalence

The verifier runs a read-only PostgreSQL transaction and re-hashes canonical target rows in
the same order as the source bundle.

Exact equivalence requires matching:

- record count;
- canonical JSONL byte count;
- SHA-256;
- vector dimension;
- bundle manifest identity;
- non-secret target identity;
- `state=VERIFIED`;
- `active=false`.

The verifier does not update `dataset_evidence` or any target row.

## Logical schema coverage

The current mapping covers the approved portable physical-L3 datasets:

- fact identifiers and canonical node payloads;
- vectors and vector dimension;
- edges;
- entities and mentions;
- metadata, including carried embedder metadata.

Each target row retains canonical material used for independent evidence. pgvector storage
does not replace canonical vector evidence.

This is not a complete whole-system migration of every L1 operational domain, restriction,
erasure marker, audit chain, outbox item, receipt, encryption setting or configuration.
Those domains require explicit schema inclusion before any whole-system cutover claim.

## Explicit non-scope

```text
successful import        != activation
exact state equivalence  != ANN quality
migration receipt        != claim evidence
PostgreSQL availability  != backend selection
physical target state    != strict Canon admission
```

This phase excludes:

- active PostgreSQL runtime reads or writes;
- runtime cutover or profile activation;
- rollback to SQLite;
- live dual-write or zero-downtime migration;
- automatic SQLite/PostgreSQL switching;
- HNSW/IVFFlat indexes or accepted ANN thresholds;
- production pooling, role provisioning or distributed fencing;
- production IdP/multi-tenancy;
- PostgreSQL backup/restore/upgrade lifecycle;
- legal, GDPR or security certification.

## Verification evidence

Permanent CI covers:

- optional dependency and lazy-load behavior;
- secret redaction;
- TLS, version, role and schema preflight;
- deterministic batching;
- transaction rollback;
- failure receipts;
- read-only target verification;
- exact mismatch behavior.

A separate integration workflow runs against PostgreSQL 16 with pgvector 0.8.2, performs a
real import and independent re-verification, confirms `active=false` and confirms no ANN
index is created.

## Remaining gates before active runtime

1. Exact-vs-ANN retrieval evaluation with accepted thresholds.
2. Source/target fencing and immutable cutover receipt.
3. Rollback proof, expiry policy and crash-window tests.
4. PostgreSQL backup/restore/upgrade lifecycle.
5. Production role, secret, certificate, pooling and retry policy.
6. Multi-process concurrency and observability evidence.
7. Separate exact-head CI, review and GitHub/Notion synchronization for every phase.

Until those gates are independently implemented, PostgreSQL/pgvector remains an inactive
migration target and **not an active Crystal runtime backend**.

## Related documents

- [Full architecture](../ARCHITECTURE.md)
- [Storage and authority boundaries](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Cross-backend migration contract](./CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [PostgreSQL/pgvector profile RFC](./POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
