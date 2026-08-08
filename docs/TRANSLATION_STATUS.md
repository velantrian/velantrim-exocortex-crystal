# Translation status and phased rollout

## Purpose

This ledger is the authoritative freshness map for multilingual Crystal documentation.
English remains the primary source and conflict resolver; translated public documentation is
a maintained product surface.

**English source checkpoint for the root README reconciliation:**
`main@e521440e9bb188d88475f17dd5bcdd161b314605`.

**D1 Russian source checkpoint:** `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`.

**Policy:** [`LOCALIZATION_POLICY.md`](LOCALIZATION_POLICY.md).  
**Tracking issue:** [#341](https://github.com/velantrian/velantrim-exocortex-crystal/issues/341).

## Root README status

PR #340 restores full visual and semantic README coverage for every supported language.
The files include purpose, evidence boundaries, mind maps, ASCII architecture, module trees,
tables, quick start, navigation and non-claims.

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

The inline `localization-status` comments record branch-time workflow state. This ledger is
the final freshness authority after merge.

## D1 — entry and use documents

The first language tranche is Russian. It establishes the repeatable D1 contract before the
same document family is reconciled for the remaining locales.

| Language | Locale index | Quick Start | Status | Implementation boundary | Source checkpoint |
|---|---:|---:|---:|---:|---|
| Russian | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` | `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c` |
| Arabic | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |
| German | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |
| Spanish | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |
| French | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |
| Hindi | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |
| Italian | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |
| Japanese | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |
| Simplified Chinese | routing current | `REFRESH_NEEDED` | `REFRESH_NEEDED` | `REFRESH_NEEDED` | — |

Russian D1 current files:

- `docs/ru/README.md`;
- `docs/ru/QUICKSTART.md`;
- `docs/ru/STATUS.md`;
- `docs/ru/IMPLEMENTATION_STATUS.md`.

## Remaining document families

Presence does not prove freshness. Until a file is checked against a recorded English
checkpoint, it remains `REFRESH_NEEDED`.

| Document family | Current multilingual state | Next phase |
|---|---|---|
| Root README | all nine supported locales `CURRENT` | maintain |
| Quick Start / Status / implementation boundary | Russian `CURRENT`; eight locales pending | D1 |
| Reviewer Guide | `REFRESH_NEEDED` | D2 |
| Security / privacy / failure modes | mostly English or stale partial translations | D2 |
| Architecture and stable ADRs | mostly English | D3 |
| Grant overview / roadmap / glossary | partial and `REFRESH_NEEDED` | D4 |
| Extended reference corpus | mixed / English | D5 |

## Planned sequence

### D1 — entry and use documents

Continue Quick Start, Status and implementation-boundary reconciliation for the remaining
eight locales. Each completed translation records the exact English source checkpoint and is
protected by `docs-status`.

### D2 — reviewer and safety documents

Translate or refresh Reviewer Guide, security, privacy and failure-mode explanations.

### D3 — architecture documents

Translate stable architecture overviews and selected mature ADR/profile documents. Preserve
Guardian, TruthGate, strict Canon, evidence and migration boundaries.

### D4 — project and grant documents

Refresh grant overview, roadmap, glossary, governance and contribution guidance without
claiming an NLnet award or re-budgeting merged baseline work.

### D5 — extended reference documents

Translate the remaining stable corpus according to reader value and maintenance cost.

## Completion rule

A document becomes `CURRENT` only when:

- it has equivalent semantic coverage for its intended reader;
- its exact English source checkpoint is recorded;
- mutable facts are reconciled or linked to exact English evidence;
- local links pass;
- capability, security, authority and grant claims are no stronger than English;
- relevant CI, including `docs-status`, is green;
- the translation PR is merged and any durable governance change is synchronized with Notion.

Native-speaker editorial certification is not implied unless it actually occurred.
