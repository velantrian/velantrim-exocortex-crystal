# Translation status and phased rollout

## Purpose

This ledger is the authoritative freshness map for multilingual Crystal documentation. English remains the primary source and conflict resolver; translations cannot strengthen implementation, security, authority, legal or grant claims.

**Root README source checkpoint:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`.  
**D1 source checkpoint:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`.  
**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.  
**D3 source checkpoint:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`.  
**D4 source checkpoint:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`.  
**D5 source checkpoint:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`.

**Policy:** [`LOCALIZATION_POLICY.md`](LOCALIZATION_POLICY.md).  
**D5 policy:** [`EXTENDED_REFERENCE_POLICY.md`](EXTENDED_REFERENCE_POLICY.md).  
**Tracking issue:** [#341](https://github.com/velantrian/velantrim-exocortex-crystal/issues/341).

## Reader reconciliation boundary

The 2026-08-10 refresh reconciles every affected public multilingual surface with the merged Reader foundation:

```text
reader_core_rc1_skeleton       = true
reader_core_rc2_structural_map = true
dedicated_reader_core          = false
```

RC-1 and RC-2 are bounded implemented/tested foundations. They do not imply automatic parsing, LLM/provider Reader orchestration, embeddings/ANN/vector DB, multi-pass/cross-document reasoning or comprehension proof.

## Root README status

| Language | File | Status |
|---|---|---:|
| English | `README.md` | `CURRENT` |
| Arabic | `README.ar.md` | `CURRENT` |
| German | `README.de.md` | `CURRENT` |
| Spanish | `README.es.md` | `CURRENT` |
| French | `README.fr.md` | `CURRENT` |
| Hindi | `README.hi.md` | `CURRENT` |
| Italian | `README.it.md` | `CURRENT` |
| Japanese | `README.ja.md` | `CURRENT` |
| Russian | `README.ru.md` | `CURRENT` |
| Simplified Chinese | `README.zh-CN.md` | `CURRENT` |

## D1 — entry and use documents

D1 is complete for all nine supported locales.

| Language | Locale index | Quick Start | Status | Implementation boundary |
|---|---:|---:|---:|---:|
| Arabic | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| German | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| Spanish | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| French | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| Hindi | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| Italian | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| Japanese | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| Russian | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |
| Simplified Chinese | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |

## D2 — reviewer and safety documents

D2 is complete for all nine supported locales. Reader RC-1/RC-2 did not change the D2 safety/reviewer source semantics, so the existing immutable D2 source checkpoint remains valid.

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

D3 is complete for all nine supported locales. The refresh distinguishes bounded RC-1/RC-2 implementation from the absent dedicated Reader runtime while preserving physical L3 != strict Canon, read-only public queries, SQLite ordinary runtime, PostgreSQL `active=false` and import-not-activation.

| Language | Architecture overview | Storage / authority boundaries |
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

## D4 — project, grant, governance and glossary

D4 is complete for all nine supported locales. It preserves submitted / under review / not awarded, approximate €50,000 planning-only, budget change none, pre-agreement baseline not funded delta, SQLite ordinary active local-first, PostgreSQL `active=false`, RC-1/RC-2 bounded implemented, dedicated Reader absent, and no legal/GDPR/security/native-speaker certification claims.

| Language | Grant Overview | Glossary |
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

## D5 — extended reference documents

D5 is complete for all nine supported locales. Each locale has one `CURRENT` Extended Reference Guide pinned to the reconciled English source checkpoint.

| Language | Extended Reference Guide |
|---|---:|
| Arabic | `CURRENT` |
| German | `CURRENT` |
| Spanish | `CURRENT` |
| French | `CURRENT` |
| Hindi | `CURRENT` |
| Italian | `CURRENT` |
| Japanese | `CURRENT` |
| Russian | `CURRENT` |
| Simplified Chinese | `CURRENT` |

Detailed ADR/profile, security/privacy/GDPR/legal, tests/benchmarks/CI, machine-readable state, AI/audit, research/RFC and grant evidence remain `ENGLISH_ONLY_BY_DESIGN`. Historical snapshots remain `RETIRED`. The resolved inventory has zero `REFRESH_NEEDED` documents after this reconciliation.

## Current family summary

| Document family | Current multilingual state |
|---|---|
| Root README | all nine supported locales `CURRENT` |
| D1 entry/use | all nine supported locales `CURRENT` |
| D2 reviewer/safety | all nine supported locales `CURRENT` |
| D3 architecture/storage authority | all nine supported locales `CURRENT` |
| D4 project/grant context | all nine supported locales `CURRENT` |
| D5 extended references | all nine supported locales `CURRENT` |

## Completion rule

A document becomes `CURRENT` only with equivalent semantic coverage, an exact source checkpoint, valid links, claims no stronger than English, green relevant CI and a merged PR. Native-speaker editorial certification is not implied unless it actually occurred.
