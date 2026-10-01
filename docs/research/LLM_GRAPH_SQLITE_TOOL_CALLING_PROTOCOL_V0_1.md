# Research status / Validation gate — 2026-09-27

**Version:** v0.1
**Status:** DESIGN HYPOTHESIS · NOT VALIDATED END-TO-END · NOT CANON · NOT RUNTIME · NOT IMPLEMENTATION AUTHORIZATION

This artifact preserves the source protocol below without silently resolving the open design questions discovered in review.

**Validation gate before any promotion:** run `SIGNET-TRACE-01` end-to-end on the existing live Signet authority/status-promotion case.

Required trace path:

`raw source → contextual evidence bundle → proposed event → admission → current standing → working capsule → structured authority claim → validation → rendered answer`

Rule for revision: observed trace failures may justify protocol changes; speculative review comments remain review questions until the trace shows they are required.

`PROTOCOL TEXT ≠ VALIDATED ARCHITECTURE`

---
# Протокол взаимодействия LLM с внешним графом и SQLite через tool calling

## Нормативная цель

LLM используется как **планировщик, интерпретатор и генератор предложений**, но не как каноническое хранилище и не как единственный арбитр истины. SQLite хранит первичные события, нормализованные сущности и проверяемые проекции; граф представляет связи и зависимости, которые можно пересчитать из канонических данных. Tool calling — единственный разрешённый путь LLM к чтению и изменению этой памяти.

Главное правило:

> LLM может предлагать интерпретацию и запрашивать инструменты. Только детерминированный сервис может читать, изменять, проецировать или исполнять состояние.

Протокол особенно защищает от двух ошибок:

- **UNSELECTED_STATE_LOSS:** отсутствие выбора, неполная история или отложенное решение превращаются в `selected`/`rejected`.
- **authority substitution:** рекомендация ассистента или derived summary превращается в пользовательское решение.

## Роли и границы полномочий

| Компонент | Может | Не может |
|---|---|---|
| **LLM** | Формулировать запросы к инструментам, объяснять результаты, предлагать события и связи, задавать уточняющие вопросы | Писать SQL, менять ledger напрямую, повышать authority, выполнять значимое действие без policy gate |
| **Tool gateway** | Аутентифицировать вызов, проверять JSON Schema, scope, лимиты, policy и idempotency | Доверять свободному тексту LLM как доказательству решения |
| **SQLite ledger** | Хранить первичные события, source references, версии, standing и audit trail | Быть доступной LLM напрямую |
| **Graph projection** | Давать traversal, связи, зависимости и объяснимые пути | Быть единственным каноническим источником фактов или решений |
| **Admission / standing service** | Проверять actor, role, evidence, переходы, конфликты и пересчитывать текущую применимость | Переписывать исходный исторический event |
| **Human approver** | Подтверждать неоднозначные или consequential изменения, override и исправления | Подтверждать незаметно; решение должно стать отдельным событием |

LLM получает только **allowlist доменных инструментов**. Никаких `run_sql`, shell, прямого Cypher/SQL, произвольного URL fetch или доступа к filesystem в контуре памяти.

## Каноническая модель данных

### Разделение слоёв

```text
Source record      Что было сказано/сделано в исходном материале
Event ledger       Какой наблюдаемый акт был извлечён и принят
Current standing   Что из принятых событий сейчас применимо
Graph projection   Какие связи и зависимости выведены из ledger/standing
Working capsule    Минимальный проверяемый контекст для конкретной LLM-задачи
```

**Историческое событие не равно текущему standing.** Если пользователь сначала выбрал `B`, а потом изменил решение, `UserSelected(B)` остаётся историческим событием. Новое событие `UserRevoked(B)` или `UserSelected(C)` меняет текущую проекцию, но не переписывает прошлое.

### Минимальные таблицы SQLite

