# Audit Response — 2026-06-17

> Scope: response to combined document/static/code/data/deploy audits.
> Status: docs-only. This file records follow-up work.
>
> **Update:** the Track 1–3B follow-ups below are now merged — Track 1 (#168),
> Track 2 (#170/#171), Track 3A (#172), Track 3B (#175). For current status see
> `docs/IMPLEMENTATION_REALITY_MATRIX.md` and `TEST_REPORT.md`.

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

## Track map (historical — all merged)

> The rows below were the original task plan. All four tracks are now merged;
> see `docs/IMPLEMENTATION_REALITY_MATRIX.md` and `TEST_REPORT.md` for live status.

| Track | Scope | Status |
|---|---|---|
| Track 1 | per-fact ProvenanceChain + DB table + erasure integration + tests | MERGED (#168) |
| Track 2 | Dockerfile, docker-compose.yml, .dockerignore from scratch | MERGED (#170/#171) |
| Track 3A | TruthPolicy strict production default | MERGED (#172) |
| Track 3B | write-path TruthGate audit tests + `gate_reason` | MERGED (#175) |

## Findings (historical — addressed)

> All P0/P1 items below are addressed in the merged tracks
> (#168 / #170-171 / #172 / #175). Retained as the historical audit record;
> see `docs/IMPLEMENTATION_REALITY_MATRIX.md` for live status.

| Priority | Finding | Required response |
|---|---|---|
| P0 | Per-fact ProvenanceChain not yet implemented in Crystal | implement Track 1, do not claim per-fact chain before tests |
| P0 | Deployment needs fail-closed Docker defaults | create Docker files with required `VELANTRIM_API_TOKEN` |
| P1 | TruthPolicy default must be explicit and testable | Track 3A |
| P1 | Write-path gate behaviour should be pinned | Track 3B |
| P1 | Knowledge graph evidence gap | label unverified/autolinker data correctly; add verifier later |
| P1 | Documentation drift across Crystal/Titan/V9/V10 | maintain `docs/STATUS.md` as current reading rule |

## Original next-steps plan (completed)

1. Merge Track 1 as a small PR. — DONE (#168)
2. Merge Track 2 as a separate PR. — DONE (#170/#171)
3. Update `STATUS.md` / implementation status after Tracks 1–2 if needed. — DONE
4. Merge Track 3A. — DONE (#172)
5. Merge Track 3B. — DONE (#175)
6. Only then consider data verifier and canonical write path expansion. — pending (future work)

## Boundary

This audit response does not import Titan wholesale into Crystal.

Crystal should extract:

- contracts;
- security lessons;
- evidence boundaries;
- minimal tested mechanisms;
- reviewer-safe documentation.

Crystal should leave speculative Full Exo-Cortex layers in research status until code, tests and flags prove otherwise.
