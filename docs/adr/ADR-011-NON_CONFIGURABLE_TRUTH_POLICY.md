# ADR-011: TruthPolicy is a non-configurable Ring Zero invariant

- **Status:** Accepted
- **Date:** 2026-08-01
- **Supersedes:** the environment-dependent portion of ADR-007

## Context

Crystal previously read `ENABLE_TRUTH_POLICY` at TruthGate call time. The secure
default blocked `source_status=LLM_OUTPUT` from being admitted as a
`claim_type=WORLD_FACT`, but setting the variable to `off` skipped that block.

A process environment variable is an operational configuration surface. It is
not an appropriate authority for weakening a Ring Zero epistemic invariant.
Configuration mistakes, inherited shell state, container manifests or an
untrusted launcher must not be able to turn model output into independent
world evidence.

## Decision

The following rule is unconditional:

```text
source_status = LLM_OUTPUT
+
claim_type = WORLD_FACT
→
TruthGate rejects admission unless the claim is represented with an honest,
independent provenance path outside the model output itself.
```

`core.truth_gate.truth_gate()` no longer reads `ENABLE_TRUTH_POLICY` or any
replacement runtime flag. Historical values such as `off`, `false`, `0` or
`legacy` are inert.

Tests, demos, migrations and fixtures must not weaken the gate. They must instead:

- provide an independent `source_status` when one genuinely exists;
- use a non-world-fact claim type for interpretation, opinion or hypothesis;
- or expect a bounded rejection.

The existing explicit, attributed and audited curator force-override remains a
governance exception under ADR-004. It does not change TruthGate's decision and
must retain the original `gate_reason`.

## Consequences

- the same evidence package and confidence threshold cannot receive a different
  LLM-world-fact decision because of process environment;
- deployment configuration can no longer disable this part of TruthPolicy;
- old `ENABLE_TRUTH_POLICY=off` deployments become strict automatically;
- tests that relied on the bypass must declare honest provenance instead;
- TruthGate still depends on the adaptive confidence threshold when
  `min_confidence` is omitted, so this ADR does not make every gate decision
  globally context-free;
- archived handoff and changelog records may describe the former behaviour as
  historical fact, but current reviewer/status/security documents must describe
  the non-configurable invariant.

## Verification

`tests/test_truth_gate.py` pins that multiple historical environment values,
including `off`, cannot admit an `LLM_OUTPUT` `WORLD_FACT`, while legitimate
external facts remain unaffected.