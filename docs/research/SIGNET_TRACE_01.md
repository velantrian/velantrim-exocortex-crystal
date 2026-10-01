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


## SOURCE-RECOVERY-01-R1 — source recovery result — 2026-09-28

Official bounded result:

```text
SOURCE-RECOVERY-01-R1
= BLOCKED_AT_STEP_0_BY_SOURCE_GAP

SIGNET-TRACE-01
= BLOCKED_AT_STEP_0_BY_SOURCE_GAP

END-TO-END RESULT
= NOT OBTAINED

Protocol v0.1
= NOT VALIDATED
= NOT FALSIFIED END-TO-END
```

The provider-native/raw historical conversation window containing the reported assistant recommendation was **not recovered**. The available inspected materials are later derived research/run/protocol/trace artifacts only.

Coverage remains `partial_or_unverified`. No historical `UserSelected` / `UserRejected` event was created.

Blocking gaps recorded by R1:
- raw Signet conversation window unavailable;
- provider-native message ID / stable locator unknown;
- original timestamp / authoritative chronology unknown;
- source completeness boundary undefined;
- no primary evidence for user selection/rejection;
- exact later artifact that performed the reported status promotion was not recovered.

No admission, current-standing mutation, working capsule, typed validator, renderer, runtime/schema change, implementation authorization, or merge was performed.

**Re-entry condition:** resume SIGNET-TRACE-01 only from Step 0 if an owner-provided raw/exported conversation window becomes available with attributable actor, chronology, immutable content identity, and an explicit completeness boundary. Do not retroactively upgrade derived records into primary evidence.

Research classification: bounded source-recoverability result; not Canon, not runtime authorization, and not end-to-end validation/falsification of Protocol v0.1.
