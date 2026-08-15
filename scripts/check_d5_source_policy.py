"""Resolve and validate the D5 repository documentation inventory after Japanese parity refresh."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/status/d5-inventory.json"
POLICY_PATH = ROOT / "docs/EXTENDED_REFERENCE_POLICY.md"
LOCALES = ("ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN")
CURRENT_LOCALES = ("de", "es", "fr", "it", "ja", "ru", "zh-CN")
ALLOWED = {"CURRENT", "REFRESH_NEEDED", "RETIRED", "ENGLISH_ONLY_BY_DESIGN"}


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def eligible_paths(extensions: set[str]) -> list[str]:
    paths: set[str] = set()
    for path in ROOT.iterdir():
        if path.is_file() and path.suffix in extensions:
            paths.add(path.relative_to(ROOT).as_posix())
    for base in (ROOT / "docs", ROOT / ".github"):
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in extensions:
                paths.add(path.relative_to(ROOT).as_posix())
    return sorted(paths)


def classify(relative: str, manifest: dict[str, object]) -> str:
    retired_exact = set(manifest["retired_exact"])
    retired_prefixes = tuple(manifest["retired_prefixes"])
    retired_exceptions = set(manifest["retired_prefix_exceptions"])
    current_exact = set(manifest["current_exact"])
    refresh_exact = set(manifest["refresh_needed_exact"])
    if relative in retired_exact:
        return "RETIRED"
    if relative.startswith(retired_prefixes) and relative not in retired_exceptions:
        return "RETIRED"
    if relative in current_exact:
        return "CURRENT"
    if relative in refresh_exact:
        return "REFRESH_NEEDED"
    for locale in LOCALES:
        if relative == f"README.{locale}.md":
            return (
                "CURRENT"
                if locale in set(manifest["root_readme_current_locales"])
                else "REFRESH_NEEDED"
            )
        if relative.startswith(f"docs/{locale}/"):
            name = relative.rsplit("/", 1)[-1]
            locale_files = set(manifest["locale_pack_files"])
            if name not in locale_files:
                return "REFRESH_NEEDED"
            if locale in set(manifest["fully_current_locales"]):
                return "CURRENT"
            if name in set(manifest["current_locale_pack_files"]):
                return "CURRENT"
            if name in set(manifest["refresh_needed_locale_pack_files"]):
                return "REFRESH_NEEDED"
            return "REFRESH_NEEDED"
    return str(manifest["default_state"])


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    policy = POLICY_PATH.read_text(encoding="utf-8")
    expected_current_locales = list(CURRENT_LOCALES)
    expected_refresh_locales = [locale for locale in LOCALES if locale not in CURRENT_LOCALES]

    if manifest.get("phase") != "D5_SOURCE_INVENTORY":
        errors.append("D5 manifest: invalid phase")
    if manifest.get("repository_checkpoint") != "3de746e74be844c6fda55849c10faac5c3f0631a":
        errors.append("D5 manifest: source-inventory checkpoint must remain the signed PR #350 merge")
    if manifest.get("tracking_issue") != 341:
        errors.append("D5 manifest: original tracking issue must remain #341")
    if manifest.get("latest_refresh_issue") != 423:
        errors.append("D5 manifest: Japanese refresh must be bound to issue #423")
    if manifest.get("supported_locales") != list(LOCALES):
        errors.append("D5 manifest: supported locale set/order mismatch")
    if manifest.get("fully_current_locales") != expected_current_locales:
        errors.append("D5 manifest: German, Spanish, French, Italian, Japanese, Russian and Simplified Chinese must be the fully current detail locales")
    if manifest.get("refresh_needed_locales") != expected_refresh_locales:
        errors.append("D5 manifest: refresh-needed locale set/order mismatch")
    if manifest.get("root_readme_current_locales") != expected_current_locales:
        errors.append("D5 manifest: German, Spanish, French, Italian, Japanese, Russian and Simplified Chinese must be the current localized root READMEs")
    if manifest.get("root_readme_refresh_needed_locales") != expected_refresh_locales:
        errors.append("D5 manifest: root README refresh-needed locale set/order mismatch")
    if manifest.get("localized_d5_decision") != "GERMAN_FRENCH_SPANISH_ITALIAN_JAPANESE_SIMPLIFIED_CHINESE_AND_RUSSIAN_ROOT_AND_DETAILS_CURRENT_TWO_ROOT_AND_READER_DETAILS_REFRESH_NEEDED":
        errors.append("D5 manifest: localization decision mismatch")
    if set(manifest.get("allowed_states", [])) != ALLOWED:
        errors.append("D5 manifest: allowed state set mismatch")
    if manifest.get("default_state") != "ENGLISH_ONLY_BY_DESIGN":
        errors.append("D5 manifest: detailed residual documents must default English-only")
    if manifest.get("refresh_needed_exact") != []:
        errors.append("D5 manifest: exact refresh entries must remain empty; locale-family rules own this backlog")

    false_claims = (
        "native_speaker_editorial_certification",
        "security_legal_gdpr_certification_claim",
        "nlnet_awarded_claim",
        "approved_budget_claim",
        "budget_change_claim",
        "dedicated_reader_core_implemented_claim",
        "active_postgresql_runtime_claim",
    )
    for key in false_claims:
        if manifest.get(key) is not False:
            errors.append(f"D5 manifest: unsupported claim flag {key}")
    for key in (
        "reader_core_rc1_skeleton_claim",
        "reader_core_rc2_structural_map_claim",
        "reader_core_rc3_multi_pass_mechanics_claim",
        "reader_core_rc4_proposition_extraction_claim",
        "reader_core_rc5_relation_candidates_claim",
    ):
        if manifest.get(key) is not True:
            errors.append(f"D5 manifest: missing bounded Reader claim {key}")

    extensions = set(manifest["eligible_extensions"])
    resolved: dict[str, str] = {}
    for relative in eligible_paths(extensions):
        state = classify(relative, manifest)
        if state not in ALLOWED:
            errors.append(f"{relative}: invalid or missing state {state!r}")
        resolved[relative] = state

    locale_files = set(manifest["locale_pack_files"])
    for locale in LOCALES:
        actual = {
            path.name
            for path in (ROOT / "docs" / locale).iterdir()
            if path.is_file() and path.suffix == ".md"
        }
        unexpected = actual - locale_files
        missing = locale_files - actual
        if unexpected:
            errors.append(f"docs/{locale}: unclassified extra localized files {sorted(unexpected)}")
        if missing:
            errors.append(f"docs/{locale}: missing D1-D5 files {sorted(missing)}")

    for relative in manifest["retired_exact"]:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"retired exact file missing: {relative}")
            continue
        searchable = normalized(path.read_text(encoding="utf-8", errors="replace"))
        if not any(marker in searchable for marker in ("historical", "archived", "handoff only")):
            errors.append(f"{relative}: retired file lacks visible historical warning")

    archive_readme = normalized((ROOT / "docs/archive/README.md").read_text(encoding="utf-8"))
    for marker in ("historical", "not canonical", "not reviewer claim material", "docs/architecture.md"):
        if normalized(marker) not in archive_readme:
            errors.append(f"archive routing: missing marker {marker!r}")

    policy_searchable = normalized(policy)
    for marker in (
        "d5-source-policy: current",
        "current",
        "refresh_needed",
        "retired",
        "english_only_by_design",
        "never permission to replace rich translations with short summaries",
        "reader_core_rc1_skeleton",
        "reader_core_rc2_structural_map",
        "reader_core_rc3_multi_pass_mechanics",
        "reader_core_rc4_proposition_extraction",
        "reader_core_rc5_relation_candidates",
        "dedicated_reader_core",
        "pre-admission",
        "has no truth/canon/esm/planner authority",
        "does not call `core.evidence.attach_evidence()`",
        "extracted_proposition",
        "reader candidate",
        "relation candidate",
        "contradiction candidate != confirmed contradiction",
        "active=false",
        "submitted / under review / not awarded",
        "budget change is none",
        "existing baseline, not future funded delta",
    ):
        if normalized(marker) not in policy_searchable:
            errors.append(f"D5 policy: missing marker {marker!r}")

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for marker in (
        "Validate D5 source inventory policy",
        "python scripts/check_d5_source_policy.py",
    ):
        if marker not in workflow:
            errors.append(f"CI workflow: missing marker {marker!r}")

    counts = Counter(resolved.values())
    if counts["CURRENT"] == 0 or counts["RETIRED"] == 0 or counts["ENGLISH_ONLY_BY_DESIGN"] == 0:
        errors.append(f"D5 inventory: implausible category counts {dict(counts)}")
    expected_refresh_count = (
        len(manifest["root_readme_refresh_needed_locales"])
        + len(manifest["refresh_needed_locales"])
        * len(manifest["refresh_needed_locale_pack_files"])
    )
    if counts["REFRESH_NEEDED"] != expected_refresh_count:
        errors.append(
            f"D5 inventory: expected refresh documents={expected_refresh_count}, observed={counts['REFRESH_NEEDED']}"
        )

    print(
        "D5 resolved inventory counts: "
        + ", ".join(f"{state}={counts[state]}" for state in sorted(ALLOWED))
    )
    print(f"D5 resolved inventory total: {len(resolved)}")
    if errors:
        print("D5 source policy validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        "D5 source inventory consistent: German + French + Spanish + Italian + Japanese + Simplified Chinese + Russian root/detail CURRENT; "
        f"localized refresh debt={expected_refresh_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
