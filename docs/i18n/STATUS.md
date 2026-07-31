# 📊 Localization Status

**Canonical documentation:** English on GitHub `main`  
**Canonical content checkpoint:** `c5a34a64`  
**Localization bundle checkpoint:** `fb3db12e`  
**Supported locales:** 10

| Locale | Root README | Documentation set | Direction | Status |
|---|---|---|---|---|
| 🇬🇧 English | `README.md` | canonical English docs | LTR | authoritative |
| 🇩🇪 Deutsch | `README.de.md` | `docs/de/` | LTR | maintained |
| 🇫🇷 Français | `README.fr.md` | `docs/fr/` | LTR | maintained |
| 🇪🇸 Español | `README.es.md` | `docs/es/` | LTR | maintained |
| 🇮🇹 Italiano | `README.it.md` | `docs/it/` | LTR | maintained |
| 🇷🇺 Русский | `README.ru.md` | `docs/ru/` | LTR | maintained |
| 🇨🇳 简体中文 | `README.zh-CN.md` | `docs/zh-CN/` | LTR | maintained |
| 🇸🇦 العربية | `README.ar.md` | `docs/ar/` | RTL | maintained |
| 🇯🇵 日本語 | `README.ja.md` | `docs/ja/` | LTR | maintained |
| 🇮🇳 हिन्दी | `README.hi.md` | `docs/hi/` | LTR | maintained |

## Automated checks

Run locally:

```bash
python scripts/check_i18n.py
```

The check validates:

- manifest structure and unique locale codes;
- presence of all root READMEs and required localized documents;
- top-and-bottom language selectors;
- selector coverage for every supported locale;
- relative selector-link targets;
- preserved identifiers in localized glossaries;
- synchronization markers in locale index and status documents.

## Maintenance rule

A localization is marked **maintained** only while its package passes the automated gate and its claims remain aligned with the English source. Passing structural checks does not substitute for native-language review of meaning.

## Expansion policy

Ten languages are sufficient for the current grant and open-source stage. Further expansion should be demand-driven rather than decorative. Priority now is synchronization quality, reviewer clarity, and product development.

---

See [`TRANSLATION_POLICY.md`](./TRANSLATION_POLICY.md) and [`locales.json`](./locales.json).
