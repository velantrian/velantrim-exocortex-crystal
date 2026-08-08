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
documentation = manifest.get("documentation", {})
grant = manifest.get("grant", {})
limits = manifest.get("storage_resource_limits", {})

expected_commit = "bbd816c09dd39a02e6de6c1014438490572f40f6"
expected_head = "d7af7c80722274f9217bc5545d150f92e9363f37"
expected_ci = 31256316536
expected_integration_ci = 31256316532
expected_jobs = [
    "code-quality",
    "test (3.11)",
    "test (3.12)",
    "jsonl-integrity",
    "eval-gate",
    "security",
    "docker-build",
    "Ring Zero mutation gate",
    "docs-status",
]

expect(manifest.get("schema_version"), 1, "manifest schema_version")
expect(checkpoint.get("commit"), expected_commit, "runtime checkpoint")
expect(checkpoint.get("validated_head"), expected_head, "validated runtime head")
expect(checkpoint.get("pull_request"), 337, "runtime checkpoint PR")
expect(checkpoint.get("ci_run"), expected_ci, "runtime exact-head CI")
expect(tests.get("python_versions"), ["3.11", "3.12"], "tested Python versions")
expect(tests.get("passed"), 2078, "tests.passed")
expect(tests.get("skipped"), 13, "tests.skipped")
expect(tests.get("failed"), 0, "tests.failed")
expect(tests.get("measured_statements"), 9756, "tests.measured_statements")
expect(tests.get("coverage_percent"), 100.0, "tests.coverage_percent")
expect(ci.get("job_count"), 9, "CI job count")
expect(ci.get("jobs"), expected_jobs, "CI job list")
expect(ci.get("all_successful"), True, "CI all_successful")
expect(integration.get("ci_run"), expected_integration_ci, "PostgreSQL integration CI")
expect(integration.get("job_count"), 1, "PostgreSQL integration job count")
expect(integration.get("all_successful"), True, "PostgreSQL integration result")
expect(integration.get("target_active"), False, "PostgreSQL target active state")
expect(integration.get("ann_indexes_present"), False, "PostgreSQL ANN index state")
expect(mutation.get("declared_mutants"), 7, "declared Ring Zero mutants")
expect(mutation.get("killed_mutants"), 7, "killed Ring Zero mutants")

required_true = (
    "public_query_surfaces_read_only",
    "explicit_contradiction_dispositions",
    "scoped_curator_authorization",
    "bounded_legacy_retrieval",
    "durable_l3_profile_lock",
    "sqlite_storage_lifecycle",
    "sqlite_logical_export_verification",
    "bounded_streaming_logical_migration",
    "postgresql_optional_driver_lazy_loaded",
    "postgresql_inactive_import",
    "postgresql_exact_state_equivalence",
)
required_false = (
    "truth_policy_runtime_bypass_present",
    "physical_l3_equals_strict_canon",
    "postgresql_target_active",
    "postgresql_normal_runtime_adapter",
    "cross_backend_migration_runtime",
    "postgresql_pgvector_runtime",
    "automatic_backend_switching",
    "distributed_curator_coordination",
    "production_idp_multitenancy",
    "dedicated_reader_core",
)
for key in required_true:
    expect(boundaries.get(key), True, f"implemented_boundaries.{key}")
for key in required_false:
    expect(boundaries.get(key), False, f"implemented_boundaries.{key}")

expect(
    boundaries.get("sqlite_logical_export_resource_contract"),
    "bounded-streaming-local-first",
    "SQLite migration resource contract",
)
expect(limits.get("bounded_streaming_issue_completed"), 331, "bounded migration issue")
expect(limits.get("postgresql_inactive_import_issue_completed"), 332, "inactive import issue")
expect(limits.get("institution_scale_claim"), False, "institution-scale claim")
expect(limits.get("benchmark_is_production_slo"), False, "benchmark production-SLO claim")

# English remains the conflict-resolving source; multilingual presentation is a maintained
# phased product surface rather than a frozen summary layer.
expect(documentation.get("authoritative_language"), "English", "documentation authority")
expect(documentation.get("working_language"), "English", "documentation working language")
expect(
    documentation.get("language_model"),
    "english_primary_source_multilingual_product_surface",
    "documentation language model",
)
expect(
    documentation.get("localized_readmes"),
    "phased_full_visual_and_semantic_parity",
    "localized README model",
)
expect(
    documentation.get("translation_status_ledger"),
    "docs/TRANSLATION_STATUS.md",
    "translation status ledger",
)
expect(
    documentation.get("localization_policy"),
    "docs/LOCALIZATION_POLICY.md",
    "localization policy path",
)
expect(documentation.get("supported_localized_readme_count"), 9, "localized README count")
expect(documentation.get("full_parity_current_locales"), ["ru"], "current full-parity locales")
expect(
    documentation.get("orientation_only_locales"),
    ["ar", "de", "es", "fr", "hi", "it", "ja", "zh-CN"],
    "temporary orientation locales",
)
expect(
    documentation.get("full_corpus_translation_required_in_single_pr"),
    False,
    "all-at-once translation requirement",
)

