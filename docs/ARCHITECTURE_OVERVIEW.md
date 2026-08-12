<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Crystal Architecture Overview

**Status date:** 2026-08-12  
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
RC-3 explicit multi-pass mechanics over declared structural targets
        ↓
RC-4 source-linked EXTRACTED_PROPOSITION candidates
        ↓
RC-5 explicit same-session/same-version relation candidates
        ↓
RC-6 bounded same-session/same-version long-context working sets
        ↓
optional caller-supplied SUMMARY with direct RC-4 leaf provenance
        ↓
normal ingest/review/evidence path
        ↓
Guardian policy checks
        ↓
TruthGate admission decision
        ↓
L1 operational state + multi-status physical L3
        ↓
deny-dominant strict Canon read projection
        ↓
read-only retrieval / answer / bounded refusal
```

Reader artifacts, structural metadata, pass ledgers, extracted propositions, relation candidates,
working sets and summaries remain upstream observations/process/candidate state. They do not own truth,
evidence admission, contradiction resolution or planner authority.

Crystal does not treat every stored node, retrieved result or model output as truth. Physical L3
stores multiple statuses. Strict Canon is the trusted read projection produced by current policy and
evidence constraints.

## Memory and review layers

| Layer | Role | Authority boundary |
|---|---|---|
| Reader RC-1 | source/version/session artifacts, fidelity and coverage | source-linked observation/candidate, not truth |
| Reader RC-2 | version-bound structural hierarchy/order | structure and prominence are metadata, not confidence |
| Reader RC-3 | explicit pass attempts, declared targets and coverage outcomes | process audit, not comprehension or admission |
| Reader RC-4 | source-linked extracted proposition candidates from completed substantive pass regions | source presentation/candidate state, not verified fact or admitted evidence |
| Reader RC-5 | typed explicit relations between valid RC-4 candidates | candidate suspicion, not confirmed contradiction/winner/admission |
| Reader RC-6 | deterministic rolling working sets and caller-supplied summaries over direct RC-4 leaves | bounded context/synthesis candidate, not comprehension/evidence/truth/Canon admission |
| L0 | process-local working state | ephemeral, not durable truth |
| L1 | SQLite operational memory | durable facts, ESM, evidence, audit, receipts, import/review and outbox state |
| L2 | pending/review staging | candidate or quarantined claims before final admission |
| L3 | graph-oriented multi-status storage | physical storage, not identical to strict Canon |
| Strict read view | TrustSnapshot / CanonicalView | deny-dominant grounding surface |

## Read and write separation

```text
ask / receipt / MCP inspection                         → core.query_pipeline.query() → read-only
explicit ingest                                        → Guardian / TruthGate → admission-capable write
Reader RC-1 / RC-2 / RC-3 / RC-4 / RC-5 / RC-6      → source/process/candidate state only → no admission side effects
```

A public query must not mutate facts, ESM, L3, outbox, episode links, embedding identity or unknown
candidates. If strict grounding is insufficient, a bounded refusal is expected.

## Storage profiles

SQLite is the ordinary active local-first profile. A first durable `auto` selection may use optional
LadybugDB when installed, otherwise SQLite, and then persists the selected backend and non-secret
locator identity. Later backend or locator conflicts fail closed. Silent fallback to ephemeral Mock
is forbidden; explicit Mock remains development/test state.

Remote Neo4j is an explicit operator choice and expands the trust boundary.

## Portability and PostgreSQL

The verified portability chain is:

```text
SQLite backup / verify / inactive restore
→ bounded deterministic logical export
→ PostgreSQL 16 + pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only target re-hash
→ exact equivalence receipt
→ target remains active=false
```

The PostgreSQL target is absent from ordinary runtime composition. Successful import or exact
equivalence is operation evidence, not activation, backend selection, TruthGate admission, strict
Canon membership, cutover, rollback, dual-write or production readiness. RC-5 adds no Reader schema
migration and does not activate PostgreSQL. RC-6 also adds no Reader persistence/schema migration and
does not activate PostgreSQL.

## Source-grounded Reader foundation

Source spans and import-session evidence are implemented baseline. RC-1 provides the bounded
evidence-linked source/session skeleton: exact source-version identity, locators, SegmentCards,
source-fidelity classes, coverage states, bookmarks/open loops, stale handling and fail-visible
failure/privacy semantics.

RC-2 adds a caller-supplied Structural Document Map anchored to the same exact SourceVersion and
SourceLocator semantics. It models hierarchy/order and explicit `RECOVERED`, `AMBIGUOUS` and
`UNSUPPORTED` structure without claiming automatic parsing.

RC-3 adds deterministic explicit multi-pass mechanics compatible with the architecture contract:
`ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK` and `TARGETED_REREAD`. A pass declares its
structural targets, records `ATTEMPTED` / `COMPLETED` / `INTERRUPTED` / `DEGRADED` state, and applies
explicit legal RC-1 coverage outcomes. Partial progress remains visible. Cross-check and targeted
re-read require prior substantive processing. Pass counts are telemetry, not comprehension scores.

RC-4 adds deterministic pre-admission proposition extraction. It can register a candidate only from
a `COMPLETED` RC-3 pass target whose recorded outcome and current matching coverage are `PROCESSED`
or `REVISITED`. Every candidate remains a `SegmentCard` with `EXTRACTED_PROPOSITION` fidelity and
replayable primary/supporting source locators. Source owner, negation, qualifiers and source-presentation
category remain explicit so an opinion, hypothesis, conditional, example, quotation or reported
position is not silently collapsed into an author-endorsed world fact.

RC-4 does not call `core.evidence.attach_evidence()`, create an `evidence_spans` row for a fact or
perform truth admission. `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`.

RC-5 adds deterministic pre-admission relation registration in `core/reader_relations.py`. It accepts
only candidate IDs already registered by one RC-4 extractor, requires one OPEN ReaderSession and one
exact SourceVersion, and preserves exact candidate/pass/node IDs plus primary/supporting provenance on
both sides and explicit rationale.

`POSSIBLE_CONTRADICTION` and `TENSION` are symmetric candidate relations; `EXCEPTION` and
`QUALIFICATION` are directional. Symmetric pairs use deterministic candidate-ID order and duplicate
same-kind pairs fail closed rather than becoming corroboration.

RC-5 does not compare raw source text automatically, infer semantic equivalence/cross-document
identity, use similarity as proof, call an LLM/provider, invoke contradiction resolution or choose a
winner. It has no truth/confidence/evidence-sufficiency/resolved/winner field and does not call
`core.evidence.attach_evidence()`.

RC-6 adds deterministic long-context orchestration in `core/reader_long_context.py` without assuming
an infinite model context window. It accepts the current registered RC-4 candidates of one OPEN
ReaderSession and exact SourceVersion, revalidates completed-pass / recovered-structure / current
coverage provenance, sorts by RC-2 structural order with a stable candidate-ID tie-break, and packs
candidates into rolling working sets under explicit candidate-count and unique direct-source-locator
budgets. One candidate is atomic with all of its direct replayable locators; if it cannot fit the
caller-declared locator budget, planning fails closed instead of splitting provenance.

A matching RC-5 registry is optional context only. RC-6 carries an existing relation ID into a
working set only when both relation endpoints are already members of that set. It neither synthesizes
a cross-set relation nor infers relation identity from adjacency/similarity.

RC-6 may register caller-supplied `SourceFidelity.SUMMARY` text for one existing working set. The
summary artifact retains the exact direct RC-4 leaf candidate IDs and the deduplicated replayable
source locators of that set. RC-6 rechecks the working-set provenance snapshot before accepting the
summary, so a summary cannot become a provenance dead-end and cannot rely on another summary as its
only support. RC-6 performs no automatic summarization.

The dedicated/full autonomous Reader / Semantic Reading runtime remains future work. There is no
automatic parser/semantic chunker, automatic NLP/LLM extraction or summarization, provider-driven
reading agent, embeddings/ANN/vector DB, automatic semantic equivalence, RC-7 cross-document reading
or automatic belief update.

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
similarity != identity
repetition != corroboration
```

