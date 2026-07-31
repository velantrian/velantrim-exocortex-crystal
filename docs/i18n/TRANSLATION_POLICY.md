# 🌐 Translation Policy

This document defines the maintenance contract for localized Crystal documentation.
It does not change runtime behavior, grant scope, API contracts, or the authority of the English documentation.

## 1. Authority

```text
GitHub main implementation     = implementation truth
English README and docs        = canonical documentation
Localized documentation        = maintained explanatory projection
Notion                         = synchronized strategy and grant map
Titan / Full Exo-Cortex        = separate research track
```

When a translation conflicts with the English source, the English source and `TEST_REPORT.md` prevail.

## 2. Supported locales

The machine-readable source is [`locales.json`](./locales.json). A locale is supported only when it has:

- a root project README;
- a documentation index;
- Quickstart;
- Status;
- Reviewer Guide;
- Grant Overview;
- Glossary;
- top-and-bottom language navigation;
- passing `scripts/check_i18n.py` validation.

## 3. Claim discipline

A translation must never strengthen the English source. In particular, it must not turn:

- `under review` into `funded`;
- `research-grade` into `production-ready`;
- `GDPR-relevant mechanisms` into `GDPR certified`;
- `security controls` into `security certified`;
- `verified evidence` into `absolute truth`;
- a future Titan/RFC concept into a current Crystal capability;
- a local optional interface into a mandatory cloud dependency.

## 4. Preserved identifiers

Contract identifiers, code symbols, CLI commands, environment variables, paths, and API endpoints remain unchanged.
The machine-enforced core list is maintained in `locales.json` and includes:

```text
TruthGate
Guardian
CanonicalView
TRACE
Receipt
Canon
```

Additional identifiers such as `ProvenanceChain`, `WORLD_FACT`, and `LLM_OUTPUT` must also remain unchanged wherever they occur, but older glossaries are not required to introduce terms absent from their source version.

Localized prose may explain these terms, but must not rename them.

## 5. Synchronization markers

Two markers are intentionally separate:

- **canonical content ref** — the English content checkpoint used for translation;
- **localization bundle ref** — the repository checkpoint at which the full language bundle was assembled.

Neither marker is a runtime certification. A navigation-only change does not require retranslation of unchanged technical prose.
A substantive English claim change does require review of every affected translation.

## 6. Required review for translation PRs

Every localization PR must confirm:

- [ ] only intended documentation/tooling files changed;
- [ ] all relative language links resolve;
- [ ] the language selector appears near the beginning and at the end;
- [ ] required documents exist for every supported locale;
- [ ] preserved identifiers remain present in each localized glossary;
- [ ] no grant, funding, certification, compliance, or capability claim was strengthened;
- [ ] `python scripts/check_i18n.py` passes;
- [ ] the full repository CI is green.

## 7. Adding another language

New languages are not accepted merely by adding one README. A proposal must include:

1. a maintainer or review path for that language;
2. all seven required localized documents;
3. native-language technical review where practical;
4. updated `locales.json`;
5. navigation updates across the existing language family;
6. passing i18n and repository CI gates.

The current ten-language set is considered sufficient for the present project stage. New languages should be added only when there is a concrete reviewer, contributor, grant, or user need.

## 8. Compact navigation policy

The selector should remain one concise Markdown line at the top and bottom of counterpart documents. Long descriptive language indexes belong in the root README and locale index pages, not in every technical document.

---

See also: [`STATUS.md`](./STATUS.md) and [`locales.json`](./locales.json).
