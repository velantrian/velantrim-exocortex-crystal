# Translation status and phased rollout

## Purpose

This ledger is the authoritative freshness map for multilingual Crystal documentation.
English remains the primary source and conflict resolver; translated public documentation
cannot strengthen implementation, security, authority or grant claims.

**Root README source checkpoint:** `main@e521440e9bb188d88475f17dd5bcdd161b314605`.  
**Russian D1 source checkpoint:** `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`.  
**Remaining-locale D1 source checkpoint:** `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130`.  
**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.  
**D3 source reconciliation:** PR #346 is partial; a corrective merged checkpoint is required before D3 translations become `CURRENT`.

**Policy:** [`LOCALIZATION_POLICY.md`](LOCALIZATION_POLICY.md).  
**Tracking issue:** [#341](https://github.com/velantrian/velantrim-exocortex-crystal/issues/341).

## Root README status

| Language | File | Status | Source checkpoint |
|---|---|---:|---|
| English | `README.md` | `CURRENT` | primary source |
| Arabic | `README.ar.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| German | `README.de.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| Spanish | `README.es.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| French | `README.fr.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| Hindi | `README.hi.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| Italian | `README.it.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| Japanese | `README.ja.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| Russian | `README.ru.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |
| Simplified Chinese | `README.zh-CN.md` | `CURRENT` | `main@e521440e9bb188d88475f17dd5bcdd161b314605` |

## D1 — entry and use documents

D1 is complete for all nine supported locales. Every locale has a current index, Quick Start,
Status and Implementation Status tied to an exact source checkpoint.

| Language | Locale index | Quick Start | Status | Implementation boundary | Source checkpoint |
|---|---:|---:|---:|---:|---|
| Arabic | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |
| German | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |
| Spanish | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |
| French | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |
| Hindi | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |
| Italian | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |
| Japanese | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |
| Russian | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c` |
| Simplified Chinese | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130` |

## D2 — reviewer and safety documents

D2 is complete for all nine supported locales. Each locale has a current Reviewer Guide and
a current Safety/Privacy/Failure summary derived from the stable English source contract.
Detailed Security, Privacy, GDPR and Failure Modes contracts remain authoritative English
references linked from every localized summary.

| Language | Reviewer Guide | Safety / privacy / failures | Source checkpoint |
|---|---:|---:|---|
| Arabic | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| German | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| Spanish | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| French | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| Hindi | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| Italian | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| Japanese | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| Russian | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |
| Simplified Chinese | `CURRENT` | `CURRENT` | `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` |

## D3 — architecture and storage authority

The compact English Architecture Overview and Storage/Authority Boundaries exist, but the
post-merge audit of PR #346 found that the detailed architecture/profile/migration/ADR files
were not part of that PR and the D3 validator was not wired into CI. Therefore no localized
D3 file is current yet.

The corrective English source checkpoint must reconcile and validate:

```text
docs/ARCHITECTURE.md
docs/ARCHITECTURE_OVERVIEW.md
docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md
docs/architecture/DURABLE_STORAGE_PROFILE.md
docs/architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md
docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md
docs/adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md
```

After that merge, each locale will translate only the compact Architecture Overview and
Storage/Authority Boundaries, while linking to the detailed English contracts. The exact
corrective merge SHA—not PR #346—will be the D3 translation source checkpoint.

## Remaining document families

| Document family | Current multilingual state | Next phase |
|---|---|---|
| Root README | all nine supported locales `CURRENT` | maintain |
| D1 entry/use | all nine supported locales `CURRENT` | maintain |
| D2 reviewer/safety | all nine supported locales `CURRENT` | maintain |
| D3 architecture/storage authority | English correction in progress; localized `REFRESH_NEEDED` | D3 |
| Grant overview / roadmap / glossary | partial and `REFRESH_NEEDED` | D4 |
| Extended reference corpus | mixed / English | D5 |

## Planned sequence

### D3 — architecture documents

Reconcile the complete stable English source first, then translate the compact architecture
and storage/authority summaries. Preserve Guardian, TruthGate, physical-L3/strict-Canon,
evidence, SQLite ordinary-runtime and PostgreSQL `active=false` boundaries.

### D4 — project and grant documents

Refresh grant overview, roadmap, glossary, governance and contribution guidance without
claiming an NLnet award or re-budgeting merged baseline work.

### D5 — extended reference documents

Translate remaining stable documents according to reader value and maintenance cost. Volatile
AI-agent logs and low-level CI records may remain English with exact evidence links.

## Completion rule

A document becomes `CURRENT` only with equivalent semantic coverage, an exact source
checkpoint, valid links, claims no stronger than English, green relevant CI and a merged PR.
Native-speaker editorial certification is not implied unless it actually occurred.
