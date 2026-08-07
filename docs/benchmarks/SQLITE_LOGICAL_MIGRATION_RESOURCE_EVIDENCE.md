# SQLite Logical Migration — Bounded Resource Evidence

**Status date:** 2026-08-08  
**Implementation PR:** #335  
**Validated runtime head:** `439df4af5a556b3c42ba9155e798f6fc35f65ecc`  
**Full exact-head CI:** `31223537748` — 9/9 successful  
**Benchmark head:** `da28ce18080c28fe98aa0fc05c51f486f859cff6`  
**Benchmark run:** `31224005804` — 2/2 successful

## Classification

This report is **local-first bounded-resource evidence**, not a production SLO, capacity
promise, institution-scale certification or PostgreSQL readiness claim.

The benchmark verifies that the issue #331 implementation crosses multiple cursor batches
without retaining complete datasets or global identifier sets in Python memory. It does not
raise the existing source, record, dataset or aggregate bundle limits.

## Reproduction

```bash
bash scripts/storage_migration_resource_benchmark.sh 1025 result-1025.json
bash scripts/storage_migration_resource_benchmark.sh 8193 result-8193.json
```

The runner creates a synthetic SQLite physical-L3 store containing nodes, vectors, edges,
entities, mentions and metadata. It then performs:

```text
SQLite source creation
→ deterministic logical export
→ export-internal independent verification
→ second independent verification
→ JSON resource report
```

The report records source and bundle bytes, timings, Python `tracemalloc` peak, Linux
`ru_maxrss`, dataset counts, vector dimension, batch size and active fail-closed limits.

## Environment

```text
Python: 3.11.15
Runner: ubuntu-24.04
Kernel: Linux 6.17.0-1020-azure x86_64
Batch size: 512 records
```

## Results

| Metric | 1,025 primary records | 8,193 primary records |
|---|---:|---:|
| Nodes | 1,025 | 8,193 |
| Vectors | 1,025 | 8,193 |
| Edges | 1,024 | 8,192 |
| Entities | 1,025 | 8,193 |
| Mentions | 1,025 | 8,193 |
| Source SQLite bytes | 450,560 | 3,141,632 |
| Bundle bytes | 360,629 | 2,869,434 |
| Export seconds, including internal verify | 0.649478 | 5.424900 |
| Second independent verify seconds | 0.361907 | 3.131820 |
| Python traced peak bytes | 1,338,163 | 1,339,001 |
| Process max RSS, Linux KiB | 23,324 | 25,600 |
| Vector dimension | 3 | 3 |

The primary-record count increased by approximately 8x while the measured Python-traced
peak changed by 838 bytes. Linux process max RSS increased by 2,276 KiB. These observations
are consistent with bounded cursor batches plus disk-backed sorting/reference indexes for
these two synthetic corpora and this runner image.

They do **not** prove constant memory for every payload shape, filesystem, Python build,
SQLite build, interruption mode or maximum accepted bundle. They also do not establish a
production latency or throughput target.

## Active fail-closed envelope

| Resource | Limit |
|---|---:|
| Control file | 1 MiB |
| Source SQLite file | 64 MiB |
| One canonical record | 1 MiB |
| Records per dataset | 200,000 |
| One dataset | 64 MiB |
| Aggregate JSONL | 384 MiB |

Increasing these limits requires a separate reviewed change with reproducible memory,
disk, time, failure-path and cleanup evidence.

## Implementation evidence

The bounded implementation provides:

- source cursor iteration through fixed `fetchmany()` batches;
- incremental canonical JSONL write, count and SHA-256;
- private disk-backed canonical edge sorting;
- same-descriptor hash-first and incremental parse verification;
- private disk-backed node/entity/reference indexes;
- bounded dangling-reference diagnostics;
- temporary-disk preflight;
- cleanup when temporary sorting or verification-index initialization fails;
- final file, exact-file-set and directory identity rechecks.

Failure-path tests cover oversized logical reads, short reads, descriptor mutation, I/O
errors and cleanup both before and after temporary verification-index connection creation.
The oversized-read test lowers the limit to the fixture size with `monkeypatch`; it does not
allocate the production 64 MiB dataset ceiling merely to exercise the branch.

Full CI evidence at the validated runtime head:

```text
Python 3.11: 2059 passed / 12 skipped / 0 failed
Python 3.12: same full coverage gate successful
9361 measured statements
100.00% line coverage
core/storage_migration.py: 626 / 626 statements
9 / 9 permanent CI jobs successful
```

## Authority and deployment boundary

```text
physical L3 state       != strict Canon
migration bundle        != claim evidence
successful verification != target activation
bounded local migration != PostgreSQL runtime
benchmark result        != production SLO
```

SQLite remains the current local-first runtime profile. PostgreSQL/pgvector, inactive
import, exact target equivalence, cutover, rollback, dual-write, distributed fencing and
server backup/upgrade lifecycle remain separate work under issue #332 and later phases.
