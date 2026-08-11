# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- localization-status: CURRENT -->

### Проверяемая local-first инфраструктура памяти, evidence и decision boundaries для надёжных ИИ-систем

`v0.3.0` · 🧪 сохранённый runtime checkpoint: **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 permanent CI jobs** · 🐘 PostgreSQL/pgvector — только optional inactive target · ⚖️ AGPL-3.0

> Crystal — не чат-бот и не автономный «оракул истины». Он разделяет источник, Reader-наблюдения, proposition/relation candidates, evidence admission, canonical truth и read-only grounding так, чтобы одно не получало authority другого без явного проверяемого перехода.

**Сохранённый runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`.  
**Reader foundation:** RC-1 → RC-2 → RC-3 → RC-4 → RC-5 реализованы как bounded PRE-ADMISSION слои.  
**Dedicated/full autonomous Reader:** не реализован.  
**Grant:** `submitted / under review / not awarded`; около €50,000 — только planning, не approved budget.  
**Политика локализации:** [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) · [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Зачем нужен Crystal

В типичной AI/RAG-системе документ, слова пользователя, retrieved fragment, model output, hypothesis и долговременная memory могут незаметно смешаться. Crystal строит между ними явные границы.

```text
source statement        != verified fact
segment                 != claim
summary                 != evidence
importance              != truth
retrieval score         != authority
model output             != source truth
Reader observation       != Canon admission
Reader coverage          != comprehension proof
Reader pass completion   != comprehension proof
EXTRACTED_PROPOSITION    != verified fact
Reader candidate         != admitted evidence
relation candidate       != admitted evidence
contradiction candidate  != confirmed contradiction
cross-document similarity != identity
repetition               != corroboration
```

RC-5 добавляет не «истину о конфликте», а только audit-ready подозрение о связи между уже существующими RC-4 candidates.

## 📖 Reader Core: пять bounded слоёв

```text
RC-0 architecture contract
        ↓
RC-1 exact SourceVersion / SourceLocator / ReaderSession
        ↓
RC-2 caller-supplied Structural Document Map
        ↓
RC-3 explicit deterministic multi-pass mechanics
        ↓
RC-4 source-linked EXTRACTED_PROPOSITION candidates
        ↓
RC-5 explicit relation candidates
        ↓
normal evidence/admission path остаётся отдельным
```

Machine truth:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

### RC-1 — evidence-linked skeleton

`core/reader_core.py` хранит identity/version источника, replayable locator, `SegmentCard`, fidelity, coverage, bookmarks/open loops и состояние ReaderSession. Source body не сохраняется. Изменение SHA/version делает прежний Reader-контекст stale вместо молчаливого reuse.

### RC-2 — Structural Document Map

`core/reader_structure.py` моделирует caller-supplied hierarchy/order: document, section/subsection, paragraph, dialogue turn, list/list item, table/table region, code block, quotation, notes, references, figure/caption. Состояния структуры: `RECOVERED`, `AMBIGUOUS`, `UNSUPPORTED`.

```text
structure/order/prominence != truth/confidence authority
```

Автоматического parser/chunker/OCR/PDF-layout/image understanding здесь нет.

### RC-3 — explicit multi-pass mechanics

Поддерживаются пять pass kinds:

```text
ORIENTATION
BROAD_READ
FOCUSED_READ
CROSS_CHECK
TARGETED_REREAD
```

Pass заранее получает declared RC-2 targets и фиксирует `ATTEMPTED`, `COMPLETED`, `INTERRUPTED` или `DEGRADED`. Для каждого target требуется explicit coverage outcome. `CROSS_CHECK` и `TARGETED_REREAD` требуют prior substantive processing; targeted reread требует rationale.

```text
pass completion != comprehension proof
```

### RC-4 — source-linked proposition extraction

`core/reader_extraction.py` принимает caller-supplied normalized proposition только из `COMPLETED` RC-3 target, где и pass outcome, и current matching coverage равны `PROCESSED` либо `REVISITED`.

Candidate сохраняет source owner, presentation category, explicit negation, scope/exception qualifiers, primary/supporting exact locators и inherited restriction/sensitivity.

Source-presentation categories:

```text
FACTUAL_ASSERTION
AUTHOR_OPINION
HYPOTHESIS
CONDITIONAL
EXAMPLE
QUOTED_SPEECH
REPORTED_POSITION
DEFINITION
UNCERTAIN_ASSERTION
```

`FACTUAL_ASSERTION` означает только способ подачи источника. Это не Crystal verification verdict.

### RC-5 — relation candidates

`core/reader_relations.py` принимает **только candidate IDs, реально зарегистрированные одним RC-4 `ReaderPropositionExtractor`**, следовательно остаётся внутри одного OPEN `ReaderSession` и одного exact `SourceVersion`.

| Relation kind | Что фиксирует Reader | Направление | Чего не доказывает |
|---|---|---|---|
| `POSSIBLE_CONTRADICTION` | подозрение на возможный конфликт | symmetric | confirmed contradiction |
| `TENSION` | напряжение между формулировками | symmetric | false/true side |
| `EXCEPTION` | right candidate — exception к left | directional | automatic override |
| `QUALIFICATION` | right candidate уточняет/сужает left | directional | truth promotion |

Каждая relation хранит `relation_id`, session identity, оба exact RC-4 candidate IDs, pass/node IDs, primary/supporting source provenance обеих сторон и explicit non-empty rationale.

Для symmetric kinds порядок пары детерминирован по candidate ID. Повторная регистрация той же пары fail-closed и не превращается в corroboration. `EXCEPTION` и `QUALIFICATION` сохраняют направление.

```text
POSSIBLE_CONTRADICTION
        !=
