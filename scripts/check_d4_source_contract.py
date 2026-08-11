"""Validate the English D4 project, grant, governance and glossary source contract through RC-5."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"
SOURCE_FILES = (
    "docs/PROJECT_GRANT_AND_GOVERNANCE.md",
    "docs/GLOSSARY.md",
    "docs/GRANT_NLNET_SCOPE.md",
    "ROADMAP.md",
    "GOVERNANCE.md",
    "CONTRIBUTING.md",
)
SUPPORTING_FILES = (
    "docs/grants/baseline-funded-delta-matrix.md",
    "docs/grants/funding-use-plan.md",
)
MARKERS = (
    "<!-- d4-source-contract: CURRENT -->",
    "<!-- d4-source-scope: project-grant-governance-glossary -->",
)
STALE = (
    "the l3 canonical graph is the single source of truth",
    "default backends are dependency-free (`mock` l3",
    "grant status: awarded",
    "crystal is gdpr compliant",
    "automatic backend switching is enabled",
    "rc-1/rc-2 are funded delivery",
)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def normalized(text: str) -> str:
    text = re.sub(r"(?m)^\s*>\s?", " ", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip().lower()


def check_links(relative: str, text: str, errors: list[str]) -> None:
    source = ROOT / relative
    for raw in LINK.findall(text):
        target = raw.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split(maxsplit=1)[0].split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        resolved = (source.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{relative}: local link escapes repository: {raw!r}")
            continue
        if not resolved.exists():
            errors.append(f"{relative}: broken local link: {raw!r}")


def require(relative: str, text: str, markers: tuple[str, ...], errors: list[str]) -> None:
    searchable = normalized(text)
    for marker in markers:
        if normalized(marker) not in searchable:
            errors.append(f"{relative}: missing current marker {marker!r}")


def main() -> int:
    errors: list[str] = []
    required = {
        "docs/PROJECT_GRANT_AND_GOVERNANCE.md": (
            "proposal: submitted",
            "review: in progress",
            "award: not awarded",
            "budget change: none",
            "€50,000",
            "active=false",
            "RC-5",
            "dedicated/full autonomous",
            "contradiction candidate != confirmed contradiction",
        ),
        "docs/GLOSSARY.md": (
            "physical L3",
            "strict Canon",
            "active=false",
            "funded delta",
            "submitted / under review / not awarded",
            "Reader Core RC-1",
            "Reader Core RC-2",
            "Reader Core RC-3",
            "Reader Core RC-4",
            "Reader Core RC-5",
            "EXTRACTED_PROPOSITION",
            "source owner",
            "proposition presentation category",
            "POSSIBLE_CONTRADICTION",
            "EXCEPTION",
            "QUALIFICATION",
            "TENSION",
            "relation rationale",
            "dedicated/full Reader Core",
            "native-speaker editorial certification",
        ),
        "docs/GRANT_NLNET_SCOPE.md": (
            "submitted / under review / not awarded",
            "budget change",
            "RC-5",
            "dedicated/full autonomous Reader",
            "cannot be budgeted again",
            "submitted proposal",
            "awarded grant",
            "Potential funded delta after RC-5",
        ),
        "ROADMAP.md": (
            "submitted / under review / not awarded",
            "budget change",
            "reader_core_rc1_skeleton",
            "reader_core_rc2_structural_map",
            "reader_core_rc3_multi_pass_mechanics",
            "reader_core_rc4_proposition_extraction",
            "reader_core_rc5_relation_candidates",
            "dedicated_reader_core",
            "RC-5 — Exceptions / Contradiction Candidate Detection",
            "contradiction candidate != confirmed contradiction",
            "RC-6",
            "RC-7",
        ),
        "GOVERNANCE.md": (
            "physical l3 != strict canon",
            "public query surfaces remain read-only",
            "postgresql/pgvector remains inactive with `active=false`",
            "nlnet proposal: submitted / under review / not awarded",
            "anything merged before an agreement is existing baseline",
        ),
        "CONTRIBUTING.md": (
            "physical l3 != strict canon",
            "sqlite | ordinary active local-first profile",
            "mock | explicit ephemeral development and ci backend",
            "postgresql/pgvector | optional inactive import/equivalence target with `active=false`",
            "submitted / under review / not awarded",
            "anything merged before a funding agreement is existing baseline",
        ),
    }

    for relative in SOURCE_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing D4 source file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in MARKERS:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        require(relative, text, required[relative], errors)
        searchable = normalized(text)
        for stale in STALE:
            if normalized(stale) in searchable:
                errors.append(f"{relative}: stale or unsupported claim {stale!r}")
        check_links(relative, text, errors)

    supporting: dict[str, str] = {}
    for relative in SUPPORTING_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing D4 supporting file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        supporting[relative] = text
        check_links(relative, text, errors)

    require(
        "baseline/delta matrix",
        supporting.get("docs/grants/baseline-funded-delta-matrix.md", ""),
        (
            "no award",
            "cannot be counted again",
            "active=false",
            "Reader RC-1",
            "Reader RC-2",
            "Reader RC-3",
            "Reader RC-4",
            "Reader RC-5",
            "reader_core_rc5_relation_candidates",
            "contradiction candidate != confirmed contradiction",
            "after RC-5",
        ),
        errors,
    )
    require(
        "funding use plan",
        supporting.get("docs/grants/funding-use-plan.md", ""),
        (
            "submitted to nlnet for review",
            "does not imply that funding has been awarded",
            "€50,000",
            "does not represent an approved budget",
            "the grant does not pay to recreate",
            "features that are already implemented",
        ),
        errors,
    )

    doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    require(
        "documentation map",
        doc_map,
        (
            "Reader Core architecture contract",
            "Grant scope",
            "Baseline-funded delta matrix",
            "submitted / under review / not awarded",
            "D4",
        ),
        errors,
    )

    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    require(
        "AI current state",
        state,
        (
            SOURCE,
            "reader_core_rc1_skeleton",
            "reader_core_rc2_structural_map",
            "reader_core_rc3_multi_pass_mechanics",
            "reader_core_rc4_proposition_extraction",
            "reader_core_rc5_relation_candidates",
            "dedicated_reader_core",
            "EXTRACTED_PROPOSITION != verified fact",
            "Reader candidate != admitted evidence",
            "contradiction candidate != confirmed contradiction",
            "NLnet remains submitted / under review / not awarded",
        ),
        errors,
    )

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    require(
        "translation ledger",
        ledger,
        (
            "## D4 — project, grant, governance and glossary",
            "D4 Reader-dependent detail translations are `CURRENT` in Russian",
            "eight other supported locales are `REFRESH_NEEDED`",
            "## D5 — extended reference documents",
        ),
        errors,
    )

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    require(
        "CI workflow",
        workflow,
        ("Validate English D4 source contract", "python scripts/check_d4_source_contract.py"),
        errors,
    )

    if errors:
        print("D4 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"English D4 project/grant/governance/glossary source contract consistent through RC-5: source={SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
