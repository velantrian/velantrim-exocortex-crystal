<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: de -->
# Implementierungsstatus Crystal

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

- Guardian/TruthGate und read-only Query Boundary: implementiert.
- SQLite-Lifecycle: implementiert.
- Inaktiver PostgreSQL/pgvector-Import: implementiert/getestet, `active=false`.
- Automatisches Backend-Switching: nicht vorhanden.
- RC-1 evidence-linked Skeleton: implementiert/getestet.
- RC-2 Structural Document Map: implementiert/getestet.
- Dedicated multi-pass Reader / Semantic Reading runtime: nicht implementiert.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
