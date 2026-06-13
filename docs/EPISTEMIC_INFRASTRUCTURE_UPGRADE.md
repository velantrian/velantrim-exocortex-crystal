# Epistemic Infrastructure Upgrade

**Status:** Future RFC only. Not current runtime.
**Planned for:** v0.3.0+ / research roadmap.
**Requires:** Separate design RFC and migration plan before implementation.
**Runtime impact in v0.2.0:** None.

> None of the features described in this document are current runtime behaviour.
> They must not be presented as implemented in README, Reviewer Overview or grant
> materials. Everything below is a design direction for future research and
> post-grant hardening.

A verified claim is incomplete without evidence, provenance, temporal validity,
scope conditions, conflict status and calibrated confidence. This document
describes the full epistemic upgrade path that takes Crystal from its current
state toward that richer model.

---

## 1. Temporal + Context / Scope Layer

**Status:** Future RFC. No schema fields today.

A claim such as "water boils at 100 °C at sea level" is always true; a claim
such as "the prime minister of country X is Y" is only true within a time window
and a jurisdiction. Crystal currently treats all facts as timeless unless the
text itself encodes the date. This section defines the future temporal and
context/scope fields.

### Temporal fields (future schema)

| Field | Type | Description |
|---|---|---|
| `valid_from` | ISO 8601 | Earliest point in time the claim is valid |
| `valid_until` | ISO 8601 or `null` | Latest valid point (`null` = no expiry known) |
| `observed_at` | ISO 8601 | When the claim was first observed/ingested |
| `invalidated_at` | ISO 8601 or `null` | When the claim was superseded or disproved |

### Context / Scope fields (future schema)

| Field | Type | Description |
|---|---|---|
| `jurisdiction` | string | Legal or geographic scope (e.g. `"EU"`, `"US-CA"`) |
| `physical_conditions` | dict | Physical preconditions (e.g. `{"altitude": "sea level"}`) |
| `domain` | string | Knowledge domain (e.g. `"chemistry"`, `"law"`) |
| `population` | string | Target population or user context |
| `scope_sensitivity` | enum | `LOW` / `MEDIUM` / `HIGH` / `JURISDICTION_SPECIFIC` |

### Point-in-time queries (future)

```python
# Not implemented — future API sketch
canon.query("what was the prime minister of X", at="2023-01-01")
```

---

## 2. Conflict Resolution Protocol

**Status:** Future RFC. No runtime implementation today.

Currently Crystal detects contradictions and flags them. It does not resolve
them automatically — a curator must decide. The future protocol adds:

- **Contested claims**: two VERIFIED claims with conflicting content are both
  retained, both shown to the curator, neither silently hidden.
- **Both TRACE paths shown**: the evidence chain for each side is visible.
- **Curator resolution**: the curator explicitly promotes one, demotes the other,
  or marks both as `HYPOTHESIS` pending further evidence.
- **No silent conflict hiding**: a contradiction that cannot be resolved must
  remain visible as `contested`, not collapsed into one "winner".

---

## 3. Negative Knowledge Registry

**Status:** Future RFC. No runtime implementation today.

Claims that have been investigated and found false are not simply absent — they
should be explicitly recorded so the system does not waste resources re-exploring
the same dead end.

| Field | Description |
|---|---|
| `rejected_claim` | The claim text that was investigated |
| `rejection_reason` | Why it was rejected (contradicted, no evidence, out of scope) |
| `rejected_at` | Timestamp |
| `rehabilitation_conditions` | Under what new evidence the claim could be reconsidered |

---

## 4. Known Unknowns Map

**Status:** Future RFC. No runtime implementation today.

The system should be able to say "I don't know" with structure, not just silence.
A known-unknowns map tracks:

| Signal | Description |
|---|---|
| Low coverage | A domain or query type where few VERIFIED facts exist |
| Weak evidence | Claims where `truth_status = USER_CLAIMED` but no EXTERNAL source found |
| Contradiction density | Areas with many unresolved conflicts |
| Staleness risk | Facts without `valid_until` that may be outdated |

---

