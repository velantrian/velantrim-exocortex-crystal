# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 **العربية**  
> 📚 [التوثيق الألماني](./docs/de/README.md) · [الفرنسي](./docs/fr/README.md) · [الإسباني](./docs/es/README.md) · [الإيطالي](./docs/it/README.md) · [الروسي](./docs/ru/README.md) · [الصيني المبسّط](./docs/zh-CN/README.md) · [العربي](./docs/ar/README.md)

### *بنية ذاكرة قابلة للتحقق، محلية أولاً ومفتوحة المصدر لذكاء اصطناعي جدير بالثقة*

`v0.3.0` · 🧪 **1713 اختباراً ناجحاً / 12 متجاوزاً** · 🎯 **تغطية 100%** · 🐍 **مسار التشغيل الافتراضي يعتمد مكتبة Python القياسية** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal طبقة ذاكرة قابلة للتحقق، وليست روبوت محادثة آخر. يحتفظ كل `claim`
> بالمصدر والحالة المعرفية وبيانات `provenance`. ويظل الإدخال التلقائي إلى الرسم
> البياني القانوني محكوماً بواسطة **Guardian + TruthGate**.

> **المصدر المعياري:** الكود المدمج في GitHub `main` والوثائق الإنجليزية يحددان
> حقيقة التنفيذ وحدود المنحة. هذه النسخة العربية ترجمة مصانة للمراجعين والمؤسسات
> والمساهمين الناطقين بالعربية. عند الاختلاف يُرجع إلى [README.md](./README.md)،
> و[docs/STATUS.md](./docs/STATUS.md)، و[TEST_REPORT.md](./TEST_REPORT.md).

---

## 🧭 Crystal في دقيقة واحدة

Crystal هو النواة العامة الموجّهة للتحقق والمنح في Velantrim:

- ذاكرة تشغيلية محلية L0/L1؛
- خلفيات محلية للرسم البياني القانوني L3؛
- حدود إدخال عبر Guardian وTruthGate؛
- `CanonicalView` لإجابات قائمة على أدلة معتمدة؛
- TRACE و`Receipt` قابلة لإعادة التحقق؛
- `Evidence Span` وطوابير مراجعة وجلسات استيراد؛
- آليات تقنية للمحو وتقييد المعالجة ذات صلة بـ GDPR؛
- تقييم حتمي وبوابات جودة في CI؛
- واجهات FastAPI وMCP اختيارية.

Crystal **ليس** Titan أو Personal ExoCortex الكامل، ولا نظام تشغيل معرفياً
مستقلاً، ولا مشروع وعي، ولا وكيلاً ذاتي التعديل. قد تؤثر أفكار البحث في RFCs
مستقبلية، لكنها ليست قدرات runtime حالية.

```text
GitHub Crystal main = حقيقة التنفيذ العامة
Notion Crystal       = خريطة استراتيجية ومنحة متزامنة
Titan / Full         = مسار بحث منفصل
```

---

## 🛡️ حدود الثقة الحالية

### مسار الإدخال

```text
إدخال / مستند / حدث وكيل
→ تصنيف وأدلة
→ Guardian + TruthGate
→ ذاكرة تشغيلية L0/L1
→ رسم بياني قانوني L3 بعد القبول
```

### مسار استعلام HTTP

