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
| Dedicated multi-pass Reader Core / Semantic Reading runtime | Not implemented | no parser/orchestration/model/vector runtime; `dedicated_reader_core=false` |

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
source/session domain skeleton, and RC-2 adds the smallest structural-map layer needed to
represent recovered document structure without claiming automatic parsing:

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
```

RC-2 represents structure supplied by a caller. It is **not** a parser, semantic chunker, OCR,
PDF-layout reconstruction, image-understanding or multimodal engine. Unsupported or ambiguous
structure stays explicit with a reason instead of being invented. Structural prominence, heading
level and document order carry no truth/confidence authority.

RC-1/RC-2 retain no source body and add no durable Reader storage schema, public API, CLI,
background worker or mandatory dependency. They have no LLM/provider, embedding, ANN/vector-
database or multi-pass orchestration integration, and no method/runtime wiring that writes Canon,
mutates `truth_status`/ESM, bypasses Guardian/TruthGate, resolves contradictions or creates
planner/belief-update authority.

Machine truth distinguishes the bounded milestones from the larger capability:

```text
reader_core_rc1_skeleton       = true
reader_core_rc2_structural_map = true
dedicated_reader_core          = false
```

Coverage telemetry reports touched/unresolved regions only; structural telemetry reports recovered
or unresolved map nodes only. Neither is a comprehension percentage. Changed source hashes remain
version boundaries; RC-2 structural nodes are anchored to the exact RC-1 `SourceVersion` and cannot
silently migrate across source versions.

Crystal does not claim an active PostgreSQL runtime backend, automatic migration,
production multi-tenancy, universal truth, zero hallucinations, legal/security
certification, consciousness or a dedicated multi-pass Reader Core runtime.