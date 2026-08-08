<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: ar -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# حدود الأمن والخصوصية والفشل

**المصدر:** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

لا يحل هذا الملخص محل الاختبارات أو المراجعة الأمنية أو الاستشارة القانونية.

## الأمن المعرفي

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

تبقى Guardian وTruthGate حدود القبول. الاستعلامات العامة read-only، وingest الصريح هو
مسار الكتابة المنفصل. لا يضمن Crystal الحقيقة أو انعدام الهلوسة؛ يجب حجب غير المدعوم أو
تعليمه أو رفضه أو جعله قابلاً للتدقيق.

## الحد المحلي

لا يحتاج التثبيت الافتراضي إلى cloud أو LLM أو telemetry أو analytics. SQLite هو الملف
النشط العادي. يمكن لـ `auto` الدائم اختيار LadybugDB الاختياري أو SQLite ويقفل الاختيار؛
Mock حالة dev/test صريحة. PostgreSQL/pgvector مجرد target غير نشط للمشغل مع `active=false`.

## البيانات والتوسع الاختياري

قد تُخزن claims وmetadata وprovenance والحالة المعرفية وgraph وrestrictions وسجلات
erasure/audit وReceipts وoutbox وbundles وbackups وexports. تخرج البيانات من الحد المحلي
فقط عند تفعيل Anthropic أو Neo4j البعيد أو Wikidata أو Redis أو ترحيل PostgreSQL أو API
أوسع أو نسخ خارجية بشكل صريح.

## التشفير والأسرار

يحمي `VELANTRIM_ENCRYPTION_KEY` حقول L1 مختارة، لا تلقائياً L3 وbackups وexports
وReceipts وlogs والملفات المؤقتة. يبقى تشفير المضيف وإدارة المفاتيح مطلوبين. لا يجوز أن
تدخل credentials في profiles أو bundles أو receipts أو logs أو issues أو Notion.

## API والخصوصية والمسح

يستخدم baseline الخاص بالـ API authentication وloopback. يحتاج العرض الخارجي إلى TLS
ومصادقة مراجعة وleast privilege وحدود وmonitoring وincident handling. Access وrectification
وrestriction وerasure وprocessing record ضوابط هندسية وليست اعتماد GDPR. مسح store النشط
لا يمسح النسخ المستقلة عالمياً.

## استجابات آمنة للفشل

| الفئة | السلوك المتوقع |
|---|---|
| Claim غير مدعوم | block أو label أو bounded refusal |
| تعديل read-only | reject / بلا تغيير حالة |
| تعارض profile | فشل قبل cache backend |
| غياب dependency | خطأ صريح بلا Mock خفي |
| فشل import | rollback، `active=false` |
| Evidence mismatch | verification failure |
| عبث Receipt/audit | فشل digest/hash |
| ترحيل كبير | fail closed عند الحدود |
| عرض شبكي | صريح ومصادق عليه فقط |
| بقاء نسخة بعد erasure | inventory ومسح منفصلان |

## عدم الادعاء

Crystal ليس اعتماداً أمنياً/قانونياً/GDPR، ولا دليلاً على scale غير محدود، ولا runtime
PostgreSQL نشطاً، ولا نظام ترحيل تلقائي، ولا ضمان حقيقة كاملة، ولا AGI/وعياً، ولا دليلاً
على منح NLnet.

التفاصيل: [Security](../../SECURITY.md)، [Privacy](../../PRIVACY.md)، [GDPR](../../GDPR.md)،
[Failure Modes](../FAILURE_MODES.md)، و[الملخص الإنجليزي](../SAFETY_PRIVACY_AND_FAILURES.md).
