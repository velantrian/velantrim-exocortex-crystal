# 🗺️ Crystal Component Map for Agents

Use this map to choose the smallest relevant inspection surface. Paths are starting points,
not substitutes for consumer and test discovery.

## 1. Claims, epistemic lifecycle and physical L3

**Start:** `core/memory.py`, `core/l3_graph.py`, `core/truth_gate.py`,
`docs/CLAIM_METADATA_GLOSSARY.md`.

**Boundary:** storage presence does not equal strict Canon membership. Writes must preserve
state, evidence, restrictions and the canonical admission path.

## 2. Durable backend identity

**Start:** `core/backend_profiles.py`, `core/_registry.py`, `core/l3_graph.py`,
`core/doctor.py`, `docs/architecture/DURABLE_STORAGE_PROFILE.md`.

The versioned profile locks ordinary deployment identity. Backend availability, package
installation, locator changes or profile deletion are not migration and cannot silently
select another store.

## 3. SQLite lifecycle and logical portability

**Start:** `core/storage_common.py`, `core/storage_backup.py`,
`core/storage_restore.py`, `core/storage_lock.py`, `core/storage_migration.py`,
`core/storage_ops.py`.

Implemented:

```text
SQLite backup → verify → inactive restore
SQLite profile → bounded canonical bundle → independent verification
```

Resource and TOCTOU checks remain fail closed. Migration evidence does not grant epistemic
authority.

## 4. PostgreSQL inactive migration target

**Start:**

- `core/postgresql_migration.py`
- `core/postgresql_migration_impl.py`
- `core/storage_ops.py`
- `docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md`
- `docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md`
- `tests/test_postgresql_migration_*.py`
- `.github/workflows/postgresql-integration.yml`

Current verified path:

```text
verified logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive schema
→ serializable import
→ independent read-only exact-state equivalence
→ non-secret receipts
```

**Decision owner:** operator migration commands preserve physical state. Guardian, TruthGate
and strict read reconciliation retain epistemic authority.

**Critical boundary:** the target remains `active=false`, is absent from ordinary runtime
composition and cannot serve normal reads or writes. No cutover, rollback, dual-write,
automatic switching or ANN acceptance is implemented.

## 5. Truth admission and safety

**Start:** Guardian functions in `core/pipeline.py`, `core/truth_gate.py`, `core/immune.py`,
`core/api_ingest_policy.py`, `docs/IMMUNE_LAYER.md`, `docs/ARCHITECTURE.md`.

A caller, model, retriever, storage profile, migration tool or Reader artifact must not mutate
strict Canon outside the audited admission path. Guardian is an architectural/runtime boundary
implemented inside the current pipeline rather than a standalone `core/guardian.py` module.

## 6. Strict read grounding

**Start:** `core/canonical_view.py`, TrustSnapshot tests, public handlers in
`core/api.py`, `core/cli.py` and MCP surfaces.

Public query/search paths are read-only. Restrictions remain deny-dominant and physical L3
must not be presented as strict Canon.

## 7. Retrieval, evidence and receipts

**Start:** `core/evidence.py`, `core/span_extract.py`, retrieval modules under `core/`,
FactsPack, TRACE, Receipt, `docs/EVAL.md`, `TEST_REPORT.md`.

Retrieval rank, similarity and model output are not evidence or admission. Every grounded
claim must retain source/provenance and refusal conditions.

**RC-4 boundary:** `core/reader_extraction.py` creates only pre-admission
`EXTRACTED_PROPOSITION` Reader candidates. It must not call `core.evidence.attach_evidence()` or
write fact evidence. A source locator is provenance, not evidence sufficiency.

**RC-5 boundary:** `core/reader_relations.py` registers only explicit relations between valid
RC-4 candidates inside one OPEN Reader session and exact source version. Exact candidate IDs,
primary/supporting provenance and rationale remain audit context, not evidence admission.

**RC-6 boundary:** `core/reader_long_context.py` groups current valid RC-4 leaves into deterministic
bounded working sets and may register caller-supplied `SUMMARY` artifacts with direct leaf provenance.
Working-set fill and summary text are not evidence, truth or Canon admission.

## 8. Contradictions and curator decisions

