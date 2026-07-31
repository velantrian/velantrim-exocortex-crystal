# 📖 مسرد المصطلحات — Velantrim Crystal بالعربية

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 **العربية**
>
> يوحّد هذا المسرد المصطلحات العربية، لكنه لا يستبدل أسماء API أو schema أو
> code identifiers الإنجليزية. تبقى المعرفات داخل code blocks والواجهات من دون تغيير.

## القاعدة العامة

تبقى الأسماء التقنية `TruthGate` و`Guardian` و`CanonicalView` و`TRACE` و`Receipt`
ظاهرة كما هي. يمكن إضافة شرح عربي عند أول ظهور، لكن اسم العقد في الكود لا يُترجم.

| المصطلح الإنجليزي | الصيغة العربية المفضلة | المعنى / الحد |
|---|---|---|
| **admission** | قبول / قرار إدخال | قرار يسمح لـ claim بالوصول إلى حالة ذاكرة أكثر موثوقية |
| **claim** | claim / ادعاء مهيكل | عبارة typed وليست حقيقة متحققة تلقائياً |
| **Canon** | Canon / المعرفة القانونية | إسقاط مقبول بدقة وصالح وفق TRACE ومسموح بالسياسة |
| **canonical graph** | الرسم البياني القانوني | رسم L3 يحمل عناصر مقبولة وحالات صريحة |
| **Guardian** | Guardian / فحص بنيوي وأمني | فحص تمهيدي لا يستبدل TruthGate |
| **TruthGate** | TruthGate / حد القبول المعرفي | يتحكم في القبول التلقائي حسب النوع والمصدر والدليل والسياسة |
| **CanonicalView** | CanonicalView / عرض القراءة القانوني | إسقاط fail-closed للإجابات المبنية على أدلة |
| **TRACE** | TRACE / مسار التبرير | سلسلة قابلة للقراءة آلياً تشرح grounding الإجابة |
| **Receipt** | Receipt / دليل مختوم | دليل قابل لإعادة التحقق وحساس للعبث حول الحقائق وprovenance |
| **receipt replay** | إعادة تحقق Receipt | فحص Receipt مرة أخرى مقابل حالة الذاكرة الحالية |
| **trajectory replay** | replay لمسار التنفيذ | تكرار execution path للتقييم، وهو مختلف عن Receipt replay |
| **provenance** | provenance / الأصل والتتبع | المصدر وطريق الإنشاء ودورة حياة claim |
| **evidence span** | Evidence Span / مقطع دليل | جزء مرجعي من مصدر يدعم claim |
| **epistemic state** | الحالة المعرفية | حالة تصف كيفية تصنيف claim، وليست confidence score فقط |
| **source status** | حالة المصدر | فئة الأصل: خارجي أو مستخدم أو model output وغيرها |
| **grounding** | grounding / الارتباط بالدليل | ربط الإجابة بـ claims المقبولة ومصادرها |
| **FactsPack** | FactsPack / حزمة حقائق مضبوطة | سياق صغير وقابل للتتبع لإنتاج الإجابة |
| **read-only query** | استعلام للقراءة فقط | عقد يستبعد mutations المحددة للذاكرة والحالة |
| **fail-closed** | الرفض عند عدم اليقين | عدم القبول الصامت عندما تكون الثقة غامضة أو متعارضة |
| **baseline** | baseline / خط الأساس | عمل منفذ ومتحقق قبل delta الممولة |
| **funded delta** | delta ممولة | عمل إضافي قابل للقياس يجب تسليمه بالتمويل |
| **deliverable** | deliverable قابلة للتحقق | artifact عامة مع دليل قبول محدد |
| **local-first** | local-first / محلي افتراضياً | البيانات والتنفيذ محليان افتراضياً والخدمات الخارجية اختيارية |
| **stdlib-only runtime** | runtime بالمكتبة القياسية | المسار الافتراضي لا يحتاج runtime dependency خارجية إلزامية |
| **restriction** | تقييد المعالجة | حد تقني لاستخدام عنصر مخزن |
| **erasure** | محو | إزالة عبر الطبقات المحددة مع قواعد audit أو tombstone |
| **review queue** | طابور المراجعة | claims معلقة أو محجوبة قبل قرار curator |
| **curator override** | استثناء curator صريح | قرار بشري منسوب وقابل للتدقيق، وليس bypass صامتاً |
| **provider independence** | استقلالية المزود | النماذج الخارجية اختيارية وقابلة للاستبدال وليست سلطة حقيقة |

## ⚠️ كلمات تتطلب الحذر

### «متحقق»

ليست كل عقدة في الرسم البياني جزءاً من Canon متحقق. لا يستخدم المصطلح إلا عندما
تدعمه الحالة وevidence وTRACE والسياسة فعلاً.

### «متوافق مع GDPR»

الصياغات المفضلة:

```text
ضوابط تقنية ذات صلة بـ GDPR
معمارية موجهة نحو GDPR
```

تجنب من دون أساس قانوني:

```text
معتمد وفق GDPR
امتثال قانوني كامل مضمون
```

### «آمن» أو «hardened»

تصف `hardened` تدابير واختبارات تقنية موثقة. وهي ليست شهادة أمنية ولا دليلاً على
غياب الثغرات.

### «الحقيقة»

`TruthGate` ليس كاشف حقيقة عالمياً. إنه حد admission معرفي مضبوط داخل نموذج بيانات
وسياسة محددين.

### «Replay»

يجب التمييز دائماً:

```text
Receipt replay    = إعادة فحص دليل موجود
Trajectory replay = تكرار execution path لأغراض evaluation
```

### «معرفي» و«حي» و«وعي»

لا تصف هذه الكلمات قدرات runtime الحالية في Crystal. أسماء modules المستوحاة
بيولوجياً استعارات هندسية وليست claims بيولوجية أو claims شخصية.

## أسلوب الوثائق العربية

يفضل:

- جمل قصيرة وقابلة للتحقق؛
- إبقاء code identifiers في backticks ومن دون ترجمة؛
- الفصل الواضح بين «منفذ» و«اختياري» و«مخطط» و«بحث»؛
- عدم تقوية claim إنجليزي عبر الترجمة؛
- ربط الأرقام بالمصدر المعياري؛
- لغة موجهة للمراجعين بدلاً من marketing مبهم.

تجنب:

- وعود الموثوقية المطلقة؛
- marketing من دون test evidence؛
- الخلط بين Titan وCrystal؛
- مساواة محتوى الرسم البياني تلقائياً بالحقيقة المتحققة؛
- تقديم PR مفتوح أو RFC بوصفه runtime.

---

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 **العربية**