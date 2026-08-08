<!-- d2-source-contract: CURRENT -->
<!-- d2-source-scope: reviewer-security-privacy-failure -->
# Safety, Privacy and Failure Boundaries

**Status date:** 2026-08-08  
**Audience:** users, reviewers and operators who need one stable safety-oriented overview.  
**Detailed sources:** [`SECURITY.md`](../SECURITY.md), [`PRIVACY.md`](../PRIVACY.md),
[`GDPR.md`](../GDPR.md), [`FAILURE_MODES.md`](./FAILURE_MODES.md) and the
[threat model](./security/threat-model.md).

This document is a translation-oriented summary. It does not replace executable tests,
security review, legal analysis or the detailed English contracts.

## 1. Authority and epistemic safety

```text
physical L3 storage != strict Canon
retrieval score      != evidence
model output         != verified world fact
migration bundle     != claim evidence
successful import    != backend activation
```

Guardian and TruthGate remain the admission boundaries. Public query surfaces are read-only;
explicit ingest is a separate write path. Curator override is explicit, attributed and
audited rather than a silent change to TruthGate policy.

Crystal does not guarantee truth or zero hallucinations. Its measurable goal is that
unsupported material is blocked, labelled, refused or auditable instead of being silently
promoted.

## 2. Default local trust boundary

The default installation has no mandatory cloud, LLM, telemetry or analytics dependency.
The ordinary documented active profile is SQLite. A durable `auto` selection may choose
optional LadybugDB when installed, otherwise SQLite, and then locks the selected backend and
non-secret locator in a durable profile. Ephemeral Mock is explicit development/test state,
not an automatic durable fallback.

PostgreSQL/pgvector is not a normal runtime backend. It is an optional operator-only inactive
import/equivalence target with `active=false`.

## 3. Data that can be stored

Depending on enabled components, local state can include:

- claims, metadata, source/provenance and epistemic state;
- graph nodes and edges in physical L3;
- review, restriction, erasure and audit records;
- receipts and cited fact identifiers;
- outbox/retry state;
- migration profiles, bundles, verification receipts and temporary files;
- backups and operator-created exports.

A local-first design does not make personal data harmless. Operators must classify stored
content, protect filesystem paths, control access and account for every copy.

## 4. Optional boundary expansion

Data can leave the device or local process only through explicit operator choices, including:

- Anthropic/Claude generation, which sends selected context to an external API;
- remote Neo4j or another explicitly configured server backend;
- Wikidata/network adapters;
- Redis or other networked queue configuration;
- PostgreSQL migration/import against a configured server;
- wider HTTP API binding or a reverse proxy;
- user-created backups, bundles or exports copied elsewhere.

A sentence-transformers model may download weights on first use, but inference is local.
Optional adapters have their own dependency, credential, retention and provider risks.

## 5. Encryption and secret limits

`VELANTRIM_ENCRYPTION_KEY` can protect selected L1 personal-data fields at rest. With the
optional `cryptography` package, Fernet is used; otherwise the project provides a
standard-library authenticated fallback. This control is off by default and does not cover
every physical L3 backend, backup, export, receipt, log or temporary file. Host disk
encryption and operational key management remain necessary where sensitivity requires them.

Passwords, tokens and credential-bearing connection strings must never enter storage
profiles, migration bundles, receipts, application logs, public issues or Notion.

## 6. HTTP and container safety

The optional API requires authenticated use and binds to loopback in the documented default.
The Docker stack is designed to fail closed without an API token and run as a non-root user.

Before any wider exposure, require:

- TLS and independently reviewed authentication;
- least-privilege filesystem and database permissions;
- secret rotation and protected configuration;
- rate/resource limits, monitoring and incident handling;
- tested backup, restore and deletion procedures.

The repository does not claim production IdP integration, complete multi-tenancy or security
certification.

## 7. Privacy operations and limits

Crystal provides mechanisms for access/export, rectification/supersession, processing
restriction, erasure and a record of processing. These are engineering controls, not legal
certification.

Erasure from the active local store does not automatically erase:

- backups or exported bundles;
- operator-copied databases;
- remote systems or third-party providers;
- already emitted logs or receipts where retention policy requires separate handling.

Operators need an inventory and deletion policy for those copies.

## 8. Failure-mode matrix

| Failure class | Expected safe behaviour | Current boundary |
|---|---|---|
| Unsupported claim | block, label or bounded refusal | Guardian/TruthGate and strict grounding |
| Read-only query mutation | reject/no state change | public query contract and tests |
| Storage profile conflict | fail before backend cache | durable profile checksum/locator lock |
| Optional dependency absent | explicit bounded error | no silent durable Mock fallback |
| Migration/import failure | transaction rollback, inactive target | `active=false`, no cutover |
| Evidence mismatch | verification failure | independent hash/count/byte checks |
| Receipt/audit tampering | verification failure | digest/hash-chain replay |
| Oversized migration input | fail closed at limits | bounded record/dataset/aggregate limits |
| Network exposure | operator-controlled and authenticated | loopback default, TLS required externally |
| Personal-data copy survives | separate inventory/deletion required | active-store erasure is not global erasure |
| Optimizer/research concept weakens safety | no runtime authority | research/RFC material is non-normative |

## 9. Explicit non-claims

Crystal is research-grade open infrastructure. It is not:

- a security, legal or GDPR certification;
- proof of production readiness or arbitrary scale;
- an active PostgreSQL runtime or automatic migration system;
- a guarantee of perfect truth, zero model error or zero hallucinations;
- AGI, consciousness or a biological-brain implementation;
- evidence of an awarded NLnet grant.

## 10. Reporting

Do not publish secrets, private data or exploitable details in public issues. Report a
security problem through the repository security-reporting channel and include the affected
commit, component, reproduction, impact and proposed mitigation without exposing sensitive
material.
