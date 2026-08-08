# Security Policy

## Supported security baseline

The current verified baseline is `main@bbd816c09dd39a02e6de6c1014438490572f40f6`
(PR #337, CI `31256316536`, PostgreSQL integration `31256316532`). Evidence includes Python
3.11/3.12 tests, 100% coverage, Ruff, Bandit, dependency audit, secret scanning, Docker,
evaluation, JSONL integrity, docs-status, Ring Zero mutation checks and a real inactive
PostgreSQL/pgvector import/equivalence test.

This is research-grade open infrastructure, **not a security, legal or GDPR certification**.

## Reporting

Do not publish secrets, private data or exploitable details in a public issue. Use the
repository security-reporting channel and include the affected commit, component,
reproduction, impact and suggested mitigation.

## Authority model

```text
physical L3 storage != strict Canon
migration bundle     != claim evidence
successful import    != backend activation
exact equivalence    != production readiness
```

TruthGate and Guardian remain the authority boundaries. Storage, retrieval, migration,
topic metadata and model output cannot bypass them.

## PostgreSQL inactive-import security

PR #337 implements issue #332 phase 1 with these controls:

- Psycopg behind an explicit optional extra and lazy import;
- PostgreSQL 16, pgvector 0.8.2 and Psycopg 3.3.x version gates;
- DSN accepted only from a named environment variable, never a CLI value;
- TLS required by default;
- strict allowlisting and quoting for the new `velantrim_inactive_*` schema;
- parameter binding for imported records;
- serializable transaction and rollback on handled pre-commit failure;
- `active=false` target control constraint;
- independent verification in a read-only transaction;
- endpoint identity represented in receipts only by a non-secret digest;
- raw database failures redacted to a bounded stage and optional SQLSTATE.

Production credentials and credential-bearing connection strings must never enter profiles,
bundles, receipts, application logs, issues or Notion.

The integration workflow uses a passwordless localhost service with PostgreSQL `trust`
authentication as **test-only** configuration inside an ephemeral job. That configuration
must not be copied to an externally reachable or persistent deployment.

## Remaining PostgreSQL boundaries

The inactive target is not an active runtime adapter and cannot serve normal reads/writes.
The repository does not yet provide production role provisioning, certificate rotation,
pooling, complete retry policy, distributed fencing, backup/restore/upgrade lifecycle,
production multi-tenancy or cutover/rollback proof.

No automatic switching is permitted. Import success, endpoint reachability or package
availability cannot select a backend.

## SQLite migration and resource security

The bounded local-first export path retains fixed limits, disk-backed ordering/reference
checks, same-descriptor verification and cleanup. Benchmark `31224005804` is bounded
local-first evidence, not a production SLO or arbitrary-scale proof.

Operators must protect database, profile, bundle, receipt and temporary paths, monitor
resources and use encrypted storage where sensitive data requires it.

## Supply chain and deployment

The default runtime remains pure standard library. Optional dependencies require isolated
extras and version bounds. Remaining work includes immutable action pins, reviewed
constraints, checksums/SBOM and scheduled maintenance.

Before network exposure, require TLS, authenticated access, least privilege, protected
storage, restore drills, secret rotation, resource monitoring and independent review.