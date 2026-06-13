# Refusal Reasons Taxonomy v0.1

`core/refusal_reasons.py`

## What it is

A stable, machine-readable taxonomy of reason codes that explain why Crystal
refuses to treat a claim as `VERIFIED`.

It is a **read-only vocabulary module**.  It does not write to memory, does not
call TruthGate, and does not produce receipts.

> Reason codes are stable identifiers.  Once published, a code is never removed
> or repurposed.  Deprecations are marked in the `description` field only.

## Why it exists

Without a standard vocabulary, rejection reasons appear as ad-hoc prose in
issue objects and check results.  Machine consumers (review tools, dashboards,
CI checks) cannot act on prose.  Reason codes give them a stable, actionable
hook.

## API

```python
from core import refusal_reasons as rr

rr.get_reason("MISSING_SOURCE")      # → dict (raises KeyError if unknown)
rr.is_valid_reason("MISSING_SOURCE") # → True / False
rr.list_reasons()                    # → list[dict] (copies — safe to mutate)
rr.format_reason("MISSING_SOURCE")   # → "[ERROR] MISSING_SOURCE: ..."
```

Each reason dict has five fields:

| Field | Type | Meaning |
|---|---|---|
| `code` | str | Stable identifier (UPPER_SNAKE_CASE) |
| `title` | str | Short human-readable title |
| `severity` | str | `INFO`, `WARN`, `ERROR`, or `CRITICAL` |
| `description` | str | What the refusal means |
| `suggestion` | str | Recommended remediation |

## Severity levels

| Level | Meaning |
|---|---|
| `INFO` | Informational — no action required |
| `WARN` | Potential issue — review recommended |
| `ERROR` | Verification cannot proceed without remediation |
| `CRITICAL` | Data integrity or security concern — investigate immediately |

## Reason codes (v0.1)

| Code | Severity | Title |
|---|---|---|
| `NO_VERIFIED_CLAIM` | INFO | No VERIFIED claim present |
| `LLM_OUTPUT_NOT_EVIDENCE` | ERROR | LLM output is not admissible evidence |
| `MISSING_SOURCE` | ERROR | No source field |
| `MISSING_PROVENANCE` | WARN | Provenance chain incomplete |
| `MISSING_EVIDENCE` | WARN | No source-span evidence record |
| `MISSING_TRACE` | WARN | No epistemic trace |
| `RECEIPT_TAMPERED` | CRITICAL | Receipt integrity check failed |
| `CONTRADICTION_UNRESOLVED` | ERROR | Unresolved contradiction |
| `UNSUPPORTED_SCHEMA_CHECK` | INFO | Check not supported by current schema |
| `TRUTHGATE_REJECTED` | ERROR | TruthGate rejected the claim |
| `GUARDIAN_BLOCKED` | CRITICAL | Guardian blocked the write |
| `REQUIRES_HUMAN_REVIEW` | WARN | Human review required |
| `OUT_OF_SCOPE` | INFO | Claim type out of scope |

## Integration with invariant-check

`velantrim invariant-check` populates `reason_code` on failing check entries
and issue entries.  PASS entries do not carry a `reason_code`.

| Check ID | Failure reason_code |
|---|---|
| `no_llm_output_verified` | `LLM_OUTPUT_NOT_EVIDENCE` |
| `verified_requires_source` | `MISSING_SOURCE` |
| `verified_requires_evidence` | `MISSING_EVIDENCE` |
| `receipt_integrity` (SKIPPED) | `UNSUPPORTED_SCHEMA_CHECK` |
| `no_direct_l3_bypass` (SKIPPED) | `UNSUPPORTED_SCHEMA_CHECK` |

### Example: FAIL with reason_code

```json
{
  "id": "no_llm_output_verified",
  "status": "FAIL",
  "violations": 1,
  "why": "A VERIFIED claim must not have source_status=LLM_OUTPUT.",
  "reason_code": "LLM_OUTPUT_NOT_EVIDENCE"
}
```

### Example: SKIPPED with reason_code

```json
{
  "id": "receipt_integrity",
  "status": "SKIPPED_UNSUPPORTED",
  "violations": 0,
  "why": "No global receipt registry in L3. Use 'velantrim verify-receipt <file>'.",
  "reason_code": "UNSUPPORTED_SCHEMA_CHECK"
}
```

### Example: PASS (no reason_code)

```json
{
  "id": "no_llm_output_verified",
  "status": "PASS",
  "violations": 0,
  "why": "No VERIFIED claim is sourced only from LLM_OUTPUT."
}
```

## What it does NOT do

- Does not write to memory or L3.
- Does not call TruthGate or Guardian.
- Does not assign scores, grades, or certifications.
- Does not make formal mathematical proof claims.
- Does not add new `truth_status` or `source_status` enum values.
- Does not change TruthGate or Guardian semantics.

## Stability guarantee

Reason codes in v0.1 are stable identifiers.  The `code` string will not
change.  Fields `severity`, `description`, and `suggestion` may be refined in
future minor versions, but the semantic meaning of each code will not change in
a breaking way.

New codes may be added in future versions.  Existing codes are never removed.

## Relationship to other modules

| Module | Role |
|---|---|
| `core/refusal_reasons.py` | Vocabulary — defines codes (this module) |
| `core/invariant_check.py` | Consumer — populates `reason_code` in check reports |
| `velantrim invariant-check` | CLI — emits JSON reports with `reason_code` fields |
| `velantrim verify-receipt` | Replay individual receipts (see `RECEIPT_TAMPERED`) |
| `velantrim audit-verify` | Verify audit log hash chain |
