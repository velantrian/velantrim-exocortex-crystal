# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — 权威来源](./README.md) · 🇨🇳 **简体中文概览**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### 面向可信 AI 系统的可验证、本地优先记忆基础设施

本文件是**简短、非权威的导览摘要**，不是完整文档翻译。工程决策、架构、状态、
安全和资助声明均以英文维护。如有差异，以 [README.md](./README.md) 和英文证据为准。

`v0.3.0` · 🧪 **2078 通过 / 13 跳过** · 🎯 **100.00% 覆盖率** · ✅ **9 个 CI 任务**

**已验证 runtime checkpoint：** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337。

Crystal 将物理存储、证据、认识论准入和可信读取分离。数据存在、检索排名或迁移成功
都不能绕过 Guardian、TruthGate 或严格 Canon 的协调过程。

## 已验证范围

- 类型化主张、来源追踪和精确原文片段；
- Guardian 与 TruthGate 准入边界；
- 不可变的 `TrustSnapshot` 与 `CanonicalView` 读取；
- 只读公共 HTTP、CLI 和 MCP 查询；
- TRACE、收据、限制、擦除及明确的矛盾处理决定；
- SQLite 作为普通本地优先配置；
- 经验证的备份/恢复与资源有界逻辑导出；
- 可选 PostgreSQL/pgvector 导入至非活动目标 schema，并独立验证精确状态。

## 存储边界

```text
SQLite = 当前普通 local-first 配置
PostgreSQL + pgvector = 可选迁移目标
active=false
无普通 runtime reads/writes
无自动切换、cutover、rollback 或 dual-write
```

PostgreSQL 驱动仅通过 `[postgresql]` 安装，并且只由显式运维命令加载。成功导入只是运维
证据，不代表 activation，也不代表进入严格 Canon。

## 不可变语义边界

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal 不宣称普遍真理、零幻觉、活动 PostgreSQL runtime、生产级多租户、distributed
exactly-once、法律/GDPR/安全认证、Titan 集成或人工意识。

## 快速开始

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 当前英文证据

- [权威 README](./README.md)
- [验证报告](./TEST_REPORT.md)
- [当前状态](./docs/STATUS.md)
- [实现矩阵](./docs/IMPLEMENTATION_STATUS.md)
- [安全政策](./SECURITY.md)
- [本地化政策](./docs/LOCALIZATION_POLICY.md)
- [简体中文文档路径](./docs/zh-CN/README.md)

NLnet 申请已提交并处于审核中；不宣称已经获批或预算发生变化。
