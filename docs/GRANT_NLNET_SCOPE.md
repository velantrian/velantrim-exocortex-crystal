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
  and `.csv`, with optional adapters for `.yaml`, `.pdf` and RDF/Linked Data
  (`.ttl`/`.n3`/`.nt`/`.rdf`) that keep the runtime stdlib-only;
- a curator review queue (`core/review.py`) for `Observed`/quarantined items;
- GDPR-relevant erasure, restriction, record-of-processing and audit logging;
- opt-in encryption at rest for L1 personal-data fields;
- dependency-free read-only MCP server;
- 829 passing tests and 100% coverage (enforced by a 100% CI gate).

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

A **baseline is already implemented** (`core/imports.py` + `core/review.py`): a
dry-run preview (`learn --dry-run`) predicts accept/reinforce/block/conflict
through the same validators with zero writes; real imports carry a session id and
can be restricted or erased as a batch (`import-session` / `session-restrict` /
`session-erase`). A **curator review queue** (`review-queue` / `review-item` /
`review-approve` / `review-reject`) now surfaces every `Observed`/quarantined
item that did not reach the canon, re-runs the gates to explain *why* it is
pending, and lets a librarian approve (promote to canon — with an explicit,
audited override for still-blocked items) or reject it; every decision is sealed
in the tamper-evident audit chain. A **baseline web review UI is also already
delivered**: a static, dependency-free Kanban board (`core/_webui/review.html`)
served by the optional HTTP API over the same audited queue operations, with a
token guard on every review endpoint. The funded work extends this to
institutional scale:

- resumable / chunked import summaries for large corpora;
- intra-batch duplicate and conflict consolidation in the preview;
- institutional hardening of the review UI: role-based curator permissions,
  multi-curator workflows, operator guidance, accessibility and
  deployment/security hardening;
- per-source licence and provenance metadata capture.

**Outcome:** safer corpus ingestion for institutions.

### WP3 — Evaluation Harness

A **baseline is already implemented** (`core/eval.py`, `velantrim eval`): a
deterministic report covering retrieval (hit@k / MRR), trace completeness,
metadata completeness, **source-span coverage**, **contradiction
precision/recall**, and receipt-replay survival. It now runs over a **curated,
multi-domain fixture corpus** (16 retrieval cases with ranking distractors, 12
labelled contradiction pairs including hard negatives), emits per-case
`metrics.jsonl` + `eval_report.md`, and is enforced by a **CI quality gate**
(`scripts/eval_gate.py`, `velantrim eval --gate`) so retrieval/grounding/
contradiction quality cannot silently regress. The harness also ships a
**report-only Russian corpus** (typo/morphology probes) and an **opt-in
character-trigram embedder** for morphology-tolerant retrieval — the English
gate remains the only CI-enforced threshold. The funded work scales this to a
credible quality signal:

- larger curated corpora across many more domains and European languages,
  promoted from report-only to gated once thresholds are calibrated;
- grounding score for generated answers;
- broader contradiction and retrieval fixtures, with adversarial cases;
- per-release tracking and published quality trend reports.

**Outcome:** measurable quality instead of narrative-only claims.

### WP4 — Stronger Knowledge Adapters

A **baseline is already implemented** (`core/adapters/`): self-registering,
optional adapters extend `velantrim learn` to PDF (`pypdf`), YAML (`PyYAML`) and
RDF/Linked Data (`rdflib`: `.ttl`/`.n3`/`.nt`/`.rdf`) while the default runtime
stays stdlib-only — a missing adapter dependency raises a clear install hint
rather than failing the core. Every adapted claim still flows through the same
Guardian → TruthGate path. The funded work hardens this for real collections:

- automatic source-span offsets during PDF/Markdown extraction (feeds WP1);
- a full RDF/Wikidata import path with Q-/P-code label resolution;
- license/source metadata capture per adapted source;
- adapters for further institutional formats (e.g. EPUB, BibTeX, OAI-PMH).

**Outcome:** better fit for libraries, archives, research datasets and public
knowledge sources.

### WP5 — Documentation, Governance and Demonstrators

A **baseline is already implemented**: an architecture diagram set
(`docs/ARCHITECTURE.md`), a vector-only comparison (`docs/COMPARISON.md`) and a
hands-on, reproducible CLI demo walkthrough with real captured output
(`docs/DEMO.md`). The funded work extends public onboarding:

- richer architecture diagrams (sequence + deployment views);
- expanded grant-facing demo walkthrough and screencast;
- issue and pull-request templates;
- deeper comparison with vector-only memory systems;
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