## Safety and privacy

The default installation has no mandatory cloud, LLM, telemetry or analytics dependency. Optional
remote adapters, wider API exposure and migration targets require explicit operator configuration.
Selected L1 field encryption is not universal encryption. Active-store erasure is not global erasure
of backups, exports, remote systems or provider copies.

Reader RC-1/RC-2/RC-3/RC-4/RC-5/RC-6 retain no source body. Derived Reader artifacts, pass records,
proposition candidates, relation candidates, working sets and summaries inherit source
restriction/sensitivity metadata through the exact source version. Reader structure/order/prominence,
pass completion, proposition extraction, relation registration, working-set fill or summary
registration cannot weaken privacy or epistemic policy.

## Current non-claims

Crystal does not claim:

- AGI, consciousness, universal truth or zero hallucinations;
- active PostgreSQL runtime or automatic backend switching;
- cutover, rollback, dual-write or accepted ANN production profile;
- production multi-tenancy or distributed exactly-once coordination;
- a completed dedicated/full autonomous Reader Core or automatic document comprehension/extraction/summarization;
- RC-7 cross-document reading or automatic semantic contradiction resolution/cross-document identity;
- security, legal or GDPR certification;
- awarded NLnet funding.

NLnet remains submitted / under review / not awarded; approximate €50,000 is planning only and budget
change is none. RC-5 merged pre-agreement becomes existing baseline. If RC-6 merges before an
agreement, RC-6 also becomes existing pre-agreement baseline rather than future funded delta.

## Detailed English contracts

- [Full architecture](./ARCHITECTURE.md)
- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Security/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md)
