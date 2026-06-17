# Backend Boundary

> Date: 2026-06-17
> Scope: storage/backend positioning for Crystal
> Status: docs-only. Backend support must be verified in code before runtime claims.

## Principle

Crystal should remain local-first and dependency-minimal by default.

```text
SQLite / local ledger first.
Embedded graph optional.
Graphiti / Neo4j optional research or advanced backend.
No backend other than the canonical store may promote truth by itself.
```

## Backend roles

| Backend / layer | Role | Crystal stance |
|---|---|---|
| SQLite | local operational ledger, facts, provenance, audit data | default / core-friendly |
| Kuzu or embedded graph | optional local graph traversal | optional, not mandatory |
| Neo4j / Graphiti | advanced temporal/semantic graph experiments | optional research / integration only |
| Vector index | candidate retrieval / similarity | not truth authority |
| NetworkX / graph lab | analysis / experiments | not truth authority |
| DuckDB / analytics | metrics and reports | not truth authority |

## Truth boundary

Backends store and retrieve data. They do not decide truth.

Truth promotion requires the Crystal admission path:

```text
claim -> evidence/source -> TruthGate/Guardian -> trace/receipt -> canonical status
```

## Graphiti boundary

Graphiti-style systems may inspire selected patterns such as temporal memory, rank fusion, batch graph fetch, or degraded trace handling.

Crystal must not make Graphiti, Neo4j, OpenAI, or cloud services mandatory for the public core.

## Public wording

Safe:

```text
Crystal is local-first and can support optional graph backends without changing its truth boundary.
```

Avoid unless implemented and required:

```text
Graphiti is Crystal's core truth store.
```
