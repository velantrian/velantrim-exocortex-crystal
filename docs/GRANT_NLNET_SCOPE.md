# Velantrim Crystal — NLnet Grant Scope

**Baseline date:** 2026-08-07  
**Baseline checkpoint:** `main@c612c1f7de067b05ed7d01ad82d47a7bc39af23a`  
**Validated head / CI:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736` / `31213056560`  
**Grant status:** submitted / under review / not awarded

## Summary

Velantrim Crystal is open-source, local-first verifiable memory infrastructure for AI
systems. It separates physical storage, evidence, epistemic admission and strict grounding
so that retrieved or generated text cannot silently become trusted memory.

The submitted application title is retained as historical application metadata. References
to GDPR mean **GDPR-oriented technical controls**—such as restriction, erasure, provenance,
audit and local processing—not automatic legal compliance or certification.

## Current verified baseline

The current public baseline already includes:

- typed claims, source metadata and evidence spans;
- explicit epistemic lifecycle and CAS-style state guards;
- Guardian structural/safety checks and TruthGate admission policy;
- physical L3 multi-status storage separated from strict Canon;
- deny-dominant `TrustSnapshot` / `CanonicalView` reads;
- read-only HTTP, CLI and MCP query paths;
- TRACE, receipts, replay and tamper-evident audit artifacts;
- restriction, erasure and import-session controls;
- review queues, resumable sessions and explicit contradiction dispositions;
- scoped curator roles/capabilities and process-local leases;
- bounded legacy retrieval and reindex refusal;
- durable backend/locator profile locking;
- SQLite backup, independent verification, inactive restore and guarded stale-lock recovery;
- deterministic SQLite logical export and independent bundle verification under fixed
  local-first resource limits;
- deterministic evaluation, 100% line coverage and a Ring Zero mutation gate.

Verification at the baseline:

```text
Python 3.11: 2047 passed / 12 skipped / 0 failed
Python 3.12: 2047 passed / 12 skipped / 0 failed
9219 statements / 100.00% coverage
7/7 declared Ring Zero mutants killed
9/9 CI jobs successful
```

## Core architecture

```text
source material / explicit claim
        ↓
typed candidate + evidence span + provenance
        ↓
Guardian structural/safety checks
        ↓
TruthGate admission policy
        ↓
L1 lifecycle + physical L3 multi-status storage
        ↓
TrustSnapshot deny-dominant reconciliation
        ↓
CanonicalView strict trusted projection
        ↓
read-only grounding + TRACE + Receipt
```

Critical distinctions:

```text
physical L3          != strict Canon
retrieval score      != evidence
model output         != independent source
migration bundle     != claim evidence
successful import    != activation
GDPR-oriented design != legal certification
```

## Storage portability baseline

The merged runtime can export a locked SQLite physical-L3 profile into deterministic
canonical JSONL and verify the completed bundle independently.

Current fail-closed envelope:

| Resource | Limit |
|---|---:|
| profile/control JSON | 1 MiB |
| source SQLite | 64 MiB |
| canonical record | 1 MiB |
| records per dataset | 200,000 |
| dataset | 64 MiB |
| aggregate JSONL | 384 MiB |

This proves a bounded local-first portability path. It does not prove streaming or
institution-scale migration.

## Proposed funded delta

The funded delta must extend—not re-label—the merged baseline. Preferred independently
verifiable packages are:

1. **Streaming migration proof** (#331)
   - cursor-batched export;
   - incremental same-descriptor hashing/parsing;
   - disk-backed referential checks;
   - disk-space/resource preflight and interruption cleanup;
   - large-corpus resource evidence.

2. **Inactive PostgreSQL/pgvector import and exact equivalence** (#332)
   - optional driver extra and reviewed version policy;
   - secret-free durable profile identity;
   - inactive import only;
   - exact identifiers, payloads, vectors, edges, metadata and restrictions comparison;
   - no activation on import success.

3. **Explicit cutover and rollback proof**
   - source/target fencing;
   - immutable cutover receipt;
   - rollback window and expiry policy;
   - crash/retry/idempotency tests.

4. **Server lifecycle and security hardening**
   - least-privilege roles, TLS and credential rotation boundaries;
   - PostgreSQL/pgvector backup, restore drill and upgrade sequencing;
   - audit redaction and operational observability;
   - no production certification claim without independent assessment.

5. **Reproducible retrieval evaluation**
   - exact search reference;
   - versioned HNSW/IVFFlat corpus;
   - recall@k, filtered recall, latency, rebuild cost and stale-index behavior;
   - ANN indexes remain rebuildable projections without truth authority.

6. **Grant/release evidence automation**
   - claim-lint and status gates for grant, roadmap and security documents;
   - release artifacts, checksums and SBOM;
   - exact SHA/CI/version evidence and documented limits.

A dedicated Reader Core may be proposed only as a later source-linked candidate-extraction
layer upstream of Guardian/TruthGate. It must not become a second Canon owner.

## Explicit exclusions

The grant scope does not claim:

- universal truth or zero hallucinations;
- AGI, consciousness or a living digital mind;
- automatic GDPR/legal/security certification;
- current PostgreSQL/pgvector runtime;
- automatic SQLite/PostgreSQL fallback;
- production multi-tenant SaaS or bundled IdP;
- distributed exactly-once behavior;
- live dual-write or zero-downtime cutover;
- Titan, Native Kernel or Mentaury as hidden Crystal runtime dependencies.

## Baseline/funding rule

```text
verified baseline at exact SHA
+
measurable new implementation delta
=
independently verifiable deliverable
```

Already merged capabilities cannot be counted again as paid work. The milestone matrix in
[`docs/grants/baseline-funded-delta-matrix.md`](./grants/baseline-funded-delta-matrix.md)
implements this rule for M1–M9.
