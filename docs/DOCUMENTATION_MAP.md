# 🧭 Crystal Documentation Map

This page routes each reader to the smallest authoritative document and prevents
duplicate implementation claims.

## Start here by audience

| Audience | First document | Then read |
|---|---|---|
| New user | [README](../README.md) | [Quick start](./QUICKSTART.md), [Architecture](./ARCHITECTURE.md) |
| Grant reviewer | [Reviewer guide](./REVIEWER_GUIDE.md) | [Test report](../TEST_REPORT.md), [Grant scope](./GRANT_NLNET_SCOPE.md) |
| Engineer | [Implementation status](./IMPLEMENTATION_STATUS.md) | [ADR index](./ADR.md), [Failure modes](./FAILURE_MODES.md) |
| Operator | [Quick start](./QUICKSTART.md) | [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md), [Threat model](./security/threat-model.md) |
| Security reviewer | [Security policy](../SECURITY.md) | [Threat model](./security/threat-model.md), [Privacy](../PRIVACY.md) |
| Researcher | [Implementation status](./IMPLEMENTATION_STATUS.md) | [Roadmap](../ROADMAP.md), RFCs, [Metaphor vs mechanism](./METAPHOR_VS_MECHANISM.md) |
| Contributor | [Contributing](../CONTRIBUTING.md) | [Test report](../TEST_REPORT.md), [Governance](../GOVERNANCE.md) |

## Authority hierarchy

```text
GitHub main code and tests
        ↓
TEST_REPORT.md + implementation-manifest.json
        ↓
docs/STATUS.md + docs/IMPLEMENTATION_STATUS.md
        ↓
README and reviewer guides
        ↓
localized translations
        ↓
RFC, roadmap and research documents
```

Notion is the synchronized strategy/grant map; it does not replace merged code
as implementation truth.

## Core architecture and trust

- [Architecture](./ARCHITECTURE.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Read-only query boundary](./architecture/read-only-query-boundary.md)
- [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md)
- [Ring Zero mutation gate](./testing/RING_ZERO_MUTATION_GATE.md)
- [CanonicalView RFC](./CANONICAL_VIEW_RFC.md)
- [ADR index](./ADR.md)

## Evidence, state and performance

- [Test report](../TEST_REPORT.md)
- [Current status](./STATUS.md)
- [Evaluation](./EVAL.md)
- [Failure modes](./FAILURE_MODES.md)
- [L3 retrieval benchmark](./benchmarks/L3_RETRIEVAL_SCALE.md)

The ESM runtime has one machine-readable specification derived from the shared
transition matrix. Performance history uses versioned scheduled/manual artifacts
and comparable-run reporting; shared PR-runner latency is not a hard SLO.

## Grant boundary

- [NLnet scope](./GRANT_NLNET_SCOPE.md)
- [Baseline versus funded delta](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)

The proposal remains submitted and under review; funding is not claimed as
awarded.

## Completed hardening workstream

The documentation/read-only/trust hardening sequence through PR #300 is complete:
read-only queries, non-configurable TruthGate policy, immutable snapshots,
mutation testing, contradiction decisions, ESM specification, performance
history, public conflict surfaces and exact status synchronization.

## Future roadmap

Independent future packages include advisory topic facets, production IAM and
multi-curator authorization, broader provenance lifecycle wiring, controlled
performance SLOs, wider mutation coverage and separate Titan research.

## Translation policy

English code-facing documents are normative. Localized pages are maintained
reader surfaces and link back to the authoritative English status and test
report.
