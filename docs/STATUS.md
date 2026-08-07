# Velantrim Crystal — Current Status

**Status date:** 2026-08-07
**Verified runtime checkpoint:** `b0df17a` (`b0df17a06d552ad2543b6d6e5efe8cd99877cfc0`, merged PR #325)
**Validated head/tree:** `aa822c49c095039de90b92fbe4fe451c7b8f13b7` / `6143d7237222935182db86a166541d0ad07887be`
**Exact-head CI:** `31182471502` — 9/9 jobs successful
**Exact verification evidence:** [TEST_REPORT.md](../TEST_REPORT.md)
**Machine-readable status:** [implementation-manifest.json](./status/implementation-manifest.json)

## Documentation language policy

English is the authoritative and actively maintained GitHub documentation language during
the current engineering phase. Existing localized top-level README files are frozen
snapshots and may lag. They will be regenerated in a dedicated final localization pass;
ordinary implementation and architecture PRs must not update them automatically.

## Authority rule

```text
GitHub Crystal main = implementation truth
TEST_REPORT + manifest = exact verified evidence
Notion Crystal pages = synchronized rationale, strategy and history
Physical L3 != strict Canon
```

## Current verified baseline

```text
Python 3.11: 2019 passed / 12 skipped
Python 3.12: successful under the same strict gate
Failed:      0
Statements:  8726
Coverage:    100.00%
Mutation:    7/7 targeted Ring Zero mutants killed
CI:          9/9 permanent jobs successful
```

## Verified storage lifecycle

The environment-selected durable L3 backend and non-secret locator are locked across
restarts. The current SQLite profile additionally supports:

- consistent online backup;
- independent fail-closed bundle verification;
- no-clobber restore to a new inactive database and profile;
- restore receipts and candidate-profile-last ordering;
- read-only lock inspection;
- explicit race-safe recovery of the current legacy empty initialization lock.

No restored profile is activated automatically.

## Cross-backend migration status

The architecture contract in
[Cross-Backend Storage Migration Contract](./architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
is accepted for future work. Runtime support remains absent.

The first approved runtime slice is deterministic read-only SQLite logical export plus
independent verification. It does not include import, cutover, rollback, PostgreSQL,
pgvector, dual-write or automatic switching.

The
[PostgreSQL + pgvector Institutional Profile RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
remains `PROPOSED / NOT RUNTIME`.

## Trust topology

```text
explicit ingest → Guardian → TruthGate → physical L3 multi-status storage

public query/search
→ read-only retrieval
→ immutable TrustSnapshot
→ Guardian + CanonicalView STRICT
→ grounded answer / bounded refusal / Receipt

storage operation
→ deployment continuity receipt
→ never epistemic admission
```

## Important remaining limitations

- no verified cross-backend import, exact-equivalence engine, cutover or rollback;
- no PostgreSQL/pgvector adapter or dependency;
- no automatic backend switching after data exists;
- no distributed curator lease/fencing;
- no bundled production identity provider or complete multi-tenancy;
- no production latency/capacity SLO;
- no verified dedicated multi-pass Reader Core;
- GDPR-oriented controls are not legal certification.

## Public claim boundary

Crystal is local-first, source/state/provenance-oriented memory infrastructure with
explicit admission, strict read grounding, contradiction review, scoped curator
authorization, TRACE and replayable receipts. It is not a universal truth oracle,
hallucination-free system, production multi-tenant service, distributed locking system,
automatic database migration platform, Titan, or an artificial-consciousness
implementation.
