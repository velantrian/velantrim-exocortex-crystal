# 🚀 クイックスタート — Velantrim Crystal

> 🌐 🇬🇧 [English](../QUICKSTART.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](../hi/QUICKSTART.md)

この手順は、clean clone から Crystal を install、test、実行するための短い経路です。
正確な依存関係と test baseline は英語の正本と `TEST_REPORT.md` を参照してください。

## 1. Clone と仮想環境

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Development install

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

default runtime は Python standard library を中心に構成され、optional interface は extra として分離されています。

## 3. Full test suite

```bash
pytest tests/ --cov=. --cov-fail-under=100
```

CI は 100% line coverage gate を要求します。正確な passing/skipped count は
[TEST_REPORT.md](../../TEST_REPORT.md) を確認してください。

## 4. Evaluation gate

```bash
python scripts/eval_gate.py --out-dir eval-artifacts
```

この gate は retrieval、grounding、TRACE completeness、contradiction detection、
Receipt replay などの regression threshold を確認します。

## 5. 基本 CLI

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

`ingest` は admission-capable path です。`ask` と `receipt` の CLI compatibility path は、
HTTP の strict read-only query contract と同一ではありません。

## 6. 永続 SQLite L3 backend

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
velantrim ask "..."
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND="sqlite"
$env:VELANTRIM_L3_PATH="./data/canon.db"
velantrim ask "..."
```

## 7. Optional FastAPI

```bash
pip install -e '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
velantrim-api
```

別 terminal で:

```bash
curl http://127.0.0.1:8000/health
```

主な endpoint:

| Method | Path | 意味 |
|---|---|---|
| `GET` | `/health` | liveness / readiness |
| `POST` | `/ingest` | Guardian + TruthGate を通る admission |
| `POST` | `/ask` | strict read-only canonical query |
| `GET` | `/receipt?q=...` | read-only query + Receipt |
| `POST` | `/verify-receipt` | Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

HTTP `/ask` と `/receipt` は、L0/L1 または L3 への write、ESM transition、outbox drain、
episode link、embedding fingerprint 初期化、adaptive verification state mutation を行わない
strict read-only surface として実装されています。

## 8. Docker

```bash
export VELANTRIM_API_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
docker compose up --build
```

compose は token がない場合 fail-closed で停止します。default publish は host loopback です。

## 9. MCP

```bash
python -m core.mcp_server
```

MCP は inspection-oriented tool を提供します。明示的な canonical write tool はありませんが、
search が未設定の embedding fingerprint を初期化する可能性があるため、zero-mutation path とは表現しません。

## 10. Reviewer verification

```bash
velantrim invariant-check
velantrim verify-receipt receipt.json --strict-provenance
velantrim audit-verify
```

`invariant-check` は既存 L3 state の read-only scan であり、TruthGate admission behavior 自体を
実行する command ではありません。TruthGate の on/off/unset behavior は test suite が正本です。

## 次に読む文書

- [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
- [STATUS.md](./STATUS.md)
- [GLOSSARY.md](./GLOSSARY.md)
- [英語 Architecture](../ARCHITECTURE.md)
- [英語 Test Report](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../QUICKSTART.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](../hi/QUICKSTART.md)
