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
**Current bounded milestone:** RC-9 deterministic lexical candidate discovery, issue #375  
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

Historical RC-8 gate label: **Next bounded Reader gate — post-RC-7 retrieval architecture decision**. That gate is completed; RC-9 is now the current bounded implementation milestone.

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

## 🚧 RC-9 — Deterministic Lexical Candidate Discovery Baseline + Benchmark Runner

Tracking issue: #375.  
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
| Precision@5 | 0.217391 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

The baseline misses the cross-lingual paraphrase and surfaces all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives. It therefore records:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

This is a measured retrieval result, **not** automatic authorization for embeddings, semantic/hybrid retrieval, ANN/vector DB or claim adjudication.

## 🧩 Backlog remains separated

- #165 — exact normalized ingest dedupe/migration; no near-duplicate/semantic matching.
- #155 — downstream Epistemic Router / Evidence State RFC.
- #214 — PII fixture / reproducible supply-chain hardening.

They remain outside RC-9.

## ⏭️ After RC-9 — explicit new authorization still required

After RC-9 is fully merged, verified, synchronized and closed, a later architecture milestone **may** consider whether measured gaps justify lexical scaling, a hybrid comparison or a semantic/vector comparison. Such a milestone must pre-register its success/failure thresholds and resource/privacy/reproducibility constraints before comparison results are observed.

RC-10, semantic/hybrid retrieval, embeddings, FTS and vector indexing are **not started** by RC-9.

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

RC-9 adds authoritative English architecture/implementation source material only; broad translation remains a separate milestone.

## 🎓 Grant boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget/payment commitment. Budget change: none.

Anything merged before an agreement is existing baseline and cannot be counted again as future paid work. Reader RC-0 through RC-9 are existing pre-agreement baseline if merged before an agreement. RC-9 is not an awarded/funded-delivery claim.

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
- [Translation status](./docs/TRANSLATION_STATUS.md)