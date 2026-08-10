<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: es -->
# Estado de implementación de Crystal

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

Guardian/TruthGate, el query boundary read-only y el lifecycle SQLite están implementados. El import PostgreSQL/pgvector inactivo está probado con `active=false`; no existe switching automático. RC-1 y RC-2 están implementados/probados como capas acotadas; el Reader multi-pass dedicado no está implementado.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
