# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-10  
**Verified runtime checkpoint:** `bbd816c` / PR #337  
**Exact evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | storage, migration and Reader artifacts cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented and tested | restore is inactive and never admission |
| Bounded-streaming SQLite logical export/verify | Implemented and tested | canonical backend-neutral bundle |
| PostgreSQL optional dependency and preflight | Implemented and tested | explicit extra, lazy load, pinned supported versions |
| Inactive PostgreSQL/pgvector import | Implemented and tested | new inactive schema only; no ordinary reads/writes |
| Exact target-state equivalence | Implemented and tested | approved bundle datasets; independent read-only re-hash |
| Active PostgreSQL runtime adapter | Not implemented | target is not registered in normal runtime composition |
| Automatic SQLite/PostgreSQL switching | Forbidden | availability and import success are not selection |
| Exact-vs-ANN retrieval evaluation | Not implemented | later separately reviewed phase |
| Cutover / rollback / dual-write | Not implemented | explicit later phases only |
| PostgreSQL server lifecycle | Not implemented | backup/restore/upgrade/pooling remain future work |
| Reader Core RC-0 architecture contract | Documented | [architecture contract](./architecture/READER_CORE_ARCHITECTURE.md) defines the authority and validation baseline |
| Reader Core RC-1 minimal evidence-linked skeleton | Implemented in bounded domain layer | `core/reader_core.py`; source/version/locator, fidelity, coverage, bookmarks/open loops, stale/failure/privacy semantics; no admission side effects |
| Reader Core RC-2 structural document map | Implemented in bounded structural layer | `core/reader_structure.py`; caller-supplied version-bound hierarchy/order/ambiguity model; no parser or admission side effects |
| Reader Core RC-3 explicit multi-pass mechanics | Implemented in bounded orchestration layer | `core/reader_passes.py`; explicit pass ledger and coverage effects over declared RC-2 targets; no autonomous/model authority |
| Reader Core RC-4 proposition extraction | Implemented in bounded pre-admission layer | `core/reader_extraction.py`; completed substantive RC-3 regions → source-linked `EXTRACTED_PROPOSITION` candidates; no fact evidence or truth admission |
| Dedicated/full Semantic Reading runtime | Not implemented | no automatic parser, autonomous NLP/model reader, cross-document engine or autonomous planner; `dedicated_reader_core=false` |

## Current storage sequence

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

Issues #331 and #332 are implemented by PRs #335 and #337. The default installation remains
pure standard library; PostgreSQL support is an optional operator path. `active=false` is
constrained in the target control state and successful equivalence cannot activate a
backend or change Guardian, TruthGate or strict Canon.

Future storage work:

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

## Reader Core implementation boundary

RC-0 remains the normative architecture contract. RC-1 adds the smallest evidence-linked
source/session domain skeleton, RC-2 adds the structural-map layer, RC-3 adds deterministic
explicit multi-pass mechanics, and RC-4 adds bounded source-linked proposition extraction
without claiming automatic language understanding or epistemic admission:

```text
SourceVersion(document_id + source_uri + SHA-256)
→ SourceLocator(exact span or explicit structural locator)
→ ReaderSession
   ├─ SegmentCard + mandatory SourceFidelity
   ├─ CoverageEntry / CoverageTelemetry
   ├─ ReaderBookmark
   └─ OpenLoop

SourceVersion + SourceLocator
→ DocumentStructuralMap
   ├─ StructuralNode(kind + order + parent)
   ├─ RECOVERED / AMBIGUOUS / UNSUPPORTED
   ├─ cycle / missing-parent / duplicate validation
   ├─ exact-span containment validation
   └─ immutable traversal + structural telemetry

ReaderSession + DocumentStructuralMap
→ MultiPassReader
   ├─ ORIENTATION
   ├─ BROAD_READ
   ├─ FOCUSED_READ
   ├─ CROSS_CHECK
   ├─ TARGETED_REREAD
   ├─ ATTEMPTED / COMPLETED / INTERRUPTED / DEGRADED ledger
   ├─ declared structural targets
   ├─ explicit per-region coverage outcomes
   └─ count-only pass telemetry

COMPLETED substantive Reader pass
→ ReaderPropositionExtractor
   ├─ primary + optional supporting structural targets
   ├─ PROCESSED / REVISITED outcome required
   ├─ EXTRACTED_PROPOSITION SegmentCard
   ├─ source owner
   ├─ factual assertion / opinion / hypothesis / conditional
   ├─ example / quoted speech / reported position / definition / uncertainty
   ├─ explicit negation + scope/exception qualifiers
   └─ count-only extraction telemetry
```

RC-4 is a validation/registration layer, not an automatic extractor. The caller supplies the
normalized proposition; RC-4 proves that the proposed candidate is anchored to a completed
substantive RC-3 reading context and still-current matching RC-1/RC-2 provenance. It fails closed
for `SEEN`, `NEEDS_REVIEW`, unresolved structure, incomplete passes, stale/mismatched coverage or
source/session mismatch.

RC-4 candidates are always `SourceFidelity.EXTRACTED_PROPOSITION`. The category
`FACTUAL_ASSERTION` means only that the source presents a statement as factual; it does **not**
mean Crystal verified the proposition. Quoted speech, reported positions, author opinion,
hypotheses, conditionals, examples, definitions and uncertain assertions remain explicit instead
of being collapsed into author-endorsed world facts.

RC-4 does not call `core.evidence.attach_evidence()` and writes no `evidence_spans` fact record.
It does not attach evidence to a fact, set evidence sufficiency, mutate `truth_status`/ESM, write
strict Canon, bypass Guardian/TruthGate or resolve contradictions. Reader extraction remains
upstream of the existing explicit ingest/review/evidence/admission path.

RC-1/RC-2/RC-3/RC-4 retain no source body and add no durable Reader storage schema, public API,
CLI, background worker or mandatory dependency. They have no automatic parser/semantic chunker,
OCR/PDF-layout or multimodal engine; no model/provider integration; no embedding, ANN/vector-
database Reader stack; no automatic cross-document proposition identity/reasoning; and no planner/
belief-update authority.

Machine truth distinguishes the bounded milestones from the larger capability:

```text
reader_core_rc1_skeleton              = true
reader_core_rc2_structural_map        = true
reader_core_rc3_multi_pass_mechanics  = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core                 = false
```

Coverage telemetry reports touched/unresolved regions only; structural telemetry reports recovered
or unresolved map nodes only; RC-3 telemetry reports pass counts/state only; RC-4 telemetry reports
candidate/category counts only. None is a comprehension, truth, confidence or evidence-sufficiency
score. Changed source hashes remain version boundaries; all Reader artifacts remain anchored to the
exact RC-1 `SourceVersion`.

Crystal does not claim an active PostgreSQL runtime backend, automatic migration,
production multi-tenancy, universal truth, zero hallucinations, legal/security
certification, consciousness or a dedicated/full autonomous Reader Core runtime.