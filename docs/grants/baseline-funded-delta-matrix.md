# Grant Baseline → Funded Delta → Acceptance Matrix

**Status:** grant-planning control · documentation only · no award/budget change  
**Frozen runtime checkpoint:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Current Reader baseline:** RC-1 + RC-2 merged pre-agreement; dedicated multi-pass Reader absent.  
**Baseline evidence:** 2078 passed / 13 skipped / 9756 statements / 100% coverage / 9 CI jobs / 1 PostgreSQL integration job

## Control rule

```text
verified baseline + new measurable funded delta
= independently verifiable public deliverable
```

Anything already merged before an agreement is existing capability and cannot be counted again as
future paid work. This includes #331 / PR #335, #332 / PR #337, Reader RC-0/RC-1/RC-2 and merged
multilingual documentation baselines.

## M1 — Reproducible runtime and release evidence

**Baseline:** pure-standard-library default runtime, deterministic tests, 100% coverage, nine-job CI,
Ring Zero, SQLite lifecycle and bounded logical migration.

**Funded delta:** reproducible wheel/sdist/container artifacts, checksums, SBOM, supported-version
manifest and clean-machine reproduction.

**Acceptance:** public artifacts reproduce a named SHA/CI checkpoint and do not rebill existing work.

## M2 — Bounded portable storage state

**Baseline:** canonical bundle, fixed batches, disk-backed ordering/reference checks, same-descriptor
verification and benchmark evidence.

**Funded delta:** only new maximum-envelope/interruption evidence or new measurable tooling; no
duplicate billing of PR #335.

## M3 — Inactive PostgreSQL/pgvector import and exact equivalence

**Baseline:** PR #337 provides optional lazy Psycopg loading, supported-version preflight, new inactive
schema, serializable import, independent exact canonical re-hash and integration evidence.

**Funded delta:** no duplicate billing of #332 / PR #337. Additional work must add separately reviewed
state domains or independently measurable operational evidence.

**Acceptance:** target remains `active=false`; import/equivalence never changes TruthGate or strict Canon.

## M4 — Reproducible exact-vs-ANN evaluation

**Baseline:** exact vector values exist in the portable bundle; no ANN index is enabled.

**Funded delta:** exact pgvector reference search, versioned HNSW/IVFFlat corpus, recall@k, filtered
recall, latency, index-size, rebuild-cost and stale-index reports.

## M5 — Explicit cutover and rollback proof

**Baseline:** durable profile identity, inactive restore/import and a contract requiring separate activation.

**Funded delta:** source/target fencing, immutable cutover receipt, explicit rollback receipt, expiry
policy and crash-window tests. No reachability-based switching.

## M6 — Server lifecycle and operational security

**Baseline:** optional migration dependency, TLS-by-default preflight, redacted failures and non-secret receipts.

**Funded delta:** least-privilege roles, certificate/credential rotation, PostgreSQL backup and independent
restore drill, retention/upgrade sequencing, pooling, retry and observability.

## M7 — Evidence and TRACE inspection UX

**Baseline:** provenance, TRACE, receipts, contradiction reports and read-only query boundary.

**Funded delta:** reviewer-facing visualization, source-span navigation, uncertainty/refusal views and
content-light audit export. UI cannot promote or mutate Canon.

## M8 — Reader work beyond RC-1 / RC-2

**Baseline:** Reader RC-0 architecture contract plus implemented/tested RC-1 evidence-linked skeleton and
RC-2 caller-supplied Structural Document Map:

```text
reader_core_rc1_skeleton       = true
reader_core_rc2_structural_map = true
dedicated_reader_core          = false
```

These existing milestones cannot be counted again as future paid work.

**Funded delta:** only separately reviewed Reader work beyond that baseline. The next candidate is RC-3
explicit multi-pass reading mechanics; later evidence extraction, exception/contradiction candidates and
long-context work must each remain separately bounded. Embeddings/ANN/vector DB are not assumed.

**Acceptance:** output stays upstream of Guardian/TruthGate; fidelity remains explicit; coverage remains
version-specific and `coverage != comprehension proof`; no second Canon owner, planner authority or
automatic belief update.

A dedicated multi-pass Reader remains not implemented until a later exact implementation gate proves it.

## M9 — Claim discipline, maintenance and independent audit

**Baseline:** docs-status, security/mutation/evaluation gates, English-authoritative policy,
machine-readable manifest and public risks.

**Funded delta:** stronger claim lint, action/dependency pinning, scheduled maintenance, independent review
artifacts and release-linked remediation.

## Explicit non-scope across M1–M9

- universal truth, zero hallucinations, AGI or consciousness;
- automatic GDPR/legal/security certification;
- autonomous self-canonization or hidden chain-of-thought storage;
- automatic backend switching or live dual-write without separate review;
- Titan, Native Kernel, Mentaury or Research Mode as current Crystal runtime.

## Change control

Any milestone change must update this matrix, current status/manifest and synchronized Notion grant pages
in the same work cycle. Budget or award status may change only from verified external grant communication.
