# Comparison — Velantrim Crystal and Other AI Memory Approaches

Velantrim Crystal is not a chatbot and not a generic RAG application. It is a
local-first, verifiable memory substrate that can sit underneath agents,
assistants, knowledge tools or offline applications.

The core distinction is:

```text
Vector memory optimises recall.
Velantrim Crystal optimises inspectable, source-aware, replayable memory.
```

## Summary table

| Approach | Main purpose | Typical strength | Typical weakness | Crystal's position |
|---|---|---|---|---|
| Long prompt / chat history | Short-term conversational continuity | Simple and immediate | Expensive, lossy, hard to audit, not durable | Crystal stores durable facts outside the prompt and retrieves compact evidence. |
| Vector-only RAG | Semantic retrieval over chunks | Good fuzzy search | Chunks are not truth; provenance and deletion can be weak | Crystal keeps typed facts, source status, epistemic state, trace and receipts. |
| Chatbot memory feature | Personalisation | Easy UX | Often opaque to the user and vendor-controlled | Crystal is local-first and inspectable by default. |
| MemGPT / Letta-style agent memory | Agent memory orchestration | Rich agent workflows | Memory semantics may be agent-centric and provider-dependent | Crystal is a lower-level verifiable memory core; agents can use it without owning the truth boundary. |
| Zep / Graphiti-style temporal memory | Temporal knowledge graphs for agents | Conversation/event memory and time-aware retrieval | Usually part of a larger service/framework boundary | Crystal is dependency-free by default and keeps canonical writes behind TruthGate. |
| Mem0-style memory layer | Application memory API | Fast integration | Abstraction can hide provenance and promotion semantics | Crystal exposes source, claim type, epistemic state and replayable receipts. |
| Offline wiki / Kiwix-style knowledge base | Offline human-readable knowledge | Robust local availability | Usually not machine-typed or claim-level auditable | Crystal stores machine-readable facts with evidence and trace. |

## What Crystal does differently

### 1. Memory is typed before it becomes canonical

Crystal separates:

- `WORLD_FACT`;
- `USER_EXPERIENCE`;
- `EMOTION`;
- `INTERPRETATION`;
- `OPINION`;
- `GOAL`;
- `PREFERENCE`.

It also records origin with `source_status` values such as `USER_REPORTED`,
`EXTERNAL`, `DERIVED`, `OBSERVED`, `LLM_OUTPUT` and `UNKNOWN`.

This prevents a common memory failure: treating a user's feeling, an LLM guess or
an external fact as the same kind of object.

### 2. The LLM is outside the truth boundary

An LLM may phrase an answer, but it is not the source of truth. Crystal's truth
boundary is the local graph, the facts, the source metadata, the evidence spans,
the trace and the receipt.

```text
LLM = language/interface layer
Graph = canonical memory
Trace = proof path
TruthGate = controlled entry into canon
```

### 3. Receipts make answers replayable

A memory system should support the question:

```text
What facts supported this answer, and are those facts still valid?
```

Crystal receipts are designed to detect drift when cited facts are changed,
restricted, erased or contradicted.

### 4. Local-first is the default, not an enterprise add-on

The default runtime path uses the Python standard library only, local SQLite/WAL
and no telemetry. Optional backends can be enabled deliberately, but the default
trust boundary is local.

### 5. GDPR-relevant operations are part of the memory model

Crystal includes technical support for:

- physical erasure;
- processing restriction;
- record of processing;
- audit log verification;
- opt-in encryption at rest;
- PII redaction.

This does not make an operator automatically legally compliant, but it gives the
operator concrete technical controls that many memory systems leave external.

## When Crystal is a good fit

Crystal is a good fit when the system needs:

- local/offline operation;
- verifiable provenance;
- durable memory outside the prompt;
- replayable answer grounding;
- inspectable claim/source metadata;
- separation between user statements, facts, opinions and LLM outputs;
- GDPR-relevant erasure and restriction paths;
- read-only agent access through MCP.

## When Crystal is not the right tool by itself

Crystal is not, by itself:

- a hosted multi-tenant SaaS product;
- an authentication and access-control platform;
- a full legal compliance package;
- a replacement for host security and backups;
- a general-purpose LLM or agent framework;
- a claim of consciousness, personhood or zero hallucinations.

For production multi-user deployments, Crystal should be placed behind a proper
application layer with authentication, authorisation, tenant isolation, backup
policy, host encryption and operational monitoring.

## Grant-facing takeaway

Most AI memory systems optimise for convenience or semantic recall. Crystal's
public-interest contribution is narrower and more infrastructural:

```text
Make AI memory local, source-aware, typed, replayable, erasable and harder to
silently corrupt.
```
