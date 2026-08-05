# 🌐 Velantrim Ecosystem / Экосистема Velantrim

> **Document type:** navigation and integration-boundary map.  
> **Authority:** this document does not authorize runtime integration, data transfer, shared Canon writes, or capability inheritance.  
> **Languages:** English is primary for Crystal's public and grant-facing surface; the Russian companion text is included below. Other localizations may follow after the English/Russian contract is stable.

## English

### Crystal's role

**Velantrim ExoCortex — Crystal** is the grant-facing, verifiable-memory infrastructure track of the wider Velantrim ecosystem.

Crystal provides evidence-aware claims, provenance, epistemic states, Guardian and TruthGate boundaries, strict Canon projections, TRACE and replayable Receipts. Crystal remains independently usable and independently auditable.

```text
Being part of the Velantrim ecosystem
≠ depending on every Velantrim project
≠ sharing one runtime or one Canon
≠ claiming an integration that has not been implemented and tested
```

### Project map

| Project | Primary role | Current relationship to Crystal |
|---|---|---|
| [💎 Crystal](https://github.com/velantrian/velantrim-exocortex-crystal) | Verifiable memory, evidence, provenance, trust and audit boundaries | This repository; implemented grant-facing track |
| [🔱 Titan](https://github.com/velantrian/Velantrim-ExoCortex-Titan) | Broader Exo-Cortex research: cognition, orchestration, retrieval, tools and agent workflows | Separate research/runtime track; future adapters require independent review |
| [🧬 Native Kernel](https://github.com/velantrian/velantrim-native-kernel) | Long-horizon substrate-neutral memory and event-contract research | Independent architecture research; Crystal does not currently run on it |
| [⭐️ Mentaury Soul](https://github.com/velantrian/velantrim-mentaury-soul) | Digital individuality, identity continuity, relationships, commitments and governed development | Separate identity research; no direct Crystal-to-identity authority path |

### Conceptual relationship map

```text
                         🌐 VELANTRIM ECOSYSTEM
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
  ⭐️ Mentaury Soul            🔱 Titan                 💎 Crystal
 identity / continuity     cognition / tools       evidence / trust
 relationships / M3        orchestration           provenance / audit
          │                        │                        │
          └──────── proposed governed contracts ──────────┘
                                   │
                                   ▼
                         🧬 Native Kernel
                 substrate-neutral contract research

Dashed/proposed relationships are architectural possibilities,
not claims of current runtime wiring.
```

### Mandatory boundaries

1. Crystal keeps its own implementation truth, tests, release status and Canon boundary.
2. Titan, Native Kernel and Mentaury do not receive automatic write authority over Crystal.
3. Crystal outputs do not become Mentaury identity state or M3 commitments automatically.
4. No project may infer capabilities, credentials, consent or authority from another project's data.
5. Any future integration requires a scoped RFC/ADR, explicit contracts, threat and privacy review, tests, rollback, Receipts and operator approval.
6. Research documents, open pull requests and Notion plans are not equivalent to merged runtime implementation.

### Safe future integration pattern

```text
proposal
→ bounded interface contract
→ adapter in an isolated branch
→ deterministic tests
→ threat/privacy review
→ Offline Shadow or read-only evaluation
→ receipts and failure analysis
→ explicit approval
→ separately versioned integration
```

---

## Русский

### Роль Crystal

**Velantrim ExoCortex — Crystal** — грантовое и публичное направление проверяемой памяти внутри более широкой экосистемы Velantrim.

Crystal отвечает за утверждения с доказательствами, provenance, эпистемические состояния, границы Guardian и TruthGate, строгие проекции Canon, TRACE и воспроизводимые Receipts. При этом Crystal остаётся самостоятельным и независимо аудируемым проектом.

```text
Принадлежность к экосистеме Velantrim
≠ зависимость от всех проектов Velantrim
≠ единый runtime или единый Canon
≠ заявление о ещё не реализованной интеграции
```

### Карта проектов

| Проект | Основная роль | Текущее отношение к Crystal |
|---|---|---|
| [💎 Crystal](https://github.com/velantrian/velantrim-exocortex-crystal) | Проверяемая память, доказательства, provenance, доверие и аудит | Этот репозиторий; реализуемое грантовое направление |
| [🔱 Titan](https://github.com/velantrian/Velantrim-ExoCortex-Titan) | Более широкий Exo-Cortex: cognition, orchestration, retrieval, инструменты и агенты | Отдельное исследовательское/runtime-направление; будущие адаптеры требуют отдельной проверки |
| [🧬 Native Kernel](https://github.com/velantrian/velantrim-native-kernel) | Долгосрочное substrate-neutral исследование памяти и event-контрактов | Независимая архитектурная работа; Crystal сейчас не работает поверх Kernel |
| [⭐️ Mentaury Soul](https://github.com/velantrian/velantrim-mentaury-soul) | Цифровая индивидуальность, continuity, отношения, commitments и управляемое развитие | Отдельное исследование identity; прямой власти над identity у Crystal нет |

### Обязательные границы

1. Crystal сохраняет собственную истину реализации, тесты, release-status и границу Canon.
2. Titan, Native Kernel и Mentaury не получают автоматического права записи в Crystal.
3. Выход Crystal не становится автоматически identity-state или M3-обязательством Mentaury.
4. Ни один проект не наследует capabilities, credentials, consent или authority из данных другого проекта.
5. Любая будущая интеграция требует ограниченного RFC/ADR, явных контрактов, threat/privacy review, тестов, rollback, Receipts и одобрения оператора.
6. Research-документ, открытый PR или план в Notion не равен реализации, смерженной в `main`.

### Безопасная последовательность интеграции

```text
предложение
→ ограниченный контракт интерфейса
→ адаптер в изолированной ветке
→ детерминированные тесты
→ threat/privacy review
→ Offline Shadow или read-only оценка
→ Receipts и анализ отказов
→ явное одобрение
→ отдельно версионируемая интеграция
```
