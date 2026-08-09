"""Validate all current D3 architecture/storage translations."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "208f1c772ee3a112cb803d2413c120bef23adb05"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
FILES = {
    locale: (
        f"docs/{locale}/ARCHITECTURE_OVERVIEW.md",
        f"docs/{locale}/STORAGE_AND_AUTHORITY_BOUNDARIES.md",
    )
    for locale in LOCALES
}
MARKERS = (
    "translation-status: CURRENT",
    "d3-boundary: physical-l3-not-strict-canon",
    "d3-boundary: public-query-read-only",
    "d3-boundary: postgresql-active=false",
    "d3-nonclaim: import-is-not-activation",
    "d3-nonclaim: reader-core-not-implemented",
    "d3-nonclaim: nlnet-not-awarded",
    "core.query_pipeline.query()",
    "active=false",
    "Reader Core",
)
UNSUPPORTED = (
    "active PostgreSQL runtime is implemented",
    "automatic backend switching is enabled",
    "Reader Core is implemented",
    "NLnet grant was awarded",
    "security, legal or GDPR certified",
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
    manifest = json.loads((ROOT / "docs/status/d3-translation-manifest.json").read_text(encoding="utf-8"))
    expected_documents = {locale: list(FILES[locale]) for locale in LOCALES}
    checks = (
        (manifest.get("phase") == "D3", "phase"),
        (manifest.get("tracking_issue") == 341, "tracking issue"),
        (manifest.get("english_source_checkpoint") == SOURCE, "source checkpoint"),
        (manifest.get("source_documents") == ["docs/ARCHITECTURE_OVERVIEW.md", "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md"], "source documents"),
        (manifest.get("current_locales") == list(LOCALES), "current locales"),
        (manifest.get("pending_locales") == [], "pending locales"),
        (manifest.get("current_documents") == expected_documents, "current documents"),
        (manifest.get("native_speaker_editorial_certification") is False, "native certification"),
        (manifest.get("active_postgresql_runtime_claim") is False, "PostgreSQL runtime claim"),
        (manifest.get("automatic_backend_switching_claim") is False, "switching claim"),
        (manifest.get("reader_core_implemented_claim") is False, "Reader Core claim"),
        (manifest.get("security_legal_gdpr_certification_claim") is False, "certification claim"),
        (manifest.get("nlnet_awarded_claim") is False, "grant claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"D3 manifest: invalid {label}")

    for locale in LOCALES:
        index_relative = f"docs/{locale}/README.md"
        index = (ROOT / index_relative).read_text(encoding="utf-8")
        for marker in (f"d3-source: main@{SOURCE}", "d3-status: CURRENT", "d4-status: REFRESH_NEEDED", "ARCHITECTURE_OVERVIEW.md", "STORAGE_AND_AUTHORITY_BOUNDARIES.md", "Localization policy", "Translation status"):
            if marker not in index:
                errors.append(f"{index_relative}: missing marker {marker!r}")
        check_links(index_relative, index, errors)
        for relative in FILES[locale]:
            path = ROOT / relative
            if not path.is_file():
                errors.append(f"missing D3 file: {relative}")
                continue
            text = path.read_text(encoding="utf-8")
            expected_source = "docs/ARCHITECTURE_OVERVIEW.md" if relative.endswith("ARCHITECTURE_OVERVIEW.md") else "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md"
            for marker in (f"translation-source: {expected_source}@{SOURCE}", f"d3-locale: {locale}", *MARKERS):
                if marker not in text:
                    errors.append(f"{relative}: missing marker {marker!r}")
            for unsupported in UNSUPPORTED:
                if unsupported in text:
                    errors.append(f"{relative}: unsupported claim {unsupported!r}")
            check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (f"D3 source checkpoint:** `main@{SOURCE}`", "D3 is complete for all nine supported locales", "| Simplified Chinese | `CURRENT` | `CURRENT` |", "D3 architecture/storage authority | all nine supported locales `CURRENT`"):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")

    current_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in ("D3 is current across all nine supported locale packs", f"main@{SOURCE}", "18 architecture/storage documents plus nine indexes", "D4 project/grant context remains `REFRESH_NEEDED`"):
        if marker not in current_state:
            errors.append(f"AI current state: missing marker {marker!r}")

    doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    for marker in ("Root READMEs, D1, D2 and D3 are current", "D3 translation manifest", "D4–D5 remain", "REFRESH_NEEDED translated document packs"):
        if marker not in doc_map:
            errors.append(f"documentation map: missing marker {marker!r}")

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for marker in ("Validate D3 translation status", "python scripts/check_d3_translation_status.py"):
        if marker not in workflow:
            errors.append(f"CI workflow: missing D3 translation validator marker {marker!r}")

    if errors:
        print("D3 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"D3 translation status is consistent: locales={len(LOCALES)}, source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
