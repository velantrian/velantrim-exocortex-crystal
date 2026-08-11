# Crystal AI Current State

**Status date:** 2026-08-11

GitHub merged `main`, executable tests, exact CI and the implementation manifest are implementation authority. Notion is synchronized strategy/history only.

## Runtime/storage truth

- retained runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- retained evidence: Python 3.11/3.12 2078 passed / 13 skipped / 0 failed, 9756 statements / 100.00% line coverage;
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
dedicated_reader_core                  = false
```

RC-5 registers `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` only over valid RC-4 candidates in one OPEN ReaderSession and exact SourceVersion. It preserves both candidate IDs, replayable source provenance and explicit rationale. Symmetric kinds canonicalize pair order; exception/qualification remain directional.

RC-5 does not perform raw-text semantic conflict detection, semantic equivalence, cross-document identity, evidence admission or contradiction resolution.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
coverage != comprehension proof
pass completion != comprehension proof
similarity != identity
repetition != corroboration
```

No Reader layer may mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, attach fact evidence, assert evidence sufficiency, promote confidence, select contradiction winners or gain planner/belief authority.

## Localization

RC-5 English source checkpoint: `51c205fe048fd69d39fcd47b43e042a50de432bc`.

Russian Reader-dependent public/detail documentation is refreshed to that immutable checkpoint. The eight other localized root README files and Reader-dependent detail packs preserve rich translations as `REFRESH_NEEDED`. D2 and Quick Start remain current in all nine locales. Tracked Reader/root debt remains 64 documents.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only; budget change none. RC-5 merged pre-agreement is existing baseline, not future funded delta.

## Next Reader work

No next Reader phase is implied. RC-6 or RC-7 requires separate authorization after RC-5 completion evidence.
