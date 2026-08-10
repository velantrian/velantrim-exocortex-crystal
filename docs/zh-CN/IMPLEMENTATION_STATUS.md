<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: zh-CN -->
# Crystal 实现状态

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage。

Guardian/TruthGate、read-only query boundary 和 SQLite lifecycle 已实现。PostgreSQL/pgvector inactive import 已在 `active=false` 下测试；没有 automatic switching。RC-1 与 RC-2 作为 bounded layer 已实现并测试；dedicated multi-pass Reader 尚未实现。

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
