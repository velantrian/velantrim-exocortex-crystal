# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-12  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Current Reader milestone:** RC-6 bounded long-context strategy under issue #369 / PR #370

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted architecture contracts remain authoritative.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- The target remains `active=false`, is absent from normal runtime composition and cannot serve ordinary reads or writes.
- No cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior exists.
- Import success, endpoint reachability, package availability and profile edits must never cause backend selection.
- Exact equivalence covers the approved logical bundle datasets; future state domains require explicit migration-contract updates.

## P1 — Server lifecycle and operational security remain incomplete

- PostgreSQL backup, restore drill, retention and upgrade sequencing are not implemented;
- production pooling, timeout/retry policy, least-privilege role provisioning and distributed fencing remain future work;
- the integration workflow's passwordless localhost `trust` service is test-only and must not be copied into externally reachable deployment;
- production credentials and credential-bearing connection strings must not enter profiles, bundles, receipts, logs, issues or Notion.

## P1 — Current migration evidence remains bounded

SQLite export/verifier resource limits remain explicit local-first bounds. PostgreSQL import uses fixed batches, but current evidence does not establish institution-scale throughput, a production SLO or arbitrary payload support.

## P1 — Production identity, tenancy and distributed coordination remain external

- curator leases are process-local;
- there is no bundled production IdP;
- there is no complete multi-tenant isolation proof;
- network policy, credential rotation and distributed fencing remain deployment responsibilities;
- no distributed exactly-once behavior is claimed.

## P1 — Supply-chain hardening is incomplete

- default runtime remains pure standard library;
- Psycopg is an explicit optional extra with a narrow supported version range;
- immutable action pinning, reviewed constraints, checksums, SBOM and scheduled update policy remain future work;
- a green dependency audit does not establish full supply-chain assurance.

## P1 — Reader has bounded runtime layers but is not a full autonomous reader

The older statement that Reader Core is merely research is stale. RC-1 through RC-5 are merged bounded runtime/domain layers and RC-6 is the current separately authorized bounded milestone. `dedicated_reader_core=false` remains the larger capability truth.

RC-6 specifically reduces long-source context pressure by deterministic rolling working sets over registered RC-4 candidates and direct provenance, not by claiming infinite context or automatic comprehension.

Risks that remain explicit:

- candidate-count/source-locator budgets are artifact budgets, not model-token guarantees;
- a `SUMMARY` artifact can omit or distort meaning if the caller supplies poor text, so it must remain non-authoritative and directly traceable to RC-4 leaf provenance;
- working-set partitioning can separate a relation across sets; RC-6 therefore carries an RC-5 relation only when both sides are in the same set and never infers a substitute cross-set relation;
- no cross-document identity/reasoning exists in RC-6; that boundary belongs to a separately authorized RC-7;
- no Reader output may bypass Guardian/TruthGate, evidence admission, explicit contradiction disposition or strict Canon policy.

```text
working-set coverage != comprehension proof
summary != evidence
summary != verified fact
similarity != identity
```

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles and receipts are operational evidence, not claim evidence;
- retrieval or ANN quality cannot override exact-state mismatch;
- GDPR-oriented controls are engineering controls, not legal compliance or certification;
- no universal truth, zero hallucinations, AGI, consciousness or production certification is claimed;
- NLnet remains submitted / under review / not awarded; no grant award or budget change is claimed.

## Next actions

1. Complete RC-6 exact-head CI, review gate, guarded merge, exact post-merge CI and GitHub↔Notion synchronization.
2. Do **not** start RC-7 without a separate bounded authorization.
3. Keep exact-vs-ANN retrieval evaluation, cutover/fencing, rollback and PostgreSQL server lifecycle as separate workstreams.
4. Preserve GitHub/Notion synchronization and exact-head CI for every material boundary change.
