# Bounded legacy retrieval benchmark

**Status:** informational methodology; not a production latency SLO.

## Purpose

Verify that the no-fingerprint compatibility path examines no more than its configured
candidate cap while the SQLite corpus grows through 1k, 10k and optional 30k facts.

## Run

```bash
python scripts/bench_legacy_retrieval.py --sizes 1000 10000
python scripts/bench_legacy_retrieval.py --sizes 30000 --json-out legacy-30k.json
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
