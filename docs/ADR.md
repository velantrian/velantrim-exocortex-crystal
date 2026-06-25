# Architecture Decision Records

Concise records of the load-bearing architectural decisions of Velantrim
Exo-Cortex Crystal. Each ADR states context, the decision, and its
consequences. Statuses: **Accepted** (governs the current design) or
**Accepted / RFC-aligned** (governs a future layer that is documentation-only
today).

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

## ADR-007: TruthGate as a pure admission function

- **Status:** Accepted
- **Context:** Admission control and persistence are easy to conflate. If the
  verification boundary also performed writes, the decision logic and the
  canon-mutation logic would be entangled, making the boundary harder to audit
  and to reason about.
- **Decision:** TruthGate is an *admission / decision function*: it takes the
  evidence package and returns a decision plus a reason (`(passed, reason)`); it
  does not write to the database and does not mutate canon. Transitioning a fact
  into the Validated state and merging it into the L3 canon is performed by the
  caller (e.g. the pipeline, ingest, or the curator review path) only when
  admission passes. It is *not* a pure function of the evidence package alone:
  when `min_confidence` is omitted it reads the contextual threshold from
  `core/adaptation` (`adaptation.verification_threshold()`) and it reads
  `ENABLE_TRUTH_POLICY` at call time, so the same input can decide differently
  as that context changes. The curator force-override (ADR-004) remains the
  documented exception that can admit a gate-blocked fact, with an audited
  actor + reason.
- **Consequences:**
  - the verification decision has no canon/DB write side-effects, and is
    testable with the threshold and `ENABLE_TRUTH_POLICY` held fixed (it is not
    guaranteed replayable across changing threshold/env state);
  - every canon write is attributable to an explicit caller, not to the gate;
  - the gate can be invoked for dry-run / preview without risk of mutation;
  - this is an architectural boundary, not a concurrency guarantee — atomicity
    of the subsequent write remains the caller's responsibility.

## ADR-008: Append-only reconcile; caller decides

- **Status:** Accepted
- **Context:** Truth maintenance (deduplication, corroboration, conflict
  detection) must never silently overwrite or auto-reject canon. A heuristic
  that promotes or deprecates facts on its own would be unauditable.
- **Decision:** Reconcile's *detection* surface is append-only and advisory.
  `record_occurrence` records a frequency signal only — it is *not* treated as
  independent evidence and never changes confidence, truth_status, or the
  epistemic state. `find_conflicts` returns candidate matches for review, not
  verdicts. Reconcile also exposes *explicit, caller-invoked* truth-maintenance
  operations — `supersede()` and `contradict()` — which **do** transition
  epistemic state (`transition_esm`), sync the change into L3 (`_sync_l3` →
  `merge_fact`) and add graph edges. These are deliberate, never automatic: the
  decision to invoke them stays with the caller, pipeline, or human curator.
- **Consequences:**
  - repeated occurrences raise frequency, never truth or confidence;
  - corroboration that *does* raise confidence stays an explicit, separate
    `reinforce()` decision;
  - conflict signals are inputs to a decision, never the decision itself;
  - reason attribution is recorded for the *force-approve* and *reject* paths
    (`review.approve(force=True, …, reason=…)` and `review.reject(…, reason=…)`);
    a normal `review.approve()` records actor (and optional note/diagnosis) but
    **not** a reason, and `supersede()` / `contradict()` / `transition_esm()` do
    not take actor/reason at all — so attribution for those is the calling
    context's responsibility, not a guarantee of the function signature.

## ADR-009: Stdlib-only runtime core; optional lazy extras

- **Status:** Accepted
- **Context:** Dependency-free claims are easy to overstate. A precise boundary
  is needed between the core runtime (which must run locally with no external
  packages) and optional capabilities that legitimately require extras.
- **Decision:** The runtime core (memory, pipeline, ingest, TruthGate,
  reconcile, consolidation) is standard-library-only. Optional backends and
  capabilities are lazy and opt-in: the Neo4j backend is optional and is *not*
  in the default backend chain (the default chain falls back to embedded /
  SQLite / in-memory backends), and optional generators/adapters may require
  external extras. The whole repository is **not** claimed to be
  dependency-free.
- **Consequences:**
  - the default local-first runtime installs and runs without third-party
    packages;
  - Neo4j is imported lazily and raises a clear, actionable error only when it
    is explicitly selected and its driver is absent;
  - grant-facing wording must say *"runtime core is stdlib-only; optional
    extras such as Neo4j / generators / adapters may require external
    dependencies"* — never *"the entire repository is dependency-free"*;
  - optional extras extend the trust/dependency boundary and stay opt-in.

## ADR-010: Bio-named modules are engineering metaphors

- **Status:** Accepted
- **Context:** Several modules carry biologically or cognitively inspired names
  (e.g. neurogenesis, immune, neurocore, fractal, salience, adaptation). Such
  names can be misread as claims of biological or conscious implementation. This
  ADR extends [ADR-006](#adr-006-research-inspirations-are-non-normative).
- **Decision:** Bio/cognitive names are engineering metaphors, not biological
  implementation claims. They describe deterministic, auditable mechanisms over
  the existing canon; they do not assert brain-like, conscious, or
  neuroplastic runtime behavior. Disclaimers in code docstrings stay
  synchronized with [METAPHOR_VS_MECHANISM.md](./METAPHOR_VS_MECHANISM.md),
  which is the canonical mapping from metaphor to mechanism.
- **Consequences:**
  - no consciousness / brain / neuroplasticity overclaim in code, docs, or
    grant materials;
  - each metaphor-named module documents the concrete mechanism it implements;
  - [METAPHOR_VS_MECHANISM.md](./METAPHOR_VS_MECHANISM.md) and
    [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) remain the sources of
    truth for what is actually implemented;
  - adding or renaming a metaphor-named module requires updating the metaphor
    mapping in the same change.
