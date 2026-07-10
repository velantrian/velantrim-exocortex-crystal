# Cognitive State and Planning Layers

**Status:** `RESEARCH / DOCUMENTED_ONLY`  
**Runtime impact:** none  
**Crystal Core impact:** none  
**Grant status:** not a current deliverable  
**Canon writes:** none  
**Promotion rule:** one neutral primitive per RFC and implementation PR

> This document records five Full Exo-Cortex research candidates in a
> reviewer-safe engineering form. It does **not** describe implemented Crystal
> runtime behaviour.

## Boundary

```text
Personal Research Mode = broad experimental architecture.
Crystal research docs = neutral candidate contracts and safety boundaries.
prototypes/research_mode = bounded, non-runtime data contracts and validators.
Crystal core = only separately implemented, tested, audited and status-synced work.
```

The fixed rule is:

```text
Research Mode may explore and propose.
Crystal may admit only bounded, tested and auditable primitives.
No research candidate may write directly to Canon or bypass TruthGate / Guardian.
```

## Candidate map

| Research concept | Crystal-safe name | Intended value | Primary risk | Status |
|---|---|---|---|---|
| Formal World Model | `CurrentStateProjection` | Separate current state from historical records | A second truth authority beside Canon | Research only |
| Self-Model | `CapabilitySnapshot` | Record actual tools, permissions and module health | Misleading consciousness or self-authority claims | Research only |
| Success Motif Memory | `StrategyOutcomeRecord` | Preserve reproducible successful methods and their limits | Self-confirming accidental success | Research only |
| General Planner | `BoundedPlan` / `PlanContract` | Machine-readable steps, dependencies and recovery | Scope creep into autonomous-agent runtime | Research only |
| User / Theory-of-Mind Model | `UserIntentHypothesis` / `InteractionContext` | Separate explicit user statements from system inference | Profiling, privacy and false psychological claims | Research only |

---

## 1. `CurrentStateProjection`

### Purpose

A read-only projection of the currently applicable state of an entity, project
or process, derived from traceable events, admitted claims and temporal
metadata.

It answers:

```text
What state is currently active?
What state was active before it?
Which event or admitted claim supports the transition?
Are there competing or contradictory candidate states?
```

It is **not**:

- a second Canon;
- an automatic world-truth engine;
- a replacement for L3;
- a prediction promoted as observation;
- permission to treat the latest record as the truest record.

### Minimal candidate contract

```text
CurrentStateProjection {
  entity_ref
  state_key
  candidate_value
  effective_from
  effective_until
  evidence_refs
  event_refs
  claim_status
  competing_state_refs
  generated_at
}
```

### Invariants

```text
Projection derives; it does not self-canonize.
Every projected state must be reconstructable from admitted claims and
traceable events.
Prediction, salience and recency are not evidence.
A conflicting state must be preserved, not silently overwritten.
```

### Dependencies

- Event Ledger / audit history;
- claim versioning and supersession;
- temporal policy;
- contradiction handling;
- provenance and receipts;
- TruthGate admission status.

### Candidate metrics

- temporal consistency;
- unsupported state mutation rate;
- version-separation accuracy;
- conflict-preservation rate;
- reconstruction success rate.

---

## 2. `CapabilitySnapshot`

### Purpose

A formal read-only record of what the system can actually do at the current
moment, which tools are available, which permissions apply and whether relevant
modules are healthy.

```text
CapabilitySnapshot {
  system_version
  runtime_mode
  active_modules
  available_tools
  unavailable_tools
  permissions
  action_limits
  memory_health
  retrieval_health
  pending_failures
  resource_budget
  last_self_check
}
```

This is engineering self-diagnostics, not a consciousness or personhood claim.

### Why it matters

Without an explicit capability state, an LLM may blur:

- a planned action and a completed action;
- a possible tool and an actually available tool;
- a generated promise and a successful storage write;
- technical ability and policy permission;
- stale memory and verified current state.

### Invariants

```text
A declared capability must be backed by an actual module or tool.
CapabilitySnapshot cannot expand its own permissions.
A planned action cannot be reported as completed.
A generated statement is not an observation.
Degraded memory or retrieval state must remain visible to routing and response policy.
```

### Candidate metrics

- capability-claim accuracy;
- false completion rate;
- permission-compliance rate;
- degraded-state detection rate;
- false tool-use claim rate.

---

## 3. `StrategyOutcomeRecord`

### Purpose

Record a strategy used in a defined context together with a measurable outcome,
verification references, reuse conditions and known failure boundaries.

```text
StrategyOutcomeRecord {
  strategy_id
  strategy_name
  problem_pattern
  context_conditions
  steps
  tool_refs
  outcome_metrics
  verifier_refs
  reuse_conditions
  exclusion_conditions
  failure_boundaries
  occurrence_count
  status
  last_confirmed_at
}
```

The record is the neutral engineering form of a broader Success Motif Memory
concept.

### Promotion path

```text
single successful run
→ SUCCESS_CANDIDATE
→ repeated success in comparable contexts
→ metric review
→ reusable strategy candidate
→ optional procedural-memory RFC
```

### Invariants

```text
User praise is not evidence of task success.
Fluent output is not a successful outcome.
A strategy is reusable only inside tested context boundaries.
A strategy record does not receive VERIFIED world-fact status.
Negative transfer must be measured and preserved.
```

