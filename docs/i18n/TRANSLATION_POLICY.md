# Translation Policy

> **Status:** Documentation governance policy  
> **Authoritative language:** English  
> **Supported set:** English, German, French, Spanish, Italian, Russian, Simplified Chinese, Arabic, Japanese, Hindi

## Purpose

Localized documentation improves accessibility, but it must not create a second source of architectural truth. English project documentation remains authoritative for technical, security, status, grant, and implementation claims.

## Invariants

1. **No stronger claims.** A translation MUST NOT make a capability, implementation status, benchmark, security property, grant outcome, or roadmap commitment stronger than its English source.
2. **Stable contract identifiers.** Contract names and identifiers such as `TruthGate`, `Guardian`, `CanonicalView`, `TRACE`, and `Receipt` remain unchanged unless the English contract itself changes.
3. **Commands stay executable.** Shell commands, API paths, environment variables, filenames, schema keys, and code identifiers are copied exactly unless localization is explicitly part of their syntax.
4. **Grant-facing conservatism.** Localized grant material must preserve qualifiers such as proposed, planned, experimental, partial, shadow, research, and not yet implemented.
5. **English resolves ambiguity.** When localized wording conflicts with English, reviewers and implementers use the English source until the translation is corrected.
6. **No silent architectural edits.** Translation PRs do not change runtime behavior, API contracts, schemas, security policy, or implementation status.

## Synchronization rule

The translation status matrix in `docs/i18n/TRANSLATION_STATUS.md` records the English baseline commit used for synchronization. A localization may be marked `current` only when its required entry points have been reviewed against that baseline or a later English commit.

## Required localized entry points

Each non-English language package should provide:

- root project README (`README.<lang>.md`);
- documentation index (`docs/<lang>/README.md`);
- quickstart;
- status overview;
- reviewer guide;
- grant overview;
- glossary.

## Language navigation convention

Use the same ordered selector across localized entry points:

`🇬🇧 English · 🇩🇪 Deutsch · 🇫🇷 Français · 🇪🇸 Español · 🇮🇹 Italiano · 🇷🇺 Русский · 🇨🇳 简体中文 · 🇸🇦 العربية · 🇯🇵 日本語 · 🇮🇳 हिन्दी`

The selector belongs near the beginning and, where practical, near the end of long localized documents. Do not add another language without updating this policy, the status matrix, required-entry-point checks, and all selectors in one reviewed change.

## Review checklist

Before merging a translation change, verify semantic parity with English, preservation of uncertainty/status qualifiers, technical identifier stability, working relative links, and a docs/tooling-only diff unless the PR explicitly has a separate implementation scope.
