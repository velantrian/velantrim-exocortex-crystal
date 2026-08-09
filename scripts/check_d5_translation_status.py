"""Validate D5 extended-reference guides for all supported locales."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
GUIDE = "EXTENDED_REFERENCE_GUIDE.md"
MARKERS = (
    "translation-status: CURRENT",
    "d5-boundary: physical-l3-not-strict-canon",
    "d5-boundary: retrieval-score-not-evidence",
    "d5-boundary: model-output-not-source-truth",
    "d5-boundary: migration-proof-not-claim-proof",
    "d5-nonclaim: import-is-not-activation",
    "d5-nonclaim: reader-core-not-implemented",
    "d5-nonclaim: nlnet-not-awarded",
    "d5-nonclaim: security-legal-gdpr-not-certified",
    "d5-nonclaim: native-speaker-editorial-not-certified",
    "physical L3", "strict Canon", "retrieval score", "evidence",
    "model output", "source truth", "migration proof", "claim proof",
    "import success", "activation", "active=false", "Reader Core",
    "submitted / under review / not awarded", "€50,000", "budget change: none",
    "CURRENT", "RETIRED", "ENGLISH_ONLY_BY_DESIGN",
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
    manifest = json.loads((ROOT / "docs/status/d5-translation-manifest.json").read_text(encoding="utf-8"))
    expected = {locale: f"docs/{locale}/{GUIDE}" for locale in LOCALES}
    checks = (
        (manifest.get("phase") == "D5_TRANSLATIONS", "phase"),
        (manifest.get("tracking_issue") == 341, "issue"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (manifest.get("source_document") == "docs/EXTENDED_REFERENCE_POLICY.md", "source document"),
        (manifest.get("current_locales") == list(LOCALES), "current locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == expected, "current documents"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"D5 translation manifest: invalid {label}")
    for key in (
        "native_speaker_editorial_certification", "security_legal_gdpr_certification_claim",
        "nlnet_awarded_claim", "approved_budget_claim", "budget_change_claim",
        "reader_core_implemented_claim", "active_postgresql_runtime_claim",
    ):
        if manifest.get(key) is not False:
            errors.append(f"D5 translation manifest: unsupported claim {key}")

    for locale in LOCALES:
        relative = expected[locale]
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in (f"translation-source: docs/EXTENDED_REFERENCE_POLICY.md@{SOURCE}", f"d5-locale: {locale}", *MARKERS):
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        check_links(relative, text, errors)
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d5-source: main@{SOURCE}", "d5-status: CURRENT", GUIDE, "Localization policy", "Translation status"):
            if marker not in index:
                errors.append(f"{index_relative}: missing marker {marker!r}")
        check_links(index_relative, index, errors)

    inventory = json.loads((ROOT / "docs/status/d5-inventory.json").read_text(encoding="utf-8"))
    if GUIDE not in inventory.get("current_locale_pack_files", []):
        errors.append("D5 inventory: localized guide is not classified CURRENT")

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for marker in ("Validate D5 translation status", "python scripts/check_d5_translation_status.py"):
        if marker not in workflow:
            errors.append(f"CI workflow: missing marker {marker!r}")

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (f"D5 source checkpoint:** `main@{SOURCE}`", "D5 is complete for all nine supported locales", "Extended Reference Guide"):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")
    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in ("D5 is current across all nine supported locale packs", "nine Extended Reference Guides", SOURCE):
        if marker not in state:
            errors.append(f"AI current state: missing marker {marker!r}")
    doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    for marker in ("D1–D5 are current", "D5 translation manifest", "nine Extended Reference Guides"):
        if marker not in doc_map:
            errors.append(f"documentation map: missing marker {marker!r}")

    if errors:
        print("D5 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"D5 translation status is consistent: locales={len(LOCALES)}, source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
