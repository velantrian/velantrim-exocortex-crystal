#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

root = Path.cwd()
manifest = json.loads((root / "docs/status/implementation-manifest.json").read_text())
errors: list[str] = []

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
    "code-quality", "test (3.11)", "test (3.12)", "jsonl-integrity",
    "eval-gate", "security", "docker-build", "Ring Zero mutation gate",
    "docs-status",
]

if manifest.get("schema_version") != 1:
    errors.append("manifest schema_version must be 1")
if checkpoint.get("commit") != expected_commit:
    errors.append("manifest runtime checkpoint must match merged PR #337")
if checkpoint.get("validated_head") != expected_head:
    errors.append("manifest validated head must match PR #337 exact-head evidence")
if checkpoint.get("pull_request") != 337:
    errors.append("manifest pull request must be 337")
if checkpoint.get("ci_run") != expected_ci:
    errors.append("manifest CI run must match PR #337 exact-head evidence")

expected_tests = {
    "passed": 2078,
    "skipped": 13,
    "failed": 0,
    "measured_statements": 9756,
    "coverage_percent": 100.0,
}
for key, expected in expected_tests.items():
    if tests.get(key) != expected:
        errors.append(f"tests.{key} must equal {expected!r}")
if tests.get("python_versions") != ["3.11", "3.12"]:
    errors.append("tests.python_versions must be Python 3.11 and 3.12")

if ci.get("job_count") != 9 or ci.get("jobs") != expected_jobs:
    errors.append("permanent CI manifest must list the nine jobs in order")
if ci.get("all_successful") is not True:
    errors.append("permanent exact-head CI must be successful")
if integration.get("ci_run") != expected_integration_ci:
    errors.append("PostgreSQL integration CI must match exact evidence")
if integration.get("job_count") != 1 or integration.get("all_successful") is not True:
    errors.append("PostgreSQL integration must record one successful job")
if integration.get("target_active") is not False:
    errors.append("PostgreSQL integration target must remain inactive")
if integration.get("ann_indexes_present") is not False:
    errors.append("inactive import must not record ANN indexes")
if mutation.get("declared_mutants") != 7 or mutation.get("killed_mutants") != 7:
    errors.append("Ring Zero evidence must remain 7/7")

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
    if boundaries.get(key) is not True:
        errors.append(f"implemented_boundaries.{key} must be true")
for key in required_false:
    if boundaries.get(key) is not False:
        errors.append(f"implemented_boundaries.{key} must be false")

if boundaries.get("sqlite_logical_export_resource_contract") != "bounded-streaming-local-first":
    errors.append("SQLite migration must remain bounded-streaming-local-first")
if limits.get("bounded_streaming_issue_completed") != 331:
    errors.append("bounded streaming completion must remain issue #331")
if limits.get("postgresql_inactive_import_issue_completed") != 332:
    errors.append("inactive PostgreSQL completion must be issue #332")
if limits.get("institution_scale_claim") is not False:
    errors.append("manifest must not claim institution-scale operation")
if limits.get("benchmark_is_production_slo") is not False:
    errors.append("resource benchmark must not be a production SLO")

if documentation.get("authoritative_language") != "English":
    errors.append("English must remain documentation authority")
if grant.get("submitted") is not True or grant.get("under_review") is not True:
    errors.append("grant must remain submitted and under review")
if grant.get("awarded") is not False or grant.get("budget_changed") is not False:
    errors.append("grant must not claim award or budget change")

