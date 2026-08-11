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
source_checkpoint = "51c205fe048fd69d39fcd47b43e042a50de432bc"
locales = ["ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN"]
refresh_locales = [locale for locale in locales if locale != "ru"]


def expect(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")

checkpoint = manifest["verified_runtime_checkpoint"]
tests = manifest["tests"]
boundaries = manifest["implemented_boundaries"]
docs = manifest["documentation"]
grant = manifest["grant"]
rc5 = manifest.get("reader_core_rc5", {})
expect(checkpoint.get("commit"), runtime_commit, "runtime checkpoint")
expect(tests.get("passed"), 2078, "tests passed")
expect(tests.get("skipped"), 13, "tests skipped")
expect(tests.get("failed"), 0, "tests failed")
expect(tests.get("measured_statements"), 9756, "measured statements")
expect(tests.get("coverage_percent"), 100.0, "coverage")
for key in ("reader_core_rc1_skeleton", "reader_core_rc2_structural_map", "reader_core_rc3_multi_pass_mechanics", "reader_core_rc4_proposition_extraction", "reader_core_rc5_relation_candidates"):
    expect(boundaries.get(key), True, key)
expect(boundaries.get("dedicated_reader_core"), False, "dedicated Reader")
expect(boundaries.get("postgresql_target_active"), False, "PostgreSQL active")
expect(rc5.get("tracking_issue"), 367, "RC-5 issue")
expect(rc5.get("pull_request"), 368, "RC-5 PR")
expect(rc5.get("runtime_module"), "core/reader_relations.py", "RC-5 runtime")
expect(rc5.get("test_module"), "tests/test_reader_relations.py", "RC-5 tests")
expect(rc5.get("input_boundary"), "registered_rc4_proposition_candidates_only", "RC-5 input")
expect(rc5.get("relation_kinds"), ["POSSIBLE_CONTRADICTION", "EXCEPTION", "QUALIFICATION", "TENSION"], "RC-5 kinds")
for key in ("same_reader_session_required", "same_source_version_required", "within_document_only", "exact_candidate_id_linkage", "primary_and_supporting_provenance_preserved", "explicit_rationale_required", "count_only_telemetry"):
    expect(rc5.get(key), True, f"RC-5 {key}")
for key in ("automatic_semantic_equivalence", "automatic_cross_document_reasoning", "contradiction_resolution_authority", "automatic_winner_selection", "evidence_admission", "fact_evidence_write", "confidence_promotion", "llm_or_provider_integration", "embeddings_or_vector_database", "truth_or_canon_authority"):
    expect(rc5.get(key), False, f"RC-5 {key}")
expect(docs.get("localized_readme_source_checkpoint"), source_checkpoint, "localized README source")
expect(docs.get("full_parity_current_locales"), ["ru"], "root current locales")
expect(docs.get("full_parity_refresh_needed_locales"), refresh_locales, "root refresh locales")
expect(docs.get("d1_source_checkpoint"), source_checkpoint, "D1 source")
expect(grant.get("submitted"), True, "grant submitted")
expect(grant.get("under_review"), True, "grant review")
expect(grant.get("awarded"), False, "grant awarded")

common = (runtime_commit, "2078 passed / 13 skipped / 0 failed", "9756", "active=false", "submitted / under review / not awarded", "Guardian", "TruthGate", "TrustSnapshot", "CanonicalView", "SQLite", "PostgreSQL", "HTTP /ask", "CLI ask", "MCP search", "docs/LOCALIZATION_POLICY.md", "docs/TRANSLATION_STATUS.md")
for locale in locales:
    relative = f"README.{locale}.md"
    path = root / relative
    text = path.read_text(encoding="utf-8")
    for marker in common:
        if marker not in text:
            errors.append(f"{relative}: missing {marker!r}")
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
        for marker in (f"localization-source: main@{source_checkpoint}", "localization-status: CURRENT", "reader_core_rc5_relation_candidates    = true", "contradiction candidate  != confirmed contradiction"):
            if marker not in text:
                errors.append(f"{relative}: missing RC-5 marker {marker!r}")
    elif f"localization-source: main@{source_checkpoint}" in text:
        errors.append(f"{relative}: REFRESH_NEEDED root falsely pins RC-5 source")

root_readme = (root / "README.md").read_text(encoding="utf-8")
for marker in ("RC-5 — exception / qualification / tension / contradiction candidates", "core/reader_relations.py", "relation candidate      != admitted evidence", "contradiction candidate != confirmed contradiction", "Dedicated/full autonomous Reader: not implemented"):
    if marker not in root_readme:
        errors.append(f"README.md: missing RC-5 marker {marker!r}")

for locale in locales:
    index = (root / "docs" / locale / "README.md").read_text(encoding="utf-8")
    status = "CURRENT" if locale == "ru" else "REFRESH_NEEDED"
    for phase in ("d1", "d3", "d4", "d5"):
        for marker in (f"{phase}-source: main@{source_checkpoint}", f"{phase}-status: {status}"):
            if marker not in index:
                errors.append(f"docs/{locale}/README.md: missing {marker!r}")
    for marker in (f"localization-index-source: main@{source_checkpoint}", "d2-status: CURRENT", "Localization policy", "Translation status"):
        if marker not in index:
            errors.append(f"docs/{locale}/README.md: missing {marker!r}")

required = {
    "docs/STATUS.md": ("reader_core_rc5_relation_candidates", "core/reader_relations.py", "contradiction candidate != confirmed contradiction", "active=false"),
    "docs/IMPLEMENTATION_STATUS.md": ("reader_core_rc5_relation_candidates", "core/reader_relations.py", "POSSIBLE_CONTRADICTION", "EXCEPTION", "QUALIFICATION", "TENSION"),
    "docs/ARCHITECTURE_OVERVIEW.md": ("RC-5", "relation candidate", "contradiction candidate != confirmed contradiction", "active=false"),
    "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md": ("Reader relation", "RC-5", "contradiction candidate != confirmed contradiction", "active=false"),
    "docs/PROJECT_GRANT_AND_GOVERNANCE.md": ("RC-5", "submitted", "€50,000", "contradiction candidate != confirmed contradiction"),
    "docs/GLOSSARY.md": ("Reader Core RC-5", "POSSIBLE_CONTRADICTION", "EXCEPTION", "QUALIFICATION", "TENSION"),
    "docs/EXTENDED_REFERENCE_POLICY.md": ("reader_core_rc5_relation_candidates", "contradiction candidate != confirmed contradiction", "REFRESH_NEEDED"),
    "docs/TRANSLATION_STATUS.md": (source_checkpoint, "Reader RC-5 boundary", "64 `REFRESH_NEEDED` localized documents"),
    "docs/ai/CURRENT_STATE.md": (source_checkpoint, "reader_core_rc5_relation_candidates    = true", "eight other localized root README files"),
    "ROADMAP.md": ("RC-5 — Exceptions / Contradiction Candidate Detection", "RC-6 long-context strategy", "RC-7 cross-document reading"),
}
for relative, markers in required.items():
    text = (root / relative).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{relative}: missing {marker!r}")

link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
link_surfaces = ["README.md", "README.ru.md", "docs/TRANSLATION_STATUS.md", "docs/DOCUMENTATION_MAP.md", *[f"docs/{locale}/README.md" for locale in locales]]
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
print("Documentation status consistent: Reader RC-1..RC-5 bounded=true, dedicated=false; Russian CURRENT; 8 locales REFRESH_NEEDED")
PY
