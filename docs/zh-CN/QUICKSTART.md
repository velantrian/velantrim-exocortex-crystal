<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: zh-CN -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 Crystal 快速开始

本指南运行本地、无强制外部依赖的基础环境，显式 ingest 一条 claim，通过
read-only 边界查询，并验证 Receipt。

## 要求

- Python 3.11 或 3.12；
- Git；
- 用于 repository 和 SQLite 数据的本地目录。

默认 runtime 不强制依赖 LLM、embedding provider 或云服务。development 和
full-test extras 会安装完整测试套件使用的可选包。

## 1. 安装

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

## 2. 验证 repository

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

精确 checkpoint 和预期指标维护在
[TEST_REPORT.md](../../TEST_REPORT.md) 中，不在本指南中重复为可变要求。

## 3. 选择持久化本地 storage

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell：

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite 仍是普通的 active local-first profile。PostgreSQL/pgvector 仅是可选的
inactive import/equivalence path，目标始终保持 `active=false`。

## 4. 显式 ingest 一条 claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` 是写操作。claim 进入 operational state，并通过配置的
Guardian/TruthGate admission path。该命令不表示 Crystal 独立证明客观真理；
admission 仍依赖 evidence 和 policy。

## 5. 通过 read-only 边界查询

```bash
velantrim ask "how does water behave"
```

公开 `ask` 使用 `core.query_pipeline.query()`，不得创建或更新 L0/L1 facts、
改变 ESM、写入 L3、操作 outbox、记录 episode links、初始化未设置的 embedding
fingerprint，或持久化 unknown candidates。

当 strict canonical grounding 不足时，bounded refusal 是预期结果。拒绝是
trust boundary 的有效结果，不一定是 runtime error。

## 6. 创建并验证 Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Receipt 使用 digest 封装 query、answer 和引用的 fact IDs，并可针对当前
memory state 重放引用。它具有 tamper-evident 性；可选 HMAC 签名需要本地
provenance key。

## 7. 运行可选 API

```bash
pip install '.[api]'
velantrim-api
```

| Method | Route | 边界 |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | 显式 admission/write path |
| `POST` | `/ask` | strict read-only query |
| `GET` | `/receipt?q=...` | query 加 Receipt |
| `POST` | `/verify-receipt` | Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

API 使用 bearer-token baseline，但不是完整的 production multi-tenant
authorization model。

## 8. 运行 MCP inspection surface

```bash
python -m core.mcp_server
```

MCP 提供 read-only search、memory reports、fact history、conflict lookup 和
Receipt verification，不暴露 canonical write tool。

## 常见边界错误

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- physical L3 不等于 strict Canon。
- confidence、重复频率或 retrieval similarity 本身不是独立 evidence。
- import/equivalence 成功不等于 activation、cutover 或 backend selection。

## 后续文档

- [README](../../README.md)
- [Documentation map](../DOCUMENTATION_MAP.md)
- [Architecture](../ARCHITECTURE.md)
- [Implementation status](../IMPLEMENTATION_STATUS.md)
- [Test report](../../TEST_REPORT.md)
- [Security policy](../../SECURITY.md)
