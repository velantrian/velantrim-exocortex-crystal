<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372  
**Signed RC-8 merge:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` — PR #374  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**Audited start after PR #378:** `main@430e643a2a3759da793f700617a327d419439dde`, CI `31603785427` — 9/9 successful  
**Current bounded milestone:** issue #379 — post-RC-9 grant presentation truth reconciliation  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader implementation baseline

RC-0 is the normative contract. RC-1 through RC-7 are merged bounded Reader/domain layers.
RC-8 is a completed architecture/research decision. RC-9 is the current implemented Reader
retrieval baseline.

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

### RC-1 — evidence-linked Reader skeleton

Exact source/version identity, replayable locators, Reader sessions, fidelity, coverage,
bookmarks/open loops and fail-visible stale/privacy semantics.

### RC-2 — structural document map

Caller-supplied version-bound hierarchy/order with explicit recovery/ambiguity states. No
parser/OCR/layout authority.

### RC-3 — explicit multi-pass mechanics

`ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD` with explicit
targets/outcomes/state and count-only telemetry.

### RC-4 — source-linked proposition extraction

Source-linked caller-supplied `EXTRACTED_PROPOSITION` candidates with attribution/category,
negation/qualifiers and exact provenance.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### RC-5 — relation candidates

Same-session/same-version PRE-ADMISSION `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`,
`QUALIFICATION` candidates with exact two-sided provenance and no resolution/admission authority.

### RC-6 — bounded long context

Deterministic bounded working sets over valid RC-4 leaves plus caller-supplied `SUMMARY` with
direct leaf provenance.

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

### RC-7 — bounded cross-document candidate links

Explicit caller-selected cross-document links with exact two-sided provenance. No automatic
semantic matching/entity resolution/corroboration.

```text
cross-document link       != Canon relation
same-topic                != same proposition
possible-same-claim       != claim identity
similarity signal         != identity proof
repetition across sources != corroboration
```

## ✅ RC-8 — retrieval architecture decision

Issue #373 / PR #374 completed. Decision:
`docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Frozen adversarial corpus:
`eval/reader_rc8_retrieval_adversarial.jsonl`.

RC-8 separated PRE-ADMISSION Reader candidate discovery from admitted-memory retrieval and
required a deterministic lexical baseline before semantic/vector machinery could even be
considered.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

Existing admitted-memory retrieval (`core/embedding.py`, `core/legacy_retrieval.py`,
`core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py` and related composition)
remains a different authority/data lifecycle.

## ✅ RC-9 — deterministic lexical candidate discovery + benchmark

Issue #375 / PR #376 completed. Runtime: `core/reader_lexical_discovery.py`. Benchmark runner:
`scripts/bench_reader_rc9_lexical.py`. Frozen result: `eval/reader_rc9_lexical_baseline.json`.

RC-9 is stdlib-only, offline and in-memory. It snapshots source-linked RC-4 proposition
candidates, applies conservative NFKC/case/whitespace normalization and stable tokenization,
then performs deterministic BM25 ranking for inspection only.

Frozen K=5 benchmark:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

The cross-lingual pair `rc8-004` is missed and all four paired hard negatives surface in top-5.
Classification:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

This is measured retrieval evidence, not semantic/adjudication accuracy and not authorization
for embeddings, semantic/hybrid retrieval, ANN/vector DB, entity/claim identity or evidence
admission.

## 📜 PR #378 — reuse/comparison preregistration only

PR #378 merged the RC-10 existing-retrieval reuse compatibility and future-comparison
preregistration contract. Tracking issue #377 remains separate.

It records which existing admitted-memory helpers may be evaluated later and freezes a future
comparison gate before results. It **does not execute** a semantic/hybrid comparator, implement
Reader FTS/vector runtime, download a model, activate PostgreSQL/pgvector or change Canon/
TruthGate/Guardian authority.

```text
comparison pass != runtime authorization
```

## 🧾 Current bounded milestone — #379 grant presentation truth reconciliation

This milestone is documentation-heavy. Its purpose is to make the public/grant first impression
match the signed RC-9 implementation and benchmark truth.

Scope:

- reconcile root English README;
- reconcile NLnet scope and existing-vs-funded-delta matrix;
- reconcile directly affected English grant/reviewer surfaces;
- publish exact RC-9 metrics with their real names and limitations;
- publish a simple reviewer reproduction path;
- update docs-status semantics so stale RC-5/RC-7-draft current-state language cannot return;
- preserve explicit localization debt rather than auto-translating it.

Out of scope: `core/**`, RC-10 comparator execution, semantic/hybrid/vector Reader runtime,
embeddings, FTS, ANN, PostgreSQL/pgvector activation, #155, #165, #214 and broad localization.

## 🧩 Backlog remains separated

- #165 — exact normalized ingest dedupe/migration; no near-duplicate/semantic matching.
- #155 — downstream Epistemic Router / Evidence State RFC.
- #214 — PII fixture / reproducible supply-chain hardening.
- #377 — separate RC-10 preregistration/completion bookkeeping; #379 does not execute a comparator.

## ⏭️ Future Reader work requires new authorization

No next Reader implementation capability follows automatically from RC-9 or #379.

A future comparison may be considered only against a frozen gate and with exact backend/model
identity, privacy/resource review and zero authority violations. Passing a comparison would make
a candidate eligible for stronger evaluation/architecture review only; it would not authorize
runtime adoption.

No semantic/hybrid comparison, embeddings, FTS, ANN/vector indexing, PostgreSQL activation,
automatic adjudication or broad localization starts automatically.

## ✅ Storage baseline remains unchanged

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL inactive import/equivalence
→ active=false
```

No automatic backend switching is introduced by Reader or grant-presentation work.

## 🌍 Localization position

Russian Reader-dependent D1/D3/D4/D5 surfaces remain tied to the immutable RC-7 English source
checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs
remain rich `REFRESH_NEEDED` translations — 64 tracked detail documents. D2 and Quick Start
remain current where source semantics did not change.

Issue #379 advances the English root/grant presentation to post-RC-9 truth only. A dedicated
later localization milestone is required for full parity with the new English first-impression
source; this debt is not hidden by automatic translation here.

## 🎓 Grant boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only,
not an approved budget/payment commitment. Budget change: none.

RC-1 through RC-9 merged before any agreement are existing pre-agreement Reader baseline and
cannot be counted again as future paid work. PR #378's preregistration is also existing
pre-agreement repository history, not funded Reader runtime.

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
- [Funding use plan](./docs/grants/funding-use-plan.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [RC-8 retrieval decision](./docs/architecture/READER_RC8_RETRIEVAL_DECISION.md)
- [RC-9 lexical baseline](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [RC-10 preregistration contract](./docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
