"""Validate mixed D5 extended-reference translation freshness after RC-5."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
REFRESH = tuple(x for x in LOCALES if x != "ru")
GUIDE = "EXTENDED_REFERENCE_GUIDE.md"

def main() -> int:
    errors: list[str] = []
    m = json.loads((ROOT / "docs/status/d5-translation-manifest.json").read_text())
    for ok, label in ((m.get("english_source_checkpoint") == SOURCE, "source"), (m.get("current_locales") == ["ru"], "current locales"), (m.get("refresh_needed_locales") == list(REFRESH), "refresh locales"), (m.get("reader_core_rc5_relation_candidates_claim") is True, "RC-5 claim"), (m.get("dedicated_reader_core_implemented_claim") is False, "dedicated claim")):
        if not ok: errors.append(f"manifest: {label}")
    for locale in LOCALES:
        status = "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
        relative = f"docs/{locale}/{GUIDE}"
        text = (ROOT / relative).read_text()
        index = (ROOT / f"docs/{locale}/README.md").read_text()
        for marker in (f"d5-source: main@{SOURCE}", f"d5-status: {status}", GUIDE):
            if marker not in index: errors.append(f"docs/{locale}/README.md: {marker}")
        if locale == "ru":
            for marker in (f"translation-source: docs/EXTENDED_REFERENCE_POLICY.md@{SOURCE}", "translation-status: CURRENT", "d5-reader: rc5-relation-candidates-implemented", "POSSIBLE_CONTRADICTION", "EXCEPTION", "QUALIFICATION", "TENSION", "submitted / under review / not awarded", "€50,000", "budget change: none", "REFRESH_NEEDED", "coverage != comprehension proof", "pass completion != comprehension proof", "EXTRACTED_PROPOSITION != verified fact", "Reader candidate != admitted evidence", "contradiction candidate != confirmed contradiction", "active=false"):
                if marker not in text: errors.append(f"{relative}: {marker}")
        elif f"translation-source: docs/EXTENDED_REFERENCE_POLICY.md@{SOURCE}" in text:
            errors.append(f"{relative}: stale translation pins RC-5 source")
    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text()
    for marker in (f"D5 source checkpoint:** `main@{SOURCE}`", "D5 Reader-dependent detail translations are `CURRENT` in Russian", "eight other supported locales are `REFRESH_NEEDED`", "64 `REFRESH_NEEDED` localized documents"):
        if marker not in ledger: errors.append(f"ledger: {marker}")
    if errors:
        print("D5 translation validation failed:")
        for error in errors: print(f"  - {error}")
        return 1
    print("D5 translation status consistent: Russian CURRENT at RC-5; 8 locales REFRESH_NEEDED")
    return 0
if __name__ == "__main__": raise SystemExit(main())
