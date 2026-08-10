<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: zh-CN -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 实现状态：Crystal 与未来工作

**日期：** 2026-08-08  
**Checkpoint：** `bbd816c` / PR #337  
**Evidence：** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Machine-readable status：** [manifest](../status/implementation-manifest.json)

| Component | 状态 | 当前边界 |
|---|---|---|
| Guardian / TruthGate / strict read projection | 已实现 | storage/migration 不能绕过 authority |
| HTTP/CLI/MCP query boundary | 已实现 | 普通 query 不修改 Canon |
| SQLite backup/verify/inactive restore | 已实现并测试 | restore inactive，不是 admission |
| bounded SQLite logical export | 已实现并测试 | canonical backend-neutral bundle |
| PostgreSQL optional dependency/preflight | 已实现并测试 | explicit extra、lazy load |
| inactive PostgreSQL/pgvector import | 已实现并测试 | 新 inactive schema，无普通 I/O |
| exact target-state equivalence | 已实现并测试 | independent read-only re-hash |
| active PostgreSQL runtime adapter | 未实现 | target 不在 normal composition |
| automatic SQLite/PostgreSQL switching | 禁止 | availability/import success 不构成选择 |
| exact-vs-ANN evaluation | 未实现 | 后续独立 phase |
| cutover / rollback / dual-write | 未实现 | 后续显式 phase |
| PostgreSQL server lifecycle | 未实现 | backup/restore/upgrade/pooling 未来工作 |
| Reader Core / Semantic Reading Layer | 未实现 | admission 前的候选 layer |

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

issue #331 与 #332 已由 PR #335 和 #337 实现。PostgreSQL 仍是
`active=false` 的可选 operator path。成功 equivalence 不能激活 backend，
也不能改变 Guardian、TruthGate 或 strict Canon。

未来工作：

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal 不声称 active PostgreSQL backend、automatic migration、production
multi-tenancy、universal truth、zero hallucinations、legal/security certification
或 consciousness。
