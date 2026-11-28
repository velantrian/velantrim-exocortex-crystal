# CR-09A — explicit cascade recovery boundary

**Status: PROPOSED / DRAFT IMPLEMENTATION / NOT RUNTIME-AUTHORIZED.**

Code baseline: `78088e029b86d8f923178d19e9cecabd650a4f61`. Issue [#504](https://github.com/velantrian/velantrim-exocortex-crystal/issues/504).
Related independent draft [#516](https://github.com/velantrian/velantrim-exocortex-crystal/pull/516) corrects the
public description of existing cascade scope. Do not duplicate its changes.

## Static producer inventory

| Surface | Observed operation | Dependency interpretation |
|---|---|---|
| `core/erasure.py::record_derivation` | Explicit L3 DERIVED_FROM edge | Declared causal relation; current callers must be inventoried; no new producer wired here |
| `core/knowledge.py::ingest_claims` | Ingest each extracted claim; attach span only for newly accepted fact | Source evidence, not automatically fact-to-fact derivation; duplicate independent evidence is a separate CR-10 gap |
| `core/imports.py::import_file` / `erase_session` | Register newly owned fact IDs after import; erase those IDs | Session ownership, not complete source/version lineage; crash window remains |
| `core/reconcile.py::supersede` | New claim through existing admission path, SUPERSEDED_BY edge | Replacement may be independent; do not infer derivation from supersession |
| `core/reconcile.py::reinforce`, `record_occurrence` | Change confidence and occurrence metadata | Evidence-dependent state update, not a new derived fact |
| `core/consolidate.py::consolidate` | Decays existing L1/L3 confidence | No new fact/summary producer |
| `core/reader_long_context.py::register_summary` | Caller-supplied summary with direct leaf locators in Reader session | Pre-admission artifact, not automatic Canon write |
| `core/reader_product_bridge.py::run` | Bounded read passes and coverage | No evidence admission or Canon write |
| `core/reader_cross_document.py::register` | Explicit cross-document candidate relation | Candidate relation, not evidence admission or causal dependence |
| L3 retrieval/episode/contradiction edges | Retrieval or relationship projection | Not a causal derivation registry |

This is a bounded static map of inspected producers, not a repository-wide proof
of absence of other writers. #504 remains open.

## Implemented candidate scope

The current erase path collects child IDs into a Python list, deletes source
L1/L3, writes a tombstone, and recurses. The physical L3 adapter deletes incident
edges. If interrupted after those edges disappear, another explicit cascade can
lose its children.

This candidate retains pending explicit child IDs in the existing L1 SQLite file
before deleting the source node. The same explicit `erase_fact(id, cascade=True)`
can resume from those IDs after reopening the graph. The pending rows are
removed only after the recursive call returns successfully. No claim, source
text, source URI or new claim hash is stored in this recovery table. Identifiers
are content-light, **not anonymous**; access, retention, backup and migration
requirements still need review.

The additive table is initialized on the cascade path, not on normal reads.
The pending plan is not a tombstone and does not prove erasure. If the root was
lost before its original tombstone, the retry may record a null content hash;
it cannot reconstruct the lost historical proof. This candidate does not change
the old fact-ID or ESM contracts, does not re-admit or re-derive content, and
does not extend the cascade scope to unrecorded dependencies.

## Explicit non-claims / HOLD

- Not a complete or automatic erasure lifecycle. The operator must explicitly
  retry with cascade enabled; no startup worker is authorized.
- Not a read/write denial fence: concurrent reads, new derivations, retry writers
  and restored old copies are not covered. The plan is a snapshot of known edges,
  not a completeness guarantee. Overlapping workers and resource bounds require
  separate deterministic acceptance tests before merge.
- Not a permanent independent lineage registry. A prior plain erase can already
  have lost edges. No retroactive inference from similarity, supersession,
  shared URI, confidence or a declared independence label.
- No changes to Ring Zero, Guardian, TruthGate, Canon authority or fact identity.
- No legal/GDPR certification. Do not use a successful local receipt as proof
  of removal from every copy or of a full erasure request.
- No automatic new-ID or re-derivation. Content-scoped deletion, source-scoped
  deletion, evidence sufficiency and identity policy need an owner decision.
- Persistent plan schema/retention, migration/backup and multi-worker semantics
  require independent review. **Merge HOLD.**

## Validation

Tests use actual local SQLite L1 and L3, synthetic claims, deterministic hashing,
and injected failures at the graph deletion/tombstone boundaries. The test
fixture reopens the graph and clears L0; it is not an OS crash or power-loss
experiment. The existing suite retains the positive, cycle and Ring Zero controls.

```bash
python -m pytest -o addopts="" tests/test_erasure_cascade_recovery.py tests/test_erasure.py -q
python -m pytest tests/ --cov=. --cov-fail-under=100
```

Local full-repository verification is not claimed: the current execution
environment could not resolve github.com to clone the repository. Existing
hosted CI may run when the draft is opened; report results only for the exact
head. No local Docker or model API is needed. The hosted matrix itself includes
a Docker build.

## Next bounded step

Reproduce the two interruption scenarios against baseline and candidate; review
the pending-plan lifetime, then decide the durable source/record-version
lineage and operation-level deny fence. Do not promote an intermediate recovery
mechanism into a complete deletion guarantee. #504 stays OPEN.
