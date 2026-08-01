# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### بنية ذاكرة قابلة للتحقق ومحلية أولاً لأنظمة ذكاء اصطناعي موثوقة

`v0.3.0` · 🧪 **نجح 1853 اختباراً / تم تجاوز 12** · 🎯 **تغطية 100%** · 🧬 **تم كشف 7/7 من الطفرات المعلنة** · ✅ **9 مهام CI** · 🐍 **مسار التشغيل الافتراضي يعتمد مكتبة Python القياسية فقط** · ⚖️ **AGPL-3.0**

> Crystal ليس روبوت محادثة آخر. إنه حدٌّ للذاكرة والأدلة والقرارات، يسجل ماهية
> الادعاء ومصدره وحالته المعرفية، وما إذا كان يجوز أن يؤسس إجابة، وكيف تمت
> معالجة التناقض بقرار صريح.

**نقطة التشغيل المتحقق منها:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — تم دمج PR #302.  
**الأدلة الدقيقة:** [TEST_REPORT.md](./TEST_REPORT.md) و
[بيان التنفيذ المقروء آلياً](./docs/status/implementation-manifest.json).

> تحافظ هذه الترجمة على حدود القدرات والأمان والحالة نفسها الموجودة في README
> الإنجليزي. تبقى أسماء API الثابتة بصيغتها البرمجية، بينما صيغت الشروحات بلغة
> عربية طبيعية.

---

## 🎯 لماذا يوجد Crystal؟

تخلط أنظمة ذكاء اصطناعي كثيرة بين المستندات المصدرية، وأقوال المستخدم، ومخرجات
النموذج، والفرضيات، والمقاطع المسترجعة، والذاكرة الدائمة داخل سياق واحد أو مخزن
متجهي واحد. عندئذ قد يكتسب النص السلس سلطة لا تدعمها أدلته.

```text
الادعاء المقنع ليس موثوقاً تلقائياً.
عقدة الرسم البياني ليست جزءاً من Canon الصارم تلقائياً.
درجة الاسترجاع ليست دليلاً.
مخرجات النموذج ليست مصدراً مستقلاً.
التناقض لا يختار الفائز بنفسه.
وسم الموضوع ليس حكماً على الحقيقة.
```

## 🧠 القدرات الأساسية

- ادعاءات محددة النوع ودورة حياة معرفية صريحة؛
- بيانات المصدر ومقاطع الأدلة وسجل المنشأ؛
- حدود قبول عبر Guardian وTruthGate؛
- رسم L3 مادي متعدد الحالات منفصل عن Canon الصارم؛
- تسوية قراءة `TrustSnapshot` غير قابلة للتغيير وتعطي الأولوية للرفض؛
- استعلامات عامة HTTP وCLI وMCP للقراءة فقط؛
- TRACE وReceipts قابلة لإعادة التشغيل وتكشف العبث؛
- قيود معالجة ومحو وتدقيق وجلسات استيراد؛
- طوابير مراجعة وجلسات قابلة للاستئناف؛
- تقارير تناقض محددة النوع وغير قابلة للتغيير؛
- قرارات صريحة `COEXIST` و`CONTEXTUALIZE` و`SUPERSEDE`؛
- حل التعارض عبر CLI وHTTP موثّق؛
- أدوار قيّمين محددة النطاق وleases محلية للقرارات؛
- faceting موضوعي إرشادي لا يمنح أي سلطة معرفية؛
- مواصفة ESM مقروءة آلياً؛
- تقييم حتمي وتغطية 100% وRing Zero mutation gate؛
- سجل إصدارات لاختبارات L3 المعيارية.

## 🏛️ نظرة معمارية

```text
إدخال صريح
→ تصنيف الادعاء + بيانات الأدلة
→ حالة Observed في L0/L1
→ Guardian → TruthGate → فحوص القيود والتناقض
→ رسم L3 مادي متعدد الحالات

استعلام عام
→ استرجاع للقراءة فقط
→ TrustSnapshot غير قابل للتغيير
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ إجابة / رفض / Receipt

تناقض غير محلول
→ ContradictionReport غير قابل للتغيير
→ تفويض actor/الدور/النطاق + decision lease
→ قرار صريح من القيّم + السبب
→ مسار كتابة قانوني قابل للتدقيق

تنقل موضوعي
→ TopicFacet إرشادي
→ تصفية وتجميع فقط — بلا قبول في Canon
```

```text
رسم L3 المادي ≠ Canon الصارم
الاستعلام ≠ الإدخال
الثقة ≠ دليل مستقل
مخرجات LLM ≠ مصدر حقائق مستقل
صلة الموضوع ≠ الحقيقة
lease محلية ≠ ضمان تنسيق موزع
```

TruthGate بوابة لسياسة القبول، وليس عرّافاً يعرف الحقيقة الموضوعية بصورة مستقلة.
أما Canon الصارم فهو إسقاط قراءة تسمح به السياسة بناءً على الأدلة والحالة وESM
وقيود المعالجة.

## 🛡️ حد الاستعلام العام للقراءة فقط

تستخدم `HTTP /ask` و`HTTP /receipt` و`CLI ask` و`CLI receipt` و`MCP search`
المسار المشترك `core.query_pipeline`. وهي لا تنشئ حقائق، ولا تغيّر ESM، ولا تكتب
في L3، ولا تشغّل outbox، ولا تهيّئ embedding fingerprint.

راجع [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ حل التناقضات بقرار صريح

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "الادعاءات تصف سياقات مختلفة" \
  --expected-report-id REPORT_ID
```

في FastAPI يجب تسجيل `POST /review/resolve-conflict` مع مصادقة التطبيق المضيف.
يتحقق `core.curator_auth` من actor والصلاحيات والنطاق. تحمي
`CuratorLeaseRegistry` عملية واحدة فقط؛ ويتطلب النشر الموزع محول lease خارجياً.

راجع [واجهات حل التعارض](./docs/CONFLICT_RESOLUTION_SURFACES.md) و
[Topic facets وcurator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md).

## 🏷️ faceting موضوعي إرشادي

يوفر `core.topic_facets` وسوماً موحدة للتنقل والتصفية والتجميع. تقيس الدرجة صلة
الموضوع فقط، ولا تغيّر حالة الحقيقة أو الأدلة أو ESM أو عضوية Canon الصارم.

## 🚀 البدء السريع

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 مسار الوثائق

- [خريطة الوثائق](./docs/DOCUMENTATION_MAP.md)
- [الحالة الحالية](./docs/STATUS.md)
- [المعمارية](./docs/ARCHITECTURE.md)
- [تقرير الاختبارات](./TEST_REPORT.md)
- [التقييم](./docs/EVAL.md)
- [نطاق NLnet](./docs/GRANT_NLNET_SCOPE.md)

## ✅ خط الأساس المتحقق منه

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 حدود الادعاء

لا يدّعي Crystal اكتشاف الحقيقة عالمياً، أو إزالة جميع الهلوسات، أو تقديم شهادة
GDPR أو أمنية، أو الجاهزية لخدمة إنتاج متعددة المستأجرين، أو تحقيق وعي اصطناعي،
أو تنفيذ Titan/Full ExoCortex. تعمل leases الحالية داخل عملية واحدة فقط؛ ويبقى
التنسيق الموزع وربط مزود هوية خارجي عملاً مستقلاً.

## 🤝 المساهمة والترخيص

راجع [CONTRIBUTING.md](./CONTRIBUTING.md) و[SECURITY.md](./SECURITY.md) و
[GOVERNANCE.md](./GOVERNANCE.md) و[AGPL-3.0](./LICENSE).
