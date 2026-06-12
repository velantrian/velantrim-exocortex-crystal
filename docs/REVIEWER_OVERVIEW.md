# Velantrim Exo-Cortex Crystal — Reviewer Overview

*Local-first, traceable AI memory infrastructure for source-grounded, auditable
AI systems.*

> Audience: external reviewers, NLnet-style grant reviewers, university
> collaborators, trustworthy-AI and digital-sovereignty programs. For the
> canonical implemented-vs-RFC-vs-vision map, see
> [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md); for the audited test
> baseline, see [TEST_REPORT.md](../TEST_REPORT.md).
> **Start hands-on:** [REVIEWER_DEMO.md](./REVIEWER_DEMO.md) — a 10-minute
> demo of the full trust loop (ingest → evidence → receipt → tamper check →
> eval gate).

## 1. Executive Summary

Velantrim Exo-Cortex Crystal is an open-source (AGPL), local-first AI memory
infrastructure that separates truth from speech. It stores typed claims with
explicit source and truth status, constructs traceable evidence paths, and
enforces architectural boundaries to prevent unsupported factual claims from
entering the verified canon. The LLM is used as a speech and synthesis layer,
not as a source of truth.

**Velantrim does not make the LLM truthful. It restricts what the LLM may
confidently say.** The system is designed to reduce unsupported factual
promotion by enforcing evidence, traceability, and boundary checks.

Crystal is a verifiable substrate, not a chatbot, AGI claim, or autonomous
agent.

## 2. Problem

Modern AI systems often conflate fluent speech with verified truth. LLM output
can be persuasive without evidence. Many memory systems store and retrieve
context but do not enforce epistemic boundaries: a remembered statement carries
no machine-readable record of where it came from, whether it was user-reported,
model-generated or externally sourced, and whether it can be audited, restricted
or erased. These systems can be hard to audit in high-stakes domains such as
education, science, law, medicine, and public-sector knowledge workflows.

## 3. Solution

Crystal is a local-first AI memory infrastructure that separates truth from
speech:

```text
Typed Claims → FactsPack → Guardian → TruthGate → TRACE / Receipt → LLM Speech Layer
```

- The LLM is speech/synthesis only; it may phrase an answer but never becomes
  the source of truth.
- **Canon is the VERIFIED + TRACE-valid memory, not the whole graph.** The
  physical memory/graph may contain hypotheses, user claims, and subjective
  states — each labelled as such and never silently upgraded.
- Confident factual answers require evidence and TRACE; without sufficient
  grounding the system abstains or downgrades confidence.
- **Velantrim blocks unsupported factual promotion into VERIFIED canon unless
  evidence and TRACE are present.**

## 4. Core invariants

| Invariant | Meaning |
|---|---|
| Speech ≠ Truth | Generated text is not canon |
| LLM_OUTPUT ≠ VERIFIED | LLM output cannot become verified without independent evidence |
| Canon = VERIFIED + TRACE-valid memory | Canon is filtered memory, not the raw graph |
| TRACE required for confidence | Confident factual claims must be auditable |
| Human curator remains final authority | The system does not autonomously rewrite values or canon; overrides are explicit, attributed and audited |

## 5. Current implementation status

Statuses follow [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)
(Implemented = code + tests in this repository).

