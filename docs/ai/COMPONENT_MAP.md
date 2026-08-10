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

## 8. Contradictions and curator decisions

**Start:** contradiction modules, `core/review.py`, `core/conflict_surfaces.py`,
`docs/CONTRADICTION_POLICY.md`.

Detection does not select a winner. `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` require
explicit authorized decisions. Curator leases remain process-local.

## 9. Imports and review queues

**Start:** import/session modules, review queue/session modules and their CLI/HTTP tests.

Partial imports must remain distinguishable from admission. Unreviewed content cannot ground
strict answers, and restriction/erasure state must propagate.

## 10. Public surfaces and runtime composition

**Start:** `core/api.py`, `core/cli.py`, `core/doctor.py`, MCP modules, `Dockerfile`,
`pyproject.toml`, `.github/workflows/ci.yml`.

Public query and doctor surfaces are read-only. PostgreSQL migration commands are explicit
operator operations and do not add an ordinary runtime adapter. Reader RC-1 has no public API,
CLI, background worker or ordinary runtime composition wiring.

## 11. Evaluation and status evidence

**Start:** `docs/EVAL.md`, `TEST_REPORT.md`,
`docs/status/implementation-manifest.json`, evaluation fixtures, Ring Zero and benchmark
workflows.

Always bind claims to an exact commit, head and CI run. Microbenchmarks and integration jobs
are not production SLOs or certification.

## 12. Long-document semantic reading

**Start:** `core/reader_core.py`, `tests/test_reader_core.py`,
`docs/architecture/READER_CORE_ARCHITECTURE.md`, `core/evidence.py`, `core/span_extract.py`,
`docs/core/INGEST_SCHEMA.md`, `docs/CONTRADICTION_POLICY.md`.

RC-0 is the normative architecture contract. RC-1 adds a bounded, pure-standard-library
**minimal evidence-linked domain skeleton** and nothing resembling a full autonomous reader.
Machine status intentionally separates these facts:

```text
reader_core_rc1_skeleton = true
dedicated_reader_core    = false
```

The RC-1 surface owns only:

- immutable source identity/version binding (`document_id`, source URI, SHA-256);
- replayable exact half-open spans or explicit structural locators;
- `ReaderSession` lifecycle;
- `SegmentCard` plus five mandatory source-fidelity classes;
- `UNREAD` / `SEEN` / `PROCESSED` / `REVISITED` / `NEEDS_REVIEW` coverage semantics;
- count/gap telemetry that never reports a comprehension percentage;
- minimal source-linked bookmarks/open loops;
- fail-visible interruption/degradation and conservative whole-session stale invalidation;
- restriction/sensitivity inheritance without retaining source body text in `SourceVersion`.

**Critical authority boundary:** `core/reader_core.py` has no ingest/TruthGate/Canon/ESM,
contradiction-decision or planner write path. Producing a Reader artifact does not admit a
claim, resolve a contradiction, change truth status or prove comprehension. A future dedicated
Reader Core still requires separately reviewed structural/multi-pass/model/runtime work.

**RC-1 non-features:** no parser/semantic chunker, LLM/provider integration, embeddings, ANN or
vector DB, durable Reader schema/migration, public API/CLI, multi-pass orchestration,
cross-document reasoning engine, planner or automatic belief update.

## 13. Documentation, grant and research governance

**Start:** `AGENTS.md`, `docs/DOCUMENTATION_SYNC_PROTOCOL.md`, `docs/STATUS.md`,
`docs/IMPLEMENTATION_STATUS.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`.

GitHub `main` proves implementation. Notion preserves deeper rationale, grant framing and
audit history. Issues #331 and #332 are merged baseline; exact-vs-ANN evaluation,
cutover/fencing, rollback and PostgreSQL server lifecycle remain separate future phases.
Automatic SQLite/PostgreSQL switching remains forbidden. Reader RC-1 merged before a grant
agreement is existing baseline and cannot be presented as awarded/funded delivery.
