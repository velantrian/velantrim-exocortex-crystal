# README Branding Proposal

> Status: documentation proposal
>
> Runtime change: none
>
> The repository owner will apply the final repository-name change manually.

## Proposed opening

Replace the current public heading and introductory identity block with:

```markdown
# 🔱 Velantrim Verifiable Memory

### *Verifiable long-term memory and provenance infrastructure for AI agents*

`v0.3.0` · 🧪 **1685 tests** · 🎯 **100% coverage** · 🐍 **pure-stdlib runtime** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Velantrim Verifiable Memory is **not another chatbot**. It is a local-first,
> verifiable memory and provenance layer that AI systems can write to and read
> from under explicit epistemic and canonical-memory controls.
>
> **Crystal** is the codename of the current memory kernel and `0.x` release line.
> **Velantrim ExoCortex** is the broader long-term research vision, not a claim
> about the current runtime.
```

## Scope paragraph

Recommended repository-boundary wording:

```markdown
> 📦 **Scope of this repository.** This repository contains the verified,
> dependency-free open core: the Crystal memory kernel, provenance and receipt
> mechanisms, GDPR-relevant controls, graph adapters, ingestion paths, read-only
> MCP integration and tested memory layers. Research directions are documented
> separately and are not runtime claims unless implemented, tested and listed in
> the current status documents.
```

## Naming rules inside the README

Use:

- `Velantrim Verifiable Memory` when introducing the product;
- `Crystal` when discussing the kernel, runtime or release line;
- `Velantrim ExoCortex` only for the broader research vision;
- `Velantrim` when referring to the wider project ecosystem.

Do not perform a blind replacement of every occurrence of `Crystal`. Existing technical references such as “Crystal runtime”, “Crystal release line” and “Crystal public core” remain meaningful.

## Recommended documentation entry

Add this row to the documentation table:

```markdown
| **[docs/PROJECT_IDENTITY.md](./docs/PROJECT_IDENTITY.md)** | Canonical product name, Crystal kernel codename and ExoCortex research boundary |
| **[docs/EXOCORTEX_VISION.md](./docs/EXOCORTEX_VISION.md)** | Long-term research vision and explicit non-goals |
| **[docs/REBRANDING_CHECKLIST.md](./docs/REBRANDING_CHECKLIST.md)** | Safe manual repository rename and compatibility checklist |
```

## Recommended transition note

For one release cycle after the repository rename:

```markdown
> Formerly published as **Velantrim ExoCortex — Crystal**. The public product is
> now presented as **Velantrim Verifiable Memory**; Crystal remains the kernel
> codename and ExoCortex remains the long-term research vision.
```

## What this proposal does not change

- package name;
- CLI commands;
- environment variables;
- import paths;
- database schema;
- licence;
- runtime behaviour;
- implementation maturity;
- test or coverage claims.

The final README edit should be reviewed against the current `main` immediately before application so that newer test baselines or status changes are not overwritten.