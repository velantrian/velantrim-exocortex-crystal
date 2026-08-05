# 📍 Crystal Current State

**Status date:** 2026-08-05  
**Current `main` head:** `8d576e1342f40d9a823885f9dcce4b1ff16d113a`  
**Verified runtime checkpoint:** `f91299c44a1a1850fa516f3abb96c916326f7a8c`
(PR #302)  
**Version:** `0.3.0`

This file is a compact orientation snapshot. Verify material claims against the current
repository before relying on them.

## 1. Why the head and runtime checkpoint differ

The runtime checkpoint records the exact commit whose implementation and test evidence
are captured in `TEST_REPORT.md` and the implementation manifest. Commits after that
checkpoint, through the current `main` head, are documentation and localization changes.
They do not create new runtime capability.

```text
f91299c  verified runtime checkpoint
   ↓
README localization and visual documentation updates
   ↓
8d576e1  GitHub ↔ Notion documentation governance
```

## 2. Verified runtime baseline

The implementation manifest records:

- Python 3.11 and 3.12;
- 1853 passed, 12 skipped, 0 failed;
- 100% measured line coverage at the checkpoint;
- 7/7 declared targeted Ring Zero mutants killed;
- nine permanent CI jobs;
- pure-standard-library default runtime.

Implemented boundaries include:

- typed claims and explicit epistemic lifecycle;
- Guardian and TruthGate admission controls;
- physical L3 separated from strict Canon;
- immutable deny-dominant `TrustSnapshot` reconciliation;
- read-only public HTTP, CLI and MCP query surfaces;
- TRACE and replayable/tamper-evident Receipts;
- review queues and resumable review sessions;
- immutable contradiction reports;
- explicit `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` decisions;
- conflict-resolution CLI and authenticated HTTP surface;
- scoped curator roles/capabilities;
- process-local decision leases;
- advisory multi-label topic facets with no truth authority;
- machine-readable ESM specification;
- scheduled/manual L3 benchmark history.

## 3. Important implemented limitations

| Area | Current reality |
|---|---|
| Decision coordination | Process-local lease registry only; no distributed lease adapter |
| Identity and tenancy | Host-authenticated actor binding exists; production IdP and multi-tenant policy are not complete |
| Physical L3 | Multi-status graph; not equivalent to strict Canon |
| Topic facets | Advisory navigation metadata only |
| Model output | Not an independent factual source |
| Default dependencies | Pure stdlib runtime; optional capabilities belong in extras |
| Compliance | GDPR-oriented mechanisms and documentation, not legal certification |
| Production posture | Not a certified, turnkey multi-tenant production service |

## 4. Open pull requests outside `main`

Open PRs are non-authoritative until merged.

- **#245 — Essence Workdesk research track:** prototype/research boundary; not Crystal
  runtime authority.
- **#249 — cognitive state and planning boundaries:** documentation-only research
  concepts; no Canon or runtime path.
- **#261 — public naming hierarchy:** branding proposal; repository/package/runtime
  identity remains unchanged until an explicit accepted migration.
- **#262 — Native Kernel compatibility boundary:** documentation-only research
  relationship; no storage replacement or live dual-write.

Agents must inspect each PR's current base, head, CI, reviews and diff before making a
claim about it.

## 5. Open issues and backlog interpretation

Open issues are hypotheses or trackers, not proof that a capability is absent. Some older
issues describe work later implemented under different PRs. Always compare the issue with
`docs/STATUS.md`, the implementation manifest, current code and tests.

Material remaining work includes:

- distributed decision coordination;
- production identity-provider and multi-tenant authorization integration;
- broader provenance lifecycle wiring;
- controlled-runner performance SLO policy;
- broader mutation testing beyond the declared Ring Zero set;
- i18n governance and link/synchronization validation (#285, #286);
- secret-scanning and fixture/PII hygiene (#214);
- legacy normalized-ID migration or normalized-claim index (#165).

## 6. Long-document semantic reading

No dedicated multi-pass `Reader Core` / `Semantic Reading Layer` with coverage maps,
bookmarks, contradiction passes, re-reading policy and document-type-aware segmentation
is part of the verified Crystal runtime at this checkpoint.

Crystal already has strong claim/evidence/provenance boundaries. A future reading layer
must produce source-linked candidates and review material; it must not silently admit
summaries or inferred importance into strict Canon.

## 7. Research and grant boundary

```text
Crystal main = public implementation truth
Notion Crystal pages = synchronized strategy, rationale and grant map
Titan / Full Exo-Cortex / Personal Exo-Cortex = separate research tracks
```

The implementation manifest records the NLnet submission as under review and not awarded
at the 2026-08-01 checkpoint. Do not convert a submission, roadmap item or research page
into a funded or implemented capability claim.

## 8. Immediate documentation state

PR #310 was merged as `8d576e1342f40d9a823885f9dcce4b1ff16d113a` and now requires every material change to
classify documentation impact as `NONE`, `GITHUB_ONLY`, or `GITHUB_AND_NOTION`.

This AI context pack extends that governance by giving agents a compact current-state,
component, risk, audit and hand-off layer. It does not change Crystal runtime behavior.
