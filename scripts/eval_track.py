# scripts/eval_track.py
# Velantrim Crystal — per-release evaluation tracking (grant WP3)
#
# Appends a timestamped eval snapshot to eval_history.jsonl after each run.
# Use `--report` to print a Markdown trend table from the history file.
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

# Allow running as script from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import eval as _eval
import core as _core_pkg


def track(*, output_path: str = "eval_history.jsonl", lang: str = "en") -> Dict[str, Any]:
    """Run eval.run_baseline() and append a timestamped snapshot to output_path.

    Returns the appended record.
    """
    report = _eval.run_baseline(lang=lang)

    ret = report["retrieval"]
    con = report["contradiction"]

    record: Dict[str, Any] = {
        "version": _core_pkg.__version__,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "lang": lang,
        "hit_at_1": ret["hit@1"],
        "hit_at_3": ret["hit@3"],
        "hit_at_5": ret["hit@5"],
        "mrr": ret["mrr"],
        "trace_completeness": report["trace_completeness"],
        "metadata_completeness": report["metadata_completeness"],
        "source_span_coverage": report["source_span_coverage"],
        "receipt_replay_survival": report["receipt_replay_survival"],
        "contradiction_precision": con["precision"],
        "contradiction_recall": con["recall"],
    }

    with open(output_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def load_history(path: str) -> List[Dict[str, Any]]:
    """Read a JSONL history file and return a list of records (oldest first).

    Returns [] if the file does not exist.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]
    except FileNotFoundError:
        return []


def format_trend_md(history: List[Dict[str, Any]]) -> str:
    """Return a Markdown table of eval history.

    Columns: version, date, lang, hit@1, hit@3, mrr, contradiction_P, contradiction_R
    Returns "No eval history found." for empty history.
    """
    if not history:
        return "No eval history found."

    header = "| version | date | lang | hit@1 | hit@3 | mrr | contradiction_P | contradiction_R |"
    sep    = "|---|---|---|---|---|---|---|---|"
    rows = []
    for rec in history:
        # Truncate ISO timestamp to date portion for readability
        ts = rec.get("timestamp", "")
        date = ts[:10] if ts else ""
        rows.append(
            f"| {rec.get('version', '')} "
            f"| {date} "
            f"| {rec.get('lang', '')} "
            f"| {rec.get('hit_at_1', '')} "
            f"| {rec.get('hit_at_3', '')} "
            f"| {rec.get('mrr', '')} "
            f"| {rec.get('contradiction_precision', '')} "
            f"| {rec.get('contradiction_recall', '')} |"
        )

    return "\n".join([header, sep] + rows)


def main(argv: List[str] | None = None) -> int:
    """CLI entry point for per-release eval tracking."""
    parser = argparse.ArgumentParser(
        description="Velantrim Crystal — per-release eval tracking (grant WP3)"
    )
    parser.add_argument(
        "--output", default="eval_history.jsonl",
        help="path to JSONL history file (default: eval_history.jsonl)"
    )
    parser.add_argument(
        "--lang", default="en", choices=["en", "ru", "de", "fr"],
        help="eval corpus language (default: en)"
    )
    parser.add_argument(
        "--report", action="store_true",
        help="print Markdown trend table from history file instead of running eval"
    )
    args = parser.parse_args(argv)

    if args.report:
        history = load_history(args.output)
        print(format_trend_md(history))
        return 0

    record = track(output_path=args.output, lang=args.lang)
    print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
