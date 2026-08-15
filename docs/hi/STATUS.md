<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: hi -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — वर्तमान स्थिति

यह Hindi status page current **post-RC-9 / post-NLI / RRTIC-v1** public architecture truth को प्रस्तुत करता है। Exact current repository truth हमेशा merged code, executable tests, exact CI और machine-readable manifests से तय होती है।

## Reader स्थिति

```text
RC-1  bounded evidence-linked skeleton                  ✅
RC-2  caller-supplied structural map                    ✅
RC-3  deterministic bounded multi-pass mechanics        ✅
RC-4  source-linked proposition extraction              ✅
RC-5  same-session relation candidates                  ✅
RC-6  bounded long-context strategy                     ✅
RC-7  cross-document candidate links                    ✅
RC-9  lexical PRE-ADMISSION candidate discovery         ✅
semantic comparator runtime                             ❌
NLI neutral-filter runtime                              ❌
RRTIC runtime authorization                             ❌
dedicated Reader Core                                   ❌
```

Machine-bound compatibility names:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
dedicated_reader_core = false
```

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
```

### Frozen research evidence

Semantic comparator v1:

`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`

NLI neutral-filter v1:

`NLI_NEUTRAL_FILTER_GATE_FAILED`

दोनों evaluation-only evidence हैं। Comparator/NLI results runtime authorization नहीं देते।

RRTIC-v1 typed inspection/suspicion architecture contract है; यह provider, reranker, proposition-identity oracle, evidence-admission authority, adjudicator या Canon writer नहीं है।

```text
dedicated_reader_core=false
semantic_hybrid_reader_runtime=false
rrtic_runtime_authorization=false
nli_reader_runtime_filter=false
```

## Authority स्थिति

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
physical L3 != strict Canon
provenance != proof of truth
```

Guardian structural/policy boundary है, truth oracle नहीं। TruthGate L3 admission authority है। TrustSnapshot deny-dominant reconciliation और CanonicalView strict trusted read projection देते हैं।

Public query path read-only है:

```text
HTTP /ask / CLI ask / MCP search
→ core.query_pipeline.query()
→ strict read-only canonical projection
```

## Storage स्थिति

SQLite ordinary active local-first profile है। PostgreSQL/pgvector optional inactive path है और `active=false` रहता है। Successful import/equivalence activation, cutover, backend selection या TruthGate admission नहीं है।

## Grant स्थिति

NLnet NGI0 Commons Fund proposal **submitted / under review / not awarded** है। लगभग €50,000 planning/transparency context है; approved budget या payment commitment नहीं।

## Historical runtime evidence

Retained checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6`.

```text
2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% line coverage
```

ये historical provenance हैं, current test-count claim नहीं। Current acceptance exact CI से आती है।
