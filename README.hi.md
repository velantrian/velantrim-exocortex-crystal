# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 **हिन्दी**  
> 📚 [German documentation](./docs/de/README.md) · [Documentation française](./docs/fr/README.md) · [Documentación en español](./docs/es/README.md) · [Documentazione italiana](./docs/it/README.md) · [Документация на русском](./docs/ru/README.md) · [简体中文文档](./docs/zh-CN/README.md) · [التوثيق العربي](./docs/ar/README.md) · [日本語ドキュメント](./docs/ja/README.md) · [हिन्दी दस्तावेज़](./docs/hi/README.md)

### *विश्वसनीय AI के लिए सत्यापनीय, local-first और open-source memory infrastructure*

`v0.3.0` · 🧪 **1713 passed / 12 skipped** · 🎯 **100% coverage** · 🐍 **pure-stdlib default runtime** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal केवल chatbot नहीं, बल्कि एक सत्यापनीय memory layer है।
> प्रत्येक fact के साथ source, epistemic state और provenance metadata जुड़े होते हैं।
> canonical graph में automatic admission को Guardian + TruthGate नियंत्रित करते हैं।

> **प्रामाणिक स्रोत:** implementation और grant से संबंधित अंतिम authoritative source GitHub `main` पर अंग्रेज़ी दस्तावेज़ हैं।
> यह हिन्दी संस्करण हिन्दी-भाषी reviewer और contributor के लिए अनुरक्षित अनुवाद है।
> किसी अंतर की स्थिति में अंग्रेज़ी दस्तावेज़ और [TEST_REPORT.md](./TEST_REPORT.md) प्राथमिक होंगे।

---

## 🧭 एक मिनट में Crystal

Crystal, Velantrim का सार्वजनिक और grant-facing core है।

- local L0/L1 operational memory;
- local L3 canonical graph backend;
- Guardian और TruthGate द्वारा admission control;
- CanonicalView द्वारा grounding;
- TRACE, provenance और replayable Receipt;
- evidence span, review queue और import session;
- GDPR-संबंधित erasure और processing-restriction mechanisms;
- deterministic evaluation और CI quality gate;
- optional FastAPI और read-oriented MCP surface।

Crystal **Titan**, पूर्ण Personal Exo-Cortex, autonomous cognitive OS,
consciousness project या self-modifying agent नहीं है। Research ideas भविष्य के RFC को प्रभावित कर सकती हैं,
लेकिन वे वर्तमान runtime capability नहीं हैं।

```text
GitHub Crystal main = सार्वजनिक implementation का authoritative source
Notion Crystal       = synchronized strategy / grant map
Titan / Full         = अलग research track
```

---

## 🛡️ Trust boundary

### Admission path

```text
input / document / agent event
→ classification and evidence
→ Guardian + TruthGate
→ L0/L1 operational memory
→ admitted L3 canonical graph
```

### HTTP query path

