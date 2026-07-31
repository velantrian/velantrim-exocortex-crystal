#!/usr/bin/env python3
"""Validate the maintained localization documentation family.

Pure-standard-library tooling so it can run in the default CI environment.
This checker validates structure and navigation; it does not certify translation quality.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "i18n" / "locales.json"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SYNC_RE = re.compile(r"main@([0-9a-f]{8})")


@dataclass(frozen=True)
class Locale:
    code: str
    label: str
    flag: str
    root_readme: Path
    docs_dir: Path


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != 1:
        raise ValueError("unsupported i18n manifest schema_version")
    return data


def locale_from(raw: dict[str, Any]) -> Locale:
    return Locale(
        code=str(raw["code"]),
        label=str(raw["label"]),
        flag=str(raw["flag"]),
        root_readme=ROOT / str(raw["root_readme"]),
        docs_dir=ROOT / str(raw["docs_dir"]),
    )


def selector_targets(locales: list[Locale], required: list[str]) -> list[Path]:
    targets = [locale.root_readme for locale in locales]
    targets.extend([ROOT / "docs" / "STATUS.md", ROOT / "docs" / "REVIEWER_GUIDE.md"])
    for locale in locales:
        if locale.code == "en":
            continue
        targets.extend(locale.docs_dir / name for name in required)
    return targets


def resolve_link(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split("#", 1)[0].split("?", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    return (source.parent / unquote(target)).resolve()


def check_selector(path: Path, locales: list[Locale], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing selector target: {path.relative_to(ROOT)}")
        return

    lines = path.read_text(encoding="utf-8").splitlines()
    selectors = [(index, line) for index, line in enumerate(lines) if line.startswith("> 🌐")]
    rel = path.relative_to(ROOT)

    if len(selectors) < 2:
        errors.append(f"{rel}: expected top and bottom language selectors")
        return
    if selectors[0][0] > 8:
        errors.append(f"{rel}: first language selector is not near the beginning")
    if selectors[-1][0] < max(0, len(lines) - 8):
        errors.append(f"{rel}: final language selector is not near the end")

    for position, selector in (selectors[0], selectors[-1]):
        for locale in locales:
            if locale.flag not in selector or locale.label not in selector:
                errors.append(
                    f"{rel}:{position + 1}: selector missing {locale.flag} {locale.label}"
                )
        for raw_target in LINK_RE.findall(selector):
            resolved = resolve_link(path, raw_target)
            if resolved is not None and not resolved.exists():
                try:
                    missing = resolved.relative_to(ROOT)
                except ValueError:
                    missing = resolved
                errors.append(f"{rel}:{position + 1}: broken selector link -> {missing}")


def check_sync_markers(
    locales: list[Locale], canonical_ref: str, errors: list[str]
) -> None:
    expected = canonical_ref[:8]
    for locale in locales:
        if locale.code == "en":
            continue
        for name in ("README.md", "STATUS.md"):
            path = locale.docs_dir / name
            if not path.is_file():
                continue
            matches = SYNC_RE.findall(path.read_text(encoding="utf-8"))
            rel = path.relative_to(ROOT)
            if not matches:
                errors.append(f"{rel}: missing localization sync marker main@XXXXXXXX")
            elif expected not in matches:
                errors.append(
                    f"{rel}: sync marker {matches!r} does not include canonical ref {expected}"
                )


def check_glossaries(
    locales: list[Locale], identifiers: list[str], errors: list[str]
) -> None:
    for locale in locales:
        if locale.code == "en":
            continue
        path = locale.docs_dir / "GLOSSARY.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        missing = [identifier for identifier in identifiers if identifier not in text]
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)}: missing preserved identifiers: {', '.join(missing)}"
            )


def main() -> int:
    try:
        manifest = load_manifest()
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"❌ i18n manifest error: {exc}")
        return 1

    errors: list[str] = []
    raw_locales = manifest.get("locales")
    if not isinstance(raw_locales, list) or not raw_locales:
        print("❌ i18n manifest error: locales must be a non-empty list")
        return 1

    try:
        locales = [locale_from(item) for item in raw_locales]
    except (KeyError, TypeError) as exc:
        print(f"❌ i18n manifest locale error: {exc}")
        return 1

    codes = [locale.code for locale in locales]
    if len(codes) != len(set(codes)):
        errors.append("locales.json: duplicate locale codes")
    if manifest.get("canonical_locale") not in codes:
        errors.append("locales.json: canonical_locale is not declared")

    required = [str(name) for name in manifest.get("required_documents", [])]
    if required != [
        "README.md",
        "QUICKSTART.md",
        "STATUS.md",
        "REVIEWER_GUIDE.md",
        "GRANT_OVERVIEW.md",
        "GLOSSARY.md",
    ]:
        errors.append("locales.json: required_documents contract changed unexpectedly")

    for locale in locales:
        if not locale.root_readme.is_file():
            errors.append(f"missing root README for {locale.code}: {locale.root_readme.relative_to(ROOT)}")
        if locale.code != "en":
            for name in required:
                path = locale.docs_dir / name
                if not path.is_file():
                    errors.append(f"missing {locale.code} document: {path.relative_to(ROOT)}")

    for target in selector_targets(locales, required):
        check_selector(target, locales, errors)

    canonical_ref = str(manifest.get("canonical_content_ref", ""))
    if not re.fullmatch(r"[0-9a-f]{8,40}", canonical_ref):
        errors.append("locales.json: canonical_content_ref must be a Git SHA")
    else:
        check_sync_markers(locales, canonical_ref, errors)

    identifiers = [str(item) for item in manifest.get("preserved_identifiers", [])]
    check_glossaries(locales, identifiers, errors)

    if errors:
        print("❌ i18n integrity validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    localized_count = len(locales) - 1
    target_count = len(selector_targets(locales, required))
    print(
        "✅ i18n integrity OK "
        f"({len(locales)} locales, {localized_count} translations, "
        f"{target_count} selector-bearing documents)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
