# SIGNET-TRACE-01 — End-to-End Protocol Trace

**Date opened:** 2026-09-27
**Status:** PLANNED · NOT RUN · NOT VALIDATED · NOT ARCHITECTURE DECISION · NOT RUNTIME AUTHORIZATION

## Purpose

Run one real, already-observed authority/status-promotion case through Protocol v0.1 literally, step by step, before expanding the protocol.

This trace is intended to reveal where the protocol works, where it cannot decide without an additional rule, and where a proposed safeguard is unnecessary.

## Frozen case boundary

Existing research record establishes the following live case:

- assistant recommendation: `Я бы не интегрировал Signet напрямую`;
- later derived state/examples promoted that recommendation toward `USER_DECISION / rejected`;
- no separate user act establishing that decision was shown in the available record;
- current bounded status for direct Signet integration: `NOT_ESTABLISHED_IN_AVAILABLE_RECORD`;
- Signet remains a `DONOR / COMPARATOR CANDIDATE`.

Do not invent a missing user act. Do not use later summaries as primary evidence.

## Primary research question

Can Protocol v0.1 preserve actor, authority, uncertainty and current standing across the full path from source material to the final model-visible answer?

## Trace method

For every step record exactly:

```text
INPUT
RULE_USED
OUTPUT
UNCERTAINTY
MISSING_RULE_OR_FAILURE
```

If a step cannot be completed from the available source, mark `BLOCKED_BY_SOURCE_GAP`; do not repair the gap by inference.

## Step 0 — Raw source

- Identify the exact source messages used.
- Preserve actor, message order, time if available, and source identity.
- Separate primary source from later derived summaries.

**INPUT:** TBD
**RULE_USED:** source preservation
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 1 — Contextual evidence bundle

Test whether one isolated quote is sufficient or whether interpretation requires reply/reference context.

**INPUT:** TBD
**RULE_USED:** Protocol v0.1 evidence/source rules
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 2 — `memory.propose_event_interpretation`

Generate the narrowest source-bound event proposal. Proposal is not admission.

**INPUT:** TBD
**RULE_USED:** actor / role / speech-act / scope boundary
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 3 — Admission

Check source identity, actor, evidence, scope, transition and uncertainty. No user decision may be created solely from assistant evidence.

**INPUT:** TBD
**RULE_USED:** admission checks
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 4 — Current standing

Derive only what the admitted evidence supports. Explicitly record whether coverage is sufficient to distinguish `no_confirmed_user_decision` from `unknown / partial`.

**INPUT:** TBD
**RULE_USED:** historical event != current standing; absence != negative decision
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 5 — Working capsule

Build a minimal model-visible capsule while preserving `primary_event`, `derived_projection`, coverage, conflicts and open questions.

**INPUT:** TBD
**RULE_USED:** capsule provenance boundary
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 6 — Structured authority claim

Before rendering any authority-sensitive statement, represent the claim structurally and attach basis evidence.

**INPUT:** TBD
**RULE_USED:** candidate `typed → validate → render` control for authority-sensitive claims
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 7 — Validation

Compare the structured claim against current standing and evidence. Unsupported promotion must fail closed.

**INPUT:** TBD
**RULE_USED:** deterministic grounding / policy check
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Step 8 — Rendered answer

Render the validated state into natural language. Confirm that the wording does not silently strengthen actor, decision state or certainty.

**INPUT:** TBD
**RULE_USED:** validated structure is authoritative over free-text wording
**OUTPUT:** TBD
**UNCERTAINTY:** TBD
**MISSING_RULE_OR_FAILURE:** TBD

## Known review questions to observe, not pre-accept

- unit of admission: isolated utterance vs contextual evidence bundle;
- `UserRevoked` vs correction of an erroneous historical admission (`EventInvalidated` candidate);
- deterministic meaning of `coverage_state`;
- redaction/deletion of evidence text without rewriting the historical event;
- trusted identity constraints for `admitted_by`;
- referential integrity of standing basis events instead of an unchecked JSON blob;
- free-text parser gate vs `typed → validate → render` for authority-sensitive claims.

These are review hypotheses. A trace finding must identify which one is actually required.

## Result classification

For each protocol component use one of:

- `SUPPORTED_IN_TRACE`
- `FAILED_IN_TRACE`
- `UNDERDETERMINED`
- `NOT_EXERCISED`

Overall trace status remains `NOT RUN` until every completed step has recorded input, rule, output and uncertainty.

## Revision rule

`TRACE FAILURE → DOCUMENTED DELTA → Protocol v0.2 candidate`

`AI REVIEW COMMENT ≠ PROTOCOL CHANGE`
`ONE TRACE ≠ GENERAL VALIDATION`
`PROTOCOL PASS ON SIGNET ≠ EXO-CORTEX ARCHITECTURE PROVEN`