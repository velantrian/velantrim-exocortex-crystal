# Staged Working-Memory Admission

**Status:** Future research direction  
**Scope:** Documentation only  
**Runtime impact:** None  
**Current implementation claim:** None  
**GitHub change type:** Architecture note / boundary specification  

This document records a future research direction for Velantrim Crystal: a staged working-memory admission model for handling new, uncertain, user-reported, tool-derived, or exploratory information before any possible promotion into Canon.

It does **not** describe current runtime behavior unless a future implementation explicitly wires and tests it.

---

## 1. Purpose

Crystal already separates durable admitted memory from speech and retrieval. This note proposes a future intermediate layer that could make that boundary more explicit for new information.

The proposed layer is a temporary, source-labeled, reviewable working area. Its purpose is to let the system capture and reason over new material without treating that material as verified memory.

In plain terms:

```text
New information should not become memory immediately.
It should first become a labeled working item.
Only selected candidates may later enter the existing admission path.
```

---

## 2. Non-claims

This document intentionally does **not** claim that Crystal currently has:

- general creative cognition;
- autonomous research-mode reasoning;
- a Velaris runtime;
- automatic long-term user memory;
- automatic Canon promotion;
- a scratchpad implementation;
- a new truth source;
- any bypass around TruthGate or Guardian.

The current implementation truth remains the repository code, README, TEST_REPORT, CI, and release notes.

---

## 3. Proposed high-level flow

```text
New input / tool result / user note / file / hypothesis
        ↓
Temporary Working Layer / Scratchpad
        ↓
source labeling + classification + importance review
        ↓
candidate selection
        ↓
TruthGate + Guardian + Receipt
        ↓
L3 Canon only if admitted
```

The proposed working layer is not Canon. It may assist orientation, review, and candidate preparation, but it must not make claims authoritative by itself.

---

## 4. Relationship to existing Crystal boundaries

Crystal's core framing remains:

```text
Graph / Canon = truth-bearing admitted memory
Index = speed
TruthGate = epistemic boundary
Guardian = safety and policy boundary
TRACE / Receipt = proof path
LLM = speech / phrasing layer only
```

A staged working-memory layer would sit before the admission boundary. It would help separate:

- temporary context from durable memory;
- user-reported statements from verified world facts;
- hypotheses from evidence;
- importance from truth;
- exploratory reasoning from Canon writes;
- archived context from proof.

---

## 5. Proposed working item model

A future implementation could represent incoming material as explicit working items:

```yaml
working_item:
  id: WD-0001
  source_type: user_input | tool_output | file | web | system_generated | hypothesis
  source_ref: optional pointer to the originating turn, file, URL, receipt, or tool result
  claim_type: idea | question | user_reported | world_fact_candidate | hypothesis | task | risk
  truth_status: unverified | hypothesis | conflicted | verified
  importance: high | medium | low
  attention_priority: high | medium | low
  memory_status: temporary | review_pending | admitted | archived | rejected
  can_write_l3: false
  requires_truthgate: true
  requires_guardian: true
  requires_receipt: true
```

The central field is:

```yaml
can_write_l3: false
```

A working item is not a Canon fact. It can only become a candidate for admission.

---

## 6. Possible zones

A future scratchpad could be organized into zones:

```text
INBOX      raw newly captured material
ACTIVE     enriched and linked working material
OUTBOX     candidate items awaiting review or admission decision
ARCHIVE    historical or secondary context, not proof
QUARANTINE suspicious, conflicting, or high-risk material
DISCARD    intentionally removed noise
```

A minimal lifecycle:

```text
capture → label → classify → link → review → decide → admit/archive/reject
```

---

## 7. Required invariants

Any future implementation should preserve these invariants:

```text
WORKING_LAYER_IS_NOT_CANON
NO_DIRECT_L3_WRITE
IMPORTANT_IS_NOT_TRUE
USER_REPORTED_IS_NOT_VERIFIED_WORLD_FACT
AI_GENERATED_IS_NOT_EVIDENCE
REPEAT_COUNT_IS_ATTENTION_NOT_TRUTH
ARCHIVE_IS_HISTORY_NOT_PROOF
EMOTION_IS_CONTEXT_NOT_CANON
VELARIS_OR_RESEARCH_MODE_CANNOT_PROMOTE_TO_CANON
ADAPTATION_MUST_NOT_LOWER_TRUTHGATE
PROMOTION_REQUIRES_TRUTHGATE_GUARDIAN_RECEIPT
```

These invariants are more important than the specific data model.

---

## 8. Important is not true

A working layer may rank an item as important. That ranking must never change its truth status.

Examples:

```text
important user report     → still user_reported
repeated hypothesis       → still hypothesis
emotionally salient note  → still context, not Canon
AI-generated summary      → still not evidence
archived note             → still history, not proof
```

