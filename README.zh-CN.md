# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### 面向可信 AI 系统的、可验证的、本地优先的记忆、证据与决策基础设施

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 个已声明的 Ring Zero mutants 已消除** · ✅ **9 个永久 CI jobs** · 🐍 **默认 runtime 只依赖 Python 标准库** · ⚖️ **AGPL-3.0**

> Crystal 不是另一个聊天机器人，也不是一个自主的“真理预言机”。它是一条记忆、证据与决策边界：记录一个 claim 是什么、来自哪里、处于什么 epistemic state、是否可以支撑回答，以及矛盾如何通过明确、可审计的决定被处理。

**已验证 runtime checkpoint：** `bbd816c09dd39a02e6de6c1014438490572f40f6` — 已合并 PR #337。  
**已验证 head / CI：** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 成功。  
**PostgreSQL 集成：** `31256316532` — PostgreSQL 16 + pgvector 0.8.2。  
**主要证据：** [TEST_REPORT.md](./TEST_REPORT.md)、[STATUS.md](./docs/STATUS.md) 与[机器可读实现清单](./docs/status/implementation-manifest.json)。

> **翻译契约：** 本文件以完整的视觉与语义覆盖为目标，不是简短摘要。英语仍是主要工作来源与冲突裁决来源；其他稳定文档按阶段翻译。参见[本地化策略](./docs/LOCALIZATION_POLICY.md)与[翻译状态](./docs/TRANSLATION_STATUS.md)。

---

## 🎯 为什么需要 Crystal

许多 AI 系统把源文档、用户陈述、模型输出、假设、检索片段和长期记忆混在同一个上下文或向量库里。缺少明确边界时，语言流畅的文本会悄悄获得其证据并不支持的权威。

```text
表达流畅的 claim 不会自动变可信。
物理 graph node 不会自动成为 strict Canon。
retrieval score 不是 evidence。
model output 不是独立事实来源。
contradiction 不会自己选择赢家。
TopicFacet 标签不是真理裁决。
成功导入数据不等于 backend activation。
```

## 🧠 Crystal 提供什么

- 类型化 claims 与明确的 epistemic lifecycle；
- source identity、精确 evidence spans 与 provenance；
- Guardian 与 TruthGate admission boundaries；
- 与 strict Canon 分离的 multi-status physical L3 graph；
- 不可变、deny-dominant 的 `TrustSnapshot`；
- 只读的 HTTP、CLI 与 MCP 公共查询面；
- TRACE 与可重放、可检测篡改的 Receipts；
- restriction、erasure、audit 与 import sessions；
- review queues 与可恢复 review sessions；
- 不可变的 `ContradictionReport`；
- 明确的 `COEXIST`、`CONTEXTUALIZE`、`SUPERSEDE` 决定；
- scoped curator capabilities 与 process-local decision leases；
- 无真理权威的 advisory TopicFacet metadata；
- 确定性 evaluation、100% line coverage 与 Ring Zero mutation gate；
- 已验证的 SQLite backup/restore 与 bounded logical migration；
- 可选、inactive 的 PostgreSQL/pgvector import 与独立 exact-state equivalence。

## 🏛️ 三种架构视图

### 🧠 思维导图

```text
🧠 Crystal
├── 🎯 目标
│   ├── 面向 AI 的可验证记忆
│   ├── local-first 信任基础设施
│   └── 与证据绑定的回答与决定
├── 🏛️ 记忆模型
│   ├── L0 — 快速工作缓存
│   ├── L1 — 运行状态与 lifecycle
│   ├── L2 — 等待 / review 边界
│   └── L3 — 物理 multi-status graph
├── 🛡️ 信任边界
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 证据与审计
│   ├── source + exact span
│   ├── provenance
│   ├── TRACE
│   └── Receipt
├── ⚖️ Review 与矛盾
│   ├── queue / session
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ 存储
│   ├── SQLite — 普通 local-first profile
│   └── PostgreSQL/pgvector — inactive target
└── 📊 验证
    ├── Python 3.11 / 3.12
    ├── 100% coverage
    ├── mutation / security / Docker
    └── exact-head CI evidence
```

### 🏗️ 信息流

```text
📥 明确 ingest
        ↓
🧾 claim type + source + exact evidence span
        ↓
🧠 L0/L1 中的 observed state
        ↓
🛡️ Guardian → ⚖️ TruthGate → 🚧 restrictions
        ↓                         ↓
⏳ L2 review               🏛️ physical L3 graph
        └──────────────┬──────────┘
                       ↓
             📐 immutable TrustSnapshot
                       ↓
          🛡️ Guardian + CanonicalView STRICT
                  ↓                 ↓
          💬 grounded answer      🚫 grounded refusal
                  ↓
             🧾 replayable Receipt
```

### 🌳 模块树

```text
🌳 Crystal
├── 🧠 Memory：L0 / L1 / L2 / L3
├── 🛡️ Trust：Guardian / TruthGate / TrustSnapshot / CanonicalView
├── 📜 Evidence：Source / Span / Provenance / TRACE / Receipt
├── ⚖️ Review：Queue / Session / ContradictionReport / Disposition
├── 🔎 Query：HTTP / CLI / MCP
├── 🗄️ Portability：SQLite lifecycle / logical bundle / inactive PostgreSQL import
└── 📊 Verification：tests / coverage / mutation / security / Docker / docs-status
```

