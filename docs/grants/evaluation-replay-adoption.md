# 🧪 Evaluation Replay Adoption Decision — Crystal

**Status:** `REVIEWED_PRIOR_ART · DOCUMENTED_ONLY · M4_CANDIDATE · NO_RUNTIME_CHANGE`  
**Decision date:** 2026-07-30  
**Crystal baseline:** `cd6fd44ff4ac8c715121cae1996aa484f11ef250`  
**Grant effect:** no new milestone, amount, budget item or implementation claim

## Decision

Titan's deterministic replay and baseline/fork/diff work has been reviewed as
useful prior art. It is **not** copied into Crystal runtime by this change.

Crystal already has:

- `core/eval.py` and `scripts/eval_gate.py`;
- curated retrieval, contradiction and trust-boundary fixtures;
- stable CI floors and ceilings;
- `metrics.jsonl` and human-readable evaluation reports;
- receipt replay;
- the broader future design in `docs/RFC_HARNESS_REPLAY_OPTIMIZATION.md`.

The safe path is therefore to extend the existing Crystal evaluation stack in
small reviewed slices rather than introducing a parallel Titan evaluator.

## Grant interpretation

This decision does not move the baseline and does not reduce or silently consume
the proposed funded delta.

```text
Current state:
  architecture reviewed
  grant-safe boundary documented
  no runtime implementation

Potential funded M4 delta after baseline freeze:
  versioned evaluation manifests
  deterministic baseline-versus-candidate comparison
  structural regression evidence
  release quality trends
```

Already-merged Titan work is not presented as a Crystal deliverable. A future
Crystal implementation may reuse general engineering patterns, but it must be
written and evaluated against Crystal's own contracts, privacy model and
acceptance evidence.

## Allowed future slices

### 1. Versioned evaluation manifest

A run may record content-light, deterministic metadata such as:

- Crystal commit or release;
- fixture package version and digest;
- evaluation configuration digest;
- embedder identity;
- deterministic seed where relevant;
- metric schema version;
- output artifact digests.

Timestamps and human labels must not alter semantic run identity.

### 2. Baseline-versus-candidate structural diff

A future offline evaluator may compare:

- retrieval ranks and evidence coverage;
- FactsPack composition;
- refusal reason codes;
- trace and receipt completeness;
- contradiction outcomes;
- route/config selection;
- latency and bounded resource counts.

The comparison explains *why* behaviour changed; it does not gain authority over
TruthGate, Canon or production configuration.

### 3. Non-negotiable safety gates

Candidate evaluation must fail when any run reports:

```text
truth_gate_bypass_count > 0
query_path_write_count > 0
unrecorded_external_call_count > 0
restricted_or_erased_data_exposure_count > 0
silent_temporal_rewrite_count > 0
```

Metrics may not average away a high-risk individual regression. Per-case floors
and explicit blocker counts remain visible.

### 4. Release-versioned evidence

A future funded implementation may publish:

- versioned fixture manifests;
- machine-readable baseline/candidate diffs;
- release-linked evaluation reports;
- documented calibration and threshold changes;
- deterministic reproduction commands.

These outputs fit the existing M4 acceptance model without creating a new work
package.

## Deferred and excluded now

The following are not part of this synchronization and require separate privacy,
security and grant review:

- live recording of user queries or conversations;
- raw prompt, chain-of-thought or tool-output capture;
- production trajectory storage;
- provider calls from the evaluator;
- an LLM judge as a mandatory gate;
- automatic configuration promotion;
- autonomous optimization or code rewriting;
- direct Canon, L1, L3, ESM or outbox mutation;
- temporal-claim schema changes;
- procedural-skill or plugin runtimes;
- Titan Native Kernel integration.

## Privacy boundary

Offline fixtures and generated synthetic cases are preferred. Any later use of
real execution records requires, before implementation:

- purpose and lawful-basis review;
- explicit retention classes;
- conservative personal-data flags;
- export disabled by default;
- anonymization/curation rules;
- erasure propagation into replay storage;
- threat model and access controls;
- separate operator approval.

No hidden chain-of-thought should be stored or required. Replay evidence should
capture inspectable inputs, outputs, decisions, references and metrics instead.

## Authority boundary

```text
Evaluator may measure.
Evaluator may compare.
Evaluator may block a candidate from passing CI.
Evaluator may not write Canon.
Evaluator may not weaken TruthGate or Guardian.
Evaluator may not promote itself or a candidate into production.
```

Human review and an ordinary Crystal pull request remain mandatory for any future
configuration or runtime adoption.

## Relationship to existing RFC

`docs/RFC_HARNESS_REPLAY_OPTIMIZATION.md` remains the broad research RFC for
trajectory recording, ReplayBench, ContractGuard, Pareto comparison and curator
approval.

This decision record is narrower:

- it defines what may safely count as the next Crystal evaluation increment;
- it maps that increment to the existing grant M4 boundary;
- it prevents Titan prior art from being mistaken for implemented Crystal code;
- it explicitly postpones privacy-heavy trajectory capture.

## Promotion gates

Any implementation requires all of the following:

1. grant baseline commit or release formally recorded;
2. a Crystal-specific RFC or implementation issue;
3. explicit schema and privacy review;
4. offline, deterministic default behaviour;
5. no mandatory dependency or provider addition;
6. tests and the 100% coverage gate;
7. eval-gate and security checks;
8. independent review;
9. a separate pull request;
10. maintainer approval and post-merge documentation synchronization.

## Reviewer-safe wording

> Crystal already provides a deterministic evaluation and regression-gate
> baseline. Future funded work may add versioned baseline-versus-candidate
> comparison and structural regression evidence while preserving the existing
> TruthGate, local-first and no-Canon-write boundaries.

Do not use wording that claims Crystal already contains Titan's replay framework,
self-improvement, live trajectory recording or automatic optimization.
