<!-- translation-source: docs/GLOSSARY.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d4-locale: ru -->
# Crystal — глоссарий и руководство по дисциплине claims

**Дата статуса:** 10 августа 2026 года  
**Назначение:** authoritative English terminology source для D4 translations.  
**Authority:** merged implementation, executable tests, exact CI и подробные English contracts сильнее этой сводки.

## Имена контрактов

Programmatic identifiers остаются неизменными в code, schemas, CLI, APIs и переведённых документах.

| Термин | Значение и граница |
|---|---|
| **claim** | Типизированное утверждение. Claim не становится автоматически verified fact. |
| **admission** | Решение, позволяющее claim войти в более доверенное состояние или проекцию. |
| **Guardian** | Structural, safety и policy checks до epistemic admission; не замена TruthGate. |
| **TruthGate** | Контролируемая epistemic admission boundary; не универсальный detector истины. |
| **physical L3** | Multi-status graph-oriented storage и retrieval state. Storage membership не означает strict Canon membership. |
| **strict Canon** | Deny-dominant доверенная read projection, разрешённая текущими evidence и policy. |
| **CanonicalView** | Fail-closed read projection для grounded responses. |
| **TrustSnapshot** | Read-time trusted state view; не переписывает physical storage. |
| **TRACE** | Machine-readable grounding path, связывающий answer с admitted claims и evidence. |
| **Receipt** | Replayable, tamper-sensitive evidence операции или ответа. Migration receipt не является claim evidence. |
| **provenance** | Источник, путь создания и lifecycle claim или artifact. |
| **evidence span** | Source-linked passage, поддерживающий candidate или admitted claim. |
| **source status** | Класс происхождения claim, например external source, user statement или model output. |
| **epistemic state** | Типизированный статус, описывающий допустимое обращение с claim; не просто confidence score. |
| **grounding** | Связывание ответа с admitted claims, evidence и traceable sources. |
| **FactsPack** | Bounded traceable context для ответа; не владелец authority. |
| **read-only query** | Query contract, который не может менять facts, ESM, L3, outbox, episode links, embedder identity или candidate state. |
| **fail-closed** | Refusal или bounded failure вместо скрытого admission при неопределённых evidence, policy или state. |
| **storage profile** | Durable deployment identity для backend и non-secret locator; не epistemic authority. |
| **migration bundle** | Deterministic portable operation artifact для approved datasets; не whole-system truth export. |
| **exact equivalence** | Равенство counts, canonical bytes и hashes утверждённого dataset; не activation или retrieval acceptance. |
| **active=false** | PostgreSQL target неактивна и не может обслуживать обычные runtime reads/writes. |
| **baseline** | Работа, уже merged и независимо evidenced до funded agreement. |
| **funded delta** | Новая измеримая работа поверх frozen baseline, принимаемая через public evidence. |
| **deliverable** | Bounded public artifact с explicit acceptance evidence. |
| **local-first** | Данные и обычные операции по умолчанию остаются локальными; remote services опциональны. |
| **provider independence** | Models/providers — заменяемые interfaces и не владеют truth authority. |
| **restriction** | Технический предел использования или раскрытия stored material. |
| **erasure** | Удаление через реализованный active-store lifecycle; независимые копии требуют отдельной обработки. |
| **review queue** | Pending или blocked claims, ожидающие explicit curator action. |
| **curator override** | Атрибутированное audited human decision; не скрытый bypass TruthGate. |
| **Reader Core RC-1** | Реализованный/протестированный bounded evidence-linked source/session skeleton с source-version identity, locators, fidelity, coverage, bookmarks/open loops и stale/failure/privacy semantics; без truth/admission authority. |
| **Reader Core RC-2** | Реализованный/протестированный caller-supplied Structural Document Map с version-bound hierarchy/order и explicit ambiguity; не automatic parser и не truth/confidence authority. |
| **dedicated Reader Core** | Будущий multi-pass Semantic Reading runtime за пределами RC-1/RC-2; не реализован. |

## Термины, требующие осторожности

### «Truth» и «canonical graph»

Не пишите, что каждый graph node является истиной. Предпочтительная формулировка:

```text
physical L3 stores typed multi-status records
strict Canon is the evidence- and policy-allowed read projection
```

### «Implemented», «tested», «current» и «planned»

Используйте эти labels раздельно:

- **implemented** — merged code exists;
- **tested** — named executable evidence exists;
- **current** — reconciled against an exact source checkpoint;
- **planned / research** — no runtime claim.

Open PR, RFC, issue, prototype или Notion page не являются current runtime evidence.

### «Reader Core implemented»

Не сворачивайте текущие bounded milestones в claim о полной capability. Предпочтительная формулировка:

```text
RC-1 minimal evidence-linked skeleton = implemented/tested
RC-2 Structural Document Map          = implemented/tested
dedicated multi-pass Reader runtime   = not implemented
coverage                              != comprehension proof
structure/order/prominence            != epistemic authority
```

### «GDPR compliant», «secure» и «hardened»

Предпочтительная формулировка:

```text
GDPR-oriented technical controls
security-relevant checks
hardened against documented threats
```

Не заявляйте legal, GDPR или security certification без внешнего authoritative evidence.

### «Replay»

```text
Receipt replay    = re-check existing evidence
trajectory replay = repeat an execution path for evaluation
```

### «Grant funded» или «awarded»

Текущий публичный статус:

```text
submitted / under review / not awarded
```

Merged baseline work нельзя переименовывать в future funded delivery. Budget или award state может измениться только по verified external grant communication.

### «Default backend»

SQLite — ordinary active local-first profile. Первый durable `auto` может выбрать optional LadybugDB, если он доступен, иначе SQLite, после чего deployment identity фиксируется. Explicit Mock — development/CI state. PostgreSQL/pgvector — неактивная `active=false` import/equivalence target, не ordinary runtime.

## Правила перевода

- Сохраняйте code identifiers и contract names без изменений.
- Переводите объяснения, а не machine identifiers.
- Сохраняйте `physical L3 != strict Canon`.
- Сохраняйте public-query read-only и explicit-ingest write separation.
- Сохраняйте SQLite ordinary runtime и PostgreSQL `active=false`.
- Сохраняйте `import/equivalence != activation`.
- Сохраняйте различие RC-1/RC-2 bounded-implemented и dedicated-Reader-not-implemented.
- Сохраняйте `coverage != comprehension proof` и structure/order/prominence != epistemic authority.
- Сохраняйте no-certification и no-award boundaries.
- Не подразумевайте native-speaker editorial certification, если её не было.

## Связанные authoritative документы

- [Project, grant and governance summary](../PROJECT_GRANT_AND_GOVERNANCE.md)
- [Полная архитектура](../ARCHITECTURE.md)
- [Архитектурный контракт Reader Core](../architecture/READER_CORE_ARCHITECTURE.md)
- [Reader implementation status](../IMPLEMENTATION_STATUS.md)
- [Grant scope](../GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](../grants/baseline-funded-delta-matrix.md)
- [Funding use plan](../grants/funding-use-plan.md)
- [Roadmap](../../ROADMAP.md)
- [Governance](../../GOVERNANCE.md)
- [Contributing](../../CONTRIBUTING.md)
