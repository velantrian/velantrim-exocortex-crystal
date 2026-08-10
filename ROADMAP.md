<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Current verified runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Completed D1–D5 documentation checkpoint:** `main@f4556e8f9775d28d4a1b2c20a28962a95e55d33e` / PR #352  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

Documentation and localization work merged after the runtime checkpoint improves public
contracts and access. It does not create a new runtime capability or grant-funded delta.
Bounded features merged after that checkpoint must carry their own exact-head and post-merge
CI evidence rather than silently rewriting the historical baseline above.

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
- 2078 tests, 9756 statements, 100% coverage and 9/9 permanent CI at the retained runtime checkpoint;
- 1/1 real PostgreSQL/pgvector integration job.

## ✅ Delivered D1–D5 documentation baseline

- English remains the working, source and conflict-resolving language.
- D1 entry/use, D2 reviewer/safety, D3 architecture/storage-authority, D4 project/grant/
  governance/glossary and D5 extended-reference surfaces are current for all nine supported
  locales: `ar`, `de`, `es`, `fr`, `hi`, `it`, `ja`, `ru`, `zh-CN`.
- D5 source inventory/policy is anchored to signed
  `main@d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9`; the final localized D5 checkpoint is
  `main@f4556e8f9775d28d4a1b2c20a28962a95e55d33e`.
- Final D5 inventory: **136 CURRENT**, **126 ENGLISH_ONLY_BY_DESIGN**, **10 RETIRED**,
  **0 REFRESH_NEEDED**, **272 total** at that checkpoint.
- Localization tracking issue #341 is **closed / completed**.
- Detailed residual technical, security, audit, machine-readable and research contracts remain
  English-only by design where recorded by the D5 policy; no native-speaker editorial,
  security, legal or GDPR certification is implied.
- Merged D1–D5 localization is existing baseline and cannot be budgeted again as future
  delivery.

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

## P2/P3 — Source-linked Reader Core

RC-0 defines the normative architecture contract at
[`docs/architecture/READER_CORE_ARCHITECTURE.md`](./docs/architecture/READER_CORE_ARCHITECTURE.md).
RC-1 adds the **minimal evidence-linked domain skeleton** needed to prove the first contract
invariants. The machine-readable distinction remains deliberately narrow:

```text
reader_core_rc1_skeleton = true
dedicated_reader_core    = false
```

### ✅ RC-1 — Minimal Evidence-Linked Reading Skeleton

The bounded RC-1 implementation provides:

- source/document identity bound to source URI and exact SHA-256 version;
- exact half-open source spans or an explicit replayable structural locator;
- `ReaderSession` lifecycle with explicit interrupted/degraded/stale state;
- `SegmentCard` with mandatory source-fidelity class;
- explicit `UNREAD` / `SEEN` / `PROCESSED` / `REVISITED` / `NEEDS_REVIEW` coverage states;
- count/gap coverage telemetry with no comprehension percentage;
- minimal source-linked bookmarks and open loops;
- conservative whole-session invalidation when source version changes and no remapping is proven;
- source restriction/sensitivity inheritance;
- tests that structurally isolate RC-1 from ingest, TruthGate, Canon/ESM, contradiction decision
  writers and planner authority.

RC-1 deliberately does **not** add a structural parser/semantic chunker, multi-pass orchestration,
LLM/provider integration, embeddings, ANN/vector DB, durable Reader storage schema, public
API/CLI/background worker, cross-document reasoning engine, planner or automatic belief update.
Source body text is not retained by the RC-1 source-version object.

### ⏭️ Later Reader phases

A dedicated Reader Core remains future work. The next separately bounded phase should be chosen
from measured needs after RC-1 rather than pre-committing to a vector stack. Candidate later work
includes structural document mapping and then explicit multi-pass mechanics. Any later phase must
preserve:

- reader artifacts/candidates upstream of normal admission;
- `coverage != comprehension proof`;
- source observation/extraction/interpretation/summary/inference separation;
- contradiction candidates without automatic resolution;
- no second Canon owner or planner/belief-update authority.

## Grant boundary

The baseline/funded-delta rule is:

```text
verified existing baseline + new measurable funded delta
= independently verifiable public deliverable
```

Issues #331/#332, PRs #335/#337 and D1–D4 documentation work merged before an agreement are
existing baseline. D5 documentation work also merged before any agreement and is existing
baseline. The merged Reader Core RC-0 architecture contract is likewise documentation baseline,
not funded Reader runtime implementation. If RC-1 merges before a grant agreement exists, that
minimal skeleton also becomes existing pre-agreement baseline and cannot be counted again as
future paid delivery.

No grant award or approved budget is claimed. Approximate €50,000 remains planning only.
Active PostgreSQL runtime selection, automatic switching, production multi-tenancy, universal
truth, zero hallucinations and legal/security/GDPR certification remain out of scope.

## Related documents

- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./docs/grants/funding-use-plan.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader Core RC-0 architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Extended reference policy](./docs/EXTENDED_REFERENCE_POLICY.md)
