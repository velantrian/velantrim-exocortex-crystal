# EU Service Security Readiness — Crystal API and Curator Surfaces

**Status:** engineering readiness checklist · documentation only  
**Applies to:** funded hardening of the optional FastAPI layer and institutional curator workflow  
**Does not claim:** EUMSS certification, managed-security-service status, legal compliance, production multi-tenancy or completed implementation

## Context

On 24 July 2026 ENISA published the draft candidate European Cybersecurity
Certification Scheme for Managed Security Services (EUMSS) for public review.
Crystal is not a managed security service and this document does not place it inside
that certification scope. The draft is useful as a European operational-trust lens
because its horizontal layer groups security expectations into:

- secure service and platform design;
- deployment and transition management;
- availability and continuity management;
- operational service management;
- continuous improvement and technology maintenance.

Primary references:

- [ENISA announcement](https://www.enisa.europa.eu/news/have-your-say-on-the-certification-of-eu-managed-security-services)
- [Draft candidate EUMSS Scheme v1.1](https://certification.enisa.europa.eu/publications/draft-candidate-eumss-scheme-v11-public-review_en)

## Crystal boundary

```text
Crystal core = local-first verifiable memory infrastructure.
FastAPI = optional operator-controlled service surface.
Review UI = privileged curator surface.
This checklist = measurable hardening guidance, not certification.
```

The current grant-safe target remains a local or institution-controlled deployment.
Production multi-tenant hosting requires a separate architecture, authorization model,
threat model and funding scope.

## 1. Secure service and platform design

### Identity and capabilities

- Deny privileged operations by default.
- Separate at minimum: `reader`, `ingester`, `curator`, `auditor`, `operator`.
- Keep read-only MCP access distinct from HTTP write capabilities.
- Require explicit capability checks at the endpoint and service layers.
- Do not infer authorization from network location alone.
- Never log raw tokens, authorization headers or personal memory content.

### Token lifecycle

- Support bounded token lifetime where tokens are used.
- Provide rotation and immediate revocation.
- Distinguish invalid, expired, revoked and insufficient-capability outcomes without
  leaking sensitive detail.
- Store only safe token fingerprints where audit correlation is required.
- Test token reuse, downgrade, replay and concurrent revocation cases.

### Input and trust boundaries

- Preserve Guardian → TruthGate as the only automatic admission path.
- Normalize and bound request sizes, evidence references, identifiers and paths.
- Reject unsupported URI schemes, control characters and ambiguous encodings.
- Keep file import inside an explicit sandbox root.
- Fail closed when trust metadata is missing or malformed.
- Apply rate and concurrency limits before expensive parsing or retrieval.

### Service defaults

- Bind to loopback by default.
- Require an explicit operator decision for non-loopback exposure.
- Document CORS, proxy, TLS termination and trusted-header assumptions.
- Provide secure defaults rather than a list of optional recommendations.

## 2. Deployment and transition management

- Validate configuration before accepting traffic.
- Record security-relevant configuration changes in a content-light audit event.
- Version database migrations and serialize first-open migration work.
- Document upgrade, rollback and compatibility procedures.
- Provide clean-start, existing-database and interrupted-upgrade tests.
- Keep secrets outside repository content and generated support bundles.
- Publish a minimal deployment diagram showing every trust boundary.

### Acceptance evidence

- reproducible local deployment recipe;
- invalid-configuration tests;
- migration and rollback fixtures;
- secure reverse-proxy example without making it mandatory;
- operator checklist for exposing the service beyond localhost.

## 3. Availability and continuity management

- Expose liveness and readiness separately where their semantics differ.
- Verify backup and restore, not only backup creation.
- Test SQLite/WAL recovery and L3 outbox retry behaviour.
- Define safe degraded modes: read-only, queueing, refusal or shutdown.
- Never turn unavailable provenance into an ungrounded successful answer.
- Preserve audit/provenance integrity checks after restart.
- Document capacity limits and expected behaviour under saturation.

### Acceptance evidence

- restore drill with deterministic verification;
- crash/restart integration tests;
- dependency/backend outage tests;
- queue/outbox replay report;
- documented refusal semantics during partial failure.

## 4. Operational service management

### Auditable events

Record content-light events for:

- authentication failure and token revocation;
- capability or role change;
- privileged ingest attempt;
- curator approve/reject/force-approve decision;
- security-relevant configuration change;
- rate-limit or policy refusal;
- receipt verification failure;
- backup/restore and integrity-check result.

Audit data must not become a second uncontrolled copy of private memory. Prefer IDs,
hashes, categories and timestamps over raw claims or source snippets.

### Incident readiness

- Maintain a security contact and vulnerability-reporting process.
- Produce a redacted diagnostic export suitable for an operator or reviewer.
- Define token compromise, data exposure, integrity failure and availability failure
  response steps.
- Document how to revoke access while preserving forensic evidence.
- Test that restricted or erased facts do not reappear in review, evidence or support
  surfaces.

## 5. Continuous improvement and maintenance

- Keep Ruff, tests, evaluation gate, Gitleaks, Bandit, pip-audit and Docker build
  checks reproducible.
- Pin security tooling deliberately and review updates.
- Track dependency and base-image vulnerabilities.
- Maintain supported Python versions and deprecation policy.
- Publish security-relevant release notes.
- Re-run the threat model when adding a new write surface, backend, parser or
  authentication method.
- Keep a documented process for accepting, mitigating or deferring security findings.

## Capability test matrix

| Action | Reader | Ingester | Curator | Auditor | Operator |
|---|---:|---:|---:|---:|---:|
| Query trusted memory | allow | allow | allow | allow | allow |
| Inspect receipts/evidence | bounded | bounded | allow | allow | allow |
| Submit candidate ingest | deny | allow | allow | deny | allow |
| Approve/reject review item | deny | deny | allow | deny | allow |
| Force approval | deny | deny | separately gated | deny | separately gated |
| Read redacted audit export | deny | deny | bounded | allow | allow |
| Change security configuration | deny | deny | deny | deny | allow |
| Rotate/revoke credentials | deny | deny | deny | deny | allow |

This is a target contract for funded hardening, not a statement that all roles already
exist in the current runtime.

## Grant mapping

```text
M2 / FastAPI hardening
├── capability model
├── token lifecycle
├── secure deployment profile
├── request/rate limits
├── operational audit export
└── failure-safe integration tests

WP2 / institutional review
├── role-based curator permissions
├── multi-curator decision flow
├── explicit force-override authority
├── accessibility and operator guidance
└── review-surface privacy controls
```

## Completion rule

Security hardening is complete only when each retained control has:

1. a documented invariant;
2. an implementation or explicit non-applicability decision;
3. an automated test where technically possible;
4. a reproducible operator check;
5. a reviewer-visible artifact.

A checklist item without evidence is planning, not a delivered security control.
