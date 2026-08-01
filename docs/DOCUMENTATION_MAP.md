# 🧭 Crystal Documentation Map

This page routes readers to the smallest authoritative document for their goal.
It exists to keep `README.md` readable and to reduce duplicate or drifting
implementation claims.

## Start here by audience

| Audience | First document | Then read |
|---|---|---|
| New user | [README](../README.md) | [Quick start](./QUICKSTART.md), [Architecture](./ARCHITECTURE.md) |
| Grant reviewer | [Reviewer guide](./REVIEWER_GUIDE.md) | [Reviewer demo](./REVIEWER_DEMO.md), [Test report](../TEST_REPORT.md), [Grant scope](./GRANT_NLNET_SCOPE.md) |
| Engineer | [Architecture](./ARCHITECTURE.md) | [Implementation status](./IMPLEMENTATION_STATUS.md), [ADR index](./ADR.md), [Failure modes](./FAILURE_MODES.md) |
| Security reviewer | [Security policy](../SECURITY.md) | [Threat model](./security/threat-model.md), [Privacy](../PRIVACY.md) |
| Researcher | [Implementation status](./IMPLEMENTATION_STATUS.md) | [Roadmap](../ROADMAP.md), RFC documents, [Metaphor vs mechanism](./METAPHOR_VS_MECHANISM.md) |
| Operator | [Quick start](./QUICKSTART.md) | [Architecture](./ARCHITECTURE.md), [EU service security readiness](./security/eu-service-security-readiness.md), [Threat model](./security/threat-model.md) |
| Contributor | [Contributing](../CONTRIBUTING.md) | [Governance](../GOVERNANCE.md), [Test report](../TEST_REPORT.md) |

## Authority hierarchy

```text
GitHub main code and tests
        ↓
TEST_REPORT.md + docs/status/implementation-manifest.json
        ↓
docs/STATUS.md + docs/IMPLEMENTATION_STATUS.md
        ↓
README and reviewer guides
        ↓
localized translations
        ↓
RFC, roadmap and research documents
```

When two documents disagree, prefer the higher surface and open a documentation
correction. Notion is the synchronized strategy and grant map; it does not
replace merged code as implementation truth.

## Core architecture and trust

- [Architecture](./ARCHITECTURE.md) — normative system boundaries and Ring Zero.
- [Implementation status](./IMPLEMENTATION_STATUS.md) — implemented, partial,
  RFC, vision and out-of-scope classification.
- [Read-only query boundary](./architecture/read-only-query-boundary.md) — HTTP,
  CLI and MCP search without durable mutation.
- [ADR-011: non-configurable TruthGate invariant](./adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md).
- [ADR-012: immutable TrustSnapshot](./adr/ADR-012-IMMUTABLE_TRUST_SNAPSHOT.md).
- [ADR-013: documentation status manifest](./adr/ADR-013-DOCUMENTATION_STATUS_MANIFEST.md).
- [Ring Zero mutation gate](./testing/RING_ZERO_MUTATION_GATE.md).
- [CanonicalView RFC](./CANONICAL_VIEW_RFC.md) — physical L3 versus strict Canon.

## Evidence, provenance and evaluation

- [Test report](../TEST_REPORT.md) — exact verified checkpoint and metrics.
- [Evaluation](./EVAL.md) — evaluation architecture and datasets.
- [Evaluation metrics](./EVALUATION_METRICS.md).
- [Failure modes](./FAILURE_MODES.md).
- [L3 retrieval scale benchmark](./benchmarks/L3_RETRIEVAL_SCALE.md).

## Grant and public-claim boundary

- [NLnet scope](./GRANT_NLNET_SCOPE.md).
- [Baseline versus funded delta](./grants/baseline-funded-delta-matrix.md).
- [Funding use plan](./grants/funding-use-plan.md).
- [Evaluation replay adoption decision](./grants/evaluation-replay-adoption.md).

The proposal is submitted and under review. These documents do not claim that
funding has been awarded.

## Current engineering backlog

The next recommended packages are intentionally separate from this documentation
hardening change:

1. **Contradiction decision contract** — typed `ContradictionReport`, explicit
   coexist/supersede/contextualize/review outcomes and no automatic winner based
   only on confidence.
2. **ESM transition specification** — one machine-checkable transition table and
   invariant checker shared by admission, review and reconciliation.
3. **Performance history** — scheduled fixed-runner retrieval benchmarks with
   historical JSON results, not unstable latency gates on shared PR runners.
4. **Advisory topic facets** — multi-label navigation metadata where
   `topic_score` is never truth, evidence quality or source authority.
5. **Role and multi-curator hardening** — authentication scopes, accountable
   review decisions and conflict-safe concurrent workflows.

## Translation policy

English code-facing documents are normative. Localized documents are maintained
reader surfaces and should link back to the authoritative English status and test
report. Translation freshness must not be inferred from file modification time
alone.
