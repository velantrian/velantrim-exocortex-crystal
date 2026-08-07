# Crystal Verification Report

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `f03e24c85922d0bb46d6d9dfee98338972135908`  
**Verified tree:** `abf75283b382697b323ab69cfa7235b47171dace`  
**Validated implementation head:** `17ce10ffe12da93be50434c73d08f05a70a5922b`  
**Pull request:** #335  
**Exact-head CI:** `31224184351`  
**Resource benchmark CI:** `31224005804`

This is evidence for the tested repository state. It is not a production, legal, security,
PostgreSQL-readiness or institution-scale certification.

## Result

| Gate | Result |
|---|---:|
| Python 3.11 | 2059 passed / 12 skipped / 0 failed |
| Python 3.12 | 2059 passed / 12 skipped / 0 failed |
| Measured statements | 9361 |
| Line coverage | 100.00% |
| `core/storage_migration.py` | 626 / 626 statements |
| Ring Zero declared mutants | 7/7 killed |
| Permanent CI jobs | 9/9 successful |
| Resource benchmark jobs | 2/2 successful |

## Runtime delta verified in PR #335

- fixed-batch SQLite cursor iteration;
- incremental canonical JSONL write, count and SHA-256;
- private disk-backed canonical edge sorting;
- same-descriptor hash-first and incremental parse verification;
- private disk-backed node/entity/reference checks;
- bounded dangling-reference diagnostics;
- temporary-disk preflight and handled-failure cleanup;
- preserved schema, vector, canonical-ordering, file-identity and TOCTOU checks.

## Resource evidence

Benchmark run `31224005804` compared 1,025 and 8,193 primary-record corpora.

| Metric | 1,025 records | 8,193 records |
|---|---:|---:|
| Source SQLite | 450,560 B | 3,141,632 B |
| Bundle | 360,629 B | 2,869,434 B |
| Export including internal verify | 0.649478 s | 5.424900 s |
| Second independent verify | 0.361907 s | 3.131820 s |
| Python traced peak | 1,338,163 B | 1,339,001 B |
| Linux process max RSS | 23,324 KiB | 25,600 KiB |

See [the full resource report](./docs/benchmarks/SQLITE_LOGICAL_MIGRATION_RESOURCE_EVIDENCE.md).
These measurements support bounded behavior for the tested synthetic local-first corpora;
they are not a production SLO or proof for every payload shape or maximum accepted bundle.

## Active fail-closed limits

| Resource | Limit |
|---|---:|
| profile/control JSON | 1 MiB |
| source SQLite file | 64 MiB |
| one canonical record | 1 MiB |
| records per dataset | 200,000 |
| one dataset | 64 MiB |
| aggregate JSONL | 384 MiB |

## Authority and future-work boundary

```text
physical L3 state       != strict Canon
logical bundle          != claim evidence
successful verification != backend activation
bounded local migration != PostgreSQL runtime
benchmark result        != production SLO
```

Issue #331 is implemented by PR #335. PostgreSQL/pgvector runtime, inactive target import,
exact target equivalence, cutover, rollback, dual-write and distributed fencing remain
absent. Issue #332 governs only the next inactive-import/equivalence phase.

## Reproduction

```bash
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
bash scripts/storage_migration_resource_benchmark.sh 1025 result-1025.json
bash scripts/storage_migration_resource_benchmark.sh 8193 result-8193.json
```
