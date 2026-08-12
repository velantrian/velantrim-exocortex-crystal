<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Current signed Reader baseline:** `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` — RC-6 merged  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader baseline through RC-6

RC-0 is the normative contract. RC-1 through RC-6 are merged bounded layers:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
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

Issue #369 / PR #370 completed. Signed merge `1f5129d3276af28608b16e369fd38d21fe38c0d5`; exact post-merge CI `31566408978` was 9/9 successful.

`core/reader_long_context.py` revalidates current RC-4 leaves, orders them by RC-2 structural order + candidate-ID tie-break, and packs bounded working sets under explicit candidate/source-locator budgets. Optional RC-5 relations are carried only when both endpoints are in-set. Caller-supplied `SUMMARY` retains direct RC-4 provenance.

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

## 🚧 RC-7 — Bounded Cross-Document Candidate Links

Tracking issue: #371. Draft implementation PR: #372.

The first runtime/test head `b75811e09323adbe2c74184ae0470dfb703fcf4c` passed exact-head smoke CI `31568205231` 9/9. This is pre-merge evidence; final RC-7 implementation truth still requires final exact-head CI, guarded merge, verified signature and post-merge push CI.

RC-7 is explicit caller-supplied registration over current registered RC-4 candidates from different document identities:

```text
registered current RC-4 candidate from document A
+
registered current RC-4 candidate from document B
→ revalidate both Reader/source/pass/structure/coverage chains
→ explicit cross-document link candidate
→ exact two-sided provenance + rationale
```

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

Symmetric `CONTRADICTS`, `SAME_TOPIC` and `POSSIBLE_SAME_CLAIM` canonicalize side order. Other kinds preserve direction. Optional inspection basis is descriptive metadata only.

```text
cross-document link       != Canon relation
cross-document support    != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic                != same proposition
possible-same-claim       != claim identity
similarity signal         != identity proof
repetition across sources != corroboration
```

RC-7 adds no automatic semantic matching, entity resolution, dedupe, embeddings/ANN/vector DB, LLM/provider/parser/OCR, evidence admission, contradiction winner, truth/Canon/ESM mutation, planner authority, Reader persistence/API/CLI/worker or PostgreSQL activation.

Machine truth on the current RC-7 implementation line:

```text
reader_core_rc7_cross_document_links = true
dedicated_reader_core                = false
```

## ⏭️ After RC-7 — reassessment only

RC-7 does **not** authorize a semantic/vector retrieval implementation.

```text
RC-6 long-context strategy
→ RC-7 cross-document reading
→ only then reassess semantic/vector retrieval needs
```

Any embeddings/ANN/vector retrieval work requires separate evidence, measured need and explicit authorization. Similarity remains a candidate signal, never identity proof.

## ✅ Storage baseline remains unchanged

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL inactive import/equivalence
→ active=false
```

No automatic backend switching is introduced by Reader work.

## 🌍 Localization position during RC-7

English is source. Russian Reader-dependent root + D1/D3/D4/D5 surfaces are currently `CURRENT` against the immutable RC-6 English checkpoint `ed96a88369f841bdb2ffd79ca020acef174685fc`. This RC-7 English source checkpoint is committed first; Russian surfaces are refreshed in a separate follow-up commit pinned to that exact SHA. Eight other Reader-dependent locales preserve rich `REFRESH_NEEDED` translations; D2 and Quick Start remain current across all nine locales.

## 🎓 Grant boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget/payment commitment. Budget change: none.

Anything merged before an agreement is existing baseline and cannot be counted again as future paid work. Reader RC-0 through RC-6 are already existing baseline. If RC-7 merges pre-agreement, RC-7 also becomes existing baseline and any potential funded Reader delta must begin after RC-7.

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
- [Translation status](./docs/TRANSLATION_STATUS.md)
