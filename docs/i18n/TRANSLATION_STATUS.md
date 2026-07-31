# Translation Status

> English documentation is authoritative. See [`TRANSLATION_POLICY.md`](TRANSLATION_POLICY.md).

**English synchronization baseline:** `fb3db12e2030d71fd32d30aacf6da91ad80df33d` (2026-07-31)

| Language | Code | Root README | Docs package | Status | Baseline |
|---|---:|---|---|---|---|
| 🇬🇧 English | `en` | `README.md` | `docs/` | authoritative | current `main` |
| 🇩🇪 Deutsch | `de` | `README.de.md` | `docs/de/` | current | `fb3db12e` |
| 🇫🇷 Français | `fr` | `README.fr.md` | `docs/fr/` | current | `fb3db12e` |
| 🇪🇸 Español | `es` | `README.es.md` | `docs/es/` | current | `fb3db12e` |
| 🇮🇹 Italiano | `it` | `README.it.md` | `docs/it/` | current | `fb3db12e` |
| 🇷🇺 Русский | `ru` | `README.ru.md` | `docs/ru/` | current | `fb3db12e` |
| 🇨🇳 简体中文 | `zh-CN` | `README.zh-CN.md` | `docs/zh-CN/` | current | `fb3db12e` |
| 🇸🇦 العربية | `ar` | `README.ar.md` | `docs/ar/` | current | `fb3db12e` |
| 🇯🇵 日本語 | `ja` | `README.ja.md` | `docs/ja/` | current | `fb3db12e` |
| 🇮🇳 हिन्दी | `hi` | `README.hi.md` | `docs/hi/` | current | `fb3db12e` |

## Meaning of status

- **authoritative** — source documentation against which localized claims are checked.
- **current** — required localized entry points exist and the package was synchronized during or after the listed English baseline.
- **review-needed** — English source changed in a way that may affect localized meaning; translation should not be presented as fully synchronized until reviewed.

## Maintenance

When an English documentation change affects architecture, status, grant language, security, setup instructions, terminology, or reviewer guidance, update this matrix in the same PR or mark affected localizations `review-needed`. Pure formatting changes do not require a synchronization reset.
