<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->
# Статус реализации Crystal

2078 passed / 13 skipped / 0 failed · 9756 statements / 100.00% line coverage.

| Компонент | Статус |
|---|---|
| Guardian / TruthGate / strict projection | Реализовано |
| Read-only HTTP/CLI/MCP query boundary | Реализовано |
| SQLite lifecycle | Реализовано |
| Inactive PostgreSQL/pgvector import | Реализовано и протестировано, `active=false` |
| Automatic SQLite/PostgreSQL switching | Запрещено / отсутствует |
| Reader Core RC-1 | Реализован bounded evidence-linked skeleton |
| Reader Core RC-2 | Реализован bounded Structural Document Map |
| Dedicated multi-pass Reader Core / Semantic Reading Layer | Не реализован |

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

Reader не может писать strict Canon, менять truth_status/ESM, обходить Guardian/TruthGate или получать planner authority. Нет parser/OCR, LLM/provider, embeddings/ANN/vector DB или multi-pass orchestration.
