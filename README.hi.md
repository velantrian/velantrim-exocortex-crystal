# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 **हिन्दी**

### विश्वसनीय AI प्रणालियों के लिए सत्यापनीय, स्थानीय-प्रथम स्मृति अवसंरचना

`v0.3.0` · 🧪 **1853 परीक्षण सफल / 12 छोड़े गए** · 🎯 **100% कवरेज** · 🧬 **घोषित 7/7 म्यूटेंट पकड़े गए** · ✅ **9 CI कार्य** · 🐍 **डिफ़ॉल्ट रनटाइम केवल Python मानक लाइब्रेरी पर** · ⚖️ **AGPL-3.0**

> Crystal कोई दूसरा चैटबॉट नहीं है। यह स्मृति, प्रमाण और निर्णय की सीमा है, जो
> दर्ज करती है कि कोई दावा क्या है, उसका स्रोत क्या है, उसकी ज्ञानमीमांसात्मक
> अवस्था क्या है, क्या वह उत्तर का आधार बन सकता है, और विरोधाभास को किस स्पष्ट
> निर्णय से सुलझाया गया।

**सत्यापित रनटाइम चेकपॉइंट:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — PR #302 मर्ज किया गया।  
**सटीक प्रमाण:** [TEST_REPORT.md](./TEST_REPORT.md) और
[मशीन-पठनीय implementation manifest](./docs/status/implementation-manifest.json)।

> यह अनुवाद अंग्रेज़ी README की वही कार्यात्मक, सुरक्षा और स्थिति सीमाएँ रखता
> है। स्थिर API पहचानकर्ता कोड वाली मूल वर्तनी में रखे गए हैं, जबकि व्याख्या
> स्वाभाविक हिन्दी में लिखी गई है।

---

## 🎯 Crystal की आवश्यकता क्यों है

कई AI प्रणालियाँ स्रोत दस्तावेज़, उपयोगकर्ता के दावे, मॉडल आउटपुट, परिकल्पनाएँ,
प्राप्त अंश और दीर्घकालिक स्मृति को एक ही संदर्भ या वेक्टर स्टोर में मिला देती
हैं। इससे धाराप्रवाह पाठ को ऐसा अधिकार मिल सकता है जिसे उसके प्रमाण समर्थन नहीं
करते।

```text
प्रभावशाली दावा अपने-आप विश्वसनीय नहीं होता।
ग्राफ का नोड अपने-आप कठोर Canon नहीं होता।
Retrieval score प्रमाण नहीं है।
मॉडल आउटपुट स्वतंत्र स्रोत नहीं है।
विरोधाभास स्वयं विजेता नहीं चुनता।
विषय-लेबल सत्य का निर्णय नहीं है।
```

## 🧠 मुख्य क्षमताएँ

- प्रकारबद्ध दावे और स्पष्ट ज्ञानमीमांसात्मक जीवनचक्र;
- स्रोत, evidence span और provenance मेटाडेटा;
- Guardian और TruthGate प्रवेश सीमाएँ;
- कठोर Canon से अलग बहु-अवस्था भौतिक L3 ग्राफ;
- अपरिवर्तनीय और deny-dominant `TrustSnapshot` पठन-सामंजस्य;
- केवल-पठन वाली सार्वजनिक HTTP, CLI और MCP क्वेरी;
- TRACE और पुनःचलाने योग्य, छेड़छाड़-पहचानने वाले Receipt;
- प्रसंस्करण प्रतिबंध, मिटाना, ऑडिट और आयात सत्र;
- समीक्षा कतारें और फिर से शुरू किए जा सकने वाले समीक्षा सत्र;
- प्रकारबद्ध, अपरिवर्तनीय विरोधाभास रिपोर्ट;
- स्पष्ट `COEXIST`, `CONTEXTUALIZE` और `SUPERSEDE` निर्णय;
- CLI और प्रमाणीकृत HTTP से संघर्ष समाधान;
- scope-सीमित क्यूरेटर भूमिकाएँ और प्रक्रिया-स्थानीय decision lease;
- अधिकार न देने वाले बहु-लेबल विषय facet;
- रनटाइम संक्रमणों से बनी मशीन-पठनीय ESM विनिर्देश;
- नियतात्मक मूल्यांकन, 100% पंक्ति कवरेज और Ring Zero mutation gate;
- संस्करणबद्ध L3 बेंचमार्क इतिहास।

## 🏛️ एक नज़र में आर्किटेक्चर

नीचे दिए गए तीन मानचित्र उसी प्रणाली को तीन पूरक दृष्टिकोणों से दिखाते हैं:
**उद्देश्य**, **सूचना-प्रवाह**, और **मॉड्यूलों के संबंध**।

