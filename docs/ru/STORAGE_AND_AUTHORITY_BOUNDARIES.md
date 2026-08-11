<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
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
# 🇷🇺 Storage и authority boundaries

```text
physical L3 != strict Canon
Reader artifact != admitted fact
Reader proposition != admitted evidence
Reader relation != confirmed contradiction
retrieval score != evidence
import success != activation
```

RC-1 связывает Reader с exact SourceVersion. RC-2/RC-3/RC-4/RC-5 наследуют эту границу. RC-5 принимает только valid registered RC-4 candidates одного session/source domain и сохраняет обе стороны relation.

`POSSIBLE_CONTRADICTION` и `TENSION` — symmetric suspicions; `EXCEPTION` и `QUALIFICATION` — directional. Relation candidate не создаёт contradiction disposition.

`coverage != comprehension proof`; `pass completion != comprehension proof`; `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`.

Public query surfaces используют `core.query_pipeline.query()` и read-only. RC-5 не вызывает `core.evidence.attach_evidence()`, не пишет strict Canon, не меняет `truth_status`/ESM и не обходит Guardian/TruthGate.

SQLite — ordinary active local-first. PostgreSQL/pgvector — inactive target `active=false`. RC-5 не меняет storage schema или runtime selection.

Dedicated/full autonomous Reader, automatic semantic equivalence, cross-document identity и awarded NLnet funding отсутствуют.
