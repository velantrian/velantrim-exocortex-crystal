<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: ar -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# دليل المراجع — Velantrim Exo-Cortex Crystal

**نقطة المصدر الإنجليزية:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
هذا الدليل واجهة إرشادية تتم صيانتها. تبقى أدلة التنفيذ هي الكود في `main`، والاختبارات
القابلة للتنفيذ، وCI الدقيق، و[TEST_REPORT.md](../../TEST_REPORT.md)، و
[manifest](../status/implementation-manifest.json).

## 1. ما الذي تتم مراجعته

Crystal بنية ذاكرة عامة ومحلية ومرتبطة بالمصادر وقابلة للتدقيق لأنظمة الذكاء الاصطناعي.
تشمل القاعدة المتحقق منها claims مصنفة، وGuardian/TruthGate، وإسقاط strict Canon فوق L3
متعدد الحالات، واستعلامات عامة للقراءة فقط، ومسار ingest صريحاً منفصلاً، وReceipts،
وprovenance قابلة للتدقيق.

لا يدّعي Crystal وجود AGI أو وعي أو حقيقة شاملة أو انعدام الهلوسة أو runtime PostgreSQL
نشط أو switching تلقائي أو multi-tenancy إنتاجي أو اعتماد أمني/GDPR أو منحة NLnet ممنوحة.

## 2. إعادة إنتاج القاعدة

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

تُقرأ المقاييس المتغيرة فقط من تقرير الاختبارات الإنجليزي.

## 3. حد القراءة والكتابة

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → صريح ومنسوب وقابل للتدقيق
```

يستخدم `ask` العام `core.query_pipeline.query()` ولا يجوز أن يغيّر facts أو ESM أو L3 أو
outbox أو episode links أو embedding identity أو المرشحين المجهولين. الرفض المحدود عند
نقص grounding الصارم سلوك آمن متوقع.

`ingest` يكتب، لكن admission يعتمد على evidence ونوع claim وpolicy وTruthGate. لا يستطيع
خرج النموذج أن يمنح نفسه صفة fact عالمي متحقق.

## 4. التخزين والترحيل

SQLite هو الملف المحلي النشط العادي. يمكن لأول `auto` دائم اختيار LadybugDB الاختياري إذا
كان مثبتاً، وإلا SQLite؛ ويُقفل الاختيار وlocator غير السري. يُمنع fallback الصامت إلى Mock
المؤقت.

PostgreSQL/pgvector مسار مشغل منفصل: bundle متحقق → preflight للإصدار/TLS → schema جديد
غير نشط → import قابل للتسلسل → re-hash مستقل للقراءة فقط → equivalence دقيقة؛ وتظل الوجهة
`active=false`.

Import/equivalence ليس activation أو selection أو TruthGate admission أو strict Canon أو
cutover أو rollback أو dual-write أو production readiness.

## 5. الأمن والخصوصية

لا يتطلب الوضع الافتراضي cloud أو LLM أو telemetry أو analytics. توسّع Neo4j البعيد،
Anthropic، Wikidata، Redis، ترحيل PostgreSQL، API الواسع أو نسخ backup/export حدود الثقة
فقط بقرار مشغل صريح.

يحمي `VELANTRIM_ENCRYPTION_KEY` حقول L1 مختارة، وليس تلقائياً كل L3 أو backup أو bundle
أو Receipt أو log أو ملف مؤقت. لا يجوز إدخال credentials أو DSN سرية في profiles أو bundles
أو receipts أو logs أو issues أو Notion.

المسح من store المحلي النشط لا يمسح تلقائياً backups أو exports أو نسخ المشغل أو الأنظمة
البعيدة أو بيانات الأطراف الثالثة.

## 6. فشل fail-closed

- تُحجب claims غير المدعومة أو تُعلّم أو تُرفض بشكل محدود.
- يفشل تعارض profile/locator قبل cache للـ backend.
- يؤدي فشل import إلى rollback ويبقي `active=false`.
- يُكتشف evidence mismatch والعبث في Receipt/audit.
- تُرفض المدخلات الزائدة بالحدود.
- غياب dependency اختيارية لا يسبب switch دائم خفياً.
- الوصول الخارجي يحتاج TLS وauthentication وleast privilege وmonitoring.

## 7. قائمة المراجعة

- [ ] تحديد `main` وCI الدقيق.
- [ ] فصل query read-only عن ingest الصريح.
- [ ] فصل L3 الفيزيائي عن strict Canon.
- [ ] فصل import PostgreSQL غير النشط عن activation.
- [ ] مراجعة الشبكة وsecrets وencryption وerasure.
- [ ] عدم استنتاج certification أو production readiness أو grant award.

المصادر الإنجليزية: [Reviewer Guide](../REVIEWER_GUIDE.md)، [Security](../../SECURITY.md)،
[Privacy](../../PRIVACY.md)، [Failure Modes](../FAILURE_MODES.md)، و
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md).
