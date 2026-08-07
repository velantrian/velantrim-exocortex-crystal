# SQLite Logical Export and Independent Verification

**Status:** implemented by issue #329 / implementation PR; not a whole-system migration
**Architecture:** [Cross-Backend Storage Migration Contract](./CROSS_BACKEND_MIGRATION_CONTRACT.md)
**Authority:** physical L3 is not strict Canon; a migration bundle is not claim evidence

## Purpose

This operator slice creates a deterministic backend-neutral representation of the locked
SQLite physical L3 and verifies it without reopening or mutating the source deployment.
It establishes only phases 2–4 of ADR-021:

```text
locked SQLite profile
→ read-only logical export
→ completion marker
→ independent fail-closed verification
```

It does not import into another backend, activate a profile, compare target state, evaluate
retrieval quality, implement PostgreSQL/pgvector, or authorize a cutover.

## Commands

```bash
velantrim-storage export-logical ./l3-export \
  --profile ~/.velantrim/velantrim-storage-profile.json

velantrim-storage verify-logical ./l3-export
```

Both commands emit one JSON object. Exit codes follow the existing storage CLI contract:

- `0` — `PASS`;
- `1` — a valid report whose status is not `PASS`;
- `2` — fail-closed operator/validation error.

## Bundle format

A completed bundle contains exactly:

```text
manifest.json
complete.json
nodes.jsonl
vectors.jsonl
edges.jsonl
entities.jsonl
mentions.jsonl
meta.jsonl
```

`complete.json` is written last. A directory without it is not a completed export.

The six JSONL files use canonical sorted-key JSON, one record per line, deterministic
ordering, owner-only file permissions, SHA-256 digests, byte sizes and record counts.
The manifest records:

- bundle schema/type;
- SQLite profile and locator digests;
- SQLite schema and user versions;
- dataset metadata;
- vector dimension, when vectors exist;
- explicit non-authority flags.

Absolute database/profile paths and credentials are not written into the bundle.

## Export guarantees

Export requires:

- a valid locked durable SQLite profile;
- regular non-symlink profile and database files;
- exact known physical L3 table columns;
- successful `PRAGMA integrity_check`;
- one explicit read transaction;
- strict JSON without duplicate keys, `NaN` or infinity;
- finite non-empty vectors with one consistent dimension;
- unchanged profile digest from export start through completion;
- a new no-clobber output directory.

A handled failure removes the incomplete output directory.

## Independent verification

Verification does not open the source profile or source database. It checks:

- exact bundle file set;
- completion and manifest schemas;
- manifest and dataset hashes over the exact bytes parsed by the verifier;
- `lstat`/`open`/`fstat` identity checks, one descriptor per file and final
  unchanged-file/directory rechecks;
- byte sizes and record counts;
- strict/canonical JSONL representation;
- strict deterministic ordering;
- record shapes and identifier consistency;
- vector element validity and dimension consistency;
- node/vector, edge and mention referential integrity;
- fixed authority boundary flags.

Successful verification proves only bundle integrity and conformance to this export schema.
It does not prove target compatibility, successful import, claim truth, strict Canon
membership, admissibility, safe activation or production readiness.

## Local-first resource contract

The first implementation is deliberately bounded rather than presented as an
institution-scale migration engine. Export and verification fail closed before accepting
inputs outside these fixed limits:

| Resource | Limit |
|---|---:|
| storage profile or control JSON file | 1 MiB |
| source SQLite database file | 64 MiB |
| one canonical JSONL record | 1 MiB |
| records in one dataset | 200,000 |
| one dataset file | 64 MiB |
| aggregate JSONL data in one bundle | 384 MiB |

The source database size and table counts are checked before full dataset materialization.
The writer also enforces per-record, per-dataset and aggregate byte limits while emitting
the bundle. The independent verifier validates declared counts and sizes before reading the
datasets and applies the same record and byte ceilings while parsing.

These limits make memory and disk exposure finite for the current local-first slice. They
do **not** establish bounded-memory operation proportional to a small batch, support for
arbitrarily large stores, or institution-scale PostgreSQL migration. Issue #331 tracks the
required cursor batching, incremental parsing/hashing and disk-backed referential checks.
PostgreSQL/pgvector work in issue #332 remains blocked on that institutional-scale gate.

Changing these constants is a migration-format and operational-policy change. It requires
review, adversarial tests, exact-head CI and synchronized documentation; operators must not
patch limits silently to bypass the fail-closed contract.

## Current limitations

- physical L3 only; L1 operational memory is not exported;
- bounded local-first resource envelope; no institution-scale claim;
- datasets and referential indexes are still materialized within the documented limits;
- no importer;
- no target schema mapping;
- no exact source/target equivalence engine;
- no retrieval-quality comparison;
- no cutover or rollback receipt;
- no encryption layer supplied by this command;
- no online distributed fencing beyond the locked deployment/profile contract;
- concurrent bundle mutation is detected and rejected, but the verifier does not provide
  an external filesystem lock to other processes.
