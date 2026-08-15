"""Validate mixed D5 extended-reference translation freshness after French parity refresh."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
CURRENT_LOCALES = ("de", "fr", "ru")
REFRESH_LOCALES = tuple(locale for locale in LOCALES if locale not in CURRENT_LOCALES)
GUIDE = "EXTENDED_REFERENCE_GUIDE.md"
READER_MARKERS = (
    "d5-reader: rc1-skeleton-implemented",
    "d5-reader: rc2-structural-map-implemented",
    "d5-reader: rc3-multi-pass-mechanics-implemented",
    "d5-reader: rc4-proposition-extraction-implemented",
    "d5-reader: rc5-relation-candidates-implemented",
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
        (ROOT / "docs/status/d5-translation-manifest.json").read_text(encoding="utf-8")
    )
    current = {locale: f"docs/{locale}/{GUIDE}" for locale in CURRENT_LOCALES}
    refresh = {locale: f"docs/{locale}/{GUIDE}" for locale in REFRESH_LOCALES}
    checks = (
        (manifest.get("phase") == "D5_TRANSLATIONS", "phase"),
        (manifest.get("tracking_issue") == 341, "tracking issue"),
        (manifest.get("latest_refresh_issue") == 414, "latest refresh issue"),
        (manifest.get("source_document") == "docs/EXTENDED_REFERENCE_POLICY.md", "source document"),
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
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
        (manifest.get("approved_budget_claim") is False, "budget claim"),
        (manifest.get("budget_change_claim") is False, "budget change claim"),
        (manifest.get("security_legal_gdpr_certification_claim") is False, "certification claim"),
        (manifest.get("active_postgresql_runtime_claim") is False, "PostgreSQL claim"),
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
                "POSSIBLE_CONTRADICTION",
                "EXCEPTION",
                "QUALIFICATION",
                "TENSION",
                "submitted / under review / not awarded",
                "€50,000",
                "budget change: none",
                "REFRESH_NEEDED",
                "coverage != comprehension proof",
                "pass completion != comprehension proof",
                "EXTRACTED_PROPOSITION != verified fact",
                "Reader candidate != admitted evidence",
                "contradiction candidate != confirmed contradiction",
            ):
                if marker not in text:
                    errors.append(f"{relative}: missing current D5 marker {marker!r}")
        elif f"translation-source: docs/EXTENDED_REFERENCE_POLICY.md@{SOURCE}" in text:
            errors.append(f"{relative}: refresh-needed translation falsely pins current source")
        check_links(relative, text, errors)

        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d5-source: main@{SOURCE}", f"d5-status: {expected_status}", GUIDE):
            if marker not in index:
                errors.append(f"{index_relative}: missing marker {marker!r}")
        check_links(index_relative, index, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D5 source checkpoint:** `main@{SOURCE}`",
        "D5 Reader-dependent detail translations are `CURRENT` in German, French and Russian",
        "six other supported locales are `REFRESH_NEEDED`",
        "48 `REFRESH_NEEDED` localized documents",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing D5 marker {marker!r}")

    if errors:
        print("D5 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("D5 translation status consistent: German + French + Russian CURRENT; 6 locales REFRESH_NEEDED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())