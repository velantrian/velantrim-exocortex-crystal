# Implementation Reality Matrix

> Date: 2026-06-17
> Scope: current implementation/status matrix for public Crystal planning
> Status: docs-only. Canonical detailed audit matrix. `docs/STATUS.md` carries the high-level summary; `docs/IMPLEMENTATION_STATUS.md` is the component-level implemented/RFC/vision map.

## Legend

| Status | Meaning |
|---|---|
| `IMPLEMENTED` | runtime code exists and is tested or reviewer-verifiable |
| `FEATURE_FLAGGED` | exists but off by default or configuration-dependent |
| `DOCUMENTED_ONLY` | design/specification only |
| `PLANNED` | accepted implementation plan, not current runtime |
| `RESEARCH` | private/future research, not public Crystal runtime |
| `LEGACY` | historical material retained for context |
| `NEEDS_VERIFICATION` | audit finding requires code/test confirmation |

## Current Track Plan

```text
Track 1  — ProvenanceChain per-fact event chain
Track 2  — Docker hardening from scratch
Track 3A — TruthPolicy production default
Track 3B — Write-path TruthGate audit/tests
```

## Matrix

| Component | Status | Evidence needed before stronger claim | Risk | Destination |
|---|---|---|---|---|
| Crystal local memory core | IMPLEMENTED | `TEST_REPORT.md`, CI | keep status synced | Crystal |
| TruthGate / Guardian boundary | IMPLEMENTED / evolving | tests for all relevant write/read paths | bypass risk if alternate paths exist | Crystal |
| TruthPolicy production default | IMPLEMENTED | `ENABLE_TRUTH_POLICY` on/off/unset behaviour pinned in `tests/test_truth_gate.py` (Track 3A, #172) | strict is the secure default; the legacy bypass must be opted into via `ENABLE_TRUTH_POLICY=off` | Crystal hardening |
| Write-path TruthGate audit | IMPLEMENTED | `tests/test_write_path_gate.py` + `core/review.py` `gate_reason` audit detail (Track 3B, #175) | force-approve path is pinned: it still calls TruthGate and records the blocking `gate_reason` (content-free) | Crystal hardening |
| TRACE / Receipt | IMPLEMENTED | receipt replay tests | overclaim if replay scope unclear | Crystal |
| Per-fact ProvenanceChain | IMPLEMENTED | `core/provenance_chain.py` (append-only, hash-chained) + tests; wired into the erase path (Track 1, #168) | per-fact chain exists and the GDPR erase path records events; broader lifecycle wiring (other state transitions) remains follow-up | Crystal hardening |
| Claim type / origin type | DOCUMENTED / candidate | validators + FactsPack + promotion tests | subjective material may leak into facts if unenforced | Crystal candidate |
| Ingest schema | DOCUMENTED | verifier + import tests | weak source/evidence metadata | Crystal candidate |
| Dedup/scale | DOCUMENTED | exact/semantic dedup tests | duplicate frequency mistaken for evidence | Crystal roadmap |
| Knowledge graph data | NEEDS_VERIFICATION | source/evidence coverage report | unverified graph may be presented as canon | Crystal data note |
| Docker deployment | IMPLEMENTED | `Dockerfile`/`docker-compose.yml`/`.dockerignore` + manual verification (Track 2, #170; Codex follow-up fixes #171) | fail-fast `VELANTRIM_API_TOKEN`, named-volume default, non-root `velantrim`, image default host `127.0.0.1`; compose binds the container to `0.0.0.0` behind host loopback publish `127.0.0.1:8000:8000` | Crystal hardening |
| Titan console | RESEARCH | not needed for Crystal claim | production UI overclaim | Titan/Full |
| Noetic Orchestration | RESEARCH | feature flag + tests | future layer presented as runtime | Full Research |
| BICA Alignment | RESEARCH / grant framing | no runtime claim | AGI/brain-like overclaim | Notion/Research |
| Graphiti/Neo4j | OPTIONAL / RESEARCH | optional integration tests | dependency creep | Research/optional |

## Correction notes

- Crystal deployment uses `VELANTRIM_API_TOKEN`, not Titan-oriented `VELANTRIM_API_KEY`.
- Docker files were created from scratch in Track 2 (#170) with Codex follow-up fixes (#171); they now exist in the repo.
- Per-fact ProvenanceChain is implemented in Crystal (Track 1, #168: `core/provenance_chain.py`, wired into the erase path); the separate Titan regression is unrelated.
- No `/facts` POST endpoint should be assumed for Track 3B.
- Major write paths route through TruthGate; Track 3B (#175) pinned behaviour and audit detail with tests (`tests/test_write_path_gate.py`).

## Rule

If a component is not in this matrix or `docs/STATUS.md`, it must not be used as a public Crystal runtime claim.
