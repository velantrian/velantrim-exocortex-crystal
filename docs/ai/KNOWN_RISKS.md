# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-07
**Verified runtime checkpoint:** `b0df17a06d552ad2543b6d6e5efe8cd99877cfc0`

This register is an orientation layer. It does not replace issues, ADRs, security
operations, tests, current code inspection or legal review.

## Severity model

- **P0:** can invalidate core trust, safety, privacy or durable-state claims.
- **P1:** materially limits production, scale, interoperability or reviewer confidence.
- **P2:** maintainability, governance, documentation or research debt.

A risk closes only with merged implementation and explicit evidence. Permanent regression
targets remain listed even after the originating defect is closed.

## Closed material findings — 2026-08-07

### #315 — curator decision crash consistency

**Closed by:** PR #319, merge `62879cd2095450de57d11fcf97c13f5f9768ad0b`,
CI `31162857843`.

SQLite now commits the authority-bearing decision, state/metadata, tamper-evident audit
proof and durable L3 projection intent together. Projection is idempotent, restartable and
observable. Restricted/erased/immutable participants fail closed and authoritative L1
restriction remains deny-dominant during L3 outages.

**Remaining boundary:** this is transactional-outbox consistency, not cross-database ACID
or distributed exactly-once delivery.

### #316 — authenticated principal binding

**Closed by:** PR #320, merge `1414862786aa0c0d4cf4ad152776dd4e55536bf0`,
CI `31164585628`.

Bundled HTTP and CLI curator writes now derive audit identity from a validated
`CuratorPrincipal`, enforce capabilities and normalized scopes, pin the current report and
use a process-local decision lease. Actor text is only an optional exact-match assertion;
authorization denial has zero canonical mutation.

**Remaining boundary:** no complete production IdP, token lifecycle, tenant isolation,
policy administration or distributed fencing is included.

### #317 — bounded legacy retrieval

**Closed by:** PR #321, merge `1748677a5c84e8a9b3af08fcaed0215efebcdd66`,
CI `31166027193`, benchmark `31165503179`.

Reviewed Mock/SQLite no-fingerprint reads use a deterministic candidate cap; unsupported
adapters return `legacy_store_requires_reindex` without a public full-corpus scan. Explicit
reindex preserves fact/ESM/trust/restriction/edge/audit authority.

**Remaining boundary:** a bounded window may miss a relevant record outside that window;
reindex is the preferred recovery path.

### Environment-selected L3 backend drift

**Closed by:** PR #322, merge `0ca66cc6e194edd06b5de2a6eb5126a30613957e`,
validated head `156e974393586ada30feaac2500eae7003cb2885`, CI `31174042124`.

The first durable environment-selected L3 backend and non-secret locator are now persisted
in a versioned profile. Later `auto` startups resolve to that lock. Malformed profiles,
backend/locator conflicts, constructor mismatches and automatic fallback to ephemeral Mock
fail closed. The pure-stdlib `velantrim-doctor` command reports profile/dependency/locator
health without opening L3 or mutating Canon.

Independent diff inspection found that the first draft stored the profile itself relative
to process `cwd`. The default was corrected before merge to
`~/.velantrim/velantrim-storage-profile.json`, with a regression test across working
directories.

**Remaining boundary:** PR #325 separately implemented SQLite backup/restore and guarded
legacy stale-lock recovery. Cross-backend migration, multi-instance deployment policy and
distributed fencing remain open.

### SQLite storage lifecycle

**Closed by:** PR #325, merge `b0df17a06d552ad2543b6d6e5efe8cd99877cfc0`, validated head `aa822c49c095039de90b92fbe4fe451c7b8f13b7`,
CI `31182471502`.

The locked SQLite profile now supports online backup, independent verification, restore
only to a new inactive database/profile, and guarded stale-lock recovery. Independent
diff review found and closed a new-writer race before final CI.

**Remaining boundary:** this is SQLite deployment continuity, not cross-backend migration,
automatic activation, distributed fencing or epistemic admission.

## P0 — permanent trust-boundary regression targets

### P0.1 TruthGate or Guardian bypass

