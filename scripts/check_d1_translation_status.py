"""Validate the completed multilingual D1 localization checkpoint."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RUSSIAN_SOURCE = "16d71e731ee658b1faa65c9ea45c0d8cca290f7c"
ALL_LOCALES_SOURCE = "a497b7d3cfbe59ca75b11d7449d5a728455b3130"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
SOURCE_BY_LOCALE = {
    locale: RUSSIAN_SOURCE if locale == "ru" else ALL_LOCALES_SOURCE
    for locale in LOCALES
}
DOCUMENTS = {
    locale: (
        f"docs/{locale}/README.md",
        f"docs/{locale}/QUICKSTART.md",
        f"docs/{locale}/STATUS.md",
        f"docs/{locale}/IMPLEMENTATION_STATUS.md",
    )
    for locale in LOCALES
}
GENERIC_BOUNDARY_MARKERS = (
    "<!-- d1-boundary: public-ask-read-only -->",
    "<!-- d1-boundary: postgresql-active=false -->",
    "<!-- d1-nonclaim: import-is-not-activation -->",
    "<!-- d1-nonclaim: nlnet-not-awarded -->",
)
STALE = (
    "1713 passed",
    "6389 measured statements",
    "PR #265",
    "CLI-команды `ask` и `receipt` пока используют исторический путь",
)
UNSUPPORTED = (
    "PostgreSQL/pgvector является текущим runtime",
    "автоматическое переключение backend включено",
    "грант NLnet получен",
    "Crystal гарантирует отсутствие hallucinations",
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


def required_markers(locale: str, relative: str) -> tuple[str, ...]:
    source = SOURCE_BY_LOCALE[locale]
    name = Path(relative).name
    if name == "README.md":
        base = (
            f"<!-- d1-source: main@{source} -->",
            "`CURRENT`",
            "`REFRESH_NEEDED`",
        )
        if locale != "ru":
            base += (
                "<!-- d1-status: CURRENT -->",
                "<!-- d2-status: REFRESH_NEEDED -->",
            )
        return base

    english_source = {
        "QUICKSTART.md": "docs/QUICKSTART.md",
        "STATUS.md": "docs/STATUS.md",
        "IMPLEMENTATION_STATUS.md": "docs/IMPLEMENTATION_STATUS.md",
    }[name]
    base = (
        f"translation-source: {english_source}@{source}",
        "translation-status: CURRENT",
    )
    if locale != "ru":
        base += (f"<!-- d1-locale: {locale} -->",) + GENERIC_BOUNDARY_MARKERS
    elif name == "QUICKSTART.md":
        base += ("core.query_pipeline.query()", "active=false", "Import — не activation")
    elif name == "STATUS.md":
        base += (
            "bbd816c09dd39a02e6de6c1014438490572f40f6",
            "2078 passed / 13 skipped / 0 failed",
            "9756 statements / 100.00% line coverage",
            "active=false",
            "Проект подан",
        )
    else:
        base += (
            "Inactive PostgreSQL/pgvector import",
            "Automatic SQLite/PostgreSQL switching",
            "Reader Core / Semantic Reading Layer",
        )
    return base


def main() -> int:
    errors: list[str] = []
    manifest_path = ROOT / "docs/status/implementation-manifest.json"
    documentation = json.loads(manifest_path.read_text(encoding="utf-8"))["documentation"]

    expected_documents = {locale: list(DOCUMENTS[locale]) for locale in LOCALES}
    checks = (
        (documentation.get("translation_tracking_issue") == 341, "tracking issue"),
        (documentation.get("d1_current_locales") == list(LOCALES), "current locales"),
        (documentation.get("d1_source_checkpoints") == SOURCE_BY_LOCALE, "source checkpoints"),
        (documentation.get("d1_current_documents") == expected_documents, "current documents"),
        (documentation.get("d1_pending_locales") == [], "pending locales"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"manifest: invalid D1 {label}")

    for locale in LOCALES:
        for relative in DOCUMENTS[locale]:
            path = ROOT / relative
            if not path.is_file():
                errors.append(f"missing D1 file: {relative}")
                continue
            text = path.read_text(encoding="utf-8")
            for marker in required_markers(locale, relative):
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            for marker in STALE:
                if marker in text:
                    errors.append(f"{relative}: stale marker {marker!r}")
            for marker in UNSUPPORTED:
                if marker in text:
                    errors.append(f"{relative}: unsupported claim {marker!r}")
            if Path(relative).name == "STATUS.md":
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
        f"Russian D1 source checkpoint:** `main@{RUSSIAN_SOURCE}`",
        f"Remaining-locale D1 source checkpoint:** `main@{ALL_LOCALES_SOURCE}`",
        "D1 is complete for all nine supported locales",
        "| Simplified Chinese | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |",
        "all nine supported locales `CURRENT`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")

    ai_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "Issue #341 D1 is complete",
        f"main@{RUSSIAN_SOURCE}",
        f"main@{ALL_LOCALES_SOURCE}",
        "Reviewer/safety documents remain D2",
    ):
        if marker not in ai_state:
            errors.append(f"AI current state: missing marker {marker!r}")

    if errors:
        print("D1 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "D1 translation status is consistent: "
        f"current={len(LOCALES)}, pending=0, source={ALL_LOCALES_SOURCE}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
