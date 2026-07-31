# 💶 Обзор гранта — Velantrim Crystal

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 **Русский**
>
> Эта страница является переводом и вспомогательным обзором. Она не заменяет
> поданную заявку или английские документы по milestones, бюджету и acceptance
> criteria. При расхождениях действует английская версия.

## 📌 Статус заявки

Velantrim Crystal подан на рассмотрение в **NLnet NGI0 Commons Fund**.
Репозиторий не утверждает, что финансирование уже предоставлено.

Публичное ядро описывается как локальная, проверяемая и open-source
инфраструктура памяти ИИ. Приоритеты — проверяемая provenance, контролируемый
допуск знаний, локальная работа и воспроизводимые доказательства качества.

## 🧭 Правило baseline / delta

```text
ТЕКУЩАЯ BASELINE
    +
ИЗМЕРИМЫЙ ФИНАНСИРУЕМЫЙ DELTA
    =
НЕЗАВИСИМО ПРОВЕРЯЕМЫЙ DELIVERABLE
```

Это правило не позволяет повторно учитывать уже слитую функцию как
финансируемую поставку.

Если `main` изменится до формального соглашения, матрицу baseline/delta нужно
обновить. Финансируемый delta должен оставаться реальным, измеримым и проверяемым
третьей стороной.

## ✅ Уже существующая baseline

Текущее публичное ядро включает, среди прочего:

- локальную память L0/L1 и graph backends L3;
- границы допуска Guardian и TruthGate;
- типы claims, source status и provenance metadata;
- TRACE и воспроизводимые Receipt;
- baseline Evidence Span;
- сессии импорта, dry-run и curator review;
- технические механизмы удаления, ограничения и audit;
- детерминированную evaluation с CI gates;
- опциональные интерфейсы FastAPI и MCP;
- локальный и provider-independent runtime по умолчанию.

Точная реализация определяется только GitHub `main`,
[docs/STATUS.md](../STATUS.md) и [TEST_REPORT.md](../../TEST_REPORT.md).

## 🧱 Планируемый финансируемый delta

Английская milestone-матрица описывает девять проверяемых направлений:

| Milestone | Краткая цель |
|---|---|
| **M1** | воспроизводимая и локально развёртываемая open-source baseline |
| **M2** | hardened опциональный FastAPI со строгими ролями и безопасными defaults |
| **M3** | усиленные Evidence Span и проверка Receipt |
| **M4** | более широкие, versioned и multilingual evaluation gates |
| **M5** | curated knowledge corpus со ссылками на источники и лицензии |
| **M6** | hardened knowledge adapters и institutional formats |
| **M7** | структурированная multilingual accessibility |
| **M8** | evaluation независимости от model providers |
| **M9** | документация, governance и onboarding reviewers |

Точные суммы, приоритеты и acceptance evidence находятся в:

- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

## 🌍 Русская документация и M7

Этот русский пакет — docs-only улучшение baseline до формальной фиксации гранта.
Он не вводит новый milestone или бюджетную статью.

Его нельзя ретроспективно описывать как полностью поставленный M7 delta. Будущий
финансируемый M7 должен предоставить дополнительную измеримую работу, например:

- поддерживаемую структуру локализации;
- определённый процесс review переводов;
- другие согласованные европейские языки;
- language-specific evaluation cases и quality reports;
- отслеживаемую синхронизацию с releases.

## 🧪 Evaluation replay и M4

Titan содержит детерминированную replay-реализацию, рассмотренную как prior art.
Для Crystal действует:

```text
Документированный prior art ≠ реализованный runtime Crystal
```

Будущий M4 может использовать стабильные digests, baseline/candidate diffs,
versioned fixtures и строгие safety gates. В scope не включаются автоматически:

- live-запись траекторий персональных запросов;
- автоматическая оптимизация или самoизменение;
- прямые или косвенные пути записи в Canon;
- обязательные вызовы внешних providers;
- автоматическое продвижение кандидатов.

## 🔒 Вне scope и границы claims

Текущая фаза не заявляет:

- закрытый SaaS;
- сознание, личность или биологическую cognition;
- «нулевые hallucinations»;
- автономную самоканонизацию;
- production-ready multi-tenant hosting без отдельной security architecture;
- обязательную зависимость от конкретного LLM provider;
- юридическую GDPR- или security-сертификацию;
- полный Personal ExoCortex или Titan как deliverable.

## 🛡️ Reviewer-safe формулировка

> Crystal уже предоставляет протестированное локальное ядро доверия для
> проверяемой памяти ИИ. Запрашиваемое финансирование предназначено для чётко
> ограниченного и измеримого engineering delta, который сделает ядро более
> воспроизводимым, развёртываемым, безопасно эксплуатируемым, multilingual и
> независимо проверяемым.

## 📚 Нормативные источники

1. [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
2. [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
3. [funding-use-plan.md](../grants/funding-use-plan.md)
4. [reviewer-qa.md](../grants/reviewer-qa.md)
5. [STATUS.md](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 **Русский**