# Grant Baseline → Funded Delta → Acceptance Matrix

**Status:** grant-planning control · documentation only · no award/budget change  
**Frozen baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**Baseline evidence:** 2078 passed / 13 skipped / 9756 statements / 100% coverage / 9 CI jobs / 1 PostgreSQL integration job

## Control rule

```text
verified baseline + new measurable funded delta
= independently verifiable public deliverable
```

Anything merged at or before the frozen baseline is existing capability and cannot be
counted again as future paid work. This includes #331 / PR #335 and #332 / PR #337.

## M1 — Reproducible runtime and release evidence

**Baseline:** pure-standard-library default runtime, deterministic tests, 100% coverage,
nine-job CI, Ring Zero, SQLite lifecycle and bounded logical migration.

**Funded delta:** reproducible wheel/sdist/container artifacts, checksums, SBOM, supported
version manifest and clean-machine reproduction.

**Acceptance:** public artifacts reproduce a named SHA/CI checkpoint and do not rebill
existing storage lifecycle work.

## M2 — Bounded portable storage state

**Baseline:** canonical bundle, fixed batches, disk-backed ordering/reference checks,
same-descriptor verification and benchmark `31224005804`.

**Funded delta:** only new maximum-envelope/interruption evidence or new measurable tooling;
no duplicate billing of PR #335.

**Acceptance:** memory, disk, time, cleanup and non-SLO limits remain reproducible and
explicit.

## M3 — Inactive PostgreSQL/pgvector import and exact equivalence

**Baseline:** PR #337 provides optional lazy Psycopg loading, supported-version preflight,
new inactive schema, serializable import, independent exact canonical re-hash, endpoint-bound
non-secret receipts and a real PostgreSQL 16 / pgvector 0.8.2 integration test.

**Funded delta:** no duplicate billing of #332 / PR #337. Additional work qualifies only if
it adds separately reviewed state domains or new independently measurable operational
evidence beyond the approved bundle datasets.

**Acceptance:** target remains `active=false`, cannot serve normal reads/writes, preserves
approved identifiers/payloads/vectors/edges/entities/mentions/metadata exactly and never
changes TruthGate or strict Canon membership.

## M4 — Reproducible exact-vs-ANN evaluation

**Baseline:** exact vector values in the portable bundle; no ANN index is enabled.

**Funded delta:** exact pgvector reference search, versioned HNSW/IVFFlat corpus, recall@k,
filtered recall, latency, index-size, rebuild-cost and stale-index reports.

**Acceptance:** exact search remains the reference; ANN requires accepted thresholds and
cannot override exact-state mismatch.

## M5 — Explicit cutover and rollback proof

**Baseline:** durable profile identity, inactive restore/import and a contract requiring
separate activation.

**Funded delta:** source/target fencing, immutable cutover receipt, explicit rollback receipt,
expiry policy and crash-window tests.

**Acceptance:** source remains authoritative until valid cutover; no capability-based or
reachability-based switching; rollback is deterministic and audited.

## M6 — Server lifecycle and operational security

**Baseline:** optional migration dependency, TLS-by-default preflight, redacted failures and
non-secret receipts. No active server runtime lifecycle is claimed.

**Funded delta:** least-privilege roles, certificate/credential rotation, PostgreSQL backup
and independent restore drill, retention/upgrade sequencing, pooling, retry and observability.

**Acceptance:** credentials never enter profiles, bundles, receipts, application logs or
Notion; multi-process semantics are tested; no certification or distributed exactly-once
overclaim.

## M7 — Evidence and TRACE inspection UX

**Baseline:** provenance, TRACE, receipts, contradiction reports and read-only query boundary.

**Funded delta:** reviewer-facing visualization, source-span navigation, uncertainty/refusal
views and content-light audit export.

**Acceptance:** displayed statements link to immutable evidence; UI cannot promote or mutate
Canon; restriction/erasure denial is preserved.

## M8 — Source-linked semantic reading prototype

**Baseline:** ordinary admission path and source/evidence spans; no dedicated Reader Core.

**Funded delta:** bounded structure map, safe segmentation, exact source spans, candidate
cards and coverage/exception/contradiction reports.

**Acceptance:** output stays upstream of Guardian/TruthGate; importance and truth remain
separate; no second Canon owner.

## M9 — Claim discipline, maintenance and independent audit

**Baseline:** docs-status, security/mutation/evaluation gates, English-authoritative policy,
machine-readable manifest and public risks.

**Funded delta:** stronger claim lint, action/dependency pinning, scheduled maintenance,
independent review artifacts and release-linked remediation.

**Acceptance:** CI rejects stale SHA/test counts and false activation/award/certification
claims; GitHub and Notion remain synchronized.

## Explicit non-scope across M1–M9

- universal truth, zero hallucinations, AGI or consciousness;
- automatic GDPR/legal/security certification;
- autonomous self-canonization or hidden chain-of-thought storage;
- automatic backend switching or live dual-write without separate review;
- Titan, Native Kernel, Mentaury or Research Mode as current Crystal runtime.

## Change control

Any milestone change must update this matrix, current status/manifest and synchronized Notion
grant pages in the same work cycle. Budget or award status may change only from verified
external grant communication.