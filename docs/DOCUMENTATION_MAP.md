# 🧭 Crystal Documentation Map

This page routes each reader to the smallest authoritative document and prevents
duplicate implementation claims.

## Start here by audience

| Audience | First document | Then read |
|---|---|---|
| New user | [README](../README.md) | [Quick start](./QUICKSTART.md), [Architecture](./ARCHITECTURE.md) |
| Grant reviewer | [Reviewer guide](./REVIEWER_GUIDE.md) | [Test report](../TEST_REPORT.md), [Grant scope](./GRANT_NLNET_SCOPE.md) |
| Engineer | [Implementation status](./IMPLEMENTATION_STATUS.md) | [ADR index](./ADR.md), [Failure modes](./FAILURE_MODES.md) |
| Operator | [Quick start](./QUICKSTART.md) | [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md), [Topic facets and curator IAM](./TOPIC_FACETS_AND_CURATOR_IAM.md) |
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
English README capability contract
        ↓
semantically aligned localized READMEs
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
- [Topic facets and curator IAM](./TOPIC_FACETS_AND_CURATOR_IAM.md)
- [Ring Zero mutation gate](./testing/RING_ZERO_MUTATION_GATE.md)
- [CanonicalView RFC](./CANONICAL_VIEW_RFC.md)
- [ADR index](./ADR.md)

## Evidence, state and performance

- [Test report](../TEST_REPORT.md)
- [Current status](./STATUS.md)
- [Implementation manifest](./status/implementation-manifest.json)
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

The documentation/read-only/trust hardening sequence through PR #302 is complete:
read-only queries, non-configurable TruthGate policy, immutable snapshots,
mutation testing, contradiction decisions, ESM specification, performance
history, public conflict surfaces, advisory topic facets, scoped curator
authorization, process-local decision leases and synchronized multilingual
README surfaces.

## Independent future roadmap

Future packages include an external distributed lease adapter, production
identity-provider and multi-tenant policy integration, broader provenance
lifecycle wiring, controlled performance SLOs, wider mutation coverage and
separate Titan research.

## Translation policy

English code-facing documents remain normative. The ten top-level README files
share one capability and safety contract. `docs-status` checks their checkpoint,
metrics, core safety markers and local links so translations cannot silently
retain an obsolete architecture description.
