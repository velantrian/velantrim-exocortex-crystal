# Velantrim Crystal — Current Status

**Status date:** 2026-08-12  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Verified tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Validated implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
**PostgreSQL integration CI:** `31256316532`  
**Reader RC-6 tracking:** issue #369 / PR #370

## Verification

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- **1/1** real PostgreSQL/pgvector integration job successful.

These counts remain the retained verified runtime checkpoint. Reader milestones merged later carry
their own exact-head and post-merge CI evidence rather than rewriting that historical checkpoint.

Exact historical evidence: [`TEST_REPORT.md`](../TEST_REPORT.md) and the
[machine-readable manifest](./status/implementation-manifest.json). Reader RC-5 was accepted with its
own exact-head/post-merge evidence on PR #368 / issue #367. RC-6 is not final implementation truth
until PR #370 reaches final exact-head 9/9 CI, guarded merge, verified merge signature and exact
post-merge push CI.

## Current verified capability boundary

Crystal retains the local-first SQLite baseline and the verified inactive PostgreSQL import/equivalence path:

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
→ active=false
```

The PostgreSQL driver is an optional extra and is lazy-loaded only by explicit operator
commands. The default installation remains pure standard library. The imported target is
not registered in ordinary runtime composition, remains `active=false`, and cannot serve
normal reads or writes.

## Reader Core bounded implementation

RC-0 is the normative architecture contract. RC-1 through RC-5 are merged bounded milestones; RC-6
is the current separately authorized bounded long-context milestone:

```text
RC-1
→ SourceVersion / SourceLocator
→ ReaderSession / SegmentCard
→ fidelity classes + coverage states
→ bookmarks / open loops
→ stale, failure and privacy semantics

RC-2
→ caller-supplied DocumentStructuralMap
→ version-bound nodes, hierarchy and document order
→ exact-span containment
→ RECOVERED / AMBIGUOUS / UNSUPPORTED
→ structural traversal / telemetry

RC-3
→ explicit ORIENTATION / BROAD_READ / FOCUSED_READ
→ explicit CROSS_CHECK / TARGETED_REREAD
→ one active pass at a time
→ attempted / completed / interrupted / degraded pass ledger
→ declared structural targets + explicit per-region coverage outcomes
→ partial progress preserved across interrupted/degraded passes
→ count-only pass telemetry

RC-4
→ completed substantive RC-3 pass context
→ source-linked EXTRACTED_PROPOSITION candidate
→ explicit source owner + proposition presentation category
→ explicit negation + scope/exception qualifiers
→ primary + supporting replayable locators
→ count-only extraction telemetry

RC-5
→ valid registered RC-4 candidate IDs only
→ one OPEN ReaderSession + one exact SourceVersion
→ POSSIBLE_CONTRADICTION / TENSION
→ EXCEPTION / QUALIFICATION
→ exact two-sided candidate/pass/node linkage
→ primary + supporting replayable provenance on both sides
→ explicit non-empty rationale
→ count-only relation telemetry

RC-6
→ current registered RC-4 candidate set only
→ one OPEN ReaderSession + one exact SourceVersion
→ revalidate completed pass / recovered structure / substantive current coverage
→ RC-2 structural order + stable candidate-ID tie-break
→ bounded rolling working sets
→ max candidates + max unique direct source locators
→ candidate atomicity; oversized candidate fails closed
→ optional RC-5 relation ID only when both sides are in-set
→ caller-supplied SourceFidelity.SUMMARY only
→ direct RC-4 leaf candidate IDs + replayable source provenance retained
→ count/resource telemetry only
```

Machine truth distinguishes these bounded layers from the larger Reader capability:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
dedicated_reader_core                  = false
```

RC-4 is deterministic candidate registration, **not** autonomous NLP/model extraction. A proposition
may be created only from a `COMPLETED` RC-3 pass target whose recorded outcome and current matching
coverage are `PROCESSED` or `REVISITED`. RC-4 preserves source-presentation distinctions for factual
assertion, author opinion, hypothesis, conditional, example, quoted speech, reported position,
definition and uncertain assertion. It also preserves source ownership, negation and qualifiers.

RC-4 candidates are source-linked `SegmentCard` artifacts with `EXTRACTED_PROPOSITION` fidelity.
They are upstream Reader candidates only. RC-4 does **not** call `core.evidence.attach_evidence()`,
attach evidence to a fact, create a Canon fact, mutate `truth_status`/ESM or assert evidence
sufficiency. `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`.

RC-5 runtime lives in `core/reader_relations.py`. `ReaderRelationRegistry` is bound to one
RC-4 `ReaderPropositionExtractor`, therefore one Reader session/source domain. It accepts only IDs
already registered by that extractor and re-validates OPEN session state, candidate session ID,
exact source version, supporting locator versions and candidate-card membership.

`POSSIBLE_CONTRADICTION` and `TENSION` are symmetric candidate relations and use deterministic
candidate-ID order. `EXCEPTION` and `QUALIFICATION` are directional: the right-hand candidate is
registered as limiting/refining the left-hand candidate. Duplicate same-kind symmetric pairs fail
closed rather than becoming corroboration.

