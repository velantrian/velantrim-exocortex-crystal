<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-translation-source: docs/IMPLEMENTATION_STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->
# Implementation Status — Reader RC-6

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
dedicated_reader_core = false
```

RC-6 runtime: `core/reader_long_context.py`; tests: `tests/test_reader_long_context.py`. Working sets сохраняют exact session/source, RC-4 candidate IDs, structural node IDs и direct replayable locators. Budgets bounded 128 candidates / 512 locators; это не model-token guarantee. Matching RC-5 relation carried только при in-set endpoints. SUMMARY caller-supplied only и direct-provenance preserving.

```text
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
summary != verified fact
summary != Canon admission
```

RC-1, RC-2, RC-3, RC-4, RC-5 и RC-6 не дают admission authority. SQLite active local-first; PostgreSQL `active=false`. Нет automatic summarization, RC-7, evidence/Canon/ESM write, contradiction winner, LLM/provider/parser/OCR/embedding/ANN, Reader DB/API/worker.

Russian RC-6 source: `ed96a88369f841bdb2ffd79ca020acef174685fc`. NLnet `submitted / under review / not awarded`; ~€50,000 planning only; budget change none.