PR #265 में जोड़ा गया HTTP query path, admission path से स्पष्ट रूप से अलग है।

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ existing Canon only
→ CanonicalView
→ answer / bounded refusal
```

इन HTTP surfaces पर प्रश्न करने से L0/L1 ingest, ESM transition,
L3 fact/edge write, outbox drain, episode link recording, embedding fingerprint initialization
या adaptive verification state में परिवर्तन नहीं होता।

### स्पष्ट residual scope

- CLI `ask` और `receipt` legacy admission-capable compatibility path का उपयोग करते हैं;
- `core.pipeline.run()` उपलब्ध रहता है;
- MCP में कोई explicit canonical write tool नहीं है, पर search किसी unset embedding fingerprint को initialize कर सकता है।

विवरण के लिए authoritative अंग्रेज़ी specification
[read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md) देखें।

---

## 🧠 Memory model

| Layer | भूमिका | सीमा |
|---|---|---|
| **L0** | process के भीतर working cache | तेज़, पुनर्निर्माण योग्य |
| **L1** | SQLite/WAL operational memory | state, restriction, update |
| **L2** | pending / curator review path | स्वतः canonical नहीं बनता |
| **L3** | canonical graph | automatic admission केवल TruthGate से |
| **TRACE / Receipt** | proof layer | grounding समझाता है और drift पहचानता है |

Physical graph में अलग-अलग truth status मौजूद हो सकते हैं। कठोर अर्थ में Canon,
VERIFIED, TRACE-valid और policy-allowed projection है; इसका अर्थ graph backend में मौजूद हर node नहीं है।

---

## 🚀 Quickstart

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

मूल CLI:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

dependency-free persistent L3 backend:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

चरणबद्ध निर्देश [docs/hi/QUICKSTART.md](./docs/hi/QUICKSTART.md) में हैं।

---

## 🔌 Optional interfaces

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Method | Path | Contract |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | Guardian + TruthGate से गुजरने वाला admission |
| `POST` | `/ask` | strict read-only canonical query |
| `GET` | `/receipt?q=...` | read-only query + Receipt |
| `POST` | `/verify-receipt` | वर्तमान state के विरुद्ध Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

FastAPI और Uvicorn optional extras हैं। Default runtime को cloud service या external model provider की आवश्यकता नहीं है।

### MCP

```bash
python -m core.mcp_server
```

MCP search, memory report, fact history, conflict lookup और Receipt verification जैसे
inspection-oriented tools देता है। ऊपर बताई गई fingerprint residual boundary बनी रहती है।

---

## 🧪 Evaluation

Crystal में deterministic evaluation baseline शामिल है।

- retrieval hit@k / MRR;
- TRACE / metadata completeness;
- source-span coverage;
- Receipt replay survival;
- contradiction precision / recall;
- trust-boundary refusal checks;
- CI regression floor / ceiling।

Titan की deterministic replay implementation को prior art के रूप में दर्ज किया गया है,
लेकिन उसे Crystal runtime में copy नहीं किया गया है। कोई भविष्य implementation मौजूदा Crystal evaluation stack को
extend करेगी, offline और non-authoritative रहेगी, और funded baseline/delta rule का पालन करेगी।

---

## 💶 Grant boundary

यह project NLnet NGI0 Commons Fund में submit किया गया है और review में है।
Public repository यह दावा नहीं करती कि funding award हो चुकी है।

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

पहले से merged कार्य baseline है और उसे paid deliverable के रूप में दोबारा नहीं गिना जाता।
कोई नया cognitive, neuromorphic या Titan mechanism स्वतः Crystal grant scope में नहीं जुड़ता।

हिन्दी overview: [docs/hi/GRANT_OVERVIEW.md](./docs/hi/GRANT_OVERVIEW.md)

Authoritative अंग्रेज़ी दस्तावेज़:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)

---

## ✅ Verification gates

| Gate | उद्देश्य |
|---|---|
| pytest + coverage | 100% line coverage वाला full suite |
| Ruff | production / tooling code lint |
| Gitleaks | committed secrets की पहचान |
| Bandit | Python static security check |
| pip-audit | dependency vulnerability report |
| Docker build | hardened image का reproducible build |
| eval-gate | retrieval / grounding / contradiction regression control |
| JSONL integrity | corpus structure / duplicate-id check |

ये controls जोखिम घटाते हैं, लेकिन सभी defects की अनुपस्थिति सिद्ध नहीं करते और न ही legal या security certification बनते हैं।

---

## 📚 हिन्दी reviewer path

1. [docs/hi/REVIEWER_GUIDE.md](./docs/hi/REVIEWER_GUIDE.md)
2. [docs/hi/QUICKSTART.md](./docs/hi/QUICKSTART.md)
3. [docs/hi/STATUS.md](./docs/hi/STATUS.md)
4. [docs/hi/GRANT_OVERVIEW.md](./docs/hi/GRANT_OVERVIEW.md)
5. [docs/hi/GLOSSARY.md](./docs/hi/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — authoritative test evidence
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — authoritative architecture

---

## ⚖️ License and contribution

Crystal **AGPL-3.0** के अंतर्गत उपलब्ध है। [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md) और [PRIVACY.md](./PRIVACY.md) देखें।

> **📊 Canon = admitted truth** · **🔗 Provenance = trust** · **🏠 Local-first = control**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 **हिन्दी**
