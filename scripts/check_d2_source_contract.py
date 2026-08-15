"""Validate the stable English D2 reviewer/safety/privacy/failure source contract."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "docs/REVIEWER_GUIDE.md",
    "docs/SAFETY_PRIVACY_AND_FAILURES.md",
    "PRIVACY.md",
    "docs/FAILURE_MODES.md",
    "SECURITY.md",
)
MARKERS = (
    "<!-- d2-source-contract: CURRENT -->",
    "<!-- d2-source-scope: reviewer-security-privacy-failure -->",
)
COMMON_BOUNDARIES = (
    "active=false",
    "not a security, legal or GDPR certification",
)
STALE = (
    "Reflects the audit-hardening work completed in this cycle (Tracks 1–3C)",
    "The default (`mock`) and `ladybug` backends are local",
    "falls back to the dependency-free **on-disk SQLite** backend",
    "uses the in-memory `mock` only as a last-resort/dev fallback",
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
    for relative in FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing D2 source file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in MARKERS:
            if marker not in text:
                errors.append(f"{relative}: missing marker {marker!r}")
        for stale in STALE:
            if stale in text:
                errors.append(f"{relative}: stale marker {stale!r}")
        check_links(relative, text, errors)

    combined = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in FILES)
    for boundary in COMMON_BOUNDARIES:
        if boundary not in combined:
            errors.append(f"D2 source contract: missing boundary {boundary!r}")
    for boundary in (
        "Public `ask` routes through `core.query_pipeline.query()`",
        "Successful import or equivalence is operation evidence, not activation",
        "Erasing active local state does not automatically erase independent copies",
    ):
        if boundary not in combined:
            errors.append(f"D2 source contract: missing boundary {boundary!r}")

    current_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in (
        "D2 reviewer/safety translations remain current across all nine supported locales",
        "Arabic, German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed",
        "one other localized root README file and Reader-dependent detail pack",
    ):
        if marker not in current_state:
            errors.append(f"AI current state: missing localization marker {marker!r}")

    map_text = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
    for marker in ("SAFETY_PRIVACY_AND_FAILURES.md", "D2 uses the stable English Reviewer Guide"):
        if marker not in map_text:
            errors.append(f"documentation map: missing marker {marker!r}")

    if errors:
        print("D2 source validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("D2 English reviewer/safety/privacy/failure source contract is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
