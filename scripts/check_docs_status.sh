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


def expect(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        errors.append(f"{label} must equal {expected!r}, got {actual!r}")


checkpoint = manifest.get("verified_runtime_checkpoint", {})
tests = manifest.get("tests", {})
ci = manifest.get("ci", {})
integration = manifest.get("postgresql_integration", {})
mutation = manifest.get("mutation_gate", {})
boundaries = manifest.get("implemented_boundaries", {})
reader = manifest.get("reader_core_rc1", {})
reader_structure = manifest.get("reader_core_rc2", {})
documentation = manifest.get("documentation", {})
grant = manifest.get("grant", {})
limits = manifest.get("storage_resource_limits", {})

runtime_commit = "bbd816c09dd39a02e6de6c1014438490572f40f6"
runtime_head = "d7af7c80722274f9217bc5545d150f92e9363f37"
source_checkpoint = "e521440e9bb188d88475f17dd5bcdd161b314605"
expected_locales = ["ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN"]
expected_jobs = [
    "code-quality", "test (3.11)", "test (3.12)", "jsonl-integrity",
    "eval-gate", "security", "docker-build", "Ring Zero mutation gate",
    "docs-status",
]

expect(manifest.get("schema_version"), 1, "manifest schema_version")
expect(checkpoint.get("commit"), runtime_commit, "runtime checkpoint")
expect(checkpoint.get("validated_head"), runtime_head, "validated runtime head")
expect(checkpoint.get("pull_request"), 337, "runtime checkpoint PR")
expect(checkpoint.get("ci_run"), 31256316536, "runtime exact-head CI")
expect(tests.get("python_versions"), ["3.11", "3.12"], "tested Python versions")
expect(tests.get("passed"), 2078, "tests.passed")
expect(tests.get("skipped"), 13, "tests.skipped")
expect(tests.get("failed"), 0, "tests.failed")
expect(tests.get("measured_statements"), 9756, "measured statements")
expect(tests.get("coverage_percent"), 100.0, "coverage")
expect(ci.get("job_count"), 9, "CI job count")
expect(ci.get("jobs"), expected_jobs, "CI jobs")
expect(ci.get("all_successful"), True, "CI result")
expect(integration.get("ci_run"), 31256316532, "PostgreSQL integration CI")
expect(integration.get("job_count"), 1, "PostgreSQL integration jobs")
expect(integration.get("all_successful"), True, "PostgreSQL integration result")
expect(integration.get("target_active"), False, "PostgreSQL target state")
expect(integration.get("ann_indexes_present"), False, "ANN index state")
expect(mutation.get("declared_mutants"), 7, "declared mutants")
expect(mutation.get("killed_mutants"), 7, "killed mutants")

for key in (
    "public_query_surfaces_read_only", "explicit_contradiction_dispositions",
    "scoped_curator_authorization", "bounded_legacy_retrieval",
    "durable_l3_profile_lock", "sqlite_storage_lifecycle",
    "sqlite_logical_export_verification", "bounded_streaming_logical_migration",
    "postgresql_optional_driver_lazy_loaded", "postgresql_inactive_import",
    "postgresql_exact_state_equivalence", "reader_core_rc1_skeleton",
    "reader_core_rc2_structural_map",
):
    expect(boundaries.get(key), True, f"implemented_boundaries.{key}")
for key in (
    "truth_policy_runtime_bypass_present", "physical_l3_equals_strict_canon",
    "postgresql_target_active", "postgresql_normal_runtime_adapter",
    "cross_backend_migration_runtime", "postgresql_pgvector_runtime",
    "automatic_backend_switching", "distributed_curator_coordination",
    "production_idp_multitenancy", "dedicated_reader_core",
):
    expect(boundaries.get(key), False, f"implemented_boundaries.{key}")
expect(boundaries.get("sqlite_logical_export_resource_contract"), "bounded-streaming-local-first", "SQLite migration contract")

expect(reader.get("tracking_issue"), 357, "Reader RC-1 tracking issue")
expect(reader.get("architecture_contract"), "docs/architecture/READER_CORE_ARCHITECTURE.md", "Reader RC-1 architecture contract")
expect(reader.get("runtime_module"), "core/reader_core.py", "Reader RC-1 runtime module")
expect(reader.get("test_module"), "tests/test_reader_core.py", "Reader RC-1 test module")
expect(reader.get("scope"), "minimal_evidence_linked_domain_skeleton", "Reader RC-1 scope")
for key in (
    "source_body_storage", "durable_storage_schema", "public_api_or_cli",
    "llm_or_provider_integration", "embeddings_or_vector_database",
    "multi_pass_orchestration", "planner_or_belief_update_authority",
    "truth_or_canon_authority", "dedicated_full_reader_core",
):
    expect(reader.get(key), False, f"reader_core_rc1.{key}")

expect(reader_structure.get("tracking_issue"), 359, "Reader RC-2 tracking issue")
expect(reader_structure.get("architecture_contract"), "docs/architecture/READER_CORE_ARCHITECTURE.md", "Reader RC-2 architecture contract")
expect(reader_structure.get("runtime_module"), "core/reader_structure.py", "Reader RC-2 runtime module")
expect(reader_structure.get("test_module"), "tests/test_reader_structure.py", "Reader RC-2 test module")
expect(reader_structure.get("scope"), "source_version_bound_structural_document_map", "Reader RC-2 scope")
expect(reader_structure.get("caller_supplied_structure"), True, "Reader RC-2 caller-supplied structure")
for key in (
    "source_body_storage", "parser_or_semantic_chunker",
    "ocr_or_pdf_layout_reconstruction", "multimodal_image_understanding",
    "durable_storage_schema", "public_api_or_cli", "llm_or_provider_integration",
    "embeddings_or_vector_database", "multi_pass_orchestration",
    "planner_or_belief_update_authority", "truth_or_canon_authority",
    "dedicated_full_reader_core",
):
    expect(reader_structure.get(key), False, f"reader_core_rc2.{key}")

expect(limits.get("bounded_streaming_issue_completed"), 331, "bounded migration issue")
expect(limits.get("postgresql_inactive_import_issue_completed"), 332, "PostgreSQL import issue")
expect(limits.get("institution_scale_claim"), False, "institution-scale claim")
expect(limits.get("benchmark_is_production_slo"), False, "benchmark SLO claim")

expect(documentation.get("authoritative_language"), "English", "documentation authority")
expect(documentation.get("working_language"), "English", "documentation working language")
expect(documentation.get("language_model"), "english_primary_source_multilingual_product_surface", "language model")
expect(documentation.get("localized_readmes"), "all_supported_locales_full_visual_and_semantic_parity", "localized README model")
expect(documentation.get("localized_readme_source_checkpoint"), source_checkpoint, "README source checkpoint")
expect(documentation.get("supported_localized_readme_count"), 9, "localized README count")
expect(documentation.get("full_parity_current_locales"), expected_locales, "full-parity locale set")
expect(documentation.get("orientation_only_locales"), [], "orientation-only root locales")
expect(documentation.get("broader_document_translation"), "phased_by_language_or_document_family", "broader translation model")
expect(documentation.get("full_corpus_translation_required_in_single_pr"), False, "all-at-once translation requirement")

expect(grant.get("submitted"), True, "grant submitted")
expect(grant.get("under_review"), True, "grant under review")
expect(grant.get("awarded"), False, "grant awarded")
expect(grant.get("budget_changed"), False, "grant budget")

localized_files = {
    "ar": "README.ar.md", "de": "README.de.md", "es": "README.es.md",
    "fr": "README.fr.md", "hi": "README.hi.md", "it": "README.it.md",
    "ja": "README.ja.md", "ru": "README.ru.md", "zh-CN": "README.zh-CN.md",
}
actual = sorted(path.name for path in root.glob("README.*.md") if path.name != "README.md")
expect(actual, sorted(localized_files.values()), "supported root README files")

root_readmes = ["README.md", *localized_files.values()]
common_readme_markers = (
    runtime_commit,
    "2078 passed / 13 skipped / 0 failed",
    "9756",
    "active=false",
    "submitted / under review / not awarded",
    "Guardian",
    "TruthGate",
    "TrustSnapshot",
    "CanonicalView",
    "SQLite",
    "PostgreSQL",
    "HTTP /ask",
    "CLI ask",
    "MCP search",
    "docs/LOCALIZATION_POLICY.md",
    "docs/TRANSLATION_STATUS.md",
)
for relative in root_readmes:
    path = root / relative
    if not path.is_file():
        errors.append(f"missing README: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    if relative != "README.md" and f"localization-source: main@{source_checkpoint}" not in text:
        errors.append(f"{relative}: missing exact localization source checkpoint")
    for marker in common_readme_markers:
        if marker not in text:
            errors.append(f"{relative}: missing full README marker {marker!r}")
    if path.stat().st_size < 6000:
        errors.append(f"{relative}: full README is unexpectedly small ({path.stat().st_size} bytes)")
    if text.count("```text") + text.count("```bash") < 7:
        errors.append(f"{relative}: insufficient visual/code-block structure")
    if text.count("|") < 20:
        errors.append(f"{relative}: insufficient table structure")
    for level in ("L0", "L1", "L2", "L3"):
        if level not in text:
            errors.append(f"{relative}: missing memory level {level}")

ledger = (root / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
for relative in localized_files.values():
    if f"`{relative}`" not in ledger or "`CURRENT`" not in ledger:
        errors.append(f"translation ledger does not record current root README {relative}")

for locale, relative in localized_files.items():
    index_path = root / "docs" / locale / "README.md"
    if not index_path.is_file():
        errors.append(f"missing locale index: docs/{locale}/README.md")
        continue
    index = index_path.read_text(encoding="utf-8")
    for marker in (
        f"localization-index-source: main@{source_checkpoint}",
        "`CURRENT`",
        "`REFRESH_NEEDED`",
        "Localization policy",
        "Translation status",
    ):
        if marker not in index:
            errors.append(f"docs/{locale}/README.md: missing status marker {marker!r}")

required: dict[str, tuple[str, ...]] = {
    "AGENTS.md": ("English-first means", "full visual and semantic parity", "docs/TRANSLATION_STATUS.md"),
    "docs/LOCALIZATION_POLICY.md": ("all nine supported locales", "Broader documents are translated progressively", "REFRESH_NEEDED"),
    "docs/TRANSLATION_STATUS.md": ("Root README status", "D1 — entry and use documents", "D5 — extended reference documents"),
    "docs/DOCUMENTATION_MAP.md": ("CURRENT full-parity localized READMEs", "REFRESH_NEEDED translated document packs", "Inactive PostgreSQL import"),
    "docs/DOCUMENTATION_SYNC_PROTOCOL.md": ("Root README target", "Progressive document translation", "A permanent short-summary model is not acceptable"),
    "docs/ai/CURRENT_STATE.md": ("all nine supported", "REFRESH_NEEDED", "active=false", "reader_core_rc2_structural_map = true"),
    "docs/ai/README.md": ("all nine supported", "docs-only PR", "REFRESH_NEEDED"),
    "TEST_REPORT.md": (runtime_commit, "2078 passed / 13 skipped / 0 failed", "31256316532"),
    "docs/STATUS.md": (runtime_commit, "PostgreSQL 16", "active=false"),
    "docs/IMPLEMENTATION_STATUS.md": ("Inactive PostgreSQL/pgvector import", "#332", "reader_core_rc2_structural_map = true"),
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

current_surfaces = list(required) + ["docs/status/implementation-manifest.json", *root_readmes]
for relative in current_surfaces:
    text = (root / relative).read_text(encoding="utf-8")
    for stale in (
        "2059 passed / 12 skipped", "9361 statements",
        "localized README files are frozen snapshots",
        "Existing translated top-level README files are retained as frozen snapshots",
        "sole authoritative actively maintained GitHub documentation language",
    ):
        if stale in text:
            errors.append(f"{relative}: stale localization/status marker {stale!r}")
    for unsupported in (
        "Grant status: awarded", "Crystal is GDPR compliant",
        "PostgreSQL/pgvector is current runtime",
        "automatic backend switching is enabled", "zero hallucinations guaranteed",
    ):
        if unsupported in text:
            errors.append(f"{relative}: unsupported claim {unsupported!r}")

link_surfaces = sorted(set(current_surfaces) | {f"docs/{locale}/README.md" for locale in localized_files})
link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
for relative in link_surfaces:
    source = root / relative
    if not source.is_file():
        continue
    for raw_target in link_pattern.findall(source.read_text(encoding="utf-8")):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split(maxsplit=1)[0].split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        resolved = (source.parent / target).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{relative}: local link escapes repository: {raw_target!r}")
            continue
        if not resolved.exists():
            errors.append(f"{relative}: broken local link: {raw_target!r}")

if errors:
    print("Documentation status validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

print(
    "Documentation status is internally consistent: checkpoint=bbd816c, "
    "tests=2078/13, statements=9756, coverage=100.00%, CI=9, mutants=7/7, "
    "reader-rc1=minimal-skeleton, reader-rc2=structural-map, dedicated-reader=false, "
    "root-readmes=10-full, localized=9-current, broader-docs=phased-refresh"
)
PY