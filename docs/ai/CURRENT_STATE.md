# 📍 Crystal Current State

**Status date:** 2026-08-07  
**Current `main` head:** `1748677a5c84e8a9b3af08fcaed0215efebcdd66`  
**Verified runtime checkpoint:** `1748677a5c84e8a9b3af08fcaed0215efebcdd66`  
**Version:** `0.3.0`

This file is a compact orientation snapshot. GitHub `main`, current code, tests and
completed Actions runs remain implementation truth. Notion stores synchronized rationale,
strategy and project history; it does not override repository evidence.

## 1. Verified hardening checkpoint

The 2026-08-07 hardening train was merged sequentially and validated on exact PR heads:

| Capability | PR | Merge SHA | Exact-head CI |
|---|---:|---|---:|
| Crash-consistent curator decisions | #319 | `62879cd2095450de57d11fcf97c13f5f9768ad0b` | `31162857843` |
| Principal-bound curator writes | #320 | `1414862786aa0c0d4cf4ad152776dd4e55536bf0` | `31164585628` |
| Bounded legacy retrieval and explicit reindex | #321 | `1748677a5c84e8a9b3af08fcaed0215efebcdd66` | `31166027193` |

The final merge commit has tree `38c829b37bb61939792c64ee01ad925d6e8afd13`,
identical to the validated PR #321 head tree.

Latest runtime evidence:

- Python 3.11: **1943 passed, 12 skipped, 0 failed**;
- Python 3.12: successful with the same strict gate;
- **7948 measured statements, 100.00% line coverage**;
- **7/7 declared Ring Zero mutants killed**;
- **9/9 permanent CI jobs successful**;
- Gitleaks, Bandit, pip-audit, eval, JSONL integrity, Ruff, docs-status and Docker green.

## 2. Current implemented boundaries

Crystal now includes:

- typed claims and explicit epistemic lifecycle;
- Guardian and TruthGate admission controls;
- physical L3 separated from strict Canon;
- immutable deny-dominant `TrustSnapshot` reconciliation;
- read-only HTTP, CLI and MCP query surfaces;
- TRACE, receipts and tamper-evident audit continuity;
- immutable contradiction reports and explicit `COEXIST`, `CONTEXTUALIZE` and
  `SUPERSEDE` decisions without an automatic winner;
- transactional SQLite curator-decision journal/outbox with idempotent L3 projection,
  restart recovery and structured pending/failed/blocked status;
- authoritative L1 restriction semantics that remain deny-dominant while secondary L3
  synchronization is unavailable;
- principal-derived curator identity, explicit capabilities, normalized candidate/target
  scopes, current-report pinning and process-local decision leases across bundled write
  surfaces;
- ADMIN-only force approval and zero canonical mutation on authorization denial;
- bounded no-fingerprint lexical retrieval for reviewed Mock/SQLite adapters;
- stable `legacy_store_requires_reindex` fail-closed behavior for unsupported legacy
  backends;
- explicit operator reindex that changes vectors/fingerprint only;
- advisory topic facets with no truth, evidence or Canon authority;
- machine-readable ESM specification and recorded retrieval benchmark evidence.

## 3. Retrieval benchmark evidence

PR #321 benchmark run `31165503179` used Python 3.11.15, candidate cap 256 and 30
measured iterations per case:

| Corpus | p50 | p95 | Maximum candidates examined |
|---:|---:|---:|---:|
| 1,000 | 1.465 ms | 1.489 ms | 256 |
| 10,000 | 1.469 ms | 1.493 ms | 256 |
| 30,000 | 1.471 ms | 1.498 ms | 256 |

The timing values are contextual hosted-runner evidence, not a latency SLO. The
load-bearing result is that candidate work remained at or below the configured cap for
all recorded corpus sizes.

## 4. Important remaining limitations

| Area | Current reality |
|---|---|
| Distributed coordination | bundled curator lease is process-local; no cross-process fencing or global exactly-once claim |
| Identity and tenancy | principal composition exists, but production IdP, token lifecycle, tenant isolation and policy administration remain host work |
| Legacy degraded retrieval | deterministic bounded windows can miss relevant records outside the window; degraded mode explicitly recommends reindex |
| Performance | benchmark evidence exists, but no production latency/capacity SLO is established |
| Mutation proof | Ring Zero mutation testing is targeted, not repository-wide |
| Supply chain | security scanning passes, but dependency/action reproducibility and pinning remain improvement work |
| Legacy normalized IDs | upgraded stores may still need a reviewed migration or normalized-claim index (#165) |
| Long documents | no verified multi-pass Reader Core / Semantic Reading Layer exists |
| Compliance | GDPR-oriented mechanisms and documentation are not legal certification |
| Production posture | Crystal is not a certified turnkey multi-tenant production service |

## 5. Closed audit findings

- **#315 / PR #319:** crash consistency closed with a durable decision/outbox model,
  idempotent projection, failure injection and recovery evidence.
- **#316 / PR #320:** bundled public curator writes now derive identity and authorization
  from configured/authenticated principals; request and CLI text cannot establish the
  audit actor.
- **#317 / PR #321:** public legacy retrieval no longer performs reviewed unbounded
  Mock/SQLite corpus scans; unsupported adapters fail closed and explicit reindex is
  available.

These closures do not remove the remaining distributed-coordination, production-identity,
recall-quality or operational-capacity boundaries listed above.

## 6. Long-document semantic reading

No dedicated multi-pass `Reader Core` / `Semantic Reading Layer` with structural maps,
coverage tracking, bookmarks, exception/contradiction passes and selective re-reading is
part of the verified runtime.

A future reading layer should produce source-linked candidate cards and coverage evidence
upstream of ordinary Guardian and TruthGate admission. It must not become a second Canon
owner or silently promote summaries, rankings or inferred importance.

## 7. Open work and research interpretation

Open issues and PRs are hypotheses, proposals or mutable work records until merged. Agents
must inspect their current base, head, diff, checks and review state before citing them.

Material remaining engineering directions include:

- external lease/fencing adapter for multi-process curator coordination;
- production identity-provider and tenant-policy integration;
- broader provenance lifecycle inventory and recovery proof;
- controlled-runner performance policy;
- broader mutation testing;
- reproducible dependency/tool/action pinning;
- normalized legacy-ID migration or index (#165);
- a separately reviewed Reader Core RFC.

Research PRs and ecosystem pages must not be represented as Crystal runtime merely because
they are public or documentation-only.

## 8. Authority and grant boundary

```text
GitHub main code + tests = implementation truth
verified runtime checkpoint = 1748677
Notion = rationale, strategy, grant context and synchronized history
Physical L3 != strict Canon
Retrieval rank != evidence or truth
Model output != independent factual source
Titan / Full Exo-Cortex / Personal Exo-Cortex = separate research tracks
```

No new award, budget, legal certification, distributed-locking, production-readiness,
zero-hallucination or artificial-consciousness claim is introduced by this checkpoint.

## 9. Documentation synchronization

PR #318 is the documentation-only synchronization record for the completed hardening
train. It updates this AI context, the known-risk register and the engineering work log,
then synchronizes the same decision-bearing facts into the Crystal Project Hub and Deep
Audit Notion pages.