**Start:** contradiction modules, `core/review.py`, `core/conflict_surfaces.py`,
`docs/CONTRADICTION_POLICY.md`.

Detection does not select a winner. `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` require
explicit authorized decisions. Curator leases remain process-local. RC-3 `CROSS_CHECK`, RC-4
proposition extraction, RC-5 relation candidates and RC-6 working sets/summaries may expose
conflict-relevant Reader state, but they cannot resolve a `ContradictionReport` or select a
canonical winner.

```text
POSSIBLE_CONTRADICTION != confirmed contradiction
relation candidate     != admitted evidence
summary                != evidence
```

## 9. Imports and review queues

**Start:** import/session modules, review queue/session modules and their CLI/HTTP tests.

Partial imports must remain distinguishable from admission. Unreviewed content cannot ground
strict answers, and restriction/erasure state must propagate. RC-4 extracted propositions,
RC-5 relation candidates and RC-6 working-set/summary artifacts remain upstream of this normal
ingest/review/evidence path.

## 10. Public surfaces and runtime composition

**Start:** `core/api.py`, `core/cli.py`, `core/doctor.py`, MCP modules, `Dockerfile`,
`pyproject.toml`, `.github/workflows/ci.yml`.

Public query and doctor surfaces are read-only. PostgreSQL migration commands are explicit
operator operations and do not add an ordinary runtime adapter. Reader RC-1 through RC-6 add no
public API, CLI, background worker or ordinary runtime-composition wiring.

## 11. Evaluation and status evidence

**Start:** `docs/EVAL.md`, `TEST_REPORT.md`,
`docs/status/implementation-manifest.json`, evaluation fixtures, Ring Zero and benchmark
workflows.

Always bind claims to an exact commit, head and CI run. Microbenchmarks and integration jobs
are not production SLOs or certification. Reader telemetry is counts/resource references only;
coverage, pass completion, extraction counts, relation counts, working-set fill and summary counts
are not comprehension, truth, confidence or evidence-sufficiency scores.

## 12. Long-document semantic reading

**Start:**

- `core/reader_core.py`, `tests/test_reader_core.py` — RC-1;
- `core/reader_structure.py`, `tests/test_reader_structure.py` — RC-2;
- `core/reader_passes.py`, `tests/test_reader_passes.py` — RC-3;
- `core/reader_extraction.py`, `tests/test_reader_extraction.py` — RC-4;
- `core/reader_relations.py`, `tests/test_reader_relations.py` — RC-5;
- `core/reader_long_context.py`, `tests/test_reader_long_context.py` — RC-6;
- `docs/architecture/READER_CORE_ARCHITECTURE.md` — normative RC-0 contract;
- `core/evidence.py`, `core/span_extract.py`, `docs/CONTRADICTION_POLICY.md` — downstream boundaries/context.