required: dict[str, list[str]] = {
    "README.md": [expected_commit, "2078 passed / 13 skipped", "PR #337",
                  "Issue #332", "inactive", "submitted and under review"],
    "TEST_REPORT.md": [expected_commit, "2078 passed / 13 skipped / 0 failed",
                       "9756", "9/9 successful", "31256316532", "PR #337"],
    "docs/STATUS.md": [expected_commit, "2078 passed / 13 skipped / 0 failed",
                       "PostgreSQL 16", "active=false", "No award or budget change"],
    "docs/IMPLEMENTATION_STATUS.md": ["bbd816c", "Inactive PostgreSQL/pgvector import",
                                      "Exact target-state equivalence", "#332"],
    "docs/ai/CURRENT_STATE.md": [expected_commit, "2078 passed / 13 skipped / 0 failed",
                                 "Issue #332", "English is the sole authoritative"],
    "docs/ai/KNOWN_RISKS.md": [expected_commit, "PR #334", "PR #337",
                               "GDPR-oriented controls", "test-only"],
    "docs/ai/WORK_LOG.md": [expected_commit, "31256316532", "PR #334",
                            "31214414769", "GITHUB_AND_NOTION"],
    "docs/ai/COMPONENT_MAP.md": ["core/postgresql_migration.py", "active=false",
                                 "Automatic SQLite/PostgreSQL switching remains forbidden"],
    "docs/GRANT_NLNET_SCOPE.md": [expected_commit, "submitted / under review / not awarded",
                                  "#332", "cannot be budgeted again"],
    "docs/grants/baseline-funded-delta-matrix.md": [expected_commit, "M1", "M9",
                                                     "PR #337", "no award/budget change"],
    "docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md": [
        "PARTIALLY IMPLEMENTED", expected_commit, "active=false", "not an active Crystal runtime backend"
    ],
    "ROADMAP.md": [expected_commit, "issues #331 and #332", "No grant award"],
    "SECURITY.md": [expected_commit, "not a security, legal or GDPR certification",
                    "test-only", "No automatic switching"],
    "AGENTS.md": ["English is the sole authoritative actively",
                  "Do not automatically update localized top-level README files",
                  "GitHub completeness invariant"],
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

current_surfaces = [
    "README.md", "TEST_REPORT.md", "docs/STATUS.md",
    "docs/IMPLEMENTATION_STATUS.md", "docs/status/implementation-manifest.json",
    "docs/ai/CURRENT_STATE.md", "docs/ai/KNOWN_RISKS.md",
    "docs/GRANT_NLNET_SCOPE.md", "docs/grants/baseline-funded-delta-matrix.md",
    "docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md", "ROADMAP.md", "SECURITY.md",
]
stale_markers = (
    "2059 passed / 12 skipped", "9361 statements",
    "f03e24c85922d0bb46d6d9dfee98338972135908", "31224184351",
    "PostgreSQL/pgvector is proposed, not current runtime",
    "inactive import and exact target equivalence (#332)",
)
for relative in current_surfaces:
    text = (root / relative).read_text(encoding="utf-8")
    for stale in stale_markers:
        if stale in text:
            errors.append(f"{relative}: stale current-status marker {stale!r}")

unsupported_claims = (
    "Grant status: awarded", "Crystal is GDPR compliant", "Crystal is GDPR certified",
    "PostgreSQL/pgvector is current runtime", "automatic backend switching is enabled",
    "zero hallucinations guaranteed",
)
for relative in current_surfaces:
    text = (root / relative).read_text(encoding="utf-8")
    for claim in unsupported_claims:
        if claim in text:
            errors.append(f"{relative}: unsupported positive claim {claim!r}")

frozen = documentation.get("frozen_localized_readme_git_blobs")
if not isinstance(frozen, dict) or not frozen:
    errors.append("manifest must pin frozen localized README Git blob IDs")
    frozen = {}
localized = sorted(path.name for path in root.glob("README.*.md") if path.name != "README.md")
if set(localized) != set(frozen):
    errors.append("localized README set differs from manifest")
for relative, expected_blob in sorted(frozen.items()):
    path = root / relative
    if not path.is_file():
        errors.append(f"frozen localized README missing: {relative}")
        continue
    content = path.read_bytes()
    actual = hashlib.sha1(f"blob {len(content)}\0".encode() + content, usedforsecurity=False).hexdigest()
    if actual != expected_blob:
        errors.append(f"{relative}: frozen snapshot changed")

link_surfaces = list(required)
link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
for relative in link_surfaces:
    source = root / relative
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
    f"grant=submitted-under-review, frozen-localized={len(localized)}"
)
PY