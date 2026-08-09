<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ar -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# حدود التخزين والسلطة

## هويات منفصلة

```text
storage profile = هوية النشر
physical L3 = حالة بيانية متعددة التصنيفات
strict Canon = إسقاط قراءة موثوق
migration bundle = دليل على سلامة العملية
retrieval score = إشارة ترتيب
model output = نص مولد
```

لا تمنح أي هوية من هذه الهويات سلطة الأخرى تلقائياً.

## الملف الدائم

SQLite هو الخيار النشط المحلي المعتاد. قد يختار أول `auto` دائم LadybugDB الاختياري أو SQLite ثم يقفل الخلفية والموقع. أي تعارض لاحق يفشل مغلقاً. Mock متاح فقط عند اختياره صراحة للتطوير أو CI.

## physical L3 مقابل strict Canon

يمكن لـphysical L3 الاحتفاظ بسجلات VERIFIED أو USER_CLAIMED أو UNVERIFIED أو HYPOTHESIS أو SUBJECTIVE أو contested أو superseded أو restricted. strict Canon هو إسقاط قراءة deny-dominant يعتمد على السياسة والدليل الحاليين. التخزين أو الاسترجاع أو الدرجة العالية لا تكفي للقبول.

## القراءة والكتابة

`core.query_pipeline.query()` هو مسار الاستعلام العام للقراءة فقط. `ingest` الصريح هو المسار القادر على الكتابة، ثم تطبق Guardian وTruthGate الحدود البنيوية والمعرفية.

## دورة SQLite والترحيل

المسار المنفذ يشمل backup وverification وinactive restore وlogical export محدوداً وحزمة حتمية متحققة. ويمكن استيراد مجموعات physical-L3 المعتمدة إلى مخطط PostgreSQL جديد غير نشط ثم إثبات التكافؤ الدقيق، مع بقاء `active=false`.

هذا لا يرحّل كل حالة L1 أو audit/outbox أو إعدادات التشفير أو النسخ المستقلة. كما لا يضيف runtime نشطاً لـPostgreSQL أو ANN مقبولاً أو switching أو cutover أو fencing أو rollback أو dual-write.

## الأسرار والنسخ

يجب ألا تدخل كلمات المرور أو الرموز أو DSN المحتوية على أسرار في profiles أو bundles أو receipts أو logs أو GitHub أو Notion. النسخ الاحتياطية والصادرات والترحيل تنشئ نسخاً إضافية؛ حذف السجل من المتجر النشط لا يحذفها تلقائياً. تشفير بعض حقول L1 ليس تشفيراً شاملاً.

## ما تثبته العمليات

| الحدث | ما يثبته | ما لا يثبته |
|---|---|---|
| سجل في L3 | استمرار مادي | عضوية strict Canon |
| نتيجة استرجاع | صلة مرشحة | كفاية الدليل |
| backup متحقق | سلامة النسخة | حقيقة الادعاء |
| import ناجح | سلامة الاستيراد | activation أو اختيار runtime |
| exact equivalence | تطابق مجموعات البيانات المعتمدة | الجاهزية الإنتاجية أو cutover |

Reader Core المتخصص غير منفذ، وNLnet ما زالت submitted / under review / not awarded.

## العقود الإنجليزية التفصيلية

- [البنية الكاملة](../ARCHITECTURE.md)
- [الملف الدائم](../architecture/DURABLE_STORAGE_PROFILE.md)
- [عقد الترحيل](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [استيراد PostgreSQL غير النشط](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
