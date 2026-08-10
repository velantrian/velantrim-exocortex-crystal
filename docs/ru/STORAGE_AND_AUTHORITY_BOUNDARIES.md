<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Хранилище и границы authority

physical L3 ≠ strict Canon. Retrieval, migration и Reader artifacts не обходят Guardian/TruthGate. Публичный `core.query_pipeline.query()` read-only. PostgreSQL target `active=false`; import success ≠ activation.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

RC-1/RC-2 не хранят source body и не имеют Canon/ESM/planner authority. Структурный порядок — metadata, а не truth/confidence.
