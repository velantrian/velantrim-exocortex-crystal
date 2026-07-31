# 🔍 Reviewer 指南 — Velantrim Crystal

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md)
>
> 本页提供简体中文验证路线，不引入新的 runtime、grant、compliance 或
> security claim。如有差异，以 GitHub `main`、[docs/STATUS.md](../STATUS.md)
> 和 [TEST_REPORT.md](../../TEST_REPORT.md) 为准。

## 1. Crystal 是什么

Crystal 是 Velantrim 公开、最小且可验证的 memory core：

- 本地优先，默认无强制 cloud dependency；
- claim 保留 source 与显式 epistemic state；
- Guardian + TruthGate 构成自动进入 L3 的 admission boundary；
- `CanonicalView` 提供严格 grounded 的 read view；
- TRACE 与 Receipt 构成可检查的 proof layer；
- 提供本地 SQLite/WAL 与 embedded graph backend；
- 具有技术性 erasure、restriction、audit 与 provenance mechanism；
- 提供可复现测试与确定性 evaluation gate。

## 2. Crystal 不是什么

Crystal 不声称自己是：

- AGI、意识、人格或生物学意义上的大脑；
- “零 hallucination”保证；
- 完整 Titan 或 Personal ExoCortex stack；
- 自我修改或自动 self-canonicalization 系统；
- 必须依赖外部 LLM、graph provider 或 cloud service 的产品；
- 法律 GDPR 认证；
- security certification 或 production-ready multi-tenant hosting；
- 所有研究概念或开放 PR 的 runtime 实现。

## 3. 权威来源

按以下顺序验证：

1. GitHub `main` — 实际已合并代码；
2. [TEST_REPORT.md](../../TEST_REPORT.md) — test 与 coverage baseline；
3. [docs/STATUS.md](../STATUS.md) — 当前 claim 与实现状态；
4. [docs/IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) — 详细组件地图；
5. [docs/ARCHITECTURE.md](../ARCHITECTURE.md) — 架构边界；
6. 英文 grant 文档 — scope 与 acceptance criteria。

Notion note、roadmap、RFC、prototype 或开放 PR 都不是已实现 capability。

## 4. Clean reproduction

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
git status --short
```

预期：

- test 与 coverage gate 通过；
- `eval_gate.py` 不报告 regression；
- generated artifact 不污染 Git working tree；
- 精确数字与 [TEST_REPORT.md](../../TEST_REPORT.md) 对照。

## 5. 验证核心合同

### 🛡️ Admission

```text
新 claim
→ classification + evidence
→ Guardian
→ TruthGate
→ operational memory / admitted Canon
```

检查问题：弱证据、无来源或错误类型的 claim 能否绕过既有 gate？

### 🔎 HTTP query

```text
POST /ask 或 GET /receipt
→ core.query_pipeline.query()
→ 既有 Canon
→ CanonicalView
→ 回答或有界拒绝
```

检查问题：在已迁移 HTTP query 中，L0/L1、L3、ESM、outbox、episode link、
embedding fingerprint 与 adaptive verification 是否保持不变？

保证故意保持精确：

- CLI `ask` 与 `receipt` 尚未迁移；
- MCP 可能初始化缺失的 embedding fingerprint。

### 🔗 TRACE 与 Receipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

检查问题：能否看见支撑回答的 fact 与 evidence reference？状态变化后能否检测 drift？

### 🧾 Audit 与 provenance

```bash
velantrim audit
velantrim audit-verify
velantrim history <fact_id>
```

`history` 与每个 fact 的 `ProvenanceChain` 是不同 view，文档和测试不应混淆。

## 6. 安全启动可选 HTTP service

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

检查：

- 没有 fallback token；
- loopback publish 为安全默认值；
- container user 非 root；
- API dependency 是可选 extra；
- `/ingest` 与 `/ask` 合同不同。

## 7. 验证 evaluation

Crystal 测量的内容包括：

- retrieval `hit@k` 与 MRR；
- TRACE 与 metadata 完整性；
- Evidence Span 覆盖率；
- Receipt replay；
- contradiction precision 与 recall；
- trust boundary 上的正确拒绝。

Titan replay 是已记录的 prior art，不是当前 Crystal capability，也不是
self-optimizing runtime。

## 8. 验证 grant 边界

Reviewer 应明确区分现有 baseline 与申请的 delta：

```text
现有且已测试的 baseline
+
具体、可测量的 funded work
=
可独立验证的 deliverable
```

已合并功能不得再次计为付费工作。Proposal 仍在评审中，不声称资金已获批。

中文摘要：[GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)  
权威来源：[GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

## 9. Review red flags

🚩 文档描述超出 `main` 或 `STATUS.md`。  
🚩 研究 module 被描述为当前 Crystal runtime。  
🚩 翻译扩大 scope、budget 或 compliance claim。  
🚩 Query 意外改变 memory state。  
🚩 平均指标掩盖 safety 或单例 regression。  
🚩 外部 provider 被静默变为强制依赖。

## 10. 最终检查

完成 review 后应能回答：

1. 哪些 claim 可以自动进入 Canon？
2. 哪些 query path 真正只读？
3. 回答如何连接至 fact 与 evidence？
4. 哪些 boundary 已实现，哪些仍是计划？
5. 扣除现有 baseline 后，真实 grant delta 是什么？

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md)