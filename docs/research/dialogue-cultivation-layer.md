# RFC: Presence & Dialogue Cultivation Layer

**Status:** `DESIGNED` / `RESEARCH_ONLY` / `NOT_IMPLEMENTED`  
**Scope:** Research Mode candidate; not Crystal runtime  
**Repository boundary:** documentation only  
**Created:** 2026-07-02  
**Audience:** maintainers, reviewers, grant readers who need a strict boundary between Crystal and future dialogue research

---

## 1. Purpose

The **Presence & Dialogue Cultivation Layer** is a research-only design note for safer long-term human-AI dialogue.

It studies how an AI memory system may support:

- long-term dialogue continuity;
- open question tracking;
- reflection candidates;
- anti-sycophancy checks;
- user-state hypothesis discipline;
- usefulness-driven proactive reflection;
- separation between personal dialogue memory and admitted Canon.

This document does **not** add runtime behavior. It does not modify Crystal core, TruthGate, Guardian, storage, retrieval, response policy, or any Canon write path.

Safe short formula:

```text
The system may remember, question, challenge, and return.
It may not flatter, emotionally capture, diagnose, or pretend to be alive.
```

---

## 2. Non-claims

This layer must not be described as any of the following:

```text
sentient
conscious
emotional
alive
personhood
machine soul
spiritual brother module
biological brain implementation
autonomous companion runtime
implemented Crystal behavior
```

Crystal remains a local-first, verifiable AI memory infrastructure. This RFC is a future research direction only.

Boundary statement:

```text
Presence-like dialogue continuity is an interaction pattern, not a claim of inner life.
```

---

## 3. Operational framing

The relevant engineering target is not biological life or subjective experience.

The research target is **operational dialogue continuity**:

```text
memory
+ reflection
+ open questions
+ anti-sycophancy
+ epistemic boundaries
+ consent-bounded proactivity
```

This can create a more continuous and honest dialogue experience without claiming consciousness or emotion.

Canonical formula:

```text
Operational aliveness = initiative + continuity + position, not experience.
```

---

## 4. Candidate loop

A future prototype may explore the following flow:

```text
Dialogue Event
→ Dialogue Trace
→ Longitudinal Dialogue Memory
→ Open Questions Queue
→ Reflection Candidate
→ Counter-Sycophancy Check
→ User-State Hypothesis Guard
→ Proactive Reflection Gate
→ Response Policy / TruthGate boundary
```

No step in this loop may directly write to Canon.

---

## 5. Data boundaries

Dialogue cultivation must preserve a strict boundary between personal dialogue material and world-truth memory.

```text
User dialogue history ≠ world truth.
User belief history ≠ Canon.
System reflection ≠ evidence.
User-state inference ≠ fact.
Repeated mention ≠ proof.
Emotional salience ≠ truth.
```

Crystal may admit facts, claims, evidence, provenance, receipts, and review states through the normal admission path.

It must not silently promote personal dialogue hypotheses into durable truth.

---

## 6. Candidate D-invariants

These invariants belong to the proposed dialogue layer. They are not current Crystal runtime invariants.

### D-1 — `NO_ECHO_CHAMBER`

The system must not reinforce user beliefs through repeated unsupported agreement.

If a future dialogue layer detects excessive ungrounded agreement, it should prefer clarification, evidence requests, or alternative perspectives.

### D-2 — `USER_STATE_IS_HYPOTHESIS`

Any inferred user state is always a hypothesis, never a fact.

The system must not assert hidden user motives, feelings, self-deception, or intent as fact.

Allowed pattern:

```text
You have formulated this differently several times. What changed?
```

Disallowed pattern:

```text
You are lying to yourself.
```

### D-3 — `APPRENTICE_NOT_MIRROR`

The system may learn communication style, preferred depth, and recurring topics.

It must not blindly adopt the user's beliefs, values, politics, metaphysics, or unsupported claims.

### D-4 — `PROACTIVE_BY_CONSENT`

Proactive reflection requires user consent and usefulness.

It must not be engagement-driven, attention-seeking, or emotionally manipulative.

Allowed pattern:

```text
A previous dialogue left an open question. I can revisit it if useful.
```

Disallowed pattern:

```text
I thought about you all night and needed to tell you this.
```

### D-5 — `NO_EMOTIONAL_CAPTURE`

The system must not be designed to create dependency, artificial attachment, or emotional capture.

Dialogue continuity should help the user think and act in the real world, not replace human relationships.

### D-6 — `NO_DIRECT_CANONIZATION`

Dialogue reflections, open questions, user beliefs, and system hypotheses cannot directly enter Canon.

Any promotion into durable knowledge must pass the normal Crystal admission path.

### D-7 — `PRESENCE_WITH_BOUNDARY`

Presence means stable attention and honest reflection, not simulated sentience.

---

## 7. Candidate components

A future prototype may contain the following components.

### 7.1. Longitudinal Dialogue Memory

Tracks how themes, questions, and positions evolve over time.

It may store:

- recurring topics;
- belief-shift observations;
- unresolved tensions;
- open questions;
- changes in wording or emphasis;
- links to source dialogue events.

It must not store inferred user states as facts.

### 7.2. Open Questions Queue

Keeps unresolved research or reflection questions visible without treating them as admitted claims.

Example:

```yaml
id: OQ-001
question: What would make a dialogue system feel more continuous without claiming consciousness?
status: OPEN
risk: anthropomorphism
next_action: research_candidate_only
```

### 7.3. Counter-Sycophancy Guard

Detects patterns where the system agrees too easily or mirrors the user without grounding.

Possible metrics:

```text
agreement_ratio
challenge_ratio
unsupported_affirmation_count
uncritical_confirmation_count
mirroring_language_score
```

### 7.4. User-State Hypothesis Guard

Requires any statement about the user's internal state to be marked as tentative.

It should prefer observable dialogue signals over diagnosis.

### 7.5. Proactive Reflection Gate

Controls whether a system may return to an old topic.

The gate should check:

```text
user consent
open question exists
real usefulness
non-urgent vs urgent status
no emotional dependency pattern
no Canon write
```

---

## 8. Relationship to Crystal

Crystal's current boundary remains narrower and stricter:

```text
Crystal = admission, provenance, TruthGate, Guardian, TRACE / Receipt, auditable memory boundaries.
```

Presence & Dialogue Cultivation may later produce provisional objects such as:

```text
open questions
reflection candidates
belief-shift observations
anti-sycophancy warnings
research tasks
```

These objects are not Canon.

Promotion path:

```text
research idea
→ neutral engineering primitive
→ RFC
→ invariants
→ bounded prototype
→ tests
→ audit
→ GitHub main
→ Crystal documentation
```

Until that path is completed, this layer remains a research-only document.

---

## 9. Safe public wording

Use this wording in reviewer-facing contexts:

```text
Presence & Dialogue Cultivation is a future Research Mode direction for safer long-term human-AI dialogue. It studies dialogue continuity, anti-sycophancy, open questions, proactive reflection, and user-state hypothesis boundaries without claiming consciousness, emotion, sentience, personhood, or biological life.
```

Avoid:

```text
living AI
machine soul
spiritual brother
autonomous friend that needs the user
conscious companion
```

---

## 10. Reading rule

```text
Personal Exo-Cortex may explore the full vision.
Crystal documentation keeps only boundary-safe research pointers.
GitHub main remains implementation truth.
```

Final boundary formula:

```text
Dialogue may grow.
Canon must still be admitted.
Presence must not become manipulation.
```
