# Velantrim Crystal — Current Status

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Signed RC-7 Reader baseline:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge / RC-9 audited start:** `bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Signed RC-9 merge:** `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 exact validated head:** `1956cbd45e5a5b794852354ed2233bf1fb6e318f`  
**RC-9 exact-head CI:** `31593097846` — 9/9 successful  
**RC-9 post-merge CI:** `31594027040` — 9/9 successful  
**Current bounded milestone:** issue #377 — RC-10 retrieval reuse compatibility + comparison pre-registration

## Verification

Current RC-9 merge signature is `verified=true`, reason `valid`. Both Python 3.11 and 3.12 passed the repository 100% coverage gate on exact-head and post-merge CI. Ring Zero, code-quality, security, eval, JSONL-integrity, Docker and docs-status were green.

Historical retained runtime evidence remains 2078 passed / 13 skipped / 0 failed, 9756 statements / 100.00% coverage at `bbd816c...`; later Reader milestones carry their own exact evidence instead of rewriting that historical checkpoint.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

The PostgreSQL target is not registered for ordinary runtime reads/writes. Automatic backend switching, cutover and rollback are absent. RC-10 adds no storage/index schema.

## Reader Core bounded implementation

RC-0 is normative architecture. RC-1 through RC-7 are merged bounded runtime/domain milestones. RC-8 is the completed retrieval architecture/research decision. RC-9 is the completed bounded PRE-ADMISSION lexical candidate-discovery implementation baseline. RC-10 is architecture/evaluation pre-registration only.

```text
RC-1 → SourceVersion / SourceLocator / ReaderSession / fidelity / coverage
RC-2 → caller-supplied version-bound Structural Document Map
RC-3 → explicit deterministic multi-pass ledger and substantive outcomes
RC-4 → source-linked EXTRACTED_PROPOSITION candidates
RC-5 → same-session/same-version explicit relation candidates
RC-6 → bounded long-context working sets + caller-supplied SUMMARY
RC-7 → explicit cross-document candidate links with exact two-sided provenance
RC-8 → discovery/identity/retrieval architecture decision
RC-9 → deterministic lexical candidate discovery + benchmark; inspection only
RC-10 → existing-retrieval reuse matrix + frozen future comparison gate; no comparison run
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

RC-8/RC-9/RC-10 do not turn `dedicated_reader_core` true and do not create a complete autonomous Reader machine flag.

### RC-4 boundary

RC-4 accepts caller-supplied normalized propositions only when anchored to a completed substantive RC-3 pass and matching provenance.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

### RC-5 boundary

Runtime: `core/reader_relations.py`.

Relation candidates are `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` over valid registered RC-4 candidates inside one OPEN ReaderSession and exact SourceVersion.

```text
reader_core_rc5_relation_candidates = true
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

### RC-6 boundary

Runtime: `core/reader_long_context.py`.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

### RC-7 boundary

Runtime: `core/reader_cross_document.py`.

Candidate kinds remain `SUPPORTS`, `CONTRADICTS`, `ELABORATES`, `REFERENCES`, `DEFINES`, `EXAMPLE_OF`, `PREREQUISITE_FOR`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`.

```text
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 provides no automatic semantic matching, identity, evidence sufficiency, contradiction winner or Canon authority.

## RC-8 architecture decision

Issue #373 / PR #374 completed. Durable decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

Crystal already had admitted-memory/query retrieval machinery in `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py` and `core/rrf.py`. That machinery is a different authority domain from PRE-ADMISSION Reader artifacts.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

RC-8 required deterministic lexical candidate discovery before any separately authorized semantic/vector comparison. Semantic/hybrid retrieval may be compared later only under a separately frozen gate.

## RC-9 deterministic lexical baseline — COMPLETE

Runtime: `core/reader_lexical_discovery.py`. Runner: `scripts/bench_reader_rc9_lexical.py`. Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Frozen result: `eval/reader_rc9_lexical_baseline.json`.

RC-9 snapshots the public RC-4 proposition surface into retrieval-only records and performs conservative NFKC/case/whitespace normalization plus stable tokenization and deterministic in-memory BM25 ranking. It adds no network/model dependency, FTS/vector schema, public Reader API or authority mutation.

Frozen K=5 result:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

The measured architecture classification is `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. Candidate discovery is not candidate adjudication. The cross-lingual paraphrase `rc8-004` is missed and all four paired hard negatives surface at K=5.

## RC-10 reuse compatibility + comparison pre-registration — IN PROGRESS

Tracking: issue #377. Contract: `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`. Machine-readable gate: `eval/reader_rc10_retrieval_comparison_preregistration.json`.

Audit disposition:

- `core/rrf.py` may be reused only as pure candidate ordering in a future isolated comparison;
- existing hashing/trigram embedders are comparison signals only;
- SentenceTransformer remains a future optional comparator requiring separate pinned dependency/model/privacy authorization;
- `get_embedder("auto")` is forbidden for preregistered Reader comparison;
- admitted-memory `core/pipeline.py`, `core/query_pipeline.py`, `core/legacy_retrieval.py` are not direct Reader pipelines/backends;
- SQLite FTS is not currently implemented for Reader and remains a future feature-detected scaling option;
- PostgreSQL/pgvector remains inactive and unauthorized for Reader.

Future comparison minimum gate is frozen before results: retain 15 RC-9 useful hits, recover `rc8-004` to 16/16 / Recall@5 1.0, MRR >=0.895833, paired hard-negative hits <=2/4, zero authority violations, exact backend identity, no auto backend selection, zero query-time network calls and no external Reader source-text transmission.

```text
comparison pass != runtime authorization
```

RC-10 executes no semantic/hybrid comparison.

## Backlog boundaries

- #165: exact normalized admitted-fact dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router / Evidence State RFC.
- #214: fixture/PII/supply-chain hygiene.

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
comparison pass        != runtime authorization
```

Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. Public `HTTP /ask`, `CLI ask` and `MCP search` remain admitted-memory read-only query surfaces, not Reader RC-9/RC-10 interfaces.

## Localization truth

Russian root + Reader-dependent D1/D3/D4/D5 surfaces remain `CURRENT` to the immutable RC-7 English checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED` translations — 64 tracked documents. D2 and Quick Start remain current across all nine locales.

RC-8 through RC-10 add English source meaning only; broad localization remains separate. The English root README still has older RC-6/RC-7 status text and is recorded as public documentation drift for a dedicated public/localization reconciliation rather than silently rewritten here.

## Grant status

NLnet is **submitted / under review / not awarded**. Approximate **€50,000** is planning only; budget change none. Work merged before an agreement is existing baseline and cannot be counted again as future funded delivery.

## Completion boundary

Issue #377 is complete only after exact-head CI, review gate, guarded merge to verified `main`, post-merge CI, synchronization/read-back of the three existing Crystal Notion pages, completion evidence and issue closure. No semantic/hybrid comparison or later Reader milestone starts automatically.
