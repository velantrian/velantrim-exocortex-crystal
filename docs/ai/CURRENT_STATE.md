# Crystal AI Current State

**Status date:** 2026-08-12

GitHub merged `main`, executable tests, exact CI and machine-readable implementation truth are authoritative. Notion is synchronized strategy/history only after successful exact post-merge evidence.

## Runtime/storage truth

- retained runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- retained evidence: Python 3.11/3.12 `2078 passed / 13 skipped / 0 failed`, 9756 statements / 100.00% line coverage;
- current signed Reader baseline: `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` — RC-6 merged via PR #370;
- RC-6 post-merge CI `31566408978`: 9/9 successful;
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
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
```

RC-1 through RC-6 are merged bounded Reader layers. RC-7 is the separately authorized current milestone under issue #371 / draft PR #372. The first runtime/test head `b75811e09323adbe2c74184ae0470dfb703fcf4c` passed exact-head smoke CI `31568205231` 9/9. The RC-7 flag above describes the implementation branch; final implementation truth still requires final exact-head CI, guarded squash merge, verified merge signature and exact post-merge push CI.

RC-4 remains deterministic source-linked PRE-ADMISSION proposition registration. RC-5 remains same-session/same-exact-source-version explicit relation registration. RC-6 is merged deterministic one-session long-context orchestration with direct RC-4 leaf provenance and caller-supplied `SUMMARY` artifacts.

RC-7 lives in `core/reader_cross_document.py`. `ReaderCrossDocumentRegistry` is constructed from explicit RC-4 extractors and requires at least two OPEN Reader sessions covering at least two different document identities. A link may name only candidate IDs already registered by those extractors.

Before each link registration RC-7 revalidates both sides against current state:

- candidate remains `SourceFidelity.EXTRACTED_PROPOSITION` and still belongs to the exact Reader session;
- exact SourceVersion and privacy binding still match every direct locator;
- candidate SegmentCard identity is still registered;
- original RC-3 pass remains `COMPLETED` and source/session-bound;
- candidate node IDs remain declared pass targets with substantive `PROCESSED` / `REVISITED` outcomes;
- RC-2 nodes remain `RECOVERED` with replay-key-matching provenance;
- current RC-1 coverage remains substantive and matches exact source/replay provenance.

RC-7 relation vocabulary is explicit and caller-supplied:

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

`CONTRADICTS`, `SAME_TOPIC` and `POSSIBLE_SAME_CLAIM` are symmetric candidates and canonicalize side order by exact source/session/candidate sort key. The other relation kinds preserve left/right direction. Duplicate semantic candidate registrations fail closed. Each link retains exact source/session/candidate/pass/node/primary+supporting locator provenance for both sides plus a non-empty rationale.

Optional `CrossDocumentInspectionBasis` values (`EXPLICIT_SOURCE_REFERENCE`, `CALLER_COMPARISON`, `LEXICAL_SIMILARITY_SIGNAL`, `SHARED_TOPIC_SIGNAL`, `OTHER`) are descriptive caller metadata only. RC-7 has no numeric similarity score, confidence, identity, winner or evidence-sufficiency field.

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
```

No Reader layer may mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction winners or gain planner/belief authority.

RC-7 adds no parser/chunker/OCR/PDF-layout/multimodal engine, LLM/provider/model routing, embeddings/ANN/vector database, automatic semantic matching/entity resolution/deduplication, automatic corroboration, public Reader API/CLI/worker, durable Reader schema or PostgreSQL activation.

## Historical localization truth retained for validators

The immutable RC-5 English localization checkpoint is `51c205fe048fd69d39fcd47b43e042a50de432bc`.
The unchanged D2 reviewer/safety/privacy/failure source checkpoint remains `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

Russian Reader-dependent public/detail documentation is refreshed relative to the historical RC-5 program and was subsequently advanced to the immutable RC-6 English checkpoint `ed96a88369f841bdb2ffd79ca020acef174685fc`. The eight other localized root README files and Reader-dependent detail packs preserve rich `REFRESH_NEEDED` translations. D2 reviewer/safety translations and Quick Start remain current across all nine supported locales.

The current RC-7 English public/machine source advances in a dedicated English checkpoint commit. Existing Russian files must not be interpreted as containing RC-7 semantics until the subsequent Russian refresh commit pins that exact new English SHA. At final RC-7 localization state, Russian root + D1/D3/D4/D5 Reader surfaces return to `CURRENT` against the immutable RC-7 checkpoint; eight other locale packs remain `REFRESH_NEEDED` and the tracked Reader/root debt remains 64 documents.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only; budget change none. RC-0 through RC-6 are existing pre-agreement baseline. If RC-7 merges before any grant agreement, RC-7 also becomes existing pre-agreement baseline and cannot be counted again as future funded delta.

## Next Reader work

RC-7 is the only currently authorized Reader milestone. Semantic/vector retrieval implementation is **not started and not implied** by RC-7. After RC-7 completion the project may reassess whether measured retrieval needs justify a separately authorized semantic/vector phase.
