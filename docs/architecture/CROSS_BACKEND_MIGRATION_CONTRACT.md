# Cross-Backend Storage Migration Contract

**Status:** Accepted architecture contract; SQLite export/verification phases implemented, later phases absent
**Decision issue:** #327
**Runtime baseline:** SQLite lifecycle from PR #325
**Documentation language:** English is authoritative during active engineering
**Implemented operator slice:** [SQLite logical export and verification](./SQLITE_LOGICAL_EXPORT.md)

## Purpose

Changing a physical storage backend is not a configuration edit. It is a controlled,
auditable transfer of physical state between two independently identified deployments.

This contract applies to future SQLite, LadybugDB, Neo4j, PostgreSQL/pgvector, or other
storage transitions. It does not grant any backend epistemic authority.

```text
backend availability != migration
profile edit/delete   != migration
import success        != activation
migration receipt     != evidence for a claim
retrieval quality     != exact state equivalence
physical L3           != strict Canon
```

## Authority boundary

Migration moves physical state only. It must not:

- call or emulate TruthGate admission;
- change Guardian decisions;
- promote, demote, verify, invalidate, restrict, erase, or resolve a claim;
- select a contradiction winner;
- convert vector similarity into evidence;
- change strict Canon membership except as an identical consequence of preserved state.

The source deployment remains authoritative until a separate explicit cutover receipt is
created after all required gates pass.

## Required phases

```text
1. preflight
2. deterministic read-only logical export
3. completed bundle publication
4. independent bundle verification
5. import into a new inactive target
6. exact state-equivalence evaluation
7. retrieval-quality evaluation
8. explicit cutover
9. optional explicit rollback
```

Each phase must be independently observable and fail closed. Completion of one phase does
not imply permission to start or claim completion of another.

## Phase 1 — Preflight

Preflight must record without exposing secrets:

- source backend, schema version, profile identity and locator digest;
- target backend/version/capabilities and inactive locator identity;
- required optional dependencies and extension versions;
- source integrity and read-only snapshot capability;
- available disk space and output/target non-existence;
- migration bundle schema version;
- expected authority-bearing and derived datasets;
- unsupported features or lossy mappings.

Preflight must reject an active target, an existing output path, malformed profiles,
unsupported schemas, missing capabilities, or a transformation that cannot preserve the
required state.

## Phase 2 — Deterministic read-only logical export

The first implementation slice is intentionally limited to SQLite logical export and
independent verification.

Export must:

- open the source read-only;
- use one stable database snapshot;
- serialize records in deterministic order;
- use canonical JSON/JSONL representations;
- preserve exact identifiers and typed payloads;
- include per-file counts, byte sizes and SHA-256 digests;
- record source profile identity without credentials;
- publish a completion marker last;
- leave the source database and profile unchanged;
- remove a handled incomplete bundle after failure.

A backup copy is not automatically a backend-neutral migration export. A migration bundle
contains logical records and explicit schema semantics rather than a source-engine database
file.

## Required logical datasets

For the current SQLite physical L3 baseline:

| Dataset | Required logical content | Ordering |
|---|---|---|
| `nodes` | `fact_id` plus parsed node payload | `fact_id` |
| `vectors` | `fact_id` plus finite numeric vector | `fact_id` |
| `edges` | source, relation, target, parsed properties | source, relation, target, canonical properties |
| `entities` | entity id, kind, label | entity id |
| `mentions` | fact id, entity id, relation | fact id, entity id, relation |
| `meta` | metadata key and value, including embedder fingerprint when present | key |

Future migrations that include L1 operational state must separately enumerate facts,
restrictions, erasure markers, evidence spans, import/review sessions, decision journals,
audit checkpoints and pending projection work. They must not imply that exporting physical
L3 alone is a complete whole-system migration.

## Phase 3 — Completed bundle publication

A valid bundle must contain:

- a versioned manifest;
- exactly the declared logical data files;
- canonical records in deterministic order;
- source identity and non-secret schema metadata;
- a completion marker written only after internal verification;
- hashes that bind the manifest and every declared file.

