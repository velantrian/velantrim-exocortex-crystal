<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: hi -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 Crystal त्वरित प्रारम्भ

यह मार्गदर्शिका स्थानीय dependency-free baseline चलाती है, एक स्पष्ट claim ingest करती है,
उसे read-only सीमा से query करती है और Receipt सत्यापित करती है।

## आवश्यकताएँ

- Python 3.11 या 3.12;
- Git;
- repository और SQLite data के लिए स्थानीय स्थान।

Default runtime को अनिवार्य LLM, embedding provider या cloud dependency की आवश्यकता नहीं।
Development और full-test extras पूरी test suite के वैकल्पिक packages स्थापित करते हैं।

## 1. Installation

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Windows PowerShell में:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Repository सत्यापित करें

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

सटीक checkpoint और अपेक्षित metrics
[TEST_REPORT.md](../../TEST_REPORT.md) में रखे जाते हैं; यहाँ उन्हें बदलने योग्य
requirements के रूप में दोहराया नहीं जाता।

## 3. Persistent local storage चुनें

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite सामान्य सक्रिय local-first profile है। PostgreSQL/pgvector केवल optional inactive
import और equivalence path है; target `active=false` रहता है।

## 4. Claim को स्पष्ट रूप से ingest करें

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` write operation है। Claim operational state में जाता है और configured
Guardian/TruthGate admission path से गुजरता है। इसका अर्थ यह नहीं कि Crystal स्वयं
objective truth सिद्ध करता है; admission evidence और policy पर निर्भर है।

## 5. Read-only सीमा से query करें

```bash
velantrim ask "how does water behave"
```

Public `ask` `core.query_pipeline.query()` का उपयोग करता है और L0/L1 facts बना या बदल
नहीं सकता, ESM transition नहीं कर सकता, L3 नहीं लिख सकता, outbox नहीं चला सकता,
episode links नहीं लिख सकता, unset embedding fingerprint initialize नहीं कर सकता और
unknown candidates persist नहीं कर सकता।

Strict canonical grounding अपर्याप्त होने पर bounded refusal अपेक्षित है। Refusal trust
boundary का वैध परिणाम है, आवश्यक नहीं कि runtime error हो।

## 6. Receipt बनाएँ और सत्यापित करें

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Receipt query, answer और cited fact IDs को digest में seal करता है और current memory state
के विरुद्ध citations replay कर सकता है। यह tamper-evident है; optional HMAC signing के
लिए locally configured provenance key चाहिए।

## 7. Optional API चलाएँ

```bash
pip install '.[api]'
velantrim-api
```

| Method | Route | सीमा |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | explicit admission/write path |
| `POST` | `/ask` | strict read-only query |
| `GET` | `/receipt?q=...` | query plus Receipt |
| `POST` | `/verify-receipt` | Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

API bearer-token baseline उपयोग करता है। यह complete production multi-tenant
authorization model नहीं है।

## 8. MCP inspection surface चलाएँ

```bash
python -m core.mcp_server
```

MCP read-only search, memory reports, fact history, conflict lookup और Receipt verification
देता है। यह canonical write tool उपलब्ध नहीं कराता।

## सामान्य boundary mistakes

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- Physical L3 strict Canon नहीं है।
- Confidence, duplicate frequency या retrieval similarity अपने-आप independent evidence नहीं।
- Successful import या equivalence activation, cutover या backend selection नहीं है।

## अगले दस्तावेज़

- [README](../../README.md)
- [Documentation map](../DOCUMENTATION_MAP.md)
- [Architecture](../ARCHITECTURE.md)
- [Implementation status](../IMPLEMENTATION_STATUS.md)
- [Test report](../../TEST_REPORT.md)
- [Security policy](../../SECURITY.md)
