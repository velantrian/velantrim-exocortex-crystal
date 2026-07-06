# scripts/bench_l3_retrieval.py
# Velantrim Crystal — L3 retrieval-scale smoke benchmark (issue #218)
#
# Measures how core.l3_graph's SQLite backend vector_search() latency behaves
# as the canonical graph grows, using synthetic, deterministic facts. This is
# a local smoke baseline, not a performance guarantee or an optimization —
# see docs/benchmarks/L3_RETRIEVAL_SCALE.md for full scope and caveats.
#
# Dependency-free: stdlib + existing project code only. No network. All data
# is synthetic and written to a temp directory, removed after each size
# unless --keep-artifacts is passed.
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List

# Allow running as a script from the project root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force the dependency-free, deterministic backends regardless of what is
# installed in the environment or set by the caller's shell — a benchmark
# that silently used a different embedder/backend on different machines
# would not be reproducible.
os.environ["VELANTRIM_EMBEDDER"] = "hashing"
os.environ["VELANTRIM_L3_BACKEND"] = "sqlite"

from core.embedding import get_embedder  # noqa: E402
from core.l3_graph import get_l3_graph  # noqa: E402

_TOPICS = [f"topic_{i:02d}" for i in range(10)]
_GROUPS = [f"group_{i:02d}" for i in range(10)]
_WARMUP_QUERIES = 10
_MEASURED_QUERIES = 100
_TOP_K = 10
_NOW = "2026-01-01T00:00:00+00:00"


def _git_commit() -> str:
    """Short commit SHA, or 'unknown' if git is unavailable (e.g. a tarball
    checkout) — never fails the benchmark over this."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root, capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:  # noqa: BLE001 — commit SHA is informational only
        pass
    return "unknown"


def _synthetic_fact(i: int) -> Dict[str, Any]:
    """Deterministic synthetic fact — content depends only on i, so results
    are reproducible across runs and machines. Shape matches what a real
    ingested EXTERNAL WORLD_FACT looks like once merged into L3
    (core/pipeline.py's _l3_payload), so the benchmark exercises the same
    node shape retrieval already handles — no new semantics invented."""
    topic = _TOPICS[i % len(_TOPICS)]
    group = _GROUPS[(i // len(_TOPICS)) % len(_GROUPS)]
    return {
        "fact_id": f"bench_fact_{i:06d}",
        "claim": f"Benchmark fact {i:06d} belongs to {topic} and {group}.",
        "source": "synthetic_benchmark",
        "confidence": 0.9,
        "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "significance": 0.5,
        "created_at": _NOW,
        "updated_at": _NOW,
        "metadata": {"topic": topic, "group": group},
    }


def _query_texts() -> List[str]:
    """Deterministic query set: one query per topic, one per group. Not
    tuned to make results look good — plain natural-language phrasing."""
    return [f"Tell me about {t}" for t in _TOPICS] + \
           [f"Tell me about {g}" for g in _GROUPS]


def _percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    k = (len(values) - 1) * (pct / 100.0)
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    if lo == hi:
        return values[lo]
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def _dir_size_bytes(path: str) -> int:
    total = 0
    for dirpath, _dirnames, filenames in os.walk(path):
        for name in filenames:
            fp = os.path.join(dirpath, name)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total


def run_one_size(n: int, keep_artifacts: bool) -> Dict[str, Any]:
    """Load n synthetic facts into a fresh, isolated SQLite L3 backend, then
    measure vector_search() latency over a fixed warmup + measured query set.
    """
    tmpdir = tempfile.mkdtemp(prefix=f"velantrim_bench_{n}_")
    os.environ["VELANTRIM_L3_PATH"] = os.path.join(tmpdir, "l3.db")
    # backend="sqlite" is explicit, so get_l3_graph() returns a fresh,
    # uncached instance (core/_registry.py only caches the backend=None
    # default path) — each size gets its own connection, closed below.
    graph = get_l3_graph("sqlite")
    embedder = get_embedder()

    t0 = time.perf_counter()
    for i in range(n):
        graph.merge_fact(_synthetic_fact(i))
    load_seconds = time.perf_counter() - t0

    query_vectors = [embedder.embed(q) for q in _query_texts()]

    for i in range(_WARMUP_QUERIES):
        graph.vector_search(query_vectors[i % len(query_vectors)], k=_TOP_K)

    latencies_ms: List[float] = []
    for i in range(_MEASURED_QUERIES):
        vec = query_vectors[i % len(query_vectors)]
        t0 = time.perf_counter()
        graph.vector_search(vec, k=_TOP_K)
        latencies_ms.append((time.perf_counter() - t0) * 1000.0)

    db_size_bytes = _dir_size_bytes(tmpdir)
    graph.close()

    result = {
        "facts": n,
        "queries": len(latencies_ms),
        "top_k": _TOP_K,
        "warmup_queries": _WARMUP_QUERIES,
        "p50_ms": round(_percentile(latencies_ms, 50), 3),
        "p95_ms": round(_percentile(latencies_ms, 95), 3),
        "max_ms": round(max(latencies_ms), 3),
        "load_seconds": round(load_seconds, 3),
        "db_size_bytes": db_size_bytes,
    }

    if keep_artifacts:
        result["artifact_dir"] = tmpdir
    else:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return result


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Velantrim L3 retrieval-scale smoke benchmark (issue #218). "
                    "Measures current behaviour; does not optimize it.")
    parser.add_argument(
        "--sizes", default="1000,10000",
        help="Comma-separated fact counts, e.g. 1000,10000,30000 "
             "(default: 1000,10000 — 30000 is opt-in, it is slow on some machines)")
    parser.add_argument(
        "--json-out", default=None,
        help="Optional path to write the full JSON results")
    parser.add_argument(
        "--keep-artifacts", action="store_true",
        help="Keep the temp SQLite files instead of deleting them after each size")
    args = parser.parse_args(argv)

    sizes = [int(s.strip()) for s in args.sizes.split(",") if s.strip()]

    commit = _git_commit()
    print("Velantrim L3 retrieval-scale smoke benchmark")
    print(f"Python: {platform.python_version()}  Platform: {platform.platform()}")
    print(f"Commit: {commit}  Backend: sqlite  Embedder: hashing")
    print()

    results = []
    for n in sizes:
        print(f"--- {n} facts ---")
        r = run_one_size(n, args.keep_artifacts)
        results.append(r)
        print(f"  load: {r['load_seconds']}s  "
              f"p50: {r['p50_ms']}ms  p95: {r['p95_ms']}ms  max: {r['max_ms']}ms  "
              f"db: {r['db_size_bytes']} bytes")
        print()

    payload = {
        "benchmark": "l3_retrieval_scale",
        "commit": commit,
        "backend": "sqlite",
        "embedder": "hashing",
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "sizes": results,
    }

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"JSON written to {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
