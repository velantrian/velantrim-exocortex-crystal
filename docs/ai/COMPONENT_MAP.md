# 🗺️ Crystal Component Map for Agents

Use this map to choose the smallest relevant inspection surface. Paths are starting
points, not substitutes for consumer and test discovery.

## 1. Claim model, epistemic lifecycle and storage

**Purpose:** represent claims, states, restrictions and durable graph records.

**Start with:**

- `core/types.py`
- `core/memory.py`
- `core/storage.py`
- `docs/CLAIM_METADATA_GLOSSARY.md`
- machine-readable ESM specification referenced from `docs/STATUS.md`

**Authority boundary:** storage presence does not equal strict Canon membership.

**Audit questions:**

- Which state transition is being attempted?
- Is the source/evidence modality preserved?
- Does the write use the canonical admission path?
- Are erasure, restriction and import-session controls preserved?

## 1A. L3 backend selection and deployment diagnostics

**Purpose:** keep the environment-selected physical L3 backend and non-secret locator
stable across process restarts and expose read-only deployment health.

**Start with:**

- `core/backend_profiles.py`
- `core/_registry.py`
- L3 constructors/factory in `core/l3_graph.py`
- `core/doctor.py`
- `docs/architecture/DURABLE_STORAGE_PROFILE.md`
- `tests/test_backend_profiles.py`
- `tests/test_storage_profile_path.py`
- `tests/test_doctor.py`

**Decision owner:** the versioned storage profile controls deployment identity for the
environment-selected singleton. It does not control epistemic admission or strict reads.

**Current runtime contract:**

```text
first durable startup
→ construct requested backend or auto-select LadybugDB/SQLite
→ atomically persist backend + non-secret locator

later startup
→ validate profile and checksum
→ reject backend/locator conflict
→ construct the locked backend
→ reject automatic Mock fallback
```

**Audit questions:**

- Can changing `cwd`, installed optional packages or an environment variable select a
  different physical store after a profile exists?
- Is the profile malformed, conflicting or missing when a durable lock is expected?
- Does a test/programmatic explicit backend remain isolated from the environment-selected
  runtime singleton?
- Does `velantrim-doctor` remain read-only and avoid opening or repairing L3?
- Is profile identity being confused with truth, evidence or Canon authority?
- Is a backend/locator change being attempted without an explicit verified migration?

**Current limitations:** one default user-level profile is assumed unless
`VELANTRIM_STORAGE_PROFILE_PATH` is configured. SQLite backup/restore and guarded legacy
stale-lock recovery are implemented; cross-backend logical export/import/cutover remains
separate work.

## 1B. SQLite lifecycle and cross-backend migration

**Implemented SQLite lifecycle:**

- `core/storage_common.py`
- `core/storage_backup.py`
- `core/storage_restore.py`
- `core/storage_lock.py`
- `core/storage_ops.py`
- `docs/architecture/SQLITE_STORAGE_LIFECYCLE.md`
- storage lifecycle tests

**Architecture-only migration contract:**

- `docs/architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md`
- `docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md`
- `docs/adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md`

**Decision owner:** migration operations preserve physical state and deployment identity;
TruthGate/Guardian and strict read reconciliation retain epistemic authority.

**Approved next runtime slice:** deterministic read-only SQLite logical export and
independent bundle verification. Import, cutover, rollback and PostgreSQL are not part of
that slice.

**Audit questions:**

- Is the source opened read-only under one stable snapshot?
- Are records canonical, deterministically ordered, counted and hashed?
- Is completion published last and independently verifiable?
- Are source database/profile and localized documentation unchanged?
- Is migration receipt language being confused with claim evidence or activation?
- Are import, cutover or PostgreSQL capabilities being claimed before implementation?

## 2. Truth admission and safety

**Purpose:** decide whether a candidate may cross into trusted/canonical state.

**Start with:**

- `core/truth_gate.py`
- `core/guardian.py`
- `core/api_ingest_policy.py`
- `docs/ARCHITECTURE.md`
- `docs/CONTRADICTION_POLICY.md`

**Decision owners:** TruthGate for admission policy; Guardian for structural/safety
constraints.

**Forbidden pattern:** a caller, model, retriever, facet, storage profile or curator helper
directly mutating strict Canon outside the audited write path.

## 3. Strict read grounding and reconciliation

**Purpose:** reconcile physical graph state into an immutable trusted read view.

**Start with:**

- `core/canonical_view.py`
- TrustSnapshot implementation and tests
- public query handlers in `core/api.py`, `core/cli.py` and MCP surfaces
- `docs/CANONICAL_VIEW_RFC.md`
- `docs/architecture/read-only-query-boundary.md`

**Decision owner:** `CanonicalView`/`TrustSnapshot` read reconciliation.

**Audit questions:**

- Is the path read-only with respect to canonical state?
- Are restrictions deny-dominant?
- Is physical L3 being mistaken for strict Canon?
- Does response metadata expose the selected view and refusal reason?

## 4. Retrieval, evidence and answer grounding

**Purpose:** retrieve candidates, preserve evidence refs and build grounded answer
material.

**Start with:**

- retrieval modules under `core/`
- evidence/provenance modules under `core/`
- FactsPack, TRACE and Receipt implementations
- `docs/EVAL.md`
- `TEST_REPORT.md`

