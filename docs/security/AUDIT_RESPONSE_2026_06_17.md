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

## Correction after Claude Code plan

Claude Code reviewed the Crystal repository plan and clarified several points:

1. The Titan `_compute_hash(actor/reason)` failure should not be treated as a confirmed Crystal runtime regression unless reproduced in this repository.
2. In Crystal, the per-fact `ProvenanceChain` is a planned/absent feature to implement from Sprint1 P1-5 / I89.
3. Docker files are Track 2 creation targets.
4. Crystal API token variable is `VELANTRIM_API_TOKEN`, not `VELANTRIM_API_KEY`.
5. TruthPolicy work is split into Track 3A and Track 3B.
6. No `/facts` POST endpoint should be assumed for Track 3B.

## Current track map

| Track | Scope | Status |
|---|---|---|
| Track 1 | per-fact ProvenanceChain + DB table + erasure integration + 7 tests | code task for Claude Code |
| Track 2 | Dockerfile, docker-compose.yml, .dockerignore from scratch | code/deploy task for Claude Code |
| Track 3A | TruthPolicy strict production default | code/test task for Claude Code |
| Track 3B | write-path TruthGate audit tests + `gate_reason` | code/test task for Claude Code |

## Immediate findings to track

| Priority | Finding | Required response |
|---|---|---|
| P0 | Per-fact ProvenanceChain not yet implemented in Crystal | implement Track 1, do not claim per-fact chain before tests |
| P0 | Deployment needs fail-closed Docker defaults | create Docker files with required `VELANTRIM_API_TOKEN` |
| P1 | TruthPolicy default must be explicit and testable | Track 3A |
| P1 | Write-path gate behaviour should be pinned | Track 3B |
| P1 | Knowledge graph evidence gap | label unverified/autolinker data correctly; add verifier later |
| P1 | Documentation drift across Crystal/Titan/V9/V10 | maintain `docs/STATUS.md` as current reading rule |

## What this repository should do next

1. Merge Track 1 as a small PR.
2. Merge Track 2 as a separate PR.
3. Update `STATUS.md` / implementation status after Tracks 1–2 if needed.
4. Merge Track 3A.
5. Merge Track 3B.
6. Only then consider data verifier and canonical write path expansion.

## Boundary

This audit response does not import Titan wholesale into Crystal.

Crystal should extract:

- contracts;
- security lessons;
- evidence boundaries;
- minimal tested mechanisms;
- reviewer-safe documentation.

Crystal should leave speculative Full Exo-Cortex layers in research status until code, tests and flags prove otherwise.
