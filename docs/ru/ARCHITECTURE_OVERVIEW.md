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
<!-- rc6-translation-source: docs/ARCHITECTURE_OVERVIEW.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/ARCHITECTURE_OVERVIEW.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
# 🇷🇺 Architecture Overview — Reader RC-7

Crystal разделяет storage, Reader process artifacts, evidence admission и trusted read projection.

```text
source → RC-1 exact source/session → RC-2 structure → RC-3 passes → RC-4 EXTRACTED_PROPOSITION
├→ RC-5 within-source relation candidates
├→ RC-6 long-context working sets/SUMMARY
└→ RC-7 cross-document link candidates
→ normal evidence/review path → Guardian → TruthGate → physical L3 / TrustSnapshot / CanonicalView
```

`core.query_pipeline.query()` остаётся read path. Public query surfaces read-only. physical L3 не равен strict Canon.

RC-1 source/session, RC-2 caller-supplied structure, RC-3 explicit passes, RC-4 source-linked propositions, RC-5 relation candidates и RC-6 working sets уже bounded layers. RC-7 добавляет explicit caller-supplied links между current RC-4 candidates из разных document identities.

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 revalidates OPEN Reader sessions, exact SourceVersion/privacy, SegmentCard membership, completed RC-3 pass, substantive targets/outcomes, recovered RC-2 structure и current coverage. Supported kinds: `SUPPORTS`, `CONTRADICTS`, `ELABORATES`, `REFERENCES`, `DEFINES`, `EXAMPLE_OF`, `PREREQUISITE_FOR`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`.

`CONTRADICTS`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM` symmetric; другие kinds directional. Inspection basis descriptive only и не превращается в similarity/identity/confidence score.

Reader artifacts pre-admission: никакой RC-1..RC-7 module не пишет strict Canon и не обходит Guardian/TruthGate. `dedicated_reader_core=false`; dedicated/full autonomous Reader не implemented.

SQLite ordinary active local-first. PostgreSQL/pgvector `active=false`; import is not activation, automatic switching absent. NLnet submitted / under review / not awarded. Русская RC-7 parity = `main@ab3ad31c437647535030e371d58f456faf14017b`; остальные восемь Reader-dependent locale packs остаются `REFRESH_NEEDED`.
