<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-reader: rc4-proposition-extraction-implemented -->
<!-- d3-reader: rc5-relation-candidates-implemented -->
<!-- d3-reader: rc6-long-context-strategy-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Storage и authority boundaries — RC-6

`physical L3 != strict Canon`; `core.query_pipeline.query()` остаётся read-only. SQLite ordinary active local-first; PostgreSQL/pgvector `active=false`; import is not activation.

RC-6 сохраняет exact SourceVersion и direct RC-4 provenance, использует bounded working sets и caller-supplied SUMMARY. Он не делает evidence admission, truth/ESM/Canon mutation, confidence promotion или contradiction resolution.

```text
RC-1 / RC-2 / RC-3 / RC-4 / RC-5 / RC-6
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
summary != verified fact
```

RC-6: `max_candidates_per_set <= 128`, `max_source_locators_per_set <= 512`; candidate atomicity; matching RC-5 relation carried only if both endpoints are in-set. No automatic summarization, LLM/provider/parser/OCR, embeddings/ANN, RC-7 cross-document identity, Reader DB/API/worker or PostgreSQL activation.

NLnet `submitted / under review / not awarded`; ~€50,000 planning only; budget change none.