أدخل PR #265 عقد قراءة صارماً ومنفصلاً:

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ Canon موجود مسبقاً فقط
→ CanonicalView
→ إجابة أو رفض محدود
```

في هذه الأسطح، طرح السؤال لا يكتب في L0/L1 أو L3، ولا يغيّر ESM، ولا يشغّل
outbox، ولا يسجل روابط حلقية، ولا يهيّئ `embedding fingerprint` مفقوداً، ولا
يعدّل حالة التحقق التكيفية.

### الحدود المتبقية المعلنة

- أوامر CLI `ask` و`receipt` ما زالت تستخدم `core.pipeline.run()` القادر على الإدخال؛
- `core.pipeline.run()` ما زال متاحاً؛
- MCP لا يعرض أداة كتابة قانونية صريحة، لكن البحث قد يهيّئ `embedding fingerprint`
  غير مضبوط.

لذلك ضمان القراءة فقط دقيق ومحدود، وليس تعميماً على كل المسارات. راجع
[read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 نموذج الذاكرة

| الطبقة | الدور | الحد |
|---|---|---|
| **L0** | cache عمل داخل العملية | سريع وقابل لإعادة البناء |
| **L1** | ذاكرة تشغيلية SQLite/WAL | حالات وقيود وتحديثات |
| **L2** | claims معلقة ومراجعة قيّمة | ليست قانونية تلقائياً |
| **L3** | الرسم البياني القانوني | الإدخال التلقائي فقط عبر TruthGate |
| **TRACE / Receipt** | طبقة إثبات | تشرح grounding وتكشف الانحراف |

قد يحتوي الرسم البياني المادي حالات حقيقة مختلفة. وبالمعنى الصارم، يشير
**Canon** إلى الإسقاط المتحقق والصالح وفق TRACE والمسموح بالسياسة، لا إلى كل
عقدة في backend الرسم البياني.

---

## 🚀 البدء السريع

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

استخدام CLI الأساسي:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

backend محلي دائم لـ L3:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

الدليل التفصيلي: [docs/ar/QUICKSTART.md](./docs/ar/QUICKSTART.md).

---

## 🔌 الواجهات الاختيارية

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| الطريقة | المسار | العقد |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | إدخال عبر Guardian + TruthGate |
| `POST` | `/ask` | استعلام قانوني للقراءة فقط |
| `GET` | `/receipt?q=...` | قراءة مع Receipt |
| `POST` | `/verify-receipt` | إعادة تحقق Receipt مقابل الحالة الحالية |
| `GET` | `/evidence/{fact_id}` | عرض أدلة عام وفق السياسة |

FastAPI وUvicorn إضافات اختيارية. لا يتطلب runtime الافتراضي خدمة سحابية أو
مزود نموذج خارجي.

### MCP

```bash
python -m core.mcp_server
```

يوفر MCP أدوات فحص للبحث وتقارير الذاكرة وتاريخ الحقائق والتعارضات والتحقق من
Receipt. وتظل الحدود المتعلقة بـ `embedding fingerprint` قائمة.

---

## 🧪 التقييم

يتضمن Crystal baseline حتمية تقيس:

- retrieval `hit@k` وMRR؛
- اكتمال TRACE والبيانات الوصفية؛
- تغطية Evidence Span؛
- بقاء Receipt عند replay؛
- precision وrecall لاكتشاف التعارض؛
- الرفض الصحيح عند حدود الثقة؛
- حدود regression في CI.

تنفيذ replay الحتمي في Titan عمل سابق موثق، وليس runtime منسوخاً إلى Crystal.
أي تطبيق لاحق يجب أن يمدد stack التقييم الحالي، ويظل offline وغير سلطوي، ويحافظ
على TruthGate وحدود الاستعلام.

---

## 💶 حدود المنحة

قُدّم المشروع إلى **NLnet NGI0 Commons Fund** وهو قيد المراجعة. لا يدّعي المستودع
أن التمويل قد مُنح.

```text
BASELINE الحالية
    +
DELTA ممولة وقابلة للقياس
    =
DELIVERABLE قابلة للتحقق المستقل
```

يبقى العمل المدمج سابقاً ضمن baseline ولا يُحتسب مرة أخرى كعمل مدفوع. ولا تُضاف
آليات معرفية أو neuromorphic أو Titan سراً إلى نطاق Crystal.

ملخص عربي: [docs/ar/GRANT_OVERVIEW.md](./docs/ar/GRANT_OVERVIEW.md)  
المصادر المعيارية:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)
- [docs/grants/evaluation-replay-adoption.md](./docs/grants/evaluation-replay-adoption.md)

---

## ✅ بوابات التحقق

| البوابة | الغرض |
|---|---|
| pytest + coverage | المجموعة الكاملة مع شرط تغطية 100% |
| Ruff | lint للكود وأدوات المستودع |
| Gitleaks | اكتشاف الأسرار الملتزم بها |
| Bandit | تحليل أمني ثابت لـ Python |
| pip-audit | تدقيق ثغرات الاعتماديات |
| Docker build | بناء صورة hardened قابلة للتكرار |
| eval-gate | ضبط regression في retrieval وgrounding والتعارض |
| JSONL integrity | التحقق من بنية corpus وتكرار المعرفات |

تقلل هذه الفحوص المخاطر، لكنها لا تثبت غياب كل عيب ولا تمثل شهادة قانونية أو
أمنية.

---

## 📚 مسار المراجع العربي

1. [docs/ar/REVIEWER_GUIDE.md](./docs/ar/REVIEWER_GUIDE.md)
2. [docs/ar/QUICKSTART.md](./docs/ar/QUICKSTART.md)
3. [docs/ar/STATUS.md](./docs/ar/STATUS.md)
4. [docs/ar/GRANT_OVERVIEW.md](./docs/ar/GRANT_OVERVIEW.md)
5. [docs/ar/GLOSSARY.md](./docs/ar/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — النتائج المعيارية
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — المعمارية المعيارية

---

## ⚖️ الترخيص والمساهمة

Crystal مرخص بموجب **AGPL-3.0**. راجع [LICENSE](./LICENSE)،
و[CONTRIBUTING.md](./CONTRIBUTING.md)، و[GOVERNANCE.md](./GOVERNANCE.md)،
و[SECURITY.md](./SECURITY.md)، و[PRIVACY.md](./PRIVACY.md).

> **📊 Canon = حقيقة مقبولة** · **🔗 Provenance = ثقة** · **🏠 Local-first = تحكم**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 **العربية**