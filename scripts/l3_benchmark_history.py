#!/usr/bin/env python3
"""Package and compare L3 retrieval benchmark artifacts.

This module does not run a second benchmark. It validates and wraps the JSON
produced by scripts/bench_l3_retrieval.py with content-light workflow metadata,
creates a Markdown summary, and compares two downloaded history artifacts.
Latency comparison is informational by default and never changes Crystal trust
or admission policy.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any, Mapping, Optional, Sequence

HISTORY_SCHEMA_VERSION = 1
BENCHMARK_NAME = "l3_retrieval_scale"
_RUN_FIELDS = (
    "repository",
    "workflow",
    "event",
    "run_id",
    "run_number",
    "run_attempt",
    "ref",
    "sha",
    "runner_os",
    "runner_arch",
)
_SIZE_FIELDS = (
    "facts",
    "measured_searches_total",
    "query_templates",
    "top_k",
    "warmup_queries",
    "p50_ms",
    "p95_ms",
    "max_ms",
    "load_seconds",
    "db_size_bytes",
)


def _nonblank(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-blank string")
    return value.strip()


def _number(value: Any, field: str, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    result = float(value)
    if result < minimum:
        raise ValueError(f"{field} must be >= {minimum}")
    return result


def validate_raw_result(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and copy the existing benchmark JSON without changing values."""
    if not isinstance(raw, Mapping):
        raise ValueError("benchmark result must be a mapping")
    if raw.get("benchmark") != BENCHMARK_NAME:
        raise ValueError(f"benchmark must be {BENCHMARK_NAME!r}")

    result = {
        "benchmark": BENCHMARK_NAME,
        "commit": _nonblank(raw.get("commit"), "commit"),
        "backend": _nonblank(raw.get("backend"), "backend"),
        "embedder": _nonblank(raw.get("embedder"), "embedder"),
        "python_version": _nonblank(raw.get("python_version"), "python_version"),
        "platform": _nonblank(raw.get("platform"), "platform"),
        "sizes": [],
    }

    sizes = raw.get("sizes")
    if not isinstance(sizes, list) or not sizes:
        raise ValueError("sizes must be a non-empty list")

    seen: set[int] = set()
    for index, item in enumerate(sizes):
        if not isinstance(item, Mapping):
            raise ValueError(f"sizes[{index}] must be a mapping")
        missing = [field for field in _SIZE_FIELDS if field not in item]
        if missing:
            raise ValueError(f"sizes[{index}] missing fields: {', '.join(missing)}")

        facts_value = item["facts"]
        if isinstance(facts_value, bool) or not isinstance(facts_value, int):
            raise ValueError(f"sizes[{index}].facts must be an integer")
        if facts_value <= 0:
            raise ValueError(f"sizes[{index}].facts must be > 0")
        if facts_value in seen:
            raise ValueError(f"duplicate fact size: {facts_value}")
        seen.add(facts_value)

        normalized = dict(item)
        for field in (
            "measured_searches_total",
            "query_templates",
            "top_k",
            "warmup_queries",
            "db_size_bytes",
        ):
            value = item[field]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"sizes[{index}].{field} must be a non-negative integer")
        for field in ("p50_ms", "p95_ms", "max_ms", "load_seconds"):
            _number(item[field], f"sizes[{index}].{field}")
        if item["p50_ms"] > item["p95_ms"] or item["p95_ms"] > item["max_ms"]:
            raise ValueError(f"sizes[{index}] latency percentiles are not ordered")
        result["sizes"].append(normalized)

    result["sizes"].sort(key=lambda row: row["facts"])
    return result


