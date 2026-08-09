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
        "proposal: submitted",
        "review: in progress",
        "award: not awarded",
        "budget change: none",
        "approximate €50,000 request",
        "not an approved budget or payment commitment",
        "physical l3 != strict canon",
        "postgresql/pgvector remains an optional inactive migration/equivalence target with `active=false`",
        "a dedicated reader core remains not implemented",
        "anything merged before a grant agreement is existing baseline",
    ),
    "docs/GLOSSARY.md": (
        "physical l3",
        "strict canon",
        "active=false",
        "funded delta",
        "submitted / under review / not awarded",
        "reader core",
        "native-speaker editorial certification",
    ),
    "docs/GRANT_NLNET_SCOPE.md": (
        "grant status:** submitted / under review / not awarded",
        "budget change:** none",
        "d1–d4 documentation work",
        "reader core is not implemented",
        "submitted proposal != awarded grant",
    ),
    "ROADMAP.md": (
        "grant status:** submitted / under review / not awarded",
        "budget change:** none",
        "sqlite ordinary active local-first profile",
        "a dedicated reader core remains not implemented",
        "d1–d4 documentation work merged before an agreement",
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
STALE = (
    "the l3 canonical graph is the single source of truth",
    "default backends are dependency-free (`mock` l3",
    "grant status: awarded",
    "crystal is gdpr compliant",
    "automatic backend switching is enabled",
    "reader core is implemented",
)
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def normalized(text: str) -> str:
    """Normalize Markdown wrapping and lightweight syntax for semantic markers."""
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

    matrix = supporting.get("docs/grants/baseline-funded-delta-matrix.md", "")
    require(
        "baseline/delta matrix",
        matrix,
        (
            "no award/budget change",
            "cannot be counted again as future paid work",
            "target remains `active=false`",
            "no dedicated reader core",
        ),
        errors,
    )

    plan = supporting.get("docs/grants/funding-use-plan.md", "")
    require(
        "funding use plan",
        plan,
        (
            "submitted to nlnet for review",
            "proposal has been submitted and is under review",
            "does not imply that funding has been awarded",
            "approx. **€50,000**",
            "does not represent an approved budget",
            "grant agreement or memorandum of understanding",
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
            "PROJECT_GRANT_AND_GOVERNANCE.md",
            "GLOSSARY.md",
            "D4 uses the compact Project/Grant/Governance overview",
            "submitted and under review, not awarded",
            "REFRESH_NEEDED translated document packs",
        ),
        errors,
    )

    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    require(
        "AI current state",
        state,
        (
            "D3 is current across all nine supported locale packs",
            "The D4 English source family is reconciled",
            "D4 project/grant context remains `REFRESH_NEEDED`",
            "D1–D4",
        ),
        errors,
    )

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    require(
        "translation ledger",
        ledger,
        (
            "## D4 — project, grant, governance and glossary",
            "Localized `GRANT_OVERVIEW.md` and `GLOSSARY.md` files",
            "remain `REFRESH_NEEDED`",
            "## D5 — extended reference documents",
        ),
        errors,
    )

    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    require(
        "CI workflow",
        workflow,
        (
            "Validate English D4 source contract",
            "python scripts/check_d4_source_contract.py",
        ),
        errors,
    )

    if errors:
        print("D4 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("English D4 project/grant/governance/glossary source contract is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
