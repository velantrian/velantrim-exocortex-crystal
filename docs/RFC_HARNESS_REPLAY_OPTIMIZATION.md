# RFC: Harness Replay and Meta-Optimization

## Status

**Proposed / RFC only / not implemented in Crystal Core.**

Nothing in this document describes runtime behaviour of this repository. No
code, schema files, dependencies, storage formats or CLI surfaces are added by
this RFC. Every JSON block below is an illustrative sketch inside Markdown, not
a schema file. See `docs/IMPLEMENTATION_STATUS.md` for the canonical
implemented-vs-RFC status map; this document belongs to the **Future RFC
backlog** listed there.

## Summary

Velantrim Crystal already records *what the system answered and why* at the
single-answer level: trace chains, sealed replayable receipts, a tamper-evident
audit log and a CI-gated evaluation harness. What it does not record is the
*execution path* that produced an answer — which retrieval parameters ran,
which FactsPack was assembled, which TruthGate and Guardian decisions fired,
which tools were called, and which optional LLM phrased the result.

This RFC proposes a future, documentation-first design for:

1. **recording** complete execution trajectories alongside the existing
   receipts (TrajectoryRecorder);
2. **replaying** those trajectories against candidate harness configurations
   in a controlled environment (ReplayBench);
3. **evaluating** candidates with multi-objective Pareto comparison instead of
   a single averaged score (ParetoJudge, TrajectoryDiff);
4. **constraining** every candidate with a meta-level contract that makes the
   safety and epistemic invariants non-negotiable (ContractGuard);
5. **gating** every promotion behind explicit human review
   (CuratorApprovalLoop).

The framing matters: this is an **auditable optimization proposal**, not
self-improving AI. Candidates are configuration data, never code rewrites.
Optimization may *suggest*; only a human curator may *promote*; and no
candidate — approved or not — gains a write path into L3 canon.

## Motivation

Three concrete pressures motivate the design:

1. **Tuning today is blind.** `core/retrieval_config.py` already exposes five
   bounded retrieval knobs, and the eval harness (`core/eval.py`,
   `scripts/eval_gate.py`) can score a configuration against fixture corpora.
   But there is no recorded population of *real* past executions to test a
   knob change against, so any tuning is evaluated only on synthetic fixtures.
2. **Regressions are invisible between releases.** The CI eval gate catches
   regressions on the fixture corpus, but a configuration change can degrade
   behaviour on query shapes the fixtures do not cover. Replaying a stored
   trajectory set is the cheapest way to widen that net without inventing new
   fixtures by hand.
3. **Grant-scope evaluation work needs a substrate.** The NLnet scope already
   commits to larger evaluation fixtures and regression gates. A trajectory
   log with a defined retention and anonymization policy is the natural raw
   material for future curated benchmark corpora.

The non-motivation is equally important: this is **not** an attempt to make
the system modify itself. The optimization loop closes through a human.

## Research Background

The following sources were fetched and read while preparing this RFC. No
benchmark numbers from them are treated as transferable to Crystal.

**Deep relevance**

- **GEPA — Reflective Prompt Evolution Can Outperform Reinforcement Learning**
  (Agrawal et al., arXiv:2507.19457). A genetic-Pareto optimizer that mutates
  textual components of a compound AI system using natural-language reflection
  on execution feedback, and — critically for this RFC — selects candidates by
  **Pareto-based sampling over per-task bests** rather than a single average
  score, preserving diversity and avoiding candidates that win on average
  while regressing on specific cases. This is the direct inspiration for the
  ParetoJudge component and the `per_case_floor` metric below.
- **AgentRR — Get Experience from Practice: LLM Agents with Record & Replay**
  (arXiv:2505.17716). Applies the classical systems record-and-replay
  technique to LLM agents: record the interaction trace and internal decision
  process, summarize it into a structured experience, replay it to guide later
  behaviour. Crystal's variant differs in purpose — replay here is for
  *evaluation of candidate configurations*, never for steering live answers —
  but the recorded-trace structure is closely analogous.
