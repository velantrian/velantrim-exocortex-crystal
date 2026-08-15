# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->
<!-- current-localization-source: main@9e048c21fb929f7d299e3af0ef03d76c1df899d6 -->

## 💠 بنية ذاكرة وأدلة تفصل الاسترجاع عن الحقيقة

Crystal هو خط بحث وتنفيذ **local-first** لذاكرة ذكاء اصطناعي قابلة للتدقيق. الفكرة الأساسية بسيطة ومحافظة: العثور على مادة تبدو ذات صلة لا يمنحها تلقائياً صفة الدليل، ولا يجعلها حقيقة، ولا يسمح لها بالدخول إلى Canon.

> 👤 **هل هذه أول مرة تقرأ عن Crystal؟** ابدأ بهذه الصفحة؛ فهي بوابة بشرية أولاً.
>
> 🤖 **للـ AI / agents / المدققين الآليين:** ابدأ من **[Special for AI →](./docs/ai/README.md)** ولا تعِد بناء الحالة الحالية من هذا README السردي وحده.
>
> 📚 **للتفاصيل المعمارية الأعمق:** انتقل إلى **[Deep System Overview →](./docs/OVERVIEW.md)**.

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐍 standard-library-first default runtime · ⚖️ **AGPL-3.0**

## 👋 ما هو Crystal؟

أنظمة RAG التقليدية تجيب جيداً عن سؤال مثل: «ما النص الأقرب إلى هذا الاستعلام؟». Crystal يهتم بالأسئلة التالية بعد ذلك:

- من أين جاءت المعلومة؟
- هل تدعم نفس proposition أم موضوعاً قريباً فقط؟
- هل وصلت إلى evidence admission أم ما زالت candidate؟
- هل تم adjudication للتناقض فعلاً؟
- هل يسمح policy بدخولها إلى trusted memory؟
- ماذا يمكن للنظام عرضه بأمان باعتباره grounded؟

القاعدة المركزية:

> **candidate discovery قد يقترح ما يستحق الفحص؛ candidate adjudication ومسار السلطة منفصلان.**

```text
fluent claim                  != trusted fact
retrieval match               != evidence
similarity                    != identity
NLI label                     != proposition identity
RRTIC suspicion               != adjudicated relation
physical L3                   != strict Canon
Reader candidate              != admitted evidence
contradiction candidate       != confirmed contradiction
```

## 🧠 النموذج الذهني

```text
💠 Crystal
├── 📥 Sources / explicit ingest
├── 📖 Reader RC-1 … RC-7
│   ├── provenance + structure
│   ├── multi-pass mechanics
│   ├── propositions
│   ├── relation candidates
│   ├── long-context working sets
│   └── cross-document candidate links
├── 🔎 RC-9 lexical PRE-ADMISSION discovery
├── 🧪 frozen comparator / NLI evaluation evidence
├── 🧩 RRTIC-v1 typed inspection contract
├── 🛡️ Guardian → TruthGate
├── 🏛️ L0 / L1 / L2 / physical L3
├── 🔐 TrustSnapshot → CanonicalView
└── 🧾 TRACE / Receipt
```

## 🏗️ مسار البيانات مقابل مسار السلطة

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
      ║  لا توجد سلطة تلقائية
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

هذا الفصل هو سبب وجود Crystal: ranking وretrieval وReader inspection أدوات اكتشاف وفحص، وليست طريقاً مختصراً إلى epistemic authority.

## 📖 ما الذي تم تنفيذه في Reader فعلياً؟

| الطبقة | الحالة | الحد الحاسم |
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
| dedicated/full Reader Core | ❌ false | لا يُدّعى أنه منفذ |

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
rrtic_runtime_provider                 = false
```

وللتوافق مع validators التاريخية يبقى أيضاً النص الدقيق:

```text
reader_core_rc5_relation_candidates    = true
contradiction candidate  != confirmed contradiction
```

## 🔎 RC-9 — baseline الاسترجاع الحالي

RC-9 هو **deterministic lexical PRE-ADMISSION candidate discovery**. لا يُسوَّق باعتباره semantic understanding ولا automatic truth verification.

Historical paired K=5 control:

```text
useful hits:               15 / 16
Recall@5:                  0.937500
Precision@5:               0.187500
MRR:                       0.895833
paired hard-negative rate: 1.000000
classification: LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

Evaluation Surface v2 أظهر أن lexical baseline مفيد لكنه لا يحل وحده multi-stratum retrieval/discrimination gaps.

## 🧪 ما الذي تعلمناه من المقارنات الدلالية؟

### Comparator v1

Frozen classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

```text
Recall@5:             1.000000
MRR:                  1.000000
hard-negative rate:   0.854167
runtime authorization: false
```

استعاد semantic recall، لكنه فشل في discrimination gate، ولذلك **لم يتحول إلى production Reader runtime**.

### NLI neutral-filter v1

