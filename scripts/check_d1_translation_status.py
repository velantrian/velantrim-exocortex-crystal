"""Validate mixed D1 localization freshness after Reader RC-5."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
REFRESH = tuple(x for x in LOCALES if x != "ru")
READER = ("reader_core_rc1_skeleton               = true", "reader_core_rc2_structural_map         = true", "reader_core_rc3_multi_pass_mechanics   = true", "reader_core_rc4_proposition_extraction = true", "reader_core_rc5_relation_candidates    = true", "dedicated_reader_core                  = false")

def main() -> int:
    errors: list[str] = []
    docs = json.loads((ROOT / "docs/status/implementation-manifest.json").read_text())["documentation"]
    if docs.get("d1_source_checkpoint") != SOURCE: errors.append("manifest: D1 source checkpoint")
    if docs.get("d1_current_locales") != ["ru"]: errors.append("manifest: D1 current locales")
    if docs.get("d1_refresh_needed_locales") != list(REFRESH): errors.append("manifest: D1 refresh locales")
    for locale in LOCALES:
        status = "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
        index = (ROOT / f"docs/{locale}/README.md").read_text()
        for marker in (f"d1-source: main@{SOURCE}", f"d1-status: {status}"):
            if marker not in index: errors.append(f"docs/{locale}/README.md: {marker}")
        for name in ("STATUS.md", "IMPLEMENTATION_STATUS.md"):
            relative = f"docs/{locale}/{name}"
            text = (ROOT / relative).read_text()
            source_doc = f"docs/{name}"
            if f"translation-source: {source_doc}@" not in text: errors.append(f"{relative}: source marker")
            if locale == "ru":
                for marker in (f"translation-source: {source_doc}@{SOURCE}", "translation-status: CURRENT", "active=false", *READER, "contradiction candidate != confirmed contradiction"):
                    if marker not in text: errors.append(f"{relative}: {marker}")
            elif f"translation-source: {source_doc}@{SOURCE}" in text:
                errors.append(f"{relative}: stale translation pins RC-5 source")
        quick = (ROOT / f"docs/{locale}/QUICKSTART.md").read_text()
        if "translation-status: CURRENT" not in quick: errors.append(f"docs/{locale}/QUICKSTART.md: not CURRENT")
    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text()
    for marker in (f"D1 source checkpoint:** `main@{SOURCE}`", "D1 Reader-dependent detail translations are `CURRENT` in Russian", "eight other supported locales are `REFRESH_NEEDED`"):
        if marker not in ledger: errors.append(f"ledger: {marker}")
    if errors:
        print("D1 translation validation failed:")
        for error in errors: print(f"  - {error}")
        return 1
    print("D1 translation status consistent: Russian CURRENT at RC-5; 8 locales REFRESH_NEEDED")
    return 0
if __name__ == "__main__": raise SystemExit(main())
