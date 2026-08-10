#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

root = Path.cwd()
manifest = json.loads((root / "docs/status/implementation-manifest.json").read_text())
errors: list[str] = []

runtime_commit = "bbd816c09dd39a02e6de6c1014438490572f40f6"
source_checkpoint = "166fab5551c4b86ee0a546b2e1d3dc7adc240c86"
locales = ["ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN"]
refresh_locales = ["ar", "de", "es", "fr", "hi", "it", "ja", "zh-CN"]
localized = {locale: f"README.{locale}.md" for locale in locales}


def expect(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")

checkpoint = manifest["verified_runtime_checkpoint"]
tests = manifest["tests"]
ci = manifest["ci"]
boundaries = manifest["implemented_boundaries"]
docs = manifest["documentation"]
grant = manifest["grant"]
rc3 = manifest.get("reader_core_rc3", {})
rc4 = manifest.get("reader_core_rc4", {})

expect(checkpoint.get("commit"), runtime_commit, "runtime checkpoint")
expect(tests.get("passed"), 2078, "tests passed")
expect(tests.get("skipped"), 13, "tests skipped")
expect(tests.get("failed"), 0, "tests failed")
expect(tests.get("measured_statements"), 9756, "measured statements")
expect(tests.get("coverage_percent"), 100.0, "coverage")
expect(ci.get("job_count"), 9, "CI job count")
expect(boundaries.get("reader_core_rc1_skeleton"), True, "Reader RC-1")
expect(boundaries.get("reader_core_rc2_structural_map"), True, "Reader RC-2")
expect(boundaries.get("reader_core_rc3_multi_pass_mechanics"), True, "Reader RC-3")
expect(boundaries.get("reader_core_rc4_proposition_extraction"), True, "Reader RC-4")
expect(boundaries.get("dedicated_reader_core"), False, "dedicated Reader")
expect(boundaries.get("postgresql_target_active"), False, "PostgreSQL active")
expect(boundaries.get("automatic_backend_switching"), False, "automatic switching")
expect(rc3.get("tracking_issue"), 363, "RC-3 tracking issue")
expect(rc3.get("runtime_module"), "core/reader_passes.py", "RC-3 runtime module")
expect(rc3.get("one_active_pass_at_a_time"), True, "RC-3 sequential pass rule")
expect(rc3.get("count_only_telemetry"), True, "RC-3 telemetry rule")
expect(rc3.get("llm_or_provider_integration"), False, "RC-3 model integration")
expect(rc3.get("truth_or_canon_authority"), False, "RC-3 truth authority")
expect(rc4.get("tracking_issue"), 365, "RC-4 tracking issue")
expect(rc4.get("runtime_module"), "core/reader_extraction.py", "RC-4 runtime module")
expect(rc4.get("completed_pass_required"), True, "RC-4 completed pass rule")
expect(rc4.get("substantive_outcomes"), ["PROCESSED", "REVISITED"], "RC-4 substantive outcomes")
expect(rc4.get("fidelity"), "EXTRACTED_PROPOSITION", "RC-4 fidelity")
expect(rc4.get("source_owner_preserved"), True, "RC-4 source owner")
expect(rc4.get("negation_and_qualifiers_preserved"), True, "RC-4 qualifiers")
expect(rc4.get("count_only_telemetry"), True, "RC-4 telemetry")
expect(rc4.get("automatic_nlp_or_llm_extraction"), False, "RC-4 automatic extraction")
expect(rc4.get("fact_evidence_write"), False, "RC-4 fact evidence write")
expect(rc4.get("truth_or_canon_authority"), False, "RC-4 truth authority")
expect(docs.get("localized_readme_source_checkpoint"), source_checkpoint, "localized README source")
expect(docs.get("full_parity_current_locales"), ["ru"], "root current locale set")
expect(docs.get("full_parity_refresh_needed_locales"), refresh_locales, "root refresh locale set")
expect(docs.get("d1_source_checkpoint"), source_checkpoint, "D1 source")
expect(docs.get("d1_current_locales"), ["ru"], "D1 current locales")
expect(docs.get("d1_refresh_needed_locales"), refresh_locales, "D1 refresh locales")
expect(grant.get("submitted"), True, "grant submitted")
expect(grant.get("under_review"), True, "grant review")
expect(grant.get("awarded"), False, "grant awarded")

common = (
    runtime_commit,
    "2078 passed / 13 skipped / 0 failed",
    "9756",
    "active=false",
    "submitted / under review / not awarded",
    "Guardian", "TruthGate", "TrustSnapshot", "CanonicalView",
    "SQLite", "PostgreSQL", "HTTP /ask", "CLI ask", "MCP search",
    "docs/LOCALIZATION_POLICY.md", "docs/TRANSLATION_STATUS.md",
)

for locale, relative in localized.items():
    path = root / relative
    if not path.is_file():
        errors.append(f"missing root README: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in common:
        if marker not in text:
            errors.append(f"{relative}: missing marker {marker!r}")
    if path.stat().st_size < 6000:
        errors.append(f"{relative}: full README too small ({path.stat().st_size} bytes)")
    if text.count("```text") + text.count("```bash") < 7:
        errors.append(f"{relative}: insufficient diagram/code blocks")
    if text.count("|") < 20:
        errors.append(f"{relative}: insufficient table structure")
    for level in ("L0", "L1", "L2", "L3"):
        if level not in text:
            errors.append(f"{relative}: missing {level}")
    if locale == "ru":
        for marker in (
            f"localization-source: main@{source_checkpoint}",
            "localization-status: CURRENT",
            "reader_core_rc4_proposition_extraction",
            "EXTRACTED_PROPOSITION != verified fact",
            "Reader candidate != admitted evidence",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing current RC-4 marker {marker!r}")
    elif f"localization-source: main@{source_checkpoint}" in text:
        errors.append(f"{relative}: refresh-needed root README falsely pins RC-4 source")

root_readme = (root / "README.md").read_text(encoding="utf-8")
for marker in (
    "Reader foundation",
    "RC-1 evidence-linked skeleton",
    "RC-2 caller-supplied Structural Document Map",
    "RC-3 explicit deterministic multi-pass mechanics",
    "RC-4 source-linked proposition extraction",
    "Dedicated/full autonomous Reader: not implemented",
    "Reader pass completion is not comprehension proof",
    "EXTRACTED_PROPOSITION is not a verified fact",
    "Reader candidate is not admitted evidence",
):
    if marker not in root_readme:
        errors.append(f"README.md: missing Reader marker {marker!r}")

for locale in locales:
    index = (root / "docs" / locale / "README.md").read_text(encoding="utf-8")
    reader_status = "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
    for marker in (
        f"localization-index-source: main@{source_checkpoint}",
        f"d1-source: main@{source_checkpoint}",
        f"d1-status: {reader_status}",
        "d2-status: CURRENT",
        f"d3-source: main@{source_checkpoint}",
        f"d3-status: {reader_status}",
        f"d4-source: main@{source_checkpoint}",
        f"d4-status: {reader_status}",
        f"d5-source: main@{source_checkpoint}",
        f"d5-status: {reader_status}",
        "Localization policy", "Translation status",
    ):
        if marker not in index:
            errors.append(f"docs/{locale}/README.md: missing {marker!r}")

required = {
    "docs/STATUS.md": (runtime_commit, "reader_core_rc1_skeleton", "reader_core_rc2_structural_map", "reader_core_rc3_multi_pass_mechanics", "reader_core_rc4_proposition_extraction", "dedicated_reader_core", "active=false", "EXTRACTED_PROPOSITION"),
    "docs/IMPLEMENTATION_STATUS.md": ("reader_core_rc1_skeleton", "reader_core_rc2_structural_map", "reader_core_rc3_multi_pass_mechanics", "reader_core_rc4_proposition_extraction", "dedicated_reader_core", "core/reader_extraction.py"),
    "docs/ARCHITECTURE_OVERVIEW.md": ("RC-1", "RC-2", "RC-3", "RC-4", "dedicated/full autonomous Reader", "active=false", "EXTRACTED_PROPOSITION != verified fact"),
    "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md": ("Reader artifact", "Reader structure", "Reader pass ledger", "Reader proposition", "active=false", "EXTRACTED_PROPOSITION"),
    "docs/PROJECT_GRANT_AND_GOVERNANCE.md": ("RC-1", "RC-2", "RC-3", "RC-4", "submitted", "€50,000", "Reader candidate"),
    "docs/GLOSSARY.md": ("Reader Core RC-1", "Reader Core RC-2", "Reader Core RC-3", "Reader Core RC-4", "EXTRACTED_PROPOSITION", "dedicated/full Reader Core"),
    "docs/EXTENDED_REFERENCE_POLICY.md": ("reader_core_rc1_skeleton", "reader_core_rc2_structural_map", "reader_core_rc3_multi_pass_mechanics", "reader_core_rc4_proposition_extraction", "dedicated_reader_core", "REFRESH_NEEDED"),
    "docs/TRANSLATION_STATUS.md": ("Russian", "REFRESH_NEEDED", "root README", source_checkpoint, "Reader RC-4 boundary"),
    "docs/DOCUMENTATION_MAP.md": ("Inactive PostgreSQL import",),
    "docs/ai/CURRENT_STATE.md": ("reader_core_rc4_proposition_extraction = true", "eight other localized root README files", "active=false", source_checkpoint),
    "TEST_REPORT.md": (runtime_commit, "2078 passed / 13 skipped / 0 failed", "31256316532"),
    "docs/GRANT_NLNET_SCOPE.md": ("submitted / under review / not awarded", "cannot be budgeted again", "RC-4"),
    "SECURITY.md": ("not a security, legal or GDPR certification", "No automatic switching"),
}
for relative, markers in required.items():
    path = root / relative
    if not path.is_file():
        errors.append(f"missing required document: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{relative}: missing current marker {marker!r}")

link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
link_surfaces = ["README.md", *localized.values(), "docs/TRANSLATION_STATUS.md", "docs/DOCUMENTATION_MAP.md", *[f"docs/{locale}/README.md" for locale in locales]]
for relative in link_surfaces:
    source = root / relative
    text = source.read_text(encoding="utf-8")
    for raw in link_pattern.findall(text):
        target = raw.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split(maxsplit=1)[0].split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        resolved = (source.parent / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{relative}: link escapes repository: {raw!r}")
            continue
        if not resolved.exists():
            errors.append(f"{relative}: broken local link: {raw!r}")

if errors:
    print("Documentation status validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

print("Documentation status is internally consistent: Reader RC-1/RC-2/RC-3/RC-4 bounded=true, dedicated=false, Russian root/detail CURRENT, 8-locale Reader/root refresh-needed")
PY
