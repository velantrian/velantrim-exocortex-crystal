<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ar -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: nlnet-not-awarded -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-reader: rc4-proposition-extraction-implemented -->
<!-- d3-reader: rc5-relation-candidates-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
# حدود التخزين والسلطة في Crystal

## 🧱 هويات منفصلة

```text
storage profile = deployment identity
physical L3     = multi-status graph storage
strict Canon    = trusted read projection
migration proof = operation evidence
Reader relation = inspection candidate
```

**physical L3 != strict Canon**. كما أن انتقال بيانات ناجح لا يصبح claim evidence ولا TruthGate admission.

## 📖 Reader لا يملك سلطة التخزين المعرفية

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
```

RC-1 وRC-2 وRC-3 وRC-4 وRC-5 bounded implemented؛ RC-6/RC-7 أيضاً مدمجان. لكن:

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
coverage != comprehension proof
pass completion != comprehension proof
```

RC-5 `POSSIBLE_CONTRADICTION` أو أي Reader relation يبقى candidate إلى أن يمر بمسار evidence/adjudication المصرح به.

## 🗄️ SQLite

SQLite هو ordinary active local-first runtime profile. L1 وphysical L3 يمكن أن يكونا durable، لكن durability لا تساوي epistemic authority.

## 🐘 PostgreSQL/pgvector

PostgreSQL/pgvector موجود كـ optional inactive import/equivalence target:

```text
optional driver
→ explicit preflight
→ inactive target schema
→ serializable import
→ independent exact-state re-hash
→ equivalence receipt
→ active=false
```

`active=false` حاسم. import success != activation. لا يوجد automatic cutover أو rollback أو dual-write أو backend switching.

## 🔐 Public query boundary

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
read-only CanonicalView projection
```

لا تقوم هذه الواجهات بكتابة L3 أو تغيير ESM أو إنشاء facts.

## 🛡️ Authority path

```text
candidate / evidence proposal
        ↓
explicit admission path
        ↓
Guardian → TruthGate
        ↓
physical L3 state
        ↓
TrustSnapshot
        ↓
CanonicalView STRICT
```

Retrieval score أو similarity أو Reader relation أو NLI label أو RRTIC suspicion لا يتجاوز هذا المسار.

## 🚫 Non-claims

- dedicated/full Reader Core غير منفذ؛
- semantic/hybrid Reader runtime غير مصرح؛
- PostgreSQL normal runtime غير نشط؛
- active Reader pgvector/ANN غير مصرح؛
- automatic contradiction adjudication غير موجود؛
- NLnet submitted / under review / not awarded.
