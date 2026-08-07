# Architecture Decision Records

Concise records of the load-bearing architectural decisions of Velantrim
Exo-Cortex Crystal. Each ADR states context, the decision and consequences.

Statuses:

- **Accepted** — governs the current implementation or documentation contract.
- **Accepted / RFC-aligned** — constrains future work that is not yet runtime.
- **Superseded in part** — remains valid except for an explicitly replaced clause.

## Focused ADR index

| ADR | Decision | Status |
|---|---|---|
| [ADR-011](./adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md) | LLM-origin world-fact rejection is non-configurable Ring Zero policy | Accepted |
| [ADR-012](./adr/ADR-012-IMMUTABLE_TRUST_SNAPSHOT.md) | read-time L3/L1 trust reconciliation uses an immutable snapshot | Accepted baseline |
| [ADR-013](./adr/ADR-013-DOCUMENTATION_STATUS_MANIFEST.md) | active implementation claims use a machine-checkable status manifest | Accepted baseline |
| [ADR-014](./adr/ADR-014-EXPLICIT_CONTRADICTION_DECISIONS.md) | a current contradiction requires an explicit, report-bound curator disposition | Accepted baseline |
| [ADR-015](./adr/ADR-015-ESM_MACHINE_SPEC.md) | one machine-readable ESM descriptor is derived from the runtime matrix | Accepted baseline |
| [ADR-016](./adr/ADR-016-INFORMATIONAL_BENCHMARK_HISTORY.md) | hosted-runner retrieval history is scheduled, versioned and informational | Accepted baseline |
| [ADR-017](./adr/ADR-017-CRASH_CONSISTENT_CURATOR_DECISIONS.md) | curator state, audit proof and durable L3 projection intent share one SQLite transaction | Accepted |
| [ADR-018](./adr/ADR-018-AUTHENTICATED_CURATOR_WRITE_COMPOSITION.md) | bundled curator writes derive identity and authorization from a validated principal | Accepted |
| [ADR-019](./adr/ADR-019-BOUNDED_LEGACY_RETRIEVAL.md) | degraded legacy retrieval is bounded and explicit reindex is separate | Accepted |
| [ADR-020](./adr/ADR-020-SQLITE-STORAGE-LIFECYCLE.md) | SQLite backup, verification, inactive restore and guarded lock recovery are explicit operator operations | Accepted |
| [ADR-021](./adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md) | backend changes require phased logical migration and explicit cutover proof | Accepted architecture contract |

---

## ADR-001: Separate Truth Authority from Speech

- **Status:** Accepted
- **Context:** A generator can produce fluent unsupported text; fluency is easily
  confused with evidence.
- **Decision:** A model or generator may extract, classify, compare, summarize or
  phrase information, but it has no direct authority to write its own output as
  verified Canon. Source-tracked memory and policy determine grounding authority.
- **Consequences:**
  - TruthGate controls automatic admission;
  - confident factual answers require strict CanonicalView grounding;
  - TRACE and Receipt expose the support path;
  - the system may abstain when grounding is insufficient.

## ADR-002: Physical L3 is not strict Canon

- **Status:** Accepted
- **Context:** Graph memory can legitimately contain hypotheses, user claims,
  subjective states, unverified data and invalidated historical records.
- **Decision:** The physical graph is typed multi-status memory. Strict Canon is
  the policy-allowed projection satisfying exact truth-status, ESM, provenance,
  confidence and processing-restriction requirements.
- **Consequences:**
  - graph membership never implies verified truth;
  - non-verified material remains labelled;
  - nothing is silently upgraded by retrieval score or confidence;
  - review and curation remain explicit.

## ADR-003: Local-first by default

- **Status:** Accepted
- **Context:** AI memory can contain sensitive personal or institutional data.
  Mandatory cloud processing introduces hidden processors and weakens control.
- **Decision:** Crystal prioritizes local storage and user-owned memory. The
  default runtime has no mandatory telemetry, cloud, LLM or network provider.
- **Consequences:**
  - supports offline use and digital sovereignty;
  - optional external providers extend the trust boundary and require opt-in;
  - erasure, restriction and auditability remain GDPR-relevant engineering
    goals, not certification claims.

## ADR-004: Human accountability for curator override

- **Status:** Accepted
- **Context:** Unsupported claims must not be silently promoted by autonomous
  heuristics.
- **Decision:** The documented exception to automatic gate policy is an explicit,
  attributed and audited curator override in the review path.
- **Consequences:**
  - every override requires an actor and reason;
  - the original blocking reason remains observable;
  - high-trust memory grows more slowly but remains accountable.

## ADR-005: Future optimization must not weaken Ring Zero

- **Status:** Accepted / RFC-aligned
- **Context:** Future replay or optimization systems may propose configuration or
  workflow changes.
