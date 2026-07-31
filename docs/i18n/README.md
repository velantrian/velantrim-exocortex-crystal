# 🌐 Crystal Internationalization

Crystal currently maintains documentation in ten languages. This directory contains the governance and validation layer for that documentation family.

## Files

- [`TRANSLATION_POLICY.md`](./TRANSLATION_POLICY.md) — authority, claim discipline, review and expansion rules;
- [`STATUS.md`](./STATUS.md) — supported locales and maintenance state;
- [`locales.json`](./locales.json) — machine-readable locale and document contract;
- [`../../scripts/check_i18n.py`](../../scripts/check_i18n.py) — pure-standard-library integrity checker.

## Local validation

```bash
python scripts/check_i18n.py
```

The automated checker validates structure and navigation. Human review remains necessary for linguistic quality and semantic equivalence.

## Current decision

The ten-language set is sufficient for the present grant and open-source stage. Maintenance quality has priority over adding further languages without a concrete reviewer or user need.