## 5. Anomaly as Interest Signal

**Status:** Future RFC. No runtime implementation today.

An unexpected query miss (no retrieval hit, unsupported provenance) is not just
an error — it is an interest signal: the system should flag what it cannot answer
and expose this as a structured gap rather than a silent failure.

---

## 6. Plausibility Pre-Filter / Spark-to-Crystal Bridge

**Status:** Future RFC. No runtime implementation today.

Before a claim reaches the TruthGate, a lightweight plausibility pre-filter
could classify it along a spectrum:

| Label | Meaning |
|---|---|
| `impossible_under_known_constraints` | Directly contradicts verified canon |
| `highly_speculative` | No supporting evidence and contradicts priors |
| `research_required` | Plausible but unverifiable without new sources |
| `partially_supported_by_L3` | Some supporting evidence but not conclusive |
| `plausible_enough_for_deep_check` | Worth full TruthGate evaluation |

This pre-filter is the bridge between a future "Spark" creative/exploratory
layer and the verified Crystal canon. Nothing from the Spark layer may become
`VERIFIED` or `WORLD_FACT` without passing through Guardian and TruthGate.

---

## 7. Confidence Calibration

**Status:** Future RFC. No runtime implementation today.

Crystal stores confidence scores but does not currently calibrate them against
empirical ground truth. Calibration would measure whether a claim stored with
`confidence = 0.9` is actually correct 90% of the time.

### Target calibration metrics

| Metric | Description |
|---|---|
| ECE (Expected Calibration Error) | Average gap between predicted confidence and empirical accuracy |
| MCE (Maximum Calibration Error) | Worst-case confidence/accuracy gap in any bin |
| Brier score | Mean squared error of probabilistic confidence estimates |
| Overconfidence rate | Share of claims stored with high confidence but later contradicted |
| Per-source calibration | ECE broken down by `source_status` (EXTERNAL vs USER_CLAIMED) |
| Per-domain calibration | ECE broken down by `claim_type` |

---

## 8. Epistemic Debt

**Status:** Future RFC. No runtime implementation today.

Epistemic debt is the accumulated backlog of claims that need epistemic work:
verification, scoping, contradiction resolution, or expiry review.

| Category | Description |
|---|---|
| `unknown_validity_claims` | Claims with no `valid_from`/`valid_until` that may be stale |
| `stale_claims` | Claims past their `valid_until` date |
| `contested_claims` | Claims in active contradiction with no curator resolution |
| `low_evidence_claims` | `USER_CLAIMED` claims with no supporting EXTERNAL source |
| `unscoped_claims` | Claims missing `jurisdiction` or `physical_conditions` where relevant |

---

## 9. Migration Strategy

**Status:** Future RFC. No migration plan today.

Adding temporal and scope fields to L3 is a non-trivial schema migration. The
migration plan must address:

- backward compatibility: existing records without `valid_from`/`valid_until` are
  treated as `valid_from = observed_at`, `valid_until = null` (no expiry known);
- gradual adoption: new ingestion paths set temporal fields when available; old
  records are flagged as `unknown_validity`;
- no silent data loss: migration is additive, never destructive.

---

## 10. Temporal Reasoning Tests (future)

**Status:** Future RFC. No test implementation today.

Required test scenarios for temporal reasoning (to be implemented alongside the
schema migration):

- point-in-time query returns only claims valid at the specified date;
- `valid_until` expiry correctly excludes a claim from fresh queries;
- conflicting claims with non-overlapping `valid_from`/`valid_until` windows are
  both retained and correctly scoped;
- `observed_at` is immutable after ingestion;
- `invalidated_at` is set only by an explicit curator action, not automatically.

---

## 11. Non-goals

This RFC does not describe:

- implementing temporal fields in Crystal v0.2.0 or any current release;
- automatic L3 promotion based on plausibility alone;
- replacing the TruthGate with probabilistic pre-filters;
- multi-user conflict resolution (that is a separate RBAC RFC);
- consciousness, AGI, or guaranteed truth detection;
- any change to the current runtime schema, enums, or test baseline.
