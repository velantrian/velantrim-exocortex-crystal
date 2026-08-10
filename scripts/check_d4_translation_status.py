"""Validate current D4 project/grant/governance/glossary translations."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
FILES = {locale: (f"docs/{locale}/GRANT_OVERVIEW.md", f"docs/{locale}/GLOSSARY.md") for locale in LOCALES}
READER_MARKERS = (
    "d4-reader: rc1-skeleton-implemented",
    "d4-reader: rc2-structural-map-implemented",
    "d4-nonclaim: dedicated-reader-core-not-implemented",
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
    manifest = json.loads((ROOT / "docs/status/d4-translation-manifest.json").read_text())
    expected = {locale: list(FILES[locale]) for locale in LOCALES}
    checks = (
        (manifest.get("phase") == "D4", "phase"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (manifest.get("current_locales") == list(LOCALES), "current locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == expected, "current documents"),
        (manifest.get("reader_core_rc1_skeleton_claim") is True, "RC-1 claim"),
        (manifest.get("reader_core_rc2_structural_map_claim") is True, "RC-2 claim"),
        (manifest.get("dedicated_reader_core_implemented_claim") is False, "dedicated Reader claim"),
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
        (manifest.get("approved_budget_claim") is False, "budget claim"),
        (manifest.get("budget_change_claim") is False, "budget change claim"),
        (manifest.get("security_legal_gdpr_certification_claim") is False, "certification claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"D4 manifest: invalid {label}")

    for locale in LOCALES:
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d4-source: main@{SOURCE}", "d4-status: CURRENT"):
            if marker not in index:
                errors.append(f"{index_relative}: missing {marker!r}")
        check_links(index_relative, index, errors)
        for relative in FILES[locale]:
            text = (ROOT / relative).read_text(encoding="utf-8")
            source_doc = "docs/PROJECT_GRANT_AND_GOVERNANCE.md" if relative.endswith("GRANT_OVERVIEW.md") else "docs/GLOSSARY.md"
            markers = (
                f"translation-source: {source_doc}@{SOURCE}",
                "translation-status: CURRENT",
                f"d4-locale: {locale}",
                "d4-boundary: physical-l3-not-strict-canon",
                "d4-boundary: retrieval-score-not-evidence",
                "d4-boundary: model-output-not-source-truth",
                "d4-boundary: migration-proof-not-claim-proof",
                "d4-nonclaim: import-is-not-activation",
                "d4-nonclaim: nlnet-not-awarded",
                "d4-nonclaim: security-legal-gdpr-not-certified",
                "d4-nonclaim: native-speaker-editorial-not-certified",
                *READER_MARKERS,
                "physical L3", "strict Canon", "active=false", "€50,000",
            )
            for marker in markers:
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    if f"D4 source checkpoint:** `main@{SOURCE}`" not in ledger:
        errors.append("translation ledger: D4 source checkpoint mismatch")
    if "D4 is complete for all nine supported locales" not in ledger:
        errors.append("translation ledger: D4 completion missing")

    if errors:
        print("D4 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"D4 translation status is consistent: locales={len(LOCALES)}, source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
