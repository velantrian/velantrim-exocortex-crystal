<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Crystal Architecture Overview

**Status date:** 2026-08-14  
**Purpose:** current English architecture entry point.  
**Authority:** merged code, exact CI, `docs/ai/CURRENT_STATE.md` and the implementation manifest remain technical truth.

## Architecture in one view

```text
exact source/document identity
        ↓
Reader RC-1…RC-4
source/session/structure/pass/proposition artifacts
        ↓
RC-5 same-document relation candidates
        ↓
RC-6 bounded long-context working sets
        ↓
RC-7 explicit cross-document candidate links
        ↓
RC-9 deterministic lexical PRE-ADMISSION discovery
        ↓
RRTIC-v1 typed inspection contract
(architecture only; not a runtime stage)
        ↓
explicit evidence / admission boundary
        ↓
Guardian → TruthGate
        ↓
physical L3 multi-status storage
        ↓
strict Canon read projection
        ↓
read-only retrieval / answer / bounded refusal
```

The dominant invariant is:

```text
discovery != evidence
inspection != adjudication
similarity != identity
runtime capability != architecture research
```

## Reader capability map

| Layer | Current state | Boundary |
|---|---|---|
| RC-1 | implemented | exact SourceVersion / SourceLocator / ReaderSession foundation |
| RC-2 | implemented | caller-supplied structural map; structure is metadata, not truth |
| RC-3 | implemented | deterministic explicit multi-pass mechanics; pass completion != comprehension proof |
| RC-4 | implemented | source-linked `EXTRACTED_PROPOSITION` candidates; `Reader candidate != admitted evidence` |
| RC-5 | implemented | same-session/same-version relation candidates in `core/reader_relations.py`; `relation candidate != admitted evidence` |
| RC-6 | implemented | bounded working sets + caller-supplied SUMMARY; summary != evidence |
| RC-7 | implemented | explicit cross-document candidate links with exact two-sided provenance |
| RC-8 | architecture/research | retrieval decision and adversarial evaluation contract |
| RC-9 | implemented | deterministic offline BM25 PRE-ADMISSION candidate discovery |
| Comparator v1 | frozen evaluation | semantic recall recovered; proposition-discrimination gate failed |
| NLI neutral-filter v1 | frozen evaluation | discrimination improved; useful-recall safety gate failed |
| RRTIC-v1 | frozen architecture contract | typed suspicion + qualifier diagnostics; no runtime authorization |

`dedicated_reader_core=false` remains the larger capability truth.

## RC-5 relation semantics remain authoritative

RC-5 registers only explicit pre-admission relations between valid RC-4 candidates from one open
ReaderSession and exact SourceVersion. Its relation kinds remain:

- `POSSIBLE_CONTRADICTION`
- `EXCEPTION`
- `QUALIFICATION`
- `TENSION`

`POSSIBLE_CONTRADICTION` and `TENSION` are symmetric candidate relations; `EXCEPTION` and
`QUALIFICATION` are directional. RC-5 preserves exact candidate/pass/node IDs, primary/supporting
provenance and explicit rationale.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

RRTIC-v1 does **not** replace, mutate or auto-register RC-5 relations.

## Post-RC-9 evaluation and RRTIC-v1

RC-9 demonstrated a useful lexical baseline but a measured cross-lingual/hard-negative gap.
Comparator v1 then recovered recall on the frozen Evaluation Surface v2, but hard-negative
discrimination failed. A preregistered bidirectional NLI neutral filter reduced hard-negative
leakage but lost useful recall and therefore failed its frozen admissibility gates.

The post-NLI reassessment classified the missing capability as a **relation-contract mismatch**:
a candidate pair needs typed relation suspicion plus explicit structural qualifier differences
before any future discriminator can be evaluated safely.

RRTIC-v1 freezes six suspicion-only relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

and ten qualifier dimensions:

```text
entity_binding
predicate_binding
argument_roles
polarity
modality_quantifier
temporal_version
jurisdiction
condition_direction
units_thresholds
attribution_causality
```

