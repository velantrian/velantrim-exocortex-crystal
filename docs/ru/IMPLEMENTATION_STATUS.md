<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- rc6-translation-source: docs/IMPLEMENTATION_STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/IMPLEMENTATION_STATUS.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
# 🇷🇺 Crystal — Implementation Status

**Signed Reader baseline:** `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` — RC-6 merged; exact post-merge CI `31566408978` 9/9.  
**RC-7 implementation:** issue #371 / PR #372; English source `ab3ad31c437647535030e371d58f456faf14017b`; checkpoint CI `31570690153` 9/9.

| Компонент | Статус | Boundary |
|---|---|---|
| RC-1 | implemented/merged | source/session skeleton |
| RC-2 | implemented/merged | caller-supplied structural map |
| RC-3 | implemented/merged | deterministic multi-pass mechanics |
| RC-4 | implemented/merged | `EXTRACTED_PROPOSITION` candidates |
| RC-5 | implemented/merged | typed same-source relation candidates |
| RC-6 | implemented/tested/merged | bounded working sets + caller SUMMARY |
| RC-7 | implemented/tested on PR branch; final merge evidence pending | explicit cross-document candidate links |
| Dedicated/full Reader | not implemented | `dedicated_reader_core=false` |

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

RC-4: `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`. RC-5: `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`; `relation candidate != admitted evidence`; `contradiction candidate != confirmed contradiction`.

RC-6 `core/reader_long_context.py`: structural order + candidate-ID tie-break, max 128 candidates / 512 locators, candidate atomicity, direct RC-4 provenance, caller `SUMMARY` only.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

RC-7 `core/reader_cross_document.py` / `tests/test_reader_cross_document.py`: 2..32 explicit `ReaderPropositionExtractor`, max 4096 links, different sessions/documents, current registered RC-4 leaves only. Revalidates exact SourceVersion/privacy, SegmentCard, completed pass, target/outcome, recovered structure and current substantive coverage.

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

Symmetric kinds: `CONTRADICTS`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`. Directional kinds сохраняют left/right. Exact session/candidate/pass/node/source/primary+supporting locator provenance сохраняется обеих сторон; duplicate semantic candidate fail closed.

Inspection basis (`EXPLICIT_SOURCE_REFERENCE`, `CALLER_COMPARISON`, `LEXICAL_SIMILARITY_SIGNAL`, `SHARED_TOPIC_SIGNAL`, `OTHER`) descriptive only, не score.

```text
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 не делает automatic semantic matching/entity resolution/dedupe, automatic corroboration, embeddings/ANN/vector DB, LLM/provider/parser/OCR, evidence admission, truth/ESM/Canon mutation, contradiction resolution/winner selection, planner authority, Reader DB/API/CLI/worker или PostgreSQL activation.

SQLite ordinary active local-first; PostgreSQL/pgvector `active=false`. NLnet **submitted / under review / not awarded**; ~€50,000 planning only; budget change none. Pre-agreement merged work — existing baseline.
