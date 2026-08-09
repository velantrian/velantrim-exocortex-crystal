"""Validate the complete English D3 architecture source contract."""

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
MARKERS = ("<!-- d3-source-contract: CURRENT -->", "<!-- d3-source-scope: architecture-storage-authority -->")
STALE = (
    "Auto backend chain: LadybugDB → SQLite → in-memory mock",
    "Future target — source-span provenance and import sessions",
    "Current runtime: the verified SQLite lifecycle exists; no cross-backend import",
    "Implementation status:** Candidate runtime in PR #337",
    "Status:** Proposed",
    "only SQLite lifecycle exists; cross-backend import/cutover is not implemented",
    "Not implemented by the first runtime slice.",
    "This change deliberately adds no PostgreSQL",
)
REQUIRED = {
    "docs/ARCHITECTURE.md": ("core.query_pipeline.query()", "Source spans, document records, import sessions and dry-run/review flows are implemented baseline", "active=false", "dedicated multi-pass Reader Core"),
    "docs/ARCHITECTURE_OVERVIEW.md": ("fallback to ephemeral Mock is forbidden", "The PostgreSQL target is absent from ordinary runtime composition", "active=false"),
    "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md": ("physical L3", "strict Canon", "active=false", "read-only"),
    "docs/architecture/DURABLE_STORAGE_PROFILE.md": ("IMPLEMENTED / TESTED / MERGED BASELINE", "first-run `auto` reaches the in-memory Mock backend", "active=false"),
    "docs/architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md": ("phases 1–6 implemented", "Phase 5 — Inactive PostgreSQL target import", "Phase 6 — Exact state equivalence", "Phase 8 — Explicit cutover and fencing", "Not implemented."),
    "docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md": ("IMPLEMENTED / TESTED / MERGED BASELINE", "bbd816c09dd39a02e6de6c1014438490572f40f6", "active=false", "active PostgreSQL runtime reads or writes"),
    "docs/adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md": ("Accepted and partially implemented", "#331 / PR #335", "#332 / PR #337", "**Active runtime cutover:** not implemented"),
}
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
    combined: list[str] = []
    for relative in FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing D3 source file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        combined.append(text)
        for marker in MARKERS:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        for marker in REQUIRED[relative]:
            if marker not in text:
                errors.append(f"{relative}: missing current marker {marker!r}")
        for stale in STALE:
            if stale in text:
                errors.append(f"{relative}: stale marker {stale!r}")
        check_links(relative, text, errors)

    all_text = "\n".join(combined)
    for marker in ("physical L3", "strict Canon", "active=false", "not activation", "read-only", "SQLite", "PostgreSQL", "fallback to ephemeral Mock is forbidden", "active PostgreSQL read/write runtime adapter", "dedicated Reader Core"):
        if marker not in all_text:
            errors.append(f"D3 source contract: missing boundary {marker!r}")

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for marker in ("Validate complete English D3 source contract", "python scripts/check_d3_source_contract.py"):
        if marker not in workflow:
            errors.append(f"CI workflow: missing D3 source validator marker {marker!r}")

    doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    for marker in ("ARCHITECTURE_OVERVIEW.md", "STORAGE_AND_AUTHORITY_BOUNDARIES.md", "D3 uses the complete stable English architecture source family", "CURRENT full-parity localized READMEs", "REFRESH_NEEDED translated document packs", "Inactive PostgreSQL import"):
        if marker not in doc_map:
            errors.append(f"documentation map: missing marker {marker!r}")

    current_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in ("D3 English source checkpoint", "main@208f1c772ee3a112cb803d2413c120bef23adb05", "complete D3 source validator"):
        if marker not in current_state:
            errors.append(f"AI current state: missing source marker {marker!r}")

    if errors:
        print("D3 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Complete D3 English architecture/storage/authority source contract is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
