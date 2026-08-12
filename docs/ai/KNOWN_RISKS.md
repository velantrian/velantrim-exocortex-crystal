# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-12  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 post-merge CI:** `31594027040` — 9/9 successful  
**Current bounded milestone:** RC-10 architecture/evaluation preregistration under issue #377

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted architecture contracts remain authoritative.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- target remains `active=false` and absent from normal runtime composition;
- no cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior exists;
- endpoint/package/profile changes must never silently select a backend;
- no Reader decision, RC-9 implementation or RC-10 contract activates PostgreSQL/pgvector.

## P1 — Server lifecycle and operational security remain incomplete

- PostgreSQL backup, restore drill, retention and upgrade sequencing are not implemented;
- production pooling, timeout/retry policy, least-privilege roles and distributed fencing remain future work;
- integration `trust` authentication is test-only;
- production credentials must not enter profiles, bundles, receipts, logs, issues or Notion.

## P1 — Current migration evidence remains bounded

SQLite export/verifier and PostgreSQL import evidence is bounded. It is not an institution-scale throughput proof, production SLO or arbitrary-payload guarantee.

## P1 — Production identity, tenancy and distributed coordination remain external

- curator leases are process-local;
- no bundled production IdP;
- no complete multi-tenant isolation proof;
- network policy, credential rotation and distributed fencing remain deployment responsibilities;
- no distributed exactly-once guarantee.

## P1 — Supply-chain hardening is incomplete

- default runtime remains pure standard library;
- Psycopg is an optional extra;
- immutable action pinning, reviewed constraints/checksums, SBOM and scheduled update policy remain future work under #214;
- a green dependency audit is not supply-chain certification.

RC-10 adds no mandatory third-party dependency, model download or new runtime package.

## P1 — Reader is bounded, not autonomous

RC-1 through RC-7 are merged bounded runtime/domain layers. RC-8 is a completed architecture/research decision. RC-9 is a completed bounded PRE-ADMISSION lexical candidate-discovery baseline. RC-10 adds only retrieval reuse compatibility plus a pre-registered future comparison gate. `dedicated_reader_core=false` remains the larger capability truth.

Remaining Reader limits include:

- no automatic parser/chunker/OCR/PDF-layout/multimodal engine;
- no automatic model/provider proposition extraction or summarization;
- no persistent Reader corpus index;
- no semantic/hybrid/vector Reader runtime;
- no automatic entity resolution or claim identity;
- no public Reader API/CLI/background worker;
- no automatic evidence admission, contradiction resolution or planner/belief authority.

## P1 — Similarity can create false identity pressure

Historical RC-8 contract label: **Post-RC-7 discovery / identity risk**. RC-9 measured that risk; RC-10 pre-registers a future comparison gate without converting retrieval into authority.

The most important retrieval risk remains epistemic category collapse:

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

RC-9 directly measured this risk: at K=5 all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives are surfaced, including same-topic/entity collisions and boilerplate overlap. Several scope-changing cases also rank highly because lexical overlap is large. Cross-lingual `rc8-004` is missed.

Mitigation remains fail-closed: Reader retrieval returns inspection candidates only; identity/evidence/adjudication fields remain absent. RC-10 requires a future comparator to improve both useful recall and paired hard-negative behavior rather than rewarding recall alone.

## P1 — Lexical recall is incomplete

The frozen RC-9 baseline reaches Recall@5 `0.937500` over 16 useful paired cases and MRR `0.895833`. It misses the cross-lingual paraphrase completely. The low-overlap paraphrase reaches rank 3 only through weak shared lexical material.

