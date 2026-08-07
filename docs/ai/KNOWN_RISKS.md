# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-07  
**Verified runtime checkpoint:** `f03e24c85922d0bb46d6d9dfee98338972135908`  
**Validated implementation head / CI:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736` / `31213056560`

This register is an orientation layer. GitHub `main`, executable tests, completed CI and

## 2026-08-08 — Bounded migration checkpoint

- #331 is implemented by PR #335; fixed cursor batches and disk-backed ordering/reference checks remove complete-dataset/global-ID retention from the production path.
- Existing local-first size limits remain active. Benchmark `31224005804` is not a production SLO or institution-scale certification.
- #332 remains open for optional inactive PostgreSQL/pgvector import and exact-state equivalence; activation and cutover remain absent.
- Resource exhaustion, temporary-disk capacity, interruption cleanup and maximum-envelope testing remain operational concerns for larger deployments.
- GDPR language remains **GDPR-oriented controls**, not legal compliance or certification.
- PR #334 remains historical grant/status baseline context; the current runtime authority is PR #335.

current issue/PR state remain authoritative.

## Severity model

- **P0** — can invalidate trust, safety, privacy or durable-state guarantees.
- **P1** — materially limits reliability, scale, interoperability or reviewer confidence.
- **P2** — maintainability, documentation, governance or research debt.

A risk closes only through merged implementation and exact evidence. Historical fixes stay
listed as regression targets when the invariant remains important.

## ✅ Latest verified storage checkpoint

PR #330 merged as `c612c1f7de067b05ed7d01ad82d47a7bc39af23a` after exact-head CI
`31213056560` completed all nine jobs successfully.

Verified evidence:

- Python 3.11 and 3.12: **2047 passed / 12 skipped / 0 failed**;
- **9219 statements / 100.00% line coverage**;
- **7/7** declared Ring Zero mutants killed;
- security, Ruff, evaluation, JSONL integrity, Docker and docs-status green.

The runtime now has deterministic SQLite logical export and independent bundle verification,
but only inside the explicit bounded local-first envelope recorded below.

## P0 — permanent regression targets

### P0.1 Guardian or TruthGate bypass

No adapter, migration path, query helper, worker or storage backend may establish trusted
state without the existing admission and safety owners.

### P0.2 Physical L3 confused with strict Canon

Physical L3 is multi-status storage. Graph membership, retrieval rank, migration success or
backend choice cannot grant strict Canon membership.

### P0.3 Query-to-write contamination

Ordinary HTTP, CLI and MCP query paths must remain read-only with respect to canonical truth
state, including provider failure, retry and degraded-retrieval paths.

### P0.4 Proof/state split

A failed or rejected durable mutation must not emit success-looking audit or receipt proof.
Authority-bearing state, recovery intent and proof must remain crash-consistent.

### P0.5 Principal identity bypass

Public curator writes must derive identity, capability and scope from a validated principal,
not request text. Process-local leases must never be described as distributed fencing.

### P0.6 Migration authority confusion

```text
migration bundle        != claim evidence
successful verification != TruthGate admission
successful import       != activation
retrieval quality       != exact state equivalence
```

## P1 — active engineering limitations

### P1.1 Institution-scale migration is not implemented — #331

The current export/verifier enforces fixed limits:

```text
control JSON          <= 1 MiB
source SQLite         <= 64 MiB
one record            <= 1 MiB
records per dataset   <= 200,000
one dataset           <= 64 MiB
aggregate JSONL       <= 384 MiB
```

This bounds the current materializing implementation but does not prove bounded peak memory
for arbitrarily large stores. Issue #331 requires cursor batching, incremental hashing and
parsing, disk-backed referential checks, disk-space preflight, cleanup and large-corpus
benchmarks. No institution-scale claim is allowed until that evidence is merged.

### P1.2 PostgreSQL/pgvector runtime is absent — #332

PostgreSQL/pgvector remains a proposed optional institutional profile. Issue #332 covers only
inactive target import and exact-state equivalence after the migration prerequisites are
satisfied. Driver/version policy, TLS and credential boundaries, server backup/restore,
ANN evaluation, cutover, rollback and fencing require explicit evidence.

SQLite remains the verified local-first/lightweight default. Automatic SQLite ↔ PostgreSQL
fallback or profile-edit migration is forbidden.

### P1.3 Distributed curator coordination is absent

The included lease registry coordinates one process only. Multi-process or multi-host claims
require an external fencing adapter, expiry/ownership semantics and failure tests.

### P1.4 Production identity and multi-tenancy are incomplete

Scoped principal composition exists, but production identity issuance, revocation, tenant
isolation and policy administration remain host responsibilities.

### P1.5 Performance evidence is not a production SLO

Current tests and benchmark artifacts do not establish production p50/p95/p99 latency,
concurrency, capacity or institution-scale resource behavior.

### P1.6 Supply-chain reproducibility remains incomplete

Security gates pass, but development constraints and GitHub Actions should be pinned more
tightly and maintained through a reviewed update policy.

### P1.7 Dedicated Reader Core is absent

Crystal has evidence spans and admission/proof boundaries, but no verified multi-pass reader
with structural maps, coverage tracking, bookmarks, exception passes and selective rereads.
Any future reader must produce source-linked candidates upstream of Guardian and TruthGate.

### P1.8 Grant/status synchronization must remain exact — #333 / PR #334

Grant-facing documents must separate the merged baseline from future funded delta. A
documentation PR is not complete merely because runtime tests pass: its exact head must pass
`docs-status`, then merge, and Notion must receive immutable post-merge evidence.

## P2 — governance and maintenance debt

- historical Notion entries may describe superseded branch states;
- localized README snapshots intentionally lag until a dedicated reconciliation pass;
- research/documentation PRs can become stale against `main`;
- targeted mutation testing is not repository-wide semantic mutation coverage;
- automated third-party review can be unavailable and must not be represented as approval.

## Grant and compliance claim boundary

The NLnet application is submitted and under review. No award or budget change is claimed.
Crystal provides GDPR-oriented controls, not legal compliance or certification. It does not
claim universal truth, zero hallucinations, production multi-tenancy, distributed exactly-once
behavior, PostgreSQL runtime, Titan integration or consciousness.

## Closure evidence template

When closing or materially changing a risk, record:

```text
risk / issue
exact base, head and merge SHA
affected authority boundary
implementation and failure behavior
exact CI and test evidence
remaining limitations
GitHub and Notion synchronization
```