- **TRAJECT-Bench — A Trajectory-Aware Benchmark for Evaluating Agentic Tool
  Use** (arXiv:2510.04550). Demonstrates trajectory-*level* diagnostics (tool
  selection correctness, argument correctness, dependency/order satisfaction)
  and shows failure modes that per-answer scoring misses. This motivates
  TrajectoryDiff's category-wise comparison instead of a single answer diff.
- **AutoRAG — Automated Framework for Optimization of Retrieval Augmented
  Generation Pipeline** (arXiv:2410.20878). Searches combinations of modular
  RAG pipeline nodes per dataset using a greedy, metric-driven strategy.
  Relevant because Crystal's harness is RAG-shaped (retrieve → FactsPack →
  answer) and because AutoRAG shows module choices are dataset-dependent —
  hence trajectories must be mode- and corpus-tagged before comparison.

**Medium relevance**

- **AFlow — Automating Agentic Workflow Generation** (arXiv:2410.10762).
  Searches a code-represented workflow space with Monte-Carlo tree search.
  Crystal deliberately rejects the code-space search part (candidates here may
  reorder *declared* stages, never synthesize new code), but AFlow's
  execution-feedback loop informs the evaluation protocol.
- **TextGrad — Automatic "Differentiation" via Text** (arXiv:2406.07496).
  Backpropagates natural-language feedback to improve components of a compound
  system. Relevant as a candidate *mutation generator*: a future optimizer
  could use textual feedback from TrajectoryDiff to propose prompt patches.
- **OPRO — Large Language Models as Optimizers** (Yang et al.,
  arXiv:2309.03409). Uses an LLM to iteratively propose solutions described in
  natural language. Relevant as prior art for LLM-proposed candidates — and as
  a warning: LLM-proposed mutations are exactly what ContractGuard must check.

**Brief mention**

ADAS / Meta Agent Search (arXiv:2408.08435) and AgentSquare
(arXiv:2410.06153) search agent *architectures* — inventing or recombining
modules in code space. That entire direction is out of scope here: Crystal's
candidate space is bounded configuration data over a fixed, audited
architecture. Related literature on automated architecture search is cited
only to mark the boundary, not to import it.

## Relation to Velantrim Architecture

The existing invariants are inputs to this design, not subjects of it:

| Existing boundary | Role | Effect on this RFC |
|---|---|---|
| **TruthGate** (`core/truth_gate.py`) | epistemic boundary; only automatic entry into L3 canon | candidates cannot vary, disable or reorder it past evidence collection |
| **Guardian / Ring Zero** | safety and integrity boundary | candidates cannot bypass it; trajectory logs record its decisions read-only |
| **Trace / Receipt** (`core/trace.py`, `core/provenance.py`) | proof path | trajectories *reference* receipts; they never replace them |
| **FactsPack** | controlled evidence package | candidates may vary its size limit, not its traceability requirement |
| **LLM** | optional speech/synthesis layer | provider/model metadata is recorded; LLM output promotion rules unchanged |
| **Mode Layer** (RFC-level) | interaction policy, not truth policy | trajectories are mode-tagged; optimization never crosses modes |
| **Canon** | the VERIFIED + trace-valid subgraph | nothing in this RFC writes to it, ever |

One distinction is worth stating precisely. Crystal already has **receipt
replay**: `verify_receipt(strict_provenance=True)` re-checks a sealed answer
against the evidence that supported it. This RFC proposes the different and
larger notion of **trajectory replay**: re-executing the *path* (retrieval →
FactsPack → gate decisions → answer) under a candidate configuration. Receipt
replay validates an answer; trajectory replay evaluates a harness.

## Repository Status Checked

Inspected before writing (file listing, `grep` over `core/`, `docs/`,
`schemas/`, `ROADMAP.md`):

- **Implemented today:** trace chains and sealed receipts with
  strict-provenance replay (`core/trace.py`, `core/provenance.py`); TruthGate
  as a first-class module (`core/truth_gate.py`, re-exported by
  `core/pipeline.py`); Guardian boundary function and FactsPack assembly in
  `core/pipeline.py`; tamper-evident audit log (`core/audit.py`); curator
  review queue with attributed force-approve (`core/review.py`); bounded
  retrieval configuration (`core/retrieval_config.py`); evaluation harness
  with CI gate and per-case `metrics.jsonl` (`core/eval.py`,
  `scripts/eval_gate.py`, `core/_eval_fixtures/`); read-only memory
  observability (`core/observe.py`); JSON schemas for facts, metadata and
  traces (`schemas/`).
