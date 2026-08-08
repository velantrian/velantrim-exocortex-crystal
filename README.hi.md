# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 **हिन्दी**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### भरोसेमंद AI प्रणालियों के लिए सत्यापन योग्य, local-first स्मृति, प्रमाण और निर्णय अवसंरचना

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 घोषित Ring Zero mutants समाप्त** · ✅ **9 स्थायी CI jobs** · 🐍 **default runtime केवल Python standard library** · ⚖️ **AGPL-3.0**

> Crystal कोई दूसरा chatbot या स्वायत्त “truth oracle” नहीं है। यह स्मृति, प्रमाण और निर्णय की सीमा है जो दर्ज करती है कि claim क्या है, वह कहाँ से आया, किस epistemic state में है, क्या वह उत्तर को ground कर सकता है, और contradiction को किस स्पष्ट, audit योग्य निर्णय से संभाला गया।

**सत्यापित runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — merged PR #337।  
**Validated head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 सफल।  
**PostgreSQL integration:** `31256316532` — PostgreSQL 16 + pgvector 0.8.2।  
**मुख्य प्रमाण:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md) और [machine-readable manifest](./docs/status/implementation-manifest.json)।

> **अनुवाद अनुबंध:** यह README छोटा सारांश नहीं, बल्कि अंग्रेज़ी संस्करण की पूर्ण दृश्य और अर्थगत प्रस्तुति है। अंग्रेज़ी मुख्य कार्य और conflict-resolution source रहती है; अन्य स्थिर दस्तावेज़ चरणों में अनुवादित होते हैं। [Localization policy](./docs/LOCALIZATION_POLICY.md) और [Translation status](./docs/TRANSLATION_STATUS.md) देखें।

---

## 🎯 Crystal क्यों आवश्यक है

कई AI प्रणालियाँ source documents, user statements, model output, hypotheses, retrieved fragments और durable memory को एक ही context या vector store में मिला देती हैं। स्पष्ट सीमाओं के बिना, धाराप्रवाह भाषा उस अधिकार को पा सकती है जिसे उसका evidence समर्थित नहीं करता।

```text
धाराप्रवाह claim अपने-आप trusted नहीं होता।
physical graph node अपने-आप strict Canon नहीं होता।
retrieval score evidence नहीं है।
model output स्वतंत्र factual source नहीं है।
contradiction स्वयं winner नहीं चुनता।
TopicFacet label truth verdict नहीं है।
successful import backend activation नहीं है।
```

## 🧠 Crystal क्या प्रदान करता है

- typed claims और explicit epistemic lifecycle;
- source identity, exact evidence spans और provenance;
- Guardian और TruthGate admission boundaries;
- strict Canon से अलग multi-status physical L3 graph;
- immutable deny-dominant `TrustSnapshot`;
- read-only HTTP, CLI और MCP query surfaces;
- TRACE और replayable tamper-evident Receipts;
- restrictions, erasure, audit और import sessions;
- review queues और resumable review sessions;
- immutable `ContradictionReport`;
- स्पष्ट `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE` decisions;
- scoped curator capabilities और process-local decision leases;
- truth authority रहित advisory TopicFacet metadata;
- deterministic evaluation, 100% line coverage और Ring Zero mutation gate;
- सत्यापित SQLite backup/restore और bounded logical migration;
- optional inactive PostgreSQL/pgvector import और independent exact-state equivalence।

## 🏛️ तीन architecture views

### 🧠 Mind map

```text
🧠 Crystal
├── 🎯 उद्देश्य
│   ├── AI के लिए सत्यापन योग्य स्मृति
│   ├── local-first trust infrastructure
│   └── evidence से जुड़े उत्तर और निर्णय
├── 🏛️ Memory
│   ├── L0 — तेज working cache
│   ├── L1 — operational state / lifecycle
│   ├── L2 — waiting / review boundary
│   └── L3 — physical multi-status graph
├── 🛡️ Trust
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Evidence
│   ├── source + exact span
│   ├── provenance
│   ├── TRACE
│   └── Receipt
├── ⚖️ Contradiction
│   ├── review queue / session
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ Storage
│   ├── SQLite — सामान्य local-first profile
│   └── PostgreSQL/pgvector — inactive target
└── 📊 Verification
    ├── Python 3.11 / 3.12
    ├── 100% coverage
    ├── mutation / security / Docker
    └── exact-head CI evidence
```

### 🏗️ सूचना प्रवाह

```text
📥 explicit ingest
        ↓
🧾 claim type + source + exact evidence span
        ↓
🧠 observed state in L0/L1
        ↓
🛡️ Guardian → ⚖️ TruthGate → 🚧 restrictions
        ↓                         ↓
⏳ L2 review               🏛️ physical L3 graph
        └──────────────┬──────────┘
                       ↓
             📐 immutable TrustSnapshot
                       ↓
          🛡️ Guardian + CanonicalView STRICT
                  ↓                 ↓
          💬 grounded answer      🚫 grounded refusal
                  ↓
             🧾 replayable Receipt
```

### 🌳 Module tree

