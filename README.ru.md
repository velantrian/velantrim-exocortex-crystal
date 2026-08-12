<!-- localization-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-localization-source: main@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- localization-status: CURRENT -->
# 🔱 Velantrim ExoCortex — Crystal

> 🇷🇺 Русская Reader-поверхность `CURRENT` для RC-6. English остаётся primary source/conflict resolver.

### Проверяемая local-first память, evidence и decision-boundary инфраструктура

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐘 PostgreSQL/pgvector integration · ⚖️ AGPL-3.0

Сохранённый runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6`.  
Исторический runtime evidence: **2078 passed / 13 skipped / 0 failed**, **9756 statements / 100.00% line coverage**.  
RC-6 English source: `ed96a88369f841bdb2ffd79ca020acef174685fc`.

Crystal не чат-бот и не «оракул истины». Он удерживает provenance и authority boundaries так, чтобы source, model output, retrieval, Reader candidates, evidence и trusted read projection не смешивались автоматически.

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

## 🎯 Критические различия

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

## 📖 Reader Core RC-1 → RC-6

| Stage | Реализованная bounded функция | Authority boundary |
|---|---|---|
| RC-1 | exact SourceVersion / SourceLocator / ReaderSession | source-linked state, не truth |
| RC-2 | caller-supplied Structural Document Map | structure/order не confidence |
| RC-3 | deterministic explicit multi-pass ledger | completion не comprehension |
| RC-4 | source-linked EXTRACTED_PROPOSITION | candidate не verified fact/evidence |
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

### RC-4 — propositions

RC-4 принимает caller-supplied normalized proposition только из `COMPLETED` RC-3 target с substantive `PROCESSED`/`REVISITED` outcome и matching current RC-1/RC-2 provenance. `FACTUAL_ASSERTION` описывает source presentation, не Crystal verification.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### RC-5 — relation candidates

`core/reader_relations.py` принимает только IDs, реально зарегистрированные одним RC-4 extractor, и требует один OPEN ReaderSession + exact SourceVersion.

| Relation | Тип | Смысл |
|---|---|---|
| POSSIBLE_CONTRADICTION | symmetric | только suspicion |
| TENSION | symmetric | tension без truth verdict |
| EXCEPTION | directional | right ограничивает left |
| QUALIFICATION | directional | right уточняет left |

Relation сохраняет обе стороны, exact candidate/pass/node IDs, primary/supporting SourceLocator и explicit rationale. RC-5 не вызывает `core.evidence.attach_evidence()`, не пишет fact evidence, не меняет `truth_status`/ESM/Canon и не выбирает winner.

```text
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

### RC-6 — bounded long-context strategy

`core/reader_long_context.py` решает long-context задачу архитектурно, а не заявлением об infinite model context.

Перед planning каждый direct RC-4 leaf проходит revalidation:

| Проверка | Требование |
|---|---|
| session | OPEN ReaderSession |
| source | exact SourceVersion |
| fidelity | EXTRACTED_PROPOSITION |
| card | registered SegmentCard identity |
| pass | COMPLETED |
| structure | RECOVERED |
| coverage | PROCESSED / REVISITED |
| provenance | exact replayable locator |

Порядок детерминирован:

```text
RC-2 structural order
→ candidate_id lexical tie-break
```

Working-set budgets:

```text
1 <= max_candidates_per_set <= 128
1 <= max_source_locators_per_set <= 512
```

Это **artifact/provenance budgets**, не model-token/context-window guarantee. Candidate atomicity требует держать один RC-4 candidate и все direct unique locators вместе. Если leaf один превышает declared locator budget, planning fail closed.

Matching RC-5 registry — optional context only. Existing relation ID переносится только когда **оба** endpoints уже находятся в одном set. Cross-set relation не копируется и не выводится заново.

