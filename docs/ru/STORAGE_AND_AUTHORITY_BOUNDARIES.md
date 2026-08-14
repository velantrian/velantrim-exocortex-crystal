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
<!-- current-translation-source: main@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Storage и Authority Boundaries

Crystal намеренно не делает storage presence эквивалентом доверия и не даёт retrieval/inspection слоям право обходить admission.

## 1. Разные identities

```text
storage profile        = deployment identity
physical L3            = multi-status graph state
strict Canon           = trusted read projection
migration bundle       = operation evidence
retrieval score        = ranking signal
model output           = generated text
Reader artifact        = source-linked observation/candidate
RC-9 retrieval result  = PRE-ADMISSION inspection candidate
RRTIC diagnostic       = typed inspection metadata
```

Ни один объект автоматически не означает другой.

## 2. Physical L3 vs strict Canon

```text
stored in L3            != trusted answer material
retrieved               != admitted
high score              != evidence
frequent copy           != independent corroboration
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
summary                 != evidence
RRTIC suspicion         != adjudicated relation
qualifier mismatch      != truth decision
```

## 3. Read/write separation

Public `HTTP /ask`, `CLI ask` и `MCP search` используют read-only query pipeline. Explicit ingest остаётся admission-capable через Guardian/TruthGate. Reader RC-1…RC-7, RC-9 retrieval и RRTIC inspection находятся upstream и сами admission не выполняют.

## 4. SQLite lifecycle и PostgreSQL target

| Backend | Current role |
|---|---|
| SQLite | ordinary active local-first runtime |
| Mock | explicit ephemeral development/test state |
| PostgreSQL/pgvector | optional inactive migration/import/equivalence target, `active=false` |

```text
active SQLite store
→ backup / independent verification / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import
→ independent exact-state equivalence
→ active=false
```

Successful import/equivalence не создаёт active PostgreSQL runtime adapter, automatic switching, cutover, rollback, dual-write, Reader vector runtime или admission authority.

## 5. Reader source/version и retrieval boundary

RC-1 связывает Reader artifacts с exact `SourceVersion`. RC-2 structure, RC-3 passes, RC-4 propositions, RC-5 relations, RC-6 working sets/SUMMARY и RC-7 cross-document links остаются внутри explicit provenance boundaries.

RC-9 добавляет deterministic offline BM25 PRE-ADMISSION candidate discovery поверх frozen Reader proposition snapshot. Он возвращает ranking/provenance metadata и inspection candidates, но не evidence/identity/Canon verdict.

```text
retrieval match != evidence
ranking != epistemic authority
candidate discovery != candidate adjudication
```

RRTIC-v1 добавляет только architecture-level typed suspicion/qualifier vocabulary для future inspection. Runtime provider отсутствует.

```text
RRTIC diagnostic != RC-5 registered relation
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
```

## 6. Authority isolation

Reader/retrieval/evaluation layers не должны:

- вызывать evidence admission как следствие similarity/ranking;
- менять `truth_status` или ESM;
- записывать strict Canon;
- ослаблять Guardian/TruthGate;
- выбирать contradiction winner;
- превращать NLI/model label в proposition identity;
- превращать benchmark pass в runtime authorization.

Comparator v1 и NLI neutral-filter v1 — frozen failed evaluation evidence, а не runtime components.

```text
NLI label != proposition identity
NLI contradiction != contradiction adjudication
evaluation pass != runtime authorization
```

## 7. Privacy boundary

Credentials/credential-bearing DSNs не должны попадать в profiles, bundles, receipts, logs, issues или Notion. Reader artifacts наследуют source restriction/sensitivity context; ranking, working-set fill или typed inspection не могут ослабить privacy policy.

## 8. Authority table

| Event | Что доказывает | Чего не доказывает |
|---|---|---|
| Reader artifact exists | bounded source-linked observation | truth/admission/comprehension |
| RC-4 candidate exists | proposition anchored to eligible Reader context | verified fact/admitted evidence |
| RC-5 relation exists | explicit auditable relation suspicion | confirmed contradiction/winner/Canon |
| RC-6 working set exists | deterministic grouping under explicit budgets | comprehension/evidence/admission |
| RC-7 link exists | explicit two-sided cross-document comparison candidate | identity/corroboration/Canon relation |
| RC-9 retrieval result exists | deterministic lexical candidate ranking | evidence sufficiency/identity |
| RRTIC diagnostic exists | typed suspicion + qualifier inspection vocabulary | adjudicated relation/truth decision |
| record stored in L3 | physical persistence | strict Canon membership |
| PostgreSQL import succeeds | transactional import | runtime activation |
| exact equivalence receipt | approved dataset equality | production readiness/cutover |

## 9. Historical RC-7 compatibility literals

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## 10. Current non-claims

Crystal не заявляет active PostgreSQL runtime, automatic switching/cutover/rollback/dual-write, accepted ANN production profile, production multi-tenancy, distributed exactly-once coordination, dedicated/full autonomous Reader, semantic/hybrid Reader runtime, Reader FTS/ANN/vector DB, NLI/CrossEncoder runtime filter, RRTIC runtime provider, automatic semantic contradiction resolution, security/legal/GDPR certification или awarded NLnet funding.

`dedicated_reader_core=false`; `semantic_hybrid_reader_runtime=false`; PostgreSQL/pgvector `active=false`. NLnet — **submitted / under review / not awarded**; ~€50,000 planning only.

Historical RC-7 source: `main@ab3ad31c437647535030e371d58f456faf14017b`. Current Russian refresh source: `main@9666781d390e3276a111cb5ee1735f6606a76283`.
