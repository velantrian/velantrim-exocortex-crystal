# 🌐 Crystal Localization Policy

## Decision

English is Crystal's sole authoritative working language.

All engineering decisions, code-facing contracts, architecture, ADRs, implementation status,
test evidence, security statements, grant claims, roadmaps and AI-agent instructions are
written and maintained in English first. When localized text differs from English, the English
source and merged implementation evidence prevail.

## Selective localization scope

Crystal does **not** require a full translation of the documentation corpus.

| Surface | Language rule |
|---|---|
| `README.md` | authoritative English public contract |
| `README.<locale>.md` | concise non-authoritative orientation summary |
| `docs/<locale>/README.md` | locale index and staleness warning |
| selected quick starts or glossaries | optional best-effort snapshots |
| architecture, ADR, status, tests, security, grant, roadmap, `docs/ai/*` | English only and normative |

A localized README should contain only the stable public layer needed to understand the
project: purpose, verified checkpoint, central capabilities, critical non-claims, storage
boundary, quick start and links to current English evidence.

## Required workflow

```text
implement and document in English
→ merge and verify the English baseline
→ open a separate docs-only localization PR
→ record the exact English source checkpoint
→ preserve capability and non-claim boundaries
→ run localization/status/link validation
```

Ordinary implementation PRs must not fan out mutable checkpoint numbers across every
translation. A localization PR is created only when the English public contract has materially
changed and the localized summaries would otherwise mislead readers.

## Translation invariants

A localization must not:

- introduce a capability absent from the English source;
- strengthen a security, privacy, legal, GDPR, production-readiness or grant claim;
- translate operational evidence into epistemic evidence;
- imply that PostgreSQL import means activation or ordinary runtime selection;
- rename stable API, CLI, enum, status or configuration identifiers;
- conceal that it may lag behind current English documentation.

The following meanings remain exact in every language:

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

## Checkpoint and staleness contract

Every maintained localized README contains a machine-readable source marker:

```html
<!-- localization-source: main@<english-source-sha> -->
```

Every locale index contains:

```html
<!-- localization-index-source: main@<english-source-sha> -->
```

The marker identifies the English contract used for reconciliation; it is not a claim that the
localized file is a complete translation of that commit. Current implementation truth remains
`main`, executable tests, CI, `TEST_REPORT.md` and the implementation manifest.

## Current reconciliation

The nine localized README summaries and locale indexes were reconciled from:

`main@e521440e9bb188d88475f17dd5bcdd161b314605`

That source records runtime PR #337 at checkpoint
`bbd816c09dd39a02e6de6c1014438490572f40f6` with 2078 passed / 13 skipped, 100.00% line
coverage, 9/9 permanent CI jobs and a successful real PostgreSQL/pgvector integration job.
The PostgreSQL target remains `active=false` and outside ordinary read/write runtime
composition.
