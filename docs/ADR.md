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
    source of implementation claims).
