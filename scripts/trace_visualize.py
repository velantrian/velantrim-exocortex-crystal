#!/usr/bin/env python
"""Velantrim Crystal — TRACE Visualization CLI (reviewer tooling, read-only)."""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

# Allow running this script directly from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.trace_visualize import to_dot, to_markdown


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for the trace visualization CLI.

    Parameters
    ----------
    argv:
        Argument list (defaults to sys.argv[1:]).

    Returns
    -------
    int
        Exit code (0 on success).
    """
    parser = argparse.ArgumentParser(
        description="Render a Velantrim receipt JSON as Markdown or DOT (read-only)."
    )
    parser.add_argument("input", help="Path to the receipt JSON file.")
    parser.add_argument(
        "--format",
        choices=["markdown", "dot"],
        default="markdown",
        help="Output format (default: markdown).",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output file path (defaults to stdout).",
    )

    args = parser.parse_args(argv)

    with open(args.input, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if args.format == "dot":
        output = to_dot(data)
    else:
        output = to_markdown(data)

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
