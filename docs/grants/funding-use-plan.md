# Funding Use Plan — Approx. €50,000 (NLnet Commons Fund)

## Application status

| Field | Value |
|---|---|
| Proposal framing | **Verifiable AI memory infrastructure for European use cases (GDPR-oriented)** |
| Programme | NLnet **NGI0 Commons Fund** |
| Requested amount | approx. **€50,000** |
| Status | **Submitted / under review / not awarded** |

> **Planning and transparency document.** This is not an approved budget, award or payment
> commitment. Private correspondence details remain outside the public repository.

## Living-baseline rule

Crystal has continued to advance while the proposal is under review. Grant accounting must
therefore be reconciled against live signed `main` at the time of any agreement.

```text
VERIFIED BASELINE AT AGREEMENT TIME
        +
NEW MEASURABLE FUNDED DELTA
        =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

Anything merged before an agreement is existing pre-agreement work and **cannot be paid for
again as future delivery**.

As of 2026-08-12, the Reader baseline includes RC-1 through RC-9. RC-9 is the deterministic
offline lexical PRE-ADMISSION candidate-discovery baseline and frozen benchmark. PR #378 also
merged an RC-10 reuse/comparison preregistration contract, but no semantic/hybrid comparison or
new Reader retrieval runtime was executed.

The canonical current split is maintained in
[Grant Baseline → Funded Delta → Acceptance Matrix](./baseline-funded-delta-matrix.md). If
repository truth advances again before an agreement, that matrix must be re-audited rather than
reusing stale application-era wording.

## Current proof point: RC-9 is existing baseline, not funded delta

Frozen `K=5` result in `eval/reader_rc9_lexical_baseline.json`:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Paired hard-negative hits | 4 / 4 |

The cross-lingual pair `rc8-004` is missed and all four paired hard negatives surface in top-5.
The result is classified `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

These are retrieval metrics on a small frozen synthetic/adversarial paired corpus. They are not
accuracy, semantic equivalence, truth-verification or evidence-admission metrics, and they do
not predetermine semantic/vector technology as the remedy.

## What funding should convert

Crystal already has a tested local-first memory/evidence core and a bounded Reader foundation.
A future grant should fund **new work that makes the public system more reproducible,
deployable, reviewable and independently measurable**, not recreation of merged code.

The exact deliverable wording below is therefore planning intent. Before any funded milestone
starts, its acceptance contract must subtract capabilities already present on signed `main`.

## Planning budget — deliverable envelopes

| # | Milestone / deliverable envelope | Planning amount |
|---|---|---:|
| M1 | **Local-first deployable prototype hardening.** Reproducible setup, packaged run path, import/export and operator documentation beyond the then-current baseline. | €9,000 |
| M2 | **Service-layer hardening.** Extend only the delta beyond any existing optional API into documented, capability-gated and tested reviewer/deployment surfaces. | €8,000 |
| M3 | **Production-strength evidence spans + receipt replay.** New exact span/replay capabilities not already in baseline, with independent fixtures and failure tests. | €8,000 |
| M4 | **Evaluation as a stronger CI quality gate.** Larger curated fixtures, frozen metrics and regression evidence beyond existing evaluation/RC-9 benchmark surfaces. | €5,000 |
| M5 | **Knowledge-base expansion.** New source-referenced, licence/provenance-aware corpus work beyond existing shipped material. | €7,000 |
| M6 | **Knowledge adapters.** New independently tested import adapters and source/licence handling that are absent at agreement time. | €5,000 |
| M7 | **Multilingual access.** Translation/accessibility work against a frozen current English source checkpoint. | €4,000 |
| M8 | **Model-independence / retrieval evaluation.** A separately authorized comparison study only where live evidence still justifies it; exact backend/model identity and privacy/resource gates required. | €3,000 |
| M9 | **Documentation, governance and onboarding.** New reviewer/contributor/release evidence beyond the then-current public documentation baseline. | €1,000 |
| | **Planning total** | **€50,000** |

These amounts remain planning context only. They do not prove award, approval or entitlement,
and they do not override a future signed milestone agreement.

### Existing-vs-new acceptance rule

A milestone may retain the same public goal while its funded acceptance criteria shrink as the
pre-agreement baseline advances. Example:

```text
if setup/documentation already exists before agreement:
    existing setup/documentation = baseline
    only demonstrably new hardening = funded delta
```

The same rule applies to Reader work. RC-1 through RC-9 cannot be rebilled. RC-10's merged
preregistration cannot be rebilled as if it had not happened.

## Retrieval / model-independence boundary

Crystal is not intended to depend on one proprietary model. Existing admitted-memory retrieval
and optional model adapters are separate from PRE-ADMISSION Reader discovery.

Any future M8 comparison must preserve:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

A comparison deliverable is an evaluation artifact, not permission to wire semantic/vector
machinery into Reader runtime. Exact model/backend identity, privacy, offline/network behavior,
resource cost and failure analysis must be recorded.

## Partial funding

If any eventual award is lower than the planning amount, scope should be reduced by removing or
shrinking later deliverables rather than relabeling already implemented baseline work as paid
work. Priority remains local-first reproducibility, evidence/replay quality, service hardening,
evaluation and reviewer documentation before broader adapters/model comparison.

Mobile applications, cloud synchronization, specialized model training and unrelated cognitive
research remain outside this plan unless separately agreed.

## Responsible data and privacy position

Velantrim is local-first and user-controlled by design. That is an engineering characteristic,
not automatic legal compliance or a security certification.

Grant-facing deployments must preserve:

- operator/user control over memory data;
- no silent upload of sensitive data to third parties;
- explicit access-control/governance requirements for institutional use;
- consent/legal-basis/transparency responsibilities where applicable;
- auditability without unnecessary personal-data exposure;
- export, restriction and deletion controls;
- documented dependency/supply-chain risks.

Known PII/supply-chain hygiene remains a separate backlog under #214.

## Expected public benefit

The intended contribution is open infrastructure rather than another chatbot:

- auditable local-first AI memory;
- source/provenance-aware Reader artifacts;
- explicit authority boundaries;
- reproducible evaluation evidence;
- inspectable retrieval limitations;
- reduced dependence on opaque cloud-only memory.

## Honest-language commitment

Crystal aims to reduce unsupported factual promotion and preserve traceable source metadata. It
does **not** claim zero hallucinations, universal truth detection, semantic understanding,
automatic claim identity, automatic corroboration, autonomous evidence admission, full security,
GDPR certification or a finished commercial platform.

The strongest grant narrative is the measured one: implement a bounded baseline, benchmark it,
publish both strengths and failures, then decide future work from evidence.

## GenAI disclosure

This document has been maintained with AI assistance and maintainer review. Repository changes,
tests, benchmark artifacts and merge history remain publicly auditable.
