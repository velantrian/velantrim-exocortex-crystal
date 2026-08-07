# PostgreSQL/pgvector Inactive Import and Exact Equivalence

**Status:** implementation candidate in PR #337; not current `main` until merged  
**Issue:** #332  
**Profile:** optional institutional migration target  
**Tested stack:** PostgreSQL 16 · pgvector 0.8.2 · Psycopg 3.3.x

## Purpose

This phase imports a completed, independently verified SQLite logical bundle into a **new,
inactive PostgreSQL schema** and proves exact logical equivalence. It does not add a normal
PostgreSQL runtime adapter or choose PostgreSQL for public reads/writes.

```text
verified completed bundle
→ server/version/TLS/role/schema preflight
→ transactional import into velantrim_inactive_*
→ independent target canonical re-hash
→ exact dataset equivalence
→ non-secret receipts
```

## Packaging

The default installation remains pure standard library. PostgreSQL support is explicit:

```bash
pip install 'velantrim-exocortex-crystal[postgresql]'
```

The supported first-phase driver range is `psycopg[binary]>=3.3,<3.4`. The driver is
lazy-loaded only when an explicit PostgreSQL migration command is selected.

## Secret boundary

The CLI accepts the **name** of an environment variable, never a DSN value:

```bash
export VELANTRIM_POSTGRES_DSN='postgresql://...'
velantrim-storage import-postgresql-inactive bundle receipts \
  --target-schema velantrim_inactive_review_20260808
```

Credentials and credential-bearing DSNs are never written to profiles, target tables,
receipts, logs, issues or Notion. Database exceptions are converted to stage and SQLSTATE
only; raw driver messages are not exposed.

## Preflight

The first reviewed profile requires:

- Psycopg 3.3.x;
- PostgreSQL major 16;
- pgvector exactly 0.8.2;
- TLS by default;
- an explicit migration role with database `CREATE` privilege;
- a writable primary, not a recovery/read-only target;
- a new schema matching `velantrim_inactive_[a-z0-9_]+`;
- the pgvector extension already installed by the operator.

Crystal does not silently install extensions, create databases, change roles or fall back
to a different server. Plaintext is allowed only through the explicit
`--allow-insecure-local-test` integration-test flag.

## Inactive target contract

The target schema contains:

- `import_control` with `active=false` enforced by a SQL check constraint;
- nodes with canonical payload text plus JSONB consistency checks;
- vectors with canonical JSON text plus pgvector equality checks;
- edges, entities, mentions and metadata;
- per-dataset expected and observed count/byte/SHA-256 evidence.

The schema name is not written into Crystal's durable active storage profile. The normal
runtime constructor does not know how to select it. Import success cannot serve public
reads/writes and cannot alter Guardian, TruthGate, ESM or strict Canon membership.

## Transaction and failure behavior

All schema creation, rows, target evidence and the `VERIFIED` control transition occur in
one serializable PostgreSQL transaction. Handled pre-commit failures roll back the entire
schema. A source bundle is re-verified before commit so the imported source identity cannot
change unnoticed.

Receipts are written into a new no-clobber directory:

```text
preflight.json
import.json
equivalence.json
complete.json   # written last
```

A failure receipt cannot look like successful completion. A failure during commit or
post-commit receipt publication is explicitly operationally uncertain and requires
independent `verify-postgresql-inactive`; it never activates the target.

## Exact equivalence

The verifier runs a read-only PostgreSQL transaction and re-hashes canonical target rows in
the same dataset order as the logical bundle. Exact equivalence requires matching:

- record count;
- canonical JSONL byte count;
- SHA-256;
- vector dimension;
- bundle manifest identity;
- non-secret target identity;
- `state=VERIFIED` and `active=false`.

The read-only verifier does not update `dataset_evidence` or any other target row.

## Explicit non-scope

```text
successful import        != activation
exact state equivalence  != ANN quality
migration receipt        != claim evidence
PostgreSQL availability  != backend selection
```

This phase excludes:

- runtime cutover or profile activation;
- rollback to SQLite;
- live dual-write or zero-downtime migration;
- HNSW/IVFFlat indexes;
- production pooling or distributed fencing;
- production IdP/multi-tenancy;
- automatic switching;
- legal, GDPR or security certification.

## Verification

Permanent unit CI covers lazy dependency handling, secret redaction, TLS/version/role/schema
preflight, batching, rollback, failure receipts, read-only verification and exact mismatch
behavior. A separate integration workflow runs against
`pgvector/pgvector:0.8.2-pg16`, performs a real import and re-verification, confirms
`active=false`, and confirms no ANN index is created.
