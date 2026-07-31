# Architecture Decision Records

Concise records of the load-bearing architectural decisions of Velantrim
Exo-Cortex Crystal. Each ADR states context, the decision, and its
consequences. Statuses: **Accepted** (governs the current design) or
**Accepted / RFC-aligned** (governs a future layer that is documentation-only
today).

Additional focused ADRs may live under [`docs/adr/`](./adr/), including
[ADR-011: Non-configurable TruthPolicy](./adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md).

---

## ADR-001: Separate Truth from Speech

- **Status:** Accepted
- **Context:** LLMs generate fluent text that may not be evidence-grounded;
  fluency is easily mistaken for verified truth.
- **Decision:** The LLM is a speech/synthesis layer only and cannot write
  directly to canon. The source of truth is the local, source-tracked memory
  plus provenance — never model confidence.
- **Consequences:**
  - requires TruthGate as the verification boundary;
  - requires TRACE for every confident factual answer;
  - requires FactsPack as the controlled evidence package for generation;
  - the system may abstain or downgrade confidence when evidence is missing.

## ADR-002: Canon is VERIFIED + TRACE-valid memory

- **Status:** Accepted
- **Context:** Raw memory/graph can contain hypotheses, user claims,
  subjective states, and unverified data — all of which are legitimate
  *memory* but not verified *truth*.
- **Decision:** Canon is not the whole graph; canon is the verified,
  trace-valid subset. The physical graph is a typed, multi-status memory
  space.
- **Consequences:**
  - the graph may store multi-status claims (`VERIFIED`, `USER_CLAIMED`,
    `UNVERIFIED`, `HYPOTHESIS`, `SUBJECTIVE`), each labelled as such;
  - only verified, trace-valid claims support confident factual answers;
  - review and curation remain necessary; nothing is silently upgraded.

## ADR-003: Local-first by default

- **Status:** Accepted
- **Context:** AI memory can contain sensitive personal data; mandatory cloud
  processing creates hidden data processors and undermines auditability.
- **Decision:** Crystal prioritizes local-first storage and user-owned memory.
  The default runtime has no telemetry and no outbound network requirement.
- **Consequences:**
  - supports digital sovereignty and offline operation;
  - any cloud/LLM-provider use must be explicit and optional (opt-in extends
    the trust boundary);
  - export, deletion, restriction and auditability remain GDPR-oriented
    design goals (not a certification claim).

## ADR-004: Human Curator for Canon Promotion

- **Status:** Accepted
- **Context:** Autonomous memory systems can drift or promote unsupported
  claims; silent automated promotion is unauditable.
- **Decision:** High-trust canon promotion requires evidence, TRACE, and
  human-curated policy boundaries. The only sanctioned exception to the
  automatic gate is the explicit, attributed, audited curator override in the
  review queue.
- **Consequences:**
  - slower canon growth;
  - higher trust per canonical fact;
  - better audit and grant posture (every override is an audit event with an
    explicit actor and reason).

## ADR-005: Future optimization must not weaken Ring Zero

- **Status:** Accepted / RFC-aligned
- **Context:** Harness Replay / meta-optimization
  ([RFC_HARNESS_REPLAY_OPTIMIZATION.md](./RFC_HARNESS_REPLAY_OPTIMIZATION.md),
  documentation-only today) may someday propose better harness
  configurations.
- **Decision:** Any future optimizer must be constrained by ContractGuard and
  cannot relax TruthGate, Guardian, or TRACE requirements. Optimization may
  suggest; only a human curator may promote.
- **Consequences:**
  - no autonomous self-modification;
  - candidate configurations require replay evaluation and human approval;
  - safety boundaries remain stable across all future optimization work.

## ADR-006: Research Inspirations are non-normative

- **Status:** Accepted
- **Context:** Velantrim is informed by memory science, cybernetics,
  human-computer augmentation, knowledge graphs, trustworthy-AI research, and
  biological inspiration patterns.
- **Decision:** Research inspirations may guide future architecture but do not
  define implementation status and do not imply brain-like, conscious, or
  biologically accurate runtime behavior.
- **Consequences:**
  - inspirations must be labeled *historical inspiration only*, *current
    architectural analogue*, or *future research direction*;
  - biological analogies cannot be used as proof of implementation;
  - grant-facing documents remain sober and implementation-grounded
    ([IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) stays the only
    source of implementation claims);
  - biologically inspired component names are documented as engineering
    metaphors in [METAPHOR_VS_MECHANISM.md](./METAPHOR_VS_MECHANISM.md).

## ADR-007: TruthGate as an admission / decision function

