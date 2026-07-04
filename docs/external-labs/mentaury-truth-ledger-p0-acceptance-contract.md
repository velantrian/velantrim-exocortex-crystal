# 🧾 Mentaury Truth Ledger Core P0 — Acceptance Contract

**Status:** `v0.1-acceptance-candidate / failed forensic audit`  
**Scope:** External Labs / research-only boundary  
**Repository boundary:** This document is **not** a Crystal production-runtime claim.  
**Acceptance rule:** `25/25` tests are required before P0 may be called accepted.

---

## Boundary

This document records an external research contract for **Mentaury / Ментаурий**, a standalone memory-centered cognitive sandbox discussed as part of the wider Velantrim Exo-Cortex research map.

It does **not** change Crystal's production scope.

Mentaury is:

- an External Labs research direction;
- not Crystal Canon;
- not a fifth Crystal runtime layer;
- not a living AI / consciousness claim;
- not accepted P0 until the full acceptance gate passes.

Crystal remains the verified memory discipline / Canon / TruthGate boundary. Mentaury may inform future research, but it must not be represented as implemented Crystal runtime until independently accepted.

---

## Core formula

```text
Event → Claim → Evidence → Receipt → Current State → Projection → Answer
```

Main invariant:

```text
event ≠ claim ≠ evidence ≠ canon ≠ cache ≠ answer
```

Short definitions:

- **Event** = something happened or was received.
- **Claim** = what was stated.
- **Evidence** = support or provenance for a claim.
- **Receipt** = deterministic admission decision record.
- **ReceiptChain** = source of admission state.
- **Projection** = rebuildable view, not source of truth.
- **Cache** = speed layer only; out of P0.
- **LLM** = speech / phrasing layer, not source of truth.

---

## Accepted research canon

1. `ClaimRecord` does **not** store truth or admission state.
2. Current admission state is derived from the latest valid `Receipt` by `receipt_seq` after chain verification.
3. `ReceiptChain` is the only source of admission state.
4. `Projection` is a rebuildable view, not a source of truth.
5. `Cache`, FAISS, Visual Explorer, Rosebud Bridge, full CR-7 diagnostics, semantic search and UI are out of P0.
6. `explain_decision()` must be deterministic and structured; no LLM reasoning.
7. Broken chain is not `RAW`. Broken chain means `CHAIN_BROKEN`, `IntegrityError`, `ChainBrokenError`, or equivalent hard integrity failure.

---

## Current audit status

DeepSeek prototype status:

```text
prototype draft / failed acceptance audit
```

Known failed facts from the forensic audit round:

- reported pytest result: `12 passed / 5 failed`;
- `verify_event_chain()` did not catch real payload tampering;
- several tests used invalid direct transitions: `RAW → CANON` or `RAW → CANDIDATE`;
- append-only trigger test expected the wrong SQLite exception type;
- some tampering tests were conceptual rather than real.

Forbidden labels until full acceptance:

- `P0 accepted`;
- `tamper-evident ledger`;
- `production-ready`;
- `Crystal Canon runtime`.

---

## Acceptance stages

### Stage A — repair current file

Existing failed tests are corrected and the old local test set passes.

Status meaning: repaired draft only; **not P0 accepted**.

### Stage B — forensic core repaired

First `21/25` tests pass.

Status meaning: forensic core repaired; **still not P0 accepted**.

### Stage C — P0 accepted

Full `25/25` tests pass in a real pytest run.

Status meaning: P0 may be accepted as `v0.1`.

Hard rule:

```text
21/25 ≠ P0 accepted
25/25 = P0 accepted
```

---

## P0 Acceptance Gate — 25 tests

### Structural integrity / append-only

1. `cannot_create_claim_without_event`
2. `cannot_create_evidence_without_claim`
3. `append_only_update_forbidden`
4. `append_only_delete_forbidden`

### Admission state machine

5. `invalid_transition_is_blocked`
6. `raw_to_canon_is_blocked_by_state_machine`
7. `raw_to_candidate_is_blocked_by_state_machine`
8. `candidate_to_canon_without_evidence_is_blocked_by_truthgate`
9. `workspace_without_evidence_allowed_with_warning`

### Forensic tampering detection

10. `event_chain_detects_payload_tampering_via_forensic_fixture`
11. `event_chain_detects_metadata_tampering_via_forensic_fixture`
12. `receipt_chain_detects_reason_tampering_via_forensic_fixture`
13. `receipt_chain_detects_evidence_refs_tampering_via_forensic_fixture`
14. `receipt_chain_detects_precheck_tampering_via_forensic_fixture`
15. `receipt_chain_detects_guardian_veto_tampering_via_forensic_fixture`

### Broken chain behavior

16. `current_state_raises_on_broken_receipt_chain`
17. `explain_decision_marks_untrusted_on_broken_chain`
18. `projection_does_not_build_on_broken_chain`

### Explain / projection / auditability

19. `explain_decision_returns_structured_dict`
20. `projection_rebuild_is_deterministic_after_restart`
21. `latest_state_derived_from_latest_valid_receipt_seq`

### Special P0 cases

22. `guardian_veto_creates_trace`
23. `guardian_veto_final_transition_is_checked`
24. `operator_override_creates_new_receipt_not_mutation`
25. `admit_is_atomic`

---

## Hash / sequence rule

If `event_seq` and `receipt_seq` are part of the hash contract, the implementation must not use:

```text
INSERT → get seq → UPDATE hash
```

because UPDATE is forbidden by append-only triggers.

Required pattern:

```text
BEGIN IMMEDIATE → reserve next_seq → compute hash with seq → INSERT → COMMIT
```

`event_hash` must cover:

```text
event_seq, event_id, timestamp, event_type, source, payload, metadata, previous_hash, schema_version
```

`receipt_hash` must cover:

```text
receipt_seq, receipt_id, claim_id, from_state, to_state, actor_id, policy_id, reason, evidence_refs, precheck_result, guardian_veto, timestamp, previous_receipt_hash, schema_version
```

---

## Forensic test harness rule

A real tampering test must:

1. create a valid record;
2. bypass the production write path using a clearly marked test-only helper;
3. physically alter stored DB content;
4. call `verify_event_chain()` or `verify_receipt_chain()`;
5. receive `False`, `ChainBrokenError`, or equivalent integrity failure.

Forbidden test patterns:

- `pass`;
- `skip`;
- `we cannot tamper in :memory:`;
- `would fail if tampered`;
- conceptual / theatrical tests.

---

## Operator mandate

Do not fix beautifully. Fix verifiably.

Rules:

1. Do not reduce the test list.
2. Do not change the constitution to fit convenient code.
3. Do not declare P0 accepted without full pytest output.
4. Do not accept the writer's own code without independent audit.
5. Keep P1/P2 frozen until `25/25`.

Final acceptance report must include:

- full pytest output;
- passed / failed count;
- changed file list;
- confirmation that no P1/P2 features were added;
- confirmation that forensic tampering tests really damage the DB and are caught by verify functions.

---

## Final formula

```text
Документ стал законом.
Код ещё должен выдержать суд.
25/25 — или P0 не принят.
```
