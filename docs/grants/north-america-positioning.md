# North American Funding Positioning — Velantrim Crystal

> **What this document is.** This is a **grant narrative / positioning** document
> for North American public-interest and research funders (US/Canada). It explains
> how Velantrim Crystal's *existing* open core can be framed for trustworthy-AI,
> AI-safety and open-source-infrastructure programmes.
>
> **What this document is not.** It is **not** an implementation-status report and
> it does **not** describe new capabilities as if they were already built. The
> single sources of technical truth remain:
> [`../IMPLEMENTATION_STATUS.md`](../IMPLEMENTATION_STATUS.md),
> [`../METAPHOR_VS_MECHANISM.md`](../METAPHOR_VS_MECHANISM.md) and
> [`../../TEST_REPORT.md`](../../TEST_REPORT.md). Where something below is a
> proposed funded deliverable rather than existing code, it is labelled as such.
>
> This "North America track" is a **positioning priority**, not a runtime priority.
> It changes how the *same* core is described for a different funder ecosystem; it
> does not change the architecture, scope discipline or claims of the project.

---

## 1. One-line positioning (North American framing)

> Velantrim Crystal is an open-source, **local-first, verifiable AI memory
> infrastructure** that acts as an **epistemic safety / audit layer** beneath AI
> systems: language models phrase answers, but a structured, source-linked memory
> with an audited gate decides what is treated as true — and every answer ships
> with a **replayable receipt** that can be verified offline.

This mirrors the European framing in
[`../GRANT_NLNET_SCOPE.md`](../GRANT_NLNET_SCOPE.md) (local-first, GDPR-relevant,
digital sovereignty) but expresses the same core in the vocabulary North American
funders use: **trustworthy AI, auditability, hallucination-resistance evaluation,
and provenance**.

| European framing (NLnet/NGI) | North American framing (NSF/Mozilla/Sloan/OTF) |
|---|---|
| Local-first, GDPR-oriented | Local-first, privacy-by-design, user-controlled data |
| Digital sovereignty | Internet freedom, data sovereignty, anti-lock-in |
| Public-interest FOSS for the digital commons | Open-source research infrastructure & trustworthy AI |
| Verifiable memory, provenance receipts | Epistemic safety layer, auditability, source-grounding |

The technical substrate is identical. Only the language of the application differs.

---

## 2. Programme fit (narrative, not status)

The table below is **positioning guidance**, not a claim of eligibility, award, or
endorsement. Each programme should be confirmed against its current published call.

| Funder / programme | Why Crystal is relevant | Language to lead with |
|---|---|---|
| **NSF** (Trustworthy AI; Safe Learning-Enabled Systems; open research infrastructure) | Source-grounded, auditable memory as a substrate for verifiable AI behaviour | Auditability, provenance, evaluation harness, reproducibility |
| **Mozilla Foundation** (trustworthy AI, open source) | Local-first, no-telemetry, AGPL core that reduces dependence on opaque cloud memory | Trustworthy AI, user agency, open-source commons |
| **Alfred P. Sloan Foundation** (open-source research software / infrastructure) | Reusable, tested infrastructure for research knowledge workflows | Open research infrastructure, sustainability, reproducibility |
| **Open Technology Fund (OTF)** | Offline-capable, sovereign, inspectable knowledge memory | Internet freedom, data sovereignty, local-first resilience |

> These are **candidate framings** to evaluate against live calls — not a statement
> that the project has applied to, qualifies for, or has been funded by any of them.

---

## 3. What already works today (grounded)

To keep this document honest, it does **not** restate the implemented feature set
as new claims. The authoritative "Implemented today" list lives in
[`../GRANT_NLNET_SCOPE.md`](../GRANT_NLNET_SCOPE.md) and is evidenced by a fully
passing test suite at 100% coverage on a standard-library runtime
([`../../TEST_REPORT.md`](../../TEST_REPORT.md)).

In one line: a tested, local-first core with an 8-state epistemic state machine, a
type-aware TruthGate/Guardian path, a local L3 canonical graph, replayable
provenance receipts, a baseline evaluation harness, and GDPR-relevant controls —
**already exists and is tested**. The North American track funds *evaluation and
safety hardening on top of that core*, not its initial construction.

---

## 4. No double-dipping — scope separation

A North American application must not fund the same deliverables as the European
([NLnet](../GRANT_NLNET_SCOPE.md)) track. The two tracks are deliberately disjoint:

