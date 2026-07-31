# 📌 Velantrim Crystal — Текущий статус

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 [日本語](../ja/STATUS.md) · 🇮🇳 [हिन्दी](../hi/STATUS.md)

**Дата статуса:** 31 июля 2026 года  
**Состояние репозитория, использованное для перевода:** `main@c5a34a64`  
**Последний checkpoint с изменением runtime:** PR #265 / `cd6fd44`  
**Нормативная baseline тестов:** [TEST_REPORT.md](../../TEST_REPORT.md)

> Эта страница является переводом статуса. При расхождениях действуют GitHub
> `main`, английский [STATUS](../STATUS.md) и
> [TEST_REPORT.md](../../TEST_REPORT.md).

---

## 🧭 Правило чтения

```text
GitHub Crystal main = публичная истина реализации
Notion Crystal       = синхронизированная карта гранта и стратегии
Titan / Full         = отдельная исследовательская лаборатория
```

Документ, заметка Notion, prototype branch или модуль Titan не является текущей
возможностью Crystal, пока он не реализован, протестирован и слит в Crystal
`main`.

## ✅ Проверенный checkpoint

PR #265 ввёл строгую read-only границу HTTP-запросов:

```text
POST /ingest   → допуск через Guardian + TruthGate
POST /ask      → строго read-only канонический запрос
GET  /receipt  → read-only запрос с Receipt
```

HTTP endpoints `/ask` и `/receipt` не записывают L0/L1 или L3, не переводят ESM,
не обрабатывают outbox, не сохраняют эпизодические связи, не инициализируют
embedding fingerprint и не изменяют адаптивную верификацию.

### Явные остаточные границы

- CLI `ask` и `receipt` остаются на `core.pipeline.run()`;
- `core.pipeline.run()` остаётся совместимым путём, способным выполнять допуск;
- MCP не имеет явных инструментов канонической записи, но поиск может
  инициализировать отсутствующий embedding fingerprint.

Это известные follow-ups, а не скрытые claims реализации.

## 🧪 Baseline проверки

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

CI run `30284938992` завершил все семь постоянных jobs до merge: тесты Python
3.11/3.12, Ruff, security, Docker build, evaluation gate и JSONL integrity.

## 🛡️ Граница публичных claims

Crystal можно описывать как:

- local-first проверяемую инфраструктуру памяти ИИ;
- ядро памяти, ориентированное на источники и provenance;
- систему с контролем допуска Guardian и TruthGate там, где он подключён;
- систему с CanonicalView, TRACE и воспроизводимыми Receipt там, где они подключены;
- runtime на стандартной библиотеке с опциональными адаптерами и интерфейсами;
- проект с техническими механизмами удаления и ограничения, релевантными GDPR;
- независимо тестируемую open-source baseline исследовательского уровня.

Crystal нельзя описывать как:

- Titan или полный Personal ExoCortex;
- автономную когнитивную операционную систему;
- сознательную, живую или биологически эквивалентную мозгу систему;
- универсально истинную или полностью свободную от hallucinations систему;
- юридически GDPR-сертифицированный продукт;
- security-сертифицированный или production-ready multi-tenant сервис;
- систему, обязательно зависящую от внешнего LLM или cloud provider.

## 💶 Статус гранта

Заявка в **NLnet NGI0 Commons Fund** подана и находится на рассмотрении.
Репозиторий не утверждает, что финансирование предоставлено.

```text
ТЕКУЩАЯ BASELINE
    +
ИЗМЕРИМЫЙ ФИНАНСИРУЕМЫЙ DELTA
    =
НЕЗАВИСИМО ПРОВЕРЯЕМЫЙ DELIVERABLE
```

Уже слитая работа остаётся baseline и не учитывается повторно как оплачиваемый
milestone. Нормативные правила поддерживаются в:

- [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

Русское резюме находится в [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md).

## 🧪 Решение по evaluation replay

Детерминированная replay-реализация Titan рассмотрена как prior art. Она не была
скопирована в runtime Crystal.

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

Будущая реализация должна расширять существующий evaluation stack Crystal,
проходить отдельный RFC/issue/PR, оставаться offline и неавторитетной, сохраняя
TruthGate и границы query-path.

## 🔬 Правило для исследований и draft PR

Открытые исследовательские или branding PR не являются истиной реализации. Перед
merge их необходимо rebase на актуальный `main`, повторно проверить грантовые
формулировки и сопоставить с нормативным статусом.

## 📚 Маршрут reviewer

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)
4. [GLOSSARY.md](./GLOSSARY.md)
5. [Нормативный английский статус](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 [日本語](../ja/STATUS.md) · 🇮🇳 [हिन्दी](../hi/STATUS.md)