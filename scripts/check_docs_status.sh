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
manifest_path = root / "docs/status/implementation-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
errors: list[str] = []

if manifest.get("schema_version") != 1:
    errors.append("manifest schema_version must be 1")

checkpoint = manifest.get("verified_runtime_checkpoint", {})
tests = manifest.get("tests", {})
ci = manifest.get("ci", {})
mutation = manifest.get("mutation_gate", {})
boundaries = manifest.get("implemented_boundaries", {})
documentation = manifest.get("documentation", {})
grant = manifest.get("grant", {})
limits = manifest.get("storage_resource_limits", {})

expected_commit = "c612c1f7de067b05ed7d01ad82d47a7bc39af23a"
expected_head = "e70c31bf517039f0dd3f77f7bc4b6d3f03936736"
expected_ci = 31213056560
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

if checkpoint.get("commit") != expected_commit:
    errors.append("manifest runtime checkpoint does not match merged PR #330")
if checkpoint.get("validated_head") != expected_head:
    errors.append("manifest validated head does not match PR #330 evidence")
if checkpoint.get("pull_request") != 330:
    errors.append("manifest pull request must be 330")
if checkpoint.get("ci_run") != expected_ci:
    errors.append("manifest CI run does not match PR #330 exact-head evidence")

expected_tests = {
    "passed": 2047,
    "skipped": 12,
    "failed": 0,
    "measured_statements": 9219,
    "coverage_percent": 100.0,
}
for key, expected in expected_tests.items():
    if tests.get(key) != expected:
        errors.append(f"tests.{key} must equal {expected!r}")
if tests.get("python_versions") != ["3.11", "3.12"]:
    errors.append("tests.python_versions must be exactly Python 3.11 and 3.12")

if ci.get("job_count") != len(expected_jobs):
    errors.append("ci.job_count must be 9")
if ci.get("jobs") != expected_jobs:
    errors.append("ci.jobs must match the nine permanent workflow jobs in order")
if ci.get("all_successful") is not True:
    errors.append("verified runtime CI must be recorded as successful")
if mutation.get("declared_mutants") != 7 or mutation.get("killed_mutants") != 7:
    errors.append("Ring Zero mutation evidence must remain 7/7")

required_false = (
    "truth_policy_runtime_bypass_present",
    "physical_l3_equals_strict_canon",
    "cross_backend_migration_runtime",
    "postgresql_pgvector_runtime",
    "automatic_backend_switching",
    "distributed_curator_coordination",
    "production_idp_multitenancy",
    "dedicated_reader_core",
)
for key in required_false:
    if boundaries.get(key) is not False:
        errors.append(f"implemented_boundaries.{key} must be false")

required_true = (
    "public_query_surfaces_read_only",
    "explicit_contradiction_dispositions",
    "scoped_curator_authorization",
    "bounded_legacy_retrieval",
    "durable_l3_profile_lock",
    "sqlite_storage_lifecycle",
    "sqlite_logical_export_verification",
)
for key in required_true:
    if boundaries.get(key) is not True:
        errors.append(f"implemented_boundaries.{key} must be true")

if boundaries.get("sqlite_logical_export_resource_contract") != "bounded-local-first":
    errors.append("logical export must remain documented as bounded-local-first")
if limits.get("institution_scale_claim") is not False:
    errors.append("manifest must not claim institution-scale migration")
if limits.get("streaming_follow_up_issue") != 331:
    errors.append("streaming migration follow-up must remain issue #331")
if limits.get("postgresql_follow_up_issue") != 332:
    errors.append("PostgreSQL follow-up must remain issue #332")

if documentation.get("authoritative_language") != "English":
    errors.append("English must remain the active documentation authority")
if grant.get("submitted") is not True or grant.get("under_review") is not True:
    errors.append("grant must remain recorded as submitted and under review")
if grant.get("awarded") is not False or grant.get("budget_changed") is not False:
    errors.append("grant manifest must not claim an award or budget change")

