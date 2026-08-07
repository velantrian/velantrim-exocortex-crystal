# PostgreSQL + pgvector Institutional Profile RFC

**Status:** PROPOSED / NOT RUNTIME
**Issue:** #327
**Dependency status:** no PostgreSQL driver or pgvector dependency is included
**Default profile:** SQLite remains the verified local-first baseline

## Intent

A future PostgreSQL/pgvector profile may support institutional, multi-process deployments
that need a managed server, stronger operational tooling and indexed vector retrieval.

This RFC is not an implementation claim and does not authorize automatic migration from
SQLite.

## Non-goals

The RFC does not claim:

- current PostgreSQL or pgvector runtime support;
- automatic SQLite-to-PostgreSQL selection or switching;
- a dedicated VectorDB dependency;
- production multi-tenancy or a bundled identity provider;
- distributed exactly-once delivery;
- live dual-write cutover;
- security, legal or GDPR certification;
- funded grant delivery.

## Packaging

The default Crystal runtime remains pure standard library.

A future implementation must place the PostgreSQL driver behind an explicit optional extra,
load it lazily and fail clearly when the profile is selected without the dependency. The
implementation must declare supported driver, PostgreSQL and pgvector version ranges and a
reviewed upgrade policy.

## Profile identity and secrets

A durable profile may contain only non-secret identity and configuration, such as:

- backend name;
- host/service identity;
- port;
- database name;
- schema name;
- TLS mode/policy identifier;
- non-secret role identifier;
- pgvector extension/version expectation;
- locator digest.

Passwords, access tokens, private keys and credential-bearing DSNs must remain in an
external secret provider or deployment environment and must never be serialized into
profiles, migration bundles, receipts, logs or Notion.

## Server lifecycle and security boundary

A production-oriented profile requires a separately reviewed deployment contract covering:

- TLS verification and certificate rotation;
- least-privilege roles for read, migration and runtime writes;
- schema ownership and extension-install privileges;
- network exposure and firewall policy;
- credential issuance, rotation and revocation;
- connection pooling and timeout policy;
- audit logging and sensitive-field redaction;
- tenant isolation assumptions;
- backup encryption and retention.

Crystal must not claim that a database connection itself provides tenant or identity
security.

## Transaction and concurrency model

A future adapter must define:

- transaction isolation for reads and writes;
- retryable SQLSTATE classes;
- idempotency keys and conflict behavior;
- schema-migration locking;
- advisory-lock or fencing semantics, if any;
- outbox/projection transaction boundaries;
- connection-loss and partial-commit recovery;
- multi-process tests.

The existing process-local curator lease must not be described as distributed coordination.

## Logical schema mapping

The implementation must publish a reviewed mapping for:

- fact payload and stable identifiers;
- vectors and dimension constraints;
- edges, entities and mentions;
- metadata and embedder fingerprint;
- restrictions/erasure and evidence/provenance state when full-system migration is added;
- audit and projection queues.

Database normalization is allowed only when deterministic export can reconstruct the same
logical state. An ORM or SQL schema is not the authority contract by itself.

## pgvector retrieval

pgvector may provide:

- exact nearest-neighbour search as the reference baseline;
- optional HNSW;
- optional IVFFlat.

Approximate indexes are rebuildable derived projections. They cannot establish evidence,
truth, ESM state or strict Canon membership.

Before enabling an approximate index, compare it with exact search using a versioned
evaluation corpus:

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

Low latency cannot compensate for low recall or state mismatch.

## Backup, restore and upgrades

The server profile requires its own verified lifecycle. SQLite backup/restore receipts
cannot be relabelled as PostgreSQL proof.

A future server lifecycle must cover:

- consistent logical/physical backup strategy;
- independent restore drill;
- point-in-time recovery policy when enabled;
- pgvector extension backup/restore behavior;
- schema and extension upgrade sequencing;
- rollback compatibility;
- backup age and restore observability;
- disaster-recovery ownership.

## Migration and activation

PostgreSQL availability must never trigger automatic backend selection after a durable
profile exists.

Migration must follow the Cross-Backend Storage Migration Contract:

```text
read-only export
→ independent verification
→ inactive import
→ exact state equivalence
→ retrieval evaluation
→ explicit cutover
```

The source remains authoritative until an explicit cutover receipt exists.

## Acceptance gates before runtime implementation

1. Backend-neutral bundle schema is implemented and verified for SQLite export.
2. PostgreSQL logical schema mapping is reviewed.
3. Optional dependency and version policy is accepted.
4. Security/credential boundary is documented and tested.
5. Exact-state fixtures exist.
6. Exact-vs-ANN evaluation corpus and thresholds are accepted.
7. Backup/restore/upgrade lifecycle is designed.
8. Cutover and rollback proof is defined.
9. Full nine-job CI and Notion synchronization pass.

Until then the profile remains `PROPOSED / NOT RUNTIME`.
