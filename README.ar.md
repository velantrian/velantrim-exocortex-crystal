# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — المصدر المعياري](./README.md) · 🇸🇦 **ملخص عربي**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### بنية ذاكرة قابلة للتحقق ومحلية أولاً لأنظمة الذكاء الاصطناعي الموثوقة

هذا الملف **ملخص إرشادي موجز وغير معياري**، وليس ترجمة كاملة للوثائق. تُحفظ القرارات الهندسية
والبنية والحالة والأمان وادعاءات المنحة باللغة الإنجليزية. عند الاختلاف تكون
[README.md](./README.md) والأدلة الإنجليزية هي المرجع.

`v0.3.0` · 🧪 **2078 ناجح / 13 متجاوز** · 🎯 **100.00% تغطية** · ✅ **9 مهام CI**

**نقطة runtime المحققة:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.

يفصل Crystal بين التخزين المادي والأدلة والقبول المعرفي والقراءات الموثوقة. لا يمكن لوجود
البيانات أو ترتيب الاسترجاع أو نجاح الترحيل تجاوز Guardian أو TruthGate أو مصالحة Canon الصارمة.

## النطاق المحقق

- ادعاءات مهيكلة ومصدر ومواضع دقيقة في النص الأصلي؛
- حدود قبول Guardian وTruthGate؛
- قراءات غير قابلة للتغيير عبر `TrustSnapshot` و`CanonicalView`؛
- استعلامات HTTP وCLI وMCP عامة للقراءة فقط؛
- TRACE وإيصالات وقيود ومحو وقرارات صريحة للتناقضات؛
- SQLite كملف تخزين محلي اعتيادي؛
- نسخ احتياطي/استعادة محققة وتصدير منطقي محدود الموارد؛
- استيراد PostgreSQL/pgvector اختياري إلى schema هدف غير نشط مع تحقق مستقل للحالة الدقيقة.

## حدود التخزين

```text
SQLite = ملف local-first الاعتيادي الحالي
PostgreSQL + pgvector = هدف ترحيل اختياري
active=false
لا توجد runtime reads/writes اعتيادية
لا switching تلقائي ولا cutover ولا rollback ولا dual-write
```

يُثبت مشغل PostgreSQL فقط عبر `[postgresql]` ولا يُحمّل إلا بأمر صريح من المشغل. نجاح الاستيراد
دليل تشغيلي، وليس activation ولا قبولاً في Canon الصارمة.

## حدود المعنى الثابتة

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

لا يدّعي Crystal حقيقة مطلقة أو انعدام الهلوسة أو runtime PostgreSQL نشطاً أو تعدد مستأجرين
إنتاجياً أو distributed exactly-once أو اعتماداً قانونياً/GDPR/أمنياً أو تكامل Titan أو وعياً اصطناعياً.

## بدء سريع

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## الأدلة الإنجليزية الحالية

- [README المعياري](./README.md)
- [تقرير التحقق](./TEST_REPORT.md)
- [الحالة الحالية](./docs/STATUS.md)
- [مصفوفة التنفيذ](./docs/IMPLEMENTATION_STATUS.md)
- [سياسة الأمان](./SECURITY.md)
- [سياسة الترجمة](./docs/LOCALIZATION_POLICY.md)
- [مسار الوثائق العربية](./docs/ar/README.md)

تم تقديم طلب NLnet وهو قيد المراجعة؛ لا يُدّعى منح التمويل أو تغيير الميزانية.