### 🧠 Mindmap — उद्देश्य और क्षमता-सीमाएँ

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 उद्देश्य
│   ├── AI के लिए सत्यापनीय स्मृति
│   ├── स्थानीय-प्रथम trust infrastructure
│   └── प्रमाण-समर्थित उत्तर और निर्णय
│
├── 🏛️ स्मृति मॉडल
│   ├── L0 — प्रक्रिया के भीतर तेज़ working cache
│   ├── L1 — परिचालन lifecycle memory
│   ├── L2 — pending और review सीमा
│   └── L3 — ग्राफ-आधारित बहु-अवस्था स्मृति
│
├── 🛡️ Trust Boundary
│   ├── Guardian — संरचनात्मक और policy जाँच
│   ├── TruthGate — admission-policy सीमा
│   ├── TrustSnapshot — अपरिवर्तनीय read reconciliation
│   └── CanonicalView — कठोर trusted projection
│
├── 📜 प्रमाण और ऑडिटयोग्यता
│   ├── provenance और evidence spans
│   ├── TRACE — grounding lineage
│   └── Receipt — replay और tamper evidence
│
├── ⚖️ समीक्षा और विरोधाभास
│   ├── review queues और resumable sessions
│   ├── अपरिवर्तनीय ContradictionReport
│   ├── COEXIST
│   ├── CONTEXTUALIZE
│   └── SUPERSEDE
│
├── 🏷️ सलाहकारी नेविगेशन
│   └── TopicFacet — multi-label, non-authoritative metadata
│
├── 🔐 शासन और समन्वय
│   ├── scope-सीमित curator roles और capabilities
│   ├── authenticated actor binding
│   └── प्रक्रिया-स्थानीय decision leases
│
└── 📊 सत्यापन
    ├── deterministic tests और evaluation
    ├── 100% line coverage
    ├── Ring Zero mutation gate
    └── versioned benchmark history
```

### 🏗️ ASCII आर्किटेक्चर — सूचना कैसे बहती है

```text
┌─────────────────────────────────────────────────────────────────────┐
│              🔱 Velantrim ExoCortex — Crystal                      │
│        AI के लिए local-first सत्यापनीय स्मृति अवसंरचना            │
└─────────────────────────────────────────────────────────────────────┘

                         📥 स्पष्ट ingest
                                │
                                ▼
               🧾 Claim type + source + evidence span
                                │
                                ▼
                     🧠 L0 / L1 Observed अवस्था
                                │
                                ▼
             🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 restrictions
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
           ⏳ L2 pending / review      🏛️ भौतिक L3 ग्राफ
                  │                           │
                  │                           ▼
                  │                 📜 provenance / TRACE
                  │                           │
                  └─────────────┬─────────────┘
                                │
                                ▼
                    📐 अपरिवर्तनीय TrustSnapshot
                                │
                                ▼
                  🛡️ Guardian + CanonicalView STRICT
                                │
                   ┌────────────┴────────────┐
                   │                         │
                   ▼                         ▼
          💬 प्रमाणित उत्तर          🚫 सीमाबद्ध अस्वीकार
                   │
                   ▼
          🧾 पुनःचलाने योग्य Receipt

⚖️ अनसुलझा विरोधाभास
        │
        ▼
📋 अपरिवर्तनीय ContradictionReport
        │
        ▼
🔐 scoped principal + capability + decision lease
        │
        ▼
🧑‍⚖️ स्पष्ट COEXIST / CONTEXTUALIZE / SUPERSEDE
        │
        ▼
📜 audited canonical write path

🏷️ TopicFacet metadata ──► केवल navigation / filtering / grouping
                         └─► truth, ESM, evidence या Canon authority कभी नहीं
