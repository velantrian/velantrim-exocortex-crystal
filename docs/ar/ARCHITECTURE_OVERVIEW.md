<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ar -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# نظرة عامة على بنية Crystal

هذه ترجمة عامة غير مُنشئة للسلطة. عند التعارض تُحسم الحقيقة بواسطة الكود المدمج والاختبارات وCI والعقود الإنجليزية.

## النموذج الأساسي

```text
مصادر + ingest صريح
→ توثيق المصدر والتطبيع
→ فحوص Guardian
→ قرار TruthGate
→ حالة L1 التشغيلية + physical L3 متعدد الحالات
→ إسقاط strict Canon الموثوق
→ استرجاع للقراءة فقط / إجابة / رفض محدود
```

وجود سجل في physical L3 لا يجعله تلقائياً جزءاً من strict Canon. نتيجة الاسترجاع أو تشابه المتجه أو نص النموذج ليست دليلاً مستقلاً.

## طبقات الذاكرة والمراجعة

- **L0:** حالة مؤقتة داخل العملية.
- **L1:** SQLite/WAL للحالة التشغيلية والأدلة والتدقيق والإيصالات وجلسات الاستيراد والمراجعة.
- **L2:** منطقة انتظار ومراجعة للادعاءات المرشحة أو المحجوزة؛ ليست طبقة حقيقة نهائية.
- **L3:** تخزين بياني متعدد الحالات؛ لا يساوي strict Canon.
- **TrustSnapshot / CanonicalView:** سطح قراءة موثوق يطبّق سياسة الرفض المهيمنة.

## فصل القراءة عن الكتابة

تعمل أسطح `HTTP /ask` و`CLI ask` وMCP عبر `core.query_pipeline.query()` للقراءة فقط. لا يجوز للاستعلام أن ينشئ حقيقة أو يقويها أو يغير ESM أو L3 أو outbox. الكتابة المقبولة تمر عبر `ingest` الصريح ثم Guardian وTruthGate.

## التخزين والترحيل

SQLite هو الملف التشغيلي المحلي النشط المعتاد. في أول تشغيل دائم قد يختار `auto` LadybugDB الاختياري أو SQLite، ثم يحفظ هوية الخلفية والموقع. لا يُسمح بالهبوط الصامت إلى Mock مؤقت.

المسار المتحقق للترحيل يصل إلى PostgreSQL/pgvector كهدف غير نشط فقط:

```text
حزمة SQLite متحققة
→ استيراد PostgreSQL معاملاتي
→ إعادة تجزئة مستقلة للقراءة فقط
→ تكافؤ دقيق
→ active=false
```

نجاح الاستيراد أو التكافؤ ليس activation ولا اختياراً للخلفية ولا قبولاً في TruthGate ولا cutover أو rollback أو dual-write. PostgreSQL غير موجود في تركيب runtime العادي.

## قراءة المستندات

source spans وسجلات المستندات وجلسات الاستيراد ومسارات dry-run/review هي baseline منفذة. أما Reader Core متعدد المرور مع خرائط التغطية وإعادة القراءة الواعية بالتناقضات والتوليف على مستوى المستند فغير منفذ.

## الحدود الحالية

لا يدّعي Crystal AGI أو الوعي أو انعدام الهلوسة، ولا runtime نشطاً لـPostgreSQL، ولا تبديلًا آلياً، ولا ANN مقبولاً للإنتاج، ولا cutover/rollback/dual-write، ولا اعتماداً أمنياً أو قانونياً أو GDPR، ولا حصولاً على منحة NLnet.

## المصادر الإنجليزية

- [البنية الكاملة](../ARCHITECTURE.md)
- [حدود التخزين والسلطة](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [حالة التنفيذ](../IMPLEMENTATION_STATUS.md)
- [عقد استيراد PostgreSQL غير النشط](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
