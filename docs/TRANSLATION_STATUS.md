# Translation status and phased rollout

## Purpose

This ledger is the authoritative freshness map for multilingual Crystal documentation. English remains the primary source and conflict resolver; translations cannot strengthen implementation, security, authority, legal or grant claims.

**Root README source checkpoint:** `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86`.  
**D1 source checkpoint:** `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86`.  
**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.  
**D3 source checkpoint:** `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86`.  
**D4 source checkpoint:** `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86`.  
**D5 source checkpoint:** `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86`.

**Policy:** [`LOCALIZATION_POLICY.md`](LOCALIZATION_POLICY.md).  
**D5 policy:** [`EXTENDED_REFERENCE_POLICY.md`](EXTENDED_REFERENCE_POLICY.md).  
**Tracking issue:** [#341](https://github.com/velantrian/velantrim-exocortex-crystal/issues/341).

## Reader RC-4 boundary

The RC-4 source checkpoint distinguishes four bounded implemented Reader layers from the still-absent dedicated/full autonomous Reader runtime:

```text
reader_core_rc1_skeleton              = true
reader_core_rc2_structural_map        = true
reader_core_rc3_multi_pass_mechanics  = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core                 = false
```

RC-3 provides deterministic explicit pass mechanics only: `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK` and `TARGETED_REREAD`; declared structural targets; attempted/completed/interrupted/degraded pass state; explicit legal coverage effects; and count-only telemetry. It does not add an autonomous model-driven Reader, parser/OCR, embeddings/ANN/vector DB, automatic cross-document reasoning, contradiction resolution or planner/belief-update authority. `coverage != comprehension proof`; `pass completion != comprehension proof`.

RC-4 adds deterministic pre-admission source-linked proposition candidate registration from completed substantive RC-3 regions. Candidates use `EXTRACTED_PROPOSITION` fidelity and preserve replayable locators, source ownership, source-presentation category, negation and qualifiers. RC-4 does not perform automatic NLP/LLM extraction, call `core.evidence.attach_evidence()`, write fact evidence, set evidence sufficiency or perform TruthGate admission. `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`.

The Russian public/detail Reader surfaces are refreshed against this checkpoint. The eight other localized root READMEs and Reader-dependent detail families preserve their prior rich translations but are explicitly `REFRESH_NEEDED` until full semantic refresh. Their old file-level `CURRENT` markers refer only to older source SHAs embedded in those files; this ledger and the locale indexes are the current freshness authority after RC-4.

## Root README status

English and Russian are current against the RC-4 Reader source. The other eight rich root READMEs remain available but require RC-4 semantic refresh.

| Language | File | Status |
|---|---|---:|
| English | `README.md` | `CURRENT` |
| Arabic | `README.ar.md` | `REFRESH_NEEDED` |
| German | `README.de.md` | `REFRESH_NEEDED` |
| Spanish | `README.es.md` | `REFRESH_NEEDED` |
| French | `README.fr.md` | `REFRESH_NEEDED` |
| Hindi | `README.hi.md` | `REFRESH_NEEDED` |
| Italian | `README.it.md` | `REFRESH_NEEDED` |
| Japanese | `README.ja.md` | `REFRESH_NEEDED` |
| Russian | `README.ru.md` | `CURRENT` |
| Simplified Chinese | `README.zh-CN.md` | `REFRESH_NEEDED` |

## D1 — entry and use documents

D1 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Their Quick Start documents remain `CURRENT` because Reader RC-4 does not change Quick Start operational semantics.

| Language | Locale index | Quick Start | Status | Implementation boundary |
|---|---:|---:|---:|---:|
| Arabic | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| German | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Spanish | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| French | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Hindi | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Italian | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Japanese | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Russian | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| Simplified Chinese | `CURRENT` | `CURRENT` | `REFRESH_NEEDED` | `REFRESH_NEEDED` |

## D2 — reviewer and safety documents

D2 remains complete for all nine supported locales. Reader RC-4 does not change the D2 safety/reviewer source semantics, so the existing immutable D2 source checkpoint remains valid.

| Language | Reviewer Guide | Safety / privacy / failures |
|---|---:|---:|
| Arabic | `CURRENT` | `CURRENT` |
| German | `CURRENT` | `CURRENT` |
| Spanish | `CURRENT` | `CURRENT` |
| French | `CURRENT` | `CURRENT` |
| Hindi | `CURRENT` | `CURRENT` |
| Italian | `CURRENT` | `CURRENT` |
| Japanese | `CURRENT` | `CURRENT` |
| Russian | `CURRENT` | `CURRENT` |
| Simplified Chinese | `CURRENT` | `CURRENT` |

## D3 — architecture and storage authority

D3 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. The Russian refresh distinguishes bounded RC-1/RC-2/RC-3/RC-4 implementation from the absent dedicated/full autonomous Reader while preserving physical L3 != strict Canon, read-only public queries, SQLite ordinary runtime, PostgreSQL `active=false`, import-not-activation, `coverage != comprehension proof`, `pass completion != comprehension proof`, `EXTRACTED_PROPOSITION != verified fact` and `Reader candidate != admitted evidence`.

| Language | Architecture overview | Storage / authority boundaries |
|---|---:|---:|
| Arabic | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| German | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Spanish | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| French | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Hindi | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Italian | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Japanese | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Russian | `CURRENT` | `CURRENT` |
| Simplified Chinese | `REFRESH_NEEDED` | `REFRESH_NEEDED` |

## D4 — project, grant, governance and glossary

D4 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Russian preserves submitted / under review / not awarded, approximate €50,000 planning-only, budget change none, pre-agreement baseline not funded delta, SQLite ordinary active local-first, PostgreSQL `active=false`, RC-1/RC-2/RC-3/RC-4 bounded implementation, dedicated/full Reader absent, pass completion not comprehension, extracted proposition not verified fact, Reader candidate not admitted evidence, and no legal/GDPR/security/native-speaker certification claims.

| Language | Grant Overview | Glossary |
|---|---:|---:|
| Arabic | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| German | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Spanish | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| French | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Hindi | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Italian | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Japanese | `REFRESH_NEEDED` | `REFRESH_NEEDED` |
| Russian | `CURRENT` | `CURRENT` |
| Simplified Chinese | `REFRESH_NEEDED` | `REFRESH_NEEDED` |

## D5 — extended reference documents

D5 Reader-dependent detail translations are `CURRENT` in Russian; eight other supported locales are `REFRESH_NEEDED`. Detailed ADR/profile, security/privacy/GDPR/legal, tests/benchmarks/CI, machine-readable state, AI/audit, research/RFC and grant evidence remain `ENGLISH_ONLY_BY_DESIGN`. Historical snapshots remain `RETIRED`.

| Language | Extended Reference Guide |
|---|---:|
| Arabic | `REFRESH_NEEDED` |
| German | `REFRESH_NEEDED` |
| Spanish | `REFRESH_NEEDED` |
| French | `REFRESH_NEEDED` |
| Hindi | `REFRESH_NEEDED` |
| Italian | `REFRESH_NEEDED` |
| Japanese | `REFRESH_NEEDED` |
| Russian | `CURRENT` |
| Simplified Chinese | `REFRESH_NEEDED` |

The resolved D5 inventory intentionally contains **64 `REFRESH_NEEDED` localized documents** after RC-4: eight root localized READMEs plus seven Reader-dependent detail document types across eight locales. This is the same tracked translation set as RC-3, now stale against a newer immutable source checkpoint; it is not an unresolved classification error.

## Current family summary

| Document family | Current multilingual state |
|---|---|
| Root README | Russian `CURRENT`; 8 localized root READMEs `REFRESH_NEEDED` against RC-4 |
| D1 entry/use | Russian Reader details `CURRENT`; 8 locale Reader details `REFRESH_NEEDED`; Quick Start all `CURRENT` |
| D2 reviewer/safety | all nine supported locales `CURRENT` |
| D3 architecture/storage authority | Russian `CURRENT`; 8 locales `REFRESH_NEEDED` |
| D4 project/grant context | Russian `CURRENT`; 8 locales `REFRESH_NEEDED` |
| D5 extended references | Russian `CURRENT`; 8 locales `REFRESH_NEEDED` |

## Completion rule

A document becomes `CURRENT` only with equivalent semantic coverage, an exact source checkpoint, valid links, claims no stronger than English, green relevant CI and a merged PR. Native-speaker editorial certification is not implied unless it actually occurred.
