# Bounded legacy retrieval benchmark

**Status:** informational evidence; not a production latency SLO.  
**Recorded:** 2026-08-07, PR #321 benchmark run `31165503179`, artifact digest `sha256:718973fc1b90058b10c78be58999872fb6beea0ee98f013da768eaefc833e39f`.

## Purpose

Verify that the no-fingerprint compatibility path examines no more than its configured
candidate cap while the SQLite corpus grows through 1k, 10k and 30k facts.

## Recorded environment

```text
Python: 3.11.15
Platform: Linux 6.17.0-1021-azure x86_64, glibc 2.39
Processor: x86_64
Candidate limit: 256
Iterations per case: 30, after 5 warm-up queries
```

## Recorded results

| Corpus size | p50 | p95 | Max candidates examined | Bound held |
|---:|---:|---:|---:|:---:|
| 1,000 | 1.465 ms | 1.489 ms | 256 | yes |
| 10,000 | 1.469 ms | 1.493 ms | 256 | yes |
| 30,000 | 1.471 ms | 1.498 ms | 256 | yes |

The measured timings are contextual shared-runner observations. The load-bearing result is
that all three cases examined at most 256 candidates, including the 30k corpus.

## Reproduce

```bash
python scripts/bench_legacy_retrieval.py \
  --sizes 1000 10000 30000 \
  --candidate-limit 256 \
  --iterations 30 \
  --json-out bounded-legacy-retrieval.json
```

The script creates a temporary SQLite L3 store, inserts synthetic fact JSON without an
embedder fingerprint, executes a fixed family of lexical queries and reports:

- p50 latency;
- p95 latency;
- maximum candidates examined;
- whether the candidate bound held;
- Python/platform/processor metadata.

## Interpretation

The load-bearing invariant is:

```text
max_candidates_examined <= configured_candidate_limit
```

Latency on shared runners is contextual evidence only. It varies with CPU, filesystem,
Python and host load and must not be treated as a hard merge-blocking SLO.

The benchmark does not measure:

- vector retrieval quality;
- semantic recall outside the deterministic candidate window;
- TruthGate or Canon correctness;
- production concurrency or remote-service capacity;
- reindex duration.

Synthetic benchmark facts are not admitted memory and the temporary database is removed
after each case.
