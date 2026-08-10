# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### بنية local-first قابلة للتحقق للذاكرة والأدلة والقرارات في أنظمة الذكاء الاصطناعي الموثوقة

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 stdlib-only default runtime · ⚖️ **AGPL-3.0**

> Crystal ليس chatbot ولا «oracle للحقيقة» يعمل ذاتياً. إنه memory/evidence/decision boundary يحفظ أصل الادعاء وحالته المعرفية وإمكانية استخدامه في grounding والقرارات الصريحة القابلة للتدقيق حول التناقضات.

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** تم تنفيذ واختبار RC-1 evidence-linked skeleton وRC-2 caller-supplied Structural Document Map؛ أما dedicated multi-pass Reader فلم يُنفذ.  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md)، [STATUS.md](./docs/STATUS.md)، [implementation manifest](./docs/status/implementation-manifest.json).

> تبقى الإنجليزية المصدر الأساسي والحاسم عند التعارض. هذا README عرض عام كامل وليس ملخصاً قصيراً. راجع [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) و[docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 لماذا Crystal

تخلط كثير من أنظمة AI/RAG بين الوثائق وأقوال المستخدم وmodel output والفرضيات والذاكرة. عندها قد يكتسب نص مقنع authority لا تدعمها الأدلة.

```text
fluent claim        != trusted fact
physical L3         != strict Canon
retrieval score     != evidence
model output        != independent source truth
migration receipt   != claim evidence
import success      != backend activation
Reader coverage     != comprehension proof
Reader structure    != truth/confidence authority
```

## 🧠 ما الذي يقدمه Crystal

- typed claims وepistemic lifecycle صريح؛
- source identity وevidence spans وprovenance؛
- Guardian وTruthGate كحدود admission؛
- physical L3 متعدد الحالات منفصل عن strict Canon؛
- TrustSnapshot وCanonicalView بسياسة deny-dominant؛
- HTTP /ask وCLI ask وMCP search للقراءة فقط؛
- TRACE وReceipts قابلة لإعادة التحقق ومقاومة للعبث؛
- review queue/session وContradictionReport؛
- قرارات COEXIST / CONTEXTUALIZE / SUPERSEDE الصريحة؛
- scoped curator capabilities وprocess-local leases؛
- SQLite lifecycle وbounded logical migration؛
- optional PostgreSQL/pgvector inactive import مع `active=false`؛
- RC-1: source/version/session وSegmentCard وfidelity وcoverage وbookmarks/open loops وstale/failure/privacy؛
- RC-2: بنية caller-supplied مرتبطة بالإصدار مع RECOVERED / AMBIGUOUS / UNSUPPORTED.

لا يحتفظ RC-1/RC-2 بنص المصدر، ولا يضيفان Reader API/CLI/worker أو durable Reader schema، ولا يملكان Canon/ESM/planner authority. لا يوجد automatic parser/OCR أو Reader LLM/provider orchestration أو embeddings/ANN/vector DB أو multi-pass/cross-document runtime.

## 🏛️ ثلاث رؤى للمعمارية

### 🧠 Mind map

```text
🧠 Crystal
├── 📖 Reader foundation
│   ├── RC-1 evidence-linked skeleton
│   ├── RC-2 Structural Document Map
│   └── dedicated multi-pass Reader — NOT IMPLEMENTED
├── 🏛️ Memory
│   ├── L0 — working cache
│   ├── L1 — operational SQLite/WAL
│   ├── L2 — pending/review
│   └── L3 — physical multi-status graph
├── 🛡️ Trust
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
└── 🗄️ Storage
    ├── SQLite — active local-first
    └── PostgreSQL/pgvector — inactive active=false
```

### 🏗️ تدفق المعلومات

```text
Source / document
      ↓
RC-1 Reader artifacts
      ↓
RC-2 structural metadata
      ↓
explicit ingest / review
      ↓
Guardian → TruthGate
      ↓
L1 + physical L3
      ↓
TrustSnapshot → CanonicalView STRICT
      ↓
Grounded answer / bounded refusal
      ↓
TRACE + Receipt
```

### 🌳 شجرة الوحدات

```text
🌳 core
├── reader_core.py       # RC-1
├── reader_structure.py  # RC-2
├── evidence.py
├── truth_gate.py
├── pipeline.py
├── query_pipeline.py
└── storage/...
```

## 🧱 أسطح الذاكرة والسلطة

| السطح | الدور | الحد الحاسم |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable |
| L2 | review/pending | لا admission تلقائي |
| L3 | physical graph | multi-status |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence لا truth generator |
| ContradictionReport | conflict | لا winner تلقائي |

## 🗄️ SQLite وPostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first runtime
    ├── reads/writes
    ├── backup/restore
    └── bounded logical export

PostgreSQL 16 + pgvector
└── optional inactive target
    ├── explicit optional dependency
    ├── SERIALIZABLE import
    ├── exact target re-hash
    └── active=false
```

نجاح import لا يعني activation أو cutover أو rollback أو dual-write أو automatic switching أو ANN acceptance أو TruthGate admission. لا يوجد normal PostgreSQL runtime adapter نشط.

## 🔎 Crystal مقابل Classic RAG

| السؤال | Classic RAG | Crystal |
|---|---|---|
| العثور على مادة ذات صلة | الوظيفة الرئيسية | adapters |
| claim مقابل trusted fact | app-specific | typed boundary |
| provenance | متغير | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| منع model self-source | ليس inherent | Ring Zero |
| التناقضات | منطق خارجي | explicit dispositions |
| replay evidence | optional | TRACE / Receipt |
| cloud/model إلزامي | يختلف | لا في default runtime |

## 🛡️ Query boundary للقراءة فقط

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

هذه الأسطح لا تنشئ facts ولا تغير ESM ولا تكتب L3. يبقى explicit ingest مسار كتابة منفصلاً.

## ⚖️ قرارات التناقض

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

## ✅ Baseline متحقق

```text
Runtime checkpoint: bbd816c09dd39a02e6de6c1014438490572f40f6
Python 3.11/3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
CI: 9/9
Ring Zero: 7/7
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
PostgreSQL target: active=false
```

## 🚧 ما لا يدعيه Crystal

لا يدعي Crystal universal truth أو zero hallucinations أو AGI/consciousness أو legal/GDPR/security certification أو production multi-tenancy أو distributed exactly-once أو active PostgreSQL runtime أو automatic switching/cutover/rollback/dual-write أو automatic Reader parsing أو embeddings/ANN/vector Reader stack أو completed dedicated multi-pass Reader Core.

تبقى NLnet **submitted / under review / not awarded**؛ نحو €50,000 للتخطيط فقط، budget change none. العمل merged قبل الاتفاق يبقى baseline.

## 📚 التنقل

- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Quick Start](./docs/QUICKSTART.md)
- [Status](./docs/STATUS.md)
- [Implementation Status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Security](./SECURITY.md)
- [Governance](./GOVERNANCE.md)
- [Contributing](./CONTRIBUTING.md)

## 🤝 المساهمة والترخيص

يجب أن تحافظ التغييرات على authority boundaries وtests/coverage ودقة claims. راجع [CONTRIBUTING.md](./CONTRIBUTING.md). الترخيص: [AGPL-3.0](./LICENSE).
