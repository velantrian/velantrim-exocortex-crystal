#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
from __future__ import annotations

import json
from pathlib import Path

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
grant = manifest["grant"]

jobs = ci.get("jobs", [])
if ci.get("job_count") != len(jobs):
    errors.append("ci.job_count does not equal len(ci.jobs)")
if len(jobs) != len(set(jobs)):
    errors.append("ci.jobs contains duplicates")
if "docs-status" not in jobs:
    errors.append("docs-status must be declared in ci.jobs")
if mutation.get("declared_mutants") != mutation.get("killed_mutants"):
    errors.append("all declared Ring Zero mutants must be killed in the verified baseline")
if boundaries.get("truth_policy_runtime_bypass_present") is not False:
    errors.append("TruthPolicy runtime bypass must remain absent")
if boundaries.get("physical_l3_equals_strict_canon") is not False:
    errors.append("physical L3 must not be documented as strict Canon")
if grant.get("awarded") is not False:
    errors.append("grant manifest must not claim an award")

english_metric = f'{tests["passed"]} passed / {tests["skipped"]} skipped'
russian_metric = f'{tests["passed"]} тестов пройдено / {tests["skipped"]} пропущено'
coverage = f'{tests["coverage_percent"]:.2f}% coverage'
checkpoint_short = checkpoint["short"]
job_count = str(ci["job_count"])
mutants = f'{mutation["killed_mutants"]}/{mutation["declared_mutants"]}'

required: dict[str, list[str]] = {
    "README.md": [english_metric, checkpoint_short, f"{job_count} CI jobs", f"{mutants} declared mutants killed"],
    "README.ru.md": [russian_metric, checkpoint_short, f"{job_count} CI jobs", f"{mutants} мутаций уничтожены"],
    "docs/STATUS.md": [english_metric, checkpoint_short, f"{job_count} permanent CI jobs", mutants],
    "TEST_REPORT.md": [english_metric, checkpoint["commit"], coverage, f"{job_count} permanent CI jobs", mutants],
    "docs/IMPLEMENTATION_STATUS.md": ["Immutable TrustSnapshot", "Ring Zero mutation gate", "Unified public read-only query boundary"],
}

for relative, needles in required.items():
    text = (root / relative).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"{relative}: missing required status marker: {needle!r}")

forbidden: dict[str, list[str]] = {
    "README.md": ["1713 passed", "cd6fd44", "all seven permanent jobs"],
    "README.ru.md": ["1713 тестов", "CLI-команды `ask` и `receipt` всё ещё", "поиск может\n  инициализировать"],
    "docs/STATUS.md": ["1713 passed", "cd6fd44", "CLI `ask` and `receipt` remain", "all seven permanent jobs"],
    "TEST_REPORT.md": ["1713 passed", "cd6fd44", "PR #265 — read-only HTTP query boundary"],
}

for relative, needles in forbidden.items():
    text = (root / relative).read_text(encoding="utf-8")
    for needle in needles:
        if needle in text:
            errors.append(f"{relative}: stale marker remains: {needle!r}")

if errors:
    print("❌ Documentation status validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

print(
    "✅ Documentation status is internally consistent: "
    f"checkpoint={checkpoint_short}, tests={english_metric}, "
    f"coverage={coverage}, jobs={job_count}, mutants={mutants}"
)
PY
