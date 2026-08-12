# Crystal AI Current State

**Status date:** 2026-08-12

GitHub merged `main`, executable tests, exact CI and machine-readable implementation truth are authoritative. Notion is synchronized strategy/history only after successful exact post-merge evidence.

## Runtime / storage truth

- retained runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- retained evidence: Python 3.11/3.12 `2078 passed / 13 skipped / 0 failed`, 9756 statements / 100.00% line coverage;
- RC-7 signed merge: `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, PR #372, post-merge CI `31572918731` 9/9;
- RC-8 signed merge / RC-9 audited start: `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6`, PR #374;
- RC-8 exact-head CI `31581756932` and post-merge CI `31582325275` completed successfully;
- current bounded milestone: Reader RC-9, tracking issue #375;
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

RC-1 through RC-7 are merged bounded Reader layers. `dedicated_reader_core=false` remains the larger capability truth. RC-9 does not change that marker: it is a bounded PRE-ADMISSION discovery baseline, not a dedicated autonomous Reader runtime.

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
retrieval match != evidence
ranking != epistemic authority
candidate discovery != candidate adjudication
```

No Reader layer may mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction winners or gain planner/belief authority.

## RC-8 — retrieval decision, completed predecessor

RC-8 is the durable architecture decision in `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`; its frozen 20-case corpus is `eval/reader_rc8_retrieval_adversarial.jsonl`. It established that existing admitted-memory retrieval (`core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py`) is a different authority domain from PRE-ADMISSION Reader artifacts and authorized only a separately bounded deterministic lexical baseline first.

## RC-9 — deterministic lexical candidate-discovery baseline

Tracking issue: #375. Architecture/result contract: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`.

RC-9 adds `core/reader_lexical_discovery.py` and `scripts/bench_reader_rc9_lexical.py`:

```text
RC-4 proposition candidate
→ conservative Unicode/case/whitespace normalization
→ stable lexical tokens
→ in-memory deterministic BM25 ranking
→ structured inspection candidate
→ downstream review only
```

The baseline is stdlib-only, offline, in-memory, bounded and explainable. It has no embedding/vector representation, no network call, no new storage schema, no public Reader API/CLI/worker and no automatic RC-7 registration. Self matches are excluded; cross-document filtering is the default; stable source/session/candidate ordering resolves ties.

Frozen benchmark snapshot: `eval/reader_rc9_lexical_baseline.json`, K=5:

- useful paired cases: 16;
- hard-negative paired cases: 4;
- Recall@5: **0.937500**;
- Precision@5: **0.217391**;
- MRR: **0.895833**;
- paired hard-negative rate@5: **1.000000**;
- cross-lingual paraphrase `rc8-004` is missed;
- all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives are surfaced in top-5.

Metric scope is retrieval-only: the frozen corpus judges each left/right mate, not every possible pair, and the ranker never emits adjudication classes.

Measured interpretation:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

This is evidence for a future architecture decision only. It does **not** authorize semantic/hybrid retrieval, embeddings, ANN/vector DB, identity inference, contradiction adjudication or Canon/evidence mutation.

## Open backlog boundaries

- **#165** remains exact normalized ingest dedupe/migration for admitted facts; it excludes near-duplicate / semantic matching.
- **#155** remains downstream Epistemic Router / Evidence State scope.
- **#214** remains PII-fixture/supply-chain hygiene.

RC-9 does not absorb any of them.

## Localization truth

The immutable localization source checkpoint remains `51c205fe048fd69d39fcd47b43e042a50de432bc` for D1/D3/D4/D5 validator history. Russian Reader-dependent public/detail documentation is current through the RC-7 localization checkpoint `ab3ad31c437647535030e371d58f456faf14017b`; eight other localized root README files and Reader-dependent detail packs remain `REFRESH_NEEDED`, totaling 64 documents. See `docs/LOCALIZATION_POLICY.md` and `docs/TRANSLATION_STATUS.md`.

RC-9 adds authoritative English implementation/status material only. Broad localization is separate.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only; budget change none. RC-0 through RC-9 are pre-agreement baseline if merged before any funding agreement and cannot be presented as awarded/funded delivery.

## Current completion boundary

Complete issue #375 only: implementation/tests/docs → exact-head CI → review gate → guarded merge → verified signed `main` → exact post-merge CI → Notion 3/3 sync/read-back → completion evidence → close issue → final live audit → STOP.

Do **not** automatically start RC-10, semantic/hybrid retrieval, embeddings, ANN/vector DB, PostgreSQL activation, localization refresh or #155/#165/#214 after RC-9.
