# 🔍 Руководство reviewer — Velantrim Crystal

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md)
>
> Эта страница предоставляет русскоязычный маршрут проверки. Она не вводит
> новых claims о runtime, гранте, compliance или security. При расхождениях
> действуют GitHub `main`, [docs/STATUS.md](../STATUS.md) и
> [TEST_REPORT.md](../../TEST_REPORT.md).

## 1. Что такое Crystal

Crystal — публичное, минимальное и проверяемое ядро памяти Velantrim:

- local-first и без обязательной cloud-зависимости;
- claims, привязанные к источникам и явному эпистемическому статусу;
- Guardian + TruthGate как граница автоматического допуска в L3;
- CanonicalView для строго обоснованного чтения;
- TRACE и Receipt как проверяемый слой доказательств;
- локальные backend-реализации SQLite/WAL и embedded graph;
- технические механизмы удаления, ограничения, audit и provenance;
- воспроизводимые тесты и детерминированные evaluation gates.

## 2. Чем Crystal не является

Crystal не утверждает, что является:

- AGI, сознанием, личностью или биологическим эквивалентом мозга;
- гарантией «нулевых hallucinations»;
- полным стеком Titan или Personal ExoCortex;
- системой самoизменения или автоматической самоканонизации;
- продуктом с обязательным внешним LLM, graph или cloud provider;
- юридической GDPR-сертификацией;
- security-сертификацией или production-ready multi-tenant hosting;
- runtime-реализацией любой исследовательской идеи или открытого PR.

## 3. Авторитетные источники

Проверяйте в следующем порядке:

1. GitHub `main` — фактически слитый код;
2. [TEST_REPORT.md](../../TEST_REPORT.md) — baseline тестов и покрытия;
3. [docs/STATUS.md](../STATUS.md) — текущий статус claims и компонентов;
4. [docs/IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) — подробная карта;
5. [docs/ARCHITECTURE.md](../ARCHITECTURE.md) — архитектурные границы;
6. английские грантовые документы — scope и acceptance criteria.

Заметка Notion, roadmap, RFC, prototype или открытый PR не является реализованной
возможностью.

## 4. Чистое воспроизведение

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
git status --short
```

Ожидаемые результаты:

- тесты и coverage gate проходят;
- `eval_gate.py` не сообщает о регрессии;
- созданные artifacts не загрязняют Git working tree;
- точные числа сверяются с [TEST_REPORT.md](../../TEST_REPORT.md).

## 5. Проверка основных контрактов

### 🛡️ Допуск

```text
новый claim
→ classification + evidence
→ Guardian
→ TruthGate
→ оперативная память / допущенный Canon
```

Контрольный вопрос: может ли слабый, неподтверждённый или неверно типизированный
claim обойти предусмотренные gates?

### 🔎 HTTP-запрос

```text
POST /ask или GET /receipt
→ core.query_pipeline.query()
→ уже существующий Canon
→ CanonicalView
→ ответ или ограниченный отказ
```

Контрольный вопрос: остаются ли L0/L1, L3, ESM, outbox, эпизодические связи,
embedding fingerprint и адаптивная верификация неизменными во время
мигрированных HTTP-запросов?

Гарантия намеренно узкая:

- CLI `ask` и `receipt` ещё не мигрированы;
- MCP может инициализировать отсутствующий embedding fingerprint.

### 🔗 TRACE и Receipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Контрольный вопрос: видны ли факты и evidence references, поддержавшие ответ, и
обнаруживается ли drift?

### 🧾 Audit и provenance

```bash
velantrim audit
velantrim audit-verify
velantrim history <fact_id>
```

`history` и per-fact `ProvenanceChain` — разные представления. Документация и
тесты не должны смешивать эти понятия.

## 6. Безопасный запуск HTTP service

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

Проверьте:

- отсутствует fallback token;
- loopback publishing является безопасным default;
- container user непривилегированный;
- API-зависимости опциональны;
- `/ingest` и `/ask` имеют разные контракты.

## 7. Проверка evaluation

Crystal измеряет, среди прочего:

- retrieval `hit@k` и MRR;
- полноту TRACE и метаданных;
- покрытие Evidence Span;
- Receipt replay;
- precision и recall противоречий;
- корректные отказы на границах доверия.

Replay из Titan является документированным prior art, а не текущей возможностью
Crystal и не самoоптимизирующимся runtime.

## 8. Проверка грантовой границы

Reviewer должен чётко разделять существующую baseline и запрашиваемый delta:

```text
существующая протестированная baseline
+
конкретная измеримая финансируемая работа
=
независимо проверяемый deliverable
```

Уже слитые функции нельзя повторно учитывать как оплачиваемую работу. Заявка
находится на рассмотрении; предоставление финансирования не заявляется.

Русское резюме: [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)  
Нормативный источник: [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

## 9. Сигналы риска

🚩 Документ утверждает больше, чем `main` или `STATUS.md`.  
🚩 Исследовательский модуль представлен как runtime Crystal.  
🚩 Перевод расширяет scope, бюджет или compliance claims.  
🚩 Query неожиданно изменяет состояние памяти.  
🚩 Средняя метрика скрывает safety-регрессию или единичный провал.  
🚩 Внешний provider неявно становится обязательным.

## 10. Финальная проверка

После review должны быть понятны ответы на вопросы:

1. Какие claims могут автоматически попасть в Canon?
2. Какие query paths действительно read-only?
3. Как ответ связан с фактами и evidence?
4. Какие границы реализованы, а какие только запланированы?
5. Какой grant delta остаётся после вычитания существующей baseline?

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md)