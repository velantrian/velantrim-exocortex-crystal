<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Crystal Architecture Overview

**Status date:** 2026-08-11  
**Purpose:** stable, translation-oriented architecture entry point.  
**Authority:** merged code, exact CI and the implementation manifest remain runtime truth.

## Core model

```text
source/document identity + exact version/hash
        ↓
RC-1 evidence-linked Reader artifacts
        ↓
RC-2 caller-supplied Structural Document Map
        ↓
RC-3 explicit multi-pass mechanics over declared targets
        ↓
RC-4 source-linked EXTRACTED_PROPOSITION candidates
        ↓
RC-5 explicit same-session/same-version relation candidates
        ↓
normal ingest/review/evidence path (separate authority)
        ↓
Guardian policy checks
        ↓
TruthGate admission decision
        ↓
L1 operational state + multi-status physical L3
        ↓
deny-dominant strict Canon read projection
```

RC-5 does not insert a new admission path. Reader relation artifacts remain upstream, pre-admission candidate state.

## Reader layers and authority

| Layer | Role | What it does not prove |
|---|---|---|
| RC-1 | source/version/session, fidelity, coverage | truth or comprehension |
| RC-2 | structural hierarchy/order/state | confidence, importance or truth |
| RC-3 | explicit pass attempts/targets/outcomes | comprehension, evidence sufficiency or admission |
| RC-4 | source-linked extracted proposition candidates | verified fact or admitted evidence |
| RC-5 | explicit relation candidates between valid RC-4 candidates | confirmed contradiction, winner, truth or admission |

RC-5 relation kinds are deliberately small: `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION`. Within RC-5, only one OPEN Reader session and exact source version are permitted. Cross-document reading remains a later separate stage.

`POSSIBLE_CONTRADICTION` and `TENSION` are symmetric candidate relations. `EXCEPTION` and `QUALIFICATION` preserve direction. The registry keeps exact proposition candidate IDs plus primary/supporting locator provenance on both sides and an explicit rationale.

## Read/write separation

```text
ask / receipt / MCP inspection       → core.query_pipeline.query() → read-only
explicit ingest                      → Guardian / TruthGate → admission-capable write
Reader RC-1 / RC-2 / RC-3 / RC-4 / RC-5
                                     → source/process/candidate artifacts only
                                     → no admission side effects
```

## Storage profiles

SQLite remains the ordinary active local-first profile. The verified PostgreSQL 16 / pgvector path is an explicit inactive migration/equivalence target and remains `active=false`. Successful import/equivalence does not establish backend activation, automatic switching, cutover, rollback, dual-write or production readiness.

## Source-grounded Reader foundation

RC-1 binds artifacts to `SourceVersion` and replayable locators without storing source body. RC-2 supplies caller-declared structure. RC-3 records explicit reading passes and legal coverage outcomes. RC-4 validates caller-supplied normalized propositions only from completed substantive RC-3 regions and stores them with `EXTRACTED_PROPOSITION` fidelity.

RC-5 then registers only explicit relations between already-registered RC-4 candidates. It fails closed when the Reader session is no longer OPEN, source versions differ, candidate/session identity is inconsistent, provenance support uses another version or a candidate card is no longer registered in the Reader session.

No semantic similarity score is treated as proof; RC-5 contains no automatic semantic equivalence engine. Duplicate registration of the same symmetric relation pair is rejected rather than interpreted as corroboration.

## Critical non-equivalences

```text
source statement        != verified fact
structure/order         != epistemic authority
coverage                != comprehension proof
pass completion         != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

RC-5 has no truth, confidence, evidence-sufficiency, resolved-contradiction or winner fields. It does not call `core.evidence.attach_evidence()`, write fact evidence, mutate Canon/ESM, bypass Guardian/TruthGate, or invoke contradiction resolution.

## Safety/privacy and non-features

Reader RC-1/RC-2/RC-3/RC-4/RC-5 retain no source body. Derived artifacts inherit exact source restriction/sensitivity context. The Reader line adds no durable Reader schema, public API/CLI/background worker, automatic parser/chunker/OCR/PDF-layout/multimodal processing, LLM/provider-driven extraction or routing, embeddings/ANN/vector DB, autonomous research planner, automatic cross-document proposition identity or belief update.

The dedicated/full autonomous Reader / Semantic Reading runtime remains **not implemented** and `dedicated_reader_core=false`.

Crystal also does not claim AGI/consciousness, universal truth, zero hallucinations, active PostgreSQL runtime, production multi-tenancy, legal/security/GDPR certification or awarded NLnet funding.

## Detailed English contracts

- [Full architecture](./ARCHITECTURE.md)
- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Security/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md)
