# 💶 نظرة عامة على المنحة — Velantrim Crystal

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](../ja/GRANT_OVERVIEW.md) · 🇮🇳 [हिन्दी](../hi/GRANT_OVERVIEW.md)
>
> هذه الصفحة أداة ترجمة وتوجيه. لا تستبدل الطلب المقدّم أو الوثائق الإنجليزية
> الخاصة بالـ milestones والميزانية ومعايير القبول. عند الاختلاف تسود النسخة الإنجليزية.

## 📌 حالة الطلب

قُدّم Velantrim Crystal إلى **NLnet NGI0 Commons Fund** للتقييم. لا يدّعي المستودع
أن التمويل قد مُنح.

تُعرض النواة العامة بوصفها بنية ذاكرة AI محلية وقابلة للتحقق ومفتوحة المصدر.
وتتمحور الأولويات حول provenance قابلة للتدقيق، وadmission محكوم للمعرفة،
والتشغيل المحلي، وأدلة جودة قابلة للتكرار.

## 🧭 قاعدة baseline / delta

```text
BASELINE الحالية
    +
DELTA ممولة وقابلة للقياس
    =
DELIVERABLE قابلة للتحقق المستقل
```

تمنع هذه القاعدة إعادة احتساب وظيفة مدمجة مسبقاً كعمل ممول.

إذا تغير `main` قبل اتفاق رسمي، يجب تحديث مصفوفة baseline/delta. ويجب أن تبقى
الـ delta الممولة حقيقية وقابلة للقياس والتحقق من طرف ثالث.

## ✅ baseline المتاحة حالياً

تشمل النواة العامة الحالية، من بين أمور أخرى:

- تخزين L0/L1 محلياً وgraph backends لـ L3؛
- حدود admission عبر Guardian وTruthGate؛
- أنواع claims وحالة المصادر وprovenance metadata؛
- TRACE وReceipt قابلة لإعادة التحقق؛
- baseline لـ Evidence Span؛
- جلسات import وdry-run وcurator review؛
- آليات تقنية للمحو والتقييد وaudit؛
- evaluation حتمية مع CI gates؛
- واجهات FastAPI وMCP اختيارية؛
- runtime محلي ومستقل عن provider افتراضياً.

تتحدد حقيقة التنفيذ فقط بواسطة GitHub `main` و[docs/STATUS.md](../STATUS.md)
و[TEST_REPORT.md](../../TEST_REPORT.md).

## 🧱 الـ delta الممولة المخطط لها

تصف المصفوفة الإنجليزية تسعة مجالات عمل قابلة للتحقق:

| Milestone | الهدف المختصر |
|---|---|
| **M1** | baseline مفتوحة المصدر وقابلة للتكرار والنشر المحلي |
| **M2** | طبقة FastAPI اختيارية hardened بأدوار واضحة وإعدادات آمنة |
| **M3** | Evidence Span أقوى والتحقق من Receipt |
| **M4** | evaluation gates أوسع ومُصدّرة ومتعددة اللغات |
| **M5** | corpus معرفة curated مع مراجع المصادر والتراخيص |
| **M6** | knowledge adapters وinstitutional formats أكثر صلابة |
| **M7** | وصول متعدد اللغات منظم |
| **M8** | evaluation لاستقلالية model providers |
| **M9** | توثيق وgovernance وonboarding للمراجعين |

المبالغ والأولويات وأدلة القبول الدقيقة في:

- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

## 🌍 التوثيق العربي وM7

هذه الحزمة العربية تحسين docs-only للـ baseline قبل تثبيت المنحة رسمياً. لا تقدم
milestone جديدة أو بند ميزانية جديداً.

ولا يجوز وصفها بأثر رجعي على أنها تسليم M7 كاملاً. يجب أن يقدم أي M7 ممول لاحقاً
قيمة إضافية قابلة للقياس، مثل:

- بنية localization مصانة؛
- عملية review محددة للترجمات؛
- لغات إضافية متفق عليها؛
- language-specific evaluation cases وتقارير جودة؛
- مزامنة قابلة للتتبع مع releases.

## 🧪 evaluation replay وM4

يحتوي Titan على تنفيذ replay حتمي رُوجع بوصفه prior art. بالنسبة إلى Crystal:

```text
prior art موثق ≠ runtime Crystal منفذ
```

قد يستخدم M4 مستقبلي digests مستقرة وbaseline/candidate diffs وversioned fixtures
وsafety gates صارمة. ولا تدخل تلقائياً في scope:

- live capture لمسارات الاستعلامات الشخصية؛
- التحسين التلقائي أو self-modification؛
- الكتابة المباشرة أو غير المباشرة إلى Canon؛
- استدعاءات provider خارجية إلزامية؛
- الترقية التلقائية للمرشحين.

## 🔒 خارج النطاق وحدود claims

لا تدّعي المرحلة الحالية:

- SaaS مغلقاً؛
- وعياً أو شخصية أو cognition بيولوجية؛
- «صفر hallucinations»؛
- self-canonicalization مستقلة؛
- hosting multi-tenant جاهزاً للإنتاج من دون security architecture منفصلة؛
- اعتماداً إلزامياً على LLM provider محدد؛
- شهادة قانونية لـ GDPR أو شهادة أمنية؛
- Personal ExoCortex الكامل أو Titan كـ deliverable.

## 🛡️ صياغة آمنة للمراجعين

> يوفر Crystal بالفعل نواة ثقة محلية ومختبرة لذاكرة AI قابلة للتحقق. ويهدف
> التمويل المطلوب إلى engineering delta محددة وقابلة للقياس تجعل النواة أكثر
> قابلية للتكرار والنشر والتشغيل الآمن والتعدد اللغوي والتحقق المستقل.

## 📚 المصادر المعيارية

1. [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
2. [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
3. [funding-use-plan.md](../grants/funding-use-plan.md)
4. [reviewer-qa.md](../grants/reviewer-qa.md)
5. [STATUS.md](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](../ja/GRANT_OVERVIEW.md) · 🇮🇳 [हिन्दी](../hi/GRANT_OVERVIEW.md)