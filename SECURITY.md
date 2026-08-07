# Security Policy

## Supported security baseline

The current verified baseline is `main@f03e24c85922d0bb46d6d9dfee98338972135908` (PR #335, CI `31224184351`). Evidence includes Python 3.11/3.12 tests, 100% coverage, Ruff, Bandit, dependency audit, secret scanning, Docker, evaluation, JSONL integrity, docs-status and Ring Zero mutation checks.

This is research-grade open infrastructure, **not a security, legal or GDPR certification**.

## Reporting

Do not publish secrets, private data or exploitable details in a public issue. Use the repository security-reporting channel and include the affected commit, component, reproduction, impact and suggested mitigation.

## Authority model

```text
physical L3 storage != strict Canon
migration bundle     != claim evidence
successful verify    != backend activation
benchmark result     != production SLO
```

TruthGate and Guardian remain the authority boundaries. Storage, retrieval, migration, topic metadata and model output cannot bypass them.

## Storage and migration security

PR #335 implements issue #331 with fixed cursor batches, incremental write/hash/count, private disk-backed canonical edge sorting, same-descriptor hash-first verification, disk-backed referential checks, bounded diagnostics, disk preflight and cleanup on handled temporary-index initialization failure.

The active envelope remains:

```text
control/record <= 1 MiB
source/dataset <= 64 MiB
records per dataset <= 200,000
aggregate JSONL <= 384 MiB
```

Benchmark `31224005804` is bounded local-first evidence, not a production SLO or arbitrary-scale proof. Operators must still protect database, profile, bundle and temporary paths, monitor disk/memory and use encrypted storage where sensitive data requires it.

## PostgreSQL/pgvector

PostgreSQL/pgvector is proposed, not current runtime. Issue #332 must define optional dependencies, supported versions, TLS, least-privilege roles, credential rotation, transaction/retry policy, schema ownership, audit redaction, backup/restore/upgrade and inactive-import cleanup. Credentials must never enter profiles, bundles, receipts, logs or Notion.

No automatic switching is permitted. Live dual-write, activation on import success, production multi-tenancy and distributed exactly-once behavior are not implemented.

## Supply chain and deployment

The default runtime remains pure standard library. Optional dependencies require isolated extras and version bounds. Remaining work includes immutable action pins, reviewed constraints, checksums/SBOM and scheduled maintenance.

Before network exposure, require TLS, authenticated access, least privilege, protected storage, restore drills, secret rotation, resource monitoring and independent review.