Caller может зарегистрировать `SourceFidelity.SUMMARY`. Перед registration immutable working-set leaf snapshot сравнивается с current direct RC-4 locators, затем leaves revalidate. Summary хранит direct candidate IDs и replayable source provenance. Другой summary не может быть единственным provenance path.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

RC-6 не генерирует summary автоматически и не получает truth/confidence/evidence-sufficiency/resolution/winner authority.

## 🏛️ Memory / authority

| Surface | Role | Boundary |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable, но не strict Canon автоматически |
| L2 | pending/review | candidate state |
| L3 | physical multi-status graph | storage presence не trust |
| Guardian | structure/safety | admission boundary |
| TruthGate | admission policy | не objective oracle |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | trusted projection | grounding surface |
| TRACE / Receipt | audit/replay | evidence trail, не admission authority |

```text
storage profile = deployment identity
migration bundle = operation evidence
physical L3 = multi-status storage
strict Canon = trusted read projection
```

## 🗄️ SQLite и PostgreSQL

SQLite остаётся ordinary active local-first. Проверенная portability chain:

```text
SQLite backup
→ independent verify
→ inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import
→ independent exact equivalence
→ active=false
```

Successful import/equivalence не означает activation, automatic switching, cutover, rollback, dual-write, TruthGate admission или strict Canon membership.

| Storage claim | Current truth |
|---|---|
| SQLite ordinary active | yes |
| PostgreSQL import/equivalence | bounded optional path |
| PostgreSQL active runtime | no |
| automatic SQLite/PostgreSQL switching | no |
| Reader RC-6 storage schema | no |

## 🔎 Public read-only query

```text
HTTP /ask
CLI ask
MCP search
```

Public query surfaces read-only. Они не создают facts, не выполняют ingest и не превращают retrieval/model output в trusted Canon.

## ⚖️ Contradiction workflow

RC-5 `POSSIBLE_CONTRADICTION` не подтверждает contradiction и не выбирает truth side. Existing audited workflow требует explicit authorized disposition: `COEXIST`, `CONTEXTUALIZE` или `SUPERSEDE`. RC-6 может лишь carry existing relation ID как context внутри set.

```text
contradiction detection != winner selection
Reader relation != resolved contradiction
RC-6 SUMMARY != contradiction evidence
```

## 🛡️ Safety, privacy и non-features

RC-1..RC-6 не удерживают source body. Derived artifacts inherit restriction/sensitivity exact source context.

| Не-функция | RC-6 |
|---|---|
| automatic summarization | absent |
| NLP/LLM/provider/model routing | absent |
| parser/chunker/OCR/PDF layout | absent |
| embeddings/ANN/vector DB | absent |
| semantic identity | absent |
| RC-7 cross-document reading | not started |
| Reader durable DB | absent |
| Reader public API/CLI/worker | absent |
| evidence admission | absent |
| truth/ESM/Canon writer | absent |
| contradiction winner | absent |
| PostgreSQL activation | absent |

## 🌍 Localization

Russian root + Reader-dependent D1/D3/D4/D5 RC-6 semantics are `CURRENT` against `ed96a88369f841bdb2ffd79ca020acef174685fc`. Immutable RC-5 source marker `51c205fe048fd69d39fcd47b43e042a50de432bc` сохранён как audit history.

D2 source остаётся `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`; D2 и Quick Start CURRENT across all 9 supported locales. Eight other Reader-dependent locale packs сохраняют rich translations как `REFRESH_NEEDED`: **64 documents**.

## 🎓 Grant truth

**NLnet: submitted / under review / not awarded.**

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: under review
award: not awarded
budget change: none
```

Приблизительно €50,000 — planning only, не approved budget/payment commitment. RC-0..RC-5 — existing pre-agreement baseline. Если RC-6 merged до agreement, он тоже existing baseline и не может повторно считаться future funded delta.

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

## 🚀 Quick Start

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

GitHub signed merged `main` + executable tests + exact CI = implementation truth. Notion синхронизируется только после exact post-merge CI.
