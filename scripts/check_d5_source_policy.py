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
    for path in ROOT.iterdir():
        if path.is_file() and path.suffix in exts:
            paths.add(path.relative_to(ROOT).as_posix())
    for base in (ROOT / "docs", ROOT / ".github"):
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in exts:
                paths.add(path.relative_to(ROOT).as_posix())
    return sorted(paths)


def classify(relative: str, manifest: dict[str, object]) -> str:
    if relative in set(manifest["retired_exact"]):
        return "RETIRED"
    if relative.startswith(tuple(manifest["retired_prefixes"])) and relative not in set(
        manifest["retired_prefix_exceptions"]
    ):
        return "RETIRED"
    if relative in set(manifest["current_exact"]):
        return "CURRENT"
    if relative in set(manifest["refresh_needed_exact"]):
        return "REFRESH_NEEDED"

    for locale in LOCALES:
        if relative == f"README.{locale}.md":
            return "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
        if relative.startswith(f"docs/{locale}/"):
            name = relative.rsplit("/", 1)[-1]
            if locale == "ru":
                return "CURRENT"
            if name in set(manifest["current_locale_pack_files"]):
                return "CURRENT"
            return "REFRESH_NEEDED"

    return str(manifest["default_state"])


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_refresh = [locale for locale in LOCALES if locale != "ru"]
    checks = (
        (manifest.get("phase") == "D5_SOURCE_INVENTORY", "phase"),
        (
            manifest.get("repository_checkpoint")
            == "3de746e74be844c6fda55849c10faac5c3f0631a",
            "inventory checkpoint",
        ),
        (manifest.get("fully_current_locales") == ["ru"], "current locale"),
        (manifest.get("refresh_needed_locales") == expected_refresh, "refresh locales"),
        (
            manifest.get("localized_d5_decision")
            == "RC5_RUSSIAN_ROOT_AND_DETAILS_CURRENT_EIGHT_ROOT_AND_READER_DETAILS_REFRESH_NEEDED",
            "RC-5 decision",
        ),
        (manifest.get("reader_core_rc5_relation_candidates_claim") is True, "RC-5 claim"),
        (
            manifest.get("dedicated_reader_core_implemented_claim") is False,
            "dedicated claim",
        ),
        (manifest.get("active_postgresql_runtime_claim") is False, "PostgreSQL claim"),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"manifest: {label}")

    resolved = {
        path: classify(path, manifest)
        for path in eligible(set(manifest["eligible_extensions"]))
    }
    counts = Counter(resolved.values())
    invalid = set(counts) - ALLOWED
    if invalid:
        errors.append(f"invalid states: {invalid}")

    expected_debt = len(expected_refresh) + len(expected_refresh) * len(
        manifest["refresh_needed_locale_pack_files"]
    )
    if counts["REFRESH_NEEDED"] != expected_debt:
        errors.append(
            f"expected REFRESH_NEEDED={expected_debt}, got {counts['REFRESH_NEEDED']}"
        )

    policy = (ROOT / "docs/EXTENDED_REFERENCE_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for marker in (
        "reader_core_rc5_relation_candidates",
        "contradiction candidate != confirmed contradiction",
        "reader candidate        != admitted evidence",
        "active=false",
        "submitted / under review / not awarded",
        "budget change is none",
    ):
        if marker.lower() not in policy:
            errors.append(f"policy: missing {marker!r}")

    if errors:
        print("D5 source policy validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    rendered_counts = ", ".join(f"{key}={counts[key]}" for key in sorted(ALLOWED))
    print(f"D5 resolved inventory counts: {rendered_counts}")
    print(
        "D5 source inventory consistent: Russian CURRENT; "
        f"RC-5 localized refresh debt={expected_debt}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
