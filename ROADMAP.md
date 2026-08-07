# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Current verified baseline:** `main@f03e24c85922d0bb46d6d9dfee98338972135908`  
**Validated head / CI:** `17ce10ffe12da93be50434c73d08f05a70a5922b` / `31224184351`

## ✅ Delivered baseline

Crystal includes the trust/evidence/query/storage lifecycle baseline plus:

- deterministic bounded-streaming SQLite logical export;
- disk-backed canonical edge ordering and referential checks;
- same-descriptor independent verification;
- cleanup and resource preflight;
- 2059 tests, 9361 statements, 100% coverage and 9/9 CI;
- benchmark `31224005804` 2/2 with explicit non-SLO limits.

## ✅ Completed — issue #331 / PR #335

The production path no longer retains complete datasets or global identifier sets. Existing
64 MiB source/dataset, 200,000-record and 384 MiB aggregate limits remain active. Raising
them requires a separate evidence-backed change.

## P1 — Inactive PostgreSQL/pgvector import (#332)

Next phase only:

```text
verified bundle
→ PostgreSQL preflight
→ inactive target import
→ exact state equivalence
→ import/equivalence receipts
```

No activation, cutover, rollback, dual-write or automatic switching.

## P2 — Exact/ANN evaluation, cutover and rollback

- exact pgvector search reference;
- versioned HNSW/IVFFlat evaluation;
- source/target fencing and explicit cutover receipt;
- rollback proof and expiry policy.

## P2 — Server lifecycle and security

- least-privilege roles, TLS and credential rotation;
- backup/restore/upgrade drills;
- transaction/retry policy and observability;
- no certification or distributed exactly-once overclaim.

## P2/P3 — Release evidence and Reader Core research

- reproducible artifacts, checksums, SBOM and dependency pinning;
- source-linked Reader Core prototype only upstream of Guardian/TruthGate.

**No grant award** or budget change is claimed. PostgreSQL runtime, automatic switching,
production multi-tenancy, universal truth, zero hallucinations and legal certification
remain out of scope.
