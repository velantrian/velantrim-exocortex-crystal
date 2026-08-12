# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c` / PR #337  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 exact validated head:** `1956cbd45e5a5b794852354ed2233bf1fb6e318f`  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**Current bounded milestone:** RC-10 / issue #377 — architecture/evaluation preregistration only  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | Reader/storage/retrieval artifacts cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented/tested | restore is inactive and never admission |
| Bounded-streaming logical export | Implemented/tested | canonical backend-neutral bundle |
| Inactive PostgreSQL/pgvector import | Implemented/tested | target remains `active=false` |
| Active PostgreSQL runtime adapter | Not implemented | absent from ordinary runtime composition |
| Automatic SQLite/PostgreSQL switching | Forbidden | import/equivalence success is not selection |
| Exact-vs-ANN retrieval evaluation | Not implemented | RC-10 preregisters a bounded future comparison gate; no evaluation is executed |
| Reader Core RC-0 architecture | Documented | normative authority/validation contract |
| Reader Core RC-1 skeleton | Implemented/merged | `core/reader_core.py` |
| Reader Core RC-2 structural map | Implemented/merged | `core/reader_structure.py` |
| Reader Core RC-3 multi-pass mechanics | Implemented/merged | `core/reader_passes.py` |
| Reader Core RC-4 proposition extraction | Implemented/merged | `core/reader_extraction.py` |
| Reader Core RC-5 relation candidates | Implemented/merged | `core/reader_relations.py` |
| Reader Core RC-6 long-context strategy | Implemented/tested/merged | `core/reader_long_context.py` |
| Reader Core RC-7 cross-document candidate links | Implemented/tested/merged | `core/reader_cross_document.py`; PR #372 |
| Reader RC-8 retrieval architecture decision | Completed architecture/research | PR #374; no semantic/vector runtime |
| Reader RC-9 lexical candidate discovery | Implemented/tested/merged bounded baseline | `core/reader_lexical_discovery.py`; PR #376; PRE-ADMISSION inspection only |
| Reader RC-10 reuse/preregistration | In progress architecture/eval contract | issue #377; no comparison execution/runtime |
| Reader semantic/hybrid/vector retrieval | Not implemented | separate future authorization/evidence required |
| Reader SQLite FTS index | Not implemented | future feature-detected scaling option only |
| Dedicated/full Semantic Reading runtime | Not implemented | `dedicated_reader_core=false` |

## Reader implementation chain

```text
SourceVersion + SourceLocator
→ RC-1 ReaderSession
→ RC-2 DocumentStructuralMap
→ RC-3 explicit reading passes
→ RC-4 EXTRACTED_PROPOSITION candidates
   ├─ RC-5 same-source relation candidates
   ├─ RC-6 bounded working sets / caller-supplied SUMMARY
   ├─ RC-7 explicit cross-document candidate links
   └─ RC-9 deterministic lexical candidate discovery → inspection only
→ RC-10 reuse/preregistration contract → no comparison executed
→ explicit downstream review/evidence/admission path
→ Guardian → TruthGate → strict Canon projection
```

RC-8 defined the discovery/identity boundary. RC-9 measured the deterministic lexical baseline. RC-10 freezes reuse constraints and a future comparison gate before any semantic/hybrid result is observed.

## RC-4 through RC-7 retained authority markers

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-5 relation kinds remain `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`. No contradiction winner/evidence admission is implied.

## RC-8 post-RC-7 architecture decision

Durable decision: [READER_RC8_RETRIEVAL_DECISION.md](./architecture/READER_RC8_RETRIEVAL_DECISION.md). Existing admitted-memory retrieval (`core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py`) is a separate authority domain.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

Semantic/hybrid retrieval may be compared later under separately frozen evidence gates; embeddings/ANN/vector do not become Reader authority by reuse.

## RC-9 deterministic lexical candidate-discovery baseline — COMPLETE

Architecture/result: [READER_RC9_LEXICAL_BASELINE.md](./architecture/READER_RC9_LEXICAL_BASELINE.md). Runtime: `core/reader_lexical_discovery.py`. Frozen result: `../eval/reader_rc9_lexical_baseline.json`.

RC-9 is stdlib-only/offline/in-memory deterministic BM25 candidate discovery. It adds no model/provider, FTS/vector schema, network call, public Reader interface, evidence write or RC-7 auto-registration.

Frozen K=5:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. Candidate discovery remains separate from candidate adjudication.

## RC-10 reuse/preregistration — IN PROGRESS

Contract: [READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md](./architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md). Machine-readable preregistration: `../eval/reader_rc10_retrieval_comparison_preregistration.json`.

Reuse disposition:

- `core/rrf.py`: future isolated Reader comparison ordering helper only;
- hashing/trigram embedders: comparator signals only;
- SentenceTransformer: future optional comparator only after separate pinned model/dependency/privacy authorization;
- `get_embedder("auto")`: forbidden for a qualifying preregistered comparison;
- admitted-memory pipeline/query/legacy-retrieval modules: no direct PRE-ADMISSION Reader wiring;
- SQLite FTS: not implemented for Reader;
- PostgreSQL/pgvector: inactive and not authorized.

Frozen future gate: retain RC-9's 15 useful hits, recover `rc8-004` to 16/16 Recall@5, MRR >=0.895833, paired hard-negative hits <=2/4, zero authority violations, exact backend identity, zero query-time network calls, no external source-text transmission.

```text
comparison pass != runtime authorization
```

No semantic/hybrid comparison is executed in RC-10.

## Machine truth

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

No `reader_core_rc9_*` or `reader_core_rc10_*` machine flag is added because neither represents a complete dedicated autonomous Reader runtime.

## Backlog isolation

- #165: exact normalized ingest dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router/Evidence State RFC.
- #214: PII fixture / reproducible supply-chain hygiene.

## Explicit non-features

No automatic Reader parser/chunker/OCR/PDF-layout/multimodal engine, model/provider proposition generation, semantic/hybrid/vector Reader runtime, automatic semantic identity/entity resolution, contradiction winner, planner/belief-update authority, evidence/Canon/ESM mutation, durable Reader retrieval schema, public Reader API/CLI/worker, active PostgreSQL runtime selection or dedicated/full autonomous Reader exists.

## Localization

Russian root + Reader-dependent D1/D3/D4/D5 surfaces remain `CURRENT` at immutable RC-7 English source checkpoint `ab3ad31c437647535030e371d58f456faf14017b`; eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, 64 tracked documents. RC-8 through RC-10 add English source meaning only; broad localization remains separate.

## Grant truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning only; budget change none. Pre-agreement merged work is existing baseline, not awarded delivery.
