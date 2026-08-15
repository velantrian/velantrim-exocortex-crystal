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
arabic_historical_source = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
arabic_parity_base = "9e048c21fb929f7d299e3af0ef03d76c1df899d6"
german_historical_source = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
german_parity_base = "ad8cec8c868f64b6dfbdc3bf3087230f59c3861c"
french_historical_source = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
french_parity_base = "7d03cce2c89f7a4c3fda85742eb358e6b49961f2"
spanish_historical_source = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
spanish_parity_base = "bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb"
italian_historical_source = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
italian_parity_base = "e436577dc5ada4692e8fe399da861a44f800e2f1"
simplified_chinese_historical_source = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
simplified_chinese_parity_base = "5e6301f0eaee1a6c85d8543be89dc2e606dc05a8"
japanese_historical_source = "6b45bdd196eb42dea7bc30f58d69799b4b1712f2"
japanese_parity_base = "5903e90f3e0f2884f4ba257a71808d19fc439ebc"
locales = ["ar", "de", "es", "fr", "hi", "it", "ja", "ru", "zh-CN"]
current_locales = ["ar", "de", "es", "fr", "it", "ja", "ru", "zh-CN"]
refresh_locales = [locale for locale in locales if locale not in current_locales]


def expect(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def normalized(text: str) -> str:
    text = re.sub(r"(?m)^\s*>\s?", " ", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip().lower()


def require(relative: str, text: str, markers: tuple[str, ...]) -> None:
    searchable = normalized(text)
    for marker in markers:
        if normalized(marker) not in searchable:
            errors.append(f"{relative}: missing current semantic marker {marker!r}")


def forbid(relative: str, text: str, phrases: tuple[str, ...]) -> None:
    searchable = normalized(text)
    for phrase in phrases:
        if normalized(phrase) in searchable:
            errors.append(f"{relative}: stale current-state phrase {phrase!r}")


checkpoint = manifest["verified_runtime_checkpoint"]
tests = manifest["tests"]
boundaries = manifest["implemented_boundaries"]
docs = manifest["documentation"]
grant = manifest["grant"]
rc5 = manifest.get("reader_core_rc5", {})

# Retained historical runtime checkpoint remains immutable evidence. Later Reader/localization
# milestones carry separate evidence and do not rewrite this compatibility record.
expect(checkpoint.get("commit"), runtime_commit, "runtime checkpoint")
expect(tests.get("passed"), 2078, "tests passed")
expect(tests.get("skipped"), 13, "tests skipped")
expect(tests.get("failed"), 0, "tests failed")
expect(tests.get("measured_statements"), 9756, "measured statements")
expect(tests.get("coverage_percent"), 100.0, "coverage")

# Current machine Reader truth is RC-1..RC-7 bounded=true, dedicated/full Reader=false.
for key in (
    "reader_core_rc1_skeleton",
    "reader_core_rc2_structural_map",
    "reader_core_rc3_multi_pass_mechanics",
    "reader_core_rc4_proposition_extraction",
    "reader_core_rc5_relation_candidates",
    "reader_core_rc6_long_context_strategy",
    "reader_core_rc7_cross_document_links",
):
    expect(boundaries.get(key), True, key)
expect(boundaries.get("dedicated_reader_core"), False, "dedicated Reader")
expect(boundaries.get("postgresql_target_active"), False, "PostgreSQL active")
expect(boundaries.get("semantic_hybrid_reader_runtime"), False, "semantic Reader runtime")
expect(boundaries.get("nli_reader_runtime_filter"), False, "NLI Reader runtime filter")
expect(boundaries.get("rrtic_runtime_provider"), False, "RRTIC runtime provider")

# Preserve the exact RC-5 machine contract as a historical invariant while public status moves
# beyond RC-5. Localization work may not mutate this bounded implementation layer.
expect(rc5.get("tracking_issue"), 367, "RC-5 issue")
expect(rc5.get("pull_request"), 368, "RC-5 PR")
expect(rc5.get("runtime_module"), "core/reader_relations.py", "RC-5 runtime")
expect(rc5.get("test_module"), "tests/test_reader_relations.py", "RC-5 tests")
expect(rc5.get("input_boundary"), "registered_rc4_proposition_candidates_only", "RC-5 input")
expect(
    rc5.get("relation_kinds"),
    ["POSSIBLE_CONTRADICTION", "EXCEPTION", "QUALIFICATION", "TENSION"],
    "RC-5 kinds",
)
for key in (
    "same_reader_session_required",
    "same_source_version_required",
    "within_document_only",
    "exact_candidate_id_linkage",
    "primary_and_supporting_provenance_preserved",
    "explicit_rationale_required",
    "count_only_telemetry",
):
    expect(rc5.get(key), True, f"RC-5 {key}")
for key in (
    "automatic_semantic_equivalence",
    "automatic_cross_document_reasoning",
    "contradiction_resolution_authority",
    "automatic_winner_selection",
    "evidence_admission",
    "fact_evidence_write",
    "confidence_promotion",
    "llm_or_provider_integration",
    "embeddings_or_vector_database",
    "truth_or_canon_authority",
):
    expect(rc5.get(key), False, f"RC-5 {key}")

# Historical phased source checkpoint remains immutable while completed locale refreshes advance
# independently against newer public semantics.
expect(docs.get("localized_readme_source_checkpoint"), source_checkpoint, "localized README source")
expect(docs.get("full_parity_current_locales"), current_locales, "root current locales")
expect(docs.get("full_parity_refresh_needed_locales"), refresh_locales, "root refresh locales")
expect(docs.get("d1_source_checkpoint"), source_checkpoint, "D1 source")
expect(docs.get("d1_current_locales"), current_locales, "D1 current locales")
expect(docs.get("d1_refresh_needed_locales"), refresh_locales, "D1 refresh locales")
expect(docs.get("latest_translation_refresh_issue"), 425, "latest translation refresh issue")
expect(docs.get("arabic_parity_audit_base"), arabic_parity_base, "Arabic parity audit base")
expect(docs.get("german_parity_audit_base"), german_parity_base, "German parity audit base")
expect(docs.get("french_parity_audit_base"), french_parity_base, "French parity audit base")
expect(docs.get("spanish_parity_audit_base"), spanish_parity_base, "Spanish parity audit base")
expect(docs.get("italian_parity_audit_base"), italian_parity_base, "Italian parity audit base")
expect(docs.get("simplified_chinese_parity_audit_base"), simplified_chinese_parity_base, "Simplified Chinese parity audit base")
expect(docs.get("japanese_parity_audit_base"), japanese_parity_base, "Japanese parity audit base")
expect(grant.get("submitted"), True, "grant submitted")
expect(grant.get("under_review"), True, "grant review")
expect(grant.get("awarded"), False, "grant awarded")

common = (
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
        for marker in (
            f"localization-source: main@{source_checkpoint}",
            "localization-status: CURRENT",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing retained localization marker {marker!r}")
    elif locale == "ar":
        for marker in (
            f"localization-source: main@{arabic_historical_source}",
            "localization-status: CURRENT",
            f"current-localization-source: main@{arabic_parity_base}",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing Arabic current/provenance marker {marker!r}")
    elif locale == "de":
        for marker in (
            f"localization-source: main@{german_historical_source}",
            "localization-status: CURRENT",
            f"current-localization-source: main@{german_parity_base}",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing German current/provenance marker {marker!r}")
    elif locale == "fr":
        for marker in (
            f"localization-source: main@{french_historical_source}",
            "localization-status: CURRENT",
            f"current-localization-source: main@{french_parity_base}",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing French current/provenance marker {marker!r}")
    elif locale == "es":
        for marker in (
            f"localization-source: main@{spanish_historical_source}",
            "localization-status: CURRENT",
            f"current-localization-source: main@{spanish_parity_base}",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing Spanish current/provenance marker {marker!r}")
    elif locale == "it":
        for marker in (
            f"localization-source: main@{italian_historical_source}",
            "localization-status: CURRENT",
            f"current-localization-source: main@{italian_parity_base}",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing Italian current/provenance marker {marker!r}")
    elif locale == "zh-CN":
        for marker in (
            f"localization-source: main@{simplified_chinese_historical_source}",
            "localization-status: CURRENT",
            f"current-localization-source: main@{simplified_chinese_parity_base}",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing Simplified Chinese current/provenance marker {marker!r}")
    elif locale == "ja":
        for marker in (
            f"localization-source: main@{japanese_historical_source}",
            "localization-status: CURRENT",
            f"current-localization-source: main@{japanese_parity_base}",
            "reader_core_rc5_relation_candidates    = true",
            "contradiction candidate  != confirmed contradiction",
        ):
            if marker not in text:
                errors.append(f"{relative}: missing Japanese current/provenance marker {marker!r}")
    elif f"localization-source: main@{source_checkpoint}" in text:
        errors.append(f"{relative}: REFRESH_NEEDED root falsely pins RC-5 source")

# Root English README is the current first-impression source and must track post-RC-9 truth.
root_readme = (root / "README.md").read_text(encoding="utf-8")
require(
    "README.md",
    root_readme,
    (
        "Current implemented Reader retrieval baseline",
        "RC-9 deterministic lexical PRE-ADMISSION candidate discovery",
        "reader_core_rc7_cross_document_links",
        "dedicated_reader_core=false",
        "Recall@5",
        "Precision@5",
        "MRR",
        "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
        "candidate discovery",
        "candidate adjudication",
        "Reviewer validation",
        "submitted / under review / not awarded",
    ),
)
forbid(
    "README.md",
    root_readme,
    (
        "RC-6 as the authoritative implemented milestone",
        "RC-7 implementation draft",
        "final RC-7 merge/signature/post-merge CI evidence is pending",
        "94% accuracy",
    ),
)

for locale in locales:
    index = (root / "docs" / locale / "README.md").read_text(encoding="utf-8")
    status = "CURRENT" if locale in current_locales else "REFRESH_NEEDED"
    for phase in ("d1", "d3", "d4", "d5"):
        for marker in (f"{phase}-source: main@{source_checkpoint}", f"{phase}-status: {status}"):
            if marker not in index:
                errors.append(f"docs/{locale}/README.md: missing {marker!r}")
    for marker in (
        f"localization-index-source: main@{source_checkpoint}",
        "d2-status: CURRENT",
        "Localization policy",
        "Translation status",
    ):
        if marker not in index:
            errors.append(f"docs/{locale}/README.md: missing {marker!r}")

# Active English status surfaces use semantic markers instead of stale exact section titles.
required = {
    "docs/STATUS.md": (
        "reader_core_rc7_cross_document_links",
        "core/reader_relations.py",
        "RC-9 deterministic lexical baseline",
        "Recall@5",
        "candidate discovery != candidate adjudication",
        "active=false",
    ),
    "docs/IMPLEMENTATION_STATUS.md": (
        "reader_core_rc7_cross_document_links",
        "core/reader_relations.py",
        "Reader RC-9 lexical candidate discovery",
        "Recall@5",
        "candidate discovery != candidate adjudication",
        "dedicated_reader_core=false",
    ),
    "docs/ARCHITECTURE_OVERVIEW.md": (
        "RC-5",
        "relation candidate",
        "contradiction candidate != confirmed contradiction",
        "active=false",
    ),
    "docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md": (
        "Reader relation",
        "RC-5",
        "contradiction candidate != confirmed contradiction",
        "active=false",
    ),
    "docs/PROJECT_GRANT_AND_GOVERNANCE.md": (
        "RC-9",
        "submitted",
        "€50,000",
        "contradiction candidate != confirmed contradiction",
        "candidate discovery",
        "candidate adjudication",
    ),
    "docs/GLOSSARY.md": (
        "Reader Core RC-5",
        "POSSIBLE_CONTRADICTION",
        "EXCEPTION",
        "QUALIFICATION",
        "TENSION",
    ),
    "docs/EXTENDED_REFERENCE_POLICY.md": (
        "reader_core_rc5_relation_candidates",
        "contradiction candidate != confirmed contradiction",
        "REFRESH_NEEDED",
    ),
    "docs/TRANSLATION_STATUS.md": (
        source_checkpoint,
        "Reader RC-5 boundary",
        "8 `REFRESH_NEEDED` localized documents",
        "Arabic, German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian",
        "RC-9",
        "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
    ),
    "docs/ai/CURRENT_STATE.md": (
        source_checkpoint,
        "reader_core_rc7_cross_document_links",
        "one other localized root README file",
        "Arabic, German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed",
        "RC-9",
        "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
    ),
    "ROADMAP.md": (
        "RC-5 — relation candidates",
        "RC-6 — bounded long context",
        "RC-7 — bounded cross-document candidate links",
        "RC-9 — deterministic lexical candidate discovery + benchmark",
        "issue #379",
    ),
}
for relative, markers in required.items():
    text = (root / relative).read_text(encoding="utf-8")
    require(relative, text, markers)

# Current grant/public surfaces must not regress to the pre-RC-9 baseline description.
for relative in (
    "README.md",
    "docs/GRANT_NLNET_SCOPE.md",
    "docs/PROJECT_GRANT_AND_GOVERNANCE.md",
    "docs/grants/baseline-funded-delta-matrix.md",
    "ROADMAP.md",
):
    text = (root / relative).read_text(encoding="utf-8")
    forbid(
        relative,
        text,
        (
            "Potential funded delta after RC-5",
            "RC-6 is currently being implemented",
            "RC-7 tracking: issue #371; implementation draft: PR #372",
            "final RC-7 merge/signature/post-merge CI evidence is pending",
        ),
    )

link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
link_surfaces = [
    "README.md",
    "README.ru.md",
    "README.ar.md",
    "README.de.md",
    "README.fr.md",
    "README.es.md",
    "README.it.md",
    "README.ja.md",
    "README.zh-CN.md",
    "docs/TRANSLATION_STATUS.md",
    "docs/DOCUMENTATION_MAP.md",
    *[f"docs/{locale}/README.md" for locale in locales],
]
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
print(
    "Documentation status consistent: Reader RC-1..RC-7 bounded=true, RC-9 lexical baseline current, "
    "dedicated=false; English grant truth post-RC-9; Arabic + German + French + Spanish + Italian + Japanese + Simplified Chinese + Russian localization current"
)
PY
