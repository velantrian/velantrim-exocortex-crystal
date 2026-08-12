# 🌍 Crystal Translation Status

**Status date:** 2026-08-12  
**Primary/source language:** English  
**Reader RC-6 immutable English source checkpoint:** `main@ed96a88369f841bdb2ffd79ca020acef174685fc`  
**Reader RC-5 immutable English source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

## Current RC-6 localization truth

Russian root + Reader-dependent D1/D3/D4/D5 surfaces are `CURRENT` to `main@ed96a88369f841bdb2ffd79ca020acef174685fc`. Eight other Reader-dependent locale packs preserve rich translations as `REFRESH_NEEDED`. D2 and Quick Start remain current across all nine supported locales.

**64 `REFRESH_NEEDED` localized documents** remain. D5 inventory: **273 total = 72 CURRENT + 127 ENGLISH_ONLY_BY_DESIGN + 64 REFRESH_NEEDED + 10 RETIRED**.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
dedicated_reader_core = false
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

## Reader RC-5 boundary

**Source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

RC-5 relation candidates remain PRE-ADMISSION: `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION`.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
similarity != identity
repetition != corroboration
```

## D1 — entry/status/implementation

**D1 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D1 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Quick Start is unchanged/current in all nine locales.

## D2 — reviewer/safety

**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

D2 reviewer/safety translations remain current across all nine supported locales. Reviewer Guide and Safety/Privacy/Failures remain `CURRENT` for all nine supported locales.

## D3 — architecture/storage/authority

**D3 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D3 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Russian now also carries RC-6 bounded working-set and provenance-preserving SUMMARY semantics.

## D4 — project/grant/governance/glossary

**D4 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D4 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Grant status remains `submitted / under review / not awarded`; approximate €50,000 is planning only; budget change none.

## D5 — extended reference

**D5 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D5 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Detailed volatile evidence remains `ENGLISH_ONLY_BY_DESIGN` where the D5 inventory declares it; retired material remains audit history.

## Authority / storage / grant

English merged `main`, executable tests and exact CI remain implementation authority. SQLite remains ordinary active local-first; PostgreSQL/pgvector remains inactive `active=false`. NLnet remains `submitted / under review / not awarded`; approximate €50,000 is planning only; budget change none. If RC-6 merges pre-agreement, it becomes existing baseline and cannot be counted again as future funded delta.