```text
🌳 Crystal
├── 🧠 Memory: L0 / L1 / L2 / L3
├── 🛡️ Trust: Guardian / TruthGate / TrustSnapshot / CanonicalView
├── 📜 Evidence: Source / Span / Provenance / TRACE / Receipt
├── ⚖️ Review: Queue / Session / ContradictionReport / Disposition
├── 🔎 Query: HTTP / CLI / MCP
├── 🗄️ Portability: SQLite lifecycle / logical bundle / inactive PostgreSQL import
└── 📊 Verification: tests / coverage / mutation / security / Docker / docs-status
```

## 🧭 मुख्य अंतर

```text
physical L3 graph    != strict Canon
query                != ingest
confidence           != independent evidence
LLM output           != independent factual source
contradiction detect != automatic winner
TopicFacet relevance != truth
migration receipt    != claim evidence
successful import    != backend activation
process-local lease  != distributed coordination
```

TruthGate admission policy gate है, स्वतंत्र रूप से objective truth जानने वाला oracle नहीं। Strict Canon evidence, status, ESM state, confidence shape और processing restrictions पर policy-allowed read projection है।

## 🧱 Memory और evidence surfaces

| Surface | भूमिका | महत्वपूर्ण सीमा |
|---|---|---|
| L0 | in-process working cache | तेज और rebuildable |
| L1 | SQLite/WAL operational memory | lifecycle, restrictions |
| L2 | logical review boundary | स्वतः Canon नहीं |
| L3 | physical multi-status memory | record presence ≠ trust |
| TrustSnapshot | immutable reconciliation | deny-dominant resolution |
| CanonicalView | strict grounding projection | केवल policy-allowed reads |
| TRACE / Receipt | proof और replay | grounding, drift, tamper evidence |
| ContradictionReport | immutable conflict | confidence winner नहीं चुनता |
| TopicFacet | navigation metadata | truth / ESM / Canon नहीं बदलता |

## 🗄️ SQLite और PostgreSQL/pgvector

```text
SQLite
└── वर्तमान सामान्य local-first runtime profile
    ├── reads / writes
    ├── backup / restore
    ├── lock recovery
    └── bounded canonical logical export

PostgreSQL 16 + pgvector
└── optional migration / equivalence profile
    ├── optional [postgresql] extra
    ├── lazy driver loading
    ├── new target schema
    ├── active=false
    ├── SERIALIZABLE import
    └── independent count / byte / SHA-256 equivalence
```

PostgreSQL target सामान्य runtime composition में नहीं है और सामान्य reads/writes नहीं कर सकता। successful import activation, automatic selection, cutover, rollback, dual-write, TruthGate admission, strict Canon membership, ANN acceptance या production multi-tenancy नहीं बनाता।

## 🔎 Crystal बनाम classical RAG

| प्रश्न | Classical RAG | Crystal |
|---|---|---|
| संबंधित सामग्री ढूँढना | मुख्य ताकत | retrieval adapters |
| user claim और verified fact अलग करना | application-specific | explicit typed boundary |
| lifecycle और contradictions track करना | अक्सर बाहरी logic | first-class states / reports |
| generated text को स्वयं source बनने से रोकना | inherent नहीं | Ring Zero invariant |
| उत्तर evidence replay करना | optional | TRACE / Receipt |
| contradiction को जवाबदेही से हल करना | application-specific | authorized dispositions |
| mandatory cloud/model provider के बिना चलना | अलग-अलग | pure-stdlib local-first baseline |

## 🛡️ सार्वजनिक read-only सीमा

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` और `MCP search` एक `core.query_pipeline` साझा करते हैं। वे facts नहीं बनाते, ESM state नहीं बदलते, L3 में नहीं लिखते और Canon को mutate नहीं करते।

## ⚖️ स्पष्ट contradiction decision

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "claims अलग contexts का वर्णन करते हैं" \
  --expected-report-id REPORT_ID
```

`CuratorLeaseRegistry` केवल एक process के भीतर coordination देता है। distributed deployment के लिए external lease adapter चाहिए।

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optional inactive PostgreSQL tooling: `pip install -e '.[postgresql]'`।

## 📚 दस्तावेज़ navigation

- [हिन्दी index](./docs/hi/README.md)
- [English documentation map](./docs/DOCUMENTATION_MAP.md)
- [Test report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Security](./SECURITY.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)

## ✅ सत्यापित baseline

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
Mutation: 7/7
CI: 9/9
PostgreSQL integration: PostgreSQL 16 + pgvector 0.8.2 successful
```

## 🚧 दावे की सीमा

Crystal universal objective-truth detection, zero hallucinations, कानूनी GDPR/security certification, production-ready multi-tenancy, distributed locking, AGI या consciousness, active PostgreSQL runtime, automatic switching, cutover/rollback या पूर्ण dedicated Reader Core का दावा नहीं करता। NLnet proposal **submitted / under review / not awarded** है।

## 🤝 योगदान और license

[CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md), [GOVERNANCE.md](./GOVERNANCE.md) और [AGPL-3.0](./LICENSE) देखें।
