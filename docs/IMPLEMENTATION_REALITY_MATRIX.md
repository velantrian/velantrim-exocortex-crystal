# Implementation Reality Matrix

> Date: 2026-06-17
> Scope: current implementation/status matrix for public Crystal planning
> Status: docs-only. This is a companion to `docs/STATUS.md`.

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
| TruthPolicy production default | PLANNED | Track 3A tests for ON/OFF/unset behaviour | unsafe if legacy mode becomes default | Crystal hardening |
| Write-path TruthGate audit | PLANNED | Track 3B behavioural tests | force-approve path needs pinned audit detail | Crystal hardening |
| TRACE / Receipt | IMPLEMENTED | receipt replay tests | overclaim if replay scope unclear | Crystal |
| Per-fact ProvenanceChain | PLANNED | Track 1 implementation + 7 tests | absent per-fact chain may be mistaken for implemented I89 | Crystal hardening |
| Claim type / origin type | DOCUMENTED / candidate | validators + FactsPack + promotion tests | subjective material may leak into facts if unenforced | Crystal candidate |
| Ingest schema | DOCUMENTED | verifier + import tests | weak source/evidence metadata | Crystal candidate |
| Dedup/scale | DOCUMENTED | exact/semantic dedup tests | duplicate frequency mistaken for evidence | Crystal roadmap |
| Knowledge graph data | NEEDS_VERIFICATION | source/evidence coverage report | unverified graph may be presented as canon | Crystal data note |
| Docker deployment | PLANNED | Dockerfile/compose/.dockerignore + manual verification | unsafe if token is optional or public bind used | Track 2 |
| Titan console | RESEARCH | not needed for Crystal claim | production UI overclaim | Titan/Full |
| Noetic Orchestration | RESEARCH | feature flag + tests | future layer presented as runtime | Full Research |
| BICA Alignment | RESEARCH / grant framing | no runtime claim | AGI/brain-like overclaim | Notion/Research |
| Graphiti/Neo4j | OPTIONAL / RESEARCH | optional integration tests | dependency creep | Research/optional |

## Correction notes

- Crystal deployment uses `VELANTRIM_API_TOKEN`, not Titan-oriented `VELANTRIM_API_KEY`.
- Docker files are Track 2 creation targets, not assumed existing files.
- Per-fact ProvenanceChain is planned/absent in Crystal; Titan reported a separate regression.
- No `/facts` POST endpoint should be assumed for Track 3B.
- Major write paths are believed to route through TruthGate; Track 3B pins behaviour and audit detail with tests.

## Rule

If a component is not in this matrix or `docs/STATUS.md`, it must not be used as a public Crystal runtime claim.
