<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Current verified runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Completed D1–D5 documentation checkpoint:** `main@f4556e8f9775d28d4a1b2c20a28962a95e55d33e` / PR #352  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

Documentation and localization work merged after the runtime checkpoint improves public
contracts and access. It does not create a new runtime capability or grant-funded delta.
Bounded features merged after that checkpoint must carry their own exact-head and post-merge
CI evidence rather than silently rewriting the historical baseline above.

## ✅ Delivered runtime baseline

Crystal includes the trust/evidence/query/storage lifecycle baseline plus:

- source-linked claims, evidence spans, document records and import/review sessions;
- Guardian structural/safety checks and TruthGate epistemic admission;
- read-only public query pipeline with TRACE and receipts;
- durable SQLite ordinary active local-first profile;
- deterministic bounded-streaming SQLite logical export and verification;
- optional lazy PostgreSQL driver path;
- PostgreSQL 16 / pgvector 0.8.2 preflight;
- serializable import into a new inactive schema;
- independent exact-state equivalence and non-secret receipts;
- 2078 tests, 9756 statements, 100% coverage and 9/9 permanent CI at the retained runtime checkpoint;
- 1/1 real PostgreSQL/pgvector integration job.

## ✅ Delivered / tracked multilingual documentation baseline

- English remains the working, source and conflict-resolving language.
- Russian Reader-dependent public/detail documentation is the current fully refreshed non-English Reader surface.
- D2 reviewer/safety and Quick Start remain current for all nine locales because Reader RC-1–RC-4 do not change their source semantics.
- Eight other locale root/detail Reader surfaces preserve rich translations and explicitly track `REFRESH_NEEDED` debt rather than using shortened replacements.
- Detailed residual technical, security, audit, machine-readable and research contracts remain English-only by design where recorded by D5 policy; no native-speaker editorial, security, legal or GDPR certification is implied.

## ✅ Completed storage phases — issues #331 and #332

PR #335 completed bounded logical migration. PR #337 completed the first PostgreSQL phase:

```text
verified bundle
→ PostgreSQL preflight
→ inactive target import
→ independent exact-state equivalence
→ receipts
→ active=false
```

The target cannot serve normal reads/writes and is not registered in ordinary runtime
composition. No activation, cutover, rollback, dual-write or automatic switching was added.

## P1 — Exact-vs-ANN retrieval evaluation

- exact pgvector search as the reference;
- versioned HNSW/IVFFlat evaluation corpus;
- recall@k, filtered recall, latency, index size and rebuild evidence;
- stale-index and missing-index degraded behaviour;
- ANN indexes remain rebuildable, non-authoritative projections.

## P1 — Explicit cutover and rollback proof

- source/target fencing;
- immutable cutover receipt;
- crash-window and partial-failure tests;
- explicit rollback receipt and expiry policy;
- no reachability-based backend selection.

## P1 — PostgreSQL server lifecycle and security

- least-privilege migration/read/runtime roles;
- TLS certificate and credential rotation;
- backup/restore/upgrade drills and retention;
- pooling, timeout/retry, observability and cleanup policy;
- no certification or distributed exactly-once overclaim.

## P2 — Release and independent audit evidence

- reproducible wheel, sdist and container artifacts;
- checksums, SBOM and supported-version manifest;
- pinned or reviewed supply-chain actions;
- clean-machine reproduction and public audit findings;
- stronger claim/status lint tied to releases.

## P2/P3 — Source-linked Reader Core

RC-0 defines the normative architecture contract at
[`docs/architecture/READER_CORE_ARCHITECTURE.md`](./docs/architecture/READER_CORE_ARCHITECTURE.md).
RC-1 adds the minimal evidence-linked source/session skeleton. RC-2 adds the bounded Structural
Document Map. RC-3 adds explicit multi-pass mechanics. RC-4 adds bounded source-linked proposition
extraction from substantively processed pass regions. The machine-readable distinction remains deliberately narrow:

```text
reader_core_rc1_skeleton              = true
reader_core_rc2_structural_map        = true
reader_core_rc3_multi_pass_mechanics  = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core                 = false
```

### ✅ RC-1 — Minimal Evidence-Linked Reading Skeleton

The bounded RC-1 implementation provides:

- source/document identity bound to source URI and exact SHA-256 version;
- exact half-open source spans or an explicit replayable structural locator;
- `ReaderSession` lifecycle with explicit interrupted/degraded/stale state;
- `SegmentCard` with mandatory source-fidelity class;
- explicit `UNREAD` / `SEEN` / `PROCESSED` / `REVISITED` / `NEEDS_REVIEW` coverage states;
- count/gap coverage telemetry with no comprehension percentage;
- minimal source-linked bookmarks and open loops;
- conservative whole-session invalidation when source version changes and no remapping is proven;
- source restriction/sensitivity inheritance;
- tests that structurally isolate RC-1 from ingest, TruthGate, Canon/ESM, contradiction decision writers and planner authority.

### ✅ RC-2 — Structural Document Map

The bounded RC-2 implementation provides a caller-supplied structural model anchored to the
same exact `SourceVersion` / `SourceLocator` semantics:

- document, section/subsection, paragraph, dialogue turn, list/list item, table/table region,
  code block, quotation, footnote/endnote/reference and figure/caption structural kinds;