def pack_history(
    raw: Mapping[str, Any],
    *,
    collected_at: Optional[str] = None,
    run_metadata: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    """Wrap one validated result in a versioned history envelope."""
    if collected_at is None:
        collected_at = datetime.now(timezone.utc).isoformat()
    collected_at = _nonblank(collected_at, "collected_at")

    if run_metadata is not None and not isinstance(run_metadata, Mapping):
        raise ValueError("run_metadata must be a mapping or None")
    run = {
        field: str(run_metadata[field]).strip()
        for field in _RUN_FIELDS
        if run_metadata is not None
        and field in run_metadata
        and str(run_metadata[field]).strip()
    }
    return {
        "history_schema_version": HISTORY_SCHEMA_VERSION,
        "collected_at": collected_at,
        "run": run,
        "result": validate_raw_result(raw),
    }


def validate_history(history: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a history envelope and return a fresh normalized mapping."""
    if not isinstance(history, Mapping):
        raise ValueError("history document must be a mapping")
    if history.get("history_schema_version") != HISTORY_SCHEMA_VERSION:
        raise ValueError(
            f"history_schema_version must be {HISTORY_SCHEMA_VERSION}"
        )
    run = history.get("run")
    if not isinstance(run, Mapping):
        raise ValueError("history run metadata must be a mapping")
    return pack_history(
        history.get("result"),
        collected_at=_nonblank(history.get("collected_at"), "collected_at"),
        run_metadata=run,
    )


def _workload_signature(row: Mapping[str, Any]) -> tuple[int, int, int, int]:
    return (
        row["measured_searches_total"],
        row["query_templates"],
        row["top_k"],
        row["warmup_queries"],
    )


def summarize_markdown(history: Mapping[str, Any]) -> str:
    """Create a stable Markdown summary for Actions and downloaded artifacts."""
    doc = validate_history(history)
    result = doc["result"]
    lines = [
        "# L3 retrieval benchmark history",
        "",
        f"- Collected: `{doc['collected_at']}`",
        f"- Commit: `{result['commit']}`",
        f"- Backend/embedder: `{result['backend']}` / `{result['embedder']}`",
        f"- Python: `{result['python_version']}`",
        f"- Platform: `{result['platform']}`",
        "",
        "| Facts | Load s | p50 ms | p95 ms | max ms | DB bytes |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["sizes"]:
        lines.append(
            f"| {row['facts']} | {row['load_seconds']} | {row['p50_ms']} | "
            f"{row['p95_ms']} | {row['max_ms']} | {row['db_size_bytes']} |"
        )
    lines.extend(
        [
            "",
            "> Informational smoke history only. Hosted-runner latency is not a "
            "production SLO or a normal pull-request gate.",
        ]
    )
    return "\n".join(lines) + "\n"


def compare_histories(
    baseline: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    warn_ratio: float = 1.25,
) -> dict[str, Any]:
    """Compare shared sizes without turning hosted-runner variance into a gate."""
    ratio = _number(warn_ratio, "warn_ratio", minimum=0.000001)
    base = validate_history(baseline)
    now = validate_history(current)
    base_result = base["result"]
    now_result = now["result"]

    comparable_environment = (
        base_result["benchmark"],
        base_result["backend"],
        base_result["embedder"],
    ) == (
        now_result["benchmark"],
        now_result["backend"],
        now_result["embedder"],
    )

    base_sizes = {row["facts"]: row for row in base_result["sizes"]}
    now_sizes = {row["facts"]: row for row in now_result["sizes"]}
    shared = sorted(set(base_sizes) & set(now_sizes))
    rows: list[dict[str, Any]] = []
    warnings: list[int] = []

    for facts in shared:
        before = base_sizes[facts]
        after = now_sizes[facts]
        workload_match = _workload_signature(before) == _workload_signature(after)
        p50_ratio = (
            round(after["p50_ms"] / before["p50_ms"], 4)
            if before["p50_ms"] > 0
            else None
        )
        p95_ratio = (
            round(after["p95_ms"] / before["p95_ms"], 4)
            if before["p95_ms"] > 0
            else None
        )
        warned = bool(
            comparable_environment
            and workload_match
            and (
                (p50_ratio is not None and p50_ratio >= ratio)
                or (p95_ratio is not None and p95_ratio >= ratio)
            )
        )
        if warned:
            warnings.append(facts)
        rows.append(
            {
                "facts": facts,
                "workload_match": workload_match,
                "p50_ratio": p50_ratio,
                "p95_ratio": p95_ratio,
                "warning": warned,
            }
        )

    return {
        "informational_only": True,
        "comparable_environment": comparable_environment,
        "warn_ratio": ratio,
        "shared_sizes": shared,
        "warning_sizes": warnings,
        "rows": rows,
    }


def comparison_markdown(comparison: Mapping[str, Any]) -> str:
    lines = [
        "# L3 retrieval benchmark comparison",
        "",
        f"- Informational only: `{str(comparison['informational_only']).lower()}`",
        f"- Backend/embedder comparable: `{str(comparison['comparable_environment']).lower()}`",
        f"- Warning ratio: `{comparison['warn_ratio']}`",
        "",
        "| Facts | Workload match | p50 ratio | p95 ratio | Warning |",
        "|---:|:---:|---:|---:|:---:|",
    ]
    if not comparison["rows"]:
        lines.append("| — | — | — | — | no shared sizes |")
    else:
        for row in comparison["rows"]:
            lines.append(
                f"| {row['facts']} | {str(row['workload_match']).lower()} | "
                f"{row['p50_ratio'] if row['p50_ratio'] is not None else 'n/a'} | "
                f"{row['p95_ratio'] if row['p95_ratio'] is not None else 'n/a'} | "
                f"{'⚠️' if row['warning'] else '—'} |"
            )
    lines.extend(
        [
            "",
            "> A warning is a review signal, not a failed SLO. Reproduce on a "
            "controlled runner before drawing a performance conclusion.",
        ]
    )
    return "\n".join(lines) + "\n"


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path: str, content: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")


def _run_metadata(args: argparse.Namespace) -> dict[str, Any]:
    return {field: getattr(args, field) for field in _RUN_FIELDS}


def _command_pack(args: argparse.Namespace) -> int:
    history = pack_history(
        _load(args.input),
        collected_at=args.collected_at,
        run_metadata=_run_metadata(args),
    )
    _write(args.output, json.dumps(history, indent=2, ensure_ascii=False) + "\n")
    summary = summarize_markdown(history)
    if args.summary_out:
        _write(args.summary_out, summary)
    print(summary, end="")
    return 0


def _command_compare(args: argparse.Namespace) -> int:
    comparison = compare_histories(
        _load(args.baseline), _load(args.current), warn_ratio=args.warn_ratio
    )
    markdown = comparison_markdown(comparison)
    if args.output:
        _write(args.output, markdown)
    print(markdown, end="")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Package and compare existing L3 retrieval benchmark JSON"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pack = sub.add_parser("pack")
    pack.add_argument("--input", required=True)
    pack.add_argument("--output", required=True)
    pack.add_argument("--summary-out")
    pack.add_argument("--collected-at")
    for field in _RUN_FIELDS:
        pack.add_argument(f"--{field.replace('_', '-')}", dest=field, default="")
    pack.set_defaults(func=_command_pack)

    compare = sub.add_parser("compare")
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--current", required=True)
    compare.add_argument("--output")
    compare.add_argument("--warn-ratio", type=float, default=1.25)
    compare.set_defaults(func=_command_compare)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = _parser().parse_args(argv)
        return args.func(args)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"benchmark history error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
