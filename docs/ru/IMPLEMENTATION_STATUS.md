<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
# 🇷🇺 Crystal — граница реализации

| Компонент | Статус | Граница |
|---|---|---|
| Reader RC-1 | implemented | `core/reader_core.py` |
| Reader RC-2 | implemented | `core/reader_structure.py` |
| Reader RC-3 | implemented | `core/reader_passes.py` |
| Reader RC-4 | implemented PRE-ADMISSION | `core/reader_extraction.py` |
| Reader RC-5 | implemented PRE-ADMISSION | `core/reader_relations.py` |
| Dedicated/full Reader | not implemented | `dedicated_reader_core=false` |
| SQLite | ordinary active local-first | unchanged |
| PostgreSQL/pgvector | inactive target | `active=false` |

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

## RC-5 contract

`ReaderRelationRegistry` принимает только candidate IDs из одного `ReaderPropositionExtractor`. Он проверяет OPEN session, exact source version, session identity, supporting locator versions и наличие candidate SegmentCard в ReaderSession.

- symmetric: `POSSIBLE_CONTRADICTION`, `TENSION`;
- directional: `EXCEPTION`, `QUALIFICATION`;
- exact candidate IDs + pass/node IDs + primary/supporting locators обеих сторон;
- explicit rationale;
- telemetry — counts by relation kind, без truth probability.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

Нет truth/confidence/evidence-sufficiency/winner fields. Нет `core.evidence.attach_evidence()`, evidence spans write, Canon/ESM mutation, Guardian/TruthGate bypass или contradiction resolution.

RC-5 также не добавляет LLM/provider, parser/OCR/layout, embeddings/ANN, semantic equivalence, cross-document reasoning, planner, API/CLI/worker, durable Reader storage или PostgreSQL activation.