- stable version-local node IDs, explicit global document order and parent/child hierarchy;
- duplicate-ID/order, missing-parent, cycle and parent-before-child validation;
- exact-span containment checks where parent and child both have exact offsets;
- explicit `RECOVERED`, `AMBIGUOUS` and `UNSUPPORTED` structural state with reasons;
- immutable traversal helpers and structural counts with no comprehension/truth score;
- restriction/sensitivity inheritance from the source version.

RC-2 does **not** discover structure automatically. It adds no parser/semantic chunker, OCR,
PDF-layout reconstruction, image understanding, multimodal parser, LLM/provider integration,
embeddings, ANN/vector DB, durable Reader storage schema, public API/CLI/background worker,
cross-document reasoning engine, planner or automatic belief update. Structural prominence and
document order are metadata, not truth/confidence authority.

### ✅ RC-3 — Explicit Multi-Pass Reading Mechanics

The bounded RC-3 implementation provides deterministic process mechanics over one OPEN RC-1
session and one exact-version RC-2 structural map:

- five pass kinds: `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD`;
- one active pass at a time;
- immutable-style pass records with `ATTEMPTED`, `COMPLETED`, `INTERRUPTED`, `DEGRADED` state;
- declared structural target IDs before a pass starts;
- explicit per-target RC-1 coverage outcomes rather than hidden progress;
- completion only when every declared target has an outcome;
- partial progress preserved on interrupted/degraded passes;
- unresolved RC-2 structure forced to fail-visible `NEEDS_REVIEW`;
- cross-check and targeted re-read require prior substantive processing;
- targeted re-read requires an explicit rationale;
- count-only telemetry; no comprehension, truth or authority score;
- source restriction/sensitivity inherited by pass records.

RC-3 is **not** an autonomous reader. It does not call an LLM/provider, discover structure, choose
research objectives, infer undeclared targets, resolve contradictions, perform automatic
cross-document reasoning, mutate Canon/ESM or own planner/belief authority. `pass completion !=
comprehension proof`.

### ✅ RC-4 — Source-Linked Proposition Extraction

The bounded RC-4 implementation turns eligible completed RC-3 pass regions into explicit
pre-admission proposition candidates:

- extraction requires a `COMPLETED` Reader pass;
- every extraction node must be a declared target of that pass;
- the recorded pass outcome and current matching coverage must be `PROCESSED` or `REVISITED`;
- unresolved structure, `SEEN`, `NEEDS_REVIEW`, source/session mismatch or stale/mismatched provenance fail closed;
- every candidate is a source-linked `SegmentCard` with `EXTRACTED_PROPOSITION` fidelity;
- primary and optional same-version supporting locators remain replayable;
- source owner remains explicit;
- source presentation remains explicit across factual assertion, author opinion, hypothesis,
  conditional, example, quoted speech, reported position, definition and uncertain assertion;
- negation and scope/exception qualifiers remain explicit;
- restriction/sensitivity is inherited from the source;
- telemetry is count/category state only, never truth, confidence or evidence sufficiency.

RC-4 is **not** automatic NLP/model extraction. The caller supplies the proposition; RC-4 validates
that it is structurally and procedurally eligible to exist as a Reader candidate. RC-4 does not call
`core.evidence.attach_evidence()`, create fact evidence, write Canon, mutate `truth_status`/ESM,
bypass Guardian/TruthGate, resolve contradictions or create planner/belief authority.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### ⏭️ Later Reader phases

A dedicated/full autonomous Reader Core remains not implemented; RC-1/RC-2/RC-3/RC-4 are bounded layers.
The next phase must be separately authorized and should come from measured need. Candidate sequence:

```text
RC-5 exceptions / contradiction candidates
→ RC-6 long-context strategy
→ RC-7 cross-document reading
→ only then reassess semantic/vector retrieval needs
```

Any later phase must preserve:

- Reader artifacts/candidates upstream of normal admission;
- `coverage != comprehension proof`;
- `pass completion != comprehension proof`;
- `EXTRACTED_PROPOSITION != verified fact`;
- `Reader candidate != admitted evidence`;
- structural position != epistemic authority;
- source observation/extraction/interpretation/summary/inference separation;
- contradiction candidates without automatic resolution;
- no second Canon owner or planner/belief-update authority.

## Grant boundary

The baseline/funded-delta rule is:

```text
verified existing baseline + new measurable funded delta
= independently verifiable public deliverable
```

Issues #331/#332, PRs #335/#337 and D1–D5 documentation work merged before an agreement are
existing baseline. Reader RC-0/RC-1/RC-2/RC-3 are pre-agreement baseline. RC-4, if merged before an
agreement, likewise becomes existing baseline and cannot be counted again as future paid delivery.
The next Reader funded delta, if any agreement later exists, must begin after the actually merged
pre-agreement Reader baseline rather than rebudgeting RC-4.

No grant award or approved budget is claimed. Approximate €50,000 remains planning only.
Active PostgreSQL runtime selection, automatic switching, production multi-tenancy, universal
truth, zero hallucinations and legal/security/GDPR certification remain out of scope.

## Related documents

- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./docs/grants/funding-use-plan.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader Core RC-0 architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Extended reference policy](./docs/EXTENDED_REFERENCE_POLICY.md)
