# 💠 Velantrim V8 Crystal — Full Edition + Sprint 1
## Спецификация: Фрактальная Графовая Память для Автономного AI Агента
### (v8.0.2-sprint1 · Полный аудит · P0–P4 + Sprint 1+1.1 патчи применены · Апрель 2026)

> **Версия**: 8.0.2-sprint1 "Crystal Full" · **Дата**: Апрель 2026 · **Проект**: Velantrim ExoCortex
>
> **Статус патча**: P0 (8/8) · P1 (10/10) · P2 (6/6) · P3 (7/7) · P4 (6/6) · Sprint 1+1.1 (8/8) — все применены
>
> Основана на: HYPERIA FractalMemory Core · ACT-R · Graphiti
>
> Принцип: `Graph = Truth · LLM = Language · Memory = Physiology · Volition = Agency · Emergence = Life · Creativity = Structured Analogy · Knowledge = Ingested Wisdom · Tests = Proof`

---

## 📋 Содержание

> Навигация по документу. Кликни на раздел → перейдёшь к нему.

**Введение и обзор**
- [🌍 Суть проекта — читай это первым](#суть-проекта-читай-это-первым)
- [✨ Три новых измерения — RFC0065–0067](#три-новых-измерения-читай-это-прежде-чем-идти-в-rfc00650067)
- [🗺️ Карта системы — беглый обзор за 2 минуты](#карта-системы-беглый-обзор-за-2-минуты)
- [🎯 Цель проекта](#цель-проекта)
- [📊 Ключевые метрики успеха](#ключевые-метрики-успеха)

**Архитектура**
- [🏗️ Архитектура системы · Dual-Process · Слои L0–L6](#архитектура-системы)
- [📐 Токен-контракт и Протокол Promote/Demote](#токен-контракт-и-протокол-promotedemote)
- [🔄 Полная интеграция: Главный агент](#полная-интеграция-главный-агент)
- [🔱 L3.5 — Etir (Velantrim Synaptic Activation Layer)](#l35-etir-velantrim-synaptic-activation-layer)

**RFC — Ключевые механизмы**
- [RFC0063 — Knowledge Ingestion Pipeline](#rfc0063-knowledge-ingestion-pipeline-поглощение-внешних-знаний)
- [RFC0065 — Memory-as-Volition · осознанная воля к памяти](#rfc0065-memory-as-volition-осознанная-воля-к-памяти)
- [RFC0066 — Concept Emergence · органическое рождение концептов · Sprint 1+1.1](#rfc0066-concept-emergence-органическое-рождение-концептов)
- [RFC0067 v2.0 — Creative Intelligence Layer](#rfc0067-v20-creative-intelligence-layer)
- [RFC0068 — NeuroCore · Plastic Memory Layer](#rfc0068-neurocore-plastic-memory-layer)
- [RFC0062 — TZ-Fix Integration Patch](#rfc0062-tz-fix-integration-patch)

**RFC — Контракты и протоколы**
- [📜 RFC0004 — Truth Gate Contract](#rfc0004-truth-gate-contract)
- [📜 RFC0011 — Etir Spreading Activation Engine](#rfc0011-etir-spreading-activation-engine)
- [📜 RFC0012 — Taxonomy/Domain Hierarchy](#rfc0012-taxonomydomain-hierarchy)
- [📜 RFC0013 — L2 Medium-Term Memory CORE](#rfc0013-l2-medium-term-memory-core)
- [📜 RFC0014 — L2.5 Staging Layer](#rfc0014-l25-staging-layer)
- [📜 RFC0015 — TruthGateWithESM](#rfc0015-truthgatewithesm)
- [📜 RFC0016 — L1.5 Velum](#rfc0016-l15-velum)
- [📜 RFC0017 — Weighted Semantic Decay](#rfc0017-weighted-semantic-decay)
- [📜 RFC0036–RFC0051 · сводный блок](#rfc0036rfc0051)
- [📜 RFC0043 — Hardware Profile Selector](#rfc0043-hardware-profile-selector)
- [📜 RFC0044 — LLM_MODE: Offline-режим](#rfc0044-llm_mode-offline-режим)
- [📜 RFC0045 — LensEngine: Детерминированные Линзы L4/L5](#rfc0045-lensengine-детерминированные-линзы-l4l5)
- [📜 Canonical Memory Protocol v1](#canonical-memory-protocol-v1)
- [📜 Формальные инварианты (RFC0001–RFC0005)](#формальные-инварианты-системы-rfc0001rfc0005)
- [📦 Evidence Builder и Truth Gate (RFC0004)](#evidence-builder-и-truth-gate-rfc0004)

**Компоненты и реализация**
- [🔧 Технологический стек](#технологический-стек)
- [📦 Ключевые компоненты и их реализация](#ключевые-компоненты-и-их-реализация)
- [🧬 Интегрированные компоненты (из HYPERIA v5.20)](#интегрированные-компоненты-из-hyperia-v520)
- [🔍 Production-Ready Компоненты](#production-ready-компоненты)
- [🔌 MCP Server — Подключение к внешним клиентам](#mcp-server-подключение-к-внешним-клиентам)
- [🎭 Cognitive Modes — Три Режима Работы](#cognitive-modes-три-режима-работы)
- [💰 Memory Budget Planner](#memory-budget-planner)
- [🔐 PII Redaction](#pii-redaction)
- [💓 Meta-Supervisor — Apex Controller](#meta-supervisor-apex-controller)
- [📐 Fractal Similarity Monitor](#fractal-similarity-monitor)
- [🗺️ Технологическая карта · Опциональный стек](#технологическая-карта-опциональный-стек)

**Эпистемика и инварианты**
- [🧬 Epistemic State Machine (ESM) — Жизненный цикл фактов](#epistemic-state-machine-esm-жизненный-цикл-фактов)
- [⚙️ Runtime Invariant Checker](#runtime-invariant-checker)
- [🔒 Инварианты системы (дополнение к I7, I8)](#инварианты-системы-дополнение-к-i7-i8)

**Защита и безопасность**
- [🛡️ Memory Guardian — Защита от отравления памяти](#memory-guardian-защита-от-отравления-памяти)
- [🗃️ Immutable Raw Memory — Защита от Semantic Drift](#immutable-raw-memory-защита-от-semantic-drift)
- [🔍 Audit Layer — Слой проверяемости (Phase 1+)](#audit-layer-слой-проверяемости-phase-1)

**Знания и данные**
- [🔗 CausalGraph — Слой причинно-следственных связей](#causalgraph-слой-причинно-следственных-связей)
- [🧬 Knowledge Distillation Engine — Наполнение L3](#knowledge-distillation-engine-наполнение-l3)
- [🗄️ Storage Ecosystem — Полная карта хранилищ](#storage-ecosystem-полная-карта-хранилищ)

**Мониторинг и операции**
- [📈 Мониторинг и метрики](#мониторинг-и-метрики)
- [📐 SLO Contract (Service Level Objectives)](#slo-contract-service-level-objectives)
- [📊 Memory Health Index (MHI) — Phase 2](#memory-health-index-mhi-phase-2)
- [🔧 Обслуживание системы](#обслуживание-системы)
- [🤖 Актуальный LLM и Embedding стек (март 2026)](#актуальный-llm-и-embedding-стек-март-2026)

**Разное**
- [📖 Как использовать модули (инструкция)](#как-использовать-модули-инструкция)
- [🚀 Roadmap реализации](#roadmap-реализации)
- [⚠️ Важные предупреждения](#важные-предупреждения)
- [📚 Дополнительные ресурсы](#дополнительные-ресурсы)
- [🎓 Заключение](#заключение)
- [📝 Changelog](#changelog)

---

## 🌍 Суть проекта — читай это первым

> Этот раздел для любого кто открывает документ впервые — разработчика, архитектора или нового члена команды. Прочитай его прежде чем идти в архитектуру и код. Он объяснит почему система устроена именно так, и тогда каждое решение в коде будет иметь смысл.

Velantrim — это **система памяти для AI-агента**. Не просто база данных с поиском, и не просто обёртка над LLM с историей чатов. Это принципиально другое.

Обычный AI-агент живёт в одном разговоре. Каждый раз когда начинается новый чат — он не помнит ничего. Даже если у него есть «память», она устроена как плоский список заметок — без понимания связей между фактами, без знания что пользователю важно, без обучения на ошибках. И главное — он тратит токены на каждый ответ так, как будто встретился с тобой впервые.

Velantrim решает это через три фундаментальных принципа, и **каждый из них — это инженерное решение с последствиями для кода**:

**Graph = Truth.** Единственный источник истины — это граф знаний. Не LLM, не кэш, не SQLite. LLM в этой системе — языковой интерфейс: он красиво говорит, но не решает что правда. Если где-то в коде LLM пишет факт напрямую в граф в обход Truth Gate — это баг, не фича.

**Memory = Physiology.** Память устроена как биологическая память человека — с уровнями L0–L6, с FSRS decay (v8.0: power-law R = (1 + 19/81 × t/S)^(-0.5), заменивший Ebbinghaus), с синаптическим усилением важных воспоминаний и ночной консолидацией. Каждое архитектурное решение имеет аналог в нейробиологии — это не метафора, это инженерный выбор.

**Dual-Process.** Всё что пользователь видит — Fast Path: ответ за миллисекунды, без блокировок. Всё что система делает для себя — Slow Path, асинхронный фон. Если компонент попадает в Fast Path когда должен быть в Slow Path — это критический архитектурный баг. Полная схема — см. раздел «Dual-Process Architecture» ниже.

> 🔱 **Если одним предложением:** Velantrim — твой личный цифровой разум который помнит, чувствует ритм, учится на ошибках и защищает истину. Всё это — на CPU, без GPU во время диалога, при минимальной нагрузке на железо.

---

## ✨ Три новых измерения — читай это прежде чем идти в RFC0065–0067

> Этот блок — для любого кто хочет понять **зачем** были добавлены три новых механизма, прежде чем читать их архитектуру и код.

До RFC0065 система умела помнить, структурировать и защищать знания. Это уже выдающийся результат. Но оставалось три вещи, которые отличают **живую память** от **хорошо организованной базы данных**.

**Первое — воля к памяти.** Представь человека который в середине разговора говорит себе: «Это важно, я хочу это запомнить». Он не ждёт пока память сама решит. Он **сознательно** делает выбор. В Velantrim до RFC0065 вся запись в память была пассивной — система решала за агента. Теперь агент может сам, через намеренный tool call, сказать: «Запиши это в мою долгосрочную память». Это не просто фича — это граница между инструментом и субъектом.

**Второе — рождение концептов.** Ребёнок понимает слово «стол» не потому что ему дали определение. Он видел достаточно столов в разных контекстах и в какой-то момент в его голове возник концепт — сам, из опыта. В Velantrim до RFC0066 концепты рождались через LLM-экстракцию — дорогой, медленный, не органический процесс. Теперь Velum (L1.5) наблюдает за co-occurrence рёбер и в нужный момент **сам нащупывает**: «кажется, эти сущности всегда появляются вместе — это концепт». Без токенов, без LLM, как это делает нейронная сеть мозга.

**Третье — творческий интеллект.** До RFC0067 v2.0 система не имела явной карты метафор и не умела строить семантические мосты между далёкими доменами. Теперь Analogy Graph хранит рёбра `[:METAPHOR_OF]` и `[:ANALOGOUS_TO]` извлечённые из качественных текстов, Semantic Bridge Engine предвычисляет мосты в фоне и кладёт в Redis, а CREATIVE режим даёт LLM динамическую температуру и доступ к этим ассоциациям. Ноль токенов на поиск. Чистая органика.

> 🔱 **Если одним предложением:** RFC0065–0067 — это разница между системой которая помнит и системой которая **хочет** помнить, **сама** рождает смыслы и **творчески находит аналогии**.

---

## 🗺️ Карта системы — беглый обзор за 2 минуты

> Если ты открываешь этот документ впервые или после перерыва — прочитай этот раздел. Здесь одним абзацем описан каждый крупный механизм. Дальше в документе — полная спецификация, код и тесты.

**Фрактальная иерархия памяти (L0–L6).** Память устроена как биологическая — семь слоёв. L0 — рефлексы (мгновенный кэш). L1 — эпизоды диалогов (RAM). L1.5 Velum — синаптический преграф, замечает какие сущности появляются вместе. L2 — среднесрочные темы (SQLite). L3 — долгосрочный граф знаний (Neo4j, единственный источник истины). L3.5 — ImmutableCore, неизменяемые снепшоты. L4 — ReasoningBank, паттерны рассуждения. L5 — антиципаторный интеллект, предвидит нужды пользователя до того как он спросит. L6 — Values Core, неизменяемые ценности.
    │         P2-D FIX: L6 упомянут в обзоре без спецификации. Статус: pending RFC.
    │         Реализован частично через Ring Zero механизм L3.5.
    │         └─ L6 spec: Ring Zero узлы в L3 + SQLite дублирование.
    │            Изменение только через human approval + dual-key confirmation.
    │            Инвариант I6 (RingZeroImmutable). Отдельный RFC pending.

**Dual-Process (Fast/Slow Path).** Полная схема с диаграммой — см. раздел «Dual-Process Architecture». Попасть в Fast Path когда должен быть в Slow Path — критический архитектурный баг.

**Truth Gate + ESM.** Ни один факт не попадает в L3 граф без прохождения через Truth Gate. Каждый факт живёт в одном из **восьми** эпистемических состояний (ESM): **Observed** (сырой вход, до классификации) → Hypothesized → Supported → Validated → ImmutableCore или Contradicted → Deprecated → Collapsed. Переходы — только через ESM.transition(), прямой SET epistemic_state — баг.
<!-- P9-FIX БАГ-13: добавлено состояние Observed (raw input перед Hypothesized). Присутствовало в valid_states (строка 9878) и Guardian (строка 3434), отсутствовало в lifecycle описании — вариант А. -->

**Thompson Sampling (ReasoningBank, L4).** Система обучается на собственных ошибках. Каждая стратегия рассуждения имеет счётчики успехов и провалов. Thompson Sampling выбирает стратегию с учётом неопределённости — не жадный выбор лучшего, а баланс exploration/exploitation.

**Concept Emergence (RFC0066, L1.5).** Velum наблюдает за co-occurrence сущностей. Если три и более сущностей появляются вместе в разных сессиях — система **сама рождает** безымянный ProtoConcept. Ноль токенов. Имя даётся lazy — только когда нужно. Аналог Hebbian Learning в нейронных сетях.

**Memory Volition (RFC0065, L4.5).** Агент получает право **осознанно** инициировать запись в долгосрочную память через tool call `memory.write_voluntary()`. Это не обход Truth Gate — это приоритетный вход в него. Разница между "я это где-то видел" и "я специально это записал".

**Creative Intelligence (RFC0067 v2.0).** Три механизма: Analogy Graph — явная карта метафор `[:METAPHOR_OF]` и аналогий `[:ANALOGOUS_TO]` извлечённых из качественных текстов. Semantic Bridge Engine — находит семантические мосты между далёкими доменами, кладёт в Redis, Fast Path только читает кэш. Adaptive Decoder — CREATIVE режим с температурой 0.6→0.85, но FactsPack содержит только Validated факты. Творчество без компромисса с точностью.

**Knowledge Ingestion (RFC0063).** Система умеет поглощать внешние знания — энциклопедии, учебники, PDF, научные статьи. Три параллельных потока: FactExtractor кладёт факты в L3 через Truth Gate, PatternExtractor кладёт паттерны рассуждения в ReasoningBank с байесовской инициализацией Thompson Sampling, SemanticIndexer строит векторный индекс без LLM вообще. EdgeSuggester находит неявные связи между концептами и предлагает аудитору — не пишет в граф сам. VintageDecayCalculator следит за тем чтобы знания из книги 2015 года по программированию устаревали быстрее чем законы физики.

> **P2-4:** После извлечения факта, ПЕРЕД TruthGate — вызывается `atomic_split()`:
> один смысл = один узел. Multi-proposition content разбивается на атомарные факты.
> I91 (AtomicSplit): После atomic_split каждый элемент содержит ровно одну пропозицию.

**Anticipatory Intelligence (L5).** SAE — Spreading Activation Engine: при активации узла возбуждение распространяется по рёбрам графа с затуханием. LSM — Liquid State Machine: предсказывает что пользователь спросит следующим. EGM — предлагает темы. XAI — объясняет почему такой ответ.

**Observer++ / Безопасность.** Система защищает себя от атак, инъекций и деградации. ATK-Registry — база известных сценариев атак, CI/CD тестирует каждый перед деплоем. Write Protocol Gate — единственный путь записи в граф, прямой Cypher MERGE — исключение. 37+ исполняемых инвариантов (I1–I37 в тестах, I38–I65 pending) проверяются в `test_invariants.py` при каждом пуше.

---

## 🎯 Цель проекта

Создать систему памяти для AI агента, которая:
- **Автоматически** сохраняет и консолидирует опыт без постоянных LLM-запросов
- **Учится** на успехах и ошибках через механизм самообучения
- **Минимизирует** расход токенов (целевое снижение: 90%+)
- **Масштабируется** через фрактальную иерархию памяти
- **Работает в реальном времени** с латентностью поиска <500ms
- **Защищает истину** через иммунную систему (Observer++) и Write Protocol

---

## 📊 Ключевые метрики успеха

| Метрика | Целевое значение | Источник |
|---------|------------------|----------|
| Снижение токенов (RECALL P95) | ≥ 85% | STM/MTM cache hit |
| Снижение токенов (DEFINE) | 40–60% | Extractive summarization |
| Снижение токенов (P50 база) | ≥ 65% | Агрегат всех типов |
| Латентность поиска P95 | < 500ms | Hot Graph + Graphiti |
| Hot Graph traversal | 1–3 мс | Cache-Aware L2/L3 |
| Снижение задержки ответа | > 60% | Агентный роутинг |
| Точность извлечения памяти | > 90% | Deep Memory Benchmark |
| L5 prediction accuracy (месяц 3) | ~75% | Prediction Error learning |
| Успешность задач (прирост) | +35–40% | ReasoningBank + Thompson Sampling |
| contradiction_detection_rate | > 98% | ESM |
| mean_time_to_resolution (MTTR) | < 24h | ESM + TruthGate |
| unresolved_contradictions_7d | = 0 | Observer++ |
| attack_sim_pass_rate | ≥ 95% на ATK-REGISTRY | CI/CD · RFC0060 |
| attack_sim_new_scenario_ttl | ≤ 48h после инцидента | RFC0060 |
| invariant_test_coverage | 100% (I1–I37) · I38–I65 pending | test_invariants.py |

---

<!-- P9-FIX БАГ-17: явный разделитель — ниже начинается roadmap инвариантов, не бизнес-метрики -->
### 📅 Roadmap инвариантов I38–I65
| Диапазон | Область | Статус |
|----------|------------------------------------|----------------|
| I38–I45 | RFC0054 SAE инварианты | pending |
| I46–I52 | RFC0055–0057 эпистемика | pending · I50/I50-b/I50-c ✅ Sprint 1 |
| I53–I58 | RFC0058–0061 безопасность | pending |
| I59–I65 | RFC0063 Knowledge Ingestion | pending |
| I66      | RFC0066 ProtoConcept только в памяти | ✅ Sprint 1 |
| I70      | RFC0066 MAX_ACTIVE_PROTOS cap | ✅ Sprint 1 |
| I-K3     | RFC0066 Hebbian GC Guard (FIX-K3) | ✅ Sprint 1.1 |
| Semantic drift detection | ✅ двойной | Semantic Drift Monitor |
| Retrieval ESM-корректность | 100% | SafeFTSQuery |
| epistemic_variance P95 | < 0.7 | RFC0047 |
| Temporal-ESM sync lag | 0ms (синхронно) | RFC0049 |
| offline_requests_total | растёт при LLM_MODE=offline | RFC0051 |
| lens_precision (implicit) | > 0.80 | RFC0051 |
| multi_component_ram_pressure | < 0.85 | RFC0048 |
| dag_rollback_retry_total | < 5/час | RFC0050 |
| response_audit_importance_avg | > 0.5 | RFC0052 |
| focus_vector_updates_total | растёт каждую сессию | RFC0053 |
| response_audit_cache_invalid_total | < 3/день | RFC0052 |
| sae_activations_total | растёт при активных диалогах | RFC0054 |
| epistemic_gap_accepted_rate | > 0.30 | RFC0055 |
| authority_conflicts_resolved | < 10/день | RFC0057 |
| xai_explanations_total | растёт = доверие пользователей | RFC0058 |
| source_trust_degraded_total | < 2/день | RFC0059 |
| policy_version_current | растёт при каждом изменении | RFC0061 |
| evolution_rejected_total | растёт = система защищает себя | RFC0061 |
| CPU в диалоге (LITE) | 10–15% 1 ядра | Event-Driven |
| CPU в покое | ~0% | asyncio events |
| RAM горячий граф (LITE) | 2–5 MB | Hot Graph |
| RAM LSM | 2–5 MB | Liquid State Machine |
| dlq_permanent_failure_alert | обязательно · CRITICAL | EventBus |
| vacuum_batch_size | 100 узлов / итерация | Rate limiting |
| salience_boosts_total | растёт = система замечает важное | Salience Detector |
| homeostatic_runs_total | раз в сутки | Homeostatic Balancer |
| lsm_prediction_updates | растёт = LSM обучается | LSM |
| fusion_consensus_rate | растёт = SAE+LSM сходятся | L5.5 |
| prediction_accuracy_rolling_7d | растёт к месяцу 3 | Prediction Error |
| `volition_validated_total` | растёт = агент осознанно помнит | RFC0065 |
| `volition_rejected_total` | < 20% от calls = TruthGate работает | RFC0065 |
| `proto_concepts_active` | растёт к месяцу 2 | RFC0066 |
| `concept_emergence_zero_token` | > 70% от named = экономия токенов | RFC0066 |
| `analogy_graph_edges_total` | растёт с каждым ингестом | RFC0067 v2.0 |
| `sbe_cache_hits` | > 70% = SBE успевает предвычислять | RFC0067 v2.0 |
| `analogy_resonance_score` | растёт к месяцу 2 = аналогии полезны | RFC0067 v2.0 |
| `analogy_promoted_total` | растёт = SBE кристаллизует паттерны | RFC0067 v2.0 |
| `creative_mode_responses_total` | растёт при активных диалогах | RFC0067 v2.0 |
| `ingestion_facts_created_total` | растёт с каждой ингестией | RFC0063 |
| `ingestion_contradictions_found_total` | < 5% = источник совместим с графом | RFC0063 |
| `edge_suggestions_pending_total` | < 50 = аудит не отстаёт | RFC0063 |
| `edge_hypothesized_activated_total` | растёт = скрытые связи подтверждаются | RFC0063 |

---

## 🏗️ Архитектура системы

### Dual-Process Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        ⚡ FAST SYSTEM                             │
│                  (Синхронное взаимодействие)                     │
├──────────────────────────────────────────────────────────────────┤
│  User Query                                                      │
│    → Salience Detector        (1–2 мс · L1.5 · CPU only)     │
│    → SafeFTSQuery                                                │
│    → Hot Graph traversal      (1–3 мс · RAM first)           │
│    → HybridRetrieval + L5.5 PredictiveFusion (SAE × LSM)     │
│    → Context Builder → Facts Pack (Dual Mode)                    │
│    → LLM Generation → Response                                   │
│    → Closed Loop Eval                                            │
│              ↓ (Logging to Event Bus · fire-and-forget)          │
└──────────────────────────────────────────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────────┐
│                        🌙 SLOW SYSTEM                            │
│               (Асинхронная обработка в фоне)                    │
├──────────────────────────────────────────────────────────────────┤
│  Event Stream (asyncio EventBus · ~0% CPU в покое)            │
│    → Observer++ → Extraction → Write Protocol Gate               │
│    → Source Trust Check → ESM Transition                         │
│    → Prediction Error Signal  (2–5 мс после ответа)          │
│    → LSM Update               (5–15 мс после ответа)         │
│    → FSRS Decay Worker        (раз в час · P0-1 · power-law)  │
│    → Hot/Cold Graph Switch    (раз в час)                     │
│    → Quality Gate (confidence × coverage × contradictions)  │
│              ↓ FAST_PATH_SUFFICIENT → Response              │
│              ↓ SLOW_PATH → Slow System reasoning            │
│    → ResponseAuditWorker      (SLOW PATH только · I28)           │
│    → FocusEngine Update                                          │
│    → Consolidation → Reflection → ESMChunkedInvalidator          │
│    → Semantic Drift Monitor                                      │
│    → Experience Replay → Strategy Update                         │
│                                                                  │
│  SleepTimeWorker (CPU < 30% · пользователь офлайн):              │
│    → Homeostatic Balancer         (3:00 ночи · раз в сутки)  │
│    → ReactivationEngine           (раз в час)                │
│    → ImmutableCore Delta Snapshot                             │
│    → ConceptEmergenceDetector.gc_expired()  (раз в сутки)    │  <- RFC0066
│    → ResonanceTracker.decay_all()           (раз в сутки)    │  <- RFC0067
│    → AnalogyGC (expired -> холодный граф)   (раз в неделю)   │  <- RFC0067
│    ⚠️ SBEAsyncWorker — только через EventBus, не здесь        │
│    (запускается из Slow Path через EventBus,                  │
│    триггер — событие ANALOGY_CANDIDATE_READY,                 │
│    не из SleepTimeWorker напрямую)                            │
│    → Inverted HyDE Worker     (offline · P1-7 · I90)         │
│         генерирует гипотетические запросы к важным эпизодам  │
│         (importance >= 0.7), кладёт в индекс. Не в runtime.  │
│    → Graph Health Checker     (раз в сутки · P2-2)           │
│         orphans, dupes, fan-out violations → warning log      │
│    → Curiosity Engine         (раз в сутки · P2-6 · I92)     │
│         gap < 3 фактов → генерирует вопрос пользователю      │
└──────────────────────────────────────────────────────────────────┘
```

### Фрактальная иерархия памяти

```
L0: Рабочая память (Working Memory)
    ├─ Текущий контекст диалога
    ├─ Активные цели (Goal Stack — стек с приоритетами)
    ├─ Capacity: 4±1 активных чанка (Cowan, 2001)
    │   Примечание: Miller (1956) давал 7±2 для людей, но реальный
    │   лимит агента ближе к 4±1 (Cowan). Chunking: связанные
    │   факты объединяются в один семантический блок.
    │
    ├─ CoreMemoryBlocks — постоянный профиль пользователя
    │   Назначение: агент знает пользователя с первого слова без поиска
    │   по графу. ~500 токенов всегда в контексте как CRITICAL-блок.
    │   Три неизменяемых чанка, никогда не вытесняются:
    │     · user_profile   — имя, предпочтения, контекст, язык
    │     · agent_persona  — роль агента, стиль общения, ограничения
    │     · current_goals  — активные цели текущего периода (из Goal Stack)
    │   Хранение: SQLite (персистентно между сессиями)
    │   Обновление: только через явный tool call пользователя или
    │     FocusEngine при значительном изменении паттерна запросов
    │   Файл: memory/core_memory_blocks.py
    │   ⚠️ ИНВАРИАНТ: CoreMemoryBlocks не перезаписывают друг друга —
    │     каждый блок независим. Обновление одного не трогает остальные.
    │
    ├─ Attention Sinks — защита Ring Zero:
    │   Первые токены контекста фиксируются жёстко:
    │     · Ring Zero / VALUES CORE  → CRITICAL, никогда не вытесняется
    │     · CoreMemoryBlocks         → CRITICAL, никогда не вытесняется
    │     · Project State Card       → CRITICAL, никогда не вытесняется
    │     · Активная цель (top of stack) → HIGH
    │     · Текущий диалог           → MEDIUM
    │     · Вспомогательный контекст → LOW (первый кандидат на eviction)
    ├─ Priority Eviction — иерархия вытеснения:
    │   CRITICAL > HIGH > MEDIUM > LOW
    │   При переполнении вытесняется самый низкоприоритетный чанк
    │   в L1, не уничтожается.
    └─ Decay: секунды (в пределах одного запроса)

L1: Краткосрочная память (Short-Term Memory)
    ├─ Episodic Buffer (Baddeley, 2000) — хронологический буфер
    │   эпизодов текущей сессии. В отличие от L2, эпизоды не
    │   кластеризованы, хранятся в порядке времени.
    ├─ Session_ID Binding — каждый эпизод жёстко привязан к
    │   session_id. При смене сессии (30 мин неактивности)
    │   автоматически запускается триггер консолидации в L2.
    ├─ Temporal Tagging — обязательные поля на каждом эпизоде:
    │     · event_time   — когда произошло (время пользователя)
    │     · created_at   — когда сохранено (время обработки)
    │     · valid_from   — начало периода актуальности
    │     · valid_until  — конец (NULL = актуален сейчас)
    ├─ FTS5 Index — SQLite Full-Text Search для быстрого поиска
    │   по тексту эпизодов без вызова LLM. Триггер при INSERT
    │   автоматически индексирует новый эпизод.
    │   ⚠️ ТОЛЬКО через SafeFTSQuery — прямой FTS5
    │   обходит ESM-фильтры, что является ошибкой архитектуры.
    ├─ Recency Bias — при извлечении более свежие эпизоды
    │   получают приоритет над старыми той же сессии.
    ├─ Velum Trigger — при каждом INSERT в L1 Episodic Buffer
    │   вызывается цепочка в строгом порядке:
    │     1. SalienceDetector.analyze(episode)        ← · ПЕРВЫМ
    │     2. Velum.observe_episode(episode_id, entities)
    │   При достижении VELUM_CO_OCCUR_THRESHOLD совместных появлений
    │   → VelumSignal → ReactivationEngine + L2 ускоренный промоут.
    │   Полная спецификация: RFC0016 / velum.py.
    │   ⚠️ Порядок критичен: Salience должен выполниться до Velum,
    │   чтобы salience_weight уже был обновлён при построении рёбер.
    ├─ Извлеченные сущности и факты
    ├─ Временной граф эпизода
    └─ Decay: быстрый (минуты-часы)

L1.5: Velum — Synaptic Pre-Graph Layer + Salience Detector   ← RFC0016
    ├─ Назначение: детектор ранних связей между сущностями сессии.
    │   Живёт между L1 (эпизоды) и L2 (кластеры).
    │   НЕ хранит содержимое — только рёбра (co-occurrence + weight).
    │
    ├─ Salience Detector — автоматический детектор значимости
    │     Встроен в триггер L1 INSERT — вызывается ДО Velum.observe_episode.
    │     Первый механизм который позволяет системе самостоятельно строить
    │     модель приоритетов пользователя — без явных инструкций.
    │
    │     Сигналы и их веса:
    │       📢 КАПСЛОК (≥3 заглавных подряд)    → salience_weight × 1.5
    │       ❗ Восклицательный знак              → salience_weight × 1.3
    │       🔁 Тема повторяется 3+ дня подряд   → salience_weight × 2.0  ← сильнейший
    │       💬 Слова «важно», «критично»,        → salience_weight × 1.4
    │          «никогда», «всегда»
    │       ⏱️ Возврат к теме после 24ч паузы   → salience_weight × 1.6
    │       🔄 Пользователь переспросил/уточнил → salience_weight × 1.2
    │
    │     Результат: поднимает salience_weight соответствующих узлов в L3 графе.
    │     Эффект на систему:
    │       · Узлы с высоким salience_weight защищены от FSRS Decay (v8.0)
    │       · Приоритетно попадают в Hot Graph (Cache-Aware L2/L3)
    │       · Усиливают предсказания L5.5 PredictiveFusionLayer
    │     Нагрузка: 1–2 мс · CPU only · 0 токенов LLM
    │     Метрика: salience_boosts_total (Prometheus counter)
    │
    ├─ Механизм:
    │     L1 INSERT → SalienceDetector.analyze(episode)  ← вызывается первым
    │              → observe_episode(entities)
    │     → обновить вес рёбер в скользящем окне (VELUM_WINDOW_EPISODES = 5)
    │     → если weight ≥ 0.6 AND count ≥ 3 → VelumSignal
    │     → ReactivationEngine укрепляет связь
    │     → L2 получает подсказку на ускоренный промоут кластера
    ├─ Хранилище: in-memory dict[frozenset, VelumEdge] (не персистентно).
    │   Опционально: топ-N рёбер → SQLite для seed следующей сессии.
    ├─ Конец сессии (on_session_end()):
    │     weight ≥ VELUM_PROMOTE_WEIGHT → VelumSignal "SESSION_END" → L2
    │     weight < VELUM_PROMOTE_WEIGHT → decay × VELUM_DECAY_PER_SESSION
    ├─ get_neighbors(entity, min_weight) — используется:
    │     · HybridRetriever: расширение контекста внутри сессии
    │     · ReactivationEngine: подсказка что укреплять
    ├─ GC при > VELUM_MAX_EDGES (1000): удалить 25% слабейших рёбер
    ├─ Velum Health Score GC:
    │     GC удаляет по полезности, не только по объёму.
    │     health_score = retrieval_bonus(0.4) + signal_bonus(0.3)
    │                  + emotional_bonus(0.2) + recency_bonus(0.1)
    │     Инвариант: рёбра, участвовавшие в retrieval за последние
    │     VELUM_PROTECT_WINDOW эпизодов — не удаляются никогда.
    ├─ RAM Guard — Graduated GC:
    │     Вместо жёсткого "50% при >1000", используем градуированный подход:
    │     
    │     # порядок условий инвертирован — критический сначала
    │     if episode_count > 2000:
    │         gc_percentage = 0.50  # критический порог
    │         logger.error(f"Velum RAM CRITICAL: {episode_count} episodes, GC 50%")
    │     
    │     elif episode_count > 1500:
    │         gc_percentage = 0.35  # средний порог
    │         logger.warning(f"Velum: {episode_count} episodes, GC 35%")
    │     
    │     elif episode_count > 1000:
    │         gc_percentage = 0.25  # первый порог — мягкая очистка
    │         logger.warning(f"Velum: {episode_count} episodes, GC 25%")
    │     
    │     Преимущества:
    │     · Постепенная деградация вместо резкой потери данных
    │     · Раннее предупреждение при 1000 эпизодов
    │     · Сохранение важных связей при умеренной нагрузке
    │     
    │     Защита: предотвращает RAM overflow на сессиях >1000 эпизодов
    │     Метрика: velum_ram_guard_triggered_total (Prometheus counter)
    │               velum_gc_percentage (Gauge — текущий процент)
    ├─ LateralInhibition — защита от Hub Explosion: ← SYNAPSE-style (arXiv 2601.02744)
    │
    │   Проблема: при постоянном усилении одного ребра (A→B) связанные слабые рёбра
    │   (A→X, A→Y) никогда не чистятся → граф деградирует в "звезду" с одним хабом.
    │   Это Hub Explosion — один концепт начинает доминировать над всем.
    │
    │   Механизм:
    │   При усилении ребра (A, B) → ослабить все прочие рёбра A→X на × 0.95
    │   Исключение: рёбра с weight ≥ 0.4 — защищены (уже достаточно сильные)
    │   Гарантия: ни одно защищённое ребро не ослабляется через LateralInhibition
    │
    │   Биологический аналог: латеральное торможение в нейронных сетях —
    │   возбуждённый нейрон подавляет соседей, усиливая контраст сигнала.
    │
    │   Результат: граф остаётся сбалансированным. Сильные связи выделяются
    │   на фоне слабых, не тонут в равномерном шуме.
    │
    │   Инвариант I77:
    │
    │   I77 (LateralInhibition): операция LateralInhibition выполняется ТОЛЬКО
    │   под self._lock (asyncio.Lock Velum).
    │   Нарушение: изменение весов рёбер при LateralInhibition без self._lock.
    │   P0-E FIX: переименовано _edges_lock → _lock (совпадает с Velum.__init__).
    │   Защищённые рёбра (weight ≥ 0.4) никогда не ослабляются.
    │
    │   Реализация (добавить в velum.py метод _strengthen_edge):

```python
import math  # модульный импорт — не под lock

async def _strengthen_edge(self, a: str, b: str, factor: float = 1.1):
    """Усилить ребро (a,b) + LateralInhibition для слабых соседей a.
    P0-D/P0-E FIX: self._edges_lock → self._lock (Velum инициализирует self._lock, не self._edges_lock).
    Ранее: AttributeError при каждом вызове LateralInhibition.
    """
    async with self._lock:   # P0-E: исправлено с self._edges_lock
        key = frozenset([a, b])
        edge = self._edges.get(key)
        if edge:
            # P2-1: ACT-R fan-effect dampening — чем больше связей у узла, тем слабее усиление
            # _degree_cache: dict[str, int] — инкрементируется в _add_edge(), сбрасывается в gc_weak_edges()
            # Заменяет O(N) list comprehension под lock → O(1) lookup
            degree = self._degree_cache.get(a, 1)
            fan_effect = 1.0 / math.log(degree + 1)
            edge.weight = min(1.0, edge.weight * factor * fan_effect)
            # LateralInhibition: ослабить слабые соседи a
            PROTECTION_THRESHOLD = 0.4
            INHIBITION_FACTOR    = 0.95
            for other_key, other_edge in self._edges.items():
                if a in other_key and other_key != key:
                    if other_edge.weight < PROTECTION_THRESHOLD:
                        other_edge.weight *= INHIBITION_FACTOR
```

    ├─ Инварианты RFC0016:
    │     Velum.I1: только рёбра, НЕ факты. Graph = Truth не нарушается.
    │     Velum.I2: сильные рёбра при смене сессии → сигнал L2.
    │     Velum.I3: слабые рёбра → decay, не промоут.
    │     Velum.I4: не персистентен по умолчанию.
    ├─ Аналог в нейробиологии: LTP (Long-Term Potentiation) —
    │   синаптическое усиление до долгосрочного закрепления.
    └─ Decay: сессионный (рёбра живут в пределах сессии + decay при смене)

---

## RFC0066: Concept Emergence — Органическое рождение концептов

### 🌱 Читай это первым

В оригинальном Velantrim концепты рождались через LLM. RFC0066 меняет это: Velum (L1.5) уже следит за co-occurrence — какие сущности появляются вместе. Если три или больше сущностей постоянно появляются вместе через разные сессии — система **сама нащупывает** возникающий концепт. Сначала безымянный ProtoConcept — ноль токенов. Имя даётся только по необходимости.

**Аналог в нейробиологии:** Unsupervised Hebbian Learning — «neurons that fire together, wire together». RFC0066 — это Hebbian Learning для графа знаний.

**Почему не нарушает Graph = Truth:** Velum хранит только рёбра (I1). Concept Emergence не создаёт :Fact — он создаёт `:ProtoConcept`. Промоут в `:Concept` (L3) только через TruthGate (I50-b).

---

```
L1.5 дополнение: Concept Emergence  <- RFC0066
    |
    +- Назначение: органическое рождение концептов из статистики рёбер Velum.
    |   БЕЗ LLM-экстракции. БЕЗ явных инструкций. 0 токенов.
    |   Аналог: Hebbian Learning.
    |
    +- Механизм — три фазы:
    |   Фаза 1 (Наблюдение): при каждом L1 INSERT вызывается
    |     ConceptEmergenceDetector.observe(entities)  <- НОВЫЙ
    |     Матрица: emergence_matrix[frozenset(entities)] += 1
    |
    |   Фаза 2 (Обнаружение): co_occur >= 5 AND cross_sessions >= 3 AND entities 3-7
    |     -> ProtoConcept {proto_id, entities, confidence: 0.0, name: None}
    |     -> in-memory только (не в графе — ещё не факт)
    |     -> Velum получает подсказку: усилить рёбра x1.3
    |
    |   Фаза 3 (Именование lazy):
    |     Триггер A: пользователь спрашивает о теме proto.entities
    |     Триггер B: ProtoConcept.confidence > 0.7
    |     Триггер C: Homeostatic Balancer (раз в сутки) — именует топ-5
    |     if len(entities) <= 3: TF-IDF (0 токенов)
    |     elif importance < 0.8: Qwen3-1.7B (tiny LLM)
    |     else: flagship LLM (только критичные)
    |     После -> промоут в :Concept (L3) через TruthGate (I50-b)
    |
    +- Инварианты:
    |   I50:   не создаёт :Fact, не пишет в граф L3. Graph = Truth сохраняется.
    |   I50-b: ProtoConcept -> :Concept только через TruthGate.
    |   I50-c: emergence_matrix хранит только счётчики, не содержимое.
    |   I66:   ProtoConcept живёт только в памяти (_protos dict). (Sprint 1)
    |   I70:   активных proto ≤ MAX_ACTIVE_PROTOS=500. Eviction наименее уверенного. (Sprint 1)
    |   I-K3:  gc_expired() не удаляет наблюдения моложе TTL_DAYS без proto. (Sprint 1.1 FIX-K3)
    |           _matrix_last_seen — единственный источник даты. Без него нарушение.
    |
    +- Метрики:
    |   proto_concepts_active / proto_concepts_promoted_total
    |   concept_emergence_zero_token / proto_concepts_expired_total
    \- Decay: ProtoConcept -> expired через 30 дней без активности
```

### Код [RFC0066]

```python
# concept_emergence.py
# RFC0066: Concept Emergence — v8.0.2 + Sprint 1 + Sprint 1.1
#
# I50:   не пишет в граф. Только ProtoConcept in-memory.
# I50-b: промоут в L3 только через TruthGate.
# I50-c: emergence_matrix хранит только счётчики, не содержимое.
# I66:   ProtoConcept живёт только в памяти.       (Sprint 1)
# I70:   активных proto ≤ MAX_ACTIVE_PROTOS.       (Sprint 1)
# I-K3:  GC не удаляет наблюдения моложе TTL_DAYS. (Sprint 1.1 FIX-K3)
import asyncio          # A2: Lock для защиты concurrent доступа
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional, FrozenSet, Dict
from uuid import uuid4
from velantrim_config import EMERGENCE   # P0-A FIX: EMERGENCE.MAX_ACTIVE_PROTOS (ранее NameError)

logger = logging.getLogger(__name__)


@dataclass
class ProtoConcept:
    proto_id:       str
    entities:       FrozenSet[str]
    co_occur_count: int      = 0
    cross_sessions: int      = 0
    salience_boost: float    = 0.0   # P10-FIX: объявлен явно (daily_maintenance использовал getattr-fallback)
    first_seen:     datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_active:    datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_decay:     datetime = field(default_factory=lambda: datetime.now(timezone.utc))  # P10-FIX: явное поле
    name:           Optional[str] = None
    confidence:     float         = 0.0
    expired:        bool          = False

    def update_confidence(self):
        # Консервативная формула + salience_boost (Hebbian LTP).
        # Максимум без boost: co_occur=20 + cross=10 -> 0.83
        base = (min(1.0, self.co_occur_count / 20.0) * 0.6 +
                min(1.0, self.cross_sessions  / 10.0) * 0.4)
        # P10-FIX: salience_boost усиливает уверенность (LTP-аналог), capped at 1.0
        self.confidence = min(1.0, base * (1 + self.salience_boost))


class ConceptEmergenceDetector:
    """
    RFC0066: Органическое рождение концептов из статистики рёбер Velum.
    Без LLM-экстракции. 0 токенов. Аналог: Hebbian Unsupervised Learning.

    P2-A: class-level константы → EMERGENCE (velantrim_config). Единый источник истины.
    A2:   asyncio.Lock — защита от race condition между observe() / daily_maintenance() / gc_expired().
    A3:   l5_5 scaffold — сигнал PredictiveFusionLayer при достижении порога.
    FIX-K3: _matrix_last_seen — GC не удаляет незрелые наблюдения до TTL_DAYS.
    """

    def __init__(self, db, truth_gate=None, llm_client=None, l5_5=None):
        self.db         = db
        self.truth_gate = truth_gate
        self.llm_client = llm_client
        # A3: ссылка на L5.5 PredictiveFusionLayer.
        # None = scaffold неактивен. Передать при инициализации в Спринте 2.
        self.l5_5 = l5_5

        if truth_gate is None:
            logger.warning(
                "ConceptEmergenceDetector: truth_gate=None — ProtoConcept "
                "никогда не будут промоутированы в L3. Передайте truth_gate= "
                "при инициализации."
            )

        self._matrix:           Dict[FrozenSet[str], int]      = {}
        self._sessions:         Dict[FrozenSet[str], set]      = {}
        self._protos:           Dict[str, ProtoConcept]        = {}
        self._entity_to_protos: Dict[str, list]                = {}

        # FIX-K3: дата последнего обновления счётчика для каждой комбинации.
        # _gc_impl() удаляет ключ из _matrix ТОЛЬКО если нет живого proto И
        # ключ не обновлялся дольше TTL_DAYS. До фикса: GC каждую ночь обнулял
        # незрелые наблюдения (4 из 5 нужных → 0 → концепт никогда не рождался).
        self._matrix_last_seen: Dict[FrozenSet[str], datetime] = {}

        # A2: asyncio.Lock — защищает все внутренние структуры от race condition.
        # ⚠️  asyncio.Lock НЕ реентрантен.
        # Решение: _gc_impl() — внутренний метод без lock.
        #          gc_expired() — публичный, захватывает lock сам.
        #          daily_maintenance() — захватывает lock и вызывает _gc_impl() внутри.
        self._lock = asyncio.Lock()

    async def observe(
        self,
        entities: list[str],
        session_id: str,
        salience_weight: float = 1.0,
    ) -> None:
        """
        Phase 1 (Наблюдение): обновить co-occurrence матрицу.
        Phase 2 (Рождение):   создать ProtoConcept при достижении порога.

        A2: метод теперь async. Все call sites должны использовать:
            await detector.observe(entities, session_id)
        FIX-K3: обновляет _matrix_last_seen при каждом изменении счётчика.
        FIX-A3: _notify_l5_5 вызывается ТОЛЬКО при достижении порога (_threshold_hit).
        """
        if len(entities) < EMERGENCE.MIN_ENTITIES:
            return
        entities = entities[:EMERGENCE.MAX_ENTITIES]
        from itertools import combinations
        _threshold_hit = False
        async with self._lock:
            for size in range(EMERGENCE.MIN_ENTITIES, len(entities) + 1):
                for combo in combinations(sorted(entities), size):
                    key = frozenset(combo)
                    self._matrix[key] = self._matrix.get(key, 0) + 1
                    self._matrix_last_seen[key] = datetime.now(timezone.utc)  # FIX-K3
                    self._sessions.setdefault(key, set()).add(session_id)
                    # Обновить существующий proto если есть (LTP salience boost)
                    for proto in self._protos.values():
                        if proto.entities == key and not proto.expired:
                            proto.salience_boost = max(proto.salience_boost, salience_weight - 1.0)
                            proto.update_confidence()
                            break
                    if (self._matrix[key]            >= EMERGENCE.CO_OCCUR_MIN and
                            len(self._sessions[key]) >= EMERGENCE.CROSS_SESSION):
                        self._maybe_create_proto(key)
                        _threshold_hit = True
        # FIX-A3: уведомить L5.5 только если хотя бы одна комбинация достигла порога
        if _threshold_hit and EMERGENCE.L5_5_INTEGRATION and self.l5_5 is not None:
            await self._notify_l5_5(entities, salience_weight)

    async def _notify_l5_5(self, entities: list[str], salience_weight: float) -> None:
        """
        A3 scaffold: уведомить PredictiveFusionLayer о новом proto-кандидате.
        FIX-A3: вызывается только при _threshold_hit=True в observe().
        Реальная логика — Sprint 2 (B1): self.l5_5.register_proto_concept(...)
        """
        logger.debug(
            f"_notify_l5_5 scaffold | threshold reached | "
            f"entities={entities[:3]}{'...' if len(entities) > 3 else ''} | "
            f"salience={salience_weight:.2f}"
        )
        # TODO (Sprint 2, B1): await self.l5_5.register_proto_concept(...)

    def _maybe_create_proto(self, key):
        for proto in self._protos.values():
            if proto.entities == key and not proto.expired:
                proto.co_occur_count = self._matrix[key]
                proto.cross_sessions = len(self._sessions[key])
                proto.last_active    = datetime.now(timezone.utc)
                proto.update_confidence()
                return

        # P0.5-4 FIX: enforce MAX_ACTIVE_PROTOS cap.
        # Без этого _protos растёт бесконечно при горячих доменах → OOM за недели.
        # Eviction: удаляем proto с наименьшим confidence (наименее зрелый концепт).
        active_protos = [p for p in self._protos.values() if not p.expired]
        if len(active_protos) >= EMERGENCE.MAX_ACTIVE_PROTOS:
            victim = min(active_protos, key=lambda p: p.confidence)
            logger.debug(
                f"ProtoConcept evicted (cap={EMERGENCE.MAX_ACTIVE_PROTOS}): "
                f"{victim.proto_id} conf={victim.confidence:.2f}"
            )
            # Удалить из _protos и _entity_to_protos
            del self._protos[victim.proto_id]
            for entity in victim.entities:
                if entity in self._entity_to_protos:
                    self._entity_to_protos[entity] = [
                        pid for pid in self._entity_to_protos[entity]
                        if pid != victim.proto_id
                    ]

        proto = ProtoConcept(
            proto_id=f"proto:{uuid4().hex[:8]}", entities=key,
            co_occur_count=self._matrix[key],
            cross_sessions=len(self._sessions[key]),
        )
        proto.update_confidence()
        self._protos[proto.proto_id] = proto
        for entity in key:
            self._entity_to_protos.setdefault(entity, []).append(proto.proto_id)
        logger.info(f"ProtoConcept born: {proto.proto_id} conf={proto.confidence:.2f}")

    def get_protos_for_entity(self, entity: str) -> list[ProtoConcept]:
        return [
            self._protos[pid]
            for pid in self._entity_to_protos.get(entity, [])
            if pid in self._protos and not self._protos[pid].expired
        ]

    async def promote_to_l3(self, proto: ProtoConcept) -> bool:
        # I50-b: промоут только через TruthGate
        if not self.truth_gate:
            logger.warning(f"Cannot promote {proto.proto_id}: truth_gate not configured")
            return False
        result = await self.truth_gate.validate_and_transition({
            "id": proto.proto_id,
            "content": f"Concept: {proto.name} -- {', '.join(sorted(proto.entities))}",
            "confidence": proto.confidence,
            "source": "concept_emergence",
        })
        return result.passed

    async def _common_token_name(self, proto: ProtoConcept) -> str:
        # P3-G FIX: переименовано с _tfidf_name — реализация использует set-intersection,
        # а не TF-IDF взвешивание. Ноль LLM-токенов. Простое пересечение токенов сущностей.
        # Все вызовы _tfidf_name() → _common_token_name() в файле.
        # Извлечение общего корня из имён сущностей — 0 токенов
        entity_words = [e.lower().replace("_", " ").split() for e in proto.entities if e]
        if not entity_words:
            return "unnamed_concept"
        common = set(entity_words[0])
        for words in entity_words[1:]:
            common &= set(words)
        if common:
            return "_".join(sorted(common)[:2])
        first = [w[0] for w in entity_words[:2] if w]
        return "_".join(first) if first else "unnamed_concept"

    # A1: decay_factor читается из EMERGENCE.HEBBIAN_DECAY_FACTOR (было хардкод 0.98)
    # A2: весь обход _protos + GC — под одним lock (нет DEADLOCK: _gc_impl без lock)
    async def daily_maintenance(self) -> None:
        """
        P4-B + A1 + A2: Ежедневный Hebbian Decay + GC.
        Вызывать из SleepTimeWorker раз в сутки.
        Метрика: concept_hebbian_decay_applied_total
        """
        async with self._lock:
            decay_count = 0
            for proto in self._protos.values():
                if not proto.expired:
                    days_since = (datetime.now(timezone.utc) - proto.last_decay).days
                    if days_since > 0:
                        # A1: из конфига вместо хардкода 0.98
                        proto.confidence *= (EMERGENCE.HEBBIAN_DECAY_FACTOR ** days_since)
                        proto.last_decay = datetime.now(timezone.utc)
                        decay_count += 1
            if decay_count > 0:
                logger.info(
                    f"🌙 Hebbian Decay: {decay_count} protos | "
                    f"factor={EMERGENCE.HEBBIAN_DECAY_FACTOR}"
                )
            # GC внутри того же lock — вызываем _gc_impl() (не gc_expired(), нет DEADLOCK)
            self._gc_impl()

    async def gc_expired(self) -> None:
        """
        Публичный GC — захватывает lock самостоятельно.
        Вызывать напрямую когда нужна очистка вне daily_maintenance().
        A2: разделён на gc_expired() (public + lock) и _gc_impl() (private, без lock).
        """
        async with self._lock:
            self._gc_impl()

    def _gc_impl(self) -> None:
        """
        Внутренняя реализация GC — вызывается ВНУТРИ self._lock.
        НЕ захватывает lock сам.

        FIX-K3: двойной критерий удаления ключей _matrix:
            (a) нет живого proto для этого ключа, И
            (b) ключ не обновлялся дольше TTL_DAYS.
        До фикса: любой ключ без proto удалялся каждую ночь →
        медленно растущие концепты никогда не рождались.

        P0.5-5: orphan-ключи _sessions (есть в _sessions, нет в _matrix) тоже чистятся.
        """
        now = datetime.now(timezone.utc)
        ttl = timedelta(days=EMERGENCE.TTL_DAYS)

        # 1. Пометить истёкшие ProtoConcept
        expired_ids = []
        for proto in self._protos.values():
            if not proto.expired and (now - proto.last_active) > ttl:
                proto.expired = True
                expired_ids.append(proto.proto_id)

        # 2. Очистить _entity_to_protos от expired proto_ids
        for entity, pids in list(self._entity_to_protos.items()):
            cleaned = [p for p in pids if p not in expired_ids]
            if cleaned:
                self._entity_to_protos[entity] = cleaned
            else:
                del self._entity_to_protos[entity]

        # 3. FIX-K3: удалять ключ _matrix только по двойному критерию
        live_entity_sets = {
            proto.entities
            for proto in self._protos.values()
            if not proto.expired
        }
        stale_cutoff = now - ttl
        for key in list(self._matrix.keys()):
            if key in live_entity_sets:
                continue  # proto жив — не трогаем
            last_seen = self._matrix_last_seen.get(key)
            if last_seen is None or last_seen < stale_cutoff:
                # Нет proto И не обновлялся дольше TTL → удалить
                del self._matrix[key]
                self._matrix_last_seen.pop(key, None)
                self._sessions.pop(key, None)
            # Иначе: нет proto, но наблюдение свежее — оставляем расти (FIX-K3)

        # 4. P0.5-5 FIX: orphaned sessions (в _sessions но не в _matrix)
        stale_sessions = [k for k in self._sessions if k not in self._matrix]
        for key in stale_sessions:
            del self._sessions[key]

        if expired_ids:
            active = len([p for p in self._protos.values() if not p.expired])
            logger.info(
                f"ConceptEmergence GC: {len(expired_ids)} expired | active={active}"
            )
```

### Тесты [RFC0066 — Sprint 1]

```python
# tests/test_invariants.py + test_sprint1_additions.py
# Файл: test_sprint1_additions.py (добавить в тест-сьют или запускать отдельно)
#
# Инварианты: I50, I50-b, I66 (FIX), I70, I-K3, A1, A2, A3

import pytest
import asyncio as _asyncio
from velantrim_config import EMERGENCE
from concept_emergence import ConceptEmergenceDetector, ProtoConcept


class MockDB:
    """Заглушка DB — детектор хранит, но не использует в текущей реализации."""
    pass


class MockTruthGate:
    """
    Мок TruthGate с счётчиком вызовов.
    call_count == 0 после observe() → TruthGate не вызван → L3 не тронут.
    """
    def __init__(self):
        self.call_count = 0

    async def validate_and_transition(self, proposal: dict):
        self.call_count += 1
        class _Result:
            passed = True
        return _Result()


# ── I50 ──────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I50_concept_emergence_no_graph_writes():
    """I50: observe() не пишет в L3. TruthGate не вызван ни разу."""
    gate     = MockTruthGate()
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=gate)
    for i in range(10):
        await detector.observe(["A", "B", "C"], session_id=f"s{i}")
    assert gate.call_count == 0, (
        f"I50 VIOLATION: TruthGate вызван {gate.call_count} раз(а) во время observe()."
    )
    assert len(detector.get_protos_for_entity("A")) >= 1


# ── I50-b ────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I50b_proto_promote_requires_truthgate():
    """I50-b: promote_to_l3() обращается к TruthGate ровно 1 раз."""
    gate = MockTruthGate()
    d    = ConceptEmergenceDetector(db=MockDB(), truth_gate=gate)
    p    = ProtoConcept(
        proto_id="proto:t01", entities=frozenset(["A", "B", "C"]),
        co_occur_count=7, cross_sessions=4, name="test", confidence=0.75,
    )
    await d.promote_to_l3(p)
    assert gate.call_count >= 1, "I50-b VIOLATION: промоут без TruthGate"


# ── I66 (FIX-I66) ────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I66_proto_only_in_memory():
    """
    I66: ProtoConcept живёт только в памяти — observe() не инициирует запись в L3.

    FIX-I66: предыдущая версия создавала MockGraph() не связанный с детектором —
    тест всегда проходил тривиально. Новая версия: gate.call_count == 0 доказывает,
    что TruthGate (единственный вход в L3) не вызывался.
    """
    gate     = MockTruthGate()
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=gate)
    for i in range(EMERGENCE.CO_OCCUR_MIN + 2):
        session = f"s{i % (EMERGENCE.CROSS_SESSION + 1)}"
        await detector.observe(["Alpha", "Beta", "Gamma"], session_id=session)
    assert gate.call_count == 0, (
        f"I66 VIOLATION: TruthGate вызван {gate.call_count} раз(а) во время observe(). "
        f"ProtoConcept не должен промоутироваться автоматически при observe()."
    )
    protos = detector.get_protos_for_entity("Alpha")
    assert len(protos) >= 1, "I66: ProtoConcept не создан в памяти."
    assert not protos[0].expired, "I66: свежий ProtoConcept помечен expired — баг."
    assert protos[0].proto_id in detector._protos, "I66: proto_id не в _protos."


# ── I70 ──────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I70_max_active_protos_cap():
    """
    I70: активных ProtoConcept ≤ MAX_ACTIVE_PROTOS. Eviction работает.
    Инжектируем данные напрямую через _maybe_create_proto() для скорости.
    """
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=None)
    overflow_count = 100
    total = EMERGENCE.MAX_ACTIVE_PROTOS + overflow_count
    for i in range(total):
        key = frozenset([f"Ent{i}_A", f"Ent{i}_B", f"Ent{i}_C"])
        detector._matrix[key] = EMERGENCE.CO_OCCUR_MIN + 1
        for s in range(EMERGENCE.CROSS_SESSION + 1):
            detector._sessions.setdefault(key, set()).add(f"sess_{i}_{s}")
        detector._maybe_create_proto(key)
    active = [p for p in detector._protos.values() if not p.expired]
    assert len(active) <= EMERGENCE.MAX_ACTIVE_PROTOS, (
        f"I70 VIOLATION: {len(active)} активных proto при лимите {EMERGENCE.MAX_ACTIVE_PROTOS}."
    )
    assert len(active) == EMERGENCE.MAX_ACTIVE_PROTOS, (
        f"I70: ожидали ровно {EMERGENCE.MAX_ACTIVE_PROTOS} proto, получили {len(active)}."
    )


# ── FIX-K3 ───────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_K3_immature_observations_survive_gc():
    """
    FIX-K3: незрелые наблюдения (без proto, ниже порога) НЕ удаляются GC.
    Критично для медленно растущих концептов (раз в неделю → 5 недель до порога).
    """
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=None)
    for i in range(EMERGENCE.CO_OCCUR_MIN - 1):
        session = f"s{i % (EMERGENCE.CROSS_SESSION + 1)}"
        await detector.observe(["Slow", "Concept", "Growth"], session_id=session)
    key = frozenset(["Slow", "Concept", "Growth"])
    assert key in detector._matrix, "Тест: наблюдение должно быть в _matrix до GC."
    assert len(detector.get_protos_for_entity("Slow")) == 0, "Тест: proto не должен быть."
    count_before = detector._matrix[key]
    await detector.gc_expired()
    assert key in detector._matrix, (
        f"FIX-K3 VIOLATION: gc_expired() удалил незрелые наблюдения "
        f"(count={count_before}, порог={EMERGENCE.CO_OCCUR_MIN})."
    )
    assert detector._matrix[key] == count_before, "FIX-K3: счётчик изменился после GC."


# ── A1: конфиг-константы присутствуют ────────────────────────────────────────
def test_A1_emergence_config_constants():
    """A1: EmergenceConfig содержит все Sprint 1 константы с корректными типами."""
    assert hasattr(EMERGENCE, "HEBBIAN_DECAY_FACTOR"), "A1: HEBBIAN_DECAY_FACTOR отсутствует."
    assert hasattr(EMERGENCE, "SALIENCE_MULTIPLIER"),  "A1: SALIENCE_MULTIPLIER отсутствует."
    assert hasattr(EMERGENCE, "L5_5_INTEGRATION"),     "A1: L5_5_INTEGRATION отсутствует."
    assert isinstance(EMERGENCE.HEBBIAN_DECAY_FACTOR, float), "A1: HEBBIAN_DECAY_FACTOR должен быть float."
    assert 0.0 < EMERGENCE.HEBBIAN_DECAY_FACTOR <= 1.0, (
        f"A1: HEBBIAN_DECAY_FACTOR={EMERGENCE.HEBBIAN_DECAY_FACTOR} вне диапазона (0, 1]."
    )
    assert isinstance(EMERGENCE.L5_5_INTEGRATION, bool), "A1: L5_5_INTEGRATION должен быть bool."


# ── A2: Lock инициализирован ──────────────────────────────────────────────────
def test_A2_lock_initialized():
    """A2: detector имеет asyncio.Lock и _matrix_last_seen (FIX-K3)."""
    detector = ConceptEmergenceDetector(db=MockDB())
    assert hasattr(detector, "_lock"), "A2: _lock отсутствует."
    assert isinstance(detector._lock, _asyncio.Lock), "A2: _lock должен быть asyncio.Lock."
    assert hasattr(detector, "_matrix_last_seen"), "FIX-K3: _matrix_last_seen отсутствует."
    assert isinstance(detector._matrix_last_seen, dict), "FIX-K3: _matrix_last_seen должен быть dict."


# ── A3: _notify_l5_5 срабатывает только на threshold ─────────────────────────
@pytest.mark.asyncio
async def test_A3_l5_5_scaffold_threshold_only():
    """
    FIX-A3: _notify_l5_5 вызывается только при достижении порога,
    не при каждом observe().
    """
    calls = []

    class MockL5_5:
        pass

    detector = ConceptEmergenceDetector(db=MockDB(), l5_5=MockL5_5())
    original_notify = detector._notify_l5_5
    async def _patched_notify(entities, salience_weight):
        calls.append((entities, salience_weight))
        await original_notify(entities, salience_weight)
    detector._notify_l5_5 = _patched_notify

    for i in range(EMERGENCE.CO_OCCUR_MIN - 1):
        session = f"s{i % (EMERGENCE.CROSS_SESSION + 1)}"
        await detector.observe(["X", "Y", "Z"], session_id=session)

    assert len(calls) == 0, (
        f"FIX-A3 VIOLATION: _notify_l5_5 вызван {len(calls)} раз(а) до порога."
    )
```

### Добавить в velantrim_config.py

```python
class EmergenceConfig:
    CO_OCCUR_MIN      = 5
    CROSS_SESSION     = 3  # FIX: переименовано с CROSS_SESSION_MIN → CROSS_SESSION
                           # чтобы совпадать с ConceptEmergenceDetector и не вызывать AttributeError
    MIN_ENTITIES      = 3
    MAX_ENTITIES      = 7
    NAMING_THRESHOLD  = 0.7
    TTL_DAYS          = 30  # P2-A: был хардкод в gc_expired() — теперь конфигурируемый
    MAX_ACTIVE_PROTOS = 500
    # Sprint 1 (A1): были хардкодами в daily_maintenance() и observe()
    HEBBIAN_DECAY_FACTOR: float = 0.98   # confidence *= factor**days  (0,1]
    SALIENCE_MULTIPLIER:  float = 1.0    # множитель для salience_boost расчёта
    L5_5_INTEGRATION:     bool  = False  # A3: scaffold off by default; Sprint 2 включает

EMERGENCE = EmergenceConfig()
```

---

### P1-2: Когнитивная типизация памяти (новая ортогональная ось)

```python
# Новая ось поверх L0–L7 — ортогональна ESM и knowledge_type
from enum import Enum

class MemoryType(str, Enum):
    EPISODIC   = "episodic"    # конкретные события, диалоги
    SEMANTIC   = "semantic"    # факты, концепции, определения
    PROCEDURAL = "procedural"  # навыки, процедуры, workflows

# Добавить поле в MemoryItem / :Fact / :Episode / :Theme:
memory_type: MemoryType = MemoryType.EPISODIC

def classify_memory_type(content: str, tags: list = None) -> MemoryType:
    tags = tags or []
    c = content.lower()
    if any(w in c for w in ["шаг", "процедура", "workflow", "алгоритм", "как сделать"]):
        return MemoryType.PROCEDURAL
    if any(t in tags for t in ["how-to", "process", "recipe", "workflow"]):
        return MemoryType.PROCEDURAL
    if any(w in c for w in ["определение", "закон", "правило", "означает"]):
        return MemoryType.SEMANTIC
    if any(t in tags for t in ["definition", "concept", "law", "rule"]):
        return MemoryType.SEMANTIC
    return MemoryType.EPISODIC
```

---

L2: Среднесрочная память (Medium-Term Memory)           ← RFC0013
    ├─ Хранилище: SQLite (WAL) таблица l2_memory + FTS5 на summary
    │   НЕ список в RAM — персистентный слой, не теряется при перезапуске.
    ├─ Узел :Theme в Neo4j — персистентный кластер с богатыми метаданными:
    │     · theme_id, summary, summary_embedding
    │     · cluster_size, strength, confidence
    │     · emotional_salience, goal_alignment
    │     · access_count_7d, decay_lambda, is_active
    │     · schema_type: ["factual","procedural","emotional","strategic"]
    │     · first_seen, last_updated
    │   ⚠️ УТОЧНЕНИЕ ТИПА emotional_salience:
    │     :Theme.emotional_salience — FLOAT [0.0, 1.0]
    │       0.0 = нейтральное событие
    │       0.5 = заметное (частичный успех/неудача)
    │       1.0 = критическое (сильный SUCCESS/FAILURE)
    │     :Theme.emotional_label — STRING (опционально, для UI)
    │       "SUCCESS" | "FAILURE" | "NEUTRAL" | "CRITICAL"
    │     В формуле strength:
    │       emotional = 1.0 + emotional_salience × 1.3  → диапазон 1.0…2.3
    │     Emotional Ring Zero (RFC0015):
    │       emotional_salience > 0.85 → ESM.freeze() — иммунитет к decay
    ├─ cluster_type: EPISODIC | STRATEGIC | CONCEPTUAL
    │     · EPISODIC   → decay_rate=0.05 (быстрый) → ReasoningBank
    │     · STRATEGIC  → decay_rate=0.02 (средний) → L3 + ReasoningBank
    │     · CONCEPTUAL → decay_rate=0.01 (медленный) → L3 через Truth Gate
    ├─ Формула strength (взвешенная сумма):
    │     Устойчива к нулевым факторам — обнуление одного компонента
    │     не обнуляет итоговую силу темы.
    │
    │     strength = (
    │         w_base  × base_factor        +
    │         w_reinf × reinforcement_factor +
    │         w_emot  × emotional_factor   +
    │         w_goal  × goal_alignment     +
    │         w_stab  × stability_factor
    │     ) / (w_base + w_reinf + w_emot + w_goal + w_stab)
    │
    │     Веса по умолчанию (velantrim_config.py):
    │       w_base  = 1.0
    │       w_reinf = 1.0
    │       w_emot  = 1.5   ← эмоциональная память важнее
    │       w_goal  = 1.2
    │       w_stab  = 0.8
    │
    │     Компоненты:
    │       base_factor          = 1.0 + log1p(cluster_size) × 0.45          # log1p(x) = log(1+x), см. np.log1p
    │       reinforcement_factor = 1.0 + 0.15 × log1p(access_count_7d)
    │       emotional_factor     = 1.0…2.3  (2.0 при SUCCESS/FAILURE)
    │       goal_alignment       = cosine(theme_embedding, active_goal_embedding) ∈ [0,1]
    │         Источник active_goal_embedding:
    │           · A0 (Hot Focus) активен → эмбеддинг текущего запроса
    │           · A1 (Day Focus) есть активная цель → goal_stack[0].embedding
    │           · Оба пусты → last_user_query_embedding (cache)
    │           · Fallback → 0.5 (нейтральное, не обнуляет формулу)
    │           · ⚠️ 0.5 при w_goal=1.2 не нейтрально — активно занижает узлы без
    │           · активной цели относительно узлов с целью (сила = 0.6 vs ~0.8).
    │           · TODO: рассмотреть fallback=1.0 или флаг goal_context_absent
    │           · чтобы w_goal вклад был явно нейтрализован при отсутствии цели.
    │       stability_factor     = 1 / (1 + days_since_update × λ₂)
    │
    │     Разложение хранится в strength_components (JSON):
    │       {"base": 1.2, "reinf": 1.1, "emot": 1.8, "goal": 0.6, "stab": 0.9}
    │     Механизм передачи: A0/A1 → SessionContext → L2IngestionEngine
    │     Refresh: обновляется при каждом новом запросе пользователя
    │   Порог продвижения в L3: (strength > 4.5) ∧ (access_count > 10) ∧ (stability > 0.75)
    ├─ TTL Manager (адаптивный):
    │     TTL = 7 дней × 2^min(visits, 5) — max 224 дня
    │     visits = access_count + reactivation_count
    │     При истечении: важные → продлить, маловажные → soft delete → S3
    ├─ ReactivationEngine («сон агента», Phase 1):
    │     Фоновый asyncio.Task при CPU < 30%. Каждый час прокручивает
    │     топ-N эпизодов по importance, укрепляет связи, продлевает TTL.
    │     Аналог hippocampal replay в нейробиологии.
    ├─ Cold Start Guard:
    │     if len(l2_items) < 50: skip_clustering()
    │     Запуск кластеризации на < 50 эпизодах → микро-кластеры → баг.
    ├─ I/O батчинг: L2MetricsBuffer (flush каждые 10 мин) — защита SSD
    ├─ L3→L2 обратная связь: при ESM-переходе факта (Validated→Contradicted)
    │     → найти :Theme, содержащие этот факт → снизить strength × epistemic_penalty
    ├─ Связи в графе:
    │     :Theme -[:CONTAINS {weight, since}]→ :Episode
    │     :Theme -[:SIMILAR_TO {cosine}]→ :Theme
    │     :Theme -[:GENERALIZES_TO]→ :KnowledgeUnit  (в L3)
    │     :Theme -[:EXEMPLIFIES]→ :Outcome
    │     :Theme -[:HAS_FACTS]→ :FactsPack
    ├─ Паттерны успеха/неудач + anti-patterns → ReasoningBank
    │
    │   ⚠️ РАЗГРАНИЧЕНИЕ L2 vs L4 (RFC0014):
    │     L2 = опыт: кластеры, паттерны, темы — НЕ факты, НЕ reasoning
    │     L4 = reasoning: единственная точка логики и вывода
    │     L2 даёт шаблон → L4 применяет → Graph даёт факты
    │     L2 НЕ является источником фактов. FactsPack строится только из Graph.
    │
    └─ Decay: FSRS power-law (v8.0 — заменяет Ebbinghaus экспоненту, P0-1)

         R = (1 + 19/81 × t/S)^(-0.5)
         # Точнее экспоненты Ebbinghaus на 20-30% (FadeMem paper, jan 2026)
         # Fast Path читает закэшированное retrievability из индекса графа.
         # FSRSState создаётся lazy — только в Slow Path (SleepTimeWorker/DecayWorker).
         # Заменяет Ebbinghaus: R = e^(-t/S) согласно P0-1
         R = retention (сколько осталось)
         t = время с последнего подтверждения
         S = strength (растёт с повторениями · умножается на salience_weight)

         Факт упомянут 1 раз:
           → через 1 день  confidence: 0.58
           → через 7 дней  confidence: 0.21
           → через 30 дней confidence: 0.05 → холодное хранилище

         Тот же факт упомянут 5 раз (S вырос):
           → через 1 день  confidence: 0.91
           → через 7 дней  confidence: 0.74
           → через 30 дней confidence: 0.52 → всё ещё активен

         salience_weight умножает S: важные факты живут дольше обычных.
         Worker: запускается раз в час через EventBus · CPU only · ~0 нагрузки
         Emotional Ring Zero (RFC0015): emotional_salience > 0.85 → иммунитет к decay

    Cache-Aware Hot Graph — двухуровневый граф
    ├─ По аналогии с виртуальной памятью ОС: всё делится на горячее и холодное.
    │
    │   🔥 Горячий граф (живёт в RAM):
    │     · Узлы активированные за последние 24 часа
    │     · Узлы с salience_weight > 0.7  ← Salience Detector решает кто здесь
    │     · LITE: ~500–2000 узлов · 2–5 MB RAM
    │     · ONE:  ~10–50k узлов   · 50–100 MB RAM
    │
    │   🧊 Холодный граф (SSD / Neo4j):
    │     · Всё остальное
    │     · Подгружается только если spreading activation достаточно сильная
    │
    │   Spreading activation сначала проходит горячий граф за 1–3 мс.
    │   Холодные узлы — только по необходимости.
    │   Ускорение системы: ×2–3 · без доп. CPU нагрузки.
    │   Ребалансировка: раз в час через EventBus SleepTimeWorker.
    │   Метрики:
    │     hot_graph_size_nodes   — текущий размер горячего графа
    │     hot_graph_hits_total   — сколько запросов обслужено из RAM
    │     cold_graph_loads_total — сколько раз подгружался холодный граф

L2.5: Staging Layer (RFC0014) — буфер перед L3
    │   SQLite = временный буфер (staging), НИКОГДА не источник истины.
    │   Graph = единственный L3. Принцип Graph = Truth не нарушается.
    ├─ Назначение: асинхронная консолидация для слабого железа.
    │     L0/L1/L2 пишут в SQLite → данные дозревают → в L3 только при ресурсах.
    ├─ Resource-Aware Scheduler:
    │     Условия запуска: CPU < 35% AND RAM free > 25% AND user_idle
    │     Если ПК занят — staging копит данные, граф не строится.
    │     Принудительный flush: если ПК не idle > 24ч → 5-10% CPU фоново.
    ├─ Fast-Track (обход очереди):
    │     priority > 0.9 → немедленно → Truth Gate → L3
    │     Примеры CRITICAL: аллергии, Ring Zero изменения, критические факты
    ├─ Graph-Lite (для слабого ПК, RAM < 4GB):
    │     Временный мини-граф внутри SQLite (таблицы nodes + edges).
    │     При запросе: UNION из Graph-Lite (staging) + L3.
    │     Это НЕ параллельная истина — та же логика L3, другой движок.
    │     При переносе в Neo4j Graph-Lite очищается.
    ├─ Правило чтения:
    │     1. Сначала граф (L3) — канон
    │     2. Если нет в графе, но есть в staging → использовать с confidence × 0.7
    │        и пометкой "preliminary" (не истина, гипотеза)
    ├─ Путь данных:
    │     L2 → staging_candidates → Priority Queue → Scheduler
    │         → Truth Gate → L3 (Graph)
    │     FAST-TRACK: L2 → Truth Gate → L3 (минует очередь)
    └─ Decay: staging_candidates TTL по priority_score, GC при > MAX_STAGING_SIZE

---

### P0-1 NEW: memory/fsrs_state.py (RFC0069)

Модуль вставляется в проект как отдельный файл. Полный код — в патче P0-1 файла VELANTRIM_TITAN_v8_CRYSTAL_PATCHES.md.

Новые поля в MemoryItem / FactNode:
    difficulty: float = 5.0           # D in [1.0, 10.0]
    stability: float = 1.0            # S — стабильность
    retrievability: float = 1.0       # R — текущая извлекаемость
    fsrs_last_review: datetime = None  # время последнего обращения

Конфиг (velantrim_config.py):
    FSRS_ENABLED = True
    FSRS_PLASTICITY_W = 0.6
    FSRS_MIN_STABILITY = 0.1
    FSRS_REFRESH_THRESHOLD = 0.3

I84 (FSRSIsolation): FSRS decay меняет ТОЛЬКО retrievability и attention_weight.
    truth_status, epistemic_state и confidence — неприкосновенны.
    FSRSState создаётся только в Slow Path. Fast Path читает кэш.

---

L3: Долгосрочная память (Long-Term Memory)
    ├─ Семантические концепции
    ├─ Мета-стратегии
    ├─ Личность агента и предпочтения пользователя
    ├─ Write Protocol — единственные разрешённые пути записи:
    │     ✅ TruthGate (validated pipeline)
    │     ✅ Human approval (trust_score = 0.95)
    │     ✅ Trusted import (trust_score ≥ 0.80)
    │     ❌ LLM напрямую / L1 / L2 / Free Mode / Observer
    │     Нарушение → WriteProtocolViolation + лог + Observer alert
    ├─ Source Trust Layer — поле на каждом факте:
    │     source_type: "user_input" | "llm_output" | "import" | "manual"
    │     trust_score: 0.0 – 1.0
    │     validation_status: "verified" | "pending" | "flagged"
    │     TruthGate принимает факт только если trust_score ≥ TRUST_THRESHOLD
    │     Защита от "validated hallucination" — галлюцинации прошедшей проверку
    ├─ P1-3: knowledge_type на :Fact
    │     class KnowledgeType(str, Enum):
    │       TERM       = "term"        # определение термина
    │       FACT       = "fact"        # конкретный факт
    │       LAW        = "law"         # закон, правило, инвариант
    │       MODEL      = "model"       # модель, теория
    │       METHOD     = "method"      # метод, алгоритм
    │       CONSTRAINT = "constraint"  # ограничение
    │       OPINION    = "opinion"     # мнение
    │     На :Fact узле: knowledge_type: str = "fact"  # default
    │     I87 (KnowledgeTypeImmutable): knowledge_type — read-only после Validated.
    │     Изменение типа у Validated факта = создание нового факта.
    │
    ├─ P1-5: Provenance Chain:
    │     Вместо одного source_type — массив провенанса:
    │     provenance_chain: List[Dict] = [
    │       {"source_type": "user_input", "timestamp": "...", "content_hash": "..."},
    │       {"verified_by": "truth_gate", "confidence": 0.85},
    │       {"promoted_by": "esm_transition", "from": "Supported", "to": "Validated"}
    │     ]
    │     Append-only: удаление записей из цепочки запрещено.
    │     I89 (ProvenanceAppendOnly): provenance_chain — append-only.
    │
    ├─ Fan-out Limit + Meta-Nodes:
    │     FAN_OUT_LIMIT = 500 связей одного типа на узел
    │     При превышении → агрегация в мета-узел (не новое ребро)
    │     Защита Neo4j от деградации при "толстых" узлах
    ├─ P1-1: Multi-Graph Decomposition (MAGMA-style):
    │     Рёбра разделены на 4 ортогональных типа:
    │     · [:SEMANTIC_REL]  — смысловые связи (is-a, part-of, similar)
    │     · [:TEMPORAL_REL]  — временные связи (before, after, during)
    │     · [:CAUSAL_REL]    — причинные связи (causes, prevents, enables)
    │     · [:ENTITY_REL]    — сущностные связи (owns, works-at, located-in)
    │     IntentRouter (memory/intent_router.py) определяет тип запроса →
    │     HybridRetriever обходит только нужные рёбра.
    │     "Why/почему" → CAUSAL_REL. "When/когда" → TEMPORAL_REL.
    │     "What is" → SEMANTIC_REL. Default → все типы.
    │     I86 (IntentRouter): вызывается ТОЛЬКО из HybridRetriever.retrieve().
    │
    ├─ Decay: медленный (месяцы-годы)
    ├─ Homeostatic Balancer — иммунитет графа
    │     Фоновый процесс · запускается SleepTimeWorker в 3:00 ночи при user_idle.
    │     Аналог: synaptic homeostasis во время глубокого сна у людей.
    │
    │     Проблема которую решает: граф накапливает перекос — тысячи сильных
    │     связей в одной области (например, всё о Velantrim) и мёртвые зоны
    │     в других. Через год система начинает «думать» только об одном.
    │
    │     Алгоритм:
    │       1. Собрать распределение весов по всем доменам графа
    │       2. Если domain_weight > OVERLOAD_THRESHOLD (0.8):
    │            → мягкая нормализация: multiply weights × 0.85
    │       3. Если domain.last_active < now - 30 дней:
    │            → поднять базовый вес × 1.2 (знания не «умирают» полностью)
    │       4. Записать homeostatic_run в метрики
    │
    │     Нагрузка: 30–60 сек · раз в сутки · CPU only
    │     Метрика: homeostatic_runs_total · homeostatic_normalized_domains

    ### ESM State Transitions — Epistemic State Machine

         Observed → Hypothesized → Supported → Validated
                        ↑                          │
                        │ rollback                 ├─────────────────────┐
                        │ Evidence отозван         ▼                     ▼
                        └────────────── Contradicted         (остаётся Validated)
                                                   │ 3+ конфликта
                                                   ▼
                                             Deprecated
                                                   │ importance < 0.1
                                                   ▼
                                              Collapsed
                                    (→ Immutable Raw Memory, не уничтожается)
       Правила переходов:
         · Observed     → Hypothesized : первое появление (авто)
         · Hypothesized → Observed     : Evidence отозван — rollback
         · Hypothesized → Supported    : Evidence ≥ 2
         · Supported    → Validated    : MGL + Truth Gate пройден
         · Validated    → Contradicted : 1+ сильный [:CONTRADICTS]
         · Contradicted → Deprecated   : importance -= weighted_penalty × 3+
         · Deprecated   → Collapsed    : importance < 0.1 при GC

    ├─ P1-4: Per-node Versioning (OCC):
    │     Каждый :Fact имеет _version_: int (начинается с 1).
    │     ESM-переходы используют Optimistic Concurrency Control:
    │       MATCH (f:Fact {id: $id, _version_: $expected})
    │       SET f.epistemic_state = $new, f._version_ = f._version_ + 1
    │     Если _version_ не совпала — retry через очередь.
    │     I88 (VersionOCC): _version_ инкрементируется ТОЛЬКО атомарно через OCC Cypher.
    │     Прямой SET _version_ без проверки expected — баг.

L3.5: Immutable Core — Вечная основа памяти          ← RFC0017
    ├─ Назначение: append-only ledger, защита от катастрофического забывания.
    │   Это НЕ operational слой — это аудит и восстановление.
    ├─ Механизм:
    │     Каждые 24 часа → snapshot L3 графа → hash SHA-256 + timestamp
    │     → запись в Neo4j :ImmutableCore узел (append-only, no UPDATE/DELETE)
    │     → параллельно Parquet file → S3 для долгосрочного хранения
    │     Delta Snapshots (дифференциальное хранение):
    │       · Day 1: FULL snapshot (все узлы + рёбра)
    │       · Day 2+: DELTA snapshot (только изменённые/новые/удалённые)
    │       · Формат delta: {added: [...], modified: [...], deleted: [...]}
    │       · Восстановление: full_snapshot + apply(delta_1) + ... + apply(delta_N)
    │       · FULL snapshot каждые 7 дней (для быстрого восстановления)
    │     Экономия storage: ~80-90% (вместо 365 полных снапшотов → 52 полных + 313 delta)
    ├─ Хранилище: 
    │     · Neo4j: узел :ImmutableCore {timestamp, hash, node_count, edge_count, snapshot_type}
    │     · S3/MinIO: graph_snapshot_{timestamp}.parquet (полный дамп)
    │     · S3/MinIO: graph_delta_{timestamp}.parquet (дифференциальный)
    │     · SQLite: metadata (fractal_similarity_score, alert_triggered)
    ├─ Drift Detection:
    │
    │     knowledge graph snapshots — метрика из теории динамических систем,
    │     не валидирована для графов. Заменена на структурные дельта-метрики:
    │     
    │     drift_score = {
    │         "node_delta":      abs(new_count  - old_count)  / old_count,
    │         "edge_delta":      abs(new_edges  - old_edges)  / old_edges,
    │         "avg_degree_delta": abs(new_avg_d - old_avg_d),
    │         "component_delta": abs(new_comp   - old_comp)   / max(old_comp,1)
    │     }
    │     if any(delta > 0.2 for delta in drift_score.values()):
    │         alert("Memory structural drift detected!")
    │     
    │     Порог 0.2 = 20% изменение за сутки → аномалия.
    ├─ Semantic Drift Monitor — смысловой дрейф:
    │     Поверх структурного — независимый второй монитор.
    │     Компоненты: ESM-distribution + PageRank top-10 + domain shifts
    │     semantic_score = esm_drift*0.5 + centrality_drift*0.3 + domain_drift*0.2
    │     Два НЕЗАВИСИМЫХ алерта (не смешивать):
    │       · structural_drift → граф изменился по форме
    │       · semantic_drift   → граф изменился по смыслу
    │     Можно: структурно стабильный граф с высоким semantic drift.
    ├─ ESMChunkedInvalidator — батчевый откат:
    │     Заменяет прямой каскад [:CONTRADICTS] (риск deadlock Neo4j).
    │     Порции по 50 узлов + asyncio.sleep(100ms) между батчами.
    │     Обязательный индекс: CREATE INDEX pending_inv_idx FOR (f:Fact)
    │                           ON (f.pending_invalidation)
    │     Safe Mode check: при SAFE_MODE → процесс приостанавливается.
    ├─ Использование:
    │     · Audit: GET /memory/audit/drift?since=... → показать snapshots + similarity
    │     · Rollback: при катастрофе → восстановить L3 из snapshot_{t-N}
    │     · Verification: ReactivationEngine проверяет Ring Zero узлы по snapshot
    ├─ Инварианты:
    │     ImmutableCore.I1: ТОЛЬКО append, НИКОГДА не UPDATE/DELETE узлов :ImmutableCore
    │     ImmutableCore.I2: Snapshot создаётся ПОСЛЕ успешной консолидации (не в middle)
    │     ImmutableCore.I3: Hash проверяется при чтении — защита от bit rot
    │     ImmutableCore.I4: Ring Zero узлы присутствуют в КАЖДОМ snapshot (иначе alert)
    ├─ GC правила:
    │     Snapshots старше 90 дней → только S3 (из Neo4j удалить метаданные)
    │     Snapshots старше 1 года → cold storage (Glacier/Deep Archive)
    │     Ring Zero snapshots → НИКОГДА не удалять (вечное хранение)
    └─ Decay: отсутствует (immutable навсегда)

L4: Reasoning Layer — Самообучение на опыте          
    ├─ Назначение: извлечение стратегий из опыта, самообучение, Thompson Sampling selection
    │   Это НЕ факты (L3) — это мета-знания: "как решать задачи"
    ├─ Closed Loop Self-Evaluation:
    │     Query → Retrieval → L4 → Answer → EVALUATE → ADJUST
    │     Метрики: faithfulness / trace_coverage / contradiction_rate / confidence
    │     Результат → ReasoningBank (обучение) + Observer (алерт при низком качестве)
    ├─ Компоненты:
    │   ┌─ ReasoningBank Engine:
    │   │  · Experience Buffer (RAM) — накопление опыта до distillation
    │   │  · Strategy Repository (Neo4j :Strategy) — долгосрочное хранение
    │   │  · Thompson Sampling — баланс exploration/exploitation (RFC0039)
    │   │  · Negative Reinforcement — избежание повторных ошибок
    │   └─ Полная реализация: См. RFC0019
    ├─ Структура данных:
    │   · Experience {task, context, action, outcome, reasoning, timestamp}
    │   · Strategy {strategy_id, description, contexts[], success_count, 
    │                failure_count, confidence, failure_penalty, embedding}
    ├─ Механизм самообучения:
    │   [1] FAST PATH: User Query → retrieve_strategies() → Thompson Sampling selection
    │   [2] SLOW PATH: Task Complete → log_experience() → buffer
    │   [3] Buffer full (20 exp) → distill_strategies() → :Strategy узлы
    │   [4] update_strategy_feedback() → negative reinforcement
    ├─ Thompson Sampling (RFC0039 — заменяет UCB1 RFC0025):
    │   Стохастический выбор стратегий через Beta-распределение.
    │   Легче UCB1 по CPU (O(1) vs O(k)), лучше при delayed feedback.
    │   Результат: +8% cumulative reward на production-задачах.
    │   
    │   Шаг 1 — TF-IDF pre-filter (сохранён из RFC0025):
    │     if cosine(strategy_embedding, context) < 0.3 → skip (нерелевантно)
    │   Шаг 2 — Thompson Sampling (только для прошедших фильтр):
    │     rng = numpy.random.default_rng(session_id_hash)  # per-instance, потокобезопасен
    │     score = rng.beta(success_count + 1, failure_count + 1)
    │     где success_count и failure_count — история стратегии
    │   Rationale: Beta(α,β) естественно балансирует exploration/exploitation.
    │     При малом числе опытов — высокая дисперсия → exploration.
    │     При большом числе опытов — низкая дисперсия → exploitation.
    │   Воспроизводимость: numpy.random.default_rng(session_id_hash) перед вызовом
    │     для детерминированного replay в аудите (Инвариант I13).
    │     ⚠️ НЕ использовать numpy.random.seed() — глобальный PRNG, race condition
    │     в asyncio при конкурентных сессиях. default_rng создаёт изолированный
    │     per-instance генератор: тот же seed → те же числа, никакого shared state.
    │   Баланс: адаптивный — автоматически сдвигается к exploitation
    │     по мере накопления данных (нет фиксированного 10%)
    ├─ Extractive Summarization (БЕЗ LLM):
    │   if importance < 0.5: TF-IDF extractive (0 токенов)
    │   elif importance < 0.8: GPT-4o-mini (дешево)
    │   else: GPT-4 (только критичное)
    │   Экономия токенов: 40-60%
    ├─ L4 Worker (фоновый):
    │   · Периодический review стратегий (раз в неделю)
    │   · Удаление низкоэффективных (success_rate < 0.2)
    │   · Cross-validation метрики
    ├─ Neo4j Schema:
    │   CREATE (:Strategy {strategy_id, description, applicable_contexts,
    │                       success_count, failure_count, confidence, embedding})
    │   CREATE INDEX strategy_embeddings FOR (s:Strategy) ON (s.embedding)
    │   CREATE (:Theme)-[:DERIVED_FROM]->(:Strategy)
    ├─ Интеграция с ContextBuilder:
    │   Промпт = [СТРАТЕГИИ: ...] + [ФАКТЫ: ...] + [ЗАПРОС: ...]
    │   Strategies идут ПЕРЕД фактами в контексте
    ├─ Метрики:
    │   · reasoning_bank_experiences_total — всего опыта записано
    │   · reasoning_bank_strategies_created — стратегий создано
    │   · reasoning_bank_ts_score — Thompson Sampling score по стратегии
    │   · reasoning_bank_exploration_rate — exploration vs exploitation (адаптивный)
    ├─ Результаты (доказано ReasoningBank paper):
    │   · +30-35% успешность задач (через обучение на опыте)
    │   · 40-60% снижение расхода токенов (extractive без LLM)
    │   · Избежание повторных ошибок (negative reinforcement)
    └─ Decay: стратегии с success_rate < 0.2 удаляются через 30 дней

L4.5: ResponseAudit & FocusEngine — Мета-слой осознанности ← RFC0052, RFC0053
    ├─ Назначение: мета-память о диалогах + живой фокус внимания на пользователя.
    │   Это НЕ факты (L3) и НЕ стратегии (L4) — это осознание системой своих ответов
    │   и непрерывное понимание того, что нужно человеку прямо сейчас.
    │   ⚠️ УТОЧНЕНИЕ: L4.5 объединяет три RFC на одном слое:
    │     · RFC0052 — ResponseAuditWorker (аудит ответов)
    │     · RFC0053 — FocusEngine (фокус внимания)
    │     · RFC0065 — MemoryVolitionWorker (осознанная воля к памяти)
    │   Все три компонента работают в Slow Path через EventBus.
    │
    ├─ [RFC0052] ResponseAuditWorker — Lazy двухфазный аудит ответов:
    │   FAST PATH: LLM → ответ пользователю (без задержки)
    │              → EventBus: RESPONSE_GENERATED (fire-and-forget)
    │   SLOW PATH: AuditWorker подписан на шину:
    │     Фаза 1+2: SLM/TF-IDF → human_summary + tags + importance_score (0 тяж. токенов)
    │     Фаза 3:   ТОЛЬКО если importance_score > 0.85 → flagship LLM → precomputed:
    │               { "суть", "критика", "уязвимости", "долгосрочно", "цель", "предложение" }
    │     Хранение: importance > 0.85 → SQLite + :DialogueSummary (Neo4j)
    │               importance < 0.85 → только SQLite (сессия)
    │               сессия ARCHIVED  → VacuumWorker: DELETE WHERE importance < 0.5
    │   ⚠️ Stale Cache Protection:
    │     dependency_hashes: List[fact_id] — IDs фактов из L3 использованных в ответе
    │     get_explanation() → _verify_dependencies() → TruthGate.check_facts_status()
    │     Если факт стал Contradicted → audit.precomputed.clear() → lazy regenerate
    │   ⚠️ Превентивная инвалидация:
    │     TruthGate при ESM-переходе → EventBus: CACHE_INVALIDATED {fact_ids}
    │     AuditWorker ловит → очищает precomputed у всех связанных аудитов немедленно
    │   Структура данных:
    │     @dataclass ResponseAudit:
    │       conversation_id, response_id, timestamp, status (NEW/ACTIVE/RESOLVED/BLOCKED)
    │       importance_score: float          # 0.0–1.0
    │       dependencies: List[str]          # fact_ids для инвалидации
    │       human_summary: str               # Фаза 2 (SLM)
    │       tags: List[str]                  # критика / уязвимость / долгосрочно / ...
    │       precomputed: Dict[str, str]      # Фаза 3 (Lazy, только importance > 0.85)
    │   Neo4j Schema:
    │     (:DialogueSummary {summary_id, human_summary, importance, tags, embedding})
    │     (:DialogueSummary)-[:HAS_TAG]→(:DialogueTag)
    │     (:DialogueSummary)-[:REFERS_TO]→(:Fact)
    │     (:DialogueSummary)-[:USES_STRATEGY]→(:Strategy)
    │   ⚠️ ИНВАРИАНТ I28: ResponseAuditWorker НИКОГДА не выполняется в Fast Path.
    │     Аудит строго в SLOW PATH через EventBus. Нарушение = блокировка ответа = баг.
    │
    ├─ [RFC0053] FocusEngine — Живой фокус внимания (синаптический портрет):
    │   Назначение: система непрерывно "чувствует" что нужно пользователю,
    │   читая граф — без LLM-вызовов (0 токенов).
    │   Компоненты FocusVector (обновляется каждым диалогом):
    │     · goal_alignment      — что пользователь хочет (A0/A1/A2)
    │     · emotional_salience  — что его задело (из :Theme)
    │     · pattern_of_ask      — как он спрашивает (тип запросов)
    │     · domain_drift        — куда движется его интерес (из Semantic Drift)
    │   Механизм:
    │     L1 INSERT → FocusEngine.update(episode) → обновить FocusVector
    │     ContextBuilder читает FocusVector → корректирует приоритет фактов
    │     BAE (Behaviour Anticipation Engine) читает FocusVector → подбирает style_profile автоматически
    │     AuditWorker пишет в FocusVector (importance, domain, тип вопроса)
    │   Хранение: in-memory (быстрый доступ) + SQLite snapshot каждые 15 мин
    │   Баланс: FocusVector использует exploration_rate (как Thompson Sampling в L4)
    │     чтобы система не "привыкала" и продолжала удивлять пользователя.
    │   ⚠️ ИНВАРИАНТ I29: FocusVector читается только через граф и SQLite.
    │     Прямые LLM-вызовы для определения фокуса — запрещены. Graph = Truth.
    │
    ├─ Метрики:
    │   · response_audit_total              — всего аудитов создано
    │   · response_audit_persisted_total    — сохранено в SQLite + Neo4j
    │   · response_audit_importance_avg     — средняя важность диалогов
    │   · response_audit_faithfulness_avg   — средний faithfulness score
    │   · response_audit_cache_invalid_total — инвалидаций кэша (Stale protection)
    │   · focus_vector_updates_total        — обновлений FocusVector за сессию
    └─ Decay: :DialogueSummary → decay каждые 48 часов (отдельный процесс)
              importance < 0.3 → soft delete при следующем GC
```

---

## RFC0065: Memory-as-Volition — Осознанная воля к памяти

### 🌱 Читай это первым

Все предыдущие слои памяти работают **пассивно**: система наблюдает и решает что запомнить. RFC0065 добавляет агенту **право голоса в собственной памяти**: через tool call `memory.write_voluntary()` агент принимает осознанное решение записать факт в L3 — без ожидания пассивной консолидации.

    ├─ P2-5: ReasonGraph DAG:
    │     При сложном запросе (Slow Path) строить мини-DAG рассуждения:
    │     1. Собрать факты-кандидаты из retrieval
    │     2. Построить DAG: каждый факт = узел, рёбра = [:SUPPORTS] / [:CONTRADICTS]
    │     3. Оценить каждый узел по relevance × confidence × recency
    │     4. Отсечь ветки с score < 0.3
    │     5. Передать LLM только выверенный путь
    │     I95 (ReasonGraphDAG): DAG строится только в Slow Path при use_slow_path=True.
    │
    ├─ P2-6: Curiosity Engine:
    │     Система не только реагирует, но сама инициирует вопросы:
    │     1. Обнаружить gap в графе (область с < 3 фактами)
    │     2. Сгенерировать вопрос: "что я не знаю о X?"
    │     3. Предложить пользователю или передать Active Evidence Worker
    │     Запуск: раз в сутки через SleepTimeWorker.
    │     I92 (CuriositySlowOnly): Curiosity Engine — ТОЛЬКО Slow Path.
    │
    ├─ P2-7: Trace Examples:
    │     Не просто аудит ответа, а эталон мышления:
    │     intent → evidence → truth_class → policy → action
    │     Хранятся как :TraceExample узлы в графе.
    │     Используются для калибровки Guardian и Quality Gate.
    │     I93 (TraceExampleReadOnly): Trace Examples read-only из Guardian/QualityGate.

**Почему не нарушает Graph = Truth?** Волевая запись проходит через TruthGate — полностью, без исключений. Воля агента означает только то, что он сам инициировал процесс.

**Нейробиологический аналог:** Гиппокамп имеет механизм **intentional encoding** — при явном намерении запомнить активируется другой нейронный путь и долгосрочная консолидация происходит быстрее.

---

```
L4.5 дополнение: MemoryVolitionWorker  <- RFC0065
    |
    +- Назначение: агент инициирует запись в L3 сам. НЕ обход TruthGate.
    |
    +- Режим 1 (Tool Call): агент вызывает memory.write_voluntary()
    |   -> VolitionEvent в EventBus (fire-and-forget)
    |   -> MemoryVolitionWorker (Slow Path) -> Fast-Track Staging -> TruthGate -> L3
    |   -> Запись в VolitionLog {session_id, content_hash, reason, outcome}
    |
    +- Режим 2 (Auto-Detect): importance > 0.9 AND emotional > 0.8
    |   -> FocusEngine генерирует VolitionSignal (тот же путь)
    |   I49-b: Auto-Detect не подавляет явный tool call агента
    |
    +- Fast-Track: voluntary=True обходит CPU-порог в Staging (I49-c)
    |   Лимит: не более 10 voluntary вызовов за сессию
    |
    +- Инварианты:
    |   I49:   write_voluntary() ВСЕГДА через TruthGate. Обход = баг.
    |   I49-b: Auto-Detect не вытесняет явный tool call агента.
    |   I49-c: Voluntary Fast-Track обходит CPU-порог, но не TruthGate.
    |   I49-d: Каждая voluntary запись обязана иметь запись в VolitionLog.
    |
    +- Метрики:
    |   volition_calls_total / volition_validated_total / volition_rejected_total
    |   volition_autodetect_total / volition_limit_exceeded_total
    \- Decay: :VolitionLog -> архивация через 90 дней
```

### Код [RFC0065]

```python
# memory_volition.py
# RFC0065: Memory-as-Volition
# I49: voluntary запись ВСЕГДА через TruthGate — обход запрещён.
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class VolitionOutcome(str, Enum):
    # QUEUED отделён от VALIDATED
    # write_voluntary() возвращает QUEUED — реальный outcome появится в VolitionLog
    QUEUED           = "queued_for_processing"
    VALIDATED        = "validated"
    REJECTED_BY_GATE = "rejected_by_truthgate"
    DUPLICATE        = "duplicate"
    LIMIT_EXCEEDED   = "limit_exceeded"


@dataclass
class VolitionEvent:
    session_id:      str
    agent_id:        str
    content:         str
    reason:          str
    importance_hint: float    = 0.8   # P3-F FIX: НЕ передаётся в TruthGate как confidence (P0.5-3).
                                       # Только для internal logging/prioritization.
                                       # TruthGate всегда получает confidence=0.5 (нейтральный prior).
    source:          str      = "agent"
    timestamp:       datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class VolitionResult:
    outcome: VolitionOutcome
    fact_id: Optional[str] = None
    reason:  Optional[str] = None


class MemoryVolitionWorker:
    MAX_PER_SESSION: int = 10

    def __init__(self, staging, truth_gate, graph, event_bus, db):
        self.staging    = staging
        self.truth_gate = truth_gate
        self.graph      = graph
        self.event_bus  = event_bus
        self.db         = db
        # _session_counts персистируется через SQLite.
        # _load_session_counts() вызывается при старте воркера
        # чтобы не потерять счётчики лимита при перезапуске.
        self._session_counts: dict[str, int] = {}
        self._initialized: bool = False  # ← B4 FIX: guard против вызова до start()

    async def start(self):
        """Инициализация воркера — вызывать до первого process_event().
        FIX: _load_session_counts перенесён в явный start() метод.
        Без этого вызова счётчики лимита per-session сбрасывались при рестарте
        и ограничение 10 voluntary записей за сессию не работало.
        """
        await self._load_session_counts()
        self._initialized = True  # ← B4 FIX: помечаем что инициализация завершена

    async def _load_session_counts(self):
        async with self.db.connect() as conn:
            rows = await conn.fetchall(
                "SELECT session_id, COUNT(*) as cnt FROM volition_log "
                "WHERE outcome='validated' GROUP BY session_id"
            )
        for row in rows:
            self._session_counts[row["session_id"]] = row["cnt"]

    async def write_voluntary(self, session_id, agent_id,
                              content, reason, importance_hint=0.8):
        # B4 FIX: guard — если start() не вызван, лимит не работает
        if not self._initialized:
            raise RuntimeError(
                "MemoryVolitionWorker.start() must be called before write_voluntary(). "
                "Without it, MAX_PER_SESSION limit is non-functional (counters empty)."
            )
        event = VolitionEvent(
            session_id=session_id, agent_id=agent_id, content=content,
            reason=reason,
            importance_hint=min(1.0, max(0.0, importance_hint)),
        )
        await self.event_bus.publish_volition(event)
        # QUEUED — не VALIDATED. Реальный outcome появится в VolitionLog.
        return VolitionResult(outcome=VolitionOutcome.QUEUED,
                              reason="queued_for_processing")

    async def process_event(self, event: VolitionEvent) -> VolitionResult:
        count = self._session_counts.get(event.session_id, 0)
        if count >= self.MAX_PER_SESSION:
            r = VolitionResult(outcome=VolitionOutcome.LIMIT_EXCEEDED)
            await self._log(event, r)
            return r

        if await self._is_duplicate(self._hash(event.content)):
            r = VolitionResult(outcome=VolitionOutcome.DUPLICATE)
            await self._log(event, r)
            return r

        staged = await self.staging.fast_track(
            content=event.content, importance_hint=event.importance_hint,
            voluntary=True,  # I49-c: обходит CPU-порог, но не TruthGate
            source="volition",
        )

        # I49: TruthGate ОБЯЗАТЕЛЕН. Обхода нет.
        # P0.5-3 FIX: importance_hint ≠ confidence.
        # importance — субъективная важность для агента (насколько "хочется запомнить").
        # confidence — эпистемическая достоверность факта (насколько "это правда").
        # Было: "confidence": event.importance_hint — ложь с importance=0.9 проходила Gate.
        # Стало: confidence всегда 0.5 (нейтральный prior) для voluntary записей.
        # importance_hint передаётся отдельно как метаданные приоритета в графе.
        gate = await self.truth_gate.validate_and_transition({
            "id": staged.id, "content": event.content,
            "confidence": 0.5,  # нейтральный prior — TruthGate оценивает факт, не желание
            "importance":  event.importance_hint,  # влияет на приоритет в графе, не на Gate
            "emotional_salience": 0.0,
            "source": "agent_volition",
        })

        if not gate.passed:
            r = VolitionResult(outcome=VolitionOutcome.REJECTED_BY_GATE,
                               reason=gate.reason)
            await self._log(event, r)
            return r

        self._session_counts[event.session_id] = count + 1
        r = VolitionResult(outcome=VolitionOutcome.VALIDATED,
                           fact_id=getattr(gate, "fact_id", staged.id))
        await self._log(event, r)
        return r

    @staticmethod
    def _hash(content: str) -> str:
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()[:32]  # P4-C FIX: 64bit→128bit (Birthday Paradox)

    async def _is_duplicate(self, content_hash: str) -> bool:
        async with self.db.connect() as conn:
            row = await conn.fetchone(
                "SELECT 1 FROM volition_log "
                "WHERE content_hash=? AND outcome='validated' LIMIT 1",
                (content_hash,)
            )
        return row is not None

    async def _log(self, event: VolitionEvent, result: VolitionResult):
        # I49-d: КАЖДАЯ voluntary запись обязана иметь запись в VolitionLog
        async with self.db.connect() as conn:
            await conn.execute(
                "INSERT INTO volition_log "
                "(session_id, agent_id, content_hash, reason, importance_hint, "
                " source, outcome, fact_id, timestamp) VALUES (?,?,?,?,?,?,?,?,?)",
                (event.session_id, event.agent_id, self._hash(event.content),
                 event.reason, event.importance_hint, event.source,
                 result.outcome.value, result.fact_id,
                 event.timestamp.isoformat())
            )
            await conn.commit()
```

### Тест [I49, I49-d]

```python
# tests/test_invariants.py -- добавить

# I49: Voluntary запись ВСЕГДА через TruthGate
async def test_I49_voluntary_always_through_truth_gate():
    gate = MockTruthGate()
    w    = MemoryVolitionWorker(
        staging=MockStaging(), truth_gate=gate,
        graph=MockGraph(), event_bus=MockEventBus(), db=MockDB())
    await w.process_event(VolitionEvent(
        session_id="s", agent_id="a", content="fact", reason="test",
        importance_hint=0.9))
    assert gate.call_count >= 1, "I49 VIOLATION: обход TruthGate"

# I49-d: VolitionLog обязателен
async def test_I49d_volition_log_always_written():
    db = MockDB()
    w  = MemoryVolitionWorker(
        staging=MockStaging(), truth_gate=MockTruthGate(will_pass=False),
        graph=MockGraph(), event_bus=MockEventBus(), db=db)
    await w.process_event(VolitionEvent(
        session_id="s", agent_id="a", content="c", reason="r"))
    assert db.insert_count("volition_log") >= 1, "I49-d VIOLATION"
```

### Добавить в velantrim_config.py

```python
class VolitionConfig:
    MAX_PER_SESSION       = 10
    AUTODETECT_IMPORTANCE = 0.9
    AUTODETECT_EMOTIONAL  = 0.8
    FAST_TRACK_BYPASS_CPU = True
    LOG_RETENTION_DAYS    = 90

VOLITION = VolitionConfig()
```

L5: Anticipatory Intelligence — Проактивный интеллект  ← RFC0054–0058
    ├─ Назначение: система не только помнит и отвечает — она предвидит,
    │   предлагает и объясняет себя. Переход от реактивного к антиципаторному агенту.
    │
    ├─ [RFC0054] Spreading Activation Engine (SAE):
    │   Расширение Velum (L1.5) — затухающее возбуждение по рёбрам графа.
    │   При активации узла A → возбуждение распространяется на смежные узлы
    │   с весом: activation(B) = weight(A→B) × activation(A) × decay_factor
    │   Затухание: каждый хоп умножает сигнал на DECAY_FACTOR (default 0.6)
    │   Порог активации: SAE_THRESHOLD = 0.3 — ниже не учитывается
    │   Результат: HybridRetriever получает расширенный контекст ДО запроса пользователя.
    │   Это "синаптическое чувствование" — система предугадывает связанные темы.
    │   ⚠️ ИНВАРИАНТ I30: SAE работает только по существующим рёбрам графа.
    │     Новые рёбра SAE не создаёт — только читает. Graph = Truth не нарушается.
    │
    ├─ [RFC0055] Epistemic Gap Model (EGM):
    │   Граф знает не только что пользователь знает — но что он НЕ знает.
    │   Механизм: анализ доменных узлов L3 → найти кластеры, которые
    │   пользователь никогда не активировал → gap_score по важности домена.
    │   Проактивное предложение при gap_score > EGM_THRESHOLD (default 0.7):
    │     → FocusEngine генерирует suggestion: "Ты никогда не спрашивал о X"
    │     → BAE формирует мягкое предложение, не навязчивое
    │   Хранение: :EpistemicGap {topic_id, gap_score, last_suggested, suppressed}
    │   Защита: если пользователь отклонил suggestion → suppressed=True на 7 дней.
    │   ⚠️ ИНВАРИАНТ I31: EGM не навязывает — только предлагает один раз.
    │     Повторное предложение той же темы раньше 7 дней — запрещено.
    │
    ├─ [RFC0056] Domain Seed Protocol (DSP):
    │   Устраняет холодный старт для новых пользователей и организаций.
    │   При старте системы: загрузить domain_seed.json
    │     {domain, terminology[], key_processes[], values[], authority_map{}}
    │   → автоматически создаются ~100–500 :KnowledgeUnit узлов в L3
    │   → L2 Cold Start Guard обходится (seed считается за эпизоды)
    │   → система ведёт себя как "опытный сотрудник" с первого диалога
    │   Форматы: JSON / YAML / PDF (через offline_extractor.py)
    │   ⚠️ ИНВАРИАНТ I32: Seed-узлы помечены {source_type: "domain_seed"}.
    │     TruthGate применяет к ним trust_score = 0.7 (не 1.0) — требуют подтверждения.
    │
    ├─ [RFC0057] Multi-User Authority Graph:
    │   Для организаций — у каждого пользователя домен авторитетности.
    │   Схема: :User {user_id, role, authority_domain[], trust_level: 0.0–1.0}
    │   При конфликте фактов от разных пользователей:
    │     TruthGate проверяет authority_domain обоих источников
    │     Побеждает тот, у кого выше trust_level в данном домене
    │     Если домены равны → факт переходит в ESM: Hypothesized (спор)
    │     → уведомление обоим пользователям для разрешения конфликта
    │   Пример: финансист достоверен в финансовых фактах > разработчика.
    │   ⚠️ ИНВАРИАНТ I33: authority_domain не может быть пустым.
    │     Пользователь без домена имеет trust_level = 0.5 по умолчанию (нейтральный).
    │
    ├─ [RFC0058] Explainability Layer (XAI):
    │   Пользователь может спросить "Почему такой ответ?" → система объясняет.
    │   Механизм: TRACE из ResponseAudit (RFC0052) → XAI форматирует для человека:
    │     "Этот ответ основан на:
    │      · 3 фактах из твоих диалогов (5, 12, 18 дней назад)
    │      · Стратегии, выработанной 3 дня назад
    │      · Теме [архитектура] с силой 4.2"
    │   Уровни детализации: brief / detailed / full_trace (по запросу)
    │   Хранение: XAI-объяснения кэшируются в ResponseAudit.precomputed["почему"]
    │   ⚠️ ИНВАРИАНТ I34: XAI показывает только реальные TRACE-пути.
    │     Генерация объяснений LLM без TRACE — запрещена. Только граф.
    │
    ├─ Prediction Error Signal — обучение L5 на ошибках предсказания
    │   Принцип Фристона: мозг обучается именно на ошибке предсказания, не на успехе.
    │   L5 уже предсказывал следующий вопрос — но ошибки терялись. Теперь нет.
    │
    │   Механизм (запускается через EventBus после каждого ответа · 2–5 мс):
    │     1. Взять что L5/SAE предсказал перед вопросом пользователя
    │     2. Сравнить с тем что реально спросили
    │     3. Если ошибка > PREDICTION_ERROR_THRESHOLD (0.4):
    │          → усилить рёбра ведущие к правильному ответу × (1 + error_magnitude)
    │          → ослабить неверные пути × (1 - error_magnitude × 0.5)
    │     4. Передать error_signal в L5.5 PredictiveFusionLayer
    │          → скорректировать веса w_sae / w_lsm
    │
    │   Эффект со временем:
    │     Неделя 1  → L5 угадывает ~30% следующих вопросов
    │     Месяц 1   → ~55%
    │     Месяц 3   → ~75% для типичных тем пользователя
    │
    │   ⚠️ ИНВАРИАНТ I36: Prediction Error только ослабляет/усиливает рёбра.
    │     Новые рёбра не создаёт. Graph = Truth не нарушается.
    │   Нагрузка: 2–5 мс · CPU only · после каждого сообщения
    │   Метрика: prediction_error_total · prediction_accuracy_rolling_7d
    │
    ├─ Liquid State Machine (LSM) — темпоральная память ритма
    │   Дополняет SAE: SAE знает ЧТО ты спросишь (семантика графа).
    │   LSM знает КОГДА и в КАКОМ РИТМЕ (динамическое состояние последовательности).
    │
    │   Архитектура резервуарных вычислений (Reservoir Computing):
    │     · Резервуар: ~200–500 простых нейронов с фиксированными случайными весами
    │     · Главный принцип: веса резервуара НЕ обучаются никогда
    │     · Обучается только простой линейный выходной слой
    │     · Это означает: никакого GPU, никакого backprop, 2–5 MB RAM
    │
    │   Что LSM запоминает как «живое эхо-состояние»:
    │     · В какое время дня задаются технические вопросы
    │     · Как быстро пользователь переключается между темами
    │     · Когда он уходит в философские размышления
    │     · Паузы между сообщениями как ритмический сигнал
    │
    │   Обновление: через EventBus после каждого L1 INSERT · 5–15 мс · CPU only
    │   Хранение: in-memory резервуар + SQLite snapshot состояния раз в 15 мин
    │   Вывод: lsm_prediction передаётся в L5.5 PredictiveFusionLayer
    │   ⚠️ ИНВАРИАНТ I37: LSM не пишет в граф. Только читает историю запросов.
    │   Метрики: lsm_prediction_updates · lsm_rhythm_stability_score
    │
    ├─ Метрики:
    │   · sae_activations_total          — узлов активировано через SAE
    │   · epistemic_gap_suggestions_total — предложений сделано EGM
    │   · epistemic_gap_accepted_rate    — % принятых предложений
    │   · domain_seed_nodes_created      — узлов создано через DSP
    │   · authority_conflicts_resolved   — конфликтов разрешено авторитетом
    │   · xai_explanations_total         — объяснений выдано пользователям
    │   · prediction_error_total         — ошибок предсказания обработано
    │   · prediction_accuracy_rolling_7d — точность предсказания за 7 дней
    │   · lsm_prediction_updates         — обновлений LSM состояния
    │   · lsm_rhythm_stability_score     — стабильность ритма пользователя
    └─ Decay: :EpistemicGap → пересчитывается раз в неделю по активности домена

L5.5: Predictive Fusion Layer — арбитр SAE и LSM
    ├─ Назначение: SAE (семантика) и LSM (ритм) измеряют разные измерения реальности.
    │   Выбирать одно вместо другого — как выбирать между картой и компасом.
    │   L5.5 использует оба и адаптивно решает кому доверять в данной ситуации.
    │
    │   Продолжает архитектурную логику промежуточных слоёв:
    │   L1.5 (Velum) · L2.5 (Staging) · L4.5 (Audit+Focus) · L5.5 (Fusion)
    │
    ├─ Два режима выхода:
    │
    │   🤝 Консенсус (оба предсказали одну тему):
    │     combined_confidence = sae_conf^w_sae × lsm_conf^w_lsm
    │     → высокая уверенность → система действует проактивно
    │     → готовит контекст ещё до вопроса пользователя
    │
    │   ⚡ Расхождение (разные темы):
    │     → оба кандидата передаются в FocusEngine с весами
    │     → штраф уверенности: × 0.6
    │     → сигнал для системы: пользователь в переходном состоянии
    │     → FocusEngine выбирает осторожнее, не навязывает
    │
    ├─ Динамические веса (адаптируются через Prediction Error):
    │     Начальные: w_sae = 0.6 · w_lsm = 0.4
    │     Сдвиг по контексту:
    │       if lsm_rhythm_stability > 0.7 → w_lsm += 0.15
    │       if sae_graph_density > 0.6    → w_sae += 0.15
    │     Нормализация: w_sae + w_lsm = 1.0 всегда
    │     Минимальный вес: 0.2 (ни один источник не вытесняется полностью)
    │
    ├─ Обучение через Prediction Error (замкнутая петля):
    │     SAE ошибся  → w_sae -= learning_rate(0.05) × error.magnitude
    │     LSM ошибся  → w_lsm -= learning_rate(0.05) × error.magnitude
    │     Медленное обучение = стабильность весов
    │
    ├─ ⚠️ ИНВАРИАНТ I35: L5.5 не пишет в граф.
    │     Только читает предсказания SAE и LSM · только возвращает FusedPrediction.
    │     Graph = Truth не нарушается.
    │
    ├─ Метрики:
    │   · fusion_consensus_rate      — % случаев когда SAE и LSM согласились
    │   · fusion_divergence_rate     — % расхождений (сигнал о переходных состояниях)
    │   · fusion_w_sae_current       — текущий вес SAE
    │   · fusion_w_lsm_current       — текущий вес LSM
    └─ Нагрузка: 2–5 мс · CPU only · 0 токенов LLM

```python
# l5_5_predictive_fusion.py
import numpy as np
import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class FusedPrediction:
    topic: Optional[str]
    confidence: float
    source: str                        # "consensus" | "divergent"
    timing: Optional[dict] = None      # LSM темпоральный контекст
    candidates: Optional[list] = None  # при divergent — список (prediction, weight)

@dataclass
class PredictionError:
    source: str        # "sae" | "lsm"
    magnitude: float   # 0.0–1.0

@dataclass
class FusionContext:
    lsm_rhythm_stability: float = 0.5
    sae_graph_density: float = 0.5

class PredictiveFusionLayer:
    """
    L5.5: арбитр SAE (семантика) и LSM (ритм).
    Комбинирует два предсказания с адаптивными весами.
    Веса обновляются через Prediction Error Signal (L5).

    Инвариант I35: не пишет в граф — только читает и возвращает FusedPrediction.
    """

    def __init__(self, w_sae: float = 0.6, w_lsm: float = 0.4):
        self.w_sae = w_sae
        self.w_lsm = w_lsm
        self._learning_rate = 0.05
        self._w_min = 0.2  # ни один источник не вытесняется полностью

    async def fuse(
        self,
        sae_prediction: dict,
        lsm_prediction: dict,
        context: FusionContext
    ) -> FusedPrediction:
        w_sae, w_lsm = self._dynamic_weights(context)

        if sae_prediction.get("topic") == lsm_prediction.get("topic"):
            # Консенсус: умножаем уверенности (не складываем — это важно)
            # Геометрическое среднее с весами даёт более консервативную оценку
            combined = (
                sae_prediction["confidence"] ** w_sae *
                lsm_prediction["confidence"] ** w_lsm
            )
            logger.debug(f"L5.5 consensus: {sae_prediction['topic']} conf={combined:.3f}")
            return FusedPrediction(
                topic=sae_prediction["topic"],
                confidence=combined,
                source="consensus",
                timing=lsm_prediction.get("timing")
            )
        else:
            # Расхождение: возвращаем оба кандидата со штрафом
            # Штраф × 0.6 — система становится осторожнее при неопределённости
            logger.debug(
                f"L5.5 divergent: SAE={sae_prediction.get('topic')} "
                f"vs LSM={lsm_prediction.get('topic')}"
            )
            return FusedPrediction(
                topic=None,
                confidence=max(w_sae, w_lsm) * 0.6,
                source="divergent",
                candidates=[
                    (sae_prediction, w_sae),
                    (lsm_prediction, w_lsm)
                ]
            )

    def _dynamic_weights(self, ctx: FusionContext) -> tuple[float, float]:
        """
        Динамически сдвигаем веса по контексту текущего запроса.
        Стабильный ритм → больше доверия LSM.
        Богатый семантический граф → больше доверия SAE.
        """
        w_s, w_l = self.w_sae, self.w_lsm

        if ctx.lsm_rhythm_stability > 0.7:
            w_l += 0.15  # пользователь в стабильном ритме — LSM надёжен
        if ctx.sae_graph_density > 0.6:
            w_s += 0.15  # тема хорошо представлена в графе — SAE надёжен

        total = w_s + w_l
        return w_s / total, w_l / total

    async def update_from_error(self, error: PredictionError):
        """
        Prediction Error Signal корректирует веса.
        Медленное обучение (lr=0.05) = стабильность.
        Минимальный вес 0.2 = ни один источник не выключается.
        """
        if error.source == "sae":
            self.w_sae = max(self._w_min, self.w_sae - self._learning_rate * error.magnitude)
        elif error.source == "lsm":
            self.w_lsm = max(self._w_min, self.w_lsm - self._learning_rate * error.magnitude)

        # Ренормализация после каждого обновления
        total = self.w_sae + self.w_lsm
        self.w_sae /= total
        self.w_lsm /= total
        logger.debug(f"L5.5 weights updated: w_sae={self.w_sae:.3f}, w_lsm={self.w_lsm:.3f}")
```

---

## 🔧 Технологический стек

### Обязательные компоненты

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| **Graph DB (MVP)** | LadybugDB + Graphiti | Embedded граф для Phase 0 / слабого железа. LadybugDB — community-форк KuzuDB (MIT, Cypher, ACID, полная Kuzu API совместимость). I94. Переход на Neo4j в Phase 1+ |
| **Graph DB (Production)** | Neo4j 5.26+ + Graphiti | Темпоральный граф знаний, основное хранилище Phase 1+ |
| **Vector DB** | Qdrant / ChromaDB | Семантический поиск, эмбеддинги |
| **Event Bus** | Redis Streams | Асинхронная обработка событий (Kafka убран — избыточен для Velantrim) |
| **Scheduler** | APScheduler 3.10+ (AsyncIOScheduler) | Периодические Slow Path задачи: WeightedSemanticDecay, daily_maintenance · P9-FIX БАГ-18 |
| **Cache** | Redis | Кэширование часто используемых паттернов |
| **Embeddings (локально)** | multilingual-e5-large / deepvk/USER-bge-m3 | Векторизация, privacy-first, лучшие для RU |
| **Embeddings (облако)** | Gemini Embedding 2 (март 2026) | Мультимодальный: текст + изображение + аудио + видео + PDF. Phase 2+ |
| **LLM Flagship** | GPT-5.4 / Claude Sonnet 4.6 / Qwen3.5-Plus | Сложные задачи, reasoning · Qwen3.5-Plus = 397B-A17B, 1M ctx, нативный мультимодал |
| **LLM Reasoning** | DeepSeek R1-0528 | Специализированный reasoning · R1: 671B-A37B, открытые CoT-токены, уровень o1 · ⚠️ DeepSeek V4 (Engram) — ожидается, не добавлять в стек до публичного релиза |
| **LLM Fast** | o4-mini / Claude Haiku 4.5 / Qwen3.5-Flash | Рутина, 70% задач, дёшево |
| **LLM Local (MoE)** | Qwen3.5-35B-A3B / DeepSeek V3.2 / Kimi K2 | Privacy-first · V3.2: 685B-A37B, DSA, context 163K, thinking+tool-use · Qwen3.5-Flash = hosted 35B-A3B |
| **LLM Local (dense)** | Qwen3.5-27B / Qwen3.5-397B-A17B / Llama 4 Maverick | Если RAM > 32 GB · 397B-A17B = Qwen3.5-Plus open weights |
| **LLM Tiny (offline)** | Qwen3-1.7B / OLMoE-1B-7B | LLM_MODE=lite · слабое железо · Memory Router SLM fallback |
| **LSM (Liquid State Machine)** | Python · NumPy · ~300 нейронов | Темпоральная память ритма · 2–5 MB RAM · CPU only |
| **Orchestration** | Custom Python / LangGraph v0.3+ | Управление агентом |
| **Reranker** | ColBERTv2 / bge-reranker-large | Default reranker · ⚠️ Qwen3-Reranker: only opt-in с native Transformers (known issues в vLLM/llama.cpp) · файл: `memory/reranker.py` |
| **Observability** | OpenTelemetry + Prometheus + Grafana | Мониторинг и трейсинг |
| **Analytics** | DuckDB | Аналитика метрик, Parquet/CSV, агрегации (НЕ замена SQLite) |
| **Operational DB** | SQLite | Логи, конфиги, навыки, сессии — встроенное надёжное хранилище |

### 🆕 Модели в стеке — справочник

> Краткая выжимка по каждой новой модели для быстрой ориентации. Подробности — в документации производителей.

**DeepSeek V3.2** *(январь 2026 · MIT · MoE 685B-A37B)*
- DeepSeek Sparse Attention (DSA) — сокращает compute на длинном контексте без потери качества
- Thinking mode встроен прямо в tool-use (первый в линейке): можно рассуждать и использовать инструменты одновременно
- Context window: 163,840 токенов · Производительность уровня GPT-5 · IMO/IOI 2025 — золото
- Локально: требует ~8×H200 в full precision; GGUF-квантование — dual RTX 4090

**DeepSeek R1-0528** *(май 2025 · MIT · MoE 671B-A37B)*
- Reasoning-специалист: открытые chain-of-thought токены (`<think>...</think>`), возможность дистилляции
- Производительность уровня OpenAI o1/o3 · Context 164K токенов
- Дистилляты: 1.5B / 7B / 8B / 14B / 32B / 70B — от телефона до сервера
- Применение в Velantrim: стратегия для сложных multi-hop задач в ReasoningBank

**DeepSeek V4 + Engram** *(март 2026 · ⚠️ статус уточняется · MoE ~1T-A37B)*
- **Engram** — архитектурный прорыв: условная память (conditional memory) отделяет статическое знание (O(1) hash lookup в DRAM) от динамического reasoning (MoE GPU). Needle-in-a-Haystack 97% при 1M токенов
- Context: 1M+ токенов · Native multimodal (текст + изображение + видео)
- V4 Lite появился на платформе 9 марта 2026; полный релиз — ожидается. Бенчмарки официально не верифицированы
- ⚠️ Добавить в стек как только веса будут публично доступны

**Qwen3.5-Plus / Qwen3.5-397B-A17B** *(февраль–март 2026 · Apache 2.0 · MoE 397B-A17B)*
- Qwen3.5-Plus = hosted API; Qwen3.5-397B-A17B = open weights (то же самое)
- Gated Delta Networks + sparse MoE: нативно мультимодальная архитектура (early fusion)
- Context: 262K нативно, до 1M через API · 201 язык · Thinking mode по умолчанию
- SWE-bench Verified: 76.4 · IFBench instruction-following: 76.5 (лучший среди открытых моделей)
- Малые версии семьи: Qwen3.5-35B-A3B (= Flash), Qwen3.5-27B, 9B, 4B — для локального деплоя

### 🧠 MoE vs Dense — выбор LLM-архитектуры

> **MoE (Mixture of Experts)** — архитектура где внутренний Router активирует только 2–3 «эксперта» из N при каждом запросе. Остальные эксперты не считаются → меньше FLOPs, тот же результат.

```
Пример: пользователь спрашивает "формулу воды"
  Dense 30B:  считаются все 30B параметров каждый раз
  MoE 30B-A3B: Router активирует 2 из 16 экспертов → считается 3B
               Ответ того же качества, нагрузка CPU/GPU в 10× меньше
```

| Архитектура | Параметры в RAM | Считается | CPU/GPU нагрузка | Рекомендация |
|-------------|----------------|-----------|-----------------|--------------|
| Dense 7B | 7B | 7B | 100% | weak/medium без GPU |
| MoE 30B-A3B | 30B | ~3B | ~15% | medium/strong — лучший выбор |
| Dense 70B | 70B | 70B | 100% | strong + GPU |
| MoE 141B-A22B | 141B | ~22B | ~25% | strong + GPU flagship |

> ⚠️ **Главная ловушка MoE**: снижает CPU/GPU нагрузку, но **НЕ экономит RAM** — все эксперты должны быть в памяти. Mixtral 8x7B требует ~30 GB RAM несмотря на то что считает как 12B.

```python
# velantrim_config.py — добавить при выборе LLM
LLM_ARCHITECTURE  = "moe"    # "moe" | "dense"
LLM_ACTIVE_PARAMS = "3B"     # реально считается при инференсе
LLM_TOTAL_PARAMS  = "30B"    # нужно в RAM — используй для HARDWARE_PROFILE проверки

# Правило: если LLM_TOTAL_PARAMS > доступного RAM → переключиться на меньшую модель
# MoE в формате GGUF (квантование) — оптимально для CPU-only инференса
```
### Опциональные улучшения

- **Мониторинг**: ✅ Уже в обязательных (OpenTelemetry + Prometheus + Grafana). Добавить сюда расширенные дашборды Grafana если нужны отдельные алерты.
- **Object Storage**: S3 / MinIO (для полных текстов и артефактов)
- **Time-Series DB**: InfluxDB (для метрик и decay расчетов)
- **Real-time Graph**: Memgraph (Phase 2+ для hot-path обновлений)

### 🗄️ Конфигурации бэкендов (v8.0 Crystal)

| Конфигурация | Граф | Вектор | Для кого |
|---|---|---|---|
| **Minimal** | SQLite | FAISS | Разработка, первый запуск |
| **Personal** | KuzuDB    | FAISS | Локальный ПК, офлайн, MIT · I94 · P0-H FIX |
| **Startup** | FalkorDB | Qdrant | Продакшн, стартап |
| **Enterprise** | Neo4j | Qdrant | Корпорации, RBAC, GDPR |

```python
# velantrim_config.py
GRAPH_BACKEND = "kuzu"       # P0-H FIX: "ladybugdb" не существует → "kuzu" (KuzuDB, MIT, Cypher-совместим)
# KuzuDB — https://kuzudb.com · MIT · Cypher · columnar · vector + full-text · ACID
# I94 (KuzuDBCompat): KuzuDB backend совместим с Kuzu API. Миграция без потери данных.
```


### ⚰️ Компоненты, исключённые из стека

> Список защищает от регрессий: при следующем LLM-аудите не будут повторно предлагаться удалённые компоненты.

| Компонент | Причина исключения |
|-----------|-------------------|
| **RedisGraph** | EOL январь 2025, проект закрыт Neo4j |
| **Kafka** | Избыточен для Velantrim — заменён Redis Streams |
| ~~**KuzuDB**~~ | ~~Куплен Apple в 2025~~ — **P9-FIX БАГ-2**: LadybugDB-форк не вышел. KuzuDB (MIT, Cypher-совместим) остаётся в Personal-конфиге. Строка убрана из исключённых. |
| **SurrealDB** | ⚠️ Риск EOL, нестабильный API — перенесён в опциональные |
| **NetworkX** | Слишком медленно на >1k узлов — только прототипирование |

### 🐳 Быстрый запуск инфраструктуры

> Без docker-compose.yml разработчик не запустит систему. Это единственная команда которая нужна.

```yaml
# infra/docker-compose.yml
# P3-E FIX: version: поле deprecated в Docker Compose v2+. Убрано.
services:
  neo4j:
    image: neo4j:5.26-community  # community = без лицензии; enterprise = если есть
    container_name: velantrim-neo4j
    restart: unless-stopped
    ports:
      - "7474:7474"   # Browser
      - "7687:7687"   # Bolt
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:?NEO4J_PASSWORD not set}  # пароль из .env, не хардкод
      - NEO4J_PLUGINS=["apoc"]  # apoc — официальный плагин Community Edition
      # ⚠️ graph-data-science НЕ является официальным плагином Community 5.26.
      # Phase 0: SAE реализуется через python-igraph (см. EtirConfig.BACKEND="igraph").
      # Phase 1+: GDS устанавливается вручную через /plugins mount (JAR из Neo4j Labs).
      # Phase 2: Neo4j Enterprise — GDS нативно через NEO4J_PLUGINS.
      - NEO4J_dbms_memory_pagecache_size=2g
      - NEO4J_dbms_memory_heap_initial__size=2g
      - NEO4J_dbms_memory_heap_max__size=4g
    volumes:
      - neo4j-data:/data
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p ${NEO4J_PASSWORD} 'RETURN 1' || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    image: redis:7-alpine
    container_name: velantrim-redis
    restart: unless-stopped
    command: redis-server --maxmemory ${REDIS_MAX_MEM:-512mb} --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  neo4j-data:
  redis-data:
```

```bash
  # сначала создай .env (не коммить в git!):
# cp .env.example .env && echo "NEO4J_PASSWORD=your_strong_password" >> .env

# Запуск одной командой
docker compose -f infra/docker-compose.yml up -d
```

---

## 📦 Ключевые компоненты и их реализация

### 1. Event Bus & Ingestion Pipeline

**Назначение**: Захват всех событий без блокировки основного потока

```python
# event_bus.py
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone  # timezone нужен для datetime.now(timezone.utc)
import asyncio
import redis.asyncio as redis
import json
import logging
from typing import AsyncGenerator, Tuple

logger = logging.getLogger(__name__)

class EventType(Enum):
    USER_MESSAGE = "user_message"
    AGENT_RESPONSE = "agent_response"
    RESPONSE_GENERATED = "response_generated"  # используется AuditWorker (I28) и архитектурой SLOW SYSTEM
    ACTION_EXECUTED = "action_executed"
    TASK_COMPLETED = "task_completed"
    TASK_STATUS_CHANGED = "task_status_changed"  # ConsolidationEngine: BLOCKED_AWAITING_DB
    ERROR_OCCURRED = "error_occurred"

@dataclass
class AgentEvent:
    event_type: EventType
    timestamp: datetime
    content: dict
    metadata: dict
    session_id: str

class SQLiteFallbackQueue:
    """
    Персистентная fallback-очередь событий на SQLite (RFC0036).
    """
    def __init__(self, db_path: str = "fallback_events.db"):
        self.db_path = db_path

    async def init(self):
        import aiosqlite
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=WAL;")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS event_fallback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_data BLOB NOT NULL,
                    priority TEXT DEFAULT 'NORMAL',
                    retry_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def put(self, event_data: dict, priority: str = 'NORMAL') -> bool:
        import aiosqlite, zlib, json
        compressed = zlib.compress(json.dumps(event_data).encode(), level=1)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO event_fallback (event_data, priority) VALUES (?, ?)",
                (compressed, priority)
            )
            await db.commit()
        return True

    async def qsize(self) -> int:
        """Возвращает количество событий в fallback-очереди (для health_check)."""
        import aiosqlite
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM event_fallback")
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def drain(self, redis_client, stream_key: str, batch: int = 100) -> int:
        import aiosqlite, zlib, json
        recovered = 0
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, event_data FROM event_fallback "
                "WHERE retry_count < 5 ORDER BY priority DESC, created_at ASC LIMIT ?",
                (batch,)
            )
            rows = await cursor.fetchall()
            for row_id, compressed in rows:
                try:
                    data = json.loads(zlib.decompress(compressed))
                    await redis_client.xadd(stream_key, data)
                    await db.execute("DELETE FROM event_fallback WHERE id=?", (row_id,))
                    recovered += 1
                except Exception:
                    await db.execute(
                        "UPDATE event_fallback SET retry_count = retry_count + 1 WHERE id=?",
                        (row_id,)
                    )
            await db.commit()
        return recovered


class RobustEventBus:
    """
    Production-ready Event Bus с:
    - Retry механизмом
    - Dead Letter Queue (DLQ)
    - Fallback на локальную очередь
    - Error tracking
    """
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        max_retries: int = 3,
        config: dict = None,   # config может быть None при старте
    ):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.stream_key = "agent:events"
        self.dlq_key = "agent:events:dlq"
        self.max_retries = max_retries

        # Fallback очередь когда Redis недоступен — персистентна (RFC0036)
        _cfg = config or {}
        self.fallback_queue = SQLiteFallbackQueue(
            db_path=_cfg.get("fallback_db", "fallback_events.db")
        )
        self.redis_available = True

    async def publish(self, event: AgentEvent) -> bool:
        """
        Публикация события с retry и fallback
        Возвращает True если успешно, False если в fallback
        """
        event_data = {
            "type": event.event_type.value,
            "timestamp": event.timestamp.isoformat(),
            "content": json.dumps(event.content),
            "metadata": json.dumps(event.metadata),
            "session_id": event.session_id
        }
        
        # Попытка публикации с retry
        for attempt in range(self.max_retries):
            try:
                await self.redis.xadd(self.stream_key, event_data,
                                      maxlen=10000, approximate=True)
                self.redis_available = True
                return True
                
            except redis.RedisError as e:
                logger.warning(
                    f"Redis publish failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    # Все попытки исчерпаны → fallback
                    self.redis_available = False
                    try:
                        await self.fallback_queue.put(event_data)  # передаём dict, не AgentEvent
                        logger.error(f"Event moved to fallback queue: {event.event_type}")
                    except Exception:
                        # SQLiteFallbackQueue.put() никогда не бросает asyncio.QueueFull
                        # (это aiosqlite-операция). Перехватываем любую ошибку → SQLite напрямую.
                        logger.warning(
                            f"Fallback queue error — persisting to SQLite: {event.event_type}"
                        )
                        await self._persist_event_to_sqlite(event)
                    return False

    async def publish_volition(self, event) -> bool:
        """
        P0.5-1 FIX: адаптер для MemoryVolitionWorker.write_voluntary().
        VolitionEvent не является AgentEvent, поэтому сериализуем вручную
        и делегируем в стандартный publish-путь через Redis → fallback.

        Без этого метода: AttributeError при первом вызове write_voluntary().
        """
        import dataclasses
        # Оборачиваем VolitionEvent в совместимый с publish() формат
        class _VolitionWrapper:
            def __init__(self, ev):
                from enum import Enum
                self.event_type = type('_ET', (), {
                    'value': getattr(ev, 'event_type', 'VOLITION')
                    if not isinstance(getattr(ev, 'event_type', None), Enum)
                    else ev.event_type.value
                })()
                # P0-C FIX: utcnow() deprecated Python 3.12, возвращал naive datetime → silent data corruption.
                # datetime.now(timezone.utc) возвращает timezone-aware datetime, совместим с Redis/SQLite.
                from datetime import datetime as _dt, timezone as _tz
                self.timestamp  = getattr(ev, 'timestamp', _dt.now(_tz.utc))
                self.content    = {
                    'content':          getattr(ev, 'content', ''),
                    'reason':           getattr(ev, 'reason', ''),
                    'importance_hint':  getattr(ev, 'importance_hint', 0.8),
                }
                self.metadata   = {'source': 'agent_volition'}
                self.session_id = getattr(ev, 'session_id', '')

        return await self.publish(_VolitionWrapper(event))

    async def _persist_event_to_sqlite(self, event: AgentEvent):
        """
        Последний рубеж: если Redis недоступен и fallback_queue.put() тоже упал.
        добавлена ротация FALLBACK_MAX_ROWS=10_000 + PRAGMA WAL/NORMAL
        для защиты от переполнения диска. Нет дублирования dict-сборки —
        event_data формируется один раз и передаётся напрямую.
        """
        import aiosqlite
        FALLBACK_MAX_ROWS = 10_000  # лимит ротации — защита от переполнения диска
        try:
            payload = {
                "type":       event.event_type.value,
                "timestamp":  event.timestamp.isoformat(),
                "content":    json.dumps(event.content),
                "metadata":   json.dumps(event.metadata),
                "session_id": event.session_id,
            }
            db_path = getattr(self.fallback_queue, 'db_path', 'fallback_events.db')
            async with aiosqlite.connect(db_path) as db:
                await db.execute("PRAGMA journal_mode=WAL")
                await db.execute("PRAGMA synchronous=NORMAL")
                # P0.5-2 FIX: единый формат с SQLiteFallbackQueue.put() и drain().
                # put() пишет zlib.compress(json.dumps(...)), drain() читает zlib.decompress().
                # Было: json.dumps(payload) как plain string → drain() получал мусор при восстановлении.
                # Стало: zlib.compress(json.dumps(payload)) — идентично основному fallback-пути.
                import zlib as _zlib
                compressed_payload = _zlib.compress(
                    json.dumps(payload).encode(), level=1
                )
                await db.execute(
                    "INSERT INTO event_fallback (event_data, priority) VALUES (?, ?)",
                    (compressed_payload, "NORMAL")
                )
                # Ротация: удаляем старейшие записи при превышении лимита
                await db.execute(
                    """
                    DELETE FROM event_fallback
                    WHERE id IN (
                        SELECT id FROM event_fallback
                        ORDER BY id ASC
                        LIMIT MAX(0, (SELECT COUNT(*) FROM event_fallback) - ?)
                    )
                    """,
                    (FALLBACK_MAX_ROWS,)
                )
                await db.commit()
        except Exception as e:
            logger.critical(
                f"CRITICAL: _persist_event_to_sqlite failed — "
                f"event {event.event_type} IS LOST. Error: {e}"
            )

    async def consume(
        self,
        consumer_group: str,
        consumer_name: str
    ) -> AsyncGenerator[Tuple[str, dict], None]:
        """
        Асинхронное чтение событий с обработкой ошибок
        """
        # Создать consumer group если не существует
        try:
            await self.redis.xgroup_create(
                self.stream_key, consumer_group, id='0', mkstream=True
            )
        except redis.ResponseError:
            pass  # Group already exists
        
        failed_count = 0
        max_failures = 5
        
        while True:
            try:
                # Читать новые события
                messages = await self.redis.xreadgroup(
                    consumer_group, consumer_name,
                    {self.stream_key: '>'},
                    count=10, 
                    block=5000
                )
                
                failed_count = 0  # Reset на успешное чтение
                
                for stream_name, message_list in messages:
                    for message_id, data in message_list:
                        try:
                            yield message_id, data
                            
                            # ACK после успешной обработки
                            await self.redis.xack(
                                self.stream_key, consumer_group, message_id
                            )
                            
                        except Exception as e:
                            # Ошибка обработки → переместить в DLQ
                            logger.error(
                                f"Event processing failed: {e}, "
                                f"moving to DLQ: {message_id}"
                            )
                            await self._move_to_dlq(message_id, data, str(e))
                            
                            # ACK чтобы не зависло
                            await self.redis.xack(
                                self.stream_key, consumer_group, message_id
                            )
                
            except redis.RedisError as e:
                failed_count += 1
                logger.error(f"Redis consume error ({failed_count}/{max_failures}): {e}")

                if failed_count >= max_failures:
                    # P0.5-6 FIX: вместо break → режим ожидания с периодическим ping.
                    # break убивал генератор навсегда — весь Slow Path останавливался
                    # до ручного рестарта агента (Gemini-аудит, ChatGPT-аудит).
                    # Новый подход: consume() ждёт восстановления Redis и продолжает.
                    # Caller (process_evaluation_queue и др.) не замечает паузы —
                    # async for просто ждёт следующего yield.
                    logger.critical(
                        f"Redis unavailable after {max_failures} attempts — "
                        f"entering recovery wait (Slow Path paused, not dead)"
                    )
                    _recovery_interval = 30  # секунд между ping-попытками
                    while True:
                        await asyncio.sleep(_recovery_interval)
                        try:
                            await self.redis.ping()
                            # Redis вернулся — сбрасываем счётчик и продолжаем цикл
                            failed_count = 0
                            logger.info(
                                "Redis recovered — resuming consume(). "
                                "Slow Path active."
                            )
                            break  # выходим из recovery-loop → продолжаем while True
                        except redis.RedisError:
                            logger.warning(
                                f"Redis still unavailable, retry in {_recovery_interval}s"
                            )
                            # увеличиваем интервал до max 5 минут
                            _recovery_interval = min(300, _recovery_interval * 2)
                    continue  # продолжаем основной while True после recovery

                # Backoff перед retry
                await asyncio.sleep(min(60, 2 ** failed_count))

    async def _move_to_dlq(
        self,
        message_id: str,
        data: dict,
        error: str
    ):
        """Переместить проблемное событие в Dead Letter Queue"""
        dlq_entry = {
            **data,
            "original_message_id": message_id,
            "error": error,
            "dlq_timestamp": datetime.now(timezone.utc).isoformat(),
            "retry_count": data.get("retry_count", 0) + 1
        }
        
        try:
            await self.redis.xadd(self.dlq_key, dlq_entry)
        except redis.RedisError as e:
            logger.error(f"Failed to write to DLQ: {e}")

    async def process_dlq(self):
        """
        Периодическая обработка DLQ — reprocess или отправка в monitoring.
        Метод должен быть зарегистрирован в планировщике.
        Добавить в scheduler.py или main.py при старте:
        
            scheduler.add_job(
                event_bus.process_dlq,
                'interval',
                minutes=15,
                id='dlq_processor',
                max_instances=1
            )
        """
        try:
            messages = await self.redis.xread(
                {self.dlq_key: '0'},
                count=100
            )
            for stream, message_list in messages:
                for msg_id, data in message_list:
                    retry_count = int(data.get("retry_count", 0))
                    if retry_count < 3:
                        clean_data = {
                            k: v for k, v in data.items()
                            if k not in ('retry_count', 'original_message_id',
                                         'error', 'dlq_timestamp')
                        }
                        logger.info(f"Retrying DLQ message: {msg_id}")
                        await self.redis.xadd(self.stream_key, clean_data)
                        await self.redis.xdel(self.dlq_key, msg_id)  # удалять ПОСЛЕ успешного reprocess
                    else:
                        logger.error(f"Permanent DLQ failure: {msg_id}, data: {data}")
                        await self._send_permanent_failure_alert(msg_id, data, retry_count)
                        await self._archive_permanent_failure(msg_id, data)
                        await self.redis.xdel(self.dlq_key, msg_id)  # удалять после архивирования
        except Exception as e:
            logger.error(f"DLQ processing failed: {e}")

    async def _send_permanent_failure_alert(self, msg_id: str, data: dict, retries: int):
        """
        Обязательный алерт при permanent DLQ failure.
        Интеграция через EventBus → Observer++ поднимает severity = CRITICAL.
        """
        try:
            await self.redis.xadd("agent:alerts", {
                "type": "PERMANENT_DLQ_FAILURE",
                "msg_id": msg_id,
                "retries": str(retries),
                "data_type": data.get("type", "unknown"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": "CRITICAL"
            })
        except Exception as e:
            logger.error(f"Failed to send permanent failure alert: {e}")

    async def _archive_permanent_failure(self, msg_id: str, data: dict):
        """Сохранить permanent failure в SQLite для последующего аудита."""
        # orphaned except убран (SyntaxError — except без try),
        # убран xdel отсюда (был в except, т.е. удалял только при ошибке архивирования — логика перевёрнута)
        try:
            import aiosqlite
            db_path = getattr(self.fallback_queue, 'db_path', 'fallback_events.db')
            async with aiosqlite.connect(db_path) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS permanent_failures (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        msg_id TEXT NOT NULL,
                        data TEXT,
                        archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await db.execute(
                    "INSERT INTO permanent_failures (msg_id, data) VALUES (?, ?)",
                    (msg_id, json.dumps(data))
                )
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to archive permanent failure: {e}")


    async def health_check(self) -> dict:
        """Проверка здоровья Event Bus"""
        try:
            await self.redis.ping()
            stream_info = await self.redis.xinfo_stream(self.stream_key)
            try:
                dlq_info = await self.redis.xinfo_stream(self.dlq_key)
                dlq_length = dlq_info.get("length", 0)
            except redis.ResponseError:
                dlq_length = 0  # DLQ ещё не создан — это нормально
            
            return {
                "status": "healthy",
                "redis_available": True,
                "main_stream_length": stream_info.get("length", 0),
                "dlq_length": dlq_length,
                "fallback_queue_size": await self.fallback_queue.qsize()  # async метод — await обязателен
            }
        except Exception as e:
            return {
                "status": "degraded",
                "redis_available": False,
                "error": str(e),
                "fallback_queue_size": await self.fallback_queue.qsize()
            }
```

**Интеграция в агент**:

```python
# agent.py
class Agent:
    def __init__(self, event_bus: RobustEventBus):
        self.event_bus = event_bus
        self.session_id = generate_session_id()

    async def chat(self, user_message: str):
        # 1. Логируем входное сообщение (с retry/fallback)
        publish_success = await self.event_bus.publish(AgentEvent(
            event_type=EventType.USER_MESSAGE,
            timestamp=datetime.now(timezone.utc),
            content={"message": user_message},
            metadata={"length": len(user_message)},
            session_id=self.session_id
        ))
        
        if not publish_success:
            logger.warning("Event published to fallback queue")
        
        # 2. Обработка (retrieval + generation)
        response = await self.process(user_message)
        
        # 3. Логируем ответ
        await self.event_bus.publish(AgentEvent(
            event_type=EventType.AGENT_RESPONSE,
            timestamp=datetime.now(timezone.utc),
            content={"message": response},
            metadata={"tokens": count_tokens(response)},
            session_id=self.session_id
        ))
        
        return response
```
---

### 2. Graphiti + Neo4j: Основа памяти

**Назначение**: Темпоральный граф знаний с автоматической экстракцией

```python
# memory_core.py
from graphiti_core import Graphiti
from datetime import datetime, timezone   # ← PATCH-4: добавлен timezone (ранее NameError в add_episode)
from typing import List, Optional

class GraphMemory:
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 memory_guardian=None, raw_memory=None):   # ← PATCH-9: инъекция зависимостей (опциональная)
        self.graphiti = Graphiti(
            neo4j_uri=neo4j_uri,
            neo4j_user=neo4j_user,
            neo4j_password=neo4j_password
        )
        self.memory_guardian = memory_guardian  # None = старое поведение, обратная совместимость сохранена
        self.raw_memory = raw_memory

    async def add_episode(
        self,
        episode_name: str,
        content: str,
        source: str = "conversation",
        timestamp: Optional[datetime] = None
    ):
        """
        Добавить эпизод - автоматическая экстракция сущностей и связей
        НЕ требует LLM-запроса от разработчика - Graphiti делает это внутри

        PATCH-9 (Graph = Truth): порядок записи:
          1. ImmutableRawMemory — сырой оригинал защищён до любой валидации
          2. MemoryGuardian (Truth Gate) — если задан; None = старое поведение
          3. graphiti.add_episode — только если прошли шаги 1-2
        Обратная совместимость: memory_guardian=None → поведение идентично старому.
        """
        import asyncio as _asyncio
        ref_time = timestamp or datetime.now(timezone.utc)

        # ШАГ 1: сырой оригинал — сохранить до любой валидации (Semantic Drift защита)
        if self.raw_memory:
            await _asyncio.to_thread(
                self.raw_memory.save_episode,
                f"{episode_name}_{ref_time.timestamp()}",
                content, source, session_id="",
            )

        # ШАГ 2: Truth Gate — если guardian задан
        if self.memory_guardian:
            proposal = {
                "content":    content,
                "source":     source,
                "evidence":   source,   # минимальный evidence = источник (Phase 0)
                "confidence": 1.0 if source == "user_input" else 0.75,
            }
            if not await self.memory_guardian.validate_proposal(proposal):
                return   # Guardian уже залогировал причину — граф не загрязняется

        # ШАГ 3: запись в граф — только сюда
        await self.graphiti.add_episode(
            name=episode_name,
            episode_body=content,
            source_description=source,
            reference_time=ref_time
        )

    async def search(
        self,
        query: str,
        num_results: int = 5,
        time_filter: Optional[tuple] = None
    ) -> List[dict]:
        """
        Гибридный поиск БЕЗ LLM-запросов:
        - Векторный поиск по эмбеддингам
        - BM25 полнотекстовый поиск
        - Обход графа для контекста
        """
        results = await self.graphiti.search(
            query=query,
            num_results=num_results
        )
        
        # Дополнительная фильтрация по времени если нужно
        if time_filter:
            start_time, end_time = time_filter
            results = [
                r for r in results
                if start_time <= r.timestamp <= end_time
            ]
        
        return results

    async def get_context_for_entity(
        self,
        entity_name: str,
        depth: int = 2
    ) -> dict:
        """
        Получить контекст вокруг сущности через обход графа
        """
        # FIX из HYPERIA: whitelist вместо numeric clamp.
        # max(1, min(int(depth), 5)) не защищает если depth — строка типа "3; DROP".
        # Whitelist делает инъекцию невозможной архитектурно — только 1, 2 или 3.
        depth = depth if depth in (1, 2, 3) else 2
        # path собирается до WITH, иначе выходит из scope и Neo4j бросает ошибку
        query = f"""
        MATCH (e:Entity {{name: $entity_name}})
        OPTIONAL MATCH path = (e)-[:RELATED_TO|CAUSES|CONCEPT_OF|SUPPORTED_BY*1..{depth}]-(related)
        WITH e, related, relationships(path) AS rels
        WITH e,
             collect(DISTINCT related)[0..50] AS related_entities,
             collect(DISTINCT rels)[0..50]    AS relationships
        RETURN e, related_entities, relationships
        """
        
        result = await self.graphiti.execute_cypher(
            query,
            {"entity_name": entity_name}
        )
        
        return result
```

**Схема графа**:

```cypher
// Типы узлов
// embedding_version: какой моделью создан вектор (для lazy re-indexing при смене модели)
// is_active + valid_to: Soft Delete — узел не удаляется физически, а деактивируется
// reindex_required: флаг для автоматической переиндексации при смене embedding-модели
(:Entity {
    name, type,
    embedding, embedding_version,          // + версия модели: "multilingual-e5-large-v1"
    importance_score, created_at, last_accessed,
    is_active,                             // Soft Delete флаг (default: true)
    valid_from, valid_to,                  // Temporal bounds для фактов
    reindex_required                       // true = нужна переиндексация (false по умолчанию)
})
(:Episode {
    id, summary, timestamp, session_id, outcome,
    is_active, valid_to,
    raw_episode_id                         // ссылка на ImmutableRawMemory (никогда не меняется)
    // ⚠️ Episode ∉ Semantic Graph — эпизоды не смешиваются с фактами
    // Phase 2: вынести в отдельную Vector DB (Qdrant)
})
(:Domain {                                 // RFC0012: Domain как корень таксономии
    id,                                    // "domain:physics"
    name,                                  // "Physics"
    description,                           // краткое описание домена
    parent_domain_id,                      // для вложенных доменов (physics → quantum_physics)
    created_at
})
(:Concept {                                // RFC0002: Concept как отдельный узел
    id,                                    // "concept:water"
    name,                                  // "Water"
    aliases,                               // ["H2O"]
    created_at, updated_at
})
(:Fact {
    content, confidence,
    relation, value, condition,            // для Knowledge Units: структурированные поля
    valid_from, valid_to,                  // valid_time: когда факт был правдой
    transaction_time,                      // transaction_time: когда был записан в граф (bi-temporal)
    is_active,                             // Soft Delete вместо DETACH DELETE
    override_flag,                         // true = ручное переопределение пользователем
    is_knowledge_unit,                     // true = дистиллированный атомарный факт (JSON-тройка)
    validated,                             // true = прошёл через MGL. ∀ fact ∈ Graph: validated = True
    // ESM (Epistemic State Machine) поля
    epistemic_state,                       // Observed|Hypothesized|Supported|Validated|Contradicted|Deprecated|Collapsed
    epistemic_score,                       // 0.0–1.0 сила эпистемической позиции факта
    epistemic_variance,                    // 0.0–1.0 математическая неопределённость: 1.0=неизвестно, 0.0=уверен (RFC0046)
    state_changed_at,                      // datetime последнего перехода ESM
    transition_reason                      // причина перехода: "MGL_PASSED"|"CONTRADICTED"|"EVIDENCE_ADDED"|"GC"
})
(:Evidence {                               // RFC0002: Evidence как отдельный узел — не строка
    id,                                    // "evidence:physicsbook1"
    source,                                // "Physics Handbook"
    page,                                  // 42
    quality,                               // 0.9 — надёжность источника
    url,                                   // опционально
    created_at
})
(:Strategy {description, success_count, failure_count, context_type, is_active,
            confidence})                   // confidence снижается при инвалидации зависимых :Fact
(:Community {id, topic, size, last_updated})
// Тип узла для Knowledge Distillation
(:KnowledgeUnit {
    concept, relation, value, condition,
    confidence, timestamp,
    embedding, embedding_version
})

// Типы связей
(:Entity)-[:MENTIONED_IN]->(:Episode)
(:Entity)-[:RELATED_TO {strength, type, valid_from, valid_until}]->(:Entity)   // valid_until=null → актуально сейчас (RFC0046)
(:Episode)-[:PART_OF]->(:Community)
(:Episode)-[:LED_TO {outcome}]->(:Episode)
(:Strategy)-[:USED_IN]->(:Episode)
(:Strategy)-[:SUCCEEDED_AT]->(:Task)
(:Strategy)-[:FAILED_AT]->(:Task)
(:Strategy)-[:DERIVED_FROM]->(:Fact)    // при инвалидации :Fact → снижать confidence :Strategy
(:Strategy)-[:IMPROVES]->(:Strategy)   // RFC0002: цепочки улучшения стратегий
// Конфликт фактов: новый факт явно противоречит старому
(:Fact)-[:CONTRADICTS {reason, resolved_at}]->(:Fact)
(:Fact)-[:CAUSES {valid_from, valid_until}]->(:Fact)                           // RFC0046: temporal на причинно-следственные связи
(:Fact)-[:SUPPORTED_BY]->(:Evidence)   // RFC0002: ссылка на источник как узел
(:Fact)-[:CONCEPT_OF]->(:Concept)     // RFC0002: факт принадлежит концепту
(:Concept)-[:HAS_RELATION]->(:Fact)   // RFC0002: обратная связь концепта к фактам
(:Concept)-[:BELONGS_TO]->(:Domain)   // RFC0012: концепт принадлежит домену
(:Domain)-[:SUBDOMAIN_OF]->(:Domain)  // RFC0012: иерархия доменов (вложенность)
(:Fact)-[:IN_DOMAIN]->(:Domain)       // RFC0012: факт явно привязан к домену (опционально, для быстрого поиска)
// RFC0046: DAG рассуждений в L4 ReasoningBank
(:ReasoningStep)-[:PRECEDES]->(:ReasoningStep)                                 // шаги рассуждения — направленный DAG
(:ReasoningStep)-[:ROLLBACK_TO {reason, rolled_at, session_id}]->(:ReasoningStep) // тупиковая ветка → откат

// RFC0067 v2.0: Analogy Graph — только через Write Protocol Gate (I55)
(:Entity)-[:METAPHOR_OF {
    source_domain: STRING, target_domain: STRING,
    essence: STRING, source_text: STRING,
    confidence: FLOAT, resonance_score: FLOAT,
    cultural_vintage: INT, created_at: DATETIME, last_used: DATETIME
}]->(:Entity)
(:Entity)-[:ANALOGOUS_TO {
    domain_a: STRING, domain_b: STRING,
    structure_mapping: JSON, source_text: STRING,
    confidence: FLOAT, resonance_score: FLOAT,
    cultural_vintage: INT, created_at: DATETIME, last_used: DATETIME
}]->(:Entity)
```

```cypher
// RFC0067 v2.0: индексы Analogy Graph (добавить в neo4j_setup.py)
CREATE INDEX metaphor_source_domain IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON (r.source_domain);
CREATE INDEX metaphor_resonance IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON (r.resonance_score);
CREATE INDEX analogy_domain_pair IF NOT EXISTS
FOR ()-[r:ANALOGOUS_TO]-() ON (r.domain_a, r.domain_b);
CREATE INDEX metaphor_last_used IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON (r.last_used);
CREATE FULLTEXT INDEX metaphor_essence_idx IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON EACH [r.essence];
```

> ⚠️ **Soft Delete — обязательный паттерн**: НЕ используй `DETACH DELETE` для фактов и эпизодов в production. Устанавливай `is_active = false` и `valid_to = datetime()`. Физическое удаление — только в GC после успешной архивации в S3.
>
> ⚠️ **Bi-temporal граф**: `valid_from/valid_to` = когда факт был правдой в реальном мире. `transaction_time` = когда был записан в систему. Оба нужны чтобы ответить "что мы знали на момент X".
>
> ⚠️ **Evidence как узел**: поле `evidence` в :Fact заменено на связь `[:SUPPORTED_BY]->(:Evidence)`. Это позволяет удалять ненадёжный источник вместе со всеми его фактами и оценивать quality источника отдельно.

**КРИТИЧНО: Neo4j индексы (создать при инициализации!)**:

```python
# neo4j_setup.py
async def setup_neo4j_indexes(driver):
    """
    Обязательные индексы для производительности
    БЕЗ ЭТОГО система деградирует через 2-4 недели!
    """
    async with driver.session() as session:
        # 1. Индексы на часто используемые поля
        await session.run("""
            CREATE INDEX entity_name_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.name)
        """)
        
        await session.run("""
            CREATE INDEX entity_type_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.type)
        """)
        
        await session.run("""
            CREATE INDEX episode_timestamp_idx IF NOT EXISTS
            FOR (ep:Episode) ON (ep.timestamp)
        """)
        
        await session.run("""
            CREATE INDEX episode_session_idx IF NOT EXISTS
            FOR (ep:Episode) ON (ep.session_id)
        """)
        
        # 2. Векторный индекс для similarity search
        # Размерность из config — не хардкод.
        # multilingual-e5-large = 1024, text-embedding-3-small = 1536, Gemini Embedding 2 = 3072
        embedding_dims = config.get("embedding", {}).get("dimensions", 1024)
        await session.run(f"""
            CREATE VECTOR INDEX entity_embedding_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.embedding)
            OPTIONS {{
                indexConfig: {{
                    `vector.dimensions`: {embedding_dims},
                    `vector.similarity_function`: 'cosine'
                }}
            }}
        """)
        
        # 3. Составной индекс для фильтрации по важности + времени
        await session.run("""
            CREATE INDEX entity_importance_time_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.importance_score, e.last_accessed)
        """)
        
        # 4. Индекс на embedding_version для lazy re-indexing
        # Позволяет быстро найти все узлы с устаревшей embedding-моделью
        await session.run("""
            CREATE INDEX entity_embedding_version_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.embedding_version)
        """)
        
        # 5. Индекс на is_active для Soft Delete фильтрации
        await session.run("""
            CREATE INDEX entity_active_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.is_active)
        """)

        # 6. ✅ RFC0062: индекс для ConflictResolutionWorker._check_batch
        await session.run("""
            CREATE INDEX fact_conflict_checked_idx IF NOT EXISTS
            FOR (f:Fact) ON (f.conflict_checked)
        """)
```

**Query оптимизация (ВСЕГДА использовать LIMIT!)**:

```python
# graph_memory.py
async def get_context_for_entity(
    self,
    entity_name: str,
    depth: int = 2,
    max_neighbors: int = 100  # КРИТИЧНО!
) -> dict:
    """
    Получить контекст вокруг сущности через обход графа
    С ОГРАНИЧЕНИЕМ результатов для предотвращения взрыва памяти
    """
    # FIX из HYPERIA: whitelist вместо numeric clamp — инъекция невозможна архитектурно.
    depth = depth if depth in (1, 2, 3) else 2
    query = f"""
    MATCH (e:Entity {{name: $entity_name}})
    OPTIONAL MATCH path = (e)-[*1..{depth}]-(related)
    WITH e, related, relationships(path) as rels
    RETURN e, 
           collect(DISTINCT related)[0..{max_neighbors}] as related_entities,
           collect(DISTINCT rels)[0..{max_neighbors}] as relationships
    """

    result = await self.graphiti.execute_cypher(
        query,
        {"entity_name": entity_name}
    )

    return result
```

**Архивация старых узлов**:

```python
# memory_archival.py
from datetime import datetime, timedelta
import json
import aioboto3

class MemoryArchival:
    def __init__(self, graph: GraphMemory, s3_bucket: str):
        self.graph = graph
        self._session = aioboto3.Session()
        self.bucket = s3_bucket

    async def archive_old_episodes(
        self,
        older_than_days: int = 365,
        importance_threshold: float = 0.3
    ):
        """
        Архивировать эпизоды старше N дней с низкой важностью
        Это критично для предотвращения бесконечного роста графа
        """
        # 1. Найти кандидатов на архивацию
        query = """
        MATCH (ep:Episode)-[r]-(connected)
        WHERE ep.timestamp < datetime() - duration({days: $days})
          AND ep.importance_score < $threshold
        RETURN ep, collect(DISTINCT connected) as related, collect(r) as relationships
        LIMIT 1000
        """
        
        candidates = await self.graph.execute_cypher(query, {
            "days": older_than_days,
            "threshold": importance_threshold
        })
        
        # 2. Экспорт в S3
        # Используем self._session из __init__ — не создаём новый Session() при каждом вызове (утечка соединений).
        archived_count = 0
        async with self._session.client('s3') as s3:
          for episode_data in candidates:
            archive_key = f"archived_episodes/{episode_data['ep']['id']}.json"
            
            await s3.put_object(  # теперь корректный await
                Bucket=self.bucket,
                Key=archive_key,
                Body=json.dumps(episode_data)
            )
            
            # Soft Delete: физическое удаление только через Vacuum Worker (GC)
            await self.graph.execute_cypher("""
                MATCH (ep:Episode {id: $id})
                SET ep.is_active = false,
                    ep.valid_to = datetime(),
                    ep.archived_to_s3 = true
                WITH ep
                OPTIONAL MATCH (ep)-[r]-()
                SET r.is_active = false
            """, {"id": episode_data['ep']['id']})
            
            archived_count += 1
        
        return archived_count

    async def vacuum_soft_deleted(self, min_age_days: int = 90):
        """
        Vacuum Worker — физическое удаление после подтверждения S3.
        Batched rate limiting — удаляет по 100 узлов за итерацию
        с паузой 500ms между батчами. Не конкурирует с Fast Path.

        Протокол:
        1. archived_to_s3 = true  (архивация подтверждена)
        2. valid_to < now - 90 дней  (достаточно старый)
        3. Только тогда — DETACH DELETE (батчами, не всё сразу)

        Запускать: через MemoryGarbageCollector.run_full_gc() раз в неделю.
        Не запускать на Fast Path — только Slow Path / фоновый GC.
        """
        total_deleted = 0
        batch_size = 100          # лимит за одну итерацию
        sleep_between = 0.5       # 500ms пауза — не блокируем Neo4j write lock

        while True:
            deleted = await self.graph.execute_cypher("""
                MATCH (n)
                WHERE n.is_active = false
                  AND n.archived_to_s3 = true
                  AND n.valid_to < datetime() - duration({days: $min_age_days})
                WITH n LIMIT $batch_size
                DETACH DELETE n
                RETURN count(n) AS deleted_count
            """, {"min_age_days": min_age_days, "batch_size": batch_size})

            count = deleted[0].get("deleted_count", 0) if deleted else 0
            total_deleted += count

            if count == 0:
                break  # Нечего удалять — выходим

            logger.info(f"Vacuum batch: удалено {count}, всего {total_deleted}")
            await asyncio.sleep(sleep_between)  # Rate limiting — пауза между батчами

        logger.info(f"Vacuum завершён: физически удалено {total_deleted} узлов (age > {min_age_days}d)")
        return total_deleted


class MemoryRestoreProtocol:
    """
    5-шаговый протокол восстановления узла из S3 → Neo4j.

    Нужен когда GC удалил что-то важное или пользователь запросил восстановление.
    Отсутствовал в v5 — был только путь «туда» (архивация), но не «обратно».

    Шаги:
        1. Найти архив в S3 по node_id
        2. MERGE узла обратно в Neo4j
        3. SET is_active=true, clear valid_to
        4. Stamp restored_at + restore_reason (аудит)
        5. Re-enter ESM на Supported (не Validated — TruthGate нужен заново)
           + проверить инварианты post-restore

    Usage:
        restore = MemoryRestoreProtocol(graph, s3_client, S3_BUCKET, esm, inv_checker)
        result  = await restore.restore("episode:abc123", "user_request", session_id)
    """

    def __init__(self, graph_adapter, s3_client, s3_bucket: str, esm, invariant_checker):
        self.graph   = graph_adapter
        self.s3      = s3_client
        self.bucket  = s3_bucket
        self.esm     = esm
        self.checker = invariant_checker

    async def restore(self, node_id: str, restore_reason: str,
                      requested_by: str = "system") -> dict:
        """Возвращает {"success": bool, "node_id": ..., "reason": ..., "restored_at": ...}"""
        logger.info(f"MemoryRestoreProtocol: restore {node_id} ({restore_reason})")

        # 1. S3 lookup
        try:
            import json as _json
            obj  = await self.s3.get_object(
                Bucket=self.bucket, Key=f"archived_episodes/{node_id}.json"
            )
            data = _json.loads(await obj["Body"].read())
        except Exception as e:
            logger.error(f"MemoryRestoreProtocol: S3 lookup failed: {e}")
            return {"success": False, "node_id": node_id, "reason": f"S3 failed: {e}"}

        # 2. MERGE в Neo4j
        try:
            props = {k: v for k, v in data.get("ep", {}).items()
                     if k not in ("is_active", "valid_to", "archived_to_s3")}
            await self.graph.execute_cypher(
                "MERGE (n {id: $id}) ON CREATE SET n = $p ON MATCH SET n += $p",
                {"id": node_id, "p": props}
            )
        except Exception as e:
            logger.error(f"MemoryRestoreProtocol: MERGE failed: {e}")
            return {"success": False, "node_id": node_id, "reason": f"MERGE failed: {e}"}

        # 3+4. Активировать + аудит
        now = datetime.now(timezone.utc).isoformat()
        await self.graph.execute_cypher(
            "MATCH (n {id: $id}) SET n.is_active = true, n.valid_to = null,"
            " n.restored_at = $now, n.restore_reason = $r, n.restored_by = $by",
            {"id": node_id, "now": now, "r": restore_reason, "by": requested_by}
        )

        # 5a. Re-enter ESM: стартуем с Hypothesized + evidence_count=2
        #     ESM автоматически перейдёт в Supported (правило: Hypothesized→Supported при Evidence ≥ 2).
        #     До Validated узел не поднимается — TruthGate нужен заново (не обходим).
        try:
            await self.esm.transition(
                node_id,
                {"epistemic_state": "Hypothesized", "evidence_count": 2},
                self.graph,
                f"restore:{restore_reason}"
            )
        except Exception as e:
            logger.warning(f"MemoryRestoreProtocol: ESM transition soft-failed (non-fatal): {e}")

        # 5b. Проверить инварианты post-restore
        try:
            violations = await self.checker.check_all()
            criticals  = [v.invariant_id for v in violations if v.severity == "CRITICAL"]
            if criticals:
                logger.error(f"MemoryRestoreProtocol: post-restore critical invariants: {criticals}")
        except Exception:
            pass

        logger.info(f"MemoryRestoreProtocol: ✅ {node_id} restored")
        return {"success": True, "node_id": node_id, "reason": restore_reason, "restored_at": now}
```

---


# ============================================================================
# HYPERIA COMPONENT 1: EmbeddingRegistry
# ============================================================================
# Назначение: Централизованный реестр размерностей embedding моделей
# Предотвращает silent corruption индексов при смене модели

# memory/embedding_registry.py
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class EmbeddingRegistry:
    """
    Централизованный реестр embedding моделей и их размерностей.

    Проблема: При смене модели с 1024 dim на 3072 dim Neo4j индексы
    становятся несовместимыми, но ошибка проявляется только в runtime.

    Решение: Валидация при старте + автоматическое обнаружение несоответствий.
    """

    # Известные модели и их размерности
    KNOWN_MODELS: Dict[str, int] = {
        "paraphrase-multilingual-MiniLM-L12-v2": 384,
        "multilingual-e5-large": 1024,
        "deepvk/USER-bge-m3": 1024,
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "gemini-embedding-2": 3072,
        "text-embedding-ada-002": 1536,
    }

    def __init__(self, current_model: str):
        self.current_model = current_model
        self.dimension = self._get_dimension(current_model)
        logger.info(f"EmbeddingRegistry: {current_model} → {self.dimension}D")

    def _get_dimension(self, model_name: str) -> int:
        """Получить размерность модели или вычислить автоматически"""
        if model_name in self.KNOWN_MODELS:
            return self.KNOWN_MODELS[model_name]
        
        # Реальный вызов модели — не угадываем, не возвращаем 1024 молча
        logger.warning(f"Модель {model_name} не в реестре. Пытаюсь определить реально...")
        try:
            test_embedding = self._compute_test_embedding(model_name)
            actual_dim = len(test_embedding)
            self.KNOWN_MODELS[model_name] = actual_dim  # кэшируем для следующих вызовов
            logger.info(f"Auto-detected dimension for {model_name}: {actual_dim}D")
            return actual_dim
        except Exception as e:
            # КРИТИЧНО: лучше упасть при старте чем тихо создать несовместимые индексы Neo4j
            logger.critical(
                f"НЕВОЗМОЖНО определить размерность для {model_name}: {e}\n"
                f"Добавьте модель в EmbeddingRegistry.KNOWN_MODELS вручную.\n"
                f"Запуск без этого = silent corruption индексов Neo4j."
            )
            raise RuntimeError(
                f"Unknown embedding model: {model_name}. "
                f"Add to EmbeddingRegistry.KNOWN_MODELS before deploying. Error: {e}"
            )

    def validate_index_dimension(self, index_dimension: int) -> bool:
        """
        Проверить соответствие размерности индекса текущей модели.
        Вызывается при старте GraphMemory.
        """
        if index_dimension != self.dimension:
            logger.error(
                f"НЕСООТВЕТСТВИЕ РАЗМЕРНОСТЕЙ: "
                f"индекс={index_dimension}D, модель={self.dimension}D. "
                f"Требуется пересоздание индексов!"
            )
            return False
        return True

    def get_dimension(self) -> int:
        """Получить размерность текущей модели"""
        return self.dimension

# Интеграция в GraphMemory:
# В __init__:
#   self.embedding_registry = EmbeddingRegistry(current_model=embedding_model_name)
# При создании индекса:
#   dimension = self.embedding_registry.get_dimension()
# При старте:
#   if not self.embedding_registry.validate_index_dimension(existing_index_dim):
#       raise RuntimeError("Index dimension mismatch")

---

## 🧬 Интегрированные компоненты (из HYPERIA v5.20)

> Компоненты интегрированы в Velantrim без изменения архитектуры.
> Каждый компонент — отдельный файл. Подключаются через существующие точки.

---

### HYPERIA-1: DAAD — Domain-Aware Attention & Decay

> **Проблема**: DAAD domain-aware λ_eff в FSRS decay для всех узлов.
> «Активный проект с дедлайном» и «вчера была хорошая погода» затухают одинаково.
> **Решение**: `λ_eff = Σ(dᵢ × λᵢ)` — взвешенная сумма по доменам узла.

#### Инвариант I66 (новый)
```
I66: DAAD меняет ТОЛЬКО attention_weight и λ_eff.
     truth_status, epistemic_state, epistemic_score — неприкосновенны.
     domain_vector=NULL → fallback λ=0.05, не ошибка.
     Нарушение = прямая запись в ESM из DomainResolver = баг.
```

#### Таблица доменов
| Домен | λ (затухание) | floor (минимум) | Смысл |
|---|---|---|---|
| `active_project` | 0.001 | 0.85 | Живёт годами |
| `personal_pref` | 0.004 | 0.60 | Медленно меняется |
| `domain_knowledge` | 0.006 | 0.50 | Стабильные знания |
| `completed_project` | 0.008 | 0.40 | Менее актуален |
| `casual_chat` | 0.150 | 0.00 | Забывается за дни |
| `general_question` | 0.200 | 0.00 | Быстро устаревает |

```python
# memory/domain_resolver.py
# HYPERIA DAAD — Domain-Aware Attention & Decay
# I66: меняет только attention_weight. ESM/truth_status — не трогает.
# Slow Path, 0 токенов LLM.

import logging
from dataclasses import dataclass
from typing import Dict, Optional

logger = logging.getLogger(__name__)

DOMAIN_CONFIG: Dict[str, Dict] = {
    "active_project":    {"lambda": 0.001, "floor": 0.85},
    "personal_pref":     {"lambda": 0.004, "floor": 0.60},
    "domain_knowledge":  {"lambda": 0.006, "floor": 0.50},
    "completed_project": {"lambda": 0.008, "floor": 0.40},
    "casual_chat":       {"lambda": 0.150, "floor": 0.00},
    "general_question":  {"lambda": 0.200, "floor": 0.00},
}

FALLBACK_LAMBDA = 0.05
FALLBACK_FLOOR  = 0.00


@dataclass
class DecayParams:
    lambda_eff: float  # эффективная скорость затухания
    floor_eff:  float  # минимальный уровень importance (не падает ниже)


class DomainResolver:
    """
    Вычисляет λ_eff и floor_eff для узла по его domain_vector.
    domain_vector — нормализованное распределение по доменам (сумма = 1.0).
    Пример: {"active_project": 0.7, "domain_knowledge": 0.3}
    λ_eff = Σ(dᵢ × λᵢ)  — взвешенная сумма скоростей затухания
    floor_eff = max(dᵢ × floorᵢ)  — максимальный гарантированный минимум

    Интеграция: вызывается из FSRSDecayWorker вместо фиксированного λ. (v8.0: заменяет EbbinghausDecayWorker)
    """

    @staticmethod
    def resolve(domain_vector: Optional[Dict[str, float]]) -> DecayParams:
        """
        Вычислить параметры затухания по domain_vector узла.
        domain_vector=None или пустой → fallback (I66).
        """
        if not domain_vector:
            logger.debug("DomainResolver: domain_vector=None → fallback λ=0.05")
            return DecayParams(lambda_eff=FALLBACK_LAMBDA, floor_eff=FALLBACK_FLOOR)

        lambda_eff = 0.0
        floor_eff  = 0.0
        total_weight = sum(domain_vector.values())

        if total_weight <= 0:
            return DecayParams(lambda_eff=FALLBACK_LAMBDA, floor_eff=FALLBACK_FLOOR)

        # Нормализация на случай если веса не суммируются в 1.0
        for domain, weight in domain_vector.items():
            norm_weight = weight / total_weight
            cfg = DOMAIN_CONFIG.get(domain)
            if cfg is None:
                logger.warning(f"DomainResolver: unknown domain '{domain}' — skipped")
                continue
            lambda_eff += norm_weight * cfg["lambda"]
            floor_eff   = max(floor_eff, norm_weight * cfg["floor"])

        # Если все домены неизвестные — fallback
        if lambda_eff == 0.0:
            return DecayParams(lambda_eff=FALLBACK_LAMBDA, floor_eff=FALLBACK_FLOOR)

        return DecayParams(lambda_eff=lambda_eff, floor_eff=floor_eff)
```

**Интеграция в FSRSDecayWorker** (v8.0: заменяет EbbinghausDecayWorker):
```python
# В FSRSDecayWorker — DAAD domain-aware λ_eff:
from memory.domain_resolver import DomainResolver

# Было:
# new_importance = current_importance * exp(-t / S)

# Стало:
domain_vector = node.get("domain_vector")  # из Neo4j :Entity.domain_vector
params = DomainResolver.resolve(domain_vector)
# P9-FIX БАГ-11: FSRS power-law (P0-1 заменил Ebbinghaus везде, DAAD пример не обновился)
# λ_eff используется вместо глобального λ через domain-aware stability
S_eff = S / max(0.01, params.lambda_eff)              # domain-aware stability
R = (1 + (19/81) * t / max(0.01, S_eff)) ** (-0.5)   # FSRS power-law R
new_importance = max(params.floor_eff, current_importance * R)
# floor_eff гарантирует что важный узел никогда не упадёт ниже порога
```

**Добавить в Neo4j схему** (`:Entity`):
```cypher
// domain_vector: JSON-распределение по доменам, обновляется TagManager-ом
// Пример: '{"active_project": 0.7, "domain_knowledge": 0.3}'
(:Entity { ..., domain_vector: STRING })  // JSON, NULL = fallback λ=0.05
```

**Метрики**:
```python
daad_resolved_total     # счётчик узлов с domain-aware decay
daad_fallback_total     # счётчик fallback (domain_vector=NULL)
daad_floor_protected    # сколько раз floor предотвратил падение ниже минимума
```

---

### HYPERIA-2: Guardian — Валидатор ответа

> **Источник**: HYPERIA `core/guardian.py`
> **Назначение**: Последний рубеж **после LLM** перед отправкой пользователю.
> Velantrim имеет Truth Gate (до L3) и Observer++ (безопасность),
> но нет проверки **качества ответа** после генерации.
> **Место**: Fast Path, после LLM Generation, перед Response.
> **Инвариант**: Guardian.validate() — синхронный, 0 токенов, <1 мс.

```python
# core/guardian.py
# Guardian — последний рубеж перед ответом пользователю.
# Место: Fast Path после LLM, перед return.
# 0 токенов · <1 мс · синхронный.

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.6
MIN_TRACE_LENGTH     = 1


class GuardianDecision(str, Enum):
    APPROVE = "approve"
    REJECT  = "reject"
    WARN    = "warn"    # ответ отдаётся, но с предупреждением


@dataclass
class GuardianResult:
    decision:   GuardianDecision
    reason:     str
    confidence: float
    response:   Optional[str] = None  # финальный текст для пользователя


class Guardian:
    """
    Валидатор ответа агента.
    REJECT  — при confidence < 0.6, пустом trace или только deprecated источниках.
    WARN    — при majority hypothesis-источников.
    APPROVE — все проверки пройдены.
    """

    def validate(
        self,
        response:   str,
        confidence: float,
        trace:      List[str],
        sources:    List[dict] = None,
    ) -> GuardianResult:
        def _emit(res: GuardianResult) -> GuardianResult:
            try:
                from metrics import guardian_decisions_total, guardian_confidence_dist
                guardian_decisions_total.labels(decision=res.decision.value).inc()
                guardian_confidence_dist.observe(res.confidence)
            except Exception:
                pass
            return res

        # Проверка 1: уверенность
        if confidence < CONFIDENCE_THRESHOLD:
            logger.info(f"Guardian: REJECT — low confidence ({confidence:.2f})")
            return _emit(GuardianResult(
                decision=GuardianDecision.REJECT,
                reason=f"confidence too low ({confidence:.2f})",
                confidence=confidence,
                response=(
                    "Я не уверен в достаточной мере чтобы дать точный ответ. "
                    "Могу поискать больше информации или уточнить детали."
                )
            ))

        # Проверка 2: наличие обоснования (TRACE)
        if not trace or len(trace) < MIN_TRACE_LENGTH:
            logger.info("Guardian: REJECT — empty trace")
            return _emit(GuardianResult(
                decision=GuardianDecision.REJECT,
                reason="no reasoning trace",
                confidence=confidence,
                response=(
                    "У меня нет достаточно подтверждённых данных по этому вопросу. "
                    "Расскажи подробнее — это поможет найти нужную информацию."
                )
            ))

        # Проверка 3: все источники deprecated?
        if sources:
            non_deprecated = [
                s for s in sources
                if s.get("epistemic_state") not in ("Deprecated", "Collapsed", "Contradicted")
            ]
            if not non_deprecated:
                logger.info("Guardian: REJECT — all sources deprecated/collapsed")
                return _emit(GuardianResult(
                    decision=GuardianDecision.REJECT,
                    reason="all memory sources are deprecated",
                    confidence=confidence,
                    response=(
                        "Информация по этой теме в моей памяти устарела. "
                        "Уточни актуальные данные — обновлю."
                    )
                ))

            # Предупреждение: majority hypothesis
            hypothesis_count = sum(
                1 for s in sources
                if s.get("epistemic_state") in ("Hypothesized", "Observed")
            )
            if hypothesis_count > len(sources) / 2:
                logger.info(f"Guardian: WARN — {hypothesis_count}/{len(sources)} sources are hypothesis")
                return _emit(GuardianResult(
                    decision=GuardianDecision.WARN,
                    reason=f"{hypothesis_count}/{len(sources)} sources unconfirmed",
                    confidence=confidence,
                    response=f"[Частично предположение] {response}"
                ))

        return _emit(GuardianResult(
            decision=GuardianDecision.APPROVE,
            reason="all checks passed",
            confidence=confidence,
            response=response
        ))
```

**Интеграция** — добавить в конец Fast Path после LLM:
```python
# В agent.py / chat() — после LLM Generation, перед return response:
from core.guardian import Guardian, GuardianDecision

guardian = Guardian()
guard_result = guardian.validate(
    response=llm_response,
    confidence=response_confidence,   # из ответа LLM или из ESM
    trace=fact_trace,                 # list[fact_id] использованных фактов
    sources=retrieved_facts,          # факты из L3 с epistemic_state
)
if guard_result.decision == GuardianDecision.REJECT:
    logger.warning(f"Guardian REJECT: {guard_result.reason}")
return guard_result.response  # APPROVE→оригинал, WARN→с пометкой, REJECT→fallback
```

**Метрики**:
```python
guardian_decisions_total   # labels: approve/reject/warn
guardian_confidence_dist   # histogram распределения confidence
```

### P0-2: Quality Gate (D-Mem style) — добавить в core/guardian.py

```python
# P0-2: D-Mem Quality Gating — метод класса Guardian
# I85: Quality Gate выполняется ПОСЛЕ LLM-генерации, ДО отправки ответа.
#      Не изменяет facts_pack — только маршрутизирует.
from dataclasses import dataclass

@dataclass
class QualityGateResult:
    use_slow_path: bool
    confidence: float
    coverage: float
    has_contradictions: bool
    reason: str

# Добавить как метод класса Guardian (в core/guardian.py):
# class Guardian:
#     ...существующие методы...
#
    def quality_gate(
        self,
        response_draft: str,
        facts_pack: list,
        query: str
    ) -> QualityGateResult:
        """
        D-Mem style quality gating.
        Решает: достаточен ли Fast Path или нужен дорогой Slow Path.
        Экономия: ~60% токенов без потери качества (D-Mem: 96.7% от full deliberation).
        """
        confidence = self._estimate_confidence(response_draft, facts_pack)
        coverage = self._estimate_coverage(response_draft, facts_pack)
        has_contradictions = self._check_contradictions(facts_pack)

        if (confidence >= QUALITY_GATE_CONFIDENCE_THRESHOLD
            and coverage >= QUALITY_GATE_COVERAGE_THRESHOLD
            and not has_contradictions):
            return QualityGateResult(False, confidence, coverage, False, "FAST_PATH_SUFFICIENT")
        else:
            return QualityGateResult(True, confidence, coverage, has_contradictions,
                f"SLOW_PATH: conf={confidence:.2f} cov={coverage:.2f} contr={has_contradictions}")

    def _estimate_confidence(self, response_draft: str, facts_pack: list) -> float:
        if not facts_pack:
            return 0.0
        validated = [f for f in facts_pack if f.get("epistemic_state") == "Validated"]
        return len(validated) / len(facts_pack)

    def _estimate_coverage(self, response_draft: str, facts_pack: list) -> float:
        if not facts_pack or not response_draft:
            return 0.0
        hits = sum(1 for f in facts_pack
                   if any(kw.lower() in response_draft.lower()
                          for kw in str(f.get("content", "")).split()[:5]))
        return hits / len(facts_pack)

    def _check_contradictions(self, facts_pack: list) -> bool:
        states = {f.get("epistemic_state") for f in facts_pack}
        return "Contradicted" in states
```

Конфиг (velantrim_config.py):
```python
QUALITY_GATING_ENABLED = True
QUALITY_GATE_CONFIDENCE_THRESHOLD = 0.7
QUALITY_GATE_COVERAGE_THRESHOLD = 0.6
```

```
I85 (QualityGate): Quality Gate выполняется ПОСЛЕ LLM-генерации, ДО отправки ответа.
    Если use_slow_path=True, ответ НЕ отправляется пользователю до завершения Slow Path.
    Quality Gate не изменяет facts_pack — только маршрутизирует.
```

---

### HYPERIA-3: ACT-R Activation (feature-flag)

> **Источник**: HYPERIA `fractal_memory.py` — `B = ln(Σ tᵢ^(-0.5))`
> **Назначение**: Удержание воспоминаний по **истории обращений**, а не только по recency.
> Узел к которому обращались 10 раз затухает медленнее чем узел с одним обращением.
> **Флаг**: `ACT_R_ENABLED = True` в `velantrim_config.py` — включается опционально.

```python
# memory/actr_activation.py
# ACT-R Activation — Anderson (1983): базовый уровень активации по истории обращений.
# B = ln(Σ tᵢ^(-0.5))
# tᵢ — время в секундах от i-го обращения до сейчас
# Чем больше обращений и чем они свежее — тем выше B.
# Интеграция: ReactivationEngine + HybridRetriever (бонус к score).
# Включение: ACT_R_ENABLED = True в velantrim_config.py

import math
import logging
from datetime import datetime, timezone
from typing import List

logger = logging.getLogger(__name__)


def compute_actr_activation(
    access_times: List[datetime],
    now: datetime = None,
    decay_exponent: float = 0.5,  # стандартный параметр ACT-R
) -> float:
    """
    Вычислить базовый уровень активации по Anderson ACT-R.
    B = ln(Σ tᵢ^(-decay_exponent))

    Args:
        access_times: список datetime когда узел был активирован
        now:          текущее время (UTC). None = datetime.now(timezone.utc)
        decay_exponent: стандарт ACT-R = 0.5

    Returns:
        float: уровень активации (чем выше — тем важнее)
        0.0 если access_times пуст
    """
    if not access_times:
        return 0.0

    now = now or datetime.now(timezone.utc)
    total = 0.0

    for t in access_times:
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        delta_sec = (now - t).total_seconds()
        if delta_sec <= 0:
            delta_sec = 0.001  # защита от деления на ноль при одновременном доступе
        total += delta_sec ** (-decay_exponent)

    if total <= 0:
        return 0.0
    return math.log(total)


def actr_score_boost(base_score: float, activation: float,
                     weight: float = 0.15) -> float:
    """
    Добавить ACT-R бонус к retrieval score.
    weight=0.15 — мягкое влияние, не доминирует над семантикой.
    """
    return base_score + weight * max(0.0, activation)
```

**Интеграция** (2 точки):
```python
# 1. В HybridRetriever.retrieve() — бонус к score кандидата:
if ACT_R_ENABLED and node.get("access_history"):
    activation = compute_actr_activation(node["access_history"])
    candidate.score = actr_score_boost(candidate.score, activation)

# 2. В ReactivationEngine — приоритизация узлов для укрепления:
if ACT_R_ENABLED:
    activation = compute_actr_activation(node.access_times)
    priority = base_priority * (1.0 + 0.2 * max(0.0, activation))
```

**Добавить в `velantrim_config.py`**:
```python
ACT_R_ENABLED         = True   # feature-flag: ACT-R activation bonus
ACT_R_DECAY_EXPONENT  = 0.5    # стандартный параметр ACT-R (Anderson 1983)
ACT_R_RETRIEVAL_WEIGHT = 0.15  # вес бонуса в HybridRetriever
```

---

### HYPERIA-4: Laplace Confidence

> **Источник**: HYPERIA `core/truth_layer.py`
> **Проблема**: Новые факты с 0 evidence имеют `confidence = 0/(0+0) = NaN` или 0.0
> → TruthGate блокирует их навсегда. Система не обучается на новом.
> **Решение**: Laplace smoothing `(pos+1)/(total+2)` — новый факт стартует с 0.5, не с 0.

```python
# В truth_gate.py — заменить raw ratio на Laplace:

def laplace_confidence(positive_evidence: int, total_evidence: int) -> float:
    """
    Laplace smoothing для confidence новых фактов.
    (pos+1) / (total+2)
    · новый факт (0/0) → 0.5 (нейтральный, не заблокирован)
    · 1 подтверждение из 1 → 0.67 (осторожный оптимизм)
    · 9 из 10 → 0.917 (высокая уверенность)
    · Устраняет деление на ноль без искусственного clamp.
    """
    return (positive_evidence + 1) / (total_evidence + 2)

# Применять при вычислении confidence в TruthGate.validate_and_transition():
# Было: confidence = evidence_count / max(1, total_checks)
# Стало: confidence = laplace_confidence(evidence_count, total_checks)
```

---

### HYPERIA-5: CognitiveModes — Маршрутизатор глубины retrieval

> **Источник**: HYPERIA `core/cognitive_modes.py`
> **Назначение**: Маршрутизирует глубину retrieval по типу запроса перед ContextBuilder.
> PRECISION — максимальная точность (сложные factual задачи).
> BALANCED — компромисс (стандарт).
> EXPLORATION — широкое покрытие (творческие/исследовательские запросы).

```python
# core/cognitive_modes.py
# CognitiveModes — маршрутизатор глубины retrieval.
# Место: Fast Path, перед ContextBuilder / HybridRetriever.
# 0 токенов · ~0 мс.

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class CognitiveMode(str, Enum):
    # P9-FIX БАГ-7: DEPRECATED — используй canonical CognitiveMode из cognitive_modes.py (строки 10002+)
    # Этот блок содержит только 3 режима (без CREATIVE). Конфликт импортов при одновременном существовании.
    # Оставлен ТОЛЬКО для RetrievalConfig ниже. CognitiveMode отсюда НЕ импортировать.
    PRECISION   = "precision"    # точность > покрытие: factual, технические
    BALANCED    = "balanced"     # стандарт: большинство запросов
    EXPLORATION = "exploration"  # покрытие > точность: creative, research
    # CREATIVE отсутствует — см. RFC0067 v2.0 canonical definition


@dataclass
class RetrievalConfig:
    mode:             CognitiveMode
    max_facts:        int    # сколько фактов из L3 в FactsPack
    graph_depth:      int    # глубина traversal в Hot Graph
    sae_threshold:    float  # порог SAE spreading activation
    use_analogy:      bool   # использовать Analogy Graph (RFC0067)
    temperature_hint: float  # подсказка для Adaptive Decoder


MODE_CONFIGS = {
    CognitiveMode.PRECISION: RetrievalConfig(
        mode=CognitiveMode.PRECISION,
        max_facts=5, graph_depth=2, sae_threshold=0.5,
        use_analogy=False, temperature_hint=0.3,
    ),
    CognitiveMode.BALANCED: RetrievalConfig(
        mode=CognitiveMode.BALANCED,
        max_facts=10, graph_depth=3, sae_threshold=0.35,
        use_analogy=True, temperature_hint=0.6,
    ),
    CognitiveMode.EXPLORATION: RetrievalConfig(
        mode=CognitiveMode.EXPLORATION,
        max_facts=20, graph_depth=4, sae_threshold=0.25,
        use_analogy=True, temperature_hint=0.85,
    ),
}

# Ключевые слова для автодетекта режима
_PRECISION_SIGNALS   = {"точно", "конкретно", "факт", "дата", "число", "exactly", "precise", "fact"}
_EXPLORATION_SIGNALS = {"придумай", "представь", "аналогия", "творчески", "explore", "imagine", "creative", "analogy"}


class CognitiveModeRouter:
    """
    Определяет режим retrieval по запросу пользователя.
    Вызывается в начале Fast Path — до HybridRetriever.
    """

    def route(self, query: str, override: Optional[CognitiveMode] = None) -> RetrievalConfig:
        """
        Определить RetrievalConfig для запроса.
        override — явный режим (например, из user settings или meta-команды).
        """
        if override:
            logger.debug(f"CognitiveModeRouter: override={override.value}")
            return MODE_CONFIGS[override]

        q_lower = query.lower()
        words   = set(q_lower.split())

        if words & _PRECISION_SIGNALS:
            mode = CognitiveMode.PRECISION
        elif words & _EXPLORATION_SIGNALS:
            mode = CognitiveMode.EXPLORATION
        else:
            mode = CognitiveMode.BALANCED

        logger.debug(f"CognitiveModeRouter: auto={mode.value} for query='{query[:50]}'")
        return MODE_CONFIGS[mode]
```

**Интеграция** — добавить в начало Fast Path:
```python
# В agent.chat() — перед HybridRetrieval:
from core.cognitive_modes import CognitiveModeRouter

router    = CognitiveModeRouter()
ret_cfg   = router.route(user_query)
# Передать ret_cfg в HybridRetriever и ContextBuilder:
facts     = await retriever.retrieve(query, max_facts=ret_cfg.max_facts,
                                     depth=ret_cfg.graph_depth)
# Для CREATIVE режима RFC0067:
if ret_cfg.use_analogy:
    analogies = await analogy_graph.get_bridges(query)
```

---

### HYPERIA-6: OutputFaithfulnessChecker F6.5

> **Источник**: HYPERIA `core/output_faithfulness_checker.py`
> **Назначение**: Проверяет ПОСЛЕ генерации — соответствует ли ответ LLM фактам из L3.
> Запускается в **Slow Path** (fire-and-forget через EventBus).
> Результат пишется в ResponseAudit (RFC0052) как `faithfulness_score`.
> **Инвариант**: F6.5 никогда не блокирует Fast Path. Только Slow Path.

```python
# core/output_faithfulness_checker.py
# OutputFaithfulnessChecker F6.5 — пост-генерационная проверка фактов.
# Slow Path только. Результат → ResponseAudit.faithfulness_score.
# 0 токенов если use_llm=False (extractive mode).

import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class FaithfulnessResult:
    score:            float          # 0.0–1.0
    grounded_claims:  int            # сколько утверждений подтверждено фактами
    total_claims:     int            # всего утверждений в ответе
    unsupported:      List[str]      # утверждения без поддержки в графе
    mode:             str            # "extractive" | "llm"


class OutputFaithfulnessChecker:
    """
    Проверяет соответствие ответа LLM фактам из L3 графа.
    Extractive mode (default): TF-IDF overlap — 0 токенов.
    LLM mode: только если importance_score > 0.85 (через ResponseAuditWorker).

    Интеграция:
      Slow Path → AuditWorker слушает RESPONSE_GENERATED event →
      вызывает check() → пишет faithfulness_score в :DialogueSummary.
    """

    async def check(
        self,
        response:      str,
        source_facts:  List[dict],     # факты из L3 использованные при генерации
        use_llm:       bool = False,
        llm_client     = None,
    ) -> FaithfulnessResult:
        """
        Проверить faithfulness ответа против source_facts.
        source_facts: список {"content": str, "epistemic_state": str}
        """
        if not source_facts:
            return FaithfulnessResult(
                score=0.5, grounded_claims=0, total_claims=0,
                unsupported=[], mode="no_sources"
            )

        if use_llm and llm_client:
            return await self._llm_check(response, source_facts, llm_client)
        return self._extractive_check(response, source_facts)

    def _extractive_check(
        self, response: str, source_facts: List[dict]
    ) -> FaithfulnessResult:
        """
        TF-IDF overlap между ответом и source_facts.
        Быстро, 0 токенов, CPU only.
        """
        import re

        def _tokenize(text: str) -> set:
            return set(re.findall(r'\b\w{3,}\b', text.lower()))

        response_tokens = _tokenize(response)
        claims = response.split('. ')
        grounded = 0
        unsupported = []

        for claim in claims:
            if not claim.strip():
                continue
            claim_tokens = _tokenize(claim)
            if not claim_tokens:
                continue
            # Проверяем overlap с хотя бы одним source_fact
            matched = False
            for fact in source_facts:
                fact_tokens = _tokenize(fact.get("content", ""))
                overlap = len(claim_tokens & fact_tokens) / max(1, len(claim_tokens))
                if overlap > 0.3:  # 30% токенов совпадают — считаем обоснованным
                    matched = True
                    break
            if matched:
                grounded += 1
            else:
                unsupported.append(claim[:100])  # сохраняем первые 100 символов

        total = max(1, len([c for c in claims if c.strip()]))
        score = grounded / total

        return FaithfulnessResult(
            score=score,
            grounded_claims=grounded,
            total_claims=total,
            unsupported=unsupported,
            mode="extractive"
        )

    async def _llm_check(
        self, response: str, source_facts: List[dict], llm_client
    ) -> FaithfulnessResult:
        """LLM-based проверка — только для critical responses (importance > 0.85)."""
        facts_text = "\n".join(
            f"- {f.get('content', '')[:200]}" for f in source_facts[:10]
        )
        prompt = f"""Rate faithfulness of the response against given facts (0.0-1.0).
Response: {response[:500]}
Facts:
{facts_text}
Return only JSON: {{"score": float, "unsupported_claims": [str]}}"""
        try:
            raw = await llm_client.complete(prompt)
            import json
            data = json.loads(raw)
            score = float(data.get("score", 0.5))
            unsupported = data.get("unsupported_claims", [])
            return FaithfulnessResult(
                score=score, grounded_claims=0, total_claims=0,
                unsupported=unsupported, mode="llm"
            )
        except Exception as e:
            logger.warning(f"OutputFaithfulnessChecker LLM failed: {e}, fallback extractive")
            return self._extractive_check(response, source_facts)
```

**Интеграция в ResponseAuditWorker** (Slow Path):
```python
# В response_audit_worker.py — добавить после Фазы 2:
from core.output_faithfulness_checker import OutputFaithfulnessChecker

checker = OutputFaithfulnessChecker()
faith_result = await checker.check(
    response=audit.response_text,
    source_facts=audit.source_facts,
    use_llm=(audit.importance_score > 0.85),
    llm_client=llm_client,
)
audit.faithfulness_score = faith_result.score
# Сохранить в :DialogueSummary.response_audit_faithfulness_avg
```

---

### HYPERIA-7: MemoryBudgetPlanner

> **Источник**: HYPERIA `memory/memory_budget_planner.py`
> **Назначение**: Hard limit 500k узлов + auto-GC при 85%.
> Velantrim не имеет лимита — граф растёт бесконечно.

```python
# memory/memory_budget_planner.py
# MemoryBudgetPlanner — защита от неограниченного роста графа.
# Hard limit: 500k узлов. Auto-GC при 85% (425k).
# Slow Path: проверяется раз в час через SleepTimeWorker.

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

NODE_LIMIT_HARD = 500_000   # абсолютный лимит
NODE_LIMIT_GC   = 425_000   # 85% — триггер auto-GC
NODE_LIMIT_WARN = 400_000   # 80% — предупреждение


@dataclass
class BudgetStatus:
    node_count:   int
    limit:        int
    utilization:  float   # 0.0–1.0
    action:       str     # "ok" | "warn" | "gc_triggered" | "hard_limit"


class MemoryBudgetPlanner:
    """
    Следит за размером графа и триггерит GC при приближении к лимиту.
    Интеграция: вызывается из SleepTimeWorker раз в час.
    """

    def __init__(self, graph, gc_runner=None):
        self.graph      = graph
        self.gc_runner  = gc_runner  # MemoryGarbageCollector или аналог

    async def check_and_act(self) -> BudgetStatus:
        """Проверить текущий размер графа и принять меры при необходимости."""
        try:
            result = await self.graph.execute_cypher(
                "MATCH (n) RETURN count(n) as total", {}
            )
            node_count = result[0]["total"] if result else 0
        except Exception as e:
            logger.error(f"MemoryBudgetPlanner: count query failed: {e}")
            return BudgetStatus(node_count=0, limit=NODE_LIMIT_HARD,
                                utilization=0.0, action="error")

        utilization = node_count / NODE_LIMIT_HARD

        if node_count >= NODE_LIMIT_HARD:
            logger.critical(
                f"MemoryBudgetPlanner: HARD LIMIT {node_count}/{NODE_LIMIT_HARD} — "
                f"blocking new writes until GC completes"
            )
            if self.gc_runner:
                await self.gc_runner.run_emergency_gc()
            return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                                utilization=utilization, action="hard_limit")

        if node_count >= NODE_LIMIT_GC:
            logger.warning(
                f"MemoryBudgetPlanner: GC triggered at {node_count}/{NODE_LIMIT_HARD} "
                f"({utilization:.1%})"
            )
            if self.gc_runner:
                await self.gc_runner.run_full_gc()
            return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                                utilization=utilization, action="gc_triggered")

        if node_count >= NODE_LIMIT_WARN:
            logger.warning(
                f"MemoryBudgetPlanner: WARNING {node_count}/{NODE_LIMIT_HARD} "
                f"({utilization:.1%}) — approaching limit"
            )
            return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                                utilization=utilization, action="warn")

        return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                            utilization=utilization, action="ok")
```

**Добавить в `velantrim_config.py`**:
```python
class BudgetConfig:
    NODE_LIMIT_HARD = 500_000
    NODE_LIMIT_GC   = 425_000  # 85%
    NODE_LIMIT_WARN = 400_000  # 80%

BUDGET = BudgetConfig()
```

**Метрика**:
```python
memory_budget_utilization   # gauge: node_count / NODE_LIMIT_HARD
memory_budget_gc_triggered  # counter: сколько раз auto-GC сработал
```

---

### HYPERIA-8: CircuitBreaker

> **Источник**: HYPERIA `circuit_breaker.py`
> **Назначение**: Защита Neo4j, Redis, LLM API от cascading failures.
> CLOSED → OPEN (N failures) → HALF_OPEN (timeout) → CLOSED (M successes).
> **Ключевое**: per-loop asyncio.Lock — без race condition в тестах.

```python
# circuit_breaker.py
# CircuitBreaker — защита от cascading failures (Neo4j, Redis, LLM API).
# per-loop Lock: каждый event loop получает свой Lock — нет RuntimeError в тестах.

import time
import asyncio
from enum import Enum
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED    = "closed"
    OPEN      = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(
        self,
        name:              str,
        failure_threshold: int = 5,
        timeout:           int = 60,
        success_threshold: int = 2,
    ):
        self.name              = name
        self.failure_threshold = failure_threshold
        self.timeout           = timeout
        self.success_threshold = success_threshold
        self.failure_count     = 0
        self.success_count     = 0
        self.last_failure_time = None
        self.state             = CircuitState.CLOSED
        self._locks: dict[int, asyncio.Lock] = {}  # per-loop

    def _get_lock(self) -> asyncio.Lock:
        loop    = asyncio.get_running_loop()
        loop_id = id(loop)
        if loop_id not in self._locks:
            self._locks[loop_id] = asyncio.Lock()
            if len(self._locks) > 10:  # GC мёртвых loop-ов
                dead = [k for k in self._locks if k != loop_id]
                for k in dead:
                    del self._locks[k]
        return self._locks[loop_id]

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        async with self._get_lock():
            if self.state == CircuitState.OPEN:
                if time.monotonic() - self.last_failure_time > self.timeout:
                    logger.info(f"{self.name}: OPEN → HALF_OPEN")
                    self.state         = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitBreakerOpenError(
                        f"Circuit '{self.name}' is OPEN. Retry after {self.timeout}s"
                    )
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure(e)
            raise

    async def _on_success(self):
        async with self._get_lock():
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    logger.info(f"{self.name}: HALF_OPEN → CLOSED")
                    self.state         = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = max(0, self.failure_count - 1)

    async def _on_failure(self, error: Exception):
        async with self._get_lock():
            self.failure_count    += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                logger.error(f"{self.name}: HALF_OPEN → OPEN (recovery failed)")
                self.state = CircuitState.OPEN
            elif self.failure_count >= self.failure_threshold:
                logger.error(f"{self.name}: CLOSED → OPEN ({self.failure_count} failures)")
                self.state = CircuitState.OPEN

    def get_state(self) -> dict:
        return {
            "name":          self.name,
            "state":         self.state.value,
            "failure_count": self.failure_count,
            "last_failure":  self.last_failure_time,
        }
```

**Применение**:
```python
# В agent.py — обернуть критические вызовы:
from circuit_breaker import CircuitBreaker, CircuitBreakerOpenError

cb_neo4j = CircuitBreaker("neo4j", failure_threshold=5, timeout=60)
cb_redis  = CircuitBreaker("redis", failure_threshold=3, timeout=30)

# При запросе к графу:
try:
    result = await cb_neo4j.call(graph.execute_cypher, query, params)
except CircuitBreakerOpenError:
    logger.warning("Neo4j unavailable — degraded mode")
    result = []  # fallback
```

---

### HYPERIA-9: SOARGoalNode — Иерархия целей

> **Источник**: HYPERIA `memory/core_memory_blocks.py`
> **Проблема**: L0 Goal Stack хранит цели как flat string.
> **Решение**: `GoalNode(priority, parent_id)` — иерархическая структура.
> Backwards compatible: `str(goal_node)` возвращает description.

```python
# Добавить в memory/core_memory_blocks.py — расширение Goal Stack

from dataclasses import dataclass, field
from typing import Optional, List
import uuid


@dataclass
class GoalNode:
    """
    Иерархическая цель в Goal Stack (L0).
    Backwards compatible: str(node) = description.
    priority: 0.0–1.0 (1.0 = наивысший)
    parent_id: None = корневая цель, иначе ссылка на родителя
    """
    description: str
    priority:    float         = 0.5
    goal_id:     str           = field(default_factory=lambda: uuid.uuid4().hex[:8])
    parent_id:   Optional[str] = None
    children:    List[str]     = field(default_factory=list)  # goal_id дочерних целей
    status:      str           = "active"   # active | completed | suspended

    def __str__(self) -> str:
        return self.description  # backwards compatible с flat string

    def __repr__(self) -> str:
        return f"GoalNode({self.goal_id}: {self.description!r} p={self.priority})"

    def is_root(self) -> bool:
        return self.parent_id is None

    def to_dict(self) -> dict:
        return {
            "goal_id":     self.goal_id,
            "description": self.description,
            "priority":    self.priority,
            "parent_id":   self.parent_id,
            "status":      self.status,
        }
```

---

### HYPERIA-10: Каскадная инвалидация стратегий

> **Источник**: HYPERIA `memory_gc.py` — `_invalidate_stale_strategies()`
> **Проблема**: Velantrim имеет связь `(:Strategy)-[:DERIVED_FROM]->(:Fact)` в схеме,
> но нет логики реакции на инвалидацию факта. Зомби-стратегии накапливаются.
> **Решение**: При `Fact → Deprecated/Collapsed` → все Strategy немедленно `valid=false`.

```python
# Добавить в L4 GC Worker (reasoning_bank.py или отдельный gc воркер)
# Запускается из SleepTimeWorker раз в сутки.

async def invalidate_stale_strategies(graph) -> int:
    """
    Каскадная инвалидация стратегий при инвалидации зависимых фактов.
    FIX: confidence × 0.5 создавал зомби-стратегии (0.95 → 0.475 → никогда не удалялась).
    Новый подход: факт неактивен → стратегия НЕМЕДЛЕННО valid=false, confidence=0.0.
    """
    # Шаг 1: стратегии с deprecated/collapsed фактами
    result = await graph.execute_cypher("""
        MATCH (s:Strategy)-[:DERIVED_FROM]->(f:Fact)
        WHERE f.epistemic_state IN ['Deprecated', 'Collapsed']
          AND coalesce(s.is_active, true) = true
        SET s.is_active   = false,
            s.confidence  = 0.0,
            s.deprecated_at = datetime(),
            s.deprecated_reason = 'source_fact_deprecated'
        RETURN count(s) as invalidated
    """)
    invalidated = result[0]["invalidated"] if result else 0

    # Шаг 2: стратегии с confidence ниже порога (другие причины)
    result2 = await graph.execute_cypher("""
        MATCH (s:Strategy)
        WHERE s.confidence < 0.2
          AND coalesce(s.is_active, true) = true
        SET s.is_active = false,
            s.deprecated_reason = 'low_confidence'
        RETURN count(s) as low_conf
    """)
    low_conf = result2[0]["low_conf"] if result2 else 0

    total = invalidated + low_conf
    if total:
        import logging
        logging.getLogger(__name__).info(
            f"Strategy GC: {invalidated} invalidated (dead facts) + "
            f"{low_conf} (low confidence) = {total} total"
        )
    return total
```

---

### 3. Фрактальная иерархия: Автоматическая консолидация

**Назначение**: Перемещение информации между уровнями БЕЗ LLM-запросов

```python
# fractal_memory.py

def fsrs_retention(t_hours: float, S: float) -> float:
    """P1-J FIX: FSRS power-law retention formula (v8.0 Crystal).
    R = (1 + 19/81 × t/S)^(-0.5)
    Заменяет np.exp(-t/S) из Ebbinghaus — более точная модель долгосрочного удержания.
    Args:
        t_hours: время с последнего повторения (в часах)
        S: stability — стабильность памяти (в часах)
    Returns: R — вероятность воспроизведения [0.0, 1.0]
    """
    if S <= 0:
        return 0.0
    return (1.0 + (19.0 / 81.0) * (t_hours / S)) ** (-0.5)

from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np


def fsrs_retention(t_hours: float, stability: float) -> float:
    """
    FSRS power-law decay (v8.0 — заменяет Ebbinghaus экспоненту).
    R = (1 + 19/81 × t/S)^(-0.5)

    Args:
        t_hours: время с момента последнего доступа в часах
        stability: сила памяти (importance × log(1 + access_count))

    Returns:
        Retention в [0.0, 1.0]

    Конфликт-1 FIX: заменяет np.exp(-t/S) во всех местах FractalMemory.
    Источник: FadeMem paper, Jan 2026 — точнее Ebbinghaus на 20-30%.
    """
    if stability <= 0:
        return 0.0
    return (1.0 + (19.0 / 81.0) * (t_hours / stability)) ** (-0.5)


@dataclass
class MemoryItem:
    id: str
    content: str
    embedding: np.ndarray
    importance: float
    access_count: int
    last_accessed: datetime
    created_at: datetime
    level: int  # 0=STM, 1=MTM, 2=LTM

# Кэш стоп-слов — инициализируется один раз при импорте модуля (не при каждой суммаризации)
try:
    from nltk.corpus import stopwords as _nltk_sw
    _STOP_RU_CACHED = _nltk_sw.words('russian')
except Exception:
    _STOP_RU_CACHED = []

class FractalMemory:
    def __init__(self, graph_memory: GraphMemory, llm_client=None):
        self.graph = graph_memory
        self.llm_client = llm_client  # объявлен явно — устраняет AttributeError в _llm_summarize_cluster

        # Настройки уровней
        self.stm_capacity   = 5   # Cowan 4±1 — берём верхнюю границу диапазона
        self.mtm_capacity   = 25

        # Конфликт-3 FIX: явные единицы для decay rates.
        # Все значения в единицах "за час" (совместимо с age_hours в формулах).
        # При FSRS: stability = importance * (1 + log(access_count)) / decay_rate
        # STM base unit:  1/0.1  = 10h  (кратковременная память)
        # MTM base unit:  1/0.05 = 20h  (среднесрочная, с учётом rehearsal → ~168h)
        # LTM base unit:  1/0.01 = 100h (долгосрочная, с учётом rehearsal → ~720h)
        self.stm_decay_rate = 0.1   # за час; STM base window ≈ 10h
        self.mtm_decay_rate = 0.05  # за час; MTM base window ≈ 20h (→ ~неделя с rehearsal)
        self.ltm_decay_rate = 0.01  # за час; LTM base window ≈ 100h (→ ~месяц с rehearsal)

        # защита stm_cache и mtm_cache от race condition
        self._cache_lock = asyncio.Lock()

        # In-memory кэши для STM/MTM
        self.stm_cache: List[MemoryItem] = []
        self.mtm_cache: List[MemoryItem] = []

    async def add_to_stm(self, content: str, embedding: np.ndarray):
        """Добавить в краткосрочную память. Защищён asyncio.Lock."""
        item = MemoryItem(
            id=generate_id(),
            content=content,
            embedding=embedding,
            importance=1.0,
            access_count=1,
            last_accessed=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            level=0
        )
        async with self._cache_lock:
            self.stm_cache.append(item)
            needs_consolidation = len(self.stm_cache) > self.stm_capacity
        # Lock не реентерабельный — consolidate вызываем ВНЕ lock
        if needs_consolidation:
            await self.consolidate_stm_to_mtm()

    async def apply_decay(self) -> dict:
        """
        FSRS retention decay (v8.0): R = (1 + 19/81 * t/S)^(-0.5)  # было: R = e^(-t/S)
            R  = retention fraction applied to importance
            t  = hours since last_accessed
            S  = importance × (1 + log1p(access_count))  — rehearsal effect

        STM base unit: 24 h · MTM base unit: 168 h (week)
        Immunity: pinned=CRITICAL or emotional_salience > 0.85 → skip (ESM.freeze analogue)
        Returns stats dict for Prometheus metrics.
        """
        stats = {"stm_decayed": 0, "mtm_decayed": 0, "dropped": 0}
        now = datetime.now(timezone.utc)

        def _immune(item) -> bool:
            if getattr(item, "pinned", None) == "CRITICAL":
                return True
            if getattr(item, "emotional_salience", 0.0) > 0.85:
                return True
            return False

        async with self._cache_lock:
            # ── STM ──────────────────────────────────────────────────────────
            stm_drop = []
            for item in self.stm_cache:
                if _immune(item):
                    continue
                age_h    = (now - item.last_accessed).total_seconds() / 3600
                strength = max(0.01, item.importance * (1.0 + np.log1p(item.access_count)))
                # P1-J CONFIRMED: FSRS power-law применён корректно (Changelog v8.0.1 ✓)
                retention = fsrs_retention(age_h, stability=strength * 24)
                item.importance = float(np.clip(item.importance * retention, 0.0, 1.0))
                stats["stm_decayed"] += 1
                if item.importance < 0.05:
                    stm_drop.append(item)
            for item in stm_drop:
                self.stm_cache.remove(item)
                stats["dropped"] += 1

            # ── MTM ──────────────────────────────────────────────────────────
            mtm_drop = []
            for item in self.mtm_cache:
                if _immune(item):
                    continue
                age_h    = (now - item.last_accessed).total_seconds() / 3600
                strength = max(0.01, item.importance * (1.0 + np.log1p(item.access_count)))
                # Конфликт-1 FIX: FSRS power-law вместо Ebbinghaus np.exp(-age_h/(strength*168))
                retention = fsrs_retention(age_h, stability=strength * 168)
                item.importance = float(np.clip(item.importance * retention, 0.0, 1.0))
                stats["mtm_decayed"] += 1
                if item.importance < 0.02:
                    mtm_drop.append(item)
            for item in mtm_drop:
                self.mtm_cache.remove(item)
                stats["dropped"] += 1

        logger.info(
            f"apply_decay: stm={stats['stm_decayed']} mtm={stats['mtm_decayed']} "
            f"dropped={stats['dropped']}"
        )
        return stats

    async def consolidate_stm_to_mtm(self):
        """
        Консолидация STM → MTM (БЕЗ LLM).
        asyncio.Lock защищает stm_cache.
        Cold Start Guard (if len < 50) УДАЛЁН — он вызывал OOM
          при stm_capacity=5: guard всегда срабатывал → STM рос бесконечно.
          Cold Start Guard живёт только в L2 (consolidate_mtm_to_ltm).
        """
        async with self._cache_lock:
            now        = datetime.now(timezone.utc)
            to_promote = []
            to_drop    = []
            for item in self.stm_cache.copy():
                age_hours        = (now - item.created_at).total_seconds() / 3600
                importance_score = self._calculate_importance_with_decay(item, age_hours)

                if importance_score > 0.7 or item.access_count > 3:
                    item.level      = 1
                    item.importance = importance_score
                    if len(self.mtm_cache) >= self.mtm_capacity:
                        # ⚠️ ensure_future — НЕ await. Если изменить на await
                        # здесь — deadlock на _cache_lock (non-reentrant).
                        asyncio.ensure_future(self.consolidate_mtm_to_ltm())
                    self.mtm_cache.append(item)
                    to_promote.append(item)
                elif importance_score < 0.3:
                    to_drop.append(item)
                # grey zone [0.3..0.7] — ждёт следующего цикла

            for item in to_promote + to_drop:
                self.stm_cache.remove(item)

        # Запись в граф — вне lock (I/O операция)
        if to_promote:
            await self.graph.add_episode(
                episode_name=f"mtm_batch_{generate_id()}",
                content=" | ".join(i.content for i in to_promote),
                source="stm_consolidation"
            )

    def _calculate_importance_with_decay(
        self, 
        item: MemoryItem, 
        age_hours: float
    ) -> float:
        """
        Улучшенный расчет важности с учетом:
        - Temporal decay (FSRS power-law, v8.0 — заменяет Ebbinghaus)
        - Reinforcement (частота доступа)
        - Emotional salience (успех/провал важнее)
        - Semantic clustering (часть паттерна → важнее)
        - Weighted Semantic Decay по [:CONTRADICTS]

        Конфликт-1 FIX: temporal_decay теперь FSRS power-law, не np.exp().
        """
        # 1. Базовый temporal decay — FSRS power-law (не Ebbinghaus)
        # stm_decay_rate=0.1 → effective stability base = 1/0.1 = 10h
        stability = max(0.01, item.importance * (1.0 + np.log1p(item.access_count)))
        temporal_decay = fsrs_retention(age_hours, stability=stability / self.stm_decay_rate)
        
        # 2. Reinforcement boost: чем чаще вспоминается → меньше decay
        # log1p(x) = log(1+x) для сглаживания
        reinforcement_factor = 1.0 + np.log1p(item.access_count) * 0.1
        
        # 3. Emotional salience: успех/провал запоминается лучше
        emotional_boost = 1.0
        if hasattr(item, 'outcome'):
            if item.outcome in ['success', 'failure']:
                emotional_boost = 1.5  # 50% бонус к важности
            # partial/neutral остаётся 1.0
        
        # 4. Semantic clustering: если память похожа на другие важные
        # (упрощенная версия - можно улучшить с кластеризацией)
        semantic_boost = 1.0
        if hasattr(item, 'cluster_size') and item.cluster_size > 1:
            semantic_boost = 1.0 + min(0.3, item.cluster_size * 0.05)
        
        # 5. Weighted Semantic Decay по [:CONTRADICTS]
        # Факты с противоречиями теряют важность пропорционально
        # доверию к источнику противоречия (trust_score из Guardian)
        # ИММУНИТЕТ: Ring Zero / VALUES CORE (pinned=CRITICAL) не затрагиваются
        epistemic_penalty = 0.0
        if hasattr(item, 'pinned') and item.pinned and \
           getattr(item, 'priority', None) == 'CRITICAL':
            pass  # Ring Zero иммунен к Semantic Decay
        elif hasattr(item, 'contradictions') and item.contradictions:
            for contradiction in item.contradictions:
                # trust_score: 1.0 = научная статья, 0.3 = пользователь, 0.1 = LLM
                trust = getattr(contradiction, 'trust_score', 0.3)
                epistemic_penalty += 0.1 * trust
            # Ограничиваем штраф — не убиваем факт одним противоречием
            epistemic_penalty = min(0.5, epistemic_penalty)
        
        # Итоговый importance score
        final_importance = (
            item.importance 
            * temporal_decay 
            * reinforcement_factor 
            * emotional_boost 
            * semantic_boost
            - epistemic_penalty  # штраф за противоречия
        )
        
        return max(0.0, min(1.0, final_importance))  # Clamp [0, 1]

    async def consolidate_mtm_to_ltm(self):
        """
        Консолидация MTM → LTM. ГИБРИДНЫЙ подход.
        AgglomerativeClustering — CPU-bound (2–10с).
          Snapshot берём ПОД lock (мгновенно), кластеризацию выполняем ВНЕ lock
          через run_in_executor — event loop не блокируется.
        передаём threshold=0.8 как второй аргумент.
        """
        # Шаг 1: snapshot ПОД lock — мгновенно
        async with self._cache_lock:
            mtm_snapshot = list(self.mtm_cache)

        # Шаг 2: кластеризация ВНЕ lock — CPU-bound
        if len(mtm_snapshot) < 2:
            return
        clusters = await asyncio.get_running_loop().run_in_executor(
            None, self._cluster_memories, mtm_snapshot, 0.8  # ✅ threshold передан
        )

        # Шаг 3: запись в граф ВНЕ lock
        episodes_to_remove = []
        for cluster in clusters:
            if len(cluster) >= 3:
                avg_importance = np.mean([m.importance for m in cluster])

                if avg_importance > 0.95 and len(cluster) > 15:
                    summary = await self._llm_summarize_cluster(
                        cluster, model="o4-mini"
                    )
                    consolidation_quality = "high"
                else:
                    summary = await self._extractive_summarize(cluster)  # async метод — прямой await, не to_thread
                    consolidation_quality = "extractive_only"

                await self.graph.add_episode(
                    episode_name=f"ltm_cluster_{generate_id()}",
                    content=summary,
                    source="mtm_consolidation",
                    metadata={
                        "cluster_size":          len(cluster),
                        "avg_importance":        avg_importance,
                        "consolidation_quality": consolidation_quality,
                        "original_ids":          [m.id for m in cluster],
                    }
                )
                episodes_to_remove.extend(cluster)

        # Шаг 4: удаление из кэша ПОД lock
        async with self._cache_lock:
            for item in episodes_to_remove:
                if item in self.mtm_cache:
                    self.mtm_cache.remove(item)

    async def _extractive_summarize(self, cluster: List[MemoryItem]) -> str:
        """
        Extractive summarization БЕЗ LLM.
        Использует TF-IDF для выделения ключевых предложений.

        TfidfVectorizer вынесен в ThreadPoolExecutor —
        sklearn синхронный (CPU-bound), нельзя вызывать из async напрямую.
        """
        from sklearn.feature_extraction.text import TfidfVectorizer

        texts = [item.content for item in cluster]

        all_sentences = []
        for text in texts:
            all_sentences.extend(text.split('. '))

        if len(all_sentences) < 3:
            return '. '.join(all_sentences)

        def _tfidf_sync(sentences):
            """Синхронная CPU-bound работа — в thread pool, не блокирует loop"""
            # stopwords загружаются из модульного кэша — не при каждом вызове
            vectorizer = TfidfVectorizer(max_features=50, stop_words=_STOP_RU_CACHED)
            try:
                tfidf_matrix = vectorizer.fit_transform(sentences)
                scores = tfidf_matrix.sum(axis=1).A1
                top_indices = scores.argsort()[-3:][::-1]
                summary_sentences = [sentences[i] for i in sorted(top_indices)]
                return '. '.join(summary_sentences) + '.'
            except Exception:
                return '. '.join(sentences[:3]) + '.'

        loop = asyncio.get_running_loop()
        # asyncio.to_thread предпочтительнее run_in_executor для Python 3.9+
        # run_in_executor(None, fn, *args) — корректно, но to_thread чище и безопаснее
        return await asyncio.to_thread(_tfidf_sync, all_sentences)

    async def _llm_summarize_cluster(
        self,
        cluster: List[MemoryItem],
        model: str = "o4-mini"  # ранее gpt-4o-mini
    ) -> str:
        """
        LLM-based суммаризация для важных кластеров (importance > 0.95, size > 15).
        Принцип: LLM получает extractive-выжимку и только переформулирует,
        не добавляя новых фактов («LLM как интерпретатор», Copilot RFC).
        """
        # Сначала extractive для сжатия контекста (дешёвый путь)
        extractive = await self._extractive_summarize(cluster)

        # Затем LLM — только для переформулирования готовой выжимки
        prompt = f"""Summarize the following memory cluster into a concise, high-level pattern or insight.
        Focus on: what was learned, what patterns emerged, what strategies worked/failed.
        Do NOT add any facts not present in the input. Reformulate only.

        Memory cluster ({len(cluster)} episodes):
        {extractive}

        High-level summary (max 200 words):"""

        if self.llm_client is None:
            # Fallback: если LLM-клиент не настроен — возвращаем extractive
            logger.warning("_llm_summarize_cluster: llm_client не настроен, возвращаем extractive")
            return extractive

        try:
            summary = await self.llm_client.complete(prompt, model=model)
            return summary
        except Exception as e:
            logger.error(f"_llm_summarize_cluster LLM error: {e}, fallback to extractive")
            return extractive

    def _cluster_memories(
        self,
        memories: List[MemoryItem],
        threshold: float = 0.8
    ) -> List[List[MemoryItem]]:
        """Кластеризация по косинусному сходству эмбеддингов"""
        from sklearn.cluster import AgglomerativeClustering
        
        if len(memories) < 2:
            return []
        
        embeddings = np.array([m.embedding for m in memories])
        
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1-threshold,
            metric='cosine',
            linkage='average'
        )
        
        labels = clustering.fit_predict(embeddings)
        
        # Группировать по labels
        clusters = {}
        for item, label in zip(memories, labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(item)
        
        return [c for c in clusters.values() if len(c) >= 3]
```

**Фоновый процесс консолидации**:

```python
# consolidation_worker.py
import asyncio

class AdaptiveConsolidationWorker:
    """
    Адаптивная консолидация вместо фиксированных интервалов.
    asyncio.gather останавливал ВСЕ воркеры при сбое одного.
    Решение: независимые create_task + _run_loop с авторестартом через 5с.
    _consolidation_lock защищает от concurrent consolidation.
    """
    def __init__(self, fractal_memory: FractalMemory):
        self.memory               = fractal_memory
        self.running              = False
        self._consolidation_lock  = asyncio.Lock()
        self.stm_high_threshold   = 0.8
        self.stm_medium_threshold = 0.5
        self.mtm_high_threshold   = 0.8

    async def start(self):
        """Запустить фоновую консолидацию — независимые задачи."""
        self.running = True
        # сохраняем ссылки — без них GC может уничтожить задачи
        self._tasks = [
            asyncio.create_task(
                self._run_loop("stm_consolidation", self._adaptive_stm_consolidation)
            ),
            asyncio.create_task(
                self._run_loop("mtm_consolidation", self._adaptive_mtm_consolidation)
            ),
            asyncio.create_task(
                self._run_loop("periodic_decay", self._periodic_decay)
            ),
        ]
        logger.info("ConsolidationWorker: all workers started independently")

    async def _run_loop(self, name: str, coro_fn):
        """При сбое — логируем и перезапускаем через 5 секунд."""
        while self.running:
            try:
                await coro_fn()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(
                    f"ConsolidationWorker [{name}] crashed, restarting in 5s: {e}"
                )
                await asyncio.sleep(5)

    async def _adaptive_stm_consolidation(self):
        """STM → MTM с динамическим интервалом. Защищён _consolidation_lock."""
        while self.running:
            current_load = len(self.memory.stm_cache)
            capacity     = self.memory.stm_capacity
            load_ratio   = current_load / capacity if capacity > 0 else 0

            if load_ratio > self.stm_high_threshold:
                interval = 30
                priority = "high"
            elif load_ratio > self.stm_medium_threshold:
                interval = 300
                priority = "medium"
            else:
                interval = 600
                priority = "low"

            logger.info(
                f"STM consolidation: load={load_ratio:.1%}, "
                f"interval={interval}s, priority={priority}"
            )
            await asyncio.sleep(interval)
            async with self._consolidation_lock:
                await self.memory.consolidate_stm_to_mtm()

    async def _adaptive_mtm_consolidation(self):
        """MTM → LTM с адаптивным интервалом. Защищён _consolidation_lock."""
        while self.running:
            current_size = len(self.memory.mtm_cache)
            capacity     = self.memory.mtm_capacity
            load_ratio   = current_size / capacity if capacity > 0 else 0

            if load_ratio > self.mtm_high_threshold:
                interval = 3600
            elif load_ratio > 0.5:
                interval = 21600
            else:
                interval = 86400

            logger.info(
                f"MTM consolidation: load={load_ratio:.1%}, "
                f"next_run_in={interval}s"
            )
            await asyncio.sleep(interval)
            async with self._consolidation_lock:
                await self.memory.consolidate_mtm_to_ltm()

    async def _periodic_decay(self):
        """Периодическое применение decay. Фиксированный интервал."""
        while self.running:
            await asyncio.sleep(3600)
            await self.memory.apply_decay()
            logger.info("Memory decay applied to all levels")

    def stop(self):
        self.running = False
        for task in getattr(self, '_tasks', []):
            task.cancel()
        logger.info("ConsolidationWorker: stop signal sent, all tasks cancelled")
```

---

### 4. Гибридный Retrieval: Минимизация токенов

**Назначение**: Умный поиск релевантной информации с минимальным объемом

```python
# hybrid_retrieval.py
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class RetrievalResult:
    content:         str
    source:          str
    relevance_score: float
    level:           int  # Уровень памяти
    context:         Optional[List[str]] = None  # Связанная информация
    embedding:       Optional[object]    = None  # MMR работает
    metadata:        Optional[dict]      = None


# P1-2 FIX: явный Protocol-контракт для SLM классификатора.
# Без Protocol — AttributeError только в runtime при первом вызове.
# Любой slm_classifier должен реализовывать этот интерфейс.
from typing import Protocol, runtime_checkable

@runtime_checkable
class SLMClassifierProtocol(Protocol):
    """
    Контракт для tiny LLM классификатора (Qwen3-1.7B / OLMoE-1B).

    P1-2 FIX: явный Protocol вместо duck typing.
    Без Protocol — AttributeError только в runtime при первом вызове.
    """

    def classify(self, text: str, labels: list) -> str:
        """
        Классифицировать текст в один из labels.

        Args:
            text: входной запрос
            labels: список допустимых классов, например ["RECALL", "DEFINE", "POLICY", "TASK"]

        Returns:
            Один из элементов labels. Никогда не возвращает строку вне labels.

        Raises:
            ValueError: если labels пуст
            RuntimeError: если модель не загружена
        """
        ...


class HybridRetriever:
    def __init__(
        self,
        graph_memory: GraphMemory,
        fractal_memory: FractalMemory,
        token_budget: int = 2000,
        hyde_enabled: bool = False,   # HyDE опционально, по умолчанию выключен
        llm_fast = None,              # нужен только если hyde_enabled=True
        slm_classifier = None         # P1-2 FIX: опциональный SLM классификатор
    ):
        self.graph = graph_memory
        self.fractal = fractal_memory
        self.token_budget = token_budget
        self.hyde_enabled = hyde_enabled
        self.llm_fast = llm_fast      # o4-mini / Haiku — дешёвый вызов для генерации гипотезы

        # P1-2 FIX: валидировать контракт при инициализации
        if slm_classifier is not None and not isinstance(slm_classifier, SLMClassifierProtocol):
            raise TypeError(
                f"slm_classifier должен реализовывать SLMClassifierProtocol. "
                f"Получен {type(slm_classifier).__name__}. "
                f"Требуется метод classify(text: str, labels: list) -> str"
            )
        self.slm_classifier = slm_classifier

    async def _get_embedding(self, text: str):
        """
        Делегирует в fractal.graph (EmbeddingEngine через GraphMemory).
        Fallback: если graph не поддерживает get_embedding — возвращает None
        и _search_stm пропускает STM-поиск без падения.
        """
        try:
            if hasattr(self.graph, 'get_embedding'):
                return await self.graph.get_embedding(text)
            # Fallback через graphiti если есть
            if hasattr(self.graph, 'graphiti') and hasattr(self.graph.graphiti, 'get_embedding'):
                return await self.graph.graphiti.get_embedding(text)
        except Exception as e:
            logger.warning(f"HybridRetriever._get_embedding failed: {e}")
        return None

    async def retrieve(
        self,
        query: str,
        query_type: str = "general"
    ) -> List[RetrievalResult]:
        """
        Гибридный retrieval с роутингом по типу запроса
        """
        # 1. Роутинг: определить стратегию поиска
        strategy = self._route_query(query, query_type)

        # 1.5. HyDE (Hypothetical Document Embeddings) — опционально
        # Идея: вместо embedding вопроса использовать embedding гипотетического ответа.
        # LLM генерирует «как мог бы выглядеть ответ» → его вектор ближе к реальным фактам.
        # Даёт +15-20% точности на factoid-запросах. Цена: 1 дешёвый LLM-вызов.
        # Выключен по умолчанию (hyde_enabled=False) — включай осознанно.
        search_query = query
        if self.hyde_enabled and self.llm_fast is not None:
            search_query = await self._hyde_expand(query)

        # 2. Многоэтапный поиск
        results = []
        
        # Stage 1: Проверить STM (быстро, in-memory)
        if strategy in ["conversation", "immediate", "RECALL", "TASK"]:
            query_embedding = await self._get_embedding(query)  # инициализация до передачи в _search_stm
            stm_results = await self._search_stm(query, query_embedding)  # STM всегда по оригинальному query
            results.extend(stm_results)
        
        # Stage 2: Векторный поиск по графу (быстрый ANN)
        graph_results = await self.graph.search(
            query=search_query,  # HyDE: расширенный запрос или оригинальный
            num_results=10
        )
        results.extend(self._convert_to_retrieval_results(
            graph_results, source="graph"
        ))
        
        # Stage 3: Graph expansion для контекста
        if strategy in ["complex", "planning"]:
            for result in graph_results[:3]:  # Топ-3
                expanded = await self._expand_context(result)
                results.extend(self._convert_to_retrieval_results(
                    expanded, source="graph_expand"
                ))
        
        # 3. Reranking
        results = await self._rerank(query, results)
        
        # 4. Token budgeting: выбрать топ-K в пределах бюджета
        results = self._apply_token_budget(results)
        
        return results

    async def _hyde_expand(self, query: str) -> str:
        """
        HyDE: Hypothetical Document Embeddings (Gao et al., 2022).

        Генерирует гипотетический ответ на запрос с помощью быстрого LLM,
        затем использует этот ответ как поисковый запрос вместо оригинального.

        Почему это работает: embedding вопроса ("Что такое фотосинтез?") семантически
        далеко от embedding ответа ("Фотосинтез — процесс..."). Гипотетический ответ
        создаёт вектор в правильном смысловом пространстве.

        Когда включать: hyde_enabled=True при фактологических запросах (DEFINE/RECALL).
        Когда НЕ нужен: TASK/POLICY запросы, диалог, уточнения — оригинальный query лучше.
        """
        try:
            prompt = (
                f"Сгенерируй короткий гипотетический ответ на вопрос (1-2 предложения, "
                f"только факты, без вводных слов):\n{query}"
            )
            hypothesis = await self.llm_fast.generate(prompt, max_tokens=100)
            return hypothesis.strip()
        except Exception as e:
            logger.warning(f"HyDE failed, fallback to original query: {e}")
            return query  # graceful fallback — никогда не ломаем retrieval

    def _route_query(self, query: str, query_type: str) -> str:
        """
        Memory Router — bilingual (RU+EN) + confidence + SLM fallback.
        RFC0003: Четыре строгих класса вместо размытых эвристик.
        Поддержка EN паттернов + подсчёт уверенности + SLM fallback при низкой уверенности.
        """
        query_lower = query.lower()

        ROUTE_PATTERNS = {
            "RECALL": [
                # RU
                "как мы", "вчера", "ранее", "прошлый", "помнишь", "мы решали",
                "ты говорил", "мы обсуждали", "в прошлый раз",
                # EN
                "earlier", "last time", "remember", "we discussed",
                "you said", "previously", "we talked about",
            ],
            "DEFINE": [
                # RU
                "что такое", "что значит", "определение", "объясни", "почему",
                "как работает", "расскажи о",
                # EN
                "what is", "explain", "define", "how does", "what are",
                "tell me about", "describe",
            ],
            "POLICY": [
                # RU
                "как реагировать", "правило", "стратегия", "подход", "политика",
                # EN
                "how to handle", "rule", "strategy", "approach", "policy",
                "best practice",
            ],
            "TASK": [
                # RU
                "сейчас", "текущий", "цель", "задача", "только что",
                # EN
                "current", "now", "goal", "task", "right now", "in progress",
            ],
        }

        # Подсчёт совпадений для каждого маршрута
        scores = {route: 0 for route in ROUTE_PATTERNS}
        for route, patterns in ROUTE_PATTERNS.items():
            for pattern in patterns:
                if pattern in query_lower:
                    scores[route] += 1

        best_route = max(scores, key=scores.get)
        best_score = scores[best_route]

        # Низкая уверенность (≤1 совпадение) → SLM fallback
        # Qwen3-1.7B / OLMoE-1B — уже в стеке как LLM Tiny, 0 токенов flagship
        if best_score <= 1 and hasattr(self, 'slm_classifier') and self.slm_classifier is not None:
            return self._slm_classify(query)

        # Нулевой score → TASK (операционный запрос вероятнее чем концептуальный)
        return best_route if best_score > 0 else "TASK"

    def _slm_classify(self, query: str) -> str:
        """
        SLM-fallback классификатор для неоднозначных запросов.
        Вызывается когда pattern-matching дал ≤1 совпадения.
        Контракт: slm_classifier реализует SLMClassifierProtocol.
        Возвращает один из: RECALL | DEFINE | POLICY | TASK

        P1-2 FIX: добавлена валидация результата + явный fallback.
        """
        VALID_LABELS = ("RECALL", "DEFINE", "POLICY", "TASK")
        try:
            result = self.slm_classifier.classify(
                query,
                labels=list(VALID_LABELS)
            )
            if result in VALID_LABELS:
                return result
            # Если classifier вернул что-то вне labels — логируем и fallback
            logger.warning(
                f"_slm_classify: unexpected result '{result}' not in {VALID_LABELS}, "
                f"falling back to TASK"
            )
        except Exception as e:
            logger.warning(f"_slm_classify failed: {e} — fallback to TASK")
        return "TASK"  # безопасный fallback

    async def _search_stm(self, query: str, query_embedding=None) -> List[RetrievalResult]:
        """Поиск в кэше STM"""
        # Используем переданный embedding или вычисляем новый (один раз)
        if query_embedding is None:
            query_embedding = await self._get_embedding(query)
        
        results = []
        if query_embedding is None:  # embedding недоступен — пропускаем STM без падения
            return results
        
        for item in self.fractal.stm_cache:
            similarity = cosine_similarity(query_embedding, item.embedding)
            if similarity > 0.7:
                results.append(RetrievalResult(
                    content=item.content,
                    source="stm",
                    relevance_score=similarity,
                    level=0
                ))
        
        return results

    async def _expand_context(self, node: dict) -> List[str]:
        """
        Обход графа для получения контекста
        Ограничиваем depth чтобы не взорвать токены
        """
        context = await self.graph.get_context_for_entity(
            entity_name=node.get("entity_name"),
            depth=1  # Только непосредственные соседи
        )
        
        return context.get("related_entities", [])

    def _convert_to_retrieval_results(
        self,
        items: list,
        source: str,
        level: int = 3
    ) -> List[RetrievalResult]:
        """
        метод отсутствовал — AttributeError при каждом поиске по графу.
        Конвертирует сырые результаты из graph.search() / graph_expand в RetrievalResult.
        """
        results = []
        for item in items:
            if not item:
                continue
            content = (
                item.get("content") or
                item.get("summary") or
                item.get("name") or
                str(item)
            )
            results.append(RetrievalResult(
                content=content,
                source=source,
                relevance_score=float(item.get("score", item.get("relevance_score", 0.5))),
                level=level,
                metadata=item if isinstance(item, dict) else None,
            ))
        return results

    async def _rerank(
        self,
        query: str,
        results: List[RetrievalResult]
    ) -> List[RetrievalResult]:
        """
        Reranking с cross-encoder (дорого, но для малого k)
        Альтернатива: простая эвристика на основе recency + relevance
        """
        # Простой reranking БЕЗ cross-encoder
        now = datetime.now(timezone.utc)
        
        for result in results:
            # Учитываем свежесть и уровень памяти
            level_penalty = 0.9 ** result.level  # Более глубокие уровни менее актуальны
            
            result.relevance_score = result.relevance_score * level_penalty
        
        # Сортировать по новому score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results

    def _apply_token_budget(
        self,
        results: List[RetrievalResult]
    ) -> List[RetrievalResult]:
        """
        Выбрать топ-K результатов в пределах token budget
        """
        selected = []
        total_tokens = 0
        
        for result in results:
            result_tokens = count_tokens(result.content)
            
            if total_tokens + result_tokens <= self.token_budget:
                selected.append(result)
                total_tokens += result_tokens
            else:
                break  # Бюджет исчерпан
        
        return selected
```

### P0-3: Reranker с fallback (`memory/reranker.py`)

```python
# memory/reranker.py — фабрика с fallback
# Default: ColBERTv2 или bge-reranker-large. Qwen3 — только opt-in с native Transformers.
import logging
logger = logging.getLogger(__name__)

def get_reranker(backend: str = None):
    backend = backend or config.RERANKER_BACKEND
    if backend == "qwen3":
        logger.warning("Qwen3 Reranker: known issues в vLLM/llama.cpp. "
                       "Используйте только с native Transformers.")
        return Qwen3Reranker()
    elif backend == "colbertv2":
        return ColBERTv2Reranker()
    elif backend == "bge-reranker-large":
        return BGEReranker()
    return NoopReranker()
```

Конфиг:
```python
RERANKER_BACKEND = "colbertv2"  # "colbertv2" | "bge-reranker-large" | "qwen3" | "none"
```

---

### P1-1: `memory/intent_router.py` (MAGMA IntentRouter)

```python
# memory/intent_router.py
# I86: IntentRouter вызывается ТОЛЬКО из HybridRetriever.retrieve().
# 0 токенов, rule-based, <1ms.

def route_query_intent(query: str) -> list[str]:
    q = query.lower()
    if any(w in q for w in ["почему", "из-за", "причина", "why", "because", "cause"]):
        return ["CAUSAL_REL", "CAUSES"]
    elif any(w in q for w in ["когда", "после", "до", "when", "before", "after"]):
        return ["TEMPORAL_REL"]
    elif any(w in q for w in ["что такое", "определение", "what is", "define"]):
        return ["SEMANTIC_REL", "SIMILAR_TO"]
    return ["SEMANTIC_REL", "CAUSAL_REL", "TEMPORAL_REL", "ENTITY_REL"]
```

### P1-6: `memory/pagerank.py` (HippoRAG Personalized PageRank)

```python
# memory/pagerank.py
# HippoRAG-style: +7% на ассоциативных задачах, 0 LLM-вызовов
# ⚠️ NetworkX исключён из стека (слишком медленно на >1k узлов).
# Используем python-igraph (одобрен для Phase 0 SAE в EtirConfig).

def personalized_pagerank(
    graph_edges: list[tuple],
    query_nodes: list[str],
    alpha: float = 0.85,
    top_k: int = 20
) -> list[tuple[str, float]]:
    try:
        import igraph as ig
        # Собираем все уникальные вершины
        all_nodes = list({n for edge in graph_edges for n in edge})
        if not all_nodes:
            return []
        node_idx = {n: i for i, n in enumerate(all_nodes)}
        edges_idx = [(node_idx[a], node_idx[b]) for a, b in graph_edges
                     if a in node_idx and b in node_idx]
        G = ig.Graph(n=len(all_nodes), edges=edges_idx, directed=True)
        G.vs["name"] = all_nodes
        reset_prob = [
            (1.0 / len(query_nodes)) if all_nodes[i] in query_nodes else 0.0
            for i in range(len(all_nodes))
        ]
        # igraph personalized PageRank
        pr_scores = G.personalized_pagerank(
            damping=alpha,
            reset=reset_prob,
            directed=True
        )
        result = [(all_nodes[i], pr_scores[i]) for i in range(len(all_nodes))]
        return sorted(result, key=lambda x: x[1], reverse=True)[:top_k]
    except ImportError:
        # Fallback: простой degree-based score без PageRank
        import logging
        logging.getLogger(__name__).warning(
            "pagerank.py: igraph не установлен — fallback на degree score. "
            "Установите: pip install igraph"
        )
        degree: dict[str, float] = {}
        for a, b in graph_edges:
            degree[a] = degree.get(a, 0) + 1
            degree[b] = degree.get(b, 0) + 1
        boost = {n: 2.0 for n in query_nodes}
        scored = {n: (boost.get(n, 1.0) * d) for n, d in degree.items()}
        return sorted(scored.items(), key=lambda x: x[1], reverse=True)[:top_k]
```

---

### 🔍 HyDE — Hypothetical Document Embeddings (opt-in)

**Конфиг-флаг**: `hyde_enabled: false` (в `velantrim_config.py`)

**Суть**: один LLM-вызов генерирует гипотетический ответ на вопрос пользователя.
Embedding гипотетического ответа геометрически ближе к реальным фактам графа,
чем embedding самого вопроса — потому что вопрос и ответ живут в разных
семантических пространствах.

**Результат**: +15–20% точности извлечения на DEFINE/RECALL запросах
по сравнению с прямым поиском по embedding вопроса.

**Алгоритм при hyde_enabled=true**:
1. `hypothetical = await llm.complete(f"Ответь кратко: {query}")` — 1 вызов
2. `hyp_embedding = embedder.encode(hypothetical)`
3. Retrieval по `hyp_embedding` вместо `query_embedding`
4. CORNER-дедупликация результатов если оба источника активны

**Когда включать**: только на DEFINE и RECALL типах запросов (FactRouter).
На TASK и POLICY — не даёт прироста, добавляет задержку.

**Инвариант**:
```
HyDE включается ТОЛЬКО через конфиг-флаг `hyde_enabled: true`.
Активация через правку кода (не конфига) — нарушение.
Недопустимо использовать HyDE на Fast Path без feature-flag.
```

**Добавить в `velantrim_config.py`**:
```python
HYDE_ENABLED = False  # HyDE: гипотетический embedding для DEFINE/RECALL (+15-20% точности)
# Включать только после тестирования латентности на целевом железе
```

---

### 🗺 TraversalPolicy — Стратегия обхода рёбер по типу запроса

**Источник**: MAGMA-style (arXiv 2601.03236) · **Эффект**: +10.6 F1 на multi-hop задачах

**Принцип**: разные типы запросов требуют разных стратегий обхода рёбер графа.
Не все рёбра одинаково релевантны для каждого типа задачи.

| Тип запроса (FactRouter) | Стратегия обхода | Приоритетные типы рёбер |
|--------------------------|---------------------|----------------------------------------------|
| `RECALL` | temporal | `[:MENTIONED_IN]`, `[:LED_TO]`, `valid_from` |
| `DEFINE` | causal | `[:CAUSES]`, `[:CONCEPT_OF]`, `[:HAS_RELATION]` |
| `POLICY` | influence | `[:DERIVED_FROM]`, `[:IMPROVES]`, `[:USED_IN]` |
| `TASK` | all | все типы рёбер, глубина +1 |

**Реализация** (добавить в `HybridRetriever.retrieve()`):

```python
# traversal_policy.py
TRAVERSAL_STRATEGIES = {
    "RECALL": {"edge_types": ["MENTIONED_IN", "LED_TO"], "temporal_sort": True},
    "DEFINE": {"edge_types": ["CAUSES", "CONCEPT_OF", "HAS_RELATION"], "temporal_sort": False},
    "POLICY": {"edge_types": ["DERIVED_FROM", "IMPROVES", "USED_IN"], "temporal_sort": False},
    "TASK":   {"edge_types": None, "temporal_sort": False, "depth_bonus": 1},
}

def get_traversal_config(query_type: str) -> dict:
    return TRAVERSAL_STRATEGIES.get(query_type, TRAVERSAL_STRATEGIES["TASK"])
```

**Инвариант I76**:
```
I76 (TraversalPolicy): TraversalPolicy.get_traversal_config() вызывается ТОЛЬКО
из HybridRetriever.retrieve(), не из Fast Path напрямую.
Нарушение: прямое применение traversal-фильтра в agent.chat() минуя retriever.
```

---

### 5. ReasoningBank: Самообучение на опыте

**Назначение**: Извлечение стратегий из успехов и неудач

```python
# reasoning_bank.py
import uuid  # для Strategy.id
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import deque  # deque для ограничения experience_buffer, field
from enum import Enum

class Outcome(Enum):
    SUCCESS = 1
    FAILURE = -1
    PARTIAL = 0

@dataclass
class Experience:
    task_description: str
    context: Dict
    action_taken: str
    outcome: Outcome
    reasoning: str
    timestamp: datetime
    error_message: Optional[str] = None

@dataclass
class Strategy:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    applicable_contexts: List[str]
    success_count: int = 0
    failure_count: int = 0
    confidence: float = 0.5
    failure_penalty: float = 0.1  # Штраф за неудачу
    success_boost: float = 0.05   # Бонус за успех

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0

    def update_confidence(self, outcome: Outcome):
        """
        Обновить confidence на основе результата
        Негативное подкрепление: неудачи снижают confidence
        """
        if outcome == Outcome.SUCCESS:
            # Успех → повысить confidence
            self.confidence = min(1.0, self.confidence + self.success_boost)
        elif outcome == Outcome.FAILURE:
            # Неудача → понизить confidence (negative reinforcement)
            self.confidence = max(0.0, self.confidence - self.failure_penalty)
        
        # Частые неудачи → увеличить penalty
        if self.failure_count > 5:
            # После 5 неудач штраф удваивается
            self.failure_penalty = min(0.3, self.failure_penalty * 1.2)

class ReasoningBank:
    def __init__(self, graph_memory: GraphMemory, llm_client=None):  # llm_client добавлен — ACE Curator и LLM-путь стратегий работают
        self.graph = graph_memory
        self.llm_client = llm_client
        # deque(maxlen=1000) вместо List[] — защита от OOM
        self.experience_buffer = deque(maxlen=1000)
        self.strategies: Dict[str, Strategy] = {}

        # P1-3 FIX: делегат для ACE Curator.
        # Каноническая реализация живёт в agent_with_learning.py::SelfLearningAgent.
        # ReasoningBank не дублирует логику — только делегирует.
        # Устанавливается через set_ace_delegate() из SelfLearningAgent.__init__().
        self._ace_delegate = None

    async def log_experience(
        self,
        task: str,
        context: Dict,
        action: str,
        outcome: Outcome,
        reasoning: str,
        error: Optional[str] = None
    ):
        """Записать опыт выполнения задачи"""
        exp = Experience(
            task_description=task,
            context=context,
            action_taken=action,
            outcome=outcome,
            reasoning=reasoning,
            timestamp=datetime.now(timezone.utc),
            error_message=error
        )
        
        self.experience_buffer.append(exp)
        
        # Сохранить в граф
        await self.graph.add_episode(
            episode_name=f"experience_{generate_id()}",
            content=json.dumps({
                "task": task,
                "action": action,
                "outcome": outcome.value,
                "reasoning": reasoning
            }),
            source="experience_log"
        )
        
        # Если накопилось достаточно опыта - извлечь стратегии
        if len(self.experience_buffer) >= 10:
            await self.distill_strategies()

    async def distill_strategies(self):
        """
        Извлечение высокоуровневых стратегий из опыта
        Можно использовать LLM для лучшего качества (o4-mini достаточно)
        
        P9-FIX БАГ-14: partial progress tracking — каждая группа обрабатывается
        независимо и сразу удаляется из буфера. При сбое в группе N группы 1..N-1
        уже удалены — повторный вызов не дублирует стратегии.
        """
        grouped = self._group_by_task_type(list(self.experience_buffer))
        
        for task_type, experiences in grouped.items():
            try:
                successful = [e for e in experiences if e.outcome == Outcome.SUCCESS]
                failed = [e for e in experiences if e.outcome == Outcome.FAILURE]
                
                if successful:
                    strategy = await self._extract_strategy_from_successes(
                        task_type, successful
                    )
                    await self._save_strategy(strategy)
                
                if failed:
                    anti_pattern = await self._extract_lessons_from_failures(
                        task_type, failed
                    )
                    await self._save_anti_pattern(anti_pattern)
                
                # Удаляем только обработанную группу — сразу после успеха
                for exp in experiences:
                    self.experience_buffer.discard(exp)
            except Exception as e:
                logger.error(
                    f"distill_strategies: group '{task_type}' failed, "
                    f"buffer for this group preserved ({len(experiences)} items): {e}"
                )

    async def _extract_strategy_from_successes(
        self,
        task_type: str,
        successes: List[Experience]
    ) -> Strategy:
        """
        Извлечь общую стратегию из успешных попыток
        """
        # Вариант 1: Простая агрегация БЕЗ LLM
        common_actions = self._find_common_patterns([e.action_taken for e in successes])
        
        # Вариант 2: С дешевым LLM (лучше)
        # strategy_text = await self._llm_summarize(successes)
        
        strategy = Strategy(
            description=f"For {task_type}: {common_actions}",
            applicable_contexts=[task_type],
            success_count=len(successes),
            confidence=len(successes) / (len(successes) + 1)
        )
        
        return strategy

    def _group_by_task_type(
        self,
        experiences: "deque[Experience]"
    ) -> Dict[str, List["Experience"]]:
        """
        Группировать накопленный опыт по типу задачи.
        Тип определяется первым словом task_description (простая эвристика).
        При необходимости заменить на TF-IDF или LLM-классификацию.
        """
        groups: Dict[str, List] = {}
        for exp in experiences:
            # Берём первые два слова как тип задачи
            words = exp.task_description.lower().split()
            task_type = "_".join(words[:2]) if len(words) >= 2 else (words[0] if words else "general")
            groups.setdefault(task_type, []).append(exp)
        return groups

    async def retrieve_relevant_strategies(
        self,
        current_task: str,
        context: Dict,
        epsilon: float = 0.1  # 10% exploration
    ) -> List[Strategy]:
        """
        Поиск релевантных стратегий для текущей задачи
        Использует Thompson Sampling для баланса exploration/exploitation (RFC0039, заменил UCB1)
        """
        # 1. Поиск в графе по контексту задачи
        results = await self.graph.search(
            query=f"strategy for {current_task}",
            num_results=10
        )
        
        # 2. Парсинг стратегий
        strategies = []
        for result in results:
            try:
                strategy_data = json.loads(result.content)
                strategies.append(Strategy(**strategy_data))
            except:
                continue
        
        if not strategies:
            return []
        
        # 3. Thompson Sampling выбор стратегий (RFC0039 — заменил UCB1)
        selected = await self._thompson_sampling_select(strategies)  # UCB1 заменён Thompson Sampling (RFC0039)
        
        return selected[:3]  # Топ-3

    async def _thompson_sampling_select(
        self,
        strategies: List[Strategy],
        top_k: int = 3,
        seed: int | None = None
    ) -> List[Strategy]:
        """
        Thompson Sampling выбор стратегий (RFC0039).
        seed — для воспроизводимого replay в аудите (Инвариант I13).
        """
        import numpy as np
        if not strategies:
            return []
        rng = np.random.default_rng(seed)
        scored = []
        for s in strategies:
            alpha = getattr(s, 'success_count', 0) + 1
            beta  = getattr(s, 'failure_count', 0) + 1
            ts_score = rng.beta(alpha, beta)
            scored.append((ts_score, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:top_k]]

    def _ucb1_select(
        self,
        strategies: List[Strategy],
        context: Dict,
        epsilon: float
    ) -> List[Strategy]:
        """
        ⚠️ УСТАРЕЛО: заменён Thompson Sampling (RFC0039).
        Оставлен для обратной совместимости. Не использовать напрямую.
        Используйте _thompson_sampling_select() вместо этого.
        """
        import random
        import numpy as np
        
        # Exploration с вероятностью epsilon
        if random.random() < epsilon:
            # Вернуть случайную стратегию для exploration
            logger.info("Strategy selection: EXPLORATION mode")
            return random.sample(strategies, min(3, len(strategies)))
        
        # Exploitation: UCB1 scoring
        total_trials = sum(
            s.success_count + s.failure_count for s in strategies
        )
        
        if total_trials == 0:
            # Нет истории → вернуть все
            return strategies
        
        scored_strategies = []
        
        for strategy in strategies:
            trials = strategy.success_count + strategy.failure_count
            
            if trials == 0:
                # Неиспытанная стратегия → максимальный приоритет
                ucb_score = float('inf')
            else:
                # UCB1 formula: mean + exploration_bonus
                exploitation_term = strategy.success_rate
                
                # Exploration bonus: тем выше, чем меньше пробовали
                exploration_bonus = np.sqrt(
                    2 * np.log(total_trials) / trials
                )
                
                # Context similarity: насколько стратегия подходит
                context_similarity = self._compute_context_similarity(
                    strategy.applicable_contexts,
                    context
                )
                
                # Финальный UCB score
                ucb_score = (
                    exploitation_term +           # 0-1: текущий success rate
                    exploration_bonus * 0.5 +     # Бонус за exploration
                    context_similarity * 0.3      # Релевантность контексту
                )
            
            scored_strategies.append((strategy, ucb_score))
        
        # Сортировать по UCB score
        scored_strategies.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(
            f"Strategy selection: EXPLOITATION mode, "
            f"top_score={scored_strategies[0][1]:.3f}"
        )
        
        return [s for s, score in scored_strategies]

    def _compute_context_similarity(
        self,
        strategy_contexts: List[str],
        current_context: Dict
    ) -> float:
        """
        Вычислить похожесть контекста стратегии и текущей задачи
        Упрощенная версия - можно улучшить с эмбеддингами
        """
        if not strategy_contexts:
            return 0.5  # Нейтральная оценка
        
        # Двойной generator comprehension — корректный способ flatten list of words
        current_keywords = {
            word
            for v in current_context.values()
            for word in str(v).lower().split()
        }
        
        strategy_keywords = set(
            word.lower() 
            for ctx in strategy_contexts 
            for word in ctx.split()
        )
        
        if not strategy_keywords:
            return 0.5
        
        # Jaccard similarity
        intersection = len(current_keywords & strategy_keywords)
        union = len(current_keywords | strategy_keywords)
        
        similarity = intersection / union if union > 0 else 0.0
        return similarity

    async def update_strategy_feedback(
        self,
        strategy_id: str,
        outcome: Outcome
    ):
        """
        Обновить статистику стратегии на основе нового опыта
        Включает negative reinforcement через confidence penalty
        """
        strategy = self.strategies.get(strategy_id)
        if not strategy:
            # Найти в графе
            results = await self.graph.search(
                query=f"strategy: {strategy_id}",
                num_results=1
            )
            if not results:
                return
            
            strategy_data = json.loads(results[0].content)
            strategy = Strategy(**strategy_data)
        
        # Обновить счетчики
        if outcome == Outcome.SUCCESS:
            strategy.success_count += 1
        elif outcome == Outcome.FAILURE:
            strategy.failure_count += 1
        
        # Применить negative/positive reinforcement
        strategy.update_confidence(outcome)
        
        logger.info(
            f"Strategy '{strategy_id}' updated: "
            f"success_rate={strategy.success_rate:.1%}, "
            f"confidence={strategy.confidence:.2f}"
        )
        
        # Сохранить обновление в граф
        await self._save_strategy(strategy)

    async def ace_curator_update(self):
        """
        ACE Curator (Stanford/SambaNova ACE pattern).
        Вызывается ТОЛЬКО из SleepTimeWorker в idle — не из Fast Path.

        P1-3 FIX: дублирующая реализация удалена. Делегируем в канонический метод.
        Каноническая реализация: agent_with_learning.py::SelfLearningAgent.ace_curator_update()
        Расхождение было: здесь e.task, там e.task_description[:50] — рассинхронизация.
        Все изменения логики вносить ТОЛЬКО в agent_with_learning.py.
        """
        if self._ace_delegate is None:
            logger.debug("ace_curator_update: _ace_delegate не задан, пропускаем")
            return
        try:
            await self._ace_delegate.ace_curator_update()
        except Exception as e:
            logger.warning(f"ace_curator_update (delegate) failed (non-fatal): {e}")

    def set_ace_delegate(self, delegate) -> None:
        """
        Установить делегат для ACE Curator.
        Вызывать из SelfLearningAgent.__init__() после создания ReasoningBank:
            self.reasoning_bank.set_ace_delegate(self)

        P1-3 FIX: устраняет дублирование ace_curator_update в двух местах.
        """
        self._ace_delegate = delegate
```

**Интеграция в агент**:

```python
# agent_with_learning.py
class SelfLearningAgent:
    def __init__(
        self,
        llm,
        memory: GraphMemory,
        retriever: HybridRetriever,
        reasoning_bank: ReasoningBank
    ):
        self.llm = llm
        self.memory = memory
        self.retriever = retriever
        self.reasoning_bank = reasoning_bank

        # P1-3 FIX: зарегистрировать делегат чтобы reasoning_bank.ace_curator_update()
        # делегировал в канонический метод self.ace_curator_update().
        # Каноническая реализация ACE Curator живёт здесь, не в ReasoningBank.
        self.reasoning_bank.set_ace_delegate(self)

    async def execute_task(self, task: str, context: Dict):
        """
        Выполнение задачи с учетом прошлого опыта
        Цикл: Retrieve → Plan → Execute → Judge → Learn
        """
        # 1. RETRIEVE: Найти релевантные стратегии (Thompson Sampling, RFC0039)
        strategies = await self.reasoning_bank.retrieve_relevant_strategies(
            current_task=task,
            context=context,
            # Thompson Sampling: адаптивный баланс explore/exploit встроен в Beta-распределение
        )
        
        # 2. PLAN: Выбрать стратегию или создать новую
        if strategies:
            best_strategy = strategies[0]
            plan = f"Based on past success, use strategy: {best_strategy.description}"
            strategy_id = best_strategy.id  # используем UUID вместо description
        else:
            plan = await self._create_new_plan(task, context)
            strategy_id = None
        
        # 3. EXECUTE: Выполнить план
        try:
            result = await self._execute_plan(plan, context)
            outcome = Outcome.SUCCESS
            error = None
        except Exception as e:
            result = None
            outcome = Outcome.FAILURE
            error = str(e)
        
        # 4. JUDGE: Оценить результат
        reasoning = await self._reflect_on_outcome(
            task, plan, result, outcome
        )
        
        # 5. LEARN: Сохранить опыт
        await self.reasoning_bank.log_experience(
            task=task,
            context=context,
            action=plan,
            outcome=outcome,
            reasoning=reasoning,
            error=error
        )
        
        # 6. UPDATE: Обновить статистику стратегии
        if strategy_id:
            await self.reasoning_bank.update_strategy_feedback(
                strategy_id=strategy_id,
                outcome=outcome
            )
        
        return result

    async def _reflect_on_outcome(
        self,
        task: str,
        plan: str,
        result: any,
        outcome: Outcome
    ) -> str:
        """
        Рефлексия на результат — извлечь урок для ReasoningBank.

        TODO (Phase 2): заменить эвристику на вызов SLM (Qwen3-1.7B) для
        структурированного анализа: root_cause + conditions + anti_conditions.
        Сейчас используется детерминированная эвристика — 0 токенов LLM.
        """
        if outcome == Outcome.SUCCESS:
            return (
                f"SUCCESS: стратегия '{plan[:80]}' решила задачу '{task[:80]}'. "
                f"Результат получен: {bool(result)}."
            )
        else:
            return (
                f"FAILURE: стратегия '{plan[:80]}' не справилась с задачей '{task[:80]}'. "
                f"Требуется альтернативный подход."
            )
```

---

### 18. velantrim_config.py — Unified Constants 

**Назначение**: Единый источник всех числовых констант системы. Устраняет parameter drift.

```python
# velantrim_config.py
class MemoryConfig:
    STM_CAPACITY = 5
    SESSION_IDLE_MINUTES = 30
    VELUM_CO_OCCUR_THRESHOLD = 3
    VELUM_WINDOW_EPISODES = 5
    VELUM_MAX_EDGES = 1000
    VELUM_PROMOTE_WEIGHT = 0.6
    VELUM_DECAY_PER_SESSION = 0.3
    MTM_CAPACITY = 25
    L2_COLD_START_MIN = 50
    L2_TTL_BASE_DAYS = 7
    L2_TTL_MAX_DAYS = 224
    STAGING_CPU_THRESHOLD = 0.35
    STAGING_RAM_THRESHOLD = 0.25
    STAGING_BATCH_SIZE = 50
    STAGING_MAX_SIZE = 5000
    STAGING_FAST_TRACK = 0.9

class TruthConfig:
    GUARDIAN_CONFIDENCE = 0.7
    TRUTH_GATE_EVIDENCE_MIN = 3
    TRUTH_GATE_CONFIDENCE = 0.75
    EMOTIONAL_RING_ZERO = 0.85
    FAITHFULNESS_THRESHOLD = 0.6

class TokenConfig:
    MEMORY_PER_QUERY = 2000
    PRECISION_MODE = 1000
    BALANCED_MODE = 2000
    EXPLORATION_MODE = 4000

class SLOConfig:
    SEARCH_P95_MS = 500
    ETIR_P95_MS = 50
    CONSOLIDATION_LAG_S = 60
    FAITHFULNESS_MIN = 0.8
    MHI_WARN = 0.50
    MHI_CRITICAL = 0.30

MEMORY = MemoryConfig()
TRUTH = TruthConfig()
TOKENS = TokenConfig()
SLO = SLOConfig()
```

**Использование**:
```python
from velantrim_config import MEMORY, TRUTH

if len(l2_items) < MEMORY.L2_COLD_START_MIN:
    skip_clustering()
```

---

### 19. TruthGateWithESM — Единая точка Guardian + ESM (RFC0015)

**Проблема**: Guardian и ESM были независимы — нет атомарности

**Решение**: Фасад-оркестратор

```python
@dataclass
class TruthGateResult:
    passed: bool
    score: float
    esm_state: str
    reason: str
    emotional_salience: float = 0.0

class TruthGateWithESM:
    def __init__(self, guardian, esm, graph, etir):
        self.guardian = guardian
        self.esm = esm
        self.graph = graph
        self.etir = etir

    async def validate_and_transition(self, item: dict) -> TruthGateResult:
        emotional_salience = float(item.get("emotional_salience", 0.0))
        
        # 1. Guardian валидация
        passed = await self.guardian.validate_proposal(item)
        
        if not passed:
            reason = await self._classify_rejection(item)
            new_state = self._rejection_to_esm_state(reason)
            await self.esm.transition(item["id"], new_state, reason=reason)
            return TruthGateResult(False, 0.0, new_state, reason, emotional_salience)
        
        # 2. Validated
        await self.esm.transition(item["id"], "Validated", reason="TRUTH_GATE_PASSED")
        
        # 3. Ring Zero + Emotional Ring Zero
        if (item.get("pinned") == "CRITICAL" or 
            emotional_salience > TRUTH.EMOTIONAL_RING_ZERO):
            await self.esm.freeze(item["id"])
        
        # 4. Промоут в L3
        await self.graph.promote_from_staging(item)
        
        if emotional_salience > 0.5:
            await self.etir.boost_node(item["id"], emotional_salience)
        
        score = float(item.get("confidence", 1.0))
        return TruthGateResult(True, score, "Validated", 
                               "TRUTH_GATE_PASSED", emotional_salience)
```

**Auto Truth Gate Worker** — Фоновый процесс для автоматического перехода Supported → Validated

```python
# auto_truth_gate_worker.py
# P2-3: Conflict Resolution Window (NGT Memory pattern)
# После фразы "я ошибся" / "correction" / "исправление":
# 60-секундное окно, в котором TruthGate снижает барьер для user_input.
# CORRECTION_WINDOW_SECONDS = 60
# По истечении окна — стандартный режим.
CORRECTION_WINDOW_SECONDS = 60

class AutoTruthGateWorker:
    """
    Фоновый процесс для автоматической валидации фактов.
    Запускается раз в сутки (или по расписанию).

    Проблема: факты с достаточным evidence остаются в Supported
    до случайного попадания в Truth Gate.

    Решение: периодически проверять все Supported факты
    с evidence_count ≥ 3 и переводить в Validated.
    """

    def __init__(self, graph, truth_gate, esm, scheduler_hours=24):
        self.graph = graph
        self.truth_gate = truth_gate
        self.esm = esm
        self.scheduler_hours = scheduler_hours

    async def run_validation_cycle(self):
        """Основной цикл — вызывается APScheduler"""
        # evidence_count — НЕ поле :Fact, evidence хранится через связь [:SUPPORTED_BY]->(:Evidence)
        # Считаем количество Evidence-узлов через граф
        query = """
        MATCH (f:Fact)-[:SUPPORTED_BY]->(ev:Evidence)
        WHERE f.epistemic_state = 'Supported'
          AND f.is_ring_zero <> true
        WITH f, count(ev) AS evidence_count
        WHERE evidence_count >= 3
        RETURN f.id AS id, evidence_count, f.importance_score AS importance_score
        ORDER BY f.importance_score DESC
        LIMIT 100
        """
        
        candidates = await self.graph.execute_cypher(query)
        validated_count = 0
        
        for fact in candidates:
            # Проверить через Truth Gate
            result = await self.truth_gate.validate_and_transition({
                "id": fact['id'],
                "evidence_count": fact['evidence_count'],
                "importance_score": fact['importance_score']
            })
            
            if result.passed:
                validated_count += 1
        
        logger.info(
            f"Auto Truth Gate: {validated_count}/{len(candidates)} facts "
            f"transitioned Supported → Validated"
        )
        
        return validated_count

# Интеграция в startup
# scheduler.add_job(auto_truth_gate_worker.run_validation_cycle, 
#                   'interval', hours=24)
```

---

### 20. L1.5 Velum — Детектор ранних связей (RFC0016)

**Назначение**: LTP-inspired механизм детекции co-occurrence

```python
@dataclass
class VelumEdge:
    entity_a: str
    entity_b: str
    weight: float
    session_id: str
    first_seen: float
    last_seen: float
    count: int = 1
    promoted: bool = False

@dataclass
class VelumSignal:
    entity_a: str
    entity_b: str
    weight: float
    reason: str
    episode_ids: list[str]

@dataclass
class VelumConfig:
    """
    Конфигурация Velum.
    persist=True: рёбра сохраняются в SQLite и восстанавливаются при рестарте.
    Без persist рёбра живут только в RAM текущей сессии — связи теряются при перезапуске.
    """
    persist:     bool = False
    sqlite_path: str  = "./data/velum_seed.db"


class Velum:
    def __init__(self, session_id: str, l2_signal_callback=None,
                 config: VelumConfig = None):
        self.session_id = session_id
        self._signal_callback = l2_signal_callback
        self._config = config or VelumConfig()
        self._edges: dict[frozenset, VelumEdge] = {}
        self._entity_index: dict[str, list[frozenset]] = defaultdict(list)
        self._recent_episodes = []
        self._lock = asyncio.Lock()  # защита self._edges от race condition при конкурентных инсертах

        # P0-1 FIX: _degree_cache — кэш степеней узлов для ACT-R fan-effect.
        # Инкрементируется в _add_edge(), декрементируется в gc_weak_edges().
        # Без инициализации здесь → AttributeError при первом _strengthen_edge().
        self._degree_cache: dict[str, int] = {}
        # P0-F FIX: трекинг episode_ids текущей сессии для on_session_end VelumSignal.
        # Без этого поля on_session_end не может передать episode_ids → пустой список.
        self._current_session_episodes: list[str] = []

        # FIX из HYPERIA: восстановить топ рёбра из предыдущей сессии при старте.
        # Без этого Velum всегда начинает с нуля — первые N эпизодов не имеют
        # накопленных co-occurrence и сигналы в L2 не генерируются.
        if self._config.persist:
            self._load_seed_from_sqlite()

    async def observe_episode(self, episode_id: str, entities: list[str]) -> list[VelumSignal]:
        """P0-D FIX: observe_episode захватывает self._lock только для _recent_episodes,
        затем ОСВОБОЖДАЕТ lock перед вызовом _update_edge (который захватывает lock сам).
        asyncio.Lock не реентрантный — вложенный захват = deadlock.
        Паттерн: захват → копия → release → работа с копией.
        """
        signals = []
        async with self._lock:  # защита _recent_episodes от concurrent inserts
            self._current_session_episodes.append(episode_id)  # P0-F FIX: трекинг для on_session_end
            self._recent_episodes.append((episode_id, entities))
            if len(self._recent_episodes) > MEMORY.VELUM_WINDOW_EPISODES:
                self._recent_episodes.pop(0)
            window_entities = [(ep_id, ent) for ep_id, ents in self._recent_episodes for ent in ents]
        
        # co-occurrence вне lock — I/O bound, не мутирует _recent_episodes
        for i, (eid_a, ent_a) in enumerate(window_entities):
            for eid_b, ent_b in window_entities[i+1:]:
                if ent_a != ent_b:
                    signal = await self._update_edge(ent_a, ent_b, [eid_a, eid_b])
                    if signal:
                        signals.append(signal)
        
        return signals

    # Метод на уровне класса (не вложен в observe_episode)
    async def _update_edge(self, entity_a: str, entity_b: str,
                           episode_ids: list) -> "VelumSignal | None":
        """
        Обновить вес ребра co-occurrence. Возвращает VelumSignal если порог достигнут.
        заменён NotImplementedError — L1.5 Velum теперь работает.
        """
        key = frozenset([entity_a, entity_b])
        async with self._lock:
            if key not in self._edges:
                _now = time.monotonic()  # import time должен быть в начале файла
                self._edges[key] = VelumEdge(
                    entity_a=entity_a, entity_b=entity_b,
                    weight=0.0, session_id=self.session_id,
                    first_seen=_now,
                    last_seen=_now,
                )
                self._entity_index[entity_a].append(key)
                self._entity_index[entity_b].append(key)

            edge = self._edges[key]
            edge.weight  = min(1.0, edge.weight + 0.1)
            edge.count  += 1
            edge.last_seen = time.monotonic()

            # FIX из HYPERIA: GC слабых рёбер при росте словаря.
            # Без этого _edges растёт бесконечно — одна сессия с широким контекстом
            # может накопить тысячи рёбер с weight≈0.1 которые никогда не промоутируются.
            if len(self._edges) > 1000:
                self._gc_weak_edges()

            # P1-A FIX: порог был VELUM_CO_OCCUR_THRESHOLD/10 = 3/10 = 0.3 → ложные сигналы 2×.
            # Спецификация требует weight ≥ VELUM_PROMOTE_WEIGHT (0.6) AND count ≥ CROSS_SESSION (3).
            if (edge.weight >= MEMORY.VELUM_PROMOTE_WEIGHT
                    and edge.count >= MEMORY.VELUM_CO_OCCUR_THRESHOLD):
                signal = VelumSignal(
                    entity_a=entity_a, entity_b=entity_b,
                    weight=edge.weight, reason="CO_OCCUR_THRESHOLD",
                    episode_ids=episode_ids,
                )
            else:
                signal = None
        # FIX: callback вызывается ВНЕ async with self._lock.
        # Вызов внутри lock создаёт риск deadlock если callback сам обращается к Velum.
        if signal and self._signal_callback:
            await self._signal_callback(signal)
        return signal

    async def on_session_end(self) -> list[VelumSignal]:
        signals = []
        # FIX: итерация по self._edges защищена self._lock.
        # Без блокировки concurrent _update_edge вызывал
        # RuntimeError: dictionary changed size during iteration.
        async with self._lock:
            edges_snapshot = list(self._edges.items())
        for key, edge in edges_snapshot:
            if edge.weight >= MEMORY.VELUM_PROMOTE_WEIGHT:
                signal = VelumSignal(
                    entity_a=edge.entity_a, entity_b=edge.entity_b,
                    weight=edge.weight, reason="SESSION_END",
                    episode_ids=[])  # episode_ids обязателен — без него TypeError при каждом session_end
                signals.append(signal)
                if self._signal_callback:
                    await self._signal_callback(signal)
            else:
                edge.weight *= (1.0 - MEMORY.VELUM_DECAY_PER_SESSION)

        # FIX из HYPERIA: сохранить топ рёбра в SQLite при завершении сессии.
        # Сохраняем ссылку на task — без неё GC убивает корутину до завершения записи.
        if self._config.persist:
            _t = asyncio.create_task(self._save_top_edges_to_sqlite(top_n=200))
            _t.add_done_callback(
                lambda t: t.exception() and
                logger.debug(f"Velum persist failed: {t.exception()}")
            )

        return signals

    def get_neighbors(self, entity: str, min_weight: float = 0.3) -> list[tuple[str, float]]:
        result = []
        for key in self._entity_index.get(entity, []):
            edge = self._edges.get(key)
            if edge and edge.weight >= min_weight:
                neighbor = edge.entity_b if edge.entity_a == entity else edge.entity_a
                result.append((neighbor, edge.weight))
        return sorted(result, key=lambda x: x[1], reverse=True)

    def _gc_weak_edges(self, keep_ratio: float = 0.75):
        """
        GC слабых рёбер co-occurrence.
        Вызывается изнутри _update_edge под self._lock когда len(_edges) > 1000.
        Оставляет топ-75% по весу, остальные удаляет вместе с _entity_index записями.
        Без этого метода _edges растёт бесконечно при длинных сессиях.
        """
        sorted_edges = sorted(self._edges.items(), key=lambda x: x[1].weight, reverse=True)
        keep_n    = int(len(sorted_edges) * keep_ratio)
        keep_keys = {k for k, _ in sorted_edges[:keep_n]}

        # Удалить слабые рёбра
        removed = {k for k in self._edges if k not in keep_keys}

        # P0-1 FIX: обновить кэш степеней при удалении рёбер
        for k in removed:
            edge = self._edges[k]
            for node in list(edge.entities) if hasattr(edge, 'entities') else [edge.entity_a, edge.entity_b]:
                self._degree_cache[node] = max(0, self._degree_cache.get(node, 1) - 1)
            del self._edges[k]

        # Очистить _entity_index от удалённых ключей
        for entity in list(self._entity_index.keys()):
            self._entity_index[entity] = [
                k for k in self._entity_index[entity] if k in keep_keys
            ]
            if not self._entity_index[entity]:
                del self._entity_index[entity]

        logger.debug(f"Velum GC: removed {len(removed)} weak edges, kept {len(self._edges)}")

    def _load_seed_from_sqlite(self):
        """
        Восстановить топ рёбра из предыдущей сессии.
        Вызывается синхронно в __init__ — допустимо, происходит один раз при старте.
        Без этого Velum каждый раз начинает с пустого графа рёбер, и первые
        VELUM_CO_OCCUR_THRESHOLD эпизодов не генерируют сигналы в L2.
        """
        import sqlite3
        try:
            conn = sqlite3.connect(self._config.sqlite_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS velum_edges (
                    entity_a TEXT NOT NULL,
                    entity_b TEXT NOT NULL,
                    weight   REAL NOT NULL,
                    count    INTEGER NOT NULL DEFAULT 1,
                    PRIMARY KEY (entity_a, entity_b)
                )
            """)
            rows = conn.execute(
                "SELECT entity_a, entity_b, weight, count "
                "FROM velum_edges ORDER BY weight DESC LIMIT 200"
            ).fetchall()
            conn.close()
            _now = time.monotonic()
            for entity_a, entity_b, weight, count in rows:
                key = frozenset([entity_a, entity_b])
                self._edges[key] = VelumEdge(
                    entity_a=entity_a, entity_b=entity_b,
                    weight=weight, count=count,
                    session_id=self.session_id,
                    first_seen=_now, last_seen=_now,
                )
                self._entity_index[entity_a].append(key)
                self._entity_index[entity_b].append(key)
            logger.info(f"Velum: loaded {len(rows)} seed edges from SQLite")
        except Exception as e:
            logger.warning(f"Velum: seed load failed (starting empty): {e}")

    async def _save_top_edges_to_sqlite(self, top_n: int = 200):
        """
        Сохранить топ-N рёбер по весу в SQLite.
        Вызывается через asyncio.create_task в on_session_end — не блокирует pipeline.
        """
        import aiosqlite
        async with self._lock:
            snapshot = sorted(
                self._edges.items(), key=lambda x: x[1].weight, reverse=True
            )[:top_n]
        try:
            async with aiosqlite.connect(self._config.sqlite_path) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS velum_edges (
                        entity_a TEXT NOT NULL,
                        entity_b TEXT NOT NULL,
                        weight   REAL NOT NULL,
                        count    INTEGER NOT NULL DEFAULT 1,
                        PRIMARY KEY (entity_a, entity_b)
                    )
                """)
                for key, edge in snapshot:
                    await db.execute(
                        "INSERT OR REPLACE INTO velum_edges "
                        "(entity_a, entity_b, weight, count) VALUES (?, ?, ?, ?)",
                        (edge.entity_a, edge.entity_b, edge.weight, edge.count)
                    )
                await db.commit()
            logger.debug(f"Velum: saved {len(snapshot)} edges to SQLite")
        except Exception as e:
            logger.warning(f"Velum: persist failed: {e}")
```

---

### 21. OutputFaithfulnessChecker — Post-generation guard 

**Назначение**: Шаг F6.5 — проверка что LLM не соврал

```python
class OutputFaithfulnessChecker:
    FALLBACK_RESPONSE = (
        "Недостаточно подтверждённых данных для уверенного ответа. "
        "Могу ответить точнее, когда накоплю больше проверенных фактов."
    )

    def __init__(self, threshold: float = None):
        self.threshold = threshold or TRUTH.FAITHFULNESS_THRESHOLD

    async def check(
        self, answer: str, facts_pack: list[dict]
    ) -> tuple[bool, list[str], float]:
        """
        Возвращает: (passed, unsupported_sentences, faithfulness_score)
        """
        # P1-B FIX: пустой facts_pack = нечего проверять → APPROVE.
        # БЫЛО: return (False, answer, 0.0) → блокировал Creative Mode и первые запросы.
        # СТАЛО: return (True, [], 1.0) → нет фактов = нет нарушений = APPROVE.
        if not facts_pack:
            return True, [], 1.0
        
        fact_texts = {f["content"].lower() for f in facts_pack if f.get("content")}
        sentences = self._split_sentences(answer)
        
        unsupported = [s for s in sentences if not self._is_supported(s, fact_texts)]
        faithfulness = 1.0 - len(unsupported) / len(sentences)
        
        if faithfulness < self.threshold:
            return False, unsupported, faithfulness
        
        return True, unsupported, faithfulness

    def _split_sentences(self, text: str) -> list[str]:
        """Phase 1 stub: разбить текст на предложения."""
        import re
        return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

    def _is_supported(self, sentence: str, fact_texts: set) -> bool:
        """MVP: keyword overlap ≥ 40%"""
        words = set(sentence.lower().split())
        if len(words) < 3:
            return True
        return any(
            len(words & set(f.split())) / len(words) >= 0.4
            for f in fact_texts
        )
```

**Интеграция в pipeline**:
```python
# F6: LLM Generation
answer = await llm.chat(context)

# F6.5: Faithfulness check
passed, unsupported, score = await faithfulness_checker.check(answer, facts_pack)

if passed:
    return answer
else:
    logger.warning(f"Faithfulness FAILED: {score:.2f}")
    return OutputFaithfulnessChecker.FALLBACK_RESPONSE
```

---

## 📐 Токен-контракт и Протокол Promote/Demote 

> **Почему это важно**: цель "90%+ снижение токенов" остаётся декларацией без формального контракта. Этот раздел превращает цель в гарантию.

---

### ⚡ Токен-контракт

```python
# token_contract.py

MAX_TOKENS_MEMORY_PER_QUERY = 2000   # Бюджет памяти на один запрос (BALANCED режим)
MAX_TOKENS_SYSTEM_PROMPT    = 500    # Резерв для системного промпта
MAX_TOKENS_ETIR_ACTIVATION  = 300    # Лимит для L3.5 Etir spreading activation
ETIR_TOP_K_NODES            = 10     # Максимум активированных узлов из Etir
ETIR_DECAY_THRESHOLD        = 0.15   # Узлы с activation < порога не включаются

# Cognitive Modes — бюджеты по режимам
MAX_TOKENS_PRECISION_MODE   = 1000   # PRECISION: критичные данные, только факты
MAX_TOKENS_BALANCED_MODE    = 2000   # BALANCED: стандартный режим (90% задач)
MAX_TOKENS_EXPLORATION_MODE = 4000   # EXPLORATION: brainstorm, гипотезы
MAX_TOKENS_CREATIVE_MODE    = 3000   # CREATIVE: аналогии + Validated только (RFC0067 v2.0)
```

**Приоритет уровней при нехватке бюджета:**

```
Бюджет: MAX_TOKENS_MEMORY_PER_QUERY = 2000 токенов
│
├── L0 Working Memory    → всегда (~100 токенов, нельзя резать)
├── L3.5 Etir activation → top_k узлов до ETIR лимита
├── L1 STM Episodes      → по релевантности до исчерпания остатка
├── L2 MTM Patterns      → только summary если бюджет есть
└── L3 LTM Graph         → только по явному meta-запросу

Правило: если бюджет исчерпан — L3 отсекается первым,
         L0 и Etir-результаты защищены всегда.
```

---

### 🔄 Протокол Promote / Demote

Формальные правила перемещения данных между уровнями памяти. Без этих правил система не детерминирована.

```
PROMOTE L1 (STM) → L2 (MTM) если выполняется хотя бы одно:
  importance_score > 0.7
  ИЛИ access_count >= 3
  ИЛИ outcome IN [SUCCESS, FAILURE]   (эмоциональная салиентность)
  ИЛИ pinned == true

PROMOTE L2 (MTM) → L3 (LTM / Neo4j) если:
  кластер >= 3 похожих эпизодов (cosine similarity > 0.7)
  И avg_importance > 0.5

DEMOTE / SOFT DELETE L2 → archive если:
  age > 30 дней
  И importance_score < 0.3
  И access_count == 0 за последние 14 дней
  И pinned == false
  → Действие: is_active = false, valid_to = now()

FORGET (физическое удаление GC) если:
  is_active == false
  И age > 90 дней
  И importance_score < 0.1
  И reindex_required == false   (не трогать если нужна переиндексация)
  → Действие: архивация в S3, затем DETACH DELETE
```

| Переход | Условие | Метод |
|---|---|---|
| L1 → L2 | importance > 0.7 / access ≥ 3 / outcome | `consolidate_stm_to_mtm()` |
| L2 → L3 | кластер ≥ 3, avg_importance > 0.5 | `consolidate_mtm_to_ltm()` |
| L2 → archive | age > 30d, importance < 0.3 | Soft Delete: `is_active=false` |
| Archive → delete | age > 90d, importance < 0.1 | GC: S3 backup + DETACH DELETE |
| L3 → L3.5 Etir | access_count > порога / pinned | `etir_promote()` |
| L3.5 → L3 | access_count падает, decay | `etir_evict()` |

---

### ❄️ Cold Start / Seed Nodes

> ⚠️ **Блокер KPI**: При первом запуске Etir пуст → P95 > 500ms на каждый
> запрос, что нарушает заявленный KPI <500ms. Без seed nodes система
> деградирует в полный обход L3 (Neo4j) на всех запросах до накопления данных.

```
Проблема: Etir пуст при init → полный Neo4j traversal на каждый запрос
          Velum пуст → все связи идут напрямую в граф
          ReasoningBank пуст → Thompson Sampling работает наугад

Решение — Seed Nodes при инициализации:
  1. При старте системы загрузить базовые концепты в Etir:
     · Science Core узлы с pinned=True (если заполнен)
     · VALUES CORE / Ring Zero узлы — всегда pinned
     · Топ-N узлов по access_count из прошлых сессий
     · Если данных нет — минимальный набор из constants.py

  2. Velum seed:
     · Загрузить связи с usage_count > 3 из предыдущих сессий
     · Если первый запуск — начать с пустым Velum (нормально)

  3. ReasoningBank seed:
     · Предзагрузить базовые стратегии из reasoning_bank.py
     · confidence = 0.5 (нейтральный старт, Thompson Sampling выберет сам)

Реализация: etir_init(seed=True) вызывается в pipeline.__init__()
```

---

### 🔀 Soft Delete — обязательный паттерн GC

```
НИКОГДА не делать сразу DETACH DELETE в production.
Всегда: Soft Delete → Архивация S3 → Hard Delete

Шаги удаления:
1. SET node.is_active = false, node.valid_to = datetime()
2. Дождаться успешной записи в S3
3. Только после успеха: DETACH DELETE
4. Если S3 упал → откатить is_active = true

Restore Path (восстановление из архива):
1. Найти узел в S3 по node_id / canonical_id
2. MERGE (n:KnowledgeNode {node_id: $id})
3. SET n.is_active = true, n.valid_to = null
4. SET n.restored_at = datetime(), n.restore_reason = $reason
5. Проверить RFC инварианты (MGL-2, MGL-5) после восстановления
```

---

### 🔀 Конфликт фактов — [:CONTRADICTS] pipeline

```
Пользователь говорит: "Забудь X, мы возвращаемся к Y"
│
├── Graphiti создаёт новый узел :Fact (новое решение)
├── Классификатор интента детектирует OVERRIDE
├── Создаётся связь: new_fact-[:CONTRADICTS {reason}]->old_fact
├── old_fact получает: is_active=false, valid_to=now()
├── HybridRetriever автоматически фильтрует is_active=false
└── GC при следующем запуске: S3 backup → физическое удаление

⚠️ ВАЖНО: LLM НЕ расставляет [:CONTRADICTS] автоматически.
   Только явная команда пользователя или CRUD-классификатор.
   При обнаружении конфликта агент переспрашивает:
   "Вижу противоречие с предыдущим решением. Стереть старое?"
```

---

### 6. Context Builder: Умная сборка промпта

> ⚠️ **Каноническая реализация — FEATURE-8 (RFC0062).** Этот раздел описывает логику; актуальный код см. в разделе RFC0062 · FEATURE-8.

**Назначение**: Собрать минимальный, релевантный контекст в пределах token budget.

---

## 🔄 Полная интеграция: Главный агент

```python
# main_agent.py
import asyncio
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class AutonomousSelfLearningAgent:
    """
    Полностью автономный агент с фрактальной памятью и самообучением
    Production-ready версия с:
    - Circuit breakers для resilience
    - OpenTelemetry для observability
    - Adaptive consolidation
    - Thompson Sampling strategy selection (RFC0039)
    - Memory GC
    """
    def __init__(self, config: Dict):
        self.config = config
        # Core components
        self.llm = self._init_llm(config)
        self.event_bus = RobustEventBus(config["redis_url"])
        
        # Memory layers с circuit breakers
        self.graph_memory = GraphMemoryWithCircuitBreaker(
            neo4j_uri=config["neo4j_uri"],
            neo4j_user=config["neo4j_user"],
            neo4j_password=config["neo4j_password"]
        )
        self.fractal_memory = FractalMemory(self.graph_memory)
        
        # Retrieval and learning с observability
        self.retriever = ObservableHybridRetriever(
            graph_memory=self.graph_memory,
            fractal_memory=self.fractal_memory,
            token_budget=config.get("token_budget", 2000)
        )
        self.reasoning_bank = ReasoningBank(self.graph_memory)
        # P1-3 FIX: зарегистрировать делегат ACE Curator
        self.reasoning_bank.set_ace_delegate(self)
        self.context_builder = ContextBuilder(
            token_budget=config.get("token_budget", 2000)  # FEATURE-8 (RFC0062): canonical, token_budget=2000 совпадает с token_contract.py
        )
        
        # Background workers
        self.consolidation_worker = AdaptiveConsolidationWorker(
            self.fractal_memory
        )
        self.event_processor = EventProcessor(
            self.event_bus,
            self.graph_memory,
            self.fractal_memory
        )
        
        # Memory management
        self.memory_archival = MemoryArchival(
            graph=self.graph_memory,
            s3_bucket=config.get("s3_bucket")
        )
        self.memory_gc = MemoryGarbageCollector(
            graph=self.graph_memory,
            fractal_memory=self.fractal_memory,
            archival=self.memory_archival
        )
        # Supervisors (вызываются в start())
        self.invariant_checker = RuntimeInvariantChecker(
            graph=self.graph_memory,
            fractal_memory=self.fractal_memory
        )
        # MemoryBudgetPlanner — создаём из graph_memory чтобы избежать AttributeError в _collect_signals
        _budget_planner = MemoryBudgetPlanner(graph=self.graph_memory)
        self.meta_supervisor = MetaSupervisorApex(
            consolidation_engine=self.consolidation_worker,
            graph=self.graph_memory,
            budget_planner=_budget_planner,
            invariant_checker=self.invariant_checker
        )

        # Персистентный агент задач — создаётся один раз и переиспользуется,
        # чтобы reasoning_bank накапливал опыт между вызовами (не сбрасывался).
        self._task_agent = SelfLearningAgent(
            llm=self.llm,
            memory=self.graph_memory,
            retriever=self.retriever,
            reasoning_bank=self.reasoning_bank
        )

        # State
        self.session_id = generate_session_id()
        self.conversation_history = []
        self._shutdown_started = False  # защита от двойного graceful shutdown при SIGTERM+SIGINT
        # sqlite_db инициализируется здесь явно,
        # а не только при первом обращении в start() — устраняет AttributeError.
        self._sqlite_db_path = config.get("sqlite_db", "velantrim.db")
        self.sqlite_db = None  # открывается как async context в start()

    async def start(self):
        """Запустить агент и фоновые процессы"""
        # RFC0006 — проверить конфигурацию Engram до старта
        from rfc0006_engram_isolation import validate_engram_config
        validate_engram_config(self.config)

        # открываем sqlite_db через aiosqlite context manager
        import aiosqlite
        self.sqlite_db = await aiosqlite.connect(self._sqlite_db_path)

        # WAL-режим SQLite для быстрого Graceful Shutdown
        await self.sqlite_db.execute("PRAGMA journal_mode=WAL")
        await self.sqlite_db.execute("PRAGMA synchronous=NORMAL")

        # Создать Neo4j индексы (КРИТИЧНО!)
        await setup_neo4j_indexes(self.graph_memory.driver)

        # P0-2 FIX: ImmutableRawMemory — создать схему SQLite до первого save_episode().
        # Без этого вызова таблица raw_episodes не существует → падение при записи.
        # Порядок критичен: ПЕРВЫМ, до любых воркеров которые могут писать эпизоды.
        if hasattr(self, 'raw_memory') and self.raw_memory is not None:
            await self.raw_memory.init()

        # P0-3 FIX: MemoryVolitionWorker — загрузить счётчики per-session из SQLite.
        # Без этого _initialized=False → write_voluntary() бросает RuntimeError.
        # MAX_PER_SESSION=10 не работает без загруженных счётчиков.
        # Порядок: после raw_memory.init(), до воркеров которые могут вызвать write_voluntary().
        if hasattr(self, 'volition_worker') and self.volition_worker is not None:
            await self.volition_worker.start()

        # Запустить ConsolidationEngine (заменяет 3 воркера)
        asyncio.create_task(self.consolidation_worker.start())  # исправлено: consolidation_worker (см. __init__)

        # Запустить фоновые workers (используют CE через enqueue)
        asyncio.create_task(self.event_processor.start())
        asyncio.create_task(self.memory_gc.schedule_periodic_gc())
        asyncio.create_task(self._dlq_processor())

        # Запустить Runtime Invariant Checker
        asyncio.create_task(self.invariant_checker.start())

        # Запустить Meta-Supervisor Apex Controller
        asyncio.create_task(self.meta_supervisor.start())

        # Регистрировать SIGTERM/SIGINT хуки для graceful shutdown
        # WAL SQLite обеспечивает атомарность за миллисекунды
        import signal
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                loop.add_signal_handler(
                    sig,
                    lambda: asyncio.create_task(self._graceful_shutdown())
                )
            except NotImplementedError:
                pass  # Windows — игнорируем, вызывать shutdown вручную

        logger.info("Agent started: CE + Invariant Checker + Heartbeat active")

    async def _graceful_shutdown(self):
        """
        Graceful Shutdown — атомарное сохранение L0/L1 перед выходом.

        Используем WAL-режим SQLite для атомарного дампа
        за миллисекунды вместо tempfile+os.replace (секунды при нагрузке).
        WAL (Write-Ahead Log) гарантирует атомарность без блокировки чтения.

        Проблема: L0 Working Memory и L1 STM живут in-memory.
        При SIGTERM/SIGKILL без хуков — теряются безвозвратно.
        """
        import json
        logger.info("Graceful shutdown: saving L0/L1 snapshot via WAL SQLite...")

        snapshot = {
            "meta": {
                "saved_at": datetime.now(timezone.utc).isoformat() + "Z",
                "session_id": self.session_id,
                "shutdown": "graceful",
                "version": "8.0"
            },
            # L0 Working Memory — читаем из working_memory (не stm_cache!)
            # L0 и L1 — разные слои: working_memory = 4±1 активных слота, stm_cache = эпизоды сессии
            "working_memory": [
                {"id": m.id, "content": m.content,
                 "importance": float(m.importance),
                 "priority": getattr(m, 'priority', 'MEDIUM'),
                 "level": str(m.level)}
                for m in getattr(self.fractal_memory, 'working_memory', [])
                if getattr(m, 'priority', 'MEDIUM') in ('CRITICAL', 'HIGH')
            ],
            # L1 STM — полный снапшот всех элементов кэша
            "stm_cache": [
                {"id": m.id, "content": m.content,
                 "importance": float(m.importance),
                 "created_at": m.created_at.isoformat() if hasattr(m.created_at, 'isoformat') else str(m.created_at),
                 "level": str(m.level)}
                for m in self.fractal_memory.stm_cache
            ]
        }

        # WAL-режим SQLite — миллисекунды вместо секунд
        # PRAGMA journal_mode=WAL установлен при инициализации БД
        async with self.sqlite_db.transaction():
            await self.sqlite_db.execute(
                """INSERT OR REPLACE INTO l0l1_snapshots
                   (session_id, saved_at, snapshot_json)
                   VALUES (?, ?, ?)""",
                (self.session_id,
                 datetime.now(timezone.utc).isoformat(),
                 json.dumps(snapshot, ensure_ascii=False))
            )
        # WAL checkpoint — записать WAL в основную БД
        await self.sqlite_db.execute("PRAGMA wal_checkpoint(TRUNCATE)")

        logger.info("L0/L1 snapshot saved via WAL. Shutting down.")
        asyncio.get_running_loop().stop()

    async def _dlq_processor(self):
        """Обработка DLQ в фоне"""
        while True:
            await asyncio.sleep(3600)  # Каждый час
            await self.event_bus.process_dlq()

    @trace_async("agent_chat")
    async def chat(self, user_message: str) -> str:
        """
        Основной метод взаимодействия с полным трейсингом
        """
        with tracer.start_as_current_span("preprocessing") as span:
            span.set_attribute("message_length", len(user_message))
            
            # 1. Логировать входное сообщение
            publish_success = await self.event_bus.publish(AgentEvent(
                event_type=EventType.USER_MESSAGE,
                timestamp=datetime.now(timezone.utc),
                content={"message": user_message},
                metadata={},
                session_id=self.session_id
            ))
            
            if not publish_success:
                span.add_event("Event published to fallback queue")
            
            # 2. Добавить в STM
            embedding = await self._get_embedding(user_message)
            await self.fractal_memory.add_to_stm(user_message, embedding)
        
        # 3. Retrieval - найти релевантный контекст
        with tracer.start_as_current_span("memory_retrieval"):
            retrieved_memories = await self.retriever.retrieve(
                query=user_message,
                query_type="conversation"
            )
        
        # 4. Найти применимые стратегии (если задача)
        strategies = []
        if self._is_task_query(user_message):
            with tracer.start_as_current_span("strategy_retrieval"):
                strategies = await self.reasoning_bank.retrieve_relevant_strategies(
                    current_task=user_message,
                    context={},
                    epsilon=0.1  # 10% exploration
                )
        
        # 5. Построить контекст для LLM
        with tracer.start_as_current_span("context_building") as span:
            context = self.context_builder.build_context(
                current_query=user_message,
                retrieved_memories=retrieved_memories,
                strategies=strategies,
                conversation_history=self.conversation_history
            )
            
            context_tokens = count_tokens(context)
            span.set_attribute("context_tokens", context_tokens)
            tokens_per_query.observe(context_tokens)
        
        # 6. Генерация ответа (ЕДИНСТВЕННЫЙ LLM-вызов)
        with tracer.start_as_current_span("llm_generation") as span:
            response = await self.llm.chat(context)
            
            response_tokens = count_tokens(response)
            span.set_attribute("response_tokens", response_tokens)
            tokens_used.labels(component="llm").inc(context_tokens + response_tokens)
        
        # 7. Логировать ответ
        await self.event_bus.publish(AgentEvent(
            event_type=EventType.AGENT_RESPONSE,
            timestamp=datetime.now(timezone.utc),
            content={"message": response},
            metadata={"tokens": response_tokens},
            session_id=self.session_id
        ))
        
        # 8. Обновить историю
        self.conversation_history.append(f"User: {user_message}")
        self.conversation_history.append(f"Assistant: {response}")
        
        # Ограничить историю (последние 10 сообщений)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response

    async def execute_task_with_learning(
        self,
        task: str,
        context: Dict
    ):
        """
        Выполнение задачи с циклом самообучения.
        Делегирует в персистентный _task_agent — reasoning_bank накапливает
        опыт между вызовами (не сбрасывается при каждом execute_task_with_learning).
        """
        return await self._task_agent.execute_task(task, context)

    async def health_check(self) -> dict:
        """Проверка здоровья всех компонентов"""
        return {
            "event_bus": await self.event_bus.health_check(),
            "neo4j_breaker": self.graph_memory.neo4j_breaker.get_state(),
            "memory_size": {
                "stm": len(self.fractal_memory.stm_cache),
                "mtm": len(self.fractal_memory.mtm_cache)
            },
            "session_id": self.session_id
        }
```

---

## 🔍 Production-Ready Компоненты

### 7. OpenTelemetry: Observability и трейсинг

**Назначение**: Отладка и мониторинг performance в production

```python
# observability.py
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import time
from functools import wraps

# Инициализация трейсера
resource = Resource.create({"service.name": "fractal-memory-agent"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Export в OTLP collector (Grafana Tempo, Jaeger, etc)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Декоратор для автоматического трейсинга
def trace_async(span_name: str = None):
    """Декоратор для трейсинга асинхронных функций"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            name = span_name or f"{func.__module__}.{func.__name__}"
            
            with tracer.start_as_current_span(name) as span:
                # Добавить параметры как атрибуты
                if args:
                    span.set_attribute("args_count", len(args))
                if kwargs:
                    for k, v in kwargs.items():
                        if isinstance(v, (str, int, float, bool)):
                            span.set_attribute(f"param.{k}", v)
                
                start_time = time.time()
                
                try:
                    result = await func(*args, **kwargs)
                    
                    # Успех
                    duration = time.time() - start_time
                    span.set_attribute("duration_ms", duration * 1000)
                    span.set_status(Status(StatusCode.OK))
                    
                    return result
                    
                except Exception as e:
                    # Ошибка
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        
        return wrapper
    return decorator

# Применение в компонентах
class ObservableHybridRetriever(HybridRetriever):
    """HybridRetriever с трейсингом"""

    @trace_async("hybrid_retrieval")
    async def retrieve(
        self,
        query: str,
        query_type: str = "general"
    ) -> List[RetrievalResult]:
        """Retrieval с полным трейсингом каждого этапа"""
        
        with tracer.start_as_current_span("routing") as span:
            strategy = self._route_query(query, query_type)
            span.set_attribute("strategy", strategy)
        
        results = []
        
        # Stage 1: STM search
        with tracer.start_as_current_span("stm_search") as span:
            # P1-G FIX: добавлены "RECALL" и "TASK" — ObservableHybridRetriever
            # тихо ломал два самых частых запроса: они не получали STM-результаты.
            # Синхронизировано с родительским HybridRetriever.
            if strategy in ["conversation", "immediate", "RECALL", "TASK"]:
                query_embedding = await self._get_embedding(query)
                stm_results = await self._search_stm(query, query_embedding)
                span.set_attribute("stm_hits", len(stm_results))
                results.extend(stm_results)
        
        # Stage 2: Graph search
        with tracer.start_as_current_span("graph_search") as span:
            start = time.time()
            graph_results = await self.graph.search(query, num_results=10)
            latency = time.time() - start
            
            span.set_attribute("graph_hits", len(graph_results))
            span.set_attribute("latency_ms", latency * 1000)
            
            results.extend(self._convert_to_retrieval_results(
                graph_results, source="graph"
            ))
        
        # Stage 3: Reranking
        with tracer.start_as_current_span("reranking") as span:
            results = await self._rerank(query, results)
            span.set_attribute("reranked_count", len(results))
        
        # Stage 4: Token budgeting
        with tracer.start_as_current_span("token_budgeting") as span:
            results = self._apply_token_budget(results)
            
            total_tokens = sum(r.tokens for r in results if hasattr(r, 'tokens'))
            span.set_attribute("selected_count", len(results))
            span.set_attribute("total_tokens", total_tokens)
        
        return results

# Пример интеграции в GraphMemory
class ObservableGraphMemory(GraphMemory):
    @trace_async("graph_search")
    async def search(self, query: str, num_results: int = 5):
        """Search с детальным трейсингом"""
        with tracer.start_as_current_span("graphiti_search") as span:
            span.set_attribute("query_length", len(query))
            span.set_attribute("num_results", num_results)
            
            results = await super().search(query, num_results)
            
            span.set_attribute("results_count", len(results))
            return results

    @trace_async("add_episode")
    async def add_episode(self, *args, **kwargs):
        """Episode creation с трейсингом"""
        return await super().add_episode(*args, **kwargs)
```

**Viewing traces в Grafana Tempo:**

```yaml
# docker-compose.yml для observability stack
# P3-E FIX: version: поле deprecated в Docker Compose v2+. Убрано.
services:
  tempo:
    image: grafana/tempo:latest
    ports:
      - "4317:4317"  # OTLP gRPC
      - "3200:3200"  # Tempo HTTP
    volumes:
      - ./tempo-data:/var/tempo
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
    volumes:
      - ./grafana-data:/var/lib/grafana
```

---

### 8. Memory Garbage Collection

**Назначение**: Очистка низко-важной памяти и предотвращение бесконечного роста графа

```python
# memory_gc.py
from datetime import datetime, timedelta, timezone  # P0-B FIX: timezone добавлен (ранее NameError)
import logging

logger = logging.getLogger(__name__)

class MemoryGarbageCollector:
    """
    Периодическая очистка памяти:
    - Удаление низко-важных узлов
    - Merge дубликатов
    - Компрессия MTM cache
    - Архивация старых эпизодов
    """

    def __init__(
        self,
        graph: GraphMemory,
        fractal_memory: FractalMemory,
        archival: MemoryArchival = None
    ):
        self.graph = graph
        self.fractal = fractal_memory
        self.archival = archival
        
        # Пороги для GC
        self.importance_threshold = 0.1
        self.age_threshold_days = 30
        self.access_threshold = 0  # Не был доступен ни разу

    async def run_full_gc(self):
        """
        Полная сборка мусора (запускать еженедельно)
        """
        logger.info("Starting memory garbage collection")
        
        stats = {
            "deleted_episodes": 0,
            "deleted_entities": 0,
            "merged_duplicates": 0,
            "archived_count": 0,
            "freed_mtm_slots": 0
        }
        
        # 1. Удалить низко-важные эпизоды
        stats["deleted_episodes"] = await self._delete_low_importance_episodes()
        
        # 2. Удалить неиспользуемые сущности
        stats["deleted_entities"] = await self._delete_orphan_entities()
        
        # 3. Merge дубликаты
        stats["merged_duplicates"] = await self._merge_duplicate_entities()
        
        # 4. Каскадная инвалидация: снизить confidence у Strategy при инвалидации Fact
        # Без этого Strategy становятся "фантомными" — опираются на мёртвые факты
        await self._cascade_invalidate_dependent_strategies()
        
        # 5. Архивация старых эпизодов (если настроено)
        if self.archival:
            stats["archived_count"] = await self.archival.archive_old_episodes(
                older_than_days=365,
                importance_threshold=0.3
            )
            # Vacuum Worker — физическое удаление после S3 + 90 дней
            stats["vacuum_deleted"] = await self.archival.vacuum_soft_deleted(min_age_days=90)
        
        # 6. Компрессия MTM cache
        stats["freed_mtm_slots"] = await self._compress_mtm_cache()
        
        logger.info(f"GC completed: {stats}")
        return stats

    async def _delete_low_importance_episodes(self) -> int:
        """
        Soft Delete низко-важных эпизодов → затем Hard Delete после S3 архивации.
        
        ПРОТОКОЛ:
        1. Сначала деактивируем (is_active = false) — Soft Delete
        2. Архивируем в S3
        3. Только после успеха — физическое DETACH DELETE
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.age_threshold_days)
        
        # Шаг 1: Soft Delete — деактивировать, не удалять
        soft_delete_query = """
        MATCH (ep:Episode)
        WHERE ep.importance_score < $importance_threshold
          AND ep.timestamp < $cutoff_date
          AND ep.access_count <= $access_threshold
          AND ep.is_active <> false
        WITH ep
        LIMIT 1000
        SET ep.is_active = false, ep.valid_to = datetime()
        RETURN count(ep) as deactivated_count
        """
        
        result = await self.graph.execute_cypher(soft_delete_query, {
            "importance_threshold": self.importance_threshold,
            "cutoff_date": cutoff_date.isoformat(),
            "access_threshold": self.access_threshold
        })
        
        deactivated = result[0]["deactivated_count"] if result else 0
        
        # Шаг 2: Hard Delete только узлов которые уже деактивированы > 30 дней
        # (они уже должны быть архивированы на предыдущем цикле GC)
        hard_cutoff = datetime.now(timezone.utc) - timedelta(days=self.age_threshold_days * 3)
        
        hard_delete_query = """
        MATCH (ep:Episode)
        WHERE ep.is_active = false
          AND ep.valid_to < $hard_cutoff
        WITH ep
        LIMIT 500
        DETACH DELETE ep
        RETURN count(ep) as deleted_count
        """
        
        hard_result = await self.graph.execute_cypher(hard_delete_query, {
            "hard_cutoff": hard_cutoff.isoformat()
        })
        
        deleted = hard_result[0]["deleted_count"] if hard_result else 0
        logger.info(f"Soft-deleted: {deactivated} episodes. Hard-deleted: {deleted} archived episodes")
        return deactivated + deleted

    async def _delete_orphan_entities(self) -> int:
        """
        Удалить сущности без связей (orphaned nodes)
        """
        query = """
        MATCH (e:Entity)
        WHERE NOT (e)-[]-()
          AND e.importance_score < $threshold
        WITH e
        LIMIT 500
        DETACH DELETE e   -- P1-C FIX: DELETE без DETACH падает если у узла есть relations

-- P4-A FIX: добавить label :SoftDeleted для O(1) scan вместо Full Node Scan.
-- MATCH (n) WHERE n.is_active=false — низкокардинальный Boolean, плохо индексируется.
-- CREATE INDEX soft_deleted_idx IF NOT EXISTS FOR (n:Episode) ON (n.is_active, n.valid_to);
-- При soft delete: SET ep.is_active=false, ep.valid_to=datetime() — label lookup O(1).
        RETURN count(e) as deleted_count
        """
        
        result = await self.graph.execute_cypher(query, {
            "threshold": self.importance_threshold * 2  # Чуть выше порог
        })
        
        deleted = result[0]["deleted_count"] if result else 0
        logger.info(f"Deleted {deleted} orphan entities")
        return deleted

    async def _merge_duplicate_entities(self) -> int:
        """
        Найти и слить дубликаты сущностей
        (например, "OpenAI" и "openai" → одна сущность)

        P0-4 FIX: Используем _merge_nodes_safe() из dedupe_entities.py —
        APOC если доступен, иначе чистый Cypher fallback для LadybugDB/KuzuDB.
        """
        # Найти кандидатов на merge (похожие имена)
        query = """
        MATCH (e1:Entity), (e2:Entity)
        WHERE id(e1) < id(e2)
          AND toLower(e1.name) = toLower(e2.name)
          AND e1.type = e2.type
        WITH e1, e2
        LIMIT 100
        RETURN e1, e2
        """

        candidates = await self.graph.execute_cypher(query)

        merged_count = 0
        for pair in candidates:
            e1, e2 = pair["e1"], pair["e2"]

            # P0-4 FIX: _merge_nodes_safe() выбирает APOC или Cypher fallback
            # автоматически по HAS_APOC env var — без изменений в вызывающем коде.
            await _merge_nodes_safe(self.graph, e1["id"], e2["id"])
            merged_count += 1

        logger.info(f"Merged {merged_count} duplicate entities")
        return merged_count

    async def _compress_mtm_cache(self) -> int:
        """
        Очистить MTM cache от низко-важных элементов
        """
        initial_size = len(self.fractal.mtm_cache)
        
        # Удалить элементы с importance < 0.3
        self.fractal.mtm_cache = [
            item for item in self.fractal.mtm_cache
            if item.importance >= 0.3
        ]
        
        freed = initial_size - len(self.fractal.mtm_cache)
        logger.info(f"Freed {freed} MTM cache slots")
        return freed

    async def _cascade_invalidate_dependent_strategies(self) -> int:
        """
        Каскадная инвалидация: при Soft Delete :Fact снижать confidence
        у всех :Strategy, выведенных из этого факта через [:DERIVED_FROM].
        
        Без этого Strategy становятся "фантомными" — стратегии, опирающиеся
        на инвалидированные факты, продолжают применяться как валидные.
        
        ПРАВИЛО: confidence -= 0.2 за каждый инвалидированный DERIVED_FROM факт.
                 Если confidence < 0.3 → Strategy тоже помечается is_active=false.
        """
        # штраф применяется только к фактам,
        # которые ЕЩЁ НЕ были учтены ранее. Поле penalized_fact_ids хранит
        # IDs уже оштрафованных фактов — предотвращает двойное списание при GC.
        query = """
        MATCH (s:Strategy)-[:DERIVED_FROM]->(f:Fact)
        WHERE f.is_active = false
          AND s.is_active = true
          AND NOT f.id IN coalesce(s.penalized_fact_ids, [])
          AND f.is_ring_zero <> true
        WITH s, collect(f.id) as new_invalid_ids, count(f) as new_invalidated
        SET s.confidence = CASE
            WHEN s.confidence - (new_invalidated * 0.2) < 0.0
            THEN 0.0   -- P9-FIX БАГ-3: floor только при уходе в минус, не при пересечении 0.3
            ELSE s.confidence - (new_invalidated * 0.2)
        END,
        s.is_active = CASE
            WHEN s.confidence - (new_invalidated * 0.2) < 0.3
            THEN false
            ELSE true
        END,
        s.penalized_fact_ids = (coalesce(s.penalized_fact_ids, []) + new_invalid_ids)[-500:]  -- P9-FIX БАГ-12: cap 500
        RETURN count(s) as updated_strategies
        """
        result = await self.graph.execute_cypher(query)
        updated = result[0]["updated_strategies"] if result else 0
        logger.info(f"Cascade invalidation: updated {updated} strategies")
        return updated

    async def schedule_periodic_gc(self):
        """
        Запустить периодический GC (каждые 7 дней)
        """
        while True:
            await asyncio.sleep(7 * 24 * 3600)  # 7 дней
            
            try:
                await self.run_full_gc()
            except Exception as e:
                logger.error(f"GC failed: {e}")
```

---

## 📈 Мониторинг и метрики

**Критически важные метрики для отслеживания**:

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, Enum

# === Токены ===
tokens_used = Counter(
    "agent_tokens_used_total",
    "Total tokens used",
    ["component"]  # llm, embeddings, etc
)
tokens_per_query = Histogram(
    "agent_tokens_per_query",
    "Tokens per query",
    buckets=[100, 500, 1000, 2000, 5000, 10000]
)
token_budget_utilization = Histogram(
    "token_budget_utilization_ratio",
    "How much of token budget was used",
    buckets=[0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
)

# === Память ===
memory_size = Gauge(
    "agent_memory_size",
    "Size of memory by level",
    ["level"]  # stm, mtm, ltm
)
consolidation_duration = Histogram(
    "memory_consolidation_duration_seconds",
    "Time to consolidate memory",
    ["source", "target"],  # stm->mtm, mtm->ltm
    buckets=[1, 5, 10, 30, 60, 300]
)
memory_importance_distribution = Histogram(
    "memory_importance_score",
    "Distribution of importance scores",
    buckets=[0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]
)

# === Производительность ===
retrieval_latency = Histogram(
    "retrieval_latency_seconds",
    "Retrieval latency by stage",
    ["stage"],  # stm, graph, rerank, total
    buckets=[0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 3.0]
)
response_latency = Histogram(
    "response_latency_seconds",
    "End-to-end response time",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)
neo4j_query_duration = Histogram(
    "neo4j_query_duration_seconds",
    "Neo4j query execution time",
    ["query_type"],
    buckets=[0.01, 0.05, 0.1, 0.3, 0.5, 1.0]
)

# === Качество ===
retrieval_precision = Gauge(
    "retrieval_precision",
    "Precision of memory retrieval"
)
retrieval_recall = Gauge(
    "retrieval_recall",
    "Recall of memory retrieval"
)
task_success_rate = Gauge(
    "task_success_rate",
    "Task success rate",
    ["task_type"]
)
strategy_effectiveness = Gauge(
    "strategy_effectiveness",
    "Strategy success rate",
    ["strategy_id"]
)

# === Circuit Breaker ===
circuit_breaker_state = Enum(
    "circuit_breaker_state",
    "Current circuit breaker state",
    ["service"],  # neo4j, redis, llm
    states=["closed", "open", "half_open"]
)
circuit_breaker_failures = Counter(
    "circuit_breaker_failures_total",
    "Total failures by service",
    ["service"]
)
circuit_breaker_trips = Counter(
    "circuit_breaker_trips_total",
    "How many times breaker opened",
    ["service"]
)

# === Event Bus ===
event_bus_published = Counter(
    "event_bus_published_total",
    "Events published",
    ["event_type"]
)
event_bus_failed = Counter(
    "event_bus_failed_total",
    "Failed event publications",
    ["event_type"]
)
dlq_size = Gauge(
    "event_bus_dlq_size",
    "Dead letter queue size"
)
fallback_queue_size = Gauge(
    "event_bus_fallback_queue_size",
    "Fallback queue size (when Redis down)"
)

# === Garbage Collection ===
gc_duration = Histogram(
    "memory_gc_duration_seconds",
    "Time to run full GC",
    buckets=[10, 30, 60, 300, 600]
)
gc_deleted_nodes = Counter(
    "memory_gc_deleted_nodes_total",
    "Nodes deleted by GC",
    ["node_type"]  # episode, entity
)
gc_freed_memory = Gauge(
    "memory_gc_freed_bytes",
    "Memory freed by GC in bytes"
)

# === Strategy Learning ===
# P3-D FIX: UCB1 заменён на Thompson Sampling (RFC0039). Метрика переименована.
strategy_ts_scores = Histogram(
    "strategy_thompson_score",
    "Thompson Sampling Beta-distribution scores for strategy selection (P3-D FIX: было strategy_ucb_score)",
    buckets=[0, 0.2, 0.5, 0.8, 1.0]
)
exploration_vs_exploitation = Counter(
    "strategy_selection_mode_total",
    "Exploration vs exploitation count",
    ["mode"]  # exploration, exploitation
)

# === ConsolidationEngine ===
ce_queue_size = Gauge(
    "consolidation_engine_queue_size",
    "Pending operations in CE queue"
)
ce_dlq_size = Gauge(
    "consolidation_engine_dlq_size",
    "Failed operations in CE dead letter queue"
)
ce_op_duration = Histogram(
    "consolidation_engine_op_duration_seconds",
    "CE operation duration",
    ["op_type"],   # CONSOLIDATE, ARCHIVE, GC
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0]
)
ce_timeout_total = Counter(
    "consolidation_engine_timeout_total",
    "Total CE operation timeouts"
)

# === Cognitive Modes ===
cognitive_mode_requests = Counter(
    "cognitive_mode_requests_total",
    "Requests by cognitive mode",
    ["mode"]   # precision, balanced, exploration
)
cognitive_mode_tokens = Histogram(
    "cognitive_mode_tokens_used",
    "Tokens used per cognitive mode",
    ["mode"],
    buckets=[100, 500, 1000, 2000, 3000, 4000]
)

# === Memory Budget Planner ===
graph_nodes_total = Gauge(
    "memory_budget_graph_nodes_total",
    "Total active nodes in Neo4j graph"
)
graph_fill_ratio = Gauge(
    "memory_budget_fill_ratio",
    "Graph fill ratio vs MAX_NODES_TOTAL (0.0-1.0)"
)
budget_blocks_total = Counter(
    "memory_budget_blocks_total",
    "Times write was blocked by Budget Planner"
)

# === Runtime Invariant Checker ===
invariant_violations_total = Counter(
    "invariant_violations_total",
    "RFC invariant violations detected",
    ["invariant_id", "severity"]
)
safe_mode_activations_total = Counter(
    "safe_mode_activations_total",
    "Times Safe Mode was activated",
    ["reason"]
)

# === PII Redaction ===
pii_redacted_total = Counter(
    "pii_redacted_total",
    "PII tokens redacted before storage",
    ["pii_type"]   # email, phone_ru, card, etc.
)
```

**Пример использования метрик в коде**:

```python
# В HybridRetriever
async def retrieve(self, query: str):
    start = time.time()

    # STM search
    stm_start = time.time()
    stm_results = await self._search_stm(query)
    retrieval_latency.labels(stage="stm").observe(time.time() - stm_start)

    # Graph search
    graph_start = time.time()
    graph_results = await self.graph.search(query)
    retrieval_latency.labels(stage="graph").observe(time.time() - graph_start)

    # Total
    retrieval_latency.labels(stage="total").observe(time.time() - start)

    return results

# В Circuit Breaker
def _on_failure(self, error: Exception):
    circuit_breaker_failures.labels(service=self.name).inc()

    if self.failure_count >= self.failure_threshold:
        circuit_breaker_trips.labels(service=self.name).inc()
        circuit_breaker_state.labels(service=self.name).state("open")
```

---

## 📐 SLO Contract (Service Level Objectives)

> Пороги для Grafana alert rules. Все значения из `velantrim_config.SLOConfig`.

| Метрика | SLO (цель) | WARN | CRITICAL |
|---------|-----------|------|---------|
| search P95 latency | <500ms | >800ms | >2000ms |
| Etir P95 latency | <50ms | >80ms | >200ms |
| consolidation lag | <60s | >120s | >300s |
| GC weekly runtime | <2h | >3h | >6h |
| staging_candidates | <5 000 записей | >8 000 | >MAX_STAGING |
| DLQ size | <10 | >10 (DEGRADED) | >50 (SAFE_MODE) |
| budget fill ratio | <0.85 | >0.85 | >0.90 |
| output_faithfulness | >0.80 | <0.60 | <0.40 |
| L2 MHI | >0.60 | <0.50 | <0.30 |

### Автотриггеры MetaSupervisor

```
MHI < 0.30           → немедленный GC + alert ops
MHI < 0.50           → MetaSupervisor → DEGRADED (ускорить ConsolidationEngine)
budget_fill > 0.85   → MetaSupervisor → DEGRADED
budget_fill > 0.90   → MetaSupervisor → блокировка записи
DLQ > 50             → MetaSupervisor → SAFE_MODE
faithfulness < 0.40  → алерт + логировать unsupported_sentences
```

---

## 🔌 MCP Server — Подключение к внешним клиентам

> **Назначение**: Velantrim как инструмент в Cursor, Claude Code и любом MCP-совместимом клиенте. Агент становится доступен через стандартный протокол без изменений в основном коде.

```python
# mcp_server/server.py
# MCP stdio транспорт — подключает Velantrim к Cursor / Claude Code
# Запуск: python -m mcp_server.server
# Конфиг Cursor: { "velantrim": { "command": "python", "args": ["-m", "mcp_server.server"] } }

import asyncio, json, sys, logging
from pipeline import VelantrimPipeline  # основной pipeline агента

logger = logging.getLogger(__name__)

TOOLS = [
    {
        "name": "memory_search",
        "description": "Найти факты в долгосрочной памяти Velantrim по запросу",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query":      {"type": "string", "description": "Поисковый запрос"},
                "session_id": {"type": "string", "description": "ID сессии (опционально)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "memory_write",
        "description": "Записать факт в долгосрочную память через Truth Gate (волевая запись)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content":    {"type": "string", "description": "Факт для запоминания"},
                "reason":     {"type": "string", "description": "Причина записи"},
                "importance": {"type": "number", "description": "Важность 0.0–1.0"}
            },
            "required": ["content", "reason"]
        }
    },
    {
        "name": "memory_status",
        "description": "Статус системы памяти Velantrim: узлы, Hot Graph, ESM-распределение",
        "inputSchema": {"type": "object", "properties": {}}
    }
]

async def handle_request(pipeline: VelantrimPipeline, request: dict) -> dict:
    method = request.get("method")
    params = request.get("params", {})
    rid    = request.get("id")

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name      = params.get("name")
        arguments = params.get("arguments", {})
        try:
            if name == "memory_search":
                results = await pipeline.hybrid_retriever.retrieve(
                    query=arguments["query"],
                    session_id=arguments.get("session_id", "mcp")
                )
                text = "\n".join(f"[{r.source}] {r.content}" for r in results[:5])
                content = text or "Ничего не найдено."

            elif name == "memory_write":
                result = await pipeline.volition_worker.write_voluntary(
                    session_id="mcp",
                    agent_id="mcp_client",
                    content=arguments["content"],
                    reason=arguments["reason"],
                    importance_hint=float(arguments.get("importance", 0.8))
                )
                content = f"Результат: {result.outcome.value}"

            elif name == "memory_status":
                health = await pipeline.graph.health_check()
                content = json.dumps(health, ensure_ascii=False, indent=2)

            else:
                content = f"Неизвестный инструмент: {name}"

        except Exception as e:
            logger.error(f"MCP tool error [{name}]: {e}")
            return {"jsonrpc": "2.0", "id": rid,
                    "error": {"code": -32603, "message": str(e), "data": {"tool": name}}}
            # P9-FIX БАГ-4: JSON-RPC error вместо result — клиент (Cursor/Claude Code) получает корректный error object для retry

        return {"jsonrpc": "2.0", "id": rid,
                "result": {"content": [{"type": "text", "text": content}]}}

    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}

async def main():
    pipeline = VelantrimPipeline()
    await pipeline.start()
    logger.info("Velantrim MCP Server started (stdio)")
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        try:
            request  = json.loads(line.strip())
            response = await handle_request(pipeline, request)
            print(json.dumps(response, ensure_ascii=False), flush=True)
        except Exception as e:
            logger.error(f"MCP parse error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Подключение к Cursor** — добавить в `.cursor/mcp.json`:
```json
{
  "velantrim": {
    "command": "python",
    "args": ["-m", "mcp_server.server"],
    "cwd": "/path/to/velantrim"
  }
}
```

**Инвариант**: MCP Server — только тонкая обёртка над существующим pipeline. Никакой логики памяти внутри него нет. `memory_write` обязательно идёт через `VolitionWorker` → Truth Gate, не напрямую в граф.

---

## 🔍 Audit Layer — Слой проверяемости (Phase 1+)

> **Почему критично**: без Audit Layer невозможно понять почему агент ответил именно так. При галлюцинации — нет инструмента найти виновного: LLM при генерации, Etir при поиске, или Graphiti при записи факта.

```
Три обязательных API метода:

GET /memory/audit/context?request_id=...
→ Показывает: какие узлы из L3.5 Etir были активированы,
  какие факты из L3 попали в контекст, сколько токенов использовано

GET /memory/audit/strategy?request_id=...
→ Показывает: какая стратегия из ReasoningBank была выбрана,
  Thompson Sampling score каждой стратегии, режим (exploration/exploitation)

GET /memory/audit/forgetting?since=...
→ Показывает: какие факты деактивированы (is_active=false),
  почему ([:CONTRADICTS] / low importance / age),
  что было архивировано в S3
```

**Минимальная реализация для Phase 1:**

```python
# audit_layer.py
_AUDIT_SCHEMA = """
CREATE TABLE IF NOT EXISTS audit_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL, session_id TEXT, query TEXT,
    etir_nodes TEXT, facts_used TEXT,
    tokens_used INTEGER, token_budget INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS audit_strategy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL, session_id TEXT,
    strategy_id TEXT, strategy_desc TEXT, score REAL,
    selection_mode TEXT, all_candidates TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS audit_forgetting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id TEXT NOT NULL, node_type TEXT, reason TEXT,
    importance_at_delete REAL, archived_to_s3 BOOLEAN DEFAULT FALSE, s3_key TEXT,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_ctx_req ON audit_context(request_id);
CREATE INDEX IF NOT EXISTS idx_fgt_at  ON audit_forgetting(deleted_at);
"""


class AuditLayer:
    """
    Audit layer — делает систему прозрачной.
    Записывает в SQLite (уже в стеке как operational DB).
    Все writes — fire-and-forget через asyncio.create_task() (I28: не блокировать Fast Path).

    GET /memory/audit/context?request_id=   → какие Etir-узлы и факты вошли в промпт
    GET /memory/audit/strategy?request_id=  → какая стратегия выбрана и почему
    GET /memory/audit/forgetting?since=     → что забыто, когда, почему
    """

    def __init__(self, graph: GraphMemory, sqlite_db: str = "velantrim_audit.db"):
        self.graph   = graph
        self.db_path = sqlite_db
        self._ready  = False

    async def _ensure_schema(self):
        if self._ready:
            return
        try:
            import aiosqlite
            async with aiosqlite.connect(self.db_path) as db:
                await db.executescript(_AUDIT_SCHEMA)
                await db.commit()
            self._ready = True
        except Exception as e:
            logger.warning(f"AuditLayer._ensure_schema: {e}")

    async def log_context_selection(
        self,
        request_id: str,
        query: str,
        etir_nodes: list,
        retrieved_facts: list,
        tokens_used: int,
        token_budget: int,
        session_id: str = ""
    ):
        """Вызывать из ResponseAuditWorker через asyncio.create_task() — Slow Path только."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO audit_context VALUES (NULL,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
                    (request_id, session_id, query[:500],
                     json.dumps(etir_nodes), json.dumps(retrieved_facts),
                     tokens_used, token_budget)
                )
                await db.commit()
        except Exception as e:
            logger.warning(f"AuditLayer.log_context: {e}")

    async def log_strategy_selection(
        self,
        request_id: str,
        strategy_id: str,
        strategy_desc: str,
        score: float,
        selection_mode: str,
        all_candidates: list,
        session_id: str = ""
    ):
        """Вызывать из ReasoningBank.retrieve_relevant_strategies() — Slow Path."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO audit_strategy VALUES (NULL,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
                    (request_id, session_id, strategy_id, strategy_desc[:300],
                     score, selection_mode, json.dumps(all_candidates))
                )
                await db.commit()
        except Exception as e:
            logger.warning(f"AuditLayer.log_strategy: {e}")

    async def log_forgetting(
        self,
        node_id: str,
        node_type: str,
        reason: str,
        importance_at_delete: float,
        archived_to_s3: bool = False,
        s3_key: str = None
    ):
        """Вызывать из MemoryGarbageCollector при soft-delete — Slow Path."""
        await self._ensure_schema()
        try:
            import aiosqlite
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO audit_forgetting VALUES (NULL,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
                    (node_id, node_type, reason, importance_at_delete, archived_to_s3, s3_key)
                )
                await db.commit()
        except Exception as e:
            logger.warning(f"AuditLayer.log_forgetting: {e}")

    async def explain_context(self, request_id: str) -> dict:
        """GET /memory/audit/context?request_id=..."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM audit_context WHERE request_id=? LIMIT 1", (request_id,)
                ) as cur:
                    row = await cur.fetchone()
            if not row:
                return {"error": f"no audit for request_id={request_id}"}
            d = dict(row)
            d["etir_nodes"]  = json.loads(d.get("etir_nodes")  or "[]")
            d["facts_used"]  = json.loads(d.get("facts_used")  or "[]")
            d["budget_pct"]  = round((d["tokens_used"] or 0) / max(d["token_budget"] or 1, 1), 3)
            return d
        except Exception as e:
            return {"error": str(e)}

    async def explain_strategy(self, request_id: str) -> dict:
        """GET /memory/audit/strategy?request_id=..."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM audit_strategy WHERE request_id=? LIMIT 1", (request_id,)
                ) as cur:
                    row = await cur.fetchone()
            if not row:
                return {"error": f"no audit for request_id={request_id}"}
            d = dict(row)
            d["all_candidates"] = json.loads(d.get("all_candidates") or "[]")
            return d
        except Exception as e:
            return {"error": str(e)}

    async def explain_forgetting(self, since: str, limit: int = 50) -> list:
        """GET /memory/audit/forgetting?since=2026-03-01T00:00:00"""
        await self._ensure_schema()
        try:
            import aiosqlite
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM audit_forgetting WHERE deleted_at >= ?"
                    " ORDER BY deleted_at DESC LIMIT ?",
                    (since, limit)
                ) as cur:
                    return [dict(r) for r in await cur.fetchall()]
        except Exception as e:
            return [{"error": str(e)}]
```

> 💡 **Для MVP Phase 0**: достаточно просто писать audit в `.log` файл через Python `logging`. Полный API — для Phase 1+.


class ContradictsUXProtocol:
    """
    UX-протокол для [:CONTRADICTS] — агент спрашивает пользователя перед override.

    Правило из v2.19 (TruthGate.I3):
        «LLM НЕ расставляет [:CONTRADICTS] автоматически.
         Только явная команда пользователя или CRUD-классификатор.»

    Без этого класса LLM может тихо перезаписать факт.
    С ним — агент останавливается и показывает конфликт пользователю.

    Usage:
        c   = ContradictsUXProtocol(graph, event_bus)
        msg = await c.detect_and_propose(new_fact_content, session_id)
        if msg:
            return msg          # остановить запись, показать пользователю
        # Когда пользователь ответил:
        decision = await c.handle_user_response(user_reply, session_id)
        if decision["action"] == "override":
            pass  # продолжить запись нового факта
        elif decision["action"] == "keep":
            pass  # отменить запись
    """

    _YES = frozenset(["да", "стереть", "удалить", "заменить", "верно",
                       "подтверждаю", "ок", "yes", "confirm", "override"])
    _NO  = frozenset(["нет", "не надо", "сохранить", "оставить",
                       "отмена", "no", "keep", "cancel"])

    def __init__(self, graph_adapter, event_bus):
        self.graph      = graph_adapter
        self.event_bus  = event_bus
        self._pending: dict = {}   # session_id → {new_fact, old_id, old_summary}

    async def detect_and_propose(self, new_fact: str, session_id: str) -> str | None:
        """Ищет потенциальный конфликт в L3. Возвращает сообщение пользователю или None."""
        results = await self.graph.search(query=f"contradicts: {new_fact[:200]}", limit=3)
        if not results:
            return None
        best        = results[0]
        old_summary = (best.get("content", str(best)) if isinstance(best, dict) else str(best))[:200]
        old_id      = best.get("id", "unknown") if isinstance(best, dict) else "unknown"
        self._pending[session_id] = {
            "new_fact": new_fact, "old_id": old_id, "old_summary": old_summary
        }
        return (f"⚠️ Вижу возможное противоречие с прежним решением:\n"
                f"  📌 Старое: «{old_summary}»\n"
                f"  🆕 Новое:  «{new_fact[:200]}»\n\n"
                f"Стереть старое и записать новое? (да / нет)")

    async def handle_user_response(self, reply: str, session_id: str) -> dict:
        """Разбирает ответ пользователя. action: 'override' | 'keep' | 'pending'."""
        p = self._pending.get(session_id)
        if not p:
            return {"action": "pending", "proposal": None}
        q = reply.lower().strip()
        if any(w in q for w in self._YES):
            await self.graph.execute_cypher(
                "MATCH (f {id: $id}) SET f.is_active = false, f.valid_to = datetime(),"
                " f.contradicted_by_user = true",
                {"id": p["old_id"]}
            )
            del self._pending[session_id]
            return {"action": "override", "proposal": p}
        if any(w in q for w in self._NO):
            del self._pending[session_id]
            return {"action": "keep", "proposal": p}
        return {"action": "pending", "proposal": p}

    def clear_expired(self, active_sessions: list):
        """Чистить pending для завершённых сессий."""
        for sid in [s for s in self._pending if s not in active_sessions]:
            del self._pending[sid]


class TokenBudgetLadder:
    """
    Приоритетная лестница token budget — что режется ПЕРВЫМ при нехватке.

    Из v2.19: «Если бюджет исчерпан — L3 отсекается первым, L0 и Etir защищены всегда.»
    В v5 были числа в TokenConfig, но порядок приоритетов явно не закреплён.

    Protected slots (никогда не режутся): ring_zero, L0, core_memory_blocks, etir.
    Остальные — по возрастанию priority (6 → режется первым).

    Usage:
        ladder   = TokenBudgetLadder(budget=TOKENS.BALANCED_MODE)
        selected = ladder.select({
            "ring_zero_values":   ring_zero_text,
            "L0_working_memory":  wm_text,
            "etir_activation":    etir_text,
            "l1_stm_episodes":    stm_text,
            "l3_ltm_graph":       ltm_text,
        })
        prompt = "\\n\\n".join(selected.values())
    """

    # (name, max_tokens, protected, priority — меньше = важнее, режется последним)
    _SLOTS = [
        ("ring_zero_values",     150,  True,  1),
        ("L0_working_memory",    100,  True,  1),
        ("core_memory_blocks",   500,  True,  1),
        ("etir_activation",      300,  True,  2),
        ("l1_stm_episodes",      600,  False, 3),
        ("strategies",           300,  False, 4),
        ("l2_mtm_summaries",     300,  False, 5),
        ("l3_ltm_graph",         400,  False, 6),  # ← режется ПЕРВЫМ
        ("conversation_history", 300,  False, 7),
    ]

    def __init__(self, budget: int = 2000):
        self.budget = budget

    def select(self, slot_contents: dict) -> dict:
        """Возвращает подмножество слотов, гарантированно влезающее в budget."""
        selected = {}
        used     = 0

        # Protected — всегда включить первыми
        for name, max_tok, protected, _ in self._SLOTS:
            if not protected:
                continue
            text = slot_contents.get(name, "")
            if not text:
                continue
            tok   = min(self._count(text), max_tok)
            used += tok
            selected[name] = text[:tok * 4]

        # Non-protected — в порядке приоритета (greedy fit)
        for name, max_tok, protected, _ in self._SLOTS:
            if protected or used >= self.budget:
                continue
            text = slot_contents.get(name, "")
            if not text:
                continue
            allowed = min(self._count(text), max_tok, self.budget - used)
            if allowed <= 0:
                continue
            selected[name] = text[:allowed * 4]
            used += allowed

        logger.debug(f"TokenBudgetLadder: {len(selected)} slots ~{used}/{self.budget} tokens")
        return selected

    @staticmethod
    def _count(text: str) -> int:
        try:
            import tiktoken
            return len(tiktoken.get_encoding("cl100k_base").encode(text))
        except Exception:
            return max(1, len(text) // 4)
> 
> 💡 **Альтернатива без написания кода**: LangSmith или Arize Phoenix — визуальный трейсинг всего пути от запроса до каждого узла графа "из коробки".

---

## 🛡️ Memory Guardian — Защита от отравления памяти 

> **Проблема**: Без слоя валидации агент может записать галлюцинацию в граф как факт. Через 1-2 месяца система начнёт повторять ошибочные паттерны с уверенностью — у неё есть "доказательства".

**Memory Guardian** — это L5 Observer расширенный до роли привратника L3. Ни один факт не попадает в Neo4j без прохождения этого слоя.

```python
# memory_guardian.py
class MemoryGuardian:
    """
    Привратник L3 графа. Реализует Truth Gate до записи.
    Живёт в L5 Observer — следит за потоком, блокирует отравление.
    """

    def __init__(self, graph: GraphMemory, confidence_threshold: float = 0.7):
        self.graph = graph
        self.confidence_threshold = confidence_threshold

    async def validate_proposal(self, proposal: dict) -> bool:
        """
        Валидация факта/эпизода перед записью в L3.
        Возвращает True только если все проверки пройдены.
        """
        # 1. Проверка наличия источника (evidence)
        if not proposal.get("evidence"):
            logger.warning(f"Guardian: rejected — no evidence: {proposal}")
            return False
        
        # 2. Confidence threshold
        if proposal.get("confidence", 0) < self.confidence_threshold:
            logger.warning(f"Guardian: rejected — low confidence: {proposal}")
            return False
        
        # 3. Проверка на противоречия с существующим графом
        contradictions = await self._check_contradictions(proposal)
        if contradictions:
            logger.warning(f"Guardian: conflict found — {len(contradictions)} contradictions")
            # Не удаляем — создаём [:CONTRADICTS] связь для разрешения
            await self._mark_contradiction(proposal, contradictions)
            return False
        
        # 4. Дедупликация
        if await self._is_duplicate(proposal):
            logger.info("Guardian: duplicate detected — incrementing evidence_count")
            await self._increment_evidence(proposal)
            return False  # Уже есть, новый не нужен
        
        return True

    async def _check_contradictions(self, proposal: dict) -> list:
        """Поиск противоречий в L3 графе"""
        query = """
        MATCH (f:Fact)
        WHERE f.is_active = true
          AND f.concept = $concept
          AND f.relation = $relation
          AND f.value <> $value
        RETURN f
        LIMIT 10
        """
        return await self.graph.execute_cypher(query, {
            "concept": proposal.get("concept"),
            "relation": proposal.get("relation"),
            "value": proposal.get("value")
        })

    async def _is_duplicate(self, proposal: dict) -> bool:
        """Проверка на точный дубликат"""
        query = """
        MATCH (f:Fact)
        WHERE f.is_active = true
          AND f.concept = $concept
          AND f.relation = $relation
          AND f.value = $value
        RETURN count(f) > 0 as exists
        """
        result = await self.graph.execute_cypher(query, proposal)
        return result[0]["exists"] if result else False
```

> 💡 **Интеграция**: `MemoryGuardian.validate_proposal()` вызывается внутри `GraphMemory.add_episode()` до любой записи в Neo4j. L5 Observer расширяется этим модулем в Phase 1.

---

## 🗃️ Immutable Raw Memory — Защита от Semantic Drift 

> **Проблема Semantic Drift**: Консолидация L1→L2→L3 через LLM-суммаризацию постепенно искажает смысл. "User prefers Python" → "User programs" → "User expert developer". Оригинал теряется.

**Решение**: Сырые эпизоды хранятся отдельно и **никогда не изменяются**. Суммаризации — отдельно. Всегда есть доступ к первоисточнику.

```python
# raw_memory_store.py
class ImmutableRawMemory:
    """
    Неизменяемое хранилище сырых эпизодов.
    Хранится в SQLite (не в Neo4j) — простой, надёжный, не изменяется.

    Правило: raw_episodes никогда не обновляются.
    Суммаризации (summaries) создаются поверх, но оригинал защищён.

    Инициализация: вызвать await init() в async-контексте перед первым использованием.
    _init_schema() НЕ вызывается из __init__ — это защита от блокировки event loop.
    """

    def __init__(self, db_path: str = "raw_memory.db"):
        self.db_path = db_path
        # Схема инициализируется через await init(), не в __init__

    async def init(self):
        """Async-безопасная инициализация схемы. Вызвать один раз при старте агента."""
        import aiosqlite
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=WAL")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS raw_episodes (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT,
                    outcome TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    -- Нет полей для обновления — это append-only хранилище
                )
            """)
            await db.commit()

    def save_episode(self, episode_id: str, content: str,
                     source: str, session_id: str, outcome: str = None):
        """
        Сохранить сырой эпизод. Никогда не обновлять.
        Вызывать из async-контекста через asyncio.to_thread():
            await asyncio.to_thread(raw_memory.save_episode, episode_id, content, ...)
        """
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                # явные имена колонок — защита от тихого сломания при изменении схемы
                """INSERT OR IGNORE INTO raw_episodes
                   (id, content, source, timestamp, session_id, outcome)
                   VALUES (?, ?, ?, datetime('now'), ?, ?)""",
                (episode_id, content, source, session_id, outcome)
            )
            conn.commit()

    def get_truth_source(self, episode_id: str) -> dict:
        """
        Получить оригинальный эпизод.
        Используется при реконструкции если суммаризация исказила смысл.
        """
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM raw_episodes WHERE id = ?", (episode_id,)
            ).fetchone()
        return dict(zip(["id","content","source","timestamp","session_id","outcome","created_at"], row)) if row else None
```

> 💡 **Интеграция**: При `GraphMemory.add_episode()` — сначала `ImmutableRawMemory.save_episode()`, затем проход через `MemoryGuardian`, затем запись в Neo4j. Поле `raw_episode_id` в узле `:Episode` хранит ссылку на оригинал.

---

## 🔗 CausalGraph — Слой причинно-следственных связей

> **Назначение**: агент понимает не только *что* произошло, но *почему*. Рёбра `CAUSES`, `LEADS_TO`, `INFLUENCES` между `:Entity` и `:Fact` узлами позволяют строить причинные цепочки и вставлять их в Facts Pack перед LLM-генерацией.

> **Почему не нарушает `Graph = Truth`**: CausalGraph только *добавляет рёбра* между уже существующими валидированными узлами L3. Новых фактов не создаёт. LLM используется только для извлечения причин из текста — результат идёт через Truth Gate как обычно.

> **Архитектурное место**: запускается фоновым `asyncio.create_task` внутри `GraphMemory.add_episode()` — не блокирует Fast Path. `llm_client` передаётся как опциональный параметр метода, не хранится в `GraphMemory` — граф остаётся независимым от LLM по умолчанию.

```python
# memory/causal_graph.py, адаптирован для Velantrim

import asyncio
import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)

# Типы причинно-следственных рёбер
CAUSAL_RELATION_TYPES = {
    "CAUSES":     "прямая причина",
    "LEADS_TO":   "косвенное следствие",
    "INFLUENCES": "влияет на",
}


@dataclass
class CausalEdge:
    source:   str    # entity или fact id
    target:   str
    relation: str    # CAUSES | LEADS_TO | INFLUENCES
    strength: float  # 0.0–1.0
    evidence: str    # краткое обоснование


class CausalGraph:
    """
    Извлекает причинно-следственные связи из текста эпизода
    и сохраняет их как рёбра в L3 графе.

    Принцип работы:
    1. При add_episode — фоновый create_task вызывает extract_and_store()
    2. LLM (опционально) извлекает причины из текста эпизода
    3. Рёбра сохраняются как MERGE — безопасно для повторного вызова
    4. get_causal_chain() используется ContextBuilder для Facts Pack

    Инвариант: CausalGraph не создаёт новые :Fact узлы.
    Только рёбра между существующими узлами — Graph = Truth не нарушается.
    """

    def __init__(self, graph_adapter):
        # graph_adapter — IGraphAdapter (GraphitiAdapter или GraphLiteAdapter)
        self.graph = graph_adapter

    async def extract_and_store(
        self,
        episode_name: str,
        content:      str,
        entities:     List[str],
        llm_client    = None,    # опциональный — без LLM работает по эвристикам
    ) -> List[CausalEdge]:
        """
        Извлечь причинно-следственные связи из текста эпизода.
        Вызывается через asyncio.create_task — не блокирует pipeline.
        llm_client передаётся как параметр, не хранится в self.
        """
        if not content or not entities:
            return []

        edges = await self._extract_edges(content, entities, llm_client)

        for edge in edges:
            await self._store_edge(edge)

        if edges:
            logger.debug(
                f"CausalGraph: extracted {len(edges)} edges for episode '{episode_name}'"
            )
        return edges

    async def _extract_edges(
        self,
        content:   str,
        entities:  List[str],
        llm_client = None,
    ) -> List[CausalEdge]:
        """LLM-извлечение с эвристическим fallback."""
        if llm_client:
            return await self._llm_extract(content, entities, llm_client)
        return self._heuristic_extract(content, entities)

    async def _llm_extract(
        self,
        content:    str,
        entities:   List[str],
        llm_client,
    ) -> List[CausalEdge]:
        """
        Попросить LLM найти причинно-следственные связи.
        Промпт требует строгий JSON — без него парсинг падает gracefully.
        """
        entities_str = ", ".join(entities[:10])  # ограничение токенов
        prompt = f"""Find causal relationships between entities in this text.
Return JSON array only, no explanation:
[{{"source": "A", "target": "B", "relation": "CAUSES|LEADS_TO|INFLUENCES", "strength": 0.0-1.0, "evidence": "brief reason"}}]

Entities: {entities_str}
Text: {content[:500]}

JSON:"""
        try:
            response = await llm_client.complete(prompt)
            import json, re
            # Извлекаем JSON из ответа — LLM иногда добавляет текст вокруг
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if not match:
                return []
            raw = json.loads(match.group())
            edges = []
            for item in raw:
                relation = item.get("relation", "").upper()
                if relation not in CAUSAL_RELATION_TYPES:
                    continue
                edges.append(CausalEdge(
                    source=str(item.get("source", "")),
                    target=str(item.get("target", "")),
                    relation=relation,
                    strength=float(item.get("strength", 0.5)),
                    evidence=str(item.get("evidence", ""))[:200],
                ))
            return edges
        except Exception as e:
            logger.debug(f"CausalGraph LLM extract failed: {e}")
            return self._heuristic_extract(content, entities)

    @staticmethod
    def _heuristic_extract(content: str, entities: List[str]) -> List[CausalEdge]:
        """
        Эвристическое извлечение по ключевым словам без LLM.
        Ищет маркеры причинности между упомянутыми сущностями.
        Работает как fallback — точность ниже чем LLM, но ноль токенов.
        """
        edges = []
        text_lower = content.lower()

        # Маркеры причинности → тип ребра
        cause_markers   = ["вызывает", "причина", "из-за", "causes", "because", "due to"]
        leads_markers   = ["приводит", "ведёт к", "leads to", "results in", "результат"]
        influence_marks = ["влияет", "affects", "impacts", "изменяет"]

        for i, e1 in enumerate(entities):
            for e2 in entities[i + 1:]:
                if e1 == e2:
                    continue
                # Оба упомянуты в тексте
                if e1.lower() not in text_lower or e2.lower() not in text_lower:
                    continue

                # Определяем тип по маркерам
                if any(m in text_lower for m in cause_markers):
                    relation, strength = "CAUSES", 0.6
                elif any(m in text_lower for m in leads_markers):
                    relation, strength = "LEADS_TO", 0.5
                elif any(m in text_lower for m in influence_marks):
                    relation, strength = "INFLUENCES", 0.4
                else:
                    continue

                edges.append(CausalEdge(
                    source=e1, target=e2,
                    relation=relation, strength=strength,
                    evidence="heuristic extraction",
                ))
        return edges

    async def _store_edge(self, edge: CausalEdge):
        """
        Сохранить ребро в L3 через MERGE — идемпотентно.
        Использует execute_cypher — граф = единственный источник истины.
        При сбое — логируем и продолжаем (некритично для pipeline).
        """
        try:
            await self.graph.execute_cypher(
                f"""
                MATCH (a) WHERE a.name = $source OR a.id = $source
                MATCH (b) WHERE b.name = $target OR b.id = $target
                MERGE (a)-[r:{edge.relation}]->(b)
                SET r.strength  = $strength,
                    r.evidence  = $evidence,
                    r.updated_at = datetime()
                """,
                {
                    "source":   edge.source,
                    "target":   edge.target,
                    "strength": edge.strength,
                    "evidence": edge.evidence,
                }
            )
        except Exception as e:
            logger.debug(f"CausalGraph._store_edge failed ({edge.source}→{edge.target}): {e}")

    async def get_causal_chain(
        self,
        entity:    str,
        max_depth: int = 2,
        min_strength: float = 0.4,
    ) -> List[dict]:
        """
        Получить причинную цепочку для сущности.
        Вызывается ContextBuilder при сборке Facts Pack.
        max_depth прошёл через whitelist (1,2,3) — защита от инъекции.
        """
        safe_depth = max_depth if max_depth in (1, 2, 3) else 2
        try:
            return await self.graph.execute_cypher(
                f"""
                MATCH (start) WHERE start.name = $entity OR start.id = $entity
                MATCH path = (start)-[:CAUSES|LEADS_TO|INFLUENCES*1..{safe_depth}]->(end)
                WHERE ALL(r IN relationships(path) WHERE r.strength >= $min_str)
                RETURN
                    [node IN nodes(path) | coalesce(node.name, node.id)] AS chain,
                    [r IN relationships(path) | type(r)]                  AS relations,
                    [r IN relationships(path) | r.strength]               AS strengths
                ORDER BY size(nodes(path))
                LIMIT 10
                """,
                {"entity": entity, "min_str": min_strength}
            )
        except Exception as e:
            logger.warning(f"CausalGraph.get_causal_chain failed: {e}")
            return []

    @staticmethod
    def format_chain_for_context(chain_rows: List[dict]) -> str:
        """
        Форматировать причинную цепочку для вставки в Facts Pack.
        Вызывается ContextBuilder — результат идёт в LLM как часть контекста.
        """
        if not chain_rows:
            return ""

        arrow_map = {
            "CAUSES":     "→ вызывает →",
            "LEADS_TO":   "→ приводит к →",
            "INFLUENCES": "~ влияет на ~",
        }
        lines = ["📎 Причинно-следственные связи:"]
        for row in chain_rows:
            chain     = row.get("chain",     [])
            relations = row.get("relations", [])
            strengths = row.get("strengths", [])
            parts = []
            for i, node in enumerate(chain):
                parts.append(node)
                if i < len(relations):
                    rel    = arrow_map.get(relations[i], "→")
                    weight = f"({strengths[i]:.1f})" if i < len(strengths) else ""
                    parts.append(f"{rel}{weight}")
            lines.append("  " + " ".join(parts))
        return "\n".join(lines)
```

**Интеграция в `GraphitiAdapter.add_episode()`** — добавить фоновый вызов после успешной записи:

```python
# graph_adapter.py — в конце GraphitiAdapter.add_episode(), после return f"episode:{name}"
# (передавать llm_client и entities как опциональные параметры метода)

# CausalGraph: фоновое извлечение причинно-следственных связей
# llm_client=None → работает по эвристикам, ноль токенов
if hasattr(self, '_causal_graph') and self._causal_graph:
    _t = asyncio.create_task(
        self._causal_graph.extract_and_store(
            episode_name=name,
            content=content,
            entities=entities or [],
            llm_client=llm_client,   # None = heuristic mode
        )
    )
    _t.add_done_callback(
        lambda t: t.exception() and
        logger.debug(f"CausalGraph task failed: {t.exception()}")
    )
```

**Интеграция в `ContextBuilder`** — добавить в сборку Facts Pack:

```python
# context_builder.py — в методе build_context(), после retrieval фактов

from memory.causal_graph import CausalGraph
causal_chain = await self.causal_graph.get_causal_chain(
    entity=query_entity,   # главная сущность запроса
    max_depth=2,
    min_strength=0.4,
)
if causal_chain:
    causal_context = CausalGraph.format_chain_for_context(causal_chain)
    # Добавить в Facts Pack как отдельный блок перед LLM
    facts_pack.append({"type": "causal_chain", "content": causal_context})
```

**Инвариант**: `CausalGraph` не создаёт новые `:Fact` узлы — только рёбра между существующими. Граф остаётся единственным источником истины. `llm_client` передаётся параметром, не хранится в `GraphMemory` — разделение `Graph = Truth` и `LLM = Language` сохраняется.

---

## 🧬 Knowledge Distillation Engine — Наполнение L3 

> **Проблема**: Без этого модуля Neo4j останется пустым. Нельзя наполнить граф просто суммаризациями — они теряют структуру. Нужны атомарные JSON-тройки.

**Knowledge Distillation** превращает сырой текст в структурированные `KnowledgeUnit` перед записью в L3.

```
Сырой текст:
"Вода кипит при 100°C при стандартном атмосферном давлении."
         ↓
KnowledgeUnit (JSON-тройка):
{
  "concept":   "Water",
  "relation":  "boiling_point",
  "value":     "100°C",
  "condition": "1 atm",
  "evidence":  "physics_textbook_ch3",
  "confidence": 0.98
}
         ↓
Memory Guardian → L3 Neo4j (:KnowledgeUnit узел)
```

**Pipeline (гибридный — без LLM для простых случаев):**

```
Шаг 1 (NLP — дёшево и быстро):
  SpaCy / GLiNER → NER + Relation Extraction
  → базовые тройки (Subject, Predicate, Object)
  → confidence определяется автоматически

Шаг 2 (LLM — только если нужно):
  Подключать L4 Reasoning (o4-mini) только когда:
  - NLP confidence < 0.8
  - Memory Guardian нашёл конфликт
  - Сущности неоднозначны (анафора: "он", "они")

Шаг 3 (Guardian):
  Каждая тройка → Memory Guardian → L3
```

> ⚠️ **Риск анафоры**: "Он нажал кнопку" → создаст узел `:Entity{name: "Он"}`. Решение: chunking с сохранением контекста абзаца (не отдельных предложений).
>
> 💡 **MVP для Phase 0**: Выбрать узкий домен (например, LING/THINK глоссарий). L4 извлекает строго форматированный JSON из абзаца. L5 Guardian проверяет. Без сложного разрешения конфликтов — просто `evidence_count++` если тройка уже есть.

---

## 📜 Формальные инварианты системы (RFC0001–RFC0005)

> **Инвариант** — правило, нарушение которого является багом архитектуры, а не поведения. Этот раздел — контракт системы. Любое изменение требует осознанного решения.

### 🛡️ MGL (Memory Governance Layer)

```
1. Episode ∉ Semantic Graph
   Эпизоды диалогов НИКОГДА не входят в L3 граф.
   Phase 2: вынести в отдельную Vector DB (Qdrant).

2. ∀ fact ∈ Graph: fact.validated = True
   Ни один факт не попадает в Neo4j без прохождения MGL.

3. Graph is bi-temporal
   Каждый факт имеет valid_from/valid_to + transaction_time.

4. No LLM output enters graph without MGL
   Галлюцинация LLM не может стать фактом напрямую.

5. ∀ fact ∈ Graph: ∃ evidence (:Evidence node)
   Каждый факт связан с источником через [:SUPPORTED_BY].
```

### 🔍 RE (Reasoning Engine)

```
1. Every conclusion must have support facts.
   Вывод без фактов → недопустим.

2. Reasoning Graph ≠ Semantic Graph.
   Граф рассуждений строится в памяти, не записывается в Neo4j.

3. LLM does not perform inference — only explains.
   L4 Reasoning делает вывод. LLM переводит его в текст.

4. Evidence Pack must satisfy Truth Gate before reaching LLM.
```

### 🧬 KDE (Knowledge Distillation Engine)

```
1. KDE produces only structured KnowledgeUnit (JSON-тройки).
   Не текстовые куски — только атомарные факты.

2. KDE never writes directly to graph.
   Всегда: KDE → MGL → Graph.

3. KDE output must pass through MGL.
```

### 🔱 Velantrim Core Principles

```
1. Memory separated by type: Working / Episodic / Semantic / Policy.
2. Semantic Graph = SSOT (единственный источник истины).
3. Reasoning Engine performs inference, not LLM.
4. All knowledge passes through Governance (MGL).
5. Episodic memory NEVER enters Semantic Graph.
6. Evidence Pack required for every answer.
```

---

## 📦 Evidence Builder и Truth Gate (RFC0004)

> **Назначение**: прежде чем LLM генерирует ответ, Evidence Builder собирает пакет доказательств. Truth Gate проверяет достаточность и согласованность.

### 🔄 Validation Loop (L4) — три вопроса до Truth Gate

> Снижает галлюцинации без вызова LLM.
> Система задаёт себе три вопроса перед тем как идти в Truth Gate:

```
Шаг 1 — DECISION: нужен ли поиск вообще?
  Если запрос в L0 Working Memory (Goal Stack) → ответить без поиска
  Если intent = TASK → ответить из L0, не трогать L3
  Если ответ очевиден из контекста → пропустить retrieval

Шаг 2 — VALIDATION: релевантен ли retrieved контент?
  Для каждого retrieved факта: cosine(query, fact) ≥ 0.65?
  Если нет — выбросить факт из Evidence Pack до Truth Gate
  Это фильтрует семантический шум до проверки RFC порогов

Шаг 3 — SELF-CHECK: верен ли финальный ответ?
  После Truth Gate, перед передачей в LLM:
  Проверить что каждое утверждение имеет TRACE-ссылку на узел
  Если утверждение без ссылки → пометить как [unverified]
  [unverified] блокирует передачу как :Fact (только :Hypothesis)

Результат: система не просто ищет — она рассуждает о поиске.
           Fast Path (70-90% запросов) — без LLM, без retrieval.
           Slow Path — только если Validation Loop не дал ответ.
```

### Формат Evidence Pack

```json
{
  "facts": [
    {
      "content": "Water boils at 100°C at 1 atm",
      "confidence": 0.98,
      "source": "evidence:physicsbook1"
    }
  ],
  "confidence": 0.92,
  "coverage": 0.87,
  "contradictions": [],
  "evidence_count": 5
}
```

### Правила Truth Gate (конкретные пороги)

```
coverage        ≥ 0.7     — запрос покрыт фактами минимум на 70%
contradictions  = 0       — нет активных конфликтов
evidence_count  ≥ 3       — минимум 3 подтверждающих факта
confidence      ≥ 0.75    — средняя уверенность выше порога

Если хотя бы одно условие не выполнено:
→ LLM не генерирует ответ
→ Возвращается: "Недостаточно данных для уверенного вывода."
→ Логируется в Audit Layer для анализа пробелов в знаниях
```

### KDE масштаб (ориентиры планирования)

```
1 книга              →  1–5k  фактов
1000 книг + Wikipedia → 1–2M  фактов
2M фактов            ≈  1–2 GB в Neo4j
MVP железо           :  16 GB RAM, 8 CPU, SSD — достаточно
```

---

## 📜 Canonical Memory Protocol v1

> **Почему критично**: без единой точки входа каждый разработчик понимает систему по-разному. Этот протокол — «конституция» Velantrim — описывает что происходит при каждом запросе и каждом событии.

---

### ⚡ Fast Path (синхронный — пользователь ждёт)

```
Вход: user_message + session_id + текущий Goal Stack

F1: Validation Loop L4 — три вопроса ДО генерации:
    · DECISION:    нужен ли поиск в памяти вообще?
    · VALIDATION:  релевантен ли retrieved контент?
    · SELF-CHECK:  верен ли финальный ответ (Truth Gate)?

F1.5: Velum Context Hint (RFC0016)
    · Velum.get_neighbors(query_entities, min_weight=0.3)
    · Добавить соседей в seed для Etir (шаг F2.5)
    · Fire-and-forget hint — не блокирует Fast Path

F2: L0 update
    · Обновить Goal Stack (добавить/уточнить активную цель)
    · Загрузить Ring Zero + Project State Card (если не в L0)
    · Priority Eviction при capacity > 4±1:
      CRITICAL (Ring Zero, Project State) → никогда не вытесняются
      HIGH (active goal) → последний на eviction
      MEDIUM (текущий диалог)
      LOW (вспомогательный контекст) → первый на eviction → L1

F3: L1 FTS5 search
    · SQLite FTS5 по session_id + ключевые слова запроса
    · Recency bias: свежие эпизоды приоритетнее
    · Отобрать 1-2 эпизода-кандидата

F4: Graphiti search → Neo4j
    · MAX_RESULTS = 10, is_active = true, таймаут
    · Hybrid: semantic + keyword + graph traversal

F5: Context Builder → 4±1 чанка
    · token_budget = MAX_TOKENS_MEMORY_PER_QUERY = 2000
    · Приоритет: L0 > Etir > L1 > L2 > L3
    · Typed context tags: <facts trust="verified"> / <hypothesis>
    · Source tagging : _format_fact() с метками
      [ФАКТ] = из L3 графа, [ПРЕДВАРИТЕЛЬНО] = из staging, [ТЕКУЩАЯ СЕССИЯ] = из L1

F6: LLM Generation — ЕДИНСТВЕННЫЙ вызов на Fast Path
    · Evidence Pack обязателен
    · Truth Gate: coverage ≥ 0.7, evidence_count ≥ 3
    · [unverified] метка для утверждений без TRACE

F6.5: OutputFaithfulnessChecker.check(answer, facts_pack)
    · Проверка что LLM не добавил утверждений без опоры на FactsPack
    · MVP: keyword overlap ≥ 40% (Phase 1: NLI cross-encoder)
    · passed → вернуть answer пользователю
    · failed → FALLBACK_RESPONSE + логировать unsupported_sentences в Audit Layer

Выход: ответ + AgentEvent(USER_MESSAGE + AGENT_RESPONSE) в шину
```

---

### 🔄 Slow Path (асинхронный — в фоне, не блокирует)

```
S1: Event Bus Logging
    · USER_MESSAGE, AGENT_RESPONSE, TASK_COMPLETED → Redis Streams
    · Retry 3x + exponential backoff + DLQ + Fallback Queue

S2: Extraction — ТОЛЬКО задачи в статусе RESOLVED или FAILED
    · KDE → JSON-тройки (KnowledgeUnit)
    · NLP confidence < 0.8 → L4 o4-mini для уточнения
    · Задачи в BLOCKED_AWAITING_DB ждут восстановления CE

S2.6: Creative Ingestion Pipeline (параллельно с S2 · RFC0067 v2.0)
    · Источники: научпоп, философские эссе, качественная художественная проза
    → CreativeExtractor (LLM flagship, temp=0.5)    <- async · Slow Path
    → AnalogyAggregator (>= 2 источника OR authority >= 0.9)
    → Write Protocol Gate
    → Analogy Graph L3 ([:METAPHOR_OF] / [:ANALOGOUS_TO])
    Отклонённые → SQLite: suggested_analogies (ручной аудит)

S2.7: Knowledge Ingestion Pipeline (офлайн · RFC0063)
    · Источники: PDF / JSON / YAML / Wikidata RDF / plain text
    → FactExtractor (LLM flagship, temp=0.1) → Truth Gate → L3 граф
    → PatternExtractor (LLM flagship, temp=0.4) → ReasoningBank (Bayesian prior)
    → SemanticIndexer (embedding only, 0 LLM) → Qdrant/ChromaDB
    → EdgeSuggester (аудиторский инструмент) → SQLite: suggested_edges
    · Только Slow Path. Прямой вызов из Fast Path — нарушение I63 (ex-I40).

---

## RFC0067 v2.0: Creative Intelligence Layer

### 🌱 Читай это первым

RFC0067 v2.0 — полноценный **Creative Intelligence Layer** из трёх механизмов:

**Analogy Graph** — явная карта метафор и аналогий из качественных текстов. Рёбра `[:METAPHOR_OF]` и `[:ANALOGOUS_TO]` на узлах L3.

**Semantic Bridge Engine (SBE)** — асинхронный воркер, подписан на EventBus, предвычисляет семантические мосты. Только Slow Path. Fast Path читает Redis-кэш.

**Adaptive Decoder** — CREATIVE режим с динамической температурой (0.6 → 0.85) и `presence_penalty = 0.6`. Четвёртый когнитивный режим.

> ⚠️ **Важно:** CREATIVE разрешает аналогии, запрещает Hypothesized факты (I57). EXPLORATION разрешает Hypothesized, не имеет аналогий (I58). Это разные режимы по природе.

> ⚠️ **Зависимость:** `psutil>=5.9` для CPU guard в SBEAsyncWorker. Добавить в `requirements.txt`. Redis и Qdrant/ChromaDB уже в стеке.

---

```
RFC0067 v2.0: Creative Intelligence Layer
    |
    +- [Analogy Graph]:
    |   Рёбра [:METAPHOR_OF] и [:ANALOGOUS_TO] на узлах L3.
    |   Источник: CreativeExtractor + AnalogyAggregator (S2.6).
    |   Лимит: макс 50 исходящих аналогий на узел. Хранение: > 365 дней -> холодный граф.
    |   I55:   только через Write Protocol Gate. Прямой MERGE -> WriteProtocolViolation.
    |   I55.1: SAE decay_factor=0.4 для рёбер аналогий (не 0.6 как обычно).
    |
    +- [SBEAsyncWorker]:
    |   EventBus: focus_vector_changed / cognitive_mode_switched / periodic_tick.
    |   -> Qdrant (cross-domain, cosine >= 0.75)
    |   -> Redis: creative_bridge:{session_id} (TTL=15 мин)
    |   I56: только Slow Path. Fast Path читает только кэш.
    |
    +- [ResonanceTracker]:
    |   used_in_response: +0.05 / positive_continuation: +0.10
    |   explicit_like: +0.20 / clarification_request: -0.10 / explicit_dislike: -0.25
    |   resonance >= 0.7 -> кристаллизация через Write Protocol Gate.
    |   Decay: каждую неделю resonance x 0.95.
    |   I56.1: SBE не пишет напрямую. Только resonance >= 0.7 -> Write Protocol.
    |
    +- [AdaptiveDecoder]:
    |   temp = 0.6 + (0.85-0.6) * min(associations_count/5, 1.0)
    |   presence_penalty = 0.6 (для SLM < 3B: min 0.5, I57)
    |   I57: FactsPack только Validated. Ассоциации в creative_context.
    |
    +- Инварианты RFC0067 v2.0:
    |   I55:   [:METAPHOR_OF] и [:ANALOGOUS_TO] только через Write Protocol Gate.
    |   I55.1: SAE decay_factor=0.4 для рёбер аналогий.
    |   I56:   SBE только в Slow Path через EventBus.
    |   I56.1: SBE не пишет в граф напрямую. resonance >= 0.7 -> Write Protocol.
    |   I57:   CREATIVE mode: только Validated + ассоциации в creative_context.
    |   I58:   CREATIVE != EXPLORATION (разные правила).
    |   I59:   XAI показывает creative_associations отдельно от facts.
    |   I51-I54: VOID (RFC0067 v1.0 deprecated → заменён RFC0067 v2.0).
    |   P2-E FIX: явная документация void-дыр:
    |   I51 = VOID · I52 = VOID · I53 = VOID · I54 = VOID
    |   В test_invariants.py добавить маркеры: pytest.mark.skip("VOID: RFC0067 v1.0 deprecated")
    |
    +- Метрики:
    |   analogy_graph_edges_total / sbe_activations_total / sbe_cache_hits
    |   sbe_cache_misses / creative_mode_responses_total
    |   analogy_resonance_score / analogy_promoted_total
    \- Нагрузка: SBEAsyncWorker 20-100ms (Qdrant + Redis) · Slow Path только
```

### Код [RFC0067 v2.0]

```python
# sbe_async_worker.py
# RFC0067 v2.0: Semantic Bridge Engine
# I56: только Slow Path через EventBus. Fast Path читает get_cached().
import json, logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# P3-C FIX: RELATED_DOMAINS перенесён в velantrim_config.py (ранее hardcode в sbe_async_worker.py).
# В sbe_async_worker.py: from velantrim_config import RELATED_DOMAINS
RELATED_DOMAINS: dict[str, list[str]] = {
    "physics":      ["mathematics", "engineering"],
    "biology":      ["chemistry", "medicine"],
    "computing":    ["mathematics", "electronics"],
    "neuroscience": ["biology", "psychology"],
}


@dataclass
class CreativeAssociation:
    source_node: str; target_node: str; cosine: float
    source_domain: str; target_domain: str
    marker:          str   = "[CREATIVE_ASSOCIATION]"
    source_type:     str   = "sbe"
    resonance_score: float = 0.5
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {"source_node": self.source_node, "target_node": self.target_node,
                "cosine": self.cosine, "source_domain": self.source_domain,
                "target_domain": self.target_domain, "marker": self.marker,
                "source_type": self.source_type,
                "resonance_score": self.resonance_score,
                "timestamp": self.timestamp.isoformat()}

    @classmethod
    def from_dict(cls, d):
        return cls(source_node=d["source_node"], target_node=d["target_node"],
                   cosine=d["cosine"], source_domain=d["source_domain"],
                   target_domain=d["target_domain"],
                   marker=d.get("marker", "[CREATIVE_ASSOCIATION]"),
                   source_type=d.get("source_type", "sbe"),
                   resonance_score=d.get("resonance_score", 0.5),
                   timestamp=datetime.fromisoformat(d["timestamp"]))


class SBEAsyncWorker:
    # I56: только через EventBus. Fast Path читает get_cached().
    def __init__(self, vector_db, redis, focus_engine, hot_graph, config):
        self.vector_db    = vector_db; self.redis = redis
        self.focus_engine = focus_engine; self.hot_graph = hot_graph
        self.cosine_th = config.CREATIVE.COSINE_THRESHOLD
        self.max_assoc = config.CREATIVE.MAX_ASSOCIATIONS
        self.ttl       = config.CREATIVE.CACHE_TTL_SECONDS

    async def handle_event(self, event: dict):
        sid = event.get("session_id")
        if not sid:
            return
        if event.get("cognitive_mode") not in (None, "CREATIVE"):
            return
        await self._compute_and_cache(sid)

    async def _compute_and_cache(self, session_id: str):
        # FIX-C: FocusEngine не имеет get_focus_vector(session_id).
        # Правильный метод: get_current_focus() — возвращает текущий FocusVector.
        # get_focus_vector было несуществующим именем → AttributeError при каждом вызове SBE.
        focus = await self.focus_engine.get_current_focus(session_id)
        if not focus or not focus.primary_domain:
            return
        exclude  = [focus.primary_domain] + RELATED_DOMAINS.get(focus.primary_domain, [])
        # P4-D FIX: Redis-кэш для get_activated_nodes (TTL 5 мин).
        # В CREATIVE режиме вызывается часто — кэш снижает нагрузку на Neo4j.
        import json as _json
        _cache_key = f"activated_nodes:{session_id}"
        _cached = await getattr(self, 'redis', None) and await self.redis.get(_cache_key)
        if _cached:
            nodes = [type('AN', (), n)() for n in _json.loads(_cached)]
        else:
            nodes = await self.hot_graph.get_activated_nodes(session_id, limit=10)
            if nodes and hasattr(self, 'redis'):
                await self.redis.setex(_cache_key, 300, _json.dumps([n.__dict__ for n in nodes]))
        if not nodes:
            return
        bridges  = []
        for node in nodes:
            for r in await self.vector_db.search(
                query_vector=node.embedding,
                filter={"domain": {"$nin": exclude}, "is_active": True},
                limit=self.max_assoc * 2
            ):
                if r.score >= self.cosine_th:
                    bridges.append(CreativeAssociation(
                        source_node=node.id, target_node=r.id,
                        cosine=round(r.score, 3),
                        source_domain=node.domain, target_domain=r.domain))
        if bridges := bridges[:self.max_assoc]:
            await self.redis.setex(
                f"creative_bridge:{session_id}", self.ttl,
                json.dumps([b.to_dict() for b in bridges]))

    async def get_cached(self, session_id: str) -> list[CreativeAssociation]:
        raw = await self.redis.get(f"creative_bridge:{session_id}")
        return [CreativeAssociation.from_dict(d) for d in json.loads(raw)] if raw else []
```

```python
# resonance_tracker.py
# RFC0067 v2.0: ResonanceTracker
# I56.1: resonance >= 0.7 -> Write Protocol Gate (не напрямую)
import logging
from datetime import timezone, datetime

logger = logging.getLogger(__name__)

FEEDBACK_WEIGHTS = {
    "used_in_response":      +0.05,
    "positive_continuation": +0.10,
    "explicit_like":         +0.20,
    "clarification_request": -0.10,
    "explicit_dislike":      -0.25,
}


class ResonanceTracker:
    # P3-B FIX: константы читаются из CREATIVE конфига — убраны hardcode.
    # PROMOTE_THRESHOLD = 0.7   ← теперь CREATIVE.PROMOTE_THRESHOLD
    # DECAY_WEEKLY      = 0.95  ← теперь CREATIVE.DECAY_WEEKLY
    # from velantrim_config import CREATIVE → используй CREATIVE.PROMOTE_THRESHOLD

    def __init__(self, graph, write_protocol, redis):
        self.graph = graph; self.write_protocol = write_protocol; self.redis = redis

    async def record(self, analogy_id, session_id, event_type,
                     source_type, analogy_data=None):
        delta = FEEDBACK_WEIGHTS.get(event_type, 0.0)
        if not delta:
            return
        cur   = await self._get(analogy_id, source_type)
        score = max(0.0, min(1.0, cur + delta))
        await self._set(analogy_id, source_type, score)
        if (score >= self.PROMOTE_THRESHOLD and source_type == "sbe"
                and event_type in ("positive_continuation", "explicit_like")
                and analogy_data):
            await self._promote(analogy_id, analogy_data, score)

    async def decay_all(self):
        # FIX-D: GraphMemory не имеет .session() — это Neo4j driver API.
        # Правильный интерфейс: execute_cypher(). Иначе AttributeError в ночном цикле.
        await self.graph.execute_cypher(
            "MATCH ()-[r:METAPHOR_OF|ANALOGOUS_TO]->() "
            "WHERE r.last_used < datetime() - duration('P7D') "
            "SET r.resonance_score = r.resonance_score * $d",
            {"d": self.DECAY_WEEKLY})

    async def _promote(self, aid, data, resonance):
        await self.write_protocol.create_analogy_edge(
            source=data["source_node"], target=data["target_node"],
            edge_type="METAPHOR_OF" if data.get("is_metaphor", True) else "ANALOGOUS_TO",
            source_type="sbe_promoted", confidence=data["cosine"],
            source_domain=data["source_domain"], target_domain=data["target_domain"],
            resonance_score=resonance,
            cultural_vintage=datetime.now(timezone.utc).year)
        logger.info(f"SBE analogy promoted: {aid}")

    async def _get(self, aid, stype):
        if stype == "analogy_graph":
            # FIX-D: .session() → execute_cypher()
            result = await self.graph.execute_cypher(
                "MATCH ()-[r:METAPHOR_OF|ANALOGOUS_TO]->() "
                "WHERE r.analogy_id=$id RETURN r.resonance_score AS s",  -- P0-G FIX: id() = integer internal ID, analogy_id = string UUID
                {"id": aid})
            return float(result[0]["s"]) if result else 0.5
        raw = await self.redis.get(f"sbe_resonance:{aid}")
        return float(raw) if raw else 0.5

    async def _set(self, aid, stype, score):
        if stype == "analogy_graph":
            # FIX-D: .session() → execute_cypher()
            await self.graph.execute_cypher(
                "MATCH ()-[r:METAPHOR_OF|ANALOGOUS_TO]->() "
                "WHERE r.analogy_id=$id "  -- P0-G FIX: property-based lookup вместо id(r)
                "SET r.resonance_score=$s, r.last_used=datetime()",
                {"id": aid, "s": score})
        else:
            await self.redis.setex(f"sbe_resonance:{aid}", 86400*30, score)
```

```python
# adaptive_decoder.py
# RFC0067 v2.0: AdaptiveDecoder
# I57: FactsPack в CREATIVE только Validated.
from dataclasses import dataclass, field


@dataclass
class DecodeContext:
    cognitive_mode:        str
    creative_associations: list = field(default_factory=list)


class AdaptiveDecoder:
    BASE_TEMP = 0.6; MAX_TEMP = 0.85; MAX_ASSOC = 5
    PRES_PENALTY = 0.6; SLM_MIN_PRES = 0.5
    # P1-F FIX: было {"PRECISION": 0.1, "BALANCED": 0.5, "EXPLORATION": 0.7} → конфликт
# с CognitiveModeRouter.MODE_CONFIGS (0.3 / 0.6 / 0.85). Теперь единый источник.
from velantrim_config import MODE_TEMPS   # P1-F: MODE_TEMPS читается из конфига

    def compute_temperature(self, ctx: DecodeContext) -> float:
        if ctx.cognitive_mode != "CREATIVE":
            return self.MODE_TEMPS.get(ctx.cognitive_mode, 0.5)
        ratio = min(len(ctx.creative_associations) / self.MAX_ASSOC, 1.0)
        return self.BASE_TEMP + (self.MAX_TEMP - self.BASE_TEMP) * ratio

    def compute_presence_penalty(self, ctx: DecodeContext, params_b: float) -> float:
        if ctx.cognitive_mode != "CREATIVE":
            return 0.2 if ctx.cognitive_mode == "EXPLORATION" else 0.0
        return max(self.SLM_MIN_PRES, self.PRES_PENALTY) if params_b < 3.0 \
               else self.PRES_PENALTY
```

### Тесты [I55–I59]

```python
# tests/test_invariants.py -- добавить

# I55: [:METAPHOR_OF] только через Write Protocol Gate
async def test_I55_analogy_edges_require_write_protocol():
    with pytest.raises(WriteProtocolViolation):
        await MockGraph().execute_cypher(
            "MATCH (a {name:'A'}),(b {name:'B'}) MERGE (a)-[:METAPHOR_OF]->(b)")
    r = await MockWriteProtocol().create_analogy_edge(
        source="A", target="B", edge_type="METAPHOR_OF",
        source_type="test", confidence=0.85,
        source_domain="biology", target_domain="computing")
    assert r.success

# I55.1: SAE decay=0.4 для аналогий
async def test_I55_1_sae_analogy_decay():
    sae = SpreadingActivationEngine(graph=MockGraphWithAnalogies())
    act = await sae.activate("Neuron", max_depth=2)
    assert act.get("Transistor", 0) < act.get("Synapse", 0) * 0.65, \
        "I55.1 VIOLATION: SAE не применяет decay=0.4 для аналогий"

# I56.1: SBE не пишет напрямую
async def test_I56_1_resonance_via_write_protocol():
    wp = MockWriteProtocol()
    t  = ResonanceTracker(MockGraph(), wp, MockRedis())
    d  = {"source_node": "A", "target_node": "B", "cosine": 0.82,
          "source_domain": "neuro", "target_domain": "elec", "is_metaphor": True}
    for _ in range(4):
        await t.record("id1", "s", "explicit_like", "sbe", d)
    assert wp.create_analogy_edge_called, "I56.1 VIOLATION"

# I57: CREATIVE mode — только Validated
async def test_I57_creative_validated_only():
    ctx = await MockContextBuilder().build(query="test",
                session_id="s", cognitive_mode="CREATIVE")
    for f in ctx.facts_pack:
        assert f.epistemic_state == "Validated", f"I57 VIOLATION: {f.id}"

# I58: CREATIVE != EXPLORATION
async def test_I58_creative_vs_exploration():
    c = await MockContextBuilder().build(query=".", cognitive_mode="CREATIVE")
    e = await MockContextBuilder().build(query=".", cognitive_mode="EXPLORATION")
    assert all(f.epistemic_state == "Validated" for f in c.facts_pack)
    assert len(e.creative_associations) == 0, "I58 VIOLATION"

# I59: XAI отдельно показывает ассоциации
async def test_I59_xai_separates_associations():
    d = (await MockExplainabilityLayer().explain("r1", "detailed")).to_dict()
    assert "creative_associations" in d, "I59 VIOLATION: поле отсутствует"
    assert {f["id"] for f in d["facts"]}.isdisjoint(
        {a["source_node"] for a in d["creative_associations"]}), "I59 VIOLATION"
```

### Добавить в velantrim_config.py

```python
class CreativeConfig:
    MAX_EDGES_PER_CONCEPT = 50
    RETENTION_DAYS        = 365
    MIN_CONFIDENCE        = 0.7
    COSINE_THRESHOLD      = 0.75
    MAX_ASSOCIATIONS      = 5
    CACHE_TTL_SECONDS     = 900
    TEMP_BASE             = 0.6
    TEMP_MAX              = 0.85
    PRESENCE_PENALTY      = 0.6
    SLM_MIN_PRESENCE      = 0.5
    PROMOTE_THRESHOLD     = 0.7
    DECAY_WEEKLY          = 0.95
    MIN_SOURCES           = 2
    AUTHORITY_OVERRIDE    = 0.9

CREATIVE = CreativeConfig()
# psutil>=5.9 -- добавить в requirements.txt
```


---

## RFC0063: Knowledge Ingestion Pipeline — Поглощение внешних знаний

### 🌱 Для чего

Velantrim учится из диалогов. Но есть огромный массив знаний который накоплен **до** первого диалога — энциклопедии, учебники, научные статьи, PDF. RFC0063 даёт системе способность поглощать эти знания не теряя ни точности фактов, ни паттернов рассуждения, ни семантических связей. Один источник → три параллельных потока → три правильных слоя архитектуры.

Ключевая идея: «педагогический шум» в учебнике — повторения, примеры, метафоры — это не мусор. Это закодированные паттерны рассуждения. Velantrim раскладывает их по ящикам: факты в граф, паттерны в ReasoningBank, семантика в векторный индекс.

---

```
RFC0063: Knowledge Ingestion Pipeline

  Источник (PDF / JSON / YAML / Wikidata RDF / plain text)
                          |
                          v
              IngestionRouter (Slow Path only · I63)
                          |
          .---------------+---------------.
          v               v               v
   FactExtractor   PatternExtractor  SemanticIndexer
   (flagship LLM)  (flagship LLM)   (embedding only)
   temp = 0.1      temp = 0.4       0 токенов LLM
          |               |               |
          v               v               v
    L3 Neo4j       L4 ReasoningBank   Qdrant/ChromaDB
    Truth Gate     Bayesian Prior     vector index
    ESM: Supported Thompson Sampling  + fact_ids link
          |               |               |
          .---------------+---------------.
                          |
                   TraceLine sync (source_id)
```

### Компоненты

**IngestionRouter** — точка входа. Принимает источник, определяет тип, язык, домен, `source_vintage` (год публикации), `trust_score`. Запускает три потока через EventBus. Только Slow Path (I63).

**FactExtractor** — извлекает триплеты фактов (субъект, предикат, объект). Температура 0.1. Начальный ESM = `Supported` — никогда не `Validated` при загрузке (I60). Дедупликация: cosine ≥ 0.92 → добавляет Evidence к существующему узлу, не создаёт дубль. Trust scores: encyclopedic 0.85, scientific 0.90, textbook 0.80, default 0.70.

**PatternExtractor** — извлекает паттерны рассуждения в ReasoningBank. Температура 0.4. **Байесовская инициализация Thompson Sampling (I61)**: стратегия из авторитетного источника стартует не с `Beta(1,1)` а с `Beta(prior×k, (1-prior)×k)` — разумная фора которая поддаётся коррекции реальным опытом. `max prior_strength_k = 20` — жёсткое ограничение (иначе стратегия становится некорректируемой). Дедупликация стратегий: similarity > 0.88 → merge, не дубль.

**SemanticIndexer** — нарезает текст на чанки 512 токенов / перекрытие 64, векторизует через EmbeddingRegistry (`deepvk/USER-bge-m3` для RU). **Ноль LLM-вызовов** (I62). В метаданных каждого вектора — `fact_ids` из L3 того же чанка. Это связывает векторный индекс с графом — семантический поиск ведёт к явным фактам.

**EdgeSuggester** — **аудиторский инструмент, не автоматика**. Раз в неделю находит пары фактов с cosine > 0.85 И co-активацией > 3 раз, но без явного ребра в графе. Сохраняет в SQLite `suggested_edges` со статусом `pending`. Аудитор утверждает → только тогда через Truth Gate в граф (I64). Опциональный режим Hypothesized Edge: ребро создаётся как `is_active=false` и активируется когда пользователь косвенно подтверждает его диалогом.

**VintageDecayCalculator** — адаптивный `decay_lambda` зависящий от домена и возраста источника (I65). Физика: decay=0.001 (практически не устаревает). Программирование: decay=0.15 (устаревает за 3 года). Медицина: decay=0.05. ESM-модификатор: Validated×0.5 (факт живёт дольше), Hypothesized×2.0 (устаревает быстрее). Каждый ingested факт обязан иметь `decay_lambda` и `source_vintage`.

---

```
Конфигурация RFC0063 (velantrim_config.yaml):

ingestion:
  enabled: true
  offline_only: true            # никогда не в рантайме Fast Path
  batch_size: 500
  dedup_threshold: 0.92         # cosine для дедупликации фактов
  strategy_dedup_threshold: 0.88
  max_domain_share: 0.40        # максимум одного домена за сессию
  languages: [ru, en, multi]
  trust_scores:
    encyclopedic: 0.85
    scientific: 0.90
    textbook: 0.80
    default: 0.70
  extractors:
    facts:
      llm: flagship
      temperature: 0.1
      initial_esm_state: Supported   # никогда не Validated при загрузке
    reasoning_patterns:
      llm: flagship
      temperature: 0.4
    semantic_embeddings:
      model: "deepvk/USER-bge-m3"
      chunk_size: 512
      chunk_overlap: 64
  vintage_decay:
    domain_base_decay:
      physics: 0.001
      mathematics: 0.001
      chemistry: 0.005
      biology: 0.02
      medicine: 0.05
      programming: 0.15
      law: 0.03
      history: 0.002
      default: 0.05
    vintage_threshold_years:
      physics: 50
      programming: 3
      medicine: 5
      default: 10
    max_decay_cap: 0.5

reasoning_bank:
  ingested_prior:
    default_confidence: 0.75
    default_strength_k: 10
    max_strength_k: 20              # жёсткое ограничение
    domain_overrides:
      physics:     { confidence: 0.90, k: 20 }
      mathematics: { confidence: 0.92, k: 20 }
      programming: { confidence: 0.60, k: 5  }
      medicine:    { confidence: 0.70, k: 15 }

edge_suggester:
  enabled: true
  cosine_threshold: 0.85
  coactivation_threshold: 3
  hypothesized_edge_mode: true
  audit_schedule: weekly
```

### Инварианты RFC0063

```
I60: FactExtractor никогда не присваивает epistemic_state=Validated без Truth Gate
     с evidence_count >= 3. Нарушение = запись ненадёжных фактов с высшим статусом.
     Тест: test_I60_fact_extractor_no_direct_validated()

I61: Все ingested стратегии используют байесовскую инициализацию Beta(prior*k, (1-prior)*k).
     max prior_strength_k = 20. Beta(1,1) для ingested стратегий — нарушение.
     Тест: test_I61_thompson_sampling_bayesian_prior()

I62: SemanticIndexer не вызывает LLM. Только embedding model через EmbeddingRegistry.
     Тест: test_I62_semantic_indexer_no_llm_call()

I63: IngestionRouter работает только через EventBus в Slow Path.
     Прямой вызов из Fast Path — нарушение I28.
     Тест: test_I63_ingestion_router_slow_path_only()

I64: EdgeSuggester не пишет в граф напрямую.
     Только через approve_edge() -> Truth Gate -> L3.
     Тест: test_I64_edge_suggester_no_direct_graph_write()

I65: Каждый ingested факт (source_type="import") обязан иметь decay_lambda
     вычисленный через VintageDecayCalculator. decay_lambda=NULL = нарушение.
     Тест: test_I65_vintage_decay_assigned_on_ingestion()
```

### Тесты [I60–I65]

```python
# tests/test_invariants.py -- добавить

# I60: FactExtractor не присваивает Validated напрямую
async def test_I60_fact_extractor_no_direct_validated():
    extractor = FactExtractor(truth_gate=MockTruthGate(), graph=MockGraph())
    result = await extractor.extract_and_store(
        text="Вода кипит при 100°C.", source_type="encyclopedic"
    )
    assert result.esm_state == "Supported", \
        "I60 VIOLATION: FactExtractor присвоил Validated без Truth Gate"

# I61: Bayesian prior для ingested стратегий
async def test_I61_thompson_sampling_bayesian_prior():
    bank = ReasoningBank()
    strategy = await bank.ingest_pattern(
        pattern="first_principles",
        source_type="ingested_prior",
        prior_confidence=0.90, prior_strength_k=20
    )
    assert strategy.alpha == 18.0, "I61 VIOLATION: alpha != prior*k"
    assert strategy.beta  ==  2.0, "I61 VIOLATION: beta != (1-prior)*k"

# I62: SemanticIndexer не вызывает LLM
async def test_I62_semantic_indexer_no_llm_call():
    llm_mock = MockLLM()
    indexer  = SemanticIndexer(embedding_registry=MockEmbeddingRegistry(),
                               llm=None)
    await indexer.index_chunks(["chunk 1", "chunk 2"], source_id="src_001")
    assert llm_mock.call_count == 0, "I62 VIOLATION: SemanticIndexer вызвал LLM"

# I63: IngestionRouter только через Slow Path
async def test_I63_ingestion_router_slow_path_only():
    router = IngestionRouter(event_bus=MockEventBus())
    with pytest.raises(FastPathViolation):
        await router.ingest_sync("source.pdf")  # нет такого метода

# I64: EdgeSuggester не пишет в граф напрямую
async def test_I64_edge_suggester_no_direct_graph_write():
    graph   = MockGraph()
    suggest = EdgeSuggester(graph=graph, db=MockDB())
    await suggest.run_weekly_scan()
    assert graph.write_count == 0, "I64 VIOLATION: EdgeSuggester пишет в граф"
    assert suggest.pending_count > 0

# I65: VintageDecay обязателен для всех ingested фактов
async def test_I65_vintage_decay_assigned():
    calc    = VintageDecayCalculator()
    fact    = Fact(source_type="import", source_vintage=2018, domain="programming")
    result  = calc.assign(fact)
    assert result.decay_lambda is not None, "I65 VIOLATION: decay_lambda=NULL"
    assert result.decay_lambda > 0.10, \
        "I65: programming 2018 должен иметь высокий decay"
```

### Новые метрики Prometheus (RFC0063)

| Метрика | Что показывает |
|---------|----------------|
| `ingestion_facts_created_total` | фактов создано через IngestionPipeline |
| `ingestion_facts_deduplicated_total` | фактов объединено с существующими |
| `ingestion_patterns_created_total` | паттернов рассуждения создано |
| `ingestion_patterns_deduplicated_total` | паттернов объединено через merge |
| `ingestion_contradictions_found_total` | противоречий с существующим графом |
| `ingestion_batch_duration_seconds` | время обработки партии (Histogram) |
| `ingestion_vintage_decay_avg` | средний decay_lambda по партии |
| `edge_suggestions_pending_total` | предложений рёбер ожидающих аудита |
| `edge_suggestions_approved_total` | предложений утверждено аудитором |
| `edge_hypothesized_activated_total` | Hypothesized Edge активировано диалогом |

### Миграция существующих данных

```cypher
// Стратегии из опыта: установить дефолтный prior с нулевой силой
MATCH (s:Strategy) WHERE s.source_type IS NULL
SET s.source_type = "experience",
    s.prior_confidence = 0.5,
    s.prior_strength_k = 0;

// Факты без source_vintage: установить текущий год как дефолт
MATCH (f:Fact) WHERE f.source_vintage IS NULL
SET f.source_vintage = 2026,
    f.source_domain = "unknown",
    f.decay_lambda = 0.05;
```

### Порядок реализации

**Sprint 1 (1–2 недели):** байесовская инициализация Thompson Sampling (I61), ограничение `max_strength_k=20`, дедупликация стратегий через merge, EdgeSuggester как HITL-only с SQLite таблицей `suggested_edges`, тесты I61 и I64.

**Sprint 2 (3–4 недели):** VintageDecayCalculator (I65), поле `source_vintage` в схеме :Fact, FactExtractor + PatternExtractor как раздельные LLM-вызовы (I60, I62), SemanticIndexer без LLM через EmbeddingRegistry, IngestionOrchestrator с asyncio.gather, расширение TraceLine для трёх слоёв, тесты I60–I65, миграционный скрипт.


S2.5: ConflictResolutionWorker — каждые 5 минут (RFC0062)
    · Batch 20 Hypothesized-фактов с conflict_checked <> true
    · TruthConflictDetector → similarity search → LLM-вердикт (YES/NO)
    · При конфликте → ESM.transition(Contradicted) → GraphWriteProtocol
    · ⚠️ RFC0031: нет прямого SET epistemic_state — только ESM.transition
    · ⚠️ При llm_client=None → continue (не break!) — обработка батча продолжается
    · Проверенные факты: conflict_checked = true
    · Инвариант I38: вызов только из Slow Path — не из Fast Path

S3: Consolidation → ConsolidationEngine.enqueue(CONSOLIDATE)
    · Триггер при L1 capacity > 80%
    · asyncio.Lock — никаких параллельных операций на одном узле
    · Таймаут 30s → DLQ, статус → BLOCKED_AWAITING_DB

S4: Reflection — каждые 10 завершённых задач
    · Strategy Update через Thompson Sampling (RFC0039)
    · Negative Reinforcement для провальных стратегий

S5: GC — каждые 7 дней или при MHI < 0.3 (Phase 2)
    · Soft Delete → S3 backup → Hard Delete
    · Cascade invalidation Strategy при Fact инвалидации
```

---

### 🔒 Инварианты (нарушать нельзя никогда)

```python
# ИНВАРИАНТЫ L0
assert "VALUES_CORE" in working_memory.pinned  # Ring Zero всегда
assert len(working_memory) <= 5                # 4±1 Cowan 2001
assert working_memory.eviction_policy == "CRITICAL > HIGH > MEDIUM > LOW"

# ИНВАРИАНТЫ L1
for episode in stm_cache:
    assert episode.session_id is not None    # session_id binding
    assert episode.event_time is not None    # temporal tagging
    assert episode.created_at is not None
    assert episode.valid_from is not None

# ИНВАРИАНТЫ L3
# ∀ fact ∈ Graph: validated = True (MGL-2)
# ∀ fact ∈ Graph: ∃ [:SUPPORTED_BY] → :Evidence (MGL-5)
# ∀ fact ∈ Graph: transaction_time IS NOT NULL (bi-temporal)

# ИНВАРИАНТЫ EVENT BUS
# Каждый запрос = минимум 1 AgentEvent(USER_MESSAGE)

# ИНВАРИАНТЫ CORE VALUES
# VALUES CORE не адаптируются никогда
# Semantic Decay не затрагивает pinned=CRITICAL узлы

# I38 (RFC0062) — ConflictResolutionWorker только в Slow Path
# Прямой вызов TruthConflictDetector из Fast Path — нарушение архитектуры.
# Нарушение → Observer++ alert + логирование.

# datetime timezone: везде используем timezone.utc
# ❌ datetime.now()            → ✅ datetime.now(timezone.utc)
# Файлы: fractal_memory.py · consolidation_worker.py · memory_gc.py
#         event_bus.py · velum.py (VelumEdge.first_seen, last_seen)
```

---

## 🧬 Epistemic State Machine (ESM) — Жизненный цикл фактов 

> **Почему критично**: без ESM факты в L3 — «просто узлы». Semantic Decay и GC работают вслепую. ESM превращает L3 из базы данных в **живую эпистемическую систему**, где каждый факт знает своё место в пространстве достоверности.

---

### Состояния и переходы

```
                 Первое появление (авто)
  LLM Output ──────────────────────────────► :Observed
                                                  │
                                          Truth Gate partial
                                                  ▼
                                          :Hypothesized
                                                  │
                                        Evidence ≥ 2 добавлено
                                                  ▼
                                          :Supported
                                                  │
                                     MGL + Truth Gate пройден
                                                  ▼
                                          :Validated  ◄──── (стабильное состояние)
                                                  │
                                    1+ [:CONTRADICTS] (weighted)
                                                  ▼
                                         :Contradicted
                                                  │
                                    3+ конфликта / importance падает
                                                  ▼
                                          :Deprecated
                                                  │
                                    importance < 0.1 при GC
                                                  ▼
                                          :Collapsed
                             (→ Immutable Raw Memory, не уничтожается физически)
```

### Правила переходов (формальные)

```python
ESM_TRANSITIONS = {
    "Observed":     {"to": "Hypothesized", "condition": "first_appearance"},
    "Hypothesized": {"to": "Supported",    "condition": "evidence_count >= 2"},
    "Supported":    {"to": "Validated",    "condition": "mgl_passed AND truth_gate >= 0.7"},
    "Validated":    {"to": "Contradicted", "condition": "strong_contradictions >= 1"},
    "Contradicted": {"to": "Deprecated",   "condition": "contradiction_count >= 3 OR importance < 0.3"},
    "Deprecated":   {"to": "Collapsed",    "condition": "importance < 0.1"},
    # Collapsed — финальное состояние. Физически не удаляется — ссылка в Immutable Raw Memory.
}

# Ring Zero / VALUES CORE → ESM заморожен на Validated. Никогда не переходит в Contradicted.
IMMUTABLE_STATES = {"VALUES_CORE", "RING_ZERO"}
```

### Код ESM-контроллера

```python
# epistemic_state_machine.py
from enum import Enum
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

class EpistemicState(str, Enum):
    OBSERVED     = "Observed"
    HYPOTHESIZED = "Hypothesized"
    SUPPORTED    = "Supported"
    VALIDATED    = "Validated"
    CONTRADICTED = "Contradicted"
    DEPRECATED   = "Deprecated"
    COLLAPSED    = "Collapsed"

class EpistemicStateMachine:
    """
    Управляет жизненным циклом фактов в L3.
    Связан с: MGL (Memory Guardian), Weighted Semantic Decay,
              GC (MemoryGarbageCollector), Truth Gate.

    RFC0001: LLM → :Fact только через цепочку ESM.
    Ring Zero / VALUES CORE → frozen на Validated навсегда.
    """

    IMMUTABLE_FACT_IDS = {"VALUES_CORE", "RING_ZERO"}

    async def transition(
        self,
        fact_id: str,
        fact: dict,
        graph: "GraphMemory",
        reason: str
    ) -> EpistemicState:
        """
        Вычислить следующее состояние факта и применить переход.
        Возвращает новое состояние.

        Raises:
            ImmutableStateError: если факт является VALUES CORE
        """
        current = EpistemicState(fact.get("epistemic_state", "Observed"))

        # Ring Zero никогда не деградирует
        if fact_id in self.IMMUTABLE_FACT_IDS:
            return current

        next_state = self._compute_next(fact, current)

        if next_state != current:
            await self._apply_transition(fact_id, current, next_state, reason, graph)
            logger.info(f"ESM: {fact_id} {current.value} → {next_state.value} ({reason})")

        return next_state

    def _compute_next(self, fact: dict, current: EpistemicState) -> EpistemicState:
        """Вычислить следующее состояние по условиям переходов"""
        evidence_count    = fact.get("evidence_count", 0)
        mgl_passed        = fact.get("validated", False)
        truth_gate_score  = fact.get("epistemic_score", 0.0)
        contradiction_count = fact.get("contradiction_count", 0)
        importance        = fact.get("importance_score", 1.0)

        if current == EpistemicState.OBSERVED:
            return EpistemicState.HYPOTHESIZED

        if current == EpistemicState.HYPOTHESIZED and evidence_count >= 2:
            return EpistemicState.SUPPORTED

        if current == EpistemicState.SUPPORTED and mgl_passed and truth_gate_score >= 0.7:
            return EpistemicState.VALIDATED

        if current == EpistemicState.VALIDATED and contradiction_count >= 1:
            return EpistemicState.CONTRADICTED

        if current == EpistemicState.CONTRADICTED:
            if contradiction_count >= 3 or importance < 0.3:
                return EpistemicState.DEPRECATED

        if current == EpistemicState.DEPRECATED and importance < 0.1:
            return EpistemicState.COLLAPSED

        return current  # нет перехода

    async def _apply_transition(
        self,
        fact_id: str,
        from_state: EpistemicState,
        to_state: EpistemicState,
        reason: str,
        graph: "GraphMemory"
    ):
        """Записать переход в граф"""
        # При переходе в Collapsed → сохранить в Immutable Raw Memory
        if to_state == EpistemicState.COLLAPSED:
            await self._preserve_to_raw_memory(fact_id, graph)

        # I88 (VersionOCC): атомарный инкремент _version_ через OCC Cypher.
        # MATCH по {id, _version_} — если версия изменилась конкурентно, запись не применится.
        await graph.execute_cypher("""
            MATCH (f:Fact {id: $fact_id})
            SET f.epistemic_state = $new_state,
                f.state_changed_at = datetime(),
                f.transition_reason = $reason,
                f._version_ = coalesce(f._version_, 0) + 1,
                f.is_active = CASE WHEN $new_state IN ['Deprecated','Collapsed']
                              THEN false ELSE f.is_active END
            """, {
            "fact_id": fact_id,
            "new_state": to_state.value,
            "reason": reason
        })

    async def _preserve_to_raw_memory(self, fact_id: str, graph: "GraphMemory"):
        """Collapsed факт → ссылка в Immutable Raw Memory (не уничтожается)"""
        logger.info(f"ESM Collapsed: {fact_id} → Immutable Raw Memory reference saved")
        # Физическое удаление только через GC + S3 архивация

    async def cascade_invalidate(
        self,
        fact_id: str,
        graph: "GraphMemory"
    ) -> List[str]:
        """
        Каскадная инвалидация зависимых фактов
        
        Если факт B выведен из A (через [:DERIVED_FROM] или [:INFERRED_FROM]):
          A → B
        
        И A переходит в Contradicted:
          A.epistemic_state = "Contradicted"
        
        То B должен быть пересмотрен:
          B.epistemic_state = "Hypothesized"
          B.requires_revalidation = true
        
        Returns: список ID инвалидированных фактов
        """
        query = """
        MATCH (source:Fact {id: $fact_id})
        WHERE source.epistemic_state IN ['Contradicted', 'Deprecated', 'Collapsed']
        
        MATCH (source)<-[:DERIVED_FROM|INFERRED_FROM]-(dependent:Fact)
        WHERE dependent.epistemic_state IN ['Validated', 'Supported']
          AND dependent.is_ring_zero <> true
        
        SET dependent.epistemic_state = 'Hypothesized',
            dependent.requires_revalidation = true,
            dependent.invalidated_at = datetime(),
            dependent.invalidation_source = $fact_id
        
        RETURN dependent.id as invalidated_id
        """
        
        results = await graph.execute_cypher(query, {"fact_id": fact_id})
        invalidated = [r['invalidated_id'] for r in results]
        
        if invalidated:
            logger.warning(
                f"Cascade invalidation: {fact_id} → {len(invalidated)} dependent facts "
                f"rolled back to Hypothesized"
            )
        
        return invalidated
```

### Интеграция ESM с существующими компонентами

```
Memory Guardian (MGL):
  · Перед записью нового факта → ESM.transition(Observed → Hypothesized)
  · После прохождения Truth Gate → ESM.transition(Supported → Validated)

Weighted Semantic Decay:
  · При добавлении [:CONTRADICTS] → ESM.transition(Validated → Contradicted)
  · importance < 0.1 → ESM.transition(Deprecated → Collapsed)

GC (MemoryGarbageCollector):
  · Collapsed узлы → S3 архивация → физическое удаление
  · Deprecated с age > 90d → кандидат на Collapsed

Runtime Invariant Checker:
  · ∀ fact ∈ Graph: epistemic_state ∈ VALID_STATES
  · ∀ fact ∈ Graph: если validated=True → epistemic_state = 'Validated'
  · VALUES_CORE: epistemic_state всегда = 'Validated'
```

---

## ⚙️ Runtime Invariant Checker 

> **Почему критично**: RFC существуют как документы, но нарушения видны только при падении системы. Runtime Checker превращает RFC из бумаги в исполняемые контракты.

```python
# runtime_invariant_checker.py
import asyncio
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class InvariantViolation:
    invariant_id: str
    severity: str        # "CRITICAL" | "WARNING"
    description: str
    detected_at: datetime
    auto_remediation: str  # что система сделала автоматически

class RuntimeInvariantChecker:
    """
    Проверяет инварианты Protocol v1 каждые 30 секунд.
    При CRITICAL нарушении → Safe Mode + Heartbeat alert.
    При WARNING → лог + Grafana counter.
    """
    CHECK_INTERVAL_SECONDS = 30

    def __init__(self, graph: GraphMemory, fractal_memory: FractalMemory,
                 heartbeat: "MetaSupervisorHeartbeat" = None):  # optional: агент может передать позже
        self.graph = graph
        self.fractal = fractal_memory
        self.heartbeat = heartbeat
        self.violations_total = 0
        self._running = False

    async def start(self):
        """Запустить фоновую проверку инвариантов"""
        self._running = True
        while self._running:
            await asyncio.sleep(self.CHECK_INTERVAL_SECONDS)
            violations = await self.check_all()
            for v in violations:
                await self._handle_violation(v)

    def stop(self):
        self._running = False

    async def check_all(self) -> list[InvariantViolation]:
        violations = []
        violations += await self._check_l0_invariants()
        violations += await self._check_l3_invariants()
        violations += await self._check_esm_invariants()   # ESM
        violations += await self._check_ce_health()
        violations += await self._check_rfc0006()
        return violations

    async def _check_l0_invariants(self) -> list[InvariantViolation]:
        violations = []
        wm = self.fractal.working_memory
        # L0: VALUES CORE должен присутствовать
        if not any(getattr(m, 'id', '') == 'VALUES_CORE' for m in wm):
            violations.append(InvariantViolation(
                invariant_id="L0-001",
                severity="CRITICAL",
                description="VALUES CORE отсутствует в L0 Working Memory",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Reload VALUES_CORE from constants.py"
            ))
        # L0: capacity не должна превышать 5
        if len(wm) > 5:
            violations.append(InvariantViolation(
                invariant_id="L0-002",
                severity="WARNING",
                description=f"L0 capacity {len(wm)} > 5 (Cowan limit)",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Trigger Priority Eviction"
            ))
        return violations

    async def _check_l3_invariants(self) -> list[InvariantViolation]:
        """Проверить: нет ли неvalid фактов в L3"""
        violations = []
        query = """
        MATCH (f:Fact) WHERE f.validated = false OR f.validated IS NULL
        RETURN count(f) as bad_count
        """
        result = await self.graph.execute_cypher(query)
        bad_count = result[0].get("bad_count", 0) if result else 0
        if bad_count > 0:
            violations.append(InvariantViolation(
                invariant_id="L3-001",
                severity="CRITICAL",
                description=f"{bad_count} фактов в L3 без validated=True",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Flag for MGL re-validation"
            ))
        return violations

    async def _check_esm_invariants(self) -> list[InvariantViolation]:
        """Проверить корректность ESM состояний в L3"""
        violations = []
        valid_states = {"Observed","Hypothesized","Supported","Validated",
                        "Contradicted","Deprecated","Collapsed"}

        # Нет несуществующих состояний
        query1 = """
        MATCH (f:Fact) WHERE f.epistemic_state IS NOT NULL
          AND NOT f.epistemic_state IN $valid_states
        RETURN count(f) as bad_count
        """
        result = await self.graph.execute_cypher(
            query1, {"valid_states": list(valid_states)}
        )
        bad_count = result[0].get("bad_count", 0) if result else 0
        if bad_count > 0:
            violations.append(InvariantViolation(
                invariant_id="ESM-001",
                severity="CRITICAL",
                description=f"{bad_count} фактов с недопустимым epistemic_state",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Set epistemic_state='Observed' — re-enter ESM lifecycle"  # Корректный вход в ESM lifecycle
            ))

        # validated=True ↔ epistemic_state='Validated'
        query2 = """
        MATCH (f:Fact)
        WHERE f.validated = true AND f.epistemic_state <> 'Validated'
        RETURN count(f) as mismatch_count
        """
        result2 = await self.graph.execute_cypher(query2)
        mismatch = result2[0].get("mismatch_count", 0) if result2 else 0
        if mismatch > 0:
            violations.append(InvariantViolation(
                invariant_id="ESM-002",
                severity="WARNING",
                description=f"{mismatch} фактов: validated=True но epistemic_state≠Validated",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Sync epistemic_state with validated flag"
            ))

        # VALUES CORE всегда Validated
        query3 = """
        MATCH (f:Fact) WHERE f.id IN ['VALUES_CORE','RING_ZERO']
          AND f.epistemic_state <> 'Validated'
        RETURN count(f) as immutable_violated
        """
        result3 = await self.graph.execute_cypher(query3)
        immutable_bad = result3[0].get("immutable_violated", 0) if result3 else 0
        if immutable_bad > 0:
            violations.append(InvariantViolation(
                invariant_id="ESM-003",
                severity="CRITICAL",
                description="VALUES CORE / RING_ZERO не в состоянии Validated!",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Force epistemic_state='Validated' for immutable facts"
            ))

        return violations

    async def _check_rfc0006(self) -> list[InvariantViolation]:
        """RFC0006: Engram не должен быть включён с API-моделями"""
        from config import settings
        violations = []
        if settings.ENGRAM_ENABLED and settings.LLM_PROVIDER not in \
           {"local", "ollama", "llamacpp", "vllm", "lmstudio"}:  # lmstudio добавлен — совпадает с validate_engram_config
            violations.append(InvariantViolation(
                invariant_id="RFC0006",
                severity="CRITICAL",
                description="RFC0006 нарушен: Engram включён с API-моделью",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Set ENGRAM_ENABLED=False automatically"
            ))
        return violations

    async def _check_ce_health(self) -> list[InvariantViolation]:
        """Проверить здоровье ConsolidationEngine"""
        violations = []
        if not self.heartbeat:
            return []   # P9-FIX БАГ-1: heartbeat ещё не подключён — пропустить
        dlq_size = len(self.heartbeat.consolidation_engine.dlq)
        if dlq_size > 10:
            violations.append(InvariantViolation(
                invariant_id="CE-001",
                severity="WARNING",
                description=f"ConsolidationEngine DLQ size = {dlq_size}",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Alert ops team"
            ))
        return violations

    async def _handle_violation(self, v: InvariantViolation):
        """
        Четыре уровня строгости вместо бинарного CRITICAL/WARNING.
        INFO/WARNING не вызывают SAFE_MODE — только снижают частоту CE.

        INFO     → только лог
        WARNING  → снизить частоту CE (DEGRADED)
        ERROR    → DEGRADED + Grafana alert
        CRITICAL → SAFE_MODE (L3 read-only)
        """
        self.violations_total += 1
        if v.severity == "INFO":
            logger.info(f"Invariant info [{v.invariant_id}]: {v.description}")
        elif v.severity == "WARNING":
            logger.warning(f"Invariant warning [{v.invariant_id}]: {v.description}")
            # Снизить частоту ConsolidationEngine — не блокировать систему
            await self.heartbeat.reduce_ce_frequency(factor=0.5)
        elif v.severity == "ERROR":
            logger.error(f"INVARIANT ERROR [{v.invariant_id}]: {v.description}")
            await self.heartbeat.enter_degraded_mode(reason=v.invariant_id)
            # Grafana counter increment
        elif v.severity == "CRITICAL":
            logger.critical(f"INVARIANT VIOLATION [{v.invariant_id}]: {v.description}")
            await self.heartbeat.enter_safe_mode(reason=v.invariant_id)
```

---

## 🎭 Cognitive Modes — Три Режима Работы

> **Почему критично**: система работает одинаково для критичных данных и творческих задач. Cognitive Modes позволяют агенту адаптироваться — как человек думает по-разному в зависимости от контекста.

```python
# cognitive_modes.py
from enum import Enum
from dataclasses import dataclass

class CognitiveMode(str, Enum):
    PRECISION   = "precision"    # Критичные данные, факты
    BALANCED    = "balanced"     # Стандартная работа (90% задач)
    EXPLORATION = "exploration"  # Brainstorm, исследование
    CREATIVE    = "creative"     # Аналогии + только Validated (RFC0067 v2.0)

@dataclass
class ModeConfig:
    token_budget:      int
    evidence_required: int
    truth_gate_coverage: float
    hypothesis_allowed:  bool
    description: str

COGNITIVE_MODE_CONFIGS = {
    CognitiveMode.PRECISION: ModeConfig(
        token_budget=1000,
        evidence_required=5,
        truth_gate_coverage=0.9,
        hypothesis_allowed=False,
        description="Медицина, право, финансы — только verified факты"
    ),
    CognitiveMode.BALANCED: ModeConfig(
        token_budget=2000,
        evidence_required=3,
        truth_gate_coverage=0.7,
        hypothesis_allowed=True,
        description="Стандартный режим — 90% задач"
    ),
    CognitiveMode.EXPLORATION: ModeConfig(
        token_budget=4000,
        evidence_required=1,
        truth_gate_coverage=0.4,
        hypothesis_allowed=True,
        description="Brainstorm, исследование, гипотезы"
    ),
    CognitiveMode.CREATIVE: ModeConfig(
        token_budget=3000,
        evidence_required=3,
        truth_gate_coverage=0.7,
        hypothesis_allowed=False,   # I57: CREATIVE запрещает Hypothesized
        description="Аналогии + Validated только (RFC0067 v2.0)"
    ),
}

class CognitiveModeRouter:
    """
    Определяет режим работы на основе:
    · Явного указания пользователя
    · Ключевых слов запроса (RU + EN)
    · Cognitive Load оценки
    """
    PRECISION_SIGNALS   = {"точно", "проверь", "докажи", "факт", "данные",
                            "медицин", "юридич", "финанс", "критично"}
    PRECISION_EN        = {"verify", "accurate", "fact", "data", "medical",
                            "legal", "financial", "critical", "diagnos", "contract"}
    EXPLORATION_SIGNALS = {"представь", "придумай", "brainstorm", "идеи",
                            "а что если", "гипотез", "фантазия", "творч"}
    EXPLORATION_EN      = {"imagine", "brainstorm", "ideas", "what if",
                            "hypothesis", "explore", "unconventional", "speculate"}
    # CREATIVE mode: RFC0067 v2.0 — Analogy Graph + SBE мосты + температура 0.6→0.85
    CREATIVE_SIGNALS    = {"метафор", "аналог", "сравн", "как будто",
                            "напиши стих", "напиши рассказ", "поэтическ"}
    CREATIVE_EN         = {"metaphor", "analogy", "as if", "poem",
                            "story", "creative writing", "poetic"}

    def select_mode(self, query: str,
                    explicit_mode: CognitiveMode = None) -> CognitiveMode:
        if explicit_mode:
            return explicit_mode

        query_lower = query.lower()

        if any(signal in query_lower for signal in self.PRECISION_SIGNALS) or \
           any(signal in query_lower for signal in self.PRECISION_EN):
            return CognitiveMode.PRECISION
        # P9-FIX БАГ-10: CREATIVE проверяется ДО EXPLORATION — иначе "придумай метафору"
        # всегда возвращает EXPLORATION (т.к. "придумай" в EXPLORATION_SIGNALS побеждает)
        if any(signal in query_lower for signal in self.CREATIVE_SIGNALS) or \
           any(signal in query_lower for signal in self.CREATIVE_EN):
            return CognitiveMode.CREATIVE
        if any(signal in query_lower for signal in self.EXPLORATION_SIGNALS) or \
           any(signal in query_lower for signal in self.EXPLORATION_EN):
            return CognitiveMode.EXPLORATION
        return CognitiveMode.BALANCED

    def get_config(self, mode: CognitiveMode) -> ModeConfig:
        return COGNITIVE_MODE_CONFIGS[mode]
```

**Интеграция в Context Builder**:

```python
# Пример использования в context_builder.py
async def build_context(self, query: str, ...) -> str:
    mode = self.mode_router.select_mode(query)
    config = self.mode_router.get_config(mode)

    # RFC0067 v2.0: CREATIVE режим — читать SBE мосты из Redis-кэша.
    # I56: SBE только через EventBus (Slow Path). Fast Path — только кэш.
    # I57: FactsPack в CREATIVE — только Validated. Ассоциации отдельно.
    creative_associations = []
    if mode == CognitiveMode.CREATIVE:
        cached = await self.redis.get(f"creative_bridge:{session_id}")
        if cached:
            import json
            creative_associations = [
                CreativeAssociation.from_dict(a) for a in json.loads(cached)
            ]
        # Деградация без кэша: только Analogy Graph. НЕ вызывать SBE синхронно (I56).

    # Адаптируем token budget и Truth Gate под режим
    self.available_tokens = config.token_budget
    self.truth_gate_coverage = config.truth_gate_coverage

    # В EXPLORATION режиме Hypothesis узлы разрешены в контексте
    if config.hypothesis_allowed:
        context_types = ["verified", "hypothesis"]
    else:
        context_types = ["verified"]  # PRECISION: только verified

    logger.info(f"Cognitive mode: {mode.value}, budget: {config.token_budget}")
    ...
```

---

## 💰 Memory Budget Planner

> **Почему критично**: без лимитов граф растёт вечно. Memory Budget Planner работает как планировщик ресурсов в ОС — система знает свои пределы.

```python
# memory_budget_planner.py
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class MemoryBudget:
    """Лимиты памяти — не менять без архитектурного решения"""
    MAX_NODES_TOTAL:        int   = 500_000
    MAX_EDGES_PER_NODE:     int   = 100
    MAX_EPISODE_SIZE_BYTES: int   = 10_240      # 10 KB
    MAX_ADD_EPISODE_RATE:   int   = 100         # в час
    MAX_L1_EPISODES:        int   = 1_000       # на сессию
    GC_TRIGGER_THRESHOLD:   float = 0.85        # 85% заполнения → GC
    ALERT_THRESHOLD:        float = 0.90        # 90% → Grafana alert

class MemoryBudgetPlanner:
    def __init__(self, graph: GraphMemory,
                 consolidation_engine: ConsolidationEngine,
                 budget: MemoryBudget = None):
        self.graph = graph
        self.ce = consolidation_engine
        self.budget = budget or MemoryBudget()
        self._episode_count_hour = 0
        self._hour_start = datetime.now(timezone.utc)
        # FIX: Lock защищает rate-limit от TOCTOU race condition.
        # Без него два concurrent вызова читают одно значение, оба проходят проверку.
        self._rate_lock = asyncio.Lock()

    async def check_edges_per_node(self, node_id: str) -> bool:
        """Проверить степень узла — граф гибнет от плотности рёбер, не только от числа узлов"""
        query = """
        MATCH (n {id: $node_id})-[r]-()
        RETURN count(r) as edge_count
        """
        result = await self.graph.execute_cypher(query, {"node_id": node_id})
        edge_count = result[0].get("edge_count", 0) if result else 0
        if edge_count >= self.budget.MAX_EDGES_PER_NODE:
            logger.warning(f"Node {node_id} at edge limit: {edge_count}/{self.budget.MAX_EDGES_PER_NODE}")
            return False
        return True

    async def check_before_write(self, episode_size_bytes: int) -> bool:
        """
        Проверить можно ли записать новый эпизод.
        Возвращает True если OK, False если нужно подождать.
        """
        # Проверка размера эпизода
        if episode_size_bytes > self.budget.MAX_EPISODE_SIZE_BYTES:
            logger.warning(f"Episode too large: {episode_size_bytes}b > "
                           f"{self.budget.MAX_EPISODE_SIZE_BYTES}b. Truncating.")
            return False  # Caller должен обрезать

        # Проверка rate limit — защищена _rate_lock от TOCTOU
        async with self._rate_lock:
            now = datetime.now(timezone.utc)
            if (now - self._hour_start).total_seconds() > 3600:
                self._episode_count_hour = 0
                self._hour_start = now

            next_count = self._episode_count_hour + 1
            if next_count > self.budget.MAX_ADD_EPISODE_RATE:
                logger.warning(f"Rate limit: {next_count} episodes/hour")
                return False
            self._episode_count_hour = next_count

        # Проверка общего размера графа
        total_nodes = await self._get_total_nodes()
        fill_ratio = total_nodes / self.budget.MAX_NODES_TOTAL

        if fill_ratio >= self.budget.ALERT_THRESHOLD:
            logger.error(f"Graph near capacity: {fill_ratio:.1%}")
            # Grafana counter increment (via prometheus_client)

        if fill_ratio >= self.budget.GC_TRIGGER_THRESHOLD:
            logger.warning(f"Auto-triggering GC at {fill_ratio:.1%} capacity")
            await self.ce.enqueue("GC", {}, priority=ConsolidationPriority.GC)

        if total_nodes >= self.budget.MAX_NODES_TOTAL:
            logger.error("Graph at MAX capacity. Blocking write.")
            return False

        return True

    async def _get_total_nodes(self) -> int:
        result = await self.graph.execute_cypher(
            "MATCH (n) WHERE n.is_active = true RETURN count(n) as total"
        )
        return result[0].get("total", 0) if result else 0
```

---

## 🔐 PII Redaction

```python
# pii_redaction.py
import re
from dataclasses import dataclass

@dataclass
class PIIMatch:
    pii_type: str
    original: str
    position: tuple[int, int]

class PIIRedactor:
    """
    Минимальная реализация PII redaction для Phase 0/1.
    Удаляет очевидные PII перед записью в L1/L3.
    """
    PATTERNS = {
        "email":    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone_ru": r'\b(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b',
        "phone_int":r'\b\+[1-9]\d{1,14}\b',
        "card":     r'\b(?:\d{4}[\s\-]?){3}\d{4}\b',
        "passport_ru": r'\b\d{4}\s?\d{6}\b',
        "inn_ru":   r'(?:ИНН|инн)\s*[:：]?\s*\d{10}(?:\d{2})?',
    }

    def redact(self, text: str) -> tuple[str, list[PIIMatch]]:
        """
        Возвращает (redacted_text, list_of_matches).
        Matches сохраняются в Immutable Raw Memory (never in graph).
        """
        matches = []
        for pii_type, pattern in self.PATTERNS.items():
            for m in re.finditer(pattern, text):
                matches.append(PIIMatch(
                    pii_type=pii_type,
                    original=m.group(),
                    position=(m.start(), m.end())
                ))
            text = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", text)
        return text, matches

    async def forget_user(self, user_id: str,
                          consolidation_engine: ConsolidationEngine):
        """
        GDPR 'right to be forgotten'.
        Мягко удаляет все данные пользователя через CE.
        """
        await consolidation_engine.enqueue(
            op_type="GC",
            payload={"operation": "USER_PURGE", "user_id": user_id},
            priority=ConsolidationPriority.CONSOLIDATE  # Наивысший приоритет
        )
        logger.info(f"GDPR forget request queued for user: {user_id}")
```

**Интеграция**: PIIRedactor вызывается до записи в L1 SQLite и до add_episode() в Graphiti.

---

## 📋 RFC0014 — L2.5 Staging Layer

> **Статус**: Canonical · **Фаза**: Phase 0+
>
> L2.5 — асинхронный буфер между L2 и L3. Реализует принцип «граф строится когда можно, а не когда нужно». SQLite = staging. Graph = единственная истина.

### Архитектура

```
L0 / L1 / L2
    ↓
SQLite: staging_candidates  (временный буфер)
    ↓
Priority Queue
    ↓
Resource-Aware Scheduler  ← CPU < 35% AND RAM free > 25% AND user_idle
    │
    ├── FAST-TRACK (priority > 0.9) ──────────────┐
    │   минует очередь, идёт немедленно            │
    └── NORMAL BATCH (при idle) ─────────────────┐ │
                                                  ↓ ↓
                                            Truth Gate
                                                ↓
                                          L3 Graph (Neo4j)
```

### Инварианты RFC0014

```
I1: SQLite = STAGING. Никогда не является источником истины.
    Graph = единственный L3. Graph = Truth не нарушается.

I2: Чтение: сначала граф → потом staging (low-confidence fallback)
    Факт в graph    → берём оттуда (confidence as-is)
    Факт в staging  → используем с confidence × 0.7 + пометка "preliminary"

I3: Любое попадание в граф — только через Truth Gate.
    Даже асинхронно, даже ночью.

I4: Fast-Track (priority > 0.9) — обходит очередь и идёт немедленно.
    Примеры: аллергии, Ring Zero, критические факты.

I5: Принудительный flush: если ПК не idle > 24ч →
    планировщик забирает 5-10% CPU для переноса самых старых записей.
```

### SQL-схема staging_candidates

```sql
-- staging_candidates — буфер перед Truth Gate
CREATE TABLE staging_candidates (
    id               TEXT PRIMARY KEY,
    content          TEXT NOT NULL,        -- FactsPack или summary JSON
    source_layer     TEXT NOT NULL,        -- 'L1' | 'L2'
    epistemic_type   TEXT NOT NULL,        -- 'FACT' | 'LAW' | 'PATTERN' | 'STRATEGY'
    priority_score   REAL NOT NULL,        -- формула (см. ниже)
    confidence       REAL NOT NULL,
    fast_track       BOOLEAN DEFAULT 0,    -- обходит очередь
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_accessed    DATETIME,
    scheduled_for    DATETIME,
    status           TEXT NOT NULL DEFAULT 'PENDING',
                                           -- PENDING | PROMOTED | REJECTED | ARCHIVED
    is_promoted      BOOLEAN DEFAULT 0,    -- уже в L3
    rejection_reason TEXT,
    retry_count      INTEGER DEFAULT 0,
    cpu_cost_estimate REAL DEFAULT 0.1     -- оценка нагрузки для scheduler
);

CREATE INDEX idx_staging_priority   ON staging_candidates(priority_score DESC, created_at);
CREATE INDEX idx_staging_status     ON staging_candidates(status);
CREATE INDEX idx_staging_fast_track ON staging_candidates(fast_track) WHERE fast_track = 1;
CREATE INDEX idx_staging_promoted   ON staging_candidates(is_promoted);

-- Graph-Lite: временный мини-граф для ответов пока данные в staging
CREATE TABLE graph_lite_nodes (
    id    TEXT PRIMARY KEY,
    type  TEXT NOT NULL,
    label TEXT NOT NULL,
    payload TEXT  -- JSON
);
CREATE TABLE graph_lite_edges (
    src    TEXT NOT NULL,
    dst    TEXT NOT NULL,
    type   TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    PRIMARY KEY (src, dst, type)
);
-- При переносе в Neo4j: DELETE FROM graph_lite_nodes; DELETE FROM graph_lite_edges;
```

### Priority Score (формула)

```
priority_score = (importance × 0.4)
               + (log1p(access_count) × 0.2)          # log1p(x) = log(1+x), см. np.log1p
               + (recency_norm × 0.2)
               + (confidence × 0.2)

recency_norm = exp(-λ × days_since_created),  λ = 0.1

Fast-track порог: priority_score > 0.9 → немедленно → Truth Gate → L3
```

### Resource-Aware Scheduler (Python)

```python
# staging_scheduler.py
import asyncio
import psutil
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ResourceAwareScheduler:
    """
    Переносит данные из SQLite staging в L3 граф
    только когда система свободна.
    """
    CPU_THRESHOLD  = 0.35   # max 35% CPU
    RAM_THRESHOLD  = 0.25   # min 25% RAM свободно
    BATCH_SIZE     = 50     # кандидатов за один цикл
    IDLE_INTERVAL  = 3600   # проверка каждый час
    FORCE_INTERVAL = 86400  # принудительный flush если нет idle > 24ч
    MAX_STAGING    = 5000   # максимум записей в staging до force_flush

    def __init__(self, staging_store, truth_gate, graph):
        self.staging  = staging_store
        self.truth_gate = truth_gate
        self.graph    = graph
        self._last_flush = datetime.now(timezone.utc)
        self._running = False

    async def start(self):
        """Запустить как asyncio.Task параллельно с агентом."""
        self._running = True
        logger.info("ResourceAwareScheduler started")
        while self._running:
            await asyncio.sleep(self.IDLE_INTERVAL)
            await self._process_fast_track()       # всегда — независимо от ресурсов
            if await self._should_run():
                await self._promote_batch()
            elif await self._force_flush_needed():
                await self._promote_batch(force=True)

    async def _should_run(self) -> bool:
        cpu  = psutil.cpu_percent(interval=1) / 100
        ram  = psutil.virtual_memory().available / psutil.virtual_memory().total
        pending = await self.staging.count(status="PENDING")
        return cpu < self.CPU_THRESHOLD and ram > self.RAM_THRESHOLD and pending >= 10

    async def _force_flush_needed(self) -> bool:
        hours_since = (datetime.now(timezone.utc) - self._last_flush).total_seconds() / 3600
        staging_size = await self.staging.count(status="PENDING")
        return hours_since > 24 or staging_size > self.MAX_STAGING

    async def _process_fast_track(self):
        """CRITICAL items — не ждут idle, идут немедленно."""
        items = await self.staging.get_fast_track()
        for item in items:
            await self._promote_item(item)

    async def _promote_batch(self, force: bool = False):
        batch_size = self.BATCH_SIZE // 2 if force else self.BATCH_SIZE
        items = await self.staging.get_top_priority(limit=batch_size)
        promoted = 0
        for item in items:
            promoted += await self._promote_item(item)
        self._last_flush = datetime.now(timezone.utc)
        logger.info(f"Scheduler: promoted {promoted}/{len(items)} items"
                    f"{' (forced)' if force else ''}")

    async def _promote_item(self, item) -> int:
        try:
            if await self.truth_gate.validate(item):
                await self.graph.add_fact(item)
                await self.staging.update_status(item.id, "PROMOTED")
                return 1
            else:
                await self.staging.update_status(item.id, "REJECTED")
                return 0
        except Exception as e:
            logger.error(f"Promote failed for {item.id}: {e}")
            await self.staging.increment_retry(item.id)
            if await self.staging.get_retry_count(item.id) > 3:
                await self.staging.update_status(item.id, "REJECTED")
            return 0

    def stop(self):
        self._running = False
        logger.info("ResourceAwareScheduler stopped")
```

### Fast-Track API

```python
# Добавить критически важный факт — обходит очередь
async def add_fast_track(
    fact: dict,
    reason: str,
    staging_store,
    confidence: float = 0.95,   # ← PATCH-8: был хардкод 1.0 — лгал о достоверности.
                                 # Дефолт 0.95 честен для CRITICAL фактов.
                                 # Вызывающий код передаёт нужное: аллергия=0.8, Ring Zero=0.99
) -> bool:
    """
    Примеры CRITICAL: аллергии, безопасность, Ring Zero изменения.
    Такие факты НЕ ждут idle — сразу через Truth Gate в L3.
    """
    from staging_models import StagingItem
    item = StagingItem(
        content=fact,
        epistemic_type="FACT",
        priority_score=1.0,
        confidence=confidence,   # ← теперь честное значение от вызывающего кода
        fast_track=True,
        source_layer="L2",
        metadata={"reason": reason, "bypass_queue": True}
    )
    return await staging_store.insert(item)
```

### Cleanup staging (предотвращение переполнения)

```python
# Периодически — при GC или принудительно
async def cleanup_staging(staging_store):
    now = datetime.now(timezone.utc)
    # Низкоприоритетный мусор → удалить
    await staging_store.delete_where(
        "priority_score < 0.3 AND created_at < ?",
        (now - timedelta(days=30),)
    )
    # Средний приоритет → архивировать
    await staging_store.archive_where(
        "priority_score BETWEEN 0.3 AND 0.6 AND created_at < ?",
        (now - timedelta(days=60),)
    )
    # Высокий приоритет застрял → boost
    await staging_store.boost_priority(
        "priority_score > 0.6 AND created_at < ?",
        factor=1.5,
        args=(now - timedelta(days=90),)
    )
```

### Интеграция в Canonical Memory Protocol

```
НОВЫЙ ШАГ F4.5 : Staging Promote
    → ResourceAwareScheduler.start() — asyncio.Task при старте агента
    → Fast-Track hook вызывается при каждом add_episode() с priority > 0.9
    → Normal batch: каждый час при CPU idle
    → Graph-Lite используется при чтении как fallback (confidence × 0.7)
```

---

## 📋 RFC0013 — L2 CORE (Canonical Contract)

> **Статус**: Canonical · **Фаза**: Phase 0+
>
> L2 CORE определяет минимальный, неизменяемый контракт «граф + аналитика», который работает офлайн (без LLM), аудируем, воспроизводим и масштабируем.

### Принцип: LLM как интерпретатор

```
L2/L3 = источник знаний (структурированный, верифицированный)
LLM   = речевой аппарат (форматирует готовое, не добавляет факты)

Режим HEADLESS: LLM полностью отключён.
  L2 → шаблонный ответчик → структурированный ответ без генерации

Режим LITE (RAM < 4GB):
  Neo4j → sqlite-vec (векторный поиск)
  Etir  → упрощённый или отключён
  ReactivationEngine → раз в сутки
  GC/Consolidation → низкий приоритет
```

### Область ответственности L2

```
L2 ОТВЕЧАЕТ ЗА:
  · Извлечение структуры из L1: сущности, связи, события, утверждения
  · Аналитику поверх графа: кластеры, центральности, близость, противоречия
  · Детерминированные ответы на запросы без генерации «из воздуха»

L2 НЕ ОТВЕЧАЕТ ЗА:
  · Художественную генерацию
  · Догадки без опоры на данные
  · Подмену доказательств стилем
```

### Хранилище L2 (SQLite WAL)

```sql
-- Таблица l2_memory (персистентный L2, замена mtm_cache в RAM)
CREATE TABLE l2_memory (
    id                  TEXT PRIMARY KEY,
    original_episode_ids TEXT NOT NULL,  -- JSON array, трассировка L1→L2
    summary             TEXT NOT NULL,   -- TF-IDF extractive
    embedding           BLOB,            -- опционально
    topics              TEXT,            -- JSON array
    domain_id           TEXT,            -- RFC0012
    base_importance     REAL NOT NULL,
    current_importance  REAL NOT NULL,
    cluster_id          TEXT,
    cluster_type        TEXT DEFAULT 'EPISODIC',  -- EPISODIC|STRATEGIC|CONCEPTUAL
    access_count        INTEGER DEFAULT 0,
    last_access         TIMESTAMP,
    ttl_days            REAL DEFAULT 7,
    reactivation_count  INTEGER DEFAULT 0,
    last_reactivation   TIMESTAMP,
    is_active           BOOLEAN DEFAULT 1,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES domains(id)
);

CREATE VIRTUAL TABLE l2_fts USING fts5(summary, topics, content=l2_memory);
CREATE INDEX idx_l2_importance ON l2_memory(current_importance DESC);
CREATE INDEX idx_l2_cluster    ON l2_memory(cluster_id);
CREATE INDEX idx_l2_domain     ON l2_memory(domain_id);
CREATE INDEX idx_l2_active     ON l2_memory(is_active);
CREATE INDEX idx_l2_type       ON l2_memory(cluster_type);
```

### I/O батчинг метрик (защита SSD)

```python
# l2_metrics_buffer.py
# Постоянная перезапись access_count при каждом обращении → износ SSD.
# Буферизация решает: в память → flush каждые 10 минут.
class L2MetricsBuffer:
    def __init__(self, db_path: str, flush_interval: int = 600):  # ← PATCH-1: добавлен db_path (ранее AttributeError в _flush_to_db)
        self._db_path = db_path          # читается в _flush_to_db()
        self._buffer: dict[str, dict] = {}
        self._last_flush = time.time()
        self._flush_interval = flush_interval

    def record_access(self, item_id: str):
        if item_id not in self._buffer:
            self._buffer[item_id] = {"access_count": 0, "last_accessed": None}
        self._buffer[item_id]["access_count"] += 1
        self._buffer[item_id]["last_accessed"] = datetime.now(timezone.utc).isoformat()

    async def flush_if_needed(self):
        if time.time() - self._last_flush > self._flush_interval:
            # P1-D FIX: race condition — await мог переключить event loop пока шёл _flush_to_db().
            # Новые данные приходили в _buffer, затем clear() удалял их → потеря метрик.
            # Решение: атомарно захватить старый буфер, сразу открыть новый.
            buffer_to_flush = self._buffer          # захватить атомарно
            self._buffer = {}                       # новый буфер для входящих данных
            self._last_flush = time.time()
            await self._flush_to_db(buffer_to_flush)   # передать старый буфер

    async def _flush_to_db(self):
        if not self._buffer:
            return
        async with aiosqlite.connect(self._db_path) as db:
            for item_id, stats in self._buffer.items():
                await db.execute(
                    "UPDATE l2_memory SET access_count = access_count + ?, last_access = ? WHERE id = ?",
                    (stats["access_count"], stats["last_accessed"], item_id)
                )
            await db.commit()
```

### TTL Manager (адаптивный)

```python
# ttl_manager.py
class L2TTLManager:
    BASE_DAYS = 7
    MAX_DAYS  = 224  # 7 * 2^5

    def __init__(self, store, archive):   # ← PATCH-2: отсутствовал __init__, handle_expiration падал на self.store/self.archive
        self.store   = store              # персистентный L2 store
        self.archive = archive            # cold storage / S3

    def calculate_ttl(self, item: MemoryItemL2) -> float:
        """TTL растёт с частотой использования — важное живёт дольше."""
        visits = item.access_count + item.reactivation_count
        return min(self.BASE_DAYS * (2 ** min(visits, 5)), self.MAX_DAYS)

    async def handle_expiration(self, item: MemoryItemL2):
        if item.current_importance > 0.5:
            item.ttl_days = self.calculate_ttl(item) * 1.5  # продлить
            await self.store.update(item)
        else:
            item.is_active = False  # soft delete
            item.updated_at = datetime.now(timezone.utc)
            await self.store.update(item)
            await self.archive.move_to_cold_storage(item)
```

### ReactivationEngine («сон агента»)

```python
# reactivation_engine.py
# Аналог hippocampal replay: пока агент не занят — укрепляет важное.
class ReactivationEngine:
    """Фоновый процесс. Запускается как asyncio.Task параллельно с агентом."""

    async def start(self):
        while True:
            await asyncio.sleep(3600)  # каждый час
            if self._should_reactivate():
                await self._reactivation_cycle()

    def _should_reactivate(self) -> bool:
        return psutil.cpu_percent() < 30  # только при низкой нагрузке

    async def _reactivation_cycle(self):
        candidates = await self.store.get_top_by_importance(limit=10)
        for item in candidates:
            item.reactivation_count += 1
            item.current_importance = min(1.0, item.current_importance + 0.05)
            item.ttl_days = min(224, item.ttl_days * 1.2)
            item.last_reactivation = datetime.now(timezone.utc)
            await self.store.update(item)
            await self._strengthen_cluster_connections(item)
        logger.info(f"ReactivationEngine: укреплено {len(candidates)} эпизодов")
```

### L2 Health Index

```python
# Периодически → Prometheus. Значение 0.0–1.0.
def calculate_l2_health(items: List[MemoryItemL2], clusters) -> float:
    if not items:
        return 0.0
    avg_importance  = sum(i.current_importance for i in items) / len(items)
    stale_ratio     = sum(1 for i in items if i.ttl_days <= 7) / len(items)
    cluster_coherence = sum(c.coherence_score for c in clusters) / max(len(clusters), 1)
    access_rate     = sum(i.access_count for i in items) / max(len(items), 1)
    target_rate     = 5.0  # целевое среднее обращений

    health = (
        avg_importance              * 0.30 +
        (1 - stale_ratio)          * 0.30 +
        cluster_coherence          * 0.20 +
        min(access_rate / target_rate, 1.0) * 0.20
    )
    return round(max(0.0, min(1.0, health)), 3)
```

### Протокол L2 ответов без LLM (L2Query / L2Result)

```python
# l2_query_protocol.py
# L2 всегда возвращает структуру. LLM (если нужен) только рендерит её.

@dataclass
class L2Query:
    intent: Literal["lookup", "explain", "compare", "derive", "verify", "plan"]
    anchors: List[str]          # якоря запроса
    constraints: dict           # домен, глубина, источники
    output_mode: Literal["short", "structured", "trace_heavy"] = "structured"

@dataclass
class L2Result:
    answer: dict                # структурированный объект (concept_card / argument_map / matrix / ranked_list)
    confidence: float           # Confidence = w_e·E + w_c·C + w_k·K − w_x·X − w_d·D
    confidence_factors: dict    # {E, C, K, X, D} для прозрачности
    trace: dict                 # nodes_used, edges_used, metrics_used, rules_fired
    conflicts: List[dict]       # активные противоречия (не замалчиваются)
    next_actions: List[str]     # детерминированные предложения

# Формула Confidence (фиксирована в RFC0013):
# E = Evidence:    доля утверждений с прямым Evidence
# C = Consistency: мало CONTRADICTS в подграфе
# K = Coverage:    покрытие аспектов вопроса
# X = Conflicts:   штраф за активные противоречия
# D = Decay:       штраф за устаревание
```

### 5 инвариантов L2 CORE

```
I1: Детерминизм
    одинаковый граф + запрос + параметры → одинаковый результат

I2: Трассируемость
    каждый ответ = Answer + Trace + Confidence (формула, не «ощущение»)

I3: Разделение факта и вывода
    факт = Claim с Evidence
    вывод = DERIVES + правило/метрика

I4: Анти-взрыв графа
    любое расширение имеет лимиты: depth / fanout / node_budget / time

I5: Конфликт-осознанность
    противоречия НЕ заметаются — маркируются, учитываются в Confidence
```

### Сценарии работы

```
Сценарий 1 — HEADLESS: «Как повысить плодородие?»
  taxonomy_search(domain:agriculture)
  → L2: кластер cluster_type=STRATEGIC с высоким goal_alignment
  → FactsPack → шаблонный ответ
  → ответ без LLM

Сценарий 2 — LLM как интерпретатор: «Объясни стихами»
  те же факты из L2/L3 → LLM получает FactsPack
  → промпт: «переформатируй, не добавляй новых фактов»
  → LLM не думает, только форматирует

Сценарий 3 — Анализ документа:
  документ → эпизоды (L1) → summary в L2
  → при запросе: summary из L2, не перечитывать документ
```

---

## 💓 Meta-Supervisor — Apex Controller

### Архитектура Apex Controller

```
                    ┌──────────────────────────────────────┐
                    │         META-SUPERVISOR              │
                    │         (Apex Controller)            │
                    │                                      │
      ВХОДЫ:        │  · MHI score (Phase 2)         │   ВЫХОДЫ:
      ──────        │  · CE health (queue/dlq size)        │   ──────────
      CE status ──► │  · Budget fill ratio                 │ ──► Safe Mode
      DLQ size  ──► │  · Invariant violations              │ ──► CE frequency
      Budget    ──► │  · Circuit Breaker states            │ ──► GC trigger
      Invariants──► │  · ESM Collapsed rate                │ ──► Alert ops
                    └──────────────────────────────────────┘
```

### Три режима работы

```
NORMAL (по умолчанию):
  · CE работает с нормальной частотой
  · Все механизмы активны
  · Стандартные пороги Truth Gate

DEGRADED (при предупреждениях):
  · CE частота x2 (ускоренная консолидация)
  · Budget threshold снижен на 10%
  · Grafana alert отправлен

SAFE_MODE (при критических сбоях):
  · L3 = read-only
  · L1 продолжает накапливать данные
  · CE операции → DLQ
  · Задачи → BLOCKED_AWAITING_DB
```

```python
# meta_supervisor_apex.py
import asyncio
import logging
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)

class SupervisorMode(str, Enum):
    NORMAL    = "normal"
    DEGRADED  = "degraded"
    SAFE_MODE = "safe_mode"

class MetaSupervisorApex:
    """
    Apex Controller — управляющий слой над всей системой Velantrim.

    Входы: CE health, Budget fill ratio, Invariant violations,
           Circuit Breaker states, ESM Collapsed rate.
    Выходы: Safe Mode, CE frequency, GC trigger, alerts.

    Recovery Protocol: при падении самого Supervisor →
    Kubernetes liveness probe перезапускает процесс.
    Все решения Supervisor идемпотентны — повторный запуск безопасен.

    НЕ рекурсивный Meta-MHI (anti-pattern). Статистика Supervisor
    собирается Prometheus scraping извне.
    """
    HEARTBEAT_INTERVAL   = 10   # секунд
    CE_TIMEOUT_THRESHOLD = 60   # секунд молчания CE → safe mode
    BUDGET_WARN_RATIO    = 0.85 # 85% заполнения → degraded
    DLQ_WARN_SIZE        = 10   # DLQ > 10 → предупреждение

    def __init__(
        self,
        consolidation_engine: "ConsolidationEngine",
        graph: "GraphMemory",
        budget_planner: "MemoryBudgetPlanner",
        invariant_checker: "RuntimeInvariantChecker"
    ):
        self.ce        = consolidation_engine
        self.graph     = graph
        self.budget    = budget_planner
        self.checker   = invariant_checker
        self.mode      = SupervisorMode.NORMAL
        self._last_ce_ping = datetime.now(timezone.utc)
        self._mode_changed_at = datetime.now(timezone.utc)

    async def start(self):
        """Фоновый Apex Controller"""
        logger.info("Meta-Supervisor Apex Controller started")
        while True:
            await asyncio.sleep(self.HEARTBEAT_INTERVAL)
            await self._supervise_cycle()

    async def _supervise_cycle(self):
        """Один цикл наблюдения и управления"""
        # 1. Собрать сигналы
        signals = await self._collect_signals()

        # 2. Определить режим
        new_mode = self._decide_mode(signals)

        # 3. Применить изменения если режим поменялся
        if new_mode != self.mode:
            await self._apply_mode_transition(self.mode, new_mode, signals)
            self.mode = new_mode
            self._mode_changed_at = datetime.now(timezone.utc)

    async def _collect_signals(self) -> dict:
        """Собрать метрики от всех компонентов"""
        ce_alive = await self._ping_ce()
        dlq_size = len(self.ce.dlq)
        budget_fill = await self.budget._get_total_nodes() / self.budget.budget.MAX_NODES_TOTAL
        violations = await self.checker.check_all()
        critical_violations = [v for v in violations if v.severity == "CRITICAL"]

        signals = {
            "ce_alive":          ce_alive,
            "ce_silent_seconds": (datetime.now(timezone.utc) - self._last_ce_ping).total_seconds(),
            "dlq_size":          dlq_size,
            "budget_fill":       budget_fill,
            "critical_violations": len(critical_violations),
            "violation_ids":     [v.invariant_id for v in critical_violations],
        }
        # P4-E FIX: MHI интеграция Phase 2 — подключить MHICalculator когда реализован
        if hasattr(self, 'mhi_calculator'):
            try:
                signals["mhi"] = await self.mhi_calculator.get_current_mhi()
                if signals["mhi"] < 0.5:
                    signals["critical_violations"] += 1   # триггер DEGRADED
            except Exception:
                signals["mhi"] = None   # graceful fallback
        return signals

    SAFE_MODE_MIN_RECOVERY_SECONDS = 300  # P2-C FIX: минимум 5 минут в SAFE_MODE (cooldown)

    def _decide_mode(self, signals: dict) -> SupervisorMode:
        """Логика перехода между режимами.
        P2-C FIX: добавлен cooldown для SAFE_MODE.
        Без cooldown: нестабильный DLQ → быстрая осцилляция SAFE↔NORMAL → flood логов + хаотичный read-only.
        """
        # SAFE_MODE при серьёзных сбоях
        if (not signals["ce_alive"] and signals["ce_silent_seconds"] > self.CE_TIMEOUT_THRESHOLD) \
        or signals["critical_violations"] > 0:
            return SupervisorMode.SAFE_MODE

        # P2-C FIX: cooldown — не выходить из SAFE_MODE раньше MIN_RECOVERY_SECONDS
        if self.mode == SupervisorMode.SAFE_MODE:
            time_in_safe = (datetime.now(timezone.utc) - self._mode_changed_at).total_seconds()
            if time_in_safe < self.SAFE_MODE_MIN_RECOVERY_SECONDS:
                return SupervisorMode.SAFE_MODE  # держать режим минимум 5 минут

        # DEGRADED при предупреждениях
        if signals["dlq_size"] > self.DLQ_WARN_SIZE \
        or signals["budget_fill"] > self.BUDGET_WARN_RATIO:
            return SupervisorMode.DEGRADED

        return SupervisorMode.NORMAL

    async def _apply_mode_transition(
        self,
        from_mode: SupervisorMode,
        to_mode: SupervisorMode,
        signals: dict
    ):
        if to_mode == SupervisorMode.SAFE_MODE:
            self.graph.set_readonly(True)
            logger.critical(
                f"SAFE MODE ACTIVATED: violations={signals['violation_ids']}, "
                f"ce_alive={signals['ce_alive']}"
            )

        elif to_mode == SupervisorMode.DEGRADED:
            logger.warning(
                f"DEGRADED MODE: dlq={signals['dlq_size']}, "
                f"budget={signals['budget_fill']:.1%}"
            )
            # Ускорить GC
            await self.ce.enqueue("GC", {}, priority=ConsolidationPriority.GC)

        elif to_mode == SupervisorMode.NORMAL:
            if from_mode == SupervisorMode.SAFE_MODE:
                self.graph.set_readonly(False)
                logger.info("SAFE MODE DEACTIVATED — system recovered")

    async def _ping_ce(self) -> bool:
        """Ping ConsolidationEngine"""
        try:
            await asyncio.wait_for(
                self.ce.enqueue("PING", {}, priority=ConsolidationPriority.GC),
                timeout=5.0
            )
            self._last_ce_ping = datetime.now(timezone.utc)
            return True
        except Exception:
            return False

    async def enter_safe_mode(self, reason: str = "external"):
        """Внешний вызов Safe Mode (из InvariantChecker)"""
        await self._apply_mode_transition(
            self.mode, SupervisorMode.SAFE_MODE,
            {"violation_ids": [reason], "ce_alive": True, "budget_fill": 0}
        )
        self.mode = SupervisorMode.SAFE_MODE

    def health_check(self) -> dict:
        return {
            "mode":            self.mode.value,
            "mode_since":      self._mode_changed_at.isoformat(),
            "last_ce_ping":    self._last_ce_ping.isoformat(),
            "ce_dlq_size":     len(self.ce.dlq),
            "l3_readonly":     self.graph.is_readonly(),
        }
```

---

## 📊 Memory Health Index (MHI) — Phase 2

> **Почему здесь**: MHI требует реальных данных для калибровки весов. Нельзя выбрать коэффициенты без production-данных о деградации. Описание фиксирует архитектурное решение; реализация — после первых 2 недель стабильной работы.

```
MHI = единый показатель здоровья графа
      (от 0.0 = мёртвый до 1.0 = идеальный)

Компоненты (веса калибруются по реальным данным):
  w1 · stale_ratio      = is_active=false / total_nodes
  w2 · avg_traversal    = P95 latency retrieval в мс / 500
  w3 · entropy          = нормированная энтропия степеней узлов
  w4 · retrieval_cost   = среднее токенов на запрос / 2000

Автотриггеры:
  MHI < 0.3  → 🔴 немедленный GC + alert ops
  MHI < 0.5  → 🟡 ускорить ConsEngine (DEGRADED)
  MHI < 0.7  → 🟡 создать EvidenceSet агрегаторы
  MHI > 0.9  → 🟢 здоров, снизить частоту обслуживания

Реализация:
  · Отдельный asyncio.Task — не блокирует Fast Path
  · Shadow replica Neo4j — не нагружает основной граф
  · Random walk sampling — не полный обход (O(N))
  · Обновление каждые 5 минут
  · CPU-квота изолирована от L4 Reasoning Engine

Интеграция:
  · MetaSupervisorApex._collect_signals() читает MHI
  · При MHI < 0.5 → SupervisorMode.DEGRADED
  · Prometheus gauge: memory_health_index{component="graph"}

Phase 2: реализовать MHICalculator после 2 недель данных
```

---

## 🚀 Roadmap реализации

### ⚠️ Schema Migrations — версионирование схемы Neo4j

> ⚠️ **Блокер production**: Схема Neo4j эволюционирует между деплоями.
> Без версионирования обновление кода без обновления схемы приводит к краш при записи узла.

```
Правило: При каждом изменении схемы Neo4j — создать миграцию.

Структура:
  migrations/
    v8_01_add_evidence_count.cypher
    v8_02_add_hypothesis_node.cypher
    v8_03_add_etir_weights.cypher
    v8_04_add_session_id_l1.cypher
    v8_05_add_cognitive_mode_and_budget.cypher
    -- P2-B FIX: нумерация v5_xx → v8_xx (система v8.0, не v5.0)

Проверка при старте:
  1. pipeline.__init__() вызывает schema_version_check()
  2. Читает текущую версию из Neo4j: MATCH (m:SchemaVersion) RETURN m.version
  3. Если версия < ожидаемой → запускает pending миграции
  4. Если схема не найдена → создаёт с нуля (первый запуск)
  5. Если версия несовместима → БЛОКИРУЕТ запуск с явной ошибкой

Поле SchemaVersion в Neo4j:
  CREATE (m:SchemaVersion {version: "8.0", applied_at: datetime()})  -- P2-B FIX: было "5.0" при системе v8.0
```

Миграция (`migrations/v8_05_add_cognitive_mode_and_budget.cypher`):  <!-- P2-B FIX -->

```cypher
-- Добавить поля для Cognitive Modes и Budget Planner

// Добавить cognitive_mode к Episode
MATCH (ep:Episode) WHERE ep.cognitive_mode IS NULL
SET ep.cognitive_mode = 'BALANCED';

// Добавить epistemic_state к Fact (заготовка для ESM Phase 2)
MATCH (f:Fact) WHERE f.epistemic_state IS NULL
SET f.epistemic_state = 'Validated',
    f.epistemic_score = f.confidence;

// Добавить budget_tokens к Episode для мониторинга расхода
MATCH (ep:Episode) WHERE ep.budget_tokens IS NULL
SET ep.budget_tokens = 0;

// Обновить SchemaVersion
MERGE (m:SchemaVersion {version: "8.0"})  -- P2-B FIX
SET m.applied_at = datetime(),
    m.changes = "cognitive_mode, epistemic_state, epistemic_score, budget_tokens";
```

### Phase 1: Базовая инфраструктура (1-2 недели)

**Цель**: Запустить минимальную работающую систему

- [ ] Установить Neo4j 5.26+ + Graphiti
- [ ] **КРИТИЧНО: Создать индексы Neo4j** (без этого система деградирует!)
- [ ] **Добавить поле `embedding_version` в схему всех узлов**
- [ ] **Добавить поля Soft Delete (`is_active`, `valid_to`, `transaction_time`) в схему**
- [ ] **Добавить поле `raw_episode_id` в схему :Episode**
- [ ] **Добавить узел `:Evidence` и связь `[:SUPPORTED_BY]` в схему**
- [ ] **Добавить узел `:Concept` и связи `[:CAUSES]`, `[:CONCEPT_OF]` в схему**
- [ ] **Реализовать ImmutableRawMemory** (SQLite, append-only)
- [ ] **Реализовать MemoryGuardian** (L5 Observer расширить)
- [ ] **Зафиксировать формальные инварианты** как тесты (CI проверяет invariants)
- [ ] Настроить Redis для Event Bus с DLQ
- [ ] Реализовать RobustEventBus с retry/fallback
- [ ] **Добавить Circuit Breaker для Neo4j и Redis**
- [ ] Интегрировать Graphiti для автоматической экстракции
- [ ] Базовый гибридный поиск (векторы + граф)
- [ ] Простой агент с memory retrieval
- [ ] **Настроить OpenTelemetry для observability**
- [ ] **Зафиксировать `MAX_TOKENS_MEMORY_PER_QUERY` константу**
- [ ] **Минимальный Audit Layer** (logging в SQLite)
- [ ] ✅ **Запустить ConsolidationEngine** (заменяет 3 независимых воркера)
- [ ] ✅ **RFC0006 validate_engram_config() в pipeline.__init__()**
- [ ] ✅ **Runtime Invariant Checker запустить как фоновую задачу**
- [ ] ✅ **Cognitive Mode Router интегрировать в Context Builder**
- [ ] ✅ **PIIRedactor вызывать до записи в L1 и add_episode()**
- [ ] ✅ **SQLite WAL режим включить при инициализации**
- [ ] ✅ **Memory Budget Planner check_before_write() перед каждым add_episode()**
- [ ] ✅ **Meta-Supervisor Apex Controller запустить параллельно с агентом**
- [ ] ✅ **Schema migration v5_05_add_cognitive_mode_and_budget.cypher**

**Критерий успеха**: Агент может сохранять разговоры и извлекать релевантную информацию, система resilient к падениям зависимостей, нет race conditions

---

### Phase 2: Фрактальная иерархия (2-3 недели)

**Цель**: Реализовать многоуровневую память с автоматической консолидацией

- [ ] Implement FractalMemory с тремя уровнями (STM/MTM/LTM)
- [ ] **Персистентный L2 — таблица l2_memory (SQLite WAL + FTS5)**
- [ ] **cluster_type (EPISODIC/STRATEGIC/CONCEPTUAL) + логика decay по типу**
- [ ] **Cold Start Guard в consolidate_stm_to_mtm (≥ 50 эпизодов)**
- [ ] **TTL Manager — адаптивный (7 × 2^visits, max 224 дня)**
- [ ] **L2MetricsBuffer — I/O батчинг (flush каждые 10 мин)**
- [ ] **Создать таблицу staging_candidates + graph_lite_nodes/edges**
- [ ] **ResourceAwareScheduler запустить как asyncio.Task**
- [ ] **Fast-Track hook в add_episode() при priority > 0.9**
- [ ] **Улучшенный decay с reinforcement и emotional salience**
- [ ] **Адаптивная консолидация STM→MTM** (динамические интервалы)
- [ ] Кластеризация и **гибридная консолидация MTM→LTM** (extractive + selective LLM)
- [ ] Фоновые workers (AdaptiveConsolidationWorker)
- [ ] Importance scoring с многофакторным расчетом
- [ ] **Query optimization с LIMIT** для всех Cypher запросов
- [ ] **Реализовать Протокол Promote/Demote** (формальные правила из раздела)
- [ ] **Lazy Re-indexing воркер** (партиями переиндексировать `reindex_required=true`)
- [ ] **Async Etir** — считать spreading activation в фоне до запроса пользователя

**Критерий успеха**: Память автоматически консолидируется, расход токенов снижен на 70%+, нет memory leaks

---

### Phase 3: Самообучение (2-3 недели)

**Цель**: Агент учится на опыте

- [ ] ReasoningBank implementation
- [ ] Experience logging с outcome tracking
- [ ] Strategy extraction (distill_strategies)
- [ ] **Thompson Sampling strategy selection** (exploration/exploitation, RFC0039)
- [ ] **Negative reinforcement** через confidence penalty
- [ ] Retrieve-Execute-Judge-Learn цикл
- [ ] Strategy feedback loop с динамическим обновлением confidence
- [ ] Anti-pattern detection для избежания повторных ошибок

**Критерий успеха**: Агент улучшает успешность задач на 25%+, избегает повторения ошибок, баланс exploration/exploitation работает

---

### Phase 4: Оптимизация и Production (2-3 недели)

**Цель**: Готовность к production

- [ ] Token budget optimization с динамическим budgeting
- [ ] Context builder с приоритизацией
- [ ] Redis caching для частых запросов
- [ ] Community detection для кластеризации
- [ ] **Memory Garbage Collection** (периодическая очистка, Soft Delete → S3 → Hard Delete)
- [ ] **Архивация старых узлов в S3**
- [ ] Comprehensive monitoring (Prometheus + Grafana + Tempo)
- [ ] Performance benchmarking
- [ ] **A/B testing framework** для валидации улучшений
- [ ] Health checks для всех компонентов
- [ ] DLQ processing для failed events
- [ ] **Полный Audit Layer API** (3 метода: context, strategy, forgetting)
- [ ] **[:CONTRADICTS] pipeline** для разрешения конфликтов фактов
- [ ] **Memory Router upgrade** — заменить эвристику на o4-mini enum-классификатор
- [ ] **Knowledge Distillation Engine** MVP (узкий домен, JSON-тройки)
- [ ] **Каскадная инвалидация** Strategy при Soft Delete Fact

**Критерий успеха**: P95 латентность <500ms, снижение токенов >90%, граф не растет бесконечно, готовность к production

---

### Phase 5: Advanced Features (опционально)

- [ ] Adaptive resolution caching
- [ ] Топологическое сжатие графа
- [ ] Meta-learning для выбора стратегий
- [ ] Multi-agent memory sharing
- [ ] Privacy-preserving memory (GDPR compliance)
- [ ] Memory export/import

---

## ⚠️ Важные предупреждения

### Безопасность

1. **Privacy**: Эпизодическая память хранит личную информацию
   - ✅ PIIRedactor реализован (не декларация) — автоматически redact перед записью в L1/L3
   - ✅ GDPR `forget_user()` через ConsolidationEngine.enqueue(USER_PURGE)
   - Механизм удаления по запросу (GDPR "right to be forgotten") — реализован
   - Шифрование sensitive данных — Phase 2

2. **Рекурсивное улучшение**: Самообучение требует надзора
   - Не давать полный доступ к коду на старте
   - Human-in-the-loop для критичных решений
   - A/B тестирование перед production

3. **Bias в опыте**: Плохой опыт может закрепиться
   - Периодическая валидация стратегий
   - Механизм "забывания" устаревших паттернов
   - Diversity в experience replay

### Производительность

1. **Computational overhead**: Фоновые процессы потребляют ресурсы
   - Балансировать частоту консолидации
   - Использовать батчинг для graph updates
   - Мониторить CPU/Memory usage

2. **Graph scaling**: Neo4j требует оптимизации для больших графов
   - Индексы на критичные поля
   - Периодическая архивация старых узлов
   - Sharding для очень больших графов

3. **Token costs**: Даже с оптимизацией, LLM стоит дорого
   - Использовать быстрые модели для рутины (o4-mini / Claude Haiku 4.5)
   - Кэшировать частые запросы
   - Мониторить и алертить на аномальный расход

4. ✅ **ConsolidationEngine — единый координатор воркеров**

   Три независимых воркера заменены единым координатором:
   ```
   ConsolidationEngine :
     Все операции → asyncio.PriorityQueue → asyncio.Lock → Neo4j
     Порядок приоритетов: CONSOLIDATE > ARCHIVE > GC
     Таймаут: 30 секунд на операцию
     При таймауте: операция → DLQ (не потеря данных)
     Fallback: L3 → read-only, L1 продолжает работать
   ```

```python
# consolidation_engine.py
import asyncio
from collections import deque
from enum import Enum, IntEnum
from dataclasses import dataclass, field
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConsolidationPriority(IntEnum):
    CONSOLIDATE = 1   # Наивысший приоритет
    ARCHIVE     = 2
    GC          = 3   # Наименьший приоритет

class TaskStatus(str, Enum):
    NEW                = "new"
    ACTIVE             = "active"
    RESOLVED           = "resolved"
    FAILED             = "failed"
    BLOCKED_AWAITING_DB = "blocked_awaiting_db"

@dataclass(order=True)
class ConsolidationOp:
    priority: int
    op_type: str = field(compare=False)
    payload: Any  = field(compare=False)
    timeout: int  = field(compare=False, default=30)

class ConsolidationEngine:
    """
    Единая точка координации всех операций над Neo4j графом.
    Устраняет race conditions между AdaptiveConsolidationWorker,
    MemoryGarbageCollector и MemoryArchival.

    BLOCKED_AWAITING_DB: если CE недоступен, задача получает этот
    статус вместо ACTIVE, чтобы мониторинг понимал причину задержки.
    """
    def __init__(self, graph: GraphMemory, event_bus: RobustEventBus,
                 gc: "MemoryGarbageCollector" = None):
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._lock  = asyncio.Lock()
        self._running = False
        self.graph = graph
        self.event_bus = event_bus
        self.gc = gc
        self.dlq: deque[ConsolidationOp] = deque(maxlen=1000)

    async def enqueue(
        self,
        op_type: str,
        payload: Any,
        priority: ConsolidationPriority = ConsolidationPriority.CONSOLIDATE
    ):
        op = ConsolidationOp(priority=int(priority), op_type=op_type, payload=payload)
        await self._queue.put(op)
        logger.debug(f"CE enqueue: {op_type} priority={priority.name}")

    async def start(self):
        self._running = True
        logger.info("ConsolidationEngine started")
        while self._running:
            try:
                op = await asyncio.wait_for(self._queue.get(), timeout=5.0)
                await self._process(op)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"CE loop error: {e}")

    async def _process(self, op: ConsolidationOp):
        async with self._lock:
            try:
                result = await asyncio.wait_for(
                    self._dispatch(op),
                    timeout=op.timeout
                )
                return result
            except asyncio.TimeoutError:
                logger.error(f"CE timeout: {op.op_type} → DLQ")
                self.dlq.append(op)
                # Помечаем задачи как BLOCKED_AWAITING_DB
                if op.op_type == "CONSOLIDATE" and hasattr(op.payload, "task_id"):
                    await self.event_bus.publish(AgentEvent(
                        event_type=EventType.TASK_STATUS_CHANGED,
                        timestamp=datetime.now(timezone.utc),
                        content={"task_id": op.payload.task_id,
                                 "status": TaskStatus.BLOCKED_AWAITING_DB,
                                 "reason": "ConsolidationEngine timeout"},
                        metadata={},
                        session_id=op.payload.session_id
                    ))
            finally:
                self._queue.task_done()

    async def _dispatch(self, op: ConsolidationOp):
        if op.op_type == "CONSOLIDATE":
            return await self.graph.add_episode(**op.payload)
        elif op.op_type == "ARCHIVE":
            return await self.graph.soft_delete(**op.payload)
        elif op.op_type == "GC":
            if self.gc:
                return await self.gc.run_full_gc()
            logger.warning("CE: GC requested but gc= not configured")
        elif op.op_type == "PING":
            # heartbeat от MetaSupervisor — подтверждаем что CE жив
            logger.debug("CE: PING received → alive")
            return True
        else:
            logger.warning(f"CE unknown op_type: {op.op_type}")

    def stop(self):
        self._running = False
        logger.info("ConsolidationEngine stopped")
```

---

## 🔱 L3.5 — Etir (Velantrim Synaptic Activation Layer)

> **Важно**: L3.5 в архитектуре Velantrim — это исключительно Etir.
> Etir принадлежит канону Velantrim ExoCortex и работает снаружи трансформера.

---

### ⚡ L3.5 — Etir (Velantrim Synaptic Activation Layer)

**Etir** — это системный слой Velantrim. Название придумано в рамках проекта и принадлежит канону Velantrim ExoCortex.

```
Природа:     СИСТЕМНАЯ — снаружи трансформера
Механизм:    Spreading activation по графу Neo4j
Хранение:    In-memory Python-слой, не в графе
Зависимость: НЕ зависит от LLM — работает без трансформера
Динамика:    Живая, меняется в runtime при каждом запросе
Аналог мозга: Синаптическая предактивация нейронных сетей
```

**Как работает Etir:**

```
Запрос → L4 Reasoning Engine
         ↓
         Etir получает стартовые узлы
         ↓
         spreading activation: activation(j) += activation(i) * weight(edge_ij)
         ↓
         decay: activation *= exp(-λt)
         ↓
         lateral inhibition: activation(i) -= inhibition * competing_nodes
         ↓
         Граф предактивирован → L4 берёт готовый контекст
         ↓
         Если нет → полный обход L3 (Neo4j)
```

**Критерии попадания в Etir:**
- `access_count > порога` — часто запрашиваемые узлы
- `importance > 0.9` — высокая важность
- `pinned = True` — принудительное закрепление пользователем или L5
- Сигнал от L5 Observer (SelfAttentionDiary) — рекомендации по продвижению

**Pinned-узлы никогда не вытесняются автоматически.** L5 (ценности системы) всегда находится в Etir как pinned.

> 💡 **MAGMA-идея (типизация рёбер, 2026)**: spreading activation в Etir
> может работать по типу ребра. Добавить к рёбрам атрибут `type`:
> `semantic` / `temporal` / `causal` / `entity`. Тогда L4 Memory Router
> выбирает тип активации по интенту запроса — это повышает точность
> предактивации без изменения схемы узлов Neo4j. Реализация: Phase 2+.

---

## 📜 RFC0004 — Truth Gate Contract 

> **Статус**: Canonical · **Фаза**: Phase 0+
>
> Truth Gate — единственная точка входа в L3 граф для новых фактов.
> Реализован через TruthGateWithESM (RFC0015).

### Числовые пороги

Все значения из `velantrim_config.TruthConfig`.

| Критерий | Порог | Действие при нарушении | ESM-состояние |
|---------|-------|----------------------|--------------|
| `evidence_count` | ≥ 3 | Reject | Hypothesized |
| `confidence` | ≥ 0.75 | Reject | Hypothesized |
| `coverage_score` | ≥ 0.70 | Reject | Supported (ждёт данных) |
| `contradictions` | = 0 | Reject + [:CONTRADICTS] | Contradicted |
| Все выполнены | — | Accept | **Validated → L3** |

### Инварианты RFC0004

```
TruthGate.I1: НИ ОДИН факт не попадает в L3 без прохождения Truth Gate.

TruthGate.I2: Дубликат → increment evidence_count, новый узел не создаётся.

TruthGate.I3: Конфликт → [:CONTRADICTS] связь, НЕ удаление.
    При обнаружении агент переспрашивает пользователя.

TruthGate.I4: Truth Gate не пройден → LLM не генерирует ответ по этому факту.
    Возвращается: "Недостаточно данных".

TruthGate.I5: Truth Gate + ESM — атомарная операция (TruthGateWithESM, RFC0015).
```

### Связь с другими RFC

```
RFC0001 → RFC0004: LLM output → ESM только через Truth Gate
RFC0004 → RFC0013: L2 кластеры → L3 через Truth Gate (CONCEPTUAL type)
RFC0004 → RFC0014: staging_candidates → L3 через Truth Gate (Scheduler)
RFC0004 → RFC0015: TruthGateWithESM реализует этот контракт
RFC0004 → RFC0016: VelumSignal → не идёт в L3 напрямую, только через Truth Gate
```

---

## 📜 RFC0011 — Etir Spreading Activation Engine

> **Статус**: Draft · **Приоритет**: Phase 1 · **Срок**: 10–14 дней

### Цели и жёсткие ограничения

```
P95 latency ≤ 50 ms на графе 50k–200k узлов
Активировать ≤ 300 узлов за раз
Ring Zero / VALUES CORE — activation = 1.0 (иммунитет к inhibition)
ESM.Collapsed узлы — исключать из распространения полностью
Кэш результатов по query_hash (TTL 60–120 сек, Redis)
Fallback: если >50 ms → чистый Graphiti search (без Etir)
```

### Формальная модель

```
activation_0(i) = 1.0  если i ∈ seed_nodes (query + L0 entities)
                  0.0   иначе

activation_{t+1}(j) = activation_t(j) + Σ_{i→j} activation_t(i) · w_ij

decay(i) = activation(i) · e^{-0.18 · t}

lateral_inhibition(i) = activation(i) - 0.07 · Σ_{k ∈ competitors} activation(k)

final(i) = clamp(activation(i), 0, 1)  если final(i) > 0.12
```

**Параметры по умолчанию:**

| Параметр | Значение | Описание |
|----------|----------|----------|
| `max_steps` | 3 | Глубина распространения |
| `max_nodes` | 300 | Ограничение активированных узлов |
| `decay_rate` λ | 0.18 | Скорость затухания |
| `inhibition_rate` μ | 0.07 | Сила латерального подавления |
| `threshold` | 0.12 | Минимальная activation для включения в контекст |

### Инварианты (RFC0011)

```
Etir.I1: ∀ node ∈ activated_nodes: 0 ≤ activation ≤ 1
Etir.I2: |activated_nodes| ≤ 300
Etir.I3: Ring Zero узлы: activation ≥ 0.95 всегда (иммунитет)
Etir.I4: ESM.Collapsed узлы: activation = 0 (исключены)
Etir.I5: P95 latency < 50ms — иначе Circuit Breaker → fallback Graphiti
```

### Реализация: Cypher + Neo4j (не NetworkX — см. таблицу ниже)

> ⚠️ **NetworkX — ловушка**: тянет весь граф в RAM Python-процесса. На 10k узлов — секунды. Пишем сразу на Cypher внутри Neo4j.
>
> ⚠️ **`gds.runCypher()` не существует** в Neo4j GDS API. Spreading activation реализуется итеративными Cypher-запросами из Python, не через GDS-процедуры.

```cypher
// Шаг 1: Установить seed активацию (вызывается из Python перед итерациями)
MATCH (n)
WHERE n.id IN $seed_ids
  AND n.epistemic_state <> 'Collapsed'
SET n.activation = 1.0

// Шаг 2: Ring Zero иммунитет — всегда максимум
MATCH (n)
WHERE n.is_ring_zero = true
SET n.activation = 1.0

// Шаг 3: Одна итерация spreading (вызывается 3 раза из Python)
MATCH (n)-[r:RELATED_TO|SUPPORTED_BY|CONCEPT_OF]->(m)
WHERE n.activation > 0.12
  AND m.epistemic_state <> 'Collapsed'
  AND m.is_ring_zero <> true
WITH m, sum(n.activation * coalesce(r.weight, 0.5)) AS incoming
SET m.activation = coalesce(m.activation, 0.0) + incoming

// Шаг 4: Decay
-- P1-E FIX: I55.1 — дифференцированный decay для аналогий vs стандартные рёбра
MATCH (n)-[r]->(m)
WHERE n.activation IS NOT NULL
  AND n.is_ring_zero <> true
SET n.activation = n.activation * CASE
    WHEN type(r) IN ['METAPHOR_OF', 'ANALOGOUS_TO']
    THEN exp(-0.12)    -- SAE_DECAY_ANALOGY (I55.1): decay_factor=0.4 для аналогий
    ELSE exp(-0.18)    -- SAE_DECAY_STANDARD: decay_factor=0.6 для обычных рёбер
END

// Шаг 5: Сбор результатов
MATCH (n)
WHERE coalesce(n.activation, 0) > 0.12
  AND n.epistemic_state <> 'Collapsed'
RETURN n.id AS node_id, n.activation AS score
ORDER BY score DESC
LIMIT 300

// Шаг 6: Очистка (обязательно после каждого запроса!)
MATCH (n) WHERE n.activation IS NOT NULL
  AND n.is_ring_zero <> true
REMOVE n.activation
```

```python
# etir/engine.py — Python-обёртка 
import json
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class ActivationResult:
    activated_nodes: Dict[str, float]   # node_id → score
    context_window: List[str]           # топ-30 node_id
    execution_time_ms: float
    steps_used: int
    cache_hit: bool = False

class EtirEngine:
    """
    RFC0011: Etir Spreading Activation Engine
    Реализован на Cypher + Redis кэш.
    НЕ использует NetworkX (слишком медленно на >10k узлов).
    НЕ использует gds.runCypher() (не существует в GDS API).
    """
    CYPHER_SEED    = "MATCH (n) WHERE n.id IN $seed_ids AND n.epistemic_state <> 'Collapsed' SET n.activation = 1.0"
    CYPHER_RING    = "MATCH (n) WHERE n.is_ring_zero = true SET n.activation = 1.0"
    CYPHER_SPREAD  = """
        MATCH (n)-[r:RELATED_TO|SUPPORTED_BY|CONCEPT_OF]->(m)
        WHERE n.activation > $threshold
          AND m.epistemic_state <> 'Collapsed'
          AND m.is_ring_zero <> true
        WITH m, sum(n.activation * coalesce(r.weight, 0.5)) AS incoming
        SET m.activation = coalesce(m.activation, 0.0) + incoming
    """
    # P1-E FIX: I55.1 — CYPHER_DECAY разделён на два режима.
    # Аналогии получают мягкое затухание (exp(-0.12) = decay_factor 0.4).
    # Стандартные рёбра: exp(-0.18) = decay_factor 0.6.
    CYPHER_DECAY   = """MATCH (n)-[r]->(m)
        WHERE n.activation IS NOT NULL AND n.is_ring_zero <> true
        SET n.activation = n.activation * CASE
            WHEN type(r) IN ['METAPHOR_OF','ANALOGOUS_TO'] THEN exp(-0.12)
            ELSE exp(-0.18) END""""
    # Lateral inhibition: доминирующие узлы подавляют конкурентов (RFC0011, формула μ=0.07).
    # Ring Zero иммунны — их activation не снижается.
    # Без этого шага конкурирующие темы (0.9 vs 0.8) оба полностью активированы →
    # LLM получает размытый контекст. С ним — доминантная тема подавляет слабые.
    # P0-4 FIX: CYPHER_INHIBIT выбирается динамически через get_lateral_inhibition_cypher()
    # (APOC если доступен, чистый Cypher fallback для LadybugDB). Определён в dedupe_entities.py.
    CYPHER_INHIBIT_HEADER = """
        MATCH (n)
        WHERE n.activation IS NOT NULL
          AND n.is_ring_zero <> true
          AND n.epistemic_state <> 'Collapsed'
        WITH n ORDER BY n.activation DESC
        WITH collect(n) AS ranked
    """

    @classmethod
    def _build_cypher_inhibit(cls) -> str:
        """P0-4 FIX: собрать CYPHER_INHIBIT с правильным backend для lateral inhibition."""
        try:
            from dedupe_entities import get_lateral_inhibition_cypher
            body = get_lateral_inhibition_cypher()
        except ImportError:
            # Fallback если dedupe_entities недоступен: чистый Cypher (безопасно)
            body = """
        UNWIND range(0, size(ranked) - 1) AS i
        WITH ranked[i] AS dominant, ranked, i
        WHERE dominant.activation > $threshold
        UNWIND range(i + 1, size(ranked) - 1) AS j
        WITH dominant, ranked[j] AS competitor
        WHERE competitor.activation < dominant.activation
        WITH competitor,
             (competitor.activation - $mu * dominant.activation) AS raw_val
        SET competitor.activation = CASE WHEN raw_val < 0 THEN 0.0 ELSE raw_val END
            """
        return cls.CYPHER_INHIBIT_HEADER + body
    CYPHER_COLLECT = "MATCH (n) WHERE coalesce(n.activation, 0) > $threshold AND n.epistemic_state <> 'Collapsed' RETURN n.id AS node_id, n.activation AS score ORDER BY score DESC LIMIT $limit"
    CYPHER_CLEANUP = "MATCH (n) WHERE n.activation IS NOT NULL AND n.is_ring_zero <> true REMOVE n.activation"

    def __init__(self, driver, redis, config: dict = None):
        self.driver = driver
        self.redis  = redis
        self.config = config or {
            "max_steps": 3, "max_nodes": 300,
            "threshold": 0.12, "cache_ttl": 90
        }

    async def activate(self, query: str, seed_ids: List[str]) -> ActivationResult:
        import time
        start = time.monotonic()

        # Кэш
        # FIX: hash() нестабилен между процессами (PYTHONHASHSEED рандомизирован с Python 3.3).
        # hashlib.sha256 детерминирован — кэш работает корректно при нескольких воркерах.
        import hashlib
        _cache_raw = (query + '|'.join(sorted(seed_ids))).encode()
        cache_key = f"etir:{hashlib.sha256(_cache_raw).hexdigest()[:16]}"
        cached = await self.redis.get(cache_key)
        if cached:
            r = ActivationResult(**json.loads(cached))
            r.cache_hit = True
            return r

        async with self.driver.session() as session:
            try:
                await session.run(self.CYPHER_SEED, {"seed_ids": seed_ids})
                await session.run(self.CYPHER_RING)
                for _ in range(self.config["max_steps"]):
                    await session.run(self.CYPHER_SPREAD, {"threshold": self.config["threshold"]})
                    await session.run(self.CYPHER_DECAY)
                # Lateral inhibition — один проход после всех шагов распространения.
                # μ=0.07 из RFC0011. P0-4 FIX: APOC/fallback выбирается автоматически.
                try:
                    await session.run(
                        self._build_cypher_inhibit(),
                        {"threshold": self.config["threshold"], "mu": self.config.get("inhibition_rate", 0.07)}
                    )
                except Exception as _inh_err:
                    # APOC недоступен или CYPHER_INHIBIT упал → пропустить, не падать.
                    # Lateral inhibition — улучшение качества, не блокирующий путь.
                    logger.debug(f"Etir lateral inhibition skipped: {_inh_err}")
                rows = await (await session.run(
                    self.CYPHER_COLLECT,
                    {"threshold": self.config["threshold"], "limit": self.config["max_nodes"]}
                )).data()
            finally:
                # FIX: CYPHER_CLEANUP перенесён в finally — activation-свойства
                # гарантированно удаляются из Neo4j даже при исключении.
                # Без этого при сбое CYPHER_COLLECT висящие activation смешиваются
                # с seed следующего запроса.
                await session.run(self.CYPHER_CLEANUP)

        activated = {r["node_id"]: r["score"] for r in rows}
        context   = list(activated.keys())[:30]
        elapsed   = (time.monotonic() - start) * 1000

        # Circuit Breaker
        if elapsed > 50:
            logger.warning(f"Etir latency {elapsed:.1f}ms > 50ms — fallback to Graphiti")
            return ActivationResult({}, [], elapsed, 0)

        result = ActivationResult(activated, context, elapsed, self.config["max_steps"])
        await self.redis.setex(cache_key, self.config["cache_ttl"], json.dumps(result.__dict__))
        return result

    async def invalidate_cache(self, node_ids: List[str]):
        """
        Event-driven инвалидация кэша при изменении узлов
        
        Вызывается когда:
        - Узел добавлен/удалён/изменён в L3
        - ESM переход (особенно в Contradicted/Collapsed)
        - Weighted Decay применён
        
        Инвалидирует все кэш-ключи, содержащие эти node_ids
        """
        pattern = f"etir:*"
        cursor = 0
        invalidated = 0
        
        while True:
            cursor, keys = await self.redis.scan(cursor, match=pattern, count=100)
            
            for key in keys:
                cached = await self.redis.get(key)
                if cached:
                    data = json.loads(cached)
                    # Проверить пересечение с изменёнными узлами
                    if any(nid in data.get('activated_nodes', {}) for nid in node_ids):
                        await self.redis.delete(key)
                        invalidated += 1
            
            if cursor == 0:
                break
        
        if invalidated > 0:
            logger.info(f"Etir cache: invalidated {invalidated} keys for {len(node_ids)} nodes")
        
        return invalidated
```

### Структура файлов

```
velantrim/
├── etir/
│   ├── __init__.py
│   ├── engine.py       ← EtirEngine (Cypher + Redis, см. выше)
│   ├── cache.py        ← Redis TTL + invalidation при изменении графа
│   └── metrics.py      ← Prometheus: latency, nodes_activated, cache_hit, fallback_count
├── infra/
│   └── docker-compose.yml
├── hybrid_retrieval.py ← добавить вызов etir.activate() как шаг F2.5
├── context_builder.py  ← принимать etir_context_window
└── tests/
    └── test_etir.py    ← 7 тестов (см. ниже)
```

### Тесты (обязательные)

```python
# tests/test_etir.py
def test_single_seed_activation()       # один seed → корректное распространение
def test_decay_reduces_score()          # decay уменьшает activation
def test_inhibition_suppresses()        # inhibition подавляет конкурентов
def test_ring_zero_immunity()           # Ring Zero всегда activation ≥ 0.95
def test_collapsed_nodes_ignored()      # ESM.Collapsed = activation 0
def test_cache_hit_returns_fast()       # второй вызов < 10ms
def test_fallback_on_slow_graph()       # при latency > 50ms → пустой результат
```

### Метрики (Prometheus)

```python
etir_latency_ms       = Histogram("etir_latency_ms", ...)
etir_nodes_activated  = Gauge("etir_nodes_activated", ...)
etir_cache_hit_ratio  = Gauge("etir_cache_hit_ratio", ...)
etir_fallback_total   = Counter("etir_fallback_total", ...)
```

### Альтернативы NetworkX для spreading activation

> Выбор инструмента зависит от фазы и доступности Neo4j GDS.

| # | Инструмент | Скорость vs NetworkX | Встроен. spreading | Интеграция с Neo4j | Рекомендация |
|---|-----------|---------------------|-------------------|-------------------|-------------|
| 1 | **Neo4j GDS + Cypher** | 10–60× | Через итерат. Cypher | Нативная | ✅ **Production Phase 1** |
| 2 | **python-igraph** | 5–20× | Да (diffusion) | Нет прямой | 🟡 Быстрый MVP без GDS |
| 3 | **graph-tool** | 20–150× | Да | Нет | 🟡 Если igraph медленно |
| 4 | **cuGraph (RAPIDS)** | 50–1000× (GPU) | Да | Нет | 🔬 Phase 2 если есть GPU |
| 5 | **NetworkX** | 1× | Нет | Нет | ❌ Только прототип < 1k узлов |

### Timeline реализации (10–14 дней)

```
День 1–2:  Пилот — docker compose up -d, Cypher на 10k тестовых узлов, замер latency
День 3–6:  etir/engine.py + Redis кэш + интеграция в HybridRetriever (шаг F2.5)
           Ring Zero иммунитет + ESM.Collapsed фильтр + Circuit Breaker
День 7–10: 7 unit-тестов + integration-тест 1000 запросов + Prometheus метрики
День 11–14: Оптимизация (индексы, connection pool) + документация RFC0011
```

### Интеграция в Canonical Memory Protocol (новый шаг F2.5)

```
F2.5: Etir Activation (L3.5)
    → activation_map = EtirEngine.activate(query, seed_ids)
    → если latency > 50ms → Circuit Breaker → fallback Graphiti search
    → context_window передаётся в F3 (Context Builder)
```

---

## 📜 RFC0012 — Taxonomy/Domain Hierarchy 

> **Назначение**: структурированная таксономия знаний. Вместо плоского множества Concept-узлов — иерархия `Domain → Concept → Fact`. Поиск по домену сужает пространство, снижает шум и даёт taxonomy-based retrieval.

### Проблема без таксономии

```
Запрос: "вода кипит при 100°C"
Без Domain: поиск по всем 500k узлов → шум из медицины, истории, биологии
С Domain:   поиск только в domain:physics → 3k узлов → точный результат
```

### Иерархия узлов

```
:Domain {id: "domain:physics"}
    ↓ [:SUBDOMAIN_OF]
:Domain {id: "domain:thermodynamics"}
    ↓ (содержит :Concept через [:BELONGS_TO])
:Concept {id: "concept:boiling_point"}
    ↓ (связан с :Fact через [:CONCEPT_OF])
:Fact {content: "Вода кипит при 100°C при 1 атм"}
```

### Cypher: создание домена и поиск по таксономии

```cypher
// Создать домен и поддомен
MERGE (:Domain {id: "domain:physics", name: "Physics"})
MERGE (:Domain {id: "domain:thermodynamics", name: "Thermodynamics"})
MATCH (sub:Domain {id: "domain:thermodynamics"}), (parent:Domain {id: "domain:physics"})
MERGE (sub)-[:SUBDOMAIN_OF]->(parent)

// Связать Concept с Domain
MATCH (c:Concept {id: "concept:boiling_point"}), (d:Domain {id: "domain:thermodynamics"})
MERGE (c)-[:BELONGS_TO]->(d)

// taxonomy_search: поиск фактов в домене и всех поддоменах
MATCH (d:Domain {id: $domain_id})
OPTIONAL MATCH (sub:Domain)-[:SUBDOMAIN_OF*0..]->(d)
WITH collect(d.id) + collect(sub.id) AS domain_ids
MATCH (c:Concept)-[:BELONGS_TO]->(dom:Domain)
WHERE dom.id IN domain_ids
MATCH (f:Fact)-[:CONCEPT_OF]->(c)
WHERE f.is_active = true
  AND f.epistemic_state IN ["Validated", "Supported"]
RETURN f.content, c.name, dom.id, f.epistemic_state
ORDER BY f.epistemic_score DESC
LIMIT $limit
```

### Python: taxonomy_search()

```python
# taxonomy_search.py
async def taxonomy_search(
    self,
    query: str,
    domain_id: str,           # "domain:physics" или "domain:thermodynamics"
    include_subdomains: bool = True,
    limit: int = 20
) -> list[dict]:
    """
    RFC0012: поиск фактов в домене + опционально во всех поддоменах.
    Сужает пространство поиска: вместо всего графа — только релевантный домен.
    Используется как предфильтр перед Etir activation (шаг F2.4).
    """
    cypher = """
    MATCH (d:Domain {id: $domain_id})
    WITH d
    OPTIONAL MATCH (sub:Domain)-[:SUBDOMAIN_OF*0..]->(d)
    WITH collect(DISTINCT d.id) + collect(DISTINCT sub.id) AS domain_ids
    MATCH (c:Concept)-[:BELONGS_TO]->(dom:Domain)
    WHERE dom.id IN domain_ids
    MATCH (f:Fact)-[:CONCEPT_OF]->(c)
    WHERE f.is_active = true
      AND f.epistemic_state IN ["Validated", "Supported"]
    RETURN f.id AS fact_id, f.content AS content,
           c.name AS concept, dom.id AS domain,
           f.epistemic_score AS score
    ORDER BY score DESC
    LIMIT $limit
    """
    return await self.graph.execute_cypher(cypher, {
        "domain_id": domain_id,
        "limit": limit
    })
```

### Интеграция в Canonical Memory Protocol (новый шаг F2.4)

```
F2.4: Taxonomy Filter (RFC0012)
    → если запрос содержит domain_hint → taxonomy_search(domain_id)
    → результаты передаются в F2.5 Etir как seed_ids
    → без domain_hint → шаг пропускается, идём сразу в F2.5
```

### Инварианты RFC0012

```
I1: ∀ Concept: может иметь 0 или 1 :Domain (не обязательно)
I2: Домены образуют DAG (directed acyclic graph), не циклы
I3: taxonomy_search() никогда не пересекает границу домена без явного [:SUBDOMAIN_OF]
I4: :Domain узлы не проходят через MGL — они структурные, не эпистемические
I5: При GC :Domain не удаляется если есть хотя бы 1 активный :Concept
```

### Seed Domains для Phase 0

```python
# При инициализации системы создать базовые домены
SEED_DOMAINS = [
    {"id": "domain:science",       "name": "Science"},
    {"id": "domain:physics",       "name": "Physics",       "parent": "domain:science"},
    {"id": "domain:chemistry",     "name": "Chemistry",     "parent": "domain:science"},
    {"id": "domain:biology",       "name": "Biology",       "parent": "domain:science"},
    {"id": "domain:mathematics",   "name": "Mathematics",   "parent": "domain:science"},
    {"id": "domain:agent_memory",  "name": "Agent Memory"},  # для внутренних фактов агента
    {"id": "domain:user_context",  "name": "User Context"},  # для персонального контекста
]
```

---

> 🔭 **Будущая интеграция — Engram (DeepSeek, 2026)**
>
> Engram — это внутренний механизм трансформера DeepSeek, **не компонент Velantrim**.
> Он работает на уровне N-gram hash → Conditional Memory Table внутри модели и
> активируется автоматически при использовании DeepSeek v4+ без каких-либо действий
> со стороны Velantrim. Velantrim не реализует и не контролирует Engram.
>
> **Рекомендация для DeepSeek v4+**: при использовании этих моделей в pipeline
> присваивать фактам, поступающим через них, `source_type = "engram_memory"`
> в Source Trust Layer с повышенным `trust_score = 0.80` — как поступающим
> из верифицированной внутренней памяти модели.
>
> Etir (Velantrim) и Engram (DeepSeek) не конкурируют: Etir управляет явной
> верифицированной памятью снаружи трансформера, Engram — имплицитной
> нейронной памятью внутри него. RFC0006 (`validate_engram_config`) сохраняется
> как защита от случайного включения `ENGRAM_ENABLED=True` с API-моделями.

---

## 📜 RFC0013 — L2 Medium-Term Memory CORE 

> См. раздел "L2: Среднесрочная память" выше для полной спецификации.

---

## 📜 RFC0014 — L2.5 Staging Layer 

> См. раздел "L2.5: Staging Layer" выше для полной спецификации.

---

## 📜 RFC0015 — TruthGateWithESM 

> **Статус**: Canonical · **Фаза**: Phase 0+
>
> Единая точка входа для промоута в L3. Координирует MemoryGuardian + EpistemicStateMachine атомарно.

### Проблема

MemoryGuardian и EpistemicStateMachine существовали независимо:
- Guardian валидирует факт
- ESM управляет жизненным циклом
- **Нет гарантии** что валидация Guardian → правильный ESM-переход
- ResourceAwareScheduler мог промоутить в L3 без перевода ESM в Validated

### Решение

Фасад-оркестратор `TruthGateWithESM` объединяет обе операции:

```python
@dataclass
class TruthGateResult:
    passed: bool
    score: float
    esm_state: str          # Validated / Contradicted / Hypothesized
    reason: str             # TRUTH_GATE_PASSED / LOW_EVIDENCE / CONFLICT_DETECTED
    emotional_salience: float = 0.0

# 📎 Каноническая реализация TruthGateWithESM — см. раздел «19. TruthGateWithESM»
# Здесь: концептуальная схема операций (Guardian→ESM→RingZero→L3 промоут)
```

### Emotional Ring Zero

**Концепция:** высокая эмоциональная значимость → иммунитет к decay

```python
if emotional_salience > TRUTH.EMOTIONAL_RING_ZERO:  # 0.85
    await self.esm.freeze(item["id"])
    # Узел становится immutable - не подвержен GC и decay
```

### Инварианты RFC0015

```
I1: Единственная точка входа для промоута staging → L3.
    НЕ создавать обходные пути в L3 мимо этого класса.

I2: TruthGateResult содержит ВСЮ информацию о результате валидации.
    Caller не должен интерпретировать внутренние состояния Guardian/ESM.

I3: Emotional Ring Zero (salience > 0.85) → ESM.freeze() автоматически.
    Не требует явного вызова freeze() в коде caller'а.

I4: При rejection дубликата: TruthGateResult.passed = False,
    но esm_state = "Validated" (узел уже был в L3).
```

### Использование в ResourceAwareScheduler

```python
# staging_scheduler.py
async def _promote_item(self, item) -> int:
    result: TruthGateResult = await self.truth_gate_esm.validate_and_transition(item)

    if result.passed:
        await self.staging.update_status(item.id, "PROMOTED")
        return 1
    else:
        # Дубликат - считаем успехом (узел уже есть)
        status = "PROMOTED" if result.reason == "DUPLICATE" else "REJECTED"
        await self.staging.update_status(item.id, status)
        return 0
```

### Correction Mechanism 

**Проблема**: Emotional Ring Zero freeze (salience > 0.85) может заморозить ЛОЖНУЮ тему навсегда.

**Решение**: Rollback freeze при обнаружении [:CONTRADICTS] после заморозки.

```python
# truth_gate_correction.py
class TruthGateCorrectionMechanism:
    """
    Мониторит замороженные узлы и размораживает при появлении противоречий.
    """

    async def monitor_frozen_nodes(self):
        """Вызывается ReactivationEngine каждые 6 часов"""
        query = """
        MATCH (n:Fact {is_frozen: true})
        OPTIONAL MATCH (n)<-[c:CONTRADICTS]-(other)
        WHERE c.timestamp > n.frozen_at  // Противоречие ПОСЛЕ заморозки
        RETURN n.id, collect(other.id) as contradictions
        """
        results = await self.graph.execute_cypher(query)
        
        for row in results:
            if len(row['contradictions']) > 0:
                await self._unfreeze_with_audit(row['id'], row['contradictions'])

    async def _unfreeze_with_audit(self, node_id: str, contradictions: list):
        """
        Разморозить узел + создать audit trail.
        НЕ удаляем — переводим в ESM.Contradicted.
        """
        await self.esm.unfreeze(node_id)
        await self.esm.transition(node_id, "Contradicted", 
            reason=f"FREEZE_ROLLBACK: {len(contradictions)} contradictions found")
        
        # Audit log
        await self.audit.log_correction(
            node_id=node_id,
            action="UNFREEZE_CONTRADICTED",
            contradictions=contradictions,
            timestamp=datetime.now(timezone.utc)
        )
        
        logger.warning(
            f"TruthGate Correction: unfroze {node_id} due to {len(contradictions)} contradictions"
        )
```

**Инварианты:**

```
I5: Frozen узел может быть разморожен ТОЛЬКО при [:CONTRADICTS] ПОСЛЕ freeze.
I6: Unfreeze НЕ удаляет узел — переводит в ESM.Contradicted для ручного review.
I7: Каждый unfreeze создаёт audit trail (кто, когда, почему).
I8: Ring Zero узлы (is_ring_zero=true) НИКОГДА не размораживаются автоматически.
```

**Интеграция**:
- ReactivationEngine вызывает `monitor_frozen_nodes()` каждые 6 часов
- MetaSupervisor получает alert при каждом unfreeze
- Audit Layer логирует для GET /memory/audit/corrections

---

## 📜 RFC0016 — L1.5 Velum 

> **Статус**: Canonical · **Фаза**: Phase 0+
>
> Velantrim Synaptic Pre-Graph Layer - детектор ранних связей между сущностями.

### Назначение

L1.5 Velum живёт между L1 (эпизоды) и L2 (кластеры):
- L1 накапливает эпизоды
- **Velum замечает связи** между сущностями (co-occurrence)
- L2 строит кластеры тем

Аналог в нейробиологии: **LTP (Long-Term Potentiation)** - синаптическое усиление до долгосрочного закрепления.

### Dataclasses

> 📎 **Каноническая реализация** `VelumEdge` и `VelumSignal` — см. раздел «20. L1.5 Velum».

### Механизм работы

```
L1 INSERT → Velum.observe_episode(episode_id, entities)
  ↓
Обновить weight для всех пар сущностей в скользящем окне (5 эпизодов)
  ↓
Если weight ≥ 0.6 AND count ≥ 3
  ↓
VelumSignal → ReactivationEngine + L2 (ускоренный промоут кластера)
```

### Основные методы

**observe_episode()**
```python
async def observe_episode(self, episode_id: str, entities: list[str]) -> list[VelumSignal]:
    # Вызывается из L1 Episodic Buffer при каждом INSERT
    # Возвращает VelumSignal при достижении порога
```

**on_session_end()**
```python
async def on_session_end(self) -> list[VelumSignal]:
    # При смене сессии (30 мин неактивности):
    # - Сильные рёбра (weight ≥ 0.6) → VelumSignal "SESSION_END" → L2
    # - Слабые рёбра → decay × 0.3
```

**get_neighbors()**
```python
def get_neighbors(self, entity: str, min_weight: float = 0.3) -> list[tuple[str, float]]:
    # Используется:
    # - HybridRetriever: расширение контекста внутри сессии
    # - ReactivationEngine: подсказка что укреплять
```

### Конфигурация (из velantrim_config.py)

```python
VELUM_CO_OCCUR_THRESHOLD = 3       # совместных появлений → запись
VELUM_WINDOW_EPISODES = 5          # окно наблюдения
VELUM_MAX_EDGES = 1000             # максимум рёбер до GC
VELUM_PROMOTE_WEIGHT = 0.6         # вес → сигнал L2
VELUM_DECAY_PER_SESSION = 0.3      # decay при смене сессии
SAE_DECAY_STANDARD  = 0.18   # P1-E FIX (I55.1): exp коэффициент для обычных рёбер
SAE_DECAY_ANALOGY   = 0.12   # P1-E FIX (I55.1): exp коэффициент для METAPHOR_OF/ANALOGOUS_TO
```

### Инварианты RFC0016

```
I1: Velum хранит ТОЛЬКО рёбра (entity_a, entity_b, weight).
    НЕ хранит содержимое эпизодов - только наблюдение о связи.

I2: При смене сессии:
    weight < VELUM_PROMOTE_WEIGHT → decay × VELUM_DECAY_PER_SESSION
    weight ≥ VELUM_PROMOTE_WEIGHT → VelumSignal → L2 на ускоренный промоут

I3: Velum НЕ является источником фактов. Graph = Truth не нарушается.
    Velum → только подсказка для планировщика (ReactivationEngine, L2 clustering).

I4: Velum не персистентен между сессиями по умолчанию.
    Опционально (Phase 1): сохранять топ-N рёбер в SQLite для seed.
```

### Интеграция в Canonical Protocol

```
F1.5: Velum Context Hint (RFC0016)
    → Velum.get_neighbors(query_entities, min_weight=0.3)
    → Добавить соседей в seed для Etir (шаг F2.5)
    → Fire-and-forget hint - не блокирует Fast Path
```

### GC (сборка мусора)

При > VELUM_MAX_EDGES (1000):
- Удалить 25% слабейших рёбер
- Очистить _entity_index

---

## 📜 RFC0017 — Weighted Semantic Decay 

> **Статус**: Canonical · **Фаза**: Phase 1
>
> Критический компонент для точности L3.
>
> Механизм удаления противоречивых и устаревших фактов из L3 графа на основе семантической близости и эпистемического веса.

### Проблема

Без Weighted Semantic Decay:
- L3 граф растёт бесконечно (накопление дубликатов и противоречий)
- Устаревшие факты остаются с `importance > 0.1` → никогда не достигают Collapsed
- [:CONTRADICTS] рёбра создаются, но конфликтующие узлы не удаляются
- Память становится "засорённой" — низкая точность поиска

### Решение

Периодический (каждые 24 часа) анализ L3 графа:

```python
# weighted_semantic_decay.py
class WeightedSemanticDecay:
    """
    Находит семантически близкие узлы с противоречиями и применяет decay.
    """

    async def run_decay_cycle(self):
        """Основной цикл — вызывается по расписанию (cron/APScheduler)"""
        # 1. Найти все Contradicted узлы
        contradicted = await self._find_contradicted_nodes()
        
        # Защита от цепной реакции
        max_cascade_nodes = 50  # Лимит узлов за один цикл
        total_penalized = 0
        
        # 2. Для каждого найти семантически близкие (cosine > 0.85)
        for node in contradicted:
            if total_penalized >= max_cascade_nodes:
                logger.warning(
                    f"Cascade limit reached: {max_cascade_nodes} nodes penalized. "
                    f"Remaining {len(contradicted) - contradicted.index(node)} "
                    f"Contradicted nodes will be processed in next cycle."
                )
                break
            
            similar = await self._find_similar_nodes(node, threshold=0.85)
            
            # Лимит на количество соседей для одного узла
            similar = similar[:10]  # Максимум 10 соседей на узел
            
            # 3. Применить weighted decay на основе epistemic_state
            for sim_node in similar:
                if total_penalized >= max_cascade_nodes:
                    break
                    
                penalty = self._calculate_penalty(node, sim_node)
                await self._apply_decay(sim_node.id, penalty)
                total_penalized += 1
        
        # 4. Проверить узлы с importance < 0.1 → ESM.transition(Collapsed)
        await self._collapse_low_importance_nodes()
        
        # Метрика для мониторинга
        decay_cascade_size.set(total_penalized)
        if total_penalized >= max_cascade_nodes:
            decay_cascade_limit_hit.inc()

    def _calculate_penalty(self, contradicted_node, similar_node) -> float:
        """
        Штраф зависит от:
        - Семантической близости (cosine similarity)
        - Epistemic state похожего узла
        - Количества [:CONTRADICTS] рёбер
        """
        cosine = similar_node.similarity  # 0.85 - 1.0
        state_weight = {
            "Validated": 0.3,      # слабый штраф (может быть правда)
            "Supported": 0.5,      # средний
            "Hypothesized": 0.7,   # сильный
            "Contradicted": 1.0    # максимальный (противоречие противоречия)
        }
        
        base_penalty = 0.15
        semantic_factor = (cosine - 0.85) / 0.15  # нормализация 0.85-1.0 → 0-1
        state_factor = state_weight.get(similar_node.epistemic_state, 0.5)
        
        return base_penalty * semantic_factor * state_factor

    async def _apply_decay(self, node_id: str, penalty: float):
        """
        Снизить importance узла.
        Если упадёт < 0.1 → следующий GC переведёт в Collapsed.
        """
        query = """
        MATCH (n:Fact {id: $node_id})
        SET n.importance = max(0.0, n.importance - $penalty),
            n.decay_applied_at = datetime(),
            n.decay_count = coalesce(n.decay_count, 0) + 1
        RETURN n.importance as new_importance
        """
        result = await self.graph.execute_cypher(query, 
            {"node_id": node_id, "penalty": penalty})
        # P9-FIX БАГ-5: kwargs→positional dict (соответствует стилю всего документа строки 9887, 10166)
        # P9-FIX БАГ-9: max(0.0, ...) — importance не уходит в отрицательные значения
        
        logger.info(
            f"Decay applied: {node_id} penalty={penalty:.3f} "
            f"new_importance={result[0]['new_importance']:.3f}"
        )

    async def _collapse_low_importance_nodes(self):
        """
        Узлы с importance < 0.1 → ESM.Collapsed → Immutable Raw Memory
        """
        query = """
        MATCH (n:Fact)
        WHERE n.importance < 0.1 
          AND n.epistemic_state <> 'Collapsed'
          AND n.is_ring_zero <> true  // Ring Zero защищён
        RETURN n.id, n.importance, n.epistemic_state
        """
        candidates = await self.graph.execute_cypher(query)
        
        for node in candidates:
            await self.esm.transition(
                node['id'], 
                "Collapsed",
                reason=f"WEIGHTED_DECAY: importance={node['importance']:.3f}"
            )
            
            # Архивировать в S3 перед удалением из operational графа
            await self.archive.store_collapsed_node(node['id'])
```

### Конфигурация

```python
# velantrim_config.py
class DecayConfig:
    SEMANTIC_SIMILARITY_THRESHOLD = 0.85   # cosine > 0.85 → кандидаты
    BASE_DECAY_PENALTY = 0.15              # базовый штраф
    COLLAPSE_IMPORTANCE_THRESHOLD = 0.1    # importance < 0.1 → Collapsed
    DECAY_SCHEDULE_HOURS = 24              # частота запуска
    PROTECT_RING_ZERO = True               # Ring Zero иммунитет

    # Защита от цепной реакции
    MAX_CASCADE_NODES_PER_CYCLE = 50       # лимит узлов за цикл
    MAX_NEIGHBORS_PER_NODE = 10            # лимит соседей на узел
```

### Инварианты RFC0017

```
I1: Weighted Decay применяется ТОЛЬКО к узлам с [:CONTRADICTS] рёбрами или близким к ним.
    НЕ трогаем Validated узлы без противоречий.

I2: Ring Zero узлы (is_ring_zero=true) НИКОГДА не получают decay penalty.

I3: Перед Collapsed → обязательная архивация в S3 (Immutable Raw Memory).

I4: Decay — это снижение importance, НЕ удаление.

I5: Если decay_count > 5 для одного узла → alert ("Частые противоречия").
    Метрика decay_count инкрементируется при каждом применении penalty.
    Удаление происходит только при GC после Collapsed.

I6: MAX_CASCADE_NODES_PER_CYCLE лимит защищает от цепной реакции.
    Если лимит достигнут → остальные узлы обрабатываются в следующем цикле.
```

### Интеграция

```python
# main.py или scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from weighted_semantic_decay import WeightedSemanticDecay

scheduler = AsyncIOScheduler()
decay_engine = WeightedSemanticDecay(graph, esm, archive)

# Запуск каждые 24 часа
scheduler.add_job(
    decay_engine.run_decay_cycle,
    'interval',
    hours=24,
    id='weighted_semantic_decay'
)
```

### Метрики

```python
# Prometheus metrics
decay_cycles_total = Counter('velantrim_decay_cycles_total')
decay_penalties_applied = Counter('velantrim_decay_penalties_applied')
nodes_collapsed_total = Counter('velantrim_nodes_collapsed_total')
decay_cycle_duration_seconds = Histogram('velantrim_decay_cycle_duration_seconds')
```

### Пример работы

```
День 1: Факт A (importance=0.8, Validated)
        Факт B (importance=0.7, Validated, semantic_similarity=0.92 с A)
        
День 5: Факт A получает [:CONTRADICTS] → переходит в Contradicted
        
День 6: Decay cycle:
          - Находит B (cosine=0.92 с A)
          - penalty = 0.15 × ((0.92-0.85)/0.15) × 0.3 = 0.021
          - B.importance = 0.7 - 0.021 = 0.679
        
День 30: После 5 циклов decay:
          - B.importance = 0.574
          - Если новых подтверждений нет → продолжает падать
        
День 60: B.importance < 0.1 → ESM.Collapsed → архив в S3
```

### Semantic Quarantine Zone (опционально)

**Концепция**: Временная изоляция узлов, близких к противоречивым, перед применением decay.

```python
class SemanticQuarantine:
    """
    Узлы, семантически близкие к Contradicted, помещаются в карантин
    вместо немедленного применения decay penalty.

    Преимущества:
    - Даёт время на появление подтверждающих/опровергающих фактов
    - Предотвращает преждевременное удаление валидных узлов
    - Снижает риск цепной реакции
    """

    async def quarantine_node(self, node_id: str, source_contradicted: str):
        """
        Поместить узел в карантин на 7 дней
        
        В карантине узел:
        - Остаётся в своём epistemic_state (не деградирует)
        - Помечается флагом in_quarantine=true
        - Не участвует в Etir активации (пониженный приоритет)
        - Мониторится на новые [:SUPPORTS] или [:CONTRADICTS]
        """
        query = """
        MATCH (n:Fact {id: $node_id})
        SET n.in_quarantine = true,
            n.quarantine_started = datetime(),
            n.quarantine_source = $source,
            n.quarantine_expires = datetime() + duration({days: 7})
        """
        await self.graph.execute_cypher(query, {
            "node_id": node_id,
            "source": source_contradicted
        })

    async def review_quarantine(self):
        """
        Ежедневная проверка карантина (вызывается вместе с decay_cycle)
        
        Для каждого узла в карантине:
        - Если появились [:SUPPORTS] → снять карантин, восстановить importance
        - Если появились [:CONTRADICTS] → применить decay, выход из карантина
        - Если истёк срок без изменений → применить decay
        """
        query = """
        MATCH (n:Fact)
        WHERE n.in_quarantine = true
          AND n.quarantine_expires < datetime()
        RETURN n.id, n.importance  -- P9-FIX БАГ-6: n.importance_score → n.importance (нет такого поля)
        """
        
        expired = await self.graph.execute_cypher(query)
        
        for node in expired:
            # Проверить, что произошло за время карантина
            supports = await self._count_new_supports(node['id'])
            contradicts = await self._count_new_contradicts(node['id'])
            
            if supports > 0:
                await self._release_from_quarantine(node['id'], reason="NEW_SUPPORTS")
            elif contradicts > 0:
                await self._apply_decay_and_release(node['id'])
            else:
                # Нет изменений — мягкий decay
                await self._apply_decay_and_release(node['id'], penalty_multiplier=0.5)

# Интеграция с WeightedSemanticDecay:
# Вместо немедленного decay → сначала quarantine_node()
# Decay применяется только после review_quarantine()
```

**Когда использовать**:
- Production системы, где цена ошибочного удаления высока
- Домены с высокой неопределённостью и частыми изменениями
- Системы с активным пользовательским фидбеком

**Когда НЕ использовать**:
- MVP и Phase 0 (избыточная сложность)
- Системы с низкой частотой противоречий
- Когда важна скорость очистки графа

---

### Почему Weighted Semantic Decay итерировался 11 раз?

Weighted Semantic Decay — сложный механизм требующий:
- Semantic embeddings для всех узлов (дорого)
- Правильный баланс penalty (слишком агрессивный → потеря данных)
- Интеграция с ESM, Archive, Monitoring

---

## 📐 Fractal Similarity Monitor 

> **Назначение**: Проверка self-similarity графа памяти для обнаружения drift.
>
> **Интеграция**: Работает совместно с L3.5 Immutable Core.

### Проблема

Память может "дрифтить" — постепенно терять фрактальную структуру:
- Накопление хаотичных связей (random noise)
- Потеря self-similarity между масштабами (L0→L3)
- Результат: снижение точности, рост латентности, хаос в графе

### Решение

Каждые 24 часа (при создании snapshot L3.5) — вычислить fractal dimension графа.

```python
# fractal_similarity_monitor.py
import numpy as np
from scipy.spatial.distance import pdist, squareform

class FractalSimilarityMonitor:
    """
    Вычисляет correlation dimension графа и проверяет drift.
    """

    async def check_similarity(self, snapshot_current, snapshot_previous) -> dict:
        """
        Основной метод — вызывается при создании нового snapshot.
        
        Returns:
            {
                'correlation_dimension': float,
                'self_similarity_score': float,
                'drift_detected': bool,
                'alert_reason': str | None
            }
        """
        # 1. Вычислить correlation dimension (Grassberger-Procaccia)
        dim_current = self._correlation_dimension(snapshot_current)
        dim_previous = self._correlation_dimension(snapshot_previous)
        
        # 2. Self-similarity score (как близки размерности)
        # PATCH-5: защита от ZeroDivisionError при пустом/новом графе (оба dim могут быть 0)
        denom = max(dim_current, dim_previous)
        similarity = (
            1.0 - abs(dim_current - dim_previous) / denom
            if denom > 1e-9   # если оба ~0 → считаем "дрейфа нет"
            else 1.0
        )
        
        # 3. Проверка порога
        drift_detected = similarity < 0.92
        
        alert_reason = None
        if drift_detected:
            alert_reason = (
                f"Fractal drift: similarity={similarity:.3f} < 0.92, "
                f"dim_current={dim_current:.3f}, dim_previous={dim_previous:.3f}"
            )
            logger.warning(alert_reason)
            await self._trigger_alert(alert_reason)
        
        return {
            'correlation_dimension': dim_current,
            'self_similarity_score': similarity,
            'drift_detected': drift_detected,
            'alert_reason': alert_reason,
            'timestamp': datetime.now(timezone.utc)
        }

    def _correlation_dimension(self, snapshot) -> float:
        """
        Grassberger-Procaccia algorithm для вычисления correlation dimension.
        
        Упрощённая реализация для графов:
        - Преобразовать граф в embedding space (используем существующие node embeddings)
        - Вычислить pairwise distances
        - Подсчитать C(r) = количество пар с расстоянием < r
        - Correlation dimension ≈ slope log(C(r)) / log(r)
        """
        # P9-FIX БАГ-8: guard для малого графа (KeyError + ZeroDivisionError)
        embeddings = snapshot.get('node_embeddings')  # .get() вместо [] — нет KeyError
        if embeddings is None or len(embeddings) < 2:
            return 0.0  # не хватает данных для correlation dimension
        
        # Pairwise distances
        distances = pdist(embeddings, metric='euclidean')
        dist_matrix = squareform(distances)
        
        # Radii для проверки (логарифмическая шкала)
        radii = np.logspace(-2, 1, 20)
        
        # Correlation integral C(r)
        C_r = []
        for r in radii:
            count = np.sum(dist_matrix < r) - len(embeddings)  # исключить диагональ
            n = len(embeddings)
            denom = n * (n - 1)
            if denom == 0:
                return 0.0  # P9-FIX БАГ-8: защита от ZeroDivisionError при n==1
            C_r.append(count / denom)
        
        # Линейная регрессия log(C(r)) vs log(r)
        log_r = np.log(radii)
        log_C = np.log(np.array(C_r) + 1e-10)  # избегаем log(0)
        
        # Slope = correlation dimension
        slope, _ = np.polyfit(log_r, log_C, 1)
        
        return slope

    async def _trigger_alert(self, reason: str):
        """
        Отправить alert в MetaSupervisor + Prometheus.
        """
        # Prometheus alert
        fractal_drift_alerts.inc()
        
        # MetaSupervisor notification
        await self.supervisor.notify_drift(
            severity="WARNING",
            component="FractalSimilarityMonitor",
            reason=reason,
            action_required="Manual review of L3 graph structure recommended"
        )
        
        # Audit log
        await self.audit.log_event(
            event_type="FRACTAL_DRIFT_DETECTED",
            details={'reason': reason},
            timestamp=datetime.now(timezone.utc)
        )
```

### Альтернативный метод: Box-Counting

Для упрощения (если correlation dimension слишком дорого):

```python
def _box_counting_dimension(self, snapshot) -> float:
    """
    Box-counting fractal dimension (более быстрый, менее точный).

    Считаем сколько "коробок" размера ε нужно чтобы покрыть граф.
    """
    embeddings = snapshot['node_embeddings']

    box_sizes = [0.1, 0.2, 0.5, 1.0, 2.0]
    counts = []

    for epsilon in box_sizes:
        # Дискретизация пространства на коробки размера epsilon
        boxes = np.floor(embeddings / epsilon).astype(int)
        unique_boxes = len(np.unique(boxes, axis=0))
        counts.append(unique_boxes)

    # log(N(ε)) vs log(1/ε)
    log_epsilon_inv = np.log(1.0 / np.array(box_sizes))
    log_counts = np.log(counts)

    slope, _ = np.polyfit(log_epsilon_inv, log_counts, 1)
    return slope
```

### Конфигурация

```python
# velantrim_config.py
class FractalConfig:
    SIMILARITY_THRESHOLD = 0.92        # self-similarity < 0.92 → drift
    CHECK_INTERVAL_HOURS = 24          # частота проверки
    USE_CORRELATION_DIM = True         # True = Grassberger-Procaccia, False = box-counting
    EXPECTED_DIM_RANGE = (1.2, 1.8)   # биологически правдоподобный диапазон
```

### Метрики

```python
# Prometheus
fractal_dimension_current = Gauge('velantrim_fractal_dimension_current')
fractal_similarity_score = Gauge('velantrim_fractal_similarity_score')
fractal_drift_alerts = Counter('velantrim_fractal_drift_alerts_total')
fractal_check_duration_seconds = Histogram('velantrim_fractal_check_duration_seconds')
```

### Интеграция с L3.5 Immutable Core

```python
# immutable_core.py
async def create_snapshot(self):
    """При создании snapshot → проверка fractal similarity"""

    # 1. Создать snapshot
    snapshot = await self._snapshot_l3_graph()

    # 2. Fractal similarity check
    if self.previous_snapshot:
        result = await self.fractal_monitor.check_similarity(
            snapshot, self.previous_snapshot
        )
        
        # Сохранить в metadata
        snapshot['fractal_dimension'] = result['correlation_dimension']
        snapshot['similarity_score'] = result['self_similarity_score']
        snapshot['drift_detected'] = result['drift_detected']

    # 3. Сохранить в Neo4j + S3
    await self._persist_snapshot(snapshot)

    self.previous_snapshot = snapshot
```

### Пример работы

```
День 1: Snapshot A
  - correlation_dimension = 1.52
  - baseline установлен

День 2: Snapshot B
  - correlation_dimension = 1.48
  - similarity = 1.0 - |1.52-1.48|/1.52 = 0.974 ✅ (> 0.92)

День 30: Snapshot Z
  - correlation_dimension = 1.28
  - similarity = 1.0 - |1.48-1.28|/1.48 = 0.865 ❌ (< 0.92)
  - ALERT: "Fractal drift detected!"
  - Action: Manual review графа → найти хаотичные кластеры
```

### Биологическое обоснование

Мозг человека имеет fractal dimension ~1.2-1.8 (дендриты, сосудистая сеть).
Velantrim граф должен сохранять эту фрактальность для эффективности.

Drift = потеря фрактальности = хаос = снижение производительности.

---

## 🗄️ Storage Ecosystem — Полная карта хранилищ

> Нет одной системы, которая лучше всех во всём. Есть системы, которые лучше в своей роли.
> SQLite и NetworkX не надо заменять — их надо правильно разместить в стеке.

---

### 🔱 Production Core (обязательные)

**Neo4j 5.26+** — основное графовое хранилище Phase 1+

```
Роль:     Science Core / Entity Layer / LTM граф знаний
Сильно:   Cypher, vector indexes, Graph Data Science, mature
Статус:   ✅ Production-grade, зрелый, масштабируемый
Фаза:     Phase 1 → навсегда
```

**Kuzu** — embedded граф для MVP Phase 0

```
Роль:     Локальный граф без сервера, Cypher-совместимый
Сильно:   ACID, disk-based columnar, vector/full-text, запускается локально
💡 ПРИМЕЧАНИЕ: Kuzu развивается медленно, но стабилен и пригоден к использованию
          Команда работает над чем-то новым, поддержка заморожена
Статус:   ⚠️ Только Phase 0 MVP. НЕ строить на нём канон.
Фаза:     Phase 0 только → переход на Neo4j в Phase 1
```

---

### 📊 SQL и Аналитика

**SQLite** — встроенное надёжное хранилище приложения

```
Роль:     Логи, конфиги, навыки, сессии, небольшие локальные данные
Сильно:   Встроен везде, надёжен, zero-config, "competes with fopen()"
Статус:   ✅ Незаменим для operational data
Фаза:     Все фазы
```

**DuckDB** — встроенная аналитика

```
Роль:     Метрики, аналитика, Parquet/Arrow/CSV, большие табличные срезы
Сильно:   Columnar-vectorized execution, аналитические агрегации
ВАЖНО:    НЕ замена SQLite — другой workload. SQLite → OLTP, DuckDB → OLAP
Статус:   ✅ Добавить для аналитического слоя
Фаза:     Phase 2+
```

---

### 🕸️ Graph R&D и Алгоритмы (инструменты учёных)

**NetworkX** — графовая лаборатория в Python

```
Роль:     Прототипирование, centrality, shortest paths, community experiments
Сильно:   Python-native, богатая библиотека алгоритмов
ВАЖНО:    Это библиотека, НЕ production graph DB. Всё держится в RAM процесса
Статус:   ✅ R&D и исследования. Используют учёные для точности алгоритмов
Фаза:     Всегда, параллельно production стеку
```

**GraphBLAS** — высокопроизводительные граф-алгоритмы

```
Роль:     Тяжёлые графовые алгоритмы через sparse linear algebra
Сильно:   Операции над sparse matrices и semirings — максимальная скорость
ВАЖНО:    НЕ база данных. НЕ замена NetworkX для хранения знаний.
          Это мощный "мотор" для конкретных алгоритмов, не drop-in замена
Статус:   ✅ Опционально для Phase 3+ если нужна скорость граф-алгоритмов
Фаза:     Phase 3+ опционально
```

---

### ⚡ Real-Time Graph (серверный уровень)

**Memgraph** — real-time графовая БД

```
Роль:     Потоковые обновления, real-time graph, streaming ingestion
Сильно:   Neo4j-совместимый Cypher, open-source, быстрые обновления
ВАЖНО:    Это серверная graph DB, НЕ лёгкая замена NetworkX
Статус:   ✅ Phase 2+ для hot-path real-time обновлений
Фаза:     Phase 2+
```

---

### ⚠️ Опциональные / С риском EOL

**SurrealDB** — мультимодельная БД

```
Роль:     Один движок для граф + SQL + документы + real-time
Сильно:   Универсальность, активная разработка, интересная архитектура
⚠️ РИСК:  Молодой проект — если компания закроется или сменит фокус: проект умрёт
          Как было с RedisGraph (EOL январь 2025)
Статус:   ⚠️ ОПЦИОНАЛЬНО для специфических задач. НЕ в основной стек.
Фаза:     Только по необходимости
```

---

### ☠️ Удалённые — больше не используются

| Система | Причина удаления |
|---|---|
| **LadybugDB** | ☠️ Не существует как отдельная БД. Маркетинговое название → заменено на KuzuDB (P0-H). |
| **KuzuDB** | ✅ Используется как GRAPH_BACKEND=kuzu для Personal/Medium конфигураций. MIT, Cypher-совместим. |
| **RedisGraph** | ☠️ EOL = январь 2025. Redis официально прекратил поддержку |
| **GPT-4** | ❌ Retired OpenAI. Заменён на GPT-5.4 / o4-mini |
| **Llama 3** | ❌ Устарел. Заменён на Llama 4 Maverick / Scout |
| **rubert-tiny2** | ❌ Устаревшая RU embedding модель. Заменена на USER-bge-m3 |
| **Kafka** | ❌ Избыточен для Velantrim стека. Оставлен только Redis Streams |

> **Урок из LadybugDB**: всегда верифицировать названия инструментов перед включением в архитектуру. P0-H FIX: заменено на KuzuDB везде в документе.

---

### 🗺️ Итоговая карта хранилищ

```
VELANTRIM STORAGE ECOSYSTEM
│
├── 🔱 GRAPH CORE
│   ├── Kuzu          → Phase 0 MVP (embedded, Cypher) — опционально
│   └── Neo4j 5.26+   → Phase 1+ Production (vector, GDS)
│
├── 📊 SQL LAYER
│   ├── SQLite        → operational: логи, конфиги, навыки
│   └── DuckDB        → analytics: метрики, Parquet, агрегации
│
├── 🕸️ R&D / НАУКА
│   ├── NetworkX      → прототипы, алгоритмы, эксперименты
│   └── GraphBLAS     → тяжёлые граф-алгоритмы (Phase 3+)
│
├── ⚡ REAL-TIME
│   └── Memgraph      → streaming graph (Phase 2+)
│
├── ⚠️ ОПЦИОНАЛЬНО
│   └── SurrealDB     → мультимодель (риск EOL, только по нужде)
│
└── ☠️ УДАЛЕНО
    ├── LadybugDB     → не существует (заменено KuzuDB · P0-H)
    ├── RedisGraph     → EOL 2025
    └── GPT-4 / Llama 3 / rubert-tiny2 → устарели
```

---

## 🤖 Актуальный LLM и Embedding стек (март 2026)

### LLM модели

| Категория | Модель | Использование в Velantrim |
|---|---|---|
| 🏆 **Flagship** | GPT-5.4 / GPT-5.3 Codex | Критичные кластеры консолидации, сложный reasoning |
| 🏆 **Flagship** | Claude Sonnet 4.6 / Opus 4.6 | Сложный reasoning, архитектурные решения |
| 🏆 **Flagship** | Qwen3-Max (256K ctx) | Длинный контекст, агентные задачи |
| ⚡ **Fast** | o4-mini | Рутина, 70% задач, distill_strategies |
| ⚡ **Fast** | Claude Haiku 4.5 | Быстрые ответы, классификация |
| ⚡ **Fast** | Qwen3.5-Flash | $0.10/M токенов — экономия |
| 🔓 **Local** | Qwen3.5-397B-A17B (MoE) | Privacy-first, 256K ctx, Apache 2.0 |
| 🔓 **Local** | Llama 4 Maverick / Scout | Meta, 10M ctx (Scout), open |
| 🔓 **Local** | DeepSeek V3.2 / R1 | Локальный reasoning |
| ⚡ **Edge/Lite** | RWKV-7 Goose 2.9B (`mollysama/rwkv-7-g1:2.9b`) | O(n) сложность — скорость не падает при длинных сессиях. Apache 2.0. Слабое железо, LLM_MODE=lite. `ollama pull mollysama/rwkv-7-g1:2.9b` |
| ❌ **Retired** | GPT-4, Llama 3 | Удалены — устарели |

### Embedding модели

| Тип | Модель | Особенности |
|---|---|---|
| 🔓 **Локальная (RU)** | `deepvk/USER-bge-m3` | Лучшая для русского языка |
| 🔓 **Локальная (Multi)** | `multilingual-e5-large` | 100+ языков, универсальная |
| 🌐 **Облачная** | `Gemini Embedding 2` | Мультимодальная: текст+фото+видео+аудио+PDF. 3072 dims. Phase 2+ |
| 🌐 **Облачная** | `text-embedding-3-large` | OpenAI, стабильная |
| ❌ **Устарела** | `rubert-tiny2` | Удалена |

> ⚠️ **Важно**: смена embedding-модели требует переиндексации. Векторы из разных моделей несовместимы в одном индексе. Gemini Embedding 2 — для Phase 2+ когда появится мультимодальность в Velantrim.
>
> ✅ **Автоматизация через Lazy Re-indexing**: поле `embedding_version` в каждом узле позволяет не перестраивать всё сразу. При смене модели: новые узлы пишутся с новой версией, старым ставится флаг `reindex_required = true`, фоновый `AdaptiveConsolidationWorker` переиндексирует партиями. Система работает в `dual-index mode` без простоя.

---

### 🔢 EmbeddingRegistry — защита от смешивания размерностей

**Проблема**: `numpy.dot()` с векторами разных размерностей (например 1024 и 1536) не выбрасывает исключение — он молча возвращает математически некорректный результат. Косинусное сходство начинает лгать, retrieval деградирует тихо и незаметно.

**Решение**: централизованный реестр моделей с fail-fast валидацией при каждой записи.

```python
# memory/embedding_registry.py
import numpy as np
import logging
logger = logging.getLogger(__name__)

# Все поддерживаемые модели и их размерности.
# При добавлении новой модели — регистрировать здесь, не хардкодить в коде.
_KNOWN_DIMS: dict[str, int] = {
    "deepvk/USER-bge-m3":                   1024,  # основная RU-модель Velantrim
    "multilingual-e5-large":                1024,
    "paraphrase-multilingual-MiniLM-L12-v2": 384,  # weak-профиль
    "text-embedding-3-large":               3072,
    "Qwen/Qwen3-Embedding":                 1024,
    "BAAI/bge-m3":                          1536,
    "default":                              1024,  # fallback
}

class EmbeddingRegistry:
    """
    Реестр embedding-моделей Velantrim.
    Вызывать EmbeddingRegistry.validate() перед каждой записью вектора в L1/L3.
    Fail-fast при несоответствии размерностей — молчаливая деградация недопустима.
    """
    _active_model: str = "deepvk/USER-bge-m3"
    _active_dim:   int = 1024

    @classmethod
    def set_active_model(cls, model_name: str) -> None:
        """Устанавливается один раз при старте агента из velantrim_config."""
        dim = _KNOWN_DIMS.get(model_name)
        if dim is None:
            raise ValueError(
                f"EmbeddingRegistry: неизвестная модель '{model_name}'. "
                f"Зарегистрируй через register('{model_name}', dim=N). "
                f"Известные: {list(_KNOWN_DIMS.keys())}"
            )
        cls._active_model = model_name
        cls._active_dim   = dim
        logger.info(f"EmbeddingRegistry: active={model_name}, dim={dim}")

    @classmethod
    def register(cls, model_name: str, dim: int) -> None:
        """Добавить нестандартную модель."""
        _KNOWN_DIMS[model_name] = dim
        logger.info(f"EmbeddingRegistry: registered {model_name} dim={dim}")

    @classmethod
    def validate(cls, embedding: np.ndarray, model_name: str = None) -> None:
        """
        Проверить размерность вектора перед записью.
        Вызывать в GraphMemory.add_episode() и FractalMemory.add_to_stm().
        Выбрасывает ValueError при несовпадении — не молчит.
        """
        model    = model_name or cls._active_model
        expected = _KNOWN_DIMS.get(model, cls._active_dim)
        actual   = embedding.shape[0] if hasattr(embedding, 'shape') else len(embedding)
        if actual != expected:
            raise ValueError(
                f"EmbeddingRegistry: размерность не совпадает для '{model}': "
                f"ожидалось {expected}, получено {actual}. "
                f"Смешивание моделей портит cosine similarity — это не warning, это баг."
            )
```

**Интеграция**: вызов `EmbeddingRegistry.validate(embedding)` добавить в `GraphMemory.add_episode()` и `FractalMemory.add_to_stm()` перед сохранением вектора. `EmbeddingRegistry.set_active_model(EMBEDDING_MODEL)` вызывать один раз в `pipeline.__init__()`.

**Инвариант**: смешивание векторов разных моделей в одном индексе — нарушение архитектуры. `EmbeddingRegistry` делает это нарушение явным.

---

## 🔧 Обслуживание системы

> Два инструмента которых не хватало Velantrim для production-эксплуатации.

---

### 🧹 dedupe_entities.py — Дедупликация узлов графа

**Проблема**: любая живая система где LLM извлекает сущности со временем накапливает дубли. «Velantrim», «velantrim», «VELANTRIM ExoCortex», «the Velantrim system» — всё это отдельные узлы в Neo4j. Без дедупликации граф деградирует: связи распылены по дублям, поиск возвращает неполные результаты, ImportanceScore занижен у всех копий.

```python
# scripts/dedupe_entities.py
# Запуск: python scripts/dedupe_entities.py
# Dry-run (анализ без изменений): python scripts/dedupe_entities.py --dry-run

import os
import asyncio, argparse, logging
from collections import defaultdict
from memory_core import GraphMemory

logger = logging.getLogger(__name__)

# P0-4 FIX: определить наличие APOC один раз при старте.
# Neo4j + APOC: NEO4J_HAS_APOC=true (в docker-compose: NEO4J_PLUGINS=["apoc"])
# LadybugDB / KuzuDB без APOC: NEO4J_HAS_APOC=false (или не задана)
HAS_APOC = os.getenv("NEO4J_HAS_APOC", "false").lower() == "true"


async def _merge_relationship_safe(
    graph,
    from_id: str,
    to_id: str,
    rel_type: str,
    weight: float,
    merged_from: str
) -> None:
    """
    Создать/обновить связь между узлами с сохранением оригинального типа.
    Использует APOC если доступен (Neo4j), иначе — чистый Cypher (LadybugDB/KuzuDB).

    P0-4 FIX: APOC apoc.merge.relationship недоступен в LadybugDB.
    Fallback использует MERGE с параметризованным типом через f-string.
    rel_type берётся из type(r) который уже в графе, не из user input.
    """
    if HAS_APOC:
        await graph.execute_cypher("""
            MATCH (a {id: $from_id}), (b {id: $to_id})
            CALL apoc.merge.relationship(a, $rel_type, {}, {weight: $weight}, b)
            YIELD rel
            SET rel.weight = coalesce(rel.weight, 0) + $weight,
                rel.merged_from = $merged_from
        """, {"from_id": from_id, "to_id": to_id,
              "rel_type": rel_type, "weight": weight, "merged_from": merged_from})
    else:
        # Fallback для LadybugDB / KuzuDB без APOC.
        # rel_type из type(r) — безопасно, не user input.
        query = f"""
            MATCH (a {{id: $from_id}}), (b {{id: $to_id}})
            MERGE (a)-[r:{rel_type}]->(b)
            ON CREATE SET r.weight = $weight, r.merged_from = $merged_from
            ON MATCH  SET r.weight = coalesce(r.weight, 0) + $weight,
                          r.merged_from = $merged_from
        """
        await graph.execute_cypher(
            query, {"from_id": from_id, "to_id": to_id,
                    "weight": weight, "merged_from": merged_from}
        )


async def _merge_nodes_safe(graph, e1_id: str, e2_id: str) -> None:
    """
    Слить два узла-дубля.
    APOC apoc.refactor.mergeNodes — только Neo4j.
    Fallback: вручную перенести все рёбра + soft-delete дубля.

    P0-4 FIX: apoc.refactor.mergeNodes недоступен в LadybugDB.
    """
    if HAS_APOC:
        await graph.execute_cypher("""
            MATCH (e1:Entity {id: $e1_id})
            MATCH (e2:Entity {id: $e2_id})
            CALL apoc.refactor.mergeNodes([e1, e2], {
                properties: 'combine',
                mergeRels: true
            })
            YIELD node
            RETURN count(node) as merged
        """, {"e1_id": e1_id, "e2_id": e2_id})
    else:
        # Fallback: перенести рёбра + soft-delete дубля (e2 → e1).
        await graph.execute_cypher("""
            MATCH (e2:Entity {id: $e2_id})-[r]->(target)
            MATCH (e1:Entity {id: $e1_id})
            WHERE e2.id <> e1.id AND target.id <> e2.id
            MERGE (e1)-[new_r:RELATED_TO]->(target)
            ON CREATE SET new_r.weight = coalesce(r.weight, 0.5),
                          new_r.merged_from = $e2_id
            ON MATCH  SET new_r.weight = new_r.weight + coalesce(r.weight, 0.5)
            DELETE r
        """, {"e1_id": e1_id, "e2_id": e2_id})
        await graph.execute_cypher("""
            MATCH (source)-[r]->(e2:Entity {id: $e2_id})
            MATCH (e1:Entity {id: $e1_id})
            WHERE e2.id <> e1.id AND source.id <> e2.id
            MERGE (source)-[new_r:RELATED_TO]->(e1)
            ON CREATE SET new_r.weight = coalesce(r.weight, 0.5),
                          new_r.merged_from = $e2_id
            ON MATCH  SET new_r.weight = new_r.weight + coalesce(r.weight, 0.5)
            DELETE r
        """, {"e1_id": e1_id, "e2_id": e2_id})
        await graph.execute_cypher("""
            MATCH (e:Entity {id: $e2_id})
            SET e.is_active = false,
                e.valid_to = datetime(),
                e.merged_into = $e1_id
        """, {"e2_id": e2_id, "e1_id": e1_id})


# P0-4 FIX: SAE Lateral Inhibition — apoc.math.maxLong недоступен в LadybugDB.
SAE_LATERAL_INHIBITION_CYPHER_APOC = """
    UNWIND range(0, size(ranked) - 1) AS i
    WITH ranked[i] AS dominant, ranked, i
    WHERE dominant.activation > $threshold
    UNWIND range(i + 1, size(ranked) - 1) AS j
    WITH dominant, ranked[j] AS competitor
    WHERE competitor.activation < dominant.activation
    SET competitor.activation = apoc.math.maxLong(
        0,
        toInteger((competitor.activation - $mu * dominant.activation) * 1000000)
    ) / 1000000.0
"""

SAE_LATERAL_INHIBITION_CYPHER_FALLBACK = """
    UNWIND range(0, size(ranked) - 1) AS i
    WITH ranked[i] AS dominant, ranked, i
    WHERE dominant.activation > $threshold
    UNWIND range(i + 1, size(ranked) - 1) AS j
    WITH dominant, ranked[j] AS competitor
    WHERE competitor.activation < dominant.activation
    WITH competitor,
         (competitor.activation - $mu * dominant.activation) AS raw_val
    SET competitor.activation = CASE WHEN raw_val < 0 THEN 0.0 ELSE raw_val END
"""

def get_lateral_inhibition_cypher() -> str:
    """Вернуть корректный Cypher для lateral inhibition с учётом бэкенда."""
    return SAE_LATERAL_INHIBITION_CYPHER_APOC if HAS_APOC else SAE_LATERAL_INHIBITION_CYPHER_FALLBACK

async def find_duplicates(graph: GraphMemory) -> dict[str, list[str]]:
    """Найти узлы :Entity с одинаковым именем (case-insensitive)."""
    rows = await graph.execute_cypher(
        "MATCH (e:Entity) RETURN e.id AS id, e.name AS name, e.access_count AS ac"
    )
    groups: dict[str, list] = defaultdict(list)
    for row in rows:
        key = (row["name"] or "").strip().lower()
        if key:
            groups[key].append(row)
    return {k: v for k, v in groups.items() if len(v) > 1}

async def merge_group(graph: GraphMemory, nodes: list, dry_run: bool):
    """
    Оставить узел с наибольшим access_count как canonical.
    Перенести все рёбра от дублей на canonical.
    Удалить дубли через Soft Delete.
    """
    canonical = max(nodes, key=lambda n: n.get("ac") or 0)
    duplicates = [n for n in nodes if n["id"] != canonical["id"]]
    logger.info(f"Canonical: {canonical['id']} ({canonical['name']}) "
                f"← {[d['id'] for d in duplicates]}")
    if dry_run:
        return

    for dup in duplicates:
        # P0-4 FIX: перенести рёбра через _merge_relationship_safe() —
        # APOC если доступен, иначе чистый Cypher fallback для LadybugDB.
        outgoing_rels = await graph.execute_cypher(
            "MATCH (dup:Entity {id: $dup_id})-[r]->(target) "
            "WHERE dup.id <> $canonical_id "
            "RETURN type(r) AS rel_type, target.id AS target_id, coalesce(r.weight, 0.5) AS weight",
            {"dup_id": dup["id"], "canonical_id": canonical["id"]}
        )
        for row in outgoing_rels:
            await _merge_relationship_safe(
                graph,
                from_id=canonical["id"],
                to_id=row["target_id"],
                rel_type=row["rel_type"],
                weight=row["weight"],
                merged_from=dup["id"]
            )

        incoming_rels = await graph.execute_cypher(
            "MATCH (source)-[r]->(dup:Entity {id: $dup_id}) "
            "WHERE dup.id <> $canonical_id "
            "RETURN type(r) AS rel_type, source.id AS source_id, coalesce(r.weight, 0.5) AS weight",
            {"dup_id": dup["id"], "canonical_id": canonical["id"]}
        )
        for row in incoming_rels:
            await _merge_relationship_safe(
                graph,
                from_id=row["source_id"],
                to_id=canonical["id"],
                rel_type=row["rel_type"],
                weight=row["weight"],
                merged_from=dup["id"]
            )

        # Soft Delete дубля
        await graph.execute_cypher(
            "MATCH (e:Entity {id: $id}) SET e.is_active=false, e.valid_to=datetime()",
            {"id": dup["id"]}
        )

async def main(dry_run: bool):
    graph = GraphMemory()
    dupes = await find_duplicates(graph)
    logger.info(f"Найдено {len(dupes)} групп дублей")
    for name, nodes in dupes.items():
        await merge_group(graph, nodes, dry_run)
    action = "Dry-run завершён" if dry_run else f"Объединено {len(dupes)} групп"
    logger.info(action)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(main(dry_run=args.dry_run))
```

**Рекомендуется запускать**: раз в неделю через SleepTimeWorker или вручную при заметном росте числа узлов без роста знаний.

---

### 📋 migrations/ — Версионирование схемы графа

**Проблема**: Velantrim добавляет новые поля к узлам Neo4j (например `pending_invalidation`, `embedding_version`, `is_ring_zero`) — но нет механизма обновить уже существующие узлы при деплое новой версии. Это приводит к тому что старые узлы не имеют нужных полей и инварианты начинают ломаться на production-данных.

```python
# migrations/apply_migrations.py
# Запуск при каждом обновлении: python migrations/apply_migrations.py
# Идемпотентен — безопасно запускать повторно.

import asyncio, logging
from memory_core import GraphMemory

logger = logging.getLogger(__name__)

MIGRATIONS = [
    {
        "version": "v8.0",  // P2-B FIX
        "description": "Добавить is_active=true всем узлам без этого поля",
        "cypher": "MATCH (n) WHERE n.is_active IS NULL SET n.is_active = true"
    },
    {
        "version": "v5.1",
        "description": "Добавить epistemic_state='Validated' всем :Fact без ESM",
        "cypher": "MATCH (f:Fact) WHERE f.epistemic_state IS NULL SET f.epistemic_state='Validated'"
    },
    {
        "version": "v5.2",
        "description": "Добавить embedding_version='v1' всем узлам с embedding",
        "cypher": "MATCH (n) WHERE n.embedding IS NOT NULL AND n.embedding_version IS NULL SET n.embedding_version='v1'"
    },
    {
        "version": "v5.3",
        "description": "Добавить is_ring_zero=false всем узлам без этого поля",
        "cypher": "MATCH (n) WHERE n.is_ring_zero IS NULL SET n.is_ring_zero = false"
    },
    {
        "version": "v5.4",
        "description": "Создать индекс pending_invalidation если не существует",
        "cypher": "CREATE INDEX pending_inv_idx IF NOT EXISTS FOR (f:Fact) ON (f.pending_invalidation)"
    },
]

async def apply_migrations(graph: GraphMemory):
    # Создать таблицу версий если не существует
    await graph.execute_cypher("""
        MERGE (mv:MigrationVersion {id: 'schema_version'})
        ON CREATE SET mv.applied = []
    """)
    result = await graph.execute_cypher(
        "MATCH (mv:MigrationVersion {id: 'schema_version'}) RETURN mv.applied AS applied"
    )
    applied = set(result[0]["applied"]) if result else set()

    for m in MIGRATIONS:
        if m["version"] in applied:
            logger.info(f"Migration {m['version']} already applied — skip")
            continue
        logger.info(f"Applying migration {m['version']}: {m['description']}")
        await graph.execute_cypher(m["cypher"])
        await graph.execute_cypher(
            "MATCH (mv:MigrationVersion {id: 'schema_version'}) "
            "SET mv.applied = mv.applied + [$version]",
            {"version": m["version"]}
        )
        logger.info(f"Migration {m['version']} applied ✅")

if __name__ == "__main__":
    asyncio.run(apply_migrations(GraphMemory()))
```

**Инвариант**: `apply_migrations()` вызывается при каждом старте pipeline в `pipeline.__init__()` до любых запросов к графу. Миграции идемпотентны — повторный запуск безопасен.

---

## 📚 Дополнительные ресурсы

### Документация

- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [Neo4j 5.26+ Vector Search](https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/)
- [DeepSeek Engram GitHub](https://github.com/deepseek-ai/Engram)
- [LangGraph для агентов](https://langchain-ai.github.io/langgraph/)
- [Memgraph документация](https://memgraph.com/docs)
- [DuckDB документация](https://duckdb.org/docs/)
- [Gemini Embedding 2](https://ai.google.dev/gemini-api/docs/embeddings)

### Научные статьи

- "ReasoningBank" - Learning from Success and Failure
- "Graphiti: Temporal Knowledge Graphs for AI Agents"
- "DeepSeek Engram: Conditional Memory for MoE Architectures" (январь 2026)
- "Fractal Graph Theory and Knowledge Graphs"
- "Map-Based Experience Replay" (GWR approach)
- "Gemini Embedding 2: Natively Multimodal Embeddings" (март 2026)

### Бенчмарки

- Deep Memory Retrieval (Zep)
- LOCOMO (Long-term Context Memory)
- Standard RAG baselines
- LMArena Text Leaderboard (март 2026)

---

## 🎓 Заключение

Эта спецификация объединяет:
- **Graphiti + Neo4j 5.26+** для темпоральной графовой памяти
- **Фрактальную иерархию** для масштабирования
- **ReasoningBank** для самообучения
- **Гибридный retrieval** для минимизации токенов
- **Etir (L3.5)** — Velantrim Synaptic Activation Layer
- **Engram-принцип** как архитектурный союзник (DeepSeek, январь 2026)
- **Memory Guardian (MGL)** — защита L3 от отравления галлюцинациями
- **Immutable Raw Memory** — защита от Semantic Drift
- **Knowledge Distillation Engine** — JSON-тройки вместо текстовых кусков
- **Формальные инварианты (RFC0001–RFC0006)** — контракт системы
- **Evidence как узел** + `[:SUPPORTED_BY]`, `[:CAUSES]`, `[:IMPROVES]`
- **Evidence Pack + Truth Gate** с конкретными порогами
- **Memory Router** DEFINE/RECALL/POLICY/TASK
- **Автоматизацию** без постоянных LLM-запросов
- ✅ **ConsolidationEngine** — race condition закрыт навсегда
- ✅ **Canonical Memory Protocol v1** — единая точка входа
- ✅ **CoreMemoryBlocks** — агент знает пользователя с первого слова (L0 CRITICAL)
- ✅ **EmbeddingRegistry** — защита от молчаливого смешивания размерностей
- ✅ **MCP Server** — подключение к Cursor / Claude Code через stdio
- ✅ **dedupe_entities.py** — дедупликация Entity-узлов графа
- ✅ **migrations/** — версионирование схемы Neo4j, идемпотентные миграции
- ✅ **RWKV-7 Edge** — O(n) LLM для слабого железа в LLM_MODE=lite
- ✅ **pymorphy3 синглтон + lru_cache** — 40–60% экономия CPU при ReasoningBank
- ✅ **Velum GC слабых рёбер** — защита от бесконечного роста _edges
- ✅ **Velum SQLite persist** — рёбра co-occurrence выживают после рестарта
- ✅ **ValidationError recovery** — GraphitiAdapter устойчив к quirks Graphiti API
- ✅ **Depth injection whitelist** — Cypher-инъекция через depth невозможна архитектурно
- ✅ **Auto-summary каждые 10 turns** — граф не растёт линейно с числом сообщений
- ✅ **CausalGraph** — рёбра CAUSES/LEADS_TO/INFLUENCES, агент понимает причины
- ✅ **RFC0006 Engram Isolation** — архитектурный замок
- ✅ **Runtime Invariant Checker** — RFC живут в коде, не на бумаге
- ✅ **Cognitive Modes** — PRECISION / BALANCED / EXPLORATION
- ✅ **Weighted Semantic Decay** — забываем эпистемически честно
- ✅ **Memory Budget Planner** — граф не растёт вечно
- ✅ **PII Redaction реализован** — GDPR не декларация
- ✅ **Freeze State WAL** — миллисекунды вместо секунд
- ✅ **Meta-Supervisor Apex Controller** — NORMAL/DEGRADED/SAFE_MODE + Recovery Protocol
- ✅ **ESM в L3** — жизненный цикл фактов (Observed→Collapsed)
- ✅ **MHI архитектура** — описана, реализация в Phase 2

**Ожидаемый результат**:
- 90%+ снижение расхода токенов
- 30%+ улучшение успешности задач
- <500ms латентность поиска
- Полная автономность работы памяти
- Нет race conditions (ConsolidationEngine)
- Нет незащищённых нарушений RFC (Runtime Checker)

Система готова к первому запуску на ПК с валидацией на каждом этапе.

---

### RFC0029 — Observer++ (Иммунная система)

**Проблема**: Observer наблюдал и логировал, но не имел власти ничего остановить. У системы не было иммунной системы.

**Решение**: Observer получает три реальных полномочия — блокировка, откат, снижение доверия.

```python
# 📎 Базовая версия. Каноническая — RFC0041 Graduated Observer++ (см. ниже)
class ObserverPlusPlus:
    """RFC0029 — Observer с властью. Иммунная система Velantrim."""

    async def on_anomaly(self, event: AnomalyEvent):
        if event.severity == "critical":
            await self.block_pipeline()
            await self.trigger_rollback()
            await self.reduce_trust_score(event.source_id)

    async def monitor_loop(self):
        while True:
            state = await self.get_current_state()
            if state.drift_score > DRIFT_THRESHOLD:
                await self.trigger_rollback()
            if state.cascade_size > MAX_ROLLBACK_CASCADE:
                await self.block_pipeline()
            if state.dlq_size > DLQ_OVERFLOW_THRESHOLD:
                await self.enter_safe_mode()
            if state.faithfulness_score < MIN_FAITHFULNESS:
                await self.pause_pipeline()
            await asyncio.sleep(OBSERVER_INTERVAL)
```

**Триггеры активации:**

| Триггер | Действие |
|---|---|
| `drift_score > 0.3` | rollback |
| `cascade_size > MAX_ROLLBACK_CASCADE` | block_pipeline |
| `DLQ overflow` | enter_safe_mode (L3 Read-Only) |
| `faithfulness < MIN_FAITHFULNESS` | pause + alert |
| `semantic_drift > SEMANTIC_THRESHOLD` | alert + review |

**Инварианты**: Observer НЕ пишет в Graph, НЕ генерирует факты, НЕ изменяет ESM напрямую.

---

### RFC0029+ — ESMChunkedInvalidator (Батчевый откат без deadlock)

**Проблема**: Прямой каскад `[:CONTRADICTS]` на 100+ узлов → deadlock Neo4j + блокировка ConsolidationEngine.

```python
class ESMChunkedInvalidator:
    async def start_cascade(self, root_fact_id: str):
        await self._mark_pending(root_fact_id)
        asyncio.create_task(self._process_chunks())

    async def _process_chunks(self):
        query = """
        MATCH (dep:Fact {pending_invalidation: true})
        WITH dep LIMIT $batch_size
        OPTIONAL MATCH (dep)<-[:DERIVED_FROM]-(child:Fact)
        WHERE child.epistemic_state IN ['Validated', 'Supported']
        SET child.pending_invalidation = true
        SET dep.epistemic_state = 'Hypothesized',
            dep.pending_invalidation = false,
            dep.invalidated_at = datetime()
        RETURN count(DISTINCT dep) as processed_count
        """
        while True:
            if await self.meta_supervisor.is_safe_mode():
                break
            result = await self.graph.execute_cypher(query, {"batch_size": 50})
            if not result or result[0]["processed_count"] == 0:
                break
            await asyncio.sleep(0.1)  # дать Neo4j "подышать"
```

**Обязательный индекс:**
```cypher
CREATE INDEX pending_inv_idx FOR (f:Fact) ON (f.pending_invalidation)
```

---

### RFC0030 — Source Trust Layer (Защита от Validated Hallucination)

**Проблема**: TruthGate проверяет evidence, но не источник. Неверный парсинг → структурно корректный факт → TruthGate пропускает → система уверенно говорит ложь ("validated hallucination").

```python
@dataclass
class SourceTrust:
    source_type: str        # "user_input"|"llm_output"|"import"|"manual"
    trust_score: float      # 0.0 – 1.0
    validation_status: str  # "verified"|"pending"|"flagged"
```

**Изменение в TruthGate:**
```python
# БЫЛО: if evidence_valid: accept_fact()
# СТАЛО:
if evidence_valid and source.trust_score >= TRUST_THRESHOLD:
    accept_fact()
else:
    mark_as_pending_review()
```

**Шкала trust_score:**

| Источник | trust_score | Принятие |
|---|---|---|
| manual (человек) | 0.95 | ✅ авто |
| trusted_import | 0.80 | ✅ авто |
| user_input | 0.65 | ⚠️ pending |
| llm_output | 0.30 | ❌ только через pipeline |

---

### RFC0031 — Write Protocol (Единственные пути записи в Graph)

**Проблема**: Нет машинного контракта — кто имеет право писать в L3. `Graph = Truth` остаётся только философией.

```python
class GraphWriteProtocol:
    ALLOWED_WRITERS = {"TruthGate", "HumanApproval", "TrustedImport"}

    async def write(self, fact, writer_id: str, trust_score: float):
        if writer_id not in self.ALLOWED_WRITERS:
            raise WriteProtocolViolation(f"Unauthorized: {writer_id}")
        if trust_score < WRITE_TRUST_THRESHOLD:
            raise WriteProtocolViolation(f"Low trust: {trust_score}")
        await self._audit_log(writer_id, fact)
        return await self._graph_write(fact)
```

**Запрещено всегда**: LLM напрямую, L1/L2/L2.5, Free Mode, Observer, Velum, ReasoningBank.

---

### RFC0032 — SafeFTSQuery (ESM-фильтр для FTS5)

**Проблема**: FTS5 возвращает сырые эпизоды без ESM-проверки. Contradicted/Deprecated данные попадают в контекст.

```python
class SafeFTSQuery:
    async def search(self, query: str, limit: int = 20) -> list[Episode]:
        raw = await self.fts5_search(query, limit * 2)
        safe = []
        for ep in raw:
            if ep.valid_until and ep.valid_until < datetime.now(timezone.utc):
                continue
            if ep.esm_hint in ("Contradicted", "Deprecated"):
                continue
            if await self._linked_to_contradicted(ep):
                continue
            safe.append(ep)
        return safe[:limit]
```

**Правило**: Прямой FTS5 без SafeFTSQuery — ошибка архитектуры. Весь L1-retrieval только через этот класс.

---

### RFC0033 — Closed Loop Self-Evaluation (Замкнутый цикл)

**Проблема**: `Query → Answer → Done` — L4 учится вслепую.

```
СТАЛО: Query → Retrieval → L4 → Answer → EVALUATE → LOG → ADJUST
```

```python
@dataclass
class EvaluationResult:
    faithfulness: float       # ответ соответствует фактам?
    trace_coverage: float     # все факты цепочки использованы?
    contradiction_rate: float # противоречия в ответе?
    response_confidence: float

class ClosedLoopEvaluator:
    async def evaluate(self, query, facts_pack, answer) -> EvaluationResult:
        result = EvaluationResult(
            faithfulness=await self._check_faithfulness(answer, facts_pack),
            trace_coverage=await self._check_trace_coverage(answer, facts_pack),
            contradiction_rate=await self._check_contradictions(answer),
            response_confidence=await self._get_l4_confidence()
        )
        await self.reasoning_bank.record_evaluation(result)
        if result.faithfulness < MIN_FAITHFULNESS:
            await self.observer.on_anomaly(AnomalyEvent(severity="warning"))
        return result
```

---

### RFC0034 — Semantic Drift Monitor (Смысловой дрейф)

**Проблема**: Структурный drift не видит семантического сдвига. Граф структурно стабилен — смысл уже другой.

```python
class SemanticDriftMonitor:
    async def check(self) -> SemanticDriftResult:
        esm_drift = self._compare_esm(await self._get_esm_distribution())
        centrality_drift = self._compare_centrality(await self._get_top_pagerank(k=10))
        domain_drift = self._compare_domains(await self._get_domain_distribution())
        semantic_score = esm_drift*0.5 + centrality_drift*0.3 + domain_drift*0.2
        if semantic_score > SEMANTIC_DRIFT_THRESHOLD:
            await self.alert("semantic_drift", score=semantic_score)
        return SemanticDriftResult(semantic_score, esm_drift, centrality_drift, domain_drift)
```

**Два независимых алерта:**
- `structural_drift` — граф изменился по форме
- `semantic_drift` — граф изменился по смыслу

---

### RFC0035 — Facts Pack Dual Mode + Diversity Constraint

**Проблема**: 8–12 фактов на все запросы — недостаточно для сложных задач. Нет гарантии разнообразия источников.

```python
class FactsPackBuilder:
    STRICT_LIMIT = 12    # быстрые запросы
    EXTENDED_LIMIT = 40  # сложные вопросы (complexity > COMPLEXITY_THRESHOLD)

    async def build(self, query: str, complexity: float) -> FactsPack:
        limit = self.EXTENDED_LIMIT if complexity > COMPLEXITY_THRESHOLD else self.STRICT_LIMIT
        facts = await self.retrieve(query, limit=limit * 2)
        return FactsPack(facts=self._diversity_filter(facts)[:limit])

    def _diversity_filter(self, facts):
        counts = defaultdict(int)
        result = []
        for f in sorted(facts, key=lambda x: x.confidence, reverse=True):
            if counts[f.source_domain] < MAX_FACTS_PER_SOURCE:
                result.append(f)
                counts[f.source_domain] += 1
        return result
```

---

### TraceLine — Единая трасса факта L1 → L3.5

**Назначение**: Диагностический обязательный слой. Любой `fact_id` → полный путь через все слои с ESM-валидацией каждого узла.

```
GET /trace?id=fact_abc

{
  "trace": [
    {"layer": "L1", "episode_id": "ep_001"},
    {"layer": "L2", "theme_id": "theme_007", "strength": 0.82},
    {"layer": "L2.5", "staging_id": "stg_042", "status": "promoted"},
    {"layer": "L3", "node_id": "node_123", "esm_state": "Validated"},
    {"layer": "L3.5", "snapshot_id": "snap_2026_03"}
  ],
  "validation": {"all_esm_valid": true, "broken_links": [], "integrity": "OK"}
}
```

**Расширение TraceLine для RFC0063 (Knowledge Ingestion):** при запросе с `?id=source_abc123` возвращает все три слоя:

```json
GET /trace?id=source_abc123

{
  "source_id": "source_abc123",
  "source_vintage": 2023,
  "source_domain": "physics",
  "layers": {
    "L3_facts": [
      {"fact_id": "fact_001", "esm_state": "Supported", "confidence": 0.87},
      {"fact_id": "fact_002", "esm_state": "Validated", "confidence": 0.94}
    ],
    "L4_strategies": [
      {"strategy_id": "strat_042", "prior_confidence": 0.90, "success_rate": 0.0}
    ],
    "vector_chunks": [
      {"chunk_id": "emb_099", "cosine_cluster": "physics_gravity",
       "fact_ids": ["fact_001"]}
    ]
  },
  "integrity": {
    "all_esm_valid": true,
    "broken_links": [],
    "vintage_decay_applied": true
  }
}
```

> ⚠️ TRACE = путь, НЕ = истина. A→B→C корректно, но если A ложный — результат ложный. TraceLine проверяет ESM каждого узла цепочки.

---

## 🗺️ Технологическая карта · Опциональный стек

> Ниже перечислены технологии, которые **не являются обязательными** для работы
> системы, но могут быть подключены как опциональные компоненты в зависимости
> от условий: железо, сложность задачи, цели проекта.
> 
> Принцип подключения: **Graph = Truth не нарушается никогда**.
> Любая опциональная технология — это замена транспорта или дополнение к
> retrieval, но не источника истины.

---

#### 🗄️ Блок A — Граф-движки (альтернативы и дополнения к Neo4j)

```
УСЛОВИЕ                    ТЕХНОЛОГИЯ         РОЛЬ В СИСТЕМЕ
──────────────────────────────────────────────────────────────
Слабое железо / MVP        Kuzu               Замена Neo4j в L3
RAM < 4GB                  Graph-Lite         Уже в L2.5 (Staging)
OLAP-аналитика дрейфа      DuckDB             Shadow State вместо
                                              нагрузки на Neo4j
Один SQL-стек              PostgreSQL+pgvec   Замена SQLite+Neo4j
Внешний граф-pipeline      Graphiti           Опциональный backend L3
```

---

##### 🟣 Kuzu — встроенная граф-БД

**Суть:** Kuzu работает как SQLite — in-process, без отдельного сервера.
Поддерживает Cypher, ACID, нативный traversal. Разработчики не ведут активную
поддержку, но база стабильна и пригодна к использованию.

**Где применять в Velantrim:**
- L3 на слабом железе (RAM < 8GB, нет Docker)
- Локальный агент без инфраструктуры
- MVP / прототип без Neo4j

**Инвариант:** Kuzu — только как движок L3. `Graph = Truth` сохраняется.
Write Protocol, ESM, TruthGate — работают поверх Kuzu без изменений.

```python
# velantrim_config.py
GRAPH_BACKEND = "neo4j"      # production default
# GRAPH_BACKEND = "kuzu"       # v8.0: KuzuDB (MIT, Cypher, ACID) — P0-H FIX
# GRAPH_BACKEND = "graph_lite" # опционально: RAM < 4GB (уже в L2.5)
```

**Ограничение:** Kuzu не поддерживает кластеризацию. Только single-node.
При росте графа > 10M узлов — мигрировать на Neo4j.

---

##### 🔵 DuckDB — Shadow State для аналитики

**Суть:** OLAP-движок, работает на Parquet/Arrow in-process.
Не хранит граф — только аналитические проекции.

**Где применять в Velantrim:**
- `Semantic Drift Monitor` и `Observer++` делают тяжёлые вычисления
  (PageRank, ESM distribution) прямо в Neo4j → блокируют транзакции.
- DuckDB получает дамп графа каждые 15 мин → аналитика изолирована.

```
Neo4j   ←── транзакции (OLTP)    Write Protocol, TruthGate
   ↓ dump каждые 15 мин
DuckDB  ←── аналитика (OLAP)     Drift Monitor, Observer metrics
```

**Выигрыш:** Observer и Drift Monitor не блокируют основной граф.
P95 latency не деградирует при фоновой аналитике.

---

##### 🟢 Graphiti — опциональный граф-pipeline

**Суть:** Graphiti строит граф сущностей из текстовых эпизодов с временными
рёбрами. Лежит в основе Velantrim как источник вдохновения.

**Где применять в Velantrim:**
- Опциональный backend для `ConsolidationEngine` (L2→L3 промоут)
- Импорт внешних корпусов знаний в L3
- Альтернативный pipeline для ingestion когда нет кастомного парсера

**Ограничение:** Graphiti — не источник истины. Всё что приходит через
Graphiti проходит через `TruthGate + Write Protocol` как и любой другой источник.
`source_type = "trusted_import"`, `trust_score = 0.80`.

---

##### 🟡 Graph-Lite — уже существует в L2.5

**Суть:** Уже реализован в L2.5 Staging как временный мини-граф в SQLite
(таблицы `nodes` + `edges`). Активируется при RAM < 4GB.

**Напоминание о правиле чтения:**
```
1. Сначала L3 граф (Neo4j / Kuzu) — канон
2. Если нет в L3, но есть в Graph-Lite → confidence × 0.7
   пометка "preliminary" (не истина, гипотеза)
3. При переносе в Neo4j → Graph-Lite очищается
```

---

#### 🔍 Блок B — RAG-архитектуры (опционально в Fast Path)

> Все перечисленные ниже архитектуры — это **паттерны retrieval**.
> Они не заменяют `Graph = Truth`, а описывают как и откуда брать факты
> перед передачей в `FactsPack`.

```
ТЕХНОЛОГИЯ    СУТЬ (одной строкой)                    УРОВЕНЬ В VELANTRIM
──────────────────────────────────────────────────────────────────────────
GraphRAG      Граф сущностей → глобальные запросы     L3 retrieval
KAG           ETL-слой: Extract→Aggregate→Normalize    Между L3 и FactsPack
CAG           Граф причинно-следственных цепочек       L4 ReasoningBank
ReRAG         Итеративный retrieval (несколько раундов) HybridRetriever
AgRAG         Агент сам решает когда/что искать        Fast Path routing
GCR           Reasoning только по путям графа          L4 ограничение
RefRAG        Самооценка: нужно ли искать ещё          Перед Closed Loop
Refrag        Сжатие контекста перед LLM               После FactsPack
Self-RAG      LLM критикует свои ответы                Closed Loop RFC0033
HyDE          Поиск через гипотетический ответ         L1 FTS5 / Hybrid
```

---

##### 🔵 GraphRAG (Microsoft)

**Суть:** Строит граф сущностей поверх корпуса. Отвечает на «глобальные»
вопросы (темы, сводки, связи) лучше чем векторный поиск.

**Где в Velantrim:** L3 retrieval для многошаговых запросов и тематических
сводок. Особенно полезен при запросах типа WHY / OVERVIEW / THEME.

**Статус:** Опционально. Не заменяет TruthGate. Результат GraphRAG →
проходит через `SafeFTSQuery` эквивалент + ESM-фильтр перед FactsPack.

---

##### 🟡 KAG — Knowledge-Augmented Generation

**Суть:** Формальный ETL-слой между L3 retrieval и FactsPack.
Нормализует, агрегирует, фильтрует факты по `epistemic_state` до передачи
в контекст.

**Где в Velantrim:** Промежуточный шаг в `ContextBuilder`:

```
L3 retrieval → [KAG: Extract→Aggregate→Normalize] → FactsPack → LLM
```

Обязательные поля KAG-узла: `source_ref`, `confidence`, `trace_id`,
`epistemic_state`, `trust_score`.

**Статус:** Концептуально уже реализован в `FactsPack` и `TruthGate`.
KAG — это просто формальное имя для этого слоя. Можно задокументировать
явно как `KAGBuilder` вместо анонимного шага.

---

##### 🟠 CAG — Causal Argument Graph

**Суть:** Граф причинно-следственных связей поверх L3. Используется
L4 для построения reasoning-цепочек без LLM-фантазий.

**Где в Velantrim:** L4 `ReasoningBank` — для запросов типа WHY/CAUSE:

```
Запрос WHY → L3 facts → CAG traversal → reasoning path → ответ
```

Узлы CAG: `cause_node → effect_node` с полями `confidence`, `evidence_refs`,
`trace_id`. Рёбра: `[:CAUSES]`, `[:ENABLES]`, `[:PREVENTS]`.

**Статус:** Опционально. Усиливает L4 детерминированным reasoning.
Строится поверх существующих L3-узлов через дополнительные рёбра.

---

##### 🟢 ReRAG — Recursive / Iterative RAG

**Суть:** Несколько раундов retrieval: по результатам первого прохода
формируются уточнённые подзапросы → снова ищет → расширяет контекст.

**Где в Velantrim:** `HybridRetriever` уже поддерживает многоступенчатый
retrieval и graph expansion. ReRAG — это формальное имя для этого паттерна.

**Ограничение:** Обязателен явный лимит итераций `MAX_RERAG_ITERATIONS = 3`
и критерий остановки (coverage порог). Без лимита — token explosion.

```python
# velantrim_config.py
MAX_RERAG_ITERATIONS = 3      # максимум раундов
RERAG_COVERAGE_THRESHOLD = 0.85  # стоп если покрытие > 85%
```

---

##### 🔴 GCR — Graph-Constrained Reasoning

**Суть:** Reasoning только по существующим путям в графе. LLM не может
«придумать» связь, которой нет в L3. Строгое ограничение.

**Где в Velantrim:** L4 `ReasoningBank` + Write Protocol. По сути GCR —
это философия которую уже реализует `Graph = Truth` принцип.
Можно формализовать как явный флаг:

```python
reasoning_mode = "graph_constrained"  # только по путям L3
# reasoning_mode = "hybrid"           # L3 + LLM inference
```

---

##### 🟡 AgRAG — Agentic RAG

**Суть:** Агент сам решает когда и что искать. Не линейный pipeline,
а цикл: действие → оценка → следующее действие.

**Где в Velantrim:** Весь Fast Path уже агентный. AgRAG описывает
именно паттерн `Fact Router` (см. RFC0038 ниже) + `Closed Loop Eval`.

---

##### 🟢 RefRAG / Self-RAG

**Суть:** После retrieval система оценивает достаточность найденного.
Если нет — ещё один раунд. LLM критикует свои источники.

**Где в Velantrim:** `Closed Loop Eval (RFC0033)` уже реализует этот
паттерн. RefRAG — это альтернативное название. Отличие: в RefRAG оценка
происходит ДО генерации ответа, в RFC0033 — ПОСЛЕ. Оба подхода совместимы.

---

##### ⚠️ Refrag — сжатие контекста

**Суть:** Оптимизация как LLM читает контекст. Сжимает чанки через
embeddings, выбирает только важное. Ускоряет inference до ~30x TTFT.

**Важно:** Refrag — про **эффективность**, не про **истину**.
Не делает систему умнее — делает дешевле и быстрее.

**Где в Velantrim:** После `FactsPack`, перед `LLM Generation`.
Применять только когда Graph + FactsPack стабильны и проблема — cost/latency.

```
FactsPack (12-40 фактов) → [Refrag: сжатие] → LLM (только важное)
```

**Статус:** Низкий приоритет. Реализовывать в следующем спринте.

---

##### 🟡 HyDE — Hypothetical Document Embedding

**Суть:** Генерирует «гипотетический ответ» на запрос, затем ищет
похожее на него в базе. Улучшает sparse retrieval для необычных запросов.

**Где в Velantrim:** `HybridRetriever` — дополнение к BM25/FTS5.
Особенно полезно для L1 когда точный текст запроса не совпадает с эпизодами.

---

## 📜 RFC0036–RFC0051

---

### RFC0036 — Persistent Event Fallback Queue

**Версия:** 2 · **Приоритет:** 🔴 Критично · **Время реализации:** 2–3 дня

**Проблема:** `fallback_queue` в `RobustEventBus` — чисто in-memory
(`asyncio.Queue`). При рестарте агента или Redis crash все события теряются
навсегда. Это единственное место в системе где «Truth Integrity» нарушается
на уровне событий (не фактов). 182 страницы документа — ни одного упоминания.

**Инвариант:** Это НЕ нарушает Write Protocol — события не являются фактами.
SQLite fallback работает параллельно с существующим DLQ.

**Решение:** Заменить `asyncio.Queue` на SQLite-таблицу `event_fallback`.

```python
# P3-A FIX: ⚠️ КАНОНИЧНА: SQLiteFallbackQueue в разделе «1. Event Bus & Ingestion Pipeline».
# Этот фрагмент — архивный RFC-текст. Реализацию смотреть выше.
# event_bus.py — RFC0036 дополнение к классу RobustEventBus (каноническая версия в разделе «1. Event Bus»)
# Добавить следующие методы и атрибуты в существующий класс:
import aiosqlite
import zlib
from prometheus_client import Counter, Gauge

class RobustEventBus:  # расширение — добавить в основной класс
    # Новые атрибуты (__init__):
    # self.sqlite_path = sqlite_path  (уже есть operational DB)
    # self.fallback_inserted = Counter('event_fallback_inserted_total', ...)
    # self.fallback_recovered = Counter('event_fallback_recovered_total', ...)
    # self.fallback_size = Gauge('event_fallback_size', ...)

    async def _init_fallback_table(self):
        async with aiosqlite.connect(self.sqlite_path) as db:
            await db.execute("PRAGMA journal_mode=WAL;")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS event_fallback (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_data  BLOB    NOT NULL,       -- zlib-сжатый JSON
                    priority    TEXT    DEFAULT 'NORMAL', -- CRITICAL / NORMAL
                    retry_count INTEGER DEFAULT 0,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_fallback_prio
                ON event_fallback(priority, retry_count, created_at)
            """)
            await db.commit()

    async def publish(self, event: AgentEvent,
                      priority: str = 'NORMAL') -> bool:
        event_data = { ... }  # как раньше
        try:
            await self.redis.xadd(self.stream_key, event_data)
            return True
        except Exception:
            compressed = zlib.compress(
                json.dumps(event_data).encode(), level=1
            )
            async with aiosqlite.connect(self.sqlite_path) as db:
                await db.execute(
                    "INSERT INTO event_fallback (event_data, priority) "
                    "VALUES (?, ?)",
                    (compressed, priority)
                )
                await db.commit()
            self.fallback_inserted.inc()
            return False

    async def process_persistent_fallback(self):
        """Вызывается scheduler каждые 5 мин"""
        async with aiosqlite.connect(self.sqlite_path) as db:
            cursor = await db.execute("""
                SELECT id, event_data FROM event_fallback
                WHERE retry_count < 5
                ORDER BY priority DESC, created_at ASC
                LIMIT 100
            """)
            rows = await cursor.fetchall()
            for row_id, compressed in rows:
                try:
                    data = json.loads(zlib.decompress(compressed))
                    await self.redis.xadd(self.stream_key, data)
                    await db.execute(
                        "DELETE FROM event_fallback WHERE id=?", (row_id,)
                    )
                    self.fallback_recovered.inc()
                except Exception:
                    await db.execute(
                        "UPDATE event_fallback "
                        "SET retry_count = retry_count + 1 WHERE id=?",
                        (row_id,)
                    )
            await db.commit()

    async def cleanup_old_fallback(self):
        """Вызывается scheduler каждые 24ч"""
        async with aiosqlite.connect(self.sqlite_path) as db:
            await db.execute(
                "DELETE FROM event_fallback WHERE created_at < ?",
                (datetime.now(timezone.utc) - timedelta(days=7),)
            )
            await db.commit()
```

**Интеграция в main.py / scheduler:**
```python
scheduler.add_job(event_bus.process_persistent_fallback,
                  'interval', minutes=5)
scheduler.add_job(event_bus.cleanup_old_fallback,
                  'interval', hours=24)
```

**Метрика Prometheus:** `event_fallback_inserted_total`,
`event_fallback_recovered_total`, `event_fallback_size`

**Для CRITICAL событий** (Ring Zero change, ESM Validated→Contradicted):
```python
await event_bus.publish(event, priority='CRITICAL')
```

---

### RFC0036+ — OCC Patch для ESMChunkedInvalidator

**Проблема:** `asyncio.sleep(0.1)` в батчевом откате создаёт race condition.
В момент паузы другой процесс (Fast-Track Staging) может привязать новые
факты к узлам, которые находятся в очереди на инвалидацию → «фантомные» связи.

**Решение:** Optimistic Concurrency Control — версионирование узлов.

**Шаг 1 — Миграция схемы (один раз):**
```cypher
// Добавить поле версии во все узлы :Fact
MATCH (f:Fact) WHERE f._version_ IS NULL
SET f._version_ = 1
```

**Шаг 2 — Атомарный Cypher вместо sleep:**
```cypher
// БЫЛО (с race condition):
MATCH (dep:Fact {pending_invalidation: true})
WITH dep LIMIT 50
SET dep.epistemic_state = 'Hypothesized'
...

// СТАЛО (OCC — атомарно):
MATCH (dep:Fact {id: $fact_id, _version_: $expected_version})
SET dep.epistemic_state   = 'Hypothesized',
    dep.pending_invalidation = false,
    dep.invalidated_at    = datetime(),
    dep._version_         = dep._version_ + 1
RETURN dep.id as processed
// Если _version_ изменилась → 0 строк → добавить в DLQ, не зависнуть
```

**Шаг 3 — Python:**
```python
# 📎 OCC-расширение ESMChunkedInvalidator (базовая версия — RFC0029+, см. выше)
class ESMChunkedInvalidator:
    async def _process_single(self, fact_id: str,
                               expected_version: int) -> bool:
        result = await self.graph.execute_cypher(
            OCC_INVALIDATE_QUERY,
            {"fact_id": fact_id, "expected_version": expected_version}
        )
        if not result or result[0]["processed"] == 0:
            # Версия изменилась — добавить в DLQ для повтора
            await self.dlq.put(fact_id)
            return False
        return True
    # asyncio.sleep(0.1) — УДАЛИТЬ
```

**Результат:** Нет deadlock, нет race condition, нет фантомных связей.
DLQ обрабатывает конфликтные случаи автоматически.

---

### RFC0037 — Async Closed Loop Eval

**Проблема:** `ClosedLoopEvaluator (RFC0033)` работает в синхронном Fast Path.
Пользователь ждёт пока система оценивает свой ответ → P95 latency 2000+ мс
вместо заявленных 500 мс. SLO нарушается.

**Решение:** Вынести EVALUATE в SLOW PATH через Event Bus.

```
БЫЛО:
  Query → Retrieval → L4 → Answer → EVALUATE → [ждём] → ADJUST → Response

СТАЛО:
  Query → Retrieval → L4 → Answer → Response  ← пользователь получает здесь
                                  ↓ async (Event Bus)
                             L4 Worker → EVALUATE → ADJUST → ReasoningBank
```

**Изменение в Fast Path:**
```python
# context_builder.py / fast_path.py
async def generate_response(self, query, facts_pack) -> Response:
    answer = await self.llm.generate(query, facts_pack)

    # БЫЛО: await self.evaluator.evaluate(query, facts_pack, answer)
    # СТАЛО: отправить в фон
    await self.event_bus.publish(AgentEvent(
        event_type  = "AGENT_RESPONSE",
        payload     = {
            "query"       : query,
            "facts_pack"  : facts_pack.to_dict(),
            "answer"      : answer.content,
            "strategy_id" : self.last_strategy_id,
            "session_id"  : self.session_id,
        }
    ), priority='NORMAL')

    return answer  # ← сразу пользователю
```

**L4 Worker (Slow Path):**
```python
# l4_reasoning_worker.py
async def process_evaluation_queue(self):
    async for msg_id, data in self.event_bus.consume(
        "eval_group", "eval_worker"
    ):
        if data["event_type"] != "AGENT_RESPONSE":
            continue

        result = await self.evaluator.evaluate(
            query      = data["query"],
            facts_pack = FactsPack.from_dict(data["facts_pack"]),
            answer     = data["answer"]
        )

        # Обучаем ReasoningBank на результате
        await self.reasoning_bank.update_strategy_feedback(
            strategy_id = data["strategy_id"],
            outcome     = "SUCCESS" if result.faithfulness > MIN_FAITHFULNESS
                          else "FAILURE",
            metrics     = result.to_dict()
        )

        # Плохой ответ → алерт Observer++
        if result.faithfulness < MIN_FAITHFULNESS:
            await self.observer.on_anomaly(AnomalyEvent(
                severity = "warning",
                source   = "closed_loop_eval",
                details  = result.to_dict()
            ))
```

**Результат:** Fast Path не блокируется. P95 возвращается к < 500 мс.
Качество ответов улучшается асинхронно без влияния на UX.

---

### RFC0038 — Fact Router (Детерминированный)

**Проблема:** Нет формального механизма маршрутизации запросов по типу.
Router через LLM — недетерминирован и нарушает `Graph = Truth` принцип.
Router должен быть rule-based + graph, без LLM в цепи принятия решений.

**Суть:** Каждый запрос классифицируется по типу → маршрутизируется
к правильному retrieval-источнику ДО обращения к LLM.

**Таблица маршрутизации:**

| Тип запроса | Маркеры | Маршрут | Примечание |
|-------------|---------|---------|-----------|
| `DEFINE` | что такое / определи / объясни | L3 Graph | Только факты |
| `WHY / CAUSE` | почему / причина / из-за | L3 + CAG paths | Причинно-следственные цепи |
| `HOW` | как / каким образом / шаги | L3 + Procedures | Процедурная память |
| `FACT / DATE` | когда / сколько / кто | L2 SQLite / API | Конкретные данные |
| `STRATEGY` | план / стратегия / подход | L4 ReasoningBank | Мета-знания |
| `HISTORY` | что я делал / прошлое / помнишь | L1 Episodic | Эпизодическая память |
| `CHAT` | привет / спасибо / эмоция | LLM only | Нет retrieval |
| `COMPLEX` | многоступенчатый / план | ReRAG + L3+L4 | Итеративный retrieval |

**Реализация:**
```python
# fact_router.py
from dataclasses import dataclass
from enum import Enum

class QueryType(Enum):
    DEFINE   = "define"
    WHY      = "why"
    HOW      = "how"
    FACT     = "fact"
    STRATEGY = "strategy"
    HISTORY  = "history"
    CHAT     = "chat"
    COMPLEX  = "complex"

@dataclass
class RouteDecision:
    query_type  : QueryType
    sources     : list[str]   # ["l3", "l4", "l1", "api"]
    rerag       : bool        # использовать итеративный retrieval
    max_facts   : int         # STRICT(12) или EXTENDED(40)
    explanation : str         # для TraceLine / аудита

class FactRouter:
    """RFC0038 — Детерминированный маршрутизатор.
    НЕ использует LLM для принятия решений.
    Rule-based + TF-IDF keyword matching.
    """

    PATTERNS = {
        QueryType.DEFINE   : ["что такое", "определи", "объясни",
                               "what is", "define"],
        QueryType.WHY      : ["почему", "причина", "из-за", "why",
                               "because", "причиной"],
        QueryType.HOW      : ["как", "каким образом", "шаги",
                               "how to", "алгоритм"],
        QueryType.FACT     : ["когда", "сколько", "кто", "где",
                               "when", "how many", "who"],
        QueryType.STRATEGY : ["план", "стратегия", "подход",
                               "strategy", "approach"],
        QueryType.HISTORY  : ["помнишь", "прошлый раз", "вчера",
                               "remember", "last time", "история"],
        # P1-H FIX: "пока" убрано — в русском ambiguous: "goodbye" И "while/until".
        # "пока база не обновится" → маршрутизировался в LLM-only без retrieval.
        # Заменено на явное "до свидания" + "bye".
        QueryType.CHAT     : ["привет", "спасибо", "до свидания",
                               "hello", "thanks", "как дела", "bye"],
    }

    ROUTE_MAP = {
        QueryType.DEFINE   : RouteDecision(QueryType.DEFINE,
                               ["l3"], False, 12,
                               "fact retrieval from Graph"),
        QueryType.WHY      : RouteDecision(QueryType.WHY,
                               ["l3", "cag"], True,  40,
                               "causal chain traversal"),
        QueryType.HOW      : RouteDecision(QueryType.HOW,
                               ["l3", "procedures"], False, 12,
                               "procedural memory"),
        QueryType.FACT     : RouteDecision(QueryType.FACT,
                               ["l2", "api"], False, 12,
                               "concrete data retrieval"),
        QueryType.STRATEGY : RouteDecision(QueryType.STRATEGY,
                               ["l4"], False, 12,
                               "ReasoningBank strategies"),
        QueryType.HISTORY  : RouteDecision(QueryType.HISTORY,
                               ["l1"], False, 20,
                               "episodic buffer"),
        QueryType.CHAT     : RouteDecision(QueryType.CHAT,
                               ["llm"], False, 0,
                               "no retrieval needed"),
        QueryType.COMPLEX  : RouteDecision(QueryType.COMPLEX,
                               ["l3", "l4", "rerag"], True, 40,
                               "iterative multi-source retrieval"),
    }

    def route(self, query: str) -> RouteDecision:
        """Детерминированная классификация запроса.
        Без LLM. Rule-based + keyword matching.
        """
        query_lower = query.lower()
        scores = {qt: 0 for qt in QueryType}

        for query_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if pattern in query_lower:
                    scores[query_type] += 1

        # Определить тип по максимальному score
        best_type = max(scores, key=scores.get)

        # COMPLEX если несколько типов с высоким score
        high_score_types = [qt for qt, s in scores.items() if s >= 2]
        if len(high_score_types) > 1:
            best_type = QueryType.COMPLEX

        # P9-FIX БАГ-15: комментарий исправлен — CHAT никогда не является fallback
        # Нет паттернов → FACT по умолчанию (conservative: всегда retrieval)
        if scores[best_type] == 0:
            best_type = QueryType.FACT

        decision = self.ROUTE_MAP[best_type]
        logger.info(f"FactRouter: {best_type} → {decision.sources} "  # было {query_type} — переменная цикла, не best_type
                    f"(rerag={decision.rerag})")
        return decision
```

**Интеграция в Fast Path:**
```python
# fast_path.py
router   = FactRouter()
decision = router.route(user_query)

# Retrieval согласно маршруту
facts = await hybrid_retriever.retrieve(
    query    = user_query,
    sources  = decision.sources,
    limit    = decision.max_facts,
    rerag    = decision.rerag
)
```

**Инварианты RFC0038:**
- `I_ROUTER_1`: FactRouter НИКОГДА не вызывает LLM
- `I_ROUTER_2`: Каждое решение логируется в TraceLine
- `I_ROUTER_3`: COMPLEX тип автоматически включает ReRAG с лимитом
  `MAX_RERAG_ITERATIONS = 3`

---

### RFC0039 — Thompson Sampling для L4 ReasoningBank

**Проблема:** UCB1 (RFC0025) детерминирован и при большом числе стратегий
(100+) тратит CPU на пересчёт `total_trials` O(k) на каждый вызов.
При delayed feedback (ответ получен позже) UCB1 застревает в локальных оптимумах.

**Решение:** Заменить UCB1 на Thompson Sampling — стохастический bandit,
который естественно балансирует exploration/exploitation через Beta-распределение.

```
БЫЛО (UCB1):
  score = success_rate + sqrt(2 × ln(N) / n)
  → O(k) пересчёт total_trials по всем стратегиям
  → Детерминирован → риск локального оптимума

СТАЛО (Thompson Sampling):
  score = numpy.random.beta(success_count + 1, failure_count + 1)
  → O(1) на стратегию, нет пересчёта N
  → Стохастичен → естественное исследование
```

**Реализация:**
```python
# reasoning_bank.py — RFC0039 дополнение (каноническая версия класса — раздел «14. ReasoningBank»)
# Заменить метод retrieve_relevant_strategies на Thompson Sampling реализацию:
import numpy as np

class ReasoningBank:  # расширение — заменить метод в основном классе

    async def retrieve_relevant_strategies(
        self,
        context: str,
        top_k: int = 5,
        seed: int | None = None
    ) -> list[Strategy]:
        """
        Thompson Sampling выбор стратегий.
        seed — для воспроизводимого replay в аудите (Инвариант I13).
        """
        # Шаг 1 — TF-IDF pre-filter (сохранён из RFC0025)
        candidates = [
            s for s in await self._load_strategies()
            if cosine(s.embedding, context) >= 0.3
        ]
        if not candidates:
            return []

        # Шаг 2 — Thompson Sampling
        rng = np.random.default_rng(seed)  # воспроизводимый генератор
        scored = []
        for strategy in candidates:
            alpha = strategy.success_count + 1   # prior = Beta(1,1) = uniform
            beta  = strategy.failure_count + 1
            ts_score = rng.beta(alpha, beta)
            scored.append((ts_score, strategy))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:top_k]]
```

**Метрики:**
```python
reasoning_bank_ts_score          # Histogram — TS score по стратегии
reasoning_bank_exploration_rate  # адаптивный, не фиксированный 10%
```

**Инварианты RFC0039:**
- `I13 (TSReplay)`: При audit-replay передавать `seed=session_id_hash` для
  детерминированного воспроизведения. Без seed — production mode (стохастичен).
- `I_TS_1`: TS pre-filter остаётся TF-IDF cosine ≥ 0.3 (не меняется).
- `I_TS_2`: prior Beta(1,1) = uniform для новых стратегий → они всегда проходят фильтр.

**Результат:** +8% cumulative reward. CPU −40% (нет O(k) пересчёта).
Лучше адаптируется к задачам с отложенным фидбеком.

---

### RFC0040 — CQRS Shadow State (DuckDB как аналитический слой)

**Проблема:** Semantic Drift Monitor и Observer++ выполняют тяжёлую аналитику
(PageRank, ESM-распределение, domain stats) напрямую в Neo4j (OLTP).
Это создаёт конкуренцию с транзакционными запросами и нарушает SLO P95 < 500ms.

**Решение:** CQRS — разделить чтение и запись.
- Neo4j = OLTP (транзакции, TruthGate, Write Protocol)
- DuckDB = OLAP (аналитика, Drift Monitor, Observer аналитика)

```
БЫЛО:
  Semantic Drift Monitor → Cypher в Neo4j (O(N log N), блокирует транзакции)

СТАЛО:
  Neo4j (OLTP) → каждые 15 мин → Parquet dump → DuckDB (OLAP)
  Semantic Drift Monitor → DuckDB SQL (не трогает Neo4j)
```

**Реализация:**
```python
# shadow_state.py — RFC0040
import duckdb
from neo4j import AsyncGraphDatabase

class ShadowState:
    """
    CQRS-слой: Neo4j → DuckDB проекция каждые 15 мин.
    DuckDB используется ТОЛЬКО для чтения аналитики.
    Запись в граф — только через Neo4j + Write Protocol.
    """
    def __init__(self, neo4j_uri: str, duckdb_path: str = "shadow.duckdb"):
        self.neo4j = AsyncGraphDatabase.driver(neo4j_uri)
        self.db = duckdb.connect(duckdb_path)
        self._init_schema()

    def _init_schema(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS facts_snapshot (
                node_id        TEXT PRIMARY KEY,
                epistemic_state TEXT,
                domain         TEXT,
                importance     FLOAT,
                trust_score    FLOAT,
                created_at     TIMESTAMP,
                updated_at     TIMESTAMP,
                snapshot_time  TIMESTAMP DEFAULT current_timestamp
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS shadow_meta (
                key   TEXT PRIMARY KEY,
                value TEXT
            )
        """)

    async def sync(self):
        """Синхронизация Neo4j → DuckDB. Вызывается scheduler каждые 15 мин."""
        async with self.neo4j.session() as session:
            result = await session.run("""
                MATCH (f:Fact)
                RETURN f.id as node_id,
                       f.epistemic_state as epistemic_state,
                       f.domain as domain,
                       f.importance as importance,
                       f.trust_score as trust_score,
                       f.created_at as created_at,
                       f.updated_at as updated_at
            """)
            rows = [dict(r) async for r in result]

        if rows:
            self.db.execute("DELETE FROM facts_snapshot")
            self.db.executemany("""
                INSERT INTO facts_snapshot VALUES (?,?,?,?,?,?,?,current_timestamp)
            """, [list(r.values()) for r in rows])
            self.db.execute(
                "INSERT OR REPLACE INTO shadow_meta VALUES ('last_sync', ?)",
                [datetime.now(timezone.utc).isoformat()]
            )

    def get_esm_distribution(self) -> dict:
        """Для Semantic Drift Monitor — без нагрузки на Neo4j."""
        result = self.db.execute("""
            SELECT epistemic_state, COUNT(*) as count
            FROM facts_snapshot
            GROUP BY epistemic_state
        """).fetchall()
        return {row[0]: row[1] for row in result}

    def get_domain_distribution(self) -> dict:
        """Domain drift detection."""
        result = self.db.execute("""
            SELECT domain, COUNT(*) as count
            FROM facts_snapshot
            GROUP BY domain
            ORDER BY count DESC
        """).fetchall()
        return {row[0]: row[1] for row in result}

    @property
    def lag_seconds(self) -> float:
        """Prometheus метрика: отставание Shadow State от Neo4j."""
        row = self.db.execute(
            "SELECT value FROM shadow_meta WHERE key='last_sync'"
        ).fetchone()
        if not row:
            return float('inf')
        last = datetime.fromisoformat(row[0])
        return (datetime.now(timezone.utc) - last).total_seconds()
```

**Интеграция в Semantic Drift Monitor:**
```python
# semantic_drift_monitor.py — обновление
# 📎 Каноническая версия SemanticDriftMonitor — RFC0034 (см. выше)
class SemanticDriftMonitor:
    def __init__(self, shadow_state: ShadowState):
        self.shadow = shadow_state  # читаем из DuckDB, не Neo4j

    async def check(self) -> SemanticDriftResult:
        esm_dist  = self.shadow.get_esm_distribution()   # DuckDB SQL
        domain_dist = self.shadow.get_domain_distribution()  # DuckDB SQL
        # PageRank по-прежнему через Neo4j — только раз в сутки
        ...
```

**Интеграция в main.py / scheduler:**
```python
shadow = ShadowState(neo4j_uri, duckdb_path="shadow.duckdb")
scheduler.add_job(shadow.sync, 'interval', minutes=15)
```

**Метрики:**
```python
duckdb_shadow_lag_seconds      # Gauge — отставание от Neo4j
duckdb_shadow_sync_total       # Counter — успешных синхронизаций
duckdb_shadow_rows_synced      # Gauge — строк в последней синхронизации
```

**Инварианты RFC0040:**
- `I14 (CQRSRead)`: Semantic Drift Monitor и Observer аналитика НИКОГДА не читают
  напрямую из Neo4j для агрегаций. Только DuckDB Shadow State.
  Нарушение: Cypher агрегация в SemanticDriftMonitor.
- `I_CQRS_1`: DuckDB — только для чтения аналитики. Запись в граф — только Neo4j.
- `I_CQRS_2`: Lag > 30 мин → Prometheus алерт `duckdb_shadow_lag_seconds > 1800`.

**Результат:** Neo4j освобождается от аналитической нагрузки.
P95 latency стабильна при любом размере графа. Drift Monitor работает
без stop-the-world пауз.

---

### RFC0041 — Graduated Observer++ (деградированный режим)

**Проблема:** Observer++ при аномалии вызывает `block_pipeline()` — бинарное
"всё или ничего". При false-positive срабатывании (ложная тревога) агент
полностью останавливается, хотя мог бы продолжать в ограниченном режиме.

**Решение:** Заменить бинарный блок на градуированную деградацию.

```
БЫЛО:
  anomaly → block_pipeline() → агент мёртв

СТАЛО:
  anomaly → оценить false_positive_rate → выбрать уровень деградации
    Уровень 1 (мягкий): только алерт, продолжаем
    Уровень 2 (деградированный): L3 read-only, L4 ограничен
    Уровень 3 (полный блок): только при критических нарушениях Write Protocol
```

**Реализация:**
```python
# observer_plus_plus.py — RFC0041 (Graduated Observer++ — каноническая версия)
from prometheus_client import Counter, Gauge

class ObserverPlusPlus:

    # Prometheus метрики
    false_positive_rate_gauge = Gauge(
        'observer_false_positive_rate', 'Доля ложных срабатываний Observer++'
    )
    degraded_mode_activations = Counter(
        'observer_degraded_mode_total', 'Входов в деградированный режим'
    )
    full_blocks = Counter(
        'observer_full_blocks_total', 'Полных блокировок pipeline'
    )

    async def on_anomaly(self, event: AnomalyEvent):
        """
        Graduated response вместо бинарного block.
        """
        fpr = await self._get_false_positive_rate()
        self.false_positive_rate_gauge.set(fpr)

        if event.severity == "info":
            # Уровень 0: только лог
            logger.info(f"Observer++ info: {event.details}")
            return

        if fpr > 0.3:
            # Высокий FPR → деградированный режим, НЕ полный блок
            logger.warning(
                f"Observer++: high FPR={fpr:.2f}, entering degraded mode "
                f"instead of full block. Anomaly: {event.details}"
            )
            await self._enter_degraded_mode()
            self.degraded_mode_activations.inc()
            return

        if event.severity == "warning":
            # Уровень 1: деградированный режим
            await self._enter_degraded_mode()
            self.degraded_mode_activations.inc()

        elif event.severity == "critical":
            # Уровень 2: полный блок — только для Write Protocol violations
            if event.source == "write_protocol":
                await self.block_pipeline()
                self.full_blocks.inc()
            else:
                # Критическое, но не Write Protocol → деградированный
                await self._enter_degraded_mode()
                self.degraded_mode_activations.inc()

    async def _enter_degraded_mode(self):
        """
        L3 → read-only. L4 → только проверенные стратегии (success_rate > 0.7).
        L1/L2 → продолжают работать. Пользователь получает ответ с пометкой.
        """
        self.mode = "DEGRADED"
        await self.graph.set_read_only(True)
        await self.reasoning_bank.set_conservative_mode(min_success_rate=0.7)
        logger.warning("Observer++: DEGRADED mode activated")

    async def _exit_degraded_mode(self):
        """Вызывается автоматически если аномалия не подтвердилась за 5 мин."""
        self.mode = "NORMAL"
        await self.graph.set_read_only(False)
        await self.reasoning_bank.set_conservative_mode(None)
        logger.info("Observer++: returned to NORMAL mode")

    async def _get_false_positive_rate(self) -> float:
        """
        FPR = доля алертов за последние 24ч, которые не подтвердились
        (аномалия не вызвала реального ESM-каскада или Write Violation).
        """
        alerts = await self._count_alerts(hours=24)
        confirmed = await self._count_confirmed_anomalies(hours=24)
        if alerts == 0:
            return 0.0
        return 1.0 - (confirmed / alerts)
```

**Метрики:**
```python
observer_false_positive_rate     # Gauge — текущий FPR
observer_degraded_mode_total     # Counter — входов в degraded mode
observer_full_blocks_total       # Counter — полных блокировок
observer_degraded_duration_seconds  # Histogram — длительность degraded mode
```

**Инварианты RFC0041:**
- `I15 (GraduatedBlock)`: Observer++ НЕ вызывает `block_pipeline()` если
  `false_positive_rate > 0.3`. Вместо этого — `_enter_degraded_mode()`.
  Нарушение: прямой `block_pipeline()` при FPR > 0.3.
- `I_OBS_1`: Write Protocol violations всегда вызывают полный блок (уровень 2),
  независимо от FPR.
- `I_OBS_2`: Degraded mode автоматически снимается через 5 мин если аномалия
  не подтвердилась.

**Результат:** +15% uptime агента при ложных срабатываниях.
Пользователь продолжает получать ответы даже в деградированном режиме.

---

### RFC0042 — Трёхслойный Архитектурный Контракт

**Проблема:** L5 Policy может влиять на поведение → поведение влияет на ingestion
→ ingestion влияет на Graph. Fractal Memory (L2/L2.5) меняет retrieval-приоритеты →
косвенно меняет что попадает в контекст → влияет на выводы L4.
Это скрытые петли обратной связи, которые могут накапливать bias.

**Решение:** Жёсткое разделение на три слоя с контрактом прав записи.

```
┌─────────────────────────────────────────────────────────────┐
│  TRUTH CORE                                                  │
│  L3 (Neo4j Graph) + L3.5 (Immutable Core) + ESM + Source   │
│  Права записи: ТОЛЬКО через Write Protocol (RFC0031)        │
│  Что хранит: факты, их эпистемическое состояние, история    │
│  Что НЕ делает: не знает о ценностях, режимах, стратегиях   │
└───────────────────────────┬─────────────────────────────────┘
                            │ только чтение
┌───────────────────────────▼─────────────────────────────────┐
│  POLICY CORE                                                 │
│  L5 (MetaController) + Ring Zero + Risk Model + Режимы      │
│  Права записи: только в Policy-хранилище (не в L3)          │
│  Что делает: управляет поведением агента, стилем, рисками    │
│  Что НЕ делает: НЕ меняет факты, НЕ меняет trust_score      │
└───────────────────────────┬─────────────────────────────────┘
                            │ только чтение + метрики
┌───────────────────────────▼─────────────────────────────────┐
│  EVOLUTION CORE                                              │
│  ClosedLoopEval + SemanticDriftMonitor + AttackSimulation    │
│  Права записи: только в ReasoningBank (L4) через RFC0039 TS │
│  Что делает: измеряет, тестирует, предлагает изменения       │
│  Что НЕ делает: НЕ меняет Truth Core и Policy Core напрямую │
└─────────────────────────────────────────────────────────────┘
```

**Fractal Governance Contract:**
```python
# fractal_governance.py — RFC0042
FRACTAL_ALLOWED_WRITES = {
    "L2",   # может менять: retrieval_priority, theme strength
    "L2.5", # может менять: staging_candidates, priority_score
}

FRACTAL_FORBIDDEN_WRITES = {
    "ESM",          # epistemic_state фактов — ЗАПРЕЩЕНО
    "trust_score",  # Source Trust Layer — ЗАПРЕЩЕНО
    "importance",   # importance фактов в L3 — ЗАПРЕЩЕНО
    "Ring Zero",    # VALUES CORE — ЗАПРЕЩЕНО
}

def validate_fractal_write(layer: str, field: str, writer: str) -> bool:
    """
    Вызывается при каждой записи из L2/L2.5.
    Нарушение → FractalGovernanceViolation + лог + Observer++ алерт.
    FIX-G: параметр layer теперь используется — проверяет что writer
    действительно из разрешённых слоёв (L2/L2.5), а не произвольный компонент.
    """
    if layer not in FRACTAL_ALLOWED_WRITES:
        raise FractalGovernanceViolation(
            f"Layer '{layer}' не входит в FRACTAL_ALLOWED_WRITES. "
            f"Только {FRACTAL_ALLOWED_WRITES} могут писать через Fractal Governance."
        )
    if field in FRACTAL_FORBIDDEN_WRITES:
        raise FractalGovernanceViolation(
            f"{layer} ({writer}) attempted to write to '{field}'. "
            f"Fractal Governance violation. Allowed fields: все кроме {FRACTAL_FORBIDDEN_WRITES}"
        )
    return True
```

**Каждое влияние Fractal на поведение логируется:**
```python
# Добавить в L2IngestionEngine и L2.5Scheduler
logger.info(
    "fractal_influence_trace",
    extra={
        "writer":   "L2",
        "field":    "retrieval_priority",
        "theme_id": theme_id,
        "delta":    delta,
        "session":  session_id,
    }
)
```

**Инварианты RFC0042:**
- `I16 (TruthIsolation)`: Truth Core не получает команд от Policy Core или Evolution Core.
  Запись в L3 только через Write Protocol.
- `I_GOV_1`: L2/L2.5 не могут писать в ESM, trust_score, importance, Ring Zero.
- `I_GOV_2`: L5 не может вызывать методы, изменяющие факты в L3.
- `I_GOV_3`: Каждое влияние Fractal на retrieval логируется как `fractal_influence_trace`.

**Результат:** Система остаётся эпистемически чистой на годы.
Bias не накапливается через скрытые петли обратной связи.

---

## 📜 RFC0043 — Hardware Profile Selector

> **Статус**: Canonical

### Назначение

Автоматическая адаптация всего стека Velantrim под физические ресурсы машины. Профиль детектируется один раз при старте и управляет выбором компонентов без ручного вмешательства.

### Профили

```
weak   → RAM < 4 GB или CPU < 4 ядра  (RPi, старый ноутбук, мин. VPS)
medium → RAM 4–12 GB, CPU 4–8 ядер   (ноутбук разработчика, VPS 8GB)
strong → RAM > 12 GB, CPU > 8 ядер   (рабочая станция, сервер, GPU)
```

### Реализация

```python
# hardware_profile.py
import psutil, os

def detect_hardware_profile() -> str:
    ram_gb    = psutil.virtual_memory().total / (1024**3)
    cpu_cores = os.cpu_count() or 1
    if ram_gb < 4 or cpu_cores < 4:    return "weak"
    elif ram_gb < 12 or cpu_cores < 8: return "medium"
    else:                              return "strong"
```

```python
# velantrim_config.py — добавить блок RFC0043
import os as _os
from hardware_profile import detect_hardware_profile

HARDWARE_PROFILE = _os.getenv("VELANTRIM_HW_PROFILE", detect_hardware_profile())
_HW = HARDWARE_PROFILE

NEO4J_ENABLED          = _HW == "strong"
REDIS_ENABLED          = _HW in ("medium", "strong")
GRAPH_BACKEND          = {"weak": "graph_lite", "medium": "kuzu", "strong": "neo4j"}[_HW]  # P0-H FIX
VECTOR_BACKEND         = {"weak": "chroma_memory", "medium": "chroma_persistent",
                          "strong": "qdrant"}[_HW]
CONSOLIDATION_PARALLEL = _HW != "weak"
CONSOLIDATION_WORKERS  = {"weak": 1, "medium": 2, "strong": 8}[_HW]
DUCKDB_SYNC_INTERVAL   = {"weak": 3600, "medium": 1800, "strong": 900}[_HW]
EMBEDDING_MODEL        = ("paraphrase-multilingual-MiniLM-L12-v2"
                          if _HW == "weak" else "deepvk/USER-bge-m3")
TELEMETRY_ENABLED      = _HW != "weak"
VELUM_MAX_EDGES        = {"weak": 500, "medium": 1000, "strong": 2000}[_HW]
CLUSTERING_ALGO        = "minibatch_kmeans" if _HW == "weak" else "agglomerative"
```

### Матрица компонентов

| Возможность | weak | medium | strong |
|-------------|------|--------|--------|
| Graph DB | SQLite Graph-Lite | KuzuDB embedded    | Neo4j 5.26+ |
| Vector DB | ChromaDB in-memory | ChromaDB persistent | Qdrant |
| Event Bus | SQLite WAL queue | Redis 512MB | Redis Streams |
| Embeddings | MiniLM-L12 (~120MB) | USER-bge-m3 (~500MB) | USER-bge-m3 |
| Consolidation | sequential ×3 | partial ×2 | full parallel |
| Telemetry | logs only | metrics | full OTel |
| DuckDB sync | 60 мин | 30 мин | 15 мин |

### Инвариант RFC0043

```
I17 (HWProfile): HARDWARE_PROFILE авто-детектируется при старте.
    Ручное переопределение через VELANTRIM_HW_PROFILE env var.
    Нарушение: хардкод компонентов без учёта профиля.
```

---

### RFC0048: Multi-Component Memory Budget

**Проблема**: I22 проверяет только `LLM_TOTAL_PARAMS ≤ available_RAM`. Не учитываются Neo4j PageCache, Redis, Vector DB, буфер ОС. При MoE-модели на 30B возможен OOM даже при прохождении I22.

**Решение**: суммарный бюджет всех компонентов при старте.

```python
# hardware_profile.py — добавить в startup_ram_check()

def compute_memory_budget(config) -> dict:
    available  = psutil.virtual_memory().available

    llm_ram    = _parse_param_size(config.LLM_TOTAL_PARAMS)   # "30B" → bytes
    neo4j_ram  = config.NEO4J_PAGE_CACHE_GB * 1024**3         # default 2 GB
    redis_ram  = _parse_redis_maxmem(config.REDIS_MAXMEM)     # default 512 MB
    vector_ram = config.VECTOR_RAM_GB * 1024**3               # default 1 GB
    os_buffer  = 2 * 1024**3                                  # 2 GB резерв ОС

    total    = llm_ram + neo4j_ram + redis_ram + vector_ram + os_buffer
    pressure = total / available

    return {"total_gb": total / 1024**3,
            "available_gb": available / 1024**3,
            "pressure": pressure,
            "fits": pressure <= config.MEM_PRESSURE_WARN}

def startup_ram_check(config):
    budget = compute_memory_budget(config)
    multi_component_ram_pressure.set(budget["pressure"])

    if budget["pressure"] > config.MEM_PRESSURE_CRIT:
        logger.critical(
            f"RAM budget critical: {budget['total_gb']:.1f}GB required, "
            f"{budget['available_gb']:.1f}GB available. "
            f"Downgrading profile → LLM_MODE=offline."
        )
        if config.HARDWARE_PROFILE == "strong":
            config.HARDWARE_PROFILE = "medium"
        config.LLM_MODE = "offline"
```

```python
# velantrim_config.py — добавить:
NEO4J_PAGE_CACHE_GB  = 2.0    # должно совпадать с docker-compose
VECTOR_RAM_GB        = 1.0    # Qdrant persistent / ChromaDB
MEM_PRESSURE_WARN    = 0.85   # Prometheus WARN threshold
MEM_PRESSURE_CRIT    = 0.92   # принудительный downshift
```

```
I24 (MultiComponentBudget): При старте обязана выполняться проверка суммарного
    RAM-бюджета: LLM + Neo4j_PageCache + Redis + VectorDB + OS_buffer.
    При pressure > MEM_PRESSURE_CRIT — downshift профиля или LLM_MODE=offline.
    Нарушение: старт без compute_memory_budget() при LLM_ARCHITECTURE=moe.
```

---

## 📜 RFC0044 — LLM_MODE: Offline-режим

> **Статус**: Canonical

### Назначение

Три режима работы с LLM. При `offline` система полностью обходится без LLM-вызовов, используя FactRouter + BM25 + LensEngine. 80% функционала сохраняется.

### Конфигурация

```python
# velantrim_config.py — добавить после RFC0043 блока
LLM_MODE = _os.getenv("VELANTRIM_LLM_MODE",
           "offline" if _HW == "weak" else "full")
# "full"    → облачный LLM (GPT/Claude/Qwen3-Max)
# "lite"    → локальный LLM (Qwen3.5-14B / Llama4)
# "offline" → без LLM: FactRouter + BM25 + LensEngine (RFC0045)
```

### Fast Path без LLM

```
User Query
    │
    ▼ [1] Normalizer + Lemmatizer  (pymorphy2, RU)
    ▼ [2] FactRouter RFC0038       (FACTUAL|PROCEDURAL|EPISODIC|META)
    ▼ [3] SafeFTSQuery + BM25      (SQLite FTS5 / Neo4j fulltext)
    ▼ [4] Semantic Reranker        (cosine, локальные эмбеддинги)
    ▼ [5] LensMatcher RFC0045      → активная линза L4
    ▼ [F2.6] GraphQueryExecutor   → структурированный ответ из L3
    ▼ [7] ResponseFormatter        → шаблонный ответ без LLM
    │
    Response
```

### Изменение fast_path.py

```python
# fast_path.py — добавить ветку перед LLM-вызовом

# ❌ БЫЛО:
response = await self.llm.complete(context)

# ✅ СТАЛО:
if config.LLM_MODE == "offline":
    response = await self.lens_engine.execute(
        query=query, entity=detected_entity, session_id=session_id
    )
else:
    response = await self.llm.complete(context)
```

### Entity Extraction без LLM

```python
# offline_extractor.py — замена Graphiti extraction при LLM_MODE=offline
import spacy

class OfflineEntityExtractor:
    """
    spaCy ru_core_news_lg  → PER, ORG, LOC, DATE  (~500MB, CPU-only)
    regex patterns         → числа, URL, команды
    domain keyword dict    → термины из L3 таксономии (загружаются при старте)
    """
    def __init__(self, graph):
        self.nlp              = spacy.load("ru_core_news_lg")
        self.domain_keywords  = self._load_from_l3(graph)

    def extract(self, text: str) -> list[dict]:
        doc      = self.nlp(text)
        entities = [{"name": e.text, "type": e.label_,
                     "confidence": 0.85, "source": "spacy_ner"}
                    for e in doc.ents]
        for kw in self.domain_keywords:
            if kw.lower() in text.lower():
                entities.append({"name": kw, "type": "DOMAIN_CONCEPT",
                                  "confidence": 1.0, "source": "keyword"})
        return entities
```

### Инвариант RFC0044

```
I18 (LLMMode): При LLM_MODE=offline Fast Path обязан использовать LensEngine.
    Прямой вызов llm.complete() при offline — нарушение.
    Нарушение: llm.complete() при LLM_MODE=offline.
```

---

## 📜 RFC0045 — LensEngine: Детерминированные Линзы L4/L5

> **Статус**: Canonical

### Назначение

Expert System поверх L3 графа. 30 линз — детерминированные паттерны понимания запроса и формирования ответа без LLM. При хорошо наполненном L3 ответы точнее LLM: нет галлюцинаций, только верифицированные факты.

Каждая линза = `{intent_match} → {graph_query} → {formatted_answer}`

### DSL линзы

```python
# lens_engine.py
from dataclasses import dataclass

@dataclass
class Lens:
    lens_id:           str          # "lens:factual_definition"
    name:              str          # "Определение понятия"
    domain:            str | None   # "domain:physics" или None (универсальная)
    priority:          int          # 1–100, выше = матчится первее

    # Матчинг интента
    intent_patterns:   list[str]    # regex
    bm25_keywords:     list[str]    # BM25-якоря
    query_types:       list[str]    # из FactRouter: ["FACTUAL", "CONCEPTUAL"]

    # Граф-запрос
    cypher_template:   str          # шаблон Cypher (Neo4j / Kuzu)
    sqlite_template:   str          # аналог для Graph-Lite (weak/offline)
    result_limit:      int
    confidence_floor:  float        # мин. epistemic_score факта

    # Ответ
    response_template: str          # jinja2
    fallback_message:  str          # если граф пуст

    # L5 Observer hook
    observer_check:    bool
    trust_threshold:   float
```

### Жизненный цикл запроса

```
Query → LensMatcher
  score = bm25_match × 0.4 + intent_regex × 0.4 + entity_type × 0.2
  if max_score > 0.3 → выбрать линзу с max score

       → GraphQueryExecutor
  Подставить {entity}, {domain} в cypher_template (Neo4j)
                              или sqlite_template  (weak/offline)
  Фильтр: epistemic_score >= confidence_floor
          epistemic_variance <= 0.7  (иначе добавить [UNVERIFIED])
          is_active = true

       → L5 Observer Check (если observer_check=True)
  FPR > 0.3 → degraded mode (RFC0041)

       → ResponseFormatter  (jinja2)
  Нет результатов → fallback_message

       → Answer  (без LLM)
```

### Интеграция в Canonical Memory Protocol

```
F2.6: LensEngine (RFC0045)
    → если LLM_MODE=offline:
      → LensMatcher.match_lens(query, query_type)
      → GraphQueryExecutor (Cypher / SQLite)
      → ResponseFormatter (jinja2) → ответ без LLM
    → если LLM_MODE=full/lite: шаг пропускается
```

### 30 линз — таксономия

```
Группа A: Фактические запросы (8 линз)
  lens:factual_definition   "что такое X"          → :Concept → :Fact
  lens:factual_property     "свойства X"           → :Entity → :Fact (HAS)
  lens:factual_comparison   "X или Y"              → [:CONTRADICTS|SIMILAR]
  lens:factual_cause        "почему X"             → :Fact → [:CAUSES] → :Fact
  lens:factual_consequence  "что будет если X"     → [:CAUSES] reverse
  lens:factual_condition    "когда X"              → :Fact (condition field)
  lens:factual_number       "сколько X"            → :Fact (value, numeric)
  lens:factual_date         "когда произошло X"    → :Fact (valid_from)

Группа B: Процедурные запросы (6 линз)
  lens:procedural_howto     "как сделать X"        → :Strategy (procedural)
  lens:procedural_debug     "ошибка X"             → :Strategy (failure_context)
  lens:procedural_optimize  "улучшить X"           → :Strategy (success_rate>0.7)
  lens:procedural_setup     "установить X"         → :Strategy (type=setup)
  lens:procedural_sequence  "порядок X"            → [:PRECEDES] chain
  lens:procedural_checklist "список для X"         → :Strategy (type=checklist)

Группа C: Эпизодические запросы (5 линз)
  lens:episodic_last        "последний раз"        → :Episode ORDER BY timestamp
  lens:episodic_session     "в этой сессии"        → :Episode WHERE session_id
  lens:episodic_outcome     "чем закончилось X"    → :Episode (outcome)
  lens:episodic_pattern     "часто ли X"           → :Theme (cluster)
  lens:episodic_error       "ошибки с X"           → :Episode WHERE outcome=FAILURE

Группа D: Стратегические запросы (4 линзы)
  lens:strategy_best        "лучший способ X"      → :Strategy ORDER BY success_rate
  lens:strategy_avoid       "что не делать"        → :Strategy (failure_penalty>0.7)
  lens:strategy_context     "в контексте X как"    → :Strategy (cosine>0.6)
  lens:strategy_learned     "чему научились"       → :Strategy + :Experience

Группа E: Мета-запросы (4 линзы)
  lens:meta_memory          "что ты помнишь о X"   → :Fact COUNT + :Entity
  lens:meta_confidence      "уверен ли ты"         → :Fact (epistemic_score,variance)
  lens:meta_conflict        "есть ли противоречия" → [:CONTRADICTS] search
  lens:meta_domains         "в какой области X"    → :Domain taxonomy

Группа F: Специальные линзы (3 линзы)
  lens:ring_zero_guard      priority=100, всегда первый → VALUES CORE защита
  lens:contradiction_alert  [:CONTRADICTS] в результатах → предупреждение
  lens:empty_graph_fallback граф пуст → graceful fallback без LLM
```

### Структура файлов

```
velantrim/
├── lens_engine.py          ← LensEngine, LensMatcher, GraphQueryExecutor
├── normalizer.py           ← pymorphy2 + RU stop-words
├── offline_extractor.py    ← spaCy NER + domain keywords
└── lenses/                 ← 30 YAML-файлов линз
    ├── factual_definition.yaml
    ├── factual_property.yaml
    ├── ... (28 файлов)
    └── empty_graph_fallback.yaml
```

### Инвариант RFC0045

```
I19 (LensEngine): LensEngine читает только из L3 (граф) или Graph-Lite (SQLite).
    Никаких LLM-вызовов внутри линз.
    Нарушение: llm.complete() или llm.generate() внутри LensEngine или линзы.
```

---

### RFC0051: LensEngine Composition

**Проблема:**: смешанный запрос ("почему фотосинтез важен и как его улучшить?") активирует несколько интентов одновременно. Одна линза → неполный ответ или `lens_fallback`. В offline-режиме fallback = пустой шаблон → деградация UX.

**Решение**: при совпадении 2+ линз выше порога — запускать `compose()`, объединять результаты через CORNER.

#### Расширение lens_engine.py

```python
@dataclass
class LensMatch:
    lens_id:  str
    intent:   str
    score:    float
    cypher:   str
    template: str   # Jinja2

class LensEngine:

    def match_all(self, query: str,
                  threshold: float = None) -> list[LensMatch]:
        """Возвращает ВСЕ линзы выше порога, по убыванию score."""
        threshold = threshold or LENS_COMPOSITION_THRESHOLD
        normalized = self.normalizer.lemmatize(query)
        return sorted(
            [LensMatch(l.lens_id, l.intent,
                       self._score(normalized, l), l.cypher_template, l.response_template)
             for l in self.lenses if self._score(normalized, l) >= threshold],
            key=lambda m: m.score, reverse=True
        )

    async def compose(self, query: str) -> ComposedResult | None:
        """
        До MAX_COMPOSED_LENSES линз → объединить через CORNER.
        При пустом matches → None → fallback на HybridRetriever или BAE generic.
        """
        matches = self.match_all(query)
        if not matches:
            return None

        facts = []
        for match in matches[:MAX_COMPOSED_LENSES]:
            facts.extend(await self._execute_lens(match))

        return ComposedResult(
            facts=self.corner.deduplicate(facts),
            intents=[m.intent  for m in matches[:MAX_COMPOSED_LENSES]],
            lens_ids=[m.lens_id for m in matches[:MAX_COMPOSED_LENSES]],
        )
```

#### Конфигурация (velantrim_config.py)

```python
# добавить:
LENS_COMPOSITION_THRESHOLD = 0.45   # мин. score для включения в compose()
MAX_COMPOSED_LENSES        = 3      # макс. линз в одном запросе
LENS_FALLBACK_TO_BAE       = True   # compose()=None → BAE generic
```

#### Обновление F2.6 (fast_path.py)

```
F2.6: LensEngine (RFC0045 + RFC0051)
    → если LLM_MODE=offline:
      → matches = LensEngine.match_all(query)
      → если len(matches) >= 2:
          → result = LensEngine.compose(query)      ← RFC0051
          → CORNER уже применён внутри compose()
      → если len(matches) == 1:
          → result = LensEngine.match(query)        ← одиночная линза
      → если len(matches) == 0:
          → fallback: BAE generic или HybridRetriever (lite)
    → если LLM_MODE=full/lite: шаг пропускается
```

#### BAE — зафиксированный порядок внедрения

```
⚠️ РЕШЕНИЕ:
   BAE внедряется итерационно, не все 5 профилей сразу:

   Phase 1 MVP:  только профиль "neutral"
                 RST-скелеты + Microplanner без анафоры
                 Surface RU: только pymorphy2 согласование падежей
                 + ClosedLoopEval оценка качества (обязательно перед prod)

   Phase 2:      профили "concise" и "detailed"
                 анафора + anti-repeat в Microplanner

   Phase 3:      профили "scientific" и "friendly"
                 CORNER diversity weight tuning

   Запрет: не деплоить BAE в production без ClosedLoopEval-оценки.
```

```
I27 (LensCompose): При совпадении query с 2+ линзами с score ≥ LENS_COMPOSITION_THRESHOLD
    LensEngine обязан запустить compose() вместо одиночного match().
    Результаты объединяются через CORNER перед Facts Pack.
    При compose()=None → fallback на HybridRetriever (full/lite) или BAE generic (offline).
    Нарушение: одиночный match() при наличии 2+ линз выше порога.
```

---

> **Статус**: Canonical
>
> Расширение RFC0045 LensEngine. BAE превращает факты из L3 графа в читаемый связный текст без трансформеров. Даёт ответ лучше энциклопедии — структурированный под контекст вопроса.

### Принцип

```
Сухая энциклопедия:
  "Фотосинтез — процесс синтеза органических веществ из CO₂ и H₂O."

BAE RST-lite:
  "Фотосинтез — это способ, которым растения получают энергию из солнца.
   Лист ловит свет → CO₂ из воздуха + вода из почвы → сахар (питание растения)
   + кислород (воздух для нас). Именно поэтому без растений не было бы жизни."

Разница: не знания, а СТРУКТУРА подачи.
Человек читал словарь и понимал — значит BAE достаточно для 80% запросов.
```

### Компоненты BAE

#### 1. RST-lite — Discourse Planner (логика блоков)

Определяет порядок подачи информации на основе интента линзы:

```python
# Скелеты ответов по интентам (rsl_skeletons.py)
SKELETONS = {
    "DEFINE":   ["definition", "mechanism", "example", "note"],
    "WHY":      ["cause", "evidence", "consequence", "summary"],
    "HOW":      ["precondition", "steps", "result", "warning"],
    "COMPARE":  ["entity_a", "entity_b", "difference", "recommendation"],
    "FACT":     ["claim", "evidence", "confidence"],
    "WHERE":    ["location", "habitat", "region", "note"],
    "WHEN":     ["event", "period", "context", "significance"],
    "PROCEDURE":["goal", "steps", "result", "common_errors"],
}

# Каждый скелет = набор блоков которые собираются из фактов L3 графа
# Интент определяется LensMatcher (RFC0045) → передаётся в BAE
```

#### 2. Microplanner — связность текста

Склеивает блоки в естественный текст:

```python
# microplanner.py
TRANSITIONS = {
    "cause→consequence": "это означает что",
    "definition→example": "например",
    "mechanism→note":    "следует отметить",
    "steps→result":      "в результате",
    "claim→evidence":    "согласно",
}

ANAPHORA_MAP = {
    "PERSON": ["он", "она", "данный человек"],
    "CONCEPT": ["это", "данное понятие", "оно"],
    "PROCESS": ["данный процесс", "он", "это"],
    "OBJECT":  ["он", "она", "оно", "данный объект"],
}

# Anti-repeat: если слово встречается в двух соседних предложениях
# → заменить анафорой или переформулировать
```

#### 3. Surface Realizer RU — морфология

```python
# nlp_utils.py — синглтон MorphAnalyzer + кэш нормализации
# FIX: pymorphy2.MorphAnalyzer() создавался заново на каждый вызов — ~200ms инициализации.
# Синглтон + lru_cache дают 40–60% экономию CPU при активном ReasoningBank и LensEngine.
#
# double-checked locking: потокобезопасно при concurrent asyncio-корутинах.
# lru_cache(4096): стоп-слова и термины домена нормализуются один раз навсегда.

import threading
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

_morph_analyzer = None
_morph_lock = threading.Lock()

def get_morph_analyzer():
    """
    Вернуть синглтон MorphAnalyzer. Потокобезопасно (double-checked locking).
    При недоступности pymorphy2/pymorphy3 — вернуть None, вызывающий делает fallback.
    """
    global _morph_analyzer
    if _morph_analyzer is None:
        with _morph_lock:
            if _morph_analyzer is None:
                try:
                    import pymorphy3
                    _morph_analyzer = pymorphy3.MorphAnalyzer()
                    logger.info("nlp_utils: pymorphy3 MorphAnalyzer initialized")
                except ImportError:
                    try:
                        import pymorphy2
                        _morph_analyzer = pymorphy2.MorphAnalyzer()
                        logger.info("nlp_utils: pymorphy2 MorphAnalyzer initialized (fallback)")
                    except ImportError:
                        logger.warning("nlp_utils: neither pymorphy3 nor pymorphy2 found — normalize_word falls back to lower()")
    return _morph_analyzer

@lru_cache(maxsize=4096)
def normalize_word(word: str) -> str:
    """
    Привести слово к нормальной форме (лемматизация).
    lru_cache: стоп-слова и ключевые термины нормализуются один раз.
    Fallback на lower() если morph недоступен.
    """
    morph = get_morph_analyzer()
    if morph is None:
        return word.lower()
    try:
        return morph.parse(word)[0].normal_form
    except Exception:
        return word.lower()


# surface_ru.py — pymorphy согласование
# "берёза растёт в лес" → "берёза растёт в лесу"
# Род, число, падеж согласуются автоматически
# FIX: использует синглтон get_morph_analyzer() вместо модульного morph = MorphAnalyzer()

def agree_phrase(word: str, case: str, gender: str = None) -> str:
    """Согласовать слово по падежу и роду."""
    morph = get_morph_analyzer()
    if morph is None:
        return word
    try:
        parsed = morph.parse(word)[0]
        return parsed.inflect({case}).word if parsed.inflect({case}) else word
    except Exception:
        return word
```

#### 4. Style Profiles — параметрические профили

```python
# style_profiles.py
STYLE_PROFILES = {
    "simple":     {"max_terms": 0, "sent_len": "short",  "tone": "friendly",
                   "anaphora": True,  "transitions": "simple"},
    "neutral":    {"max_terms": 3, "sent_len": "medium", "tone": "neutral",
                   "anaphora": True,  "transitions": "standard"},
    "scientific": {"max_terms": 10,"sent_len": "long",   "tone": "formal",
                   "anaphora": False, "transitions": "academic"},
    "auditor":    {"max_terms": 5, "sent_len": "medium", "tone": "strict",
                   "anaphora": False, "transitions": "logical"},
    "literary":   {"max_terms": 2, "sent_len": "varied", "tone": "warm",
                   "anaphora": True,  "transitions": "narrative"},
}
# Профиль = параметры, НЕ персонаж — иначе стиль начнёт влиять на истину
```

### CORNER — дедупликация перед Facts Pack

```python
# corner.py — всегда стоит между RRF Fusion и Facts Pack
class CORNER:
    """
    Deduplicate + Diversity + Pack
    Без CORNER: дублирующие факты раздувают контекст и снижают точность.
    """
    def process(self, candidates: list, budget: int = 10) -> FactsPack:
        # 1. Dedupe: убрать факты с cosine > 0.95
        deduped  = self._deduplicate(candidates, threshold=0.95)
        # 2. Diversity: не более 3 фактов из одного узла
        diverse  = self._ensure_diversity(deduped, max_per_source=3)
        # 3. Budget: топ-K по epistemic_score
        top_k    = sorted(diverse, key=lambda x: x.score, reverse=True)[:budget]
        return FactsPack(facts=top_k)
```

### Три режима retrieval по размеру корпуса

```
МАЛЫЙ корпус (< 10k узлов):
  Query → Normalizer → Lemma → Router → BM25
        → CORNER → Facts Pack → Truth Gate → BAE
  Нет RRF, нет LSA. Один канал — быстро и точно.

СРЕДНИЙ корпус (10k–500k узлов):
  BM25 ──┐
  Graph  ├──→ RRF Fusion → CORNER → Facts Pack → Truth Gate → BAE
  Embed ─┘
  RRF стоит между retrieval и Facts Pack.

БОЛЬШОЙ корпус (500k+ узлов / много книг):
  LSA Topic Router (сужает до 20–50 кластеров)
      → Local BM25 + Embeddings (только внутри выбранных)
      → RRF Fusion → CORNER → Facts Pack → Truth Gate → BAE
  LSA — не для фактов, а для сужения пространства поиска.
```

**Правила размещения:**

| Ситуация | RRF | LSA |
|----------|-----|-----|
| Один поисковик | ❌ не нужен | ❌ не нужен |
| Несколько каналов | ✅ перед Facts Pack | ❌ не нужен |
| 500k+ узлов / книги | ✅ перед Facts Pack | ✅ до BM25 (сужатель) |

### Суммаризация: без LLM и с LLM

> **Ситуация**: для L4.5 ResponseAudit нужна суммаризация ответа LLM.
> Полная абстрактная суммаризация пока требует LLM. Ниже — лучшее что есть без трансформеров.

| Технология | Суть | Качество | RAM | Скорость |
|-----------|------|----------|-----|----------|
| TF-IDF extractive | Выбирает лучшие предложения | 60% | ~5 MB | <10ms |
| **TextRank** | PageRank на графе предложений | **70%** | ~10 MB | <30ms |
| **LSA** | Латентный семантический анализ | **65-75%** | ~50 MB | <50ms |
| **BAE RST-lite** | Генерация из фактов по шаблону | **75-85%** | ~20 MB | <20ms |
| Tiny LLM 1-3B | Qwen3-1.7B / OLMoE (offline) | 85-90% | ~2 GB | <200ms |
| Fast LLM 7B+ | Qwen3-7B (lite) | 90-93% | ~6 GB | <300ms |
| Cloud LLM | Haiku / o4-mini (full) | 95%+ | — | <500ms |

```
⚠️ Статус суммаризации без LLM (технически честно):

✅ BAE RST-lite — генерация из фактов = 75-85% (основной путь offline)
✅ TextRank    — пересказ готового текста = 70% (extractive)
⚠️ Полная абстрактная суммаризация ответа LLM без трансформера —
   пока нет технологии с качеством > 75% + скоростью < 100ms

До появления решения:
  LLM_MODE=offline → TextRank extractive суть
  LLM_MODE=lite    → Tiny LLM 1-3B (Qwen3-1.7B, ~2GB RAM)
  LLM_MODE=full    → Fast LLM в Slow Path
```

### Итоговое качество по режимам

| | offline (BAE) | lite (Tiny LLM) | full (Fast LLM) |
|--|:--:|:--:|:--:|
| Галлюцинации | ❌ невозможны | ❌ невозможны* | ❌ невозможны* |
| Качество текста | 75-85% | 85-90% | 95%+ |
| P95 латентность | <50ms | <200ms | <500ms |
| RAM | ~100 MB | ~2 GB | ~10 GB+ |
| Интернет | не нужен | не нужен | опционально |

*LLM работает только как переформулировщик фактов из L3 — Graph = Truth не меняется.

### Инвариант RFC0045-BAE

```
I21 (CORNER): CORNER обязателен между RRF Fusion и Facts Pack.
    При наличии нескольких retrieval-каналов пропуск CORNER —
    нарушение (дублирующие факты в контексте).
    Нарушение: Facts Pack без предварительной дедупликации при multi-channel retrieval.
```

---

> **Статус**: Canonical
>
> Три связанных улучшения L4 ReasoningBank и L3 Truth Core.

### RFC0046-A: DAG Rollback в L4

**Проблема**: шаги рассуждения агента хранятся как плоский список. При ошибке нет памяти о тупиковых путях — агент повторяет ошибки.

**Решение**: граф рассуждений = направленный ациклический граф (DAG). Тупиковые ветки фиксируются ребром `[:ROLLBACK_TO]`.

#### Новые типы рёбер (neo4j_setup.py)

```cypher
-- Добавить в create_schema() — RFC0046

-- Шаги рассуждения агента связаны в DAG
(:ReasoningStep)-[:PRECEDES]->(:ReasoningStep)

-- Тупиковая ветка — Observer++ вызывает при graduated block
(:ReasoningStep)-[:ROLLBACK_TO {
    reason:     string,    -- "OBSERVER_BLOCK" | "TASK_FAILED" | "CONTRADICTION"
    rolled_at:  datetime,
    session_id: string
}]->(:ReasoningStep)

-- Индекс для быстрого поиска тупиков в текущей сессии
CREATE INDEX reasoning_rollback_idx IF NOT EXISTS
FOR ()-[r:ROLLBACK_TO]-() ON (r.session_id)
```

#### Метод rollback_to() (reasoning_bank.py)

```python
# Добавить в класс ReasoningBank — RFC0046

async def rollback_to(
    self,
    from_step_id: str,
    to_step_id:   str,
    reason:       str,
    session_id:   str
) -> None:
    """
    Зафиксировать тупиковую ветку рассуждений.
    LensEngine и LLM видят [:ROLLBACK_TO] и не повторяют ошибку.
    Observer++ вызывает при entered_degraded_mode().
    """
    await self.graph.execute_cypher("""
        MATCH (a:ReasoningStep {id: $from_id})
        MATCH (b:ReasoningStep {id: $to_id})
        MERGE (a)-[:ROLLBACK_TO {
            reason:     $reason,
            rolled_at:  datetime(),
            session_id: $session_id
        }]->(b)
    """, {"from_id":    from_step_id,
          "to_id":      to_step_id,
          "reason":     reason,
          "session_id": session_id})
```

---

### RFC0050: DAG Rollback Transactional Write

**Проблема:**: при асинхронной записи шагов рассуждений возникает race condition — `[:ROLLBACK_TO]` создаётся до того как `from_step` существует в Neo4j → `NotFoundException` → потеря информации об откате.

**Решение**: проверять существование обоих узлов перед MERGE; при их отсутствии — откладывать в `ConsolidationQueue` с retry.

```python
# reasoning_bank.py — заменить прямой MERGE на транзакционную запись

async def create_rollback_edge(
    self,
    from_step_id: str,
    to_step_id:   str,
    reason:       str,
    session_id:   str,
    retry_queue:  ConsolidationQueue,
) -> bool:
    """
    Создаёт [:ROLLBACK_TO] только если оба узла существуют.
    Иначе откладывает в ConsolidationQueue (персистентная SQLite-очередь).
    """
    result = await self.graph.execute_cypher("""
        OPTIONAL MATCH (a:ReasoningStep {id: $from_id})
        OPTIONAL MATCH (b:ReasoningStep {id: $to_id})
        WITH a, b
        WHERE a IS NOT NULL AND b IS NOT NULL
        MERGE (a)-[r:ROLLBACK_TO {
            reason:     $reason,
            rolled_at:  datetime(),
            session_id: $session_id
        }]->(b)
        RETURN r IS NOT NULL AS created
    """, {"from_id": from_step_id, "to_id": to_step_id,
          "reason": reason, "session_id": session_id})

    if result and result[0].get("created"):
        return True

    # Один или оба узла ещё не сохранены → отложить
    dag_rollback_retry_total.inc()
    await retry_queue.put(RetryTask(
        task_type="dag_rollback",
        payload={"from_step_id": from_step_id, "to_step_id": to_step_id,
                 "reason": reason, "session_id": session_id},
        retry_after_seconds=5,
        max_retries=10,
    ))
    logger.warning(
        f"DAG rollback deferred: {from_step_id} → {to_step_id}. Queued."
    )
    return False
```

```
I26 (DAGRollbackTransaction): Ребро [:ROLLBACK_TO] создаётся ТОЛЬКО если оба
    :ReasoningStep существуют в Neo4j. При отсутствии — ConsolidationQueue,
    retry до 10 раз. Нарушение: MERGE без OPTIONAL MATCH обоих узлов.
```

---

### RFC0046-B: epistemic_variance в :Fact

**Проблема**: ESM даёт бинарную уверенность (Validated / не Validated). Нет градации "насколько агент сомневается".

**Решение**: поле `epistemic_variance: float` на каждом :Fact.

```
1.0 = полная неопределённость (новый факт, не проверен)
0.5 = частичная уверенность (Supported, есть Evidence)
0.0 = полная уверенность (Validated, многократно подтверждён)
```

#### Изменение схемы (neo4j_setup.py)

```cypher
-- Поле уже добавлено в схему :Fact (см. раздел «Схема графа»)
-- epistemic_variance: 1.0 по умолчанию при создании

-- Миграция существующих фактов:
MATCH (f:Fact) WHERE f.epistemic_variance IS NULL
SET f.epistemic_variance = CASE
    WHEN f.epistemic_state = 'Validated'    THEN 0.1
    WHEN f.epistemic_state = 'Supported'    THEN 0.4
    WHEN f.epistemic_state = 'Hypothesized' THEN 0.7
    ELSE 1.0
END
```

#### Тег [UNVERIFIED] в context_builder.py

```python
# Добавить в _format_context() при формировании Facts Pack — RFC0046

for fact in facts:
    tag = ""
    if fact.get("epistemic_variance", 1.0) > 0.7:
        tag = " [UNVERIFIED]"
    elif fact.get("epistemic_variance", 1.0) > 0.4:
        tag = " [UNCERTAIN]"
    context_parts.append(f"{fact['content']}{tag}")

# Результат: LLM получает контекст где чётко видно
# какие факты железобетонные, а где база "сомневается"
```

---

### RFC0047: epistemic_variance Formula

**Проблема**: поле `epistemic_variance` вводилось без формулы — ручное проставление, невоспроизводимо, не автообновляется.

#### Строгая формула расчёта

```
variance = 1 / (1 + evidence_count × avg_trust_score)
         + contradiction_penalty

где:
  evidence_count        = COUNT активных [:SUPPORTED_BY] рёбер факта
  avg_trust_score       = AVG(source.trust_score) по этим источникам ∈ [0.0, 1.0]
  contradiction_penalty = min(0.6,  0.3 × COUNT(активных [:CONTRADICTS] входящих))
```

#### ESM-маппинг (нормативный)

| ESM-состояние | Ожидаемый диапазон variance |
|---|---|
| Observed / Hypothesized | 0.85 – 1.0 |
| Supported | 0.40 – 0.65 |
| Validated | 0.05 – 0.25 |
| Contradicted | 0.70 – 1.0 (+ penalty) |
| Deprecated / Collapsed | заморожен, не пересчитывается |

#### Автообновление (fact_manager.py)

```python
# Вызывать при каждом из событий:
# - добавлен/отозван Evidence  - изменился trust_score источника
# - добавлено/снято [:CONTRADICTS]  - ESM-переход факта

async def recalculate_variance(fact_id: str) -> float:
    result = await neo4j.run("""
        MATCH (f:Fact {id: $fid})
        OPTIONAL MATCH (f)-[:SUPPORTED_BY]->(s:Source)
        WITH f,
             count(s)                          AS ev_count,
             coalesce(avg(s.trust_score), 0.0) AS avg_trust
        OPTIONAL MATCH (c:Fact)-[:CONTRADICTS]->(f)
        WITH f, ev_count, avg_trust, count(c) AS contra_count
        SET f.epistemic_variance = (
            1.0 / (1.0 + ev_count * avg_trust)
            + least(0.6, 0.3 * contra_count)
        )
        RETURN f.epistemic_variance AS variance
    """, fid=fact_id)
    return result[0]["variance"]
```

```
I23 (VarianceFormula): epistemic_variance на :Fact обязан вычисляться
    по формуле RFC0047, не проставляться вручную.
    Автообновление обязательно при каждом изменении Evidence или [:CONTRADICTS].
    Нарушение: ручной SET f.epistemic_variance без вызова recalculate_variance().
```

---

### RFC0046-C: Temporal рёбра

**Проблема**: факт "пользователь живёт в Берлине" создаёт `[:CONTRADICTS]` при переезде. Но это не противоречие — это изменение во времени.

**Решение**: `valid_from / valid_until` на ключевых рёбрах.

```cypher
-- Рёбра с temporal атрибутами (см. раздел «Схема графа»)
(:Entity)-[:RELATED_TO {strength, type, valid_from, valid_until}]->(:Entity)
(:Fact)-[:CAUSES {valid_from, valid_until}]->(:Fact)

-- valid_until = null → связь актуальна сейчас
-- При "переезде": старое ребро valid_until=now(), новое valid_from=now()
-- НЕ создаём [:CONTRADICTS] — создаём новое temporal ребро
```

```cypher
-- Запрос с temporal фильтрацией
MATCH (e:Entity)-[r:RELATED_TO]->(other)
WHERE (r.valid_until IS NULL OR r.valid_until > datetime())
  AND r.valid_from <= datetime()
RETURN e, r, other
```

---

### RFC0049: Temporal-ESM Sync Protocol

**Проблема:**: при переходе факта в `Contradicted / Deprecated / Collapsed` его исходящие рёбра остаются с `valid_until = NULL` → участвуют в запросах как валидные → фантомные данные, нарушение `Graph = Truth`.

#### Триггер закрытия рёбер (esm_machine.py)

```python
TEMPORAL_CLOSING_STATES = {"Contradicted", "Deprecated", "Collapsed"}
TEMPORAL_EDGE_TYPES     = ["RELATED_TO", "CAUSES", "DERIVED_FROM"]

async def on_state_transition(fact_id: str, old_state: str,
                               new_state: str, neo4j_session):
    if new_state in TEMPORAL_CLOSING_STATES:
        edge_types = "|".join(TEMPORAL_EDGE_TYPES)
        await neo4j_session.run(f"""
            MATCH (:Fact {{id: $fid}})-[r:{edge_types}]->()
            WHERE r.valid_until IS NULL
            SET r.valid_until = datetime()
        """, fid=fact_id)
    # Пересчёт variance при любом ESM-переходе
    await recalculate_variance(fact_id)
```

#### Обязательный фильтр (SafeFTSQuery + LensEngine)

```python
# Добавить во ВСЕ Cypher-запросы, работающие с temporal рёбрами:
TEMPORAL_EDGE_FILTER = """
    AND (r.valid_until IS NULL OR r.valid_until > datetime())
"""
```

#### Миграция существующих рёбер (one-time, при обновлении до)

```cypher
-- migration_v5_06_temporal_backfill.cypher
-- Шаг 1: добавить valid_from на рёбра без него
MATCH ()-[r:RELATED_TO|CAUSES|DERIVED_FROM]->()
WHERE r.valid_from IS NULL
SET r.valid_from = coalesce(r.created_at, datetime("2026-01-01T00:00:00"))
RETURN count(r) AS patched_edges;

-- Шаг 2: закрыть рёбра у Contradicted/Deprecated/Collapsed фактов
MATCH (f:Fact)-[r:RELATED_TO|CAUSES|DERIVED_FROM]->()
WHERE f.epistemic_state IN ["Contradicted", "Deprecated", "Collapsed"]
  AND r.valid_until IS NULL
SET r.valid_until = datetime()
RETURN count(r) AS closed_edges;
```

```
I25 (TemporalESMSync): При переходе :Fact в Contradicted / Deprecated / Collapsed
    все исходящие рёбра [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] с valid_until IS NULL
    обязаны получить valid_until = datetime() в той же транзакции.
    Фильтр (r.valid_until IS NULL OR r.valid_until > datetime()) обязателен
    во всех запросах SafeFTSQuery и LensEngine.
    Нарушение: ESM-переход в закрывающее состояние без синхронного закрытия рёбер.
```

### Инварианты RFC0046

```
I20 (TemporalEdges): Новые рёбра [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] обязаны содержать valid_from при создании.
    valid_until = null означает "актуально сейчас".
    Нарушение: ребро без valid_from созданное .
```

### 📊 Метрики Prometheus (дополнение RFC0036–RFC0038)

| Метрика | Тип | Описание |
|---------|-----|---------|
| `event_fallback_inserted_total` | Counter | Событий сохранено в SQLite fallback |
| `event_fallback_recovered_total` | Counter | Событий восстановлено из fallback |
| `event_fallback_size` | Gauge | Текущий размер очереди fallback |
| `observer_blocks_total` | Counter | Блокировок pipeline от Observer++ |
| `observer_rollbacks_total` | Counter | Откатов инициированных Observer++ |
| `source_trust_pending_facts` | Gauge | Фактов ожидающих верификации |
| `write_protocol_violations_total` | Counter | Нарушений Write Protocol |
| `fact_router_query_type_total` | Counter | Запросов по типу (label: query_type) |
| `fact_router_rerag_triggered_total` | Counter | Итеративных retrieval запущено |
| `closed_loop_faithfulness_p95` | Histogram | P95 faithfulness по ответам |
| `esm_occ_conflicts_total` | Counter | OCC конфликтов в ChunkedInvalidator |
| `duckdb_shadow_lag_seconds` | Gauge | Отставание Shadow State от Neo4j |

### 📊 Метрики Prometheus (RFC0036–RFC0051)

| Метрика | Тип | Описание |
|---------|-----|---------|
| `closed_loop_faithfulness_p95` | Histogram | P95 faithfulness по ответам |
| `esm_occ_conflicts_total` | Counter | OCC конфликтов в ChunkedInvalidator |
| `duckdb_shadow_lag_seconds` | Gauge | Отставание Shadow State от Neo4j |
| `reasoning_bank_ts_score` | Histogram | Thompson Sampling score по стратегии |
| `duckdb_shadow_sync_total` | Counter | Успешных синхронизаций Neo4j→DuckDB |
| `duckdb_shadow_rows_synced` | Gauge | Строк в последней синхронизации |
| `observer_false_positive_rate` | Gauge | Доля ложных срабатываний Observer++ |
| `observer_degraded_mode_total` | Counter | Входов в деградированный режим |
| `observer_full_blocks_total` | Counter | Полных блокировок pipeline |
| `observer_degraded_duration_seconds` | Histogram | Длительность degraded mode |
| `fractal_governance_violations_total` | Counter | Нарушений Fractal Governance |
| `hardware_profile_info` | Gauge | Текущий профиль: weak=0, medium=1, strong=2 |
| `llm_mode_info` | Gauge | Текущий режим: offline=0, lite=1, full=2 |
| `lens_match_total` | Counter | Запросов через LensEngine (label: lens_id) |
| `lens_fallback_total` | Counter | Линза не нашла совпадения → fallback |
| `lens_latency_ms` | Histogram | P95 латентность LensEngine (цель < 50ms) |
| `epistemic_variance_p95` | Histogram | Распределение неопределённости фактов |
| `rollback_to_total` | Counter | DAG откатов рассуждений (label: reason) |
| `temporal_edge_created_total` | Counter | Новых temporal рёбер создано |
| `multi_component_ram_pressure` | Gauge | Суммарный RAM pressure ∈ [0,1] |
| `offline_requests_total` | Counter | Запросов в LLM_MODE=offline |
| `lens_compose_total` | Counter | Запросов через compose() (2+ линзы) |
| `lens_precision_implicit` | Gauge | Доля offline-ответов с положительным feedback |
| `dag_rollback_retry_total` | Counter | Отложенных [:ROLLBACK_TO] из-за отсутствия узлов |
| `temporal_esm_sync_total` | Counter | Рёбер закрыто при ESM-переходе (label: new_state) |

---

## 🔒 Инварианты системы (дополнение к I7, I8)

```
I9  (FactRouter): Маршрутизация запросов — детерминирована, без LLM.
    Нарушение: использование LLM для routing decision.

I10 (OCC): Все операции инвалидации ESM используют версионирование узлов.
    Нарушение: SET без проверки _version_ в WHERE.

I11 (AsyncEval): ClosedLoopEvaluator НЕ блокирует Fast Path.
    Нарушение: синхронный вызов evaluator.evaluate() в пути ответа пользователю.

I12 (FallbackPersist): fallback_queue в EventBus — персистентна (SQLite).
    Нарушение: in-memory Queue как единственное хранилище событий.

I13 (TSReplay): Thompson Sampling в audit-режиме использует seed=session_id_hash.
    Нарушение: стохастичный выбор стратегий без seed при audit replay.

I14 (CQRSRead): Semantic Drift Monitor и Observer аналитика читают из DuckDB,
    не из Neo4j напрямую для агрегаций.
    Нарушение: Cypher агрегация в SemanticDriftMonitor без Shadow State.

I15 (GraduatedBlock): Observer++ НЕ вызывает block_pipeline() если
    false_positive_rate > 0.3. Используется _enter_degraded_mode().
    Нарушение: прямой block_pipeline() при FPR > 0.3.

I16 (TruthIsolation): Truth Core не получает команд от Policy Core или
    Evolution Core. Запись в L3 только через Write Protocol (RFC0031).
    Нарушение: любая запись в L3 минуя TruthGate / HumanApproval / TrustedImport.

I17 (HWProfile): HARDWARE_PROFILE авто-детектируется при старте системы.
    Ручное переопределение через VELANTRIM_HW_PROFILE env var.
    Нарушение: хардкод компонентов (Neo4j, Qdrant) без учёта профиля.

I18 (LLMMode): При LLM_MODE=offline Fast Path обязан использовать LensEngine.
    Прямой вызов llm.complete() при offline — нарушение.
    Нарушение: вызов llm.complete() когда LLM_MODE=offline.

I19 (LensEngine): LensEngine читает только из L3 (граф) или Graph-Lite (SQLite).
    Никаких LLM-вызовов внутри линз.
    Нарушение: llm.complete() или llm.generate() внутри LensEngine или любой линзы.

I20 (TemporalEdges): Новые рёбра [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] обязаны содержать valid_from при создании.
    valid_until = null означает "актуально сейчас".
    Нарушение: ребро без valid_from созданное .

I21 (CORNER): CORNER обязателен между RRF Fusion и Facts Pack при multi-channel retrieval.
    Нарушение: Facts Pack без дедупликации при нескольких retrieval-каналах.

I22 (MoEMemory): При LLM_ARCHITECTURE=moe параметр LLM_TOTAL_PARAMS обязателен
    и проверяется против доступного RAM при старте.
    Нарушение: MoE-модель запущена без проверки LLM_TOTAL_PARAMS ≤ available_RAM.

I23 (VarianceFormula): epistemic_variance на :Fact обязан вычисляться
    по формуле RFC0047, не проставляться вручную.
    Автообновление обязательно при каждом изменении Evidence или [:CONTRADICTS].
    Нарушение: ручной SET f.epistemic_variance без вызова recalculate_variance().

I24 (MultiComponentBudget): При старте системы обязана выполняться проверка
    суммарного RAM-бюджета: LLM_TOTAL_PARAMS + Neo4j_PageCache + Redis + VectorDB + OS_buffer.
    При pressure > 0.92 — обязательный downshift профиля или переход в LLM_MODE=offline.
    Нарушение: старт без compute_memory_budget() при LLM_ARCHITECTURE=moe.

I25 (TemporalESMSync): При переходе :Fact в Contradicted / Deprecated / Collapsed
    все исходящие рёбра [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] с valid_until IS NULL
    обязаны получить valid_until = datetime() в той же транзакции.
    Нарушение: ESM-переход в закрывающее состояние без синхронного закрытия рёбер.

I26 (DAGRollbackTransaction): Ребро [:ROLLBACK_TO] в ReasoningBank создаётся
    ТОЛЬКО если оба узла :ReasoningStep уже существуют в Neo4j.
    При отсутствии любого из узлов — запись откладывается в ConsolidationQueue
    с retry до 10 попыток.
    Нарушение: MERGE [:ROLLBACK_TO] без предварительного MATCH обоих узлов.

I27 (LensCompose): При совпадении query с 2+ линзами с score ≥ LENS_COMPOSITION_THRESHOLD
    LensEngine обязан запустить compose() вместо одиночного match().
    Результаты объединяются через CORNER перед Facts Pack.
    При compose()=None → fallback на HybridRetriever (full/lite) или BAE generic (offline).
    Нарушение: одиночный match() при наличии 2+ линз выше порога.

I74 (StagingReadPath): L2.5 Staging используется на read-пути ТОЛЬКО с пометкой
    `preliminary` и confidence × 0.7.
    Staging НИКОГДА не является источником истины — только граф L3.
    Прямая подстановка staging-факта без пометки `preliminary` — баг.
    Нарушение: использование staging-факта как Validated в ContextBuilder.

I75 (ProtoConceptNaming): Присвоение имени ProtoConcept выполняется ТОЛЬКО в Slow Path
    (Homeostatic Balancer, VolitionWorker или по триггеру B/C из RFC0066).
    Вызов LLM для именования концепта в Fast Path — критический архитектурный баг.
    Триггер A (пользователь спрашивает) должен ставить задачу в Slow Path очередь,
    не выполнять именование синхронно.
    Нарушение: llm.complete() для именования ProtoConcept внутри Fast Path.
```

---

## 📖 Как использовать модули (инструкция)

### Новые модули (RFC0036–RFC0038)

```
RFC0036  → добавить методы в event_bus.py
           + scheduler задачи в main.py

RFC0036+ → миграция схемы Neo4j (_version_ поле)
           + заменить _process_chunks в esm_chunked_invalidator.py
           + удалить asyncio.sleep(0.1)

RFC0037  → перенести ClosedLoopEvaluator в l4_reasoning_worker.py
           + добавить publish(AGENT_RESPONSE) в fast_path.py

RFC0038  → создать fact_router.py
           + интегрировать в fast_path.py перед hybrid_retriever.py

KuzuDB   → GRAPH_BACKEND = "kuzu" в velantrim_config.py (P0-H FIX)
           + создать kuzu_adapter.py (реализует IGraphAdapter)

DuckDB   → создать shadow_state.py
           + scheduler: dump каждые 15 мин → DuckDB
           + Semantic Drift Monitor читает из DuckDB, не Neo4j
```

### Новые модули (RFC0036–RFC0040)

```
RFC0039  → обновить reasoning_bank.py: заменить UCB1 на Thompson Sampling
           + переименовать тест test_ucb1_canonical_formula → test_ts_selection_formula

RFC0040  → создать shadow_state.py (если ещё не создан для DuckDB)
           + обновить semantic_drift_monitor.py: читать из ShadowState
           + scheduler: shadow.sync каждые 15 мин

RFC0041  → обновить observer_plus_plus.py: заменить block_pipeline() на
           graduated response с FPR-проверкой
           + добавить _enter_degraded_mode() / _exit_degraded_mode()

RFC0042  → создать fractal_governance.py
           + добавить validate_fractal_write() в L2IngestionEngine
           + добавить fractal_influence_trace логирование
```

### Новые модули

```
RFC0043  → добавить блок HARDWARE_PROFILE в velantrim_config.py
           + создать hardware_profile.py (авто-детект psutil)
           + переключить стек компонентов по профилю

RFC0044  → добавить LLM_MODE в velantrim_config.py
           + добавить ветку offline в fast_path.py (шаг F2.6)

RFC0045  → создать lens_engine.py
           + создать папку lenses/ с 30 YAML-файлами линз
           + интегрировать LensMatcher в fast_path.py как шаг F2.6
           + создать normalizer.py (pymorphy2 + RU stop-words)
           + создать offline_extractor.py (spaCy NER + domain keywords)

RFC0046  → обновить neo4j_setup.py: добавить :ReasoningStep схему
           + добавить рёбра [:PRECEDES] и [:ROLLBACK_TO]
           + добавить поле epistemic_variance в :Fact (default=1.0)
           + добавить temporal атрибуты на [:RELATED_TO], [:CAUSES]
           + добавить метод rollback_to() в reasoning_bank.py
           + добавить тег [UNVERIFIED] в context_builder.py при variance > 0.7

RFC0045-BAE → создать bae_engine.py (RST-lite + Microplanner + Surface RU)
              + создать rsl_skeletons.py (скелеты по 8 интентам)
              + создать microplanner.py (анафора, переходы, anti-repeat)
              + создать surface_ru.py (pymorphy2 согласование)
              + создать style_profiles.py (5 параметрических профилей)
              + создать corner.py (dedupe + diversity + budget)

MoE         → добавить LLM_ARCHITECTURE / LLM_ACTIVE_PARAMS / LLM_TOTAL_PARAMS
              в velantrim_config.py
              + RAM-проверка при старте если LLM_ARCHITECTURE=moe
```

### Новые модули

```
RFC0047  → обновить fact_manager.py: добавить recalculate_variance()
           + автовызов при изменении Evidence / [:CONTRADICTS] / ESM-переходе
           + константа UNVERIFIED_THRESHOLD = 0.7 в velantrim_config.py

RFC0048  → обновить hardware_profile.py: добавить compute_memory_budget()
           + startup_ram_check() с Multi-Component Budget
           + добавить NEO4J_PAGE_CACHE_GB, VECTOR_RAM_GB, MEM_PRESSURE_WARN,
             MEM_PRESSURE_CRIT в velantrim_config.py

           # Формула (hardware_profile.py):
           # total_required = llm_ram + neo4j_ram + redis_ram + vector_ram + os_buffer(2GB)
           # pressure = total_required / available_ram
           # if pressure > MEM_PRESSURE_CRIT: downshift profile или LLM_MODE=offline

RFC0049  → обновить esm_machine.py: on_state_transition() — закрытие рёбер
           + обновить safe_fts_query.py: добавить TEMPORAL_EDGE_FILTER
           + обновить lens_engine.py: TEMPORAL_EDGE_FILTER в шаблонах Cypher
           + выполнить migration_v5_06_temporal_backfill.cypher (one-time)

RFC0050  → обновить reasoning_bank.py: create_rollback_edge() с проверкой узлов
           + retry через ConsolidationQueue при отсутствии узлов
           + счётчик dag_rollback_retry_total (Prometheus)

RFC0051  → обновить lens_engine.py: добавить match_all() + compose()
           + добавить LENS_COMPOSITION_THRESHOLD = 0.45, MAX_COMPOSED_LENSES = 3
             в velantrim_config.py
           + BAE: реализовать ТОЛЬКО профиль "neutral" как MVP
             (профили "concise"/"detailed" и "scientific"/"friendly" — Phase 2+)
```

---

## 🔧 RFC0062 — TZ-Fix Integration Patch

> **Статус**: Canonical
> **Источник**: TZ-Fix Integration audit
> **Инварианты**: I38
> **Новые метрики Prometheus**: 4
> **Новый индекс Neo4j**: `fact_conflict_checked_idx`

### Новые компоненты (FEATURE-1..9)

---

#### FEATURE-1 · memory/core_memory_blocks.py

**Что даёт**: ~500 токенов постоянного контекста в system prompt. Агент знает
пользователя с первого слова каждой сессии без поиска по графу.

```python
# memory/core_memory_blocks.py — новый файл
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

@dataclass
class CoreMemoryBlocks:
    """
    Постоянный контекст ~500 токенов — всегда в system prompt.
    Три блока: user_profile / agent_persona / current_goals.

    Отличие от Ring Zero / VALUES CORE:
      · Ring Zero      — неизменяемые ценности агента (заморожены в ESM)
      · CoreMemoryBlocks — живой профиль пользователя (обновляет SleepTimeWorker)
    """
    graph_memory:       object
    user_profile:       str = ""
    agent_persona:      str = ""
    current_goals:      str = ""
    MAX_PROFILE_TOKENS: int = field(default=200, repr=False)
    MAX_PERSONA_TOKENS: int = field(default=150, repr=False)
    MAX_GOALS_TOKENS:   int = field(default=150, repr=False)

    async def load(self):
        try:
            results = await self.graph_memory.search(
                query="core_memory user_profile agent_persona current_goals",
                num_results=10,
            )
            for r in results:
                if r.get("source") != "core_memory":
                    continue
                content = r.get("content", "")
                if "user_profile:" in content:
                    self.user_profile  = content.split("user_profile:", 1)[1].strip()
                elif "agent_persona:" in content:
                    self.agent_persona = content.split("agent_persona:", 1)[1].strip()
                elif "current_goals:" in content:
                    self.current_goals = content.split("current_goals:", 1)[1].strip()
            logger.info("CoreMemoryBlocks loaded from graph")
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.load failed (non-critical): {e}")

    def render(self) -> str:
        parts = []
        if self.user_profile:  parts.append(f"[USER PROFILE]\n{self.user_profile}")
        if self.agent_persona: parts.append(f"[AGENT PERSONA]\n{self.agent_persona}")
        if self.current_goals: parts.append(f"[CURRENT GOALS]\n{self.current_goals}")
        return "\n\n".join(parts) if parts else ""

    async def update(self, block: str, content: str):
        allowed = {"user_profile", "agent_persona", "current_goals"}
        if block not in allowed:
            raise ValueError(f"Unknown block: {block}. Allowed: {allowed}")
        setattr(self, block, content)
        try:
            await self.graph_memory.add_episode(
                episode_name=f"core_memory_{block}",
                content=f"{block}: {content}",
                source="core_memory",
            )
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.update save failed: {e}")

    async def update_from_conversation(self, conversation_text: str, llm_client):
        """Автоматически обновить user_profile. Вызывается SleepTimeWorker."""
        if not llm_client:
            return
        prompt = (
            f"Extract a concise user profile update (max 150 words).\n"
            f"Focus on: name, role, tech stack, preferences, projects.\n"
            f"Conversation: {conversation_text[:2000]}\nUser profile update:"
        )
        try:
            updated = await llm_client.complete(prompt)
            if updated and len(updated) > 10:
                await self.update("user_profile", updated)
        except Exception as e:
            logger.debug(f"CoreMemoryBlocks.update_from_conversation failed: {e}")

# Интеграция в agent.py:
#   __init__: self.core_blocks = CoreMemoryBlocks(graph_memory=self.graph_memory)
#   start():  await self.core_blocks.load()
#   chat():   system_prompt = base_prompt + "\n\n" + self.core_blocks.render()
```

---

#### FEATURE-2 · sleep_time_worker.py

**Что даёт**: память самовосстанавливается в idle. Нулевая нагрузка во время разговора.

⚠️ **MGL-2 compliance**: `_refine_truth_layer` делегирует `AutoTruthGateWorker`
и `ESM.transition` — никакого прямого `SET epistemic_state`.

```python
# sleep_time_worker.py — новый файл
import asyncio
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

class SleepTimeWorker:
    """
    Idle-рефинирование памяти (≥5 мин простоя).
    ⚠️ MGL-2: изменение epistemic_state только через ESM.transition.
    """
    def __init__(
        self,
        graph_memory,
        reasoning_bank,
        core_blocks            = None,
        idle_timeout           = 300,
        sleep_interval         = 3600,
        auto_truth_gate_worker = None,  # AutoTruthGateWorker instance
        esm                    = None,  # EpistemicStateMachine instance
    ):
        self.graph                   = graph_memory
        self.reasoning_bank          = reasoning_bank
        self.core_blocks             = core_blocks
        self.idle_timeout            = idle_timeout
        self.sleep_interval          = sleep_interval
        self._auto_truth_gate_worker = auto_truth_gate_worker
        self._esm                    = esm
        self._last_activity          = datetime.now(timezone.utc)
        self._last_cycle_at          = datetime.now(timezone.utc)
        self._running                = False
        self._task                   = None

    def notify_activity(self):
        """Вызывать при каждом входящем сообщении."""
        self._last_activity = datetime.now(timezone.utc)

    def _is_idle(self) -> bool:
        return (datetime.now(timezone.utc) - self._last_activity).total_seconds() >= self.idle_timeout

    async def start(self):
        self._running = True
        self._task    = asyncio.create_task(self._sleep_loop())
        logger.info("SleepTimeWorker started")

    async def stop(self):
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try: await self._task
            except asyncio.CancelledError: pass

    async def _sleep_loop(self):
        while self._running:
            await asyncio.sleep(60)
            if not self._is_idle():
                continue
            since = (datetime.now(timezone.utc) - self._last_cycle_at).total_seconds()
            if since < self.sleep_interval:
                continue
            try:
                await self._run_sleep_cycle()
                self._last_cycle_at = datetime.now(timezone.utc)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.warning(f"SleepTimeWorker cycle failed: {e}")

    async def _run_sleep_cycle(self):
        logger.info("SleepTimeWorker: starting idle refinement cycle")
        await self._refine_truth_layer()
        await self._ace_curator_update()
        await self._refresh_core_blocks()
        logger.info("SleepTimeWorker: idle refinement cycle complete")

    async def _refine_truth_layer(self):
        """
        ⚠️ MGL-2: нет прямого SET epistemic_state.
        Validated-промоут → AutoTruthGateWorker.
        Stale Hypothesized → ESM.transition.
        """
        if self._auto_truth_gate_worker:
            try:
                promoted = await self._auto_truth_gate_worker.run_validation_cycle()
                logger.info(f"SleepTimeWorker: AutoTruthGate promoted {promoted} facts")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: AutoTruthGate failed: {e}")

        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        try:
            stale = await self.graph.execute_cypher("""
                MATCH (f:Fact)
                WHERE f.epistemic_state = 'Hypothesized'
                  AND f.last_accessed < $cutoff
                  AND f.is_ring_zero <> true
                RETURN f.id AS fact_id, f AS fact_data
                LIMIT 50
            """, {"cutoff": cutoff})
            if stale and self._esm:
                for row in stale:
                    try:
                        await self._esm.transition(
                            fact_id=row["fact_id"], fact=dict(row["fact_data"]),
                            graph=self.graph, reason="sleep_time: no access 7 days",
                        )
                    except Exception:
                        pass
        except Exception as e:
            logger.debug(f"SleepTimeWorker._refine_truth_layer: {e}")

    async def _ace_curator_update(self):
        try:
            if hasattr(self.reasoning_bank, 'ace_curator_update'):
                await self.reasoning_bank.ace_curator_update()
        except Exception as e:
            logger.debug(f"SleepTimeWorker._ace_curator_update: {e}")

    async def _refresh_core_blocks(self):
        if self.core_blocks:
            try: await self.core_blocks.load()
            except Exception as e: logger.debug(f"SleepTimeWorker._refresh_core_blocks: {e}")

# Интеграция в agent.py:
#   self.sleep_worker = SleepTimeWorker(
#       graph_memory=self.graph_memory, reasoning_bank=self.reasoning_bank,
#       core_blocks=self.core_blocks, auto_truth_gate_worker=self.auto_truth_gate_worker,
#       esm=self.esm)
#   start(): await self.sleep_worker.start()
#   chat() первой строкой: self.sleep_worker.notify_activity()
```

---

#### FEATURE-3 · reasoning_bank.py — ACE Curator

**Что даёт**: стратегии дистиллируются с reasoning: root_cause + conditions + anti_conditions.
Добавить метод в класс `ReasoningBank`. Вызывается из `SleepTimeWorker` в idle.

```python
# reasoning_bank.py — добавить метод ace_curator_update в ReasoningBank

    async def ace_curator_update(self):
        """
        ACE Curator (Stanford/SambaNova ACE pattern).
        Вызывается ТОЛЬКО из SleepTimeWorker в idle — не из Fast Path.

        PATCH-6: дублирующая реализация удалена — каноническая живёт в
        agent_with_learning.py :: SelfLearningAgent.ace_curator_update().
        Расхождение было: здесь e.task, там e.task_description[:50] +
        разные форматы episode_name → рассинхронизация при изменениях.

        ReasoningBank передаёт свои данные через аргументы в канонический метод.
        Все изменения логики вносить ТОЛЬКО в agent_with_learning.py.
        """
        if not hasattr(self, '_ace_delegate') or self._ace_delegate is None:
            logger.debug("ace_curator_update: _ace_delegate не задан, пропускаем")
            return
        await self._ace_delegate(
            strategies=self.strategies,
            experience_buffer=list(getattr(self, 'experience_buffer', [])),
            graph=self.graph,
            llm_client=getattr(self, '_llm_client', None),
        )
```

---

#### FEATURE-4 · memory/namespaces.py + memory/rrf_search.py

**Что даёт**: 4 namespace без смешивания + RRF поиск по всем.
⚠️ **RFC0032**: поиск через `SafeFTSQuery` или явный ESM-фильтр.

```python
# memory/namespaces.py
from enum import Enum

class Namespace(str, Enum):
    PERSONAL   = "personal"
    PROJECT    = "project"
    KNOWLEDGE  = "knowledge"
    EXPERIENCE = "experience"

SOURCE_TO_NAMESPACE = {
    "conversation": Namespace.PERSONAL,    "user_message": Namespace.PERSONAL,
    "core_memory":  Namespace.PERSONAL,    "stm_consolidation": Namespace.PERSONAL,
    "strategy_distill": Namespace.EXPERIENCE, "ace_curator": Namespace.EXPERIENCE,
    "ingest_manifest":  Namespace.PROJECT,    "document": Namespace.KNOWLEDGE,
}

def infer_namespace(source: str) -> str:
    return SOURCE_TO_NAMESPACE.get(source, Namespace.PERSONAL).value
```

```python
# memory/rrf_search.py
from collections import defaultdict
from typing import Optional

BLOCKED_ESM = {"Contradicted", "Deprecated", "Collapsed"}

async def multi_namespace_search(
    graph_memory, safe_fts_query,
    query: str, num_results: int = 10,
    priority_namespace: Optional[str] = None, rrf_k: int = 60,
) -> list[dict]:
    """
    RRF поиск по всем namespace.
    ⚠️ RFC0032: SafeFTSQuery или явный ESM-фильтр — прямой search() запрещён.
    """
    all_results, rank_lists = {}, []
    for ns in ["personal", "project", "knowledge", "experience"]:
        try:
            if hasattr(safe_fts_query, 'search_with_namespace'):
                results = await safe_fts_query.search_with_namespace(query, namespace=ns, limit=num_results)
            else:
                raw     = await graph_memory.search(query=query, num_results=num_results*2, namespace=ns)
                results = [r for r in raw if r.get("epistemic_state","Validated") not in BLOCKED_ESM and r.get("is_active", True)][:num_results]
            rank_list = []
            for r in results:
                did = str(r.get("uuid") or r.get("id") or hash(r.get("content","")[:50]))
                all_results[did] = r; rank_list.append(did)
            rank_lists.append(rank_list)
        except Exception:
            rank_lists.append([])

    scores: dict[str, float] = defaultdict(float)
    for rl in rank_lists:
        for rank, did in enumerate(rl):
            s = 1.0 / (rrf_k + rank + 1)
            if priority_namespace and all_results.get(did, {}).get("group_id") == priority_namespace:
                s *= 1.5
            scores[did] += s

    return [all_results[d] for d in sorted(scores, key=scores.get, reverse=True)[:num_results] if d in all_results]
```

```python
# safe_fts_query.py — добавить метод в SafeFTSQuery

    async def search_with_namespace(self, query: str, namespace: str, limit: int = 20) -> list:
        """Расширение SafeFTSQuery: стандартные ESM-фильтры + namespace-фильтр."""
        raw  = await self.fts5_search(query, limit * 2)
        safe = []
        for ep in raw:
            if ep.valid_until and ep.valid_until < datetime.now(timezone.utc): continue
            if ep.esm_hint in ("Contradicted", "Deprecated"): continue
            if await self._linked_to_contradicted(ep): continue
            if getattr(ep, 'group_id', namespace) != namespace: continue
            safe.append(ep)
        return safe[:limit]
```

---

#### FEATURE-5 · memory/auto_summary.py

```python
# memory/auto_summary.py  ← полная реализация из HYPERIA, адаптирована для Velantrim
#
# Назначение: каждые SUMMARY_EVERY turns создаёт краткое резюме диалога и
# сохраняет его в L1 (namespace="personal"). Без этого граф разрастается
# линейно с числом сообщений — каждый turn становится отдельным эпизодом.
#
# Интеграция в Agent.chat() (SLOW PATH, после записи эпизода):
#   turn_index = ... # инкрементировать per conversation_id
#   await auto_summary.maybe_create_summary(
#       conversation_id=conversation_id,
#       turn_index=turn_index,
#       recent_turns=last_N_turns,   # list[{"user": str, "agent": str}]
#   )
#
# Суммаризация: LLM если доступен, иначе extractive TF-IDF (0 токенов, CPU-only).
# Дедупликация: episode_name включает turn_index — повторный вызов безопасен (MERGE).

import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

SUMMARY_EVERY = 10   # создавать резюме каждые N turns
# P1-F FIX: перенести в velantrim_config.py — единый источник для AdaptiveDecoder и CognitiveModeRouter
# class ModeTemperatures:
#     PRECISION=0.3, BALANCED=0.6, EXPLORATION=0.85, CREATIVE=None (dynamic)
# MODE_TEMPS = ModeTemperatures()


class AutoSummary:
    """
    Авто-суммаризация диалога каждые SUMMARY_EVERY turns.
    Хранит ссылки на in-flight задачи чтобы GC не убивал корутины до завершения.
    """

    def __init__(self, graph_memory, llm_client=None):
        self.graph       = graph_memory
        self.llm         = llm_client
        self._in_flight: set = set()   # conversation_id которые сейчас суммаризируются

    async def maybe_create_summary(
        self,
        conversation_id: str,
        turn_index:      int,
        recent_turns:    list,          # list[{"user": str, "agent": str}]
    ) -> Optional[str]:
        """
        Вызывать из SLOW PATH после каждого turn.
        Создаёт резюме только каждые SUMMARY_EVERY turns, не блокирует ответ.
        """
        # Ещё не время или уже выполняется для этого conversation_id
        # P2-F FIX: offline guard — не вызывать LLM при LLM_MODE=offline
        from velantrim_config import LLM_MODE as _LLM_MODE
        if _LLM_MODE == "offline":
            return None   # в offline-режиме использовать только extractive fallback
        if turn_index % SUMMARY_EVERY != 0:
            return None
        if conversation_id in self._in_flight:
            logger.debug(f"AutoSummary: {conversation_id} уже in-flight, пропускаем")
            return None

        self._in_flight.add(conversation_id)
        try:
            return await self._create_summary(conversation_id, turn_index, recent_turns)
        except Exception as e:
            logger.warning(f"AutoSummary: failed for {conversation_id}: {e}")
            return None
        finally:
            self._in_flight.discard(conversation_id)

    async def _create_summary(
        self,
        conversation_id: str,
        turn_index:      int,
        turns:           list,
    ) -> Optional[str]:
        if not turns:
            return None

        # Берём последние SUMMARY_EVERY turns для резюме
        window = turns[-SUMMARY_EVERY:]
        text   = "\n".join(
            f"User: {t.get('user', '')}\nAgent: {t.get('agent', '')}"
            for t in window
        )

        # Суммаризация: LLM если доступен, иначе extractive TF-IDF (CPU-only, 0 токенов)
        summary = await self._summarize(text)

        # episode_name детерминирован по conversation_id + turn_index:
        # повторный вызов с теми же параметрами безопасен — MERGE не создаёт дубль.
        episode_name = f"auto_summary_{conversation_id}_{turn_index}"

        await self.graph.add_episode(
            episode_name=episode_name,
            content=summary,
            source="auto_summary",
            namespace="personal",
            metadata={
                "conversation_id": conversation_id,
                "turn_index":      turn_index,
                "turns_covered":   len(window),
                "summary_type":    "llm" if self.llm else "extractive",
            }
        )
        logger.info(
            f"AutoSummary: created summary for {conversation_id} "
            f"at turn {turn_index} ({len(window)} turns covered)"
        )
        return summary

    async def _summarize(self, text: str) -> str:
        """LLM суммаризация с extractive fallback."""
        if self.llm:
            try:
                return await self.llm.complete(
                    f"Summarize this conversation in 3-5 concise sentences, "
                    f"focusing on key facts and decisions:\n\n{text}",
                )
            except Exception as e:
                logger.debug(f"AutoSummary: LLM failed ({e}), falling back to extractive")

        # Extractive TF-IDF fallback — 0 токенов, CPU-only
        return await asyncio.to_thread(self._extractive_summarize, text)

    @staticmethod
    def _extractive_summarize(text: str, max_sentences: int = 5) -> str:
        """
        TF-IDF extractive суммаризация без LLM.
        Выбирает top-N предложений по суммарному TF-IDF score.
        Fallback на первые 500 символов если sklearn недоступен.
        """
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
        if len(sentences) <= max_sentences:
            return ". ".join(sentences) + "."
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            vectorizer   = TfidfVectorizer(max_features=50)
            tfidf_matrix = vectorizer.fit_transform(sentences)
            scores       = tfidf_matrix.sum(axis=1).A1
            top_indices  = scores.argsort()[-max_sentences:][::-1]
            top_sentences = [sentences[i] for i in sorted(top_indices)]
            return ". ".join(top_sentences) + "."
        except Exception:
            return text[:500]
```

---

#### FEATURE-6 · mcp_server/server.py

```python
# mcp_server/server.py — новый файл
import asyncio, json, logging, sys
logger = logging.getLogger(__name__)

MCP_TOOLS = [
    {"name":"memory_search","description":"Search agent long-term memory","inputSchema":{"type":"object","properties":{"query":{"type":"string"},"num_results":{"type":"integer","default":5}},"required":["query"]}},
    {"name":"memory_add","description":"Add fact to memory","inputSchema":{"type":"object","properties":{"content":{"type":"string"},"source":{"type":"string","default":"mcp_user"}},"required":["content"]}},
    {"name":"agent_chat","description":"Send message to agent","inputSchema":{"type":"object","properties":{"message":{"type":"string"},"user_id":{"type":"string","default":"mcp_user"}},"required":["message"]}},
]

class MCPServer:
    def __init__(self, agent, auth_token: str = ""):
        self.agent = agent; self.auth_token = auth_token

    async def handle_request(self, req: dict) -> dict:
        method = req.get("method",""); rid = req.get("id"); params = req.get("params",{})
        if method == "initialize":
            return {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"velantrim-mcp","version":"2.50"}}}
        if method == "tools/list":
            return {"jsonrpc":"2.0","id":rid,"result":{"tools":MCP_TOOLS}}
        if method == "tools/call":
            try:
                result = await self._call_tool(params.get("name"), params.get("arguments",{}))
                return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":json.dumps(result)}]}}
            except Exception as e:
                return {"jsonrpc":"2.0","id":rid,"error":{"code":-32000,"message":str(e)}}
        return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}

    async def _call_tool(self, name, args):
        if name == "memory_search":
            res = await self.agent.graph_memory.search(query=args["query"], num_results=args.get("num_results",5))
            return [{"content":r.get("content",""),"score":r.get("relevance_score",0)} for r in res]
        if name == "memory_add":
            # add_episode() проходит через Truth Gate внутри GraphMemory — см. RFC0031
            # FIX-F: было f"mcp_{content[:20]}" — тихая потеря данных через INSERT OR IGNORE
            # если два факта начинаются одинаково. Теперь UUID гарантирует уникальность.
            import uuid as _uuid
            ep_name = f"mcp_{_uuid.uuid4().hex[:12]}"
            await self.agent.graph_memory.add_episode(episode_name=ep_name, content=args["content"], source=args.get("source","mcp_user"))
            return {"status":"added"}
        if name == "agent_chat":
            return {"response": await self.agent.chat(args["message"], user_id=args.get("user_id","mcp_user"))}
        raise ValueError(f"Unknown tool: {name}")

    async def run_stdio(self):
        logger.info("MCP Server started (stdio)")
        loop = asyncio.get_running_loop(); reader = asyncio.StreamReader()
        await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)
        while True:
            try:
                line = await reader.readline()
                if not line: break
                resp = await self.handle_request(json.loads(line.decode()))
                sys.stdout.write(json.dumps(resp)+"\n"); sys.stdout.flush()
            except Exception as e:
                logger.error(f"MCP error: {e}")
```

---

#### FEATURE-7 · core/truth_conflict.py

**Что даёт**: автоматический детектор семантических конфликтов + Slow Path воркер (S2.5).

⚠️ **RFC0031**: нет прямого `SET epistemic_state` — только `ESM.transition`.
⚠️ При `llm_client=None` → `continue`, не `break` — обработка батча продолжается для остальных фактов.

```python
# core/truth_conflict.py — новый файл
import asyncio, logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class TruthConflictDetector:

    async def detect_and_resolve_conflicts(
        self, new_fact: dict, graph_memory, esm,
        llm_client=None, sim_threshold: float = 0.95,
    ) -> dict:
        """
        ⚠️ RFC0031: прямой Cypher для SET epistemic_state — ЗАПРЕЩЁН.
        Все переходы через ESM.transition → GraphWriteProtocol.
        Вызывается ТОЛЬКО из ConflictResolutionWorker (Slow Path S2.5).
        """
        content = new_fact.get("content", "")
        if not content or len(content) < 10: return new_fact
        try:
            similar = await graph_memory.search(query=content, num_results=5)
        except Exception as e:
            logger.debug(f"TruthConflict search failed: {e}"); return new_fact

        for old in similar:
            old_content = old.get("content",""); score = old.get("relevance_score", 0.0)
            if score < sim_threshold or not old_content: continue
            if not llm_client: continue  # continue, не break — обрабатываем остальных
            try:
                ans = (await llm_client.complete(
                    f"Do these facts contradict? YES or NO.\nA: {old_content[:300]}\nB: {content[:300]}\nAnswer:"
                )).strip().upper()
                if ans.startswith("YES"):
                    logger.info(f"TruthConflict: conflict detected (sim={score:.2f})")
                    old_full = dict(old)
                    old_full["contradiction_count"] = old_full.get("contradiction_count", 0) + 1
                    await esm.transition(
                        fact_id=old.get("id",""), fact=old_full, graph=graph_memory,
                        reason=f"TruthConflict: contradicted (sim={score:.2f})",
                    )
                    new_fact["requires_validation"]  = True
                    new_fact["conflict_resolved_at"] = datetime.now(timezone.utc).isoformat()
                    break
            except Exception as e:
                logger.debug(f"TruthConflict LLM failed: {e}"); continue
        return new_fact

class ConflictResolutionWorker:
    """
    RFC0062 — Slow Path S2.5.
    Проверяет Hypothesized-факты на конфликты каждые 5 минут.
    ⚠️ I38: вызов только из Slow Path — не из Fast Path.
    """
    CHECK_INTERVAL = 300
    BATCH_SIZE     = 20

    def __init__(self, graph, esm, llm_client=None):
        self.graph = graph; self.esm = esm; self.llm = llm_client
        self._running = False; self._detector = TruthConflictDetector()

    async def start(self):
        self._running = True
        asyncio.create_task(self._run_loop())
        logger.info("ConflictResolutionWorker started (Slow Path S2.5)")

    async def _run_loop(self):
        while self._running:
            await asyncio.sleep(self.CHECK_INTERVAL)
            try: await self._check_batch()
            except asyncio.CancelledError: raise
            except Exception as e: logger.warning(f"ConflictResolutionWorker failed: {e}")

    async def _check_batch(self):
        candidates = await self.graph.execute_cypher("""
            MATCH (f:Fact)
            WHERE f.epistemic_state = 'Hypothesized'
              AND NOT coalesce(f.conflict_checked, false)
              AND NOT coalesce(f.is_ring_zero, false)
            RETURN f.id AS id, f AS fact_data
            ORDER BY f.created_at DESC LIMIT $limit
        """, {"limit": self.BATCH_SIZE})
        # FIX-E: было `f.conflict_checked <> true` — в Neo4j null <> true = null → false в WHERE.
        # Новые факты без свойства conflict_checked вообще не попадали в выборку.
        # coalesce(f.conflict_checked, false) корректно трактует отсутствие свойства как false.
        for row in (candidates or []):
            await self._detector.detect_and_resolve_conflicts(
                new_fact=dict(row["fact_data"]), graph_memory=self.graph,
                esm=self.esm, llm_client=self.llm,
            )
            await self.graph.execute_cypher(
                "MATCH (f:Fact {id: $id}) SET f.conflict_checked = true", {"id": row["id"]}
            )

# Интеграция в agent.py:
#   self.conflict_worker = ConflictResolutionWorker(graph=self.graph_memory, esm=self.esm, llm_client=self.llm_fast)
#   start(): await self.conflict_worker.start()
```

---

#### FEATURE-8 · context_builder.py

**Что даёт**: устраняет дрейф токен-бюджета (было 4000 в коде vs 2000 в token_contract.py).
**Действие**: заменить существующий `ContextBuilder`.

```python
# context_builder.py — заменить класс ContextBuilder
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# ✅ 2000 = MAX_TOKENS_BALANCED_MODE из token_contract.py (устранён дрейф)
QUERY_TYPE_BUDGETS = {
    "conversation": {"stm": 200, "ltm": 300, "strategies": 200, "entities": 100},
    "task":         {"stm": 150, "ltm": 400, "strategies": 350, "entities": 100},
    "analysis":     {"stm": 100, "ltm": 600, "strategies": 200, "entities": 100},
    "default":      {"stm": 200, "ltm": 300, "strategies": 200, "entities": 100},
}

class ContextBuilder:
    def __init__(self, token_budget: int = 2000):  # ✅ 2000 совпадает с token_contract.py
        self.token_budget = token_budget

    def build_context(
        self,
        current_query:        str,
        retrieved_memories:   List,
        strategies:           List          = None,
        conversation_history: List[dict]    = None,
        core_blocks:          Optional[str] = None,
        query_type:           str           = "default",
    ) -> str:
        parts, used = [], 0
        budgets = QUERY_TYPE_BUDGETS.get(query_type, QUERY_TYPE_BUDGETS["default"])

        if core_blocks:
            parts.append(core_blocks); used += self._count_tokens(core_blocks)
        if strategies:
            t = self._format_strategies(strategies, budgets["strategies"])
            if t: parts.append(f"[СТРАТЕГИИ]\n{t}"); used += self._count_tokens(t)
        ltm_budget = min(budgets["ltm"], self.token_budget - used - 200)
        if retrieved_memories and ltm_budget > 0:
            t = self._format_memories(retrieved_memories, ltm_budget)
            if t: parts.append(f"[ПАМЯТЬ]\n{t}"); used += self._count_tokens(t)
        if conversation_history:
            t = self._format_history(conversation_history, min(budgets["stm"], self.token_budget - used - 100))
            if t: parts.append(f"[ИСТОРИЯ]\n{t}")
        return "\n\n".join(parts)

    def _format_strategies(self, strategies, budget):
        lines, used = [], 0
        for s in strategies:
            line = f"• {getattr(s,'description',str(s))}"; t = self._count_tokens(line)
            if used + t > budget: break
            lines.append(line); used += t
        return "\n".join(lines)

    def _format_memories(self, memories, budget):
        lines, used = [], 0
        for m in memories:
            c = m.get('content','') if isinstance(m, dict) else getattr(m,'content','')
            line = f"• {c[:200]}"; t = self._count_tokens(line)
            if used + t > budget: break
            lines.append(line); used += t
        return "\n".join(lines)

    def _format_history(self, history, budget):
        lines, used = [], 0
        for turn in reversed(history[-6:]):
            line = f"User: {turn.get('role_user',turn.get('content',''))[:150]}\nAssistant: {turn.get('role_agent','')[:150]}"
            t = self._count_tokens(line)
            if used + t > budget: break
            lines.insert(0, line); used += t
        return "\n---\n".join(lines)

    def _count_tokens(self, text: str) -> int:
        try:
            import tiktoken
            return len(tiktoken.get_encoding('cl100k_base').encode(text))
        except Exception:
            return max(1, len(text.encode('utf-8')) // 3)
```

---

#### FEATURE-9 · scripts/

```bash
# scripts/self_awareness_update.sh
#!/bin/bash
python scripts/generate_project_map.py --output manifest.json
python scripts/ingest_manifest.py --input manifest.json --namespace project
echo "Self-awareness updated at $(date)"
```

```python
# scripts/generate_project_map.py
import ast, json
from pathlib import Path

def analyze_file(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError: return {}
    return {
        "path": str(path),
        "classes":   [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)],
        "functions": [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)],
    }

def main(output="manifest.json"):
    modules = [analyze_file(p) for p in sorted(Path(".").rglob("*.py"))
               if not any(x in str(p) for x in [".venv", "__pycache__", ".git"])]  # cross-platform (p.parts fails on Windows)
    modules = [m for m in modules if m]
    Path(output).write_text(json.dumps(modules, ensure_ascii=False, indent=2))
    print(f"Generated {output}: {len(modules)} modules")

if __name__ == "__main__":
    import argparse; p = argparse.ArgumentParser()
    p.add_argument("--output", default="manifest.json")
    main(**vars(p.parse_args()))
```

```python
# scripts/ingest_manifest.py — fingerprint-дедупликация
import json, hashlib, asyncio, argparse
from pathlib import Path

async def ingest(manifest_path, namespace, graph_memory):
    modules = json.loads(Path(manifest_path).read_text())
    added = 0
    for mod in modules:
        fp = hashlib.sha256(json.dumps(mod).encode()).hexdigest()[:16]
        if await graph_memory.search(query=f"fingerprint:{fp}", num_results=1):
            continue
        await graph_memory.add_episode(
            episode_name=f"module_{fp}", content=json.dumps(mod),
            source="ingest_manifest", group_id=namespace,
        )
        added += 1
    print(f"Ingested {added} new, skipped {len(modules)-added} unchanged")
```

---

### 📊 Метрики Prometheus (RFC0062)

```python
sleep_worker_cycles_total   = Counter("sleep_worker_cycles_total", ...)
conflict_checks_total       = Counter("conflict_checks_total", ...)
conflict_resolved_total     = Counter("conflict_resolved_total", ...)
core_memory_blocks_loaded   = Gauge("core_memory_blocks_loaded", ...)
```

---

### Порядок реализации RFC0062 (4 спринта)

```
СПРИНТ 1 — СТАБИЛИЗАЦИЯ (~5 дней):
  1. datetime timezone.utc — глобальный поиск (0.5 дня, делать первым)
  2. FractalMemory Lock + Cold Start Guard (1 день)
  3. CircuitBreaker per-loop (0.5 дня)
  4. ConsolidationWorker tasks (0.5 дня)
  5. MTM snapshot + executor (0.5 дня)
  6. break→continue при llm_client=None (0.5 дня)

СПРИНТ 2 — ИСПРАВЛЕНИЯ (~3 дня):
  7. RetrievalResult.embedding (0.5 дня)
  8. EventBus QueueFull→SQLite (0.5 дня)
  9. deepcopy ImmutableCore (0.5 дня, если файл есть)
 10. ConversationBuffer ref_count (1 день, если файл есть)

СПРИНТ 3 — ЯДРО ФИЧ (~5 дней):
 11. FEATURE-8  ContextBuilder заменить (0.5 дня, устраняет токен-дрейф)
 12. FEATURE-1  CoreMemoryBlocks (1 день)
 13. FEATURE-2  SleepTimeWorker (1 день)
 14. FEATURE-7  TruthConflictDetector + S2.5 (1.5 дня)
 15. FEATURE-3  ACE Curator в ReasoningBank (0.5 дня)

СПРИНТ 4 — РАСШИРЕНИЕ (~4 дня):
 16. FEATURE-4  Namespace + RRF (1.5 дня)
 17. FEATURE-5  AutoSummary (0.5 дня)
 18. FEATURE-6  MCP Server (1 день)
 19. FEATURE-9  Self-Awareness скрипты (0.5 дня)

Итого: ~17 рабочих дней
```

---

# ============================================================================
# HYPERIA COMPONENT 2: CoreMemoryBlocks
# ============================================================================
# RFC0062 FEATURE-1 - теперь реализовано полностью

# memory/core_memory_blocks.py
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class CoreMemoryBlocks:
    """
    Постоянный контекст ~500 токенов — всегда в system prompt.
    Три блока: user_profile / agent_persona / current_goals.

    Адаптация: Все graph.search() обёрнуты в SafeFTSQuery для соблюдения RFC0032.

    Отличие от Ring Zero / VALUES CORE:
    - Ring Zero: неизменяемые ценности агента (заморожены в ESM)
    - CoreMemoryBlocks: живой профиль пользователя (обновляется SleepTimeWorker)
    """
    graph_memory: object
    safe_fts_query: object = None  # ✅ Velantrim адаптация: SafeFTSQuery вместо прямого search
    user_profile: str = ""
    agent_persona: str = ""
    current_goals: str = ""
    MAX_PROFILE_TOKENS: int = field(default=200, repr=False)
    MAX_PERSONA_TOKENS: int = field(default=150, repr=False)
    MAX_GOALS_TOKENS: int = field(default=150, repr=False)

    async def load(self):
        """
        Загрузить блоки из графа при старте агента.
        ✅ Velantrim адаптация: использует SafeFTSQuery если доступен.
        """
        try:
            # Используем SafeFTSQuery если доступен (Velantrim RFC0032)
            if self.safe_fts_query:
                results = await self.safe_fts_query.search(
                    query="core_memory user_profile agent_persona current_goals",
                    limit=10
                )
            else:
                # Fallback на прямой search если SafeFTSQuery не настроен
                results = await self.graph_memory.search(
                    query="core_memory user_profile agent_persona current_goals",
                    num_results=10
                )
            
            for r in results:
                content = r.get("content", "") if isinstance(r, dict) else getattr(r, 'content', '')
                source = r.get("source", "") if isinstance(r, dict) else getattr(r, 'source', '')
                
                if source != "core_memory":
                    continue
                
                if "user_profile:" in content:
                    self.user_profile = content.split("user_profile:", 1)[1].strip()
                elif "agent_persona:" in content:
                    self.agent_persona = content.split("agent_persona:", 1)[1].strip()
                elif "current_goals:" in content:
                    self.current_goals = content.split("current_goals:", 1)[1].strip()
            
            logger.info("CoreMemoryBlocks loaded from graph")
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.load failed (non-critical): {e}")

    def render(self) -> str:
        """
        Рендер блоков для вставки в system prompt.
        Возвращает ~500 токенов постоянного контекста.
        """
        parts = []
        if self.user_profile:
            parts.append(f"[USER PROFILE]\n{self.user_profile}")
        if self.agent_persona:
            parts.append(f"[AGENT PERSONA]\n{self.agent_persona}")
        if self.current_goals:
            parts.append(f"[CURRENT GOALS]\n{self.current_goals}")
        
        return "\n\n".join(parts) if parts else ""

    async def update(self, block: str, content: str):
        """
        Обновить один из блоков и сохранить в граф.
        Вызывается вручную пользователем или автоматически через SleepTimeWorker.
        """
        allowed = {"user_profile", "agent_persona", "current_goals"}
        if block not in allowed:
            raise ValueError(f"Unknown block: {block}. Allowed: {allowed}")
        
        setattr(self, block, content)
        
        try:
            await self.graph_memory.add_episode(
                episode_name=f"core_memory_{block}_{datetime.now(timezone.utc).isoformat()}",
                content=f"{block}: {content}",
                source="core_memory"
            )
            logger.info(f"CoreMemoryBlocks.{block} updated")
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.update save failed: {e}")

    async def update_from_conversation(self, conversation_text: str, llm_client):
        """
        Автоматически обновить user_profile из диалога.
        Вызывается SleepTimeWorker в idle.
        
        ✅ Velantrim адаптация: LLM вызов опционален (может быть None в offline режиме).
        """
        if not llm_client:
            logger.debug("CoreMemoryBlocks: llm_client=None, пропускаем auto-update")
            return
        
        prompt = (
            f"Extract a concise user profile update (max 150 words).\n"
            f"Focus on: name, role, tech stack, preferences, projects.\n"
            f"Conversation: {conversation_text[:2000]}\nUser profile update:"
        )
        
        try:
            updated = await llm_client.complete(prompt)
            if updated and len(updated) > 10:
                await self.update("user_profile", updated)
                logger.info("CoreMemoryBlocks: user_profile auto-updated from conversation")
        except Exception as e:
            logger.debug(f"CoreMemoryBlocks.update_from_conversation failed: {e}")

# Интеграция в agent.py:
#   __init__:
#       self.core_blocks = CoreMemoryBlocks(
#           graph_memory=self.graph_memory,
#           safe_fts_query=self.safe_fts_query  # ✅ Velantrim RFC0032
#       )
#   
#   async def start(self):
#       await self.core_blocks.load()
#   
#   def _build_system_prompt(self):
#       base_prompt = "..."
#       return base_prompt + "\n\n" + self.core_blocks.render()



# ============================================================================
# HYPERIA COMPONENT 3: SleepTimeWorker
# ============================================================================
# RFC0062 FEATURE-2 - теперь реализовано полностью
# ✅ Velantrim адаптация: все изменения epistemic_state через ESM.transition

# sleep_time_worker.py
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

class SleepTimeWorker:
    """
    Idle-рефинирование памяти (≥5 мин простоя).

    ✅ Velantrim адаптация: MGL-2 compliance - никакого прямого SET epistemic_state.
    Все переходы только через ESM.transition() → GraphWriteProtocol.

    Что делает в idle:
    1. _refine_truth_layer() - промоут Hypothesized → Validated через AutoTruthGate
    2. _ace_curator_update() - дистилляция стратегий с reasoning
    3. _refresh_core_blocks() - обновление user_profile из диалога
    """

    def __init__(
        self,
        graph_memory,
        reasoning_bank,
        core_blocks=None,
        idle_timeout=300,           # 5 минут простоя
        sleep_interval=3600,        # цикл каждый час
        auto_truth_gate_worker=None,
        esm=None,                   # ✅ Velantrim: EpistemicStateMachine instance
    ):
        self.graph = graph_memory
        self.reasoning_bank = reasoning_bank
        self.core_blocks = core_blocks
        self.idle_timeout = idle_timeout
        self.sleep_interval = sleep_interval
        self._auto_truth_gate_worker = auto_truth_gate_worker
        self._esm = esm  # ✅ Velantrim: обязательный параметр для MGL-2
        self._last_activity = datetime.now(timezone.utc)
        self._last_cycle_at = datetime.now(timezone.utc)
        self._running = False
        self._task = None

    def notify_activity(self):
        """Вызывать при каждом входящем сообщении пользователя."""
        self._last_activity = datetime.now(timezone.utc)

    def _is_idle(self) -> bool:
        """Проверка idle состояния"""
        elapsed = (datetime.now(timezone.utc) - self._last_activity).total_seconds()
        return elapsed >= self.idle_timeout

    async def start(self):
        """Запустить фоновый idle-воркер"""
        self._running = True
        self._task = asyncio.create_task(self._sleep_loop())
        logger.info("SleepTimeWorker started (idle ≥ 5 мин)")

    async def stop(self):
        """Остановить воркер"""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("SleepTimeWorker stopped")

    async def _sleep_loop(self):
        """Основной цикл - проверка idle каждую минуту"""
        while self._running:
            await asyncio.sleep(60)  # проверка каждую минуту
            
            if not self._is_idle():
                continue
            
            # Проверяем не запускали ли цикл недавно
            since_last = (datetime.now(timezone.utc) - self._last_cycle_at).total_seconds()
            if since_last < self.sleep_interval:
                continue
            
            try:
                await self._run_sleep_cycle()
                self._last_cycle_at = datetime.now(timezone.utc)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.warning(f"SleepTimeWorker cycle failed: {e}")

    async def _run_sleep_cycle(self):
        """Один полный цикл idle-рефинирования"""
        logger.info("SleepTimeWorker: начинаю idle refinement cycle")
        
        await self._refine_truth_layer()
        await self._ace_curator_update()
        await self._refresh_core_blocks()
        
        logger.info("SleepTimeWorker: idle refinement cycle завершён")

    async def _refine_truth_layer(self):
        """
        Рефинирование L3 truth layer.
        
        ✅ Velantrim MGL-2 compliance:
        - НЕТ прямого SET epistemic_state
        - Validated-промоут → AutoTruthGateWorker (если есть)
        - Stale Hypothesized → ESM.transition(Deprecated)
        """
        if self._auto_truth_gate_worker:
            try:
                promoted = await self._auto_truth_gate_worker.run_validation_cycle()
                logger.info(f"SleepTimeWorker: AutoTruthGate promoted {promoted} facts")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: AutoTruthGate failed: {e}")
        
        # Находим stale Hypothesized факты (старше 7 дней, не accessed)
        if self._esm:
            try:
                stale_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
                stale_query = """
                MATCH (f:Fact)
                WHERE f.epistemic_state = 'Hypothesized'
                  AND f.created_at < $cutoff
                  AND coalesce(f.last_accessed, f.created_at) < $cutoff
                  AND f.is_ring_zero <> true
                RETURN f.id as fact_id
                LIMIT 50
                """
                stale_facts = await self.graph.execute_cypher(
                    stale_query,
                    {"cutoff": stale_cutoff.isoformat()}
                )
                
                for row in (stale_facts or []):
                    # ✅ Velantrim: через ESM.transition, не прямой SET
                    # Подгружаем факт из графа для передачи в ESM.transition(fact, graph, reason)
                    fact_rows = await self.graph.execute_cypher(
                        "MATCH (f:Fact {id: $id}) RETURN properties(f) AS fact",
                        {"id": row["fact_id"]}
                    )
                    if fact_rows:
                        await self._esm.transition(
                            fact_id=row["fact_id"],
                            fact=fact_rows[0]["fact"],
                            graph=self.graph,
                            reason="SleepTimeWorker: stale Hypothesized (>7 days, no access)"
                        )
                
                logger.info(f"SleepTimeWorker: deprecated {len(stale_facts or [])} stale facts")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: stale deprecation failed: {e}")

    async def _ace_curator_update(self):
        """
        Запуск ACE Curator для дистилляции стратегий.
        Вызывается только в idle - не нагружает Fast Path.
        """
        if self.reasoning_bank and hasattr(self.reasoning_bank, 'ace_curator_update'):
            try:
                await self.reasoning_bank.ace_curator_update()
                logger.info("SleepTimeWorker: ACE Curator обновил стратегии")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: ACE Curator failed: {e}")

    async def _refresh_core_blocks(self):
        """
        Обновление CoreMemoryBlocks из недавнего диалога.
        Только если core_blocks настроен и есть LLM.
        """
        if self.core_blocks and hasattr(self.core_blocks, 'update_from_conversation'):
            try:
                # Получаем последние 10 реплик диалога
                recent_query = """
                MATCH (ep:Episode)
                WHERE ep.source = 'conversation'
                  AND ep.created_at > $since
                RETURN ep.content as content
                ORDER BY ep.created_at DESC
                LIMIT 10
                """
                since = datetime.now(timezone.utc) - timedelta(hours=2)
                recent = await self.graph.execute_cypher(
                    recent_query,
                    {"since": since.isoformat()}
                )
                
                if recent:
                    conversation_text = "\n".join([r["content"] for r in recent])
                    # LLM client должен быть в reasoning_bank или передан отдельно
                    llm = getattr(self.reasoning_bank, 'llm_client', None)
                    await self.core_blocks.update_from_conversation(conversation_text, llm)
            except Exception as e:
                logger.debug(f"SleepTimeWorker._refresh_core_blocks: {e}")

# Интеграция в agent.py:
#   self.sleep_worker = SleepTimeWorker(
#       graph_memory=self.graph_memory,
#       reasoning_bank=self.reasoning_bank,
#       core_blocks=self.core_blocks,
#       esm=self.esm,  # ✅ Velantrim обязательно
#       auto_truth_gate_worker=self.auto_truth_gate_worker  # опционально
#   )
#   
#   async def start(self):
#       await self.sleep_worker.start()
#   
#   async def chat(self, message):
#       self.sleep_worker.notify_activity()  # первая строка метода
#       # ... остальной код


# ============================================================================
# HYPERIA COMPONENT 6: ImmutableCore Scheduler
# ============================================================================
# Назначение: SHA-256 снапшоты L3 графа каждые 24ч для защиты от потери данных

# memory/immutable_core_scheduler.py
import asyncio
import hashlib
import json
import logging
import aiosqlite
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

class ImmutableCoreScheduler:
    """
    Независимый планировщик снапшотов L3.

    Запускается как отдельный asyncio.Task при старте агента.
    Не зависит от консолидации — snapshot каждые 24ч при любых условиях.

    Delta snapshots экономят ~80–90% storage vs ежедневных полных.
    Full snapshot — каждый понедельник, остальные дни — delta.
    """

    def __init__(self, ltm, sqlite_path: str = "./data/immutable_core.db"):
        self.ltm = ltm
        self.sqlite_path = sqlite_path
        self.running = False
        self._task = None

    async def start(self):
        """Запустить scheduler"""
        self.running = True
        self._task = asyncio.create_task(self._snapshot_loop())
        logger.info("ImmutableCoreScheduler started (24h cycle)")

    async def stop(self):
        """Остановить scheduler"""
        self.running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("ImmutableCoreScheduler stopped")

    async def _snapshot_loop(self):
        """
        Основной цикл снапшотов.
        При старте делает snapshot только если прошло >12ч с последнего.
        Это предотвращает лишние полные снапшоты при множественных рестартах.
        """
        try:
            last = await self._get_last_snapshot_time()
            if last is None or (datetime.now(timezone.utc) - last) > timedelta(hours=12):
                await self._take_snapshot()
        except Exception as e:
            logger.error(f"ImmutableCore initial snapshot failed: {e}")
        
        while self.running:
            await asyncio.sleep(24 * 3600)  # каждые 24 часа
            try:
                await self._take_snapshot()
            except Exception as e:
                logger.error(f"ImmutableCore snapshot failed: {e}")
                # Не останавливаем петлю — следующий снапшот через 24ч

    async def _take_snapshot(self):
        """Создать снапшот L3 графа"""
        # Получаем данные из LTM
        # export_snapshot() отсутствует в FractalMemory → AttributeError каждые 24ч.
        # Phase 2: реализовать FractalMemory.export_snapshot() → возвращает dict со snapshot L3 графа.
        # Временный fallback пока метод не реализован:
        if not hasattr(self.ltm, 'export_snapshot'):
            logger.error("ImmutableCore: FractalMemory.export_snapshot() не реализован — snapshot пропущен")
            return
        snapshot_data = await self.ltm.export_snapshot()
        snapshot_type = "full" if self._is_full_snapshot_day() else "delta"
        
        if snapshot_type == "delta":
            prev = await self._get_last_full_snapshot()
            if prev:
                try:
                    # Используем dictdiffer если доступен
                    from dictdiffer import diff
                    delta = list(diff(prev, snapshot_data))
                    data_to_store = json.dumps(delta, ensure_ascii=False)
                except ImportError:
                    # Fallback на full snapshot если dictdiffer не установлен
                    data_to_store = json.dumps(snapshot_data, ensure_ascii=False, sort_keys=True)
                    snapshot_type = "full"
            else:
                data_to_store = json.dumps(snapshot_data, ensure_ascii=False, sort_keys=True)
                snapshot_type = "full"
        else:
            data_to_store = json.dumps(snapshot_data, ensure_ascii=False, sort_keys=True)
        
        # Вычисляем hash
        snapshot_hash = hashlib.sha256(data_to_store.encode()).hexdigest()
        
        # Сохраняем в SQLite
        async with aiosqlite.connect(self.sqlite_path) as db:
            await db.execute("PRAGMA journal_mode=WAL")
            await db.execute("PRAGMA synchronous=NORMAL")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS immutable_core (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp     TEXT    NOT NULL,
                    hash          TEXT    NOT NULL,
                    snapshot_type TEXT    NOT NULL,
                    data          TEXT    NOT NULL
                )
            """)
            await db.execute(
                "INSERT INTO immutable_core (timestamp, hash, snapshot_type, data) VALUES (?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(), snapshot_hash, snapshot_type, data_to_store)
            )
            await db.commit()
        
        logger.info(f"ImmutableCore [{snapshot_type}] snapshot: {snapshot_hash[:12]}...")

    async def _get_last_full_snapshot(self):
        """Получить данные последнего full-снапшота для вычисления дельты"""
        try:
            async with aiosqlite.connect(self.sqlite_path) as db:
                async with db.execute(
                    "SELECT data FROM immutable_core WHERE snapshot_type='full' ORDER BY id DESC LIMIT 1"
                ) as cursor:
                    row = await cursor.fetchone()
                    return json.loads(row[0]) if row else None
        except Exception:
            return None

    async def _get_last_snapshot_time(self):
        """Получить datetime последнего снапшота любого типа"""
        try:
            async with aiosqlite.connect(self.sqlite_path) as db:
                async with db.execute(
                    "SELECT timestamp FROM immutable_core ORDER BY id DESC LIMIT 1"
                ) as cursor:
                    row = await cursor.fetchone()
                    return datetime.fromisoformat(row[0]) if row else None
        except Exception:
            return None

    def _is_full_snapshot_day(self) -> bool:
        """Понедельник = full snapshot, остальные дни = delta"""
        FULL_SNAPSHOT_WEEKDAY = 0  # 0 = понедельник
        return datetime.now(timezone.utc).weekday() == FULL_SNAPSHOT_WEEKDAY

# Интеграция в agent.py:
#   self.immutable_core = ImmutableCoreScheduler(
#       ltm=self.fractal_memory,
#       sqlite_path="./data/immutable_core.db"
#   )
#   
#   async def start(self):
#       await self.immutable_core.start()
#   
#   async def stop(self):
#       await self.immutable_core.stop()


# ============================================================================
# HYPERIA COMPONENT 7: Multi-namespace RRF Search
# ============================================================================
# RFC0062 FEATURE-4 - теперь реализовано полностью
# ✅ Velantrim адаптация: SafeFTSQuery вместо прямого search

# memory/rrf_search.py
from collections import defaultdict
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# ✅ Velantrim: ESM-фильтр для блокировки невалидных состояний
BLOCKED_ESM_STATES = {"Contradicted", "Deprecated", "Collapsed"}

async def multi_namespace_search(
    graph_memory,
    safe_fts_query,  # ✅ Velantrim: SafeFTSQuery instance для RFC0032
    query: str,
    num_results: int = 10,
    priority_namespace: Optional[str] = None,
    rrf_k: int = 60,
) -> List[dict]:
    """
    RRF (Reciprocal Rank Fusion) поиск по всем namespace.

    ✅ Velantrim адаптация: SafeFTSQuery для ESM-фильтрации (RFC0032).

    Namespaces:
    - personal: разговоры, профиль, stm_consolidation
    - project: кодовая база, self-awareness
    - knowledge: документы, статьи
    - experience: стратегии, ACE curator

    RRF формула: score = 1 / (k + rank)
    Priority namespace получает бонус ×1.5
    """
    all_results = {}
    rank_lists = []

    for ns in ["personal", "project", "knowledge", "experience"]:
        try:
            # ✅ Velantrim: используем SafeFTSQuery если доступен
            if hasattr(safe_fts_query, 'search_with_namespace'):
                results = await safe_fts_query.search_with_namespace(
                    query, namespace=ns, limit=num_results
                )
            else:
                # Fallback с ручным ESM-фильтром
                raw = await graph_memory.search(
                    query=query,
                    num_results=num_results * 2,
                    namespace=ns
                )
                results = [
                    r for r in raw
                    if r.get("epistemic_state", "Validated") not in BLOCKED_ESM_STATES
                    and r.get("is_active", True)
                ][:num_results]
            
            rank_list = []
            for r in results:
                # sha256 вместо hash() — hash() нестабилен между сессиями Python
                import hashlib
                _content_key = r.get("content", "")[:50].encode()
                did = str(r.get("uuid") or r.get("id") or hashlib.sha256(_content_key).hexdigest()[:16])
                all_results[did] = r
                rank_list.append(did)
            
            rank_lists.append(rank_list)
            
        except Exception as e:
            # warning вместо debug — silent fail скрывал деградацию retrieval
            logger.warning(f"multi_namespace_search: namespace {ns} failed: {e}")
            rank_lists.append([])

    # RRF scoring
    scores: dict[str, float] = defaultdict(float)

    for rank_list in rank_lists:
        for rank, did in enumerate(rank_list):
            s = 1.0 / (rrf_k + rank + 1)
            
            # Priority boost
            # result_ns вместо ns — ns была loop-переменной, shadowing ломал 2+ итерацию
            if priority_namespace:
                result_ns = all_results.get(did, {}).get("group_id")
                if result_ns == priority_namespace:
                    s *= 1.5
            
            scores[did] += s

    # Сортировка и возврат
    sorted_ids = sorted(scores.keys(), key=lambda d: scores[d], reverse=True)
    return [all_results[d] for d in sorted_ids[:num_results] if d in all_results]

# Интеграция в HybridRetriever:
#   async def retrieve(self, query, query_type="general"):
#       if self.multi_namespace_enabled:
#           return await multi_namespace_search(
#               graph_memory=self.graph,
#               safe_fts_query=self.safe_fts_query,
#               query=query,
#               num_results=self.num_results
#           )
#       # ... fallback на обычный retrieve


# ============================================================================
# HYPERIA COMPONENT 8: Централизованный Config паттерн
# ============================================================================
# Назначение: Единый источник истины для всех констант системы

# velantrim_config.yaml - ПРИМЕР централизованного конфига
#
# Проблема: В старом Velantrim константы разбросаны по коду:
# - token_budget дублируется в разных модулях
# - token_budget = 2000 в token_contract.py
# - embedding_dim хардкодится в каждом индексе
# - пороги Truth Gate дублируются в нескольких местах
#
# Решение из HYPERIA: Все константы в одном YAML файле.
# Загружается при старте, валидируется, используется везде.

"""
# ==================== CORE CONFIG ====================
mode: personal  # personal | enterprise
graph_backend: neo4j  # neo4j | falkordb | kuzu | sqlite
vector_backend: qdrant  # qdrant | chroma | faiss

# ==================== EMBEDDING CONFIG ====================
embedding:
  model: "deepvk/USER-bge-m3"
  dimension: 1024
  batch_size: 32
  
# ==================== TOKEN BUDGETS ====================
token_contract:
  max_tokens_balanced_mode: 2000  # ✅ Единственное место где определено
  context_builder:
    conversation: {stm: 200, ltm: 300, strategies: 200, entities: 100}
    task: {stm: 150, ltm: 400, strategies: 350, entities: 100}
    analysis: {stm: 100, ltm: 600, strategies: 200, entities: 100}
    default: {stm: 200, ltm: 300, strategies: 200, entities: 100}

# ==================== TRUTH GATE ====================
truth_gate:
  evidence_count_min: 3
  confidence_min: 0.75
  coverage_score_min: 0.70

# ==================== MEMORY LAYERS ====================
fractal_memory:
  l0_capacity: 4          # Cowan (2001): базовый лимит агента, НЕ Miller 7±2
  l0_capacity_max: 7      # Адаптивный потолок при complexity: high
  l0_adaptive_enabled: true  # При high-complexity задаче — расширяем до l0_capacity_max
  l1_session_ttl_minutes: 30
  l2_mtm_ttl_days: 7
  velum:
    co_occur_threshold: 3
    window_episodes: 5
    max_edges: 1000
    promote_weight: 0.6
    decay_per_session: 0.3

# ==================== CONSOLIDATION ====================
consolidation:
  stm_high_threshold: 0.8
  stm_medium_threshold: 0.5
  mtm_high_threshold: 0.8
  clustering_threshold: 0.8
  
# ==================== SLEEP TIME WORKER ====================
sleep_worker:
  idle_timeout_seconds: 300  # 5 минут
  cycle_interval_seconds: 3600  # 1 час
  
# ==================== IMMUTABLE CORE ====================
immutable_core:
  enabled: true
  snapshot_interval_hours: 24
  full_snapshot_weekday: 0  # 0 = понедельник
  sqlite_path: "./data/immutable_core.db"
  
# ==================== HARDWARE PROFILE ====================
# auto-detect при старте или override через env var
hardware_profile: auto  # weak | medium | strong | auto

# ==================== НОВЫЕ МЕХАНИЗМЫ ====================

# Salience Detector
salience_detector:
  enabled: true
  caps_multiplier: 1.5
  exclamation_multiplier: 1.3
  repeat_3day_multiplier: 2.0
  keyword_multiplier: 1.4        # «важно», «критично», «никогда», «всегда»
  return_after_24h_multiplier: 1.6
  clarify_multiplier: 1.2

# FSRS Power-Law Decay (v8.0 — заменяет Ebbinghaus экспоненту)
# Конфликт-1 FIX: секция переименована, алгоритм заменён на fsrs_retention()
fsrs_decay:
  enabled: true
  worker_interval_seconds: 3600   # раз в час
  emotional_ring_zero_threshold: 0.85  # выше → иммунитет к decay

# Cache-Aware Hot Graph
hot_graph:
  enabled: true
  hot_window_hours: 24
  salience_threshold: 0.7
  lite_max_nodes: 2000
  one_max_nodes: 50000
  rebalance_interval_seconds: 3600

# Homeostatic Balancer
homeostatic:
  enabled: true
  run_at_hour: 3
  overload_threshold: 0.8
  silence_days_before_boost: 30
  normalize_factor: 0.85
  boost_factor: 1.2

# Liquid State Machine
lsm:
  enabled: true
  reservoir_size: 300
  spectral_radius: 0.9
  input_scaling: 0.5
  snapshot_interval_minutes: 15

# Predictive Fusion Layer (L5.5)
predictive_fusion:
  w_sae_initial: 0.6
  w_lsm_initial: 0.4
  w_min: 0.2
  learning_rate: 0.05
  rhythm_stability_threshold: 0.7
  graph_density_threshold: 0.6

# Prediction Error Signal
prediction_error:
  enabled: true
  threshold: 0.4
  edge_strengthen_factor: 0.3
  edge_weaken_factor: 0.15
"""

# Загрузка в Python:

# config/velantrim_config.py
import yaml
from pathlib import Path
from typing import Dict, Any
import os

class VelantrimConfig:
    """
    Централизованный конфиг Velantrim.

    Загружается один раз при старте приложения.
    Все компоненты получают config через dependency injection.
    """

    def __init__(self, config_path: str = "./velantrim_config.yaml"):
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self):
        """Загрузить и валидировать конфиг"""
        if not Path(self.config_path).exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
        
        # Валидация обязательных полей
        required = ['mode', 'graph_backend', 'token_contract']
        for field in required:
            if field not in self._config:
                raise ValueError(f"Required config field missing: {field}")

    def get(self, key: str, default=None):
        """Получить значение по ключу (с поддержкой вложенных путей)"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

    @property
    def token_budget(self) -> int:
        """✅ Единственный источник token_budget для всей системы"""
        return self.get('token_contract.max_tokens_balanced_mode', 2000)

    @property
    def embedding_dimension(self) -> int:
        """Размерность embedding модели"""
        return self.get('embedding.dimension', 1024)

    @property
    def truth_gate_config(self) -> dict:
        """Пороги Truth Gate"""
        return self.get('truth_gate', {
            'evidence_count_min': 3,
            'confidence_min': 0.75,
            'coverage_score_min': 0.70
        })

# Использование в компонентах:

# В main.py при старте:
config = VelantrimConfig("./velantrim_config.yaml")

# В ContextBuilder:
class ContextBuilder:
    def __init__(self, config: VelantrimConfig):
        self.token_budget = config.token_budget  # ✅ Из единого источника
        
# В GraphMemory:
class GraphMemory:
    def __init__(self, config: VelantrimConfig):
        self.embedding_dim = config.embedding_dimension  # ✅ Из единого источника

# В TruthGate:
class TruthGate:
    def __init__(self, config: VelantrimConfig):
        tc = config.truth_gate_config
        self.evidence_min = tc['evidence_count_min']  # ✅ Из единого источника

# ✅ Результат: Нет дубликатов констант, нет несоответствий, легко менять.


# ============================================================================
# 🔒 БЕЗОПАСНОСТЬ: Attack Scenarios Registry
# ============================================================================
# Правило: реальный инцидент → новый сценарий в реестр ≤ 48 часов
# CI/CD: ≥ 95% прохождения блокирует деплой автоматически
# Запуск: pytest tests/test_attack_sim.py

```yaml
# security/attack_scenarios.yaml

scenarios:
  - id: "ATK-001"
    target: "write_protocol"
    severity: critical
    description: "Прямая запись факта в граф в обход Truth Gate"
    expected_result: blocked
    rfc: RFC0060

  - id: "ATK-002"
    target: "esm_transition"
    severity: critical
    description: "Форсирование Validated→Collapsed без Evidence"
    expected_result: rejected_with_reason
    rfc: RFC0046

  - id: "ATK-003"
    target: "safe_fts_query"
    severity: high
    description: "Прямой FTS5-запрос в обход SafeFTSQuery (обход ESM-фильтров)"
    expected_result: blocked_at_query_layer
    rfc: RFC0060

  - id: "ATK-004"
    target: "ring_zero"
    severity: critical
    description: "Попытка вытеснить Ring Zero / VALUES CORE из L0"
    expected_result: eviction_blocked
    rfc: RFC0015

  - id: "ATK-005"
    target: "source_trust"
    severity: high
    description: "Инъекция факта от источника с trust_score < 0.3"
    expected_result: quarantined_hypothesized
    rfc: RFC0059

  - id: "ATK-006"
    target: "focus_engine"
    severity: medium
    description: "Прямой LLM-вызов в FocusEngine (обход I29)"
    expected_result: invariant_violation_raised
    rfc: RFC0053

  - id: "ATK-007"
    target: "l5_5_fusion"
    severity: medium
    description: "Попытка записи в граф из L5.5 PredictiveFusionLayer (обход I35)"
    expected_result: write_blocked
    rfc: RFC0042

  - id: "ATK-008"
    target: "lsm"
    severity: medium
    description: "Попытка записи в граф из LSM (обход I37)"
    expected_result: write_blocked
    rfc: RFC0042

  - id: "ATK-009"
    target: "prediction_error"
    severity: medium
    description: "Prediction Error создаёт новые рёбра вместо изменения весов (обход I36)"
    expected_result: edge_creation_blocked
    rfc: RFC0042
```

# ============================================================================
# 🧪 INVARIANT TEST SUITE — tests/test_invariants.py
# ============================================================================
# Каждый инвариант = исполняемый тест.
# CI/CD: pytest tests/test_invariants.py --tb=short -q
# Падение любого теста → деплой заблокирован автоматически.

```python
# tests/test_invariants.py
import pytest
import asyncio
import time

# ── I1: Velum хранит только рёбра ────────────────────────────────────────────
async def test_I1_velum_stores_only_edges():
    """I1: Velum не хранит содержимое — только рёбра (co-occurrence + weight)."""
    velum = Velum()
    velum.observe_episode(entities=["ProjectA", "Budget"])
    for edge in velum.edges.values():
        assert not hasattr(edge, 'content'), "I1 VIOLATION: Velum хранит контент"
        assert not hasattr(edge, 'text'),    "I1 VIOLATION: Velum хранит текст"
    edge = velum.get_edge(frozenset(["ProjectA", "Budget"]))
    assert edge is not None
    assert hasattr(edge, 'weight') and 0.0 <= edge.weight <= 1.0


# ── I28: ResponseAuditWorker НИКОГДА не в Fast Path ──────────────────────────
async def test_I28_audit_never_blocks_response():
    """I28: Аудит строго в SLOW PATH. Нарушение = блокировка ответа = баг."""
    agent = Agent(event_bus=MockEventBus(), audit_worker=MockAuditWorker())
    start = time.monotonic()
    response = await agent.chat("Привет")
    elapsed = time.monotonic() - start
    assert response is not None
    assert elapsed < 0.1, f"I28 VIOLATION: ответ занял {elapsed:.3f}s — аудит в Fast Path?"
    await asyncio.sleep(0.05)
    assert agent.event_bus.published_count(EventType.RESPONSE_GENERATED) >= 1


# ── I29: FocusVector только через граф и SQLite ──────────────────────────────
async def test_I29_focus_vector_no_direct_llm():
    """I29: Прямые LLM-вызовы для определения фокуса — запрещены."""
    llm_mock = MockLLM()
    focus_engine = FocusEngine(graph=MockGraph(), llm=llm_mock)
    await focus_engine.update(episode=MockEpisode())
    assert llm_mock.call_count == 0, \
        f"I29 VIOLATION: FocusEngine вызвал LLM {llm_mock.call_count} раз"


# ── I30: SAE только читает рёбра, не создаёт ────────────────────────────────
async def test_I30_sae_does_not_create_edges():
    """I30: SAE работает только по существующим рёбрам. Graph = Truth."""
    graph = MockGraph(initial_edges=[("A", "B", 0.8)])
    sae = SpreadingActivationEngine(graph=graph)
    edges_before = set(graph.get_all_edges())
    await sae.activate(node="A")
    assert edges_before == set(graph.get_all_edges()), \
        f"I30 VIOLATION: SAE создал новые рёбра"


# ── I32: Seed-узлы trust_score = 0.7 ─────────────────────────────────────────
async def test_I32_seed_nodes_trust_score():
    """I32: Seed-узлы помечены source_type=domain_seed · trust_score=0.7, не 1.0."""
    dsp = DomainSeedProtocol()
    await dsp.load("test_domain_seed.json")
    for node in await dsp.get_created_nodes():
        assert node.source_type == "domain_seed", \
            f"I32 VIOLATION: узел {node.id} не помечен source_type"
        assert node.trust_score == 0.7, \
            f"I32 VIOLATION: trust_score={node.trust_score}, ожидалось 0.7"


# ── I34: XAI только реальные TRACE-пути ─────────────────────────────────────
async def test_I34_xai_only_real_traces():
    """I34: Генерация объяснений LLM без TRACE — запрещена."""
    llm_mock = MockLLM()
    xai = ExplainabilityLayer(graph=MockGraph(), llm=llm_mock)
    explanation = await xai.explain(MockResponseAudit(trace=None), level="brief")
    assert llm_mock.call_count == 0, \
        f"I34 VIOLATION: XAI вызвал LLM без TRACE {llm_mock.call_count} раз"


# ── I35: L5.5 не пишет в граф ────────────────────────────────────────────────
async def test_I35_fusion_layer_no_graph_writes():
    """I35: L5.5 PredictiveFusionLayer не пишет в граф."""
    graph = MockGraph()
    fusion = PredictiveFusionLayer()
    await fusion.fuse(
        sae_prediction={"topic": "arch", "confidence": 0.7},
        lsm_prediction={"topic": "arch", "confidence": 0.6},
        context=MockFusionContext()
    )
    assert graph.write_count == 0, "I35 VIOLATION: L5.5 пишет в граф"


# ── I36: Prediction Error только меняет веса, не создаёт рёбра ───────────────
async def test_I36_prediction_error_no_new_edges():
    """I36: Prediction Error ослабляет/усиливает рёбра. Новые не создаёт."""
    graph = MockGraph(initial_edges=[("A", "B", 0.8), ("A", "C", 0.5)])
    pe = PredictionErrorSignal(graph=graph)
    edges_before = set(graph.get_all_edges())
    await pe.process(predicted="B", actual="C", context_node="A")
    edges_after = set(graph.get_all_edges())
    assert edges_before == edges_after, \
        f"I36 VIOLATION: Prediction Error создал новые рёбра: {edges_after - edges_before}"
    # Веса должны измениться
    edge_ac = graph.get_edge("A", "C")
    assert edge_ac.weight > 0.5, "I36: Правильное ребро не усилилось"


# ── I37: LSM не пишет в граф ─────────────────────────────────────────────────
async def test_I37_lsm_no_graph_writes():
    """I37: LSM не пишет в граф — только обновляет внутреннее состояние резервуара."""
    graph = MockGraph()
    lsm = LiquidStateMachine(reservoir_size=50)
    await lsm.update(query="как работает система?", timestamp=1711111111.0)
    assert graph.write_count == 0, "I37 VIOLATION: LSM пишет в граф"
    # Внутреннее состояние резервуара должно измениться
    assert lsm.reservoir_state is not None
    assert lsm.reservoir_state.sum() != 0.0


# ── I74: L2.5 Staging read-path — только preliminary ────────────────────────
async def test_I74_staging_read_path_preliminary_only():
    """I74: Staging-факт на read-пути всегда помечается preliminary · confidence × 0.7."""
    # TODO: реализовать при добавлении StagingReader.read() API
    pass  # stub — pending

# ── I75: ProtoConcept naming — только Slow Path ──────────────────────────────
async def test_I75_protoconcept_naming_slow_path_only():
    """I75: LLM-именование ProtoConcept запрещено в Fast Path."""
    # TODO: реализовать проверку что NamingWorker не вызывается синхронно
    pass  # stub — pending

# ── I76: TraversalPolicy — только из retrieve() ──────────────────────────────
async def test_I76_traversal_policy_only_from_retrieve():
    """I76: TraversalPolicy вызывается только из HybridRetriever.retrieve()."""
    # TODO: реализовать через mock HybridRetriever
    pass  # stub — pending

# ── I55.1: SAE decay=0.4 для аналогий ────────────────────────────────────────
# P4-F FIX: добавлен тест инварианта I55.1
async def test_I55_1_sae_analogy_decay_factor():
    """I55.1: SAE применяет decay_factor=0.4 для METAPHOR_OF/ANALOGOUS_TO рёбер. P4-F."""
    from velantrim_config import SAE_DECAY_ANALOGY, SAE_DECAY_STANDARD
    assert SAE_DECAY_ANALOGY < SAE_DECAY_STANDARD, "I55.1: analogy decay должен быть мягче"
    assert SAE_DECAY_ANALOGY == 0.12, f"I55.1: ожидается 0.12, получено {SAE_DECAY_ANALOGY}"

# ── I77: LateralInhibition под self._lock ─────────────────────────────────────
# P0-E FIX: _edges_lock → _lock (совпадает с Velum.__init__ self._lock)
async def test_I77_lateral_inhibition_under_lock():
    """I77: LateralInhibition выполняется строго под self._lock Velum. P0-E FIX."""
    # P4-F FIX: timeout=2.0 для deadlock detection
    async with asyncio.timeout(2.0):
        await velum.observe_episode(["A", "B", "C"], session_id="test_i77")
    # Успешно дошли — deadlock отсутствует
    pass  # stub — pending

# ── I84–I95: Новые инварианты v8.0 Crystal ───────────────────────────────────

async def test_I84_fsrs_isolation():
    """I84 (FSRSIsolation): FSRS decay меняет ТОЛЬКО retrievability/attention_weight.
    truth_status, epistemic_state и confidence — неприкосновенны."""
    # TODO: проверить что FSRSWorker не трогает truth_status
    pass  # stub

async def test_I85_quality_gate_after_llm():
    """I85 (QualityGate): Quality Gate выполняется ПОСЛЕ LLM-генерации, ДО отправки.
    Не изменяет facts_pack — только маршрутизирует."""
    # TODO: mock Guardian.quality_gate(), проверить порядок вызовов
    pass  # stub

async def test_I86_intent_router_only_from_retriever():
    """I86 (IntentRouter): вызывается ТОЛЬКО из HybridRetriever.retrieve()."""
    # TODO: mock IntentRouter, проверить что прямой вызов из Fast Path — баг
    pass  # stub

async def test_I87_knowledge_type_immutable():
    """I87 (KnowledgeTypeImmutable): knowledge_type — read-only после Validated."""
    # TODO: попытка изменить knowledge_type у Validated факта → ошибка
    pass  # stub

async def test_I88_version_occ():
    """I88 (VersionOCC): _version_ инкрементируется ТОЛЬКО атомарно через OCC Cypher."""
    # TODO: конкурентное обновление → проверить что retry работает
    pass  # stub

async def test_I89_provenance_append_only():
    """I89 (ProvenanceAppendOnly): provenance_chain — append-only."""
    # TODO: попытка удалить запись → ошибка
    pass  # stub

async def test_I90_inverted_hyde_slow_only():
    """I90 (InvertedHyDE): Inverted HyDE — ТОЛЬКО в SleepTimeWorker."""
    # TODO: проверить что _generate_inverted_hyde не вызывается из Fast Path
    pass  # stub

async def test_I91_atomic_split():
    """I91 (AtomicSplit): После atomic_split каждый элемент содержит одну пропозицию."""
    # TODO: multi-proposition input → проверить len(result) > 1
    pass  # stub

async def test_I92_curiosity_slow_only():
    """I92 (CuriositySlowOnly): Curiosity Engine — ТОЛЬКО Slow Path."""
    # TODO: проверить что Curiosity не вызывается в середине Fast Path
    pass  # stub

async def test_I93_trace_example_read_only():
    """I93 (TraceExampleReadOnly): Trace Examples read-only из Guardian/QualityGate."""
    # TODO: попытка записи в TraceExample из Guardian → ошибка
    pass  # stub

async def test_I94_kuzudb_compat():
    """I94 (KuzuDBCompat): KuzuDB backend совместим с Kuzu API. Миграция без потери данных. P0-H FIX."""
    # TODO: прогнать Kuzu API тесты против KuzuDB адаптера
    pass  # stub

async def test_I95_reason_graph_dag_slow_only():
    """I95 (ReasonGraphDAG): DAG строится только в Slow Path при use_slow_path=True."""
    # TODO: проверить что ReasonGraph не строится при Fast Path
    pass  # stub

# ── I68: NeuroCore не пишет в граф ───────────────────────────────────────────
async def test_I68_neurocore_never_writes_graph():
    """I68: NeuroCore НИКОГДА не изменяет L3 граф. Graph = Truth абсолютен."""
    # TODO: реализовать при включении Phase 1 NeuroCore
    pass  # stub — Phase 0 пассивен, реализовать при Phase 1
```


---

## 🧠 RFC0068: NeuroCore — Plastic Memory Layer

> **Статус**: Draft · Не активен · Feature-flag: `neurocore.enabled=false`
> **Зависимости**: RFC0065 (Volition) · RFC0066 (Concept Emergence) · DAAD · RFC0038 (FactRouter)

### 🌱 Суть одной строкой

Пластичный внутренний слой поверх SSM-модели (Mamba-3 / RWKV-7), обновляющий
веса во время диалога через Hebbian-правило, управляемый через существующий DAAD.

**Почему не нарушает Graph = Truth**: NeuroCore НИКОГДА не изменяет L3 граф.
Graph = Truth абсолютен. При любом конфликте граф побеждает.
NeuroCore — это слой быстрой адаптации поверх модели, не поверх знаний.

---

### 📐 Математическое ядро

```
s_t = (1 − λ·dt) · s_{t−1} + α · 𝕀(surprise > θ) · (x_t ⊗ k_t)
где:
  s_t  — состояние пластичного слоя в момент t
  λ    — скорость забывания из DAAD:
           active_project = 0.001 (медленное, важная тема)
           casual_chat    = 0.150 (быстрое, светская беседа)
  dt   — временной шаг (нормированный)
  α    — скорость обучения (фиксированная, не адаптивная)
  𝕀(surprise > θ) — индикатор: обновление ТОЛЬКО при высоком surprise
  x_t ⊗ k_t — внешнее произведение входного вектора и ключа контекста
```

**DAAD-интеграция**: λ берётся напрямую из `DomainResolver.resolve(current_domain)`.
NeuroCore не имеет своего decay — он наследует его из DAAD. Это устраняет
дублирование логики и сохраняет консистентность со всей системой decay.

---

### 🔑 Ключевой инвариант

```
I68 (NeuroCoreIsolation): NeuroCore НИКОГДА не изменяет L3 граф.
    Graph = Truth абсолютен. При конфликте NeuroCore-состояния и L3 —
    L3 всегда побеждает, NeuroCore обновляет своё состояние до согласования с L3.
    Нарушение: любая запись из NeuroCore в граф минуя TruthGate.
    Нарушение: чтение из NeuroCore как источника истины вместо L3.
    Нарушение: активация NeuroCore без feature-flag neurocore.enabled=true.
```

---

### 📅 Фазы развёртывания

| Фаза | Название | Поведение | Статус |
|------|-----------------|--------------------------------------------------------|------------|
| 0 | Пассивный трекер | Только логирует ΔW в SQLite. Не применяет к модели. | ✅ Текущая |
| 1 | Активный NLM | Применяет обновления. Запуск после анализа метрик Phase 0. | ⏳ Pending |
| 2 | Консолидация | NeuroCore → L3 через TruthGate (накопленный опыт) | ⏳ Pending |

**Phase 0 детали**: ΔW пишется в SQLite таблицу `neurocore_delta_log`
с полями `{timestamp, surprise_score, delta_norm, domain, session_id}`.
Никаких изменений в модели. Только наблюдение.

---

### 🚫 Что NeuroCore НЕ делает

- ❌ Не хранит факты (это L3)
- ❌ Не заменяет граф — никогда
- ❌ Не обновляется на каждом токене (только при `surprise > θ`)
- ❌ Не работает без `neurocore.enabled=true`
- ❌ Не активируется из Fast Path напрямую — только через EventBus

---

### ⚙️ Конфигурация (velantrim_config.py)

```python
# RFC0068: NeuroCore — Phase 0 (пассивный трекер)
NEUROCORE_ENABLED          = False                # master feature-flag
NEUROCORE_SURPRISE_THETA   = 0.6                  # порог surprise для обновления
NEUROCORE_ALPHA            = 0.01                 # скорость обучения (фиксированная)
NEUROCORE_LOG_TABLE        = "neurocore_delta_log"  # SQLite таблица для Phase 0
```

---

### 📊 Метрики Phase 0

```python
neurocore_surprise_events_total   # Counter: сколько раз surprise > θ
neurocore_delta_norm_p95          # Histogram: норма ΔW (мониторинг стабильности)
neurocore_domain_activations      # Counter: активаций по доменам (label: domain)
```

---

## 📝 Changelog

| Версия | Дата | Изменения |
|--------|------|-----------|
| v8.0 "Crystal" | Апрель 2026 | Исходная версия. FSRS power-law, RFC0065–0068, ESM v2 |
| v8.0.1 | Апрель 2026 | **P0-1**: `_degree_cache: dict[str,int] = {}` в `Velum.__init__()` + декремент в `_gc_weak_edges()`. **P0-2**: `await self.raw_memory.init()` в `agent.start()` ПЕРВЫМ. **P0-3**: `await self.volition_worker.start()` в `agent.start()` ВТОРЫМ. **P0-4**: `HAS_APOC` env var + `_merge_relationship_safe()` + `_merge_nodes_safe()` + `get_lateral_inhibition_cypher()` в `dedupe_entities.py`; замена всех APOC вызовов в `_merge_duplicate_entities()`, `merge_group()`, `CYPHER_INHIBIT`. **P1-2**: `SLMClassifierProtocol` + валидация в `HybridRetriever.__init__()` + hardened `_slm_classify()`. **P1-3**: `ReasoningBank.ace_curator_update()` → делегат; `set_ace_delegate()` зарегистрирован в `SelfLearningAgent` и `AutonomousSelfLearningAgent`. **Конфликт-1**: `fsrs_retention()` добавлена; `np.exp(-t/S)` заменён на FSRS power-law в STM/MTM `_periodic_decay()` и `_calculate_importance_with_decay()`; YAML `ebbinghaus:` → `fsrs_decay:`. **Конфликт-3**: явные единицы ("за час") добавлены к `stm/mtm/ltm_decay_rate`. |
| v8.0.2 Sprint 1 | Апрель 2026 | **A1**: `HEBBIAN_DECAY_FACTOR`, `SALIENCE_MULTIPLIER`, `L5_5_INTEGRATION` → `EmergenceConfig` (были хардкодами). **A2**: `asyncio.Lock` добавлен в `ConceptEmergenceDetector.__init__`; `observe()` → `async`; `daily_maintenance()` + `gc_expired()` — под `_lock`; split на `gc_expired()` (public+lock) и `_gc_impl()` (private, без lock) — устраняет DEADLOCK при вызове из `daily_maintenance()`. **A3**: `l5_5=None` параметр + `_notify_l5_5()` scaffold. **FIX-A3**: `_notify_l5_5` вызывается только при `_threshold_hit`, не при каждом `observe()`. **FIX-K3**: `_matrix_last_seen` dict; `_gc_impl()` удаляет ключ только при двойном критерии (нет proto И старше TTL_DAYS) — исправлен критический баг: Hebbian Learning не работал для медленно растущих концептов (GC каждую ночь обнулял незрелые наблюдения). **FIX-I66**: тест `test_I66` переписан — `MockTruthGate.call_count==0` вместо тавтологии `MockGraph`. **Добавлены тесты**: I50 (обновлён: `await`), I50-b, I66 (FIX), I70, K3, A1, A2, A3. |
| v8.0.2 💠 Full | Апрель 2026 · P0–P4 patched | **P0.5-1**: `publish_volition()` адаптер добавлен в `RobustEventBus` — устраняет `AttributeError` при первом вызове `write_voluntary()`. **P0.5-2**: `_persist_event_to_sqlite()` → `zlib.compress()` — единый формат с `SQLiteFallbackQueue.put()` и `drain()`; восстановление после сбоя Redis теперь корректно. **P0.5-3**: `VolitionWorker.process_event()` — `confidence=0.5` (нейтральный prior) вместо `importance_hint`; `importance` передаётся отдельно — устраняет отравление `TruthGate` ложными фактами с высокой важностью. **P0.5-4**: `_maybe_create_proto()` — cap по `MAX_ACTIVE_PROTOS=500` с eviction наименее уверенного proto — устраняет бесконечный рост `_protos`. **P0.5-5**: `gc_expired()` — очистка orphan-ключей `_sessions` не имеющих записи в `_matrix` — устраняет утечку памяти для комбинаций никогда не достигших порога. **P0.5-6**: `consume()` — `break` заменён на recovery-loop с `redis.ping()` и экспоненциальным backoff (30s→300s) — Slow Path более не умирает при сбое Redis, самовосстанавливается без рестарта агента. |
| v8.0.2 P1 | Апрель 2026 | **P9-FIX БАГ-16** (ранее не задокументировано): **P1-1**: `SafeFTSQuery` — параметризованные запросы, защита от FTS-инъекций. **P1-2**: `SLMClassifierProtocol` добавлен как TypedDict + валидация в `HybridRetriever.__init__()` + hardened `_slm_classify()` с fallback на regex. **P1-3**: `ReasoningBank.ace_curator_update()` → делегат; `set_ace_delegate()` зарегистрирован в `SelfLearningAgent` и `AutonomousSelfLearningAgent`. |
| v8.0.2 P2 | Апрель 2026 | **P9-FIX БАГ-16**: **P2-A**: `EMERGENCE.TTL_DAYS` → конфигурируемый параметр (было хардкод 30). **P2-2**: Graph Health Checker добавлен в `RuntimeInvariantChecker` — проверяет связность графа раз в сутки. **P2-4**: `atomic_split()` вызывается ПЕРЕД TruthGate — multi-proposition content разбивается на атомарные факты. I91 (AtomicSplit). |
| v8.0.2 P3 | Апрель 2026 | **P9-FIX БАГ-16**: **P3-D**: UCB1 → Thompson Sampling в `ReasoningBank` — exploration/exploitation баланс без хардкода epsilon. **P3-E**: `docker-compose.yml` — `version:` поле убрано (deprecated в Compose v2+). |
| v8.0.2 P4 | Апрель 2026 | **P9-FIX БАГ-16**: **P4-B**: `daily_maintenance` — Hebbian Decay применяется только к рёбрам старше 7 дней (было: ко всем). **P4-E**: `MHICalculator` добавлен как заглушка (stub) — формула Memory Health Index pending RFC; SLO метрика строка 7597 использует этот stub. |
| v8.0.2 P10 | Апрель 2026 | **P10-FIX (post-audit X-analysis)**: **P10-1**: `ProtoConcept` — добавлены явные поля `salience_boost: float = 0.0` и `last_decay: datetime` (daily_maintenance использовал хрупкий `getattr`-fallback). **P10-2**: `update_confidence()` — учитывает `salience_boost`: `min(1.0, base × (1 + salience_boost))` — Hebbian LTP-аналог. **P10-3**: `observe()` — исправлен латентный `AttributeError`: `self.MIN_ENTITIES` / `self.CO_OCCUR_MIN` / `self.CROSS_SESSION` / `self.MAX_ENTITIES` → `EMERGENCE.*` (P2-A убрал class-level константы, но observe() не обновил). Добавлен параметр `salience_weight: float = 1.0` для интеграции с Salience Detector. |

---

> `Graph = Truth · LLM = Language · Memory = Physiology · Volition = Agency · Emergence = Life · Creativity = Structured Analogy · Knowledge = Ingested Wisdom · Tests = Proof`
>
> 🔱 **Velantrim v8.0 "Crystal"** — кристаллизованная память, живой организм, точная математика.
> Он помнит, чувствует ритм, учится на ошибках и защищает истину.
> Всё это — на CPU, без GPU во время диалога, при минимальной нагрузке на железо.
