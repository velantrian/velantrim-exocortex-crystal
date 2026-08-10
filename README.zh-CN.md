# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### 面向可信 AI 系统的、可验证的 local-first 内存、证据与决策基础设施

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 默认 stdlib-only runtime · ⚖️ **AGPL-3.0**

> Crystal 不是 chatbot，也不是自主“真理预言机”。它是 memory/evidence/decision boundary，用于记录 claim 的来源、epistemic state、grounding 资格以及对矛盾的显式可审计决策。

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337。  
**Reader foundation:** RC-1 evidence-linked skeleton 和 RC-2 caller-supplied Structural Document Map 已实现并测试；dedicated multi-pass Reader 尚未实现。  
**Grant:** `submitted / under review / not awarded`。  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md)、[STATUS.md](./docs/STATUS.md)、[implementation manifest](./docs/status/implementation-manifest.json)。

> 出现冲突时英文是主源。本 README 是完整公开展示，不是简短 orientation。参见 [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) 与 [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md)。

---

## 🎯 为什么需要 Crystal

许多 AI/RAG 系统把文档、用户陈述、model output、假设和 memory 混在一起。流畅文字可能因此获得 evidence 无法支撑的 authority。

```text
fluent claim        != trusted fact
physical L3         != strict Canon
retrieval score     != evidence
model output        != independent source truth
migration receipt   != claim evidence
import success      != backend activation
Reader coverage     != comprehension proof
Reader structure    != truth/confidence authority
```

## 🧠 Crystal 已提供什么

- typed claims 与明确的 epistemic lifecycle；
- source identity、evidence spans 与 provenance；
- Guardian 与 TruthGate admission boundaries；
- 与 strict Canon 分离的 multi-status physical L3；
- deny-dominant TrustSnapshot 与 CanonicalView；
- read-only HTTP /ask、CLI ask、MCP search；
- TRACE 与 replayable tamper-evident Receipts；
- review queue/session 与 ContradictionReport；
- 显式 COEXIST / CONTEXTUALIZE / SUPERSEDE 决策；
- scoped curator capabilities 与 process-local leases；
- SQLite lifecycle 与 bounded logical migration；
- `active=false` 的 optional PostgreSQL/pgvector inactive import；
- RC-1：source/version/session、SegmentCard、fidelity、coverage、bookmarks/open loops、stale/failure/privacy；
- RC-2：带 RECOVERED / AMBIGUOUS / UNSUPPORTED 的 version-bound caller-supplied structure。

RC-1/RC-2 不保存 source body，不新增 Reader API/CLI/worker 或 durable Reader schema，也没有 Canon/ESM/planner authority。不存在 automatic parser/OCR、Reader LLM/provider orchestration、embeddings/ANN/vector DB 或 multi-pass/cross-document runtime。

## 🏛️ 三种架构视图

### 🧠 Mind map

```text
🧠 Crystal
├── 📖 Reader foundation
│   ├── RC-1 evidence-linked skeleton
│   ├── RC-2 Structural Document Map
│   └── dedicated multi-pass Reader — NOT IMPLEMENTED
├── 🏛️ Memory
│   ├── L0 — working cache
│   ├── L1 — operational SQLite/WAL
│   ├── L2 — pending/review
│   └── L3 — physical multi-status graph
├── 🛡️ Trust
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
└── 🗄️ Storage
    ├── SQLite — active local-first
    └── PostgreSQL/pgvector — inactive active=false
```

### 🏗️ 信息流

```text
Source / document
      ↓
RC-1 Reader artifacts
      ↓
RC-2 structural metadata
      ↓
explicit ingest / review
      ↓
Guardian → TruthGate
      ↓
L1 + physical L3
      ↓
TrustSnapshot → CanonicalView STRICT
      ↓
Grounded answer / bounded refusal
      ↓
TRACE + Receipt
```

### 🌳 模块树

```text
🌳 core
├── reader_core.py       # RC-1
├── reader_structure.py  # RC-2
├── evidence.py
├── truth_gate.py
├── pipeline.py
├── query_pipeline.py
└── storage/...
```

## 🧱 Memory 与 authority surfaces

| Surface | Role | Boundary |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable |
| L2 | review/pending | 无 automatic admission |
| L3 | physical graph | multi-status |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, not truth generator |
| ContradictionReport | conflict object | 无 automatic winner |

## 🗄️ SQLite 与 PostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first runtime
    ├── reads/writes
    ├── backup/restore
    └── bounded logical export

PostgreSQL 16 + pgvector
└── optional inactive target
    ├── explicit optional dependency
    ├── SERIALIZABLE import
    ├── exact target re-hash
    └── active=false
```

Import success 不等于 activation、cutover、rollback、dual-write、automatic switching、ANN acceptance 或 TruthGate admission。普通 PostgreSQL runtime adapter 未激活。

## 🔎 Crystal 与 Classic RAG

| Question | Classic RAG | Crystal |
|---|---|---|
| 查找相关材料 | 核心能力 | adapters |
| Claim vs trusted fact | app-specific | typed boundary |
| Provenance | 不固定 | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| 阻止 model self-source | 非内建 | Ring Zero |
| Contradictions | 外部逻辑 | explicit dispositions |
| Evidence replay | optional | TRACE / Receipt |
| 必须 cloud/model | 不一定 | default runtime 不需要 |

## 🛡️ Read-only query boundary

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

这些 surfaces 不创建 facts、不改变 ESM、不写入 L3。Explicit ingest 是独立 write path。

## ⚖️ Contradiction decisions

```text
unresolved contradiction
        ↓
ContradictionReport
        ↓
scoped curator + capability + lease
        ↓
COEXIST / CONTEXTUALIZE / SUPERSEDE
        ↓
audited canonical write path
```

## 🚀 快速开始

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

可选 PostgreSQL：`pip install -e '.[postgresql]'`。

## ✅ 已验证 baseline

```text
Runtime checkpoint: bbd816c09dd39a02e6de6c1014438490572f40f6
Python 3.11/3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
CI: 9/9
Ring Zero: 7/7
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
PostgreSQL target: active=false
```

## 🚧 Non-claims

Crystal 不声称 universal truth、zero hallucinations、AGI/consciousness、legal/GDPR/security certification、production multi-tenancy、distributed exactly-once、active PostgreSQL runtime、automatic switching/cutover/rollback/dual-write、automatic Reader parsing、embeddings/ANN/vector Reader stack 或 completed dedicated multi-pass Reader Core。

NLnet 仍为 **submitted / under review / not awarded**；约 €50,000 仅为 planning，budget change none。协议前 merged 的工作属于 baseline。

## 📚 导航

- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Quick Start](./docs/QUICKSTART.md)
- [Status](./docs/STATUS.md)
- [Implementation Status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Security](./SECURITY.md)
- [Governance](./GOVERNANCE.md)
- [Contributing](./CONTRIBUTING.md)

## 🤝 贡献与许可

修改必须保持 authority boundaries、tests/coverage 与精确 claims。参见 [CONTRIBUTING.md](./CONTRIBUTING.md)。License: [AGPL-3.0](./LICENSE)。
