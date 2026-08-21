<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- truthgate-v1-source: docs/IMPLEMENTATION_STATUS.md@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a -->
<!-- truthgate-v1-status: CURRENT -->
<!-- d1-locale: ar -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# حالة التنفيذ — Crystal

هذه الصفحة تميّز بين ما هو **bounded implemented** وما هو evaluation/architecture only وما هو غير مصرح به في runtime.

## TruthGate v1 — مطابقة التنفيذ بعد PR #440

أُعيدت مراجعة صفحة D1 هذه مقابل التغيير الجوهري في السياسة الإنجليزية عند `main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a`. تستخدم admission الافتراضية لـ `WORLD_FACT` سياسة ثابتة ومحددة الإصدار: `DEFAULT_MIN_CONFIDENCE = 0.05` و`TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"`. يبقى التكيّف المحلي داخل العملية telemetry/research ولا يغيّر default admission threshold. يظل `min_confidence` الصريح caller parameter محدوداً للتدفقات الداخلية/tests الحالية. لا يضيف هذا Reader/RAG/retrieval runtime، ولا يفعّل PostgreSQL/pgvector، ولا يوسّع Canon، ولا ينقل authority إلى Titan. تبقى markers المصدر السابقة provenance تاريخية.

## 📊 مصفوفة التنفيذ

| المكوّن | الحالة | الحد الحالي |
|---|---|---|
| Reader RC-1 | ✅ implemented bounded | evidence-linked domain skeleton |
| Reader RC-2 | ✅ implemented bounded | caller-supplied structural map |
| Reader RC-3 | ✅ implemented bounded | explicit deterministic multi-pass mechanics |
| Reader RC-4 | ✅ implemented bounded | source-linked proposition extraction |
| Reader RC-5 | ✅ implemented bounded | pre-admission relation candidates |
| Reader RC-6 | ✅ implemented bounded | bounded long-context strategy |
| Reader RC-7 | ✅ implemented bounded | cross-document candidate links |
| Reader RC-9 lexical candidate discovery | ✅ implemented | deterministic PRE-ADMISSION retrieval baseline |
| Comparator v1 | 🧊 frozen gate fail | evaluation only |
| NLI neutral-filter v1 | 🧊 frozen gate fail | evaluation only |
| RRTIC-v1 | 🧩 frozen architecture contract | no runtime provider |
| dedicated/full Reader Core | ❌ not implemented | `dedicated_reader_core=false` |
| SQLite | ✅ ordinary active local-first | operational profile |
| PostgreSQL/pgvector import | ✅ bounded inactive import/equivalence | `active=false` |
| PostgreSQL normal runtime adapter | ❌ not implemented | no normal reads/writes |

## 🧬 Machine boundary names

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

RC-5 implementation lives in `core/reader_relations.py`. Its relation candidates remain same-session/same-source-version inspection artifacts, not truth decisions.

## 🛡️ Epistemic boundary

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
candidate discovery != candidate adjudication
```

No Reader layer writes admitted evidence merely because a candidate was extracted, linked, ranked or classified.

## 🔐 Public query

`HTTP /ask`, `CLI ask` و`MCP search` route through `core.query_pipeline.query()` as read-only canonical projection. They do not create facts or mutate Canon.

## 🗄️ Storage implementation

SQLite remains the normal local-first runtime. PostgreSQL/pgvector remains an optional inactive import/equivalence target with `active=false`; import success is not activation and does not authorize automatic backend switching.

## 🔬 Research/runtime distinction

Comparator v1 classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.  
NLI v1 classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.  
RRTIC-v1: architecture contract only; `runtime_authorization=false`.

Therefore semantic/hybrid retrieval, NLI filtering and RRTIC runtime provider are not production capabilities.

## 💶 Grant truth

NLnet remains **submitted / under review / not awarded**. Approximately €50,000 is planning context only; budget change: none. Work merged before any funding agreement remains existing baseline.