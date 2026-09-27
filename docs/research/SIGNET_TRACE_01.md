# SIGNET-TRACE-01 — End-to-End Protocol Trace

## Official status restoration — 2026-09-28

The Grok run heading `TRACE_COMPLETE_ON_AVAILABLE_RECORD` / `SIGNET-TRACE-01 COMPLETE` is **withdrawn as the official experiment result**.

Preregistered stop rule from the TZ: if primary Signet source cannot be restored at Step 0, **stop**. Continuing Steps 1–8 on later derived documents is a different analysis.

```
SIGNET-TRACE-01
= BLOCKED_AT_STEP_0_BY_SOURCE_GAP

END-TO-END RESULT
= NOT OBTAINED

Protocol v0.1
= NOT VALIDATED
= NOT FALSIFIED END-TO-END
```

## Requalification of the Grok 2026-09-28 findings

| Finding | Correct class |
|---|---|
| raw conversation not recovered | SOURCE GAP = official Step 0 result |
| coverage example vs invariant 8 | separate protocol audit: `COVERAGE_CONTRACT_INCONSISTENCY = CONFIRMED` |
| admission-unit context gap | DESIGN CANDIDATE / UNDERDETERMINED |
| reported-speech source gap | DESIGN CANDIDATE / strongly motivated |
| Protocol v0.2 from this trace | NOT JUSTIFIED |

A small **v0.1.1** consistency correction for the coverage example is allowed as protocol self-consistency work. It is not Signet E2E validation.

Remaining design changes wait for a raw source pack.

The earlier Grok write-up remains archival analysis of derived materials. It must not be cited as TRACE_COMPLETE.

Tracking: Issue #489.
Draft PR #490 stays unmerged and is not an architecture promotion.
