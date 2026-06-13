# Crystal Invariant Checker

`velantrim invariant-check`

## What it does

Runs a read-only, machine-executable check against the current Crystal L3
canonical state and emits a JSON report of which epistemic invariants are
satisfied, which are violated, and which cannot be checked given the current
schema.

It is **reviewer / conformance tooling**. It does not claim to be a formal
mathematical proof.

> The invariant checker does not make claims true. It checks whether the
> current Crystal state violates selected epistemic invariants that the
> implementation can verify.

## What it does NOT do

- Does not write to memory or L3.
- Does not call TruthGate.
- Does not modify or generate receipts.
- Does not replace `velantrim verify-receipt` (which replays an individual receipt).
- Does not replace `velantrim audit-verify` (which checks the audit log hash chain).
- Does not produce a health score, transparency score, or certification.
- Does not make formal correctness guarantees.

## Implemented checks (v0.1)

| Check ID | Status | What is verified |
|---|---|---|
| `no_llm_output_verified` | Implementable | No `VERIFIED` claim has `source_status=LLM_OUTPUT` |
| `verified_requires_source` | Implementable | Every `VERIFIED` claim has a non-empty source field |
| `verified_requires_evidence` | Implementable (evidence-span sub-check only) | Every `VERIFIED` claim has at least one source-span evidence record |
| `receipt_integrity` | `SKIPPED_UNSUPPORTED` | See below |
| `no_direct_l3_bypass` | `SKIPPED_UNSUPPORTED` | See below |

## What `SKIPPED_UNSUPPORTED` means

A check marked `SKIPPED_UNSUPPORTED` was not performed because the current
schema or audit log does not expose the information needed to evaluate it.

This is not a PASS. It means the invariant is not verifiable at this level.

| Check | Why unsupported |
|---|---|
| `receipt_integrity` | L3 does not maintain a global receipt registry. Use `velantrim verify-receipt <file>` to replay individual receipts. |
| `no_direct_l3_bypass` | The audit log captures compliance events (erase/restrict) but not L3 write events. Structural enforcement is provided by TruthGate and Guardian at write time. |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | PASS — all implementable checks passed |
| `1` | WARN — no failures, but no implementable checks could run |
| `2` | FAIL — at least one check detected a violation |

## Example: PASS output

```json
{
  "status": "PASS",
  "checked_at": "2026-06-13T12:00:00Z",
  "checks": [
    {
      "id": "no_llm_output_verified",
      "status": "PASS",
      "violations": 0,
      "why": "No VERIFIED claim is sourced only from LLM_OUTPUT."
    },
    {
      "id": "verified_requires_source",
      "status": "PASS",
      "violations": 0,
      "why": "All VERIFIED claims carry a non-empty source field."
    },
    {
      "id": "verified_requires_evidence",
      "status": "PASS",
      "violations": 0,
      "why": "All VERIFIED claims carry at least one source-span evidence record."
    },
    {
      "id": "receipt_integrity",
      "status": "SKIPPED_UNSUPPORTED",
      "violations": 0,
      "why": "No global receipt registry in L3. Use 'velantrim verify-receipt <file>'."
    },
    {
      "id": "no_direct_l3_bypass",
      "status": "SKIPPED_UNSUPPORTED",
      "violations": 0,
      "why": "Audit log captures compliance events but not L3 write events."
    }
  ],
  "issues": []
}
```

## Example: FAIL output

```json
{
  "status": "FAIL",
  "checked_at": "2026-06-13T12:00:00Z",
  "checks": [
    {
      "id": "no_llm_output_verified",
      "status": "FAIL",
      "violations": 1,
      "why": "A VERIFIED claim must not have source_status=LLM_OUTPUT."
    }
  ],
  "issues": [
    {
      "check_id": "no_llm_output_verified",
      "severity": "ERROR",
      "fact_id": "ing:abc123def456",
      "why": "truth_status=VERIFIED but source_status=LLM_OUTPUT",
      "suggestion": "Demote to UNVERIFIED or attach external evidence and review."
    }
  ]
}
```

## Why this supports reviewer confidence

The checker makes the runtime invariants machine-readable and independently
runnable. A reviewer can:

1. Run `velantrim invariant-check` against a live or exported state.
2. Read the JSON report to confirm the claimed invariants hold.
3. Identify which checks were skipped and why, rather than receiving an
   unqualified PASS.

The `SKIPPED_UNSUPPORTED` status ensures the report never overstates what was
verified.

## Read-only guarantee

`velantrim invariant-check` does not write to any store. It queries:

- L3 canonical graph (`all_facts()`)
- Evidence span store (`has_evidence()`)

It does not call TruthGate, Guardian, the review queue, or any write-path function.

## Relationship to other commands

| Command | Purpose |
|---|---|
| `velantrim invariant-check` | Global at-rest invariant scan (this command) |
| `velantrim verify-receipt <file>` | Replay a specific sealed receipt against the canon |
| `velantrim audit-verify` | Verify the tamper-evident audit log hash chain |
| `velantrim evidence <fact_id>` | Inspect source-span evidence for a specific fact |
