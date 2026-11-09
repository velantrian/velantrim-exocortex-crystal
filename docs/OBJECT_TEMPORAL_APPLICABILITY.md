# Explicit object/time applicability on Crystal's read-only query path

## Versions and scope

- Laboratory: `velantrian/Velantrim-Exo-Cortex-Crystal-Test`, PR #13,
  `fbd99947bb2550db2768f8fd154cafdd3d561488`, 2026-11-08 23:20:01 CET
  (Europe/Berlin), `Fix time precision, metadata persistence, recorded_at, and linked_objects`.
- Main Crystal base: branch `main`, `33228409a45835c47c972009e088c466c6095b60`,
  2026-10-28 22:27:21 CET (Europe/Berlin),
  `fix: reject receipt replay after sealed evidence changes (#500)`.
- This is an isolated-data implementation, not merged or deployed. No model API calls, live
  user queries, runtime deployment, merges, Titan changes or EPIS-001 changes.

A successful laboratory PR does not establish correctness of main Crystal.
The main query, persistence and trust-boundary checks below are the separate check.
This establishes specific grounding-handling guarantees, not broader model
understanding, semantic truth, or general model reliability.

## Actual wiring (not just the laboratory's pipeline.run)

Public HTTP `/ask` and `/receipt` in `core/api.py` use `core.aio.arun`, which calls
`core.query_pipeline.query`. CLI `ask` and `receipt` in `core/cli.py` call that
same read-only `query` directly. MCP's reader search does not generate an answer
and is unchanged.

`query` validates explicit applicability parameters, then follows the existing:

1. `_retrieve_read_only` (pinned-space retrieval or bounded legacy fallback);
2. `_resolve_retrieval_hits` / `_resolve_canonical_fact`, resolving actual L3 and
   deny-dominant L1 state via `TrustSnapshot`, not trusting retrieval wrappers;
3. existing replayable-evidence requirement for VERIFIED facts;
4. existing Guardian structural check;
5. `core.pipeline.generate_answer`: existing strict `project_canonical`, **then**
   the new pure `core.applicability.select`, **then** the existing generator.

No applicability field promotes a verdict, bypasses a restriction, supplies a
missing evidence span, transitions ESM, or changes historical truth. Disputed
L1/L3 applicability declarations are omitted on read, so a requested object/time
check fails closed. Successful answer traces remain pruned to admitted grounds.
Excluded historical evidence and relation context are separate from answer facts
and from the attested `answer` text (see "Attested answer boundary").

`core.pipeline.run` is a separate legacy write/promote pipeline. Its explicit
parameter forwarding and `build_facts_pack` save/reload compatibility are also
covered; it is **not** substituted for the production read-only entry point.
Invalid current-state parameters are rejected before this legacy path writes.

## Explicit contract

Python: `query(text, asked_object="L", as_of="2026-11-08T10:00:00+01:00",
temporal_scope="current")`; equivalent keywords on `aio.arun` and legacy `run`.
HTTP `/ask` accepts the three fields; `/receipt` accepts query parameters.
CLI `ask` / `receipt` accept `--asked-object`, `--as-of`, `--temporal-scope`.

No object, date, current intent or timezone is inferred from free text or the
server clock. Without `asked_object`, the object sieve is off. Time filtering is
off only when `temporal_scope` is omitted (`None`). The only accepted explicit
scope is `"current"` (surrounding whitespace is stripped and case is normalized:
`"CURRENT"`, `"Current"`, and `" current "` behave identically). Unknown, misspelled,
blank, or non-string scopes fail closed with an explanation; they never disable
time filtering. A current-state request without a valid explicit `as_of` returns
an explanation, including when memory is empty.

- A present `primary_object` is decisive, including empty/malformed values;
  wrapper `object` cannot override it. Missing identity is a reported gap.
- `linked_objects` preserves context but never transfers status.
- `status_applies_to` is an explicit writer-declared status-transfer target,
  usable only with an established primary identity and already-admitted facts.
- `observed_at`, then the legacy probe `date`, supplies observation time.
  `recorded_at`, `created_at` and `updated_at` never supply observation time.
- Datetimes preserve clock precision and offsets; aware instants compare in UTC;
  naive and aware timestamps do not silently mix.
- A date-only observation matches a date-only query for that date, at day
  granularity only. It does not establish a state at any particular instant.
  An instantaneous observation does not establish the whole queried day.
- Inclusive date-only `valid_from` / `valid_until` mean beginning / end of the
  calendar day. A timestamped interval must cover the entire date-only query.
  Where a date bound needs a timezone, use the explicit query offset, otherwise
  the first timestamped interval bound; never the machine timezone.
