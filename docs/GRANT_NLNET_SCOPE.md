# Velantrim Crystal — NLnet Grant Scope

**Baseline date:** 2026-08-08  
**Baseline checkpoint:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Grant status:** submitted / under review / not awarded

Velantrim Crystal is open-source, local-first verifiable memory infrastructure. References
to GDPR mean **GDPR-oriented technical controls**, not automatic legal compliance or
certification.

## Current verified baseline

The prior trust/evidence/query/review and bounded SQLite migration baseline now also
includes PR #337:

- explicit optional Psycopg extra and lazy loading;
- PostgreSQL 16 / pgvector 0.8.2 / Psycopg 3.3.x preflight;
- TLS-required production path and a separately marked local-test-only plaintext flag;
- import into a new `active=false` schema only;
- serializable transactional import from a verified logical bundle;
- independent read-only canonical target re-hash;
- exact record-count, canonical-byte-count and SHA-256 equivalence;
- non-secret endpoint-bound receipts and redacted failures;
- real PostgreSQL/pgvector integration evidence.

Verification:

```text
Python 3.11 / 3.12: 2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% coverage
7/7 Ring Zero mutants killed
9/9 permanent CI jobs successful
1/1 PostgreSQL integration job successful
```

This establishes portable inactive migration evidence for the approved bundle datasets. It
does not establish an active PostgreSQL runtime backend, institution-scale throughput,
production multi-tenancy, legal certification or grant award.

## Proposed funded delta after the new baseline

Issues #331 and #332 are already implemented and cannot be budgeted again. Preferred future
packages begin with:

1. **Exact-vs-ANN retrieval evaluation**
   - exact pgvector search reference;
   - versioned HNSW/IVFFlat corpus and thresholds;
   - recall, latency, index-size, rebuild and stale-index evidence.
2. **Explicit cutover and source/target fencing**
   - immutable cutover receipt;
   - no reachability-based or automatic switching;
   - crash-window and partial-failure tests.
3. **Rollback proof and expiry policy**
   - explicit rollback receipt, validity window and deterministic recovery evidence.
4. **PostgreSQL server lifecycle and operational security**
   - least-privilege roles, certificate/credential rotation;
   - backup, independent restore drill, retention and upgrade sequencing;
   - pooling, timeout/retry and observability policy.
5. **Release, supply-chain and independent audit evidence**
   - reproducible artifacts, checksums, SBOM, pinned actions and public review findings.

## Critical distinctions and exclusions

```text
physical L3          != strict Canon
migration bundle     != claim evidence
successful import    != activation
exact equivalence    != production runtime
GDPR-oriented design != legal certification
```

No automatic backend switching, active PostgreSQL runtime selection, production
multi-tenancy, distributed exactly-once, universal truth, zero hallucinations, AGI or
consciousness is claimed. The baseline/funding rule remains: merged capabilities cannot be
counted again as paid future work.

See the [M1–M9 matrix](./grants/baseline-funded-delta-matrix.md).