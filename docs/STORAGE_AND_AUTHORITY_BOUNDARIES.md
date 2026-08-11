<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Storage and Authority Boundaries

**Status date:** 2026-08-11  
**Runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`.

## 1. Separate identities

```text
storage profile        = deployment identity
physical L3            = multi-status graph state
strict Canon           = trusted read projection
migration bundle       = operation evidence
retrieval score        = ranking signal
model output           = generated text
Reader artifact        = source-linked observation/candidate
Reader structure       = version-bound document metadata
Reader pass ledger     = reading-process audit state
Reader proposition     = pre-admission RC-4 candidate
Reader relation        = pre-admission RC-5 candidate relation
```

None automatically implies another. Reader state cannot bypass Guardian or TruthGate.

## 2. Physical L3 vs strict Canon

Physical L3 may contain multiple epistemic statuses. Strict Canon is a deny-dominant trusted read projection.

```text
stored in L3           != trusted answer material
retrieved              != admitted
high score             != evidence
frequent copy          != independent corroboration
Reader card            != admitted fact
Reader structure       != truth/confidence
Reader pass complete   != comprehension or truth
EXTRACTED_PROPOSITION  != verified fact
Reader candidate       != admitted evidence
relation candidate     != admitted evidence
contradiction candidate != confirmed contradiction
```

## 3. Read/write separation

Public `HTTP /ask`, `CLI ask` and `MCP search` use the read-only query pipeline. Explicit ingest is admission-capable through Guardian/TruthGate. Reader RC-1 through RC-5 are upstream domain layers and do not perform admission.

## 4. SQLite lifecycle and PostgreSQL target

```text
active SQLite store
→ backup / independent verification / inactive restore
→ bounded logical export
→ optional PostgreSQL 16 + pgvector inactive import
→ independent exact-state equivalence
→ active=false
```

PostgreSQL is absent from ordinary runtime composition. RC-5 introduces no schema migration and no backend selection/switching.

## 5. Reader source/version boundary

RC-1 binds every Reader artifact to an exact `SourceVersion`. RC-2 structure, RC-3 passes, RC-4 propositions and RC-5 relations remain inside that source/version authority boundary.

RC-4 candidate registration requires completed substantive RC-3 context. RC-5 accepts only candidates actually registered in one RC-4 extractor, requires the same session and exact source version, and preserves both sides' primary/supporting `SourceLocator` provenance plus candidate IDs.

`ReaderRelationRegistry` fails closed for stale/finished Reader sessions, unknown candidates, duplicate relation IDs, duplicate symmetric semantic pairs, mismatched source versions, inconsistent candidate session identity and detached candidate cards.

`POSSIBLE_CONTRADICTION` and `TENSION` are candidate suspicions, not contradiction dispositions. `EXCEPTION` and `QUALIFICATION` remain separate directional relations.

## 6. Authority isolation

RC-5 does not call `core.evidence.attach_evidence()`, create `evidence_spans`, write strict Canon, mutate `truth_status` or ESM, weaken Guardian/TruthGate, promote confidence, assert evidence sufficiency or choose a contradiction winner. It does not import the existing contradiction-resolution modules.

No raw-source semantic comparison, semantic similarity proof, automatic equivalence, cross-document identity, LLM/provider calls, parser/OCR/layout, embeddings/ANN/vector database or autonomous planner is introduced.

Telemetry is only count/state by relation kind. It is not truth probability or confidence.

## 7. Secret/privacy boundary

Credentials and credential-bearing DSNs must not enter profiles, bundles, receipts, logs, issues or Notion. Reader RC-1/RC-2/RC-3/RC-4/RC-5 retain no source body. Reader relation sides inherit the exact source restriction/sensitivity context.

## 8. Authority table

| Event | What it proves | What it does not prove |
|---|---|---|
| Reader artifact exists | bounded source-linked observation | truth/admission/comprehension |
| structural node exists | caller-supplied document metadata | confidence/truth/importance |
| Reader pass completes | targets received explicit legal outcomes | comprehension/truth/admission |
| RC-4 candidate exists | proposition is anchored to eligible Reader context | verified fact/admitted evidence |
| RC-5 relation exists | caller registered an auditable relation suspicion between valid RC-4 candidates | confirmed contradiction, winner, evidence sufficiency, truth or Canon membership |
| record stored in L3 | physical persistence | strict Canon membership |
| retrieval result | candidate relevance | evidence sufficiency |
| PostgreSQL import succeeds | transactional import | runtime activation |
| exact equivalence receipt | approved dataset equality | production readiness/cutover |

## 9. Current non-claims

Crystal does not claim active PostgreSQL runtime, automatic migration/switching, accepted ANN production quality, cutover/rollback/dual-write, production multi-tenancy, distributed exactly-once coordination, dedicated/full autonomous Reader runtime, automatic semantic contradiction resolution, security/legal/GDPR certification or awarded NLnet funding.

## 10. Detailed English sources

- [Full architecture](./ARCHITECTURE.md)
- [Architecture overview](./ARCHITECTURE_OVERVIEW.md)
- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
