# 🚀 Quickstart — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 [日本語](../ja/QUICKSTART.md) · 🇮🇳 **हिन्दी**

यह clean clone से Crystal को install, test और run करने का संक्षिप्त path है।
सटीक dependencies और test baseline के लिए authoritative अंग्रेज़ी दस्तावेज़ तथा `TEST_REPORT.md` देखें।

## 1. Clone और virtual environment

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

Default runtime मुख्यतः Python standard library पर आधारित है; optional interfaces अलग extras में हैं।

## 3. Full test suite

```bash
pytest tests/ --cov=. --cov-fail-under=100
```

CI 100% line coverage gate की मांग करता है। सटीक passing/skipped count के लिए
[TEST_REPORT.md](../../TEST_REPORT.md) देखें।

## 4. Evaluation gate

```bash
python scripts/eval_gate.py --out-dir eval-artifacts
```

यह gate retrieval, grounding, TRACE completeness, contradiction detection और
Receipt replay सहित regression thresholds जाँचता है।

## 5. मूल CLI

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

`ingest` admission-capable path है। `ask` और `receipt` का CLI compatibility path,
HTTP strict read-only query contract के समान नहीं है।

## 6. Persistent SQLite L3 backend

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

दूसरे terminal में:

```bash
curl http://127.0.0.1:8000/health
```

मुख्य endpoints:

| Method | Path | अर्थ |
|---|---|---|
| `GET` | `/health` | liveness / readiness |
| `POST` | `/ingest` | Guardian + TruthGate से गुजरने वाला admission |
| `POST` | `/ask` | strict read-only canonical query |
| `GET` | `/receipt?q=...` | read-only query + Receipt |
| `POST` | `/verify-receipt` | Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

HTTP `/ask` और `/receipt` ऐसे strict read-only surfaces हैं जो L0/L1 या L3 write,
ESM transition, outbox drain, episode link, embedding fingerprint initialization या
adaptive verification state mutation नहीं करते।

## 8. Docker

```bash
export VELANTRIM_API_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
docker compose up --build
```

Token न होने पर compose fail-closed रुकता है। Default publish host loopback पर है।

## 9. MCP

```bash
python -m core.mcp_server
```

MCP inspection-oriented tools देता है। इसमें explicit canonical write tool नहीं है,
लेकिन search unset embedding fingerprint को initialize कर सकता है; इसलिए इसे zero-mutation path नहीं कहा जाता।

## 10. Reviewer verification

```bash
velantrim invariant-check
velantrim verify-receipt receipt.json --strict-provenance
velantrim audit-verify
```

`invariant-check` existing L3 state का read-only scan है; यह TruthGate admission behavior को स्वयं execute नहीं करता।
TruthGate के on/off/unset behavior का authoritative proof test suite है।

## आगे पढ़ें

- [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
- [STATUS.md](./STATUS.md)
- [GLOSSARY.md](./GLOSSARY.md)
- [अंग्रेज़ी Architecture](../ARCHITECTURE.md)
- [अंग्रेज़ी Test Report](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 [日本語](../ja/QUICKSTART.md) · 🇮🇳 **हिन्दी**
