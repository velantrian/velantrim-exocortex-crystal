"""Validate mixed D1 localization freshness after Arabic parity refresh."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
CURRENT_LOCALES = ("ar", "de", "es", "fr", "it", "ja", "ru", "zh-CN")
REFRESH_LOCALES = tuple(locale for locale in LOCALES if locale not in CURRENT_LOCALES)
READER_MARKERS = (
    "reader_core_rc1_skeleton = true",
    "reader_core_rc2_structural_map = true",
    "reader_core_rc3_multi_pass_mechanics = true",
    "reader_core_rc4_proposition_extraction = true",
    "reader_core_rc5_relation_candidates = true",
    "dedicated_reader_core = false",
)
AUTHORITY_MARKERS = (
    "EXTRACTED_PROPOSITION != verified fact",
    "Reader candidate != admitted evidence",
    "contradiction candidate != confirmed contradiction",
)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def normalize_spacing(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text)


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
        locale: [
            f"docs/{locale}/README.md",
            f"docs/{locale}/QUICKSTART.md",
            f"docs/{locale}/STATUS.md",
            f"docs/{locale}/IMPLEMENTATION_STATUS.md",
        ]
        for locale in CURRENT_LOCALES
    }
    for ok, label in (
        (documentation.get("translation_tracking_issue") == 341, "tracking issue"),
        (documentation.get("latest_translation_refresh_issue") == 425, "latest refresh issue"),
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
                normalized = normalize_spacing(text)
                for marker in (*READER_MARKERS, *AUTHORITY_MARKERS):
                    if marker not in normalized:
                        errors.append(f"{relative}: missing normalized Reader evidence {marker!r}")
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
        "D1 Reader-dependent detail translations are `CURRENT` in Arabic, German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian",
        "one other supported locale is `REFRESH_NEEDED`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing D1 marker {marker!r}")

    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "Arabic, German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed",
        "one other localized root README file and Reader-dependent detail pack",
        "reader_core_rc5_relation_candidates    = true",
    ):
        if marker not in state:
            errors.append(f"AI current state: missing marker {marker!r}")

    if errors:
        print("D1 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("D1 translation status consistent: Arabic + German + French + Spanish + Italian + Japanese + Simplified Chinese + Russian CURRENT; 1 locale REFRESH_NEEDED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