**Boundary:** retrieval rank, similarity, confidence or topic relevance is not admission
or truth.

**Audit questions:**

- Can every grounded claim be traced to source/evidence?
- Are model-derived statements labelled as such?
- Are refusal/partial-evidence conditions retained?
- Can a read accidentally create or reinforce a fact?

## 5. Provenance, TRACE, Receipt and audit

**Purpose:** provide replayable and tamper-evident proof of decisions and answers.

**Start with:**

- `core/audit.py`
- TRACE and Receipt modules under `core/`
- provenance modules under `core/`
- related tests and evaluation fixtures

**Decision owner:** the proof contract, not the presentation layer.

**Audit questions:**

- Is the record append-only or mutation-safe where required?
- Does it preserve source, policy and decision identifiers?
- Can the receipt be replayed deterministically?
- Are failures recorded without claiming a successful state change?

## 6. Contradictions and curator decisions

**Purpose:** detect conflicts, expose immutable reports and apply explicit audited
resolutions.

**Start with:**

- contradiction modules under `core/`
- `core/review.py`
- `core/conflict_surfaces.py`
- `docs/CONTRADICTION_POLICY.md`
- `docs/CONFLICT_RESOLUTION_SURFACES.md`

**Decision owner:** explicit conflict-resolution path with scoped authorization.

**Invariants:**

- detection does not select a winner;
- `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` are explicit decisions;
- no silent last-write/last-verified-wins behavior;
- failed authorization or lease acquisition must fail closed.

## 7. Curator authorization and coordination

**Purpose:** bind actors to scoped roles/capabilities and coordinate conflicting
curator actions.

**Start with:**

- `core/curator_auth.py`
- curator lease registry implementation
- authenticated conflict-resolution HTTP surface
- `docs/TOPIC_FACETS_AND_CURATOR_IAM.md`

**Current limitation:** the included lease registry is process-local, not distributed.

**Audit questions:**

- Is actor identity host-authenticated and matched?
- Is capability scope checked against the target facts/action?
- Does coordination survive multiple processes or only one process?
- Is a distributed guarantee being claimed without an adapter?

## 8. Advisory topic facets

**Purpose:** navigation, filtering and grouping.

**Start with:**

- `core/topic_facets.py`
- `docs/TOPIC_FACETS_AND_CURATOR_IAM.md`
- relevant tests

**Boundary:** topic relevance is advisory metadata only. It cannot alter evidence,
epistemic state, contradictions, TruthGate decisions or strict Canon membership.

## 9. Import, review queues and resumable sessions

**Purpose:** controlled intake and human review without bypassing admission policy.

**Start with:**

- import/session modules under `core/`
- review queue/session modules under `core/`
- CLI and HTTP import/review surfaces
- tests covering interruption, resume, restriction and rollback

**Audit questions:**

- Is session state resumable and idempotent?
- Are partial imports distinguishable from committed admission?
- Can unreviewed content ground strict answers?
- Are erasure and restriction propagated?

## 10. Public surfaces and runtime composition

**Purpose:** expose read/query, ingest, review, conflict and operator diagnostics through
stable interfaces.

**Start with:**

- `core/api.py`
- `core/cli.py`
- `core/doctor.py`
- MCP modules under `core/`
- `Dockerfile`
- package entry points in `pyproject.toml`
- `.github/workflows/ci.yml`

**Boundary:** public query/search and doctor surfaces are read-only. Mutating operations
require explicitly named and authenticated write/review surfaces.

## 11. Evaluation, mutation and performance evidence

**Purpose:** prove behavioral contracts and detect semantic drift.

**Start with:**

- `docs/EVAL.md`
- `TEST_REPORT.md`
- `docs/status/implementation-manifest.json`
- evaluation fixtures and scripts
- Ring Zero mutation gate
- benchmark history documents and workflows

**Audit questions:**

- Which exact commit produced the numbers?
- Does the gate measure runtime code or documentation only?
- Are skipped tests and environment caveats visible?
- Is a microbenchmark being presented as a production SLO?
- Was an unavailable automated review service incorrectly presented as approval?

## 12. Long-document semantic reading

**Current state:** no verified dedicated Reader Core/Semantic Reading Layer with
multi-pass coverage control is listed in the implementation manifest.

A future component should remain upstream of admission:

```text
source document
  → structural map and safe segments
  → source-linked candidate cards
  → coverage/contradiction/exception passes
  → review material
  → ordinary Guardian + TruthGate admission
```

It must not become a second Canon owner or turn summary importance into truth.

## 13. Documentation, grant and research governance

**Start with:**

- `AGENTS.md`
- `docs/DOCUMENTATION_MAP.md`
- `docs/DOCUMENTATION_SYNC_PROTOCOL.md`
- `docs/STATUS.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/GRANT_NLNET_SCOPE.md`
- `docs/ADR.md`
- `ROADMAP.md`

**Authority rule:** GitHub `main` proves implementation. Notion preserves deeper
rationale, roadmap and grant history. Research PRs and issues remain non-authoritative
until separately implemented and merged.

PostgreSQL/pgvector, dedicated VectorDB integration and automatic SQLite/PostgreSQL
switching are research/future deployment profiles, not current Crystal runtime.
