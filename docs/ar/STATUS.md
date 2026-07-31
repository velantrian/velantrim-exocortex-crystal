# 📌 Velantrim Crystal — الحالة الحالية

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 **العربية**

**تاريخ الحالة:** 31 يوليو 2026  
**حالة المستودع المستخدمة لهذه الترجمة:** `main@9f90cb60`  
**آخر checkpoint غيّر runtime:** PR #265 / `cd6fd44`  
**baseline الاختبارات المعيارية:** [TEST_REPORT.md](../../TEST_REPORT.md)

> هذه الصفحة ترجمة للحالة. عند الاختلاف تكون GitHub `main` و[STATUS الإنجليزي](../STATUS.md)
> و[TEST_REPORT.md](../../TEST_REPORT.md) هي المرجع.

---

## 🧭 قاعدة القراءة

```text
GitHub Crystal main = حقيقة التنفيذ العامة
Notion Crystal       = خريطة منحة واستراتيجية متزامنة
Titan / Full         = مختبر بحث منفصل
```

لا يُعد أي مستند أو ملاحظة Notion أو prototype branch أو module من Titan capability
حالية في Crystal حتى يُنفذ ويُختبر ويُدمج في `main`.

## ✅ checkpoint المتحقق

أدخل PR #265 حد HTTP صارماً للقراءة فقط:

```text
POST /ingest   → admission عبر Guardian + TruthGate
POST /ask      → استعلام قانوني للقراءة فقط
GET  /receipt  → قراءة صارمة مع Receipt
```

لا تكتب HTTP endpoints `/ask` و`/receipt` في L0/L1 أو L3، ولا تغيّر ESM، ولا تشغّل
outbox، ولا تسجل روابط حلقية، ولا تهيّئ `embedding fingerprint`، ولا تعدّل adaptive verification.

### الحدود المتبقية الصريحة

- CLI `ask` و`receipt` ما زالت على `core.pipeline.run()`؛
- `core.pipeline.run()` مسار توافق قادر على admission؛
- MCP لا يملك أداة كتابة قانونية صريحة، لكن البحث قد يهيّئ fingerprint مفقوداً.

هذه follow-ups معروفة وليست claims تنفيذ مخفية.

## 🧪 baseline التحقق

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

أكمل CI run `30284938992` الوظائف السبع الدائمة قبل الدمج: Python 3.11/3.12،
Ruff، security، Docker build، evaluation gate وJSONL integrity.

## 🛡️ حدود claims العامة

يمكن وصف Crystal بأنه:

- بنية ذاكرة AI محلية أولاً وقابلة للتحقق؛
- نواة ذاكرة تركز على المصادر وprovenance؛
- نظام بحدود admission عبر Guardian وTruthGate حيث تكون موصولة؛
- نظام يستخدم CanonicalView وTRACE وReceipt قابلة لإعادة التحقق حيث تكون موصولة؛
- runtime افتراضي بمكتبة Python القياسية مع محولات اختيارية؛
- مشروع بآليات محو وتقييد تقنية ذات صلة بـ GDPR؛
- baseline مفتوحة المصدر قابلة للاختبار المستقل.

لا يجوز وصف Crystal بأنه:

- Titan أو Personal ExoCortex الكامل؛
- نظام تشغيل معرفي مستقل؛
- واعٍ أو حي أو مماثل بيولوجياً للدماغ؛
- صحيح عالمياً أو خالٍ تماماً من hallucinations؛
- معتمد قانونياً وفق GDPR؛
- معتمد أمنياً أو جاهزاً لـ multi-tenant production؛
- معتمداً إلزامياً على LLM خارجي أو cloud provider.

## 💶 حالة المنحة

قُدم الطلب إلى **NLnet NGI0 Commons Fund** وهو قيد التقييم. لا يدّعي المستودع أن
التمويل قد مُنح.

```text
BASELINE الحالية
    +
DELTA ممولة وقابلة للقياس
    =
DELIVERABLE قابلة للتحقق المستقل
```

يبقى العمل المدمج ضمن baseline ولا يُحتسب مرة أخرى كـ milestone مدفوعة. تُحفظ
القواعد المعيارية في:

- [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

الملخص العربي في [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md).

## 🧪 قرار evaluation replay

رُوجع replay الحتمي في Titan بوصفه prior art، ولم يُنسخ إلى runtime Crystal.

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

أي تنفيذ مستقبلي يجب أن يمدد stack التقييم الحالي، ويمر عبر RFC/issue/PR منفصل،
ويبقى offline وغير سلطوي، ويحافظ على TruthGate وحدود الاستعلام.

## 📚 مسار المراجع

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)
4. [GLOSSARY.md](./GLOSSARY.md)
5. [الحالة الإنجليزية المعيارية](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 **العربية**