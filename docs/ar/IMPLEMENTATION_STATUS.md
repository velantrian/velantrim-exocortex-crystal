<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ar -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# حالة التنفيذ: Crystal والعمل المستقبلي

**التاريخ:** 2026-08-08  
**نقطة التشغيل:** `bbd816c` / PR #337  
**الأدلة:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**الحالة الآلية:** [manifest](../status/implementation-manifest.json)

| المكوّن | الحالة | الحد الحالي |
|---|---|---|
| Guardian / TruthGate / العرض الصارم | منفذ | التخزين والترحيل لا يتجاوزان السلطة |
| استعلامات HTTP/CLI/MCP | منفذة | الاستعلامات العادية لا تعدّل Canon |
| SQLite backup/verify/restore غير نشط | منفذ ومختبر | restore غير نشط وليس قبولاً |
| تصدير SQLite منطقي محدود | منفذ ومختبر | bundle قانوني محايد للـ backend |
| تبعية وpreflight لـ PostgreSQL | منفذ ومختبر | إضافة صريحة وتحميل كسول |
| استيراد PostgreSQL/pgvector غير نشط | منفذ ومختبر | schema جديد غير نشط، بلا I/O عادي |
| تكافؤ دقيق لحالة الوجهة | منفذ ومختبر | إعادة hash مستقلة للقراءة فقط |
| adapter تشغيل PostgreSQL نشط | غير منفذ | الوجهة خارج التكوين العادي |
| switching تلقائي SQLite/PostgreSQL | ممنوع | التوفر ونجاح الاستيراد ليسا اختياراً |
| تقييم exact-vs-ANN | غير منفذ | مرحلة لاحقة مستقلة |
| cutover / rollback / dual-write | غير منفذ | مراحل صريحة لاحقة |
| دورة خادم PostgreSQL | غير منفذة | backup/restore/upgrade/pooling مستقبلية |
| Reader Core / Semantic Reading Layer | غير منفذ | طبقة مرشحة قبل القبول |

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

نُفذت issue #331 و#332 عبر PR #335 و#337. يبقى PostgreSQL مسار مشغل اختياري
مع `active=false`. لا يمكن لنجاح التكافؤ تفعيل backend أو تغيير Guardian أو TruthGate
أو Canon الصارم.

العمل المستقبلي:

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

لا يدّعي Crystal وجود backend PostgreSQL نشط، أو ترحيل تلقائي، أو multi-tenancy
إنتاجي، أو حقيقة شاملة، أو انعدام الهلوسة، أو اعتماد قانوني/أمني، أو وعي.