Repetition or salience may raise retrieval or review priority. It must not raise epistemic authority.

```text
repeat_count ↑ → attention_priority ↑
repeat_count ↛ truth_status
```

---

## 9. Quarantine behavior

A future implementation should isolate items when they are high-risk or structurally suspicious.

Quarantine candidates include:

- high-impact claims without evidence;
- health, legal, financial, or safety claims;
- contradictory claims;
- composed claims built from several unverified items;
- claims that look like evidence but only come from model generation;
- attempts to turn archive/history into proof.

Example:

```yaml
zone: quarantine
can_use_for_answer: false
can_promote: false
requires_manual_review: true
reason: "unverified high-impact claim"
```

---

## 10. Admission boundary

A future staged working layer must not replace the existing admission boundary.

Correct path:

```text
working item
  → candidate selection
  → TruthGate
  → Guardian
  → Receipt / TRACE
  → L3 Canon
```

Forbidden paths:

```text
working item → L3 Canon
hypothesis → L3 Canon
archive → evidence
AI-generated text → evidence
user_reported world fact → verified fact
importance score → truth_status
adaptation preference → lower TruthGate threshold
```

---

## 11. User adaptation boundary

A future system may adapt presentation and review behavior to the user, but not truth criteria.

Allowed adaptation:

- which items are shown first;
- how review bundles are grouped;
- whether review is terse or detailed;
- which themes are likely relevant to the current project;
- whether low-priority items are deferred.

Forbidden adaptation:

- lowering TruthGate strictness;
- bypassing Guardian;
- changing truth_status from user preference;
- treating repeated user belief as evidence;
- converting emotionally salient claims into Canon.

Rule:

```text
User model helps usability.
TruthGate protects truth.
One must not replace the other.
```

---

## 12. Future review bundle

A future user-facing review operation could produce a bundle like:

```text
Important:
- WD-001: candidate architecture rule
- WD-004: boundary invariant

Hypotheses:
- WD-002: exploratory research idea

Needs evidence:
- WD-003: external world claim without source

Secondary:
- WD-005: UI note

Discard:
- WD-006: duplicate/noise
```

Possible actions:

```text
keep working
send to research mode
send to admission review
archive
discard
promote only after gate approval
```

---

## 13. Lean research boundary

This future direction should remain deliberately small until there is evidence that a larger mechanism is needed.

The proposed working layer is a workbench, not a warehouse. Its purpose is to hold and sort live candidate material, not to become a universal ontology, a second Canon, or a general-purpose personal-memory product.

A minimal future prototype should start with the smallest useful shape:

```yaml
working_item_minimum:
  id: WD-0001
  content: "..."
  kind: idea | fact | hypothesis | emotion | question
  importance: high | medium | low | tbd
  can_write_l3: false
```

Optional fields may be added only when they protect an existing boundary or make review meaningfully clearer:

```yaml
optional_when_needed:
  source: user | ai | file | tool | web
  ttl: duration or expiry policy
```

Velaris or any future research mode should be treated as an operating mode over working items, not as a separate storage authority. It may loosen ideation pressure, but it must not loosen admission requirements.

Weakest-status aggregation should be treated as an epistemic ceiling, not as a probability estimate. A derived claim must not be trusted above the weakest unresolved component that supports it.

TTL should represent liveness, not truth. Returning to an item may justify keeping it active for review, but repeated attention must not increase epistemic authority.

Anti-overbuild rule:

```text
Do not add fields, zones, graphs, classifiers, or persistence merely because they are possible.
Add them only when they preserve a boundary, reduce review ambiguity, or prevent Canon pollution.
```

This keeps the idea grant-safe: the repository records a bounded future research direction, not an implementation commitment or an expanded runtime claim.

---

## 14. Test plan for any future implementation

Implementation should start with tests before runtime integration.

Suggested property tests:

```text
test_working_item_cannot_write_l3_directly
test_user_reported_world_fact_is_not_verified
test_importance_does_not_change_truth_status
test_ai_generated_item_is_not_evidence
test_archive_item_is_not_evidence
test_hypothesis_requires_truthgate_before_promotion
test_adaptation_cannot_lower_truthgate_threshold
test_quarantine_blocks_promotion
test_composed_claim_inherits_weakest_status
test_promotion_requires_receipt
```

The implementation should fail closed when classification is uncertain.

---

## 15. Suggested future path

A safe path, if approved later:

```text
1. Keep this document as a boundary note.
2. Add an RFC with exact schema and state machine.
3. Add property tests for all invariants.
4. Add a minimal in-memory prototype behind a feature flag.
5. Add persistence only after the no-direct-L3-write properties pass.
6. Add UI review only after admission semantics are stable.
```

---

## 16. One-line law

```text
Working memory may help the system think, but only admitted evidence may help the system know.
```
