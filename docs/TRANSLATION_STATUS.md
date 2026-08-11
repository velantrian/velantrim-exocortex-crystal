# 🌍 Crystal Translation Status

**Status date:** 2026-08-11  
**Primary/source language:** English  
**Reader RC-5 immutable English source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

Translation state is evidence, not aspiration. `CURRENT` means a localized surface has been semantically refreshed against its recorded source. `REFRESH_NEEDED` means the rich prior translation is intentionally preserved but known to lag the current English Reader meaning.

## Reader RC-5 boundary

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

## Root localized READMEs

**Source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

- Russian root README: `CURRENT`.
- Arabic, German, Spanish, French, Hindi, Italian, Japanese and Simplified Chinese root READMEs: `REFRESH_NEEDED`.
- Their rich pre-RC-5 translations are preserved; none is replaced by a short summary and falsely marked current.

## D1 — entry/status/implementation

**D1 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D1 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Quick Start is unchanged/current in all nine locales.

Russian current: `docs/ru/STATUS.md`, `docs/ru/IMPLEMENTATION_STATUS.md`, locale index and Quick Start. Other locale STATUS/IMPLEMENTATION_STATUS files remain rich, stale Reader translations.

## D2 — reviewer/safety

**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

D2 source semantics did not change in RC-5. D2 remains complete for all nine supported locales. Reviewer Guide and Safety/Privacy/Failures remain `CURRENT` for all nine supported locales.

| D2 surface | Translation state |
|---|---|
| D2 reviewer/safety | all nine supported locales `CURRENT` |

| Locale | Reviewer Guide | Safety/Privacy/Failures |
|---|---|---|
| Arabic | `CURRENT` | `CURRENT` |
| German | `CURRENT` | `CURRENT` |
| Spanish | `CURRENT` | `CURRENT` |
| French | `CURRENT` | `CURRENT` |
| Hindi | `CURRENT` | `CURRENT` |
| Italian | `CURRENT` | `CURRENT` |
| Japanese | `CURRENT` | `CURRENT` |
| Russian | `CURRENT` | `CURRENT` |
| Simplified Chinese | `CURRENT` | `CURRENT` |

## D3 — architecture/storage/authority

**D3 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D3 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Russian now includes RC-5 same-session/same-version relation candidates and the unchanged PostgreSQL `active=false` boundary.

## D4 — project, grant, governance and glossary

**D4 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D4 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Grant truth remains `submitted / under review / not awarded`, approximate €50,000 planning only, budget change none. Pre-agreement RC-5 is existing baseline.

## D5 — extended reference documents

**D5 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D5 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Detailed volatile evidence remains `ENGLISH_ONLY_BY_DESIGN` where the D5 inventory says so; retired material remains audit history.

## Mixed-status accounting

Eight refresh-needed locales × (root README + 7 Reader-dependent detail documents) = **64 `REFRESH_NEEDED` localized documents**.

```text
8 root READMEs
+ 8 × 2 D1 Reader detail docs
+ 8 × 2 D3 Reader detail docs
+ 8 × 2 D4 Reader detail docs
+ 8 × 1 D5 Reader guide
= 64
```

This debt does not include D2 or Quick Start because those source semantics did not change. It also does not imply native-speaker editorial, legal, security or GDPR certification.

## Source of truth

English merged `main`, executable tests and exact CI remain implementation authority. Localized documents explain that truth; they do not redefine it.
