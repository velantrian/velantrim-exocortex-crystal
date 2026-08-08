<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ja -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 Crystal クイックスタート

このガイドでは、必須外部依存のないローカル基盤を起動し、明示的な claim を
ingest し、read-only 境界から問い合わせ、Receipt を検証します。

## 要件

- Python 3.11 または 3.12
- Git
- repository と SQLite data を置くローカル領域

標準 runtime に LLM、embedding provider、cloud は必須ではありません。
development/full-test extras は完全な test suite 用の任意 package を導入します。

## 1. インストール

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Repository の検証

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

正確な checkpoint と期待値は [TEST_REPORT.md](../../TEST_REPORT.md) に保持され、
この文書では変動する要件として重複させません。

## 3. 永続ローカル storage の選択

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite は通常の active local-first profile です。PostgreSQL/pgvector は任意の
inactive import/equivalence path に限られ、target は `active=false` のままです。

## 4. Claim を明示的に ingest

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` は write operation です。claim は operational state に入り、設定された
Guardian/TruthGate admission path で評価されます。Crystal が客観的真実を単独で
証明する意味ではなく、admission は evidence と policy に依存します。

## 5. Read-only 境界から query

```bash
velantrim ask "how does water behave"
```

公開 `ask` は `core.query_pipeline.query()` を使い、L0/L1 fact の作成・更新、
ESM transition、L3 write、outbox operation、episode link 記録、未設定 embedding
fingerprint の初期化、unknown candidate の永続化を行ってはなりません。

strict canonical grounding が不足する場合、bounded refusal は正常です。これは
trust boundary の有効な結果であり、必ずしも runtime error ではありません。

## 6. Receipt の作成と検証

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Receipt は query、answer、引用 fact ID を digest で封印し、現在の memory state
に対して citation を再検証できます。tamper-evident であり、任意 HMAC 署名には
ローカル provenance key が必要です。

## 7. 任意 API の実行

```bash
pip install '.[api]'
velantrim-api
```

| Method | Route | 境界 |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | 明示的 admission/write |
| `POST` | `/ask` | strict read-only query |
| `GET` | `/receipt?q=...` | query と Receipt |
| `POST` | `/verify-receipt` | Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

API は bearer-token baseline を使います。完全な production multi-tenant
authorization model ではありません。

## 8. MCP inspection surface の実行

```bash
python -m core.mcp_server
```

MCP は read-only search、memory report、fact history、conflict lookup、Receipt
verification を提供します。canonical write tool は公開しません。

## よくある境界の誤り

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- physical L3 は strict Canon ではありません。
- confidence、duplicate frequency、retrieval similarity だけでは独立 evidence になりません。
- import/equivalence 成功は activation、cutover、backend selection ではありません。

## 次の文書

- [README](../../README.md)
- [Documentation map](../DOCUMENTATION_MAP.md)
- [Architecture](../ARCHITECTURE.md)
- [Implementation status](../IMPLEMENTATION_STATUS.md)
- [Test report](../../TEST_REPORT.md)
- [Security policy](../../SECURITY.md)
