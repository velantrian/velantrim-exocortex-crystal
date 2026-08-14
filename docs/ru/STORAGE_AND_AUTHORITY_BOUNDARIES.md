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

Crystal не делает storage presence эквивалентом доверия и не позволяет retrieval/inspection обходить admission.

## Surface identities

```text
storage profile        = deployment identity
physical L3            = multi-status graph state
strict Canon           = trusted read projection
migration bundle       = operation evidence
retrieval score        = ranking signal
Reader artifact        = source-linked candidate
RC-9 retrieval result  = PRE-ADMISSION inspection candidate
RRTIC diagnostic       = typed inspection metadata
```

`core.query_pipeline.query()` — read-only public query path. `HTTP /ask`, `CLI ask`, `MCP search` не выполняют Reader admission writes.

## Retained Reader compatibility

```text
RC-1 source/session
RC-2 structure
RC-3 pass ledger
RC-4 proposition
RC-5 relation candidate
RC-6 working set / SUMMARY
RC-7 cross-document candidate
RC-9 lexical candidate discovery
```

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
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

RC-9 returns deterministic lexical ranking/provenance metadata only. RRTIC-v1 adds architecture-level typed suspicion/qualifier vocabulary only.

```text
retrieval match != evidence
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC diagnostic != RC-5 registered relation
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
evaluation pass != runtime authorization
```

## Memory / authority

| Surface | Role | Boundary |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable operational memory |
| L2 | pending/review | candidate state |
| physical L3 | multi-status graph | not strict Canon |
| Guardian | structural/safety | admission boundary |
| TruthGate | admission policy | not objective oracle |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | read projection | trusted grounding surface |

## SQLite / PostgreSQL

```text
SQLite active local-first
→ backup / independent verification / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import
→ independent exact equivalence
→ active=false
```

Import/equivalence is operation evidence, **not activation**, automatic switching, cutover, rollback, dual-write, Reader vector runtime or admission authority.

## Isolation rules

Reader/retrieval/evaluation layers may not mutate truth status merely because a candidate ranked highly, turn an NLI label into proposition identity, choose a contradiction winner, admit evidence, bypass Guardian/TruthGate or write strict Canon.

Comparator v1 and NLI neutral-filter v1 remain frozen failed evaluation evidence. `dedicated_reader_core=false`; `semantic_hybrid_reader_runtime=false`; `rrtic_runtime_authorization=false`.

## Privacy / non-claims

Source restriction/sensitivity context remains policy metadata; rank, working-set fill or RRTIC qualifier does not weaken privacy. No active PostgreSQL Reader runtime, automatic switching, semantic/hybrid Reader runtime, FTS/ANN/vector DB, RRTIC runtime provider, automatic evidence/identity/Canon authority, security/legal/GDPR certification or awarded funding is claimed.

NLnet **submitted / under review / not awarded**; ~€50,000 planning only.

Historical RC-7 source: `main@ab3ad31c437647535030e371d58f456faf14017b`. Current Russian refresh source: `main@9666781d390e3276a111cb5ee1735f6606a76283`.
