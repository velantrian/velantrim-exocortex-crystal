# Velantrim Verifiable Memory — Project Identity

> Status: public naming and scope contract
>
> Runtime change: none
>
> Package/repository rename: intentionally out of scope for this document

## Canonical public identity

**Public product name:** **Velantrim Verifiable Memory**

**Public descriptor:**

> Verifiable long-term memory and provenance infrastructure for AI agents.

The descriptor should accompany the product name in reviewer-facing, community-facing and grant-facing contexts until the function of the project is widely understood.

## Naming hierarchy

```text
Velantrim
├── Velantrim Verifiable Memory — the current public open-source product
├── Crystal — the codename of the current memory kernel and release line
└── Velantrim ExoCortex — the broader long-term research vision
```

### Velantrim

`Velantrim` is the wider project and research identity.

### Velantrim Verifiable Memory

`Velantrim Verifiable Memory` is the clear public name for the software delivered by this repository. It describes the implemented engineering focus:

- local-first long-term memory for AI systems;
- provenance and source metadata;
- explicit epistemic state;
- controlled admission through TruthGate where implemented;
- traceable retrieval and replayable receipts;
- privacy, restriction and erasure controls;
- model-independent memory infrastructure.

This name should be used in the first heading, repository description, external posts, grant summaries and technical introductions.

### Crystal

`Crystal` remains the codename of the current memory kernel and `0.x` release line.

It may be used in technical phrases such as:

- Crystal kernel;
- Crystal runtime;
- Crystal release line;
- Crystal compatibility;
- Crystal implementation boundary.

It should not be used alone in a first introduction where a new reader would not know what the project does.

Recommended form:

> Velantrim Verifiable Memory, powered by the Crystal memory kernel.

### Velantrim ExoCortex

`Velantrim ExoCortex` is the broader research direction: a future, user-controlled cognitive extension that may preserve useful context, knowledge and continuity across AI systems.

It is **not** a claim that this repository currently implements a complete exocortex, autonomous mind, consciousness, biological cognition or AGI.

The research boundary is defined in [`EXOCORTEX_VISION.md`](./EXOCORTEX_VISION.md).

## Current implementation boundary

The repository may describe itself as:

> A verifiable, local-first, open-source memory and provenance layer for AI systems.

The repository must not imply that the following are current production capabilities unless separately implemented, tested and documented:

- a complete personal exocortex;
- autonomous hidden goals;
- consciousness or sentience;
- a biological brain simulation;
- automatic truth from LLM output;
- a production-ready multi-user cloud service;
- perfect hallucination prevention;
- complete personal profiling from isolated observations.

## Recommended presentation

### GitHub heading

```text
Velantrim Verifiable Memory
```

### Subtitle

```text
Verifiable long-term memory and provenance infrastructure for AI agents.
```

### Short description

```text
Local-first, verifiable memory and provenance infrastructure for long-running AI agents.
```

### One-paragraph introduction

> Velantrim Verifiable Memory is an open-source, local-first memory and provenance layer for AI agents. The current Crystal kernel stores facts with source metadata and epistemic state, supports controlled promotion into canonical memory, and provides traceable retrieval and replayable receipts. Velantrim ExoCortex is the broader research vision, not a claim about the current runtime.

## Compatibility policy

A public branding change does not require an immediate breaking rename of:

- the Python package;
- CLI commands;
- environment variables;
- database schemas;
- import paths;
- Docker images;
- existing repository URLs.

Those technical identifiers should be changed only through a separate compatibility plan and release decision.

## Naming rule for future documents

Every new public document should make the hierarchy visible at least once:

```text
Velantrim Verifiable Memory = current product
Crystal = current kernel codename
ExoCortex = long-term research vision
```

This separation preserves the original vision while making the present engineering purpose immediately understandable.