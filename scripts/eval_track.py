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
import tempfile
from datetime import datetime, timezone
from typing import Any, Dict, List

# Allow running as script from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import eval as _eval
import core as _core_pkg


def track(*, output_path: str = "eval_history.jsonl", lang: str = "en") -> Dict[str, Any]:
    """Run eval.run_baseline() and append a timestamped snapshot to output_path.

    The baseline run uses a temporary, isolated database so it never pollutes
    the live canon configured via VELANTRIM_DB / VELANTRIM_L3_PATH.

    Returns the appended record.
    """
    import core.memory as _mem
    import core.l3_graph as _l3

    with tempfile.TemporaryDirectory(prefix="velantrim-eval-track-") as _tmpdir:
        # Redirect L1 and L3 stores to the temp dir for the duration of the
        # baseline run.  Save both the env vars AND the module-level SQLITE_PATH
        # attribute (which is read at import time) so that in-process reuse of
        # the module never writes to the caller's live canon.
        _old_db = os.environ.get("VELANTRIM_DB")
        _old_l3 = os.environ.get("VELANTRIM_L3_PATH")
        _old_sqlite_path = _mem.SQLITE_PATH
        _tmp_db = os.path.join(_tmpdir, "eval.db")
        _tmp_l3 = os.path.join(_tmpdir, "l3.db")
        try:
            os.environ["VELANTRIM_DB"] = _tmp_db
            os.environ["VELANTRIM_L3_PATH"] = _tmp_l3
            _mem.SQLITE_PATH = _tmp_db

            # Flush caches so the baseline run starts with a clean slate
            # against the temp DB.
            _mem._L0.clear()
            _l3.reset_l3_graph()

            report = _eval.run_baseline(lang=lang)
        finally:
            # Restore original env vars and the module-level attribute.
            # Use dict-update style to avoid conditional branches for coverage.
            _restore_db = {k: v for k, v in [("VELANTRIM_DB", _old_db)]
                           if v is not None}
            _restore_l3 = {k: v for k, v in [("VELANTRIM_L3_PATH", _old_l3)]
                           if v is not None}
            os.environ.pop("VELANTRIM_DB", None)
            os.environ.pop("VELANTRIM_L3_PATH", None)
            os.environ.update(_restore_db)
            os.environ.update(_restore_l3)
            _mem.SQLITE_PATH = _old_sqlite_path
            # Flush caches so the next access reconnects to the restored path.
            _mem._L0.clear()
            _l3.reset_l3_graph()

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
        "unsupported_provenance": report["unsupported_provenance"],
        "contradiction_precision": con["precision"],
        "contradiction_recall": con["recall"],
        "contradiction_false_positive_rate": con["false_positive_rate"],
        "violations": report.get("boundary", {}).get("violations"),
        "refusal_correctness": report.get("boundary", {}).get("refusal_correctness"),
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

    header = ("| version | date | lang | hit@1 | hit@3 | hit@5 | mrr"
              " | trace_completeness | metadata_completeness | source_span_coverage"
              " | receipt_replay_survival | contradiction_P | contradiction_R |")
    sep    = "|---|---|---|---|---|---|---|---|---|---|---|---|---|"
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
            f"| {rec.get('hit_at_5', '')} "
            f"| {rec.get('mrr', '')} "
            f"| {rec.get('trace_completeness', '')} "
            f"| {rec.get('metadata_completeness', '')} "
            f"| {rec.get('source_span_coverage', '')} "
            f"| {rec.get('receipt_replay_survival', '')} "
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
