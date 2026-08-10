# Crystal Current State

**Status date:** 2026-08-10  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**Completed D1–D5 documentation checkpoint:** `f4556e8f9775d28d4a1b2c20a28962a95e55d33e` / PR #352  
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores synchronized rationale and history; it does not override repository evidence.

## 1. Verified runtime evidence

- Python 3.11 and 3.12: **2078 passed / 13 skipped / 0 failed** at the retained verified runtime checkpoint;
- **9756 statements / 100.00% coverage** at that checkpoint;
- PostgreSQL migration modules: **44/44 + 336/336 statements**;
- **7/7** Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- **1/1** real PostgreSQL/pgvector integration job successful.

Newer bounded features must carry their own exact-head and post-merge CI evidence rather than silently rewriting the historical checkpoint above.

## 2. Current storage and migration capability

SQLite remains the ordinary active local-first profile. PostgreSQL remains `active=false`, absent from ordinary runtime composition and unable to serve normal reads or writes. Import/equivalence does not establish activation, automatic selection, cutover, rollback, dual-write, TruthGate admission or strict Canon membership.

## 3. Grant and remaining limitations

The NLnet proposal is submitted / under review / not awarded. Approximate €50,000 is planning only, not an approved budget or payment commitment. Budget change is none. Work merged before an agreement is existing baseline and cannot be counted again as funded delta. A dedicated multi-pass Reader Core / Semantic Reading runtime is not implemented. No legal, GDPR, security or native-speaker editorial certification is claimed.

## 4. Documentation language and D1–D3

English is the primary working, source and conflict-resolving language. Translations create no independent implementation, security, grant, TruthGate or Canon authority.

Issue #341 D1 is complete for all nine supported locales. Russian D1 is tied to `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`; the other eight locales are tied to `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130`.

D1 is current across all nine supported locale packs. D2 reviewer/safety translations are current against `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`. The D2 English source family is reconciled.

**D3 English source checkpoint:** `main@208f1c772ee3a112cb803d2413c120bef23adb05`. The complete D3 source validator covers the stable architecture/storage authority family. D3 is current across all nine supported locale packs. The D3 validator covers **18 architecture/storage documents plus nine indexes**.

## 5. D4 state

The D4 English source family is reconciled at `main@151b41c680190f7f3de729bf63e8e80a9d2285ce` across `docs/PROJECT_GRANT_AND_GOVERNANCE.md`, `docs/GLOSSARY.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`, `GOVERNANCE.md`, `CONTRIBUTING.md` and grant evidence routing.

D4 is current across all nine supported locale packs. The D4 validator covers **18 project/grant/glossary documents plus nine indexes**, exact source checkpoint, local links and all mandatory capability, authority, grant and certification non-claims.

D1–D4 remain current multilingual public surfaces while D5 adds the extended-reference routing layer.

## 6. D5 completed state

D5 source inventory/policy is anchored to signed `main@d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9`. D5 is current across all nine supported locale packs through **nine Extended Reference Guides** and nine synchronized indexes. The final D5 documentation checkpoint is signed `main@f4556e8f9775d28d4a1b2c20a28962a95e55d33e` from PR #352.

The D5 source validator classifies the live corpus as `CURRENT`, `REFRESH_NEEDED`, `RETIRED` or `ENGLISH_ONLY_BY_DESIGN`. Final inventory is **136 CURRENT**, **126 ENGLISH_ONLY_BY_DESIGN**, **10 RETIRED**, **0 REFRESH_NEEDED**, **272 total** at the completed D5 checkpoint. Detailed ADR/profile contracts, security/privacy/GDPR/legal mapping, tests/benchmarks/CI, machine-readable status, AI/audit/archive context, research/RFC and grant evidence are not bulk translated. Historical snapshots remain preserved with retirement routing.

D1–D5 are current multilingual public surfaces for all nine supported locales: `ar`, `de`, `es`, `fr`, `hi`, `it`, `ja`, `ru`, `zh-CN`. Issue #341 is closed / completed.

See [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md), [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md), [`../EXTENDED_REFERENCE_POLICY.md`](../EXTENDED_REFERENCE_POLICY.md), [`../status/d4-translation-manifest.json`](../status/d4-translation-manifest.json), [`../status/d5-inventory.json`](../status/d5-inventory.json) and [`../status/d5-translation-manifest.json`](../status/d5-translation-manifest.json).