Machine status intentionally separates the bounded layers from the absent full capability:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
dedicated_reader_core = false
```

### RC-1 ownership

RC-1 owns immutable source identity/version binding, replayable locators, `ReaderSession`,
`SegmentCard`, source-fidelity classes, explicit coverage states, bookmarks/open loops,
fail-visible interruption/degradation, conservative stale invalidation and privacy metadata
inheritance. It retains no source body.

### RC-2 ownership

RC-2 owns a caller-supplied, exact-version Structural Document Map: hierarchy/order, structural
kinds, exact-span containment and explicit `RECOVERED` / `AMBIGUOUS` / `UNSUPPORTED` state. It is
not an automatic parser and structural prominence is not epistemic authority.

### RC-3 ownership

RC-3 owns deterministic explicit pass mechanics over one OPEN RC-1 session and one exact-version
RC-2 map. It supports `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK` and
`TARGETED_REREAD`, one active pass at a time, declared targets, explicit region coverage outcomes,
`ATTEMPTED` / `COMPLETED` / `INTERRUPTED` / `DEGRADED` state and partial-progress preservation.
It does not call a model/provider, infer hidden targets or prove comprehension.

### RC-4 ownership

RC-4 validates/registers a caller-supplied normalized proposition as a source-linked Reader
candidate only when it is anchored to a `COMPLETED` RC-3 pass target with both recorded and current
matching substantive coverage (`PROCESSED` or `REVISITED`). It preserves primary/supporting
replayable locators, source owner, source-presentation category, explicit negation and qualifiers.
Every candidate has `EXTRACTED_PROPOSITION` fidelity.

**Critical authority boundary:** RC-4 has no `core.evidence` import and no fact evidence writer. It
does not attach evidence, set evidence sufficiency, mutate truth/ESM/Canon, bypass Guardian/TruthGate,
resolve contradictions or gain planner/belief-update authority.

### RC-5 ownership

RC-5 owns deterministic explicit relation registration over candidate IDs already registered by
one RC-4 `ReaderPropositionExtractor`. `ReaderRelationRegistry` is bounded to one OPEN
`ReaderSession` and one exact `SourceVersion` and re-validates candidate session/source/provenance
membership fail closed.

The intentionally small relation set is:

- `POSSIBLE_CONTRADICTION` — symmetric suspicion only;
- `TENSION` — symmetric tension without claiming contradiction;
- `EXCEPTION` — directional, right candidate limits the left;
- `QUALIFICATION` — directional, right candidate refines the left.

Every relation preserves both exact candidate IDs, pass/node IDs, primary/supporting locators and
an explicit non-empty rationale. Symmetric relations canonicalize candidate-ID pair order; duplicate
same-kind symmetric pairs fail closed rather than becoming corroboration. Directional relations
preserve direction.

RC-5 has no truth/confidence/evidence-sufficiency/resolved/winner fields. It does not call
`core.evidence.attach_evidence()`, write fact evidence, invoke contradiction resolution, mutate
truth/ESM/Canon, bypass Guardian/TruthGate or gain planner/belief-update authority.

### RC-6 ownership

RC-6 owns bounded long-context orchestration over the **current registered RC-4 leaf candidates** of
one existing extractor. `ReaderLongContextStrategy` requires one OPEN ReaderSession and exact
SourceVersion, revalidates pass/structure/coverage/provenance, then orders candidates by RC-2
structural order with a stable candidate-ID tie-break.

Working-set resources are explicit Reader-artifact budgets:

```text
1 <= max_candidates_per_set <= 128
1 <= max_source_locators_per_set <= 512
```

They are not model-token/context-window guarantees. Candidate atomicity keeps each RC-4 candidate
with all of its direct unique replayable locators; a candidate that cannot fit the declared locator
budget fails closed.

A matching RC-5 registry is optional. Existing relation IDs are carried only when both endpoints are
already in the same working set; cross-set relation IDs are not copied and no relation is inferred.

`register_summary()` accepts caller-supplied text only and always produces a
`SourceFidelity.SUMMARY` artifact. Before registration it compares current direct leaf provenance to
the immutable working-set snapshot and revalidates those RC-4 leaves. The summary keeps direct
candidate IDs and replayable source locators; another summary cannot be its only provenance path.

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

RC-6 has no truth/confidence/evidence-sufficiency/resolution/winner fields, no evidence admission,
no automatic summarization/model/provider/parser/OCR/embedding/ANN dependency, no RC-7 cross-document
identity/reasoning, no Reader persistence/API/CLI/worker and no PostgreSQL activation.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
similarity != identity
repetition != corroboration
```

**Current non-features:** no automatic parser/semantic chunker/OCR/PDF-layout/multimodal engine,
no automatic NLP/LLM/provider Reader extraction or summarization, no embeddings/ANN/vector DB, no
automatic semantic equivalence or RC-7 cross-document proposition identity/reasoning, no durable
Reader schema/migration and no dedicated/full autonomous Reader runtime.

## 13. Documentation, grant and research governance

**Start:** `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`,
`docs/IMPLEMENTATION_STATUS.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`.

GitHub `main` proves implementation. Notion preserves deeper rationale, grant framing and
audit history. Issues #331 and #332 are merged baseline; exact-vs-ANN evaluation,
cutover/fencing, rollback and PostgreSQL server lifecycle remain separate future phases.
Automatic SQLite/PostgreSQL switching remains forbidden. Reader RC-0 through RC-5 are existing
pre-agreement baseline. RC-6 is the current separately authorized milestone; if it merges before a
grant agreement it also becomes existing baseline. RC-7 is not started and requires a separate
bounded authorization after RC-6 completion evidence.
