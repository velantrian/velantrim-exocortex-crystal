<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-translation-source: docs/STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->
# Velantrim Crystal — текущий статус RC-6

Сохранённый runtime evidence: **2078 passed / 13 skipped / 0 failed**, **9756 statements / 100.00% line coverage**. SQLite ordinary active local-first; PostgreSQL target `active=false`.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
dedicated_reader_core = false
```

RC-6 использует deterministic bounded working sets над registered RC-4 leaves; `max_candidates_per_set <= 128`, `max_source_locators_per_set <= 512`, candidate atomicity. Caller-supplied SUMMARY сохраняет direct leaf provenance.

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
summary != verified fact
```

RC-6 не делает evidence admission, truth/ESM/Canon mutation, contradiction resolution, automatic summarization, LLM/provider/parser/OCR, embeddings/ANN, RC-7 cross-document reading, Reader persistence/API/worker или PostgreSQL activation.

Русский RC-6 parity привязан к `ed96a88369f841bdb2ffd79ca020acef174685fc`; восемь других Reader packs остаются `REFRESH_NEEDED` (64 docs). NLnet `submitted / under review / not awarded`; ~€50,000 planning only; budget change none.
