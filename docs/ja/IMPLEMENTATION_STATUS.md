<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ja -->
# Crystal 実装状態

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

Guardian/TruthGate、read-only query boundary、SQLite lifecycle は実装済みです。PostgreSQL/pgvector inactive import は `active=false` で検証済み、automatic switching はありません。RC-1/RC-2 は bounded layer として実装・テスト済みで、dedicated multi-pass Reader は未実装です。

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
