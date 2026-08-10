<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ja -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 実装状態: Crystal と将来作業

**日付:** 2026-08-08  
**Checkpoint:** `bbd816c` / PR #337  
**Evidence:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Machine-readable status:** [manifest](../status/implementation-manifest.json)

| Component | 状態 | 現在の境界 |
|---|---|---|
| Guardian / TruthGate / strict read projection | 実装済み | storage/migration は authority を回避不可 |
| HTTP/CLI/MCP query boundary | 実装済み | 通常 query は Canon を変更しない |
| SQLite backup/verify/inactive restore | 実装・検証済み | restore は inactive、admission ではない |
| bounded SQLite logical export | 実装・検証済み | canonical backend-neutral bundle |
| PostgreSQL optional dependency/preflight | 実装・検証済み | explicit extra、lazy load |
| inactive PostgreSQL/pgvector import | 実装・検証済み | 新規 inactive schema、通常 I/O なし |
| exact target-state equivalence | 実装・検証済み | independent read-only re-hash |
| active PostgreSQL runtime adapter | 未実装 | normal composition に未登録 |
| automatic SQLite/PostgreSQL switching | 禁止 | availability/import success は選択でない |
| exact-vs-ANN evaluation | 未実装 | 後続の独立 phase |
| cutover / rollback / dual-write | 未実装 | 後続の明示 phase |
| PostgreSQL server lifecycle | 未実装 | backup/restore/upgrade/pooling は将来 |
| Reader Core / Semantic Reading Layer | 未実装 | admission 前の候補 layer |

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

issue #331/#332 は PR #335/#337 で実装済みです。PostgreSQL は `active=false` の任意
operator path です。equivalence 成功は backend を activate せず、Guardian、
TruthGate、strict Canon を変更しません。

将来作業:

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal は active PostgreSQL backend、自動 migration、production multi-tenancy、
universal truth、zero hallucinations、法務/security certification、consciousness を
主張しません。