## 🧭 核心区别

```text
physical L3 graph    != strict Canon
query                != ingest
confidence           != independent evidence
LLM output           != independent factual source
contradiction detect != automatic winner
TopicFacet relevance != truth
migration receipt    != claim evidence
successful import    != backend activation
process-local lease  != distributed coordination
```

TruthGate 是 admission policy gate，不是能够独立知道客观真理的 oracle。Strict Canon 是在 evidence、status、ESM state、confidence shape 与 processing restrictions 上形成的 policy-allowed read projection。

## 🧱 记忆与证据表面

| 表面 | 作用 | 关键边界 |
|---|---|---|
| L0 | 进程内工作缓存 | 快速且可重建 |
| L1 | SQLite/WAL 运行记忆 | lifecycle、restrictions、pending work |
| L2 | 逻辑 review 边界 | 不会自动成为 Canon |
| L3 | 物理 multi-status memory | 存在记录不等于可信 |
| TrustSnapshot | 不可变 reconciliation | deny-dominant L1/L3 解析 |
| CanonicalView | strict grounding projection | 只允许 policy-approved reads |
| TRACE / Receipt | 证明与 replay | grounding、drift、tamper evidence |
| ContradictionReport | 不可变冲突对象 | confidence 不选择赢家 |
| TopicFacet | 导航 metadata | 不改变 truth、ESM 或 Canon |

## 🗄️ SQLite 与 PostgreSQL/pgvector

```text
SQLite
└── 当前普通 local-first runtime profile
    ├── reads / writes
    ├── backup / restore
    ├── lock recovery
    └── bounded canonical logical export

PostgreSQL 16 + pgvector
└── 可选 migration / equivalence profile
    ├── optional [postgresql] extra
    ├── lazy driver loading
    ├── new target schema
    ├── active=false
    ├── SERIALIZABLE import
    └── independent count / byte / SHA-256 equivalence
```

PostgreSQL target 不在普通 runtime composition 中，不能提供普通 reads/writes。成功 import 不意味着 activation、automatic selection、cutover、rollback、dual-write、TruthGate admission、strict Canon membership、ANN acceptance 或 production multi-tenancy。

## 🔎 Crystal 与经典 RAG

| 问题 | 经典 RAG | Crystal |
|---|---|---|
| 找到相关材料 | 核心优势 | 通过 retrieval adapters |
| 区分用户陈述与已验证事实 | 应用自行处理 | 显式 typed boundary |
| 跟踪 lifecycle 与矛盾 | 通常是外部逻辑 | first-class states 与 reports |
| 防止生成文本成为自己的来源 | 非内建 | Ring Zero invariant |
| 重放回答证据 | 可选 | TRACE 与 Receipt |
| 负责任地处理矛盾 | 应用自行处理 | authorized dispositions |
| 无强制 cloud/model provider | 视实现而定 | pure-stdlib local-first baseline |

## 🛡️ 公共只读边界

`HTTP /ask`、`HTTP /receipt`、`CLI ask`、`CLI receipt` 与 `MCP search` 共享 `core.query_pipeline`。它们不创建 facts、不迁移 ESM state、不写入 L3，也不改变 Canon。

## ⚖️ 明确的矛盾决定

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "这些陈述描述了不同上下文" \
  --expected-report-id REPORT_ID
```

当前 `CuratorLeaseRegistry` 只在单一进程内防止并发决定；分布式部署需要 external lease adapter。

## 🚀 快速开始

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

可选 inactive PostgreSQL 工具：`pip install -e '.[postgresql]'`。

## 📚 文档导航

- [简体中文索引](./docs/zh-CN/README.md)
- [English documentation map](./docs/DOCUMENTATION_MAP.md)
- [测试报告](./TEST_REPORT.md)
- [当前状态](./docs/STATUS.md)
- [实现状态](./docs/IMPLEMENTATION_STATUS.md)
- [架构](./docs/ARCHITECTURE.md)
- [安全策略](./SECURITY.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [本地化策略](./docs/LOCALIZATION_POLICY.md)
- [翻译状态](./docs/TRANSLATION_STATUS.md)

## ✅ 已验证基线

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
Mutation: 7/7
CI: 9/9
PostgreSQL integration: PostgreSQL 16 + pgvector 0.8.2 successful
```

## 🚧 声明边界

Crystal 不声明：普适客观真理检测、零 hallucinations、法律意义上的 GDPR/security certification、production-ready multi-tenancy、distributed locking、AGI 或 consciousness、active PostgreSQL runtime、automatic switching、cutover/rollback，或已完成的 dedicated Reader Core。NLnet proposal 仍为 **submitted / under review / not awarded**。

## 🤝 贡献与许可

参见 [CONTRIBUTING.md](./CONTRIBUTING.md)、[SECURITY.md](./SECURITY.md)、[GOVERNANCE.md](./GOVERNANCE.md) 与 [AGPL-3.0](./LICENSE)。
