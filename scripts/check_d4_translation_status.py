"""Validate all current D4 project/grant/governance/glossary translations."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "151b41c680190f7f3de729bf63e8e80a9d2285ce"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
FILES = {
    locale: (
        f"docs/{locale}/GRANT_OVERVIEW.md",
        f"docs/{locale}/GLOSSARY.md",
    )
    for locale in LOCALES
}
MARKERS = (
    "translation-status: CURRENT",
    "d4-boundary: physical-l3-not-strict-canon",
    "d4-boundary: retrieval-score-not-evidence",
    "d4-boundary: model-output-not-source-truth",
    "d4-boundary: migration-proof-not-claim-proof",
    "d4-nonclaim: import-is-not-activation",
    "d4-nonclaim: reader-core-not-implemented",
    "d4-nonclaim: nlnet-not-awarded",
    "d4-nonclaim: security-legal-gdpr-not-certified",
    "d4-nonclaim: native-speaker-editorial-not-certified",
    "physical L3",
    "strict Canon",
    "active=false",
    "Reader Core",
    "€50,000",
)
UNSUPPORTED = (
    "active PostgreSQL runtime is implemented",
    "automatic backend switching is enabled",
    "Reader Core is implemented",
    "NLnet grant was awarded",
    "approved €50,000 budget",
    "security, legal or GDPR certified",
    "native-speaker editorial certification: true",
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
    manifest = json.loads(
        (ROOT / "docs/status/d4-translation-manifest.json").read_text(encoding="utf-8")
    )
    expected_documents = {locale: list(FILES[locale]) for locale in LOCALES}
    checks = (
        (manifest.get("phase") == "D4", "phase"),
        (manifest.get("tracking_issue") == 341, "tracking issue"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (
            manifest.get("source_documents")
            == ["docs/PROJECT_GRANT_AND_GOVERNANCE.md", "docs/GLOSSARY.md"],
            "source documents",
        ),
        (manifest.get("current_locales") == list(LOCALES), "current locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == expected_documents, "current documents"),
        (
            manifest.get("locale_indexes")
            == [f"docs/{locale}/README.md" for locale in LOCALES],
            "locale indexes",
        ),
        (manifest.get("native_speaker_editorial_certification") is False, "native certification"),
        (manifest.get("security_legal_gdpr_certification_claim") is False, "certification claim"),
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
        (manifest.get("approved_budget_claim") is False, "approved budget claim"),
        (manifest.get("budget_change_claim") is False, "budget change claim"),
        (manifest.get("reader_core_implemented_claim") is False, "Reader Core claim"),
        (manifest.get("active_postgresql_runtime_claim") is False, "PostgreSQL runtime claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"D4 manifest: invalid {label}")

    for locale in LOCALES:
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (
            f"d4-source: main@{SOURCE}",
            "d4-status: CURRENT",
            "GRANT_OVERVIEW.md",
            "GLOSSARY.md",
            "Localization policy",
            "Translation status",
        ):
            if marker not in index:
                errors.append(f"{index_relative}: missing marker {marker!r}")
        if not any(
            marker in index
            for marker in ("d5-status: INVENTORY_PENDING", "d5-status: CURRENT")
        ):
            errors.append(
                f"{index_relative}: missing valid D5 progression marker "
                "('d5-status: INVENTORY_PENDING' or 'd5-status: CURRENT')"
            )
        check_links(index_relative, index, errors)

        for relative in FILES[locale]:
            path = ROOT / relative
            if not path.is_file():
                errors.append(f"missing D4 file: {relative}")
                continue
            text = path.read_text(encoding="utf-8")
            expected_source = (
                "docs/PROJECT_GRANT_AND_GOVERNANCE.md"
                if relative.endswith("GRANT_OVERVIEW.md")
                else "docs/GLOSSARY.md"
            )
            for marker in (
                f"translation-source: {expected_source}@{SOURCE}",
                f"d4-locale: {locale}",
                *MARKERS,
            ):
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            for unsupported in UNSUPPORTED:
                if unsupported in text:
                    errors.append(f"{relative}: unsupported claim {unsupported!r}")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D4 source checkpoint:** `main@{SOURCE}`",
        "D4 is complete for all nine supported locales",
        "| Simplified Chinese | `CURRENT` | `CURRENT` |",
        "D4 project/grant context | all nine supported locales `CURRENT`",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")

    current_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "D4 is current across all nine supported locale packs",
        f"main@{SOURCE}",
        "18 project/grant/glossary documents plus nine indexes",
    ):
        if marker not in current_state:
            errors.append(f"AI current state: missing marker {marker!r}")
    if not any(
        marker in current_state
        for marker in (
            "D5 extended-reference inventory remains pending",
            "D5 source inventory/policy is anchored",
        )
    ):
        errors.append("AI current state: missing valid D5 progression marker")

    doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    for marker in (
        "Root READMEs and D1–D4 are current",
        "D4 translation manifest",
        "D5 remains a separate inventory phase",
        "all nine supported locale packs",
    ):
        if marker not in doc_map:
            errors.append(f"documentation map: missing marker {marker!r}")

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for marker in (
        "Validate D4 translation status",
        "python scripts/check_d4_translation_status.py",
    ):
        if marker not in workflow:
            errors.append(f"CI workflow: missing D4 translation validator marker {marker!r}")

    if errors:
        print("D4 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"D4 translation status is consistent: locales={len(LOCALES)}, source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
