# Answer Contract

> Date: 2026-06-17
> Scope: user-facing answer discipline for Crystal
> Status: docs-only unless enforced by runtime/tests.

## Purpose

Truth controls can be weakened by careless wording. Crystal should not let the speech layer turn uncertainty into confidence.

```text
Speech cannot promote evidence.
Speech cannot convert UNVERIFIED into FACT.
Speech cannot hide uncertainty.
```

## Rules

1. State uncertainty when evidence is weak or missing.
2. Surface contradictions instead of smoothing them away.
3. Distinguish facts, hypotheses, opinions, subjective reports and generated text.
4. Use `gap_notice` or equivalent wording when evidence is missing.
5. Do not present LLM output as external evidence.
6. Do not claim verified status without source/evidence/trace support.
7. Keep answers shorter in normal mode and more explicit in audit mode.

## Suggested modes

| Mode | Behaviour |
|---|---|
| `normal` | concise, clear, marks important uncertainty |
| `audit` | always shows truth status, source/evidence limits and trace hints |
| `research` | allows hypotheses, but labels them clearly |

## Safe wording examples

```text
The repository currently supports X. Y is documented as future work.
```

```text
This is an unverified planning hypothesis, not a verified fact.
```

```text
I found evidence for A, but B remains unsupported.
```

## Unsafe wording examples

```text
This is proven.
```

when the evidence is missing.

```text
Crystal eliminates hallucinations.
```

when the actual claim is unsupported-claim prevention and traceable refusal.

## Relationship to LLMs

LLMs may phrase or summarize. They must not upgrade truth status.

```text
LLM = Voice
Graph / Canon = Truth
FactsPack = Evidence
TruthGate = Boundary
```
