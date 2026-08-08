"""Validate the stable English D3 architecture source contract."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "docs/ARCHITECTURE.md",
    "docs/ARCHITECTURE_OVERVIEW.md",
    "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md",
    "docs/architecture/DURABLE_STORAGE_PROFILE.md",
    "docs/architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md",
    "docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md",
    "docs/adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md",
)
MARKERS = (
    "<!-- d3-source-contract: CURRENT -->",
    "<!-- d3-source-scope: architecture-storage-authority -->",
)
STALE = (
    "Auto backend chain: LadybugDB → SQLite → in-memory mock",
    "Future target — source-span provenance and import sessions",
    "Current runtime: the verified SQLite lifecycle exists; no cross-backend import",
    "Implementation status:** Candidate runtime in PR #337",
    "Status:** Proposed",
)
REQUIRED_BOUNDARIES = (
    "physical L3",
    "strict Canon",
    "active=false",
    "not activation",
    "read-only",
    "SQLite",
    "PostgreSQL",
)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_links(relative: str, text: str, errors: list[str]) -> None:
    source = ROOT / relative
    for raw in LINK.findall(text):
        target = raw.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split(maxsplit=1)[0].split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        resolved = (source.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{relative}: local link escapes repository: {raw!r}")
            continue
        if not resolved.exists():
            errors.append(f"{relative}: broken local link: {raw!r}")


def main() -> int:
    errors: list[str] = []
    combined_parts: list[str] = []

    for relative in FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing D3 source file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        combined_parts.append(text)
        for marker in MARKERS:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        for stale in STALE:
            if stale in text:
                errors.append(f"{relative}: stale marker {stale!r}")
        check_links(relative, text, errors)

    combined = "\n".join(combined_parts)
    for marker in REQUIRED_BOUNDARIES:
        if marker not in combined:
            errors.append(f"D3 source contract: missing boundary {marker!r}")

    for marker in (
        "Source spans and import-session evidence are implemented baseline",
        "Silent fallback to ephemeral Mock is forbidden",
        "The PostgreSQL target is absent from ordinary runtime composition",
        "active PostgreSQL read/write runtime adapter",
        "dedicated Reader Core",
    ):
        if marker not in combined:
            errors.append(f"D3 source contract: missing marker {marker!r}")

    map_text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    for marker in (
        "ARCHITECTURE_OVERVIEW.md",
        "STORAGE_AND_AUTHORITY_BOUNDARIES.md",
        "D3 uses the stable English architecture overview",
    ):
        if marker not in map_text:
            errors.append(f"documentation map: missing marker {marker!r}")

    current_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "D1 is current across all nine supported locale packs",
        "D2 reviewer/safety translations are",
        "English D3 architecture source contract is stable",
    ):
        if marker not in current_state:
            errors.append(f"AI current state: missing marker {marker!r}")

    if errors:
        print("D3 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("D3 English architecture/storage/authority source contract is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
