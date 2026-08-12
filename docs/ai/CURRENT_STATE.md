# Crystal AI Current State

**Status date:** 2026-08-12

GitHub merged `main`, executable tests, exact CI and machine-readable implementation truth are
authoritative. Notion is synchronized strategy/history only after successful exact post-merge
evidence.

## Live starting point for grant-presentation reconciliation

- audited starting `main`: `430e643a2a3759da793f700617a327d419439dde`;
- signature: `verified=true`, reason `valid`;
- latest starting-main push CI `31603785427`: 9/9 successful;
- open PRs before issue #379: 0;
- current bounded documentation milestone: **post-RC-9 grant presentation truth reconciliation, issue #379**;
- branch: `agent/post-rc9-grant-truth-reconciliation`;
- scope: public/grant English truth + reproducibility + semantic docs guards only; no `core/**` runtime expansion.

The starting main contains PR #378 (`430e643…`), which merged the RC-10 existing-retrieval
reuse / future-comparison **preregistration contract only**. Issue #377 remains separate from
#379. No semantic/hybrid comparator was executed and no new Reader retrieval runtime was added.

## Current verified Reader implementation checkpoint

- signed authoritative RC-9 Reader merge: `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`;
- merge signature: `verified=true`, reason `valid`;
- PR #376 exact validated head: `1956cbd45e5a5b794852354ed2233bf1fb6e318f`;
- RC-9 exact-head CI `31593097846`: 9/9 successful;
- RC-9 post-merge push CI `31594027040`: 9/9 successful;
- issue #375: closed / completed.

Historical compatibility evidence remains:

- retained runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- signed RC-7 Reader baseline: `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`;
- RC-7 post-merge CI `31572918731`: 9/9 successful;
- signed RC-8 merge: `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374;
- RC-8 exact-head / post-merge CI: `31581756932` / `31582325275` successful.

## Runtime / storage truth

- SQLite ordinary active local-first;
- PostgreSQL/pgvector inactive target `active=false`;
- normal PostgreSQL runtime adapter / automatic switching absent;
- no Reader FTS schema, semantic/vector index, network service or new model dependency is added by #379;
- existing admitted-memory retrieval remains a separate authority/data lifecycle from Reader PRE-ADMISSION discovery.

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

RC-1 through RC-7 are merged bounded Reader layers. `dedicated_reader_core=false` remains the
larger capability truth. RC-8 is a completed architecture/research decision; RC-9 is the
completed deterministic lexical candidate-discovery implementation baseline. PR #378 adds a
future-comparison preregistration contract only and does not create a complete Reader runtime.

Authority invariants:

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
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

No Reader layer may mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate,
attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction
winners or gain planner/belief authority from retrieval rank.

## RC-8 — completed retrieval architecture decision

Issue #373 / PR #374 completed. Durable decision:
`docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Adversarial corpus:
`eval/reader_rc8_retrieval_adversarial.jsonl`.

RC-8 identified corpus candidate discovery as the missing capability and required a
deterministic lexical baseline before semantic/vector machinery could even be considered.
Existing admitted-memory retrieval modules (`core/embedding.py`, `core/legacy_retrieval.py`,
`core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py`, retrieval composition in
`core/pipeline.py`) are not automatic Reader identity authority.

## RC-9 — deterministic lexical candidate discovery: COMPLETE

Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Frozen result:
`eval/reader_rc9_lexical_baseline.json`.

RC-9 uses stdlib-only, offline, in-memory deterministic BM25 over conservative NFKC/case/
whitespace normalized proposition snapshots. Self matches are excluded; cross-document
filtering is default; result fields contain retrieval/provenance metadata only.

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

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. These are candidate-discovery metrics,
not semantic/adjudication/identity accuracy. The measured gap does not authorize embeddings,
semantic/hybrid retrieval, ANN/vector DB or evidence/Canon promotion.

## PR #378 / issue #377 — preregistration history, not Reader runtime

Contract: `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`. Machine-readable
preregistration: `eval/reader_rc10_retrieval_comparison_preregistration.json`.

The dedup/reuse audit records what existing admitted-memory retrieval may or may not be reused in
a future isolated comparison. It freezes future comparison gates before results are observed.

```text
comparison pass != runtime authorization
```

No qualifying semantic/hybrid comparison has been executed. SQLite FTS remains unimplemented
for Reader. PostgreSQL/pgvector remains inactive `active=false`.

## Grant-presentation reconciliation under #379

The live audit found high-visibility truth drift despite current compact architecture/status
evidence:

- root `README.md` still presented RC-6 as authoritative and RC-7 as draft/in progress;
- `docs/GRANT_NLNET_SCOPE.md` and `docs/grants/baseline-funded-delta-matrix.md` still treated
  the baseline as ending at RC-5 / RC-6-in-progress;
- `scripts/check_d4_source_contract.py` actively protected the stale RC-5 grant narrative;
- adjacent reviewer/funding/orientation surfaces lacked the current RC-9 proof point.

Issue #379 reconciles those English public/grant surfaces against RC-9 and changes the D4
semantic validator so stale RC-5/RC-7-draft current-state wording cannot silently return.
It adds no runtime capability.

## Open backlog boundaries

- **#165** remains exact normalized ingest dedupe/migration for admitted facts; it excludes near-duplicate / semantic matching.
- **#155** remains downstream Epistemic Router / Evidence State RFC around FactsPack/TruthGate/Guardian.
- **#214** remains PII-fixture/supply-chain hygiene.
- **#377** remains separate RC-10 preregistration/completion bookkeeping; #379 does not execute its comparator or create a Reader runtime.

## Localization truth

The immutable historical D1/D3/D4/D5 source checkpoint
`51c205fe048fd69d39fcd47b43e042a50de432bc` remains required by the executable phased
localization contract. Russian Reader-dependent public/detail documentation is refreshed
through RC-7. The eight other localized root README files and Reader-dependent detail packs
remain `REFRESH_NEEDED`; tracked Reader-dependent detail debt remains 64 documents.

Historical executable localization markers retained:

- D2 reviewer/safety translations remain current across all nine supported locales.
- Russian D1/D3/D4/D5 detail pack is current to its recorded checkpoint.
- eight other locale detail packs require Reader refresh.
- D2 translation source checkpoint: `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

The English root/grant presentation advances to post-RC-9 truth in #379. Broad translation is
not part of this milestone; localized text must not be represented as newer than its recorded
checkpoint.

## Grant truth

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning
only; budget change none. RC-1 through RC-9 merged before an agreement are existing baseline and
cannot be counted again as future funded delivery. PR #378's preregistration is also existing
pre-agreement repository history, not funded Reader runtime.

## Current action / STOP boundary

Complete only issue #379:

```text
public/grant truth reconciliation
→ docs/status validation
→ PR exact-head CI
→ independent semantic review
→ guarded merge
→ signed main
→ exact post-merge CI
→ Notion 3/3 sync/read-back
→ completion evidence / close
→ final live audit
→ STOP
```

Do **not** execute semantic/hybrid comparison, add embeddings/ANN/vector DB, implement Reader
FTS, activate PostgreSQL/pgvector, perform automatic entity/claim identity, start broad
localization, or absorb #155/#165/#214.
