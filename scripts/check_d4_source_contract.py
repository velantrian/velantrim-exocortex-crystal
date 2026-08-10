"""Validate the English D4 project, grant, governance and glossary source contract."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
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
REQUIRED = {
    "docs/PROJECT_GRANT_AND_GOVERNANCE.md": (
        "proposal: submitted", "review: in progress", "award: not awarded",
        "budget change: none", "approximate €50,000 request",
        "not an approved budget or payment commitment", "physical l3",
        "postgresql/pgvector remains an optional inactive migration/equivalence target with `active=false`",
        "reader core rc-1, rc-2, rc-3 and rc-4", "dedicated/full autonomous semantic reading runtime",
        "anything merged before a grant agreement is existing baseline", "extracted_proposition",
        "reader candidate", "core.evidence.attach_evidence()",
    ),
    "docs/GLOSSARY.md": (
        "physical l3", "strict canon", "active=false", "funded delta",
        "submitted / under review / not awarded", "reader core rc-1", "reader core rc-2",
        "reader core rc-3", "reader core rc-4", "extracted_proposition",
        "source owner", "proposition presentation category", "dedicated/full reader core",
        "native-speaker editorial certification",
    ),
    "docs/GRANT_NLNET_SCOPE.md": (
        "grant status:** submitted / under review / not awarded", "budget change:** none",
        "reader rc-1/rc-2/rc-3 and rc-4", "dedicated/full autonomous reader", "rc-4",
        "cannot be budgeted again as funded delivery", "submitted proposal    != awarded grant",
        "potential funded delta after rc-4",
    ),
    "ROADMAP.md": (
        "grant status:** submitted / under review / not awarded", "budget change:** none",
        "reader_core_rc1_skeleton", "reader_core_rc2_structural_map",
        "reader_core_rc3_multi_pass_mechanics", "reader_core_rc4_proposition_extraction",
        "dedicated_reader_core", "rc-4 — source-linked proposition extraction",
        "extracted_proposition != verified fact", "reader candidate      != admitted evidence",
        "rc-5 exceptions / contradiction candidates",
    ),
    "GOVERNANCE.md": (
        "physical l3 != strict canon", "public query surfaces remain read-only",
        "postgresql/pgvector remains inactive with `active=false`",
        "nlnet proposal: submitted / under review / not awarded",
        "anything merged before an agreement is existing baseline",
    ),
    "CONTRIBUTING.md": (
        "physical l3 != strict canon", "sqlite | ordinary active local-first profile",
        "mock | explicit ephemeral development and ci backend",
        "postgresql/pgvector | optional inactive import/equivalence target with `active=false`",
        "submitted / under review / not awarded",
        "anything merged before a funding agreement is existing baseline",
    ),
}
STALE = (
    "the l3 canonical graph is the single source of truth",
    "default backends are dependency-free (`mock` l3", "grant status: awarded",
    "crystal is gdpr compliant", "automatic backend switching is enabled",
    "rc-1/rc-2 are funded delivery", "reader work beyond rc-3",
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
    for relative in SOURCE_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing D4 source file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in MARKERS:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        require(relative, text, REQUIRED[relative], errors)
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

    require("baseline/delta matrix", supporting.get("docs/grants/baseline-funded-delta-matrix.md", ""), (
        "no award/budget change", "cannot be counted again as future paid work",
        "target remains `active=false`", "reader rc-1", "reader rc-2", "reader rc-3", "reader rc-4",
        "reader_core_rc4_proposition_extraction = true",
        "extracted_proposition != verified fact", "reader candidate != admitted evidence",
        "reader work beyond rc-4",
    ), errors)
    require("funding use plan", supporting.get("docs/grants/funding-use-plan.md", ""), (
        "submitted to nlnet for review", "proposal has been submitted and is under review",
        "does not imply that funding has been awarded", "approx. **€50,000**",
        "does not represent an approved budget", "grant agreement or memorandum of understanding",
        "the grant does not pay to recreate", "features that are already implemented",
    ), errors)

    doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    require("documentation map", doc_map, (
        "Reader Core architecture contract", "Grant scope", "Baseline-funded delta matrix",
        "submitted / under review / not awarded", "D4",
    ), errors)
    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    require("AI current state", state, (
        "Russian Reader-dependent public/detail documentation is refreshed",
        "eight other localized root README files and Reader-dependent detail packs",
        "reader_core_rc1_skeleton", "reader_core_rc2_structural_map",
        "reader_core_rc3_multi_pass_mechanics", "reader_core_rc4_proposition_extraction",
        "dedicated_reader_core", "EXTRACTED_PROPOSITION != verified fact",
        "Reader candidate != admitted evidence",
    ), errors)
    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    require("translation ledger", ledger, (
        "## D4 — project, grant, governance and glossary",
        "D4 Reader-dependent detail translations are `CURRENT` in Russian",
        "eight other supported locales are `REFRESH_NEEDED`",
        "## D5 — extended reference documents",
    ), errors)
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    require("CI workflow", workflow, (
        "Validate English D4 source contract", "python scripts/check_d4_source_contract.py",
    ), errors)

    if errors:
        print("D4 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("English D4 project/grant/governance/glossary source contract is consistent through RC-4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