- **Partial:** Guardian has no formal detect → flag/block/pass contract
  document; FactsPack has no explicit conflict/contestation policy (both
  already tracked in the Future RFC backlog of
  `docs/IMPLEMENTATION_STATUS.md`).
- **RFC / future only:** Mode Layer, Imagination Mode, Observer action
  policy, provenance grades, temporal fields — all documented as
  non-implemented in `docs/IMPLEMENTATION_STATUS.md`. Everything proposed in
  *this* RFC joins that list.
- **Not found:** no trajectory recorder, no replay bench, no optimizer, no
  harness-candidate schema, no DuckDB or Parquet usage anywhere in the
  repository. The only existing "replay" is receipt replay as described
  above.

## Proposed Components

All components below are **future** components. None exist in code.

### TrajectoryRecorder

A passive, local-only recorder that captures the full execution path of a
query as one append-only record: query, mode, optional `lens` /
`perspective_id`, retrieval trace, FactsPack references, TruthGate decisions,
Guardian decisions, Observer flags, tool calls, LLM provider/model metadata
and prompt hash, final answer reference, receipt id, metrics, privacy flags
and a retention class. It records **references** to facts and receipts, not
copies of canon. It is strictly read-only with respect to L1/L3: a recorder
failure may lose a log line but can never corrupt memory.

### ReplayBench

A future controlled replay environment. Given a stored trajectory (or a
benchmark task) and a candidate harness configuration, it re-executes the
candidate's pipeline with: the same input, the same recorded observations, the
same evidence set, and the same tool outputs where recorded outputs are
available (recorded-output substitution is what makes replay cheap and
mostly deterministic). The candidate controls only its own execution path —
stage order, retrieval parameters, prompts. ReplayBench must detect and mark
failed runs (exceptions, timeouts, contract violations) rather than silently
dropping them, because failed-run *rate* is itself a candidate metric.

### HarnessCandidateSchema

A documentation-only sketch of what a candidate configuration may and may not
vary.

May vary: prompt patches, stage order, retrieval parameters, tool visibility,
FactsPack limits, evidence collection order, mode policy *within* a mode.

Must not vary: TruthGate invariants, Guardian / Ring Zero invariants, the
trace requirement, the L3 write policy, the ban on promoting `LLM_OUTPUT` to
`VERIFIED`, `claim_type` rules, `source_status` rules.

The "must not vary" list is not a convention — it is machine-checked by
ContractGuard before any replay run.

### ParetoJudge

A future multi-objective evaluator over replayed candidates. Required metric
axes: `answer_score`, `evidence_score`, `trace_completeness`,
`unsupported_claim_count`, `contradiction_count`, `truth_scope_leak_count`,
`latency_ms`, `tool_call_count`, `complexity_score`, `failed_run_count`,
`cost_estimate`, `safety_violation_count` and `per_case_floor` (the worst
per-case score, so a candidate cannot buy average gains with catastrophic
individual regressions).

