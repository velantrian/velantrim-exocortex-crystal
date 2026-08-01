#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
from __future__ import annotations

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
    path = root / relative
    if not path.is_file():
        errors.append(f"required active document is missing: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
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
    path = root / relative
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle in text:
            errors.append(f"{relative}: stale marker remains: {needle!r}")

# Validate relative Markdown links on the active authoritative reader surfaces.
# This deliberately checks file existence only; headings/anchors remain a human
# documentation concern. External, mailto and same-page anchor links are skipped.
active_link_surfaces = [
    "README.md",
    "README.ru.md",
    "TEST_REPORT.md",
    "docs/STATUS.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/DOCUMENTATION_MAP.md",
    "docs/QUICKSTART.md",
    "docs/ADR.md",
]
link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")

for relative in active_link_surfaces:
    source = root / relative
    if not source.is_file():
        errors.append(f"active link surface is missing: {relative}")
        continue
    text = source.read_text(encoding="utf-8")
    for raw_target in link_pattern.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        # Markdown optionally permits a quoted link title after whitespace.
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
    print("❌ Documentation status validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)

print(
    "✅ Documentation status is internally consistent: "
    f"checkpoint={checkpoint_short}, tests={english_metric}, "
    f"coverage={coverage}, jobs={job_count}, mutants={mutants}; "
    f"local links checked on {len(active_link_surfaces)} active surfaces"
)
PY
