# 📖 शब्दावली — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 [日本語](../ja/GLOSSARY.md) · 🇮🇳 **हिन्दी**

यह glossary हिन्दी documentation में explanatory terminology को consistent रखती है। Contract identifiers,
code symbols, CLI commands, environment variables और API paths का अनुवाद नहीं किया जाता।

| Term | हिन्दी में अर्थ |
|---|---|
| **Canon** | verified, TRACE-valid और policy-allowed canonical projection; graph में मौजूद हर node नहीं। |
| **CanonicalView** | query के समय policy और verification boundaries लागू करके Canon का projection। |
| **TruthGate** | claim के automatic admission का निर्णय लेने वाला gate; identifier untranslated रहता है। |
| **Guardian** | admission path का policy / safety control component। |
| **TRACE** | answer grounding और provenance समझाने वाला proof-oriented trace। |
| **Receipt** | answer और evidence state को seal करने वाला record, जिसे बाद में replay / verify किया जा सकता है। |
| **Provenance** | fact, source, transition, review और erase की origin/history information। |
| **ProvenanceChain** | per-fact append-only hash-chained lifecycle record; current wiring scope के लिए अंग्रेज़ी status देखें। |
| **Evidence span** | source का वह specific range जो claim को support करता है। |
| **Claim** | source, epistemic state और metadata वाला candidate information; यह स्वतः Canon नहीं होता। |
| **WORLD_FACT** | world fact के रूप में classified claim type; इसे admission policy pass करनी होती है। |
| **LLM_OUTPUT** | model output से उत्पन्न claim type; अकेले यह `WORLD_FACT` के रूप में automatically canonicalize नहीं होता। |
| **L0** | process-local working cache; तेज़ और rebuildable। |
| **L1** | SQLite/WAL operational memory; state, restriction और update रखती है। |
| **L2** | pending / curator review path; स्वतः Canon में नहीं जाता। |
| **L3** | canonical graph backend; automatic admission केवल TruthGate से। |
| **Admission** | claim को operational / canonical state में स्वीकार करने वाली write-capable process। |
| **Read-only query** | existing Canon पढ़ने वाली query; कभी-कभी specifically HTTP `/ask` और `/receipt` strict contract। |
| **Bounded refusal** | evidence या policy boundary अपर्याप्त होने पर अनुमान से gap न भरते हुए सीमित refusal। |
| **Outbox** | deferred write / delivery workflow के लिए operational mechanism। |
| **ESM** | epistemic state machine; claim state transitions दर्शाती है। |
| **Embedding fingerprint** | embedding configuration / state consistency के लिए fingerprint; MCP residual scope ध्यान में रखें। |
| **Audit log** | erase, restriction और override जैसे accountable events का record। |
| **Gate reason** | TruthGate द्वारा block किए जाने का concrete reason; force-approve audit में record होता है। |
| **Baseline** | grant proposal से पहले `main` में merged current implementation और evidence। |
| **Funded delta** | baseline से अलग, measurable और independently verifiable future deliverable। |
| **Runtime checkpoint** | audited implementation behavior वाला commit; localization sync marker से अलग। |
| **Localization sync marker** | वह short `main` commit marker जिससे translation synchronized है; runtime behavior claim नहीं। |
| **Titan** | Crystal से अलग research track; current Crystal runtime या automatic grant scope नहीं। |
| **Full Personal Exo-Cortex** | long-term research vision; public Crystal baseline के समान नहीं। |

## Untranslated identifiers

हिन्दी text में भी निम्न original spelling में रहते हैं:

```text
TruthGate
Guardian
CanonicalView
TRACE
Receipt
Canon
ProvenanceChain
L0 / L1 / L2 / L3
WORLD_FACT
LLM_OUTPUT
ENABLE_TRUTH_POLICY
VELANTRIM_L3_BACKEND
VELANTRIM_L3_PATH
VELANTRIM_API_TOKEN
```

## Wording cautions

- “Canon” को केवल “सारा graph data” न लिखें;
- “verified” को “पूर्णतः और सदैव सत्य” तक मजबूत न करें;
- “GDPR-relevant mechanism” को “GDPR certified” न लिखें;
- “security control” को “security certification” न लिखें;
- “under review” को “funding awarded” न लिखें;
- HTTP read-only guarantee को पूरे CLI / MCP पर लागू न करें।

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 [日本語](../ja/GLOSSARY.md) · 🇮🇳 **हिन्दी**
