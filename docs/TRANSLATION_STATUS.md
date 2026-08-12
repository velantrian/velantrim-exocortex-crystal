# 🌍 Crystal Translation Status

**Status date:** 2026-08-12  
**Primary/source language:** English  
**Reader RC-7 immutable English source checkpoint:** `main@ab3ad31c437647535030e371d58f456faf14017b`  
**Reader RC-7 checkpoint CI:** `31570690153` — 9/9 successful  
**Reader RC-6 immutable English source checkpoint:** `main@ed96a88369f841bdb2ffd79ca020acef174685fc`  
**Reader RC-5 immutable English source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

## Current RC-7 localization truth

Russian root + Reader-dependent D1/D3/D4/D5 surfaces are `CURRENT` to `main@ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs preserve rich translations as `REFRESH_NEEDED`. D2 and Quick Start remain current across all nine supported locales.

**64 `REFRESH_NEEDED` localized documents** remain. D5 inventory: **273 total = 72 CURRENT + 127 ENGLISH_ONLY_BY_DESIGN + 64 REFRESH_NEEDED + 10 RETIRED**.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
dedicated_reader_core = false
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 is a bounded explicit cross-document candidate-link layer with exact two-sided provenance and no evidence/identity/Canon authority. **RC-7 does not start semantic/vector retrieval.** Embeddings, ANN/vector DB, automatic semantic matching, entity resolution and claim identity remain not implemented/not implied and require separate future authorization after RC-7 completion.

## Reader RC-6 boundary — preserved history

**Source checkpoint:** `main@ed96a88369f841bdb2ffd79ca020acef174685fc`

RC-6 remains merged bounded long-context baseline: deterministic working sets over current registered RC-4 leaves in one OPEN ReaderSession / exact SourceVersion, direct RC-4 leaf provenance, optional in-set RC-5 context and caller-supplied `SUMMARY`.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

## Reader RC-5 boundary — preserved history

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

D1 Reader-dependent detail translations are `CURRENT` in Russian at the RC-7 refresh layer while preserving immutable D1 source markers. Eight other supported locales are `REFRESH_NEEDED`. Quick Start is unchanged/current in all nine locales.

## D2 — reviewer/safety

**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

D2 remains complete for all nine supported locales. D2 reviewer/safety translations remain current across all nine supported locales. Reviewer Guide and Safety/Privacy/Failures remain `CURRENT` for all nine supported locales.

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

D3 Reader-dependent detail translations are `CURRENT` in Russian at the RC-7 refresh layer. Eight other supported locales are `REFRESH_NEEDED`. Russian carries RC-7 cross-document provenance/non-identity semantics plus RC-6 bounded working-set/SUMMARY semantics.

## D4 — project, grant, governance and glossary

**D4 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D4 Reader-dependent detail translations are `CURRENT` in Russian at the RC-7 refresh layer. Eight other supported locales are `REFRESH_NEEDED`. Grant remains `submitted / under review / not awarded`; approximate €50,000 planning only; budget change none.

## D5 — extended reference documents

**D5 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D5 Reader-dependent detail translations are `CURRENT` in Russian at the RC-7 refresh layer. Eight other supported locales are `REFRESH_NEEDED`. Detailed volatile evidence remains `ENGLISH_ONLY_BY_DESIGN` where declared; retired material remains audit history.

## Authority / storage / grant

English merged `main`, executable tests and exact CI remain implementation authority. SQLite ordinary active local-first; PostgreSQL/pgvector inactive `active=false`. NLnet remains `submitted / under review / not awarded`; approximate €50,000 planning only; budget change none. RC-0 through RC-6 are existing pre-agreement baseline. If RC-7 merges pre-agreement, it also becomes existing baseline and cannot be counted again as future funded delta.