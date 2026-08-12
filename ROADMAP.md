<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372  
**RC-7 exact-head CI:** `31572324596` — 9/9 successful  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge / RC-9 audited start:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` — PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376  
**RC-9 exact validated head:** `1956cbd45e5a5b794852354ed2233bf1fb6e318f`  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**Current bounded milestone:** RC-10 retrieval reuse compatibility + comparison pre-registration, issue #377  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader baseline through RC-7

RC-0 is the normative contract. RC-1 through RC-7 are merged bounded layers:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
```

### ✅ RC-1 — Minimal Evidence-Linked Reading Skeleton
Exact source/version identity, replayable locators, Reader sessions, fidelity, coverage, bookmarks/open loops and fail-visible stale/privacy semantics.

### ✅ RC-2 — Structural Document Map
Caller-supplied version-bound hierarchy/order with explicit `RECOVERED`, `AMBIGUOUS`, `UNSUPPORTED`; no parser/OCR/layout authority.

### ✅ RC-3 — Explicit Multi-Pass Reading Mechanics
`ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD`; explicit targets/outcomes/state and count-only telemetry.

### ✅ RC-4 — Source-Linked Proposition Extraction
Completed substantive RC-3 context may register source-linked `EXTRACTED_PROPOSITION` candidates with attribution/category/negation/qualifiers and exact provenance.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### ✅ RC-5 — Exceptions / Contradiction Candidate Detection

`core/reader_relations.py` registers explicit PRE-ADMISSION `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` over valid RC-4 candidates inside one OPEN ReaderSession / exact SourceVersion. It preserves exact two-sided provenance and rationale and has no resolution/admission authority.

```text
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

### ✅ RC-6 — Bounded Long-Context Strategy

Issue #369 / PR #370 completed. `core/reader_long_context.py` builds bounded working sets over current RC-4 leaves and caller-supplied `SUMMARY` artifacts with direct leaf provenance.

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

The historical sequencing phrase remains: **RC-6 long-context strategy → RC-7 cross-document reading**.

### ✅ RC-7 — Bounded Cross-Document Candidate Links

Issue #371 / PR #372 completed. Signed merge `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`; exact validated head `b1cf79594f702194b4dce66ac2ef2546d4154f15`; exact-head CI `31572324596` 9/9; post-merge CI `31572918731` 9/9.

`core/reader_cross_document.py` registers explicit caller-selected current RC-4 candidates from different document identities after revalidating both Reader/source/pass/structure/coverage/provenance chains.

Candidate vocabulary:

```text
SUPPORTS
CONTRADICTS
ELABORATES
REFERENCES
DEFINES
EXAMPLE_OF
PREREQUISITE_FOR
SAME_TOPIC
POSSIBLE_SAME_CLAIM
```

```text
cross-document link       != Canon relation
cross-document support    != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic                != same proposition
possible-same-claim       != claim identity
similarity signal         != identity proof
repetition across sources != corroboration
```

RC-7 adds no automatic corpus discovery, semantic matching, entity resolution, dedupe, embeddings/ANN/vector DB, LLM/provider/parser/OCR, evidence admission, contradiction winner, truth/Canon/ESM mutation, planner authority, Reader persistence/API/CLI/worker or PostgreSQL activation.

## ✅ RC-8 — Post-RC-7 Candidate Discovery & Retrieval Architecture Decision

Historical RC-8 gate label: **Next bounded Reader gate — post-RC-7 retrieval architecture decision**. That gate is completed; RC-9 is also now completed and RC-10 is the current architecture/evaluation milestone.

Issue #373 / PR #374 completed.  
Decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`.  
Adversarial corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

RC-8 is a bounded **architecture/research milestone**, not a runtime retrieval implementation.

### Capability gap

After RC-7, Crystal can represent a cross-document pair when the caller already knows which two propositions to compare. It cannot discover promising pairs efficiently across a large Reader corpus.

The audit also found that Reader needs a formal distinction among:

```text
SAME_PROPOSITION_CANDIDATE
PARAPHRASE_CANDIDATE
RELATED_CLAIM
SAME_TOPIC
POSSIBLE_CONTRADICTION
MERELY_SIMILAR
```

### Architecture decision

Existing admitted-memory retrieval (`core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py`) is a different authority domain from PRE-ADMISSION Reader artifacts. It may inform/reuse implementation later, but cannot be wired directly into Reader identity by assumption.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

RC-8 required the first separately authorized Reader implementation to be **deterministic lexical candidate discovery + benchmark runner**.

Option order for future evidence remained:

```text
deterministic normalized/token baseline
        ↓
SQLite FTS candidate (feature-detected, bounded fallback)
        ↓
measured hybrid comparison if needed
        ↓
measured semantic/vector comparison only if justified
```

Neural embeddings, ANN/vector DB and semantic identity remained **deferred**. PostgreSQL/pgvector remained inactive `active=false` and not a Reader default.

### Evaluation gate

The 20-case synthetic adversarial corpus covers exact variants, paraphrases, low-lexical-overlap/cross-lingual cases, same-topic traps, negation, modality, quantifiers, time/version, attribution, exceptions, homonyms, boilerplate, numerical thresholds, units and jurisdiction/conditions.

RC-8 deliberately did not invent post-hoc semantic/vector thresholds and did not start implementation beyond the frozen decision/corpus.

