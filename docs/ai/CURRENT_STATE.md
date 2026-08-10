# Crystal AI Current State

**Status date:** 2026-08-10

GitHub merged `main`, executable tests, exact CI and the machine-readable implementation manifest are implementation authority. Notion records synchronized strategy/history and never overrides GitHub evidence.

## Runtime / storage truth

- verified runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- Python 3.11/3.12: 2078 passed / 13 skipped / 0 failed;
- 9756 statements / 100.00% line coverage;
- SQLite remains ordinary active local-first;
- PostgreSQL/pgvector remains an inactive target with `active=false`;
- normal PostgreSQL runtime adapter and automatic backend switching remain absent.

## Reader truth

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

RC-1 implements the bounded evidence-linked source/session skeleton. RC-2 implements the bounded caller-supplied Structural Document Map. Neither may mutate truth_status/ESM, write strict Canon, bypass Guardian/TruthGate, resolve contradictions or create planner/belief-update authority. No automatic parser/OCR, Reader LLM/provider orchestration, embeddings/ANN/vector database or multi-pass/cross-document reasoning runtime is present. `coverage != comprehension proof`.

## Localization

Issue #341 D1 is complete and remains the localization tracking issue. D1 is current across all nine supported locale packs at `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`.

D2 reviewer/safety translations are current across all nine supported locales at `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`; the Reader milestones did not change D2 source semantics.

D3 is current across all nine supported locale packs at `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`: 18 architecture/storage documents plus nine indexes.

D4 is current across all nine supported locale packs at `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`: 18 project/grant/glossary documents plus nine indexes.

D5 is current across all nine supported locale packs at `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`: nine Extended Reference Guides plus nine indexes.

All nine root README translations are full-parity public presentations and are current against `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`. The ledger supports `REFRESH_NEEDED`, but the reconciled current inventory has none.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget or payment commitment. Budget change: none. Work merged before any agreement, including Reader RC-0/RC-1/RC-2 and this documentation reconciliation if merged pre-agreement, is existing baseline and cannot be counted again as future funded delta.

## Next Reader work

RC-3 / explicit multi-pass reading mechanics is the next candidate separately bounded Reader milestone. It is not started and has no implementation authority yet.
