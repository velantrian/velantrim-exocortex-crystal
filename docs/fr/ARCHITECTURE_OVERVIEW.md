<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: fr -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Vue d’ensemble de l’architecture

source/version → RC-1 artifacts → RC-2 structure → Guardian → TruthGate → physical L3 → strict Canon. `core.query_pipeline.query()` est read-only; PostgreSQL reste `active=false`.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

La structure et la couverture Reader ne sont pas une autorité épistémique. `coverage != comprehension proof`.
