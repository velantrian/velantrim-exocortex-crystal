<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
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
# 🇷🇺 Обзор архитектуры Crystal

```text
exact source/version
→ RC-1 source/session artifacts
→ RC-2 structural map
→ RC-3 explicit passes
→ RC-4 EXTRACTED_PROPOSITION candidates
→ RC-5 relation candidates
→ normal admission path остаётся отдельным
→ Guardian → TruthGate
→ L1 + physical L3
→ TrustSnapshot / CanonicalView
```

RC-5 — same-session/same-version PRE-ADMISSION layer. Он не является новой веткой admission и не решает contradiction. `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` сохраняют exact linkage и rationale.

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
similarity != identity
```

Public `HTTP /ask`, `CLI ask`, `MCP search` идут через `core.query_pipeline.query()` и остаются read-only. Reader RC-1..RC-5 не пишет Canon/ESM/evidence.

Physical L3 — multi-status storage; strict Canon — deny-dominant trusted read projection. Их нельзя отождествлять.

SQLite остаётся ordinary active local-first. PostgreSQL/pgvector — optional inactive migration/equivalence target с `active=false`; import is not activation. Automatic switching отсутствует.

Dedicated/full autonomous Reader, automatic parser/OCR/NLP/LLM extraction, embeddings/ANN, cross-document semantic identity и belief-update authority не реализованы. NLnet не awarded.
