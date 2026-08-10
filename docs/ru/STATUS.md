<!-- translation-source: docs/STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->
# Текущий статус Crystal

**Дата:** 10 августа 2026.  
Runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6`.

- 2078 passed / 13 skipped / 0 failed
- 9756 statements / 100.00% line coverage
- 9/9 постоянных CI jobs
- PostgreSQL/pgvector target остаётся `active=false`
- Проект подан в NLnet, находится на рассмотрении и не получил award.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

RC-1 — минимальный evidence-linked session/source skeleton. RC-2 — caller-supplied Structural Document Map. Полноценный multi-pass Reader, parser, LLM orchestration, embeddings/ANN/vector DB не реализованы. `coverage != comprehension proof`.
