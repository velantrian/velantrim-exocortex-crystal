"""Validate mixed D4 translation freshness after Reader RC-5."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
REFRESH = tuple(x for x in LOCALES if x != "ru")
FILES = ("GRANT_OVERVIEW.md", "GLOSSARY.md")
LEGACY = ("d4-boundary: physical-l3-not-strict-canon", "d4-boundary: retrieval-score-not-evidence", "d4-boundary: model-output-not-source-truth", "d4-boundary: migration-proof-not-claim-proof", "d4-nonclaim: import-is-not-activation", "d4-nonclaim: nlnet-not-awarded", "d4-nonclaim: security-legal-gdpr-not-certified", "d4-nonclaim: native-speaker-editorial-not-certified")

def main() -> int:
    errors: list[str] = []
    manifest = json.loads((ROOT / "docs/status/d4-translation-manifest.json").read_text())
    for ok, label in ((manifest.get("english_source_checkpoint") == SOURCE, "source"), (manifest.get("current_locales") == ["ru"], "current locales"), (manifest.get("refresh_needed_locales") == list(REFRESH), "refresh locales"), (manifest.get("reader_core_rc5_relation_candidates_claim") is True, "RC-5 claim"), (manifest.get("nlnet_awarded_claim") is False, "grant claim")):
        if not ok: errors.append(f"manifest: {label}")
    for locale in LOCALES:
        status = "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
        index = (ROOT / f"docs/{locale}/README.md").read_text()
        for marker in (f"d4-source: main@{SOURCE}", f"d4-status: {status}"):
            if marker not in index: errors.append(f"docs/{locale}/README.md: {marker}")
        for name in FILES:
            relative = f"docs/{locale}/{name}"
            text = (ROOT / relative).read_text()
            source_doc = "docs/PROJECT_GRANT_AND_GOVERNANCE.md" if name == "GRANT_OVERVIEW.md" else "docs/GLOSSARY.md"
            for marker in (f"translation-source: {source_doc}@", f"d4-locale: {locale}", "physical L3", "strict Canon", "active=false", "€50,000"):
                if marker not in text: errors.append(f"{relative}: {marker}")
            if locale == "ru":
                for marker in (f"translation-source: {source_doc}@{SOURCE}", "translation-status: CURRENT", "RC-5", "EXTRACTED_PROPOSITION", "Reader candidate", "contradiction candidate != confirmed contradiction"):
                    if marker not in text: errors.append(f"{relative}: {marker}")
                if name == "GRANT_OVERVIEW.md":
                    for marker in ("programme: NLnet NGI0 Commons Fund", "proposal: submitted", "review: in progress", "award: not awarded", "budget change: none"):
                        if marker not in text: errors.append(f"{relative}: {marker}")
                else:
                    for marker in ("source owner", "proposition presentation category", "POSSIBLE_CONTRADICTION", "EXCEPTION", "QUALIFICATION", "TENSION"):
                        if marker not in text: errors.append(f"{relative}: {marker}")
            else:
                for marker in LEGACY:
                    if marker not in text: errors.append(f"{relative}: missing legacy marker {marker}")
                if f"translation-source: {source_doc}@{SOURCE}" in text: errors.append(f"{relative}: stale translation pins RC-5 source")
    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text()
    for marker in (f"D4 source checkpoint:** `main@{SOURCE}`", "D4 Reader-dependent detail translations are `CURRENT` in Russian", "eight other supported locales are `REFRESH_NEEDED`"):
        if marker not in ledger: errors.append(f"ledger: {marker}")
    if errors:
        print("D4 translation validation failed:")
        for error in errors: print(f"  - {error}")
        return 1
    print("D4 translation status consistent: Russian CURRENT at RC-5; 8 locales REFRESH_NEEDED")
    return 0
if __name__ == "__main__": raise SystemExit(main())
