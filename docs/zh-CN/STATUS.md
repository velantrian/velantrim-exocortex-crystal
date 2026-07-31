# 📌 Velantrim Crystal — 当前状态

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/STATUS.md)

**状态日期：** 2026-07-31  
**本翻译对应的 repository 状态：** `main@9f90cb60`  
**最后一个改变 runtime 的 checkpoint：** PR #265 / `cd6fd44`  
**权威测试 baseline：** [TEST_REPORT.md](../../TEST_REPORT.md)

> 本页是状态翻译。如有差异，以 GitHub `main`、英文
> [STATUS](../STATUS.md) 和 [TEST_REPORT.md](../../TEST_REPORT.md) 为准。

---

## 🧭 阅读规则

```text
GitHub Crystal main = 公开实现事实
Notion Crystal       = 同步的 grant 与战略地图
Titan / Full         = 独立研究实验室
```

文档、Notion note、prototype branch 或 Titan module 只有在 Crystal 中实现、
测试并合并至 `main` 后，才算当前 Crystal capability。

## ✅ 已验证 checkpoint

PR #265 引入了严格只读的 HTTP query boundary：

```text
POST /ingest   → 经 Guardian + TruthGate admission
POST /ask      → 严格只读 canonical query
GET  /receipt  → 严格只读 query 加 Receipt
```

HTTP `/ask` 与 `/receipt` 不写入 L0/L1 或 L3，不改变 ESM，不处理 outbox，
不记录 episode link，不初始化 embedding fingerprint，也不改变 adaptive
verification state。

### 明确的剩余范围

- CLI `ask` 与 `receipt` 仍使用 `core.pipeline.run()`；
- `core.pipeline.run()` 仍是可执行 admission 的兼容路径；
- MCP 没有显式 canonical write tool，但搜索可能初始化尚未设置的
  embedding fingerprint。

这些是已知 follow-up，不是隐藏 capability。

## 🧪 验证 baseline

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

改变 runtime 的 checkpoint 合并前，CI 的永久 job 包括 Python 3.11/3.12、
Ruff、security、Docker build、evaluation gate 与 JSONL integrity。精确证据以
英文 [TEST_REPORT.md](../../TEST_REPORT.md) 和 GitHub Actions 为准。

## 🛡️ Public claim 边界

Crystal 可以描述为：

- 本地优先的可验证 AI memory infrastructure；
- 面向 source 与 provenance 的 memory core；
- 在已接线路径上具有 Guardian 与 TruthGate admission control；
- 在已接线路径上具有 CanonicalView、TRACE 与可 replay 的 Receipt；
- 默认仅依赖标准库，adapter 与 interface 可选；
- 具有与 GDPR 相关的技术性删除与 restriction mechanism；
- 可独立测试的开源 research-grade baseline。

Crystal 不应描述为：

- Titan 或完整 Personal ExoCortex；
- 自主认知操作系统；
- 有意识、生命或生物学等价的大脑；
- 普遍真实或无 hallucination；
- 获得法律 GDPR 认证；
- 获得安全认证或可直接用于 production multi-tenant hosting；
- 必须依赖外部 LLM 或 cloud provider。

## 💶 Grant 状态

NLnet NGI0 Commons Fund proposal 已提交并处于评审中。Repository 不声称
资金已经获批。

```text
当前 BASELINE
    +
可测量的 FUNDED DELTA
    =
可独立验证的 DELIVERABLE
```

已合并工作保持为 baseline，不会再次计入付费 milestone。权威控制文档：

- [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

中文说明见 [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)。

## 🧪 Evaluation replay 决策

Titan 的确定性 replay 实现已作为 prior art 接受审查，但未复制到 Crystal
runtime。

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

未来实现必须扩展现有 Crystal evaluation stack，通过独立 RFC/issue/PR，
保持 offline 与 non-authoritative，并维持 TruthGate 与 query boundary。

## 🔬 Research 与 draft PR 规则

开放的研究或 branding PR 不是实现事实。合并前必须基于当前 `main` 重新检查，
审计 grant wording，并验证其不与权威状态文档冲突。

## 📚 Reviewer 路径

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)
4. [GLOSSARY.md](./GLOSSARY.md)
5. [英文权威状态](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/STATUS.md)