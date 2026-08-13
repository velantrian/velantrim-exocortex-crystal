# Crystal AI Current State

**Status date:** 2026-08-13

GitHub merged `main`, executable tests, exact CI and machine-readable implementation truth are
authoritative. Notion is synchronized strategy/history only after successful exact post-merge
evidence.

## Live starting point for post-RC-10 reassessment

- audited starting `main`: `59cf060629c25ddf0747ca46ea1fadf87fa86857`;
- signature: `verified=true`, reason `valid`;
- exact starting-main push CI `31620098274`: 9/9 successful;
- open PRs before issue #382: 0;
- issue #379: closed / completed;
- issue #377: closed / completed after the missing RC-10 completion-evidence bookkeeping step;
- current bounded architecture milestone: **post-RC-10 evaluation adequacy / next-milestone decision, issue #382**;
- branch: `agent/post-rc10-reader-evaluation-reassessment`;
- scope: architecture/evaluation truth + status reconciliation only; no `core/**` runtime expansion.

The starting main contains PR #378, which merged the RC-10 existing-retrieval reuse /
future-comparison **preregistration contract only**. No semantic/hybrid comparator was executed
and no new Reader retrieval runtime was added. Closing #377 does not authorize execution.

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
- RC-8 exact-head / post-merge CI: `31581756932` / `31582325275` successful;
- post-RC-9 grant reconciliation final checkpoint: `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`, CI `31620098274` 9/9 successful.

## Runtime / storage truth

- SQLite ordinary active local-first;
- PostgreSQL/pgvector inactive target `active=false`;
- normal PostgreSQL runtime adapter / automatic switching absent;
- no Reader FTS schema, semantic/vector index, network service or new model dependency is added by #382;
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
Issue #382 is architecture/evaluation only.

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

## PR #378 / issue #377 — RC-10 preregistration COMPLETE, not Reader runtime

Contract: `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`. Machine-readable
preregistration: `eval/reader_rc10_retrieval_comparison_preregistration.json`.

The dedup/reuse audit records what existing admitted-memory retrieval may or may not be reused in
a future isolated comparison. It freezes future comparison gates before results are observed.
Issue #377 is now closed / completed because PR #378's exact-head/post-merge/Notion evidence was
already satisfied and only its final bookkeeping step was missing.

```text
comparison pass != runtime authorization
```

No qualifying semantic/hybrid comparison has been executed. SQLite FTS remains unimplemented
for Reader. PostgreSQL/pgvector remains inactive `active=false`.

## Post-RC-9 grant-presentation reconciliation — COMPLETE

Issue #379 / PR #380 / PR #381 reconciled high-visibility English public/grant surfaces against
the signed RC-9 baseline. Final signed checkpoint is `59cf060629c25ddf0747ca46ea1fadf87fa86857`;
exact push CI `31620098274` is 9/9 successful.

That milestone added no Reader runtime capability and is no longer the current action.

## Post-RC-10 architecture reassessment — #382

Durable decision: `docs/architecture/READER_POST_RC10_REASSESSMENT.md`. Machine-readable decision:
`eval/reader_post_rc10_reassessment.json`.

The key separation is:

```text
measured retrieval-quality gap != measured scaling gap
```

### Evidence

RC-9 demonstrates two retrieval-quality limitations on the frozen RC-8 corpus:

1. `rc8-004` EN/RU cross-lingual paraphrase is missed;
2. all four paired hard negatives surface at K=5.

No current Reader benchmark demonstrates a binding corpus-size, latency, memory or index-build
problem. Therefore SQLite FTS, ANN/vector indexing or a server backend would optimize an
unmeasured problem if selected now.

### Existing utility assessment

- `core/rrf.py`: reusable future rank-fusion utility only; ordering is not authority.
- `HashingEmbedder`: deterministic lexical cosine control signal only.
- `TrigramHashingEmbedder`: morphology/typo-tolerant character signal only; noise/scope risks remain.
- `SentenceTransformerEmbedder`: future optional model-backed comparison class only; current
  existence does not satisfy exact immutable model/dependency/privacy admission.
- admitted-memory pipeline/query/legacy retrieval: no direct PRE-ADMISSION Reader wiring.
- SQLite FTS: future scaling option only after a measured scale blocker.
- PostgreSQL/pgvector: not authorized for Reader and remains inactive.

### Selected next bounded milestone

The smallest justified next milestone is **Reader Retrieval Evaluation Surface v2**.

Its role is to freeze a stronger judged evaluation surface before model-backed comparator
results are observed, preserve the historical RC-8 corpus and unchanged RC-10 screen, and
reproduce RC-9 as the control. It should include multiple cases per material identity/scope trap,
multiple cross-lingual useful and hard-negative cases, and judged candidate pools/qrels rather
than relying only on one intended pair per synthetic case.

**Evaluation Surface v2 is NOT STARTED by #382.** It requires a new bounded authorization after
#382 completes. A model-backed comparator is forbidden in the same corpus-freeze milestone.

Only after Evaluation Surface v2 is frozen may a separately authorized comparator execution be
considered. A later comparator must still pass the unchanged RC-10 screen:

- retain all 15 RC-9 useful hits;
- recover `rc8-004` to 16/16 useful paired recall;
- MRR >= `0.895833`;
- paired hard-negative hits <= `2/4`;
- zero authority violations;
- exact backend/model/index identity;
- no `auto` backend;
- zero query-time network calls;
- zero external Reader source-text transmission;
- deterministic lexical fallback for any later runtime proposal.

Even a pass remains eligibility for stronger evaluation/architecture review, not runtime
authorization.

## Open backlog boundaries

- **#165** remains exact normalized ingest dedupe/migration for admitted facts; it excludes near-duplicate / semantic matching.
- **#155** remains downstream Epistemic Router / Evidence State RFC around FactsPack/TruthGate/Guardian.
- **#214** remains PII-fixture/supply-chain hygiene.
- **#382** is the current architecture/evaluation decision; it does not execute a comparator or create Reader runtime.

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

The English root/grant presentation advanced to post-RC-9 truth in completed #379. #382 adds
English architecture/evaluation truth only. Broad translation is not part of this milestone;
localized text must not be represented as newer than its recorded checkpoint.

## Grant truth

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning
only; budget change none. RC-1 through RC-9 merged before an agreement are existing baseline and
cannot be counted again as future funded delivery. PR #378's preregistration and #382's
architecture decision are also existing pre-agreement repository history if merged before an
agreement, not funded Reader runtime.

## Current action / STOP boundary

Complete only issue #382:

```text
post-RC-10 architecture/evaluation decision
→ status truth reconciliation
→ PR exact-head CI
→ evidence-grounded semantic review
→ guarded merge
→ signed main
→ exact post-merge CI
→ Notion 3/3 sync/read-back
→ completion evidence / close
→ final live audit
→ STOP
```

Do **not** start Evaluation Surface v2, execute semantic/hybrid comparison, add embeddings/ANN/
vector DB, implement Reader FTS, activate PostgreSQL/pgvector, perform automatic entity/claim
identity, start broad localization, or absorb #155/#165/#214.