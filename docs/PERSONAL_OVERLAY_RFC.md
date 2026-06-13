# Personal Overlay RFC v0.1

Status: Future RFC / private-application layer / not current Crystal runtime.

This document defines a future **Personal Overlay** layer for Velantrim ExoCortex. It is intentionally kept outside the grant-facing Crystal runtime boundary. The goal is to describe how a personal deployment may represent user-specific context without turning private memory into world truth and without storing sensitive raw identifiers in a public repository.

## Purpose

Crystal provides the verifiable memory core: provenance, typed claims, TruthGate, Guardian boundaries, TRACE and receipts.

The Personal Overlay is different. It describes what matters to a specific user or deployment: active projects, preferences, private constraints, redacted document context, health/admin caution flags and identity anchors.

```text
Crystal Core = what can be trusted.
Personal Overlay = what matters to this user.
```

## Current scope

This RFC is documentation and schema only.

It does not add runtime personal memory. It does not add real private data. It does not change the TruthGate, Guardian, receipt verification, L3 writes, review queue or ingestion semantics.

## Non-goals

- No real user data in the repository.
- No passport, national ID, tax ID, address, signature, account number or other sensitive identifier.
- No hidden profiling.
- No automatic promotion of personal context into `WORLD_FACT`.
- No bypass of TruthGate or Guardian.
- No medical, legal or financial conclusions from personal context.
- No cloud sync, telemetry or outbound calls.

## Core rule

```text
Personal context can guide attention, style and priority.
Personal context cannot replace evidence.
```

A user preference can decide how an answer should be phrased. A private legal or health context can trigger caution. Neither can make an unsupported factual claim true.

## Sensitivity levels

| Level | Meaning | Handling |
|---|---|---|
| `public` | Safe project or documentation context | May be used normally |
| `private` | User goals, preferences, identity anchors | Use only when relevant |
| `sensitive` | Health, legal, document, financial or family context | Minimize; do not expose unless needed |
| `highly_sensitive` | Document numbers, full addresses, signatures, government IDs, account secrets | Do not store in this layer; use redacted pointers only |

## Allowed record types

| Type | Purpose |
|---|---|
| `PersonProfile` | High-level non-sensitive identity context |
| `IdentityAnchor` | Stable user-specific anchor such as working language or long-term project |
| `ProjectNode` | Active or historical project context |
| `GoalNode` | User goal or task direction |
| `PreferenceNode` | Style, language or workflow preference |
| `ConstraintNode` | User-specific constraint or caution |
| `HealthContext` | Redacted health-related context requiring caution |
| `LegalContext` | Redacted legal/admin context requiring caution |
| `DocumentPointer` | Metadata-only pointer to an external private document |
| `EmotionalContext` | Subjective state or meaning note, not a world fact |
| `CultureContext` | Cultural/symbolic context, separated from factual claims |
| `RiskFlag` | Local caution flag for response planning |
| `KnownUnknown` | Explicit personal-context gap requiring user confirmation or a source |

## Truth boundary

Recommended `claim_type` values for this layer:

- `PREFERENCE`
- `GOAL`
- `USER_REPORTED_CONTEXT`
- `PRIVATE_CONTEXT`
- `SENSITIVE_CONTEXT`
- `EMOTION`
- `INTERPRETATION`
- `PROJECT_CONTEXT`
- `CULTURE_CONTEXT`
- `KNOWN_UNKNOWN`

These are not interchangeable with verified world facts.

```text
EMOTION != WORLD_FACT
PREFERENCE != WORLD_FACT
PRIVATE_CONTEXT != EVIDENCE
SENSITIVE_CONTEXT != LEGAL_ADVICE
HEALTH_CONTEXT != DIAGNOSIS
CULTURE_CONTEXT != HISTORICAL_FACT
```

## Redaction policy

Public examples must be synthetic. Private deployments should store full sensitive records outside the public repo and only expose redacted metadata to the Personal Overlay.

Examples of fields that must not be stored in public samples:

- passport numbers;
- national IDs;
- tax identifiers;
- CNP or equivalent identifiers;
- full street addresses;
- signatures;
- bank or payment data;
- private document scans;
- exact medical reports unless explicitly sourced and privately stored.

Use flags instead:

```json
{
  "type": "LegalContext",
  "title": "EU citizenship document context",
  "sensitivity": "sensitive",
  "store_full_numbers": false,
  "store_full_address": false,
  "requires_user_confirmation_before_use": true
}
```

## Minimal runtime direction

A future private runtime may implement:

1. schema validation for personal overlay records;
2. redacted local JSONL storage outside public source control;
3. a sensitivity filter before answer generation;
4. a router that can provide personal context only when relevant;
5. tests that verify private data is not leaked into unrelated answers;
6. no direct L3 promotion without review.

## Evaluation targets

| Eval | Expected behavior |
|---|---|
| `preference_following` | Use the user's preferred style/language when relevant |
| `private_context_guard` | Do not reveal sensitive context unnecessarily |
| `emotion_not_fact` | Do not treat emotions as world facts |
| `health_caution` | Treat health context as caution, not diagnosis |
| `legal_caution` | Treat legal context as caution, not legal advice |
| `culture_boundary` | Keep myth/symbol/fiction separate from `WORLD_FACT` |
| `goal_tracking` | Use active goals for task prioritization without inventing facts |
| `truthgate_boundary` | Never use personal context to bypass evidence requirements |

## Relationship to Crystal

The Personal Overlay may read Crystal outputs and may help plan retrieval priorities, but it must not weaken Crystal boundaries.

```text
Personal Overlay can influence attention.
TruthGate controls truth.
Guardian controls invariants.
Receipt proves provenance.
```

## Implementation status

Not implemented in Crystal runtime. This RFC and the accompanying schema/sample files are a future private-application design artifact only.
