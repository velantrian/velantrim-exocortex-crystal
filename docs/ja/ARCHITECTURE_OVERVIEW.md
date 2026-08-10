<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ja -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# アーキテクチャ概要

source/version → RC-1 artifacts → RC-2 structure → Guardian → TruthGate → physical L3 → strict Canon。`core.query_pipeline.query()` は read-only、PostgreSQL は `active=false` です。

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

Reader の coverage/structure は epistemic authority ではありません。`coverage != comprehension proof`。
