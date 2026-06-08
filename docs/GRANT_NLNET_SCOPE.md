# Velantrim Crystal — NLnet Grant Scope

## Summary

Velantrim Crystal is an AGPL-licensed, local-first, verifiable AI memory core. It
is designed for systems that need long-term memory without silently turning user
statements, model guesses or unverified claims into persistent truth.

The core stores memory as source-tracked facts with epistemic state,
`claim_type`, `source_status`, provenance traces and replayable receipts. It runs
locally by default, uses no mandatory cloud service and has a standard-library
runtime path.

## Problem

Modern AI systems often treat memory as an opaque vector store or a long prompt.
That creates several public-interest problems:

- users cannot reliably inspect where a remembered fact came from;
- subjective statements, model output and world facts can be mixed together;
- deletion and restriction are difficult to verify;
- external providers may become unavoidable data processors;
- local/offline operation is often not a first-class design goal;
- regulators and institutions cannot replay how an answer was grounded.

## Proposed solution

Velantrim Crystal provides a verifiable memory layer underneath AI systems:

```text
input / file / agent event
  → claim extraction and classification
  → Guardian + TruthGate
  → local L0/L1 working memory
  → local L3 canonical graph
  → retrieval / FactsPack
  → traceable answer / receipt
```

The LLM is optional. It may phrase the final answer, but correctness should come
from local retrieved facts, not from model confidence.

## Implemented today

The current open core already includes:

- L0/L1 memory and an epistemic state machine;
- local L3 graph backends (`auto` → LadybugDB → SQLite → mock);
- type-aware TruthGate and Guardian path;
- source and source-status tracking;
- replayable provenance receipts (Receipt v2 with sealed source-span evidence);
- a baseline source-span evidence store (`core/evidence.py`) — imported facts
  auto-attach their source, with content-light source/claim hashes;
- a baseline evaluation harness (`core/eval.py`) reporting retrieval/trace/receipt
  metrics;
- external knowledge ingestion for `.txt`, `.md`, `.json`, `.jsonl`, `.ndjson`,
  and `.csv`;
- GDPR-relevant erasure, restriction, record-of-processing and audit logging;
- opt-in encryption at rest for L1 personal-data fields;
- dependency-free read-only MCP server;
- 593 passing tests and ~99% coverage.

## Why this fits public-interest infrastructure

Crystal is relevant to European public-interest technology because it is:

- **local-first**: no mandatory cloud and no outbound network calls by default;
- **auditable**: facts carry source, state, trace and receipts;
- **privacy-preserving by design**: data remains under operator control;
- **open-source**: AGPL-licensed core;
- **institution-friendly**: suited to schools, universities, libraries, archives,
  public-sector bodies, research groups and regulated organisations;
- **LLM-independent**: useful even where an external AI provider is unavailable,
  expensive or inappropriate.

## Proposed funded work packages

### WP1 — Evidence Span Store and Receipt v2

A **baseline is already implemented** (`core/evidence.py` + Receipt v2): facts
carry `source_uri`/kind, chunk id, span offsets and content-light source/claim
hashes; imported facts auto-attach their source; receipts seal and replay that
evidence. The funded work extends this to production strength:

- automatic line/section/character span extraction during PDF/Markdown ingestion;
- original-snippet retrieval and side-by-side source display;
- multi-source corroboration and per-span conflict surfacing;
- receipt replay against exact stored source spans at scale.

**Outcome:** stronger claim-to-source auditability for research, education and
public-sector use.

### WP2 — Import Sessions and Dry-run Review

A **baseline is already implemented** (`core/imports.py`): a dry-run preview
(`learn --dry-run`) predicts accept/reinforce/block/conflict through the same
validators with zero writes; real imports carry a session id and can be
restricted or erased as a batch (`import-session` / `session-restrict` /
`session-erase`). The funded work extends this to institutional scale:

- resumable / chunked import summaries for large corpora;
- intra-batch duplicate and conflict consolidation in the preview;
- a curator review queue for `Observed`/quarantined items (the full L2 path);
- per-source licence and provenance metadata capture.

**Outcome:** safer corpus ingestion for institutions.

### WP3 — Evaluation Harness

A **baseline is already implemented** (`core/eval.py`, `velantrim eval`): a
deterministic report covering retrieval (hit@k / MRR), trace completeness,
metadata completeness, **source-span coverage**, **contradiction
precision/recall**, and receipt-replay survival. The funded work scales it to a
credible quality signal:

- curated fixture corpora and per-case `metrics.jsonl` / `eval_report.md`;
- grounding score for generated answers;
- CI regression gates so quality cannot silently drop between releases;
- broader contradiction and retrieval fixtures across domains.

**Outcome:** measurable quality instead of narrative-only claims.

### WP4 — Stronger Knowledge Adapters

Add optional adapters while keeping the default runtime dependency-free:

- PDF text extraction adapter;
- YAML adapter;
- RDF/Wikidata import path;
- license/source metadata handling.

**Outcome:** better fit for libraries, archives, research datasets and public
knowledge sources.

### WP5 — Documentation, Governance and Demonstrators

Improve public onboarding:

- architecture diagram;
- grant-facing demo walkthrough;
- issue and pull-request templates;
- comparison with vector-only memory systems;
- optional browser/PWA companion demo documentation.

**Outcome:** easier adoption by public-interest contributors and reviewers.

## Out of scope for this grant phase

- closed-source SaaS productisation;
- autonomous personality rewriting;
- claims of consciousness or artificial personhood;
- “zero hallucination” claims;
- mandatory dependence on a specific LLM provider;
- production multi-tenant hosting without a dedicated auth/security layer.

## Success criteria

A successful grant phase should produce:

- release-tagged open-source code;
- reproducible tests and evaluation reports;
- source-span receipts for imported knowledge;
- safe dry-run ingestion workflow;
- clear documentation for local/offline operation;
- governance and contributor pathway for public-interest maintenance.

## GenAI disclosure note

Project documentation and planning may use AI assistance for drafting, review and
comparison. Final repository changes are reviewed by the maintainer and should be
traceable through commits, tests and source files.
