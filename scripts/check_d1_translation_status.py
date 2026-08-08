"""Validate the current phased D1 localization checkpoint."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "16d71e731ee658b1faa65c9ea45c0d8cca290f7c"
FILES = {
    "docs/ru/README.md": (
        f"d1-source: main@{SOURCE}",
        "`CURRENT` (D1)",
        "`REFRESH_NEEDED` (D2)",
    ),
    "docs/ru/QUICKSTART.md": (
        f"translation-source: docs/QUICKSTART.md@{SOURCE}",
        "translation-status: CURRENT",
        "core.query_pipeline.query()",
        "active=false",
        "Import — не activation",
    ),
    "docs/ru/STATUS.md": (
        f"translation-source: docs/STATUS.md@{SOURCE}",
        "translation-status: CURRENT",
        "bbd816c09dd39a02e6de6c1014438490572f40f6",
        "2078 passed / 13 skipped / 0 failed",
        "9756 statements / 100.00% line coverage",
        "active=false",
        "Проект подан",
    ),
    "docs/ru/IMPLEMENTATION_STATUS.md": (
        f"translation-source: docs/IMPLEMENTATION_STATUS.md@{SOURCE}",
        "translation-status: CURRENT",
        "Inactive PostgreSQL/pgvector import",
        "Automatic SQLite/PostgreSQL switching",
        "Reader Core / Semantic Reading Layer",
    ),
}
STALE = (
    "1713 passed",
    "6389 measured statements",
    "PR #265",
    "CLI-команды `ask` и `receipt` пока используют исторический путь",
)
UNSUPPORTED = (
    "PostgreSQL/pgvector является текущим runtime",
    "автоматическое переключение backend включено",
    "грант NLnet получен",
    "Crystal гарантирует отсутствие hallucinations",
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
    documentation = json.loads(
        (ROOT / "docs/status/implementation-manifest.json").read_text(encoding="utf-8")
    )["documentation"]
    expected_pending = ["ar", "de", "es", "fr", "hi", "it", "ja", "zh-CN"]
    expected_documents = list(FILES)

    checks = (
        (documentation.get("translation_tracking_issue") == 341, "tracking issue"),
        (documentation.get("d1_current_locales") == ["ru"], "current locales"),
        (documentation.get("d1_source_checkpoints") == {"ru": SOURCE}, "source checkpoint"),
        (documentation.get("d1_pending_locales") == expected_pending, "pending locales"),
        (
            documentation.get("d1_current_documents", {}).get("ru")
            == expected_documents,
            "current documents",
        ),
    )
    for ok, label in checks:
        if not ok:
            errors.append(f"manifest: invalid D1 {label}")

    for relative, markers in FILES.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing Russian D1 file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(
            f"{relative}: missing marker {marker!r}"
            for marker in markers
            if marker not in text
        )
        errors.extend(
            f"{relative}: stale marker {marker!r}"
            for marker in STALE
            if marker in text
        )
        errors.extend(
            f"{relative}: unsupported claim {marker!r}"
            for marker in UNSUPPORTED
            if marker in text
        )
        check_links(relative, text, errors)

    ledger = (ROOT / "docs/TRANSLATION_STATUS.md").read_text(encoding="utf-8")
    for marker in (
        f"D1 Russian source checkpoint:** `main@{SOURCE}`",
        "| Russian | `CURRENT` | `CURRENT` | `CURRENT` | `CURRENT` |",
        "`docs/ru/IMPLEMENTATION_STATUS.md`",
        "Russian `CURRENT`; eight locales pending",
    ):
        if marker not in ledger:
            errors.append(f"translation ledger: missing marker {marker!r}")

    ai_state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text(encoding="utf-8")
    for marker in ("Issue #341", f"main@{SOURCE}", "Russian D1 documents are"):
        if marker not in ai_state:
            errors.append(f"AI current state: missing marker {marker!r}")

    if errors:
        print("D1 translation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"D1 translation status is consistent: current=ru, source={SOURCE}, pending=8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
