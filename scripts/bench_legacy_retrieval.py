#!/usr/bin/env python3
"""Informational benchmark for the bounded no-fingerprint retrieval path.

This benchmark is not a merge-blocking latency SLO. It verifies that Python
candidate work remains capped as the SQLite corpus grows and reports p50/p95
latency with environment metadata. Run 30k explicitly when resources allow.
"""
from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.l3_graph import SqliteL3Graph  # noqa: E402
from core.legacy_retrieval import bounded_legacy_retrieve  # noqa: E402


def _percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * fraction))))
    return ordered[index]


def _seed(graph: SqliteL3Graph, size: int) -> None:
    rows = []
    for index in range(size):
        topic = index % 97
        payload = {
            "fact_id": f"bench:{index:08d}",
            "claim": f"bounded legacy topic {topic} group {index % 13}",
            "source": "synthetic-benchmark",
            "confidence": 0.9,
            "epistemic_state": "Validated",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "truth_status": "VERIFIED",
            "restricted": False,
        }
        rows.append((payload["fact_id"], json.dumps(payload)))
    with graph._lock, graph._conn:
        graph._conn.executemany("INSERT INTO nodes(fact_id, data) VALUES(?, ?)", rows)
        graph._conn.execute("DELETE FROM meta WHERE key = 'embedder_fp'")


def run_case(size: int, *, candidate_limit: int, iterations: int) -> dict:
    with tempfile.TemporaryDirectory(prefix="velantrim-legacy-bench-") as tmp:
        graph = SqliteL3Graph(str(Path(tmp) / "l3.db"))
        try:
            _seed(graph, size)
            timings = []
            examined = []
            for index in range(iterations + 5):
                query = f"bounded legacy topic {index % 97}"
                started = time.perf_counter()
                hits = bounded_legacy_retrieve(
                    query,
                    k=5,
                    graph=graph,
                    candidate_limit=candidate_limit,
                )
                elapsed_ms = (time.perf_counter() - started) * 1000.0
                if index >= 5:
                    timings.append(elapsed_ms)
                    examined.append(
                        max(
                            (hit.get("_legacy_candidates_examined", 0) for hit in hits),
                            default=min(size, candidate_limit),
                        )
                    )
            return {
                "size": size,
                "candidate_limit": candidate_limit,
                "iterations": iterations,
                "p50_ms": round(statistics.median(timings), 3),
                "p95_ms": round(_percentile(timings, 0.95), 3),
                "max_candidates_examined": max(examined, default=0),
                "candidate_bound_held": max(examined, default=0) <= candidate_limit,
            }
        finally:
            graph.close()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[1000, 10000])
    parser.add_argument("--candidate-limit", type=int, default=256)
    parser.add_argument("--iterations", type=int, default=30)
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args(argv)
    if any(size < 1 for size in args.sizes):
        parser.error("sizes must be positive")
    if args.iterations < 1:
        parser.error("iterations must be positive")

    report = {
        "benchmark": "bounded_legacy_retrieval",
        "informational_only": True,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "cases": [
            run_case(
                size,
                candidate_limit=args.candidate_limit,
                iterations=args.iterations,
            )
            for size in args.sizes
        ],
        "caveat": (
            "Hosted/shared-runner timings are not a hard SLO. The invariant under "
            "test is candidate work, not an absolute latency threshold."
        ),
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    return 0 if all(case["candidate_bound_held"] for case in report["cases"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
