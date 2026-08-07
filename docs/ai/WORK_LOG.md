# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It
is not a replacement for Git history, issues, pull requests, `CHANGELOG.md` or Notion.
Earlier detailed entries remain available through Git history.


## 2026-08-08 — PR #335 bounded migration merged

- Merge: `f03e24c85922d0bb46d6d9dfee98338972135908`; validated head `17ce10ffe12da93be50434c73d08f05a70a5922b`; exact-head CI `31224184351` 9/9.
- Evidence: 2059 passed / 12 skipped, 9361 statements, 100.00% coverage; benchmark `31224005804` 2/2.
- Implemented fixed cursor batches, disk-backed canonical edge sorting, same-descriptor incremental verification, disk-backed referential checks and failure cleanup.
- First CI runs exposed SHA-diagnostic precedence and missing fail-closed branch coverage; both were fixed before merge.
- Impact classification: `GITHUB_AND_NOTION`.
- #331 becomes merged baseline after this status synchronization; #332 remains the next inactive PostgreSQL import/equivalence phase.

## 2026-08-07 — Grant/status baseline synchronization (#333 / PR #334)

### Scope

Reconcile public README, verification/status files, grant scope, M1–M9 funded deltas,
roadmap, security policy and AI context with the runtime merged by PR #330.

### Verified baseline

- runtime merge: `c612c1f7de067b05ed7d01ad82d47a7bc39af23a`;
- validated runtime head: `e70c31bf517039f0dd3f77f7bc4b6d3f03936736`;
- verified tree: `17d65f52ac1d985fca249e6c9a183168d6116ffb`;
- exact-head runtime CI: `31213056560`, 9/9 successful;
- Python 3.11 and 3.12: 2047 passed / 12 skipped / 0 failed;
- 9219 statements / 100.00% coverage;
- 7/7 declared Ring Zero mutants killed.

### Findings and corrections

- the first PR #334 head updated only nine documentation files while its description also
  claimed README, claim-gate and complete AI-context synchronization;
- exact-head CI `31214414769` correctly failed `docs-status` while the other eight jobs
  passed;
- the failure exposed a stale README, a stale validation contract and incorrect frozen
  localized README blob IDs;
- live Notion verification found premature top callouts claiming PR #334 was merged and
  issue #333 closed;
- corrective `CURRENT TRUTH` callouts were prepended to the Project Hub, Current
  Architectural Position and Grant-Safe Module Roadmap before continuing the repair.

### Changes in the repaired branch

- publish a concise reviewer-facing README tied to PR #330 evidence;
- correct the machine-readable manifest and nine frozen localized README Git blob IDs;
- refresh `KNOWN_RISKS.md` with #331, #332 and claim boundaries;
- replace this compact work log with an exact current hand-off;
- update `scripts/check_docs_status.sh` to validate the current baseline, grant/security
  non-claims, required issue references, local links and frozen translation bytes;
- preserve localized README files unchanged.

### Completion gate

PR #334 is authoritative only after its latest exact head passes all nine jobs and is merged.
After merge, record the immutable merge SHA, exact-head CI and remaining #331/#332 work in
all three Crystal Notion pages. The mutable PR record remains the authority for branch and
merge status.

### Synchronization class

`GITHUB_AND_NOTION`

---

## 2026-08-07 — Deterministic SQLite logical export merged (#329 / PR #330)

### Scope

Implement the first runtime phase governed by ADR-021: read-only logical export from a
locked durable SQLite profile and independent fail-closed bundle verification.

### Result

PR #330 merged as `c612c1f7de067b05ed7d01ad82d47a7bc39af23a`.

Implemented:

- canonical JSONL datasets for nodes, vectors, edges, entities, mentions and metadata;
- completion-marker-last no-clobber publication;
- independent descriptor-bound verification;
- schema, strict JSON, ordering, vector and referential-integrity checks;
- source/profile mutation and path-swap defenses;
- explicit fail-closed local-first resource limits.

### Validation

- exact head: `e70c31bf517039f0dd3f77f7bc4b6d3f03936736`;
- CI `31213056560`: 9/9 successful;
- Python 3.11 and 3.12: 2047 passed / 12 skipped / 0 failed;
- 9219 statements / 100.00% coverage;
- Ring Zero mutation, security, Ruff, eval, JSONL integrity, docs-status and Docker green.

### Boundary and remaining work

The merged slice is bounded local-first operation, not institution-scale streaming.

- #331: cursor batching, incremental verification, disk-backed referential checks and
  large-corpus resource evidence;
- #332: future optional inactive PostgreSQL/pgvector import and exact-state equivalence;
- later separate phases: retrieval evaluation, explicit cutover, rollback and fencing.

No migration bundle, backend profile or successful verification grants epistemic authority
or activates another backend.
