# Crystal AI Current State

**Status date:** 2026-08-12

GitHub merged `main`, executable tests, exact CI and the implementation manifest are implementation authority. Notion is synchronized strategy/history only after successful post-merge evidence.

## Runtime/storage truth

- retained runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- retained evidence: Python 3.11/3.12 `2078 passed / 13 skipped / 0 failed`, 9756 statements / 100.00% line coverage;
- SQLite ordinary active local-first;
- PostgreSQL/pgvector inactive target `active=false`;
- normal PostgreSQL runtime adapter / automatic switching absent.

## Reader truth

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
dedicated_reader_core                  = false
```

RC-1 through RC-5 are merged bounded Reader layers. RC-6 is the current separately authorized milestone under issue #369 / PR #370; final RC-6 implementation truth still requires final exact-head CI, guarded merge, verified merge signature and exact post-merge push CI.

RC-4 remains source-linked PRE-ADMISSION proposition registration. RC-5 remains same-session/same-exact-source-version explicit relation registration over valid RC-4 candidates only.

RC-6 lives in `core/reader_long_context.py` and is a deterministic, one-session / one-exact-source-version long-context strategy over already-registered RC-4 proposition candidates. It revalidates direct leaves and orders them by RC-2 structural order with candidate-ID tie-breaking, then partitions them into rolling working sets under explicit candidate-count and unique direct source-locator budgets. One candidate remains atomic with all direct replayable locators; a candidate that cannot fit the declared locator budget fails closed.

An optional matching RC-5 registry contributes relation IDs only when both relation sides are inside the same working set. RC-6 does not infer a new relation and does not carry a cross-set relation into either set.

RC-6 can register caller-supplied `SourceFidelity.SUMMARY` artifacts for an existing working set. Every summary retains the exact direct RC-4 leaf candidate IDs and the deduplicated replayable source locators of that set. Before summary registration the immutable working-set leaf-provenance snapshot is compared to current RC-4 leaves and those leaves are then revalidated. A summary cannot use another summary as its only provenance path. Summary text is not generated automatically.

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
similarity != identity
repetition != corroboration
```

No Reader layer may mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction winners or gain planner/belief authority.

RC-6 adds no parser/chunker/OCR/PDF-layout/multimodal engine, LLM/provider/model routing, token-context claim, embeddings/ANN/vector database, automatic semantic equivalence, RC-7 cross-document reading, public Reader API/CLI/worker, durable Reader schema or PostgreSQL activation.

## Localization

The immutable RC-5 English localization checkpoint is `51c205fe048fd69d39fcd47b43e042a50de432bc`.

Russian Reader-dependent public/detail documentation is refreshed and `CURRENT` **against that RC-5 checkpoint**. The eight other localized root README files and Reader-dependent detail packs remain rich `REFRESH_NEEDED` translations. D2 reviewer/safety translations and Quick Start remain current in all nine supported locales.

The current English RC-6 public/machine source advances in a dedicated English checkpoint commit. Existing Russian files must not be interpreted as containing RC-6 semantics until the subsequent Russian refresh commit pins that exact new English SHA. At final RC-6 localization state, Russian root + D1/D3/D4/D5 Reader surfaces return to `CURRENT` against the immutable RC-6 checkpoint; eight other locale packs remain `REFRESH_NEEDED` and the tracked Reader/root debt remains 64 documents.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only; budget change none. RC-0 through RC-5 are existing pre-agreement baseline. If RC-6 merges before any grant agreement, RC-6 also becomes existing pre-agreement baseline and cannot be counted again as future funded delta.

## Next Reader work

RC-6 is the only currently authorized Reader milestone. RC-7 cross-document reading is **not started and not implied** by RC-6. Any RC-7 work requires a new bounded authorization after RC-6 completion evidence.
