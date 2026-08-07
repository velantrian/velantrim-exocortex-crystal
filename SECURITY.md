# Security Policy

Velantrim Crystal is local-first verifiable memory infrastructure for AI systems. It may
store sensitive claims, provenance and evidence metadata. Treat deployments as
security-sensitive data systems.

## Supported security baseline

The current verified baseline is `main@c612c1f7de067b05ed7d01ad82d47a7bc39af23a`
(PR #330, CI `31213056560`). Security evidence includes Bandit, dependency audit, secret
scanning, Ruff, Python 3.11/3.12 tests, 100% line coverage, Docker checks and a Ring Zero
mutation gate.

This is research-grade open infrastructure, not a security, legal or GDPR certification.

## Reporting a vulnerability

Do not publish exploitable details, secrets or private user data in a public issue.
Contact the maintainer privately through the repository security-reporting channel. Include:

- affected version/commit;
- component and deployment profile;
- reproduction steps or proof of concept;
- expected and observed impact;
- suggested mitigation when known.

## Authority model

Crystal separates storage from epistemic authority:

```text
physical L3 storage != strict Canon
retrieval score      != evidence
migration bundle     != claim evidence
successful import    != activation
```

TruthGate owns epistemic admission policy. Guardian owns structural/safety checks. Storage,
retrieval, migration, topic metadata and model output must not bypass either boundary.

## Authentication and authorization

The repository now includes scoped curator roles/capabilities and authenticated actor
binding on implemented mutation surfaces. This is a baseline authorization layer, not a
complete production identity system.

Current limitations:

- no bundled production IdP;
- no complete tenant-isolation model;
- curator leases are process-local, not distributed fencing;
- deployment TLS, token issuance, rotation and revocation remain operator responsibilities;
- reverse-proxy/network policy remains external to the pure-stdlib core.

## Storage security

### SQLite local-first profile

Crystal locks the durable backend and non-secret locator across restarts. SQLite lifecycle
operations provide backup, independent verification, inactive restore and explicit guarded
lock recovery.

The logical-export runtime additionally provides deterministic canonical JSONL export and
independent verification under fixed local-first resource limits.

Limits:

```text
control JSON          <= 1 MiB
source SQLite         <= 64 MiB
record                <= 1 MiB
records per dataset  <= 200,000
dataset               <= 64 MiB
aggregate JSONL       <= 384 MiB
```

These limits reduce unbounded resource-exhaustion exposure but do not establish streaming
or institution-scale migration security. Issue #331 tracks that work.

### Encryption boundary

L1 encryption is optional and profile-dependent. Physical L3 SQLite/Ladybug data and
logical export bundles are not automatically encrypted by Crystal. Operators handling
sensitive data should use reviewed full-disk/filesystem encryption, protected backup
storage and access controls.

The standard-library crypto fallback is a compatibility path, not an independently audited
cryptographic product. Sensitive institutional deployments should require a reviewed
third-party cryptography implementation and external security assessment.

### PostgreSQL/pgvector

PostgreSQL/pgvector is proposed, not current runtime. A future institutional profile must
define and test:

- TLS certificate verification;
- least-privilege runtime/read/migration roles;
- credential provider, rotation and revocation;
- schema/extension ownership;
- transaction isolation and retryable SQLSTATE policy;
- connection timeout/pooling behavior;
- backup encryption, restore drills and upgrade sequencing;
- audit-log redaction and tenant assumptions.

Credentials and credential-bearing DSNs must never be stored in durable profiles, migration
bundles, receipts, logs, issues or Notion.

## Migration security

A backend transition is a governed migration:

```text
read-only export
→ independent verification
→ inactive target import
→ exact state equivalence
→ retrieval evaluation
→ explicit cutover
→ optional rollback
```

Backend reachability, installed packages, profile editing or successful SQL inserts must
never trigger automatic switching.

## Data handling

- Do not commit real user data, tokens, credentials or private evidence corpora.
- Prefer synthetic fixtures in tests and benchmarks.
- Restriction and erasure state must propagate to trusted read paths and migrations.
- Logs and receipts should contain identifiers/reason codes rather than unnecessary content.
- Notion synchronization must not copy secrets or private datasets into public GitHub docs.

## Dependency and supply-chain boundary

The default runtime remains pure standard library. Optional dependencies must be isolated
behind extras, lazy-loaded and version-bounded.

Remaining work includes immutable GitHub Action pins, reviewed dependency constraints,
checksums/SBOM for releases and scheduled update policy. An all-green dependency audit does
not replace supply-chain hardening.

## Deployment checklist

Before exposing Crystal beyond localhost:

- place it behind TLS and authenticated access control;
- use least-privilege service accounts;
- protect database, profile, backup and export paths;
- establish encrypted backup retention and restore drills;
- configure secret rotation/revocation;
- monitor disk, memory, failures and stale locks;
- review resource limits against the deployment profile;
- do not claim production multi-tenancy or certification without independent evidence.

## Non-claims

Crystal does not claim zero vulnerabilities, zero hallucinations, universal truth,
production certification, automatic GDPR compliance, institution-scale PostgreSQL runtime,
distributed exactly-once behavior or safe automatic backend switching.
