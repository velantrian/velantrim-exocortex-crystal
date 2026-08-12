<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` — PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**Current bounded milestone:** RC-10 reuse compatibility + comparison pre-registration, issue #377  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader baseline through RC-7

RC-0 is normative. RC-1 through RC-7 are merged bounded layers:

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
Exact SourceVersion/SourceLocator identity, Reader sessions, fidelity, coverage and stale/privacy semantics.

### ✅ RC-2 — Structural Document Map
Caller-supplied version-bound hierarchy/order; structure is metadata, not truth.

### ✅ RC-3 — Explicit Multi-Pass Reading Mechanics
`ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD` with explicit state/outcomes.

### ✅ RC-4 — Source-Linked Proposition Extraction

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### ✅ RC-5 — Exceptions / Contradiction Candidate Detection

`core/reader_relations.py` registers PRE-ADMISSION `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` over valid RC-4 candidates.

```text
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

### ✅ RC-6 — Bounded Long-Context Strategy

The historical sequencing phrase remains: **RC-6 long-context strategy → RC-7 cross-document reading**.

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

### ✅ RC-7 — Bounded Cross-Document Candidate Links

Issue #371 / PR #372 completed at signed `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`; post-merge CI `31572918731` 9/9.

```text
cross-document link       != Canon relation
cross-document support    != admitted evidence
same-topic                != same proposition
possible-same-claim       != claim identity
similarity signal         != identity proof
repetition across sources != corroboration
```

RC-7 adds no automatic semantic matching, embeddings/ANN/vector, entity resolution, evidence admission or contradiction winner.

## ✅ RC-8 — Post-RC-7 Candidate Discovery & Retrieval Architecture Decision

Issue #373 / PR #374 completed. Decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

RC-8 identified corpus candidate discovery as the gap, not “a vector DB”. It separated PRE-ADMISSION Reader candidate discovery from admitted-memory retrieval and required a deterministic lexical baseline before any semantic/vector comparison.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

Historical option order remains:

```text
deterministic normalized/token baseline
        ↓
SQLite FTS candidate (feature-detected, bounded fallback)
        ↓
measured hybrid comparison if needed
        ↓
measured semantic/vector comparison only if justified
```

## ✅ RC-9 — Deterministic Lexical Candidate Discovery Baseline + Benchmark Runner

Issue #375 / PR #376 completed. Signed merge `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`; exact validated head `1956cbd45e5a5b794852354ed2233bf1fb6e318f`; exact-head CI `31593097846` 9/9; post-merge CI `31594027040` 9/9.

Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Runtime: `core/reader_lexical_discovery.py`. Frozen result: `eval/reader_rc9_lexical_baseline.json`.

Frozen K=5:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. The cross-lingual paraphrase is missed; all four paired hard negatives are surfaced. This is retrieval evidence, not candidate adjudication or semantic/vector authorization.

## 🚧 RC-10 — Existing Retrieval Reuse Compatibility + Comparison Pre-Registration

Tracking issue: #377. Contract: `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`. Machine-readable gate: `eval/reader_rc10_retrieval_comparison_preregistration.json`.

RC-10 exists specifically to avoid duplicating what Crystal already has. Audit found admitted-memory vector/hash/trigram/optional-SBERT retrieval, graph walk, bounded legacy lexical retrieval and pure RRF already exist.

Disposition:

```text
core/rrf.py                         → future comparison reuse candidate
HashingEmbedder / TrigramHashing   → comparator signals only
SentenceTransformerEmbedder        → future optional comparator only
get_embedder("auto")               → forbidden for preregistered comparison
core/pipeline.py                    → not a Reader pipeline
core/query_pipeline.py              → not a Reader pipeline
core/legacy_retrieval.py            → not a Reader backend
SQLite FTS5                         → not implemented for Reader; future scaling option
PostgreSQL/pgvector                 → inactive / not authorized
```

Future comparison gate is frozen before results: retain all 15 RC-9 positive hits, recover `rc8-004` to 16/16 Recall@5, MRR >=0.895833, paired hard-negative hits <=2/4, zero authority violations, exact backend identity, no auto mode, zero query-time network calls and no external source-text transmission.

```text
comparison pass != runtime authorization
```

RC-10 runs no semantic/hybrid comparator and adds no Reader retrieval runtime.

## 🧩 Backlog remains separated

- #165 — exact normalized admitted-fact dedupe/migration; no near-duplicate/semantic matching.
- #155 — downstream Epistemic Router / Evidence State RFC.
- #214 — PII fixture / reproducible supply-chain hardening.

## ⏭️ After RC-10 — explicit new authorization still required

If RC-10 merges, a future milestone may execute an isolated comparator against the frozen gate. Passing only makes the comparator eligible for stronger evaluation/architecture review; it does not authorize runtime adoption. A larger/stronger evaluation surface remains required before semantic Reader runtime could be considered.

Do not automatically implement FTS, semantic/hybrid runtime, embeddings, ANN/vector indexing, PostgreSQL activation, adjudication or localization refresh.

## ✅ Storage baseline remains unchanged

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL inactive import/equivalence
→ active=false
```

## 🌍 Localization position

Russian root + Reader-dependent D1/D3/D4/D5 surfaces remain `CURRENT` to the immutable RC-7 English source checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, 64 tracked documents. RC-8 through RC-10 add English source meaning only; broad translation stays separate.

The English root README still carries an older RC-6/RC-7 checkpoint and is tracked by RC-10 as public-documentation drift; correcting it with proper localized freshness accounting belongs in a separate public/localization reconciliation rather than being hidden inside this architecture milestone.

## 🎓 Grant boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved commitment. Anything merged before an agreement is existing baseline and cannot be counted again as future funded delta.
