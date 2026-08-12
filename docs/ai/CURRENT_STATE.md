# Crystal AI Current State

**Status date:** 2026-08-12

GitHub merged `main`, executable tests, exact CI and machine-readable implementation truth are authoritative. Notion is synchronized strategy/history only after successful exact post-merge evidence.

## Runtime / storage truth

- retained runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- retained evidence: Python 3.11/3.12 `2078 passed / 13 skipped / 0 failed`, 9756 statements / 100.00% line coverage;
- signed RC-7 Reader baseline: `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`;
- RC-7 merged via PR #372 from exact validated head `b1cf79594f702194b4dce66ac2ef2546d4154f15`;
- RC-7 exact-head CI `31572324596`: 9/9 successful;
- RC-7 post-merge CI `31572918731`: 9/9 successful;
- RC-8 merged via PR #374; signed RC-9 audited start: `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6`;
- RC-8 exact validated head `a9a4e3b67c514c6c0eece58424c209e9693d3dd7`; exact-head CI `31581756932`: successful;
- RC-8 post-merge CI `31582325275`: successful;
- merge signature for `bd85479e...`: verified / valid;
- current bounded milestone: Reader RC-9 under issue #375;
- SQLite ordinary active local-first;
- PostgreSQL/pgvector inactive target `active=false`;
- normal PostgreSQL runtime adapter / automatic switching absent.

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

RC-1 through RC-7 are merged bounded Reader layers. `dedicated_reader_core=false` remains the larger capability truth. RC-9 does not change this machine marker: it is a bounded PRE-ADMISSION retrieval baseline, not a dedicated autonomous Reader runtime.

- **RC-4** registers caller-supplied, source-linked PRE-ADMISSION proposition candidates with replayable provenance.
- **RC-5** registers explicit same-session/same-exact-source-version relation candidates.
- **RC-6** provides deterministic bounded long-context working sets over current RC-4 leaves and caller-supplied `SUMMARY` artifacts with direct leaf provenance.
- **RC-7** (`core/reader_cross_document.py`) registers explicit caller-supplied cross-document candidate links across at least two different document identities, with exact two-sided provenance and no evidence/identity/Canon authority.
- **RC-9** (`core/reader_lexical_discovery.py`) ranks PRE-ADMISSION Reader proposition snapshots lexically for inspection only; it does not register RC-7 links or adjudicate identity/evidence.

RC-7 relation vocabulary:

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

`CONTRADICTS`, `SAME_TOPIC` and `POSSIBLE_SAME_CLAIM` are symmetric candidates. Optional inspection-basis metadata such as `LEXICAL_SIMILARITY_SIGNAL` and `SHARED_TOPIC_SIGNAL` is descriptive only. RC-7 has no numeric similarity, confidence, identity, winner or evidence-sufficiency authority.

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
```

No Reader layer may mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction winners or gain planner/belief authority.

## RC-8 — post-RC-7 retrieval architecture decision

Issue #373 / PR #374 completed. RC-8 is **architecture/research + truth reconciliation only** and added no Reader retrieval runtime.

Durable decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`.  
Adversarial corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

Post-RC-7 audit identified three real gaps:

1. RC-7 can register a pair but cannot discover promising pairs across a large Reader corpus;
2. Reader lacks a formal adjudication taxonomy separating same proposition, paraphrase, related claim, same topic, possible contradiction and merely similar;
3. Reader lacked a frozen adversarial benchmark proving whether lexical retrieval is insufficient and whether semantic/vector retrieval is worth its added cost and risk.

Crystal already has admitted-memory retrieval modules (`core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py`). Those operate around admitted L3/query paths, whereas RC-4..RC-7 artifacts are PRE-ADMISSION. Existing retrieval code is therefore not automatic authorization to wire semantic/vector ranking into Reader identity.

RC-8 decision:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

RC-8 required the first separately authorized implementation to be a deterministic lexical candidate-discovery baseline + benchmark runner. Semantic/hybrid/vector retrieval remained deferred.

Historical RC-8 compatibility marker retained for the executable documentation contract:

```text
retrieval policy current    = deterministic lexical baseline first; RC-9 implements and measures that baseline; semantic/vector remains deferred
```