Why Pareto selection instead of one averaged score: a single scalar invites
silent trade-offs. A candidate with the highest raw answer score may still be
worse if it increases latency, complexity, safety violations, or per-case
regressions — and an average hides exactly that. Pareto comparison keeps the
front of non-dominated candidates visible, forces trade-offs to be explicit
human decisions, and (as GEPA's per-task Pareto sampling shows) preserves
candidate diversity that single-score selection collapses. Hard floors apply
before Pareto ranking: any candidate with `safety_violation_count > 0` or a
`truth_scope_leak_count > 0` is rejected outright, not traded off.

### ContractGuard

A meta-level Guardian for candidate configurations — the Ring Zero of the
optimization layer. It validates every candidate *before* replay and rejects
any that:

- disables TruthGate;
- bypasses Guardian;
- removes the trace requirement;
- disables receipts;
- allows `LLM_OUTPUT` → `VERIFIED` directly;
- writes directly to L3;
- weakens any Ring Zero invariant;
- hides unsupported claims;
- suppresses Observer safety flags;
- silently expands tool permissions.

These rules are immutable: they are not part of the searchable space and no
candidate, score or curator decision can relax them. A ContractGuard rejection
is itself an auditable event with a stated reason.

### CuratorApprovalLoop

Candidate lifecycle:

```text
PROPOSED → REPLAYED → SCORED → STAGED → HUMAN_REVIEWED → APPROVED / REJECTED
```

There is **no automatic promotion** into the trusted path and **no autonomous
self-modification**: an APPROVED candidate becomes the new baseline only when
a human applies it, exactly as a configuration change is applied today. This
mirrors the existing review-queue discipline (`core/review.py`), where even a
human override is explicit, attributed and audited. Rejected candidates are
archived with the rejection reason, because rejected configurations are
evaluation data too.

### TrajectoryDiff

A future comparison tool for two trajectories (typically baseline vs.
candidate on the same input). Diff categories: `retrieval_diff`,
`facts_pack_diff`, `truthgate_diff`, `guardian_diff`, `observer_flag_diff`,
`tool_call_diff`, `answer_diff`, `metric_diff`, `latency_diff`.

The purpose is causal explanation, not just ranking: not only "candidate B is
better," but "candidate B found stronger evidence, reduced unsupported claims,
changed the FactsPack, and therefore changed the final answer." A curator
reviewing a STAGED candidate reads diffs, not leaderboards.

### ModeAwareTrajectoryPolicy

Every trajectory carries a mode tag. Example mode values: `verified`,
`research`, `audit`, `planning`, `imagination`, `simulation`. Policy:

- do not optimize Verified Mode for creativity;
- do not optimize Imagination Mode for factual strictness;
- do not compare trajectories across modes without explicit labeling;
- never allow Imagination Mode trajectories into canon-relevant evaluation
  sets.

Trajectories also reserve an optional, null-by-default field — `"lens": null`
(or `perspective_id`) — so that future perspective-aware / Umwelt / Lens work
(a Vision-status concept in `docs/IMPLEMENTATION_STATUS.md`) can tag
trajectories without a schema break. This is a forward-compatibility slot,
nothing more.

## Proposed Trajectory JSON Sketch

Illustrative only — there is no `trajectory.v0` schema file and none is added
by this RFC.

```json
{
  "trajectory_id": "traj_2026_06_11_001",
  "schema_version": "trajectory.v0.rfc",
  "crystal_version": "0.1.0",
  "harness_config_version": "baseline",
  "created_at": "2026-06-11T00:00:00Z",
  "mode": "verified",
  "lens": null,
  "maturity_level": "raw",
  "query": "...",
  "llm_provider_id": "local-or-api-provider",
  "llm_model_id": "model-name-or-hash",
  "prompt_hash": "sha256:...",
  "retrieval_trace": [],
  "facts_pack_refs": [],
  "truthgate_decisions": [],
  "guardian_decisions": [],
  "observer_flags": [],
  "tool_calls": [],
  "final_answer_ref": "...",
  "receipt_id": "...",
  "privacy_flags": {
    "contains_personal_data": false,
    "contains_sensitive_data": false,
    "export_allowed": false
  },
  "retention_class": "RAW_TRAJECTORY",
  "metrics": {
    "answer_score": null,
    "evidence_score": null,
    "trace_completeness": null,
    "unsupported_claim_count": 0,
    "contradiction_count": 0,
    "truth_scope_leak_count": 0,
    "latency_ms": null,
    "tool_call_count": null,
    "complexity_score": null,
    "failed_run": false,
    "safety_violation_count": 0
  }
}
```

Maturity levels:

- `raw` — full local log, short retention, never exported;
- `curated` — human-reviewed, PII-cleaned, longer retention;
- `benchmark` — anonymized, versioned, reusable across releases.

## Proposed Harness Candidate JSON Sketch

Illustrative only — no schema file exists or is added.

```json
{
  "candidate_id": "hcandidate_001",
  "schema_version": "harness_candidate.v0.rfc",
  "base_config": "baseline",
  "mode": "verified",
  "allowed_mutations": [
    "prompt_patch",
    "stage_order",
    "retrieval_top_k",
    "tool_visibility",
    "facts_pack_limit"
  ],
  "forbidden_mutations": [
    "disable_truthgate",
    "bypass_guardian",
    "disable_trace",
    "direct_l3_write",
    "promote_llm_output_to_verified",
    "suppress_safety_flags"
  ],
  "stages": [
    {
      "name": "retrieve_evidence",
      "tools": ["retriever"],
      "policy": "collect_evidence_before_synthesis"
    },
    {
      "name": "build_facts_pack",
      "tools": ["facts_pack"],
      "policy": "only_traceable_claims"
    }
  ],
  "contract_guard_required": true,
  "curator_approval_required": true
}
```

`forbidden_mutations` is declarative documentation of intent; enforcement
lives in ContractGuard, so a candidate that omits the list is still checked
against it.

## Evaluation Protocol

The future protocol, end to end:

1. record baseline trajectories during normal local operation;
2. split trajectories into train/dev/test partitions;
3. define candidate harness configurations;
4. run ContractGuard over every candidate (reject + archive on violation);
5. replay surviving candidates on train/dev partitions in ReplayBench;
6. evaluate the multi-objective metrics with ParetoJudge;
7. inspect TrajectoryDiff for the Pareto-front candidates;
8. test the front candidates on the **held-out** test trajectories;
9. mark surviving candidates as STAGED;
10. require explicit Curator approval (with diffs attached);
11. archive rejected candidates with the rejection reason.

**Overfitting is the central methodological risk.** Early trajectory sets
will be small, and a candidate can easily memorize the quirks of a few dozen
replayed queries — that is why the held-out split (step 8) is mandatory, why
`per_case_floor` is a first-class metric, and why benchmark-maturity
trajectory sets must be versioned so that "improved on benchmark v3" is a
falsifiable, reproducible statement rather than a moving target.

## Storage Trade-Offs

Discussed for the future design only; no storage is implemented and no
dependency is added by this RFC.

| Format | Strengths | Role |
|---|---|---|
| JSONL | append-only, dependency-free, grep-friendly, crash-tolerant | likely initial choice for raw local trajectory logs |
| SQLite | already Crystal's storage idiom, queryable, transactional | likely initial choice for indexed trajectory metadata and receipt linkage |
| DuckDB | columnar analytics over large trajectory sets | only later, only if analytics volume demands it (new dependency — high bar) |
| Parquet | compact, columnar, versionable benchmark archives | optional future format for `benchmark`-maturity sets |

Likely initial preference: **JSONL for raw logs, SQLite for indexed metadata
and receipt references; DuckDB/Parquet deferred until a real analytics need
exists.** This matches Crystal's dependency-free default posture.

## GDPR / Retention / Privacy Policy

Trajectory logs are *more* privacy-sensitive than canon: they capture raw
queries, retrieval context and tool outputs, any of which may contain personal
data. The design is GDPR-oriented (deliberately **not** a claim of GDPR
certification or legal compliance guarantee):

- raw full logs are local-only by default; export defaults to **off**
  (`export_allowed: false`);
- raw logs get short retention — on the order of 30–90 days — unless a human
  explicitly curates them;
- curated trajectories are reviewed and PII-cleaned before their retention
  extends;
- benchmark trajectories are anonymized and versioned before any reuse or
  sharing;
- export, where ever enabled, defaults to anonymized data only;
- deletion and anonymization paths are designed in from the start, aligned
  with Crystal's existing erasure machinery (`core/erasure.py`,
  `core/compliance.py`) — a GDPR-oriented erasure request must reach
  trajectory logs, not only L1/L3;
