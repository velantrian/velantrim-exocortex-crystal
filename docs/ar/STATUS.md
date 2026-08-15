<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ar -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — الحالة الحالية

**حالة العرض:** Human-First / post-RC-9 / post-NLI / RRTIC-v1  
**دليل التشغيل التاريخي المحتفظ به:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**الحقيقة الآلية:** [implementation manifest](../status/implementation-manifest.json)  
**الدليل التاريخي:** [TEST_REPORT.md](../../TEST_REPORT.md)

## 📖 Reader الحالي

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
dedicated_reader_core = false
```

RC-1…RC-7 هي طبقات bounded implemented. RC-9 هو deterministic lexical PRE-ADMISSION candidate discovery. Comparator v1 وNLI neutral-filter v1 نتائج تقييم frozen وليستا runtime stages. RRTIC-v1 عقد architecture/inspection فقط، من دون runtime provider authorization.

## 🛡️ حد السلطة

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
coverage != comprehension proof
pass completion != comprehension proof
candidate discovery != candidate adjudication
```

لا يملك Reader أو retrieval أو similarity أو NLI أو RRTIC حق تجاوز Guardian أو TruthGate أو evidence admission أو Canon.

## 🔐 الاستعلام العام

```text
HTTP /ask
CLI ask
MCP search
    ↓
core.query_pipeline.query()
    ↓
strict read-only canonical projection
```

هذه الواجهات read-only ولا تكتب facts أو physical L3 أو Canon.

## 🗄️ التخزين

```text
SQLite ordinary local-first          ACTIVE
PostgreSQL/pgvector import target     INACTIVE
PostgreSQL Reader activation          NOT AUTHORIZED
active=false
```

نجاح import أو equivalence لا يعني activation أو cutover أو switching أو dual-write.

## 🧪 دليل runtime التاريخي

يبقى هذا الدليل مثبتاً عند checkpoint التاريخي ولا يُقدّم باعتباره عدد اختبارات آخر milestone:

```text
2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% line coverage
7/7 Ring Zero mutants killed
9/9 permanent CI jobs
```

## 💶 المنحة

NLnet NGI0 Commons Fund: **submitted / under review / not awarded**. نحو €50,000 planning context فقط، budget change: none. لا يوجد grant-award claim ولا legal/security/GDPR certification claim.

## 🚫 غير مصرح به حالياً

- dedicated/full Reader Core؛
- semantic/hybrid Reader runtime؛
- NLI runtime filter؛
- RRTIC runtime provider؛
- embeddings/ANN/vector Reader stack؛
- active PostgreSQL normal runtime؛
- automatic contradiction adjudication أو automatic winner selection.
