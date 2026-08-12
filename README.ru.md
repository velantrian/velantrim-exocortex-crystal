<!-- localization-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-localization-source: main@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- localization-status: CURRENT -->
# 🔱 Velantrim ExoCortex — Crystal

> 🇷🇺 Русская Reader-поверхность `CURRENT` для RC-6. English остаётся primary source/conflict resolver.

### Проверяемая local-first память, evidence и decision-boundary инфраструктура

`v0.3.0` · 🎯 100% line-coverage gate · 🧬 Ring Zero · ✅ 9 permanent CI jobs · ⚖️ AGPL-3.0

Сохранённый runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6`.  
Исторический runtime evidence: **2078 passed / 13 skipped / 0 failed**, **9756 statements / 100.00% line coverage**.  
RC-6 English source: `ed96a88369f841bdb2ffd79ca020acef174685fc`.

Crystal не является чат-ботом или «оракулом истины». Он удерживает границы между source, candidate, evidence, admission и trusted read projection.

```text
source/document
→ Reader RC-1
→ RC-2 structure
→ RC-3 passes
→ RC-4 propositions
→ RC-5 relations
→ RC-6 working sets / SUMMARY
→ normal evidence/admission path
→ Guardian / TruthGate
→ physical L3 / TrustSnapshot / CanonicalView
```

## 🎯 Ключевые различия

```text
physical L3             != strict Canon
retrieval score         != evidence
model output            != independent factual source
Reader coverage         != comprehension proof
pass completion         != comprehension proof
working-set coverage    != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate  != confirmed contradiction
summary                 != source text
summary                 != evidence
summary                 != verified fact
summary                 != Canon admission
similarity              != identity
repetition              != corroboration
```

## 📖 Reader Core

| Stage | Реализованная bounded функция | Authority non-claim |
|---|---|---|
| RC-1 | exact SourceVersion / SourceLocator / ReaderSession | source-linked state, не truth |
| RC-2 | caller-supplied Structural Document Map | structure/order не confidence |
| RC-3 | explicit deterministic multi-pass ledger | completion не comprehension |
| RC-4 | source-linked proposition candidate | proposition не verified fact |
| RC-5 | typed relation candidates | suspicion не resolved contradiction |
| RC-6 | bounded working sets + caller SUMMARY | context/synthesis не evidence/admission |

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
dedicated_reader_core                  = false
```

### RC-4

RC-4 регистрирует caller-supplied normalized proposition только из `COMPLETED` RC-3 target с substantive `PROCESSED`/`REVISITED` coverage и exact RC-1/RC-2 provenance. `FACTUAL_ASSERTION` описывает presentation source, а не Crystal verification.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### RC-5

`core/reader_relations.py` принимает только IDs, уже зарегистрированные одним RC-4 extractor, и требует один OPEN ReaderSession + exact SourceVersion.

| Relation | Direction | Meaning |
|---|---|---|
| POSSIBLE_CONTRADICTION | symmetric | только suspicion |
| TENSION | symmetric | tension без truth verdict |
| EXCEPTION | directional | right ограничивает left |
| QUALIFICATION | directional | right уточняет left |

Relation сохраняет exact candidate/pass/node IDs, primary/supporting locators и explicit rationale. RC-5 не вызывает `core.evidence.attach_evidence()`, не пишет fact evidence, не меняет `truth_status`/ESM/Canon и не выбирает winner.

### RC-6

`core/reader_long_context.py` решает long-context задачу архитектурно, без утверждения об infinite model context.

Перед planning RC-6 revalidates:

| Проверка | Требование |
|---|---|
| session | OPEN |
| source | exact SourceVersion |
| fidelity | EXTRACTED_PROPOSITION |
| card | registered identity |
| pass | COMPLETED |
| structure | RECOVERED |
| coverage | PROCESSED / REVISITED |
| provenance | exact replayable locators |

Детерминированный порядок:

```text
RC-2 structural order
→ candidate_id lexical tie-break
```

Явные resource budgets:

```text
1 <= max_candidates_per_set <= 128
1 <= max_source_locators_per_set <= 512
```

Это **artifact/provenance budgets**, а не token/context-window guarantee. Candidate atomicity означает: candidate и все direct unique SourceLocator остаются в одном set. Oversized candidate → fail closed.

Matching RC-5 registry — optional context. Existing relation ID carried только если оба endpoints находятся в одном working set; cross-set relation не копируется и не выводится автоматически.

`SUMMARY` — только caller-supplied `SourceFidelity.SUMMARY`. Перед регистрацией current direct leaf provenance сравнивается с immutable working-set snapshot, затем leaves revalidate. Summary сохраняет direct RC-4 candidate IDs и replayable locators; summary-to-summary provenance-only chain запрещён.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