### Candidate metrics

- reproducibility;
- strategy-reuse success rate;
- context-match accuracy;
- negative-transfer rate;
- measured improvement over baseline.

---

## 4. `BoundedPlan` / `PlanContract`

### Purpose

Represent a plan as an inspectable and machine-readable structure rather than a
free-form textual suggestion.

```text
PlanContract {
  plan_id
  goal_ref
  user_intent_ref
  state_projection_ref
  assumptions
  constraints
  steps
  dependencies
  permissions
  resource_budget
  success_criteria
  stop_conditions
  recovery_policy
  status
  created_at
  revised_at
}

PlanStep {
  step_id
  action_type
  inputs
  tool_requirement
  preconditions
  expected_output
  verification_method
  risk_level
  reversible
  approval_required
  status
  result_ref
}
```

### Authority separation

```text
Planner proposes.
Guardian permits or blocks.
Tool layer executes.
Verifier confirms outcomes.
TruthGate governs claims produced by the process.
```

### Safe initial scope

- dry-run by default;
- no background autonomy;
- read-only or reversible operations first;
- no self-generated mission;
- no irreversible action without explicit approval;
- no direct Planner-to-Canon path.

### Candidate metrics

- goal-completion rate;
- dependency-violation rate;
- premature-completion rate;
- recovery success rate;
- unauthorized-action attempt rate;
- replanning quality.

---

## 5. `UserIntentHypothesis` / `InteractionContext`

### Purpose

Keep a strict distinction between what a user explicitly said, what the user
confirmed, and what the system merely inferred about a goal or context.

```text
UserIntentHypothesis {
  hypothesis_text
  confidence
  evidence_turn_ids
  confirmation_status
  expires_at
  sensitivity_level
}
```

Suggested origin labels:

```text
EXPLICIT_USER_STATEMENT
USER_CONFIRMED
SYSTEM_INFERENCE
IMPORTED_SOURCE
TEMPORARY_CONTEXT
```

### Invariants

```text
A system inference is not a fact about the user.
Sensitive inferences are not durable by default.
No hidden psychological diagnosis or personality typing.
The user must be able to correct or remove an inference.
High-impact action requires explicit consent or authority.
Data minimization applies to every durable field.
```

### Relation to GoalState / GapGate

```text
low goal confidence → ask
hard blocker → ask
soft ambiguity → refine
high confidence + reversible low-risk action → act
high-risk or irreversible ambiguity → ask
```

### Candidate metrics

- goal-inference accuracy;
- explicit-versus-inferred separation;
- correction responsiveness;
- unwanted-personalization rate;
- consent compliance;
- sensitive-inference retention rate.

---

## Combined flow

```text
UserIntentHypothesis
→ GoalState / GapGate
→ CurrentStateProjection
→ CapabilitySnapshot
→ BoundedPlan
→ action and verification
→ StrategyOutcomeRecord
```

| Question | Candidate |
|---|---|
| What did the user explicitly request, and what is only inferred? | `UserIntentHypothesis` |
| What is the currently applicable state? | `CurrentStateProjection` |
| What can the system actually do now? | `CapabilitySnapshot` |
| How can the task be executed within policy and resource limits? | `BoundedPlan` |
| Which method produced a verified, repeatable result? | `StrategyOutcomeRecord` |

## Explicit non-goals

```text
No AGI, consciousness, sentience or personhood claim.
No autonomous identity rewriting.
No self-preservation objective.
No unrestricted artificial drives.
No hidden user profiling.
No prediction-to-truth promotion.
No research-module direct writes to Canon.
No bypass of TruthGate, Guardian, provenance, receipts or human review.
```

Risk, novelty, success and resource-load signals may exist only as transparent
policy inputs to salience, planning, telemetry and Guardian review. They must not
become hidden objectives or truth signals.

## Threat model summary

| Threat | Required mitigation |
|---|---|
| Projection becomes a competing truth store | Derive read-only from traceable admitted inputs |
| Snapshot grants itself new powers | Permissions are externally supplied and immutable to the snapshot |
| Successful-looking output becomes a reusable strategy | Require verifier-backed outcome metrics and comparable repetitions |
| Planner expands into unbounded autonomy | Dry-run/reversible scope, capability checks, approval gates |
| User inference becomes profiling | Explicit/inferred labels, expiry, minimization, correction and deletion |
| Research language is read as runtime truth | `RESEARCH / DOCUMENTED_ONLY` status in file and PR |

## Promotion path

```text
research source
→ Crystal boundary note
→ neutral primitive
→ separate RFC
→ schema, invariants and threat model
→ behavioural emulator
→ bounded prototype under prototypes/research_mode/
→ tests and evaluation
→ security/privacy review
→ implementation PR
→ merge to main
→ STATUS / IMPLEMENTATION_STATUS / TEST_REPORT sync
→ only then a possible runtime or grant-safe claim
```

Each candidate must be promoted independently. A single PR that introduces all
five into `core/` would be scope creep and should be rejected.

## Final reading rule

```text
Remember with proof.
Represent current state without creating a second truth.
Describe capability without claiming consciousness.
Plan within permission.
Learn from measured outcomes.
Model user intent as a revisable hypothesis.
```

Current Crystal behaviour remains defined by code and tests on `main`,
`TEST_REPORT.md`, `docs/STATUS.md`, and implementation-status documentation.