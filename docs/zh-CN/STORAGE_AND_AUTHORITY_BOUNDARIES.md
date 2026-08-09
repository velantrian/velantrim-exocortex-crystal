<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: zh-CN -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# 存储与权威边界

## 分离的身份

```text
storage profile = 部署身份
physical L3 = 多状态图数据
strict Canon = 可信读取投影
migration bundle = 操作完整性证据
retrieval score = 排序信号
model output = 生成文本
```

任何一种身份都不会自动授予另一种身份的权威。

## durable profile

SQLite是普通active local-first profile。首次durable `auto`可选择可选LadybugDB或SQLite，并锁定backend及非秘密locator。后续冲突fail-closed。Mock仅作为显式development/CI状态。

## physical L3与strict Canon

physical L3可包含VERIFIED、USER_CLAIMED、UNVERIFIED、HYPOTHESIS、SUBJECTIVE、contested、superseded或restricted记录。strict Canon是根据当前证据和policy形成的deny-dominant projection。存储、retrieval或高分均不足以获得信任。

## 读取与写入

公共查询通过`core.query_pipeline.query()`以read-only方式运行。显式`ingest`才是可写入的接纳路径，Guardian和TruthGate随后施加结构与认识论边界。

## SQLite生命周期与迁移

已实现backup、独立验证、inactive restore、有界确定性logical export和bundle验证。批准的physical-L3 datasets可导入新的inactive PostgreSQL schema并进行精确比较；目标保持`active=false`。

这不是对全部L1、audit/outbox、加密元数据、配置或独立副本的whole-system migration。不存在active PostgreSQL runtime、ANN acceptance、automatic switching、cutover、fencing、rollback或dual-write。

## 秘密与副本

密码、token、私钥和含凭据DSN不得写入profiles、bundles、receipts、logs、GitHub或Notion。Backups、exports和migrations会生成额外副本；从active store删除并不会自动删除它们。选定L1字段加密不等于通用加密。

## 操作证据

| 事件 | 能证明 | 不能证明 |
|---|---|---|
| L3记录 | 物理持久化 | strict Canon成员资格 |
| retrieval结果 | 候选相关性 | 证据充分性 |
| 已验证backup | backup完整性 | claim真实性 |
| 成功import | import完整性 | activation或runtime selection |
| exact equivalence | 批准datasets相等 | 生产就绪或cutover |

专用Reader Core尚未实现；NLnet仍为submitted / under review / not awarded。

## 详细英文合同

- [完整架构](../ARCHITECTURE.md)
- [Durable Storage Profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Migration Contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
