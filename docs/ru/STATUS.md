<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- rc6-translation-source: docs/STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/STATUS.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
# 🇷🇺 Crystal — текущий статус

**Reader baseline:** signed `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` — RC-6 merged.  
**RC-7:** issue #371 / PR #372; русский source parity = `ab3ad31c437647535030e371d58f456faf14017b`.

```text
bbd816c09dd39a02e6de6c1014438490572f40f6
2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% line coverage
```

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
dedicated_reader_core = false
```

RC-1 = exact source/session; RC-2 = structure; RC-3 = explicit pass ledger; RC-4 = source-linked `EXTRACTED_PROPOSITION`; RC-5 = PRE-ADMISSION relations; RC-6 = bounded working sets + caller SUMMARY; RC-7 = explicit cross-document candidate links между current RC-4 candidates из разных documents.

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## RC-7 boundary

`core/reader_cross_document.py` принимает explicit extractor/session bindings и revalidates OPEN ReaderSession, current registered RC-4 candidate, `EXTRACTED_PROPOSITION`, exact SourceVersion/privacy, SegmentCard membership, completed pass, target/outcome, recovered RC-2 structure и current substantive coverage. Left/right `document_id` обязаны отличаться.

Kinds: `SUPPORTS`, `CONTRADICTS`, `ELABORATES`, `REFERENCES`, `DEFINES`, `EXAMPLE_OF`, `PREREQUISITE_FOR`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`. Symmetric: `CONTRADICTS`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`; остальные directional.

Exact session/candidate/pass/node/source/locator provenance и non-empty rationale сохраняются обеих сторон. Inspection basis descriptive only; нет similarity score, identity, confidence, evidence sufficiency, resolution или winner.

RC-7 не вызывает `core.evidence.attach_evidence()`, не меняет `truth_status`/ESM/Canon, не обходит Guardian/TruthGate, не делает automatic corroboration/contradiction resolution, embeddings/ANN/vector DB, LLM/provider/parser/OCR или PostgreSQL activation.

```text
physical L3 != strict Canon
Reader cross-document link != admitted evidence
cross-document contradiction candidate != confirmed contradiction
```

SQLite ordinary active local-first; PostgreSQL/pgvector `active=false`; automatic backend switching отсутствует. `HTTP /ask`, `CLI ask`, `MCP search` read-only.

RC-5 checkpoint `51c205fe048fd69d39fcd47b43e042a50de432bc`, RC-6 checkpoint `ed96a88369f841bdb2ffd79ca020acef174685fc` сохранены как история. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED`; D2 reviewer/safety translations remain current across all nine supported locales; Quick Start current all 9.

NLnet **submitted / under review / not awarded**; ~€50,000 planning only; budget change none. RC-7 pre-agreement merge станет existing baseline.
