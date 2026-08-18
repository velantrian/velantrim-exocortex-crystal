# Crystal Pre-Freeze Evidence Package

Status: **freeze candidate; not production authorization**.

Implementation candidate SHA: `7855c6d94c91c77a2e7666902c8012360f028a50`

This package accompanies the Crystal pre-freeze remediation branch. The exact
implementation baseline SHA and CI run IDs are pinned only after the final code
commit has passed the supported Python 3.11/3.12 matrix. A documentation-only
closure commit may reference that already-tested implementation SHA.

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

Crystal does not claim that retrieval equals truth, ranking equals confidence, a graph
path is proof, a source label is exact evidence, source count implies independent
corroboration, an embedding fallback preserves semantic equivalence, bounded hop
depth alone bounds graph work, or green CI constitutes production authorization.

## Freeze exit gate

- [ ] Python 3.11 full CI green on the exact implementation candidate.
- [ ] Python 3.12 full CI green on the exact implementation candidate.
- [ ] `scripts/eval_gate.py` green with the frozen fixture manifest.
- [ ] No temporary pre-freeze patch/workflow files remain.
- [ ] Final reviewer package pins the tested implementation SHA and CI/eval evidence.
- [ ] No advanced RAG framework, semantic Reader runtime, or new authority path introduced.
