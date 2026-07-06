# L3 Retrieval-Scale Smoke Benchmark

**Status:** benchmark baseline only. No runtime behaviour change.
**Script:** [`scripts/bench_l3_retrieval.py`](../../scripts/bench_l3_retrieval.py)
**Issue:** #218

This document is a companion to
[`docs/benchmarks/BENCHMARK_METHODOLOGY.md`](./BENCHMARK_METHODOLOGY.md), which
benchmarks a different thing: **that** document measures the value TruthGate
and Trace/Receipt add to answer *correctness/verifiability*. **This** document
measures raw retrieval *latency at scale* — a performance characteristic, not
a correctness one. Do not conflate the two.

## 1. Purpose

Velantrim Crystal has strong correctness/eval/security discipline (100% test
coverage, a deterministic eval gate), but until now had no reproducible
measurement of how `core.l3_graph`'s retrieval latency behaves as the local
knowledge base grows. This benchmark exists to establish that baseline —
**not** to optimize anything. It is a smoke measurement for reviewer
confidence and future engineering decisions, not a production SLO.

## 2. What it measures

- `core.l3_graph`'s SQLite backend (`SqliteL3Graph`) — the dependency-free,
  local-first default when the optional LadybugDB backend is not installed.
- `vector_search(query_vector, k=10)` latency directly, over a fixed set of
  20 deterministic queries (10 topic-based + 10 group-based), each run
  `10` times warmup (discarded) + `100` times measured.
- Bulk `merge_fact()` load time for the synthetic corpus.
- On-disk database size at measurement time (includes any active WAL/SHM
  sidecar files — SQLite may checkpoint and shrink this further on a clean
  close, so this number is "size while the benchmark connection is open,"
  not "final resting size").
- Python version, platform, and the repository's commit SHA (best-effort;
  `"unknown"` if `git` is unavailable, e.g. a tarball checkout).

## 3. What it does NOT measure

- **Not the full `core.pipeline.retrieve()` path.** That path adds embedding
  the query, demo-seed lookup, and a multi-hop graph-walk over
  `CO_OCCURRED`/`CONTRADICTS`/`SUPERSEDED_BY` edges. The synthetic benchmark
  facts carry no such edges, so a graph-walk would be a near no-op here and
  would only muddy what is actually being measured: the L3 backend's own
  `vector_search()`.
- **Not Guardian or TruthGate overhead.** Synthetic facts are written
  directly via `graph.merge_fact()`, bypassing `core.ingest.ingest()`'s
  Guardian → TruthGate admission path entirely. This benchmark is about
  retrieval, not admission.
- **Not the optional LadybugDB or Neo4j backends.** Both are explicitly
  out of scope for a dependency-free, reproducible-anywhere benchmark; the
  SQLite backend's docstring already notes LadybugDB "adds a real vector
  index for scale," which this benchmark does not attempt to verify.
- **Not a production capacity guarantee, and not an optimization.** No
  retrieval algorithm, schema, or TruthGate change is part of this work.
- **Not embedding *quality*.** The `hashing` embedder is deterministic and
  dependency-free but is explicitly documented elsewhere
  (`core/embedding.py`) as not a semantic embedder; this benchmark only
  cares about its speed and determinism, not retrieval relevance.

## 4. How to run

```bash
# Default sizes (1,000 / 10,000 facts) — practical for a local run.
python scripts/bench_l3_retrieval.py

# Explicit sizes:
python scripts/bench_l3_retrieval.py --sizes 1000,10000

# 30,000 is opt-in — it is slow on constrained machines (see Caveats):
python scripts/bench_l3_retrieval.py --sizes 1000,10000,30000

# Write machine-readable output:
python scripts/bench_l3_retrieval.py --sizes 1000,10000 --json-out /tmp/l3_bench.json

# Keep the temp SQLite files instead of deleting them after each size:
python scripts/bench_l3_retrieval.py --sizes 1000 --keep-artifacts
```

The script is stdlib + existing project code only — no new dependency, no
network access, no external fixture file. Facts and queries are generated
from a fixed, deterministic scheme (`bench_fact_000001` /
`"Benchmark fact 000001 belongs to topic_07 and group_03."`); the same size
produces the same corpus and the same query set on every run. Absolute
latency numbers still depend on the machine, not just the code — see
Caveats.

## 5. Example output

This is real output from this repository's own baseline run (section 6), not
an illustrative placeholder:

```text
Velantrim L3 retrieval-scale smoke benchmark
Python: 3.11.15  Platform: Linux-6.18.5-x86_64-with-glibc2.39
Commit: 2507c73  Backend: sqlite  Embedder: hashing

--- 1000 facts ---
  load: 1.384s  p50: 390.415ms  p95: 399.914ms  max: 422.019ms  db: 16625288 bytes
```

