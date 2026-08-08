# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### بنية تحتية قابلة للتحقق ومحلية أولاً للذاكرة والأدلة والقرارات في أنظمة الذكاء الاصطناعي الموثوقة

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **تم القضاء على 7/7 من Ring Zero mutants المعلنة** · ✅ **9 وظائف CI دائمة** · 🐍 **الـ runtime الافتراضي يعتمد على مكتبة Python القياسية فقط** · ⚖️ **AGPL-3.0**

> Crystal ليست chatbot أخرى وليست «عرافاً مستقلاً للحقيقة». إنها حدّ للذاكرة والدليل والقرار يسجل ماهية claim، ومصدرها، وحالتها epistemic state، وهل يمكنها grounding إجابة، وكيف عولج contradiction بقرار صريح وقابل للتدقيق.

**runtime checkpoint الموثق:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337 مدموجة.  
**validated head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — نجاح 9/9.  
**PostgreSQL integration:** `31256316532` — PostgreSQL 16 + pgvector 0.8.2.  
**الأدلة الأساسية:** [TEST_REPORT.md](./TEST_REPORT.md)، [STATUS.md](./docs/STATUS.md)، و[implementation manifest](./docs/status/implementation-manifest.json).

> **عقد الترجمة:** هذه النسخة عرض عربي كامل بصرياً ودلالياً وليست ملخصاً قصيراً. تبقى الإنجليزية مصدر العمل الأساسي وحسم التعارض، وتُترجم المستندات المستقرة الأخرى على مراحل. راجع [سياسة الترجمة](./docs/LOCALIZATION_POLICY.md) و[حالة الترجمات](./docs/TRANSLATION_STATUS.md).

---

## 🎯 لماذا توجد Crystal

تخلط أنظمة AI كثيرة مستندات المصدر، وأقوال المستخدم، ومخرجات النموذج، والفرضيات، ومقاطع retrieval، والذاكرة الدائمة في context أو vector store واحد. من دون حدود صريحة قد يكتسب النص المقنع سلطة لا تدعمها أدلته.

```text
الـ claim البليغة لا تصبح موثوقة تلقائياً.
physical graph node لا تصبح strict Canon تلقائياً.
retrieval score ليس evidence.
model output ليس مصدراً واقعياً مستقلاً.
contradiction لا يختار الفائز بنفسه.
TopicFacet label ليس حكماً على الحقيقة.
successful import لا يعني backend activation.
```

## 🧠 ما الذي تقدمه Crystal

- claims typed ودورة حياة epistemic صريحة؛
- source identity وexact evidence spans وprovenance؛
- حدود admission عبر Guardian وTruthGate؛
- physical L3 graph متعدد الحالات منفصل عن strict Canon؛
- `TrustSnapshot` ثابت وdeny-dominant؛
- واجهات HTTP وCLI وMCP عامة للقراءة فقط؛
- TRACE وReceipts قابلة لإعادة التشغيل وكاشفة للتلاعب؛
- restrictions وerasure وaudit وimport sessions؛
- review queues وreview sessions قابلة للاستئناف؛
- `ContradictionReport` ثابت؛
- قرارات `COEXIST` و`CONTEXTUALIZE` و`SUPERSEDE`؛
- scoped curator capabilities وprocess-local decision leases؛
- TopicFacet استشاري بلا سلطة على الحقيقة؛
- evaluation حتمي و100% line coverage وRing Zero mutation gate؛
- SQLite backup/restore وbounded logical migration موثقان؛
- PostgreSQL/pgvector import اختياري inactive مع exact-state equivalence مستقلة.

## 🏛️ ثلاث رؤى للمعمارية

### 🧠 خريطة ذهنية

```text
🧠 Crystal
├── 🎯 الغاية
│   ├── ذاكرة قابلة للتحقق للـ AI
│   ├── trust infrastructure محلية أولاً
│   └── إجابات وقرارات مرتبطة بالدليل
├── 🏛️ Memory
│   ├── L0 — working cache سريع
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
│   ├── SQLite — profile عادي local-first
│   └── PostgreSQL/pgvector — inactive target
└── 📊 Verification
    ├── Python 3.11 / 3.12
    ├── 100% coverage
    ├── mutation / security / Docker
    └── exact-head CI evidence
```

