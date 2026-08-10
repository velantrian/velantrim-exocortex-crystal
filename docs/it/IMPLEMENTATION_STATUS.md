<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: it -->
# Stato di implementazione Crystal

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

Guardian/TruthGate, query read-only e lifecycle SQLite sono implementati. L’import PostgreSQL/pgvector inattivo è testato con `active=false`; switching automatico assente. RC-1 e RC-2 sono implementati/testati come layer bounded; il Reader multi-pass dedicato non è implementato.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