```

### 🌳 संबंध-वृक्ष — मॉड्यूल कैसे जुड़े हैं

```text
🌳 Crystal प्रणाली के संबंध
│
├── 🧠 Memory Layer
│   ├── L0 ──► तेज़, पुनर्निर्माण योग्य working cache
│   ├── L1 ──► lifecycle, restrictions और pending work
│   ├── L2 ──► logical review boundary
│   └── L3 ──► graph-backed multi-status storage
│
├── 🛡️ Trust Layer
│   ├── Guardian ──► structural और policy validation
│   ├── TruthGate ──► admission decision
│   ├── TrustSnapshot ──► deny-dominant L1/L3 reconciliation
│   └── CanonicalView ──► strict grounding projection
│
├── 📜 Evidence Layer
│   ├── source metadata
│   ├── evidence spans
│   ├── provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Review Layer
│   ├── review queue
│   ├── resumable review session
│   ├── ContradictionReport
│   └── स्पष्ट disposition
│       ├── COEXIST
│       ├── CONTEXTUALIZE
│       └── SUPERSEDE
│
├── 🔐 Authorization Layer
│   ├── CuratorPrincipal
│   ├── role और scoped capability
│   ├── authenticated actor match
│   └── प्रक्रिया-स्थानीय decision lease
│
├── 🏷️ Advisory Layer
│   └── TopicFacet
│       ├── multi-label
│       ├── केवल relevance score
│       └── truth या admission पर कोई अधिकार नहीं
│
├── 🔎 Public Query Layer
│   ├── HTTP /ask और /receipt
│   ├── CLI ask और receipt
│   └── MCP search
│       └── साझा read-only query pipeline
│
└── 📊 Verification Layer
    ├── Python 3.11 / 3.12 tests
    ├── coverage gate
    ├── Ring Zero mutation gate
    ├── security और container checks
    └── benchmark history
```

### केंद्रीय भेद

```text
भौतिक L3 ग्राफ ≠ कठोर Canon
query ≠ ingest
confidence ≠ स्वतंत्र प्रमाण
LLM आउटपुट ≠ स्वतंत्र तथ्य-स्रोत
विरोधाभास ≠ स्वचालित विजेता
विषय-संबंधिता ≠ सत्य या प्रमाण की गुणवत्ता
स्थानीय lease ≠ वितरित समन्वय की गारंटी
```

TruthGate प्रवेश-नीति का द्वार है, वस्तुनिष्ठ सत्य को स्वतंत्र रूप से जानने वाला
oracle नहीं। कठोर Canon प्रमाण, स्थिति, ESM अवस्था, confidence की संरचना और
प्रसंस्करण प्रतिबंधों पर आधारित नीति-अनुमत पठन projection है।

## 🛡️ सार्वजनिक केवल-पठन क्वेरी सीमा

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` और `MCP search`
`core.query_pipeline` साझा करते हैं। वे तथ्य नहीं बनाते, ESM नहीं बदलते, L3 में
नहीं लिखते, outbox नहीं चलाते और embedding fingerprint प्रारंभ नहीं करते।

विवरण: [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md)।

## ⚖️ विरोधाभास का स्पष्ट समाधान

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "दावे अलग संदर्भों का वर्णन करते हैं" \
  --expected-report-id REPORT_ID
```

FastAPI में `POST /review/resolve-conflict` को होस्ट अनुप्रयोग की प्रमाणीकरण
व्यवस्था के साथ पंजीकृत करना आवश्यक है। `core.curator_auth` actor, क्षमता और
scope जाँचता है। `CuratorLeaseRegistry` केवल एक प्रक्रिया की रक्षा करता है;
वितरित तैनाती के लिए बाहरी lease adapter आवश्यक है।

देखें [Conflict-resolution surfaces](./docs/CONFLICT_RESOLUTION_SURFACES.md) और
[Topic facets and curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md)।

## 🏷️ सलाहकारी विषय facet

`core.topic_facets` नेविगेशन, फ़िल्टर और समूह बनाने के लिए सामान्यीकृत लेबल देता
है। score केवल विषय-संबंधिता दर्शाता है; वह truth status, प्रमाण, ESM या कठोर
Canon सदस्यता नहीं बदलता।

## 🚀 त्वरित आरंभ

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 दस्तावेज़

- [दस्तावेज़ मानचित्र](./docs/DOCUMENTATION_MAP.md)
- [वर्तमान स्थिति](./docs/STATUS.md)
- [स्थापत्य](./docs/ARCHITECTURE.md)
- [परीक्षण रिपोर्ट](./TEST_REPORT.md)
- [मूल्यांकन](./docs/EVAL.md)
- [NLnet दायरा](./docs/GRANT_NLNET_SCOPE.md)

## ✅ सत्यापित आधाररेखा

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 दावों की सीमा

Crystal सार्वभौमिक सत्य-पहचान, सभी hallucination का अंत, GDPR या सुरक्षा
प्रमाणीकरण, production multi-tenant readiness, कृत्रिम चेतना या Titan/Full
ExoCortex लागू करने का दावा नहीं करता। वर्तमान lease केवल एक प्रक्रिया तक
सीमित हैं; वितरित समन्वय और बाहरी पहचान प्रदाता का एकीकरण स्वतंत्र भावी कार्य हैं।

## 🤝 योगदान और लाइसेंस

[CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) और [AGPL-3.0](./LICENSE) देखें।