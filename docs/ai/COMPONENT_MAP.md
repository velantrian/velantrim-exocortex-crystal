# 🗺️ Crystal Component Map for Agents

Use this map to choose the smallest relevant inspection surface. Paths are starting points, not substitutes for producer/consumer/test discovery.

## 1. Claims, epistemic lifecycle and physical L3

**Start:** `core/memory.py`, `core/l3_graph.py`, `core/truth_gate.py`. Storage presence does not equal strict Canon membership.

## 2. Durable backend identity

**Start:** `core/backend_profiles.py`, `core/_registry.py`, `core/l3_graph.py`, `core/doctor.py`. Backend availability must not silently select another store.

## 3. SQLite lifecycle and logical portability

**Start:** `core/storage_common.py`, `core/storage_backup.py`, `core/storage_restore.py`, `core/storage_lock.py`, `core/storage_migration.py`, `core/storage_ops.py`.

## 4. PostgreSQL inactive migration target

**Start:** `core/postgresql_migration.py`, `core/postgresql_migration_impl.py`, `docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md`. Current target remains `active=false`.

## 5. Truth admission and safety

**Start:** Guardian functions in `core/pipeline.py`, `core/truth_gate.py`, `core/immune.py`, `core/api_ingest_policy.py`. Reader/retrieval artifacts cannot bypass Guardian/TruthGate.

## 6. Strict read grounding

**Start:** `core/canonical_view.py`, `core/trust_snapshot.py`, public API/CLI/MCP handlers. Public query/search paths are read-only.

## 7. Admitted-memory retrieval

**Start:**

- `core/embedding.py` — hashing/trigram hashing + optional SentenceTransformer;
- `core/legacy_retrieval.py` — bounded lexical fallback for legacy/uninitialised L3;
- `core/retrieval_config.py` — bounded admitted-memory knobs;
- `core/query_pipeline.py` — canonical read-only query path;
- `core/rrf.py` — rank fusion;
- `core/pipeline.py` — admitted-memory vector/graph retrieval composition.

```text
retrieval rank != truth
similarity != identity
ranking != epistemic authority
```

Do not wire admitted-memory modules directly into Reader identity merely because they exist.

## 8. Reader proposition extraction and same-document relations

**Start:** `core/reader_extraction.py`, `core/reader_relations.py`.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

## 9. Reader long context

**Start:** `core/reader_long_context.py`.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

## 10. Reader cross-document candidate links

**Start:** `core/reader_cross_document.py`.

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

Signed RC-7 merge remains `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`; post-merge CI `31572918731` 9/9.

## 11. RC-8 retrieval architecture decision — COMPLETE

**Start:** `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`, `eval/reader_rc8_retrieval_adversarial.jsonl`, issue #373 / PR #374.

RC-8 separates candidate discovery, candidate adjudication and downstream evidence/admission. It required a deterministic lexical baseline before any semantic/hybrid/vector comparison.

## 12. RC-9 deterministic lexical candidate discovery — COMPLETE

**Start:** `core/reader_lexical_discovery.py`, `scripts/bench_reader_rc9_lexical.py`, `eval/reader_rc9_lexical_baseline.json`, `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`, PR #376 / issue #375.

Signed merge: `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`; exact-head/post-merge CI `31593097846` / `31594027040`, 9/9.

Frozen K=5: Recall 0.937500; Precision 0.187500; MRR 0.895833; paired hard-negative rate 1.000000. Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

`ReaderLexicalMatch` exposes retrieval/provenance metadata only. Candidate discovery is not candidate adjudication.

## 13. RC-10 reuse compatibility + preregistration — CURRENT BOUNDED MILESTONE

**Start:**

- `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`;
- `eval/reader_rc10_retrieval_comparison_preregistration.json`;
- `tests/test_reader_rc10_retrieval_preregistration.py`;
- issue #377.

RC-10 does not add runtime. Its audit disposition is:

- `core/rrf.py` → future isolated comparison reuse candidate only;
- deterministic hashing/trigram embedders → comparator signals only;
- SentenceTransformer → future optional comparator requiring separate authorization;
- `get_embedder("auto")` → forbidden for preregistered Reader comparison;
- admitted-memory pipeline/query/legacy retrieval → no direct PRE-ADMISSION Reader wiring;
- SQLite FTS → not implemented for Reader, future feature-detected scaling option;
- PostgreSQL/pgvector → inactive / unauthorized.

Future gate: recover `rc8-004`, retain all 15 RC-9 useful hits, Recall@5 1.0, MRR >=0.895833, paired hard-negative hits <=2/4, zero authority violations, exact backend identity and zero query-time network calls.

```text
comparison pass != runtime authorization
```

## 14. Contradictions and curator decisions

Detection does not select a winner. `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE` require explicit authorized decisions.

## 15. Public surfaces and runtime composition

**Start:** `core/api.py`, `core/cli.py`, MCP modules, Dockerfile, pyproject and CI. Reader RC-1 through RC-10 add no public Reader API/CLI/background worker. RC-10 adds no dependency or index.

## 16. Evaluation and status evidence

**Start:** `docs/EVAL.md`, `TEST_REPORT.md`, `docs/status/implementation-manifest.json`, RC-8/RC-9/RC-10 eval files and CI.

The RC-8/9 corpus is a small synthetic paired diagnostic surface, not production semantic certification.

## 17. Reader architecture chain

**Start:**

- `core/reader_core.py` — RC-1;
- `core/reader_structure.py` — RC-2;
- `core/reader_passes.py` — RC-3;
- `core/reader_extraction.py` — RC-4;
- `core/reader_relations.py` — RC-5;
- `core/reader_long_context.py` — RC-6;
- `core/reader_cross_document.py` — RC-7;
- `core/reader_lexical_discovery.py` — RC-9;
- `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md` — RC-10.

Machine truth:

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

Current non-features: no automatic Reader parser/OCR/model extraction, no semantic/hybrid/vector Reader runtime, no automatic semantic equivalence/entity resolution, no durable Reader retrieval schema/migration and no dedicated/full autonomous Reader runtime.

## 18. Documentation, grant and research governance

**Start:** `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`, `docs/IMPLEMENTATION_STATUS.md`, `ROADMAP.md`, `docs/GRANT_NLNET_SCOPE.md`.

NLnet remains `submitted / under review / not awarded`. Issues #155, #165 and #214 remain separate. The English root README still carries older RC-6/RC-7 public status and is recorded as localization/public-documentation debt rather than silently rewritten inside RC-10.
