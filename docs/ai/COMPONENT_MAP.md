# 🗺️ Crystal Component Map for Agents

Use this map to choose the smallest relevant inspection surface. GitHub merged `main`, executable tests and exact CI are implementation authority.

## 1. Claims / admission / storage

**Start:** `core/memory.py`, `core/l3_graph.py`, `core/truth_gate.py`, `core/pipeline.py`, `core/backend_profiles.py`.

SQLite remains the active ordinary local-first profile. PostgreSQL/pgvector remains an inactive `active=false` import/equivalence target. Backend availability must not silently select another store.

## 2. Read/query and admitted-memory retrieval

**Start:** `core/canonical_view.py`, `core/trust_snapshot.py`, `core/query_pipeline.py`, `core/embedding.py`, `core/legacy_retrieval.py`, `core/rrf.py`.

```text
retrieval rank != truth
similarity != identity
ranking != epistemic authority
```

These admitted-memory utilities are not automatic PRE-ADMISSION Reader identity authority.

## 3. Reader RC-1..RC-5

**Start:**
- `core/reader_core.py` / `tests/test_reader_core.py`;
- `core/reader_structure.py` / `tests/test_reader_structure.py`;
- `core/reader_passes.py` / `tests/test_reader_passes.py`;
- `core/reader_extraction.py` / `tests/test_reader_extraction.py`;
- `core/reader_relations.py` / `tests/test_reader_relations.py`.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

## 4. Reader RC-6 / RC-7

**Start:** `core/reader_long_context.py`, `core/reader_cross_document.py` and their tests.

RC-7 signed merge `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`; post-merge CI `31572918731`.

```text
working-set coverage != comprehension proof
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## 5. Reader RC-8 / RC-9 / RC-10

**RC-8:** `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`, `eval/reader_rc8_retrieval_adversarial.jsonl`.

**RC-9:** `core/reader_lexical_discovery.py`, `scripts/bench_reader_rc9_lexical.py`, `eval/reader_rc9_lexical_baseline.json`, `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`; signed merge `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`, post-merge CI `31594027040`.

Historical RC-9 classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

**RC-10:** `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`, `eval/reader_rc10_retrieval_comparison_preregistration.json`; PR #378 / issue #377 completed. No comparator executed.

```text
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

## 6. Post-RC-10 reassessment

**Start:** `docs/architecture/READER_POST_RC10_REASSESSMENT.md`, `eval/reader_post_rc10_reassessment.json`; issue #382 / PR #383.

Decision: `measured retrieval-quality gap != measured scaling gap`; Evaluation Surface v2 selected as the next bounded evaluation milestone.

## 7. Reader Retrieval Evaluation Surface v2 — CURRENT EVALUATION EVIDENCE

**Start:**

- `docs/architecture/READER_RETRIEVAL_EVAL_V2.md`;
- `scripts/bench_reader_eval_v2_lexical.py`;
- `eval/reader_retrieval_eval_v2_queries.jsonl`;
- `eval/reader_retrieval_eval_v2_candidates.jsonl`;
- `eval/reader_retrieval_eval_v2_qrels.jsonl`;
- `eval/reader_retrieval_eval_v2_manifest.json`;
- `eval/reader_retrieval_eval_v2_rc9_control.json`;
- `eval/reader_retrieval_eval_v2_future_comparator_gate.json`;
- `tests/test_bench_reader_eval_v2_lexical.py`;
- `tests/test_reader_retrieval_eval_v2_status.py`;
- issue #384 / PR #385.

Final surface: 24 queries, 144 candidates/qrels, judgment coverage `1.0`, opaque content-derived qrel-label-independent candidate IDs, composite SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.

Reviewed scope conflicts in q04 and q23 are useful `POSSIBLE_CONTRADICTION` candidates. The final q23 review-class correction changes the qrels/surface hash but not the RC-9 ranking metrics.

Unchanged RC-9 final v2 control: 42/48 useful, Recall@5 `0.875000`, fixed-slot Precision@5 `0.350000`, judged precision-over-returned `0.355932`, MRR `0.857639`, 38/48 hard negatives.

The future gate is frozen before model-backed results and requires exact backend/model/dependency/index identity or explicit no-index, privacy review, no `auto`, zero query-time network calls and zero external Reader source-text transmission.

```text
retrieval match != evidence
similarity != identity
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

No model-backed comparator execution and no semantic/hybrid/vector Reader runtime is added.

## 8. Machine Reader truth

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
bounded_reader_product_bridge_v0_1 = true   # merged in PR #455; current main since 2026-08-23
dedicated_reader_core = false
```

### Reader Product Bridge v0.1 — MERGED / IN MAIN

**Start:** `core/reader_product_bridge.py`, `tests/test_reader_product_bridge.py`, `docs/architecture/READER_PRODUCT_BRIDGE_V0_1.md`.

PR #455 merged reviewed head `5636e312305369513ac3541761d339c27c3010b3` as signed merge commit `06e81edc159838b4129b41284d701823ce49cff8`. Final exact-head CI #1787 / run `32643913034` completed 9/9 SUCCESS before merge.

The bridge composes existing RC-1..RC-3 primitives into a foreground product-style run with exactly one `BROAD_READ` and at most one `TARGETED_REREAD`. Remaining session-visible `UNREAD`/`NEEDS_REVIEW` coverage fails closed to `DEGRADED`.

Its boundedness is **pass-bounded orchestration depth**. v0.1 intentionally does not claim a target-count, character, time, token or executor-cost budget; such resource ceilings require a separate reviewed stage.

```text
scheduled != processed
coverage != comprehension proof
Reader product result != evidence admission
Reader product result != Canon
merge != production authorization
```

It adds no parser/file ingestion, LLM/provider, automatic extraction, semantic/vector retrieval, public CLI/API, persistence, background worker, TruthGate/Guardian/memory/Canon write path, or production authorization.

No automatic Reader parser/OCR/multimodal engine, semantic/hybrid/vector Reader runtime, automatic semantic equivalence/entity resolution, durable Reader vector schema or dedicated/full autonomous Reader exists.

## 9. Documentation / grant governance

**Start:** `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`, `docs/IMPLEMENTATION_STATUS.md`, `ROADMAP.md`, `docs/ai/WORK_LOG.md`.

NLnet remains `submitted / under review / not awarded`. Issues #155, #165 and #214 remain separate scopes. Notion is synchronized only after exact post-merge evidence.
