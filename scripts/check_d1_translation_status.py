"""Validate the current multilingual D1 localization checkpoint."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
DOCUMENTS = {
    locale: (
        f"docs/{locale}/README.md",
        f"docs/{locale}/QUICKSTART.md",
        f"docs/{locale}/STATUS.md",
        f"docs/{locale}/IMPLEMENTATION_STATUS.md",
    )
    for locale in LOCALES
}
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
READER_MARKERS = (
    "reader_core_rc1_skeleton = true",
    "reader_core_rc2_structural_map = true",
    "dedicated_reader_core = false",
)


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
    expected_sources = {locale: SOURCE for locale in LOCALES}
    expected_documents = {locale: list(DOCUMENTS[locale]) for locale in LOCALES}
    for ok, label in (
        (documentation.get("translation_tracking_issue") == 341, "tracking issue"),
        (documentation.get("d1_current_locales") == list(LOCALES), "current locales"),
        (documentation.get("d1_source_checkpoints") == expected_sources, "source checkpoints"),
        (documentation.get("d1_current_documents") == expected_documents, "current documents"),
        (documentation.get("d1_pending_locales") == [], "pending locales"),
    ):
        if not ok:
            errors.append(f"manifest: invalid D1 {label}")

    for locale in LOCALES:
        for relative in DOCUMENTS[locale]:
            path = ROOT / relative
            if not path.is_file():
                errors.append(f"missing D1 file: {relative}")
                continue
            text = path.read_text(encoding="utf-8")
            name = path.name
            if name == "README.md":
                markers = (f"d1-source: main@{SOURCE}", "d1-status: CURRENT")
            else:
                english = {
                    "QUICKSTART.md": "docs/QUICKSTART.md",
                    "STATUS.md": "docs/STATUS.md",
                    "IMPLEMENTATION_STATUS.md": "docs/IMPLEMENTATION_STATUS.md",
                }[name]
                markers = (
                    f"translation-source: {english}@{SOURCE}",
                    "translation-status: CURRENT",
                )
            for marker in markers:
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            if name in {"STATUS.md", "IMPLEMENTATION_STATUS.md"}:
                for marker in READER_MARKERS:
                    if marker not in text:
                        errors.append(f"{relative}: missing Reader reconciliation marker {marker!r}")
                for marker in (
                    "2078 passed / 13 skipped / 0 failed",
                    "9756 statements / 100.00% line coverage",
                    "active=false",
                ):
                    if marker not in text:
                        errors.append(f"{relative}: missing current evidence {marker!r}")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D1 source checkpoint:** `main@{SOURCE}`",
        "D1 is complete for all nine supported locales",
        "all nine supported locales `CURRENT`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")

    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in ("Issue #341 D1 is complete", f"main@{SOURCE}"):
        if marker not in state:
            errors.append(f"AI current state: missing marker {marker!r}")

    if errors:
        print("D1 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"D1 translation status is consistent: locales={len(LOCALES)}, source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