### 🏗️ تدفق المعلومات

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

### 🌳 شجرة الوحدات

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

## 🧭 الفروق المركزية

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

TruthGate بوابة admission policy وليست oracle تعرف الحقيقة الموضوعية وحدها. strict Canon هو policy-allowed read projection فوق evidence وstatus وESM state وشكل confidence وprocessing restrictions.

## 🧱 أسطح الذاكرة والدليل

| السطح | الدور | الحد الحاسم |
|---|---|---|
| L0 | working cache داخل العملية | سريع وقابل لإعادة البناء |
| L1 | ذاكرة SQLite/WAL التشغيلية | lifecycle وrestrictions |
| L2 | logical review boundary | ليس Canon تلقائياً |
| L3 | physical multi-status memory | وجود السجل ≠ الثقة |
| TrustSnapshot | immutable reconciliation | deny-dominant resolution |
| CanonicalView | strict grounding projection | policy-allowed reads فقط |
| TRACE / Receipt | proof وreplay | grounding وdrift وtamper evidence |
| ContradictionReport | conflict ثابت | confidence لا يختار الفائز |
| TopicFacet | navigation metadata | لا يغير truth أوESM أوCanon |

## 🗄️ SQLite وPostgreSQL/pgvector

```text
SQLite
└── runtime profile عادي local-first
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

هدف PostgreSQL غائب عن runtime composition العادية ولا يخدم reads/writes عادية. نجاح import لا يثبت activation أوautomatic selection أوcutover أوrollback أوdual-write أوTruthGate admission أوstrict Canon membership أوANN acceptance أوproduction multi-tenancy.

## 🔎 Crystal مقارنة بـ RAG التقليدي

| السؤال | RAG تقليدي | Crystal |
|---|---|---|
| العثور على مادة ذات صلة | نقطة القوة الأساسية | retrieval adapters |
| فصل قول المستخدم عن fact موثق | منطق التطبيق | explicit typed boundary |
| تتبع lifecycle والتناقضات | غالباً خارجي | first-class states / reports |
| منع النص المولد من أن يصبح مصدره | ليس inherent | Ring Zero invariant |
| إعادة تشغيل evidence للإجابة | اختياري | TRACE / Receipt |
| حل contradiction بمساءلة | خاص بالتطبيق | authorized dispositions |
| العمل بلا cloud/model provider إلزامي | يختلف | pure-stdlib local-first baseline |

## 🛡️ الحد العام للقراءة فقط

تشترك `HTTP /ask` و`HTTP /receipt` و`CLI ask` و`CLI receipt` و`MCP search` في `core.query_pipeline`. لا تنشئ facts ولا تغير ESM state ولا تكتب في L3 ولا تعدّل Canon.

## ⚖️ قرار صريح للتناقض

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "claims describe different contexts" \
  --expected-report-id REPORT_ID
```

يمنع `CuratorLeaseRegistry` القرارات المتزامنة داخل process واحدة فقط؛ deployment موزع يحتاج external lease adapter.

## 🚀 البدء السريع

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

أدوات PostgreSQL inactive الاختيارية: `pip install -e '.[postgresql]'`.

## 📚 التنقل في التوثيق

- [الفهرس العربي](./docs/ar/README.md)
- [English documentation map](./docs/DOCUMENTATION_MAP.md)
- [Test report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Security](./SECURITY.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)

## ✅ خط الأساس الموثق

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

## 🚧 حدود الادعاء

لا تدّعي Crystal اكتشافاً عالمياً للحقيقة الموضوعية، أو zero hallucinations، أو شهادة GDPR/security قانونية، أو production-ready multi-tenancy، أو distributed locking، أو AGI/وعي، أو active PostgreSQL runtime، أو automatic switching، أو cutover/rollback، أو Reader Core مخصصاً مكتملاً. ما زال مقترح NLnet **submitted / under review / not awarded**.

## 🤝 المساهمة والترخيص

راجع [CONTRIBUTING.md](./CONTRIBUTING.md)، [SECURITY.md](./SECURITY.md)، [GOVERNANCE.md](./GOVERNANCE.md)، و[AGPL-3.0](./LICENSE).
