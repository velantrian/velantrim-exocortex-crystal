"""Validate mixed D5 extended-reference translation freshness."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "0c3d537831e4f1cb5a43d61bc2cbc8b05c080df5"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
CURRENT_LOCALES = ("ru",)
REFRESH_LOCALES = tuple(locale for locale in LOCALES if locale not in CURRENT_LOCALES)
GUIDE = "EXTENDED_REFERENCE_GUIDE.md"
READER_MARKERS = (
    "d5-reader: rc1-skeleton-implemented",
    "d5-reader: rc2-structural-map-implemented",
    "d5-reader: rc3-multi-pass-mechanics-implemented",
    "d5-nonclaim: dedicated-reader-core-not-implemented",
)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_links(relative: str, text: str, errors: list[str]) -> None:
    source = ROOT / relative
    for raw in LINK.findall(text):
        target = raw.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split(maxsplit=1)[0].split("#", 1)[0].split("?", 1)[0])
        resolved = (source.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{relative}: link escapes repository: {raw!r}")
            continue
        if not resolved.exists():
            errors.append(f"{relative}: broken link: {raw!r}")


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((ROOT / "docs/status/d5-translation-manifest.json").read_text())
    current = {"ru": f"docs/ru/{GUIDE}"}
    refresh = {locale: f"docs/{locale}/{GUIDE}" for locale in REFRESH_LOCALES}
    checks = (
        (manifest.get("phase") == "D5_TRANSLATIONS", "phase"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (manifest.get("current_locales") == list(CURRENT_LOCALES), "current locales"),
        (manifest.get("refresh_needed_locales") == list(REFRESH_LOCALES), "refresh locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == current, "current documents"),
        (manifest.get("refresh_needed_documents") == refresh, "refresh documents"),
        (manifest.get("reader_core_rc1_skeleton_claim") is True, "RC-1 claim"),
        (manifest.get("reader_core_rc2_structural_map_claim") is True, "RC-2 claim"),
        (manifest.get("reader_core_rc3_multi_pass_mechanics_claim") is True, "RC-3 claim"),
        (manifest.get("dedicated_reader_core_implemented_claim") is False, "dedicated Reader claim"),
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"D5 manifest: invalid {label}")

    for locale in LOCALES:
        expected_status = "CURRENT" if locale in CURRENT_LOCALES else "REFRESH_NEEDED"
        relative = f"docs/{locale}/{GUIDE}"
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in (
            "translation-source: docs/EXTENDED_REFERENCE_POLICY.md@",
            f"d5-locale: {locale}",
            "d5-boundary: physical-l3-not-strict-canon",
            "d5-boundary: retrieval-score-not-evidence",
            "d5-boundary: model-output-not-source-truth",
            "d5-boundary: migration-proof-not-claim-proof",
            "d5-nonclaim: import-is-not-activation",
            "d5-nonclaim: nlnet-not-awarded",
            "d5-nonclaim: security-legal-gdpr-not-certified",
            "d5-nonclaim: native-speaker-editorial-not-certified",
            "physical L3",
            "strict Canon",
            "active=false",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        if locale in CURRENT_LOCALES:
            for marker in (
                f"translation-source: docs/EXTENDED_REFERENCE_POLICY.md@{SOURCE}",
                "translation-status: CURRENT",
                *READER_MARKERS,
                "submitted / under review / not awarded",
                "€50,000",
                "budget change: none",
                "REFRESH_NEEDED",
                "coverage != comprehension proof",
                "pass completion != comprehension proof",
            ):
                if marker not in text:
                    errors.append(f"{relative}: missing current D5 marker {marker!r}")
        else:
            if f"translation-source: docs/EXTENDED_REFERENCE_POLICY.md@{SOURCE}" in text:
                errors.append(f"{relative}: refresh-needed translation falsely pins current source")
        check_links(relative, text, errors)

        index = (ROOT / f"docs/{locale}/README.md").read_text(encoding="utf-8")
        for marker in (f"d5-source: main@{SOURCE}", f"d5-status: {expected_status}", GUIDE):
            if marker not in index:
                errors.append(f"docs/{locale}/README.md: missing marker {marker!r}")

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D5 source checkpoint:** `main@{SOURCE}`",
        "D5 Reader-dependent detail translations are `CURRENT` in Russian",
        "eight other supported locales are `REFRESH_NEEDED`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing D5 marker {marker!r}")

    if errors:
        print("D5 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("D5 translation status is consistent: Russian CURRENT; 8 locales REFRESH_NEEDED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
