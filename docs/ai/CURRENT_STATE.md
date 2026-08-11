# Crystal AI Current State

**Status date:** 2026-08-11

GitHub merged `main`, executable tests, exact CI and the machine-readable implementation manifest are implementation authority. Notion records synchronized strategy/history and never overrides GitHub evidence.

## Runtime / storage truth

- retained verified runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- retained evidence: Python 3.11/3.12 2078 passed / 13 skipped / 0 failed, 9756 statements / 100.00% line coverage;
- later Reader milestones carry separate exact-head and post-merge CI evidence;
- SQLite remains ordinary active local-first;
- PostgreSQL/pgvector remains an inactive target with `active=false`;
- normal PostgreSQL runtime adapter and automatic backend switching remain absent.

## Reader truth

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

RC-1 is the evidence-linked source/session skeleton. RC-2 is the caller-supplied Structural Document Map. RC-3 is deterministic explicit multi-pass mechanics. RC-4 is deterministic source-linked pre-admission proposition candidate registration. RC-5 is deterministic pre-admission relation candidate registration over already-registered RC-4 candidates.

RC-5 uses one `ReaderRelationRegistry` bound to one RC-4 extractor/session/source domain. It registers `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION` or `TENSION`, preserves both exact candidate IDs and both sides' replayable source provenance, requires explicit rationale and rejects stale/mismatched source/session context. Symmetric kinds use canonical pair ordering; exception and qualification remain directional.

RC-5 is not automatic semantic conflict detection. No raw source comparison, semantic equivalence inference, cross-document identity, LLM/provider, parser/OCR, embeddings/ANN/vector DB, evidence admission or contradiction resolution is added.

```text
source statement        != verified fact
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
coverage                != comprehension proof
pass completion         != comprehension proof
similarity              != identity
repetition              != corroboration
```

RC-1/RC-2/RC-3/RC-4/RC-5 may not mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction winners or create planner/belief-update authority.

## Localization

English is the primary/source technical language. Russian Reader-dependent public/detail documentation is refreshed to the immutable RC-5 English source checkpoint recorded in `docs/TRANSLATION_STATUS.md`. Eight other localized roots and Reader-dependent detail packs preserve rich existing translations as explicit `REFRESH_NEEDED` debt. D2 reviewer/safety and Quick Start remain current across all nine supported locales. The tracked Reader/root refresh debt remains 64 documents.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget or payment commitment. Budget change: none. Work merged before any agreement, including Reader RC-0/RC-1/RC-2/RC-3/RC-4/RC-5 when merged, is existing baseline and cannot be counted again as future funded delta.

## Next Reader work

Do not infer a next implementation from this state. Any RC-6 long-context work or later RC-7 cross-document reading requires a separately authorized bounded milestone after RC-5 completion evidence.
