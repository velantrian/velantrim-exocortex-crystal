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

checkpoint = manifest["verified_runtime_checkpoint"]
tests = manifest["tests"]
ci = manifest["ci"]
mutation = manifest["mutation_gate"]
boundaries = manifest["implemented_boundaries"]
documentation = manifest["documentation"]
grant = manifest["grant"]

jobs = ci.get("jobs", [])
if ci.get("job_count") != len(jobs):
    errors.append("ci.job_count does not equal len(ci.jobs)")
if len(jobs) != len(set(jobs)):
    errors.append("ci.jobs contains duplicates")
if "docs-status" not in jobs:
    errors.append("docs-status must be declared in ci.jobs")
if mutation.get("declared_mutants") != mutation.get("killed_mutants"):
    errors.append("all declared Ring Zero mutants must be killed")
if boundaries.get("truth_policy_runtime_bypass_present") is not False:
    errors.append("TruthPolicy runtime bypass must remain absent")
if boundaries.get("physical_l3_equals_strict_canon") is not False:
    errors.append("physical L3 must not be documented as strict Canon")
if boundaries.get("sqlite_storage_lifecycle") is not True:
    errors.append("verified SQLite storage lifecycle must be recorded")
if boundaries.get("cross_backend_migration_runtime") is not False:
    errors.append("manifest must not claim cross-backend migration runtime")
if boundaries.get("postgresql_pgvector_runtime") is not False:
    errors.append("manifest must not claim PostgreSQL/pgvector runtime")
if boundaries.get("automatic_backend_switching") is not False:
    errors.append("automatic backend switching must remain absent")
if documentation.get("authoritative_language") != "English":
    errors.append("English must be the active documentation authority")
if grant.get("awarded") is not False:
    errors.append("grant manifest must not claim an award")

english_metric = f'{tests["passed"]} passed / {tests["skipped"]} skipped'
coverage = f'{tests["coverage_percent"]:.2f}% coverage'
checkpoint_short = checkpoint["short"]
job_count = str(ci["job_count"])
mutants = f'{mutation["killed_mutants"]}/{mutation["declared_mutants"]}'

required: dict[str, list[str]] = {
    "README.md": [
        english_metric,
        checkpoint["commit"],
        f"{job_count} CI jobs",
        f"{mutants} declared mutants killed",
        "English is the authoritative",
        "Cross-backend migration is not yet runtime",
    ],
    "TEST_REPORT.md": [
        english_metric,
        checkpoint["commit"],
        coverage,
        f"{job_count} permanent CI jobs",
        "PR #325",
    ],
    "docs/STATUS.md": [
        english_metric,
        checkpoint_short,
        "9/9 permanent jobs successful",
        "English is the authoritative",
        "PostgreSQL + pgvector",
    ],
    "docs/IMPLEMENTATION_STATUS.md": [
        checkpoint_short,
        "SQLite backup/verify/restore lifecycle",
        "Cross-backend migration architecture",
        "PostgreSQL/pgvector institutional profile",
    ],
    "docs/ai/CURRENT_STATE.md": [
        checkpoint["commit"],
        "2019 passed",
        "English is the sole authoritative",
        "Approved next runtime slice",
    ],
    "docs/architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md": [
        "migration receipt     != evidence for a claim",
        "deterministic read-only logical export",
        "Automatic backend switching after data exists is forbidden",
    ],
    "docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md": [
        "PROPOSED / NOT RUNTIME",
        "no PostgreSQL driver or pgvector dependency",
        "SQLite remains the verified local-first baseline",
    ],
    "docs/adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md": [
        "Accepted architecture contract",
        "The first implementation slice is limited",
    ],
    "AGENTS.md": [
        "English is the sole authoritative actively",
        "Do not automatically update localized top-level README files",
    ],
    "docs/DOCUMENTATION_SYNC_PROTOCOL.md": [
        "Active language and localization policy",
        "dedicated final localization pass",
    ],
}

for relative, needles in required.items():
    path = root / relative
    if not path.is_file():
        errors.append(f"required English authority document is missing: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"{relative}: missing required status marker: {needle!r}")

english_surfaces = list(required) + [
    "docs/ADR.md",
    "docs/DOCUMENTATION_MAP.md",
    "docs/architecture/DURABLE_STORAGE_PROFILE.md",
    "docs/architecture/SQLITE_STORAGE_LIFECYCLE.md",
    "docs/ai/COMPONENT_MAP.md",
    "docs/ai/KNOWN_RISKS.md",
    "docs/ai/WORK_LOG.md",
]

# Historical logs may legitimately mention older checkpoints. Stale mutable evidence is
# forbidden only on current public/status surfaces.
current_status_surfaces = [
    "README.md",
    "TEST_REPORT.md",
    "docs/STATUS.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/status/implementation-manifest.json",
    "docs/ai/CURRENT_STATE.md",
]
stale_markers = (
    "1853 passed",
    "7236",
    "merged PR #302",
    "README.pt-BR.md",
)
for relative in current_status_surfaces:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    for stale in stale_markers:
        if stale in text:
            errors.append(f"{relative}: stale current-status marker remains: {stale!r}")

l3_source = (root / "core/l3_graph.py").read_text(encoding="utf-8")
for stale in ("Graph = Truth", "single source of canonical truth"):
    if stale in l3_source:
        errors.append(f"core/l3_graph.py: stale authority marker remains: {stale!r}")

# Validate relative Markdown links on reader-facing English surfaces. Work logs and risk
# history are intentionally excluded because historical references may be archived.
active_link_surfaces = [
    *required.keys(),
    "docs/ADR.md",
    "docs/DOCUMENTATION_MAP.md",
    "docs/architecture/DURABLE_STORAGE_PROFILE.md",
    "docs/architecture/SQLITE_STORAGE_LIFECYCLE.md",
    "docs/QUICKSTART.md",
    "docs/REVIEWER_GUIDE.md",
]
link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")

for relative in dict.fromkeys(active_link_surfaces):
    source = root / relative
    if not source.is_file():
        errors.append(f"active English link surface is missing: {relative}")
        continue
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

# Frozen translations must remain byte-for-byte identical until the dedicated final
# localization pass. Git blob IDs are content-addressed and include the byte length.
frozen = documentation.get("frozen_localized_readme_git_blobs")
if not isinstance(frozen, dict) or not frozen:
    errors.append("manifest must pin frozen localized README Git blob IDs")
    frozen = {}

localized = sorted(
    path.name
    for path in root.glob("README.*.md")
    if path.name != "README.md"
)
if set(localized) != set(frozen):
    errors.append(
        "localized README set differs from the frozen manifest: "
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
            f"{relative}: frozen snapshot changed: "
            f"expected={expected_blob}, actual={actual_blob}"
        )

if errors:
    print("Documentation status validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

print(
    "Documentation status is internally consistent: "
    f"checkpoint={checkpoint_short}, tests={english_metric}, "
    f"coverage={coverage}, jobs={job_count}, mutants={mutants}; "
    f"English authority surfaces={len(english_surfaces)}, "
    f"frozen localized snapshots={len(localized)}"
)
PY
