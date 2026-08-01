# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### 面向可信 AI 系统的可验证、本地优先记忆基础设施

`v0.3.0` · 🧪 **1853 项测试通过 / 12 项跳过** · 🎯 **100% 覆盖率** · 🧬 **7/7 个声明的变异体被检出** · ✅ **9 个 CI 任务** · 🐍 **默认运行时仅依赖 Python 标准库** · ⚖️ **AGPL-3.0**

> Crystal 不是另一个聊天机器人，而是一条记忆、证据与决策边界。它记录
> 一条陈述是什么、来自哪里、处于何种认知状态、能否作为回答依据，以及
> 矛盾是如何通过明确决定得到处理的。

**已验证的运行时检查点：** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — 已合并 PR #302。  
**精确证据：** [TEST_REPORT.md](./TEST_REPORT.md) 与
[机器可读实现清单](./docs/status/implementation-manifest.json)。

> 本译文与英文 README 保持相同的功能、安全和状态边界。稳定的 API 标识符
> 保留代码中的原名，说明文字则使用自然中文表达。

---

## 🎯 为什么需要 Crystal

许多 AI 系统会把源文档、用户陈述、模型输出、假设、检索片段和持久记忆
混在同一上下文或向量库中。这样一来，表达流畅的文字可能获得其证据并不
支持的权威性。

```text
表达有说服力，不等于可信。
图中的节点，不等于严格 Canon。
检索分数，不等于证据。
模型输出，不等于独立来源。
矛盾不会自行选出赢家。
主题标签不是事实真伪判定。
```

## 🧠 主要能力

- 类型化陈述与明确的认知生命周期；
- 来源、证据片段和溯源元数据；
- Guardian 与 TruthGate 准入边界；
- 与严格 Canon 分离的多状态物理 L3 图；
- 不可变、拒绝优先的 `TrustSnapshot` 读取协调；
- 严格只读的公开 HTTP、CLI 与 MCP 查询；
- TRACE 与可重放、可检测篡改的 Receipt；
- 处理限制、删除、审计和导入会话控制；
- 审核队列与可恢复审核会话；
- 类型化、不可变的矛盾报告；
- 明确的 `COEXIST`、`CONTEXTUALIZE` 与 `SUPERSEDE` 决定；
- 通过 CLI 和已认证 HTTP 进行冲突处理；
- 受 scope 限制的策展角色/权限与进程内 decision lease；
- 不赋予权威的多标签主题 facet；
- 从运行时转换派生的机器可读 ESM 规范；
- 确定性评估、100% 行覆盖与 Ring Zero mutation gate；
- 带版本化产物的 L3 基准历史。

## 🏛️ 架构概览

```text
显式 ingest
→ 陈述分类 + 证据元数据
→ L0/L1 中的 Observed 状态
→ Guardian → TruthGate → 限制/矛盾检查
→ 多状态物理 L3 图

公开查询
→ 只读 retrieval
→ 不可变 TrustSnapshot
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ 回答 / 拒绝 / Receipt

未解决的矛盾
→ 不可变 ContradictionReport
→ actor/角色/scope 授权 + decision lease
→ 策展者明确决定 + 原因
→ 可审计的 canonical 写入路径

主题导航
→ 建议性 TopicFacet
→ 仅用于筛选/分组 — 不会准入 Canon
```

```text
物理 L3 图 ≠ 严格 Canon
query ≠ ingest
confidence ≠ 独立证据
LLM 输出 ≠ 独立事实来源
主题相关性 ≠ 真值
本地 lease ≠ 分布式协调保证
```

TruthGate 是准入策略门，而不是独立判断客观真理的预言机。严格 Canon 是
根据证据、状态、ESM 和处理限制形成的、由策略允许的读取投影。

## 🛡️ 公开只读查询边界

`HTTP /ask`、`HTTP /receipt`、`CLI ask`、`CLI receipt` 和 `MCP search`
共同使用 `core.query_pipeline`。它们不会创建事实、转换 ESM、写入 L3、
处理 outbox，也不会初始化 embedding fingerprint。

详见 [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md)。

## ⚖️ 明确处理矛盾

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "这些陈述描述的是不同情境" \
  --expected-report-id REPORT_ID
```

在 FastAPI 中，`POST /review/resolve-conflict` 必须使用宿主应用的认证机制。
`core.curator_auth` 检查 actor、权限和 scope。`CuratorLeaseRegistry` 只能保护
单个进程；分布式部署必须提供外部 lease 适配器。

详见 [冲突处理接口](./docs/CONFLICT_RESOLUTION_SURFACES.md) 与
[主题 facet 和 curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md)。

## 🏷️ 建议性主题 facet

`core.topic_facets` 提供用于导航、筛选和分组的规范化标签。facet 分数只表示
主题相关性，不会改变 truth status、证据、ESM 或严格 Canon 成员资格。

## 🚀 快速开始

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 文档入口

- [文档地图](./docs/DOCUMENTATION_MAP.md)
- [当前状态](./docs/STATUS.md)
- [架构](./docs/ARCHITECTURE.md)
- [测试报告](./TEST_REPORT.md)
- [评估](./docs/EVAL.md)
- [NLnet 范围](./docs/GRANT_NLNET_SCOPE.md)

## ✅ 已验证基线

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 声明边界

Crystal 不声称能够普遍识别真理、完全消除幻觉、提供 GDPR 或安全认证、已具备
生产级多租户能力、实现人工意识或具备 Titan/Full ExoCortex 功能。当前 lease
仅在单进程内有效；分布式协调和外部身份提供方集成仍是独立工作。

## 🤝 参与与许可

参见 [CONTRIBUTING.md](./CONTRIBUTING.md)、[SECURITY.md](./SECURITY.md)、
[GOVERNANCE.md](./GOVERNANCE.md) 与 [AGPL-3.0](./LICENSE)。
