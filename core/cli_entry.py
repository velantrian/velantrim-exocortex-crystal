# core/cli_entry.py
# Installed console entry point with a strict read-only boundary for ask/receipt.
#
# The historical core.cli module remains the broad command implementation and
# still exposes the legacy admission-capable `run` compatibility path when
# invoked directly. The installed `velantrim` command enters here so ordinary
# query commands cannot silently mutate memory.

from __future__ import annotations

import json
import sys
from typing import List, Optional

from core import provenance
from core import cli as legacy_cli
from core.query_pipeline import query


def _run_query_command(argv: List[str]) -> Optional[int]:
    """Handle installed-CLI query commands, or return None to delegate."""
    if len(argv) != 2 or argv[0] not in {"ask", "receipt"}:
        return None

    result = query(argv[1])
    if argv[0] == "ask":
        print(result.get("answer") or f"[blocked] {result.get('error')}")
        return 0

    if result.get("answer") is None:
        print(json.dumps({"error": result.get("error")}, ensure_ascii=False))
        return 1
    print(json.dumps(provenance.build_receipt(result), ensure_ascii=False, indent=2))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Installed `velantrim` entry point.

    `ask` and `receipt` use core.query_pipeline.query(). Every other command is
    delegated unchanged to core.cli.main(), preserving the established CLI.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    handled = _run_query_command(args)
    if handled is not None:
        return handled
    return legacy_cli.main(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())