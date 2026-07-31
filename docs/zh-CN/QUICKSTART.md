# 🚀 快速开始 — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 [日本語](../ja/QUICKSTART.md)
>
> **说明：** 命令、package name、environment variable 与 API path 不翻译。
> 如有差异，以 GitHub `main` 和英文文档为准。

## 1. 克隆 repository

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
```

## 2. 创建 virtual environment

Linux/macOS：

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. 安装开发环境

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Crystal 默认 runtime 仅依赖 Python 标准库。开发、API 与 adapter dependency
均为可选 extra。

## 4. 执行完整验证

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

权威 baseline 位于 [TEST_REPORT.md](../../TEST_REPORT.md)。当前记录为：

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

这些数字不能替代在 clean clone 上独立运行测试。

## 5. 使用 CLI

### 写入 claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` 是 admission 操作。新 claim 需要经过既有 classification、Guardian
与 TruthGate boundary。

### 提问

```bash
velantrim ask "how does water behave"
```

⚠️ CLI `ask` 与 `receipt` 当前仍使用可执行 admission 的历史兼容路径
`core.pipeline.run()`。严格零写入保证目前适用于已迁移的 HTTP `/ask` 与
`/receipt`，不能泛化到所有 caller。

### 生成并验证 Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Receipt 是对所用 fact 与 provenance reference 的 sealed proof。Replay 会将其
与当前状态比较，可暴露 drift 或 tampering。

## 6. 启用本地持久化 L3 backend

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

SQLite path 保持在本地。Crystal 不会自动把数据发送给 cloud 或 model provider。

## 7. 启动可选 FastAPI 接口

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
velantrim-api
```

默认地址：

```text
http://127.0.0.1:8000
```

示例：

```bash
curl http://127.0.0.1:8000/health
```

| 方法 | 路径 | 行为 |
|---|---|---|
| `POST` | `/ingest` | 经 Guardian + TruthGate admission |
| `POST` | `/ask` | 严格只读既有 Canon |
| `GET` | `/receipt?q=...` | 只读 query 加 Receipt |
| `POST` | `/verify-receipt` | Receipt replay |

## 8. 启动可选 MCP server

```bash
python -m core.mcp_server
```

MCP 不提供显式 canonical write tool，但搜索可能初始化尚未设置的 embedding
fingerprint，因此不称为完全无 mutation 的路径。

## 9. 后续文档

- [Reviewer 指南](./REVIEWER_GUIDE.md)
- [当前状态](./STATUS.md)
- [Grant 概览](./GRANT_OVERVIEW.md)
- [术语表](./GLOSSARY.md)
- [英文权威架构](../ARCHITECTURE.md)
- [英文权威 Evaluation](../EVAL.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 [日本語](../ja/QUICKSTART.md)