# L3 Retrieval-Scale Smoke Benchmark

**Status:** deterministic local benchmark + scheduled informational history  
**Benchmark:** [`scripts/bench_l3_retrieval.py`](../../scripts/bench_l3_retrieval.py)  
**History tooling:** [`scripts/l3_benchmark_history.py`](../../scripts/l3_benchmark_history.py)  
**Workflow:** [`.github/workflows/l3-benchmark-history.yml`](../../.github/workflows/l3-benchmark-history.yml)  
**Issue:** #218

This benchmark measures raw SQLite L3 vector-search latency. It does not measure
answer correctness, TruthGate quality or full query-pipeline latency. Those are
separate evaluation concerns.

## Purpose

Crystal's default SQLite backend performs an exact vector scan. The benchmark
provides a deterministic smoke workload so maintainers can observe how latency,
load time and on-disk size change as the synthetic graph grows.

It is a reviewer and engineering signal, not a production SLO.

## Workload

For each requested fact count, the script:

1. creates an isolated temporary SQLite L3 store;
2. forces the dependency-free hashing embedder;
3. inserts deterministic synthetic `WORLD_FACT` nodes directly into L3;
4. runs 10 discarded warmup searches;
5. runs 100 measured searches over 20 deterministic query templates;
6. records p50, p95, max, load time and open database size.

Fixed workload fields are included in every JSON size row:

```text
measured_searches_total = 100
a query_templates       = 20
top_k                    = 10
warmup_queries           = 10
```

The label above is descriptive; the actual JSON key is `query_templates`.

## What it measures

- `SqliteL3Graph.vector_search()` exact-scan performance;
- deterministic hashing-vector generation already used by the project;
- synthetic bulk load time;
- open SQLite database/WAL/SHM size;
- Python, platform and best-effort commit metadata.

## What it does not measure

- full `core.pipeline.retrieve()` or `core.query_pipeline.query()` latency;
- Guardian, TruthGate, CanonicalView, TRACE or Receipt overhead;
- retrieval relevance or semantic embedding quality;
- LadybugDB, Neo4j or other optional backend performance;
- realistic domain corpora or graph-walk density;
- production capacity, availability or SLO compliance.

Synthetic facts are inserted directly through `merge_fact()` because the target
of this benchmark is backend retrieval mechanics, not admission policy.

## Local use

```bash
# Default smoke sizes
python scripts/bench_l3_retrieval.py

# Explicit sizes
python scripts/bench_l3_retrieval.py --sizes 100,1000,10000

# Machine-readable result
python scripts/bench_l3_retrieval.py \
  --sizes 1000,10000 \
  --json-out /tmp/l3-raw.json

# Package a versioned history artifact
python scripts/l3_benchmark_history.py pack \
  --input /tmp/l3-raw.json \
  --output /tmp/l3-history.json \
  --summary-out /tmp/l3-summary.md
```

The benchmark uses only the standard library and existing Crystal code. It does
not require network access or an external fixture.

## Scheduled history

The `L3 Benchmark History` workflow runs weekly and can also be started manually
with an explicit comma-separated size list.

Each run uploads, for up to 90 days:

- `raw.json` — unchanged output from the existing benchmark;
- `history.json` — schema-versioned envelope with workflow metadata;
- `summary.md` — compact result table;
- `benchmark.log` — console output.

The workflow also writes `summary.md` to the GitHub Actions job summary.

```text
existing deterministic benchmark
        ↓
versioned history envelope
        ↓
90-day Actions artifact sequence
```

The workflow is separate from the normal pull-request CI matrix. A slow hosted
runner does not block code merge.

## Comparing downloaded artifacts

```bash
python scripts/l3_benchmark_history.py compare \
  --baseline previous-history.json \
  --current current-history.json \
  --output comparison.md \
  --warn-ratio 1.25
```

Comparison is informational:

- it compares only shared fact counts;
- it reports whether backend/embedder metadata matches;
- it checks that measured-search count, query-template count, `top_k` and warmup
  workload match for each size;
- it reports p50/p95 ratios;
- ratios above the selected threshold produce a warning marker, not a failed SLO.

A warning should be reproduced on controlled hardware before it is treated as a
performance regression.

## Historical local baseline

Historical pre-optimization run:

| Facts | Load time | p50 | p95 | max | DB size (open) |
|---:|---:|---:|---:|---:|---:|
| 100 | 0.150 s | 37.53 ms | 40.79 ms | 43.59 ms | 3.48 MB |
| 1,000 | 1.384 s | 390.42 ms | 399.91 ms | 422.02 ms | 16.63 MB |
| 10,000 | 14.763 s | 4,011.84 ms | 4,142.27 ms | 4,426.21 ms | 132.85 MB |

Environment: Python 3.11.15,
`Linux-6.18.5-x86_64-with-glibc2.39`, commit `2507c73-dirty`, SQLite backend,
hashing embedder.

These values show approximately linear exact-scan growth on that machine. They
must not be presented as universal Crystal latency.

## Joined-scan optimization A/B

Same-machine measurements from 2026-07-10:

| Facts | Version | p50 | p95 | max |
|---:|:---|---:|---:|---:|
| 100 | before | 30.867 ms | 37.729 ms | 38.490 ms |
| 100 | after | 24.532 ms | 30.297 ms | 37.012 ms |
| 1,000 | before | 309.465 ms | 340.945 ms | 378.449 ms |
| 1,000 | after | 250.736 ms | 283.286 ms | 300.451 ms |

Observed local reduction: 20.5% p50 / 19.7% p95 at 100 facts and 19.0% p50 /
16.9% p95 at 1,000 facts. The portable regression guarantee is structural: the
SQLite path materializes candidates with one joined `SELECT` rather than one
vector scan plus per-positive-candidate point reads.

The path remains O(N); this optimization did not introduce an ANN index.

## History schema boundary

`history.json` wraps but does not rewrite the benchmark result:

```json
{
  "history_schema_version": 1,
  "collected_at": "2026-08-01T00:00:00Z",
  "run": {
    "repository": "owner/repository",
    "run_id": "...",
    "sha": "...",
    "runner_os": "Linux"
  },
  "result": {
    "benchmark": "l3_retrieval_scale",
    "backend": "sqlite",
    "embedder": "hashing",
    "sizes": []
  }
}
```

The packer validates required fields, non-negative metrics, unique positive fact
sizes and ordered p50 ≤ p95 ≤ max latency values. Malformed artifacts fail
packaging rather than becoming history.

## Caveats

- Hosted-runner history is useful for trends, not stable absolute SLOs.
- GitHub artifact retention is bounded; important release evidence should be
  exported separately when needed.
- Exact SQLite scan latency remains close to linear in fact count.
- The hashing fixture intentionally shares vocabulary across facts; it is not a
  retrieval-quality corpus.
- Open database size includes active sidecar files.
- 30,000 facts remains opt-in because exact-scan runs can be slow on constrained
  machines.
- Backend/embedder/workload equality still does not guarantee identical hardware,
  filesystem, SQLite build, cache state or host load.
