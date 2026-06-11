# Funding Use Plan — Approx. €50,000 (NLnet Commons Fund)

## Application status

| Field | Value |
|---|---|
| Proposal framing | **Verifiable AI memory infrastructure for GDPR-compliant Europe** |
| Programme | NLnet **NGI0 Commons Fund** |
| Requested amount | approx. **€50,000** |
| Status | Submitted to NLnet for review |

> **This is a planning and transparency document.** It does not represent an
> approved budget unless and until a grant agreement or Memorandum of Understanding
> is signed with NLnet. The proposal has been submitted and is under review; this
> does not imply that funding has been awarded. Private correspondence details
> (internal application reference, review-timeline specifics) are intentionally
> kept out of this public repository.

For a first NGI0 Commons Fund proposal, **€50,000 is the upper boundary normally
allowed by the programme**. Larger follow-up funding may become possible only after
successful completion of earlier funded work and public delivery of the results;
the programme's lifetime maximum for a single third party is €500,000. NLnet pays
per **completed, independently verifiable milestone**, so every euro below is tied
to a concrete deliverable that can be checked against the public repository.

---

## What the funding converts

Velantrim already exists as a tested research-grade core: 838 passing tests, 100%
coverage, a standard-library runtime, a local L3 canonical graph, a type-aware
TruthGate, replayable provenance receipts, GDPR-relevant controls and a read-only
MCP server. See [REVIEWER_NOTES.md](../REVIEWER_NOTES.md) and
[GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md).

The grant converts this **research-grade core into a reproducible, deployable
open-source MVP**: something an external developer, institution or reviewer can
run, query over an API, audit, and extend — not just a test suite.

The work plan below maps directly onto the five work packages already defined in
[GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md) (WP1–WP5), plus the deployment and
accessibility work needed to make the core usable in practice.

---

## Milestone budget (deliverable-based)

Each milestone is a self-contained deliverable with a verifiable output in the
repository. The order reflects priority: if the awarded amount is smaller, the
later milestones are deferred (see *Partial funding* below).

| # | Milestone / deliverable | Maps to | Amount |
|---|---|---|---:|
| M1 | **Local-first deployable prototype.** Stabilise the local pipeline, packaged install, reproducible setup, import/export, documented run path. | WP5 | €9,000 |
| M2 | **FastAPI service layer.** Endpoints for ingest, retrieval, trace/evidence inspection and health/status; local deployment instructions; tests. | new | €8,000 |
| M3 | **Production-strength evidence spans + Receipt v2.** Span extraction during PDF/Markdown ingest, original-snippet retrieval, multi-source corroboration, receipt replay against stored spans. | WP1 | €8,000 |
| M4 | **Evaluation harness as a CI quality gate.** Curated fixtures, grounding score, contradiction P/R, regression gates so quality cannot silently drop. | WP3 | €5,000 |
| M5 | **Knowledge-base expansion.** Larger source-referenced, graph-ready fact corpus across scientific, practical, educational and civic domains; licence/provenance metadata. | WP2/WP4 | €7,000 |
| M6 | **Knowledge adapters.** PDF/YAML/RDF-Wikidata import paths with licence and source-metadata handling, default runtime kept dependency-free. | WP4 | €5,000 |
| M7 | **Multilingual access.** Localisation structure and interface/documentation support for major European languages and a path toward UN languages. | new | €4,000 |
| M8 | **Model-independence evaluation.** Comparative evaluation across several LLMs to demonstrate that correctness comes from structured memory, not from any single proprietary model. | WP3 | €3,000 |
| M9 | **Documentation, governance and onboarding.** Architecture diagram, demo walkthrough, contributor pathway, examples for reviewers and external users. | WP5 | €1,000 |
| | **Total** | | **€50,000** |

A limited part of the development and curation milestones (M1, M5, M9 in
particular) may be delivered with **part-time contractor or assistant support**
(documentation, data cleaning, localisation, issue triage, knowledge curation) to
reduce the risk of a single-maintainer bottleneck. NLnet permits subcontracting;
the deliverables remain the unit of payment.

---

## Why model/API access is part of the budget (M8)

Velantrim is **not** intended to depend on any single AI model. Milestone M8
funds comparative evaluation across multiple LLMs precisely to **prove
model-independence**: that correct answers come from structured, source-linked
memory rather than from one proprietary model's confidence.

External LLMs are treated as replaceable language interfaces. The truth layer
remains structured memory, graph-ready data, source references, metadata and
trace. This milestone is an evaluation deliverable (a comparison report), not a
recurring subscription cost.

---

## Partial funding plan

If the awarded amount is lower than €50,000, the scope is reduced proportionally.
Priority order:

1. M1 — local-first deployable prototype;
2. M3 — evidence spans and Receipt v2;
3. M2 — basic FastAPI interface;
4. M4 — evaluation as a CI gate;
5. M9 — documentation and onboarding;
6. M5 — a small but high-quality knowledge base;
7. M7 — initial multilingual support;
8. M6, M8 — adapters and broad model evaluation deferred to a later phase.

Mobile applications, cloud synchronisation and specialised model training are
**out of scope for this grant phase** and belong to potential future funding.

---

## Responsible data and privacy position

Velantrim is local-first and user-controlled by design. For any institutional or
workplace adaptation, the following are non-negotiable:

- users control their own memory data;
- sensitive data is not silently uploaded to third-party systems;
- institutional deployments require access control and explicit governance;
- organisational or personal data is handled with consent, a legal basis and
  transparency;
- audit logs support accountability without exposing unnecessary personal data;
- memory export and deletion are first-class features.

This project supports **knowledge and workflow assistance with consent and
GDPR-compliant governance** — not employee surveillance. Any deployment in
schools, research, public administration or healthcare-adjacent settings must be
designed around privacy, consent, auditability and the right to erasure.

---

## Expected public benefit

Velantrim contributes to the European digital commons by exploring a more
transparent approach to AI memory. The benefit is infrastructure, not another
chatbot:

- auditable AI memory;
- local-first knowledge systems;
- source-grounded retrieval;
- structured fact storage with provenance;
- multilingual access;
- offline knowledge resilience;
- safer human–AI collaboration;
- reduced dependence on opaque, cloud-only AI memory.

The broader aim is to help people, organisations and institutions work with AI
systems that remember through structured, inspectable, source-linked memory
rather than opaque conversation history alone.

---

## Honest-language commitment

This plan deliberately avoids overclaiming. Velantrim **reduces unsupported
factual promotion**, **requires traceable source metadata**, and **supports
auditable memory operations**. It does **not** claim to eliminate hallucination
entirely, nor to be a finished commercial platform. The deliverable of this grant
phase is a credible, testable, documented open-source MVP — a foundation for
future European funding, institutional pilots and public collaboration.

## GenAI disclosure

This document was drafted with AI assistance and reviewed by the maintainer. All
repository changes are traceable through commits, tests and source files.