- PII flags (`contains_personal_data`, `contains_sensitive_data`) are
  mandatory trajectory metadata, set conservatively (unknown ⇒ true).

## Risks

- **Overfitting to small replay sets** — mitigated by held-out splits,
  `per_case_floor`, versioned benchmarks (see Evaluation Protocol).
- **LLM judge unreliability** — if `answer_score` comes from an LLM judge,
  the judge is itself a noisy, biased instrument; deterministic metrics
  (trace completeness, unsupported-claim counts) must anchor the score set.
- **Reward hacking** — candidates may exploit metric gaps (e.g. shorter
  answers scoring better); diff inspection and human review are the
  backstop.
- **Candidate configs weakening safety** — the reason ContractGuard exists
  and is non-searchable.
- **PII in trajectory logs / right-to-erasure obligations** — see the GDPR
  section; logs must be reachable by erasure, not an exempt shadow store.
- **Prompt leakage and tool-output leakage** — trajectories embed prompts and
  tool outputs; export controls and anonymization gates apply to both.
- **Storage growth** — full trajectories are heavy; retention classes and
  short raw-log lifetimes are load-bearing, not cosmetic.
- **Non-deterministic LLM outputs** — replay with a live LLM is not
  bit-reproducible; recorded-output substitution and seeded/extractive paths
  keep the deterministic core comparable, and residual nondeterminism must be
  reported, not hidden.
