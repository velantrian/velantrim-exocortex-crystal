# Crystal Pre-Freeze Evidence Package

Status: **freeze candidate; not production authorization**.

Implementation baseline SHA: `a563a0f6661c477ca6403b4cda8775acf190e799`.

Final implementation CI evidence: GitHub Actions `CI` run **#1738** (`run_id=32195304666`) on that exact SHA.

- Python 3.11: **2322 passed, 13 skipped, 100.00% coverage**.
- Python 3.12: **2322 passed, 13 skipped, 100.00% coverage**.
- Eval gate: **green**.
- Security: **green**.
- Code quality / Ruff: **green**.
- Documentation status: **green**.
- JSONL integrity: **green**.
- Ring Zero mutation gate: **green**.
- Hardened Docker image build: **green**.

This document is a docs-only child commit over the tested implementation baseline. The implementation SHA above, not the documentation child SHA, is the commit-pinned code/test evidence object.

## Architecture boundary

- General admitted-memory retrieval: bounded vector recall + default-deny graph recall + RRF.
- Reader RC-9: deterministic lexical **pre-admission** candidate discovery.
- Reader semantic/hybrid runtime: **not authorized**.
- Retrieval rank / graph activation: navigation signals only; never truth or evidence authority.
- Public query path: read-only and deny-dominant.

## Freeze blockers remediated

1. Logical-export verification uses directory identity plus deterministic entry inventory and a bounded directory-entry ceiling.
2. Graph recall uses a positive edge allow-list and independent work ceilings.
3. Grant strict grounding requires replayable non-empty evidence spans for VERIFIED facts.
4. Grant retrieval profile requires a pinned embedder; mismatch/provider degradation is explicit.
5. TRACE v2 calls relevance `retrieval_score` and carries bounded retrieval explanation.
6. In the grant profile, reinforcement accepts an authoritative `evidence_id`; lineage is derived from the evidence store, `UNKNOWN`/`SAME_LINEAGE` cannot raise support, and one lineage can contribute at most once.
7. Concept clustering excludes non-Validated, restricted, and store-conflicted facts.
8. The shipping evaluation corpus is hash-frozen; a missing/malformed manifest fails closed and the gate checks strict provenance + lineage metrics.

## Explicit non-claims

Crystal does not claim that retrieval equals truth, ranking equals confidence, a graph path is proof, a source label is exact evidence, source count implies independent corroboration, an embedding fallback preserves semantic equivalence, bounded hop depth alone bounds graph work, or green CI constitutes production authorization. Durable SQLite/Cypher graph backends push edge limits into the backend query; `MockL3Graph` is a non-durable test backend and is not part of the production resource-bound claim. The HTTP API exposes evidence read-only; it does not expose `attach_evidence()` or `reinforce()` as remote write authority.

## Freeze exit gate

- [x] Python 3.11 full CI green on implementation SHA `a563a0f6661c477ca6403b4cda8775acf190e799`.
- [x] Python 3.12 full CI green on implementation SHA `a563a0f6661c477ca6403b4cda8775acf190e799`.
- [x] `scripts/eval_gate.py` green with the frozen fixture manifest.
- [x] Security, code-quality, docs-status, JSONL-integrity, Ring Zero mutation, and Docker build gates green.
- [x] No temporary pre-freeze patch/workflow files remain.
- [x] Reviewer package identifies the exact implementation baseline and exact CI run.
- [x] No advanced RAG framework, semantic Reader runtime, or new authority path introduced.

## Freeze recommendation

The pre-freeze remediation scope is complete. The branch is suitable for reviewer inspection and an explicit human freeze/merge decision. This package does **not** itself authorize production deployment, Canon mutation, or merge to `main`.
