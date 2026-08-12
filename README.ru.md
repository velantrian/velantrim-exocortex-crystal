<!-- localization-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-localization-source: main@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-localization-source: main@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- localization-status: CURRENT -->
<!-- rc7-status: CURRENT -->
# 🔱 Velantrim ExoCortex — Crystal

> 🇷🇺 Русская Reader-поверхность `CURRENT` для RC-7. English остаётся primary source и conflict resolver.

### Проверяемая local-first память, evidence и decision-boundary инфраструктура

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐘 PostgreSQL/pgvector integration · ⚖️ AGPL-3.0

**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`.  
**Retained tests:** `2078 passed / 13 skipped / 0 failed`; **9756 statements / 100.00% line coverage**.  
**Signed Reader baseline:** `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` — RC-6 merged; post-merge CI `31566408978` 9/9.  
**RC-7 English source checkpoint:** `ab3ad31c437647535030e371d58f456faf14017b`; exact checkpoint CI `31570690153` 9/9.

Crystal не чат-бот и не «оракул истины». Он удерживает provenance и authority boundaries так, чтобы source, model output, retrieval, Reader candidates, evidence и trusted read projection не смешивались автоматически.

```text
source/document
→ Reader RC-1
→ RC-2 structure
→ RC-3 passes
→ RC-4 propositions
├→ RC-5 within-source relations
├→ RC-6 working sets / SUMMARY
└→ RC-7 cross-document link candidates
→ normal evidence/admission path
→ Guardian / TruthGate
→ physical L3 / TrustSnapshot / CanonicalView
```

## 🎯 Критические неравенства

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
contradiction candidate != confirmed contradiction
summary                 != source text
summary                 != evidence
summary                 != verified fact
summary                 != Canon admission
cross-document link     != Canon relation
cross-document support  != admitted evidence
same-topic              != same proposition
possible-same-claim     != claim identity
similarity signal       != identity proof
repetition across sources != corroboration
similarity              != identity
repetition              != corroboration
```

## 📖 Reader Core RC-1 → RC-7

| Stage | Bounded функция | Authority boundary |
|---|---|---|
| RC-1 | exact SourceVersion / SourceLocator / ReaderSession | source-linked state, не truth |
| RC-2 | caller-supplied Structural Document Map | structure/order не confidence |
| RC-3 | deterministic explicit multi-pass ledger | completion не comprehension |
| RC-4 | source-linked EXTRACTED_PROPOSITION | candidate не verified fact/evidence |
| RC-5 | typed relation candidates | suspicion не resolved contradiction |
| RC-6 | bounded working sets + caller SUMMARY | context/synthesis не evidence/admission |
| RC-7 | explicit cross-document candidate links | comparison не identity/Canon relation |

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
```

### RC-4 — propositions

RC-4 принимает caller-supplied normalized proposition только из `COMPLETED` RC-3 target с substantive `PROCESSED`/`REVISITED` outcome и matching current RC-1/RC-2 provenance. `FACTUAL_ASSERTION` описывает source presentation, а не Crystal verification.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### RC-5 — relation candidates

`core/reader_relations.py` принимает IDs, реально зарегистрированные одним RC-4 extractor, и требует один OPEN ReaderSession + exact SourceVersion. `POSSIBLE_CONTRADICTION`, `TENSION` symmetric; `EXCEPTION`, `QUALIFICATION` directional. Exact candidate/pass/node IDs, primary/supporting SourceLocator и explicit relation rationale сохраняются.

```text
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

### RC-6 — bounded long-context strategy

`core/reader_long_context.py` решает long-context задачу архитектурно. RC-6 уже merged в signed `main@1f5129d3276af28608b16e369fd38d21fe38c0d5`.

Перед planning каждый direct RC-4 leaf revalidated: OPEN session, exact source, `EXTRACTED_PROPOSITION`, registered card, `COMPLETED` pass, `RECOVERED` structure, current `PROCESSED`/`REVISITED` coverage и exact replayable locator.

```text
RC-2 structural order
→ candidate_id lexical tie-break
```

```text
1 <= max_candidates_per_set <= 128
1 <= max_source_locators_per_set <= 512
```

Candidate atomicity удерживает proposition и все direct unique locators вместе. RC-5 relation IDs — optional context only, если оба endpoints уже в одном set. Caller-supplied `SourceFidelity.SUMMARY` сохраняет direct RC-4 leaf provenance; summary-to-summary shortcut не создаётся.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

### RC-7 — bounded cross-document candidate links

Runtime: `core/reader_cross_document.py`. RC-7 связывает **только явно указанные caller'ом** current RC-4 proposition candidates из **разных document identities**. Это не automatic semantic matcher.

Перед регистрацией обе стороны повторно проверяются:

