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
<!-- rc6-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
# 🇷🇺 Storage и Authority Boundaries

Crystal не делает storage presence эквивалентом доверия.

```text
physical L3 != strict Canon
migration success != activation
retrieval score != evidence
Reader artifact != admitted evidence
cross-document link != Canon relation
```

| Backend | Current role |
|---|---|
| SQLite | ordinary active local-first runtime |
| Mock | explicit ephemeral dev/CI fallback |
| PostgreSQL/pgvector | optional inactive import/equivalence target, `active=false` |

```text
SQLite backup → independent verification → inactive restore → bounded logical export
→ PostgreSQL preflight → inactive transactional import → independent exact equivalence → active=false
```

Successful import/equivalence не создаёт active PostgreSQL runtime adapter, automatic backend switching, cutover или admission authority. Public query surfaces read-only.

RC-1 source/session, RC-2 structure, RC-3 pass ledger, RC-4 proposition, RC-5 relation, RC-6 working set/SUMMARY и RC-7 cross-document link — разные pre-admission artifacts.

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document support != admitted evidence
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 хранит exact source/session/candidate/pass/node/locator provenance обеих сторон и требует different document identities. Link conservatively restricted, если restricted хотя бы одна сторона; sensitivities остаются metadata, не score.

`dedicated_reader_core=false`; dedicated/full autonomous Reader не implemented. NLnet submitted / under review / not awarded. Русская RC-7 parity = `main@ab3ad31c437647535030e371d58f456faf14017b`.
