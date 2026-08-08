<!-- translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ar -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — الحالة الحالية

**التاريخ:** 2026-08-08  
**نقطة التشغيل المتحقق منها:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**الشجرة المتحقق منها:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**رأس التنفيذ المتحقق:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**PR / CI:** #337 / `31256316536`  
**CI لتكامل PostgreSQL:** `31256316532`

## التحقق

- Python 3.11: **2078 passed / 13 skipped / 0 failed**؛
- Python 3.12: **2078 passed / 13 skipped / 0 failed**؛
- **9756 statements / 100.00% line coverage**؛
- `core/postgresql_migration.py`: **44/44 statements**؛
- `core/postgresql_migration_impl.py`: **336/336 statements**؛
- إنهاء **7/7** من طفرات Ring Zero؛
- نجاح **9/9** من وظائف CI الدائمة؛
- نجاح **1/1** من تكامل PostgreSQL/pgvector الحقيقي.

الأدلة الدقيقة: [TEST_REPORT.md](../../TEST_REPORT.md) و
[البيان القابل للقراءة آلياً](../status/implementation-manifest.json).

## حد القدرات المتحقق منه

يحافظ Crystal على أساس SQLite المحلي وينفذ المرحلة الأولى من issue #332:

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

برنامج تشغيل PostgreSQL إضافة اختيارية تُحمّل كسولاً فقط عبر أوامر مشغل صريحة.
يبقى التثبيت الافتراضي معتمداً على المكتبة القياسية. لا تسجل الوجهة المستوردة في
التكوين التشغيلي العادي، وتبقى `active=false` ولا تخدم قراءات أو كتابات عادية.

## حد السلطة

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

لا تتغير Guardian وTruthGate وrestrictions وTrustSnapshot وCanonicalView.

## غير موجود بعد

- تشغيل PostgreSQL نشط للقراءة والكتابة؛
- تقييم exact-vs-ANN وحدود ANN المقبولة؛
- activation أو cutover أو fencing أو rollback أو dual-write؛
- دورة backup/restore/upgrade وpooling إنتاجي وfencing موزع؛
- IdP/multi-tenancy إنتاجي أو اعتماد قانوني أو أمني أو GDPR؛
- Reader Core متحقق ومخصص.

## حالة المنحة

المشروع مقدم وقيد المراجعة. **لا يُدّعى الحصول على المنحة أو تغيير الميزانية.**
أصبح PR #337 وissue #332 جزءاً من الأساس المدمج ولا يجوز احتسابهما مرة أخرى كعمل
مستقبلي ممول.
