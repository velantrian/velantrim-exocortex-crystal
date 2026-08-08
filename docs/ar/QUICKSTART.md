<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ar -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 البدء السريع مع Crystal

يشغّل هذا الدليل الأساس المحلي بلا تبعيات إلزامية، ويُدخل ادعاءً صريحاً، ثم يستعلم
عنه عبر حد القراءة فقط ويتحقق من Receipt.

## المتطلبات

- Python 3.11 أو 3.12؛
- Git؛
- موقع محلي للمستودع وبيانات SQLite.

لا يحتاج التشغيل الافتراضي إلى LLM أو مزود embeddings أو خدمة سحابية. تثبّت إضافات
التطوير والاختبار الحزم الاختيارية اللازمة لمجموعة الاختبارات الكاملة.

## 1. التثبيت

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

في Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. التحقق من المستودع

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

توجد نقطة التحقق الدقيقة والمقاييس المتوقعة في
[TEST_REPORT.md](../../TEST_REPORT.md)، ولا تُكرر هنا كمتطلبات قابلة للتغير.

## 3. اختيار التخزين المحلي الدائم

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

يبقى SQLite ملف التشغيل المحلي العادي والنشط. أما PostgreSQL/pgvector فهو مسار
اختياري لاستيراد غير نشط والتحقق من التكافؤ، وتظل الوجهة `active=false`.

## 4. إدخال ادعاء صريح

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` عملية كتابة. يدخل الادعاء الحالة التشغيلية ويمر عبر مسار القبول
Guardian/TruthGate المهيأ. لا يعني ذلك أن Crystal يثبت الحقيقة الموضوعية بشكل مستقل؛
فالقبول يعتمد على الأدلة والسياسة.

## 5. الاستعلام عبر حد القراءة فقط

```bash
velantrim ask "how does water behave"
```

يستخدم `ask` العام الدالة `core.query_pipeline.query()` ولا يجوز أن ينشئ أو يعدّل
حقائق L0/L1، أو يغيّر ESM، أو يكتب إلى L3، أو يشغّل outbox، أو يحفظ روابط الحلقات،
أو يهيئ fingerprint للـ embeddings لم يكن مضبوطاً، أو يخزن مرشحين مجهولين.

عندما لا يتوفر grounding قانوني صارم، يُتوقع رفض محدود. الرفض نتيجة صحيحة لحد الثقة
وليس بالضرورة خطأ تشغيل.

## 6. إنشاء Receipt والتحقق منه

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

يختم Receipt الاستعلام والإجابة ومعرّفات الحقائق المستشهد بها داخل digest، ويمكنه
إعادة فحص الاستشهادات مقابل حالة الذاكرة الحالية. وهو يكشف العبث؛ أما توقيع HMAC
الاختياري فيحتاج مفتاح provenance محلياً.

## 7. تشغيل API الاختياري

```bash
pip install '.[api]'
velantrim-api
```

| الطريقة | المسار | الحد |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | مسار قبول/كتابة صريح |
| `POST` | `/ask` | استعلام صارم للقراءة فقط |
| `GET` | `/receipt?q=...` | استعلام مع Receipt |
| `POST` | `/verify-receipt` | إعادة تحقق Receipt |
| `GET` | `/evidence/{fact_id}` | عرض أدلة خاضع للسياسة |

يستخدم API أساس bearer-token، وليس نموذج تفويض multi-tenant إنتاجياً كاملاً.

## 8. تشغيل سطح فحص MCP

```bash
python -m core.mcp_server
```

يوفر MCP بحثاً للقراءة فقط، وتقارير ذاكرة، وتاريخ الحقائق، والبحث عن التعارضات،
والتحقق من Receipts. لا يوفّر أداة كتابة قانونية.

## أخطاء الحدود الشائعة

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- L3 الفيزيائي ليس Canon الصارم.
- confidence أو تكرار النسخ أو تشابه retrieval ليست أدلة مستقلة وحدها.
- نجاح الاستيراد أو التكافؤ ليس activation أو cutover أو اختيار backend.

## الوثائق التالية

- [README](../../README.md)
- [خريطة التوثيق](../DOCUMENTATION_MAP.md)
- [المعمارية](../ARCHITECTURE.md)
- [حالة التنفيذ](../IMPLEMENTATION_STATUS.md)
- [تقرير الاختبارات](../../TEST_REPORT.md)
- [سياسة الأمن](../../SECURITY.md)