This produces `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. It does not authorize semantic/vector work. RC-10 freezes thresholds before future comparison results are known: retain the existing 15 useful hits, recover `rc8-004` to 16/16, keep MRR >=0.895833 and reduce paired hard-negative hits to <=2/4.

## P1 — Existing retrieval machinery is not automatically Reader-safe

Crystal already contains admitted-memory retrieval in:

- `core/embedding.py`;
- `core/legacy_retrieval.py`;
- `core/retrieval_config.py`;
- `core/query_pipeline.py`;
- `core/rrf.py`;
- admitted vector/graph retrieval composition in `core/pipeline.py`.

Closed #317 / merged PR #321 already implemented a bounded legacy lexical fallback for admitted-memory stores. Reimplementing the same stack under a Reader name would create duplicate semantics and authority confusion.

RC-10 therefore makes reuse disposition explicit:

- admitted-memory pipeline/query/legacy retrieval must not be wired directly into PRE-ADMISSION Reader;
- `HashingEmbedder` / `TrigramHashingEmbedder` are comparator signals only;
- existing embedder token/stopword policy is not automatically a Reader-safe semantic representation;
- optional `SentenceTransformerEmbedder` is a future comparator only under separate pinned dependency/model/privacy authorization;
- `get_embedder("auto")` is forbidden for a preregistered Reader comparison because backend identity may change;
- pure `core/rrf.py` may be reused only as ordering with explicit Reader candidate identity and no authority promotion.

## P1 — Semantic/vector retrieval remains unauthorized for Reader

Neural embeddings may improve paraphrase/cross-lingual recall, but introduce:

- model/package footprint and optional downloads;
- model/version drift and vector-space mismatch lifecycle;
- privacy/network policy questions;
- non-obvious hard negatives;
- threshold/ranking instability;
- vector index rebuild/migration requirements;
- temptation to treat similarity as identity.

ANN/vector backends additionally add approximation and index-lifecycle complexity.

RC-10 runs **no semantic/hybrid comparison** and adds no model dependency. Its future gate requires exact backend/model identity, zero query-time network calls, no external Reader source-text transmission and zero authority violations. Passing only means eligibility for stronger evaluation/architecture review.

## P1 — SQLite FTS needs capability handling if later selected

SQLite FTS/BM25 scaling is already documented in `docs/core/DEDUP_AND_SCALE.md` and RC-8. The post-RC-9 repository audit found no current Reader FTS5 virtual-table / `MATCH` implementation.

A future Reader scaling backend must feature-detect rather than assume FTS5 availability and must provide a bounded deterministic fallback. RC-10 does not implement FTS or any index/schema migration.

## P1 — Benchmark misuse could overstate capability

`eval/reader_rc8_retrieval_adversarial.jsonl` is a small synthetic 20-case paired contract corpus. It is designed to expose failure classes, not certify production retrieval quality.

The corpus judges only each case's left/right pair. RC-9 Recall@K/MRR track the known useful mate; Precision@K uses the bounded fixed-K synthetic definition; paired hard-negative rate tracks the known `SAME_TOPIC` / `MERELY_SIMILAR` mate. These metrics are retrieval evidence, not adjudication accuracy or corpus-wide semantic precision.

RC-10 explicitly prevents a passing future comparison from becoming runtime authorization. A stronger/larger evaluation surface remains required before any semantic Reader runtime adoption can be considered.

## P1 — In-memory O(corpus) RC-9 baseline is not a scale claim

RC-9 intentionally uses a bounded in-memory O(corpus) scorer with `MAX_READER_LEXICAL_RECORDS = 100000` and `MAX_READER_LEXICAL_TOP_K = 1000`. The frozen benchmark has 20 index records and 20 queries (at most 400 record comparisons). This is a baseline measurement, not a production-scale indexing claim.

## P1 — Exact-vs-ANN evaluation remains unexecuted

The repository has historical exact/vector retrieval mechanisms in admitted-memory paths, but no qualifying Reader exact-vs-ANN or semantic/hybrid comparison has been executed. RC-10 only freezes comparison requirements. No ANN acceptance, latency/SLO claim or approximate-index correctness claim exists.

## P1 — Public English README drift

The post-RC-9 audit found `README.md` still presenting an older RC-6/RC-7-in-progress checkpoint. That underclaims current implementation rather than granting unsafe authority, but it violates desired public truth synchronization.

RC-10 records the finding; broad root/localized README reconciliation remains a separate documentation milestone because the localization policy requires source-checkpoint/freshness accounting rather than a hidden English-only rewrite.

## P2 — Localization debt remains explicit

Russian Reader-dependent surfaces remain current to immutable RC-7 checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, totaling 64 documents. RC-8 through RC-10 add English architecture/status meaning only; broad translation stays separate.

## Open backlog isolation

- **#165**: exact normalized ingest dedupe/migration, not near-duplicate or semantic matching. Do not turn it into Reader identity.
- **#155**: Epistemic Router/Evidence State RFC downstream of FactsPack. Do not merge with PRE-ADMISSION discovery.
- **#214**: fixture/PII/supply-chain hygiene. Any future model dependency requires explicit security/dependency treatment rather than being smuggled through RC-10.

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles/receipts are operational evidence, not claim evidence;
- retrieval or ANN quality cannot override exact-state/evidence/trust policy;
- GDPR-oriented controls are engineering controls, not legal compliance/certification;
- no universal truth, zero hallucinations, AGI, consciousness or production certification is claimed;
- NLnet remains `submitted / under review / not awarded`; approximate €50,000 planning only.

## Next actions

1. Complete only RC-10 issue #377: architecture/eval contract + truth reconciliation → exact-head CI → review → guarded merge → signed/verified main → post-merge CI → Notion sync/read-back → completion evidence → close → final live audit → STOP.
2. Do **not** automatically execute semantic/hybrid comparison, implement FTS, embeddings, ANN/vector DB, localization refresh, #155, #165 or #214 after RC-10.
3. Keep #155, #165, #214 and PostgreSQL/cutover/ANN workstreams separate unless a future live audit proves a direct dependency.
4. Preserve exact-head evidence and GitHub↔Notion synchronization for every material boundary change.