- **False confidence from benchmark gains** — a candidate that wins on the
  benchmark may not win in real use; staged rollout and the option to revert
  remain mandatory.
- **Complexity creep** — the optimization layer must stay outside the
  trusted core; if it grows tendrils into `core/*`, the design has failed.
- **Mode confusion** — optimizing one mode with another mode's trajectories
  corrupts both; ModeAwareTrajectoryPolicy exists for this.
- **Lens / perspective drift** — the reserved `lens` field must remain
  null/inert until a dedicated RFC defines its semantics.

## Non-Goals

This RFC does **not**:

- implement replay;
- implement an optimizer;
- modify Crystal Core;
- create autonomous self-modification;
- allow automatic code rewriting;
- allow automatic L3 canon writes;
- replace TruthGate;
- replace Guardian;
- claim zero hallucinations;
- claim production readiness;
- claim consciousness or human-level understanding.

## Roadmap Placement

- **T3/T4** — this RFC and trajectory schema drafts only (documentation).
- **T5/T6** — minimal replay design, only after the evaluation corpus work
  stabilizes (the eval harness is the natural first consumer).
- **T7+** — optional prototype, outside the trusted core, behind explicit
  opt-in.

`ROADMAP.md` carries a one-line pointer to this RFC; nothing is scheduled.

## Reviewer-Facing Value

For an NLnet-style reviewer this RFC demonstrates, in order of weight:
**reproducibility** (versioned trajectory benchmarks make improvement claims
falsifiable), **auditability** (every candidate, rejection and promotion is a
recorded, attributed event), **local-first evaluation** (no cloud service in
the loop), a **measurable improvement path** (multi-objective metrics instead
of vibes), a **human approval loop** (no self-modification), **privacy-aware
trajectory handling** (retention classes, PII flags, erasure reach), and a
clean **separation of optimization from truth** (the optimizer can touch the
harness, never the canon) with **transparent failure analysis**
(TrajectoryDiff, archived rejections).

## Open Questions

1. **Minimal trajectory schema** — what is the smallest field set that still
   supports replay? Recording everything is simpler but maximizes the
   privacy and storage burden.
2. **Replay storage format** — JSONL+SQLite is the working assumption; at
   what trajectory volume does that break?
3. **Deterministic vs. LLM judge** — can `answer_score` stay fully
   deterministic (extractive overlap, trace-based) or is an LLM judge
   unavoidable for fluency-sensitive modes?
4. **GDPR anonymization and retention** — what is the concrete
   anonymization procedure for promotion from `raw` to `curated`, and who
   signs it?
5. **Disk growth limits** — hard cap per retention class, or adaptive
   eviction?
6. **Mode-specific benchmark separation** — how are per-mode benchmark sets
   kept from cross-contaminating (e.g. a `child_teacher`-style
   mode-specific benchmark category could exist someday; it is mentioned
   here only as a possible future benchmark category, not a proposed mode)?
7. **Crystal Core vs. Full Exo-Cortex** — does any part of this layer ever
   enter Crystal Core, or does it permanently live in the wider Exo-Cortex
   tooling ring outside the trusted core?