An incomplete directory, a directory with undeclared files, a symlinked file, a malformed
record, a count mismatch, an ordering violation, or a hash mismatch is invalid.

## Phase 4 — Independent verification

Verification must be possible without opening or mutating the source deployment.

It must validate:

- completion marker and manifest schemas;
- manifest hash;
- exact allowed file set;
- file sizes, SHA-256 digests and record counts;
- canonical JSON encoding and deterministic ordering;
- identifier/payload shape;
- finite vector elements and consistent dimensions when vectors exist;
- source profile identity and declared backend;
- declared database schema/user version;
- cross-record diagnostics such as missing node/vector references.

Verification proves bundle integrity and contract conformance. It does not prove claim
truth, target compatibility, successful import, or safe cutover.

## Phase 5 — Inactive target import

Not implemented by the first runtime slice.

A future importer must:

- require a new inactive target and explicit target profile path;
- never overwrite or activate the current profile;
- be idempotent or use an explicit resumable journal;
- document transaction boundaries and crash windows;
- preserve restrictions, erasure and audit semantics;
- produce an import receipt;
- leave the source active after success.

## Phase 6 — Exact state equivalence

Exact equivalence is a blocking gate. It must compare source export and target logical
export after import.

At minimum, future full-system migration proof must cover:

- facts and stable identifiers;
- serialized payload semantics;
- vectors, dimensions and embedder fingerprint;
- edges, entities, mentions and metadata;
- epistemic/ESM/trust state;
- contradiction dispositions;
- restrictions and erasure markers;
- evidence/provenance references;
- audit checkpoints and receipt continuity;
- pending projection/outbox work.

A single mismatch blocks cutover even when retrieval benchmarks look good.

## Phase 7 — Retrieval-quality equivalence

Retrieval evaluation is separate from exact-state equivalence.

For exact search and approximate indexes, record:

- exact nearest-neighbour baseline;
- recall@k and filtered recall;
- ranking drift for a versioned query corpus;
- latency and memory/index size;
- index build/rebuild duration;
- behavior when the index is stale or unavailable.

Approximate HNSW/IVFFlat performance cannot waive an exact-state mismatch.

## Phase 8 — Explicit cutover

Cutover is not implemented by the first runtime slice.

A future cutover must require:

- verified export, import, exact-equivalence and retrieval receipts;
- explicit operator confirmation;
- target health and backup proof;
- atomic or fail-closed profile activation;
- a cutover receipt binding source and target identities;
- documented read/write freeze or fencing semantics.

Automatic backend switching after data exists is forbidden.

## Phase 9 — Rollback

Rollback must be explicit and must not silently overwrite state written after cutover.
A future design must define:

- the rollback window;
- write freeze/fencing behavior;
- target changes after activation;
- source revalidation;
- rollback receipt and audit continuity;
- conditions under which rollback is no longer safe.

## Security and privacy

- Credentials, tokens, passwords, DSNs with secrets and private keys must never enter the
  bundle or storage profile.
- Bundle permissions should default to owner-only.
- Export and verification must reject final symlinks and no-clobber violations.
- Sensitive payloads remain sensitive; migration does not create a public artifact.
- Encryption-at-rest or transport encryption is deployment policy, not proof of claim truth.

## First runtime implementation slice

The approved first slice is:

```text
locked SQLite profile
→ deterministic read-only logical export
→ completed backend-neutral bundle
→ independent fail-closed verification
```

It explicitly excludes import, PostgreSQL, pgvector, activation, rollback, dual-write,
live cutover and automatic switching.

## Acceptance evidence for each implementation PR

- exact base/head/merge SHA;
- focused adversarial tests;
- 100% repository line-coverage gate;
- all nine permanent CI jobs;
- deterministic repeat-export evidence;
- source immutability proof;
- malformed/tampered/symlink/no-clobber tests;
- explicit remaining limitations;
- GitHub and Notion synchronization.
