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
| `RESEARCH` | private/future research, not public Crystal runtime |
| `LEGACY` | historical material retained for context |
| `NEEDS_VERIFICATION` | audit finding requires code/test confirmation |

## Matrix

| Component | Status | Evidence needed before stronger claim | Risk | Destination |
|---|---|---|---|---|
| Crystal local memory core | IMPLEMENTED | `TEST_REPORT.md`, CI | keep status synced | Crystal |
| TruthGate / Guardian boundary | IMPLEMENTED / evolving | tests for all write/read paths | bypass risk if alternate paths exist | Crystal |
| TRACE / Receipt | IMPLEMENTED | receipt replay tests | overclaim if replay scope unclear | Crystal |
| Provenance chain | NEEDS_VERIFICATION | append/verify/tamper tests | audit regression reported in Titan | Crystal hardening |
| Claim type / origin type | DOCUMENTED / candidate | validators + FactsPack + promotion tests | subjective material may leak into facts if unenforced | Crystal candidate |
| Ingest schema | DOCUMENTED | verifier + import tests | weak source/evidence metadata | Crystal candidate |
| Dedup/scale | DOCUMENTED | exact/semantic dedup tests | duplicate frequency mistaken for evidence | Crystal roadmap |
| Knowledge graph data | NEEDS_VERIFICATION | source/evidence coverage report | unverified graph may be presented as canon | Crystal data note |
| Deployment security | NEEDS_VERIFICATION | compose/Dockerfile review | unsafe defaults can weaken auth | Crystal hardening |
| Titan console | RESEARCH | not needed for Crystal claim | production UI overclaim | Titan/Full |
| Noetic Orchestration | RESEARCH | feature flag + tests | future layer presented as runtime | Full Research |
| BICA Alignment | RESEARCH / grant framing | no runtime claim | AGI/brain-like overclaim | Notion/Research |
| Graphiti/Neo4j | OPTIONAL / RESEARCH | optional integration tests | dependency creep | Research/optional |

## Rule

If a component is not in this matrix or `docs/STATUS.md`, it must not be used as a public Crystal runtime claim.