| Area | Status | Notes |
|---|---|---|
| Typed claims (`claim_type` / `source_status` / `truth_status` separation) | Implemented | Canonical enums in `core/memory.py` and `schemas/`; `FACT` is a human-facing alias only — the machine truth status is `VERIFIED` (T2 alignment) |
| TruthGate | Implemented | `core/truth_gate.py` — type-aware, the only automatic entry into L3 canon; behaviour-pinned by tests |
| FactsPack | Partial | Grounding pack used by the answer path; explicit conflict policy is a future RFC |
| TRACE / Receipt | Implemented | Trace chains + sealed, replayable receipts identified by content digest (no separate receipt_id); strict-provenance replay |
| Guardian / Ring Zero | Partial (baseline) + docs | Boundary function runs before the gate; formal contract document is future work; Ring Zero invariants documented in [ARCHITECTURE.md](./ARCHITECTURE.md) |
| Local-first storage | Implemented | SQLite/WAL working memory; dependency-free SQLite default for the canonical graph; pluggable graph-backend direction (see IMPLEMENTATION_STATUS for backend roles) |
| GDPR-oriented design goals | Partial | Local-first storage, erasure/restriction, tamper-evident audit, PII redaction as design targets — explicitly **not** a certification claim |
| CI / tests / eval gate | Implemented | CI jobs: tests (3.11/3.12), eval gate, security, JSONL integrity. Latest reported baseline: see [TEST_REPORT.md](../TEST_REPORT.md) (exact counts live there and in the README badge only); 100% coverage gate preserved, eval gate passed |
| P0 / P0.1 documentation honesty cleanup | Completed | Implementation-status map, canon semantics, overclaim wording removed (PR #103, #105) |
| T2 schema alignment | Completed | KB/schema vocabulary aligned with runtime reality (PR #106) |
| Harness Replay / Meta-Optimization | RFC only | [RFC_HARNESS_REPLAY_OPTIMIZATION.md](./RFC_HARNESS_REPLAY_OPTIMIZATION.md) — documentation only, no runtime |

## 6. Research context

Velantrim is informed by a long tradition of work on memory, human-computer
augmentation, and trustworthy knowledge systems. Vannevar Bush's Memex
introduced the idea of associative knowledge trails; Licklider and Engelbart
framed computers as tools for augmenting human intellect rather than replacing
judgment. In Crystal, these ideas are translated into a verifiable
architecture: TRACE formalizes evidence paths, TruthGate separates unsupported
claims from verified canon, and the LLM remains a speech layer rather than a
source of truth. These references are architectural inspirations, not claims
that Crystal is brain-like, conscious, or biologically accurate.

## 7. Roadmap

| Step | Scope | Status |
|---|---|---|
| P0 | Architecture honesty / implementation status | Completed |
| P0.1 | Overclaim cleanup / grant-safe wording | Completed |
| T2 | KB schema alignment | Completed (PR #106 merged) |
| T3 | Eval corpus expansion | Next |
| T4 | Reproducible MVP packaging | Planned |
| T5 | Reviewer demo package | Planned |
| T6+ | Larger traceable KB and research tracks | Research |
| Follow-up | Research Inspirations document (non-normative context, not implementation status) | Planned follow-up |

## 8. Grant and university value

The project is positioned as infrastructure for scientific knowledge
management, education technology, agent evaluation, and digital sovereignty
programs — not as artificial consciousness or zero-hallucination chat.

Concretely relevant to: digital sovereignty (local-first, no mandatory cloud),
trustworthy AI (verification boundary, controlled factual promotion), AI safety
(non-bypassable invariants, human-curated canon), reproducible evaluation
(CI-gated eval harness, replayable receipts), knowledge-graph research (typed,
source-tracked claims), GDPR-oriented auditability, and education/research
demonstrators.

## 9. What Crystal is not

- Not a chatbot.
- Not an AGI claim.
- Not artificial consciousness.
- Not a guarantee of perfect truth.
- Not a replacement for expert judgment.
- Not a self-improving autonomous agent.
- Not a brain-like or biologically conscious system.

## 10. Research-grade future (not current runtime)

All items below are future / research roadmap / not current runtime: a
10k–100k traceable-facts demonstrator, ProfSearch, Causal Spine, Essence
Distiller, Harness Replay runtime and ReplayBench (RFC only today), the
FactsPack Conflict Policy, and a Meta-Cognitive Monitor as a future research
umbrella over evaluation and boundary-monitoring concepts (see
[EVALUATION_METRICS.md](./EVALUATION_METRICS.md)). Research inspirations
(memory science, human-computer augmentation, cybernetics, knowledge graphs,
trustworthy-AI research) are tracked as non-normative context — intellectual
foundations and architectural patterns, never implementation claims (see
ADR-006 in [ADR.md](./ADR.md)). Biological analogies in project materials are
used only as architectural inspiration patterns, not as claims that the system
is brain-like, conscious, or biologically accurate.