required: dict[str, list[str]] = {
    "README.md": [
        "2047 passed / 12 skipped",
        expected_commit,
        "9 CI jobs",
        "7/7 declared mutants killed",
        "English is the authoritative",
        "Issue #331",
        "Issue #332",
        "submitted and under review",
    ],
    "TEST_REPORT.md": [
        expected_commit,
        "2047 passed / 12 skipped / 0 failed",
        "100.00%",
        "9/9 successful",
        "PR #330",
        "#331",
        "#332",
    ],
    "docs/STATUS.md": [
        expected_commit,
        "2047 passed / 12 skipped / 0 failed",
        "9/9",
        "PostgreSQL/pgvector",
        "#331",
        "#332",
        "No award or budget change",
    ],
    "docs/IMPLEMENTATION_STATUS.md": [
        "c612c1f",
        "SQLite logical export/verify",
        "#331",
        "#332",
        "PostgreSQL/pgvector institutional profile",
    ],
    "docs/ai/CURRENT_STATE.md": [
        expected_commit,
        "2047 passed / 12 skipped / 0 failed",
        "English is the sole authoritative",
        "#331",
        "#332",
        "no award or budget change",
    ],
    "docs/ai/KNOWN_RISKS.md": [
        expected_commit,
        "#331",
        "#332",
        "PR #334",
        "GDPR-oriented controls",
    ],
    "docs/ai/WORK_LOG.md": [
        expected_commit,
        "PR #334",
        "31214414769",
        "GITHUB_AND_NOTION",
        "#331",
        "#332",
    ],
    "docs/GRANT_NLNET_SCOPE.md": [
        expected_commit,
        "submitted / under review / not awarded",
        "#331",
        "#332",
    ],
    "docs/grants/baseline-funded-delta-matrix.md": [
        expected_commit,
        "M1",
        "M9",
        "#331",
        "#332",
        "no award/budget change",
    ],
    "ROADMAP.md": [
        expected_commit,
        "#331",
        "#332",
        "PostgreSQL",
        "No grant award",
    ],
    "SECURITY.md": [
        expected_commit,
        "not a security, legal or GDPR certification",
        "#331",
        "PostgreSQL/pgvector is proposed, not current runtime",
        "automatic switching",
    ],
    "AGENTS.md": [
        "English is the sole authoritative actively",
        "Do not automatically update localized top-level README files",
        "GitHub completeness invariant",
    ],
}

for relative, needles in required.items():
    path = root / relative
    if not path.is_file():
        errors.append(f"required current document is missing: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"{relative}: missing required current marker: {needle!r}")

current_status_surfaces = [
    "README.md",
    "TEST_REPORT.md",
    "docs/STATUS.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/status/implementation-manifest.json",
    "docs/ai/CURRENT_STATE.md",
    "docs/ai/KNOWN_RISKS.md",
    "docs/GRANT_NLNET_SCOPE.md",
    "docs/grants/baseline-funded-delta-matrix.md",
    "ROADMAP.md",
    "SECURITY.md",
]
stale_markers = (
    "2019 passed / 12 skipped",
    "b0df17a06d552ad2543b6d6e5efe8cd99877cfc0",
    "31182471502",
    "PR #334 merged",
    "issue #333 is closed",
    "AUTO-MERGE ARMED",
)
for relative in current_status_surfaces:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    for stale in stale_markers:
        if stale in text:
            errors.append(f"{relative}: stale current-status marker remains: {stale!r}")

unsupported_positive_claims = (
    "Grant status: awarded",
    "Crystal is GDPR compliant",
    "Crystal is GDPR certified",
    "PostgreSQL/pgvector is current runtime",
    "automatic backend switching is enabled",
    "zero hallucinations guaranteed",
)
claim_surfaces = [
    "README.md",
    "docs/STATUS.md",
    "docs/GRANT_NLNET_SCOPE.md",
    "docs/grants/baseline-funded-delta-matrix.md",
    "ROADMAP.md",
    "SECURITY.md",
]
for relative in claim_surfaces:
    text = (root / relative).read_text(encoding="utf-8")
    for claim in unsupported_positive_claims:
        if claim in text:
            errors.append(f"{relative}: unsupported positive claim: {claim!r}")

# Frozen localized README snapshots must remain byte-for-byte identical. Git blob IDs are
# content-addressed over the exact bytes and length.
frozen = documentation.get("frozen_localized_readme_git_blobs")
if not isinstance(frozen, dict) or not frozen:
    errors.append("manifest must pin frozen localized README Git blob IDs")
    frozen = {}

localized = sorted(path.name for path in root.glob("README.*.md") if path.name != "README.md")
if set(localized) != set(frozen):
    errors.append(
        "localized README set differs from manifest: "
        f"files={localized!r}, manifest={sorted(frozen)!r}"
    )
for relative, expected_blob in sorted(frozen.items()):
    path = root / relative
    if not path.is_file():
        errors.append(f"frozen localized README is missing: {relative}")
        continue
    content = path.read_bytes()
    actual_blob = hashlib.sha1(
        f"blob {len(content)}\0".encode("ascii") + content,
        usedforsecurity=False,
    ).hexdigest()
    if actual_blob != expected_blob:
        errors.append(
            f"{relative}: frozen snapshot changed: expected={expected_blob}, actual={actual_blob}"
        )

# Validate relative Markdown links on active reader-facing surfaces.
active_link_surfaces = [
    "README.md",
    "TEST_REPORT.md",
    "docs/STATUS.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/ai/CURRENT_STATE.md",
    "docs/ai/KNOWN_RISKS.md",
    "docs/GRANT_NLNET_SCOPE.md",
    "docs/grants/baseline-funded-delta-matrix.md",
    "ROADMAP.md",
    "SECURITY.md",
    "AGENTS.md",
]
link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
for relative in active_link_surfaces:
    source = root / relative
    text = source.read_text(encoding="utf-8")
    for raw_target in link_pattern.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = target.split(maxsplit=1)[0]
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
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
    f"checkpoint={checkpoint.get('short')}, tests=2047/12, statements=9219, "
    "coverage=100.00%, jobs=9, mutants=7/7, grant=submitted-under-review, "
    f"frozen localized snapshots={len(localized)}"
)
PY
