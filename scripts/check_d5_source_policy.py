"""Resolve and validate the D5 repository documentation inventory through Reader RC-5."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/status/d5-inventory.json"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
ALLOWED = {"CURRENT", "REFRESH_NEEDED", "RETIRED", "ENGLISH_ONLY_BY_DESIGN"}

def eligible(exts: set[str]) -> list[str]:
    paths: set[str] = set()
    for p in ROOT.iterdir():
        if p.is_file() and p.suffix in exts: paths.add(p.relative_to(ROOT).as_posix())
    for base in (ROOT / "docs", ROOT / ".github"):
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in exts: paths.add(p.relative_to(ROOT).as_posix())
    return sorted(paths)

def classify(relative: str, m: dict[str, object]) -> str:
    if relative in set(m["retired_exact"]): return "RETIRED"
    if relative.startswith(tuple(m["retired_prefixes"])) and relative not in set(m["retired_prefix_exceptions"]): return "RETIRED"
    if relative in set(m["current_exact"]): return "CURRENT"
    if relative in set(m["refresh_needed_exact"]): return "REFRESH_NEEDED"
    for locale in LOCALES:
        if relative == f"README.{locale}.md": return "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
        if relative.startswith(f"docs/{locale}/"):
            name = relative.rsplit("/", 1)[-1]
            if locale == "ru": return "CURRENT"
            if name in set(m["current_locale_pack_files"]): return "CURRENT"
            return "REFRESH_NEEDED"
    return str(m["default_state"])

def main() -> int:
    errors: list[str] = []
    m = json.loads(MANIFEST.read_text())
    expected_refresh = [x for x in LOCALES if x != "ru"]
    checks = ((m.get("phase") == "D5_SOURCE_INVENTORY", "phase"), (m.get("repository_checkpoint") == "3de746e74be844c6fda55849c10faac5c3f0631a", "inventory checkpoint"), (m.get("fully_current_locales") == ["ru"], "current locale"), (m.get("refresh_needed_locales") == expected_refresh, "refresh locales"), (m.get("localized_d5_decision") == "RC5_RUSSIAN_ROOT_AND_DETAILS_CURRENT_EIGHT_ROOT_AND_READER_DETAILS_REFRESH_NEEDED", "RC-5 decision"), (m.get("reader_core_rc5_relation_candidates_claim") is True, "RC-5 claim"), (m.get("dedicated_reader_core_implemented_claim") is False, "dedicated claim"), (m.get("active_postgresql_runtime_claim") is False, "PostgreSQL claim"))
    for ok, label in checks:
        if not ok: errors.append(f"manifest: {label}")
    resolved = {p: classify(p, m) for p in eligible(set(m["eligible_extensions"]))}
    counts = Counter(resolved.values())
    if not set(counts).issubset(ALLOWED): errors.append(f"invalid states: {set(counts) - ALLOWED}")
    expected_debt = len(expected_refresh) + len(expected_refresh) * len(m["refresh_needed_locale_pack_files"])
    if counts["REFRESH_NEEDED"] != expected_debt: errors.append(f"expected REFRESH_NEEDED={expected_debt}, got {counts['REFRESH_NEEDED']}")
    policy = (ROOT / "docs/EXTENDED_REFERENCE_POLICY.md").read_text().lower()
    for marker in ("reader_core_rc5_relation_candidates", "contradiction candidate != confirmed contradiction", "reader candidate        != admitted evidence", "active=false", "submitted / under review / not awarded", "budget change is none"):
        if marker.lower() not in policy: errors.append(f"policy: missing {marker!r}")
    if errors:
        print("D5 source policy validation failed:")
        for error in errors: print(f"  - {error}")
        return 1
    print("D5 resolved inventory counts: " + ", ".join(f"{k}={counts[k]}" for k in sorted(ALLOWED)))
    print(f"D5 source inventory consistent: Russian CURRENT; RC-5 localized refresh debt={expected_debt}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
