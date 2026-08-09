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
        "submitted / under review / not awarded",
        "budget change: none",
        "physical L3      != strict Canon",
        "PostgreSQL/pgvector remains an optional inactive migration/equivalence target with `active=false`",
        "A dedicated Reader Core remains not implemented",
        "Anything merged before a grant agreement is existing baseline",
    ),
    "docs/GLOSSARY.md": (
        "physical L3",
        "strict Canon",
        "active=false",
        "funded delta",
        "submitted / under review / not awarded",
        "Reader Core",
        "Native-speaker editorial certification",
    ),
    "docs/GRANT_NLNET_SCOPE.md": (
        "Grant status:** submitted / under review / not awarded",
        "Budget change:** none",
        "D1–D4 documentation work",
        "Reader Core is not implemented",
        "submitted proposal   != awarded grant",
    ),
    "ROADMAP.md": (
        "Grant status:** submitted / under review / not awarded",
        "Budget change:** none",
        "SQLite is the ordinary active local-first profile",
        "A dedicated Reader Core remains not implemented",
        "D1–D4 documentation work merged before an agreement",
    ),
    "GOVERNANCE.md": (
        "physical L3      != strict Canon",
        "public query surfaces remain read-only",
        "PostgreSQL/pgvector remains inactive with `active=false`",
        "NLnet proposal: submitted / under review / not awarded",
        "Anything merged before an agreement is existing baseline",
    ),
    "CONTRIBUTING.md": (
        "physical L3      != strict Canon",
        "SQLite | ordinary active local-first profile",
        "Mock | explicit ephemeral development and CI backend",
        "PostgreSQL/pgvector | optional inactive import/equivalence target with `active=false`",
        "submitted / under review / not awarded",
        "Anything merged before a funding agreement is existing baseline",
    ),
}
STALE = (
    "the L3 canonical graph is the single source of truth",
    "default backends are dependency-free (`mock` L3",
    "Grant status: awarded",
    "funding has been awarded",
    "Crystal is GDPR compliant",
    "automatic backend switching is enabled",
    "Reader Core is implemented",
)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


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
        for marker in REQUIRED[relative]:
            if marker not in text:
                errors.append(f"{relative}: missing current marker {marker!r}")
        for stale in STALE:
            if stale in text:
                errors.append(f"{relative}: stale or unsupported claim {stale!r}")
        check_links(relative, text, errors)

    for relative in SUPPORTING_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing D4 supporting file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        check_links(relative, text, errors)

    matrix = (ROOT / "docs/grants/baseline-funded-delta-matrix.md").read_text(encoding="utf-8")
    for marker in (
        "no award/budget change",
        "cannot be counted again as future paid work",
        "target remains `active=false`",
        "no dedicated Reader Core",
    ):
        if marker not in matrix:
            errors.append(f"baseline/delta matrix: missing marker {marker!r}")

    plan = (ROOT / "docs/grants/funding-use-plan.md").read_text(encoding="utf-8")
    for marker in (
        "Submitted to NLnet for review",
        "does not imply that funding has been awarded",
        "approx. **€50,000**",
        "does not represent an approved budget",
        "The grant does not pay to recreate features that are already implemented",
    ):
        if marker not in plan:
            errors.append(f"funding use plan: missing marker {marker!r}")

    doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    for marker in (
        "PROJECT_GRANT_AND_GOVERNANCE.md",
        "GLOSSARY.md",
        "D4 uses the compact Project/Grant/Governance overview",
        "submitted and under review, not awarded",
        "REFRESH_NEEDED translated document packs",
    ):
        if marker not in doc_map:
            errors.append(f"documentation map: missing marker {marker!r}")

    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "D3 is current across all nine supported locale packs",
        "The D4 English source family is reconciled",
        "Localized D4 documents remain `REFRESH_NEEDED`",
        "D1–D4",
    ):
        if marker not in state:
            errors.append(f"AI current state: missing marker {marker!r}")

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        "## D4 — project, grant, governance and glossary",
        "Localized `GRANT_OVERVIEW.md` and `GLOSSARY.md` files",
        "remain `REFRESH_NEEDED`",
        "## D5 — extended reference documents",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for marker in (
        "Validate English D4 source contract",
        "python scripts/check_d4_source_contract.py",
    ):
        if marker not in workflow:
            errors.append(f"CI workflow: missing D4 source validator marker {marker!r}")

    if errors:
        print("D4 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("English D4 project/grant/governance/glossary source contract is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