| Проверка | Fail-closed требование |
|---|---|
| session | обе ReaderSession OPEN |
| candidate | current registered RC-4 ID |
| fidelity | EXTRACTED_PROPOSITION |
| source | exact SourceVersion + privacy binding |
| card | SegmentCard identity зарегистрирован |
| pass | COMPLETED и тот же session/source |
| target/outcome | target declared; PROCESSED/REVISITED |
| structure | node RECOVERED + exact replay key |
| coverage | current substantive coverage + locator |
| documents | left.document_id != right.document_id |

```text
SUPPORTS
CONTRADICTS
ELABORATES
REFERENCES
DEFINES
EXAMPLE_OF
PREREQUISITE_FOR
SAME_TOPIC
POSSIBLE_SAME_CLAIM
```

`CONTRADICTS`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM` — symmetric candidates и canonicalize side order по exact source/session/candidate sort key. Остальные kinds directional и сохраняют left/right meaning.

Каждый link сохраняет exact left/right `session_id`, `candidate_id`, `pass_id`, `node_ids`, exact `SourceVersion`, primary/supporting `SourceLocator`, non-empty rationale и optional descriptive `inspection_basis`.

Inspection basis: `EXPLICIT_SOURCE_REFERENCE`, `CALLER_COMPARISON`, `LEXICAL_SIMILARITY_SIGNAL`, `SHARED_TOPIC_SIGNAL`, `OTHER`. Это причина сравнения, не similarity score, confidence или identity proof.

```text
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 не делает automatic semantic matching, entity resolution, claim dedupe, corroboration, contradiction winner selection или evidence admission.

## 🏛️ Memory / authority

| Surface | Role | Boundary |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable, не strict Canon автоматически |
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
Reader cross-doc link = pre-admission comparison candidate
```

## 🗄️ SQLite и PostgreSQL

SQLite ordinary active local-first. Проверенная portability chain:

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
| Reader RC-7 storage schema | no |

## 🔎 Public read-only query

```text
HTTP /ask
CLI ask
MCP search
```

Public query surfaces read-only: не создают facts, не выполняют ingest и не превращают retrieval/model output в trusted Canon.

## ⚖️ Contradiction workflow

RC-5 `POSSIBLE_CONTRADICTION` и RC-7 `CONTRADICTS` — candidate surfaces. Ни одна не подтверждает contradiction и не выбирает truth side. Existing audited workflow требует explicit authorized disposition: `COEXIST`, `CONTEXTUALIZE` или `SUPERSEDE`.

```text
contradiction candidate != confirmed contradiction
cross-document contradiction candidate != confirmed contradiction
Reader link != resolved contradiction
```

## 🛡️ Safety, privacy и non-features

RC-1..RC-7 не удерживают source body. Derived artifacts сохраняют restriction/sensitivity exact source context. Cross-document link `restricted=true`, если restricted хотя бы одна сторона; sensitivity labels остаются metadata, но не становятся score.

| Не-функция | RC-7 |
|---|---|
| automatic semantic matching | absent |
| automatic entity resolution / dedupe | absent |
| automatic corroboration | absent |
| NLP/LLM/provider/model routing | absent |
| parser/chunker/OCR/PDF layout | absent |
| embeddings/ANN/vector DB | absent |
| Reader durable DB | absent |
| Reader public API/CLI/worker | absent |
| evidence admission | absent |
| truth/ESM/Canon writer | absent |
| contradiction winner | absent |
| PostgreSQL activation | absent |

## 🌍 Localization

Исторический RC-5 source marker `51c205fe048fd69d39fcd47b43e042a50de432bc` и RC-6 marker `ed96a88369f841bdb2ffd79ca020acef174685fc` сохранены как audit trail. Русская RC-7 parity привязана к English source `ab3ad31c437647535030e371d58f456faf14017b`.

D2 source остаётся `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`; D2 reviewer/safety translations remain current across all nine supported locales. Quick Start CURRENT across all 9 supported locales. Eight other Reader-dependent locale packs сохраняют rich translations как `REFRESH_NEEDED`: **64 documents**.

## 🎓 Grant truth

**NLnet: submitted / under review / not awarded.**

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

Приблизительно €50,000 — planning only, не approved budget/payment commitment. RC-0..RC-6 — existing pre-agreement baseline. Если RC-7 merged до agreement, он тоже становится existing baseline и не может повторно считаться future funded delta.

## 🚧 Не заявляется

```text
AGI / consciousness                   = not claimed
universal truth / zero hallucinations = not claimed
active PostgreSQL runtime             = not implemented
automatic backend switching           = not implemented
dedicated/full autonomous Reader      = not implemented
automatic semantic/vector Reader      = not implemented
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
