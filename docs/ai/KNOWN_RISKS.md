# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-15  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Repository HEAD / exact CI / active milestone:** `RESOLVE_LIVE_GITHUB`  
**Current bounded milestone selected by this register:** none

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted architecture contracts remain authoritative. Historical checkpoints below are evidence, not current-HEAD declarations.

Historical Reader compatibility anchor retained for executable preregistration contracts: RC-9 signed merge `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`, post-merge CI `31594027040`, and RC-10 preregistration/completion bookkeeping issue `#377`. These markers do not authorize a current workstream; `comparison pass != runtime authorization`.

## ✅ Closed audit finding — migration final recheck is content-bound

The 2026-08-15 audit identified that the logical migration verifier's final unchanged-file check depended on `(device, inode, size, mtime, ctime)`. On filesystems with coarse observable timestamp precision, a same-size rewrite could make that final recheck weaker than the intended fail-closed contract even though the earlier dataset read had already validated SHA-256.

The bounded remediation reuses the existing SHA-256 primitive: the initial safe read now retains a content digest in the verification snapshot and the final recheck performs a bounded safe reread, comparing both file identity and digest. This is integrity hardening only:

- migration bundle schema is unchanged;
- resource ceilings remain bounded;
- migration bundles remain operational evidence, not claim evidence;
- PostgreSQL/pgvector remains inactive;
- no Canon, Guardian or TruthGate authority changes.

## ✅ Closed audit finding — direct ingest uses the existing outbox after L3 failure

Direct `core.ingest.ingest()` and the main query pipeline share the same cross-store limitation: L1/SQLite and physical L3 do not have one transaction. The audit found that direct ingest could commit the ESM transition to `Validated` and then lose the L3 merge without adding a repair record.

The bounded remediation reuses the already-existing outbox. A post-gate direct-ingest L3 merge failure now:

- returns `accepted=false`;
- records a block outcome;
- enqueues the fact for the existing secondary-sync recovery path;
- does not create a second admission or bypass Guardian/TruthGate;
- can be healed by the existing `drain_l3_outbox()` path.

This is recovery parity, not a new recovery subsystem or epistemic authority mechanism.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- target remains `active=false` and absent from normal runtime composition;
- no cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior exists;
- endpoint/package/profile changes must never silently select another store;
- no Reader decision, later Reader evaluation, EPIS-001 architecture work, security hardening or audit remediation activates PostgreSQL/pgvector.

## P1 — Server lifecycle and operational security remain incomplete

- PostgreSQL backup/restore drill, retention and upgrade sequencing remain separate future work;
- production pooling, timeout/retry policy, least-privilege roles and distributed fencing remain future work;
- integration `trust` authentication is test-only;
- production credentials must not enter profiles, bundles, receipts, logs, issues or Notion.

## P1 — Current migration evidence remains bounded

SQLite export/verifier and PostgreSQL import evidence is bounded. It is not an institution-scale throughput proof, production SLO or arbitrary-payload guarantee. Digest-aware final rechecking strengthens integrity but does not prove immutability after verification returns or provide a transactional cutover.

## P1 — Production identity, tenancy and distributed coordination remain external

- curator leases are process-local;
- no bundled production IdP;
- no complete multi-tenant isolation proof;
- network policy, credential rotation and distributed fencing remain deployment responsibilities;
- no distributed exactly-once guarantee.

## P1 — Supply-chain hardening is bounded, not certified

Issue #214 is **COMPLETED / CLOSED**. Its verification-chain work remains historical evidence:

- committed GitHub Action `uses:` references are pinned to reviewed immutable commit SHAs;
- Bandit and pip-audit verification-tool versions are exact in `.github/requirements-security.txt`;
- weekly Dependabot proposals provide an explicit reviewable update path;
- `docs/security/FIXTURE_DATA_MANIFEST.json` conservatively classifies the reviewed data surface;
- the manifest refuses a repository-wide PII-clean claim and records no confirmed secret/PII incident in the bounded reviewed scope.

This does **not** establish supply-chain, security, privacy or GDPR certification. A green dependency/secret scan is evidence for that run only.

## P1 — Reader remains bounded, not autonomous

RC-1 through RC-7 are merged bounded runtime/domain layers. RC-8 through the later comparator, NLI and RRTIC milestones are bounded research/evaluation/architecture work. EPIS-001 is a frozen architecture-only evidence-state contract. `dedicated_reader_core=false` remains the larger capability truth.

Remaining Reader limits include:

- no automatic parser/chunker/OCR/PDF-layout/multimodal engine;
- no automatic model/provider proposition extraction or summarization;
- no persistent Reader corpus index;
- no semantic/hybrid/vector Reader runtime;
- no automatic entity resolution or claim identity;
- no public Reader API/CLI/background worker;
- no automatic evidence admission, contradiction resolution or planner/belief authority;
- no EPIS-001 runtime implementation or authorization.

## P1 — Similarity can create false identity pressure

The core retrieval risk remains epistemic category collapse:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

High lexical/vector similarity can hide decisive differences in negation, modality, quantifiers, temporal scope, jurisdiction, attribution, units, entity identity or conditions. Conversely, useful paraphrases can have low lexical overlap.

RC-9 directly measured this risk: at K=5 all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives surface, including same-topic/entity collisions and boilerplate overlap. The cross-lingual `rc8-004` pair is missed.

Mitigation remains fail-closed: Reader retrieval returns inspection candidates only; identity/evidence/adjudication fields remain absent.

## P1 — Lexical recall is incomplete

The frozen RC-9 baseline reaches Recall@5 `0.937500` over 16 useful paired cases and MRR `0.895833`. It misses the cross-lingual paraphrase completely. Useful paired hits are 15/16.

