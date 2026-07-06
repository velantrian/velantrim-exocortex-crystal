# 📋 Changelog

All notable changes to Velantrim ExoCortex — Crystal are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Versioning note.** `0.1.0` is the **first public release** of the open core.
> The architecture descends from the internal "v8" Crystal design line (tracked in
> `ROADMAP.md`); the published package version in `pyproject.toml` is the single
> source of truth for releases.

## [Unreleased]

### Added
- **Deterministic `response_policy` v0** (#201): new pure read-path module
  `core/response_policy.py` (`decide_response_policy`) decides response framing
  (e.g. `requires_citation`) from `claim_type`, `source_status`, and
  `epistemic_state`. Read-path only — no TruthGate calls, no L3 writes, no new
  runtime deps; a static guard test pins the no-forbidden-calls invariant. See
  `docs/RESPONSE_POLICY_V0.md`.
- **Research Mode v0.5 scaffold** (#204): exploratory `EssenceCard` model under
  `prototypes/research_mode/` — excluded from the installable runtime package
  list, not wired into `core/`, TruthGate, storage, the extractor, the worker,
  or the dashboard. 20 new tests.

### Fixed
- **Small correctness hardening after the audit follow-up** (#222): five
  small, independent correctness/UX bugs, plus two Codex-review follow-ups.
  (1) `truth_gate()` treats a missing `confidence` as a controlled rejection
  instead of raising `KeyError` — gate semantics unchanged, only the
  rejection-message construction was crashing. (2)
  `volition.write_voluntary()` now passes `source_status="USER_REPORTED"`
  explicitly instead of relying on `classify_claim()`'s fallback, so a
  self-authored fact's status is declared, not incidental. (3)
  `erase_fact()` is a true no-op for a `fact_id` that never existed (no
  tombstone/audit/provenance event), while still correctly erasing an
  L3-only orphan — a fact_id present only in the canonical graph, not L1
  (initial fix missed this; caught in Codex review and fixed in the same
  PR). (4) the `retrieval-config-set` CLI returns a controlled `invalid
  retrieval config: ...` error instead of a raw traceback on malformed
  numeric input (`k=abc`, `k=--5`). (5) `pii.py`'s PHONE detector no longer
  false-flags a bare ISO-8601 date (`2026-07-06`) as personal data,
  validated via `datetime.strptime` rather than shape alone (a shape-only
  check would have wrongly exempted phone-like values such as
  `5555-12-34`; also caught in Codex review). 8 new regression tests.
- **P0 integrity follow-up to the audit-hardening PR (#206)** (#216): three
  audit-confirmed integrity bugs. (1) `store_fact()` upsert no longer poisons
  the L0 cache with a reset `restricted` flag or a fresh `created_at` on a
  conflict-update — both are now re-read from the persisted row, mirroring the
  existing `epistemic_state` fix (#195). (2) `audit.append_event()` /
  `provenance_chain.append()` serialize their read-tail-then-insert sequence
  with `BEGIN IMMEDIATE` plus a bounded retry (`memory.call_with_lock_retry`)
  instead of racing on a computed `seq`, which could silently drop a
  compliance/provenance event under concurrent writers (e.g. FastAPI's thread
  pool). (3) `knowledge.ingest_claims()` now reports `new_fact_ids` (facts this
  call actually created) separately from `fact_ids` (all accepted, including
  duplicate hits of pre-existing facts); `imports.import_file()` enrolls only
  `new_fact_ids` into the import session, so a session that only duplicated an
  existing claim can no longer `erase_session()` / `restrict_session()` a fact
  it never created. 7 new regression tests.
- **PDF adapter span preservation** (#182): repeated identical paragraphs now
  keep distinct source spans (`core/adapters/pdf_adapter.py`). Adds a regression
  test in `tests/test_wp1_spans.py`; the suite stays at 100% coverage (exact
  count lives in the README badge / `TEST_REPORT.md`).
- **CAS guard on ESM transitions** (#190): `transition_esm` is now a
  compare-and-swap — the update matches on the expected prior state, checks
  rowcount, and only updates the L0 cache after the DB write succeeds. On a
  CAS miss the stale L0 entry is evicted and the promotion callers
  (`core/pipeline.py`, `core/ingest.py`, `core/review.py`) abort instead of
  continuing to an L3 merge / success / audit path. Low-severity
  defense-in-depth for concurrent/async use, not a full atomicity guarantee.
- **`store_fact` upsert no longer overwrites `epistemic_state`** (#195): the
  `ON CONFLICT DO UPDATE` in `core/memory.py` was silently overwriting an
  existing fact's `epistemic_state`, bypassing the `ESM_TRANSITIONS` matrix
  enforced by `transition_esm()`. The conflict path now preserves the
  persisted state and re-reads it within the same connection before the L0
  cache is populated; `core/pipeline.py` syncs the in-flight fact dict from
  the persisted store before the ESM promotion guard runs.
- **`test_p0_hardening` subprocess `ModuleNotFoundError`** (#197): probe
  subprocesses spawned outside the repo (`cwd=tmp_path`) now get the repo root
  prepended to `PYTHONPATH`, fixing two tests that import `core.memory`.

### Documentation
- **Epistemic dogfooding cases log** (#183): added
  `docs/dogfooding/EPISTEMIC_CASES.md` (KNOWN / PARTIAL / UNKNOWN cases).
  Docs-only; evaluation input, not a source of truth.
- Status / grant docs synced to the post-#182/#183 baseline. The exact test count
  now lives only in the README badge and `TEST_REPORT.md`; other docs point there.
  Bio-inspired `core/` modules are clarified as tested baseline mechanisms /
  engineering metaphors — not biological cognition and not the full Personal
  Research Mode (which is tracked separately, outside this repository).
- **Claim metadata glossary linked from README** (#189).
- **Audit-grounded ADRs 007-010** (#191): added to `docs/ADR.md`.
- **STRIDE threat model** (#192): added `docs/security/threat-model.md`, then
  linked from `SECURITY.md` (#193).
- **Softened Codex-flagged accuracy claims** (#194): narrows reviewer-facing
  wording in `docs/ADR.md`, `docs/security/threat-model.md`, and
  `docs/REVIEWER_GUIDE.md` to match verified code behaviour (addresses
  unresolved Codex accuracy comments on #191, #192, #176). Docs-only; no
  runtime change.
- **Staged working-memory admission boundary note** (#198, clarified in #199):
  added and then refined `docs/architecture/STAGED_WORKING_MEMORY_ADMISSION.md`.
- **README positioning note** (#200): grant-safe positioning draft at
  `docs/grants/grant-safe-readme-positioning.md`.
- **Status sync after response_policy and Research Mode scaffold** (#205):
  README / `TEST_REPORT.md` baseline updated to 1252 passed / 12 skipped /
  100% coverage (69 test files, confirmed by a fresh full-suite run on
  `main @ 063cfdc`); `docs/STATUS.md` records #201 as IMPLEMENTED and #204 as
  a RESEARCH scaffold under `prototypes/research_mode/`, explicitly not wired
  into runtime/TruthGate/storage/extractor/worker/dashboard. Docs-only; PR
  #202 is noted as DRAFT (not merged, not implementation truth).

## [0.3.0] — 2026-06-17 (reviewer preview)

> Audit-hardening milestone (Tracks 1–3B) + reviewer packaging. Tagged
> `v0.3.0-reviewer-preview`. Runtime freeze after this release: no new features,
> only reviewer-facing packaging. Test baseline: 1209 passed, 12 skipped, 100%
> coverage. Deferred (not in this release): knowledge-graph data verifier,
> broader ProvenanceChain lifecycle wiring, canonical write-path expansion.

### Added
- **Write-path TruthGate audit** (Track 3B): `core/review.py` now records
  `gate_reason` (the specific blocking reason from the gate diagnosis) in the
  `review_force_approve` audit detail, so a curator override is accountable
  against *why* the gate blocked — not just that it did. Content-free (no claim
  text). New behaviour pins in `tests/test_write_path_gate.py` and
  `tests/test_api.py`: force-approve still calls TruthGate; the override audit
  carries `gate_reason`; `POST /ingest` with `LLM_OUTPUT + WORLD_FACT` is
  blocked (`accepted=False`); a bulk dry-run predicts a `blocked` verdict for
  the same case. Behaviour-pinning + audit detail only — no new write paths and
  no `/facts` endpoint.
- **Strict TruthPolicy production default** (Track 3A): `core/truth_gate.py` now
  reads `ENABLE_TRUTH_POLICY` (at call time, so it is test-overridable) to make
  the strict policy the explicit, documented default — `unset` and `on` both
  mean strict ON; only `ENABLE_TRUTH_POLICY=off` opts into the legacy bypass of
  the `LLM_OUTPUT`→`WORLD_FACT` rule (the fact is then judged on source +
  confidence alone). Secure-by-default: any value other than `off` is strict.
  3 behaviour tests in `tests/test_truth_gate.py` pin on / off / unset. The
  source requirement and confidence threshold are unchanged in all modes.
- `core/provenance_chain.py`: per-fact, append-only, hash-chained provenance log
  (Sprint1 P1-5, invariant I89 ProvenanceAppendOnly). Distinct from the **global**
  compliance ledger (`core/audit.py`) and the per-**answer** receipt provenance
  (`core/provenance.py`): this chain records the ordered lifecycle events of a
  single fact. Each entry seals `sha256(prev_hash|event_type|fact_id|from_state|
  to_state|payload_str|created_at|actor|reason)` and links to the previous entry
  for the same `fact_id`, so editing/deleting/reordering any past entry is
  detectable. `append()` is content-light (hash/marker, never claim text) and
  never raises (returns `False` on failure, so a provenance-write problem cannot
  block a critical-path caller); `verify()` reports an empty chain as
  `empty_chain`/`no_events` — never as a verified non-empty chain. New SQLite
  table `provenance_chain` in `core/memory.py`. Currently wired into the GDPR
  erasure path (`core/erasure.py::erase_fact` records an `erase` event); broader
  lifecycle wiring (ingest/promote/restrict) is follow-up.
- `core/rrf.py` (PR #163): pure-stdlib Reciprocal Rank Fusion helper for rank
  fusion / retrieval ordering. Implemented as a standalone helper — it does not
  assign `truth_status`, does not change `confidence`, and does not bypass
  TruthGate or Guardian. Not yet wired into `retrieve()`.
- `core/refusal_reasons.py`: stable machine-readable Refusal Reasons Taxonomy v0.1 —
  13 reason codes (`NO_VERIFIED_CLAIM`, `LLM_OUTPUT_NOT_EVIDENCE`, `MISSING_SOURCE`,
  `MISSING_PROVENANCE`, `MISSING_EVIDENCE`, `MISSING_TRACE`, `RECEIPT_TAMPERED`,
  `CONTRADICTION_UNRESOLVED`, `UNSUPPORTED_SCHEMA_CHECK`, `TRUTHGATE_REJECTED`,
  `GUARDIAN_BLOCKED`, `REQUIRES_HUMAN_REVIEW`, `OUT_OF_SCOPE`) with `code`, `title`,
  `severity` (INFO/WARN/ERROR/CRITICAL), `description`, and `suggestion` fields;
  API: `get_reason()`, `is_valid_reason()`, `list_reasons()`, `format_reason()`
- `core/invariant_check.py` now populates `reason_code` on failing and SKIPPED
  check entries and issue entries (PASS entries carry no `reason_code`)
- `docs/REFUSAL_REASONS.md`: full taxonomy documentation (codes, severities,
  integration with `invariant-check`, stability guarantee, what it does NOT do)
- `examples/refusal_reason_llm_output.json`,
  `examples/refusal_reason_missing_source.json`,
  `examples/refusal_reason_receipt_tampered.json`: reference JSON examples
- `core/invariant_check.py`: read-only machine-executable invariant checker —
  verifies selected epistemic invariants over the current L3 canonical state and
  emits a machine-readable JSON report; 3 implemented checks
  (`no_llm_output_verified`, `verified_requires_source`,
  `verified_requires_evidence`) + 2 `SKIPPED_UNSUPPORTED` checks with honest
  explanations; exit codes 0=PASS / 1=WARN / 2=FAIL
- `velantrim invariant-check` CLI command
- `docs/INVARIANT_CHECK.md`: documentation (what it does, what it does NOT do,
  SKIPPED_UNSUPPORTED semantics, exit codes, example outputs)
- `examples/invariant_check_pass.json`, `examples/invariant_check_fail.json`:
  reference output examples
- `core/trace_visualize.py`: read-only TRACE / Receipt visualization formatter (Markdown + DOT output) for reviewer tooling
- `scripts/trace_visualize.py`: CLI wrapper for trace visualization
- `docs/TRACE_VISUALIZATION.md`: documentation for the visualization helper
- `docs/PERSONAL_OVERLAY_RFC.md`: Future RFC for a personal-deployment overlay layer
  (status: design artifact only, not Crystal runtime — no TruthGate/Guardian/L3 changes)
- `schemas/personal_overlay.schema.json`: JSON Schema for future personal overlay records;
  `allOf` conditionals make `store_full_numbers`, `store_full_address`, and
  `requires_user_confirmation_before_use` **required and constrained** when
  `sensitivity: highly_sensitive`, and make `not_world_fact: true` **required**
  for `EMOTION`, `INTERPRETATION`, `PRIVATE_CONTEXT`, and `SENSITIVE_CONTEXT` claim types.
  Note: `store_full_numbers: false` and `not_world_fact: true` are **default-annotated**
  (recommended) values for all records; records omitting these fields still validate
  unless the conditional triggers apply — operators must enforce the privacy policy at
  application level for records that do not match the conditional conditions
- `examples/personal_overlay.redacted.sample.jsonl`: five synthetic redacted sample records
  (preference, goal, legal context pointer, health caution flag, emotional context);
  no real sensitive identifiers

### Fixed
- **Exact-duplicate ingest dedup — repeat is frequency, not evidence** (PR #164,
  Variant B): previously an exact repeat of an already-`Validated` fact was
  treated as independent evidence and auto-reinforced (`confidence++`). Now an
  exact repeat updates occurrence metadata only — `occurrences` / `last_seen` /
  `sources_seen` / `fingerprint_sha256` (kept separate from `observations`) — via
  the new `core/reconcile.record_occurrence`. It does not call `reinforce()`,
  does not increase `confidence`, and does not count as independent evidence.
  `core/ingest._fact_id` now hashes normalized content (NFC + trim + collapse
  whitespace + casefold) with a legacy raw-text id fallback; dry-run verdicts in
  `imports.py` / `kb_ingest.py` were synced (`reinforce` → `duplicate`). Legacy
  normalized-id migration / normalized-claim index is tracked separately in #165
  and is not implemented in this change.
- **README docs-table duplicate**: removed the remaining duplicate
  `docs/COMPARISON.md` row from the README documentation table (a previous
  changelog entry claimed this was already done; the duplicate was in fact still
  present and is corrected in this hygiene pass).
- **CI coverage gap** (PR #130): `ebooklib` and `requests` were missing from
  `requirements-dev.txt` and `pyproject.toml [dev]`; their absence caused
  `tests/test_adapters.py` to be skipped wholesale in CI (39 tests, including
  YAML/PDF/RDF/BibTeX coverage), dropping coverage below 100%.
- **TRACE viz — list input** (PR #130): `_extract_receipt_and_verify` now handles
  trace-array (`list[dict]`) input from `build_trace()`; previously crashed with
  `AttributeError` on `.get()`.
- **TRACE viz — DOT backslash escape** (PR #130): `_escape()` in `to_dot` now
  escapes `\` before `"`, producing valid DOT when fact_ids contain backslashes.
- **TRACE viz — per-citation verify status** (PR #130): `to_markdown` now
  surfaces `verify["citations"]` status next to each citation (e.g. `, verify=ok`).
- **scripts/trace_visualize.py direct execution** (PR #130): added
  `sys.path.insert(0, repo_root)` bootstrap so the script works when run
  directly as `python scripts/trace_visualize.py ...`.

### Changed
- Synchronized the README badge and `TEST_REPORT.md` baseline after the PR #137
  safe repo hygiene pass (1130 → 1141 tests, 5130 → 5158 statements; 100%
  coverage preserved). The full per-module coverage table was regenerated so its
  rows and total agree with a live `--cov=.` run.
- Clarified in `docs/IMPLEMENTATION_STATUS.md` and `ROADMAP.md` that the
  implemented Crystal **Fractal Memory baseline** (multi-scale anchoring) is a
  memory anchoring mechanism, distinct from the broader private Personal Research
  Mode concept ("Fractal Memory = Structure + Attention + Consolidation") and
  from Fractal Attention; recorded the implemented optional knowledge adapters as
  shipped baselines rather than future work.

## [0.2.0] — 2026-06-13

### Added
- **PR5 — Force Override Audit Pinning** (grant WP2 hardening):
  - `core/review.py` — `approve(..., force=True, ...)` now emits a
    `RuntimeWarning` when a blocked fact is force-approved; message is
    content-free (fact_id, actor, diagnosis — no claim text). All existing
    guards preserved: explicit non-empty actor required, non-empty reason
    required, 500-char reason limit enforced, `review_force_approve` audit
    event and `review.override` metric unchanged.
  - `tests/test_force_override_audit.py` — 11 behaviour-pinned tests:
    rejection without actor/reason, RuntimeWarning emission, content-free
    warning and audit event, normal approve emits no warning, metric
    increment.
- **PR4 — KB Dry-Run Batch Manifest** (grant WP2/WP4 hardening):
  - `core/kb_ingest.py` — `dry_run_batch(claims)` and
    `dry_run_manifest_file(path)` predict accept/reinforce/blocked/conflict
    for every claim in a JSONL or JSON-array manifest WITHOUT writing
    anything to memory; reuses the same Guardian + TruthGate pipeline as
    the live ingest path so preview matches reality.
  - `core/cli.py` — `velantrim kb-ingest <manifest.jsonl>` CLI command.
  - `tests/test_kb_dryrun.py` — 16 behaviour-pinned tests: manifest shape,
    LLM_OUTPUT blocking, EXTERNAL accept, reinforce detection, empty claim,
    no-write invariant, JSONL/JSON/NDJSON file I/O, FileNotFoundError,
    ValueError on non-array JSON, custom source, empty file, CLI round-trip.
- `docs/SPARK_RFC.md` (new) — Future RFC for the Spark Layer: sandboxed
  generative/exploratory reasoning within the Velantrim Exo-Cortex; covers
  Imagination Mode, the Spark-to-Crystal Bridge (plausibility pre-filter),
  Spark output types and their canon eligibility, Mode Layer integration,
  and an explicit boundary distinguishing Spark (a technology component) from
  Velantrim Culture (a human/social layer, out of scope for Crystal).
  Status: Future RFC / v0.3.0+ research roadmap / no runtime feature.
- `docs/IMPLEMENTATION_STATUS.md` — Imagination Mode / Spark row updated with
  link to SPARK_RFC.md; SPARK_RFC added to Future RFC backlog.
- **PR3 — Resumable Review Sessions** (grant WP2 hardening):
  - `core/memory.py` — `review_sessions` SQLite table with DDL auto-migration
    on `_db()` open; `save_review_session`, `get_review_session`,
    `list_review_sessions` storage helpers.
  - `core/review.py` — `create_session`, `get_session`, `list_sessions`,
    `resume_session`, `record_session_decision`, `complete_session` — a
    session snapshots pending claim IDs at creation; `resume_session` returns
    only unresolved Observed items in stable order (the curator sees the same
    batch on return). No claim text stored in session records.
  - `tests/test_review_resumable.py` — 14 behaviour-pinned tests covering
    session lifecycle, the core resumability invariant
    (`test_review_resume_shows_same_pending_claims`), decision recording,
    batch_size cap and status filtering.
- Future RFC document `docs/EPISTEMIC_INFRASTRUCTURE_UPGRADE.md` — Temporal Layer,
  Context/Scope, Conflict Resolution, Negative Knowledge, Known Unknowns, Plausibility
  Pre-Filter, Confidence Calibration and Epistemic Debt; explicitly marked as
  non-runtime / v0.3.0+ research roadmap.
- `docs/DIGITAL_SOVEREIGNTY.md` — "Efficient AI" section with future evaluation
  metrics (`llm_calls_avoided_per_query`, `tokens_saved_per_answer`, etc.);
  no performance guarantees claimed.

### Changed
- `README.md` — geopolitical wording tightened: "US-based or other third-party
  AI providers" → "external third-party AI or cloud providers outside
  operator-controlled infrastructure"; healthcare row clarified to add
  "not for clinical decision-making, diagnosis, or treatment".
- `SECURITY.md` — supported-version table split: `0.1.x` (active Crystal line)
  separated from `8.x` (historical/separate research archive, not the
  grant-facing support target).
- `docs/IMPLEMENTATION_STATUS.md` — `EPISTEMIC_INFRASTRUCTURE_UPGRADE` added
  to Future RFC backlog; Resumable Review Sessions marked Implemented.

## [0.1.1] — 2026-06-13

### Added
- **T5 — Reviewer demo package** (docs-only, no runtime change):
  `docs/REVIEWER_DEMO.md` — a 10-minute hands-on reviewer path with output
  captured at the audited baseline: isolated setup → ingest (USER_CLAIMED
  honesty) → answer without an LLM → typed-canon report → sourced import with
  evidence spans (VERIFIED) → sealed receipt → strict-provenance replay →
  controlled receipt-integrity check on a copy (tampered receipt is detected)
  → evaluation gate with enforcing boundary metrics. Root `DEMO.md` becomes a
  thin demo index pointing at the maintained walkthroughs (REVIEWER_DEMO /
  docs/DEMO / DEMO_UI) so the demos cannot drift apart; links added in
  README, REVIEWER_OVERVIEW and REVIEWER_NOTES; `demo-data/` and
  `eval-artifacts/` added to `.gitignore` so the demo leaves the tree clean.

### Changed
- **T4 — Reproducible MVP packaging** (no runtime behaviour change): the
  documented reviewer path (`pip install -e '.[dev]'` → `pytest` →
  `eval_gate`) now actually reproduces the audited state from a clean clone —
  the `[dev]` extra was missing six test-exercised optional layers
  (fastapi/httpx/cryptography/pyyaml/pypdf/rdflib) and is now aligned with
  `requirements-dev.txt` (cross-referenced as a single documented path; CI
  workflows untouched); the YAML-adapter edge test gains a missing
  `importorskip` guard (skips instead of erroring without pyyaml); generated
  evaluation artifacts (`eval_report.md`, `metrics.jsonl`) are no longer
  tracked, so running the validation no longer dirties the working tree;
  README and REVIEWER_NOTES gain a "clean clone → green run → clean tree"
  reviewer-validation block; RELEASE_CHECKLIST adds fresh-venv,
  artifact-hygiene and `python -m build` (manual) smoke checks; the two
  remaining legacy root documents carry historical-status banners.

### Added
- **T3 — Eval corpus expansion: trust-boundary behaviour corpus** (eval-only
  core addition; TruthGate/pipeline/ingest behaviour untouched):
  - new `core/_eval_fixtures/boundaries.json` — 15 behaviour cases pinning the
    existing trust boundaries in the eval gate: abstention on unsupported
    queries, the LLM_OUTPUT→VERIFIED promotion ban, subjective-claim typing
    (OPINION/EMOTION → SUBJECTIVE, INTERPRETATION → HYPOTHESIS), and no-trace
    refusal;
  - new `core/eval.boundary_eval()` replays the corpus against the live
    pipeline and reports two **enforcing** gate metrics:
    `boundary.refusal_correctness = 1.0` (floor) and
    `boundary.violations = 0` (ceiling); `run_baseline()` runs the boundary
    corpus first on the fresh canon (custom fixtures skip it and the gate
    skips the thresholds accordingly);
  - retrieval corpus 16 → 22 cases (6 new domains), contradiction corpus
    12 → 15 labelled pairs (negation, numeric, hard negative) — aggregate
    metrics improved (hit@1 0.875 → 0.9091, precision 0.857 → 0.8889);
  - T2 vocabulary guard tests: schema enums must stay bit-identical to
    `core/memory.py` (and `FACT` must never appear as a machine
    truth_status), fixture vocabulary must stay canonical;
  - narrow, negation-aware research-status guard test: reviewer/status docs
    must never present ProfSearch / Causal Spine / Meta-Cognitive Monitor /
    Training Substrate / Temporal Layer as implemented runtime;
  - test baseline: see `TEST_REPORT.md` (counter hygiene).
- **Research-inspirations boundary** (docs-only, reviewer-package follow-up):
  explicit boundary that research inspirations (memory science, human-computer
  augmentation, cybernetics, biological patterns) are **non-normative** and
  must not be presented as implemented runtime behavior — new ADR-006, a short
  "Research context" paragraph in the reviewer overview (Memex / Licklider /
  Engelbart as architectural inspirations only), two new failure-mode rows
  (research-inspiration and biological-metaphor confusion) and a
  `research_status_confusion_count` target metric.
- **Reviewer-facing documentation package** (docs-only): `docs/REVIEWER_OVERVIEW.md`
  (one-page grant-safe overview: problem, solution, invariants, verified
  status table, roadmap, non-goals), `docs/ADR.md` (five architecture decision
  records incl. truth-vs-speech separation and the Ring Zero optimization
  boundary), `docs/FAILURE_MODES.md` (honest risk matrix with
  implemented/partial/RFC statuses) and `docs/EVALUATION_METRICS.md` (target
  metrics for T3/T4 and future ReplayBench; Meta-Cognitive Monitor explicitly
  marked future research umbrella, not runtime). Linked from README,
  IMPLEMENTATION_STATUS and REVIEWER_NOTES.

### Changed
- **T2 — KB schema and vocabulary alignment** (docs/schema only, no runtime
  behaviour change): the KB roadmap example now uses the canonical machine
  vocabulary (`truth_status: VERIFIED` — `FACT` is a human-facing alias only;
  `fact_id` instead of `id`; KB-layer extension fields explicitly labeled);
  `guardian_verified` is marked **reserved / not emitted by the runtime yet**
  in both schemas; `metadata.schema.json` is labeled a **target** provenance
  envelope (current runtime provenance lives in trace/receipt/audit);
  `trace.schema.json` now describes the artifacts the runtime actually emits
  (trace items from `core/trace.py` and sealed v2 receipts from
  `core/provenance.py`, identified by content digest — no separate
  receipt_id); `docs/grant-readiness-hardening.md` wording made precise
  (enums aligned; structure aligned by this pass); the old
  `docs/architecture/implementation-status.md` bridge carries a superseded
  banner pointing to `docs/IMPLEMENTATION_STATUS.md`. No new truth_status
  values were added (no REJECTED/DEPRECATED).
- **P0.1 docs honesty cleanup** (docs/comment-only, no runtime change):
  neutralized the remaining affirmative overclaim wording — `core/observe.py`
  header comment no longer says "without hallucinations" (now:
  source-grounded memory observability); the legacy design spec
  `docs/Velantrim_V8_Crystal_Sprint1_toc.md` gains a visible historical-status
  banner pointing to `docs/IMPLEMENTATION_STATUS.md`, and its
  "Production-Ready Components" / "Fully autonomous agent" /
  "Production-ready …" phrases are reworded to historical/bounded design
  language. The GitHub repository description still requires a manual update
  in settings (tracked in the PR).

### Added
- **RFC: Harness Replay and Meta-Optimization**
  (`docs/RFC_HARNESS_REPLAY_OPTIMIZATION.md`, documentation-only): a future,
  not-implemented design for auditable trajectory recording, controlled replay
  of candidate harness configurations, Pareto-based multi-objective evaluation,
  an immutable ContractGuard (candidates can never disable TruthGate/Guardian/
  trace or write to L3) and a mandatory human curator approval loop. RFC-only:
  no runtime code, schemas or dependencies; short pointers added to ROADMAP,
  IMPLEMENTATION_STATUS and REVIEWER_NOTES.
- **EITI → Crystal audit series (PR #93–#98)** — six sequential, gate-preserving
  PRs porting sterilized EITI concepts into the verifiable core:
  - *PR #93* — documentation consistency pass: canonical repo-wide coverage
    command in `DEMO.md`, honest L2 baseline status in README/ARCHITECTURE,
    delivered baselines moved out of the roadmap's future-work list.
  - *PR #94* — **tunable retrieval configuration** (`core/retrieval_config.py`):
    five bounded, validated knobs (defaults bit-identical to the historical
    constants), `VELANTRIM_RETRIEVAL_CONFIG` env loading, content-free
    `retrieval_config_saved` audit event, `retrieval-config-show`/`-set` CLI.
  - *PR #95* — **salience-derived significance** (`core/salience.py`):
    auto-significance for live utterances from CAPS/exclamation/importance
    markers (RU+EN), explainability metadata with fixed marker categories only;
    ranking-only — never touches confidence, truth_status or epistemic state.
  - *PR #96* — **opt-in trigram embedder + Russian eval corpus**:
    `hashing-trigram-2048` for morphology-tolerant retrieval (the default
    word-level embedder and its id stay frozen), report-only
    `velantrim eval --lang ru` corpus with typo/morphology probes; the English
    CI eval gate is unchanged.
  - *PR #97* — **MOSC advisory claim-type classifier** (`core/mosc.py`):
    validated keyword weights (package data, audited content-free overrides via
    `VELANTRIM_MOSC_PATH`), abstains below threshold in favour of the
    historical regex fallback; never suggests WORLD_FACT, never writes to L3.
  - *PR #98* — **review HTTP API + static Kanban review UI**: token-guarded
    `/review/*` endpoints (constant-time Bearer comparison), force-approve
    uses a mandatory reason and a dedicated `review_force_approve` audit
    event (explicit actor accountability hardening follows in the next PR),
    dependency-free `core/_webui/review.html` shell that embeds no memory
    content.

### Security
- **Post-merge hardening round** (cross-audit follow-up to PR #93–#98):
  - force-approve now demands an **explicit** non-empty actor — the
    backward-compatible default identity `curator` applies only to normal
    (non-force) approves and can no longer sign a blocking-diagnosis override
    (library refusal + HTTP 422 + CLI `--actor` without a default);
  - force-approve reason is capped at 500 characters (library + pydantic);
  - MOSC weights `threshold` is bounded to `(0, 5]` — an absurdly large
    threshold would silently mute the classifier;
  - `save_config()` sha256 now covers the **exact file bytes** (including the
    trailing newline), so `sha256sum <file>` matches the audit event;
  - `review.decisions(include_claim=False)` and
    `GET /review/decisions?include_claim=false` return content-free decision
    records without rehydrating claim text/claim_type from L1 (the review UI
    keeps the default `true`);
  - PII-negative pin test: salience explainability metadata carries only
    marker categories and numeric scores, never raw emails/phones/text.

### Changed
- **Docs honesty hotfix (P0, documentation-only):** clarified architecture
  status boundaries — Crystal core vs full Exo-Cortex vision vs Velantrim
  Culture (`docs/IMPLEMENTATION_STATUS.md`); made "Graph = Truth" technically
  precise (physical graph = multi-status memory space; canon = the VERIFIED,
  trace-valid subgraph); added a concise technical Ring Zero definition;
  clarified graph-backend roles (SQLite default, LadybugDB candidate in the
  Kuzu lineage, KuzuDB legacy/archived predecessor, Neo4j optional
  inspector/demo tooling — never required runtime).
- **TruthGate extracted into `core/truth_gate.py`** (move-only, behaviour
  preserved bit-for-bit): the verification boundary is now visible as a
  first-class module; `core/pipeline.py` re-exports `truth_gate`, so every
  existing import path (`ingest`/`review`/`reconcile`/`imports`) and the
  `monkeypatch.setattr(pipeline, "truth_gate", …)` test idiom keep working
  unchanged. `_truth_status_for()` intentionally stays in `pipeline.py`.
  New pin tests freeze the gate semantics (LLM_OUTPUT-as-WORLD_FACT blocked,
  subjective pass, low-confidence and missing-source blocked, adaptive
  threshold via `core/adaptation`). Test baseline after the extraction: 838.
  Counter hygiene: exact test counts now live only in `TEST_REPORT.md` and the
  README badge; every other document references the report instead of carrying
  a number that can drift.
- **P1 cross-audit hardening** (follow-up to the P0 round):
  - the evaluation harness now replays receipts with `strict_provenance=True`,
    so a VERIFIED citation without source-span evidence fails
    `receipt_replay_survival` (and the CI eval gate), not just the
    `unsupported_provenance` count;
  - `velantrim verify-receipt` gains `--strict-provenance` (parity with the
    HTTP API's `strict_provenance` option);
  - README adds two deployment-honesty notes: the sector table now carries an
    explicit caveat (local single-user library — no auth/multi-tenant, on-disk
    L3 not field-encrypted yet) and the FastAPI section a "localhost-only,
    no auth" warning;
  - `core/l3_graph.py` comments no longer assert the unverified
    "successor to Kuzu / Apple acquisition" claims (now: "Kuzu lineage;
    upstream repository archived Oct. 2025") and the stale "default — mock"
    header comment matches the real `auto` chain;
  - removed the duplicated `docs/COMPARISON.md` row in the README
    documentation table.

### Fixed
- **P0 cross-audit hardening** (Claude / ChatGPT / Grok review):
  - `VELANTRIM_DB` is now actually read by `core/memory.py`, so
    `scripts/eval_gate.py` and the `docs/DEMO.md` instructions truly isolate the
    L1 SQLite store (previously the variable was set but ignored and L1 always
    wrote to `./data/velantrim_memory.db`).
  - `reconcile._sync_l3()` now mirrors the pipeline's self-heal path: on an L3
    merge failure the fact is queued in the L3 outbox for `drain_l3_outbox()`
    instead of silently losing the sync.
  - `core/consolidate.py` no longer calls `merge_fact(None)` when an L1 record
    was erased while its L3 node lingers (defensive `_remerge` guard).
  - `PRIVACY.md` now describes the real default L3 backend chain
    (`auto` → LadybugDB → **on-disk SQLite** → in-memory mock) instead of
    claiming the in-memory mock is the default.
  - TruthGate invariant wording made precise across README / ARCHITECTURE /
    implementation-status: TruthGate is the only **automatic** entry into L3;
    the sole exception is the explicit, audited curator override in the review
    queue (`core/review.py`).
  - Documentation figures re-synced to the verified suite (**717 passing tests,
    12 skipped optional-backend tests, 100% coverage**) and the coverage gate
    unified at **100%** across `pyproject.toml`, CI and contributor docs
    (previously CI enforced 95% while `pyproject.toml` required 100%).

### Added
- **FastAPI service layer** (`core/api.py`, optional `pip install '.[api]'`,
  console script `velantrim-api`): HTTP endpoints `/health`, `/ingest`, `/ask`,
  `/receipt`, `/verify-receipt`, `/evidence/{fact_id}` — thin async wrappers over
  `core/aio.py` that mirror the CLI and add no TruthGate-bypassing write path.
  FastAPI/uvicorn stay an optional extra; the default runtime is standard-library
  only.
- **RFC0063 — External knowledge ingestion** (`core/knowledge.py`): bulk-import
  `.txt` / `.md` / `.json` / `.jsonl` / `.csv` knowledge files through the same
  Guardian → TruthGate path as user utterances; imported facts carry
  `source_status = EXTERNAL` with the source file as provenance. CLI `learn`.
- **RFC0068 — NeuroCore Phase 0** (`core/neurocore.py`): a passive plasticity
  tracker that logs the norm of the would-be weight delta (ΔW) when surprise > θ.
  Now wired into `pipeline.run()` — when enabled (`VELANTRIM_NEUROCORE`) every
  query records a surprise tick (surprise ≈ 1 − top retrieval relevance, incl.
  zero-hit cold-start queries). Off by default; never touches the model and never
  writes the L3 graph (invariant I68). CLI `neurocore-report`.
- **Sprint-A A9 — LLM call safety** (`core/generation.py`): bounded retry with
  exponential backoff on transient API failures, no retry for non-transient
  errors, output ceiling, graceful degradation to the extractive generator.
- **Evaluation quality gate** (`scripts/eval_gate.py`, `velantrim eval --gate`,
  grant WP3 baseline): the harness now runs over a curated, multi-domain fixture
  corpus bundled with the package (`core/_eval_fixtures/` — 16 retrieval cases
  with ranking distractors, 12 labelled contradiction pairs incl. hard
  negatives), emits per-case `metrics.jsonl` + `eval_report.md`, and is enforced
  by a dedicated `eval-gate` CI job with regression thresholds so retrieval /
  grounding / contradiction quality cannot silently drop. `velantrim eval` gains
  `--detail`, `--md` and `--gate`.
- **Hands-on demo walkthrough** (`docs/DEMO.md`, grant WP5 baseline): a
  reproducible CLI tour with real captured output — ingest → ask → provenance
  receipt + replay → contradiction detection → knowledge import + source-span
  evidence → GDPR erase + tamper-evident audit → NeuroCore telemetry → eval
  harness → optional HTTP. Linked from the README and the NLnet scope.
- Community & governance docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `GOVERNANCE.md`, this `CHANGELOG.md`, `.github/FUNDING.yml`, and
  `docs/SPRINT_A_STATUS.md` (honest A1–A10 triage).
- README: a "Data sovereignty & offline autonomy" section (local-only storage,
  accurate answers without an LLM / offline, durable interconnections, EU data
  sovereignty).

### Changed
- README headline version aligned to the published package version (`0.1.0`).
- Audit cleanup (#73): `BackendRegistry.reset()` now closes a cached L3 instance
  exposing `close()` (no SQLite connection leak across resets); `get_l3_graph`
  `auto` docstring corrected; `concept.hebbian_weights()` folds directed edge
  counts robustly; assorted LOW smells (`verify-receipt` file handle, decimal
  handling in `contradiction._content`).
- Documentation figures synced to the suite as it stood at the time (**633
  tests, ~99% coverage**) across README, ROADMAP, GDPR, and TEST_REPORT —
  superseded by the 717 / 100% re-sync recorded under *Fixed* above.

### Removed
- Dead research scaffolding: velum's unused observation window
  (`VELANTRIM_VELUM_WINDOW` env knob — recorded but never read by co-occurrence
  counting) and the decorative, unenforced `_Tool.capability` field on the
  read-only MCP server.

## [0.1.0] — first public release

Initial public release of the verifiable, local-first memory core:

- **Foundation:** L0/L1 memory layers, the 8-state Epistemic State Machine, the
  swappable L3 canonical graph (`auto`→LadybugDB / on-disk SQLite / mock / Neo4j),
  vector + graph retrieval, swappable embedder and answerer, utterance ingestion,
  and `pip`-installable packaging with the `velantrim` CLI.
- **Trust & truth:** Guardian + TruthGate, provenance trace, replayable answer
  receipts, contradiction detection, FSRS-style consolidation, and the Immune /
  CRISPR memory guard (RFC0072).
- **Privacy & GDPR:** Art. 17 erasure (+ cascade & tombstones), Art. 18
  restriction, Art. 30 record-of-processing, Art. 32 encryption at rest, a
  tamper-evident audit log, and PII redaction.
- **Living memory (biologically-inspired):** Fractal Memory (RFC0070), Epigenetic
  Adaptation (RFC0071), Neurogenesis (RFC0073), Concept Emergence (RFC0066),
  Memory Volition (RFC0065), Velum L1.5 (RFC0016), and the Analogy Graph +
  Semantic Bridges + CREATIVE mode (RFC0067 v2.0).
- **Ops & integration:** pluggable Redis/SQLite re-merge queue, async entry
  points, a dependency-free read-only MCP server, observability, and the CLI.

[Unreleased]: https://github.com/velantrian/velantrim-exocortex-crystal/compare/v0.3.0-reviewer-preview...HEAD
[0.3.0]: https://github.com/velantrian/velantrim-exocortex-crystal/compare/v0.2.0...v0.3.0-reviewer-preview
[0.2.0]: https://github.com/velantrian/velantrim-exocortex-crystal/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/velantrian/velantrim-exocortex-crystal/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/velantrian/velantrim-exocortex-crystal/releases/tag/v0.1.0
