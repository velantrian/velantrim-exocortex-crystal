# 🔍 Velantrim Exocortex Crystal — глубокий аудит и грантовый анализ

> **Дата аудита:** 2026-07-04 · **Ревизия:** `9822591` (v0.3.0, ветка main)
> **Метод:** полный обход репозитория (код, тесты, CI, документация, git-история) + проверка актуальных грантовых программ.
> **GenAI disclosure:** отчёт подготовлен с помощью AI-ассистента (Claude Code) и предназначен для ревью мейнтейнером — в той же практике прозрачности, что принята в остальных документах репозитория.
> **Приватность:** отчёт не содержит деталей частной переписки с фондами; статус заявок упоминается только в объёме, уже публично зафиксированном в `docs/grants/funding-use-plan.md`.

> **Snapshot boundary:** this report is a dated audit snapshot, not the source of implementation truth.
> The canonical implementation boundary remains `docs/STATUS.md`, `docs/IMPLEMENTATION_REALITY_MATRIX.md`, and `TEST_REPORT.md`.
>
> **Open work boundary:** open PRs and issues are not treated as implemented runtime behaviour unless separately merged into `main` and reflected in the canonical status documents. In particular, PR #206 and issue #211 are follow-up/current work, not part of the audited `main` snapshot.
>
> **External programme note:** grant deadlines, programme status and eligibility are point-in-time observations and must be rechecked before applying.

---

## 🧭 1. Executive summary

**Вердикт: это реальный, работающий, дисциплинированно построенный проект — не витрина и не vaporware.** Ядро verifiable-памяти (TruthGate, hash-chain аудит, replayable receipts, GDPR-механика) действительно реализовано и покрыто тестами, объём которых превышает объём самого кода. Главные риски — не технические, а проектные: один автор, короткая публичная история (~2,5 недели коммитов) и документация, растущая быстрее кода.

| Измерение | Оценка | Комментарий |
|---|:---:|---|
| 🏗️ Техническая зрелость ядра | ⭐⭐⭐⭐☆ | Рабочий MVP-код production-уклона; честные ограничения задокументированы |
| 🧪 Тестовая дисциплина | ⭐⭐⭐⭐⭐ | ~14k строк тестов ≥ ~13k строк кода; CI-гейт покрытия 100% |
| 📜 Документация и честность | ⭐⭐⭐⭐⭐ | «Honesty rule», Reality Matrix, Metaphor-vs-Mechanism — образцово |
| 🛡️ GDPR / verifiability | ⭐⭐⭐⭐☆ | Реализовано по статьям 5/17/18/30/32; hash-chain + HMAC (не Merkle/PKI) |
| 👥 Устойчивость проекта | ⭐⭐☆☆☆ | Соло-мейнтейнер, нет внешних контрибьюторов, история 18 дней |
| 📣 Внешние сигналы (adoption) | ⭐☆☆☆☆ | Нет PyPI-релиза, пользователей, независимых ревью, цитирований |
| 🎯 Грантовая готовность (NLnet-профиль) | ⭐⭐⭐⭐☆ | Сильное попадание в критерии NGI0; слабое место — impact-доказательства |

---

## 🏗️ 2. Как устроен проект

### 2.1 Философия

Три принципа, последовательно проведённые через код и документацию:

> **Graph = Truth · LLM = Language · Memory = Physiology**

LLM — заменяемый «речевой интерфейс»; источником истины является канонический граф фактов, в который ничего не попадает мимо аудируемого **TruthGate**. Это инверсия обычного RAG: не «модель решает, что правда», а «структурированная память решает, что модель имеет право сказать».

### 2.2 Конвейер и слои памяти

```
Query → Retrieve → FactsPack → Trace → Guardian → TruthGate → Answer(+Receipt)
```

