# Localization and translation policy

## Status

This is the active multilingual documentation contract. It supersedes the permanent
summary-only model introduced by PR #339.

English remains the primary working, source and conflict-resolving language. Crystal is not
an English-only documentation project. English-first means **source-first**, not English-only.

## 1. Authority and translation

- Merged implementation, executable tests, exact CI and current English technical evidence
  resolve disagreements.
- Translation does not create a separate architecture, security, grant or epistemic authority.
- A translation must not strengthen capabilities, remove limitations or turn proposed work
  into implemented work.
- `docs/TRANSLATION_STATUS.md` is the authoritative freshness ledger. Inline source/status
  comments are trace metadata and do not replace the ledger.

## 2. Root README contract

`README.md` and every supported `README.<locale>.md` are full public presentations of the
same project.

Each completed README preserves equivalent coverage of:

- purpose and positioning;
- meaningful emoji and visual hierarchy;
- mind map;
- ASCII information flow;
- module tree;
- memory/evidence tables;
- SQLite and PostgreSQL/pgvector boundaries;
- classic-RAG comparison;
- public read-only query boundary;
- explicit contradiction decisions;
- quick start and navigation;
- verified evidence and explicit non-claims;
- contribution and license information.

Literal sentence order or byte-for-byte identity is not required. Semantic and visual
coverage are required. A localized root README must not be permanently reduced to a short
orientation summary.

PR #340 restores this full README layer for all nine supported locales:
Arabic, German, Spanish, French, Hindi, Italian, Japanese, Russian and Simplified Chinese.

## 3. Broader documents are translated progressively

The full documentation corpus is not required in one PR. Runtime and architecture work must
not wait until every translated document is current.

```text
English implementation and technical documentation
        ↓
exact-head review, tests and merge
        ↓
translation impact assessment
        ↓
one language or document-family PR
        ↓
source checkpoint + freshness ledger + link/claim review
        ↓
next translation phase
```

A translation PR may update one language, several related languages or one stable document
family. Completed phases merge independently.

## 4. Document translation phases

### D1 — entry and use

- locale documentation indexes;
- Quick Start;
- current Status and implementation boundary.

### D2 — reviewer and safety

- Reviewer Guide;
- Security and privacy explanations;
- failure modes.

### D3 — architecture

- stable architecture overview;
- trust, Canon, evidence and migration boundaries;
- selected mature ADRs and profiles.

### D4 — project and grant context

- roadmap;
- grant overview and funded-delta explanation;
- glossary;
- governance and contribution guidance.

### D5 — extended reference corpus

Translate remaining stable, high-value reference documents according to reader value,
maturity and maintenance cost. Volatile AI-agent logs and exact low-level CI records may
remain English when a translated explanation links to the authoritative evidence.

## 5. Freshness states

Every tracked translation uses one of:

- `CURRENT` — reviewed against the recorded English source checkpoint;
- `IN_PROGRESS` — active work exists but has not merged;
- `REFRESH_NEEDED` — a translation exists but facts or structure lag;
- `ORIENTATION_ONLY` — temporary safe navigation pending a full translation;
- `NOT_STARTED` — no maintained translation yet;
- `RETIRED` — intentionally no longer maintained, with rationale.

All nine root README translations become `CURRENT` with the merge of PR #340. Existing
translated document packs remain `REFRESH_NEEDED` until separately checked.

## 6. Change discipline

Implementation PRs:

- update English technical and public sources first;
- record whether translated public meaning changed;
- avoid mixing broad translation work into runtime changes.

Translation PRs:

- identify the exact English source checkpoint;
- preserve diagrams, tables and reader experience;
- reconcile tests, coverage, runtime checkpoint and grant state;
- check local links and code blocks;
- retain stable API identifiers;
- use natural target-language prose rather than mechanical word-for-word translation;
- list documents deliberately deferred to later phases.

## 7. Evidence and claim safety

A translated document may carry current verified values, link to current English evidence or
be visibly marked stale. It may never claim a newer or stronger checkpoint than the English
source.

The following distinctions must survive translation:

```text
physical L3 graph != strict Canon
retrieval score   != evidence
model output      != independent factual source
migration receipt != claim evidence
successful import != backend activation
process-local lease != distributed coordination
```

## 8. Supported root locales

- Arabic — `README.ar.md`;
- German — `README.de.md`;
- Spanish — `README.es.md`;
- French — `README.fr.md`;
- Hindi — `README.hi.md`;
- Italian — `README.it.md`;
- Japanese — `README.ja.md`;
- Russian — `README.ru.md`;
- Simplified Chinese — `README.zh-CN.md`.

Additional languages require a maintenance plan and an entry in the status ledger.

## 9. CI expectations

CI verifies objective invariants without pretending to replace language review:

- all supported root files and locale indexes exist;
- every root README has a full-presentation structural floor;
- current checkpoint, capability and non-claim markers are present;
- local links resolve;
- the manifest and translation ledger agree;
- no maximum-size rule rejects a full translation;
- broader translated documents remain explicitly marked until reviewed.

Human or language-model review remains necessary for natural language, semantic fidelity,
terminology and RTL/diagram quality.

## 10. Notion synchronization

Notion records the durable language decision, phase status, final merge evidence and next
translation families. It does not duplicate the translated files. GitHub remains the public
source for all translations and their maintenance ledger.
