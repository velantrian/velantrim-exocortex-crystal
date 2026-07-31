# 🔍 دليل المراجع — Velantrim Crystal

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](../ja/REVIEWER_GUIDE.md)
>
> توفر هذه الصفحة مسار تحقق بالعربية. لا تقدم claim جديداً حول runtime أو المنحة
> أو compliance أو security. عند الاختلاف تكون GitHub `main` و[docs/STATUS.md](../STATUS.md)
> و[TEST_REPORT.md](../../TEST_REPORT.md) هي المرجع.

## 1. ما هو Crystal؟

Crystal هو نواة الذاكرة العامة والمحدودة والقابلة للتحقق في Velantrim:

- local-first ومن دون cloud dependency إلزامية؛
- claims مرتبطة بالمصادر وحالة معرفية صريحة؛
- Guardian + TruthGate كحد admission تلقائي إلى L3؛
- CanonicalView لقراءة مبنية على أدلة معتمدة؛
- TRACE وReceipt كطبقة إثبات قابلة للفحص؛
- backends محلية SQLite/WAL ورسم بياني مضمّن؛
- آليات تقنية للمحو والتقييد وaudit وprovenance؛
- اختبارات قابلة للتكرار وبوابات تقييم حتمية.

## 2. ما الذي لا يدّعيه Crystal؟

لا يدّعي Crystal أنه:

- AGI أو وعياً أو شخصية أو مكافئاً بيولوجياً للدماغ؛
- ضماناً لـ «صفر hallucinations»؛
- stack Titan أو Personal ExoCortex الكامل؛
- نظام self-modification أو self-canonicalization؛
- منتجاً يعتمد إلزامياً على LLM أو graph أو cloud provider؛
- شهادة قانونية للامتثال لـ GDPR؛
- شهادة أمنية أو استضافة multi-tenant جاهزة للإنتاج؛
- تنفيذ runtime لكل فكرة بحث أو PR مفتوح.

## 3. المصادر الحاكمة

تحقق بالترتيب التالي:

1. GitHub `main` — الكود المدمج فعلياً؛
2. [TEST_REPORT.md](../../TEST_REPORT.md) — baseline الاختبارات والتغطية؛
3. [docs/STATUS.md](../STATUS.md) — حالة claims والمكونات؛
4. [docs/IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) — الخريطة التفصيلية؛
5. [docs/ARCHITECTURE.md](../ARCHITECTURE.md) — حدود المعمارية؛
6. وثائق المنحة الإنجليزية — scope ومعايير القبول.

لا تعد ملاحظة Notion أو roadmap أو RFC أو prototype أو PR مفتوح capability منفذة.

## 4. إعادة إنتاج نظيفة

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
git status --short
```

المتوقع:

- نجاح الاختبارات وcoverage gate؛
- عدم إبلاغ `eval_gate.py` عن regression؛
- عدم تلويث generated artifacts لشجرة Git؛
- مقارنة الأرقام الدقيقة مع [TEST_REPORT.md](../../TEST_REPORT.md).

## 5. التحقق من العقود الأساسية

### 🛡️ admission

```text
claim جديد
→ classification + evidence
→ Guardian
→ TruthGate
→ ذاكرة تشغيلية / Canon مقبول
```

سؤال التحقق: هل يستطيع claim ضعيف أو بلا دليل أو سيئ النوع تجاوز البوابات؟

### 🔎 استعلام HTTP

```text
POST /ask أو GET /receipt
→ core.query_pipeline.query()
→ Canon موجود مسبقاً
→ CanonicalView
→ إجابة أو رفض محدود
```

سؤال التحقق: هل تبقى L0/L1 وL3 وESM وoutbox والروابط الحلقية وembedding fingerprint
والتحقق التكيفي من دون تغيير أثناء استعلامات HTTP المنقولة؟

الضمان محدود عمداً:

- CLI `ask` و`receipt` لم تُنقلا بعد؛
- MCP قد يهيّئ embedding fingerprint مفقوداً.

### 🔗 TRACE وReceipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

سؤال التحقق: هل تظهر الحقائق ومراجع evidence التي دعمت الإجابة؟ وهل يُكتشف drift؟

### 🧾 audit وprovenance

```bash
velantrim audit
velantrim audit-verify
velantrim history <fact_id>
```

`history` و`ProvenanceChain` لكل fact عرضان مختلفان، ويجب ألا تخلطهما الوثائق أو الاختبارات.

## 6. تشغيل خدمة HTTP بحذر

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

تحقق من:

- عدم وجود fallback token؛
- loopback publish كإعداد آمن افتراضي؛
- container user غير privileged؛
- API dependencies اختيارية؛
- اختلاف عقدي `/ingest` و`/ask`.

## 7. التحقق من التقييم

يقيس Crystal، من بين أمور أخرى:

- retrieval `hit@k` وMRR؛
- اكتمال TRACE والبيانات الوصفية؛
- تغطية Evidence Span؛
- Receipt replay؛
- precision وrecall للتعارضات؛
- الرفض الصحيح عند حدود الثقة.

Replay في Titan prior art موثق، وليس capability حالية في Crystal أو runtime ذاتي التحسين.

## 8. التحقق من حدود المنحة

يجب فصل baseline الحالية عن delta المطلوبة بوضوح:

```text
baseline موجودة ومختبرة
+
عمل ممول محدد وقابل للقياس
=
deliverable قابلة للتحقق المستقل
```

لا يجوز احتساب الوظائف المدمجة سابقاً مرة أخرى كعمل مدفوع. الطلب قيد التقييم ولا
يدّعي منح التمويل.

الملخص العربي: [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)  
المصدر المعياري: [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

## 9. إشارات الخطر

🚩 مستند يدّعي أكثر من `main` أو `STATUS.md`.  
🚩 module بحثي يوصف بأنه runtime Crystal.  
🚩 ترجمة توسع scope أو الميزانية أو compliance claims.  
🚩 query تغير حالة الذاكرة بصورة غير متوقعة.  
🚩 metric متوسط يخفي safety regression أو فشلاً فردياً.  
🚩 provider خارجي يصبح إلزامياً ضمنياً.

## 10. الفحص النهائي

بعد review ينبغي أن تكون قادراً على الإجابة:

1. ما claims التي يمكن أن تدخل Canon تلقائياً؟
2. ما query paths التي هي read-only فعلاً؟
3. كيف ترتبط الإجابة بالحقائق وevidence؟
4. ما الحدود المنفذة وما الذي ما زال مخططاً؟
5. ما grant delta المتبقية بعد خصم baseline الحالية؟

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 **العربية** · 🇯🇵 [日本語](../ja/REVIEWER_GUIDE.md)