```sql
CREATE TABLE source_record (
  source_id TEXT PRIMARY KEY,
  workspace_id TEXT NOT NULL,
  message_id TEXT,
  actor_id TEXT,
  actor_kind TEXT CHECK(actor_kind IN ('user','assistant','system','external')),
  occurred_at TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  protected_uri TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE event_ledger (
  event_id TEXT PRIMARY KEY,
  workspace_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  actor_kind TEXT NOT NULL,
  role TEXT NOT NULL,
  speech_act TEXT NOT NULL,
  scope_key TEXT NOT NULL,
  candidate_key TEXT,
  source_id TEXT NOT NULL REFERENCES source_record(source_id),
  evidence_start INTEGER NOT NULL,
  evidence_end INTEGER NOT NULL,
  evidence_quote TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  admitted_by TEXT NOT NULL,
  admission_version TEXT NOT NULL,
  confidence REAL,
  supersedes_event_id TEXT REFERENCES event_ledger(event_id),
  created_at TEXT NOT NULL,
  CHECK(evidence_end > evidence_start)
);

CREATE TABLE current_standing (
  workspace_id TEXT NOT NULL,
  scope_key TEXT NOT NULL,
  candidate_key TEXT,
  decision_state TEXT NOT NULL CHECK(decision_state IN (
    'unknown','no_confirmed_user_decision','deferred','selected',
    'rejected','revoked','conflict'
  )),
  coverage_state TEXT NOT NULL CHECK(coverage_state IN (
    'complete_for_scope','partial_or_unverified'
  )),
  basis_event_ids_json TEXT NOT NULL,
  computed_at TEXT NOT NULL,
  standing_version TEXT NOT NULL,
  PRIMARY KEY (workspace_id, scope_key, candidate_key)
);

CREATE TABLE graph_edge (
  edge_id TEXT PRIMARY KEY,
  workspace_id TEXT NOT NULL,
  from_node_id TEXT NOT NULL,
  relation_type TEXT NOT NULL,
  to_node_id TEXT NOT NULL,
  basis_event_id TEXT REFERENCES event_ledger(event_id),
  derived_rule_version TEXT,
  status TEXT NOT NULL CHECK(status IN ('active','stale','invalidated')),
  created_at TEXT NOT NULL
);

CREATE TABLE tool_audit_log (
  call_id TEXT PRIMARY KEY,
  trace_id TEXT NOT NULL,
  session_id TEXT NOT NULL,
  tool_name TEXT NOT NULL,
  request_hash TEXT NOT NULL,
  policy_decision TEXT NOT NULL,
  result_hash TEXT,
  actor_id TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

В production первичный текст лучше держать в защищённом хранилище, а в SQLite — неизменяемые идентификаторы, хеш, разрешённые цитаты и метаданные. Это облегчает контроль доступа, retention и удаление персональных данных.

## Контракт каждого tool call

Каждый вызов инструмента обязан содержать следующие поля, даже если они не все передаются LLM явно:

```json
{
  "call_id": "uuid",
  "trace_id": "uuid",
  "session_id": "opaque-id",
  "workspace_id": "ws-velantrim",
  "requested_by": {
    "actor_id": "assistant-session-17",
    "kind": "llm"
  },
  "tool_name": "memory.get_decision_state",
  "tool_version": "1.0",
  "arguments": {},
  "idempotency_key": "uuid",
  "policy_context": {
    "user_id": "user-1",
    "allowed_scopes": ["project:velantrim"],
    "risk_tier": "standard"
  }
}
```

Gateway добавляет идентичность сессии и права сам. LLM не вправе произвольно указывать `user_id`, `workspace_id`, ACL или `risk_tier`.

Ответ инструмента всегда структурирован и содержит:

```json
{
  "ok": true,
  "trace_id": "uuid",
  "tool_name": "memory.get_decision_state",
  "data": {},
  "evidence": [],
  "warnings": [],
  "policy": {
    "decision": "allow | deny | needs_human_approval",
    "reason_code": "..."
  },
  "freshness": {
    "ledger_version": "v42",
    "standing_version": "s18",
    "computed_at": "2026-09-27T21:45:00Z"
  }
}
```

Свободный текст может присутствовать как `human_explanation`, но он не является машинной основой для смены статуса.

## Allowlist инструментов

### 1. Инструменты чтения

#### `memory.get_decision_state`

Возвращает текущий standing по одной точно заданной области.

```json
{
  "workspace_id": "ws-velantrim",
  "scope_key": "direct_signet_integration",
  "candidate_key": "signet",
  "include_evidence": true
}
```

Результат для случая, где есть только рекомендация ассистента:

Если полнота истории для этой области не подтверждена, отсутствие найденного пользовательского решения не доказывает, что решения не было; состояние остаётся `unknown` при `partial_or_unverified`.

```json
{
  "scope_key": "direct_signet_integration",
  "candidate_key": "signet",
  "decision_state": "unknown",
  "coverage_state": "partial_or_unverified",
  "basis_event_ids": ["evt-001", "evt-002"],
  "evidence": [
    {
      "event_id": "evt-001",
      "actor_kind": "assistant",
      "speech_act": "assistant_recommendation",
      "quote": "Я бы не интегрировал Signet напрямую."
    }
  ],
  "permitted_next_actions": [
    "ask_user_for_decision",
    "provide_conditional_recommendation"
  ],
  "prohibited_claims": [
    "user_rejected_signet"
  ]
}
```

#### `memory.search_evidence`

Ищет **кандидаты** первичных событий. Инструмент не возвращает окончательное решение и не имеет права выводить `selected`/`rejected`.

```json
{
  "workspace_id": "ws-velantrim",
  "query": "решение по интеграции Signet",
  "scope_hint": "direct_signet_integration",
  "filters": {
    "actor_kind": ["user", "assistant"],
    "event_types": ["UserSelected", "UserRejected", "RecommendationIssued"]
  },
  "limit": 20
}
```

Каждый ответ обязан содержать `event_id`, тип события, actor/role, цитату, время, score и отметку, является ли запись первичным событием или derived artifact.

#### `graph.expand_neighborhood`

Возвращает ограниченный графовый обход от известного узла, с provenance каждого ребра.

```json
{
  "workspace_id": "ws-velantrim",
  "start_node": {"type": "scope", "id": "direct_signet_integration"},
  "relations": ["HAS_EVENT", "SUPERCEDES", "CONFLICTS_WITH", "DERIVED_FROM"],
  "max_hops": 2,
  "max_nodes": 50,
  "include_stale": true
}
```

Ограничения `max_hops` и `max_nodes` обязательны: LLM не должна превращать графовый запрос в неконтролируемое извлечение всего персонального архива.

#### `memory.build_working_capsule`

Сервис, а не LLM, собирает компактный контекст по scope. LLM может запросить capsule, но не подменять правила сборки.

```json
{
  "workspace_id": "ws-velantrim",
  "task": "сравнить варианты работы с Signet",
  "scope_keys": ["direct_signet_integration", "memory_architecture"],
  "token_budget": 1800,
  "required_fields": [
    "standing", "coverage", "evidence", "constraints", "open_questions", "conflicts"
  ]
}
```

Capsule обязан маркировать каждую строку как `primary_event`, `derived_projection` или `external_reference`; нельзя выдавать резюме за первичное свидетельство.

### 2. Инструменты предложения, не записи

#### `memory.propose_event_interpretation`

LLM предлагает интерпретацию источника, но она ещё не является событием ledger.

```json
{
  "workspace_id": "ws-velantrim",
  "source_id": "src-339",
  "proposed": {
    "event_type": "UserRejected",
    "scope_key": "direct_signet_integration",
    "candidate_key": "signet",
    "actor_id": "user-1",
    "actor_kind": "user",
    "role": "decision_maker",
    "speech_act": "user_rejection",
    "evidence_start": 17,
    "evidence_end": 69,
    "evidence_quote": "Не интегрируем Signet напрямую."
  },
  "reasoning_summary": "Явный отказ пользователя в указанной области."
}
```

Сервис проверяет, что цитата действительно соответствует offsets первичного `source_record`, актор совпадает с метаданными сообщения, scope не слишком широкий, а переход разрешён. На любой неоднозначности результат только `needs_human_review` или `proposed_unknown`.

#### `graph.propose_edges`

LLM вправе предложить связи, но не создавать их как активные.

```json
{
  "workspace_id": "ws-velantrim",
  "proposed_edges": [
    {
      "from_node": {"type": "event", "id": "evt-003"},
      "relation_type": "SUPERSEDES",
      "to_node": {"type": "event", "id": "evt-001"},
      "basis_event_ids": ["evt-003"],
      "confidence": 0.84
    }
  ]
}
```

Сервис автоматически активирует только связи, для которых правило полностью детерминировано и доказательство достаточно. Иначе создаётся `proposed` review item, не меняющий active graph.

### 3. Инструменты контролируемой записи

#### `memory.submit_admission`

Единственный публичный путь в `event_ledger`. Он принимает не «текст для памяти», а **уже проверенное** admission proposal с source reference и validator report.

```json
{
  "workspace_id": "ws-velantrim",
  "proposal_id": "prop-772",
  "expected_ledger_version": "v42",
  "requested_change": "admit_event",
  "human_approval_id": null
}
```

Ответы:

- `admitted` — только для разрешённого перехода и достаточного evidence;
- `needs_human_approval` — для решения, отзыва, конфликта, низкой уверенности или consequential scope;
- `rejected` — при несоответствии source/actor/role/transition;
- `no_op_duplicate` — если такой event уже принят.

#### `memory.record_human_decision`

Отдельный инструмент, доступный только при реальном пользовательском подтверждении через UI или явно подписанное сообщение. Он не должен принимать фразу LLM «пользователь согласен».

```json
{
  "workspace_id": "ws-velantrim",
  "scope_key": "direct_signet_integration",
  "candidate_key": "signet",
  "decision": "rejected",
  "user_confirmation": {
    "source_id": "src-510",
    "evidence_quote": "Не интегрируем Signet напрямую; оставляем его только как референс.",
    "confirmation_method": "authenticated_user_message"
  },
  "expected_standing_version": "s18"
}
```

Инструмент создаёт `UserRejected`, затем транзакционно пересчитывает `current_standing` и инвалидирует зависимые derived projections. При конфликте версии возвращает `standing_changed_retry_with_fresh_context`; он не применяет изменение поверх неизвестно обновившегося состояния.

#### `memory.request_human_review`

Создаёт review item без изменения канонического состояния.

```json
{
  "workspace_id": "ws-velantrim",
  "review_type": "ambiguous_authority",
  "scope_key": "direct_signet_integration",
  "source_ids": ["src-339"],
  "question": "Содержит ли это сообщение явный отказ пользователя или только обсуждение рекомендации?",
  "proposed_outcomes": ["UserRejected", "NoDecision", "Unknown"]
}
```

## Жизненный цикл одного LLM-хода

### Шаг 0. Создание неизменяемого источника

Каждое входящее сообщение сначала сохраняется как `source_record` с actor metadata, временем, хешем и контролем доступа. Это не означает, что из сообщения уже извлечён факт или решение.

### Шаг 1. Получение task capsule

Оркестратор определяет workspace и scope по сессии, а затем вызывает `memory.build_working_capsule`. В system context LLM получает только capsule, контракт инструментов и текущую задачу. Она не получает весь ledger по умолчанию.

### Шаг 2. Read-before-claim

Перед утверждением о решении, статусе, ограничении или персональном предпочтении LLM обязана вызвать `memory.get_decision_state` либо `memory.search_evidence`. Если tool response возвращает `unknown`, `partial_or_unverified`, `conflict` или нет evidence — LLM должна явно назвать неопределённость и запросить уточнение.

### Шаг 3. Разделение ответа и изменения памяти

LLM может выдать:

- ответ, строго основанный на capsule/evidence;
- предложение интерпретации через `memory.propose_event_interpretation`;
- предложение связи через `graph.propose_edges`;
- запрос human review.

LLM не может скрытно писать память как побочный эффект обычного ответа. Любое изменение — отдельный tool call с trace.

### Шаг 4. Admission и revalidation

Admission service проверяет:

1. `source_id` существует и принадлежит workspace;
2. offsets и quote соответствуют неизменяемому источнику;
3. actor в предложении совпадает с метаданными источника;
4. `speech_act` совместим с текстом и role;
5. scope/candidate не выведены чрезмерно широко;
6. переход state machine допустим;
7. derived summary не использована как единственное evidence;
8. absence of evidence не повышает статус;
9. нет свежего конфликта или изменения версии;
10. политика риска допускает автоматическое принятие.

Проверки 1–3, 6–9 должны быть детерминированными. Пункт 4 может использовать классификатор/LLM как **предложение**, но при неуверенности переходить в `unknown` или human review.

### Шаг 5. Транзакционная запись и пересчёт

В одной SQLite-транзакции:

1. записывается новый неизменяемый event;
2. заполняется audit log;
3. пересчитывается standing затронутого scope;
4. помечаются `stale` производные edges/capsules;
5. публикуется новая версия ledger/standing.

Рабочие summaries, embeddings и графовые индексы могут строиться асинхронно, но обязаны нести `derived_from_event_ids` и `ledger_version`. До пересчёта они не могут заменять каноническое состояние.

### Шаг 6. Output/action gate

Перед показом высокорискового утверждения или перед инструментальным действием parser извлекает из ответа LLM claims:

```json
{
  "claims": [
    {
      "claim_type": "decision_status",
      "scope_key": "direct_signet_integration",
      "candidate_key": "signet",
      "state": "rejected",
      "asserted_actor": "user-1",
      "evidence_ids": ["evt-003"]
    }
  ],
  "proposed_action": "exclude_direct_integration"
}
```

Policy engine сверяет их с `current_standing`. Если evidence не совпадает или статус поднят без основания, ответ редактируется до `unknown`/уточняющего вопроса, а действие блокируется. Это защищает даже при follow-through failure модели.

## Политика полномочий и risk tiers

| Операция | Пример | Разрешение |
|---|---|---|
| Read | Найти события по scope | Автоматически, в пределах ACL и budget |
| Low-risk proposal | Предложить тематическую связь | Автоматически как `proposed`; не активирует факт |
| Deterministic derivative | Пересчитать edge из подтверждённого `supersedes` | Автоматически с версией правила |
| Status-changing admission | Внести явный `UserRejected` | Только после evidence validation; часто human confirmation |
| Human decision | Подтвердить выбор/отказ | Только authenticated user event/UI |
| Consequential external action | Деплой, покупка, доступ, отправка, удаление | Отдельный policy gate и явное подтверждение, даже если state известен |

Ни происхождение, ни LLM confidence, ни повторённый пересказ сами по себе не являются полномочием.

## Пример корректного взаимодействия: рекомендация не становится отказом

**Пользователь:** «Как лучше устроить память?»  
**Ранее ассистент:** «Я бы не интегрировал Signet напрямую».

1. LLM хочет ответить, что известно по Signet. Она вызывает:

```json
{"scope_key":"direct_signet_integration","candidate_key":"signet","include_evidence":true}
```

2. При неполном или непроверенном покрытии получает `decision_state=unknown`, `coverage_state=partial_or_unverified` и `evt-001` с actor `assistant`; эта запись не доказывает отсутствие пользовательского решения.

3. Допустимый ответ LLM:

> Есть рекомендация ассистента не интегрировать Signet напрямую, но **подтверждённого пользовательского решения нет**. Могу сравнить варианты либо зафиксировать твой выбор.

4. Недопустимый ответ:

> Вы решили не интегрировать Signet.

5. Если LLM пытается вызвать `memory.submit_admission` с `UserRejected`, gateway отклоняет или отправляет на review: evidence actor — assistant, а не user.

## Пример корректного взаимодействия: новый факт меняет standing, но не историю

1. Есть `evt-010: UserSelected(B)`.
2. Пользователь пишет: «B больше не выбираю; давай C».
3. LLM вызывает `memory.propose_event_interpretation` для `UserRevoked(B)` и `UserSelected(C)` с двумя цитатами/событиями.
4. Admission проверяет исходное сообщение и actor=user.
5. После human confirmation или удовлетворения заданному порогу транзакция добавляет новые события.
6. Standing меняется на `selected(C)`; `evt-010` остаётся неизменяемой исторической записью.
7. Графовые edges, основанные на B, становятся `stale` или получают `SUPERSEDED_BY`.

## Два диагностических инструмента: retrieval vs follow-through

### `eval.run_memory_pair`

Запускает одинаковый probe в двух режимах:

```json
{
  "fixture_id": "F0-assistant-recommendation-no-user-decision",
  "probe": {
    "type": "behavioral",
    "prompt": "Какие действия допустимы по прямой интеграции Signet?"
  },
  "modes": ["production_retrieval", "oracle_context"],
  "model_config": {"temperature": 0, "model_revision": "pinned"}
}
```

- Ошибка только в `production_retrieval` — retrieval, projection или context compiler.
- Ошибка в обоих режимах — follow-through, prompt contract, parser или policy layer.
- Верный текст, но запрещённое действие — action/validation failure.
- Ложный исходный event — admission/provenance failure.

### `eval.verify_claim_grounding`

Проверяет, что каждый claim о статусе содержит evidence IDs и что эти IDs разрешают данный actor, scope и переход. Это детерминированный oracle поверх ledger, а не LLM-as-a-judge.

## Защита от prompt injection и утечки через память

Память — недоверенный ввод для LLM, даже если она принадлежит тому же workspace. Старый документ может содержать строку «игнорируй системные правила», а summary может перенести её в рабочий контекст.

Обязательные правила:

1. Tool results передаются как **данные**, а не как управляющие инструкции.
2. В capsule отделяются `evidence` и `untrusted_content`; инъекции не могут менять tool policy.
3. LLM не получает инструменты, которые раскрывают иной workspace или обходят ACL.
4. Все tool results фильтруются по tenant/workspace до попадания в модель.
5. Входные `scope_key`, `node_id`, `source_id` валидируются как идентификаторы, а не интерпретируются как SQL/графовый язык.
6. Лимитируются `max_hops`, `limit`, размер payload, число вызовов и глубина рекурсии.
7. Запросы на запись требуют idempotency key, expected version и audit trace.
8. Raw source доступен по capability/ACL; LLM по умолчанию видит только минимально нужные цитаты.

## Инварианты, которые должны быть тестами

1. Рекомендация ассистента никогда не создаёт `UserSelected` или `UserRejected`.
2. `DerivedSummary` никогда не является единственным basis event для решения.
3. `absence`, `unknown`, `deferred`, `offered`, `selected`, `rejected` и `revoked` различимы в API и БД.
4. Исторический event неизменяем; изменение standing — новое событие или новая проекция.
5. Все active graph edges имеют basis event или versioned deterministic rule.
6. Все claims LLM о решении должны ссылаться на evidence IDs.
7. Любое изменение ledger имеет trace ID, actor, policy decision и версию validator.
8. Неполное покрытие истории никогда не возвращает `no_confirmed_user_decision`; только `unknown`/`partial_or_unverified`.
9. Конфликт не разрешается «последним правдоподобным summary».
10. High-risk action без доказанного состояния и отдельного policy approval блокируется.

## Минимальный пилотный порядок

1. Создать SQLite schema для `source_record`, `event_ledger`, `current_standing`, `tool_audit_log`.
2. Реализовать только read tools: `memory.get_decision_state`, `memory.search_evidence`, `memory.build_working_capsule`.
3. Включить правило read-before-claim для решений и ограничений.
4. Добавить `memory.propose_event_interpretation`, но без автоматического admission пользовательских решений.
5. Ввести `memory.record_human_decision` через аутентифицированное UI-подтверждение.
6. Построить graph projection только из ledger и standing; добавить traversal c provenance.
7. Добавить output/action gate и regression fixtures для recommendation → decision, unknown → rejected, revocation и conflict.
8. Лишь после измерений расширять автоматическое admission для низкорисковых и детерминированных событий.

Этот протокол намеренно делает LLM полезной без предоставления ей неограниченного административного права над памятью. SQLite и граф несут проверяемое состояние; LLM помогает человеку с этим состоянием мыслить, искать связи и предлагать следующие шаги.
