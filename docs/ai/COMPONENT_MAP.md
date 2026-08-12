# 🗺️ Crystal Component Map for Agents

Use this map to choose the smallest relevant inspection surface. Paths are starting points, not substitutes for consumer and test discovery.

## 1. Claims, epistemic lifecycle and physical L3

**Start:** `core/memory.py`, `core/l3_graph.py`, `core/truth_gate.py`, `docs/CLAIM_METADATA_GLOSSARY.md`.

**Boundary:** storage presence does not equal strict Canon membership. Writes must preserve state, evidence, restrictions and the canonical admission path.

## 2. Durable backend identity

**Start:** `core/backend_profiles.py`, `core/_registry.py`, `core/l3_graph.py`, `core/doctor.py`, `docs/architecture/DURABLE_STORAGE_PROFILE.md`.

The versioned profile locks ordinary deployment identity. Backend availability, package installation, locator changes or profile deletion cannot silently select another store.

## 3. SQLite lifecycle and logical portability

**Start:** `core/storage_common.py`, `core/storage_backup.py`, `core/storage_restore.py`, `core/storage_lock.py`, `core/storage_migration.py`, `core/storage_ops.py`.

```text
SQLite backup → verify → inactive restore
SQLite profile → bounded canonical bundle → independent verification
```

Migration evidence does not grant epistemic authority.

## 4. PostgreSQL inactive migration target

**Start:** `core/postgresql_migration.py`, `core/postgresql_migration_impl.py`, `core/storage_ops.py`, `docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md`, `docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md`, PostgreSQL integration tests/workflow.

Current verified target remains `active=false`, absent from ordinary runtime composition. No cutover, rollback, dual-write, automatic switching or ANN acceptance is implied.

## 5. Truth admission and safety

**Start:** Guardian functions in `core/pipeline.py`, `core/truth_gate.py`, `core/immune.py`, `core/api_ingest_policy.py`, `docs/IMMUNE_LAYER.md`, `docs/ARCHITECTURE.md`.

A caller, model, retriever, storage profile, migration tool or Reader artifact must not mutate strict Canon outside the audited admission path.

## 6. Strict read grounding

**Start:** `core/canonical_view.py`, `core/trust_snapshot.py`, public handlers in `core/api.py`, `core/cli.py`, MCP surfaces, `core/query_pipeline.py`.

Public query/search paths are read-only. Restrictions remain deny-dominant and physical L3 must not be presented as strict Canon.

## 7. Admitted-memory retrieval

**Start:**

- `core/embedding.py` — hashing/trigram hashing and optional SentenceTransformer embedding abstraction;
- `core/legacy_retrieval.py` — bounded lexical fallback for legacy/uninitialised L3 stores;
- `core/retrieval_config.py` — bounded admitted-memory retrieval knobs;
- `core/query_pipeline.py` — canonical read-only query path;
- `core/rrf.py` — rank fusion helper;
- `core/pipeline.py` — admitted-memory retrieval/grounding path.

**Authority boundary:** these modules operate around admitted L3/query state. Retrieval rank, similarity and model output are not evidence or admission.

```text
retrieval rank != truth
similarity != identity
ranking != epistemic authority
```

Do not wire these modules directly into Reader identity simply because they already exist.

## 8. Reader proposition extraction and same-document relations

**Start:** `core/reader_extraction.py`, `core/reader_relations.py`, corresponding tests.

- RC-4 creates PRE-ADMISSION `EXTRACTED_PROPOSITION` candidates with replayable provenance.
- RC-5 registers explicit relation candidates inside one OPEN Reader session / exact SourceVersion.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

## 9. Reader long context

**Start:** `core/reader_long_context.py`, `tests/test_reader_long_context.py`.

RC-6 groups current valid RC-4 leaves into deterministic bounded working sets and may register caller-supplied `SUMMARY` artifacts with direct leaf provenance.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

## 10. Reader cross-document candidate links

**Start:** `core/reader_cross_document.py`, `tests/test_reader_cross_document.py`.

RC-7 is merged under PR #372. `ReaderCrossDocumentRegistry` accepts explicit caller-selected RC-4 candidates from different document identities, revalidates both provenance chains and records an explicit cross-document relation candidate.

Relation vocabulary:

```text
SUPPORTS / CONTRADICTS / ELABORATES / REFERENCES / DEFINES
EXAMPLE_OF / PREREQUISITE_FOR / SAME_TOPIC / POSSIBLE_SAME_CLAIM
```

Optional `LEXICAL_SIMILARITY_SIGNAL` or `SHARED_TOPIC_SIGNAL` metadata is descriptive only.

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## 11. RC-8 post-RC-7 retrieval architecture decision

Historical RC-8 contract label: **Post-RC-7 retrieval architecture decision (RC-8)**. That milestone is completed; RC-9 is the current bounded implementation baseline.

**Start:**

- `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`;
- `eval/reader_rc8_retrieval_adversarial.jsonl`;
- `tests/test_reader_rc8_retrieval_architecture.py`;
- issue #373 / PR #374.

RC-8 is a completed architecture/research milestone. It identifies the missing capability as **candidate discovery across a Reader corpus**, not a vector database.

It separates:

```text
candidate discovery → proposes pairs worth inspection
candidate adjudication → decides review class under explicit constraints
admission/evidence → separate downstream authority path
```

