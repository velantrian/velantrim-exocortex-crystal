# 📌 Velantrim Crystal — Current Status

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/STATUS.md) · 🇫🇷 [Français](./fr/STATUS.md) · 🇪🇸 [Español](./es/STATUS.md) · 🇮🇹 [Italiano](./it/STATUS.md) · 🇷🇺 [Русский](./ru/STATUS.md) · 🇨🇳 [简体中文](./zh-CN/STATUS.md) · 🇸🇦 [العربية](./ar/STATUS.md) · 🇯🇵 [日本語](./ja/STATUS.md)

**Status date:** 2026-07-30  
**Current implementation truth:** GitHub `main` at `cd6fd44ff4ac8c715121cae1996aa484f11ef250`  
**Current audited baseline:** [TEST_REPORT.md](../TEST_REPORT.md)

## Reading rule

```text
GitHub Crystal main = public implementation truth
Notion Crystal pages = synchronized grant and strategy map
Titan / Full Exo-Cortex = separate research laboratory
```

A document, Notion note, prototype branch or Titan component is not a current
Crystal capability unless it is implemented, tested and merged into Crystal
`main`.

## Current verified checkpoint

Merged PR #265 introduced the strict read-only HTTP query boundary:

```text
POST /ingest       → admission through Guardian + TruthGate
POST /ask          → strict read-only canonical query
GET  /receipt      → strict read-only canonical query plus receipt
```

The HTTP `/ask` and `/receipt` surfaces do not write L0/L1 or L3, transition ESM,
operate the outbox, record episode links, initialize an embedding fingerprint, or
mutate adaptive verification state.

### Residual scope

The guarantee is not generalized beyond the surfaces that were migrated:

- CLI `ask` and `receipt` remain on `core.pipeline.run()`;
- `core.pipeline.run()` remains an admission-capable compatibility path;
- MCP has no explicit canonical write tools, but search may initialize an unset
  embedding fingerprint.

These residuals are follow-up work, not hidden implementation claims.

## Verification baseline

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

CI run `30284938992` completed all seven permanent jobs successfully before merge:
Python 3.11/3.12 tests, Ruff, security, Docker build, evaluation gate and JSONL
integrity.

## Current public claim boundary

Crystal may be described as:

- local-first verifiable AI memory infrastructure;
- a source- and provenance-oriented memory core;
- a system with Guardian and TruthGate admission controls where wired;
- a system with CanonicalView, TRACE and replayable receipts where wired;
- a standard-library default runtime with optional adapters and interfaces;
- a project with GDPR-relevant erasure and restriction mechanisms;
- an independently testable open-source research-grade baseline.

Crystal must not be described as:

- Titan or the Full Personal Exo-Cortex;
- an autonomous cognitive operating system;
- conscious, alive or biologically equivalent to a brain;
- universally truthful or hallucination-free;
- legally GDPR-certified;
- security-certified or production multi-tenant ready;
- dependent on a mandatory external LLM or cloud provider.

## Grant status

The NLnet NGI0 Commons Fund proposal has been submitted and is under review. The
repository does not claim that funding has been awarded.

Grant change control follows:

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

Already-merged work remains baseline and is not counted again as a paid
milestone. Current grant controls are maintained in:

- [GRANT_NLNET_SCOPE.md](./GRANT_NLNET_SCOPE.md)
- [grants/baseline-funded-delta-matrix.md](./grants/baseline-funded-delta-matrix.md)
- [grants/funding-use-plan.md](./grants/funding-use-plan.md)

## Evaluation replay decision

Titan's deterministic replay implementation has been reviewed as prior art. It is
not copied into Crystal runtime by this synchronization.

Current classification:

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

Crystal already has `core/eval.py`, `scripts/eval_gate.py` and the broader
trajectory replay RFC. Any future replay implementation must extend that existing
stack after the grant baseline is formally fixed, use a separate RFC/PR, remain
offline and non-authoritative, and preserve TruthGate and query-path boundaries.

See [grants/evaluation-replay-adoption.md](./grants/evaluation-replay-adoption.md).

## Research and draft PR rule

Open research or branding PRs are not implementation truth. Before merge they
must be rebased against current `main`, re-audited for grant wording and checked
for conflicts with this status document.

## Canonical reviewer path

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [REVIEWER_DEMO.md](./REVIEWER_DEMO.md)
3. [../TEST_REPORT.md](../TEST_REPORT.md)
4. [ARCHITECTURE.md](./ARCHITECTURE.md)
5. [EVAL.md](./EVAL.md)
6. [GRANT_NLNET_SCOPE.md](./GRANT_NLNET_SCOPE.md)

Localized reviewer paths:

- 🇩🇪 [Reviewer-Leitfaden](./de/REVIEWER_GUIDE.md) · [Schnellstart](./de/QUICKSTART.md) · [Grant-Übersicht](./de/GRANT_OVERVIEW.md)
- 🇫🇷 [Guide reviewer](./fr/REVIEWER_GUIDE.md) · [Démarrage rapide](./fr/QUICKSTART.md) · [Vue subvention](./fr/GRANT_OVERVIEW.md)
- 🇪🇸 [Guía para reviewers](./es/REVIEWER_GUIDE.md) · [Inicio rápido](./es/QUICKSTART.md) · [Resumen de subvención](./es/GRANT_OVERVIEW.md)
- 🇮🇹 [Guida per reviewer](./it/REVIEWER_GUIDE.md) · [Avvio rapido](./it/QUICKSTART.md) · [Panoramica della sovvenzione](./it/GRANT_OVERVIEW.md)
- 🇷🇺 [Руководство reviewer](./ru/REVIEWER_GUIDE.md) · [Быстрый старт](./ru/QUICKSTART.md) · [Обзор гранта](./ru/GRANT_OVERVIEW.md)
- 🇨🇳 [Reviewer 指南](./zh-CN/REVIEWER_GUIDE.md) · [快速开始](./zh-CN/QUICKSTART.md) · [Grant 概览](./zh-CN/GRANT_OVERVIEW.md)
- 🇸🇦 [دليل المراجع](./ar/REVIEWER_GUIDE.md) · [البدء السريع](./ar/QUICKSTART.md) · [نظرة عامة على المنحة](./ar/GRANT_OVERVIEW.md)
- 🇯🇵 [日本語 reviewer guide](./ja/REVIEWER_GUIDE.md) · [クイックスタート](./ja/QUICKSTART.md) · [Grant 概要](./ja/GRANT_OVERVIEW.md)

The previous long-form status snapshot is preserved byte-for-byte at:

`docs/archive/grant-sync/STATUS_PRE_SYNC_2026-07-30.md`

---

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/STATUS.md) · 🇫🇷 [Français](./fr/STATUS.md) · 🇪🇸 [Español](./es/STATUS.md) · 🇮🇹 [Italiano](./it/STATUS.md) · 🇷🇺 [Русский](./ru/STATUS.md) · 🇨🇳 [简体中文](./zh-CN/STATUS.md) · 🇸🇦 [العربية](./ar/STATUS.md) · 🇯🇵 [日本語](./ja/STATUS.md)