Every RC-5 relation preserves relation/session IDs, both exact RC-4 candidate IDs, both pass IDs,
structural node IDs, primary/supporting source locators and explicit rationale. It has no truth,
confidence, evidence-sufficiency, resolved or winner field.

RC-5 is deterministic explicit registration, **not** raw-text semantic contradiction detection.
It does not infer semantic equivalence or cross-document identity, use similarity as proof, call an
LLM/provider, invoke contradiction resolution or choose a winner.

RC-6 runtime lives in `core/reader_long_context.py`. `ReaderLongContextStrategy` is bound to one
RC-4 extractor and can optionally accept a matching RC-5 registry. Planning revalidates each direct
leaf candidate against the current OPEN session, exact source, completed pass, recovered RC-2 node,
current `PROCESSED`/`REVISITED` coverage and registered SegmentCard identity. It then sorts by RC-2
structural order with candidate-ID tie-break and greedily packs working sets under caller-declared
candidate-count/source-locator budgets. One candidate and all direct unique locators are atomic.

Existing RC-5 relation IDs are snapshot context only. A relation is carried into a working set only
when both endpoints are already in that set. RC-6 never infers a cross-set relation, semantic identity
or corroboration.

`ReaderSummaryCandidate` is caller-supplied only and always uses `SourceFidelity.SUMMARY`. Before
registration RC-6 compares current direct leaf locators with the immutable working-set snapshot and
then re-validates the direct RC-4 leaves. The summary stores the direct candidate IDs and replayable
source provenance; another summary cannot be its only provenance path. RC-6 does not generate summary
text automatically.

RC-1/RC-2/RC-3/RC-4/RC-5/RC-6 retain no source body and add no durable Reader storage schema, public
API/CLI/background worker, parser/chunker/OCR/PDF-layout engine, LLM/provider integration,
embeddings/ANN/vector DB or automatic RC-7 cross-document reasoning. They have no method/runtime wiring
that mutates `truth_status`/ESM, writes strict Canon, bypasses Guardian/TruthGate, promotes confidence,
attaches fact evidence, resolves contradictions or creates planner/belief-update authority.

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
structure/order/prominence != epistemic authority
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

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
Reader artifact         = source-linked candidate/observation
Reader structure        = document metadata
Reader pass ledger      = reading-process audit state
Reader proposition      = pre-admission source-linked candidate
Reader relation         = pre-admission relation candidate
Reader working set      = bounded provenance-preserving context snapshot
Reader SUMMARY          = caller-supplied synthesis candidate
migration/import        != TruthGate admission
successful equivalence  != backend activation
Reader coverage         != comprehension proof
Reader pass completion  != comprehension proof
working-set coverage    != comprehension proof
summary                 != evidence / verified fact / Canon admission
```

Guardian, TruthGate, restrictions, TrustSnapshot and CanonicalView remain unchanged.

## Localization truth

English is the primary/source technical language. Russian root and Reader-dependent D1/D3/D4/D5
surfaces are current against immutable English RC-5 source checkpoint
`51c205fe048fd69d39fcd47b43e042a50de432bc`; that RC-5 marker remains historical checkpoint truth.
The current English RC-6 source checkpoint is committed separately before Russian RC-6 refresh, so
existing Russian surfaces must not be interpreted as containing RC-6 semantics until the subsequent
translation commit pins the new exact English SHA. Eight other Reader-dependent locale surfaces
preserve rich translations as `REFRESH_NEEDED`; the tracked Reader/root debt remains 64 documents.
D2 and Quick Start remain current in all nine locales because RC-6 does not change those contracts.

## Still absent

- active PostgreSQL read/write runtime selection;
- exact-vs-ANN retrieval evaluation and accepted ANN thresholds;
- activation, cutover, source/target fencing, rollback or dual-write;
- PostgreSQL backup/restore/upgrade lifecycle, production pooling and distributed fencing;
- production IdP/multi-tenancy and legal/security/GDPR certification;
- automatic Reader parser/semantic chunker/OCR/PDF-layout or multimodal understanding;
- dedicated autonomous/full Semantic Reading runtime;
- automatic NLP/LLM proposition/relation/summary generation or Reader provider integration;
- embeddings, ANN/vector database, semantic equivalence or RC-7 cross-document proposition identity/reasoning engine;
- automatic evidence attachment to facts or admission of Reader candidates;
- automatic contradiction resolution/winner selection;
- planner/autonomous research/belief-update authority.

## Grant status

The NLnet project is **submitted / under review / not awarded**. Approximate **€50,000** is planning
only, not an approved budget or payment commitment. **Budget change: none.** PR #337 and Reader
RC-0/RC-1/RC-2/RC-3/RC-4/RC-5, when merged before an agreement, are existing baseline and cannot be
counted again as future funded delta. If RC-6 merges before an agreement, RC-6 also becomes existing
pre-agreement baseline. Future funding must begin with separately reviewed work beyond the actually
merged pre-agreement baseline.