expect(grant.get("submitted"), True, "grant submitted")
expect(grant.get("under_review"), True, "grant under review")
expect(grant.get("awarded"), False, "grant awarded")
expect(grant.get("budget_changed"), False, "grant budget changed")

required: dict[str, list[str]] = {
    "README.md": [
        expected_commit,
        "2078 passed / 13 skipped / 0 failed",
        "9756 statements / 100.00% line coverage",
        "merged PR #337",
        "active=false",
        "submitted / under review / not awarded",
        "Mind map",
        "ASCII architecture",
        "Module tree",
        "docs/TRANSLATION_STATUS.md",
    ],
    "README.ru.md": [
        "<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->",
        "<!-- localization-status: CURRENT -->",
        "2078 passed / 13 skipped / 0 failed",
        "9756 statements / 100.00% line coverage",
        "active=false",
        "Mindmap",
        "ASCII-архитектура",
        "Дерево модулей",
        "Успешный импорт",
        "submitted / under review / not awarded",
    ],
    "TEST_REPORT.md": [
        expected_commit,
        "2078 passed / 13 skipped / 0 failed",
        "9756",
        "9/9 successful",
        "31256316532",
        "PR #337",
    ],
    "docs/STATUS.md": [
        expected_commit,
        "2078 passed / 13 skipped / 0 failed",
        "PostgreSQL 16",
        "active=false",
        "No award or budget change",
    ],
    "docs/IMPLEMENTATION_STATUS.md": [
        "bbd816c",
        "Inactive PostgreSQL/pgvector import",
        "Exact target-state equivalence",
        "#332",
    ],
    "docs/ai/CURRENT_STATE.md": [
        expected_commit,
        "2078 passed / 13 skipped / 0 failed",
        "Issue #332",
        "English is the primary working",
        "ORIENTATION_ONLY",
        "REFRESH_NEEDED",
    ],
    "docs/ai/README.md": [
        "English-first means source-first, not",
        "full visual and semantic coverage",
        "ORIENTATION_ONLY",
        "docs-only PR",
    ],
    "docs/ai/KNOWN_RISKS.md": [
        expected_commit,
        "PR #334",
        "PR #337",
        "GDPR-oriented controls",
        "test-only",
    ],
    "docs/ai/WORK_LOG.md": [
        expected_commit,
        "31256316532",
        "PR #334",
        "31214414769",
        "GITHUB_AND_NOTION",
    ],
    "docs/ai/COMPONENT_MAP.md": [
        "core/postgresql_migration.py",
        "active=false",
        "Automatic SQLite/PostgreSQL switching remains forbidden",
    ],
    "docs/GRANT_NLNET_SCOPE.md": [
        expected_commit,
        "submitted / under review / not awarded",
        "#332",
        "cannot be budgeted again",
    ],
    "docs/grants/baseline-funded-delta-matrix.md": [
        expected_commit,
        "M1",
        "M9",
        "PR #337",
        "no award/budget change",
    ],
    "docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md": [
        "PARTIALLY IMPLEMENTED",
        expected_commit,
        "active=false",
        "not an active Crystal runtime backend",
    ],
    "ROADMAP.md": [expected_commit, "issues #331 and #332", "No grant award"],
    "SECURITY.md": [
        expected_commit,
        "not a security, legal or GDPR certification",
        "test-only",
        "No automatic switching",
    ],
    "AGENTS.md": [
        "English-first means",
        "full visual and semantic parity",
        "ORIENTATION_ONLY",
        "docs/TRANSLATION_STATUS.md",
        "GitHub completeness invariant",
    ],
    "docs/DOCUMENTATION_MAP.md": [
        "English-first means source-first, not English-only",
        "CURRENT full-parity localized READMEs",
        "ORIENTATION_ONLY / REFRESH_NEEDED",
        "Inactive PostgreSQL import",
    ],
    "docs/DOCUMENTATION_SYNC_PROTOCOL.md": [
        "English-first means source-first, not English-only",
        "Root README target",
        "Progressive document translation",
        "A permanent short-summary model is not acceptable",
    ],
    "docs/LOCALIZATION_POLICY.md": [
        "English-first means **source-first**, not English-only.",
        "full public presentations",
        "Phased translation instead of an all-at-once gate",
        "ORIENTATION_ONLY",
        "Human or language-model review",
    ],
    "docs/TRANSLATION_STATUS.md": [
        "README.ru.md",
        "IN_PROGRESS",
        "ORIENTATION_ONLY",
        "T2 — German entry surface",
        "T6 — reviewer, architecture, safety and grant documents",
    ],
}