| Слой | Реализация | Файл |
|---|---|---|
| **L0** | LRU-кэш в памяти процесса (cap 5) | `core/memory.py` |
| **L1** | SQLite (WAL) — рабочее/pending-хранилище | `core/memory.py` (745 LOC) |
| **L3** | Канонический граф «истины», 4 бэкенда: Mock / SQLite / LadybugDB / Neo4j (`VELANTRIM_L3_BACKEND=auto`) | `core/l3_graph.py` (1033 LOC) |
| **Proof-слой** | Trace / Receipt / Evidence spans | `core/{trace,provenance,evidence}.py` |

Инвариант «прямой MERGE в L3 мимо TruthGate — архитектурный баг» реально энфорсится в write-path (см. `core/pipeline.py`, write-path audit PR #175).

### 2.3 Эпистемическая машина состояний (ESM)

Атомарная единица — **факт** с 8-состоянийной ESM (`Observed → Hypothesized → Supported → Validated → ImmutableCore`, плюс `Contradicted / Deprecated / Collapsed`), валидируемой матрицей переходов с CAS-защитой (#190), и ортогональными осями `claim_type` (WORLD_FACT, EMOTION, OPINION…) и `source_status` (USER_REPORTED, LLM_OUTPUT, DERIVED…). Это продуманная эпистемика, а не декорация — переходы покрыты тестами (`tests/test_esm.py`).

### 2.4 Verifiability: что реализовано на самом деле ✅

| Механизм | Суть | Файл |
|---|---|---|
| 🔗 **Глобальный audit log** | Append-only hash-chain (SHA-256), `verify_audit_log()` пересчитывает всю цепь; лог tamper-evident; при включённом HMAC (`VELANTRIM_AUDIT_KEY`) появляется защита от подделки при условии, что ключ остаётся секретным; content-free (без персональных данных) | `core/audit.py` |
| 🧬 **Per-fact provenance chain** | Отдельная hash-цепь на каждый `fact_id`; спроектирована так, чтобы никогда не ломать GDPR-erasure | `core/provenance_chain.py` |
| 🧾 **Replayable receipts** | `build_receipt()` запечатывает query+answer+citations под SHA-256 (+HMAC); `verify_receipt()` реплеит цитаты против живого канона и детектит drift (ok/erased/modified/…); хранится `claim_sha256`, а не текст | `core/provenance.py` |
| 📍 **Evidence spans (Receipt v2)** | Привязка фактов к источнику: URI + char-span + `source_sha256`/`claim_sha256` | `core/evidence.py` |

⚠️ **Честная граница:** верифицируемость построена на **линейных hash-цепях + симметричном HMAC**. В коде нет Merkle-деревьев и нет подписей на открытых ключах — и репозиторий нигде этого и не заявляет. Важно держать эту же точность во всех грантовых текстах.

### 2.5 GDPR-механика: сильнейшая часть проекта 🛡️

| Статья GDPR | Реализация | Файл |
|---|---|---|
| **Art. 17** (erasure) | Физическое удаление по L0/L1/L3/outbox + immutable tombstone с content-light erasure-метаданными (`fact_id`, timestamp, reason, actor + hash удалённого claim — не сам текст claim); каскад по `DERIVED_FROM` с защитой от циклов | `core/erasure.py` |
| **Art. 18** (restriction) | Флаг `restricted` исключает факт из retrieval и graph-walk | `core/compliance.py` |
| **Art. 30** (record of processing) | `record_of_processing`, `erasure_log` | `core/compliance.py` |
| **Art. 32** (encryption at rest) | Field-level шифрование claim/metadata; Fernet/AES или stdlib-only HMAC-SHA256-CTR encrypt-then-MAC; PBKDF2 200k. **Opt-in**: off by default (identity-функция без ключа), включается `VELANTRIM_ENCRYPTION_KEY` | `core/crypto.py` |
| **Art. 5** (minimisation) | PII-детекция/редакция: EMAIL, IBAN, карта (Luhn), IPv4, PHONE. **Opt-in**: off by default, включается `VELANTRIM_REDACT_PII=1` | `core/pii.py` |

Формулировка в документах корректно осторожная: «GDPR-relevant controls, not a legal certification». 👍

### 2.6 Retrieval, эмбеддинги, LLM

- **Гибридный retrieval:** косинусный recall + multi-hop graph-walk (spreading activation, PPR-lite); рёбра CONTRADICTS/SUPERSEDED_BY имеют вес 0, чтобы опровергнутое не «подкачивалось».
- ⚠️ **Дефолтный эмбеддер — лексический** (`HashingEmbedder`, hashing trick 2048-dim, честно задокументировано «NOT neural semantics»); нейронный `SentenceTransformerEmbedder` — опциональный extra. Vector search в SQLite-бэкенде — честный линейный cosine-скан (ANN отложен на LadybugDB).
- **Генерация:** по умолчанию детерминированный `ExtractiveGenerator` (без LLM и сети); опционально `AnthropicGenerator` со строго заземлённым промптом и graceful fallback. Ключей и сети для работы и тестов **не требуется вообще**.
- **Zero runtime dependencies:** `dependencies = []` в `pyproject.toml` — заявление «pure stdlib runtime» подтверждается.

### 2.7 Прототипы vs runtime 🧪

Здесь важно различать два разных набора файлов, которые легко спутать по названию:

- **`prototypes/`** (`fractal_memory_layer.py`, `hybrid_biological_memory.py`, `immune_crispr_memory_guard.py`, `neurogenesis_dynamic_growth.py`, `research_mode/`) — исследовательские модули, **явно не подключённые к боевому конвейеру** (прямо написано в `prototypes/README.md`: «not part of the Crystal runtime pipeline unless explicitly imported»).
- **`core/`** — по `docs/METAPHOR_VS_MECHANISM.md` (Table A) в runtime реализованы и покрыты тестами **7** био-метафорных механизмов со статусом `Implemented`: Fractal Memory anchoring (`core/fractal.py`, RFC0070 — multi-scale anchoring, не когнитивная Fractal Attention), Epigenetic Adaptation (`core/adaptation.py`, RFC0071 — единый глобальный tag, регулирующий порог TruthGate), Immune Layer + CRISPR Guard (`core/immune.py`, RFC0072 — базовый advisory-скрининг включён всегда, strict-блокировка опциональна через `VELANTRIM_IMMUNE_STRICT`), Neurogenesis (`core/neurogenesis.py`, RFC0073), Concept Emergence (`core/concept.py`, RFC0066), Memory Volition (`core/volition.py`, RFC0065). Единственный модуль с явным флагом «off by default» — **NeuroCore** (`core/neurocore.py`, RFC0068, `VELANTRIM_NEUROCORE`).

✅ Граница, которую важно сохранить в грантовых текстах: это **implemented baseline-механизмы** (детерминированное anchoring/pattern-matching/threshold-adjustment, всё покрыто тестами) — а не биологическая когниция и не полноценный Personal Research Mode («Fractal Memory = Structure + Attention + Consolidation» и т.п. остаются вне runtime). «Реализовано» здесь означает конкретную узкую механику, а не метафору целиком.

---

## 📊 3. Цифры и их верификация

| Метрика | Значение | Статус проверки |
|---|---|---|
| Python-код всего | ~28,4k LOC | ✅ пересчитано в этом аудите |
| — ядро `core/` | ~12,1k + 730 (adapters) | ✅ |
| — тесты | ~14,1k LOC, 69 файлов, 1177 `def test_` | ✅ |
| Markdown-документация | ~33k строк / 85 файлов | ✅ (docs ≈ code!) |
| Заявлено тестов | **1252 passed / 12 skipped, 100% coverage** (`TEST_REPORT.md`) | ✅ **подтверждено прогоном** |
| CI | pytest 3.11/3.12 + `--cov-fail-under=100` + bandit + pip-audit + eval-gate + jsonl-integrity | ✅ конфиг проверен |
| Релизы | Только `v0.3.0-reviewer-preview` — предок текущего HEAD (`git tag --merged 9822591`) | ✅ |
| PyPI | ❌ пакет не опубликован | ✅ проверено |
| История | 52 коммита текущей ветки main, 2026-06-17 → 2026-07-04, автор фактически один | ✅ |

⚠️ **Уточнение по тегам/истории:** теги `v0.1.0`, `v0.1.1`, `v0.2.0` (`git ls-remote --tags`) указывают на **не связанную** с текущим `main` линию коммитов с первым коммитом от **2026-04-08** (`git merge-base --is-ancestor v0.1.0 9822591` → `no`). То есть в какой-то момент история проекта была переписана/сквошена: текущая ветка main начинается заново 2026-06-17 (52 коммита), а старые теги ведут в отрезанную, недостижимую из HEAD линию разработки. Формулировка «52 коммита, 17 июня → 4 июля» относится **только к текущей ветке main**, а не ко всей истории проекта с апреля 2026 — этот нюанс стоит держать в уме при любых грантовых заявлениях о «возрасте» проекта.

**Эмпирическая проверка тестов:** ✅ полный suite прогнан в рамках этого аудита (`pip install -e '.[dev]' && pytest tests/`, ревизия `9822591`): **1252 passed, 12 skipped, 0 failed, total coverage 100.00% (5661 statements), 5 мин 04 сек.** Заявленные в README и `TEST_REPORT.md` цифры полностью соответствуют действительности.

Два безобидных наблюдения: (1) «1252 заявлено vs 1177 `def test_`» — разница объясняется параметризацией, число из `TEST_REPORT.md` подтверждено прогоном; (2) в живом прогоне измеренная поверхность — 5661 statements против 5461 в per-module таблице `TEST_REPORT.md` — сама таблица честно помечена как «predates recent PRs, will be regenerated», стоит обновить при следующем полном аудите.

---

## ✅ 4. Сильные стороны

1. 🧪 **Тестовая культура выше, чем у большинства грантовых заявителей.** Тесты гоняют реальный end-to-end конвейер (не только моки), suite спроектирован работать офлайн без опциональных зависимостей (`tests/conftest.py` — образцовый).
2. 🕯️ **Культура честности как архитектурный принцип.** `IMPLEMENTATION_REALITY_MATRIX.md`, «honesty rule», `METAPHOR_VS_MECHANISM.md`, отказ от «zero hallucination»-клеймов, GenAI-disclosure в грант-документах. Для NLnet-ревьюеров это редкий и заметный сигнал доверия.
3. 🔌 **Zero-dependency локальный runtime** — заявка «local-first, no telemetry, no outbound calls» подтверждается кодом, а не маркетингом.
4. 🛡️ **GDPR-механика реализована по статьям**, а не абстрактно («privacy by design» здесь — конкретные функции с тестами).
5. 🧾 **Полный governance-набор:** AGPL-3.0, CONTRIBUTING, CoC, SECURITY + STRIDE threat model, GOVERNANCE с честным признанием bus-factor, шаблоны issue/PR.
6. 🎯 **Грантовая инфраструктура уже готова:** funding-use-plan с помильными деливераблами M1–M9 = €50k, WP1–WP5, подготовленные ответы на вопросы второго раунда (`reviewer-qa.md`), партиальный план финансирования. Это ровно тот формат, за который NLnet платит.

---

## 🚨 5. Риски и слабые места

| # | Риск | Серьёзность | Комментарий |
|---|---|:---:|---|
| 1 | **Bus-factor = 1.** 50/52 коммитов — один человек; внешних контрибьюторов нет | 🔴 | Главный вопрос любого фонда про устойчивость. Признано в GOVERNANCE.md — но признание ≠ митигание |
| 2 | **Короткая публичная история** (~18 дней) | 🟠 | Ревьюеры видят «свежесозданный» репозиторий; компенсируется только качеством и релизной дисциплиной |
| 3 | **Docs растут быстрее кода** (~33k строк MD ≈ весь Python) | 🟠 | Риск восприятия «документационного проекта». Последние ~30 коммитов почти все `docs:` |
| 4 | **Нет внешних сигналов adoption:** ни PyPI, ни пользователей, ни независимого ревью, ни писем поддержки | 🟠 | Прямо бьёт по impact-критерию NLnet (40% веса) |
| 5 | **Дефолтный семантический поиск — лексический**, ANN — линейный скан | 🟡 | Честно задокументировано, но на демо «semantic memory» без sbert-extra будет слабее ожиданий |
| 6 | **Нет линтера/типизации в CI** (ruff/mypy отсутствуют) | 🟡 | Дешёвое улучшение, заметное аудитору |
| 7 | **HMAC-ключи симметричные** — verifiability доверяет держателю ключа | 🟡 | Для «независимой проверяемости» третьей стороной со временем нужны подписи/якорение |
| 8 | **Расхождение бейджей возможно при дрейфе** (1252 vs 1177 def) | 🟢 | Управляется правилом «только TEST_REPORT.md несёт число» — соблюдать |

---

## 🧩 Current open work not included in this snapshot

This report audits the repository state at revision `9822591`. The following items are important, but are not counted as implemented behaviour in this snapshot:

| Item | Status | Why it matters |
|---|---|---|
| PR #206 — Audit hardening: Ring Zero sync guards, API auth, path sandbox, RRF | Open / not merged at snapshot boundary | Important hardening candidate: secondary L3 sync guard, API token guard, path sandboxing, force-override metadata, RRF wiring. It should be reviewed separately before being treated as implementation truth. |
| Issue #211 — Structural Stress Smoke Test | Open issue / read-only diagnostic scope | Useful Mentaury-style review-ordering diagnostic, but explicitly no Canon writes, no TruthGate integration, no FactsPack integration, and no Crystal runtime mutation. |
| Issue #196 — claim rewrite / validation identity | Open P0/P1 integrity follow-up | Highest-priority semantic integrity gap: validated claim text must not silently change under the same `fact_id` without versioning, reset, or revalidation. |

---

## 🎯 6. Соответствие NLnet NGI0 Commons Fund

Статус: заявка подана и находится на рассмотрении (как публично зафиксировано в `docs/grants/funding-use-plan.md`). Оценка ниже — по опубликованным критериям NGI0 (веса из `docs/grants/reviewer-qa.md`): **техника/осуществимость 30% · релевантность/импакт 40% · value for money 30%**, проходной балл > 5.0/7.

### 6.1 Техническое превосходство и осуществимость (30%) — прогноз: сильно 💪 (~5.5–6/7)

- ✅ Работающее ядро до гранта («the grant hardens and deploys this, it does not start it» — и это правда).
- ✅ Milestone-план идеально ложится в модель оплаты NLnet «за проверяемый деливерабл».
- ✅ Reproducible: стенд поднимается одной командой, тесты офлайн.
- ⚠️ Что спросят: bus-factor (Q: «что будет, если вы выбудете на 3 месяца?»), реалистичность 9 milestone'ов на одного человека, независимость от Anthropic-стека.

### 6.2 Релевантность / импакт (40%) — прогноз: средне, это главный фронт работ 📣 (~4–5/7)

- ✅ Тематика — прямое попадание в NGI-нарратив: digital commons, data sovereignty, local-first, GDPR, AGPL, «reclaim the public nature of the internet».
- ✅ Мультиязычность (M7) и «инфраструктура, а не чатбот» — правильные акценты.
- ❌ Нет доказуемого сообщества/пользователей/инсталляций; нет писем поддержки (шаблоны в `letters-of-support.md` есть — отправленных писем нет).
- ❌ Нет ни одного внешнего кейса «кто-то, кроме автора, это запустил».
- 👉 За 12–15 недель ревью это можно частично закрыть (см. §8).

### 6.3 Value for money (30%) — прогноз: сильно 💶 (~5.5–6/7)

- ✅ €50k на 9 деливераблов с приоритетным партиальным планом — образцовая структура для первого NGI0-гранта.
- ✅ M8 (model-independence) грамотно обоснован как evaluation, а не подписка на API.
- ⚠️ Возможный вопрос: €7k на KB-экспансию (M5) — самый «мягкий» деливерабл, стоит иметь метрики приёмки.

**Итого:** заявка выглядит выше проходного порога по технике и цене; решающим будет impact. **Всё, что усиливает «нас уже кто-то использует и поддерживает», сейчас ценнее любого нового кода.**

---

## 🚀 7. Соответствие moonshot-фондам (профиль Emergent Ventures)

Фонды типа Emergent Ventures (Mercatus Center) оценивают не milestone-планы, а **смелость идеи и ставку на человека**: «zero to one», скорость, потенциал astronomically positive effect, безразличие к регалиям; быстрый путь к самоокупаемости считается плюсом, решение принимается стремительно (нередко — короткий Zoom-разговор сразу после подачи).

**Что в профиле проекта работает на этот формат:**
- 🧠 Контрарная большая идея: «инвертировать RAG — истина живёт в проверяемой памяти, а не в весах модели». Это тезис уровня инфраструктуры, не фичи.
- ⚡ Демонстрируемая скорость исполнения: за ~3 недели — рабочее ядро, 100%-coverage CI, полный governance. Это сильный «ставка-на-человека» сигнал.
- 🌍 Понятный общественный интерес: verifiable AI memory как противовес opaque cloud memory.

**Что этому формату мешает:**
- 📉 Нет истории «пользователи растут» / прототипа, который можно потрогать за 30 секунд (живое demo, видео).
- 🗣️ Нарратив в репозитории заточен под европейского инфраструктурного ревьюера (WP, milestones, GDPR); moonshot-фонду нужен один абзац: *какое невозможное будущее это открывает и почему именно вы*.
- 💵 Отсутствие намёка на путь к самоокупаемости (для EV это «feature, not bug»).

👉 Практический вывод: для таких фондов главный артефакт — **60–90-секундное живое демо + одностраничный manifesto**, не аудит и не test report.

---

## 🔧 8. Что улучшить: приоритизированный план

### 🔥 P0 — до окончания ревью NLnet (следующие 4–10 недель)

1. **🎬 Публичное демо за 60 секунд.** Скринкаст/асциинема: ingest → ask → receipt → tamper → erasure. Одна ссылка в README. Это одновременно усиливает NLnet-impact и закрывает главный пробел для moonshot-фондов.
2. **📦 Релиз на PyPI** (`pip install velantrim-exocortex-crystal` — точное имя пакета из `pyproject.toml`). Короткое имя `velantrim` для CLI-команды уже занято как entry point внутри пакета, но как отдельное *имя пакета на PyPI* оно не зарезервировано — это отдельное решение на будущее, а не то же самое действие. Пакет собран, релиз превращает «репозиторий» в «инфраструктуру, которую можно поставить» и даёт скачивания как метрику.
3. **✉️ Разослать письма поддержки.** Шаблоны в `docs/grants/letters-of-support.md` готовы — нужны 2–4 реальных эндорсмента (университетская группа, библиотека/архив, privacy-NGO, знакомый мейнтейнер FOSS). Для impact-критерия (40%!) это самый дешёвый прирост.
4. **👥 Митигировать bus-factor делом:** позвать хотя бы одного co-maintainer/regular reviewer (пусть с ограниченной ролью), включить в GOVERNANCE.md; 2–3 «good first issue» + разметка контрибьютор-пути.
5. **🧹 Дешёвая техническая гигиена:** ruff + mypy (хотя бы `core/`) в CI; бейдж. Полдня работы, заметный сигнал аудитору.

### 🌱 P1 — ближайшие 2–3 месяца

6. **🧪 Публичный воспроизводимый бенчмарк** против 1–2 базовых RAG-стеков (retrieval hit@k, receipt-replay survival, contradiction P/R) — коротко, с фиксированными corpus/fixtures. «Verifiable» должен быть измерим.
7. **🔐 Дорожная карта asymmetric verifiability:** подписи ed25519 для receipts (или прозрачный лог/anchoring), чтобы проверка не требовала доверия держателю HMAC-ключа. Даже RFC-документ уже усилит заявку.
8. **🌍 Мини-кейс реального использования:** один задокументированный пилот (собственная исследовательская группа, знакомая библиотека, курс) с цитируемым отзывом.
9. **📊 Балансировать коммит-историю:** держать видимую долю `feat:`/`fix:`-коммитов; doc-heavy лента — считываемый риск.

### 🔭 P2 — стратегически

10. **ANN-поиск и нейронные эмбеддинги в default-опыте** (или явный однострочный upgrade-путь) — сейчас разрыв между ожиданием «semantic memory» и лексическим дефолтом.
11. **Юридическое оформление** (ИП/OÜ/vzw/фонд) — многие программы (Horizon cascade, STF) требуют устойчивую сущность-получателя.
12. **Публикация/препринт** об эпистемической машине состояний + verifiable receipts — открывает академические и AI-safety источники финансирования.

---

## 💶 9. Куда ещё подавать: карта грантов (июль 2026)

| Программа | Сумма | Статус / дедлайн | Fit | Комментарий |
|---|---|---|:---:|---|
| **[NGI TALER 14th call](https://nlnet.nl/news/2026/20260601-call.html)** (NLnet) | €5k–50k | **до 1 авг 2026, 12:00 CEST** | 🟡 | Только при честном угле «verifiable receipts/provenance для платёжных экосистем»; не натягивать — NLnet те же ревьюеры |
| **[NGI Fediversity](https://nlnet.nl/fediversity/)** (NLnet) | €5k–50k | **12th call открыт с 1 июня 2026, дедлайн 1 авг 2026, 12:00 CEST** | 🟢 | Реальный угол: verifiable memory / provenance-слой для Fediverse-инстансов и модерации знаний |
| **[Sovereign Tech Fund](https://www.sovereign.tech/programs/fund)** | от €50k | rolling | 🟡→🟢 | Требует статуса «критической инфраструктуры с adoption» — подавать после появления пользователей; отличная цель на 2027 |
| **[Sovereign Tech Fellowship](https://www.sovereign.tech/programs/fellowship)** | контракт 3–12 мес | заявки были до 6 апр 2026; следующий цикл — следить | 🟢 | Формат «оплачиваемый мейнтейнер» идеально бьётся с bus-factor-проблемой |
| **[Coefficient Giving (ex-Open Philanthropy) — Technical AI Safety RFP](https://coefficientgiving.org/funds/navigating-transformative-ai/request-for-proposals-technical-ai-safety-research/)** | часть $40M RFP | 🔴 **закрыт** (приём заявок завершился 15 апр 2025; форма для «revise & resubmit» была открыта до 15 июля 2025) — мониторить следующий цикл RFP | 🟡 | Угол на будущее: «epistemic audit layer / truthful-AI infrastructure»; принимают independent researchers. Использовать `docs/grants/north-america-positioning.md`, когда откроется новый цикл |
| **[Mozilla — Democracy x AI Incubator](https://www.mozillafoundation.org/en/what-we-do/grantmaking/incubator/democracy-ai-cohort/)** | $50k (Tier I) → $250k | дедлайн марта 2026 прошёл; следить за следующей когортой | 🟢 | Категория «better information systems / verification tools» — прямое попадание |
| **[OTF — FOSS Sustainability Fund](https://www.opentech.fund/funds/free-and-open-source-software-sustainability-fund/)** | варьируется | concept notes до 7 мая 2026 — прошёл; цикл повторяется | 🟡 | Фокус internet freedom; проверить соответствие миссии и eligibility |
| **[NGI Open Calls (Horizon cascade)](https://ngi.eu/opencalls/)** | €5k–50k+ | постоянно появляются новые | 🟢 | Открыты для individuals; мониторить ежемесячно — профиль «trustworthy AI / data sovereignty» появляется регулярно |
| **Prototype Fund (DE)** | €47.5k | — | 🔴 | Требуется налоговое резидентство Германии — только если применимо |
| **Emergent Ventures-класс (moonshot)** | $5k–100k+ | rolling, решение быстрое | 🟢 | См. §7: нужен manifesto + живое демо, не milestone-план |
| **GitHub Sponsors / Open Collective** | донаты | сейчас | 🟢 | `FUNDING.yml` уже есть, но всё закомментировано — раскомментировать и включить; даже $10/мес — это «community traction» для NLnet |

**Правило анти-double-dipping** уже зафиксировано в `docs/grants/north-america-positioning.md` (разделение EU/NA-скоупов) — при подаче в несколько фондов держать непересекающиеся деливераблы. ✅

---

## 📌 10. Чеклист на ближайшие 90 дней

- [ ] 🎬 Записать 60-сек демо и вставить в README (неделя 1)
- [ ] 📦 Опубликовать v0.3.x на PyPI (неделя 1–2)
- [ ] ✉️ Отправить 3–5 писем поддержки по готовым шаблонам (недели 1–3)
- [ ] 🧹 ruff + mypy в CI (неделя 2)
- [ ] 💰 Включить FUNDING.yml (неделя 2)
- [ ] 👥 Найти co-maintainer / постоянного ревьюера (недели 2–8)
- [ ] 🧪 Мини-бенчмарк vs baseline-RAG, опубликовать в `docs/benchmarks/` (недели 3–6)
- [ ] 🌍 Один задокументированный пилот-кейс (недели 4–10)
- [ ] 🔍 Мониторить [ngi.eu/opencalls](https://ngi.eu/opencalls/) и следующие циклы Mozilla/STF/OTF (ежемесячно)
- [ ] 🚀 Подготовить one-page manifesto для moonshot-фондов (неделя 2–3)

---

## 📤 Publication recommendation

Recommended handling:

1. Keep this file as a **dated grant/internal audit snapshot**.
2. Do not use it as the canonical implementation-status source.
3. If opened as a PR, open it as a **Draft PR** first.
4. PR title suggestion:

```text
docs(grants): add dated grant audit report
```

5. PR body should explicitly say:

> This is a dated grant/internal audit snapshot.
> It does not replace `TEST_REPORT.md`, `docs/STATUS.md`, or `docs/IMPLEMENTATION_REALITY_MATRIX.md`.
> Open PR #206 and issue #211 are not treated as merged implementation truth.

6. After PR #206 or #196 are merged, this report should either remain unchanged as a dated snapshot or receive a clearly labelled follow-up note.

---

## 🧾 Приложение: методология и границы аудита

**Проверено эмпирически в этом аудите:** структура и объём кода (LOC-подсчёт), содержимое всех ключевых модулей ядра (`core/*`), конфигурация CI и покрытия, git-история и авторство, отсутствие пакета на PyPI, наличие тегов релизов, а также **полный прогон тест-suite с гейтом покрытия** (1252 passed / 12 skipped / 100.00%, см. §3).

**Authoritative baseline:** каноническим источником точного числа тестов остаётся `TEST_REPORT.md` (правило репозитория: только этот файл несёт точную цифру); в данном аудите его значения дополнительно подтверждены живым прогоном.

**Не проверялось:** работа опциональных бэкендов (LadybugDB, Neo4j, sbert, Anthropic), Docker-образ, содержание заявок, поданных в фонды (аудит опирается только на публичные документы репозитория).