Frozen classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
Recall@5:             0.958333
MRR:                  1.000000
hard-negative rate:   0.375000
runtime authorization: false
```

خفض leakage لكنه لم يكن recall-safe وفق frozen gate. النتيجة evidence للتقييم فقط.

## 🧩 RRTIC-v1 — عقد الفحص، لا محرك حقيقة

RRTIC-v1 يجمّد suspicion-only relation families ويجعل qualifier mismatches مرئية قبل أي authority decision.

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

```text
identity_claimed=false
evidence_admitted=false
adjudication_performed=false
runtime_authorization=false
```

RRTIC لا يفلتر أو يعيد الترتيب تلقائياً، ولا يقرر proposition identity، ولا يكتب Canon، ولا يسجل RC-5 relation تلقائياً.

## 🛡️ جدار السلطة الدائم

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
coverage != comprehension proof
pass completion != comprehension proof
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
retrieval match != evidence
candidate discovery != candidate adjudication
```

أي retrieval أو ranking أو similarity أو NLI أو RRTIC diagnostic يبقى خارج evidence admission إلى أن يمر عبر المسار المصرح به.

## 🏛️ L0 / L1 / L2 / L3

| السطح | الدور | ما لا يعنيه |
|---|---|---|
| L0 | working cache | ليس ذاكرة موثوقة دائمة |
| L1 | operational local state | لا يساوي Canon تلقائياً |
| L2 | pending / review | لا admission ذاتي |
| physical L3 | multi-status graph | **physical L3 != strict Canon** |
| TrustSnapshot | reconciliation | لا يمنح retrieval authority |
| CanonicalView | trusted projection | policy-allowed only |
| TRACE / Receipt | audit / replay | operation evidence لا truth generator |

## 🗄️ SQLite وPostgreSQL/pgvector

```text
SQLite ordinary local-first             ACTIVE
PostgreSQL/pgvector import target        INACTIVE
PostgreSQL normal runtime adapter        NOT IMPLEMENTED
PostgreSQL Reader activation             NOT AUTHORIZED
active=false
```

نجاح import أو exact-state equivalence هو دليل على سلامة العملية، وليس activation أو cutover أو dual-write أو rollback أو automatic switching.

## 🔐 واجهات القراءة العامة

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

هذه الواجهات لا تنشئ facts ولا تعدّل Canon ولا تمنح نتيجة retrieval صفة evidence.

## ⚖️ التناقضات

```text
unresolved contradiction
        ↓
ContradictionReport
        ↓
scoped curator + capability + lease
        ↓
COEXIST / CONTEXTUALIZE / SUPERSEDE
        ↓
audited canonical write path
```

لا يوجد automatic winner selection من Reader أو similarity أو NLI.

## ✅ دليل التشغيل التاريخي المحتفظ به

هذا checkpoint مهم كدليل runtime تاريخي، لكنه ليس وصفاً لآخر عدد اختبارات بعد كل milestone لاحق:

```text
verified runtime checkpoint:
bbd816c09dd39a02e6de6c1014438490572f40f6

Python 3.11 / 3.12:
2078 passed / 13 skipped / 0 failed

9756 statements / 100.00% line coverage
CI: 9/9
Ring Zero: 7/7
```

## 💶 حقيقة المنحة

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

الحالة الدقيقة المختصرة تبقى: **submitted / under review / not awarded**. نحو **€50,000** هو planning/transparency context فقط، وليس awarded budget أو التزام دفع. ما تم دمجه قبل أي اتفاق يبقى existing baseline ولا يجوز احتسابه لاحقاً كـ funded delta جديد.

## 🚧 Capability reality-check

| الادعاء | الحقيقة الحالية |
|---|---|
| Reader RC-1…RC-7 | ✅ bounded implemented |
| RC-9 lexical discovery | ✅ implemented |
| semantic/hybrid Reader runtime | ❌ false |
| NLI runtime filter | ❌ false |
| RRTIC runtime provider | ❌ false |
| dedicated/full Reader Core | ❌ false |
| active PostgreSQL runtime | ❌ false (`active=false`) |
| automatic backend switching | ❌ false |
| automatic contradiction adjudication | ❌ false |
| legal/GDPR/security certification | ❌ not claimed |
| native-speaker editorial certification | ❌ not claimed |
| NLnet award | ❌ not awarded |

## 🚀 البدء السريع

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

PostgreSQL اختياري: `pip install -e '.[postgresql]'`.

## 🧭 أين تذهب بعد ذلك؟

- 👤 [Deep System Overview](./docs/OVERVIEW.md)
- 🤖 [Special for AI](./docs/ai/README.md)
- 📊 [Current State for AI](./docs/ai/CURRENT_STATE.md)
- 🗺️ [Documentation map](./docs/DOCUMENTATION_MAP.md)
- 📖 [Reader architecture](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- 🧾 [Status](./docs/STATUS.md)
- 🧱 [Implementation Status](./docs/IMPLEMENTATION_STATUS.md)
- 🛡️ [Security](./SECURITY.md)
- ⚖️ [Governance](./GOVERNANCE.md)

Localization governance remains explicit:

```text
docs/LOCALIZATION_POLICY.md
docs/TRANSLATION_STATUS.md
```

الإنجليزية هي المصدر الحاكم عند التعارض. كلمة `CURRENT` تعني parity against a recorded source/audit contract، ولا تعني native-speaker certification ولا freshness تلقائية بعد أي تغيير إنجليزي مستقبلي.
