# Velantrim Crystal — Current Status

**Status date:** 2026-08-10  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Verified tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Validated implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
**PostgreSQL integration CI:** `31256316532`

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

Exact evidence: [`TEST_REPORT.md`](../TEST_REPORT.md) and the
[machine-readable manifest](./status/implementation-manifest.json).

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
```

The PostgreSQL driver is an optional extra and is lazy-loaded only by explicit operator
commands. The default installation remains pure standard library. The imported target is
not registered in ordinary runtime composition, remains `active=false`, and cannot serve
normal reads or writes.

## Reader Core bounded implementation

RC-0 is the normative architecture contract. Four bounded implementation milestones are represented by the current Reader implementation line; each milestone carries its own exact CI evidence rather than rewriting the retained historical runtime checkpoint:

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
```

Machine truth distinguishes these bounded layers from the larger Reader capability:

```text
reader_core_rc1_skeleton             = true
reader_core_rc2_structural_map       = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core                = false
```

RC-4 is deterministic candidate registration, **not** autonomous NLP/model extraction. A proposition may be created only from a `COMPLETED` RC-3 pass target whose recorded outcome and current matching coverage are `PROCESSED` or `REVISITED`. RC-4 preserves source-presentation distinctions for factual assertion, author opinion, hypothesis, conditional, example, quoted speech, reported position, definition and uncertain assertion. It also preserves source ownership, negation and qualifiers instead of silently turning reported or conditional text into an unqualified world fact.

RC-4 candidates are implemented as source-linked `SegmentCard` artifacts with `EXTRACTED_PROPOSITION` fidelity. They are upstream Reader candidates only. RC-4 does **not** call `core.evidence.attach_evidence()`, attach evidence to a fact, create a Canon fact, mutate `truth_status`/ESM or assert evidence sufficiency. `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`.

RC-1/RC-2/RC-3/RC-4 retain no source body and add no durable Reader storage schema, public API/CLI/background worker, parser/chunker/OCR/PDF-layout engine, LLM/provider integration, embeddings/ANN/vector DB or automatic cross-document reasoning. They have no method/runtime wiring that mutates `truth_status`/ESM, writes strict Canon, bypasses Guardian/TruthGate, resolves contradictions or creates planner/belief-update authority. `coverage != comprehension proof`; pass completion likewise does not prove comprehension. Structural position/order/prominence is metadata, not truth/confidence authority.

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
migration/import        != TruthGate admission
successful equivalence  != backend activation
Reader coverage         != comprehension proof
Reader pass completion  != comprehension proof
Reader structure        != epistemic authority
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
```

Guardian, TruthGate, restrictions, TrustSnapshot and CanonicalView remain unchanged.

## Still absent

- active PostgreSQL read/write runtime selection;
- exact-vs-ANN retrieval evaluation and accepted ANN thresholds;
- activation, cutover, source/target fencing, rollback or dual-write;
- PostgreSQL backup/restore/upgrade lifecycle, production pooling and distributed fencing;
- production IdP/multi-tenancy and legal/security/GDPR certification;
- automatic Reader parser/semantic chunker/OCR/PDF-layout or multimodal understanding;
- dedicated autonomous/full Semantic Reading runtime;
- automatic NLP/LLM proposition extraction or Reader provider integration;
- embeddings, ANN/vector database or automatic cross-document proposition identity/reasoning engine;
- automatic evidence attachment to facts or admission of Reader candidates;
- planner/autonomous research/belief-update authority.

## Grant status

The project is submitted and under review. **No award or budget change** is claimed. PR #337,
Reader RC-0/RC-1/RC-2/RC-3 and any RC-4 work merged before an agreement are existing baseline and cannot
be counted again as future funded delta. Future funding must begin with separately reviewed work
beyond the verified pre-agreement baseline.