#!/usr/bin/env python
"""Velantrim Crystal — evaluation quality gate (grant WP3).

Runs the baseline evaluation harness over the curated bundled corpus in an
isolated, ephemeral canon, writes machine- and human-readable artifacts
(``metrics.jsonl`` + ``eval_report.md``), and exits non-zero if any metric falls
below its regression threshold (``core.eval.DEFAULT_GATE`` / ``_GATE_MAX``). Wired
into CI so retrieval / grounding / contradiction quality cannot silently drop
between releases.

    python scripts/eval_gate.py [--out-dir DIR]

Deterministic: dependency-free hashing embedder + extractive answerer.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path


def _isolate_canon() -> None:
    """Point every store at a throwaway temp dir so the gate never touches real
    data and runs from a clean, deterministic canon."""
    tmp = tempfile.mkdtemp(prefix="velantrim-eval-gate-")
    os.environ["VELANTRIM_L3_PATH"] = str(Path(tmp) / "l3.db")
    os.environ["VELANTRIM_DB"] = str(Path(tmp) / "l1.db")
    os.environ["VELANTRIM_DEMO_SEED"] = "0"
    os.environ.pop("VELANTRIM_NEUROCORE", None)


def main() -> int:
    parser = argparse.ArgumentParser(description="Velantrim evaluation quality gate")
    parser.add_argument("--out-dir", default=".",
                        help="directory for metrics.jsonl + eval_report.md (default: .)")
    args = parser.parse_args()

    _isolate_canon()
    # Import only after the environment is set, so backends bind to the temp dir.
    from core import eval as ev

    report = ev.run_baseline(detail=True)
    verdict = ev.gate(report)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # metrics.jsonl: one JSON object per line — aggregate first, then per-case.
    with (out / "metrics.jsonl").open("w", encoding="utf-8") as fh:
        aggregate = {k: v for k, v in report.items() if k != "cases_detail"}
        fh.write(json.dumps({"kind": "aggregate", **aggregate}, ensure_ascii=False) + "\n")
        for case in report.get("cases_detail", []):
            fh.write(json.dumps({"kind": "case", **case}, ensure_ascii=False) + "\n")

    (out / "eval_report.md").write_text(ev.format_report_md(report), encoding="utf-8")

    # Console summary.
    ret = report["retrieval"]
    con = report["contradiction"]
    print("Velantrim evaluation gate")
    print(f"  cases:        {report['cases']}")
    print(f"  retrieval:    hit@1={ret['hit@1']} hit@3={ret['hit@3']} "
          f"hit@5={ret['hit@5']} mrr={ret['mrr']}")
    print(f"  grounding:    trace={report['trace_completeness']} "
          f"metadata={report['metadata_completeness']} "
          f"span={report['source_span_coverage']} "
          f"strict_span={report['strict_source_span_coverage']} "
          f"receipts={report['receipt_replay_survival']} "
          f"unsupported={report['unsupported_provenance']} "
          f"lineage_known={report['lineage']['known_lineage_coverage']} "
          f"lineage_dupes={report['lineage']['same_lineage_duplicate_rate']}")
    print(f"  contradiction: precision={con['precision']} recall={con['recall']} "
          f"fpr={con['false_positive_rate']}")
    bnd = report.get("boundary", {})
    if bnd:
        print(f"  boundary:     cases={bnd['cases']} "
              f"refusal_correctness={bnd['refusal_correctness']} "
              f"violations={bnd['violations']}")

    if verdict["passed"]:
        print("✅ quality gate PASSED")
        return 0

    print("❌ quality gate FAILED:")
    for f in verdict["failures"]:
        print(f"   {f['metric']} = {f['value']}  (must be {f['op']} {f['threshold']})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
