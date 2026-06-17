# Audit Response — 2026-06-17

> Scope: response to combined document/static/code/data/deploy audits.
> Status: docs-only. This file records follow-up work; it does not claim fixes are complete.

## Summary

The audits converge on one conclusion:

```text
Crystal has a strong Truth-first architecture.
Titan contains valuable research and implementation material.
The public Crystal line needs status clarity, deployment hardening, data-quality boundaries and provenance verification.
```

## Immediate findings to track

| Priority | Finding | Required response |
|---|---|---|
| P0 | Possible provenance-chain actor/reason regression reported in Titan audit | reproduce in Crystal if applicable; add append/verify/tamper tests |
| P0 | Unsafe Docker/compose defaults reported in Titan audit | require explicit API key; bind local by default; non-root image |
| P1 | TruthPolicy may be optional in some paths | decide production profile and add contract tests |
| P1 | Knowledge graph evidence gap | label unverified/autolinker data correctly; add verifier rules |
| P1 | Documentation drift across Crystal/Titan/V9/V10 | maintain `docs/STATUS.md` as current reading rule |
| P1 | Health/MHI fallback semantics | missing store should be degraded/safe, not healthy |

## What this repository should do next

1. Keep `docs/STATUS.md` current.
2. Add or verify provenance-chain contract tests.
3. Harden deployment defaults.
4. Add claim type/origin type documentation before runtime changes.
5. Add ingest and dedup contracts.
6. Add knowledge graph status and verifier rules before making data-quality claims.

## Boundary

This audit response does not import Titan wholesale into Crystal.

Crystal should extract:

- contracts;
- security lessons;
- evidence boundaries;
- minimal tested mechanisms;
- reviewer-safe documentation.

Crystal should leave speculative Full Exo-Cortex layers in research status until code, tests and flags prove otherwise.