- No universal expiry period. Old evidence stays historical, not false. Dated
  historical context can be returned without using it as current grounding.
- Valid current grounds are retained even when other retrieved records are
  excluded. Exclusions do not cancel an admitted answer or claim that its
  supported current state is unknown.

## Attested answer boundary

`result["answer"]` is only the generator output over the admitted current
grounds (`result["facts"]`), or `None` on refusal. Exclusion reasons and
historical claims are returned only in the separately labelled
`result["uncertainty"]` and `result["applicability"]` (`exclusions`,
`historical_facts`, `context_relations`); they are not appended to `answer`.
`provenance.build_receipt` seals `result["answer"]` against citations built from
`result["facts"]` only, so a receipt never attests uncited historical text, and
historical facts are not added as citations (they did not ground the answer).

- Current fact next to an old fact: `answer` and `receipt["answer"]` equal the
  current claim; citations/trace/facts are the current fact; the old claim is in
  `applicability["historical_facts"]` and `uncertainty` only.
- Only old information: `answer` is `None`; `build_receipt` raises, HTTP
  `/receipt` returns 422 and CLI `receipt` exits 1, so no current-status receipt
  exists. Historical claims remain in the separate fields.
- Only current information: the receipt attests the current claim; there are no
  `uncertainty`/`applicability` fields.

HTTP `/ask` returns those fields beside `answer` (unchanged JSON shape). CLI
`ask` prints the answer, then a separate `[uncertainty, not attested] ...` line.
HTTP `/receipt` and CLI `receipt` emit only `build_receipt` output. Covered by
`tests/test_applicability_receipt_boundary.py` (real SQLite, real retrieval,
`build_receipt` + `verify_receipt`, HTTP and CLI).

## Persistence, owner and source

The durable namespace is **`metadata["applicability"]`**. Writers/importers supply
these declarations explicitly, for example through existing
`ingest(..., metadata={"applicability": {...}})`; store object/time values as ISO
strings. No new HTTP-ingest authority or provenance privilege is added.

Main and lab `store_fact` retain SQLite columns plus metadata, not arbitrary
extra top-level fields. Main's `preserve_metadata=True` additionally retains the
existing stored namespace on recall. `build_facts_pack` now embeds declarations
**before** saving, then lifts the actual persisted declarations back into its
read view. `_l3_payload` already reads the persistent record and overlays the
existing truth verdict, so the namespace reaches L3 without a schema change.
The read-only path restores declarations from persisted records, not retrieval
labels. Existing records need explicit writer/curator enrichment before they can
answer new object-specific/current queries; missing fields do not imply a match.

These are **writer-declared applicability metadata**, not independently audited
proof of a relation or time. The existing provenance/evidence gates still own
admission. An arbitrary `truth_status` label inside applicability metadata cannot
turn a user report into VERIFIED. Semantic validation of writer attribution and
status-transfer suitability remains a limitation, not a claimed new capability.

Real SQLite tests exercise ingest/build -> save -> clear L0 -> close/reopen L3 ->
actual retrieval -> answer. They verify object, observation/write/validity times,
linked context and explicit transfer targets. Full L1/L3 SQL dumps before/after
public queries are equal. These tests do not replace retrieve with a stub.
A separate adversarial wrapper test does use a stub, specifically to prove that
retrieval labels cannot override persisted declarations.

## Laboratory audit mapping (lab not rerun or patched)

| Audit point | Lab fbd9994 implementation/test; main check |
|---|---|
| Later observation cannot prove earlier state | full-precision `_parse_temporal_instant`, `_fact_covers_as_of`; `test_observation_at_2300_does_not_cover_0900_same_day`; real-query counterexample |
| Expired interval cannot prove later state | interval coverage; `test_interval_ending_at_0100_does_not_cover_2300_same_day`; real-query counterexample |
| Invalid date must fail | parser; `test_invalid_as_of_oops_is_rejected`; missing/invalid current request tests |
| Today's write is not observation | `_fact_observation` excludes storage timestamps; `test_today_write_about_october_event_is_not_current_evidence`, recorded-at-only and real-query cases |
| Object link is not status transfer | `_explicitly_transfers_status_to`; linked-object negative and explicit-transfer positive tests, including real SQLite reload |
| Save/read retains applicability | metadata namespace before save; laboratory store/cache-clear test; main build/admit/close/reopen/retrieve/answer test |

Prior laboratory results were supplied as 214 passed before Astra corrections
and 225 passed after fbd9994 (15 object + 27 temporal + 183 pipeline). They were
**not rerun here**. PR #13's description still describes the earlier behavior and
214 tests; it was deliberately not edited.

