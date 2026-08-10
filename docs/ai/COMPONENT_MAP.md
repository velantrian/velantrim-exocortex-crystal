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

**Audit questions:**

- Is Psycopg still optional and lazy-loaded?
- Are versions, TLS, schema absence and target identity checked fail closed?
- Can connection details or raw database failures leak into receipts/logs?
- Is equivalence recomputed independently from canonical target rows?
- Is inactive import being confused with activation or full-system migration?

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

## 8. Contradictions and curator decisions

**Start:** contradiction modules, `core/review.py`, `core/conflict_surfaces.py`,
`docs/CONTRADICTION_POLICY.md`.

Detection does not select a winner. `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` require
explicit authorized decisions. Curator leases remain process-local. RC-3 `CROSS_CHECK` and RC-4
proposition extraction may expose conflict-relevant Reader state, but they cannot resolve a
`ContradictionReport` or select a canonical winner.

## 9. Imports and review queues

**Start:** import/session modules, review queue/session modules and their CLI/HTTP tests.

Partial imports must remain distinguishable from admission. Unreviewed content cannot ground
strict answers, and restriction/erasure state must propagate. RC-4 extracted propositions remain
upstream of this normal ingest/review/evidence path.

## 10. Public surfaces and runtime composition

**Start:** `core/api.py`, `core/cli.py`, `core/doctor.py`, MCP modules, `Dockerfile`,
`pyproject.toml`, `.github/workflows/ci.yml`.

Public query and doctor surfaces are read-only. PostgreSQL migration commands are explicit
operator operations and do not add an ordinary runtime adapter. Reader RC-1/RC-2/RC-3/RC-4 add
no public API, CLI, background worker or ordinary runtime-composition wiring.

## 11. Evaluation and status evidence

**Start:** `docs/EVAL.md`, `TEST_REPORT.md`,
`docs/status/implementation-manifest.json`, evaluation fixtures, Ring Zero and benchmark
workflows.

Always bind claims to an exact commit, head and CI run. Microbenchmarks and integration jobs
are not production SLOs or certification. Reader telemetry is count/state only; coverage, pass
completion and extraction counts are not comprehension, truth, confidence or evidence-sufficiency
scores.

## 12. Long-document semantic reading

**Start:**

- `core/reader_core.py`, `tests/test_reader_core.py` — RC-1;
- `core/reader_structure.py`, `tests/test_reader_structure.py` — RC-2;
- `core/reader_passes.py`, `tests/test_reader_passes.py` — RC-3;
- `core/reader_extraction.py`, `tests/test_reader_extraction.py` — RC-4;
- `docs/architecture/READER_CORE_ARCHITECTURE.md` — normative RC-0 contract;
- `core/evidence.py`, `core/span_extract.py`, `docs/CONTRADICTION_POLICY.md` — downstream boundaries/context.

Machine status intentionally separates the bounded layers from the absent full capability:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core = false
```

### RC-1 ownership

RC-1 owns immutable source identity/version binding, replayable locators, `ReaderSession`,
`SegmentCard`, five source-fidelity classes, explicit coverage states, bookmarks/open loops,
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

Source-presentation categories include factual assertion, author opinion, hypothesis, conditional,
example, quoted speech, reported position, definition and uncertain assertion. `FACTUAL_ASSERTION`
means only that the **source presents** a statement as factual; it is not a Crystal verification
status.

**Critical authority boundary:** RC-4 has no `core.evidence` import and no fact evidence writer. It
does not attach evidence, set evidence sufficiency, mutate truth/ESM/Canon, bypass Guardian/TruthGate,
resolve contradictions or gain planner/belief-update authority.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

**Current non-features:** no automatic parser/semantic chunker/OCR/PDF-layout/multimodal engine,
no automatic NLP/LLM/provider Reader extraction, no embeddings/ANN/vector DB, no automatic
cross-document proposition identity/reasoning, no durable Reader schema/migration and no dedicated/full
autonomous Reader runtime.

## 13. Documentation, grant and research governance

**Start:** `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`,
`docs/IMPLEMENTATION_STATUS.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`.

GitHub `main` proves implementation. Notion preserves deeper rationale, grant framing and
audit history. Issues #331 and #332 are merged baseline; exact-vs-ANN evaluation,
cutover/fencing, rollback and PostgreSQL server lifecycle remain separate future phases.
Automatic SQLite/PostgreSQL switching remains forbidden. Reader RC-0/RC-1/RC-2/RC-3 and RC-4, if
merged before a grant agreement, are existing baseline and cannot be presented as awarded/funded
delivery. The next Reader candidate after accepted RC-4 is separately authorized RC-5
exceptions/contradiction candidates; do not start it implicitly.
