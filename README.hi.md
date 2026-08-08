# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — प्रामाणिक स्रोत](./README.md) · 🇮🇳 **हिन्दी सारांश**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### भरोसेमंद AI प्रणालियों के लिए सत्यापनीय, local-first स्मृति अवसंरचना

यह फ़ाइल **संक्षिप्त, गैर-मानक परिचय** है; पूरी दस्तावेज़ीकरण का अनुवाद नहीं। इंजीनियरिंग
निर्णय, आर्किटेक्चर, स्थिति, सुरक्षा और अनुदान दावे अंग्रेज़ी में बनाए जाते हैं। अंतर होने पर
[README.md](./README.md) और अंग्रेज़ी प्रमाण मान्य होंगे।

`v0.3.0` · 🧪 **2078 पास / 13 स्किप** · 🎯 **100.00% कवरेज** · ✅ **9 CI जॉब**

**सत्यापित runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337।

Crystal भौतिक भंडारण, प्रमाण, epistemic admission और विश्वसनीय read views को अलग रखता है। डेटा
की मौजूदगी, retrieval ranking या migration सफलता Guardian, TruthGate या strict Canon reconciliation
को पार नहीं कर सकती।

## सत्यापित दायरा

- typed claims, provenance और सटीक source spans;
- Guardian और TruthGate admission boundaries;
- immutable `TrustSnapshot` और `CanonicalView` reads;
- read-only सार्वजनिक HTTP, CLI और MCP queries;
- TRACE, receipts, restriction, erasure और स्पष्ट contradiction decisions;
- सामान्य स्थानीय प्रोफ़ाइल के रूप में SQLite;
- सत्यापित backup/restore और bounded-resource logical export;
- inactive target schema में वैकल्पिक PostgreSQL/pgvector import और स्वतंत्र exact-state verification।

## Storage सीमा

```text
SQLite = वर्तमान सामान्य local-first profile
PostgreSQL + pgvector = वैकल्पिक migration target
active=false
कोई सामान्य runtime reads/writes नहीं
कोई automatic switching, cutover, rollback या dual-write नहीं
```

PostgreSQL driver केवल `[postgresql]` से install होता है और केवल स्पष्ट operator command से load
होता है। successful import operational evidence है, activation या strict Canon admission नहीं।

## स्थिर अर्थ सीमाएँ

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal universal truth, zero hallucinations, active PostgreSQL runtime, production multi-tenancy,
distributed exactly-once, legal/GDPR/security certification, Titan integration या artificial
consciousness का दावा नहीं करता।

## Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## वर्तमान अंग्रेज़ी प्रमाण

- [प्रामाणिक README](./README.md)
- [Verification report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Security policy](./SECURITY.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [हिन्दी दस्तावेज़ मार्ग](./docs/hi/README.md)

NLnet आवेदन जमा है और समीक्षा में है; पुरस्कार या बजट परिवर्तन का दावा नहीं किया गया है।
