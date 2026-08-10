<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: fr -->
# Statut d’implémentation Crystal

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

Guardian/TruthGate, queries read-only et lifecycle SQLite sont implémentés. L’import PostgreSQL/pgvector inactif est testé avec `active=false`; le switching automatique est absent. RC-1 et RC-2 sont implémentés/testés comme couches bornées; le Reader multi-pass dédié n’est pas implémenté.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
