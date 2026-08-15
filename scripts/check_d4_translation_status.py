"""Validate mixed D4 project/grant/governance translation freshness after Italian parity refresh."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
CURRENT_LOCALES = ("de", "es", "fr", "it", "ru")
REFRESH_LOCALES = tuple(locale for locale in LOCALES if locale not in CURRENT_LOCALES)
FILES = {
    locale: (f"docs/{locale}/GRANT_OVERVIEW.md", f"docs/{locale}/GLOSSARY.md")
    for locale in LOCALES
}
LEGACY_BOUNDARY_MARKERS = (
    "d4-boundary: physical-l3-not-strict-canon",
    "d4-boundary: retrieval-score-not-evidence",
    "d4-boundary: model-output-not-source-truth",
    "d4-boundary: migration-proof-not-claim-proof",
    "d4-nonclaim: import-is-not-activation",
    "d4-nonclaim: nlnet-not-awarded",
    "d4-nonclaim: security-legal-gdpr-not-certified",
    "d4-nonclaim: native-speaker-editorial-not-certified",
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
        (ROOT / "docs/status/d4-translation-manifest.json").read_text(encoding="utf-8")
    )
    current = {locale: list(FILES[locale]) for locale in CURRENT_LOCALES}
    refresh = {locale: list(FILES[locale]) for locale in REFRESH_LOCALES}
    checks = (
        (manifest.get("phase") == "D4", "phase"),
        (manifest.get("tracking_issue") == 341, "tracking issue"),
        (manifest.get("latest_refresh_issue") == 419, "latest refresh issue"),
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
            errors.append(f"D4 manifest: invalid {label}")

    for locale in LOCALES:
        expected_status = "CURRENT" if locale in CURRENT_LOCALES else "REFRESH_NEEDED"
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d4-source: main@{SOURCE}", f"d4-status: {expected_status}"):
            if marker not in index:
                errors.append(f"{index_relative}: missing {marker!r}")
        check_links(index_relative, index, errors)

        for relative in FILES[locale]:
            text = (ROOT / relative).read_text(encoding="utf-8")
            is_grant = relative.endswith("GRANT_OVERVIEW.md")
            source_doc = (
                "docs/PROJECT_GRANT_AND_GOVERNANCE.md" if is_grant else "docs/GLOSSARY.md"
            )
            for marker in (
                f"translation-source: {source_doc}@",
                f"d4-locale: {locale}",
                "physical L3",
                "strict Canon",
                "active=false",
                "€50,000",
            ):
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            if locale in CURRENT_LOCALES:
                for marker in (
                    f"translation-source: {source_doc}@{SOURCE}",
                    "translation-status: CURRENT",
                    "RC-1",
                    "RC-2",
                    "RC-3",
                    "RC-4",
                    "RC-5",
                    "dedicated",
                    "EXTRACTED_PROPOSITION",
                    "Reader candidate",
                    "contradiction candidate != confirmed contradiction",
                ):
                    if marker not in text:
                        errors.append(f"{relative}: missing current D4 semantic marker {marker!r}")
                grant_markers = (
                    (
                        "programme: NLnet NGI0 Commons Fund",
                        "proposal: submitted",
                        "review: in progress",
                        "award: not awarded",
                        "budget change: none",
                    )
                    if is_grant
                    else ("submitted / under review / not awarded", "budget change", "not awarded")
                )
                for marker in grant_markers:
                    if marker not in text:
                        errors.append(f"{relative}: missing current grant marker {marker!r}")
                if not is_grant:
                    for marker in (
                        "source owner",
                        "proposition presentation category",
                        "POSSIBLE_CONTRADICTION",
                        "EXCEPTION",
                        "QUALIFICATION",
                        "TENSION",
                    ):
                        if marker not in text:
                            errors.append(f"{relative}: missing RC-5 glossary marker {marker!r}")
            else:
                for marker in LEGACY_BOUNDARY_MARKERS:
                    if marker not in text:
                        errors.append(f"{relative}: restored baseline missing legacy boundary marker {marker!r}")
                if f"translation-source: {source_doc}@{SOURCE}" in text:
                    errors.append(f"{relative}: refresh-needed translation falsely pins current source")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D4 source checkpoint:** `main@{SOURCE}`",
        "D4 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian and Russian",
        "four other supported locales are `REFRESH_NEEDED`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing D4 marker {marker!r}")

    if errors:
        print("D4 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("D4 translation status consistent: German + French + Spanish + Italian + Russian CURRENT; 4 locales REFRESH_NEEDED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
