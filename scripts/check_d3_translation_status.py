"""Validate mixed D3 architecture/storage translation freshness after RC-5."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
REFRESH = tuple(locale for locale in LOCALES if locale != "ru")
FILES = ("ARCHITECTURE_OVERVIEW.md", "STORAGE_AND_AUTHORITY_BOUNDARIES.md")


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(
        (ROOT / "docs/status/d3-translation-manifest.json").read_text(encoding="utf-8")
    )
    checks = (
        (manifest.get("english_source_checkpoint") == SOURCE, "source"),
        (manifest.get("current_locales") == ["ru"], "current locales"),
        (manifest.get("refresh_needed_locales") == list(REFRESH), "refresh locales"),
        (manifest.get("reader_core_rc5_relation_candidates_claim") is True, "RC-5 claim"),
        (manifest.get("dedicated_reader_core_implemented_claim") is False, "dedicated claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"manifest: {label}")

    for locale in LOCALES:
        status = "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
        index = (ROOT / f"docs/{locale}/README.md").read_text(encoding="utf-8")
        for marker in (f"d3-source: main@{SOURCE}", f"d3-status: {status}"):
            if marker not in index:
                errors.append(f"docs/{locale}/README.md: {marker}")

        for name in FILES:
            relative = f"docs/{locale}/{name}"
            text = (ROOT / relative).read_text(encoding="utf-8")
            source_doc = f"docs/{name}"
            for marker in (
                f"translation-source: {source_doc}@",
                f"d3-locale: {locale}",
                "d3-boundary: physical-l3-not-strict-canon",
                "d3-boundary: public-query-read-only",
                "d3-boundary: postgresql-active=false",
                "active=false",
            ):
                if marker not in text:
                    errors.append(f"{relative}: {marker}")

            if locale == "ru":
                for marker in (
                    f"translation-source: {source_doc}@{SOURCE}",
                    "translation-status: CURRENT",
                    "d3-reader: rc5-relation-candidates-implemented",
                    "RC-5",
                    "coverage != comprehension proof",
                    "pass completion != comprehension proof",
                    "EXTRACTED_PROPOSITION != verified fact",
                    "Reader candidate != admitted evidence",
                    "contradiction candidate != confirmed contradiction",
                ):
                    if marker not in text:
                        errors.append(f"{relative}: {marker}")
            elif f"translation-source: {source_doc}@{SOURCE}" in text:
                errors.append(f"{relative}: stale translation pins RC-5 source")

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D3 source checkpoint:** `main@{SOURCE}`",
        "D3 Reader-dependent detail translations are `CURRENT` in Russian",
        "eight other supported locales are `REFRESH_NEEDED`",
    ):
        if marker not in ledger:
            errors.append(f"ledger: {marker}")

    if errors:
        print("D3 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("D3 translation status consistent: Russian CURRENT at RC-5; 8 locales REFRESH_NEEDED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
