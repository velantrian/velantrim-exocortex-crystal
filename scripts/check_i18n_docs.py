#!/usr/bin/env python3
"""Dependency-free structural checks for supported documentation translations."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGS = {
    "de": "Deutsch", "fr": "Français", "es": "Español", "it": "Italiano",
    "ru": "Русский", "zh": "简体中文", "ar": "العربية", "ja": "日本語", "hi": "हिन्दी",
}
REQUIRED = ("README.md", "QUICKSTART.md", "STATUS.md", "REVIEWER_GUIDE.md", "GRANT_OVERVIEW.md", "GLOSSARY.md")
SELECTOR_TOKENS = ("English", "Deutsch", "Français", "Español", "Italiano", "Русский", "简体中文", "العربية", "日本語", "हिन्दी")
errors = []

policy = ROOT / "docs/i18n/TRANSLATION_POLICY.md"
status = ROOT / "docs/i18n/TRANSLATION_STATUS.md"
for p in (policy, status):
    if not p.exists():
        errors.append(f"missing governance file: {p.relative_to(ROOT)}")

for code, label in LANGS.items():
    root_readme = ROOT / f"README.{code}.md"
    if not root_readme.exists():
        errors.append(f"missing root localization: {root_readme.name}")
    lang_dir = ROOT / "docs" / code
    for name in REQUIRED:
        p = lang_dir / name
        if not p.exists():
            errors.append(f"missing localized entry point: {p.relative_to(ROOT)}")

# Root READMEs are the stable navigation surface and must expose all supported languages.
root_readmes = [ROOT / "README.md"] + [ROOT / f"README.{code}.md" for code in LANGS]
for p in root_readmes:
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    missing = [token for token in SELECTOR_TOKENS if token not in text]
    if missing:
        errors.append(f"{p.name}: language selector missing {', '.join(missing)}")

if status.exists():
    text = status.read_text(encoding="utf-8")
    for code, label in LANGS.items():
        if f"`{code}`" not in text or label not in text:
            errors.append(f"translation status missing language row: {code} / {label}")

if errors:
    print("❌ i18n documentation validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(f"✅ i18n documentation OK ({1 + len(LANGS)} languages, {len(LANGS) * (1 + len(REQUIRED))} localized entry points checked)")
