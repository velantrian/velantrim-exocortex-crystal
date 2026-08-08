# PostgreSQL + pgvector Institutional Profile RFC

**Status:** PARTIALLY IMPLEMENTED / INACTIVE MIGRATION ONLY / NOT ACTIVE RUNTIME  
**Architecture issue:** #327  
**Implemented phase:** #332 / PR #337 / `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Default profile:** SQLite remains the verified local-first baseline

## Intent

A PostgreSQL/pgvector profile may support future institutional, multi-process deployments
that need a managed server and indexed vector retrieval. The merged implementation covers
only governed import into an inactive target and independent exact-state equivalence.

It does not authorize automatic migration, ordinary PostgreSQL reads/writes or cutover.

## Implemented phase

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 / Psycopg 3.3.x preflight
→ new velantrim_inactive_* schema
→ serializable transactional import
→ independent read-only canonical target re-hash
→ exact record / byte / SHA-256 equivalence
→ non-secret receipts
```

The detailed operator contract is documented in
[POSTGRESQL_INACTIVE_IMPORT.md](./POSTGRESQL_INACTIVE_IMPORT.md).

The target control record is constrained to `active=false`. The schema is not registered in
ordinary runtime composition and cannot serve normal reads or writes.

## Non-goals and remaining boundaries

The implemented phase does not claim:

- active PostgreSQL or pgvector runtime support;
- automatic SQLite-to-PostgreSQL selection or switching;
- exact or approximate retrieval acceptance;
- a dedicated VectorDB dependency;
- production multi-tenancy or a bundled identity provider;
- distributed exactly-once delivery;
- live dual-write, cutover or rollback;
- PostgreSQL backup/restore/upgrade lifecycle;
- security, legal or GDPR certification;
- funded grant delivery or grant award.

## Packaging

The default Crystal runtime remains pure standard library. Psycopg is available only through
the explicit `[postgresql]` extra and is imported lazily by explicit operator commands.
Missing or unsupported dependencies fail closed.

The implemented version policy is:

- Psycopg 3.3.x;
- PostgreSQL major version 16;
- pgvector 0.8.2.

Any version-range change requires separate compatibility evidence and review.

## Profile identity and secrets

The inactive-import phase does not store a PostgreSQL profile. The operator provides only the
name of an environment variable containing connection configuration. Receipts bind to a
non-secret digest derived from endpoint metadata.

Passwords, tokens, private keys and credential-bearing connection strings must remain in an
external secret provider or deployment environment and must never be serialized into
profiles, migration bundles, receipts, application logs, issues or Notion.

A digest of host, port, database and role metadata is operational identity evidence. It is
not authentication, authorization or secret storage.

## Security boundary

The implemented preflight checks supported versions, TLS state, recovery mode, writability,
schema absence and non-secret locator metadata. TLS is required by default. Plaintext is
available only through an explicit local-test flag.

The real integration workflow uses a passwordless localhost PostgreSQL `trust` service only
inside an ephemeral job. It must not be treated as deployment guidance.

Production deployment still requires separately reviewed contracts for:

- certificate validation and rotation;
- least-privilege migration/read/runtime roles;
- network exposure and firewall policy;
- credential issuance, rotation and revocation;
- connection pooling, timeout and retry policy;
- audit logging and sensitive-field redaction;
- tenant isolation assumptions;
- backup encryption, retention and restore drills.

## Transaction and concurrency model

The inactive import uses one SERIALIZABLE transaction and rolls back handled pre-commit
failures. The source bundle is verified again before commit. Independent equivalence runs in
a read-only transaction.

This phase does not establish:

- online zero-downtime migration;
- distributed fencing;
- general retry/idempotency across operator restarts;
- active multi-process runtime semantics;
- outbox/projection transaction boundaries.

The existing process-local curator lease must not be described as distributed coordination.

## Logical schema mapping

The implemented mapping covers the approved portable bundle datasets:

- fact identifiers and canonical payloads;
- vectors and vector dimension;
- edges;
- entities and mentions;
- metadata, including embedder-related metadata carried by the bundle.

Each target row retains canonical JSON used for independent byte-for-byte evidence. pgvector
storage does not replace canonical vector evidence.

Restrictions, erasure, provenance, contradiction dispositions, audit checkpoints or pending
projection work require explicit inclusion in the portable schema whenever they exist as
separate state domains. No full-system cutover claim is allowed until every required domain
is covered and independently equivalent.

## pgvector retrieval

No HNSW or IVFFlat index is created by the inactive-import phase. Exact and approximate
retrieval remain future work.

Before any ANN enablement, compare it with exact search using a versioned evaluation corpus:

```text
exact state equivalence gate
+
exact retrieval baseline
+
recall@k / filtered recall
+
latency / index size / rebuild cost
+
stale-index degraded behavior
```

Approximate indexes remain rebuildable derived projections. They cannot establish evidence,
truth, ESM state or strict Canon membership.

## Backup, restore and upgrades

SQLite lifecycle receipts cannot be relabelled as PostgreSQL proof. A future active server
profile requires its own backup strategy, independent restore drill, retention, extension
upgrade sequencing, rollback compatibility and disaster-recovery ownership.

## Migration and activation

PostgreSQL availability and successful import must never trigger backend selection.

```text
read-only export
→ independent bundle verification
→ inactive import                 [implemented]
→ exact state equivalence         [implemented]
→ retrieval evaluation            [not implemented]
→ explicit cutover and fencing    [not implemented]
→ rollback proof                  [not implemented]
```

The source remains authoritative until a separately reviewed explicit cutover receipt
exists.

## Remaining acceptance gates before active runtime

1. Exact-vs-ANN retrieval evaluation and accepted thresholds.
2. Source/target fencing and immutable cutover receipt.
3. Rollback proof, expiry policy and crash-window tests.
4. PostgreSQL backup/restore/upgrade lifecycle.
5. Production role, secret, certificate, pooling and retry policy.
6. Multi-process concurrency and observability evidence.
7. Exact-head CI, independent review and GitHub/Notion synchronization for each phase.

Until those gates are separately implemented, PostgreSQL/pgvector remains an inactive
migration target and **not an active Crystal runtime backend**.