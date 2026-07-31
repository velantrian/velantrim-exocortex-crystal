# 🇸🇦 التوثيق العربي — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/README.md) · 🇫🇷 [Français](../fr/README.md) · 🇪🇸 [Español](../es/README.md) · 🇮🇹 [Italiano](../it/README.md) · 🇷🇺 [Русский](../ru/README.md) · 🇨🇳 [简体中文](../zh-CN/README.md) · 🇸🇦 **العربية**

## 🔒 قاعدة الترجمة والمرجعية

هذه الصفحات مسار عربي مصان للمراجعين والمؤسسات والمساهمين. لا تغيّر runtime أو
نطاق المنحة.

```text
GitHub main + الوثائق الإنجليزية المعيارية = المصدر الحاكم
الوثائق الألمانية والفرنسية والإسبانية والإيطالية والروسية والصينية والعربية = ترجمات وأدلة قراءة
```

عند الاختلاف يُطبّق الترتيب التالي:

1. الكود المدمج فعلياً في GitHub `main`؛
2. [TEST_REPORT.md](../../TEST_REPORT.md) لأرقام الاختبارات والتغطية؛
3. [docs/STATUS.md](../STATUS.md) لحالة التنفيذ الحالية؛
4. وثائق المنحة الإنجليزية للنطاق والميزانية والمخرجات.

لا يجوز للترجمة أن تقوّي أي capability مقارنة بالمصدر الإنجليزي. عبارات مثل
«مرتبط بـ GDPR» و«hardened» و«قابل للتحقق» و«محلي» أوصاف تقنية وليست شهادات
قانونية أو أمنية.

---

## 🧭 مسار القراءة المقترح

| الترتيب | المستند | الغرض |
|---:|---|---|
| 1 | [README العربي](../../README.ar.md) | ملخص المشروع والحدود والمعمارية |
| 2 | [دليل المراجع](./REVIEWER_GUIDE.md) | ما ينبغي أن يتحقق منه المراجع الخارجي |
| 3 | [البدء السريع](./QUICKSTART.md) | التثبيت والاختبارات وCLI وAPI الاختياري |
| 4 | [الحالة الحالية](./STATUS.md) | حدود التنفيذ والclaims العامة |
| 5 | [نظرة عامة على المنحة](./GRANT_OVERVIEW.md) | ملخص عربي grant-safe |
| 6 | [المسرد](./GLOSSARY.md) | مصطلحات تقنية متسقة |

---

## 📚 المصادر الإنجليزية المعيارية

| المستند | المحتوى الحاكم |
|---|---|
| [README.md](../../README.md) | نقطة الدخول العامة والclaims الحالية |
| [TEST_REPORT.md](../../TEST_REPORT.md) | baseline قابلة للتكرار للاختبارات والتغطية |
| [docs/STATUS.md](../STATUS.md) | حالة التنفيذ الحالية |
| [docs/REVIEWER_GUIDE.md](../REVIEWER_GUIDE.md) | مسار المراجع الإنجليزي |
| [docs/ARCHITECTURE.md](../ARCHITECTURE.md) | حدود المعمارية والتخزين |
| [docs/EVAL.md](../EVAL.md) | منهجية التقييم |
| [docs/GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md) | نطاق المنحة المقدّم |
| [مصفوفة baseline/delta](../grants/baseline-funded-delta-matrix.md) | milestones وأدلة القبول |
| [Funding Use Plan](../grants/funding-use-plan.md) | الميزانية والأولويات |

---

## 🛠️ قاعدة الصيانة

```text
1. تحديث المصدر الإنجليزي ودمجه أولاً
2. التحقق من main الحالي
3. مزامنة الترجمات في PR منفصل خاص بالوثائق
4. عدم إدخال رقم أو claim جديد في ترجمة فقط
```

أُعدّت الحزمة العربية على أساس Crystal `main@9f90cb60`. ويظل آخر checkpoint غيّر
runtime هو PR #265 / `cd6fd44`.

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/README.md) · 🇫🇷 [Français](../fr/README.md) · 🇪🇸 [Español](../es/README.md) · 🇮🇹 [Italiano](../it/README.md) · 🇷🇺 [Русский](../ru/README.md) · 🇨🇳 [简体中文](../zh-CN/README.md) · 🇸🇦 **العربية**