# Crystal Verification Report

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Verified tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Validated implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Pull request:** #337  
**Exact-head CI:** `31256316536`  
**PostgreSQL integration CI:** `31256316532`

This is evidence for the tested repository state. It is not a production, legal, security,
grant-award or institution-scale certification.

## Result

| Gate | Result |
|---|---:|
| Python 3.11 | 2078 passed / 13 skipped / 0 failed |
| Python 3.12 | 2078 passed / 13 skipped / 0 failed |
| Measured statements | 9756 |
| Line coverage | 100.00% |
| `core/postgresql_migration.py` | 44 / 44 statements |
| `core/postgresql_migration_impl.py` | 336 / 336 statements |
| Ring Zero declared mutants | 7/7 killed |
| Permanent CI jobs | 9/9 successful |
| Real PostgreSQL/pgvector integration | 1/1 successful |

## Runtime delta verified in PR #337

- explicit `[postgresql]` optional extra and lazy Psycopg loading;
- PostgreSQL 16, pgvector 0.8.2 and Psycopg 3.3.x preflight;
- TLS-required production path with an explicit local-test-only plaintext override;
- new allowlisted `velantrim_inactive_*` target schema;
- serializable transactional import from a verified completed logical bundle;
- target control state constrained to `active=false`;
- independent read-only canonical target re-hash;
- exact record-count, canonical-byte-count and SHA-256 equivalence per dataset;
- endpoint-bound, non-secret receipts and redacted database failures;
- no ANN indexes, runtime registration, activation, cutover, rollback or dual-write.

## Real integration evidence

Run `31256316532` used the ephemeral `pgvector/pgvector:0.8.2-pg16` service and verified:

- real import and a separate verification pass;
- PostgreSQL 16.14, pgvector 0.8.2 and Psycopg 3.3.4;
- `state=VERIFIED` and `active=false`;
- exact canonical equality for nodes, vectors, edges, entities, mentions and metadata;
- absence of HNSW/IVFFlat indexes;
- absence of credential-bearing material in receipts.

The workflow uses a passwordless localhost test service. This is test-only configuration,
not deployment guidance.

## Authority boundary

```text
physical L3 state       != strict Canon
logical bundle          != claim evidence
successful import       != backend activation
exact state equivalence != ordinary runtime availability
integration success     != production certification
```

Issue #332 is implemented by PR #337 only for inactive import and exact equivalence of the
approved bundle datasets. Exact-vs-ANN evaluation, cutover/fencing, rollback, server
backup/restore/upgrade lifecycle and active PostgreSQL runtime selection remain absent.

## Reproduction

```bash
pip install -e '.[dev,postgresql]'
pytest tests/ --cov=. --cov-fail-under=100
```

A real PostgreSQL 16 server with pgvector 0.8.2 is required for the dedicated integration
test.