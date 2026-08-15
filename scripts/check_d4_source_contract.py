"""Validate English D4 project/grant/governance truth against the post-RC-9 baseline."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
# Retained immutable D4 translation-source checkpoint. Current English grant truth may
# advance independently; translated freshness is governed by TRANSLATION_STATUS.md.
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
    "docs/grants/reviewer-qa.md",
)
MARKERS = (
    "<!-- d4-source-contract: CURRENT -->",
    "<!-- d4-source-scope: project-grant-governance-glossary -->",
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
            errors.append(f"{relative}: missing current semantic marker {marker!r}")


def forbid(relative: str, text: str, phrases: tuple[str, ...], errors: list[str]) -> None:
    searchable = normalized(text)
    for phrase in phrases:
        if normalized(phrase) in searchable:
            errors.append(f"{relative}: stale or unsupported current-state phrase {phrase!r}")


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
            "RC-9",
            "dedicated_reader_core=false",
            "retrieval match",
            "candidate discovery",
            "candidate adjudication",
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
            "POSSIBLE_CONTRADICTION",
            "EXCEPTION",
            "QUALIFICATION",
            "TENSION",
            "dedicated/full Reader Core",
        ),
        "docs/GRANT_NLNET_SCOPE.md": (
            "submitted / under review / not awarded",
            "budget change",
            "RC-9",
            "dedicated_reader_core",
            "existing pre-agreement baseline",
            "cannot later be rebilled",
            "Recall@5",
            "Precision@5",
            "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
            "candidate discovery",
            "candidate adjudication",
        ),
        "ROADMAP.md": (
            "submitted / under review / not awarded",
            "reader_core_rc1_skeleton",
            "reader_core_rc7_cross_document_links",
            "dedicated_reader_core",
            "RC-9",
            "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
            "candidate discovery",
            "candidate adjudication",
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
            "Reader RC-7",
            "Reader RC-8",
            "Reader RC-9",
            "dedicated_reader_core",
            "Recall@5",
            "Precision@5",
            "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
            "candidate discovery",
            "candidate adjudication",
        ),
        errors,
    )
    require(
        "funding use plan",
        supporting.get("docs/grants/funding-use-plan.md", ""),
        (
            "submitted / under review / not awarded",
            "€50,000",
            "not an approved budget",
            "RC-9",
            "cannot be paid for again",
            "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
        ),
        errors,
    )
    require(
        "reviewer Q&A",
        supporting.get("docs/grants/reviewer-qa.md", ""),
        (
            "RC-9",
            "Recall@5",
            "Precision@5",
            "not presented as “94% accuracy”",
            "submitted / under review / not awarded",
            "dedicated_reader_core=false",
            "candidate discovery",
            "candidate adjudication",
        ),
        errors,
    )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(
        "root README",
        readme,
        (
            "Current implemented Reader retrieval baseline",
            "RC-9 deterministic lexical PRE-ADMISSION candidate discovery",
            "Recall@5",
            "Precision@5",
            "MRR",
            "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
            "Reviewer validation",
            "submitted / under review / not awarded",
            "dedicated_reader_core=false",
            "candidate discovery",
            "candidate adjudication",
        ),
        errors,
    )
    check_links("README.md", readme, errors)

    stale_current_phrases = (
        "Potential funded delta after RC-5",
        "RC-6 is currently being implemented",
        "RC-7 tracking: issue #371; implementation draft: PR #372",
        "final RC-7 merge/signature/post-merge CI evidence is pending",
        "RC-7: planned cross-document",
    )
    for relative, text in (
        ("README.md", readme),
        ("docs/GRANT_NLNET_SCOPE.md", (ROOT / "docs/GRANT_NLNET_SCOPE.md").read_text(encoding="utf-8")),
        ("docs/grants/baseline-funded-delta-matrix.md", supporting.get("docs/grants/baseline-funded-delta-matrix.md", "")),
        ("docs/PROJECT_GRANT_AND_GOVERNANCE.md", (ROOT / "docs/PROJECT_GRANT_AND_GOVERNANCE.md").read_text(encoding="utf-8")),
    ):
        forbid(relative, text, stale_current_phrases, errors)

    forbid(
        "root README",
        readme,
        (
            "94% accuracy",
            "semantic understanding is implemented",
            "automatic truth verification is implemented",
            "Crystal implements automatic truth verification",
            "grant status: awarded",
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
            "reader_core_rc7_cross_document_links",
            "dedicated_reader_core",
            "RC-9",
            "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
            "NLnet remains submitted / under review / not awarded",
        ),
        errors,
    )

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    require(
        "translation ledger",
        ledger,
        (
            "## D4 — project / grant / glossary",
            "D4 Reader-dependent detail translations are `CURRENT` in all nine supported locales",
            "No supported Reader-dependent locale pack remains `REFRESH_NEEDED`",
            "## D5 — extended reference corpus",
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

    print(
        "English D4 project/grant/governance truth consistent with post-RC-9 public baseline; "
        f"retained translation source={SOURCE}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
