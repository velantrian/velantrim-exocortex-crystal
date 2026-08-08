# 🇷🇺 Русский маршрут документации

<!-- localization-index-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- d1-source: main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c -->

[Полный русский README](../../README.ru.md) имеет статус `CURRENT` после PR #340.
Он сохраняет назначение, визуальную структуру, mindmap, ASCII-поток, таблицы,
ограничения, Quick Start и навигацию.

Фаза D1 для русского языка обновляет entry/use документы против точного
английского checkpoint `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`:

- [README](../../README.ru.md) — `CURRENT`;
- [Quick Start](./QUICKSTART.md) — `CURRENT` (D1);
- [Текущий статус](./STATUS.md) — `CURRENT` (D1);
- [Статус реализации](./IMPLEMENTATION_STATUS.md) — `CURRENT` (D1);
- [Руководство reviewer](./REVIEWER_GUIDE.md) — `REFRESH_NEEDED` (D2);
- [Глоссарий](./GLOSSARY.md) — `REFRESH_NEEDED` (D4);
- [Обзор гранта](./GRANT_OVERVIEW.md) — `REFRESH_NEEDED` (D4).

## Правило authority

```text
merged code + exact CI
→ English primary source
→ CURRENT Russian translation
```

Перевод не может расширять capability, security, grant, TruthGate или Canon
claims сверх английского источника.

Первичные источники:

- [English README](../../README.md);
- [TEST_REPORT](../../TEST_REPORT.md);
- [Current status](../STATUS.md);
- [Implementation status](../IMPLEMENTATION_STATUS.md);
- [Localization policy](../LOCALIZATION_POLICY.md);
- [Translation status](../TRANSLATION_STATUS.md).

Следующая русская фаза — D2: Reviewer Guide, security/privacy и failure-mode
explanations.
