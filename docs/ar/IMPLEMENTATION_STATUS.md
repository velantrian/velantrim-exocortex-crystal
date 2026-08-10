<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ar -->
# حالة تنفيذ Crystal

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

Guardian/TruthGate وحدود الاستعلام read-only ودورة SQLite منفذة. استيراد PostgreSQL/pgvector غير النشط مختبر مع `active=false` ولا يوجد switching تلقائي. RC-1 وRC-2 منفذان ومختبران كطبقتين محدودتين، بينما الـReader المخصص multi-pass غير منفذ.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```
