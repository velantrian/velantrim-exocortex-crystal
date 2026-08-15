<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d5-locale: ar -->
<!-- translation-status: CURRENT -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
<!-- d5-reader: rc5-relation-candidates-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
# دليل المراجع الموسعة — Arabic CURRENT

هذا الدليل يربط القارئ العربي بالمراجع الإنجليزية التفصيلية من دون تحويل الترجمة إلى مصدر سلطة مستقل. حالات التوثيق هي `CURRENT` و`REFRESH_NEEDED` و`RETIRED` و`ENGLISH_ONLY_BY_DESIGN`.

## 🧠 Reader boundary

RC-1…RC-5 bounded implemented، كما أن RC-6/RC-7 مدمجان وRC-9 lexical PRE-ADMISSION discovery implemented. لكن dedicated/full Reader Core غير مدعى.

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

RC-5 vocabulary المحتفظ بها:

```text
POSSIBLE_CONTRADICTION
EXCEPTION
QUALIFICATION
TENSION
```

هذه relation candidates inspection artifacts؛ لا تمنح evidence admission أو truth authority.

## 🛡️ Authority / storage boundaries

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import success != activation
SQLite = ordinary active local-first
PostgreSQL/pgvector = inactive target
active=false
```

Public query يمر عبر `core.query_pipeline.query()` كـ read-only canonical projection.

## 🧪 Evaluation boundaries

Comparator v1: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.  
NLI neutral-filter v1: `NLI_NEUTRAL_FILTER_GATE_FAILED`.  
RRTIC-v1: typed inspection architecture contract؛ runtime authorization false.

لا يتحول similarity أو NLI أو RRTIC suspicion إلى proposition identity أو admitted evidence أو adjudication تلقائياً.

## 💶 Grant truth

```text
programme: NLnet NGI0 Commons Fund
submitted / under review / not awarded
€50,000 = planning context only
budget change: none
```

لا approved-budget claim ولا security/legal/GDPR certification ولا native-speaker editorial certification.

## 🌍 Localization state

Arabic D1/D3/D4/D5 surfaces هي `CURRENT` في هذا parity milestone. حالة `REFRESH_NEEDED` تظل جزءاً من localization-state vocabulary ومن historical compatibility records ولا يجوز حذفها من policy أو history لمجرد أن Arabic تقدم إلى current.

## 📚 المراجع الحاكمة

- [Extended Reference Policy](../EXTENDED_REFERENCE_POLICY.md)
- [Documentation Map](../DOCUMENTATION_MAP.md)
- [Current English Status](../STATUS.md)
- [Architecture Overview](../ARCHITECTURE_OVERVIEW.md)
- [Storage and Authority Boundaries](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Localization Policy](../LOCALIZATION_POLICY.md)
- [Translation Status](../TRANSLATION_STATUS.md)
- [Security](../../SECURITY.md)
- [Privacy](../../PRIVACY.md)
- [GDPR](../../GDPR.md)
- [Archive](../archive/README.md)