JSON shape (`--json-out`):

```json
{
  "benchmark": "l3_retrieval_scale",
  "commit": "2507c73",
  "backend": "sqlite",
  "embedder": "hashing",
  "python_version": "3.11.15",
  "platform": "Linux-6.18.5-x86_64-with-glibc2.39",
  "sizes": [
    {
      "facts": 1000,
      "queries": 100,
      "top_k": 10,
      "warmup_queries": 10,
      "p50_ms": 390.415,
      "p95_ms": 399.914,
      "max_ms": 422.019,
      "load_seconds": 1.384,
      "db_size_bytes": 16625288
    }
  ]
}
```

## 6. Current baseline (local run)

Measured in this session's sandboxed container — see Caveats before reading
anything into absolute numbers.

```text
python scripts/bench_l3_retrieval.py --sizes 100,1000,10000 --json-out /tmp/l3_bench_full.json
```

Python `3.11.15`, `Linux-6.18.5-x86_64-with-glibc2.39`, commit `2507c73`,
backend `sqlite`, embedder `hashing`, `top_k=10`, `10` warmup + `100`
measured queries per size.

| Facts | Load time | p50 | p95 | max | DB size (open) |
|---:|---:|---:|---:|---:|---:|
| 100 | 0.150 s | 37.53 ms | 40.79 ms | 43.59 ms | 3.48 MB |
| 1,000 | 1.384 s | 390.42 ms | 399.91 ms | 422.02 ms | 16.63 MB |
| 10,000 | 14.763 s | 4,011.84 ms | 4,142.27 ms | 4,426.21 ms | 132.85 MB |

**30,000 facts was not run for this baseline.** The 10,000-fact size alone
took ~8.5 minutes wall-clock in this sandboxed container; extrapolating the
~10x-per-10x-facts scaling observed between the three measured sizes, 30,000
would be expected to take on the order of tens of minutes here. This is
itself a direct illustration of the Caveats section below (retrieval latency
scaling with corpus size due to the per-candidate `get_fact()` pattern), not
an omission — a future run on faster hardware, or after the follow-up
retrieval-algorithm work referenced in Caveats, may find `--sizes
1000,10000,30000` practical.

Latency scales close to linearly with fact count across the three measured
points (100 → 1,000 is ~10.4x; 1,000 → 10,000 is ~10.3x), consistent with
the `get_fact()`-per-candidate behaviour described in Caveats: with this
synthetic corpus, most candidates clear the `similarity > 0` bar, so
`vector_search()`'s cost is dominated by roughly one point-query per stored
fact, not by the cosine-scoring pass itself.

## 7. Caveats

- **This is a local smoke baseline, not a universal performance guarantee.**
  Numbers depend on hardware, Python version, filesystem, SQLite build,
  backend, and machine load at run time. Do not cite these numbers as a
  general Crystal performance claim.
- **`vector_search()` does more than a single linear scan.** For every
  candidate row whose cosine similarity is `> 0`, the SQLite backend issues
  a *separate* `get_fact()` point-query to materialize the full node before
  scoring and truncating to `k`. With the synthetic corpus (short,
  vocabulary-overlapping claims), most or all candidates clear the `> 0`
  bar, so a single `vector_search()` call can issue on the order of *N*
  additional point-queries, not just one scan of the vectors table. This
  benchmark surfaces that behaviour as observed; it does not change it —
  that would be retrieval-algorithm work, explicitly out of scope for this
  PR (tracked as a possible follow-up, not started here).
- **30,000 facts can be slow on constrained machines**, consistent with the
  point above — the per-query cost is not fixed, it grows with corpus size.
  `--sizes` defaults to `1000,10000` for this reason; 30,000 is opt-in.
- **The synthetic corpus is adversarial-adjacent for a hashing embedder in
  one specific way**: all claims share most of their vocabulary
  ("Benchmark fact NNNNNN belongs to topic_NN and group_NN"), so genuine
  semantic separation is weak and most facts will show *some* similarity to
  any query. This is a deliberate, disclosed property of the fixture, not a
  hidden skew — real-world corpora with more varied text may or may not
  trigger the same `get_fact()`-per-candidate pattern to the same degree.
- **Database size at measurement time includes any open WAL/SHM sidecar
  files**; the number is not necessarily the file size after a clean
  shutdown/checkpoint.
- **This benchmark does not run in CI** and is not a merge gate. It is a
  manually-invoked local tool.
