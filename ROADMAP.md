<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372  
**Signed RC-8 merge:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` — PR #374  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**PR #378 / RC-10 preregistration merge:** `main@430e643a2a3759da793f700617a327d419439dde`; issue #377 is closed / completed  
**Post-grant-reconciliation checkpoint:** signed `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`, CI `31620098274` — 9/9 successful  
**Current bounded milestone:** issue #382 — post-RC-10 evaluation adequacy / next-milestone architecture decision  
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

## ✅ PR #378 / issue #377 — RC-10 preregistration complete

PR #378 merged the RC-10 existing-retrieval reuse compatibility and future-comparison
preregistration contract. Its tracking issue #377 is now closed / completed after the missing
completion-evidence bookkeeping step was repaired.

It records which existing admitted-memory helpers may be evaluated later and freezes a future
comparison gate before results. It **does not execute** a semantic/hybrid comparator, implement
Reader FTS/vector runtime, download a model, activate PostgreSQL/pgvector or change Canon/
TruthGate/Guardian authority.

```text
comparison pass != runtime authorization
```

## ✅ Post-RC-9 grant presentation reconciliation — complete

Issue #379 / PR #380 plus final-audit micro-fix PR #381 completed the public/grant truth
reconciliation. Final signed checkpoint: `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`;
exact push CI `31620098274` was 9/9 successful.

The reconciliation changed presentation/truth surfaces only. It added no Reader runtime,
semantic/vector retrieval, FTS, storage activation or epistemic authority.

## 🧭 Current bounded milestone — #382 post-RC-10 reassessment

Durable decision: `docs/architecture/READER_POST_RC10_REASSESSMENT.md`. Machine-readable
architecture decision: `eval/reader_post_rc10_reassessment.json`.

The reassessment distinguishes the measured retrieval-quality problem from an unmeasured scale
problem:

```text
measured retrieval-quality gap != measured scaling gap
```

Current evidence does not justify SQLite FTS/ANN/server infrastructure as the next Reader step.
The existing hashing/trigram embedders remain comparison signals, and `core/rrf.py` remains a
pure future ordering utility. A model-backed cross-lingual comparator is plausible as a later
experiment but is not selected or executed here.

The smallest justified next bounded milestone is **Reader Retrieval Evaluation Surface v2**:
a stronger pre-frozen judged evaluation surface plus unchanged RC-9 control reproduction,
created before any model-backed comparator result is observed.

**Evaluation Surface v2 is NOT STARTED by #382.** It requires separate authorization after this
architecture milestone completes.

## 🧩 Backlog remains separated

- #165 — exact normalized ingest dedupe/migration; no near-duplicate/semantic matching.
- #155 — downstream Epistemic Router / Evidence State RFC.
- #214 — PII fixture / reproducible supply-chain hardening.
- #382 — current architecture/evaluation decision only; no comparator execution/runtime.

## ⏭️ Future Reader work requires new authorization

No Reader implementation capability follows automatically from RC-9, PR #378 or #382.

The next selected research milestone, if separately authorized, is **Evaluation Surface v2**.
It must preserve the existing RC-8 corpus and RC-10 thresholds unchanged, add a separate
versioned stronger judged surface, and reproduce RC-9 as the control without running a
model-backed comparator in the same corpus-freeze milestone.

Only after that surface is frozen may a separately authorized comparator execution be
considered. Any future comparator still must pass the unchanged RC-10 screen and then the
stronger evaluation; a pass remains architecture-review eligibility only.

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

No automatic backend switching is introduced by Reader architecture or grant-presentation work.

## 🌍 Localization position

Russian Reader-dependent D1/D3/D4/D5 surfaces remain tied to the immutable RC-7 English source
checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs
remain rich `REFRESH_NEEDED` translations — 64 tracked detail documents. D2 and Quick Start
remain current where source semantics did not change.

The post-RC-9 grant reconciliation advanced the English root/grant presentation only. The #382
architecture decision is English source material; broad localization remains a separate
milestone and existing translation debt is not hidden.

## 🎓 Grant boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only,
not an approved budget/payment commitment. Budget change: none.

RC-1 through RC-9 merged before any agreement are existing pre-agreement Reader baseline and
cannot be counted again as future paid work. PR #378's preregistration and the #382 architecture
decision are also existing pre-agreement repository history if merged before any funding
agreement; neither is funded Reader runtime.

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
- [Post-RC-10 reassessment](./docs/architecture/READER_POST_RC10_REASSESSMENT.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)