<!-- d2-source-contract: CURRENT -->
<!-- d2-source-scope: reviewer-security-privacy-failure -->
# Security Policy

## Supported security baseline

The current verified runtime baseline is `main@bbd816c09dd39a02e6de6c1014438490572f40f6`
(PR #337, CI `31256316536`, PostgreSQL integration `31256316532`). Evidence includes Python
3.11/3.12 tests, 100% coverage, Ruff, Bandit, dependency audit, secret scanning, Docker,
evaluation, JSONL integrity, docs-status, Ring Zero mutation checks and a real inactive
PostgreSQL/pgvector import/equivalence test.

This is research-grade open infrastructure, **not a security, legal or GDPR certification**.

A compact reviewer-facing summary is available in
[`docs/SAFETY_PRIVACY_AND_FAILURES.md`](./docs/SAFETY_PRIVACY_AND_FAILURES.md).

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

## Default and optional trust boundaries

The default installation has no mandatory cloud, LLM or external database dependency. The
ordinary documented active profile is SQLite. A durable `auto` selection may choose optional
LadybugDB when installed, otherwise SQLite, and then locks the chosen profile. It must not
silently fall back to ephemeral Mock.

Network/trust-boundary expansion is explicit: remote Neo4j, Anthropic generation, Wikidata,
Redis, wider API exposure or a PostgreSQL migration target require operator configuration.
Each requires independent credential, TLS, retention and access review.

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

## Supply chain and verification reproducibility

The default runtime remains pure standard library. Optional dependencies require isolated
extras and version bounds.

The committed GitHub Actions workflows pin every third-party `uses:` reference to a reviewed
40-character commit SHA while retaining a human-readable release comment. The security job
also installs Bandit and pip-audit from exact versions in
[`.github/requirements-security.txt`](./.github/requirements-security.txt). This makes the
verification implementation materially more reproducible for a recorded repository SHA; it
does **not** make dependency vulnerability databases immutable and does not constitute
supply-chain certification.

Updates are not abandoned: [`.github/dependabot.yml`](./.github/dependabot.yml) requests weekly
reviewable proposals for GitHub Actions and the dedicated `.github` Python security-tool
surface. Update PRs still require ordinary CI/review/merge discipline; there is no auto-merge
or automatic trust promotion.

The bounded committed-data review is recorded in
[`docs/security/FIXTURE_DATA_MANIFEST.json`](./docs/security/FIXTURE_DATA_MANIFEST.json). It
classifies the Reader evaluation datasets/results and historical Sprint 1 dump by provenance
and role. The manifest deliberately does **not** claim that the entire repository is free of
PII, secrets, licensing risk or other sensitive material. A confirmed incident, if one is ever
found, requires artifact-specific response; git-history rewriting is not authorized by this
hardening work.

Remaining broader supply-chain work may include reviewed hashes for additional package
artifacts, an SBOM, and stronger end-to-end dependency locking where justified. A green
Bandit/pip-audit/Gitleaks run is evidence for that run, not a security or legal certification.

Before network exposure, require TLS, authenticated access, least privilege, protected
storage, restore drills, secret rotation, resource monitoring and independent review.
