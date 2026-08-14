"""Validate mixed D3 architecture/storage translation freshness after German parity refresh."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
CURRENT_LOCALES = ("de", "ru")
REFRESH_LOCALES = tuple(locale for locale in LOCALES if locale not in CURRENT_LOCALES)
FILES = {
    locale: (
        f"docs/{locale}/ARCHITECTURE_OVERVIEW.md",
        f"docs/{locale}/STORAGE_AND_AUTHORITY_BOUNDARIES.md",
    )
    for locale in LOCALES
}
READER_MARKERS = (
    "d3-reader: rc1-skeleton-implemented",
    "d3-reader: rc2-structural-map-implemented",
    "d3-reader: rc3-multi-pass-mechanics-implemented",
    "d3-reader: rc4-proposition-extraction-implemented",
    "d3-reader: rc5-relation-candidates-implemented",
    "d3-nonclaim: dedicated-reader-core-not-implemented",
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
            errors.append(f"{relative}: link escapes repository: {raw!r}")
            continue
        if not resolved.exists():
            errors.append(f"{relative}: broken link: {raw!r}")


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(
        (ROOT / "docs/status/d3-translation-manifest.json").read_text(encoding="utf-8")
    )
    current = {locale: list(FILES[locale]) for locale in CURRENT_LOCALES}
    refresh = {locale: list(FILES[locale]) for locale in REFRESH_LOCALES}
    checks = (
        (manifest.get("phase") == "D3", "phase"),
        (manifest.get("tracking_issue") == 341, "tracking issue"),
        (manifest.get("latest_refresh_issue") == 412, "latest refresh issue"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (manifest.get("current_locales") == list(CURRENT_LOCALES), "current locales"),
        (manifest.get("refresh_needed_locales") == list(REFRESH_LOCALES), "refresh locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == current, "current documents"),
        (manifest.get("refresh_needed_documents") == refresh, "refresh documents"),
        (manifest.get("reader_core_rc1_skeleton_claim") is True, "RC-1 claim"),
        (manifest.get("reader_core_rc2_structural_map_claim") is True, "RC-2 claim"),
        (manifest.get("reader_core_rc3_multi_pass_mechanics_claim") is True, "RC-3 claim"),
        (manifest.get("reader_core_rc4_proposition_extraction_claim") is True, "RC-4 claim"),
        (manifest.get("reader_core_rc5_relation_candidates_claim") is True, "RC-5 claim"),
        (manifest.get("dedicated_reader_core_implemented_claim") is False, "dedicated Reader claim"),
        (manifest.get("active_postgresql_runtime_claim") is False, "PostgreSQL runtime claim"),
        (manifest.get("automatic_backend_switching_claim") is False, "switching claim"),
        (manifest.get("security_legal_gdpr_certification_claim") is False, "certification claim"),
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"D3 manifest: invalid {label}")

    for locale in LOCALES:
        expected_status = "CURRENT" if locale in CURRENT_LOCALES else "REFRESH_NEEDED"
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d3-source: main@{SOURCE}", f"d3-status: {expected_status}"):
            if marker not in index:
                errors.append(f"{index_relative}: missing {marker!r}")
        check_links(index_relative, index, errors)

        for relative in FILES[locale]:
            text = (ROOT / relative).read_text(encoding="utf-8")
            source_doc = (
                "docs/ARCHITECTURE_OVERVIEW.md"
                if relative.endswith("ARCHITECTURE_OVERVIEW.md")
                else "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md"
            )
            for marker in (
                f"translation-source: {source_doc}@",
                f"d3-locale: {locale}",
                "d3-boundary: physical-l3-not-strict-canon",
                "d3-boundary: public-query-read-only",
                "d3-boundary: postgresql-active=false",
                "d3-nonclaim: import-is-not-activation",
                "d3-nonclaim: nlnet-not-awarded",
                "core.query_pipeline.query()",
                "active=false",
            ):
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            if locale in CURRENT_LOCALES:
                for marker in (
                    f"translation-source: {source_doc}@{SOURCE}",
                    "translation-status: CURRENT",
                    *READER_MARKERS,
                    "RC-1",
                    "RC-2",
                    "RC-3",
                    "RC-4",
                    "RC-5",
                    "coverage != comprehension proof",
                    "pass completion != comprehension proof",
                    "EXTRACTED_PROPOSITION != verified fact",
                    "Reader candidate != admitted evidence",
                    "contradiction candidate != confirmed contradiction",
                ):
                    if marker not in text:
                        errors.append(f"{relative}: missing current Reader marker {marker!r}")
            elif f"translation-source: {source_doc}@{SOURCE}" in text:
                errors.append(f"{relative}: refresh-needed translation falsely pins current source")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D3 source checkpoint:** `main@{SOURCE}`",
        "D3 Reader-dependent detail translations are `CURRENT` in German and Russian",
        "seven other supported locales are `REFRESH_NEEDED`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing D3 marker {marker!r}")

    if errors:
        print("D3 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("D3 translation status consistent: German + Russian CURRENT; 7 locales REFRESH_NEEDED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
