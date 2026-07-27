# Grant Baseline → Funded Delta → Acceptance Matrix

**Status:** grant-planning control · documentation only · no new runtime claim  
**Scope:** NLnet / NGI0 Commons proposal, approximately €50,000  
**Source of implementation truth:** current GitHub `main`, `TEST_REPORT.md`, `docs/STATUS.md`, reproducible CI artifacts

## Purpose

Crystal already has a substantial tested baseline. The grant does not pay to recreate
features that already exist. It funds a measurable conversion from a research-grade
open core into a reproducible, deployable and institution-ready open-source MVP.

Every milestone must be read as:

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

A baseline capability may be reused as the starting point, but it is not itself a
funded deliverable. If the baseline advances before a grant agreement is signed, this
matrix must be updated so that funded work remains a real delta.

## Milestone matrix

| Milestone | Baseline today | Funded delta | Acceptance evidence |
|---|---|---|---|
| **M1 — Local-first deployable prototype (€9,000)** | Packaged Python install, CLI, local SQLite/WAL operational store, local L3 backends, Docker build gate, reproducible test instructions. | Stabilised release packaging; clean-clone setup; documented import/export, backup/restore and local deployment path; release-grade configuration validation and upgrade guidance. | Release tag; clean-clone smoke script; documented install/run/backup/restore walkthrough; tests that start from an empty environment; reproducible build evidence. |
| **M2 — Hardened FastAPI service (€8,000)** | Optional `.[api]` layer with health, ingest, ask, receipt verification, evidence access and token-guarded review endpoints. | Capability-based authorization; explicit reader/ingester/curator/auditor boundaries; token lifecycle and revocation; request/rate limits; secure deployment profile; operational audit export; failure-safe API behaviour. | Role-matrix integration tests; denied-by-default tests; token rotation/revocation tests; threat model; hardened local deployment guide; redacted audit/incident export fixture. |
| **M3 — Production-strength evidence spans and Receipt v2 (€8,000)** | Baseline evidence store and sealed receipts with source identifiers, chunk references, span fields and content-light hashes. | Automatic line/section/character spans for PDF and Markdown; original-snippet retrieval; multi-source corroboration; per-span conflict surfacing; replay at realistic corpus scale. | Exact-span fixture corpus; tamper and replay tests; side-by-side source demonstration; multi-source conflict cases; published evaluation artifact. |
| **M4 — Evaluation quality gate (€5,000)** | Deterministic retrieval/trace/receipt evaluation, source-span coverage, contradiction precision/recall and an English CI gate; report-only Russian probes. | Larger multi-domain fixtures; calibrated multilingual tracks; generated-answer grounding score; adversarial retrieval and contradiction cases; per-release quality trends. | Public fixtures and labels; threshold configuration; CI regression tests; release-versioned `metrics.jsonl` and report; documented calibration method. |
| **M5 — Knowledge-base expansion (€7,000)** | Draft knowledge material exists outside the audited Crystal release boundary and is not automatically canonical. | Curated, versioned, source-referenced corpus package with licence/provenance metadata, deduplication, validation and review-safe import workflow. | Corpus manifest; source and licence records; schema/integrity checks; dry-run import report; sample receipts; proof that corpus content is not promoted by bypassing TruthGate. |
| **M6 — Knowledge adapters (€5,000)** | Optional PDF, YAML and RDF/Linked Data adapters; default runtime remains standard-library only. | Production hardening; precise source spans; licence metadata; Wikidata Q/P label resolution; selected institutional formats such as EPUB, BibTeX or OAI-PMH where agreed. | Adapter fixtures; malformed-input and missing-dependency tests; source/licence preservation tests; documented install hints; no new mandatory runtime dependency. |
| **M7 — Multilingual access (€4,000)** | English CI gate, report-only Russian corpus, morphology-tolerant optional retrieval and mixed English/Russian documentation. | Localisation structure; selected European-language interface/documentation support; calibrated language-specific evaluation tracks named in the final agreement. | Versioned locale catalogues; language fixtures; documented translation review; per-language evaluation report; no unsupported claim of equal quality across all languages. |
| **M8 — Model-independence evaluation (€3,000)** | Extractive local answerer is the default; external LLMs are optional and outside the truth boundary. | Comparative evaluation across replaceable language-model interfaces to test whether the same structured memory and receipts preserve factual grounding independently of provider. | Reproducible comparison protocol; multiple model-interface runs; shared FactsPack/receipt inputs; provider-neutral report; no mandatory provider dependency introduced. |
| **M9 — Documentation, governance and onboarding (€1,000)** | Architecture, reviewer guide, demo, status documents and contributor/governance foundations already exist. | Coherent onboarding path; maintained issue/PR templates; reviewer-ready runbook and demonstrator; documentation QA and current-state navigation. | Documentation inventory; clean-clone reviewer walkthrough; contributor pathway; issue/PR templates; link and command validation; release-linked documentation checkpoint. |

## Cross-cutting security delta

M2 and the institutional part of WP2 should use
[`docs/security/eu-service-security-readiness.md`](../security/eu-service-security-readiness.md)
as a non-certification readiness checklist. It converts broad “security hardening”
language into testable controls around authorization, deployment, continuity,
operations and maintenance.

## Research boundary

New cognitive or neuromorphic ideas are not automatically grant work. In particular,
the external intrinsic-noise consolidation hypothesis is tracked only as a
research boundary in
[`docs/research/INTRINSIC_NOISE_CONSOLIDATION_BOUNDARY.md`](../research/INTRINSIC_NOISE_CONSOLIDATION_BOUNDARY.md).
It does not change current runtime, TruthGate, L3, receipts, milestones or budget.

## Change-control rules

1. Do not count an already merged capability as a funded delta.
2. Record the exact baseline commit or release when a grant agreement starts.
3. Tie every payment milestone to repository artifacts and acceptance tests created
   during the funded period.
4. If scope is reduced, remove later deltas rather than weakening acceptance criteria
   for the retained milestones.
5. Keep Research Mode, Personal Exo-Cortex and speculative cognitive mechanisms out
   of the strict grant implementation claim unless separately approved and verified.
6. Do not claim certification, legal compliance, production multi-tenancy, zero
   hallucinations or autonomous self-canonisation.

## Reviewer-safe one-line answer

> Crystal already provides the tested trust kernel; the grant funds the measurable
> engineering delta required to make that kernel reproducible, deployable, secure,
> scalable, multilingual and independently reviewable as public infrastructure.