This produces `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. Later frozen comparator/NLI evidence does not authorize semantic/vector runtime work; RRTIC-v1 remains an architecture inspection contract rather than a runtime backend decision.

## P1 — Hard-negative pressure is explicit

RC-9 paired hard-negative rate@5 is `1.000000`: all 4/4 known paired hard negatives are surfaced. This is not hidden by the grant presentation. Later comparator/NLI evaluations remain frozen evidence and do not themselves authorize a Reader runtime mechanism.

## P1 — Existing retrieval machinery is not automatically Reader-safe

Crystal already contains admitted-memory retrieval in `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py` and admitted vector/graph composition in `core/pipeline.py`.

Closed #317 / merged PR #321 already implemented a bounded legacy lexical fallback for admitted-memory stores. Reimplementing or wiring that stack directly under a Reader name would create duplicate semantics and authority confusion.

The later Reader research line preserves the same authority separation:

- admitted-memory retrieval must not be wired directly into PRE-ADMISSION Reader;
- embedding comparators are evaluation signals only unless a separate runtime milestone authorizes otherwise;
- automatic backend/model selection is forbidden for qualifying frozen comparisons;
- pure ordering utilities may not promote candidates into evidence or Canon authority.

## P1 — Semantic/vector retrieval remains unauthorized for Reader

Neural embeddings may improve paraphrase/cross-lingual recall, but introduce model/package footprint, version drift, privacy/network questions, hard negatives, ranking instability and index lifecycle complexity.

Frozen comparator/NLI results and RRTIC-v1 do not authorize ANN/vector storage, semantic Reader runtime, PostgreSQL/pgvector activation, automatic identity/adjudication or evidence admission. Passing an evaluation gate would mean only eligibility for stronger evaluation and architecture review, not runtime authorization.

## P1 — SQLite FTS needs capability handling if later selected

SQLite FTS/BM25 scaling is documented, but no current Reader FTS5 virtual-table / `MATCH` implementation exists. A future scaling backend must feature-detect rather than assume FTS5 and must preserve a bounded deterministic fallback.

## P1 — Benchmark misuse could overstate capability

`eval/reader_rc8_retrieval_adversarial.jsonl` is a small synthetic paired contract corpus designed to expose failure classes, not certify production retrieval quality.

RC-9 metrics remain Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, paired hard-negative rate@5 `1.000000`. These are retrieval metrics, not “94% accuracy”, semantic precision, claim-identity accuracy, truth accuracy, contradiction accuracy or evidence-admission correctness. Later v2/comparator/NLI surfaces are likewise bounded research evidence rather than production certification.

## P1 — In-memory O(corpus) RC-9 baseline is not a scale claim

RC-9 intentionally uses a bounded in-memory O(corpus) scorer. Its frozen benchmark is a baseline measurement, not a production-scale indexing or latency/SLO claim.

## P1 — Exact-vs-ANN / semantic runtime remains unselected

The repository has historical exact/vector retrieval mechanisms in admitted-memory paths and frozen semantic comparator evidence in the Reader research line. None of that is a qualifying Reader ANN/vector runtime authorization.

## P1 — Public/grant claim drift requires executable protection

Public/grant surfaces must route volatile repository lifecycle state back to live GitHub rather than treating historical SHAs, closed issues or old localization counts as current truth. Historical compatibility literals may remain only when they are explicitly labeled as historical/non-current.

## P2 — Operational backend identity remains environment-sensitive in developer `auto` modes

Two existing developer-friendly `auto` selections remain operational boundaries rather than Canon-authority defects:

- `VELANTRIM_QUEUE_BACKEND=auto` can resolve to Redis when the package/server is available and SQLite otherwise;
- `VELANTRIM_EMBEDDER=auto` can fall back from sentence-transformers to the hashing embedder, while a persistent-store mismatch is warning-only unless `VELANTRIM_EMBEDDER_STRICT` is enabled.

For persistent/service deployments, operators should pin the intended queue/embedder configuration and treat the resolved state as deployment identity. This audit remediation does not change the global defaults or claim distributed exactly-once behavior.

## P2 — Localization parity is separate from English source reconciliation

All nine supported localized Reader-dependent packs were current at the starting checkpoint. The 2026-08-15 audit remediation intentionally edits English authoritative/current-truth surfaces only. Localized documentation is not modified here; any parity work caused by later English source movement is a separate explicit documentation task.

## Open backlog isolation

- **#165 — OPEN**: exact normalized ingest dedupe/migration, not near-duplicate or semantic matching.
- **#155 — CLOSED/completed**: EPIS-001 architecture contract only; EPIS runtime remains `NOT IMPLEMENTED / NOT AUTHORIZED`.
- **#214 — CLOSED/completed**: bounded fixture/data and supply-chain verification reproducibility history.

Among these three residual scopes, only #165 is open. It is not auto-started by this register or by the audit remediation. Always resolve live GitHub because newer bounded issues/PRs may exist.

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles/receipts are operational evidence, not claim evidence;
- retrieval quality cannot override evidence/trust policy;
- local-first/offline does not itself prove security or GDPR compliance;
- immutable workflow pins improve reproducibility but do not prove supply-chain security;
- no universal truth, zero hallucinations, AGI, consciousness or production certification is claimed;
- NLnet remains `submitted / under review / not awarded`; approximate €50,000 planning only.

## Next actions

1. Resolve live GitHub and Notion before selecting a new bounded milestone; this static register does not select one.
2. Do **not** automatically implement #165, EPIS-001 runtime, Reader semantic/hybrid/vector runtime, FTS, ANN/vector DB, model/provider wiring or storage/backend activation.
3. Keep queue/embedder production-like configuration explicit rather than treating environment-dependent `auto` resolution as durable deployment identity.
4. Treat future action/tool/dependency updates as reviewable proposals, never automatic trust promotion.
