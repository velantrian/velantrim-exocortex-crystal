# Velantrim Crystal — NLnet Grant Scope

**Baseline date:** 2026-08-08  
**Baseline checkpoint:** `main@f03e24c85922d0bb46d6d9dfee98338972135908`  
**Validated head / CI:** `17ce10ffe12da93be50434c73d08f05a70a5922b` / `31224184351`  
**Grant status:** submitted / under review / not awarded

Velantrim Crystal is open-source, local-first verifiable memory infrastructure. References
to GDPR mean **GDPR-oriented technical controls**, not automatic legal compliance or
certification.

## Current verified baseline

The prior trust/evidence/query/review baseline now also includes PR #335:

- fixed-batch SQLite logical export;
- incremental canonical JSONL write/hash/count;
- private disk-backed canonical edge ordering;
- same-descriptor hash-first independent verification;
- private disk-backed referential-integrity checks;
- bounded diagnostics, disk preflight and handled-failure cleanup;
- reproducible local-first resource evidence.

Verification:

```text
Python 3.11 / 3.12: 2059 passed / 12 skipped / 0 failed
9361 statements / 100.00% coverage
7/7 Ring Zero mutants killed
9/9 permanent CI jobs successful
2/2 resource benchmark jobs successful
```

The active envelope remains 64 MiB source/dataset, 200,000 records per dataset and 384 MiB
aggregate JSONL. Benchmark `31224005804` covers 1,025 and 8,193-record synthetic corpora. It is
not a production SLO or institution-scale certification.

## Proposed funded delta after the new baseline

Already merged #331 work cannot be budgeted again. Preferred future packages begin with:

1. **Inactive PostgreSQL/pgvector import and exact equivalence** (#332)
   - optional driver/version policy and secret-free profile identity;
   - inactive target only;
   - exact identifiers, payloads, vectors, edges, metadata, restrictions and provenance;
   - failure cleanup and receipts; no activation on import success.
2. **Exact-vs-ANN retrieval evaluation**
   - exact search reference and versioned HNSW/IVFFlat corpus;
   - recall, latency, index size and rebuild evidence;
   - ANN remains a rebuildable non-authoritative projection.
3. **Explicit cutover and rollback proof**
   - source/target fencing, immutable receipts, rollback window and crash tests.
4. **Server lifecycle and security**
   - TLS, least-privilege roles, credential rotation, backup/restore/upgrade drills.
5. **Release and audit evidence**
   - reproducible artifacts, checksums, SBOM and independent review.

## Critical distinctions and exclusions

```text
physical L3          != strict Canon
migration bundle     != claim evidence
successful import    != activation
benchmark result     != production SLO
GDPR-oriented design != legal certification
```

No current PostgreSQL runtime, automatic backend switching, production multi-tenancy,
distributed exactly-once, universal truth, zero hallucinations, AGI or consciousness is
claimed. The baseline/funding rule remains: merged capabilities cannot be counted again as
paid future work.

See the [M1–M9 matrix](./grants/baseline-funded-delta-matrix.md).