```
        ┌──────────────────────────┐        ┌──────────────────────────────┐
        │  EU / NLnet (infra)       │        │  US/CA (safety & evaluation)  │
        ├──────────────────────────┤        ├──────────────────────────────┤
        │ • local-first deployable  │        │ • safety / red-team &         │
        │   prototype (WP5)         │        │   adversarial evaluation      │
        │ • evidence span store +   │        │   harness (extends WP3 eval)  │
        │   Receipt v2 hardening    │  ≠     │ • interpretability / audit    │
        │   (WP1)                   │        │   studies of gate decisions   │
        │ • ingestion & review      │        │ • benchmark / fixture-corpus  │
        │   (WP2)                   │        │   expansion (adversarial)     │
        │ • knowledge adapters (WP4)│        │ • grounding-score & robustness│
        └──────────────────────────┘        │   measurement                 │
                                             └──────────────────────────────┘
```

- **EU/NLnet funds**: local-first infrastructure, evidence/receipt hardening (WP1),
  import sessions & curator review (WP2), and knowledge adapters (WP4).
- **US/CA funds**: AI-safety evaluation — a red-team / adversarial test harness,
  interpretability and audit studies of TruthGate decisions, and expansion of the
  evaluation benchmark corpus. This is an **extension on top of** the existing
  WP3 evaluation harness ([`../GRANT_NLNET_SCOPE.md`](../GRANT_NLNET_SCOPE.md) §WP3),
  not a duplicate of it.
- **Explicit commitment**: no single deliverable, milestone, or unit of work is
  charged to more than one funder. The EU budget and milestones in
  [`./funding-use-plan.md`](./funding-use-plan.md) remain the EU track of record;
  any North American budget would be a separate, non-overlapping work plan.

The safety / red-team harness described above is a **proposed funded deliverable**,
not existing code.

---

## 5. Privacy & regulatory-context positioning

Crystal is local-first and user-controlled by design (no telemetry, no outbound
calls by default), which makes its privacy posture portable across regulatory
regimes. This is a **design-property mapping**, not a legal claim:

> Crystal applies **privacy-by-design** concepts that can be mapped to different
> regulatory contexts — including GDPR data-subject expectations,
> **CCPA-style** privacy expectations, and emerging AI-transparency discussions —
> **without claiming legal certification or compliance** with any specific statute.

Operators remain responsible for their own legal compliance. Crystal provides the
technical primitives (local storage, erasure, restriction, record-of-processing,
audit logging) that *support* such obligations; it does not assert that any
deployment is "GDPR-compliant" or "CCPA-compliant".

---

## 6. Out of scope (same discipline as the EU track)

Consistent with [`../GRANT_NLNET_SCOPE.md`](../GRANT_NLNET_SCOPE.md) and
[`../METAPHOR_VS_MECHANISM.md`](../METAPHOR_VS_MECHANISM.md), this positioning does
**not** claim, and the project does **not** pursue:

- AGI, consciousness, artificial personhood, or a "digital brain";
- elimination of hallucination ("zero-hallucination");
- a production-ready autonomous intelligence;
- closed-source SaaS productisation;
- mandatory dependence on a specific LLM provider.

The honest claim is narrow and testable: Crystal **reduces unsupported factual
promotion** through structured, source-linked memory and an auditable gate, and
makes memory operations **inspectable and replayable**.

---

## 7. Cross-references

- [`../IMPLEMENTATION_STATUS.md`](../IMPLEMENTATION_STATUS.md) — implemented vs RFC vs vision (source of truth).
- [`../METAPHOR_VS_MECHANISM.md`](../METAPHOR_VS_MECHANISM.md) — biological naming vs actual software mechanisms.
- [`../../TEST_REPORT.md`](../../TEST_REPORT.md) — current audited test/coverage baseline.
- [`../GRANT_NLNET_SCOPE.md`](../GRANT_NLNET_SCOPE.md) — European scope and work packages (WP1–WP5).
- [`./funding-use-plan.md`](./funding-use-plan.md) — EU milestone budget (track of record).
- [`./reviewer-qa.md`](./reviewer-qa.md) — reviewer Q&A and one-line positioning.

## GenAI disclosure

This document was drafted with AI assistance and reviewed by the maintainer. It is
a positioning narrative; all technical claims are grounded in the current
repository state and the documents cross-referenced above. Repository changes are
traceable through commits.
