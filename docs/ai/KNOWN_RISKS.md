# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated implementation head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current
issues and accepted ADRs remain authoritative. PR #334 is historical grant/status context;
PR #337 is the current runtime checkpoint.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- Issue #332 is implemented for preflight, inactive import and exact equivalence only.
- The target remains `active=false`, is absent from normal runtime composition and cannot
  serve ordinary reads or writes.
- No cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior
  exists.
- Exact equivalence covers the approved logical bundle datasets. Any future state domain
  added to Crystal requires an explicit schema and migration-contract update before a
  full-system cutover claim.
- Import success, endpoint reachability, package availability and profile edits must never
  cause backend selection.

## P1 — Server lifecycle and operational security remain incomplete

- PostgreSQL backup, restore drill, retention and upgrade sequencing are not implemented;
- production pooling, timeout/retry policy, least-privilege role provisioning and distributed
  fencing remain deployment/future-work boundaries;
- the integration workflow uses a passwordless localhost `trust` service only inside an
  ephemeral test job and must not be copied into an externally reachable deployment;
- TLS is required by default, but production certificate, secret-provider and rotation
  operations remain outside the repository;
- production credentials and credential-bearing connection strings must not enter profiles,
  bundles, receipts, application logs, issues or Notion;
- hashed endpoint identity binds receipts operationally but is not authentication or secret
  storage.

## P1 — Current migration evidence remains bounded

The SQLite export/verifier retains explicit local-first limits: 64 MiB source/dataset,
200,000 records per dataset and 384 MiB aggregate JSONL. PostgreSQL import uses fixed
batches, but current evidence does not establish institution-scale throughput, a production
SLO or arbitrary payload support.

## P1 — Production identity, tenancy and distributed coordination remain external

- curator leases are process-local;
- there is no bundled production IdP;
- there is no complete multi-tenant isolation proof;
- network policy, credential rotation and distributed fencing remain deployment
  responsibilities;
- no distributed exactly-once behavior is claimed.

## P1 — Supply-chain hardening is incomplete

- the default runtime remains pure standard library;
- Psycopg is an explicit optional extra with a narrow supported version range;
- immutable action pinning, reviewed constraints, checksums, SBOM and scheduled update
  policy remain future work;
- a green dependency audit does not establish full supply-chain assurance.

## P2 — Reader Core remains research, not runtime

Crystal does not yet implement a dedicated multi-pass Reader Core or Semantic Reading Layer.
Any future implementation must preserve source spans, coverage and contradictions, remain
upstream of Guardian/TruthGate and never become a second Canon owner.

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles and receipts are operational evidence, not claim evidence;
- retrieval or ANN quality cannot override exact-state mismatch;
- GDPR-oriented controls are engineering controls, not legal compliance or certification;
- no universal truth, zero hallucinations, AGI, consciousness or production certification
  is claimed;
- the project is submitted and under review; no grant award or budget change is claimed.

## Next actions

1. Build exact-vs-ANN retrieval evaluation as a separate reviewed phase.
2. Require explicit source/target fencing before any cutover.
3. Add rollback proof and expiry policy separately.
4. Implement PostgreSQL backup/restore/upgrade lifecycle and operational role policy.
5. Preserve GitHub/Notion synchronization and exact-head CI for every material boundary
   change.