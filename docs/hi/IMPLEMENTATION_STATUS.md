<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: hi -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Implementation स्थिति — Crystal

यह page current implemented boundary और research-only surfaces को अलग रखती है।

| Component | स्थिति | सीमा |
|---|---|---|
| Guardian / TruthGate / CanonicalView | ✅ implemented | retrieval/Reader authority bypass नहीं करते |
| HTTP/CLI/MCP query | ✅ implemented | `core.query_pipeline.query()` read-only |
| Reader RC-1…RC-7 | ✅ bounded implemented | pre-admission artifacts/candidates |
| RC-9 lexical discovery | ✅ implemented | deterministic PRE-ADMISSION only |
| Semantic comparator v1 | 🧊 frozen evaluation | runtime नहीं |
| NLI neutral-filter v1 | 🧊 frozen gate fail | runtime नहीं |
| RRTIC-v1 | 🧩 architecture contract | runtime authorization नहीं |
| SQLite ordinary runtime | ✅ active | local-first |
| PostgreSQL/pgvector import/equivalence | ✅ bounded optional | target `active=false` |
| Active PostgreSQL runtime | ❌ false | normal composition में नहीं |
| Dedicated Reader Core | ❌ false | implemented claim नहीं |
| Semantic/vector Reader runtime | ❌ false | authorized नहीं |

Reader machine truth:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
dedicated_reader_core=false
semantic_hybrid_reader_runtime=false
rrtic_runtime_authorization=false
nli_reader_runtime_filter=false
```

Research classifications:

```text
SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED
NLI_NEUTRAL_FILTER_GATE_FAILED
```

इनका अर्थ measured evaluation evidence है, runtime admission नहीं।

Authority firewall:

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
physical L3 != strict Canon
```

SQLite active ordinary profile है। PostgreSQL/pgvector optional inactive target है; successful import/equivalence backend activation, automatic switching, cutover, rollback या dual-write नहीं है।

NLnet proposal submitted है, review में है और **not awarded** है। लगभग €50,000 planning context only है।

Historical runtime checkpoint `bbd816c09dd39a02e6de6c1014438490572f40f6` और `2078 passed / 13 skipped / 0 failed` केवल retained provenance हैं।
