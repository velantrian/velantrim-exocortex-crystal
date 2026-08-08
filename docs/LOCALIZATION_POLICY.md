# Localization and translation policy

## Status

This document defines the active repository policy for multilingual documentation.
It supersedes the summary-only localization model introduced by PR #339.

English remains the primary working and source language, but multilingual documentation
is an intended maintained product surface rather than a permanently reduced summary layer.

## 1. Language authority

- Implementation, tests, CI evidence and the merged English source documents remain the
  conflict resolver when translations disagree.
- English is written and verified first so engineering work has one stable review surface.
- Translation does not create a separate architecture, security, grant or epistemic authority.
- A translation must not strengthen capabilities, remove limitations or convert proposed
  work into implemented work.

English-first means **source-first**, not English-only.

## 2. README parity target

The root `README.md` and every supported `README.<locale>.md` are intended to be full public presentations of the same project.

A completed README translation must preserve equivalent coverage of:

- project purpose and positioning;
- the visual language of the source, including meaningful emoji, mind maps, ASCII diagrams,
  architecture trees and tables;
- verified capability and evidence boundaries;
- current limitations and explicit non-claims;
- storage/runtime boundaries;
- quick-start instructions;
- documentation navigation, contribution and licensing information.

Literal sentence order or byte-for-byte structure is not required. Semantic and visual
coverage is required. Localized README files must not be permanently reduced to short
orientation summaries.

## 3. Phased translation instead of an all-at-once gate

Runtime and architecture work must not be blocked until every language is updated.
Translation proceeds in dedicated documentation-only PRs after the English baseline is
merged and stable.

The normal sequence is:

```text
English implementation and documentation
        ↓
exact-head review, tests and merge
        ↓
translation status assessment
        ↓
one or more language/document translation PRs
        ↓
locale-specific review and link/status validation
```

A localization PR may update one language, several related languages or one document family.
It is not required to update every locale in the same PR.

## 4. Translation phases

### Phase A — public entry surface

1. full root README translation;
2. locale documentation index;
3. quick start;
4. current status and implementation boundary.

### Phase B — reviewer and safety surface

1. reviewer guide;
2. security policy;
3. privacy/GDPR explanations;
4. architecture overview and failure modes.

### Phase C — project and grant context

1. roadmap and grant overview;
2. glossary;
3. selected stable ADRs and architecture profiles;
4. contribution and governance guidance.

### Phase D — extended reference corpus

Translate remaining stable documents according to reader value, maturity and maintenance
cost. Volatile AI-agent logs, exact CI records and low-level implementation evidence may
remain English when a translated explanation links to the authoritative source.

## 5. Freshness states

Every maintained translation is tracked in `docs/TRANSLATION_STATUS.md` using one of:

- `CURRENT` — reviewed against the recorded English source checkpoint;
- `IN_PROGRESS` — active translation work exists but is not merged;
- `REFRESH_NEEDED` — full or partial translation exists but its facts or structure lag;
- `ORIENTATION_ONLY` — temporary safe summary pending full translation;
- `NOT_STARTED` — no maintained translation yet;
- `RETIRED` — intentionally no longer maintained, with rationale.

`ORIENTATION_ONLY` is a temporary migration state, not the target README format.

## 6. Change discipline

Implementation PRs:

- update authoritative English surfaces;
- record whether translated public meaning changed;
- do not mix broad translation work into runtime changes unless the change is tiny and safe.

Localization PRs:

- identify the exact English source checkpoint;
- preserve diagrams, tables and reader experience where meaningful;
- reconcile mutable evidence such as tests, coverage, runtime checkpoint and grant state;
- check local links and code blocks;
- retain stable API identifiers in their programmatic form;
- use natural target-language prose rather than mechanical word-for-word translation;
- list documents deliberately left for later phases.

## 7. Evidence and status claims

Mutable evidence must not silently remain stale in a translation. A translated document may:

1. carry the current verified value;
2. link to the English evidence and label the local value as historical; or
3. omit a volatile number when the document is explicitly marked `REFRESH_NEEDED` or
   `ORIENTATION_ONLY`.

A localized document may never claim a newer or stronger checkpoint than the verified English
source.

## 8. Supported root README locales

The current supported root README locale set is:

- Arabic — `README.ar.md`;
- German — `README.de.md`;
- Spanish — `README.es.md`;
- French — `README.fr.md`;
- Hindi — `README.hi.md`;
- Italian — `README.it.md`;
- Japanese — `README.ja.md`;
- Russian — `README.ru.md`;
- Simplified Chinese — `README.zh-CN.md`.

Additional languages require an owner or maintenance plan and must be added to the translation
status ledger.

## 9. CI expectations

CI should verify objective invariants without pretending to judge translation quality fully:

- supported files and locale indexes exist;
- translation status entries exist;
- local links resolve;
- source checkpoints use an explicit format;
- current translations do not exceed English capability claims;
- full README translations are not rejected merely because they are large;
- temporary orientation files are clearly identified as temporary.

Human or language-model review remains necessary for semantic fidelity, natural language and
visual parity.

## 10. Notion synchronization

Notion records the durable localization decision, phase status and final merge evidence. It
does not duplicate every translated document. GitHub remains the complete public source for
the translated files and their maintenance ledger.
