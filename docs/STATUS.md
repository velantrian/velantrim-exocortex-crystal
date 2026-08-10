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

RC-0 is the normative architecture contract. Two bounded implementation milestones are now merged and tested:

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
```

Machine truth distinguishes these foundations from the larger Reader capability:

```text
reader_core_rc1_skeleton       = true
reader_core_rc2_structural_map = true
dedicated_reader_core          = false
```

RC-1/RC-2 retain no source body and add no durable Reader storage schema, public API/CLI/background worker, LLM/provider integration, embeddings/ANN/vector DB or multi-pass orchestration. They have no method/runtime wiring that mutates `truth_status`/ESM, writes strict Canon, bypasses Guardian/TruthGate, resolves contradictions or creates planner/belief-update authority. `coverage != comprehension proof`; structural position/order/prominence is metadata, not truth/confidence authority.

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
Reader artifact         = source-linked candidate/observation
Reader structure        = document metadata
migration/import        != TruthGate admission
successful equivalence  != backend activation
Reader coverage         != comprehension proof
Reader structure        != epistemic authority
```

Guardian, TruthGate, restrictions, TrustSnapshot and CanonicalView remain unchanged.

## Still absent

- active PostgreSQL read/write runtime selection;
- exact-vs-ANN retrieval evaluation and accepted ANN thresholds;
- activation, cutover, source/target fencing, rollback or dual-write;
- PostgreSQL backup/restore/upgrade lifecycle, production pooling and distributed fencing;
- production IdP/multi-tenancy and legal/security/GDPR certification;
- automatic Reader parser/semantic chunker/OCR/PDF-layout or multimodal understanding;
- dedicated multi-pass Reader orchestration / Semantic Reading runtime;
- Reader LLM/provider, embeddings, ANN/vector database or cross-document reasoning engine.

## Grant status

The project is submitted and under review. **No award or budget change** is claimed. PR #337,
Reader RC-0/RC-1/RC-2 and other work merged before any agreement are existing baseline and cannot
be counted again as future funded delta. Future funding must begin with separately reviewed work
beyond the verified pre-agreement baseline.