Review classes defined by RC-8:

- `SAME_PROPOSITION_CANDIDATE`;
- `PARAPHRASE_CANDIDATE`;
- `RELATED_CLAIM`;
- `SAME_TOPIC`;
- `POSSIBLE_CONTRADICTION`;
- `MERELY_SIMILAR`.

RC-8 required the first separately authorized implementation baseline to be deterministic lexical candidate discovery + a benchmark runner. Hybrid/neural/vector/ANN work remained deferred. PostgreSQL/pgvector remains inactive `active=false`.

```text
retrieval match != evidence
similarity != identity
repetition != corroboration
cross-document candidate != Canon relation
ranking != epistemic authority
candidate discovery != candidate adjudication
```

## 12. RC-9 deterministic lexical candidate discovery

**Start:**

- `core/reader_lexical_discovery.py`;
- `scripts/bench_reader_rc9_lexical.py`;
- `tests/test_reader_lexical_discovery.py`;
- `tests/test_bench_reader_rc9_lexical.py`;
- `tests/test_reader_rc9_status.py`;
- `eval/reader_rc9_lexical_baseline.json`;
- `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`;
- issue #375.

RC-9 snapshots the public RC-4 proposition surface into retrieval-only records, applies conservative NFKC/case/whitespace normalization and stable tokenization, then performs deterministic in-memory BM25 ranking. Self matches are excluded; cross-document filtering is default; ties use stable source/session/candidate ordering.

`ReaderLexicalMatch` exposes only retrieval and provenance metadata: identifiers, lexical score, rank, method/version, matched terms and privacy metadata. It does not output RC-8 review classes or any identity/evidence/Canon verdict.

Frozen K=5 result: Recall 0.937500; Precision 0.217391; MRR 0.895833; paired hard-negative rate 1.000000. The cross-lingual pair is missed and all four paired hard negatives are surfaced within top-5. Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

That classification does not authorize embeddings, semantic/hybrid retrieval, ANN/vector DB, entity/claim identity or adjudication.

## 13. Contradictions and curator decisions

**Start:** contradiction modules, `core/review.py`, `core/conflict_surfaces.py`, `docs/CONTRADICTION_POLICY.md`.

Detection does not select a winner. `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` require explicit authorized decisions. RC-5/RC-7 candidates and RC-9 retrieval candidates may expose conflict-relevant state, but cannot resolve a `ContradictionReport` or select a canonical winner.

## 14. Imports and review queues

**Start:** import/session modules, review queue/session modules and their CLI/HTTP tests.

Partial imports must remain distinguishable from admission. Unreviewed content cannot ground strict answers. Reader RC-4..RC-9 artifacts remain upstream of the normal ingest/review/evidence path.

## 15. Public surfaces and runtime composition

**Start:** `core/api.py`, `core/cli.py`, `core/doctor.py`, MCP modules, `Dockerfile`, `pyproject.toml`, `.github/workflows/ci.yml`.

Reader RC-1 through RC-9 add no public Reader API, CLI, background worker or ordinary runtime-composition wiring. RC-9 adds no mandatory runtime dependency or persistent index.

## 16. Evaluation and status evidence

**Start:** `docs/EVAL.md`, `TEST_REPORT.md`, `docs/status/implementation-manifest.json`, evaluation fixtures, Ring Zero and benchmark workflows.

Always bind implementation claims to exact commit/head/CI. RC-9’s 20-case synthetic result is a retrieval baseline, not production retrieval-quality or semantic-adjudication certification.

## 17. Reader architecture chain

**Start:**

- `core/reader_core.py`, `tests/test_reader_core.py` — RC-1;
- `core/reader_structure.py`, `tests/test_reader_structure.py` — RC-2;
- `core/reader_passes.py`, `tests/test_reader_passes.py` — RC-3;
- `core/reader_extraction.py`, `tests/test_reader_extraction.py` — RC-4;
- `core/reader_relations.py`, `tests/test_reader_relations.py` — RC-5;
- `core/reader_long_context.py`, `tests/test_reader_long_context.py` — RC-6;
- `core/reader_cross_document.py`, `tests/test_reader_cross_document.py` — RC-7;
- `core/reader_lexical_discovery.py`, `tests/test_reader_lexical_discovery.py` — RC-9;
- `docs/architecture/READER_CORE_ARCHITECTURE.md` — normative RC-0 contract;
- `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md` — post-RC-7 decision;
- `docs/architecture/READER_RC9_LEXICAL_BASELINE.md` — RC-9 measured baseline.

Machine implementation truth:

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

**Current non-features:** no automatic Reader parser/semantic chunker/OCR/PDF-layout/multimodal engine, no automatic NLP/LLM/provider Reader extraction or summarization, no semantic/hybrid/vector Reader retrieval, no automatic semantic equivalence/entity resolution, no durable Reader retrieval schema/migration and no dedicated/full autonomous Reader runtime.

## 18. Documentation, grant and research governance

**Start:** `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`.

GitHub `main` proves implementation. Notion preserves deeper rationale/strategy/history after exact post-merge evidence. NLnet remains `submitted / under review / not awarded`. RC-9 is a bounded pre-agreement lexical retrieval baseline, not funded semantic retrieval. Issues #155, #165 and #214 remain separate scopes.