Each qualifier is limited to `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 has no scalar truth/confidence score, accept/reject rule, reranking, model execution,
evidence admission, contradiction adjudication, Canon mutation or runtime provider.

```text
RRTIC suspicion    != adjudicated relation
qualifier mismatch != truth decision
NLI label          != proposition identity
NLI contradiction  != contradiction adjudication
comparison pass    != runtime authorization
```

## Memory and authority layers

| Layer | Role | Authority boundary |
|---|---|---|
| Reader PRE-ADMISSION | source-linked process, proposition, relation, discovery and inspection candidates | no truth/evidence/Canon authority |
| L0 | process-local working state | ephemeral, not durable truth |
| L1 | SQLite operational memory | durable facts, ESM, evidence, audit, receipts and review state |
| L2 | pending/review staging | candidate or quarantined claims before final admission |
| physical L3 | graph-oriented multi-status storage | physical storage, not identical to strict Canon |
| strict Canon | `TrustSnapshot` / `CanonicalView` | deny-dominant trusted read projection |

Public query paths through `core.query_pipeline.query()` are read-only. A query must not mutate facts,
ESM, L3, outbox, episode links, embedding identity or unknown candidates. When strict grounding is
insufficient, bounded refusal is expected.

## Storage profiles

SQLite is the ordinary active local-first profile. A first durable `auto` selection may use optional
LadybugDB when installed, otherwise SQLite, and then persists the selected backend and non-secret
locator identity. Later backend/locator conflicts fail closed. Silent fallback to ephemeral Mock is
forbidden; explicit Mock remains development/test state.

Remote Neo4j is an explicit operator choice and expands the trust boundary.

## Portability and PostgreSQL

The verified portability chain remains:

```text
SQLite backup / verify / inactive restore
→ bounded deterministic logical export
→ PostgreSQL 16 + pgvector preflight
→ new inactive target schema
→ serializable import
→ independent read-only target re-hash
→ exact equivalence receipt
→ target remains active=false
```

The PostgreSQL target is absent from ordinary runtime composition. Successful import/equivalence is
operation evidence, **not activation**, backend selection, TruthGate admission, strict Canon membership,
cutover, rollback, dual-write or production readiness. Reader RC-1…RC-9 and RRTIC-v1 add no
PostgreSQL Reader activation.

## Safety and privacy

The default installation has no mandatory cloud, LLM, telemetry or analytics dependency. Optional
remote adapters, wider API exposure and migration targets require explicit operator configuration.
Selected L1 field encryption is not universal encryption. Active-store erasure is not global erasure
of backups, exports, remote systems or provider copies.

Reader artifacts inherit source restriction/sensitivity metadata. Structure, pass completion,
proposition extraction, relation registration, working-set fill, lexical ranking or typed inspection
cannot weaken privacy or epistemic policy.

## Current non-claims

Crystal does not claim:

- AGI, consciousness, universal truth or zero hallucinations;
- active PostgreSQL runtime or automatic backend switching;
- cutover, rollback, dual-write or accepted ANN production profile;
- production multi-tenancy or distributed exactly-once coordination;
- a completed dedicated/full autonomous Reader;
- automatic parser/OCR/PDF-layout/multimodal understanding;
- semantic/hybrid Reader runtime, Reader FTS/ANN/vector DB, CrossEncoder/NLI runtime filter or RRTIC runtime provider;
- automatic semantic identity, contradiction resolution, evidence admission or Canon mutation from retrieval;
- security, legal or GDPR certification;
- awarded NLnet funding.

NLnet remains **submitted / under review / not awarded**; approximate €50,000 is planning context only.
RC-1…RC-9, Comparator v1, NLI v1 and RRTIC-v1 are existing pre-agreement history if completed before
any funding agreement and cannot later be relabeled as newly funded runtime delivery.

## Detailed English contracts

- [Full architecture](./ARCHITECTURE.md)
- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [RC-9 lexical baseline](./architecture/READER_RC9_LEXICAL_BASELINE.md)
- [RRTIC-v1 typed inspection contract](./architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Current status](./STATUS.md)
- [Security/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md)