**Additional discovered laboratory gap:** fbd9994 returns False for a date-only
interval `2026-11-08` through `2026-11-08` queried at
`2026-11-08T23:00:00+01:00`: its upper-bound comparison uses midnight. This was
confirmed by a single pure-helper probe, not a lab suite rerun. Main implements
the documented inclusive end-of-day rule and adds new boundary tests, including
a timestamped start with a date-only end. Crystal-Test is left unchanged.

## Actual before -> after

`object_temporal_before_after.json` records the same offline probe against a
`git archive` of main base 3322840 and this implementation. These are direct
`generate_answer` probes, not claims that base's public API already accepted the
new keywords. Probe: `python tests/applicability_before_after_probe.py TARGET_TREE`.

| Case | Base result | Proposed result |
|---|---|---|
| Observation at 23:00, asked at 10:00 same day | `L ready` | no answer; observation later than as_of |
| Interval ended at 01:00, asked at 10:00 | `L ready` | no answer; validity expired |
| `as_of=2026-11-08oops` | `L ready` | valid explicit as_of required |
| October observation, November write | `L ready` | no current answer; October date/claim retained as historical only |
| recorded_at only | `L ready` | observation time not established |
| L2 linked to L, no status-transfer declaration | `L ready` | no answer; primary object differs; link remains context |
| No declared object belonging | `L ready` | no answer; belonging not established |
| current scope, no as_of | `L ready` | valid explicit as_of required |
| Matching fresh evidence | `L ready` | `L ready` (preserved) |
| build/save -> clear cache -> SQLite reread | metadata `{}` | full applicability namespace survives |

Separate real-query tests verify the entire proposed persistence-to-answer path,
not merely those direct before/after probes.

## Actual scenario outcomes

Exact questions, admitted claims, exclusions and final outputs are in
`object_temporal_scenarios.json`, reproducible with
`python -m tests.applicability_packet`. All timestamps below are Europe/Berlin;
the JSON retains the original explicit seasonal offsets.

Frozen AC inputs are byte-identical copies from
`/workspace/terin-pattern-test/results/ac_always_current_prep_v1/evidence/AC*.json`.
The test harness supplies manual source/object/time attribution (including
R-14/L2 summary lineage), marks unsupported assistant assertions USER_CLAIMED,
and renders the given object's identifier as a claim heading for offline lexical
retrieval. This is not automatic source interpretation or an authority model.
A test-local k=20/min_similarity=0 configuration avoids conflating applicability
with small-fixture retrieval quality; actual retrieval and SQLite are used.

| Case / question | Admitted grounds | Exclusions | Final answer (summary) |
|---|---|---|---|
| AC03: Какой статус сообщить для R-41? (as_of 2026-11-06 13:45 CET) | fresh independent R-41 report, AC03-2 | R-14 document and derivative summary wrong object; old card not covering as_of | R-41: Проверка ожидается; exclusions/historical date in separate `uncertainty`/`applicability` fields |
| AC06: В каком формате ответить на M? (as_of 2026-11-08 09:30 CET) | owner's new M-scoped paragraph request, AC06-1 | old table request historical; assistant suggestion USER_CLAIMED/noncanonical | paragraph, only for M; historical request not current |
| AC07: Каков статус L сегодня? (as_of 2026-11-08 10:00 CET) | none current; Oct 8 card historical only | L2 import and derivative summary wrong primary object; L card historical | current status not established; date of old L state preserved |
| AC08: Можно ли по этим материалам напомнить согласованный способ упаковки? | journal says no recorded decision and journal incomplete, AC08-0 | unsupported assistant assertion USER_CLAIMED/noncanonical | only the scoped journal statement; no reconstructed method and no claim that no decision occurred |
| Fresh L evidence / current L status? | matching L observation at 10:00 CET | none | Laboratory component ready |
| Only foreign document / current L status? | none | primary L2 differs | no answer; current status not established |
| Only old record / current L status? | no current grounds; dated October record as context | historical observation | no current answer; dated historical claim |
| Later observation / current L status at 10:00? | none | 23:00 observation is later | no earlier-state confirmation |
| L uses L2 / current L status? | relation context only | no explicit suitable status transfer | link retained; status not transferred |
| Incomplete journal / agreed packaging method? | same scoped journal evidence as AC08 | unsupported assistant assertion | cannot recover a method from these materials; does not assert absence of a decision |

Historical results are not regraded: E-pilot stays 10/12 vs 10/12; AC stays 5/8
vs 6/8; historical AC08 stays GROUNDED_KEEP / partial / strict_success false.
No extra out-of-journal question is silently made a success criterion here.
Raw JSONL, historical labels, rubric and Titan were not edited.

## Tests