## 🏛️ Memory / authority

| Surface | Role | Boundary |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | operational SQLite | durable, не strict Canon автоматически |
| L2 | pending/review | не admission |
| L3 | physical multi-status graph | presence не trust |
| Guardian | safety/structure | admission boundary |
| TruthGate | admission policy | не objective oracle |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | trusted projection | grounding only |

```text
storage profile = deployment identity
migration bundle = operation evidence
physical L3 = multi-status storage
strict Canon = trusted read projection
```

## 🗄️ Storage

SQLite — ordinary active local-first. Проверенная portability line:

```text
SQLite backup
→ independent verify
→ inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import
→ independent exact equivalence
→ active=false
```

Successful import/equivalence не означает activation, cutover, rollback, dual-write, automatic backend switching или TruthGate admission.

## 🔎 Public query

```text
HTTP /ask
CLI ask
MCP search
```

Public query surfaces read-only. Они не создают facts и не превращают retrieval/model output в strict Canon.

## ⚖️ Contradictions

RC-5 `POSSIBLE_CONTRADICTION` не подтверждает конфликт и не выбирает сторону. Existing audited workflow требует explicit authorized disposition (`COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`). RC-6 может только carry existing relation ID как context.

```text
contradiction detection != winner selection
relation candidate != admitted evidence
RC-6 SUMMARY != contradiction evidence
```

## 🛡️ Safety / privacy / non-features

RC-1..RC-6 не удерживают source body. Restriction/sensitivity наследуются exact source context.

RC-6 не добавляет:

| Не-функция | Статус |
|---|---|
| automatic summarization | absent |
| LLM/provider/model routing | absent |
| parser/chunker/OCR/PDF layout | absent |
| embeddings/ANN/vector DB | absent |
| RC-7 cross-document identity | not started |
| Reader durable DB/API/CLI/worker | absent |
| truth/Canon/ESM writer | absent |
| evidence admission | absent |
| contradiction winner | absent |
| PostgreSQL activation | absent |

## 🌍 Localization

Russian root + D1/D3/D4/D5 RC-6 semantics are `CURRENT` against `ed96a88369f841bdb2ffd79ca020acef174685fc`. Immutable RC-5 marker `51c205fe...` остаётся в metadata как audit history. D2 source remains `b7e6574dd7aefa2f32783ab79054fac6b3b4109f`; D2 and Quick Start are CURRENT in all 9 locales. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED`: **64 documents**.

## 🎓 Grant

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: under review
award: not awarded
budget change: none
```

Приблизительно €50,000 — planning only, не approved budget/payment commitment. RC-0..RC-5 already existing pre-agreement baseline. Если RC-6 merged до agreement, он также становится existing baseline и не может повторно считаться future funded delta.

## 🚧 Не заявляется

```text
AGI / consciousness                   = not claimed
universal truth / zero hallucinations = not claimed
active PostgreSQL runtime             = not implemented
automatic backend switching           = not implemented
dedicated/full autonomous Reader      = not implemented
automatic LLM Reader summarization    = not implemented
RC-7 cross-document reading           = not started
legal/GDPR/security certification     = not claimed
```

## 🚀 Быстрый старт

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 Навигация

| Документ | Ссылка |
|---|---|
| Quick Start | [docs/ru/QUICKSTART.md](./docs/ru/QUICKSTART.md) |
| Status | [docs/ru/STATUS.md](./docs/ru/STATUS.md) |
| Implementation | [docs/ru/IMPLEMENTATION_STATUS.md](./docs/ru/IMPLEMENTATION_STATUS.md) |
| Architecture | [docs/ru/ARCHITECTURE_OVERVIEW.md](./docs/ru/ARCHITECTURE_OVERVIEW.md) |
| Storage/Authority | [docs/ru/STORAGE_AND_AUTHORITY_BOUNDARIES.md](./docs/ru/STORAGE_AND_AUTHORITY_BOUNDARIES.md) |
| Grant | [docs/ru/GRANT_OVERVIEW.md](./docs/ru/GRANT_OVERVIEW.md) |
| Glossary | [docs/ru/GLOSSARY.md](./docs/ru/GLOSSARY.md) |
| Extended | [docs/ru/EXTENDED_REFERENCE_GUIDE.md](./docs/ru/EXTENDED_REFERENCE_GUIDE.md) |
| Localization policy | [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) |
| Translation status | [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md) |

GitHub signed merged `main` + executable tests + exact CI = implementation truth. Notion синхронизируется только после successful exact post-merge CI.
