# 🚀 البدء السريع — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 **العربية**
>
> **ملاحظة:** لا تُترجم الأوامر وأسماء الحزم ومتغيرات البيئة ومسارات API. عند
> الاختلاف تكون GitHub `main` والوثائق الإنجليزية هي المرجع.

## 1. استنساخ المستودع

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
```

## 2. إنشاء بيئة افتراضية

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. تثبيت بيئة التطوير

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

يعتمد runtime الافتراضي لـ Crystal على مكتبة Python القياسية. وتبقى اعتماديات
التطوير وAPI والمحولات extras اختيارية.

## 4. تشغيل التحقق الكامل

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

الـ baseline المعيارية موجودة في [TEST_REPORT.md](../../TEST_REPORT.md):

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

هذه الأرقام لا تستبدل تشغيلاً مستقلاً على clone نظيف.

## 5. استخدام CLI

### إدخال claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

الإدخال عملية admission. تمر claims الجديدة عبر classification وGuardian وTruthGate.

### طرح سؤال

```bash
velantrim ask "how does water behave"
```

⚠️ أوامر CLI `ask` و`receipt` ما زالت تستخدم `core.pipeline.run()` القادر على
admission. ضمان عدم الكتابة الصارم ينطبق على HTTP endpoints المنقولة `/ask`
و`/receipt`، لا على كل callers.

### إنشاء Receipt والتحقق منه

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Receipt دليل مختوم للحقائق ومراجع provenance المستخدمة. يقارن replay الدليل
بالحالة الحالية ويمكنه كشف drift أو العبث.

## 6. تفعيل تخزين L3 محلي دائم

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

يبقى مسار SQLite محلياً. لا يرسل Crystal البيانات تلقائياً إلى cloud أو model provider.

## 7. تشغيل FastAPI الاختياري

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
velantrim-api
```

العنوان الافتراضي:

```text
http://127.0.0.1:8000
```

مثال:

```bash
curl http://127.0.0.1:8000/health
```

| الطريقة | المسار | السلوك |
|---|---|---|
| `POST` | `/ingest` | admission عبر Guardian + TruthGate |
| `POST` | `/ask` | قراءة صارمة من Canon الموجود |
| `GET` | `/receipt?q=...` | قراءة مع Receipt |
| `POST` | `/verify-receipt` | replay لـ Receipt |

## 8. تشغيل خادم MCP الاختياري

```bash
python -m core.mcp_server
```

لا يقدم MCP أدوات كتابة قانونية صريحة. لكن البحث قد يهيّئ `embedding fingerprint`
مفقوداً؛ لذلك لا يوصف بأنه مسار خالٍ تماماً من mutation.

## 9. المستندات التالية

- [دليل المراجع](./REVIEWER_GUIDE.md)
- [الحالة الحالية](./STATUS.md)
- [نظرة عامة على المنحة](./GRANT_OVERVIEW.md)
- [المسرد](./GLOSSARY.md)
- [المعمارية المعيارية](../ARCHITECTURE.md)
- [التقييم المعياري](../EVAL.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 **العربية**