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
if boundaries.get("topic_facets_authoritative") is not False:
    errors.append("topic facets must remain non-authoritative")
if boundaries.get("distributed_decision_lease_adapter") is not False:
    errors.append("manifest must not claim a bundled distributed lease adapter")
if grant.get("awarded") is not False:
    errors.append("grant manifest must not claim an award")

english_metric = f'{tests["passed"]} passed / {tests["skipped"]} skipped'
russian_metric = f'{tests["passed"]} тестов пройдено / {tests["skipped"]} пропущено'
coverage = f'{tests["coverage_percent"]:.2f}% coverage'
checkpoint_short = checkpoint["short"]
job_count = str(ci["job_count"])
mutants = f'{mutation["killed_mutants"]}/{mutation["declared_mutants"]}'

locale_markers: dict[str, list[str]] = {
    "README.md": [english_metric, f"{job_count} CI jobs", f"{mutants} declared mutants killed"],
    "README.de.md": [f'{tests["passed"]} bestanden / {tests["skipped"]} übersprungen', f"{job_count} CI-Jobs", f"{mutants} deklarierte Mutanten erkannt"],
    "README.fr.md": [f'{tests["passed"]} tests réussis / {tests["skipped"]} ignorés', f"{job_count} tâches CI", f"{mutants} mutants déclarés éliminés"],
    "README.es.md": [f'{tests["passed"]} pruebas superadas / {tests["skipped"]} omitidas', f"{job_count} tareas de CI", f"{mutants} mutantes declarados eliminados"],
    "README.it.md": [f'{tests["passed"]} test superati / {tests["skipped"]} ignorati', f"{job_count} job CI", f"{mutants} mutanti dichiarati eliminati"],
    "README.ru.md": [russian_metric, f"{job_count} CI jobs", f"{mutants} мутаций уничтожены"],
    "README.zh-CN.md": [f'{tests["passed"]} 项测试通过 / {tests["skipped"]} 项跳过', f"{job_count} 个 CI 任务", f"{mutants} 个声明的变异体被检出"],
    "README.ar.md": [f'نجح {tests["passed"]} اختباراً / تم تجاوز {tests["skipped"]}', f"{job_count} مهام CI", f"تم كشف {mutants} من الطفرات المعلنة"],
    "README.ja.md": [f'{tests["passed"]} 件成功 / {tests["skipped"]} 件スキップ', f"CI {job_count} ジョブ", f"宣言済み変異 {mutants} を検出"],
    "README.hi.md": [f'{tests["passed"]} परीक्षण सफल / {tests["skipped"]} छोड़े गए', f"{job_count} CI कार्य", f"घोषित {mutants} म्यूटेंट पकड़े गए"],
}

shared_readme_markers = [
    checkpoint_short,
    "core.query_pipeline",
    "core.topic_facets",
    "core.curator_auth",
    "CuratorLeaseRegistry",
    "TrustSnapshot",
    "TopicFacet",
    "COEXIST",
    "CONTEXTUALIZE",
    "SUPERSEDE",
]

for relative, localized in locale_markers.items():
    path = root / relative
    if not path.is_file():
        errors.append(f"localized README is missing: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in localized + shared_readme_markers:
        if needle not in text:
            errors.append(f"{relative}: missing localization/status marker: {needle!r}")

required: dict[str, list[str]] = {
    "docs/STATUS.md": [english_metric, checkpoint_short, f"{job_count} permanent CI jobs", mutants, "Advisory topic facets"],
    "TEST_REPORT.md": [english_metric, checkpoint["commit"], coverage, f"{job_count} permanent CI jobs", mutants, "PR #302"],
    "docs/IMPLEMENTATION_STATUS.md": ["Immutable TrustSnapshot", "Ring Zero mutation gate", "Unified public read-only query boundary", "Advisory topic facets", "Scoped curator authorization"],
    "docs/DOCUMENTATION_MAP.md": ["Topic facets and curator IAM", "localized READMEs", "PR #302"],
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

for relative in locale_markers:
    text = (root / relative).read_text(encoding="utf-8")
    for stale in ("1713", "PR #265", "CLI `ask` and `receipt` still", "CLI `ask` et `receipt` utilisent encore"):
        if stale in text:
            errors.append(f"{relative}: stale architecture/status marker remains: {stale!r}")

# Validate relative Markdown links on every active reader surface.
active_link_surfaces = [
    *locale_markers.keys(),
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
    f"localized_readmes={len(locale_markers)}, "
    f"local links checked on {len(active_link_surfaces)} active surfaces"
)
PY
