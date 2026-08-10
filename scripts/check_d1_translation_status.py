"""Validate mixed D1 localization freshness after Reader RC-4."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "166fab5551c4b86ee0a546b2e1d3dc7adc240c86"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
CURRENT_LOCALES = ("ru",)
REFRESH_LOCALES = tuple(locale for locale in LOCALES if locale not in CURRENT_LOCALES)
READER_MARKERS = (
    "reader_core_rc1_skeleton = true",
    "reader_core_rc2_structural_map = true",
    "reader_core_rc3_multi_pass_mechanics = true",
    "reader_core_rc4_proposition_extraction = true",
    "dedicated_reader_core = false",
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
    documentation = json.loads(
        (ROOT / "docs/status/implementation-manifest.json").read_text(encoding="utf-8")
    )["documentation"]
    refresh_docs = {
        locale: [f"docs/{locale}/STATUS.md", f"docs/{locale}/IMPLEMENTATION_STATUS.md"]
        for locale in REFRESH_LOCALES
    }
    unchanged_docs = {locale: [f"docs/{locale}/QUICKSTART.md"] for locale in REFRESH_LOCALES}
    current_docs = {
        "ru": [
            "docs/ru/README.md",
            "docs/ru/QUICKSTART.md",
            "docs/ru/STATUS.md",
            "docs/ru/IMPLEMENTATION_STATUS.md",
        ]
    }
    for ok, label in (
        (documentation.get("translation_tracking_issue") == 341, "tracking issue"),
        (documentation.get("d1_source_checkpoint") == SOURCE, "source checkpoint"),
        (documentation.get("d1_current_locales") == list(CURRENT_LOCALES), "current locales"),
        (documentation.get("d1_refresh_needed_locales") == list(REFRESH_LOCALES), "refresh locales"),
        (documentation.get("d1_current_documents") == current_docs, "current documents"),
        (documentation.get("d1_refresh_needed_documents") == refresh_docs, "refresh documents"),
        (documentation.get("d1_unchanged_current_documents") == unchanged_docs, "unchanged documents"),
        (documentation.get("d1_pending_locales") == [], "pending locales"),
    ):
        if not ok:
            errors.append(f"manifest: invalid D1 {label}")

    for locale in LOCALES:
        expected_status = "CURRENT" if locale in CURRENT_LOCALES else "REFRESH_NEEDED"
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d1-source: main@{SOURCE}", f"d1-status: {expected_status}"):
            if marker not in index:
                errors.append(f"{index_relative}: missing marker {marker!r}")
        check_links(index_relative, index, errors)

        quick_relative = f"docs/{locale}/QUICKSTART.md"
        quick = (ROOT / quick_relative).read_text(encoding="utf-8")
        for marker in ("translation-source: docs/QUICKSTART.md@", "translation-status: CURRENT"):
            if marker not in quick:
                errors.append(f"{quick_relative}: missing marker {marker!r}")
        check_links(quick_relative, quick, errors)

        for name in ("STATUS.md", "IMPLEMENTATION_STATUS.md"):
            relative = f"docs/{locale}/{name}"
            text = (ROOT / relative).read_text(encoding="utf-8")
            english = f"docs/{name}"
            if f"translation-source: {english}@" not in text:
                errors.append(f"{relative}: missing source marker")
            if locale in CURRENT_LOCALES:
                for marker in (
                    f"translation-source: {english}@{SOURCE}",
                    "translation-status: CURRENT",
                    "active=false",
                ):
                    if marker not in text:
                        errors.append(f"{relative}: missing current Reader evidence {marker!r}")
                normalized = re.sub(r"[ \t]+", " ", text)
                for marker in READER_MARKERS:
                    if marker not in normalized:
                        errors.append(f"{relative}: missing normalized Reader evidence {marker!r}")
                for marker in ("EXTRACTED_PROPOSITION != verified fact", "Reader candidate != admitted evidence"):
                    if marker not in text:
                        errors.append(f"{relative}: missing RC-4 authority marker {marker!r}")
                if name == "STATUS.md":
                    for marker in (
                        "2078 passed / 13 skipped / 0 failed",
                        "9756 statements / 100.00% line coverage",
                    ):
                        if marker not in text:
                            errors.append(f"{relative}: missing runtime evidence {marker!r}")
            elif f"translation-source: {english}@{SOURCE}" in text:
                errors.append(f"{relative}: refresh-needed translation falsely pins current source")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D1 source checkpoint:** `main@{SOURCE}`",
        "D1 Reader-dependent detail translations are `CURRENT` in Russian",
        "eight other supported locales are `REFRESH_NEEDED`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing D1 marker {marker!r}")

    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "Russian Reader-dependent public/detail documentation is refreshed",
        "eight other localized root README files and Reader-dependent detail packs",
    ):
        if marker not in state:
            errors.append(f"AI current state: missing marker {marker!r}")

    if errors:
        print("D1 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("D1 translation status is consistent: Russian CURRENT at RC-4; 8 locales Reader refresh needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
