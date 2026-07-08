# OSS Verifiable Memory Landscape

Status: `RESEARCH_REFERENCE / ROADMAP`

This document records architectural patterns from the open-source AI memory, RAG, observability, and software-supply-chain ecosystems that are relevant to Velantrim Crystal.

It is not an implementation-status document. Nothing listed here should be described as shipped unless a dedicated PR, test report, and implementation status entry confirm it.

## Core finding

No single mature open-source project was identified that combines all of the following layers as first-class capabilities:

1. context-preserving retrieval;
2. temporal or epistemic memory state;
3. admission / validation before memory or answer use;
4. operational execution tracing;
5. cryptographic or tamper-evident receipts / attestations.

Existing projects are strong, but they are specialized. Velantrim Crystal's differentiation window is the disciplined integration of these layers into a local-first verifiable AI memory infrastructure.

## Borrowed architectural patterns

| Pattern | Reference family | Velantrim use | Status |
| --- | --- | --- | --- |
| Contextual Retrieval | Anthropic-style contextual headers | Improve chunk retrieval without making headers the source of truth | `ROADMAP` |
| Temporal Assertions | Graphiti / Zep-style temporal graphs | Assertions should know when they became valid, when they were superseded, and which episode/evidence produced them | `ROADMAP` |
| Admission Layer | Guardrails / Self-RAG-style validators and critique signals | TruthGate should decide what can enter memory, retrieval context, and final answers | `PARTIAL / ROADMAP` |
| Operational Tracing | Phoenix / Langfuse-style traces | Debug request -> retrieval -> rerank -> TruthGate -> answer paths | `ROADMAP` |
| Attestations / Receipts | in-toto / Rekor-style signed claims and transparency logs | Represent memory transitions and TruthGate verdicts as verifiable receipts | `ROADMAP` |
| Directed Forgetting / Decay | memory-decay and consolidation literature | Prevent memory rot by demoting stale, weak, redundant, or superseded assertions | `ROADMAP` |

## First-class objects to preserve

Velantrim should keep the following objects separate. Do not collapse them into one informal JSON blob.

```text
Chunk -> ContextHeader -> Assertion -> Evidence -> Receipt
```

### Chunk

A raw or normalized span from a document, message, import session, or event.

A chunk is retrieval material, not truth by itself.

### ContextHeader

A short, generated description of where the chunk fits inside the larger document or conversation.

Purpose: improve BM25 / embedding retrieval.

Boundary: it is not Canon and not an independent source of truth.

### Assertion

A candidate claim extracted from chunks, episodes, or user input.

Assertions should have status, scope, confidence, timestamps, and provenance.

### Evidence

The concrete support for an assertion: source reference, span, quote, import session, episode, and confidence metadata.

Rule: no evidence, no verified assertion.

### Receipt

A durable record of a memory transition or verdict.

Examples:

- assertion accepted;
- assertion rejected;
- assertion restricted;
- assertion erased;
- assertion superseded;
- TruthGate allowed a claim into an answer;
- TruthGate blocked a claim.

Receipts should be designed so they can later be serialized as attestation-like objects and optionally anchored in a tamper-evident log.

## Recommended integration sequence

1. Add Contextual Retrieval as an ingestion / retrieval booster, not as memory core.
2. Introduce temporal assertions with explicit validity and supersession metadata.
3. Strengthen TruthGate as a two-tier admission layer:
   - fast deterministic validators for ordinary paths;
   - slower evidence-aware checks for high-risk or ambiguous paths.
4. Define Receipt objects for assertion lifecycle transitions and TruthGate verdicts.
5. Add operational trace UX for debugging and replay.
6. Add directed forgetting / decay for stale, duplicate, weak, or superseded assertions.

## Reviewer-safe positioning

Use:

> Velantrim Crystal aims to integrate existing open-source patterns into a coherent local-first verifiable AI memory infrastructure.

Avoid:

> Velantrim is the only project in the world.

Avoid:

> Velantrim has implemented all of these layers.

Correct boundary:

> This document is a research and roadmap reference. Implementation truth remains GitHub `main`, `TEST_REPORT.md`, `docs/STATUS.md`, and `docs/IMPLEMENTATION_STATUS.md`.

## Practical meaning

The project should not compete as another generic memory SDK.

Velantrim Crystal should be framed as a trust layer for AI memory:

```text
Contextual Retrieval = better search
Temporal Assertions = better memory hygiene
TruthGate = better admission discipline
Receipts = better auditability
Tracing = better debugging
Decay = less memory rot
```

## Grant-safe summary

Velantrim Crystal targets the gap between fragmented open-source components and regulated real-world AI use. It does not replace RAG, vector databases, observability tools, or attestation standards. It can compose their patterns into a stricter memory lifecycle where AI systems can show what they used, why it was admitted, where it came from, and how the decision can be audited.
