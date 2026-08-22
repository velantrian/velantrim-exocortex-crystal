# 🌐 Velantrim Ecosystem / Экосистема Velantrim

> **Document type:** navigation and integration-boundary map.  
> **Authority:** orientation only; this document does not authorize runtime integration, data transfer, shared Canon writes or capability inheritance.  
> **Crystal lifecycle:** **V1 COMPLETE / 100% / FREEZE-STABILITY / P0=0 / P1=0**.  
> **Atlas rule:** live owning repositories and owning Current State records override this navigation map for volatile implementation facts.

## English

### Crystal's role

**Velantrim Exo-Cortex — Crystal** is the trusted local-first memory/evidence kernel of the wider Velantrim ecosystem. V1 is complete and in freeze/stability. Crystal provides evidence admission, provenance/lineage, bounded canonical writes, Guardian/TruthGate boundaries, TRACE, receipts, local persistence/recovery and auditable replay.

```text
Being part of the Velantrim ecosystem
!= depending on every Velantrim project
!= sharing one runtime or one Canon
!= transferring authority between domains
!= claiming an integration that has not been implemented and tested
```

### Six-project Atlas topology

| Project | Primary role | Relationship to Crystal |
|---|---|---|
| [💠 Crystal](https://github.com/velantrian/velantrim-exocortex-crystal) | Trusted local-first memory/evidence, provenance, bounded Canon writes, integrity and receipts | This repository; **V1 COMPLETE / FREEZE-STABILITY** |
| [🗿 Titan](https://github.com/velantrian/Velantrim-ExoCortex-Titan) | Orchestration, providers/models/tools, retrieval composition, adapters, benchmarks and research incubation | Separate orchestration/research owner; cannot promote research into Crystal authority automatically |
| [🧬 Native Kernel](https://github.com/velantrian/velantrim-native-kernel) | Technology-neutral semantic laws, invariants and reference contracts | Separate semantic-constitution owner; specification does not grant Crystal runtime authority |
| [🌀 Mentaury Soul](https://github.com/velantrian/velantrim-mentaury-soul) | Bounded cognition/identity: claims, beliefs, self, relationships and commitments | Crystal evidence may be transported only through bounded admitted contracts; evidence is not belief or identity |
| 🪁 Mentaury Kernel | Cross-domain composition specifications, compatibility, provenance preservation and non-escalation | Specification/composition layer only; not a central online authority server |
| 🌎 Continuum | Falsifiable process-continuity research across lost/replaced inference/context/runtime | Research/shadow domain; pilot or continuity hypothesis does not become Crystal evidence or authority automatically |

### Conceptual relationship map

```text
                         🗺️ VELANTRIM KNOWLEDGE ATLAS
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
       💠 Crystal                 🗿 Titan              🧬 Native Kernel
   evidence / trust          orchestration / R&D       semantic laws
             │                        │                        │
             ├──────────────┐         │         ┌──────────────┤
             ▼              ▼         ▼         ▼              ▼
        🌀 Soul        🪁 Mentaury Kernel              🌎 Continuum
 cognition/identity     composition specs          continuity research

All cross-domain arrows mean bounded contracts/proposals only.
They do not imply shared Canon, authority inheritance or current runtime wiring.
```

### Cross-domain authority law

```text
SOURCE DOMAIN
    │ proposes / transports
    ▼
AdmissionRequest
    │
    ▼
TARGET-DOMAIN validation
    ├── DENY → DecisionReceipt
    └── ALLOW → CapabilityLease
                     │
                     ▼
                bounded use
                     │
                     ▼
              ConsumptionReceipt
```

A source domain cannot grant itself permission to mutate a target domain. Target-domain-authorized authority decides ALLOW/DENY. Integration is not authority transfer.

### Mandatory boundaries

1. Each project keeps its own implementation truth, tests, lifecycle status and authority boundary.
2. Titan, Native Kernel, Soul, Mentaury Kernel and Continuum receive no automatic write authority over Crystal.
3. Crystal evidence or receipts do not automatically become Soul belief/identity state.
4. Soul cognition/identity output does not automatically become Crystal Canon.
5. Mentaury Kernel composition is specification, not central authorization.
6. Continuum research/pilot output is not evidence or production authority by default.
7. Shared vocabulary, contracts or research inspiration do not imply shared ownership.
8. Any future authority-impacting integration requires explicit bounded contracts, validation, auditability and owner authorization.
9. Research documents, open PRs, Notion pages and CI success are not equivalent to runtime/production authorization.

### Crystal stop boundary

Crystal V1 completion does not authorize V1.x/V2, Reader expansion, GraphRAG, semantic/hybrid/vector runtime, PostgreSQL/pgvector activation, EITI/EPIS runtime integration, distributed sync or central authority routing. Future work requires a separate explicit owner decision.

---

## Русский

### Роль Crystal

**Velantrim Exo-Cortex — Crystal** — trusted local-first ядро памяти и доказательств в экосистеме Velantrim. **V1 завершён на 100% и находится в FREEZE / STABILITY; P0=0, P1=0.** Crystal отвечает за admission evidence, provenance/lineage, ограниченные записи Canon, Guardian/TruthGate, TRACE, Receipts, локальное хранение/восстановление и проверяемый replay.

```text
Принадлежность к Velantrim
!= единый монолит
!= единый runtime
!= единый Canon
!= наследование authority
!= автоматически реализованная интеграция
```

### Шесть owning-проектов Atlas

| Проект | Основная роль | Отношение к Crystal |
|---|---|---|
| 💠 Crystal | Trusted memory/evidence, provenance, bounded Canon, integrity, receipts | Этот репозиторий; **V1 COMPLETE / FREEZE-STABILITY** |
| 🗿 Titan | Orchestration, providers/models/tools, retrieval composition, adapters, benchmarks, incubation | Отдельный research/orchestration owner; исследования не получают Crystal authority автоматически |
| 🧬 Native Kernel | Технологически нейтральные semantic laws и invariants | Отдельная semantic constitution; spec != implementation |
| 🌀 Mentaury Soul | Claims, beliefs, self/identity, relationships, commitments | Evidence Crystal != belief/identity Soul; перенос только через bounded admitted contracts |
| 🪁 Mentaury Kernel | Cross-domain composition, compatibility, provenance preservation, non-escalation | Specification-only; не центральный сервер authority |
| 🌎 Continuum | Исследование process continuity и recovery/rehydration | Research/shadow; pilot != evidence и не даёт Crystal authority |

### Закон междоменной authority

Источник может только **предложить или транспортировать** данные. Право изменения целевого домена определяется целевым доменом через bounded admission/lease/receipt contract. Интеграция не означает перенос власти.

### Обязательные границы

1. Каждый проект сохраняет собственную implementation truth и authority boundary.
2. Ни один соседний проект не получает автоматического права записи в Crystal.
3. Evidence/Receipt Crystal не становятся автоматически belief или identity Soul.
4. Output Soul не становится автоматически Crystal Canon.
5. Mentaury Kernel задаёт composition rules, но не является центральным authority router.
6. Continuum остаётся исследованием continuity; pilot и hypothesis не равны evidence.
7. Общий словарь и shared contracts не означают общего владельца или общего Canon.
8. Любая authority-impacting интеграция требует явного bounded contract, проверки, аудита и owner authorization.
9. Research, Notion, открытый PR или зелёный CI не равны production/runtime authorization.

### Stop boundary Crystal

V1 завершён. Автоматического следующего milestone нет. V1.x/V2, GraphRAG, semantic/hybrid Reader, PostgreSQL/pgvector, EPIS/EITI runtime, distributed sync и central authority routing остаются неавторизованными до отдельного решения владельца.
