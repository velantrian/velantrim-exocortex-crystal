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
- `lstat`/`open`/`fstat` identity checks, one descriptor per file and final unchanged-file/directory rechecks;
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

## Current limitations

- physical L3 only; L1 operational memory is not exported;
- no importer;
- no target schema mapping;
- no exact source/target equivalence engine;
- no retrieval-quality comparison;
- no cutover or rollback receipt;
- no encryption layer supplied by this command;
- no online distributed fencing beyond the locked deployment/profile contract;
- concurrent bundle mutation is detected and rejected, but the verifier does not provide an external filesystem lock to other processes.
