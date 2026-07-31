# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 **简体中文**   · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md)
> 📚 [德语文档](./docs/de/README.md) · [法语文档](./docs/fr/README.md) · [西班牙语文档](./docs/es/README.md) · [意大利语文档](./docs/it/README.md) · [俄语文档](./docs/ru/README.md) · [简体中文文档](./docs/zh-CN/README.md) · [التوثيق العربي](./docs/ar/README.md) · [日本語ドキュメント](./docs/ja/README.md)

### *面向可信 AI 的可验证、本地优先、开源记忆基础设施*

`v0.3.0` · 🧪 **1713 项通过 / 12 项跳过** · 🎯 **100% 覆盖率** · 🐍 **默认运行时仅依赖 Python 标准库** · ⚖️ **AGPL-3.0** · 🔒 **本地优先**

> Crystal 是可验证的记忆层，而不是另一个聊天机器人。每个 claim 都保留
> 来源、认识论状态和 provenance 元数据。自动进入 canonical graph 的过程
> 仍由 **Guardian + TruthGate** 管理。

> **权威来源：** GitHub `main` 中已合并的代码与英文规范文档决定实现状态和
> grant 范围。本简体中文版本是面向 reviewer、机构和中文贡献者的维护性翻译。
> 如有差异，以 [README.md](./README.md)、[docs/STATUS.md](./docs/STATUS.md)
> 和 [TEST_REPORT.md](./TEST_REPORT.md) 为准。

---

## 🧭 一分钟了解 Crystal

Crystal 是 Velantrim 面向公开 grant 的核心：

- 本地 L0/L1 operational memory；
- 本地 L3 canonical graph backend；
- Guardian 与 TruthGate admission control；
- 用于严格 grounding 的 `CanonicalView`；
- 可重放的 TRACE、provenance 与 Receipt；
- Evidence Span、review queue 与 import session；
- 与 GDPR 相关的技术性删除和处理限制机制；
- 确定性 evaluation 与 CI quality gate；
- 可选的 FastAPI 与 MCP 接口。

Crystal **不是** Titan、完整 Personal ExoCortex、自主认知操作系统、意识项目
或自我修改 agent。研究概念可进入未来 RFC，但不代表当前 runtime capability。

```text
GitHub Crystal main = 公开实现事实
Notion Crystal       = 同步的战略与 grant 地图
Titan / Full         = 独立研究轨道
```

---

## 🛡️ 当前信任边界

### Admission 路径

```text
输入 / 文档 / agent 事件
→ 分类与 evidence
→ Guardian + TruthGate
→ L0/L1 operational memory
→ 已准入的 L3 canonical graph
```

### HTTP 查询路径

