<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: hi -->
# Crystal implementation status

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

Guardian/TruthGate, read-only query boundary और SQLite lifecycle implemented हैं। PostgreSQL/pgvector inactive import `active=false` के साथ tested है; automatic switching नहीं है। RC-1 और RC-2 bounded layers के रूप में implemented/tested हैं; dedicated multi-pass Reader implemented नहीं है।

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
