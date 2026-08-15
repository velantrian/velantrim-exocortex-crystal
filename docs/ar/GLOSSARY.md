<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d4-locale: ar -->
<!-- translation-status: CURRENT -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# مسرد Crystal وضوابط الادعاءات

- **physical L3**: تخزين بياني متعدد الحالات؛ لا يساوي **strict Canon** تلقائياً.
- **strict Canon**: trusted read projection بعد تطبيق policy/authority، وليس كل ما يوجد في L3.
- **retrieval score**: ranking signal؛ ليس evidence.
- **model output**: مادة مولدة؛ ليست source truth مستقلة.
- **migration proof**: دليل على سلامة النقل/التكافؤ؛ ليس claim proof.
- **active=false**: target موجود لكنه غير مفعل كـ normal runtime.
- **Reader Core RC-1**: evidence-linked source/version/session skeleton.
- **Reader Core RC-2**: caller-supplied Structural Document Map.
- **Reader Core RC-3**: deterministic explicit multi-pass mechanics.
- **Reader Core RC-4**: source-linked `EXTRACTED_PROPOSITION` candidates.
- **Reader Core RC-5**: pre-admission relation candidates؛ لا contradiction adjudication.
- **source owner**: attribution التي تحفظ من قال proposition داخل المصدر؛ لا يجوز تحويلها تلقائياً إلى system belief.
- **proposition presentation category**: توصيف لكيفية تقديم proposition في المصدر، مثل factual assertion أو hypothesis؛ ليس truth label.
- **POSSIBLE_CONTRADICTION**: RC-5 candidate؛ لا يعني confirmed contradiction.
- **EXCEPTION**: RC-5 directional candidate يصف استثناءً محتملاً.
- **QUALIFICATION**: RC-5 directional candidate يصف قيداً/تخصيصاً محتملاً.
- **TENSION**: RC-5 candidate يصف توتراً يستحق الفحص.
- **Reader candidate**: مادة pre-admission؛ `Reader candidate != admitted evidence`.
- **contradiction candidate**: `contradiction candidate != confirmed contradiction`.
- **dedicated/full Reader Core**: capability غير مدعاة؛ bounded RC layers لا تعني نظام Reader كامل مستقل.
- **candidate discovery**: العثور/الترتيب؛ منفصل عن candidate adjudication.
- **funded delta**: عمل مستقبلي مؤهل فقط إذا كان خارج existing pre-agreement baseline ومسموحاً باتفاق التمويل.

## 💶 Funding vocabulary

```text
submitted / under review / not awarded
budget change: none
€50,000 = planning context only
```

لا تعني `CURRENT` في localization وجود native-speaker editorial certification. ولا توجد security/legal/GDPR certification claim.
