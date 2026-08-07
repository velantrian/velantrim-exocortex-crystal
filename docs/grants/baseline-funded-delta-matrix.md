# Grant Baseline → Funded Delta → Acceptance Matrix

**Status:** grant-planning control · documentation only · no award/budget change  
**Frozen baseline:** `main@c612c1f7de067b05ed7d01ad82d47a7bc39af23a`  
**Validated head / CI:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736` / `31213056560`  
**Baseline evidence:** 2047 passed / 12 skipped / 9219 statements / 100% coverage / 9 CI jobs

## Control rule

```text
verified baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

Anything merged at or before the frozen baseline is existing capability and cannot be
counted again as future paid work.

## M1 — Reproducible local-first runtime and release evidence

**Baseline already present**

- pure-standard-library default runtime;
- deterministic tests/evaluation and 100% line coverage;
- nine-job CI and Ring Zero mutation gate;
- durable SQLite profile, backup/verify/inactive restore;
- deterministic bounded SQLite logical export/verify.

**Funded delta**

- reproducible wheel/sdist and container artifacts;
- checksums, SBOM and supported-version manifest;
- clean-machine installation/reproduction scripts;
- release-linked exact SHA/CI evidence and documented operational limits.

**Acceptance**

- public release artifacts install on supported Python versions;
- checksums/SBOM are generated reproducibly;
- clean-environment smoke tests reproduce the named checkpoint;
- no existing storage lifecycle work is billed again.

## M2 — Institution-scale portable storage state

**Baseline already present**

- backend-neutral canonical JSONL bundle schema;
- independent fail-closed verification;
- fixed local-first resource limits;
- accepted cross-backend migration architecture and PostgreSQL RFC.

**Funded delta**

- issue #331 streaming/incremental export and verification;
- cursor batching and incremental same-descriptor hashing/parsing;
- disk-backed node/entity/reference checks;
- disk-space preflight, interruption cleanup and large-corpus evidence.

**Acceptance**

- bounded peak-memory tests at declared corpus sizes;
- deterministic bundle equality across repeated runs;
- adversarial oversized/corrupt inputs fail closed;
- benchmark report includes memory, disk, time and tested limits.

## M3 — Inactive PostgreSQL/pgvector import and exact equivalence

**Baseline already present**

- SQLite local-first source profile;
- deterministic verified bundle;
- no-automatic-switching contract;
- PostgreSQL/pgvector architecture only.

**Funded delta**

- optional PostgreSQL driver extra with version policy;
- secret-free institutional profile identity;
- import into an inactive target only;
- deterministic exact-state equivalence receipts;
- failure cleanup and retry/idempotency behavior.

**Acceptance**

- identifiers, payloads, vectors, edges, entities, mentions and metadata compare exactly;
- approved restrictions/erasure/provenance state is not dropped;
- target cannot serve normal reads/writes before explicit cutover;
- successful import never changes TruthGate or strict Canon membership.

## M4 — Reproducible retrieval-quality evaluation

**Baseline already present**

- deterministic evaluation infrastructure;
- bounded retrieval and explicit degraded/reindex behavior;
- exact vector values in the portable bundle.

**Funded delta**

- exact pgvector search reference implementation;
- versioned HNSW/IVFFlat corpus and manifests;
- recall@k, filtered recall, latency, index size, rebuild cost and stale-index tests;
- machine-readable regression reports.

**Acceptance**

- exact search is the reference baseline;
- ANN enablement requires accepted recall thresholds;
- exact-state mismatch cannot be overridden by latency/recall results;
- indexes remain rebuildable non-authoritative projections.

## M5 — Explicit cutover and rollback proof

**Baseline already present**

- durable profile identity;
- inactive SQLite restore;
- migration contract requiring separate activation.

**Funded delta**

- source/target fencing and preflight;
- immutable cutover receipt;
- explicit rollback receipt and expiry/window policy;
- crash-window, retry and partial-failure tests.

**Acceptance**

- source remains authoritative until a valid cutover receipt;
- no capability-based or reachability-based switching;
- rollback behavior is deterministic and audited;
- profile edit/delete is rejected as migration.

## M6 — Server lifecycle and operational security

**Baseline already present**

- scoped curator roles/capabilities;
- authenticated actor binding on implemented write surfaces;
- process-local leases and audit receipts;
- SQLite lifecycle proof.

**Funded delta**

- PostgreSQL least-privilege read/runtime/migration roles;
- TLS verification and credential rotation/revocation contract;
- PostgreSQL/pgvector backup, restore drill and upgrade sequencing;
- audit redaction, timeout/pooling policy and operator diagnostics.

**Acceptance**

- independently tested restore drill;
- credentials never enter profiles, bundles, receipts, logs or Notion;
- multi-process tests document transaction/retry semantics;
- no production IdP, certification or distributed exactly-once overclaim.

## M7 — Evidence and TRACE inspection UX

**Baseline already present**

- source/evidence metadata, provenance, TRACE and receipts;
- review sessions and contradiction reports;
- read-only query boundary.

**Funded delta**

- reviewer-facing TRACE/receipt visualization;
- source-span and policy/evidence navigation;
- explicit uncertainty, refusal and contradiction views;
- content-light export for independent audit.

**Acceptance**

- every displayed statement links to immutable evidence/provenance identifiers;
- UI does not mutate Canon or promote claims;
- restricted/erased content is denied consistently;
- automated accessibility and security tests pass.

## M8 — Source-linked semantic reading prototype

**Baseline already present**

- ordinary ingest/admission path;
- source/evidence spans and review queues;
- explicit statement that no dedicated Reader Core exists.

**Funded delta**

- bounded multi-pass document structure map;
- safe segmentation and exact source-span preservation;
- source-linked candidate cards;
- coverage, exception, contradiction and re-read reports.

**Acceptance**

- output remains candidate material upstream of Guardian/TruthGate;
- extraction confidence, importance and truth confidence stay separate;
- no second Canon owner or automatic promotion;
- coverage and source-span reproducibility tests pass.

## M9 — Claim discipline, maintenance and independent audit

**Baseline already present**

- docs-status, security, mutation and evaluation gates;
- English-authoritative documentation policy;
- machine-readable implementation manifest;
- public known-risks and audit workflow.

**Funded delta**

- grant/roadmap/security claim-lint gate;
- dependency/action pinning and scheduled maintenance reports;
- independent architecture/security review artifacts;
- release-linked risk closure and remediation evidence.

**Acceptance**

- CI rejects stale SHA/test counts and false PostgreSQL/award/certification claims;
- actions/dependencies follow a reviewed pin/update policy;
- independent findings and resolutions are public;
- grant pages and runtime status remain synchronized.

## Explicit non-scope across M1–M9

- universal truth, zero hallucinations or AGI;
- consciousness, living digital mind or human-brain simulation;
- automatic GDPR/legal/security certification;
- autonomous self-canonization;
- hidden chain-of-thought storage;
- automatic backend switching or live dual-write unless separately reviewed;
- Titan, Native Kernel, Mentaury or Research Mode as current Crystal runtime.

## Change control

Any milestone change must update this matrix, the current status/manifest and synchronized
Notion grant pages in the same work cycle. Budget or award status may change only from
verified external grant communication.