- **Status:** Accepted; environment-policy clause superseded by ADR-011
- **Context:** Admission control and persistence are easy to conflate. If the
  verification boundary also performed writes, the decision logic and the
  canon-mutation logic would be entangled, making the boundary harder to audit
  and reason about.
- **Decision:** TruthGate is an *admission / decision function*: it takes the
  evidence package and returns a decision plus a reason (`(passed, reason)`); it
  does not write to the database and does not mutate canon. Transitioning a fact
  into Validated and merging it into L3 is performed by the caller only when
  admission passes. It is not a pure function of the evidence package alone
  when `min_confidence` is omitted because it reads the contextual threshold
  from `core/adaptation`. However, the `LLM_OUTPUT` + `WORLD_FACT` rejection is
  fixed Ring Zero policy: ADR-011 removes the former `ENABLE_TRUTH_POLICY`
  environment dependency. The curator force-override (ADR-004) remains the
  documented, explicit governance exception; it does not change the gate's
  decision and must preserve the blocking reason.
- **Consequences:**
  - the verification decision has no canon/DB write side effects;
  - confidence-threshold decisions are testable with the threshold fixed;
  - process environment cannot disable the model-origin world-fact block;
  - every canon write is attributable to an explicit caller or audited curator
    action, not to an implicit gate write;
  - the gate can be invoked for dry-run/preview without mutation;
  - atomicity of the subsequent write remains the caller's responsibility.

## ADR-008: Append-only reconcile; caller decides

- **Status:** Accepted
- **Context:** Truth maintenance (deduplication, corroboration, conflict
  detection) must never silently overwrite or auto-reject canon. A heuristic
  that promotes or deprecates facts on its own would be unauditable.
- **Decision:** Reconcile's *detection* surface is append-only and advisory.
  `record_occurrence` records a frequency signal only — it is *not* treated as
  independent evidence and never changes confidence, truth_status, or the
  epistemic state. `find_conflicts` returns candidate matches for review, not
  verdicts. Reconcile also exposes explicit, caller-invoked truth-maintenance
  operations — `supersede()` and `contradict()` — which transition epistemic
  state, sync the change into L3 and add graph edges. The decision to invoke
  them stays with the caller or human curator.
- **Consequences:**
  - repeated occurrences raise frequency, never truth or confidence;
  - corroboration that raises confidence stays an explicit `reinforce()` decision;
  - conflict signals are inputs to a decision, never the decision itself;
  - reason attribution is recorded for force-approve and reject paths; calling
    context remains responsible where lower-level functions lack actor/reason.

## ADR-009: Stdlib-only runtime core; optional lazy extras

- **Status:** Accepted
- **Context:** Dependency-free claims are easy to overstate. A precise boundary
  is needed between the core runtime and optional capabilities requiring extras.
- **Decision:** The runtime core is standard-library-only. Optional backends and
  capabilities are lazy and opt-in: Neo4j is optional and not in the default
  backend chain; optional generators/adapters may require external extras. The
  whole repository is not claimed to be dependency-free.
- **Consequences:**
  - the default local-first runtime installs without third-party packages;
  - Neo4j imports lazily and errors clearly only when explicitly selected;
  - grant-facing wording says the runtime core is stdlib-only while optional
    extras may require dependencies;
  - optional extras extend the trust/dependency boundary and stay opt-in.

## ADR-010: Bio-named modules are engineering metaphors

- **Status:** Accepted
- **Context:** Several modules carry biologically or cognitively inspired names
  such as neurogenesis, immune, neurocore, fractal, salience and adaptation.
  These can be misread as biological or conscious implementation claims.
- **Decision:** Bio/cognitive names are engineering metaphors, not biological
  implementation claims. They describe deterministic, auditable mechanisms over
  existing memory and do not assert brain-like, conscious or neuroplastic
  runtime behavior. Disclaimers stay synchronized with
  [METAPHOR_VS_MECHANISM.md](./METAPHOR_VS_MECHANISM.md).
- **Consequences:**
  - no consciousness/brain/neuroplasticity overclaim in code, docs or grants;
  - each metaphor-named module documents its concrete mechanism;
  - `METAPHOR_VS_MECHANISM.md` and `IMPLEMENTATION_STATUS.md` remain sources of
    truth for implemented behavior;
  - adding or renaming a metaphor-named module requires updating the mapping.

## ADR-011: TruthPolicy is non-configurable Ring Zero policy

The focused accepted decision is maintained at
[`docs/adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md`](./adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md).
It supersedes only ADR-007's former environment-dependent policy clause; all
other ADR-007 admission/write separation remains in force.