- **Decision:** An optimizer may suggest candidates but cannot relax TruthGate,
  Guardian, CanonicalView, restriction or TRACE/Receipt invariants.
- **Consequences:**
  - no autonomous trust-policy weakening;
  - candidate changes require deterministic evaluation and human approval;
  - optimization remains outside direct Canon authority.

## ADR-006: Research inspirations are non-normative

- **Status:** Accepted
- **Context:** The project uses concepts from memory science, cybernetics,
  knowledge graphs and biological inspiration.
- **Decision:** Inspiration does not define implementation status and does not
  imply a conscious, brain-like or biologically accurate runtime.
- **Consequences:**
  - inspirations are labelled as history, analogue or future research;
  - biological names are engineering metaphors;
  - [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) governs current
    capability claims.

## ADR-007: TruthGate is an admission decision function

- **Status:** Accepted; environment-policy clause superseded by ADR-011
- **Context:** Decision logic and persistence are easier to audit when separated.
- **Decision:** TruthGate returns a decision and reason; it does not itself write
  Canon. The caller performs an allowed transition/write only after approval.
  Contextual confidence thresholds may still be supplied/read as documented, but
  the LLM-origin world-fact rejection cannot be disabled by process environment.
- **Consequences:**
  - gate evaluation has no Canon write side effect;
  - dry-run/preview is possible;
  - subsequent write atomicity remains the caller's responsibility;
  - ADR-011 supersedes only the former configurable policy clause.

## ADR-008: Reconcile detects; an accountable caller decides

- **Status:** Accepted
- **Context:** Deduplication, occurrence tracking and contradiction detection must
  not silently overwrite or auto-reject memory.
- **Decision:** Detection surfaces are advisory. Exact repeated occurrence records
  frequency metadata only. Explicit truth-maintenance operations require a caller
  or curator decision.
- **Consequences:**
  - frequency does not increase truth or confidence;
  - conflict signals are inputs, not verdicts;
  - reason/actor attribution is required where a decision changes state.

## ADR-009: Stdlib-only runtime core; optional lazy extras

- **Status:** Accepted
- **Context:** Dependency-free claims must distinguish runtime core from the full
  development and adapter ecosystem.
- **Decision:** The default runtime core is standard-library-only. Optional
  adapters, APIs, generators and backends remain lazy and opt-in.
- **Consequences:**
  - basic local runtime installs without third-party dependencies;
  - optional features fail clearly when selected without their extras;
  - the repository as a whole is not described as dependency-free.

## ADR-010: Bio-named modules are engineering metaphors

- **Status:** Accepted
- **Context:** Names such as immune, neurocore, fractal or neurogenesis can be
  mistaken for biological implementation claims.
- **Decision:** Such names describe deterministic software mechanisms, not brain,
  consciousness or neuroplasticity equivalence.
- **Consequences:**
  - every metaphor-named component documents its concrete mechanism;
  - [METAPHOR_VS_MECHANISM.md](./METAPHOR_VS_MECHANISM.md) remains the mapping;
  - documentation and grant material avoid biological overclaim.

## ADR-011: TruthPolicy is non-configurable Ring Zero policy

See [ADR-011](./adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md).

## ADR-012: Immutable TrustSnapshot at the read boundary

See [ADR-012](./adr/ADR-012-IMMUTABLE_TRUST_SNAPSHOT.md).

## ADR-013: Machine-checkable documentation status

See [ADR-013](./adr/ADR-013-DOCUMENTATION_STATUS_MANIFEST.md).

## ADR-014: Explicit contradiction decisions

See [ADR-014](./adr/ADR-014-EXPLICIT_CONTRADICTION_DECISIONS.md).

## ADR-015: ESM machine specification

See [ADR-015](./adr/ADR-015-ESM_MACHINE_SPEC.md).

## ADR-016: Informational benchmark history

See [ADR-016](./adr/ADR-016-INFORMATIONAL_BENCHMARK_HISTORY.md).

## ADR-017: Crash-consistent curator decisions

See [ADR-017](./adr/ADR-017-CRASH_CONSISTENT_CURATOR_DECISIONS.md).

## ADR-018: Authenticated curator write composition

See [ADR-018](./adr/ADR-018-AUTHENTICATED_CURATOR_WRITE_COMPOSITION.md).

## ADR-019: Bounded legacy retrieval

See [ADR-019](./adr/ADR-019-BOUNDED_LEGACY_RETRIEVAL.md).

## ADR-020: SQLite storage lifecycle

See [ADR-020](./adr/ADR-020-SQLITE-STORAGE-LIFECYCLE.md).

## ADR-021: Explicit cross-backend migration contract

See [ADR-021](./adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md).