for relative, needles in required.items():
    path = root / relative
    if not path.is_file():
        errors.append(f"required document missing: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"{relative}: missing current marker {needle!r}")

# Full public presentation uses a minimum floor, never a maximum-size restriction.
for relative, minimum in (("README.md", 12000), ("README.ru.md", 12000)):
    size = (root / relative).stat().st_size
    if size < minimum:
        errors.append(f"{relative}: full README is unexpectedly small ({size} < {minimum} bytes)")

supported_locales = {
    "ar": "README.ar.md",
    "de": "README.de.md",
    "es": "README.es.md",
    "fr": "README.fr.md",
    "hi": "README.hi.md",
    "it": "README.it.md",
    "ja": "README.ja.md",
    "ru": "README.ru.md",
    "zh-CN": "README.zh-CN.md",
}
localized = sorted(path.name for path in root.glob("README.*.md") if path.name != "README.md")
if set(localized) != set(supported_locales.values()):
    errors.append("supported root README locale set differs from localization policy")

status_text = (root / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
for locale, relative in supported_locales.items():
    if not (root / relative).is_file():
        errors.append(f"supported localized README missing: {relative}")
    index_path = root / "docs" / locale / "README.md"
    if not index_path.is_file():
        errors.append(f"locale documentation index missing: docs/{locale}/README.md")
    if f"`{relative}`" not in status_text:
        errors.append(f"translation ledger does not list {relative}")

orientation_readmes = sorted(set(supported_locales.values()) - {"README.ru.md"})
for relative in orientation_readmes:
    text = (root / relative).read_text(encoding="utf-8")
    for needle in (
        "<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->",
        "active=false",
        "README.md",
    ):
        if needle not in text:
            errors.append(f"{relative}: temporary orientation file missing {needle!r}")

for locale, relative in supported_locales.items():
    index = (root / "docs" / locale / "README.md").read_text(encoding="utf-8")
    expected_state = "CURRENT" if locale == "ru" else "ORIENTATION_ONLY"
    for needle in (
        "localization-index-source: main@e521440e9bb188d88475f17dd5bcdd161b314605",
        expected_state,
        "REFRESH_NEEDED",
        "Translation status",
    ):
        if needle not in index:
            errors.append(f"docs/{locale}/README.md: missing phased status marker {needle!r}")

current_surfaces = [
    "README.md",
    "README.ru.md",
    "TEST_REPORT.md",
    "docs/STATUS.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/status/implementation-manifest.json",
    "docs/ai/CURRENT_STATE.md",
    "docs/ai/README.md",
    "docs/ai/KNOWN_RISKS.md",
    "docs/DOCUMENTATION_MAP.md",
    "docs/DOCUMENTATION_SYNC_PROTOCOL.md",
    "docs/LOCALIZATION_POLICY.md",
    "docs/TRANSLATION_STATUS.md",
    "docs/GRANT_NLNET_SCOPE.md",
    "docs/grants/baseline-funded-delta-matrix.md",
    "docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md",
    "ROADMAP.md",
    "SECURITY.md",
]
stale_markers = (
    "2059 passed / 12 skipped",
    "9361 statements",
    "f03e24c85922d0bb46d6d9dfee98338972135908",
    "31224184351",
    "PostgreSQL/pgvector is proposed, not current runtime",
    "inactive import and exact target equivalence (#332)",
    "localized README files are frozen snapshots",
    "Existing translated top-level README files are retained as frozen snapshots",
)
for relative in current_surfaces:
    text = (root / relative).read_text(encoding="utf-8")
    for stale in stale_markers:
        if stale in text:
            errors.append(f"{relative}: stale current-status marker {stale!r}")

unsupported_claims = (
    "Grant status: awarded",
    "Crystal is GDPR compliant",
    "Crystal is GDPR certified",
    "PostgreSQL/pgvector is current runtime",
    "automatic backend switching is enabled",
    "zero hallucinations guaranteed",
)
for relative in current_surfaces:
    text = (root / relative).read_text(encoding="utf-8")
    for claim in unsupported_claims:
        if claim in text:
            errors.append(f"{relative}: unsupported positive claim {claim!r}")

link_surfaces = sorted(
    set(required)
    | set(supported_locales.values())
    | {f"docs/{locale}/README.md" for locale in supported_locales}
)
link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
for relative in link_surfaces:
    source = root / relative
    if not source.is_file():
        continue
    text = source.read_text(encoding="utf-8")
    for raw_target in link_pattern.findall(text):
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
    "Documentation status is internally consistent: "
    "checkpoint=bbd816c, tests=2078/13, statements=9756, coverage=100.00%, "
    "permanent-jobs=9, postgresql-integration=1, mutants=7/7, "
    "grant=submitted-under-review, readme-parity=en+ru, "
    f"phased-orientation={len(orientation_readmes)}"
)
PY
