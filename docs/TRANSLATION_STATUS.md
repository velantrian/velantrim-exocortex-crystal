# Translation status and phased rollout

## Purpose

This ledger is the authoritative freshness map for multilingual Crystal documentation.
English remains the primary source and conflict resolver; translated public documentation
cannot strengthen implementation, security, authority or grant claims.

**Root README source checkpoint:** `main@e521440e9bb188d88475f17dd5bcdd161b314605`.  
**Russian D1 source checkpoint:** `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`.  
**Remaining-locale D1 source checkpoint:** `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130`.  
**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.  
**D3 source checkpoint:** `main@208f1c772ee3a112cb803d2413c120bef23adb05`.

**Policy:** [`LOCALIZATION_POLICY.md`](LOCALIZATION_POLICY.md).  
**Tracking issue:** [#341](https://github.com/velantrian/velantrim-exocortex-crystal/issues/341).

## Root README status

All nine supported localized root READMEs are `CURRENT`; English remains the primary source.

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
Safety/Privacy/Failure summary. Detailed Security, Privacy, GDPR and Failure Modes contracts
remain authoritative English references.

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

D3 is complete for all nine supported locales. Each locale has a current Architecture
Overview and Storage/Authority Boundaries document derived from the corrected English source
checkpoint merged by PR #347. Detailed profiles, migration contracts and ADR-021 remain
conflict-resolving English technical contracts.

| Language | Architecture overview | Storage / authority boundaries | Source checkpoint |
|---|---:|---:|---|
| Arabic | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| German | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| Spanish | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| French | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| Hindi | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| Italian | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| Japanese | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| Russian | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |
| Simplified Chinese | `CURRENT` | `CURRENT` | `main@208f1c772ee3a112cb803d2413c120bef23adb05` |

D3 preserves physical-L3/strict-Canon separation, read-only public queries, SQLite ordinary
runtime, PostgreSQL `active=false`, import-not-activation and Reader-Core-not-implemented
boundaries. Native-speaker editorial certification is not implied.

## Remaining document families

| Document family | Current multilingual state | Next phase |
|---|---|---|
| Root README | all nine supported locales `CURRENT` | maintain |
| D1 entry/use | all nine supported locales `CURRENT` | maintain |
| D2 reviewer/safety | all nine supported locales `CURRENT` | maintain |
| D3 architecture/storage authority | all nine supported locales `CURRENT` | maintain |
| D4 project/grant context | `REFRESH_NEEDED` translated document packs | D4 |
| D5 extended reference corpus | mixed / English | D5 |

### D4 — project and grant documents

Refresh grant overview, roadmap, glossary, governance and contribution guidance without
claiming an NLnet award or re-budgeting merged baseline work.

### D5 — extended references

Prioritize stable reader-value documents. Volatile AI-agent logs and low-level CI records may
remain English with exact evidence links and an explicit rationale.

## Completion rule

A document becomes `CURRENT` only with equivalent semantic coverage, an exact source
checkpoint, valid links, claims no stronger than English, green relevant CI and a merged PR.
Native-speaker editorial certification is not implied unless it actually occurred.