## 7. Post-i18n backlog reconciliation

Tracking issue #353 records the reconciliation evidence. The four stale pre-D5 pull requests were resolved without rebasing them onto current `main`:

- #245 → `MOVE_TO_SEPARATE_RESEARCH_TRACK`; Essence Workdesk prototype was not promoted into Crystal;
- #249 → `MOVE_TO_SEPARATE_RESEARCH_TRACK`; Personal/Full Exo-Cortex planning research stays outside Crystal;
- #261 → `REQUIRES_OPERATOR_DECISION`; no branding, repository, package, import, CLI or environment rename was applied;
- #262 → `SUPERSEDED`; current repository governance already defines the Native Kernel independence boundary and no runtime integration was created.

The bounded remaining backlog is:

- #155 → `REQUIRES_REWRITE`: Epistemic Router remains unimplemented and requires a fresh evidence-based RFC before any runtime discussion;
- #165 → `STILL_VALID`: legacy normalized-ID migration/index remains a separate data-maintenance task;
- #214 → `STILL_VALID`: residual fixture review and reproducible supply-chain pinning remain P2 hygiene.

Issues #156, #157, #203, #219 and ASR Phase-0 #228 were closed as completed from current evidence; #159 was closed as superseded; #211 was closed as out of scope for Crystal; #215 was closed as expired. None of those closures adds a runtime capability.

## 8. Reader Core RC-0 / RC-1 state

The normative Reader Core architecture remains
[`../architecture/READER_CORE_ARCHITECTURE.md`](../architecture/READER_CORE_ARCHITECTURE.md).
RC-0 defines source/version identity, structural maps, Segment Cards, explicit coverage,
multi-pass reading, source-linked bookmarks, exception preservation, contradiction candidates,
open questions, source-fidelity classes, provenance, stale-version invalidation, fail-visible
partial reading and the non-authority test plan.

RC-1 implements only the minimum evidence-linked domain skeleton needed to prove the first
contract invariants. The implementation surface is `core/reader_core.py` with tests in
`tests/test_reader_core.py`:

```text
SourceVersion
  document_id + source_uri + SHA-256
        ↓
SourceLocator
  exact half-open span OR explicit structural locator
        ↓
ReaderSession
  ├─ SegmentCard + SourceFidelity
  ├─ CoverageEntry / CoverageTelemetry
  ├─ ReaderBookmark
  └─ OpenLoop
        ↓
fail-visible interrupted/degraded/stale state
```

The five fidelity classes remain explicit:

```text
DIRECT_SOURCE_OBSERVATION
EXTRACTED_PROPOSITION
READER_INTERPRETATION
SUMMARY
INFERENCE
```

Coverage retains the RC-0 states `UNREAD`, `SEEN`, `PROCESSED`, `REVISITED` and
`NEEDS_REVIEW`. Telemetry reports state counts/gaps only: `coverage != comprehension proof`.
A changed source version conservatively stales the RC-1 session; there is no remapping/diff
engine in this milestone and historical artifacts keep their old source binding.

Authority remains unchanged:

```text
source/document + exact provenance
→ RC-1 Reader artifacts/candidates
→ no automatic admission side effect
→ existing explicit ingest/review/evidence path
→ Guardian / Immune boundary
→ TruthGate
→ multi-status storage
→ strict read projection
```

The machine-readable distinction is intentional:

```text
reader_core_rc1_skeleton = true
dedicated_reader_core    = false
```

RC-1 has no durable Reader storage schema or migration, public API/CLI/background worker,
mandatory dependency, LLM/provider integration, parser/semantic chunker, embeddings/ANN/vector
database, multi-pass orchestration, cross-document reasoning engine, planner/belief-update
authority or direct Canon/TruthGate wiring. Source body text is not retained by the RC-1
source-version object. Restrictions/sensitivity are inherited by derived Reader artifacts.

Therefore RC-1 is implementation evidence for a **minimal evidence-linked skeleton**, not for
a dedicated/full long-document reading system. Reader importance is not truth, Reader
observations are not Canon admission, and contradiction candidates do not replace the existing
contradiction/curator decision contract.
