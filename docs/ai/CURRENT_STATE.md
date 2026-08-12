# Crystal AI Current State

**Status date:** 2026-08-12

GitHub merged `main`, executable tests, exact CI and machine-readable implementation truth are authoritative. Notion is synchronized strategy/history only after successful exact post-merge evidence.

## Current verified Reader checkpoint

- signed authoritative Reader main: `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`;
- merge signature: `verified=true`, reason `valid`;
- Reader RC-9 merged by PR #376 from exact validated head `1956cbd45e5a5b794852354ed2233bf1fb6e318f`;
- RC-9 exact-head CI `31593097846`: 9/9 successful;
- RC-9 post-merge push CI `31594027040`: 9/9 successful;
- issue #375: closed / completed;
- current bounded milestone: **Reader RC-10 architecture/evaluation pre-registration under issue #377**;
- RC-10 executes no semantic/hybrid comparison and adds no retrieval runtime.

Historical compatibility evidence remains:

- retained runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- signed RC-7 Reader baseline: `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`;
- RC-7 post-merge CI `31572918731`: 9/9 successful;
- signed RC-8 merge / RC-9 audited start: `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374;
- RC-8 exact-head / post-merge CI: `31581756932` / `31582325275` successful.

## Runtime / storage truth

- SQLite ordinary active local-first;
- PostgreSQL/pgvector inactive target `active=false`;
- normal PostgreSQL runtime adapter / automatic switching absent;
- RC-10 adds no SQLite FTS schema, vector index, network service or model dependency.

## Reader implementation truth

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

RC-1 through RC-7 are merged bounded Reader layers. `dedicated_reader_core=false` remains the larger capability truth. RC-8, RC-9 and RC-10 do not create a full autonomous Reader machine flag.

- **RC-4** registers caller-supplied, source-linked PRE-ADMISSION proposition candidates with replayable provenance.
- **RC-5** (`core/reader_relations.py`) registers explicit same-session / same-exact-source-version relation candidates: `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`.
- **RC-6** provides deterministic bounded long-context working sets and caller-supplied `SUMMARY` artifacts with direct RC-4 leaf provenance.
- **RC-7** (`core/reader_cross_document.py`) registers explicit caller-selected cross-document candidate links with exact two-sided provenance.
- **RC-9** (`core/reader_lexical_discovery.py`) ranks PRE-ADMISSION Reader proposition snapshots lexically for inspection only; it does not register RC-7 links or adjudicate identity/evidence.
- **RC-10** documents reuse compatibility and freezes comparison gates only; no comparator is executed in this milestone.

RC-7 relation vocabulary remains:

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

Authority invariants remain:

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
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
retrieval match != evidence
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

No Reader layer may mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction winners or gain planner/belief authority.

## RC-8 — post-RC-7 retrieval architecture decision

Issue #373 / PR #374 completed. Durable decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Adversarial corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

RC-8 found the corpus candidate-discovery gap and distinguished admitted-memory retrieval from PRE-ADMISSION Reader artifacts. Historical executable marker retained:

```text
retrieval policy current    = deterministic lexical baseline first; RC-9 implements and measures that baseline; semantic/vector remains deferred
```

Existing admitted-memory retrieval modules are `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py` and retrieval composition in `core/pipeline.py`. Existing retrieval code is not automatic Reader identity authority.

## RC-9 — deterministic lexical candidate-discovery baseline: COMPLETE

Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Frozen result: `eval/reader_rc9_lexical_baseline.json`.

RC-9 uses stdlib-only, offline, in-memory deterministic BM25 over conservative NFKC/case/whitespace normalized proposition snapshots. Self matches are excluded; cross-document filtering is default; result fields contain retrieval/provenance metadata only.

Frozen K=5 result:

- useful paired cases: 16;
- hard-negative paired cases: 4;
- Recall@5: **0.937500**;
- Precision@5: **0.187500**;
- MRR: **0.895833**;
- paired hard-negative rate@5: **1.000000**;
- useful paired hits: 15/16;
- hard-negative paired hits: 4/4;
- cross-lingual paraphrase `rc8-004` is missed.

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. These are candidate discovery metrics, not candidate adjudication or identity accuracy.

## RC-10 — existing retrieval reuse compatibility + pre-registration: IN PROGRESS

Tracking issue: #377. Contract: `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`. Machine-readable preregistration: `eval/reader_rc10_retrieval_comparison_preregistration.json`.

Dedup audit conclusion:

- `core/rrf.py` is a pure ordering helper potentially reusable in a future isolated Reader comparison;
- deterministic hashing/trigram embedders are comparison signals only, not Reader-safe semantic/identity contracts;
- optional SentenceTransformer remains a future comparator requiring separate pinned-model/dependency/privacy authorization;
- `get_embedder("auto")` is forbidden for a preregistered Reader comparison;
- `core/pipeline.py`, `core/query_pipeline.py` and `core/legacy_retrieval.py` must not be wired directly into PRE-ADMISSION Reader because their callers/data lifecycle belong to admitted memory;
- SQLite FTS is documented as a future scaling option but no Reader FTS runtime was found on the audited main;
- PostgreSQL/pgvector remains inactive `active=false`.

RC-10 freezes a future gate before results are observed: recover `rc8-004`, retain all 15 prior useful hits, reach 16/16 Recall@5, keep MRR >= 0.895833, reduce paired hard-negative hits to <=2/4, record exact backend identity, use zero query-time network calls and preserve zero authority violations. Passing that gate means only `ELIGIBLE_FOR_STRONGER_EVALUATION_AND_ARCHITECTURE_REVIEW_ONLY`.

## Open backlog boundaries

- **#165** remains exact normalized ingest dedupe/migration for admitted facts; it explicitly excludes near-duplicate / semantic matching.
- **#155** remains downstream Epistemic Router / Evidence State RFC around FactsPack/TruthGate/Guardian.
- **#214** remains PII-fixture/supply-chain hygiene.

## Localization truth

The immutable historical D1/D3/D4/D5 source checkpoint `51c205fe048fd69d39fcd47b43e042a50de432bc` remains required by the executable phased localization contract. Russian Reader-dependent public/detail documentation is refreshed through RC-7. The eight other localized root README files and Reader-dependent detail packs remain `REFRESH_NEEDED`; tracked debt remains 64 documents. D2 and Quick Start remain current across all nine supported locales.

RC-8/RC-9/RC-10 add English architecture/status meaning only. Broad localization is separate. The root English `README.md` still contains an older RC-6/RC-7 public checkpoint; RC-10 records this as public documentation drift rather than silently rewriting all localized README surfaces in an architecture milestone.

## Grant truth

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning only; budget change none. Work merged before any agreement is existing baseline and cannot be counted again as future funded delivery.

## Next action boundary

Complete only issue #377: architecture/eval contract + truth reconciliation → exact-head CI → review gate → guarded merge → verified main → exact post-merge CI → Notion sync/read-back → completion evidence → close issue → STOP.

Do **not** automatically execute semantic/hybrid comparison, add embeddings/ANN/vector DB, implement FTS, activate PostgreSQL/pgvector, perform automatic entity/claim identity, start broad localization, or absorb #155/#165/#214.