## RC-9 — deterministic lexical candidate-discovery baseline

Tracking issue: #375. Architecture/result contract: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Frozen machine-readable result: `eval/reader_rc9_lexical_baseline.json`.

RC-9 adds a stdlib-only, offline, in-memory deterministic BM25 baseline:

```text
RC-4 proposition candidate
→ conservative NFKC/case/whitespace normalization
→ stable lexical tokens
→ deterministic BM25 candidate ranking
→ structured inspection candidates
→ downstream review only
```

The ranker preserves material lexical tokens (including negation, modal/quantifier words, numbers, dates and versions), excludes self matches, defaults to cross-document discovery and uses a stable source/session/candidate tie-break. Result fields contain lexical score/rank/method/matched terms and source linkage, not epistemic verdicts.

Frozen K=5 benchmark over the unchanged 20-case RC-8 corpus:

- useful paired cases: 16;
- hard-negative paired cases: 4;
- Recall@5: **0.937500**;
- Precision@5: **0.187500**;
- MRR: **0.895833**;
- paired hard-negative rate@5: **1.000000**;
- cross-lingual paraphrase `rc8-004` is missed;
- all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives are surfaced in top-5.

Precision@5 uses a fixed `positive paired queries × K` denominator over this synthetic benchmark and is not a fully judged corpus-wide semantic precision claim. The corpus judges the known left/right pair only; these are retrieval metrics, not adjudication accuracy. The measured interpretation is `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. It does not authorize embeddings, semantic/hybrid retrieval, ANN/vector DB, entity/claim identity, contradiction adjudication or Canon/evidence mutation.

## Open backlog boundaries

- **#165** remains exact normalized ingest dedupe/migration for admitted facts; it explicitly excludes near-duplicate / semantic matching. It must not become a Reader semantic-identity oracle.
- **#155** remains the downstream Epistemic Router / Evidence State RFC around FactsPack/TruthGate/Guardian, separate from PRE-ADMISSION Reader discovery.
- **#214** remains PII-fixture/supply-chain hygiene. RC-9 introduces no mandatory dependency or production data surface.

## Localization truth

The immutable historical RC-5 English localization checkpoint remains `51c205fe048fd69d39fcd47b43e042a50de432bc` for validators and phased-source accounting. The unchanged D2 reviewer/safety/privacy/failure source checkpoint remains `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

Russian Reader-dependent public/detail documentation is refreshed through the completed RC-7 localization phase. The eight other localized root README files and Reader-dependent detail packs preserve rich `REFRESH_NEEDED` translations. D2 reviewer/safety translations remain current across all nine supported locales. Quick Start remains current across all nine supported locales.

For compatibility with the immutable D2 localization/source contract, the canonical status phrases remain: **Russian D1/D3/D4/D5 detail pack is current** and **eight other locale detail packs require Reader refresh**. These phrases describe the same current RC-7 localization truth below and do not roll Reader status back to RC-5.

Current RC-7 localization truth is recorded in `docs/TRANSLATION_STATUS.md`: Russian root + Reader-dependent D1/D3/D4/D5 surfaces are `CURRENT` to the immutable RC-7 English source checkpoint `ab3ad31c437647535030e371d58f456faf14017b`; eight other Reader-dependent locale packs remain `REFRESH_NEEDED`; tracked Reader/root debt remains 64 documents.

RC-9 adds English architecture/implementation source material only. Broad translation remains a separate documentation milestone and does not silently change the RC-7 localization freshness ledger.

## Grant truth

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning only; budget change none. RC-0 through RC-9 are existing pre-agreement baseline if merged before any agreement. RC-9 is not an awarded/funded-work claim.

## Next action boundary

Complete issue #375 only: implementation/tests/docs → exact-head CI → review gate → guarded merge → verified main → exact post-merge CI → Notion sync/read-back → completion evidence → close issue → final live audit → STOP.

Do **not** automatically start RC-10, semantic/hybrid retrieval, embeddings, ANN/vector DB, entity resolution, PostgreSQL activation, localization refresh or #155/#165/#214 after RC-9.
