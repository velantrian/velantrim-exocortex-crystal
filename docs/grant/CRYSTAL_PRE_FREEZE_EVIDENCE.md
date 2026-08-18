# Crystal Pre-Freeze Evidence Package

Status: **freeze candidate; not production authorization**.

Cleaned implementation baseline SHA: `5b419ed8e268c72caf3d707666006507ab2eefe7`

This package accompanies the Crystal pre-freeze remediation branch. The baseline above contains the production remediation code with all temporary pre-freeze patch scripts and one-shot workflows removed. The current documentation-only child commit is used to trigger the repository's normal supported CI matrix against the same implementation tree.

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
6. Evidence lineage is unknown by default; same-lineage reinforcement cannot increase support twice.
7. Concept clustering excludes non-Validated, restricted, and store-conflicted facts.
8. The shipping evaluation corpus is hash-frozen and gates strict provenance + lineage metrics.

## Explicit non-claims

Crystal does not claim that retrieval equals truth, ranking equals confidence, a graph path is proof, a source label is exact evidence, source count implies independent corroboration, an embedding fallback preserves semantic equivalence, bounded hop depth alone bounds graph work, or green CI constitutes production authorization.

## Freeze exit gate

- [ ] Python 3.11 full CI green on the cleaned implementation tree.
- [ ] Python 3.12 full CI green on the cleaned implementation tree.
- [x] `scripts/eval_gate.py` green with the frozen fixture manifest in the focused Wave 4 gate.
- [x] No temporary pre-freeze patch/workflow files remain.
- [x] Reviewer package identifies the cleaned implementation baseline.
- [x] No advanced RAG framework, semantic Reader runtime, or new authority path introduced.
