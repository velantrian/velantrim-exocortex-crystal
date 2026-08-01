# 📌 Velantrim Crystal — Current Status

> 🌐 🇬🇧 **English** · 🇷🇺 [Русский](../README.ru.md)

**Status date:** 2026-08-01  
**Verified runtime checkpoint:** `f91299c` (`f91299c44a1a1850fa516f3abb96c916326f7a8c`, merged PR #302)  
**Exact verification evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [implementation-manifest.json](./status/implementation-manifest.json)

## Authority rule

```text
GitHub Crystal main = implementation truth
TEST_REPORT + manifest = exact verified evidence
Notion Crystal Project Hub = synchronized strategy and grant map
Titan / Full ExoCortex = separate research track
```

## Current verified baseline

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Failed:      0
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 targeted Ring Zero mutants killed
CI:          9 permanent CI jobs
```

## Completed hardening sequence

1. 🔒 Unified read-only HTTP, CLI and MCP query boundary.
2. 🛡️ Non-configurable LLM-origin TruthGate invariant.
3. 🧩 Immutable `TrustSnapshot` reconciliation.
4. 🧬 Targeted Ring Zero mutation gate.
5. 📖 Detailed README, documentation map and drift-detection CI.
6. ⚖️ Typed contradiction reports and explicit curator dispositions.
7. 🧭 Machine-readable ESM specification derived from runtime transitions.
8. 📊 Scheduled/manual L3 performance history with comparable-run reporting.
9. 🔌 Public conflict-resolution CLI and authenticated FastAPI route.
10. 🏷️ Advisory multi-label topic facets with no truth or Canon authority.
11. 👥 Scoped curator roles/capabilities and process-local decision leases.
12. 🌐 Semantically aligned top-level READMEs in ten languages.

## Trust topology

```text
explicit ingest
→ pending L0/L1 state
→ Guardian
→ TruthGate
→ contradiction/restriction checks
→ physical L3 multi-status graph

public query/search
→ read-only retrieval
→ immutable TrustSnapshot
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ answer / bounded refusal / Receipt

unresolved contradiction
→ immutable ContradictionReport
→ authenticated actor + scoped role/capability check
→ process-local decision lease
→ explicit COEXIST / CONTEXTUALIZE / SUPERSEDE decision
→ audited canonical write path

topic navigation
→ advisory TopicFacet metadata
→ filtering/grouping only
→ never truth, evidence or Canon admission authority
```

Important invariants:

```text
Physical L3 ≠ strict Canon
retrieval score ≠ truth
confidence ≠ independent evidence
LLM output ≠ independent factual source
query ≠ ingest
contradiction ≠ automatic winner
topic score ≠ truth or admission permission
process-local lease ≠ distributed coordination guarantee
```

## Public conflict-resolution and curator surfaces

- CLI: `python -m core.conflict_surfaces ...`
- HTTP: `POST /review/resolve-conflict`
- Core authority: `core.review.resolve_conflict`
- Authorization helper: `core.curator_auth`
- Local coordination helper: `CuratorLeaseRegistry`

The HTTP helper requires host-provided authentication. Actor identity, role
capabilities and fact scopes fail closed. The included lease registry coordinates
only workers inside one process; distributed deployments must provide an
external lease adapter. See [CONFLICT_RESOLUTION_SURFACES.md](./CONFLICT_RESOLUTION_SURFACES.md)
and [TOPIC_FACETS_AND_CURATOR_IAM.md](./TOPIC_FACETS_AND_CURATOR_IAM.md).

## Advisory topic facets

`core.topic_facets` supports normalized multi-label metadata for navigation,
filtering and grouping. Facet score means topic relevance only. It cannot change
truth status, evidence, ESM state, contradiction decisions or strict Canon
membership.

## Remaining independent roadmap

The agreed hardening, contradiction, topic-facet and local curator-IAM packages
are complete. Remaining packages are independent future work:

- external/distributed decision-lease adapter;
- production identity-provider integration and multi-tenant policy;
- broader provenance lifecycle wiring;
- controlled-runner performance SLO policy;
- additional repository-wide mutation coverage;
- Titan cognitive integration as a separate research track.

## Public claim boundary

Crystal is local-first, source/state/provenance-oriented memory infrastructure
with explicit admission, strict read grounding, contradiction review, advisory
topic navigation, scoped curator authorization, TRACE and replayable Receipts.
It is not a universal truth oracle, hallucination-free system, legal/security
certification, production multi-tenant service, distributed locking system,
Titan, or an artificial-consciousness implementation.

## Reviewer path

1. [README](../README.md)
2. [Documentation map](./DOCUMENTATION_MAP.md)
3. [Quick start](./QUICKSTART.md)
4. [Read-only query boundary](./architecture/read-only-query-boundary.md)
5. [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md)
6. [Topic facets and curator IAM](./TOPIC_FACETS_AND_CURATOR_IAM.md)
7. [Test report](../TEST_REPORT.md)
8. [Implementation status](./IMPLEMENTATION_STATUS.md)
9. [Architecture](./ARCHITECTURE.md)
10. [Grant scope](./GRANT_NLNET_SCOPE.md)
