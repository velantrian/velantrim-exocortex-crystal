# 🗺️ Crystal Component Map for Agents

Use this map to choose the smallest relevant inspection surface. Paths are starting points, not
substitutes for consumer/test discovery. GitHub merged `main` + executable tests + exact CI is
implementation authority.

## 1. Claims, epistemic lifecycle and physical L3

**Start:** `core/memory.py`, `core/l3_graph.py`, `core/truth_gate.py`,
`docs/CLAIM_METADATA_GLOSSARY.md`.

Storage presence does not equal strict Canon membership.

## 2. Durable backend identity

**Start:** `core/backend_profiles.py`, `core/_registry.py`, `core/l3_graph.py`, `core/doctor.py`,
`docs/architecture/DURABLE_STORAGE_PROFILE.md`.

Backend availability must not silently select another store.

## 3. SQLite lifecycle and logical portability

**Start:** `core/storage_common.py`, `core/storage_backup.py`, `core/storage_restore.py`,
`core/storage_lock.py`, `core/storage_migration.py`, `core/storage_ops.py`.

```text
SQLite backup → verify → inactive restore
SQLite profile → bounded canonical bundle → independent verification
```

## 4. PostgreSQL inactive migration target

**Start:** `core/postgresql_migration.py`, `core/postgresql_migration_impl.py`,
`docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md`,
`docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md`.

Current target remains `active=false`; no automatic switching/cutover is implied.

## 5. Truth admission and safety

**Start:** Guardian functions in `core/pipeline.py`, `core/truth_gate.py`, `core/immune.py`,
`core/api_ingest_policy.py`.

Reader/retrieval/evaluation artifacts cannot bypass the audited admission path.

## 6. Strict read grounding

**Start:** `core/canonical_view.py`, `core/trust_snapshot.py`, `core/query_pipeline.py`,
public handlers in `core/api.py`, `core/cli.py` and MCP surfaces.

Public query/search paths are read-only.

## 7. Admitted-memory retrieval

**Start:** `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`,
`core/query_pipeline.py`, `core/rrf.py`, `core/pipeline.py`.

These modules operate around admitted memory and are not automatic PRE-ADMISSION Reader identity
authority.

```text
retrieval rank != truth
similarity != identity
ranking != epistemic authority
```

## 8. Reader RC-1..RC-5

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

## 9. Reader RC-6 long context

**Start:** `core/reader_long_context.py`, `tests/test_reader_long_context.py`.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != Canon admission
```

## 10. Reader RC-7 cross-document candidates

**Start:** `core/reader_cross_document.py`, `tests/test_reader_cross_document.py`.

Signed merge `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`; post-merge CI `31572918731`.

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## 11. Reader RC-8 retrieval architecture decision

**Start:** `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`,
`eval/reader_rc8_retrieval_adversarial.jsonl`,
`tests/test_reader_rc8_retrieval_architecture.py`; issue #373 / PR #374.

RC-8 defined candidate-discovery/identity/admission separation and required lexical evidence
before semantic/vector machinery could be considered.

## 12. Reader RC-9 deterministic lexical candidate discovery — COMPLETE

**Start:** `core/reader_lexical_discovery.py`, `scripts/bench_reader_rc9_lexical.py`,
`tests/test_reader_lexical_discovery.py`, `tests/test_bench_reader_rc9_lexical.py`,
`eval/reader_rc9_lexical_baseline.json`,
`docs/architecture/READER_RC9_LEXICAL_BASELINE.md`; issue #375 / PR #376.

Signed merge `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`; post-merge CI `31594027040`.

Historical K=5 result: Recall `0.937500`; Precision `0.187500`; MRR `0.895833`;
paired hard-negative rate `1.000000`. Classification:
`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## 13. Reader RC-10 reuse/comparison preregistration — COMPLETE

**Start:** `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`,
`eval/reader_rc10_retrieval_comparison_preregistration.json`,
`tests/test_reader_rc10_retrieval_preregistration.py`; PR #378 / issue #377.

RC-10 is preregistration only. No semantic/hybrid comparator is executed.

```text
comparison pass != runtime authorization
```

## 14. Post-RC-10 reassessment — COMPLETE

**Start:** `docs/architecture/READER_POST_RC10_REASSESSMENT.md`,
`eval/reader_post_rc10_reassessment.json`; issue #382 / PR #383.

Decision: `measured retrieval-quality gap != measured scaling gap`; Evaluation Surface v2 was
selected as the next bounded research milestone.

## 15. Reader Retrieval Evaluation Surface v2 — CURRENT EVALUATION EVIDENCE

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

Final surface: 24 queries, 144 candidates/qrels, judgment coverage `1.0`, opaque
content-derived **qrel-label-independent** candidate IDs, composite SHA-256
`7af2b1247e1c1c2590b6b2c830dd605da646989856b6c29cee18aac3e1f785e8`.

Unchanged RC-9 final v2 control: 42/48 useful, Recall@5 `0.875000`, fixed-slot Precision@5
`0.350000`, judged precision-over-returned `0.355932`, MRR `0.857639`, 38/48 hard negatives.

The v2 gate is frozen before any model-backed result and requires exact backend/model/dependency
identity, exact index identity when indexed or explicit no-index, privacy review, no `auto`,
zero query-time network calls and zero external Reader source-text transmission.

```text
retrieval match != evidence
similarity != identity
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

**No model-backed comparator execution and no semantic/hybrid/vector Reader runtime is added.**

## 16. Contradictions and curator decisions

**Start:** contradiction modules, `core/review.py`, `core/conflict_surfaces.py`,
`docs/CONTRADICTION_POLICY.md`.

Detection/retrieval does not select a winner.

## 17. Imports, review queues and public composition

**Start:** import/review session modules, `core/api.py`, `core/cli.py`, MCP modules, `Dockerfile`,
`pyproject.toml`, `.github/workflows/ci.yml`.

Reader RC-1 through Evaluation Surface v2 add no public autonomous Reader service or new ordinary
runtime-composition wiring.

## 18. Evaluation and status evidence

**Start:** `docs/EVAL.md`, `TEST_REPORT.md`, `docs/status/implementation-manifest.json`,
`docs/STATUS.md`, `docs/IMPLEMENTATION_STATUS.md`, Ring Zero/eval workflows.

Always bind implementation claims to exact commit/head/CI. Retrieval benchmarks are not
semantic-adjudication certifications.

## 19. Machine Reader truth

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
dedicated_reader_core = false
```

No automatic Reader parser/OCR/multimodal engine, semantic/hybrid/vector Reader runtime,
automatic semantic equivalence/entity resolution, durable Reader vector schema or dedicated/full
autonomous Reader exists.

## 20. Documentation, grant and research governance

**Start:** `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`,
`docs/IMPLEMENTATION_STATUS.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`,
`docs/ai/WORK_LOG.md`.

GitHub merged `main` proves implementation; Notion is synchronized only after exact post-merge
evidence. NLnet remains `submitted / under review / not awarded`. Issues #155, #165 and #214
remain separate scopes.
