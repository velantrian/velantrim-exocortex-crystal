# Crystal Pre-Freeze Evidence Package

Status: **freeze candidate; not production authorization**.

Corrective closure status: **pending final exact-SHA CI evidence**.

The exact freeze-candidate SHA is intentionally not pinned until the corrective delta and the full Python 3.11/3.12 matrix are green on one head. Intermediate SHAs are not freeze evidence.

## Architecture boundary

- General admitted-memory retrieval: bounded vector recall + default-deny graph recall + RRF.
- Reader RC-9: deterministic lexical **pre-admission** candidate discovery.
- Reader semantic/hybrid runtime: **not authorized**.
- Retrieval rank / graph activation: navigation signals only; never truth or evidence authority.
- Public query path: read-only and deny-dominant.

## Freeze blockers remediated

1. Logical-export verification uses directory identity plus deterministic entry inventory.
2. Graph recall uses a positive edge allow-list and independent work ceilings.
3. Grant strict grounding requires replayable evidence spans for VERIFIED facts.
4. Grant retrieval profile requires a pinned embedder; mismatch/provider degradation is explicit.
5. TRACE v2 calls relevance `retrieval_score` and carries bounded retrieval explanation.
6. In the grant profile, reinforcement accepts an authoritative `evidence_id`; lineage is derived from the evidence store, `UNKNOWN`/`SAME_LINEAGE` cannot raise support, and one lineage can contribute at most once.
7. Concept clustering excludes non-Validated, restricted, and store-conflicted facts.
8. The shipping evaluation corpus is hash-frozen; a missing/malformed manifest fails closed and the gate checks strict provenance + lineage metrics.

## Explicit non-claims

Crystal does not claim that retrieval equals truth, ranking equals confidence, a graph path is proof, a source label is exact evidence, source count implies independent corroboration, an embedding fallback preserves semantic equivalence, bounded hop depth alone bounds graph work, or green CI constitutes production authorization. Durable SQLite/Cypher graph backends push edge limits into the backend query; `MockL3Graph` is a non-durable test backend and is not part of the production resource-bound claim. The HTTP API exposes evidence read-only; it does not expose `attach_evidence()` or `reinforce()` as remote write authority.

## Freeze exit gate

- [ ] Python 3.11 full CI green on the cleaned implementation tree.
- [ ] Python 3.12 full CI green on the cleaned implementation tree.
- [x] `scripts/eval_gate.py` green with the frozen fixture manifest in the focused Wave 4 gate.
- [x] No temporary pre-freeze patch/workflow files remain.
- [x] Reviewer package identifies the cleaned implementation baseline.
- [x] No advanced RAG framework, semantic Reader runtime, or new authority path introduced.
