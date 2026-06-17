# Claim Type and Origin Type

> Date: 2026-06-17
> Scope: Crystal epistemic-type contract
> Status: docs-only unless runtime support is explicitly implemented and tested.

## Purpose

Crystal must distinguish what a statement is from how verified it is.

```text
memory != knowledge
experience != world fact
importance != confidence
LLM output != evidence
```

## Orthogonal axes

| Axis | Field | Question |
|---|---|---|
| Verification | `epistemic_state` / `truth_status` | How verified is it? |
| Modality | `claim_type` | What kind of statement is it? |
| Origin | `origin_type` | Where did it come from? |
| Reliability | `confidence` | How reliable is the support? |
| Retrieval priority | `salience` | How important is it for attention/retrieval? |

## Recommended claim types

```text
WORLD_FACT
USER_EXPERIENCE
EMOTION
INTERPRETATION
OPINION
GOAL
PREFERENCE
SYSTEM_NOTE
UNKNOWN
```

## Recommended origin types

```text
USER_REPORTED
SYSTEM_OBSERVED
DERIVED
EXTERNAL
LLM_OUTPUT
SYSTEM_GENERATED
UNKNOWN
```

## Core rules

### Subjective material is valid, but scoped

A feeling or opinion can be a valid record of user state. It must not be converted into a world fact without explicit evidence and conversion.

Example:

```text
Valid subjective memory: user reported feeling anxious about a grant deadline.
Invalid world fact: the grant process is dangerous.
```

### LLM output is not evidence

LLM-generated text may produce a candidate claim. It is not external evidence and must not become verified canon by itself.

### Unknown is not a world fact

`UNKNOWN` without evidence should not be promoted to verified factual status.

### Salience is not confidence

A memory can be important for retrieval while still unverified.

## Public wording

Safe:

```text
Crystal separates factual claims, subjective records, generated text and external evidence.
```

Avoid unless fully implemented:

```text
All runtime paths already enforce claim-type promotion rules.
```

## Claude Code follow-up

Before any runtime change, Claude Code should map this contract to existing validators and tests, then add narrow contract tests for promotion ceilings and FactsPack rendering.