## ✅ RC-9 — Deterministic Lexical Candidate Discovery Baseline + Benchmark Runner

Issue #375 / PR #376 completed.  
Signed merge: `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`.  
Exact validated head: `1956cbd45e5a5b794852354ed2233bf1fb6e318f`.  
Exact-head CI `31593097846`: 9/9 successful.  
Post-merge push CI `31594027040`: 9/9 successful.  
Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`.  
Runtime: `core/reader_lexical_discovery.py`.  
Benchmark runner: `scripts/bench_reader_rc9_lexical.py`.  
Frozen result: `eval/reader_rc9_lexical_baseline.json`.

RC-9 implements the first measured baseline authorized by RC-8:

```text
RC-4 proposition candidates
        ↓
conservative NFKC/case/whitespace normalization
        ↓
stable lexical tokens
        ↓
deterministic in-memory BM25
        ↓
top-K inspection candidates
        ↓
benchmark / downstream review
```

The baseline is stdlib-only and offline. It adds no storage schema, network call, semantic/vector runtime, PostgreSQL activation, automatic entity/claim identity, contradiction adjudication, evidence admission, Canon mutation or automatic RC-7 relation registration.

Frozen K=5 benchmark:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

Precision@5 uses the fixed `positive paired queries × K` denominator defined by the RC-9 bounded synthetic benchmark; it is not a fully judged corpus-wide semantic precision claim. The baseline misses the cross-lingual paraphrase and surfaces all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives. It therefore records:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

This is a measured retrieval result, **not** automatic authorization for embeddings, semantic/hybrid retrieval, ANN/vector DB or claim adjudication.

## 🚧 RC-10 — Existing Retrieval Reuse Compatibility + Comparison Pre-Registration

Tracking issue: #377.  
Decision/preregistration contract: `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`.  
Machine-readable preregistration: `eval/reader_rc10_retrieval_comparison_preregistration.json`.

The pre-start audit found substantial retrieval machinery already exists in the **admitted-memory** authority domain: deterministic hashing/trigram embedders, optional SentenceTransformer, admitted vector retrieval, graph walk, bounded legacy lexical retrieval (#317 / PR #321), retrieval config and pure stdlib RRF.

RC-10 therefore **does not build another retrieval stack**. It freezes a reuse matrix:

```text
core/rrf.py                         → future isolated comparison reuse candidate
HashingEmbedder / TrigramHashing   → comparator signals only
SentenceTransformerEmbedder        → future optional comparator only
get_embedder("auto")               → forbidden for preregistered comparison
core/pipeline.py                    → not a Reader pipeline
core/query_pipeline.py              → not a Reader pipeline
core/legacy_retrieval.py            → not a Reader backend
SQLite FTS5                         → not implemented for Reader; future scaling option
PostgreSQL/pgvector                 → inactive / not authorized
```

The future comparison gate is frozen before results are observed:

- retain all 15 useful pairs already found by RC-9;
- recover `rc8-004`, yielding 16/16 / Recall@5 1.0;
- MRR >= 0.895833;
- paired hard-negative hits <= 2/4;
- zero authority violations;
- exact backend/model identity, no `auto` mode;
- zero query-time network calls and no external Reader source-text transmission;
- deterministic lexical fallback required for any later runtime proposal.

```text
comparison pass != runtime authorization
```

RC-10 runs no semantic/hybrid comparator and adds no FTS/vector/runtime implementation.

## 🧩 Backlog remains separated

- #165 — exact normalized ingest dedupe/migration; no near-duplicate/semantic matching.
- #155 — downstream Epistemic Router / Evidence State RFC.
- #214 — PII fixture / reproducible supply-chain hardening.

They remain outside RC-10.

## ⏭️ After RC-10 — explicit new authorization still required

If RC-10 completes, a later milestone may execute an isolated comparator against the frozen RC-10 gate. Passing makes a comparator eligible only for a stronger/larger evaluation and architecture review. It does not authorize Reader runtime adoption.

No semantic/hybrid comparison, embeddings, FTS, ANN/vector indexing, PostgreSQL activation, automatic adjudication or broad localization is started automatically.

## ✅ Storage baseline remains unchanged

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL inactive import/equivalence
→ active=false
```

No automatic backend switching is introduced by Reader work.

## 🌍 Localization position

Russian root + Reader-dependent D1/D3/D4/D5 surfaces remain `CURRENT` to the immutable RC-7 English source checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs preserve rich `REFRESH_NEEDED` translations — 64 tracked documents. D2 and Quick Start remain current across all nine locales.

RC-8 through RC-10 add authoritative English architecture/status source material only; broad translation remains a separate milestone. The root English README still presents an older RC-6/RC-7 checkpoint; RC-10 records that as public-documentation debt rather than hiding a broad localized refresh inside this architecture milestone.

## 🎓 Grant boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget/payment commitment. Budget change: none.

Anything merged before an agreement is existing baseline and cannot be counted again as future paid work. Reader RC-0 through RC-10 are existing pre-agreement baseline if merged before an agreement. RC-10 is not an awarded/funded-delivery claim.

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

## Related documents

- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [RC-7 cross-document contract note](./docs/architecture/READER_RC7_CROSS_DOCUMENT.md)
- [RC-8 retrieval decision](./docs/architecture/READER_RC8_RETRIEVAL_DECISION.md)
- [RC-9 lexical baseline](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [RC-10 reuse/preregistration](./docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)