已合并的 PR #265 引入了独立的严格只读 HTTP 查询合同：

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ 仅使用既有 Canon
→ CanonicalView
→ 回答或有界拒绝
```

对这些 HTTP surface，提问不会写入 L0/L1，不会转换 ESM，不会写入 L3 fact
或 edge，不会处理 outbox，不会记录 episode link，不会初始化 embedding
fingerprint，也不会改变 adaptive verification state。

### 明确披露的剩余范围

只读保证是精确而非泛化的：

- CLI `ask` 与 `receipt` 仍使用可执行 admission 的历史兼容路径；
- `core.pipeline.run()` 仍然可用；
- MCP 不提供显式 canonical write tool，但搜索可能初始化尚未设置的
  embedding fingerprint，因此不称为零变更路径。

详见 [read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md)。

---

## 🧠 记忆模型

| 层 | 角色 | 边界 |
|---|---|---|
| **L0** | 进程内工作缓存 | 快速、可重建 |
| **L1** | SQLite/WAL operational memory | 状态、限制与更新 |
| **L2** | pending claim 与 curator review | 不会自动成为 canonical |
| **L3** | canonical graph | 自动准入只能经过 TruthGate |
| **TRACE / Receipt** | proof layer | 解释 grounding 并检测 drift |

物理 graph 可以保存不同 truth status。严格意义上的 **Canon** 仅指 VERIFIED、
TRACE 有效且 policy 允许的投影，而不是 graph backend 中的每个节点。

---

## 🚀 快速开始

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

基础 CLI：

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

本地持久化且无额外依赖的 L3 backend：

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

详细步骤见 [docs/zh-CN/QUICKSTART.md](./docs/zh-CN/QUICKSTART.md)。

---

## 🔌 可选接口

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| 方法 | 路径 | 合同 |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | 经 Guardian + TruthGate admission |
| `POST` | `/ask` | 严格只读 canonical query |
| `GET` | `/receipt?q=...` | 只读 query 加 Receipt |
| `POST` | `/verify-receipt` | 对当前状态重放 Receipt |
| `GET` | `/evidence/{fact_id}` | 按 policy 输出 public evidence view |

FastAPI 与 Uvicorn 是可选 extra。默认 runtime 不要求 cloud service 或第三方
model provider。

### MCP

```bash
python -m core.mcp_server
```

MCP 提供面向检查的搜索、memory report、fact history、conflict lookup 与
Receipt verification 工具。上述 embedding fingerprint 剩余边界仍然适用。

---

## 🧪 Evaluation

Crystal 已包含确定性的 evaluation baseline：

- retrieval `hit@k` 与 MRR；
- TRACE 与 metadata 完整性；
- Evidence Span 覆盖率；
- Receipt replay survival；
- contradiction precision 与 recall；
- trust-boundary refusal check；
- CI regression floor 与 ceiling。

Titan 的确定性 replay 实现属于已审查的 prior art，而不是已复制到 Crystal
的 runtime。未来实现必须扩展现有 Crystal evaluation stack，保持 offline、
non-authoritative，并维持 baseline / funded delta 规则。

---

## 💶 Grant 边界

项目已提交至 **NLnet NGI0 Commons Fund** 评审。公开 repository **不声称**
资金已经获批。

```text
当前 BASELINE
    +
可测量的 FUNDED DELTA
    =
可独立验证的 DELIVERABLE
```

已合并工作保持为 baseline，不会再次计为付费交付。认知、neuromorphic 或
Titan 机制不会被静默加入 Crystal grant scope。

中文摘要：[docs/zh-CN/GRANT_OVERVIEW.md](./docs/zh-CN/GRANT_OVERVIEW.md)  
英文权威来源：

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)
- [docs/grants/evaluation-replay-adoption.md](./docs/grants/evaluation-replay-adoption.md)

---

## ✅ 验证 Gate

| Gate | 用途 |
|---|---|
| pytest + coverage | 完整测试套件与强制 100% line coverage |
| Ruff | production code 与 repository tooling lint |
| Gitleaks | 检测已提交的 secret |
| Bandit | Python 静态安全检查 |
| pip-audit | dependency vulnerability audit |
| Docker build | 可复现的 hardened image build |
| eval-gate | retrieval、grounding 与 contradiction regression control |
| JSONL integrity | corpus 结构与重复 ID 检查 |

这些控制可以降低风险，但不能证明不存在任何缺陷，也不构成法律或安全认证。

---

## 📚 中文 Reviewer 路径

1. [docs/zh-CN/REVIEWER_GUIDE.md](./docs/zh-CN/REVIEWER_GUIDE.md)
2. [docs/zh-CN/QUICKSTART.md](./docs/zh-CN/QUICKSTART.md)
3. [docs/zh-CN/STATUS.md](./docs/zh-CN/STATUS.md)
4. [docs/zh-CN/GRANT_OVERVIEW.md](./docs/zh-CN/GRANT_OVERVIEW.md)
5. [docs/zh-CN/GLOSSARY.md](./docs/zh-CN/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — 权威测试结果
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — 权威架构说明

---

## ⚖️ 许可证与贡献

Crystal 采用 **AGPL-3.0**。参见 [LICENSE](./LICENSE)、
[CONTRIBUTING.md](./CONTRIBUTING.md)、[GOVERNANCE.md](./GOVERNANCE.md)、
[SECURITY.md](./SECURITY.md) 与 [PRIVACY.md](./PRIVACY.md)。

> **📊 Canon = 已准入事实** · **🔗 Provenance = 信任** · **🏠 Local-first = 控制**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md)