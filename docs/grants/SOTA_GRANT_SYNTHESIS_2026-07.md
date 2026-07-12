# Velantrim Crystal — SOTA / Grant Position Synthesis, July 2026

**Status of this document:** dated synthesis map, docs-only. It does not
supersede [`docs/STATUS.md`](../STATUS.md), [`TEST_REPORT.md`](../../TEST_REPORT.md),
[`docs/REVIEWER_CHECKPOINT_2026-07.md`](../REVIEWER_CHECKPOINT_2026-07.md), or any
existing grant document. It links to canonical detailed documents instead of
repeating them.

## 1. Purpose and boundary

This document is a synthesis map written after the completed PR #206–#226
audit-hardening cycle (correctness fixes, contradiction/immune-layer docs,
the CanonicalView RFC, the L3 retrieval benchmark, and the reviewer
checkpoint). Its job is narrow: connect the project's existing comparison,
grant, reviewer and benchmark documents into one compact "where does Crystal
stand now" view — it is not a new audit, not a new comparison table, and not
a new grant application.

If anything here appears to disagree with a more detailed or more recent
source, the detailed document wins:

- [`docs/STATUS.md`](../STATUS.md) and [`TEST_REPORT.md`](../../TEST_REPORT.md) —
  current implementation and test-baseline truth;
- [`docs/REVIEWER_CHECKPOINT_2026-07.md`](../REVIEWER_CHECKPOINT_2026-07.md) —
  what changed in the completed hardening cycle;
- [`docs/COMPARISON.md`](../COMPARISON.md),
  [`docs/grants/grant-safe-readme-positioning.md`](./grant-safe-readme-positioning.md),
  [`docs/grants/GRANT_AUDIT_REPORT.md`](./GRANT_AUDIT_REPORT.md),
  [`docs/grants/funding-use-plan.md`](./funding-use-plan.md),
  [`docs/grants/reviewer-qa.md`](./reviewer-qa.md) — the detailed comparison,
  positioning, audit and grant documents this file maps to.

## 2. One-paragraph current position

