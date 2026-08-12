# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-12  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-8 merge / RC-9 audited start:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**Current bounded milestone:** RC-9 implementation under issue #375

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted architecture contracts remain authoritative.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- target remains `active=false` and absent from normal runtime composition;
- no cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior exists;
- endpoint/package/profile changes must never silently select a backend;
- no Reader decision or RC-9 implementation activates PostgreSQL/pgvector.

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

RC-9 adds no mandatory third-party dependency.

## P1 — Reader is bounded, not autonomous

RC-1 through RC-7 are merged bounded runtime/domain layers. RC-8 is a completed architecture/research decision. RC-9 adds only bounded PRE-ADMISSION lexical candidate discovery. `dedicated_reader_core=false` remains the larger capability truth.

Remaining Reader limits include:

- no automatic parser/chunker/OCR/PDF-layout/multimodal engine;
- no automatic model/provider proposition extraction or summarization;
- no persistent Reader corpus index;
- no semantic/hybrid/vector Reader retrieval;
- no automatic entity resolution or claim identity;
- no public Reader API/CLI/background worker;
- no automatic evidence admission, contradiction resolution or planner/belief authority.

## P1 — Similarity can create false identity pressure

The most important retrieval risk remains epistemic category collapse:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

High lexical/vector similarity can hide decisive differences in negation, modality, quantifiers, temporal scope, jurisdiction, attribution, units, entity identity or conditions. Conversely, useful paraphrases can have low lexical overlap.

RC-9 directly measures this risk: at K=5 all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives are surfaced, including same-topic/entity collisions and boilerplate overlap. Several scope-changing cases also rank highly because lexical overlap is large.

Mitigation: RC-9 returns inspection candidates only, preserves material lexical tokens, exposes matched terms and contains no identity/truth/corroboration/adjudication fields.

## P1 — Lexical recall is incomplete

The frozen RC-9 baseline reaches Recall@5 `0.937500` over 16 useful paired cases and MRR `0.895833`. It misses the cross-lingual paraphrase completely. The low-overlap paraphrase reaches rank 3 only through weak shared lexical material.

This produces the measured classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. It does not authorize semantic/vector work. Any later comparison remains a separate milestone with thresholds pre-registered before comparison results are known.

## P1 — Existing retrieval machinery is not automatically Reader-safe

Crystal already contains admitted-memory retrieval in `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py` and `core/rrf.py`.

Risk: reusing these modules without a new boundary contract could accidentally blur admitted-L3 query retrieval with PRE-ADMISSION Reader candidate discovery.

Mitigation in RC-9: the lexical baseline is a separate Reader module and does not call existing admitted-memory retrieval machinery.

## P1 — Semantic/vector retrieval is still not authorized for Reader

Neural embeddings may improve paraphrase/cross-lingual recall, but introduce:

- model/package footprint and optional downloads;
- model/version drift and vector-space mismatch lifecycle;
- privacy/network policy questions;
- non-obvious hard negatives;
- threshold/ranking instability;
- vector index rebuild/migration requirements;
- temptation to treat similarity as identity.

ANN/vector backends additionally add approximation and index-lifecycle complexity.

RC-9 measured a lexical gap but did not run a semantic comparison and did not authorize embeddings, hybrid retrieval, ANN/vector DB or PostgreSQL/pgvector Reader retrieval.

## P1 — SQLite FTS needs capability handling if later selected

SQLite FTS remains attractive for local-first persistent lexical discovery, but FTS capabilities can vary by SQLite build. A future Reader scaling backend must feature-detect rather than assume FTS5 availability and must provide a bounded deterministic fallback. RC-9 remains in-memory and does not implement FTS.

## P1 — Benchmark misuse could overstate capability

`eval/reader_rc8_retrieval_adversarial.jsonl` is a small synthetic 20-case contract corpus. It is designed to expose failure classes, not certify production retrieval quality.

The corpus judges only each case's left/right pair. RC-9 Recall@K/MRR track the known useful mate; Precision@K treats other returned corpus entries as synthetic decoys; paired hard-negative rate tracks the known `SAME_TOPIC` / `MERELY_SIMILAR` mate. These metrics are retrieval evidence, not adjudication accuracy.

## P1 — In-memory O(corpus) RC-9 baseline is not a scale claim

RC-9 intentionally uses a bounded in-memory O(corpus) scorer with `MAX_READER_LEXICAL_RECORDS = 100000` and `MAX_READER_LEXICAL_TOP_K = 1000`. The frozen benchmark has 20 index records and 20 queries (at most 400 record comparisons). This is a baseline measurement, not a production-scale indexing claim.

## P2 — Localization debt remains explicit

Russian Reader-dependent RC-7 surfaces are current to immutable RC-7 English checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, totaling 64 documents. RC-9 adds English implementation/status source only; broad translation stays separate.

## Open backlog isolation

- **#165**: exact normalized ingest dedupe/migration, not near-duplicate or semantic matching. Do not turn it into Reader identity.
- **#155**: Epistemic Router/Evidence State RFC downstream of FactsPack. Do not merge with PRE-ADMISSION discovery.
- **#214**: fixture/PII/supply-chain hygiene. Any future model dependency would require explicit treatment there or in a dedicated security scope.

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles/receipts are operational evidence, not claim evidence;
- retrieval or ANN quality cannot override exact-state mismatch;
- GDPR-oriented controls are engineering controls, not legal compliance/certification;
- no universal truth, zero hallucinations, AGI, consciousness or production certification is claimed;
- NLnet remains `submitted / under review / not awarded`; approximate €50,000 planning only.

## Next actions

1. Complete only RC-9 issue #375: code/tests/docs → exact-head CI → review → guarded merge → signed/verified main → post-merge CI → Notion sync/read-back → completion evidence → close → final live audit → STOP.
2. Do **not** automatically start RC-10, semantic/hybrid retrieval, embeddings, FTS, ANN/vector DB, localization refresh, #155, #165 or #214 after RC-9.
3. Keep #155, #165, #214 and PostgreSQL/cutover/ANN workstreams separate unless a future audit proves a dependency.
4. Preserve exact-head evidence and GitHub↔Notion synchronization for every material boundary change.