<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Current verified runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

Documentation and localization work merged after the runtime checkpoint improves public
contracts and access. It does not create a new runtime capability or grant-funded delta.

## ✅ Delivered runtime baseline

Crystal includes the trust/evidence/query/storage lifecycle baseline plus:

- source-linked claims, evidence spans, document records and import/review sessions;
- Guardian structural/safety checks and TruthGate epistemic admission;
- read-only public query pipeline with TRACE and receipts;
- durable SQLite ordinary active local-first profile;
- deterministic bounded-streaming SQLite logical export and verification;
- optional lazy PostgreSQL driver path;
- PostgreSQL 16 / pgvector 0.8.2 preflight;
- serializable import into a new inactive schema;
- independent exact-state equivalence and non-secret receipts;
- 2078 tests, 9756 statements, 100% coverage and 9/9 permanent CI;
- 1/1 real PostgreSQL/pgvector integration job.

## ✅ Delivered documentation baseline

- English remains the working, source and conflict-resolving language.
- Root README plus D1 entry/use, D2 reviewer/safety and D3 architecture/storage-authority
  surfaces are current in all nine supported locales.
- D4 source contracts cover project, grant, governance, contributing and glossary terminology
  before localized D4 reconciliation.
- Merged localization is existing baseline and cannot be budgeted again as future delivery.

## ✅ Completed storage phases — issues #331 and #332

PR #335 completed bounded logical migration. PR #337 completed the first PostgreSQL phase:

```text
verified bundle
→ PostgreSQL preflight
→ inactive target import
→ independent exact-state equivalence
→ receipts
→ active=false
```

The target cannot serve normal reads/writes and is not registered in ordinary runtime
composition. No activation, cutover, rollback, dual-write or automatic switching was added.

## P1 — Exact-vs-ANN retrieval evaluation

- exact pgvector search as the reference;
- versioned HNSW/IVFFlat evaluation corpus;
- recall@k, filtered recall, latency, index size and rebuild evidence;
- stale-index and missing-index degraded behaviour;
- ANN indexes remain rebuildable, non-authoritative projections.

## P1 — Explicit cutover and rollback proof

- source/target fencing;
- immutable cutover receipt;
- crash-window and partial-failure tests;
- explicit rollback receipt and expiry policy;
- no reachability-based backend selection.

## P1 — PostgreSQL server lifecycle and security

- least-privilege migration/read/runtime roles;
- TLS certificate and credential rotation;
- backup/restore/upgrade drills and retention;
- pooling, timeout/retry, observability and cleanup policy;
- no certification or distributed exactly-once overclaim.

## P2 — Release and independent audit evidence

- reproducible wheel, sdist and container artifacts;
- checksums, SBOM and supported-version manifest;
- pinned or reviewed supply-chain actions;
- clean-machine reproduction and public audit findings;
- stronger claim/status lint tied to releases.

## P2/P3 — Source-linked Reader Core prototype

Current baseline already has source spans, document records and import sessions. A dedicated
Reader Core remains not implemented.

Future bounded research/engineering may add:

- structure maps and safe segmentation;
- exact source-linked candidate cards;
- coverage, exception and contradiction reports;
- multi-pass rereading and document-level synthesis;
- outputs that remain upstream of Guardian and TruthGate.

It must not become a second Canon owner or conflate importance with truth.

## Grant boundary

The baseline/funded-delta rule is:

```text
verified existing baseline + new measurable funded delta
= independently verifiable public deliverable
```

Issues #331/#332, PRs #335/#337 and D1–D4 documentation work merged before an agreement are
existing baseline. They cannot be counted again as future paid delivery.

No grant award or approved budget is claimed. Active PostgreSQL runtime selection, automatic
switching, production multi-tenancy, universal truth, zero hallucinations and legal/security/
GDPR certification remain out of scope.

## Related documents

- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./docs/grants/funding-use-plan.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
