<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
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
# نظرة عامة على بنية Crystal

هذه ترجمة current لحدود البنية العامة؛ الحقيقة التنفيذية الحاكمة تبقى في الكود والاختبارات والـ CI والعقود الإنجليزية.

## 🧠 Reader bounded architecture

```text
RC-1 source/version/session skeleton
   ↓
RC-2 Structural Document Map
   ↓
RC-3 explicit multi-pass mechanics
   ↓
RC-4 EXTRACTED_PROPOSITION candidates
   ↓
RC-5 relation candidates
   ↓
RC-6 bounded long-context working sets
   ↓
RC-7 cross-document candidate links
   ↓
RC-9 lexical PRE-ADMISSION discovery
   ↓
RRTIC-v1 typed inspection contract
```

RC-1 وRC-2 وRC-3 وRC-4 وRC-5 طبقات implemented bounded، كما أن RC-6 وRC-7 مدمجان. وجودها لا يعني dedicated/full Reader Core.

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
```

## 🛡️ Authority firewall

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
coverage != comprehension proof
pass completion != comprehension proof
```

RC-5 relation candidate — بما في ذلك `POSSIBLE_CONTRADICTION` — لا يصبح admitted evidence أو confirmed contradiction تلقائياً.

## 🏛️ Memory / authority

```text
L0 working cache
L1 operational state
L2 pending/review
physical L3 multi-status graph
        ↓
Guardian → TruthGate
        ↓
TrustSnapshot → CanonicalView STRICT
```

**physical L3 != strict Canon**. التخزين الفيزيائي لا يحدد وحده ما يمكن عرضه كحقيقة موثوقة.

## 🔐 Public query boundary

```text
HTTP /ask | CLI ask | MCP search
              ↓
core.query_pipeline.query()
              ↓
strict read-only canonical projection
```

Public query surfaces read-only؛ لا facts writes ولا Canon mutation.

## 🗄️ Storage profiles

SQLite هو ordinary active local-first profile. PostgreSQL/pgvector هو optional inactive import/equivalence target مع `active=false`. نجاح import أو hash equivalence لا يعني activation أو backend switching.

## 🔬 Research layers

RC-9 يقدم deterministic lexical candidate discovery. Comparator v1 وNLI neutral-filter v1 frozen evaluation results؛ كلاهما لا يملك runtime authorization. RRTIC-v1 عقد typed inspection لا يفلتر أو يعيد الترتيب أو يحسم الهوية أو التناقض تلقائياً.

## 🚫 Non-claims

لا يوجد automatic semantic matching كسلطة، ولا evidence admission تلقائي، ولا contradiction adjudication تلقائي، ولا dedicated Reader Core، ولا active PostgreSQL Reader runtime. NLnet remains submitted / under review / not awarded.
