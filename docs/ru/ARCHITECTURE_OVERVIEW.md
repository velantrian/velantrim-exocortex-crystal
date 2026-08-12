<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- rc6-translation-source: docs/ARCHITECTURE_OVERVIEW.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
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
# Обзор архитектуры Crystal — RC-6

RC-1 → RC-2 → RC-3 → RC-4 → RC-5 → RC-6 образуют bounded Reader foundation; `dedicated_reader_core=false`.

```text
SourceVersion / SourceLocator
→ RC-1 ReaderSession
→ RC-2 Structural Document Map
→ RC-3 MultiPassReader
→ RC-4 EXTRACTED_PROPOSITION
→ RC-5 relation candidates
→ RC-6 bounded working sets
→ caller-supplied SUMMARY with direct RC-4 leaf provenance
→ normal evidence/admission path
→ Guardian / TruthGate
→ physical L3 / strict Canon read projection
```

`core.query_pipeline.query()` остаётся read-only для public ask/search. Reader layers не делают admission.

RC-6 revalidates OPEN session, exact source, completed pass, recovered structure и substantive current coverage; сортирует по structural order + candidate ID; применяет `max_candidates_per_set <= 128` и `max_source_locators_per_set <= 512`. Candidate atomicity fail closed.

Matching RC-5 relation переносится только при двух in-set endpoints. `SUMMARY` caller-supplied only; current direct leaf provenance сравнивается с immutable working-set snapshot.

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

SQLite ordinary active local-first; PostgreSQL/pgvector target `active=false`. Successful import is not activation. RC-6 не добавляет Reader DB, parser/OCR, LLM/provider, embeddings/ANN, RC-7 cross-document reading, contradiction resolution, evidence admission или Canon/ESM mutation.

NLnet `submitted / under review / not awarded`; ~€50,000 planning only; budget change none.
