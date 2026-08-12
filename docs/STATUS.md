# Velantrim Crystal — Current Status

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**RC-7 signed merge:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**RC-8 signed merge / RC-9 audited start:** `bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head CI:** `31581756932` — successful  
**RC-8 post-merge CI:** `31582325275` — successful  
**Current bounded milestone:** issue #375 — Reader RC-9 deterministic lexical candidate discovery baseline

## Verification

Historical retained runtime evidence remains Python 3.11/3.12 **2078 passed / 13 skipped / 0 failed**, **9756 statements / 100.00% line coverage**, 7/7 declared Ring Zero mutants killed and 9/9 permanent CI jobs successful. Later Reader milestones carry their own exact-head/post-merge evidence.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

No Reader RC-9 change activates PostgreSQL, pgvector, automatic backend switching, cutover or rollback.

## Reader Core bounded implementation

RC-0 is normative architecture. RC-1 through RC-7 are merged bounded Reader layers; RC-8 is the completed retrieval architecture decision; RC-9 is the bounded PRE-ADMISSION lexical discovery implementation baseline.

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

RC-5 remains `core/reader_relations.py` with `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`; `relation candidate != admitted evidence` and `contradiction candidate != confirmed contradiction` remain unchanged.

RC-7 remains `core/reader_cross_document.py` and preserves:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## RC-9 lexical discovery baseline

Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Runtime: `core/reader_lexical_discovery.py`. Benchmark runner: `scripts/bench_reader_rc9_lexical.py`. Frozen output: `eval/reader_rc9_lexical_baseline.json`.

RC-9 snapshots already extracted RC-4 propositions into a retrieval-only record, performs conservative NFKC/case/whitespace normalization, preserves material lexical tokens, builds a deterministic in-memory BM25 representation and returns auditable top-K inspection candidates with lexical score, rank, method/version, matched terms and source/document linkage.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

No automatic review class, evidence admission, TruthGate/Guardian/Canon mutation, claim merge or RC-7 relation registration is performed.

### Frozen K=5 result

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.217391 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

The cross-lingual paraphrase is missed and all four paired hard negatives are surfaced within top-5. The measured classification is `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`; this does not authorize semantic/vector machinery.

## Authority boundary

```text
physical L3            = multi-status storage
strict Canon           = trusted read projection
Reader artifact        = source-linked pre-admission/process state
Reader relation        = relation candidate
Reader cross-doc link  = explicit comparison candidate
retrieval candidate    = item proposed for inspection
successful import      != backend activation
```

Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. Public `HTTP /ask`, `CLI ask` and `MCP search` remain read-only admitted-memory/query surfaces and are not wired to RC-9.

## Localization / grant / backlog

Russian Reader-dependent RC-7 surfaces remain current; eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, 64 documents. RC-9 does not perform the localization refresh.

NLnet is **submitted / under review / not awarded**. Approximate €50,000 is planning only; budget change none. RC-9 is not funded-delivery evidence.

Issues #155, #165 and #214 remain separate.

## Still absent after RC-9

- semantic/hybrid Reader retrieval;
- Reader embeddings or sentence-transformers;
- ANN / FAISS / HNSW / vector DB;
- PostgreSQL/pgvector Reader activation;
- durable Reader retrieval schema/index;
- automatic entity resolution / claim identity / contradiction adjudication;
- automatic evidence admission or Canon linking;
- public Reader retrieval API/CLI/background worker;
- dedicated/full autonomous Semantic Reading runtime.

## Completion boundary

Issue #375 is complete only after exact-head CI, review gate, guarded merge to signed/verified `main`, exact post-merge CI, synchronization/read-back of the three existing Crystal Notion pages, completion evidence and issue closure. Then STOP; no next Reader milestone starts automatically.