**Risk:** a new API, adapter, import path, review helper or background process writes
trusted/canonical state without established admission and safety boundaries.

**Required proof for every affected change:** explicit authority owner, adversarial tests,
fail-closed dependency behavior, exact-head CI and mutation evidence for the changed
boundary.

### P0.2 Query-to-write contamination

**Risk:** query, retrieval or read-only surfaces create, promote, reinforce, reindex or
otherwise mutate canonical memory.

**Required proof:** HTTP, CLI and MCP queries remain read-only across normal, degraded,
provider-failure and retry paths. Reindex remains a separate explicit operator action.

### P0.3 Strict Canon leakage

**Risk:** restricted, erased, unverified or contested physical L3 records enter strict
grounding because graph presence, similarity or rank is mistaken for proof.

**Required proof:** deny-dominant immutable reconciliation and consumer-level integration
tests.

### P0.4 Proof/state split regression

**Risk:** a curator mutation commits without durable audit/projection intent, or a failed
operation produces success-looking proof.

**Required proof:** transactional decision journal, idempotent recovery, failure injection,
audit-chain verification and no-resurrection tests remain green.

### P0.5 Principal identity bypass

**Risk:** a new public write path derives audit identity, capability or target scope from
untrusted request/CLI text rather than a validated principal.

**Required proof:** complete write-surface inventory, actor-spoof tests and zero mutation on
configuration, capability, scope, report or lease denial.

### P0.6 Storage-profile authority confusion

**Risk:** a deployment profile, database connection, graph presence or vector index is
misrepresented as epistemic authority or used to bypass normal Canon reconciliation.

**Required proof:** profile selection remains deployment-only; Guardian, TruthGate,
restrictions and `TrustSnapshot` remain the owners of admission and strict reads.

## P1 — current engineering and operational limitations

### P1.1 Cross-backend migration runtime is absent

ADR-021 defines the required phased contract, but no verified cross-backend import,
equivalence, cutover or rollback command exists. The approved first implementation slice
is read-only SQLite logical export plus independent bundle verification.

**Do not claim:** automatic database switching, verified dual-write, lossless cross-backend
migration, PostgreSQL support or rollback.

**Closure proof:** deterministic export/verify first; then separate inactive-target import,
source/target exact-state comparison, retrieval evaluation, explicit cutover, rollback
proof and structured receipts.

### P1.2 Default profile and stale-lock operations need deployment policy

The user-level default profile is appropriate for one default local deployment. Services,
containers and multiple instances should configure `VELANTRIM_STORAGE_PROFILE_PATH`
explicitly. A hard crash can leave the bounded `.lock` file and cause fail-closed startup;
no automatic stale-lock deletion is claimed.

**Closure proof:** documented instance identity, safe lock ownership/age semantics,
operator-assisted recovery and adversarial multi-process tests.

### P1.3 Distributed curator coordination is absent

The included lease registry coordinates one process only.

**Do not claim:** distributed locking, global exactly-once decisions or stale-writer
fencing across processes/hosts.

**Closure proof:** external adapter contract, ownership/expiry/fencing semantics,
multi-process failure tests, recovery metrics and deployment documentation.

### P1.4 Production identity provider and multi-tenancy are incomplete

Principal composition and scoped capabilities exist, but production identity issuance,
rotation/revocation, tenant isolation and policy administration remain host responsibilities.

**Closure proof:** tenant model, authenticated identity mapping, authorization matrix,
isolation tests, revocation/audit behavior and reviewed deployment integration.

### P1.5 Bounded degraded retrieval trades recall for work limits

A deterministic legacy candidate window can miss relevant records outside the window.
The response exposes degraded mode and recommends reindex.

**Do not claim:** bounded compatibility retrieval has vector-equivalent recall or semantic
completeness.

**Closure direction:** complete reindex, or separately review a bounded indexed lexical
strategy with measured recall and migration behavior.

### P1.6 Broader provenance lifecycle wiring

Strong proof exists on central verified paths, but future adapters and less central
lifecycle operations can introduce orphaned state/proof windows.

