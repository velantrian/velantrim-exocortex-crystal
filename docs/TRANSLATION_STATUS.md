# 🌍 Crystal Translation Status

**Status date:** 2026-08-12  
**Primary/source language:** English  
**Reader RC-6 immutable English source checkpoint:** `main@ed96a88369f841bdb2ffd79ca020acef174685fc`  
**Reader RC-5 immutable English source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

Translation state is evidence, not aspiration. `CURRENT` means a localized surface has been semantically refreshed against its recorded source. `REFRESH_NEEDED` means the rich prior translation is intentionally preserved but known to lag the current English Reader meaning.

## Current RC-6 localization truth

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
dedicated_reader_core                  = false
```

Russian root + Reader-dependent D1/D3/D4/D5 surfaces are `CURRENT` to `main@ed96a88369f841bdb2ffd79ca020acef174685fc`. Eight other Reader-dependent locale packs preserve their rich RC-5-era translations and remain `REFRESH_NEEDED`; they are not relabeled as RC-6 current. D2 and Quick Start remain current across all nine supported locales because RC-6 does not change those source contracts.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

### Mixed-status accounting

Eight refresh-needed locales × (root README + 7 Reader-dependent detail documents) = **64 `REFRESH_NEEDED` localized documents**.

```text
8 root READMEs
+ 8 × 2 D1 Reader detail docs
+ 8 × 2 D3 Reader detail docs
+ 8 × 2 D4 Reader detail docs
+ 8 × 1 D5 Reader guide
= 64
```

D5 inventory remains: **273 total = 72 CURRENT + 127 ENGLISH_ONLY_BY_DESIGN + 64 REFRESH_NEEDED + 10 RETIRED**.

## Historical RC-5 boundary retained for D1–D5 evidence

The RC-5 checkpoint below remains immutable historical evidence used by the existing D1–D5 validators. RC-6 adds a new executable localization gate rather than rewriting that evidence.

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

RC-5 adds explicit same-session/same-source-version PRE-ADMISSION relation candidates over valid RC-4 proposition candidates: `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION`.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
similarity != identity
repetition != corroboration
```

## Root localized READMEs — RC-5 historical checkpoint

**Source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

- Russian root README was `CURRENT` at RC-5 and is now additionally refreshed to RC-6.
- Arabic, German, Spanish, French, Hindi, Italian, Japanese and Simplified Chinese root READMEs remain `REFRESH_NEEDED`.
- Their rich translations are preserved; none is replaced by a short summary and falsely marked current.

## D1 — entry/status/implementation

**D1 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D1 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Quick Start is unchanged/current in all nine locales.

Russian current: `docs/ru/STATUS.md`, `docs/ru/IMPLEMENTATION_STATUS.md`, locale index and Quick Start. Other locale STATUS/IMPLEMENTATION_STATUS files remain rich, stale Reader translations.

## D2 — reviewer/safety

**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

D2 source semantics did not change in RC-5 or RC-6. D2 remains complete for all nine supported locales. Reviewer Guide and Safety/Privacy/Failures remain `CURRENT` for all nine supported locales.

| D2 surface | Translation state |
|---|---|
| D2 reviewer/safety | all nine supported locales `CURRENT` |

## D3 — architecture/storage/authority

**D3 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D3 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Russian now also includes RC-6 bounded working-set/summary semantics and the unchanged PostgreSQL `active=false` boundary.

## D4 — project, grant, governance and glossary

**D4 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D4 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Grant truth remains `submitted / under review / not awarded`, approximate €50,000 planning only, budget change none. Pre-agreement RC-5 is existing baseline; RC-6 becomes existing baseline if merged before agreement.

## D5 — extended reference documents

**D5 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D5 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Detailed volatile evidence remains `ENGLISH_ONLY_BY_DESIGN` where the D5 inventory says so; retired material remains audit history.

## Source of truth

English merged `main`, executable tests and exact CI remain implementation authority. Localized documents explain that truth; they do not redefine it. NLnet remains `submitted / under review / not awarded`; approximate €50,000 is planning only; budget change none. SQLite remains ordinary active local-first; PostgreSQL/pgvector remains inactive `active=false`.
