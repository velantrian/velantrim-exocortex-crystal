# Failure Modes and Mitigations

An honest risk matrix for Velantrim Exo-Cortex Crystal. Status reflects the
mitigation as it exists in this repository today (see
[IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) for the canonical
status map). These mitigations do not prove perfect truth; they enforce
evidence, traceability, and boundary behaviour.

| Failure Mode | Risk | Mitigation | Status |
|---|---|---|---|
| TruthGate bypass | Unverified material enters L3 canon silently | TruthGate is the only automatic write path into L3 (`core/truth_gate.py`); the sole exception is the explicit, attributed, audited curator override; behaviour pinned by tests | implemented |
| LLM writes directly to canon | Model output becomes "truth" without evidence | The LLM sits outside the truth boundary; no write path from generation into L3; `LLM_OUTPUT` claims map to `UNVERIFIED` and are blocked from VERIFIED WORLD_FACT by the gate | implemented |
| TRACE incomplete | Confident answer cannot be audited | Answers are grounded through trace chains; receipts seal citations with content hashes; strict-provenance replay fails a VERIFIED citation without source-span evidence (CI eval gate) | implemented |
| FactsPack empty or weak | Answer generated without sufficient grounding | Insufficient-grounding block: the pipeline abstains (answer = null) instead of guessing | implemented |
| LLM_OUTPUT promoted as VERIFIED | Model self-confirmation loop | `_truth_status_for` maps LLM_OUTPUT to UNVERIFIED; TruthGate blocks LLM_OUTPUT-as-WORLD_FACT; pinned by dedicated tests | implemented |
| OPINION / EMOTION promoted as WORLD_FACT | Subjective claims masquerade as facts | Type-aware gate: subjective claim types always map to SUBJECTIVE truth status, never to VERIFIED world facts | implemented |
| Mode mixing (imagination/research output treated as verified) | Creative or exploratory output contaminates canon | Mode Layer / Imagination Mode are RFC-level; the fixed boundary rule (imagination output stays sandboxed, cannot become VERIFIED/WORLD_FACT without review) is documented in advance | RFC |
| Overfitting to replay benchmark | Optimization "wins" do not generalize | Held-out trajectory splits, per-case floors, versioned benchmark sets — defined in the Harness Replay RFC | RFC |
| Stale or contradictory knowledge | Outdated facts answer confidently | Contradiction detection links conflicts non-destructively (`core/contradiction.py`, `core/reconcile.py`); ESM states (Contradicted/Deprecated) track lifecycle; an explicit answer-layer conflict policy is a future RFC | partial |
| Source / provenance missing | Claims cannot be attributed | `source_status` is mandatory vocabulary; missing-source WORLD_FACT claims are blocked by the gate; evidence spans link claims to exact source offsets | implemented |
| Graph contains hypotheses mistaken for canon | Multi-status memory read as all-true | Canon is defined as the VERIFIED + trace-valid subgraph; statuses are explicit fields; the "Graph = Truth" precision note documents this distinction | implemented (docs + fields) |
| Guardian policy weakened by future optimizer | Optimization erodes safety boundaries | ContractGuard (RFC): candidate configurations cannot disable TruthGate/Guardian/TRACE; immutable, non-searchable rules; human approval loop | RFC |
| Personal data lingers in memory | GDPR-oriented erasure obligations unmet | Erasure with cascade and tombstones, processing restriction, tamper-evident audit, PII redaction — design targets, not certification | partial |

Notes:

- "implemented" = code + tests in this repository enforce the mitigation today;
- "partial" = baseline exists, hardening or a formal policy document is pending;
- "RFC" = the mitigation is designed in documentation only, with the boundary
  rule fixed in advance;
- nothing in this table claims the elimination of model error — the measurable
  goal is that unsupported claims are blocked, labelled, or auditable rather
  than silently promoted.
