# 🗺️ Crystal Component Map for Agents

Use this map to choose the smallest relevant inspection surface. Paths are starting points, not substitutes for producer/consumer/test discovery.

## 1. Truth, storage and read authority

- Claims/L3: `core/memory.py`, `core/l3_graph.py`, `core/truth_gate.py`.
- SQLite lifecycle: `core/storage_*.py`; ordinary active local-first.
- PostgreSQL inactive migration: `core/postgresql_migration*.py`; target `active=false`, not ordinary runtime.
- Strict read grounding: `core/canonical_view.py`, `core/trust_snapshot.py`, `core/query_pipeline.py`, public HTTP/CLI/MCP handlers.

Physical L3 is not strict Canon. Public query/search paths are read-only. Guardian and TruthGate remain the admission owners.

## 2. Admitted-memory retrieval

Start with `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py`.

These operate around admitted L3/query state. Retrieval rank, similarity and model output are not evidence or admission.

```text
retrieval rank != truth
similarity != identity
ranking != epistemic authority
```

Do not wire these modules directly into Reader identity simply because they already exist.

## 3. Reader RC-1 → RC-7

- RC-1: `core/reader_core.py` / `tests/test_reader_core.py`.
- RC-2: `core/reader_structure.py` / `tests/test_reader_structure.py`.
- RC-3: `core/reader_passes.py` / `tests/test_reader_passes.py`.
- RC-4: `core/reader_extraction.py` / `tests/test_reader_extraction.py`.
- RC-5: `core/reader_relations.py` / `tests/test_reader_relations.py`.
- RC-6: `core/reader_long_context.py` / `tests/test_reader_long_context.py`.
- RC-7: `core/reader_cross_document.py` / `tests/test_reader_cross_document.py`.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 registers explicit caller-selected cross-document pairs only; it does not discover corpus pairs automatically.

## 4. RC-8 retrieval architecture decision

Start: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`, `eval/reader_rc8_retrieval_adversarial.jsonl`, `tests/test_reader_rc8_retrieval_architecture.py`.

RC-8 separates PRE-ADMISSION candidate discovery from downstream adjudication/admission and authorizes lexical baseline measurement before any semantic/vector comparison.

## 5. RC-9 deterministic lexical candidate discovery

Start:

- `core/reader_lexical_discovery.py`;
- `scripts/bench_reader_rc9_lexical.py`;
- `tests/test_reader_lexical_discovery.py`;
- `tests/test_bench_reader_rc9_lexical.py`;
- `eval/reader_rc9_lexical_baseline.json`;
- `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`;
- issue #375.

RC-9 is PRE-ADMISSION, stdlib-only, offline and in-memory. It uses conservative lexical normalization/tokenization and deterministic BM25 ranking to suggest inspection candidates. It does not assign RC-8 review classes or create RC-7 links.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

Frozen K=5 benchmark: Recall 0.937500; Precision 0.217391; MRR 0.895833; paired hard-negative rate 1.000000. The measured classification is `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`, not semantic/vector authorization.

## 6. Contradictions / review / admission

Start: contradiction modules, `core/review.py`, `core/conflict_surfaces.py`, `core/pipeline.py`, `core/truth_gate.py`.

Detection/discovery does not select a winner. `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE` remain explicit audited curator decisions. RC-5/RC-7/RC-9 cannot resolve a contradiction or admit evidence.

## 7. Public surfaces and runtime composition

Start: `core/api.py`, `core/cli.py`, MCP modules, `Dockerfile`, `pyproject.toml`, `.github/workflows/ci.yml`.

Reader RC-1 through RC-9 add no public Reader retrieval API, CLI or background worker. RC-9 does not change ordinary runtime storage composition and adds no mandatory dependency.

## 8. Evaluation and status evidence

Start: `TEST_REPORT.md`, `docs/status/implementation-manifest.json`, `docs/STATUS.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ai/CURRENT_STATE.md`, Ring Zero/eval workflows.

RC-9 benchmark is a small synthetic retrieval baseline, not production quality certification. Exact-head CI and post-merge CI remain required evidence for implementation status.

## 9. Reader implementation truth

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

Current non-features: no automatic Reader parser/OCR/multimodal engine; no automatic NLP/LLM extraction/summarization; no semantic/hybrid/vector Reader retrieval; no automatic entity/claim identity; no durable Reader retrieval schema; no public Reader retrieval service; no dedicated/full autonomous Reader runtime.

## 10. Documentation, grant and research governance

Start: `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`.

GitHub `main` proves implementation; Notion is synchronized after exact post-merge evidence. NLnet remains `submitted / under review / not awarded`. Issues #155, #165 and #214 remain separate from RC-9.
