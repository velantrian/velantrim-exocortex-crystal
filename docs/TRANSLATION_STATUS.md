# Translation status and phased rollout

## Purpose

This ledger makes multilingual work explicit. It separates the target state from the current
state so a temporary short README is not mistaken for the permanent localization model.

**Authoritative English baseline before this correction:**
`main@25803c59a6f4a1299d57f7deeff402c5a371a1ce`.

**Policy:** [`LOCALIZATION_POLICY.md`](LOCALIZATION_POLICY.md).

## Root README rollout

| Language | File | Current state | Target | Next action |
|---|---|---:|---|---|
| English | `README.md` | `CURRENT` | Primary source and conflict resolver | Continue English-first maintenance |
| Russian | `README.ru.md` | `IN_PROGRESS` | Full visual and semantic parity | Refresh restored full README against current evidence |
| German | `README.de.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Rebuild from stable English visual baseline |
| French | `README.fr.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Translate in Romance-language phase |
| Spanish | `README.es.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Translate in Romance-language phase |
| Italian | `README.it.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Translate in Romance-language phase |
| Simplified Chinese | `README.zh-CN.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Rebuild and language-review diagrams |
| Japanese | `README.ja.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Rebuild and language-review diagrams |
| Hindi | `README.hi.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Rebuild in multilingual expansion phase |
| Arabic | `README.ar.md` | `ORIENTATION_ONLY` | Full visual and semantic parity | Rebuild with RTL-aware visual review |

`ORIENTATION_ONLY` is temporary. It does not satisfy the full README parity target.

## Existing locale document packs

The repository already contains translated locale packs such as `QUICKSTART.md`, `STATUS.md`,
`REVIEWER_GUIDE.md`, `GLOSSARY.md` and `GRANT_OVERVIEW.md` under `docs/<locale>/`.
Their presence does not prove freshness. Until each pack is checked against a recorded English
checkpoint, treat it as `REFRESH_NEEDED` unless its locale index states otherwise.

## Planned phases

### T1 — policy correction and Russian README

- remove the permanent summary-only rule;
- restore the full visual Russian README form;
- reconcile current runtime, tests, storage and grant boundaries;
- add this status ledger and CI-safe phased policy.

### T2 — German entry surface

- full German README;
- German locale index and quick-start audit;
- current status/non-claim reconciliation.

### T3 — French, Spanish and Italian entry surfaces

- full visual README parity for all three;
- shared structural review with independent language review;
- locale index and quick-start refresh.

### T4 — Simplified Chinese and Japanese entry surfaces

- full visual README parity;
- verify code blocks, diagram width and terminology consistency;
- locale index and quick-start refresh.

### T5 — Hindi and Arabic entry surfaces

- full visual README parity;
- RTL-specific review for Arabic;
- locale index and quick-start refresh.

### T6 — reviewer, architecture, safety and grant documents

Translate stable documents progressively by document family. Do not wait for the entire corpus
to be ready before merging a completed and reviewed language phase.

## Completion rule

A language reaches README `CURRENT` only when:

- it is a full presentation rather than a short summary;
- purpose, diagrams, tables, quick start, limitations and navigation have equivalent coverage;
- current mutable facts are reconciled or intentionally linked to English evidence;
- local links pass;
- capability and grant claims are no stronger than English;
- the localization PR is merged and its exact source checkpoint is recorded here.
