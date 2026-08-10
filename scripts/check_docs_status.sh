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
source_checkpoint = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
locales = ["ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN"]
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

expect(checkpoint.get("commit"), runtime_commit, "runtime checkpoint")
expect(tests.get("passed"), 2078, "tests passed")
expect(tests.get("skipped"), 13, "tests skipped")
expect(tests.get("failed"), 0, "tests failed")
expect(tests.get("measured_statements"), 9756, "measured statements")
expect(tests.get("coverage_percent"), 100.0, "coverage")
expect(ci.get("job_count"), 9, "CI job count")
expect(boundaries.get("reader_core_rc1_skeleton"), True, "Reader RC-1")
expect(boundaries.get("reader_core_rc2_structural_map"), True, "Reader RC-2")
expect(boundaries.get("dedicated_reader_core"), False, "dedicated Reader")
expect(boundaries.get("postgresql_target_active"), False, "PostgreSQL active")
expect(boundaries.get("automatic_backend_switching"), False, "automatic switching")
expect(docs.get("localized_readme_source_checkpoint"), source_checkpoint, "localized README source")
expect(docs.get("full_parity_current_locales"), locales, "root locale set")
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
    "reader_core_rc1_skeleton", "reader_core_rc2_structural_map", "dedicated_reader_core",
)

for locale, relative in localized.items():
    path = root / relative
    if not path.is_file():
        errors.append(f"missing root README: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    if f"localization-source: main@{source_checkpoint}" not in text:
        errors.append(f"{relative}: wrong localization source")
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

root_readme = (root / "README.md").read_text(encoding="utf-8")
for marker in ("Reader foundation", "reader_core_rc1", "reader_core_rc2", "dedicated multi-pass Reader"):
    if marker not in root_readme:
        errors.append(f"README.md: missing Reader marker {marker!r}")

for locale in locales:
    index = (root / "docs" / locale / "README.md").read_text(encoding="utf-8")
    for marker in (
        f"localization-index-source: main@{source_checkpoint}",
        f"d1-source: main@{source_checkpoint}",
        "d2-status: CURRENT",
        f"d3-source: main@{source_checkpoint}",
        f"d4-source: main@{source_checkpoint}",
        f"d5-source: main@{source_checkpoint}",
        "Localization policy", "Translation status",
    ):
        if marker not in index:
            errors.append(f"docs/{locale}/README.md: missing {marker!r}")

required = {
    "docs/STATUS.md": (runtime_commit, "reader_core_rc1_skeleton", "reader_core_rc2_structural_map", "dedicated_reader_core", "active=false"),
    "docs/IMPLEMENTATION_STATUS.md": ("reader_core_rc1_skeleton = true", "reader_core_rc2_structural_map = true", "dedicated_reader_core          = false"),
    "docs/ARCHITECTURE_OVERVIEW.md": ("RC-1", "RC-2", "dedicated multi-pass Reader", "active=false"),
    "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md": ("Reader artifact", "Reader structure", "active=false"),
    "docs/PROJECT_GRANT_AND_GOVERNANCE.md": ("RC-1", "RC-2", "submitted", "€50,000"),
    "docs/GLOSSARY.md": ("Reader Core RC-1", "Reader Core RC-2", "dedicated Reader Core"),
    "docs/EXTENDED_REFERENCE_POLICY.md": ("reader_core_rc1_skeleton", "reader_core_rc2_structural_map", "dedicated_reader_core"),
    "docs/TRANSLATION_STATUS.md": ("D1 is complete", "D2 is complete", "D3 is complete", "D4 is complete", "D5 is complete"),
    "docs/DOCUMENTATION_MAP.md": ("CURRENT full-parity localized READMEs", "REFRESH_NEEDED translated document packs", "Inactive PostgreSQL import"),
    "docs/ai/CURRENT_STATE.md": ("all nine supported", "REFRESH_NEEDED", "active=false", "reader_core_rc2_structural_map = true"),
    "docs/ai/README.md": ("all nine supported", "docs-only PR", "REFRESH_NEEDED"),
    "TEST_REPORT.md": (runtime_commit, "2078 passed / 13 skipped / 0 failed", "31256316532"),
    "docs/GRANT_NLNET_SCOPE.md": ("submitted / under review / not awarded", "cannot be budgeted again"),
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

print("Documentation status is internally consistent: Reader RC-1/RC-2 bounded=true, dedicated=false, root-readmes=9-current, D1-D5 current")
PY
