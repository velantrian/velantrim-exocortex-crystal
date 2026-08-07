# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> **Authority rule:** only merged `main` code, tests and exact CI evidence are current
> implementation truth. Proposed work is not runtime capability.

**Current verified baseline:** `main@c612c1f7de067b05ed7d01ad82d47a7bc39af23a`  
**Validated head / CI:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736` / `31213056560`

## ✅ Delivered baseline

Crystal currently has:

- typed claims, evidence spans, provenance and epistemic lifecycle;
- Guardian and TruthGate admission boundaries;
- physical L3 multi-status storage separated from strict Canon;
- immutable deny-dominant trusted read projections;
- read-only public HTTP, CLI and MCP query paths;
- TRACE, receipts, replay, restriction and erasure controls;
- explicit contradiction reports and authorized dispositions;
- scoped curator authorization with process-local leases;
- bounded retrieval and explicit reindex refusal;
- durable backend/locator profile locking;
- SQLite backup, verify, inactive restore and guarded lock recovery;
- deterministic SQLite logical export and independent bundle verification;
- a fixed fail-closed local-first export resource envelope;
- 2047 tests, 100% coverage, 7/7 declared mutants and 9/9 CI jobs.

## 🧱 Current storage position

```text
SQLite
  = verified local-first/lightweight default

PostgreSQL + pgvector
  = optional future institutional profile
```

No automatic fallback or capability-based switching is permitted after a durable profile
exists.

## P1 — Institution-scale migration proof (#331)

Goal: remove full-dataset/full-file materialization as a scale blocker.

Deliverables:

- cursor-batched export;
- incremental descriptor-bound hashing and JSONL parsing;
- disk-backed referential checks;
- disk-space/resource preflight;
- interruption cleanup;
- large-corpus memory/disk/time benchmarks.

Exit gate: reproducible bounded peak-memory evidence at declared corpus sizes.

## P1 — Inactive PostgreSQL/pgvector import (#332)

Blocked by #331.

Deliverables:

- optional driver extra and version policy;
- secret-free institutional profile;
- inactive target import only;
- exact state equivalence receipts;
- exact-search reference and later ANN evaluation;
- no activation from successful import.

## P1 — Grant baseline and claim gates (#333)

Deliverables:

- freeze the PR #330 baseline;
- recalculate M1–M9 funded deltas;
- remove stale storage/auth claims;
- validate grant, roadmap and security surfaces in CI;
- preserve submitted/under-review/not-awarded status.

## P2 — Explicit cutover and rollback

Separate reviewed phase after exact target equivalence:

```text
preflight
→ source/target fencing
→ explicit cutover receipt
→ observed target operation
→ rollback window
→ optional explicit rollback receipt
```

No live dual-write or zero-downtime claim is assumed.

## P2 — Server lifecycle and security

- PostgreSQL/pgvector backup and independent restore drill;
- TLS, least-privilege roles and credential rotation;
- transaction isolation/retry policy;
- extension/schema upgrade sequencing;
- audit redaction and operator observability;
- multi-process tests without distributed exactly-once overclaim.

## P2 — Release and supply-chain hardening

- reviewer-preview release from the current baseline;
- wheel/sdist/container artifacts;
- checksums and SBOM;
- pinned actions/dependency policy;
- scheduled security and maintenance updates.

## P3 — Source-linked Reader Core prototype

A future semantic reading layer may provide:

- document structure maps;
- safe segmentation and exact source spans;
- source-linked candidate cards;
- coverage, exception, contradiction and re-read reports.

It must remain upstream of ordinary Guardian/TruthGate admission and must never become a
second Canon owner.

## Explicitly out of scope

- universal truth or zero hallucinations;
- consciousness, AGI or a living digital mind;
- automatic GDPR/legal/security certification;
- automatic backend switching;
- hidden chain-of-thought storage;
- production multi-tenant SaaS without a separate reviewed deployment track;
- Titan, Native Kernel, Mentaury or Research Mode as current Crystal runtime.

## Completion discipline

Every roadmap item requires:

```text
issue / RFC
→ narrow implementation PR
→ tests and failure-path evidence
→ exact-head CI
→ status/manifest update
→ Notion synchronization where required
→ merge SHA and known limitations
```
