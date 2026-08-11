<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
# 🇷🇺 Crystal — текущий статус

**Дата:** 2026-08-11  
**Сохранённый runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Evidence checkpoint:** 2078 passed / 13 skipped / 0 failed; 9756 statements / 100.00% line coverage.

GitHub merged `main`, executable tests и exact CI — implementation truth. Числа выше относятся к сохранённому storage/runtime checkpoint; Reader milestones имеют собственный exact-head/post-merge CI evidence.

## Reader machine truth

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

RC-5 работает поверх зарегистрированных RC-4 candidates в одном OPEN ReaderSession и одном exact SourceVersion. Relation kinds: `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION`. Обе стороны сохраняют exact candidate IDs и replayable primary/supporting provenance; rationale обязателен.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
coverage != comprehension proof
pass completion != comprehension proof
similarity != identity
repetition != corroboration
```

RC-5 не вызывает `core.evidence.attach_evidence()`, не пишет fact evidence, не меняет `truth_status`/ESM/strict Canon, не обходит Guardian/TruthGate, не повышает confidence и не выбирает winner. Automatic semantic equivalence/cross-document identity отсутствует.

## Storage

SQLite — ordinary active local-first. PostgreSQL/pgvector остаётся inactive target с `active=false`. RC-5 не добавляет Reader schema migration и backend switching.

## Localization

Русский D1/D3/D4/D5 и root README имеют `CURRENT` относительно `51c205fe048fd69d39fcd47b43e042a50de432bc`. Остальные восемь Reader-dependent locale surfaces — `REFRESH_NEEDED`; D2/Quick Start current во всех девяти.

## Grant

NLnet: submitted / under review / not awarded. Около €50,000 — planning only; budget change none. RC-5, merged pre-agreement, становится existing baseline.
