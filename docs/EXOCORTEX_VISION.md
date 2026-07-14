# Velantrim ExoCortex — Long-Term Research Vision

> Status: `RESEARCH / DOCUMENTED_ONLY`
>
> Runtime change: none
>
> Canon write path: none
>
> Current product: [Velantrim Verifiable Memory](./PROJECT_IDENTITY.md)

## Purpose

Velantrim ExoCortex is the broader research vision behind Velantrim: a future, user-controlled cognitive extension that can preserve useful context, knowledge, provenance and continuity across different AI systems without treating unverified model output as truth.

The current repository does **not** claim to implement a complete exocortex. It provides a narrower engineering foundation: verifiable memory and provenance infrastructure, currently developed under the `Crystal` kernel codename.

## Research thesis

A useful long-term AI memory system should not merely store conversations. It should distinguish:

```text
information received
≠ information understood
≠ information verified
≠ information worth preserving
```

The long-term ExoCortex research direction therefore studies how information may move through controlled stages:

```text
episode
→ incomplete context
→ candidate interpretation
→ evidence and contradiction review
→ memory-worth decision
→ verified long-term memory
```

This is a research model, not a declaration that these stages all exist in the current runtime.

## Desired properties

A future ExoCortex should be:

- **user-controlled** — the user remains the authority over personal data and long-term continuity;
- **model-independent** — memory should not be locked to one LLM vendor;
- **provenance-first** — important claims should remain traceable to sources and evidence;
- **epistemically honest** — observations, user statements, hypotheses and verified facts should remain distinguishable;
- **local-first where practical** — private memory should not require a mandatory external cloud;
- **incremental** — the system should process new or changed information instead of repeatedly revalidating its entire history;
- **bounded** — background reasoning should operate under explicit compute, time and storage budgets;
- **reversible and auditable** — promotion, restriction, correction and erasure should leave verifiable operational records without retaining erased personal content as hidden copies;
- **non-coercive** — the system must not invent hidden user goals or construct sensitive profiles from isolated observations.

## Relationship to the current product

```text
Velantrim Verifiable Memory
        │
        ├── current public engineering product
        ├── Crystal memory kernel
        ├── provenance / evidence / receipts
        ├── epistemic and canonical-memory controls
        └── research foundation for future ExoCortex work

Velantrim ExoCortex
        │
        ├── long-term research direction
        ├── cross-model continuity
        ├── information incubation
        ├── bounded consolidation
        ├── user-reviewed personal context
        └── future cognitive-extension experiments
```

The relationship is one-way in the current release boundary:

```text
implemented and tested memory mechanisms
→ may support ExoCortex research

research concepts
→ do not become runtime truth without a separate RFC, implementation, tests and review
```

## Candidate research areas

### 1. Epistemic incubation

Study a temporary layer where incomplete or ambiguous information can remain without immediate promotion into durable canonical memory.

Candidate distinctions include:

- incomplete information;
- low-value information;
- repeated evidence;
- temporal updates;
- semantic duplicates;
- unresolved contradictions;
- candidate personal patterns.

### 2. Information-sensitive routing

Study routing decisions based on more than message length:

- risk;
- urgency;
- ambiguity;
- novelty;
- context sufficiency;
- memory impact;
- expected compute cost.

A short high-risk message may require deeper attention than a long routine log.

### 3. Bounded background consolidation

Study background processing that uses:

- debounce and coalescing;
- dirty-set propagation;
- exact and semantic deduplication;
- bounded batches;
- explicit LLM-call budgets;
- one controlled synthesis task rather than one task per message.

### 4. Memory-worth decisions

Truth, safety and long-term value are different questions.

A future memory-worth contract may combine existing mechanisms such as salience, source trust, evidence, privacy risk, temporal persistence and storage budget. It must not automatically modify truth confidence merely because a fact is frequently retrieved.

### 5. Agent-run memory

External AI agents may produce large intermediate logs. A future `AgentRun` capsule could preserve:

- task;
- agent identity;
- final result;
- artifacts;
- verification status;
- provenance receipt;
- reference to detailed logs.

Intermediate reasoning should not automatically become thousands of canonical facts.

### 6. Cross-model continuity

Study how a user may carry a controlled, inspectable memory layer across different AI models while preserving:

- source boundaries;
- privacy restrictions;
- user corrections;
- explicit consent;
- exportability;
- verifiable retrieval.

## Explicit non-goals

This research vision does not authorize or claim:

- consciousness, sentience or personhood;
- autonomous psychological profiling;
- hidden or latent goals assigned to the user;
- automatic confidence changes during retrieval;
- direct research-mode writes into canonical memory;
- deletion of raw evidence without an audited retention and erasure contract;
- automatic replacement of immutable operator-defined values;
- unrestricted autonomous tool execution;
- a biological simulation of the human brain;
- AGI implementation.

## Promotion discipline

A research concept may become part of the public runtime only through an explicit sequence:

```text
research note
→ RFC
→ threat model
→ measurable success criteria
→ isolated prototype
→ adversarial tests
→ implementation PR
→ independent review
→ documented runtime status
```

No research document is evidence that a capability is already implemented.

## Success criteria for the research direction

Progress should be measured through observable engineering metrics, for example:

- duplicate facts per request;
- internal checks per unique episode;
- background tasks spawned and coalesced;
- LLM calls per consolidation cycle;
- retrieval latency and context size;
- provenance completeness;
- wrong-memory promotion rate;
- user correction success;
- residual-data verification after erasure;
- memory usefulness under bounded compute.

Claims such as “human-like”, “ten times faster” or “complete personal understanding” require evidence and should not be used as unmeasured product promises.

## Summary

Velantrim ExoCortex remains the long-term vision: a user-controlled and verifiable cognitive extension built on disciplined memory rather than opaque accumulation.

Velantrim Verifiable Memory is the present product. Crystal is its current kernel codename. The research vision remains visible, but clearly separated from implementation truth.