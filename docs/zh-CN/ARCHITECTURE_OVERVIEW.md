<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: zh-CN -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal 架构概览

本译文用于导览。若存在冲突，以已合并代码、可执行测试、精确CI和英文合同为准。

## 核心模型

```text
来源 + 显式 ingest
→ provenance + 规范化
→ Guardian 检查
→ TruthGate 决策
→ 运行态 L1 + 多状态 physical L3
→ deny-dominant strict Canon 读取投影
→ read-only retrieval / 回答 / 有界拒答
```

记录存入physical L3并不等于进入strict Canon。Retrieval score、向量相似度和model output都不是独立证据。

## 记忆与审阅层

- **L0：** 进程内临时上下文。
- **L1：** 使用SQLite/WAL保存运行状态、证据、审计、receipts、import/review sessions和outbox。
- **L2：** 候选或隔离claim的pending/review staging，不是最终真值层。
- **L3：** 面向图的多状态存储，与strict Canon不同。
- **TrustSnapshot / CanonicalView：** deny-dominant可信读取界面。

## 读写分离

`HTTP /ask`、`CLI ask`和MCP通过`core.query_pipeline.query()`进行read-only查询。查询不能创建或强化事实，也不能改变ESM、L3、outbox、episode links或embedder identity。只有显式`ingest`能进入由Guardian和TruthGate控制的可写入接纳路径。

## 存储配置与可移植性

SQLite是普通active local-first profile。首次durable `auto`可以选择可选LadybugDB或SQLite，并锁定backend与非秘密locator identity。禁止静默退回临时Mock。

已验证的PostgreSQL/pgvector路径止于非活动目标：

```text
已验证SQLite bundle
→ 事务式PostgreSQL导入
→ 独立read-only重哈希
→ 精确等价
→ active=false
```

Import或equivalence不等于activation、backend selection、TruthGate admission、cutover、rollback或dual-write。PostgreSQL不在普通runtime composition中。

## 文档阅读

Source spans、document records、import sessions以及dry-run/review flows属于已实现baseline。带coverage maps、contradiction-aware rereading和document-level synthesis的专用multi-pass Reader Core尚未实现。

## 非声明

Crystal不声称AGI、意识、零幻觉、active PostgreSQL runtime、automatic switching、已接受的生产ANN、cutover/rollback/dual-write、安全/法律/GDPR认证或NLnet获批。

## 英文来源

- [完整架构](../ARCHITECTURE.md)
- [存储与权威边界](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [实现状态](../IMPLEMENTATION_STATUS.md)
- [非活动PostgreSQL导入](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