Velantrim Crystal is local-first, verifiable AI memory infrastructure — not a
chatbot, not a generic RAG application, and not a claim of AGI or
consciousness. It separates candidate speech (what an LLM says) from trusted
memory (what the graph/canon holds), using an implemented TruthGate admission
boundary, a Trace/Receipt proof path, per-fact provenance, and GDPR-oriented
controls (erasure, restriction, audit logging) within the project's stated
scope. The PR #206–#226 cycle added audit-confirmed correctness fixes,
documented contradiction/immune-layer behaviour, an explicit CanonicalView
RFC boundary between the physical graph and strict canon, a first retrieval-
scale benchmark baseline, and a reviewer-facing checkpoint of all of the
above — improving correctness and documentation clarity, not adding new
runtime capability beyond the specific bug fixes named in that cycle. A
subsequent cycle (PR #257, hardened by PR #258) then implemented the
strict-grounding slice of that same CanonicalView RFC as real, tested
runtime behavior — see section 4 below.

## 3. SOTA position map

This is a positioning map, not a benchmark claim — see
[`docs/COMPARISON.md`](../COMPARISON.md) for the full comparison table and
reasoning behind each row.

| SOTA area | Typical current approach | Crystal position | Canonical doc |
|---|---|---|---|
| Vector RAG / vector stores | Similarity search over chunks; the model judges what's true | Crystal emphasizes typed, source-linked facts and an explicit admission truth boundary, rather than treating retrieved chunks as authority | [`docs/COMPARISON.md`](../COMPARISON.md) |
| Chatbot memory features | Vendor-controlled personalization, often opaque | Crystal differs by being local-first and inspectable by default, with no mandatory cloud path | [`docs/COMPARISON.md`](../COMPARISON.md) |
| Agent memory frameworks (MemGPT/Letta-style) | Agent-centric memory orchestration, provider-dependent semantics | Crystal emphasizes a lower-level, framework-independent verifiable memory core that an agent can sit on top of | [`docs/COMPARISON.md`](../COMPARISON.md) |
| Temporal graph memory (Zep/Graphiti-style) | Time-aware conversational/event graphs, usually service-bound | Crystal differs by being dependency-free by default and keeping canonical writes behind an audited TruthGate | [`docs/COMPARISON.md`](../COMPARISON.md) |
| Provenance / receipt systems | Varies widely; often absent or ad hoc | Crystal implements per-fact provenance chains and replayable answer receipts as first-class, tested primitives | [`docs/REVIEWER_CHECKPOINT_2026-07.md`](../REVIEWER_CHECKPOINT_2026-07.md) |
| Local-first private AI infrastructure | Often an enterprise add-on to a cloud-first product | Crystal's default runtime path is stdlib-only, local SQLite/WAL, no telemetry | [`docs/COMPARISON.md`](../COMPARISON.md), [`docs/DIGITAL_SOVEREIGNTY.md`](../DIGITAL_SOVEREIGNTY.md) |
| Compliance-oriented AI memory | Compliance bolted on externally, or claimed without technical backing | Crystal implements GDPR-relevant technical controls (erasure, restriction, audit log, PII redaction) as project-scoped features, not a legal certification | [`docs/grants/funding-use-plan.md`](./funding-use-plan.md) |
| Reviewer / grant reproducibility | Claims often unverifiable without vendor cooperation | Crystal ties every claim to a public repository, a 100%-coverage test baseline, and a dated reviewer checkpoint | [`TEST_REPORT.md`](../../TEST_REPORT.md), [`docs/REVIEWER_CHECKPOINT_2026-07.md`](../REVIEWER_CHECKPOINT_2026-07.md) |

## 4. What is newly stronger after PR #206–#226

This is the main new content of this document — the delta the rest of the
grant/reviewer documents predate:

- **Correctness hardening**: 8 audit-confirmed bugs fixed across PRs #216 and
  #222 (store_fact L0-cache poisoning, an audit/provenance write-lock race,
  an import-session duplicate-erasure bug, a TruthGate missing-confidence
  crash, a volition source_status gap, an erase_fact no-op/orphan bug, a CLI
  traceback, a PII false positive), plus 2 more caught and fixed via
  Codex review on those same PRs. Detail:
  [`docs/REVIEWER_CHECKPOINT_2026-07.md`](../REVIEWER_CHECKPOINT_2026-07.md#2-what-changed-in-the-completed-cycle).
- **Contradiction / immune-layer documentation**: the previously-undocumented
  safe-surfacing behaviour of `core/contradiction.py`, `core/reconcile.py`
  and `core/immune.py` is now written down, including what is *not* done
  (no silent auto-resolution). Detail:
  [`docs/CONTRADICTION_POLICY.md`](../CONTRADICTION_POLICY.md),
  [`docs/IMMUNE_LAYER.md`](../IMMUNE_LAYER.md).
- **CanonicalView RFC boundary — now partially implemented**: a named,
  reviewable contract distinguishing the physical L3 graph from a
  trusted-only, `VERIFIED` + trace-valid read projection. The strict-grounding
  slice is implemented and merged (`core/canonical_view.py`, wired into
  `core/pipeline.py::generate_answer()`, PR #257) and hardened by a
  seven-commit corrective cycle (PR #258) that dispositioned all 9 review
  threads on #257 and closed 17 further independent-review findings — both
  PRs report 0 unresolved review threads. The RFC's `review`/`full_graph`
  read modes, a CLI/API `trusted_only` exposure, and the
  conflicting-`VERIFIED`-facts abstention policy remain unimplemented.
  Detail: [`docs/CANONICAL_VIEW_RFC.md`](../CANONICAL_VIEW_RFC.md),
  [`docs/STATUS.md`](../STATUS.md).
- **L3 retrieval benchmark baseline**: the first reproducible, dependency-free
  measurement of `core.l3_graph`'s SQLite-backend retrieval latency at scale,
  including a disclosed near-linear scaling characteristic — a smoke
  baseline, not an optimization or a production SLO. Detail:
  [`docs/benchmarks/L3_RETRIEVAL_SCALE.md`](../benchmarks/L3_RETRIEVAL_SCALE.md).
- **Reviewer checkpoint**: a single, dated document that separates
  implemented vs. RFC-only vs. benchmark-only work across this whole cycle,
  so a reviewer does not have to reconstruct that boundary from eight PRs.
  Detail: [`docs/REVIEWER_CHECKPOINT_2026-07.md`](../REVIEWER_CHECKPOINT_2026-07.md).

## 5. Existing documents map

This map exists to prevent doc sprawl — check here before writing a new
grant/reviewer document.

| Question | Best existing document |
|---|---|
| What is Crystal? | [`README.md`](../../README.md) / [`docs/REVIEWER_GUIDE.md`](../REVIEWER_GUIDE.md) |
| How is it different from RAG/vector DB/agent memory? | [`docs/COMPARISON.md`](../COMPARISON.md) |
| What is the grant-safe public framing? | [`docs/grants/grant-safe-readme-positioning.md`](./grant-safe-readme-positioning.md) |
| What did the deep grant audit find? | [`docs/grants/GRANT_AUDIT_REPORT.md`](./GRANT_AUDIT_REPORT.md) |
| How would NLnet funding be used? | [`docs/grants/funding-use-plan.md`](./funding-use-plan.md) |
| What might reviewers ask? | [`docs/grants/reviewer-qa.md`](./reviewer-qa.md) |
| What changed after the audit-hardening cycle? | [`docs/REVIEWER_CHECKPOINT_2026-07.md`](../REVIEWER_CHECKPOINT_2026-07.md) |
| What is current implementation truth? | [`docs/STATUS.md`](../STATUS.md) / [`TEST_REPORT.md`](../../TEST_REPORT.md) |
| Where does Crystal stand relative to SOTA right now? | this document |

## 6. Grant relevance, without duplicating grant docs

This section is intentionally short. It does not replace or restate
[`docs/grants/GRANT_AUDIT_REPORT.md`](./GRANT_AUDIT_REPORT.md) or
[`docs/grants/funding-use-plan.md`](./funding-use-plan.md).

**NLnet relevance**: open-source (AGPL-3.0), local-first by default, a
verifiable-memory approach aligned with public-interest digital infrastructure,
and milestone-verifiable work checkable against the public repository. Full
detail: [`docs/grants/funding-use-plan.md`](./funding-use-plan.md),
[`docs/grants/reviewer-qa.md`](./reviewer-qa.md).

**Hub71 / AI infrastructure relevance** (kept generic — see boundary below):
trustworthy AI infrastructure, auditable AI memory, a provenance/governance
layer beneath an application's own AI stack, and an enterprise-AI-trust angle
(traceable answers, GDPR-oriented controls). This paragraph does not
independently verify or restate any current Hub71 programme terms.

**General reviewer relevance**: every claim in this document is meant to be
checkable against `main` — the test baseline, the reviewer checkpoint, and
the named source files — rather than taken on trust.

**Boundary**: this document is not an application form and does not replace
programme-specific application text. It does not state or assume current
Hub71 eligibility, terms, or deadlines.

## 7. What is not yet SOTA / remaining gaps

Being explicit about gaps is part of reviewer trust, not a weakness to hide.

| Gap | Status |
|---|---|
| CanonicalView implementation | Partially implemented — strict-grounding slice merged (PR #257, hardened PR #258); `review`/`full_graph` modes, CLI/API `trusted_only` exposure, and conflict-abstention policy remain RFC-only ([`docs/CANONICAL_VIEW_RFC.md`](../CANONICAL_VIEW_RFC.md)) |
| L3 retrieval optimization | Benchmark baseline exists ([`docs/benchmarks/L3_RETRIEVAL_SCALE.md`](../benchmarks/L3_RETRIEVAL_SCALE.md)); the observed near-linear scaling is not yet addressed |
| Property / invariant test suite | Future work — not started; current suite is example-based (see [`TEST_REPORT.md`](../../TEST_REPORT.md) for the current pass/skip count and coverage) |
| Independent external adoption | Limited — no PyPI release, no known third-party deployments, no independent citations to date |
| Public package / release maturity | No public package release yet; the project is at pre-release, tested-core maturity |

## 8. Safe claim language

Reuse this block in grant or reviewer text instead of re-deriving wording.

**Good:**

```text
local-first verifiable AI memory infrastructure
GDPR-oriented controls
auditable provenance and replayable receipts
TruthGate-mediated memory admission
benchmark baseline, not a performance guarantee
strict CanonicalView grounding implemented for answer generation
```

**Avoid:**

```text
GDPR compliant / certified
AI Act compliant
zero hallucinations
AGI
consciousness
production-scale performance guarantee
implemented trusted-only CanonicalView reads (the full three-mode
  trusted_only/review/full_graph RFC contract, CLI/API exposure, and
  conflict-abstention policy remain unimplemented — see section 4)
```

## 9. Suggested short external pitch

Velantrim Crystal is a local-first verifiable AI memory layer that treats LLM
output as candidate speech, not truth. Instead of letting retrieved text
become authority by repetition, Crystal attaches claim type, source status,
epistemic state, and provenance to memory before it can be treated as
trusted, and produces replayable receipts for the answers built from that
memory. Recent hardening work added audit-confirmed
correctness fixes, an explicit RFC boundary for canonical reads, and a
retrieval-scale benchmark baseline, making the project easier to review and
safer to extend. It is not a chatbot, not a generic RAG app, and not a
compliance certification — it is open-source infrastructure for auditable AI
memory.

---

*This document is a dated synthesis (July 2026, after PR #206–#226). For
anything not covered here, or if it appears to disagree with a more recent
state of `main`, `docs/STATUS.md`, `TEST_REPORT.md`, and the linked documents
above are authoritative.*