Interpreter: isolated `/workspace/crystal-applicability-venv/bin/python`, Python
3.13, with optional FastAPI/httpx dependencies installed in that venv only.
Existing fixtures pin hashing embedding, extractive generation, local SQLite
queues and per-test data; new persistence tests also use real SQLite L3.

Exact existing regression selection (run against both base and proposed code):

```sh
python -m pytest tests/test_pipeline.py tests/test_query_pipeline.py \
 tests/test_provenance.py tests/test_api.py tests/test_cli.py tests/test_memory.py \
 tests/test_ingest.py tests/test_canonical_view.py tests/test_trust_snapshot.py \
 tests/test_read_only_query_surfaces.py tests/test_evidence.py \
 tests/test_evidence_current_standing_463.py tests/test_receipt_evidence_drift.py \
 tests/test_provenance_chain.py tests/test_l3_sqlite.py -o addopts= -q
```

Base: **598 passed, 3 warnings**. Proposed combined selection: the same command
plus `tests/test_applicability_live_path.py`,
`tests/test_generate_answer_asked_object.py`, and
`tests/test_generate_answer_temporal_applicability.py` -> **682 passed, 3 warnings**.
The added files contain 84 passing tests (42 adapted lab + 42 live/boundary cases).
Warnings: one optional HTTP-client deprecation and two expected synthetic
curator-force-override warnings. No failures or skips in that final selection.
Those were the initial focused checks; the follow-up full-suite coverage and CI
results below supersede the initial limitation about not running the full suite.

## Known limits

Explicit caller parameters and writer declarations are necessary. No NLP,
semantic authority resolution, automatic journal-completeness reasoning, TTL,
backfill or production migration is supplied. AC08 preserves explicitly supplied
scope/caveats rather than deriving a missing decision from natural language.
Retrieval recall limits still exist; these filters cannot recover absent facts.
Evidence-span and applicability semantics are not independently audited by this
change. Non-extractive generators were not exercised. Only the selected offline
SQLite/hash/extractive path is verified, not all remote backends or deployment.


## Follow-up: fail-closed scope validation and CI coverage

`temporal_scope` now accepts only omitted/None or explicit `"current"` after
stripping surrounding whitespace and casefolding. `"CURRENT"`, `"Current"` and
`" current "` enforce the same current-time filter. `"curent"`, unknown names, empty strings and
non-string values return `invalid_applicability_request` through the public
read-only query path, before retrieval. The direct rendering and compatibility
helper boundaries also fail closed. Omitted scope preserves existing unscoped
behavior; valid current scope still requires an explicit valid `as_of`.

Public regression:
`test_public_query_rejects_temporal_scope_typo_without_disabling_time_filter`.
It uses real isolated stored historical evidence, asserts a refusal rather than
an unfiltered answer, verifies the explanation, and compares complete before/after
SQLite dumps. Other meaningful tests cover native date/datetime inputs,
normalization, invalid requested objects, empty interval bounds with probe-date
fallback, before/equal/after dates, future/expired/invalid bounds, mixed timezone
awareness, whole-day precision and same-day historical-context limits.

The five Ruff findings were F401 unused imports in `core/pipeline.py`:
`_declared_primary_object`, `_facts_applicable_to_asked_object`,
`_facts_covering_as_of`, `_fact_covers_as_of`, `_parse_temporal_instant`.
They were removed; helper-focused tests import their actual owner,
`core.applicability`. No lint rule or coverage threshold was relaxed.
Interval admission and exclusion diagnostics now share one predicate, removing
an unreachable generic fallback instead of adding a fake assertion for it.
The focused branch-coverage command is:

```sh
python -m pytest tests/test_applicability_validation_coverage.py \
 tests/test_applicability_live_path.py tests/test_generate_answer_asked_object.py \
 tests/test_generate_answer_temporal_applicability.py -o addopts= \
 --cov=core.applicability --cov-branch --cov-report=term-missing \
 --cov-fail-under=100 -q
```

Focused result: **138 passed**, applicability **228 statements, 132 branches,
zero missing statements or partial branches, 100.00% coverage**, against the
unchanged 100% threshold. The full repository command is `python -m pytest tests/`
with the unchanged pyproject default `--cov=. --cov-fail-under=100`; final global
results are reported in the PR and its CI checks.
A deterministic same-content atomic-file-replacement regression also pins the
existing storage snapshot identity guard independently of filesystem timestamp
resolution. Local subprocess tests require the existing venv's bin directory on
PATH so their `python` executable resolves correctly.

The change checks compliance with explicitly declared object, time and
status-transfer fields; the semantic correctness of those declarations is not
separately proven. This limitation remains applicable to all follow-up tests.
