# NLnet Reviewer Q&A — Velantrim Crystal

Internal preparation for likely NGI0 Commons Fund second-round questions.
NLnet's published review weighs **technical excellence / feasibility (30%)**,
**relevance / impact / strategic potential (40%)** and **cost-effectiveness /
value for money (30%)**, with a pass bar above 5.0/7. The fund asks applicants to
be short and concrete — *what* and *how*, not *why* — and pays per completed,
independently verifiable milestone.

These answers are written to be accurate to the repository as it exists today.
Where something is a grant deliverable rather than existing code, it says so.
The detailed reviewer contract is maintained in
[baseline-funded-delta-matrix.md](./baseline-funded-delta-matrix.md).

---

### Q1. How is Velantrim different from RAG, vector stores, or chatbot memory?

Vector-only RAG and chatbot memory retrieve text by similarity and let the model
decide what is true. Velantrim inverts that: the **canonical graph is the source
of truth**, and every fact carries an epistemic state, a `claim_type`, a
`source_status` and a `truth_status` assigned by an audited **TruthGate** — not
by model confidence. Answers come with **replayable receipts** that can be
verified offline, without the LLM that produced them. The LLM is a replaceable
phrasing interface, not the truth layer. This is memory infrastructure with
provenance, not a similarity index.

### Q2. What is the concrete MVP for this funding phase?

A reproducible, deployable, local-first open-source MVP:

1. a stable local pipeline with documented setup, import and export;
2. a hardened **FastAPI service layer** (ingest / retrieve / trace inspection /
   health) — a baseline optional API already exists today (`pip install '.[api]'`,
   `velantrim-api`: token-guarded review endpoints + `/health`, a thin async
   wrapper over `core/aio.py`); M2 hardens and extends it into a documented,
   capability-gated and tested service layer;
3. production-strength source-span receipts (a baseline exists in
   `core/evidence.py` + Receipt v2);
4. an expanded evaluation harness with calibrated regression gates (a baseline CI
   gate already exists in `core/eval.py` + `scripts/eval_gate.py`);
5. a small, source-linked knowledge-base package;
6. initial multilingual readiness.

Not a commercial platform — a credible, testable foundation.

### Q3. What already works today, before any funding?

The open core is tested, not vapourware: **a fully passing test suite at 100%
coverage on a standard-library runtime** (current audited baseline in
`TEST_REPORT.md`). Implemented: L0/L1 memory and the 8-state epistemic
state machine; local L3 graph backends (`auto` → LadybugDB → SQLite → mock);
type-aware TruthGate and Guardian; source / source-status tracking; replayable
provenance receipts with sealed source-span evidence; a baseline evidence store
(`core/evidence.py`); a baseline evaluation harness (`core/eval.py`); external
ingestion for txt/md/json/jsonl/ndjson/csv; GDPR-relevant erasure, restriction,
record-of-processing and audit logging; opt-in encryption at rest; and a
read-only MCP server. The grant hardens, scales and deploys this; it does not
start it.

### Q4. Why is approximately €50,000 reasonable if much of the baseline exists?

€50,000 is the upper boundary normally allowed for a *first* NGI0 Commons Fund
proposal. The budget is split into nine independently verifiable milestones
(see [funding-use-plan.md](./funding-use-plan.md)), each mapped to a concrete
repository artifact and a euro amount.

The baseline is explicitly excluded from paid acceptance. Each milestone follows:

```text
baseline today + funded engineering delta = independently verifiable deliverable
```

The delta matrix states what is already implemented, what new work funding buys and
which public artifact proves completion. Core engineering carries most of the weight;
model/API evaluation and contractor support are deliberately small and bounded.
NLnet pays on milestone completion, so each euro is checkable against public commits,
tests, reports and release artifacts.

### Q5. Why are model/API costs in the budget if this is open infrastructure?

They fund **comparative evaluation to prove model-independence**, not dependence
on a proprietary provider: benchmarking retrieval under trace constraints,
multilingual robustness checks and adapter-compatibility testing across several
LLMs. The deliverable is a comparison report. The truth-bearing layer remains
structured memory, metadata, source references and trace — never a single
external model.

### Q6. How do you validate your claims rather than asserting them?

Through reproducible, inspectable outputs: regression tests for memory and
metadata behaviour; documented record formats and validation rules (the JSON
schemas in `schemas/`); a deterministic evaluation report (retrieval hit@k/MRR,
trace completeness, source-span coverage, contradiction precision/recall,
receipt-replay survival); and CI gates so quality cannot silently regress. We do
**not** claim to eliminate hallucination — the claim is *reduced unsupported
factual promotion* through structured, source-linked memory.

Each funded milestone adds its own acceptance evidence rather than relying on a
narrative progress report.

### Q7. What is the European / public-interest dimension?

Local-first by default (no mandatory cloud, no telemetry, no outbound calls),
AGPL-3.0 copyleft, data sovereignty and user-controlled memory, GDPR-relevant
controls (erasure, restriction, record-of-processing, audit), and a multilingual
access path for major European languages. The output is reusable open-source
infrastructure for the digital commons, not a single consumer app — suitable for
schools, libraries, archives, research groups and public-sector bodies that need
inspectable, sovereign memory.

For API and curator hardening, the project also maintains a non-certification
[EU service security readiness checklist](../security/eu-service-security-readiness.md)
covering secure design, deployment, continuity, operations and maintenance.

### Q8. How will you ensure sustainability beyond the grant?

This phase produces a reviewable, reusable MVP: open documentation, a modular
architecture with no provider lock-in, reproducible setup, and a contributor
pathway (CONTRIBUTING, GOVERNANCE, issue/PR templates). That is a credible basis
for community contribution and follow-on funding. The grant is positioned as a
first phase toward a reusable foundation, not the final funding for a finished
product.

### Q9. What if the awarded amount is lower than requested?

The plan is viable under partial funding. Priority order: (1) local-first
stabilisation; (2) metadata/trace/evidence validation; (3) hardened FastAPI layer
(extends the `.[api]` baseline); (4) evaluation expansion and regression quality;
(5) documentation; (6) a small knowledge-base package; (7) initial multilingual
support. Adapters, broad model evaluation, mobile apps, cloud sync and specialised
models are deferred to later phases.

The retained milestones keep their acceptance criteria; later milestones are removed
rather than redefining already implemented baseline work as a paid deliverable.

### Q10. What are the main risks and how are they controlled?

The chief risks are **scope creep**, **over-generalisation** and **baseline/deliverable
confusion**. They are controlled by deliberately constraining this phase to one core
problem — verifiable local-first AI memory — and three early use contexts: personal /
research knowledge workflows, educational / civic multilingual knowledge support,
and developer-facing local / FastAPI integration.

Medicine, finance, agriculture, public-administration deployments, mobile apps,
production multi-tenancy and a specialised model are explicitly **out of scope for
this phase** and belong to future, separately funded work. New cognitive or
neuromorphic research is also isolated from the funded MVP; for example, intrinsic-
noise consolidation is documented as research-only and cannot write to Canon or
change grant milestones.

---

## Scope discipline (the one-line positioning)

> Velantrim is an open-source, local-first, **verifiable AI memory
> infrastructure** that separates language generation from truth-bearing memory.
> LLMs speak; structured, source-linked memory decides what is true.

Three early use contexts for this phase — everything else is future work:

1. personal and research knowledge workflows;
2. educational and civic multilingual knowledge support;
3. developer-facing local / FastAPI integration.
