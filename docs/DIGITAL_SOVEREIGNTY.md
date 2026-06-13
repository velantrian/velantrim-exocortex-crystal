# Digital Sovereignty

Velantrim Crystal is designed as a local-first memory core for AI systems.

## Core idea

The owner of the system should control where memory is stored, when it is exported and whether any external AI service is used.

## Defaults

- no mandatory cloud service
- no telemetry by default
- no outbound network calls by default
- local storage by default
- optional operator-controlled export and sync
- optional LLM use for phrasing or interface quality

## Why this matters

AI memory can become sensitive infrastructure. If long-term memory is stored only inside external cloud systems, users and organisations lose control over continuity, auditability and data location.

Velantrim separates the memory core from the language model. The graph and provenance layer remain local; an LLM may be used only as an optional interface.

## European relevance

This supports:

- privacy by design
- auditable AI workflows
- reduced dependence on closed AI platforms
- public-sector and institutional self-hosting
- user-controlled data export and deletion

## Efficient AI: reducing unnecessary LLM work

Velantrim is designed to reduce unnecessary repeated LLM work by reusing local
structured memory, graph relations, FactsPack evidence and TRACE paths before
invoking external language models.

When a query can be answered from the local verified canon — without an LLM call
— no tokens are sent to an external service. This is a design property, not a
performance guarantee.

Future evaluation should measure:

| Metric | Description |
|---|---|
| `llm_calls_avoided_per_query` | Queries answered from local memory without LLM invocation |
| `tokens_saved_per_answer` | Estimated tokens not sent because local retrieval succeeded |
| `cpu_only_retrieval_success_rate` | Share of queries resolved by local graph retrieval alone |
| `trace_reuse_rate` | Share of answers that reused an existing TRACE path |
| `facts_pack_reuse_rate` | Share of answers built from a cached FactsPack |
| `local_data_retention_ratio` | Share of data that never left the local device |

These metrics are targets for future evaluation harness extensions, not current
claims. No guaranteed energy savings, GPU elimination, or LLM replacement is
implied.

## Boundary

This document does not claim absolute security or automatic legal compliance. It defines the project direction: local-first, auditable and operator-controlled AI memory.
