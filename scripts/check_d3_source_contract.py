"""Validate the English D3 architecture source contract through Reader RC-5."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"


def main() -> int:
    errors: list[str] = []
    overview = (ROOT / "docs/ARCHITECTURE_OVERVIEW.md").read_text(encoding="utf-8")
    storage = (ROOT / "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md").read_text(
        encoding="utf-8"
    )
    combined = overview + "\n" + storage

    for marker in (
        "d3-source-contract: CURRENT",
        "d3-source-scope: architecture-storage-authority",
        "RC-1",
        "RC-2",
        "RC-3",
        "RC-4",
        "RC-5",
        "core/reader_relations.py",
        "POSSIBLE_CONTRADICTION",
        "EXCEPTION",
        "QUALIFICATION",
        "TENSION",
        "EXTRACTED_PROPOSITION",
        "Reader candidate",
        "relation candidate",
        "contradiction candidate != confirmed contradiction",
        "physical L3",
        "strict Canon",
        "active=false",
        "read-only",
        "dedicated/full autonomous Reader",
    ):
        if marker not in combined:
            errors.append(f"D3 source: missing {marker!r}")

    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        SOURCE,
        "reader_core_rc5_relation_candidates    = true",
        "dedicated_reader_core                  = false",
        "eight other localized root README files",
    ):
        if marker not in state:
            errors.append(f"CURRENT_STATE: missing {marker!r}")

    contract = (ROOT / "docs/architecture/READER_CORE_ARCHITECTURE.md").read_text(
        encoding="utf-8"
    )
    for marker in (
        "Contradiction candidates",
        "Cross-document links",
        "Reader observation",
        "Canon admission",
    ):
        if marker not in contract:
            errors.append(f"Reader contract: missing {marker!r}")

    if errors:
        print("D3 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"D3 English source contract consistent through RC-5: source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
