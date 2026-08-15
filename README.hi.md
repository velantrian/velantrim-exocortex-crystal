# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 **हिन्दी**

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->
<!-- current-localization-source: main@e1df11219ee4fc3b9c175b05c7569e568cf6f512 -->

## 💠 ऐसी AI memory जिसमें retrieval और truth अलग रहते हैं

Crystal एक **local-first, auditable AI memory/evidence infrastructure** है। इसका मूल नियम जानबूझकर conservative है: कोई relevant item मिल जाना उसे evidence, verified fact या Canon authority नहीं बनाता।

> 👤 **पहली बार Crystal पढ़ रहे हैं?** इस page से शुरू करें — यह human-first entry point है।
>
> 🤖 **AI / agents / automated reviewers:** **[Special for AI →](./docs/ai/README.md)** से शुरू करें; narrative README से machine state reconstruct न करें।
>
> 📚 **गहरी architecture view:** **[Deep System Overview →](./docs/OVERVIEW.md)**।

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐍 standard-library-first default runtime · ⚖️ **AGPL-3.0**

किसी conflict में English primary source है। Localization policy: [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md). Current freshness ledger: [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 👋 Crystal क्या करता है?

Traditional RAG अक्सर पूछता है: “इस query से सबसे relevant text क्या है?” Crystal उसके बाद वाले प्रश्नों को formal बनाता है:

- यह जानकारी कहाँ से आई?
- क्या यह उसी proposition को support करती है या केवल related topic है?
- क्या यह केवल candidate है या evidence admission तक पहुँची?
- क्या contradiction वास्तव में adjudicate हुआ?
- क्या policy इसे trusted memory में आने देती है?
- grounded answer में क्या safely दिखाया जा सकता है?

Central boundary:

> **candidate discovery निरीक्षण के लिए items सुझा सकता है; candidate adjudication और authority path अलग रहते हैं।**

```text
fluent claim                  != trusted fact
retrieval match               != evidence
similarity                    != identity
ranking                       != epistemic authority
repetition                    != corroboration
candidate discovery           != candidate adjudication
Reader candidate              != admitted evidence
relation candidate            != admitted evidence
contradiction candidate       != confirmed contradiction
cross-document link           != Canon relation
NLI label                     != proposition identity
RRTIC suspicion               != adjudicated relation
evaluation pass               != runtime authorization
physical L3                   != strict Canon
```

Historical compatibility literal retained exactly:

```text
contradiction candidate  != confirmed contradiction
```

## 🧠 Mental model

```text
💠 Crystal
├── 📥 Sources / explicit ingest
├── 📖 Reader RC-1 … RC-7
│   ├── provenance + structure
│   ├── bounded multi-pass mechanics
│   ├── source-linked propositions
│   ├── relation candidates
│   ├── long-context working sets
│   └── cross-document candidate links
├── 🔎 RC-9 lexical PRE-ADMISSION discovery
├── 🧪 frozen semantic-comparator / NLI evaluation evidence
├── 🧩 RRTIC-v1 typed inspection contract
├── 🛡️ Guardian → TruthGate
├── 🏛️ L0 / L1 / L2 / physical L3
├── 🔐 TrustSnapshot → CanonicalView
└── 🧾 TRACE / Receipt
```

## 🏗️ Data path और authority path

```text
Source / document
      ↓
Reader RC-1 … RC-7 bounded artifacts
      ↓
RC-9 lexical candidate discovery
      ↓
RRTIC suspicion / typed inspection
      ↓
inspection candidate
      ║
      ║  automatic authority नहीं
      ▼
explicit evidence / review path
      ↓
Guardian → TruthGate
      ↓
physical L3
      ↓
TrustSnapshot → CanonicalView STRICT
      ↓
grounded output / bounded refusal
```

Discovery ≠ Authority.

## 📖 Reader में वास्तव में क्या implemented है?

| Layer | Status | Boundary |
|---|---|---|
| RC-1 | ✅ bounded implemented | source/version/session + evidence-linked artifacts |
| RC-2 | ✅ bounded implemented | caller-supplied Structural Document Map |
| RC-3 | ✅ bounded implemented | deterministic explicit multi-pass mechanics |
| RC-4 | ✅ bounded implemented | source-linked pre-admission proposition extraction |
| RC-5 | ✅ bounded implemented | same-session relation candidates |
| RC-6 | ✅ bounded implemented | bounded long-context strategy |
| RC-7 | ✅ bounded implemented | explicit cross-document candidate links |
| RC-9 | ✅ implemented | deterministic lexical PRE-ADMISSION candidate discovery |
| Semantic comparator | 🧊 frozen evaluation | runtime authorization = false |
| NLI neutral-filter | 🧊 frozen gate fail | runtime authorization = false |
| RRTIC-v1 | 🧩 architecture contract | runtime provider = false |
| dedicated/full Reader Core | ❌ false | implemented claim नहीं |

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
semantic_hybrid_reader_runtime         = false
nli_reader_runtime_filter              = false
rrtic_runtime_authorization            = false
```

Important proposition boundary:

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
```

## 🔎 RC-9 — current retrieval baseline

RC-9 **deterministic lexical PRE-ADMISSION candidate discovery** है। यह semantic understanding, proposition identity या truth verification नहीं है।

Historical paired K=5 control:

```text
useful hits:               15 / 16
Recall@5:                  0.937500
Precision@5:               0.187500
MRR:                       0.895833
paired hard-negative rate: 1.000000
classification: LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

## 🧪 Semantic comparator और NLI से क्या सीखा?

### Comparator v1

Frozen classification:

`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`

Semantic recall recovered, लेकिन discrimination gate fail हुआ। इसलिए यह **evaluation-only** है; semantic/vector runtime authorized नहीं है।

### NLI neutral-filter v1

Frozen classification:

`NLI_NEUTRAL_FILTER_GATE_FAILED`

NLI label proposition identity नहीं है और independent factual source भी नहीं। Runtime NLI filter authorized नहीं है।

## 🧩 RRTIC-v1 क्या है — और क्या नहीं

RRTIC-v1 एक **architecture contract for typed inspection / suspicion** है। यह runtime model/provider, reranker, semantic retriever, proposition-identity oracle, evidence admission authority, contradiction adjudicator या Canon writer नहीं है।

```text
rrtic_runtime_authorization=false
nli_reader_runtime_filter=false
semantic_hybrid_reader_runtime=false
```

## 🛡️ Authority firewall

- **Guardian** structural integrity / policy boundary है; truth oracle नहीं।
- **TruthGate** L3 admission authority है।
- **TrustSnapshot** deny-dominant reconciliation देता है।
- **CanonicalView** strict trusted read-time projection है।
- TRACE / provenance auditability देता है; provenance proof of truth नहीं है।

Public read-only surfaces:

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

ये surfaces facts create नहीं करतीं, ESM mutate नहीं करतीं और L3 में write नहीं करतीं। Explicit ingest अलग write path है।

## 🗄️ Storage reality

```text
SQLite
└── ordinary active local-first runtime

PostgreSQL 16 + pgvector
└── optional inactive target
    ├── explicit optional dependency
    ├── transactional import / equivalence checks
    └── active=false
```

Successful import activation, backend selection, cutover, rollback, dual-write, ANN acceptance या TruthGate admission नहीं है।

```text
physical L3 != strict Canon
successful import != backend activation
```

## 💶 Grant truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress / under review
award: not awarded
budget change: none
```

लगभग €50,000 केवल planning/transparency context है; approved budget या payment commitment नहीं। Agreement से पहले merged work existing baseline है।

## 🧾 Historical runtime evidence

पुराने runtime checkpoint को provenance के रूप में रखा गया है, current test-count claim के रूप में नहीं:

```text
checkpoint: bbd816c09dd39a02e6de6c1014438490572f40f6
2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% line coverage
```

Current acceptance हमेशा exact GitHub CI से तय होता है।

## 🚧 Explicit non-claims

Crystal निम्न claims नहीं करता:

- universal truth / zero hallucinations;
- AGI या consciousness;
- dedicated Reader Core implemented;
- semantic/vector Reader runtime enabled;
- RRTIC runtime authorized;
- NLI runtime filtering enabled;
- active PostgreSQL runtime;
- automatic backend switching/cutover/rollback/dual-write;
- legal/GDPR/security certification;
- native-speaker editorial certification;
- NLnet award या approved ~€50k budget।

## 📚 Navigation

- [Special for AI](./docs/ai/README.md)
- [Deep System Overview](./docs/OVERVIEW.md)
- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Status](./docs/STATUS.md)
- [Implementation Status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Security](./SECURITY.md)
- [Governance](./GOVERNANCE.md)

License: [AGPL-3.0](./LICENSE).
