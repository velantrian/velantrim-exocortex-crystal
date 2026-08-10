"""Validate D5 extended-reference guides for all supported locales."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
GUIDE = "EXTENDED_REFERENCE_GUIDE.md"
READER_MARKERS = (
    "d5-reader: rc1-skeleton-implemented",
    "d5-reader: rc2-structural-map-implemented",
    "d5-nonclaim: dedicated-reader-core-not-implemented",
    "reader_core_rc1_skeleton = true",
    "reader_core_rc2_structural_map = true",
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
    expected = {locale: f"docs/{locale}/{GUIDE}" for locale in LOCALES}
    for ok, label in (
        (manifest.get("phase") == "D5_TRANSLATIONS", "phase"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (manifest.get("current_locales") == list(LOCALES), "current locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == expected, "current documents"),
        (manifest.get("reader_core_rc1_skeleton_claim") is True, "RC-1 claim"),
        (manifest.get("reader_core_rc2_structural_map_claim") is True, "RC-2 claim"),
        (manifest.get("dedicated_reader_core_implemented_claim") is False, "dedicated Reader claim"),
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
    ):
        if not ok:
            errors.append(f"D5 manifest: invalid {label}")

    for locale in LOCALES:
        relative = expected[locale]
        text = (ROOT / relative).read_text(encoding="utf-8")
        markers = (
            f"translation-source: docs/EXTENDED_REFERENCE_POLICY.md@{SOURCE}",
            "translation-status: CURRENT",
            f"d5-locale: {locale}",
            "d5-boundary: physical-l3-not-strict-canon",
            "d5-boundary: retrieval-score-not-evidence",
            "d5-boundary: model-output-not-source-truth",
            "d5-boundary: migration-proof-not-claim-proof",
            "d5-nonclaim: import-is-not-activation",
            "d5-nonclaim: nlnet-not-awarded",
            "d5-nonclaim: security-legal-gdpr-not-certified",
            "d5-nonclaim: native-speaker-editorial-not-certified",
            *READER_MARKERS,
            "physical L3", "strict Canon", "active=false",
            "submitted / under review / not awarded", "€50,000", "budget change: none",
            "CURRENT", "RETIRED", "ENGLISH_ONLY_BY_DESIGN",
        )
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        check_links(relative, text, errors)
        index = (ROOT / f"docs/{locale}/README.md").read_text(encoding="utf-8")
        for marker in (f"d5-source: main@{SOURCE}", "d5-status: CURRENT", GUIDE):
            if marker not in index:
                errors.append(f"docs/{locale}/README.md: missing marker {marker!r}")

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    if f"D5 source checkpoint:** `main@{SOURCE}`" not in ledger:
        errors.append("translation ledger: D5 source checkpoint mismatch")
    if "D5 is complete for all nine supported locales" not in ledger:
        errors.append("translation ledger: D5 completion missing")

    if errors:
        print("D5 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"D5 translation status is consistent: locales={len(LOCALES)}, source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
