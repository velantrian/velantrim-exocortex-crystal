"""Validate all current D2 reviewer/safety translations."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "b7e6574dd7aefa2f32783ab79054fac6b3b4109f"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
FILES = {
    locale: (
        f"docs/{locale}/REVIEWER_GUIDE.md",
        f"docs/{locale}/SAFETY_PRIVACY_AND_FAILURES.md",
    )
    for locale in LOCALES
}
MARKERS = (
    "translation-status: CURRENT",
    "d2-boundary: public-ask-read-only",
    "d2-boundary: postgresql-active=false",
    "d2-boundary: erasure-not-global",
    "d2-nonclaim: security-legal-gdpr-not-certified",
    "d2-nonclaim: nlnet-not-awarded",
    "active=false",
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
    manifest = json.loads((ROOT / "docs/status/d2-translation-manifest.json").read_text(encoding="utf-8"))
    expected_documents = {locale: list(FILES[locale]) for locale in LOCALES}
    checks = (
        (manifest.get("phase") == "D2", "phase"),
        (manifest.get("tracking_issue") == 341, "tracking issue"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (manifest.get("current_locales") == list(LOCALES), "current locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == expected_documents, "current documents"),
        (manifest.get("native_speaker_editorial_certification") is False, "native certification"),
        (manifest.get("security_legal_gdpr_certification_claim") is False, "certification claim"),
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"D2 manifest: invalid {label}")

    for locale in LOCALES:
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d2-source: main@{SOURCE}", "d2-status: CURRENT", "SAFETY_PRIVACY_AND_FAILURES.md"):
            if marker not in index:
                errors.append(f"{index_relative}: missing marker {marker!r}")
        check_links(index_relative, index, errors)
        for relative in FILES[locale]:
            path = ROOT / relative
            if not path.is_file():
                errors.append(f"missing D2 file: {relative}")
                continue
            text = path.read_text(encoding="utf-8")
            expected_source = "docs/REVIEWER_GUIDE.md" if relative.endswith("REVIEWER_GUIDE.md") else "docs/SAFETY_PRIVACY_AND_FAILURES.md"
            for marker in (f"translation-source: {expected_source}@{SOURCE}", f"d2-locale: {locale}", *MARKERS):
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D2 source checkpoint:** `main@{SOURCE}`",
        "All nine supported D2 locale packs remain `CURRENT`",
        "D2 reviewer/safety translations remain current across all nine supported locales",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")

    current_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "Arabic, German, French, Spanish, Hindi, Italian, Japanese, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed",
        "D2 reviewer/safety translations remain current across all nine supported locales",
        f"main@{SOURCE}",
    ):
        if marker not in current_state:
            errors.append(f"AI current state: missing marker {marker!r}")

    if errors:
        print("D2 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"D2 translation status is consistent: locales={len(LOCALES)}, source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
