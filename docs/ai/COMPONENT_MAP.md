# Crystal AI Component Map

**Status date:** 2026-08-11

## Reader chain

| Layer | Runtime | Input authority | Output | Epistemic authority |
|---|---|---|---|---|
| RC-1 | `core/reader_core.py` | exact `SourceVersion` | Reader source/session artifacts | none |
| RC-2 | `core/reader_structure.py` | RC-1 source/version | declared structure | none |
| RC-3 | `core/reader_passes.py` | RC-1 session + RC-2 map | explicit pass ledger/coverage | none |
| RC-4 | `core/reader_extraction.py` | completed substantive RC-3 target | `EXTRACTED_PROPOSITION` candidate | none |
| RC-5 | `core/reader_relations.py` | valid registered RC-4 candidates, one session/version | typed relation candidate | none |

RC-5 kinds: `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION`.

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

## Authority components

- Guardian — admission structural/safety boundary;
- TruthGate — epistemic admission policy;
- TrustSnapshot / CanonicalView — strict read projection;
- evidence subsystem — fact evidence/admission path, separate from Reader;
- contradiction report/review/disposition — explicit resolution workflow, separate from RC-5 candidate suspicions.

## Storage components

- SQLite — ordinary active local-first;
- logical migration — verified bounded export;
- PostgreSQL/pgvector — inactive target with `active=false`;
- no automatic backend switching.

## Non-connections by design

`core/reader_relations.py` depends only on lower Reader layers (`reader_core`, `reader_extraction`). It does not import evidence admission, contradiction resolution, Guardian, TruthGate or ESM modules and introduces no LLM/provider/parser/embedding/DB dependency.
