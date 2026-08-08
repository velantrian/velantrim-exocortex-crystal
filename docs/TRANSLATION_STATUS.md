# Translation status and phased rollout

## Purpose

This ledger is the authoritative freshness map for multilingual Crystal documentation.
English remains the primary source and conflict resolver; translated public documentation
is a maintained product surface and cannot strengthen implementation, security, authority
or grant claims.

**Root README source checkpoint:** `main@e521440e9bb188d88475f17dd5bcdd161b314605`.  
**Russian D1 source checkpoint:** `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`.  
**Remaining-locale D1 source checkpoint:** `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130`.

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

D1 is complete for all nine supported locales. Each locale has a current documentation
index, Quick Start, Status and Implementation Status tied to an exact English checkpoint.

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

D1 current files for every locale:

```text
docs/<locale>/README.md
docs/<locale>/QUICKSTART.md
docs/<locale>/STATUS.md
docs/<locale>/IMPLEMENTATION_STATUS.md
```

The `docs-status` gate validates exact checkpoints, manifest membership, local links,
mutable evidence markers and capability/grant non-claims across all current D1 files.

## Remaining document families

Presence does not prove freshness. Until a file is checked against a recorded English
checkpoint, it remains `REFRESH_NEEDED`.

| Document family | Current multilingual state | Next phase |
|---|---|---|
| Root README | all nine supported locales `CURRENT` | maintain |
| Quick Start / Status / implementation boundary | all nine supported locales `CURRENT` | maintain |
| Reviewer Guide | `REFRESH_NEEDED` | D2 |
| Security / privacy / failure modes | mostly English or stale partial translations | D2 |
| Architecture and stable ADRs | mostly English | D3 |
| Grant overview / roadmap / glossary | partial and `REFRESH_NEEDED` | D4 |
| Extended reference corpus | mixed / English | D5 |

## Planned sequence

### D2 — reviewer and safety documents

Translate or refresh Reviewer Guide, security, privacy and failure-mode explanations while
preserving all certification and production-readiness non-claims.

### D3 — architecture documents

Translate stable architecture overviews and selected mature ADR/profile documents. Preserve
Guardian, TruthGate, strict Canon, evidence and migration boundaries.

### D4 — project and grant documents

Refresh grant overview, roadmap, glossary, governance and contribution guidance without
claiming an NLnet award or re-budgeting merged baseline work.

### D5 — extended reference documents

Translate remaining stable documents according to reader value and maintenance cost. Volatile
AI-agent logs and low-level CI records may remain English with exact evidence links.

## Completion rule

A document becomes `CURRENT` only when it has equivalent semantic coverage, an exact source
checkpoint, current mutable facts, valid local links, claims no stronger than English, green
relevant CI and a merged PR. Native-speaker editorial certification is not implied unless it
actually occurred.
