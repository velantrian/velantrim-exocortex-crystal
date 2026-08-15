<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
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
# نظرة عامة على المشروع والمنحة والحوكمة

Crystal هو مشروع local-first للذاكرة والأدلة وحدود القرار في أنظمة AI القابلة للتدقيق. التمويل لا يغير حدود السلطة ولا يحول retrieval أو Reader candidates إلى evidence.

## 💶 Funding truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

الحالة المختصرة الدقيقة: **submitted / under review / not awarded**. مبلغ **€50,000** تقريباً هو planning/transparency context فقط؛ ليس approved budget أو award أو payment commitment.

أي عمل merged قبل اتفاق تمويل يبقى existing baseline ولا يجوز إعادة احتسابه funded delta لاحقاً.

## 📖 Reader baseline

RC-1 وRC-2 وRC-3 وRC-4 وRC-5 bounded implemented؛ RC-6/RC-7 مدمجان؛ RC-9 deterministic lexical PRE-ADMISSION candidate discovery implemented. هذا لا يعني dedicated/full Reader Core.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

Comparator v1 وNLI neutral-filter v1 frozen gate failures؛ RRTIC-v1 architecture contract only. لا runtime authorization لأي منها.

## 🛡️ Governance boundaries

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import success != activation
candidate discovery != candidate adjudication
```

SQLite ordinary local-first active. PostgreSQL/pgvector optional inactive target مع `active=false`.

Guardian وTruthGate وTrustSnapshot وCanonicalView تبقى authority boundaries. لا يملك Reader أو retrieval أو grant scope سلطة تجاوزها.

## 🚫 ما لا ندعيه

- `dedicated_reader_core=false`؛
- لا active PostgreSQL normal runtime؛
- لا automatic truth verification؛
- لا automatic contradiction adjudication؛
- لا security/legal/GDPR certification؛
- لا native-speaker editorial certification؛
- لا grant award.
