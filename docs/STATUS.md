# Velantrim Crystal — Current Status

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Signed RC-7 Reader baseline:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 exact validated head:** `b1cf79594f702194b4dce66ac2ef2546d4154f15`  
**RC-7 exact-head CI:** `31572324596` — 9/9 successful  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge / RC-9 audited start:** `bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact validated head:** `a9a4e3b67c514c6c0eece58424c209e9693d3dd7`  
**RC-8 exact-head CI:** `31581756932` — successful  
**RC-8 post-merge CI:** `31582325275` — successful  
**Current bounded milestone:** issue #375 — RC-9 deterministic lexical candidate discovery baseline

## Verification

Historical retained runtime evidence remains:

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- PostgreSQL integration CI `31256316532` successful against PostgreSQL 16 + pgvector 0.8.2.

Later Reader milestones carry their own exact-head/post-merge evidence rather than rewriting that historical runtime checkpoint. RC-7 and RC-8 are fully merged; the RC-9 audited starting commit signature is verified / valid.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

The PostgreSQL target is not registered for ordinary runtime reads/writes. Automatic backend switching, cutover and rollback are absent.

## Reader Core bounded implementation

RC-0 is normative architecture. RC-1 through RC-7 are merged bounded runtime/domain milestones. RC-8 is the completed retrieval architecture/research decision. RC-9 is the bounded PRE-ADMISSION lexical candidate-discovery implementation baseline.

```text
RC-1 → SourceVersion / SourceLocator / ReaderSession / fidelity / coverage
RC-2 → caller-supplied version-bound Structural Document Map
RC-3 → explicit deterministic multi-pass ledger and substantive outcomes
RC-4 → source-linked EXTRACTED_PROPOSITION candidates
RC-5 → same-session/same-version explicit relation candidates
RC-6 → bounded long-context working sets + caller-supplied SUMMARY
RC-7 → explicit cross-document candidate links with exact two-sided provenance
RC-8 → architecture/research decision about discovery/identity/retrieval evaluation
RC-9 → deterministic lexical candidate discovery + benchmark; inspection only
```

Machine implementation truth:

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

RC-9 does not change `dedicated_reader_core=false`; it is not a full autonomous Reader runtime flag.

### RC-4 boundary

RC-4 accepts caller-supplied normalized propositions only when anchored to a `COMPLETED` RC-3 pass and current matching `PROCESSED` / `REVISITED` coverage. `FACTUAL_ASSERTION` records source presentation, not Crystal verification.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

### RC-5 boundary

Runtime: `core/reader_relations.py`.

`ReaderRelationRegistry` accepts current registered RC-4 IDs from one OPEN ReaderSession / exact SourceVersion and registers `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` with exact two-sided provenance and rationale.

```text
reader_core_rc5_relation_candidates = true
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

No contradiction resolution/winner selection or evidence admission is performed.

### RC-6 boundary

Runtime: `core/reader_long_context.py`.

RC-6 builds deterministic bounded working sets over current RC-4 leaves, carries only already in-set RC-5 relation context, and permits caller-supplied `SourceFidelity.SUMMARY` artifacts with direct leaf provenance.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

### RC-7 boundary

Runtime: `core/reader_cross_document.py`.

`ReaderCrossDocumentRegistry` requires explicit RC-4 extractors covering at least two different document identities. Each link names current registered RC-4 candidates from different documents and revalidates source/session/pass/structure/coverage/provenance before registration.

Candidate kinds:

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

Optional inspection basis is descriptive only. RC-7 provides no numeric similarity, evidence sufficiency, identity, winner or Canon authority.