**Closure proof:** mutation/read surface inventory, common receipt/provenance contract,
replay and recovery tests.

### P1.7 Performance evidence is not a production SLO

The 1k/10k/30k benchmark proves the configured candidate bound on one hosted-runner
environment. It does not establish production p50/p95/p99, concurrency or capacity.

**Closure proof:** versioned workload, controlled environment, thresholds, storage-growth
limits and regression/operations policy.

### P1.8 Mutation testing remains targeted

The checkpoint proves 7/7 declared Ring Zero mutants killed, not repository-wide semantic
mutation coverage.

**Closure proof:** expanded mutation inventory and bounded execution policy.

### P1.9 Reproducible supply-chain pinning remains incomplete

Gitleaks, Bandit and pip-audit pass. However, development dependencies, security tools and
GitHub Actions should be constrained/pinned more tightly for reproducibility and reviewable
updates.

**Closure proof:** versioned constraints/lock strategy, action SHA pinning, scheduled
newest-compatible checks and automated update policy.

### P1.10 Legacy normalized-ID migration gap (#165)

Pre-normalization stores may retain case/whitespace variants that new ingest does not fully
deduplicate.

**Closure proof:** reviewed migration or persistent normalized-claim index, collision
policy, occurrence preservation and backwards-compatibility tests.

### P1.11 Dedicated long-document Reader Core is absent

Crystal has evidence spans and strong admission/proof boundaries, but no verified
multi-pass reader with structural maps, coverage tracking, bookmarks, exception and
contradiction passes or selective re-reading.

**Safe direction:** source-linked candidate cards upstream of Guardian and TruthGate; no
second Canon owner.

## P2 — governance, maintenance and research debt

### P2.1 Research PR accumulation

Research/documentation PRs can become stale against `main`, overlap or be mistaken for
runtime authority.

**Closure proof:** periodic reconciliation, current status headers and explicit
merge/close decisions.

### P2.2 Stale issues and historical status text

Issue bodies and old Notion callouts can describe pre-merge reality after implementation
has moved forward.

**Control:** prefer current issue state, merged PRs, exact-head CI and the newest dated
snapshot. Preserve old records as history, not current truth.

### P2.3 Documentation/context drift

AI context and Notion snapshots can become stale when mutable heads/checks are copied into
multiple places.

**Control:** duplicate immutable facts such as final merge SHA, accepted ADR and completed
CI evidence; keep mutable branch/check status in GitHub and use a clearly dated current
snapshot.

### P2.4 Compliance and grant overclaim

GDPR-oriented features, public grant materials and roadmap pages can be misread as legal
certification, funding award or production approval.

**Control:** preserve explicit submission/award, implementation/research and
mechanism/certification distinctions.

### P2.5 Automated review availability

Codex/Copilot review may be unavailable because of quota, account or integration limits.
This must not be represented as successful independent review.

**Control:** preserve the service limitation in the PR timeline, require exact-head CI,
record manual diff findings and do not fabricate approval evidence.

## Research-only boundaries

The following remain proposed/research unless separately implemented and merged:

- PostgreSQL/pgvector institutional deployment profile;
- dedicated VectorDB integration;
- automatic cross-backend migration or switching;
- Essence Workdesk and dialogue-board experiments;
- cognitive-state, planning and user-intent hypotheses;
- Native Kernel compatibility/event substrate concepts;
- Personal Exo-Cortex, Mentaury and Full Exo-Cortex modules;
- ASR/Small Core active-state recovery;
- artificial-consciousness or digital-person claims.

## Risk evidence template

When closing or materially changing a risk, record:

```text
risk id
exact PR, final head and merge SHA
affected authority boundary
implementation summary
exact CI run and test/coverage evidence
runtime wiring/default state
migration/recovery behavior
remaining limitations
GitHub and Notion synchronization
```

### P2.6 Frozen localization drift

English is the active authority language. Existing localized READMEs may lag until the
dedicated final translation pass.

**Control:** do not cite localized mutable metrics as current evidence; keep English
status/manifest/TEST_REPORT coherent; perform one explicit localization PR after the
engineering baseline is frozen.