confirmed contradiction
        !=
resolved contradiction / winner
```

RC-5 не сравнивает raw source text семантически и не вычисляет similarity proof. Cross-document Reader stage не добавлен.

## 🔐 Authority firewall

```text
Reader RC-1..RC-5
        │
        ├── no truth_status / ESM mutation
        ├── no strict Canon write
        ├── no Guardian / TruthGate bypass
        ├── no core.evidence.attach_evidence()
        ├── no evidence sufficiency
        ├── no confidence promotion
        ├── no contradiction winner
        ├── no semantic identity inference
        └── no planner / belief-update authority
```

RC-5 artifact не содержит truth probability, confidence, evidence-sufficiency, resolved или winner fields. Существующий contradiction workflow остаётся отдельной authority surface.

## 🏛️ Архитектура и память

```text
🧠 Reader foundation
├── RC-1 provenance/fidelity/coverage
├── RC-2 structure
├── RC-3 pass ledger
├── RC-4 proposition candidates
└── RC-5 relation candidates

🏛️ Memory / trust
├── L0 — ephemeral working state
├── L1 — durable operational SQLite state
├── L2 — pending/review boundary
├── L3 — physical multi-status graph/storage
├── Guardian
├── TruthGate
├── TrustSnapshot
└── CanonicalView
```

| Поверхность | Роль | Authority boundary |
|---|---|---|
| Reader RC-1 | exact source/session artifacts | observation ≠ truth |
| Reader RC-2 | structural address space | structure ≠ confidence |
| Reader RC-3 | reading-process audit | completion ≠ comprehension |
| Reader RC-4 | proposition candidate | extracted ≠ verified |
| Reader RC-5 | relation candidate | contradiction candidate ≠ confirmed contradiction |
| L0 | рабочее состояние | ephemeral |
| L1 | operational state | durable, но не автоматически strict Canon |
| L2 | pending/review | требует admission/review |
| L3 | physical storage | multi-status ≠ strict Canon |
| TrustSnapshot | deny-dominant reconciliation | read policy surface |
| CanonicalView | trusted grounding projection | policy/evidence constrained |

## 🛡️ Read/write separation

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
TrustSnapshot / CanonicalView
     ↓
read-only answer / bounded refusal
```

Отдельно:

```text
explicit ingest / evidence
     ↓
Guardian
     ↓
TruthGate
     ↓
L1 + physical L3
     ↓
strict read projection
```

Reader RC-5 не соединяет эти пути обходным способом.

## 🗄️ Storage truth

```text
SQLite
└── ordinary active local-first runtime
    ├── normal reads/writes
    ├── backup / verify / inactive restore
    └── bounded logical export

PostgreSQL 16 + pgvector
└── optional inactive migration/equivalence target
    ├── lazy optional dependency
    ├── fresh inactive target schema
    ├── exact state verification
    └── active=false
```

Import/backend support != runtime activation. RC-5 не добавляет Reader DB schema migration и не активирует PostgreSQL.

## ⚖️ Contradiction governance

```text
RC-5 relation candidate
        ↓
(no automatic promotion)
        ↓
normal source/evidence/admission workflow
        ↓
ContradictionReport / review machinery
        ↓
explicit authorized disposition
```

Reader не выбирает победителя и не маркирует одну сторону false.

## 🚀 Быстрый старт

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optional PostgreSQL tooling устанавливается отдельно; обычный local-first runtime от него не зависит.

## 🌍 Localization truth

Русский root README и Reader-dependent D1/D3/D4/D5 surfaces полностью обновлены к immutable English source checkpoint `51c205fe048fd69d39fcd47b43e042a50de432bc` и имеют `CURRENT`. D2 и Quick Start остаются `CURRENT` во всех девяти locale, потому что RC-5 не меняет их source semantics.

Остальные восемь locale сохраняют богатые предыдущие переводы и честно остаются `REFRESH_NEEDED`. Их нельзя заменять короткими summary только ради формального статуса. Tracked Reader/root translation debt остаётся 64 docs.

## 💶 Grant boundary

```text
submitted proposal != awarded grant
planning amount     != approved budget
pre-agreement merge != future funded delta
```

NLnet остаётся `submitted / under review / not awarded`; около €50,000 — planning only; budget change = none. RC-0/RC-1/RC-2/RC-3/RC-4/RC-5, если merged до agreement, являются existing baseline и не могут позже повторно считаться funded delta.

## 🚧 Что по-прежнему отсутствует

- dedicated/full autonomous Semantic Reader;
- automatic NLP/LLM proposition или contradiction extraction;
- model/provider routing внутри Reader;
- automatic parser/chunker, OCR, PDF layout reconstruction, multimodal image understanding;
- embeddings, ANN, Reader vector DB;
- automatic cross-document semantic identity;
- automatic contradiction resolution/winner selection;
- autonomous research planner или belief update;
- public Reader API/CLI/background worker;
- durable Reader database schema;
- active PostgreSQL runtime/automatic backend switching;
- legal/security/GDPR certification;
- awarded NLnet funding.

## 📚 Текущие источники

- [Статус](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture overview](./docs/ARCHITECTURE_OVERVIEW.md)
- [Reader Core architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Storage and authority boundaries](./docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Roadmap](./ROADMAP.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