```text
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## RC-8 architecture decision

Issue #373 / PR #374 completed. Durable decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Synthetic adversarial corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

The audit found that RC-7 can **register** explicit pairs but does not **discover** useful pairs across a corpus. Reader also lacked an evaluation taxonomy separating:

- same proposition candidate;
- paraphrase candidate;
- related claim;
- same topic;
- possible contradiction;
- merely similar.

Crystal already has admitted-memory/query retrieval machinery in `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py` and `core/rrf.py`. That machinery belongs to a different authority domain from PRE-ADMISSION Reader artifacts and is not directly wired into Reader by RC-8 or RC-9.

RC-8 decision:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

RC-8 required a deterministic lexical candidate-discovery baseline and benchmark runner before any separately authorized semantic/vector comparison.

## RC-9 deterministic lexical baseline

Runtime: `core/reader_lexical_discovery.py`. Benchmark runner: `scripts/bench_reader_rc9_lexical.py`. Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Frozen result: `eval/reader_rc9_lexical_baseline.json`.

RC-9 snapshots the public RC-4 proposition surface into retrieval-only records and performs conservative NFKC/case/whitespace normalization plus stable tokenization and deterministic in-memory BM25 ranking. It preserves material lexical tokens and carries source/document/privacy linkage into structured inspection candidates.

It does not emit RC-8 review classes, automatically register RC-7 relations, write evidence, mutate ESM/TruthGate/Guardian/Canon, call semantic/vector retrieval, add a network dependency, add a Reader persistence schema or activate PostgreSQL/pgvector.

Frozen K=5 result:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.217391 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

The baseline misses the cross-lingual paraphrase and surfaces all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives within top-5. The measured architecture classification is `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

That classification is retrieval evidence only. It does **not** authorize semantic/hybrid retrieval, embeddings, ANN/vector DB, identity inference or adjudication.

## Backlog boundaries

- #165: exact normalized ingest dedupe/migration only; explicitly not semantic matching. Separate from Reader semantic identity.
- #155: downstream Epistemic Router / Evidence State RFC. Separate from PRE-ADMISSION Reader candidate discovery.
- #214: fixture/PII/supply-chain hygiene. RC-9 adds no mandatory dependency or production data surface.

## Authority boundary

```text
physical L3            = multi-status storage
strict Canon           = trusted read projection
Reader artifact        = source-linked pre-admission/process state
Reader relation        = relation candidate
Reader working set     = bounded context snapshot
Reader SUMMARY         = caller-supplied synthesis candidate
Reader cross-doc link  = explicit comparison candidate
retrieval candidate    = item proposed for inspection
successful import      != backend activation
```

Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. RC-9 grants no evidence/truth/Canon/planner authority. Public `HTTP /ask`, `CLI ask` and `MCP search` remain admitted-memory read-only query surfaces and are not RC-9 interfaces.

## Localization truth

Russian root + Reader-dependent D1/D3/D4/D5 surfaces are `CURRENT` to the immutable RC-7 English source checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED` translations — **64 tracked documents**. D2 reviewer/safety and Quick Start remain current across all nine supported locales.

RC-9 adds English architecture/implementation source material only; it does not silently mark the eight locale packs current and does not rewrite the RC-7 localization checkpoint.

## Grant status

NLnet is **submitted / under review / not awarded**. Approximate **€50,000** is planning only, not an approved budget/payment commitment. **Budget change: none.** RC-0 through RC-9 are existing pre-agreement baseline if merged before an agreement; RC-9 is not evidence of funded delivery.

## Still absent after RC-9

- durable/corpus-scale Reader lexical index;
- SQLite FTS Reader index;
- semantic/hybrid/vector Reader retrieval implementation or accepted semantic thresholds;
- ANN/vector Reader index;
- automatic semantic identity/equivalence/entity resolution/deduplication;
- automatic Reader parser/OCR/multimodal/model-provider generation;
- automatic evidence admission or contradiction winner selection;
- planner/autonomous research/belief-update authority;
- active PostgreSQL read/write runtime selection, automatic switching/cutover/rollback;
- dedicated/full autonomous Semantic Reading runtime.

## Completion boundary

Issue #375 is complete only after exact-head CI, review gate, guarded merge to verified `main`, post-merge CI, synchronization/read-back of the three existing Crystal Notion pages, completion evidence and issue closure. No next Reader milestone starts automatically; after closure, STOP.