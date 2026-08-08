# Translation status and phased rollout

## Purpose

This ledger is the authoritative freshness map for multilingual Crystal documentation.
English remains the primary source and conflict resolver; translated public documentation is
a maintained product surface.

**English source checkpoint for the root README reconciliation:**
`main@e521440e9bb188d88475f17dd5bcdd161b314605`.

**Policy:** [`LOCALIZATION_POLICY.md`](LOCALIZATION_POLICY.md).

## Root README status

PR #340 restores full visual and semantic README coverage for every supported language.
The files include purpose, evidence boundaries, mind maps, ASCII architecture, module trees,
tables, quick start, navigation and non-claims.

| Language | File | Status after PR #340 | Source checkpoint |
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

## Existing locale document packs

The repository contains `QUICKSTART.md`, `STATUS.md`, `REVIEWER_GUIDE.md`, `GLOSSARY.md` and
`GRANT_OVERVIEW.md` under `docs/<locale>/`. Presence does not prove freshness. Until a file is
checked against a recorded English checkpoint, it remains `REFRESH_NEEDED`.

| Document family | Current multilingual state | Next phase |
|---|---|---|
| Locale index | `CURRENT` routing, document freshness labelled | maintain with every phase |
| Quick Start | `REFRESH_NEEDED` | D1 |
| Status / implementation boundary | `REFRESH_NEEDED` | D1 |
| Reviewer Guide | `REFRESH_NEEDED` | D2 |
| Security / privacy / failure modes | mostly English or stale partial translations | D2 |
| Architecture and stable ADRs | mostly English | D3 |
| Grant overview / roadmap / glossary | partial and `REFRESH_NEEDED` | D4 |
| Extended reference corpus | mixed / English | D5 |

## Planned sequence

### D1 — entry and use documents

Refresh locale indexes, Quick Start and status/implementation-boundary explanations. A PR may
complete one language or a related language group.

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
- mutable facts are reconciled or linked to exact English evidence;
- local links pass;
- capability, security, authority and grant claims are no stronger than English;
- the translation PR is merged and the source checkpoint is recorded here.
