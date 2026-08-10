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
| Dedicated/full Semantic Reading runtime | Not implemented | no automatic parser, model-driven reader, cross-document engine or autonomous planner; `dedicated_reader_core=false` |

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
source/session domain skeleton, RC-2 adds the smallest structural-map layer needed to
represent recovered document structure without claiming automatic parsing, and RC-3 adds
deterministic explicit multi-pass mechanics without claiming an autonomous reader:

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
```

RC-3 records what the caller actually attempted. It does not call an LLM/provider, decide its own objective, infer undeclared targets or convert pass completion into understanding. `CROSS_CHECK` and `TARGETED_REREAD` require prior substantive processing. Unresolved structural regions can only remain fail-visible through `NEEDS_REVIEW`. Partial outcomes remain visible when a pass is interrupted or degraded.

RC-1/RC-2/RC-3 retain no source body and add no durable Reader storage schema, public API, CLI,
background worker or mandatory dependency. They have no parser/semantic chunker, OCR/PDF-layout or
multimodal engine; no model/provider integration; no embedding, ANN/vector-database Reader stack;
no automatic cross-document reasoning; and no method/runtime wiring that writes Canon, mutates
`truth_status`/ESM, bypasses Guardian/TruthGate, resolves contradictions or creates planner/
belief-update authority.

Machine truth distinguishes the bounded milestones from the larger capability:

```text
reader_core_rc1_skeleton             = true
reader_core_rc2_structural_map       = true
reader_core_rc3_multi_pass_mechanics = true
dedicated_reader_core                = false
```

Coverage telemetry reports touched/unresolved regions only; structural telemetry reports recovered
or unresolved map nodes only; RC-3 telemetry reports pass counts/state only. None is a comprehension
percentage or truth score. Changed source hashes remain version boundaries; RC-2 structural nodes and
RC-3 pass records remain anchored to the exact RC-1 `SourceVersion`.

Crystal does not claim an active PostgreSQL runtime backend, automatic migration,
production multi-tenancy, universal truth, zero hallucinations, legal/security
certification, consciousness or a dedicated/full autonomous Reader Core runtime.