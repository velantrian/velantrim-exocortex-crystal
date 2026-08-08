# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — основной и нормативный](./README.md) · 🇷🇺 **Русский обзор**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### Проверяемая локальная инфраструктура памяти для надёжных ИИ-систем

Этот файл — **сокращённый неавторитетный обзор**, а не полный перевод документации.
Актуальные инженерные решения, архитектура, безопасность, статус и грантовые утверждения
ведутся на английском. При расхождении действует [README.md](./README.md) и проверяемые
английские документы.

`v0.3.0` · 🧪 **2078 пройдено / 13 пропущено** · 🎯 **100.00% покрытия** · ✅ **9 CI-задач**

**Проверенный runtime-checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.

Crystal разделяет физическое хранение, доказательства, эпистемический допуск и доверенные
чтения. Guardian и TruthGate нельзя обойти через наличие записи, рейтинг поиска или успешную
миграцию.

## Что уже реализовано

- типизированные утверждения, происхождение и точные фрагменты источников;
- Guardian и TruthGate как границы допуска;
- неизменяемые `TrustSnapshot` и `CanonicalView`;
- read-only HTTP, CLI и MCP-запросы;
- TRACE, receipts, ограничения, стирание и явная работа с противоречиями;
- SQLite как обычный локальный профиль;
- проверяемый backup/restore и ограниченный потоковый логический экспорт;
- необязательный PostgreSQL/pgvector импорт в **неактивную** целевую схему с независимой
  проверкой точного состояния.

## Граница хранилищ

```text
SQLite = текущий обычный local-first профиль
PostgreSQL + pgvector = необязательная цель миграции
active=false
нет обычных runtime reads/writes
нет автоматического переключения, cutover, rollback или dual-write
```

Драйвер PostgreSQL устанавливается только через `[postgresql]` и загружается при явной
операторской команде. Успешный импорт — операционное свидетельство, но не активация и не
включение данных в строгий Canon.

## Неизменяемые ограничения смысла

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal не заявляет универсальную истину, нулевые галлюцинации, активный PostgreSQL runtime,
production multi-tenancy, distributed exactly-once, юридическую/GDPR/security сертификацию,
интеграцию с Titan или искусственное сознание.

## Быстрый старт

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## Актуальные английские источники

- [Основной README](./README.md)
- [Отчёт проверки](./TEST_REPORT.md)
- [Текущий статус](./docs/STATUS.md)
- [Матрица реализации](./docs/IMPLEMENTATION_STATUS.md)
- [Политика безопасности](./SECURITY.md)
- [Политика локализации](./docs/LOCALIZATION_POLICY.md)
- [Русский маршрут документации](./docs/ru/README.md)

Заявка NLnet подана и рассматривается; грант и изменение бюджета не заявлены.
