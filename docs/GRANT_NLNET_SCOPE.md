<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# Velantrim Crystal — NLnet Grant Scope

**Baseline date:** 2026-08-09  
**Frozen runtime checkpoint:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

Velantrim Crystal is open-source, local-first verifiable memory infrastructure. References
to GDPR mean **GDPR-oriented technical controls**, not automatic legal compliance or
certification.

This document describes public technical scope. It is not an award notice, signed agreement,
approved budget or payment commitment.

## Current verified runtime baseline

The trust/evidence/query/review and bounded storage baseline includes:

- Guardian structural/safety checks and TruthGate epistemic admission;
- read-only public query surfaces with TRACE and receipts;
- source spans, document records, import sessions and curator review paths;
- durable SQLite ordinary active local-first profile;
- bounded deterministic SQLite logical export and independent verification;
- optional lazy Psycopg extra;
- PostgreSQL 16 / pgvector 0.8.2 / Psycopg 3.3.x preflight;
- TLS-required ordinary PostgreSQL path and explicit local-test-only plaintext override;
- import into a fresh `active=false` schema only;
- SERIALIZABLE transactional import from a verified bundle;
- independent read-only target canonical re-hash;
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

This establishes portable inactive migration evidence for approved physical-L3 datasets. It
does not establish active PostgreSQL runtime, whole-system migration, institution-scale
throughput, production multi-tenancy, legal certification or grant award.

## Current documentation baseline

English is the working, source and conflict-resolving language. Current public baseline
includes:

- full root README parity for nine supported locales;
- D1 entry/use translations;
- D2 reviewer/safety translations;
- D3 architecture/storage-authority translations;
- D4 English project/grant/governance/glossary source contracts before localized D4 refresh.

Any localization or governance work merged before a grant agreement is existing baseline and
cannot be counted again as funded delivery.

## Baseline and funded-delta control

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

Issues #331 and #332, PRs #335 and #337, and merged D1–D4 documentation work cannot be
budgeted again. If `main` advances before an agreement, the baseline/funded-delta matrix must
be reconciled so each funded package remains genuinely additional and independently auditable.

## Potential funded delta after the frozen baseline

Qualifying future packages may include:

1. **Reproducible release evidence**
   - wheel/sdist/container reproduction;
   - checksums, SBOM and supported-version manifest;
   - clean-machine verification.
2. **Exact-vs-ANN retrieval evaluation**
   - exact pgvector search reference;
   - versioned HNSW/IVFFlat corpus and thresholds;
   - recall, latency, index-size, rebuild and stale-index evidence.
3. **Explicit cutover and source/target fencing**
   - immutable cutover receipt;
   - no reachability-based or automatic switching;
   - crash-window and partial-failure tests.
4. **Rollback proof and expiry policy**
   - explicit rollback receipt, validity window and deterministic recovery evidence.
5. **PostgreSQL server lifecycle and operational security**
   - least-privilege roles, certificate and credential rotation;
   - backup, independent restore drill, retention and upgrade sequencing;
   - pooling, timeout/retry and observability policy.
6. **Evidence and TRACE inspection UX**
   - source-span navigation and reviewer-facing uncertainty/refusal views;
   - read-only, content-light audit export.
7. **Source-linked Reader Core prototype**
   - bounded structure maps, segmentation, candidate cards and coverage reports;
   - output remains upstream of Guardian and TruthGate;
   - no second Canon owner.
8. **Maintenance and independent audit evidence**
   - stronger claim lint, action/dependency pinning and public remediation reports.

A dedicated Reader Core is not implemented in the current baseline.

## Critical distinctions and exclusions

```text
physical L3          != strict Canon
migration bundle     != claim evidence
successful import    != activation
exact equivalence    != production runtime
GDPR-oriented design != legal certification
submitted proposal   != awarded grant
```

No automatic backend switching, active PostgreSQL runtime selection, ANN production
acceptance, cutover, rollback, dual-write, production multi-tenancy, distributed
exactly-once, universal truth, zero hallucinations, AGI or consciousness is claimed.

## Budget and award control

The public funding-use plan discusses an approximate €50,000 request. It remains planning and
transparency material until verified external communication establishes an agreement.

Award or budget state may change only from authoritative external evidence, such as a signed
grant agreement or Memorandum of Understanding. Private correspondence details are not
published as runtime or budget claims.

## Authoritative supporting documents

- [Project, grant and governance overview](./PROJECT_GRANT_AND_GOVERNANCE.md)
- [Glossary and claim discipline](./GLOSSARY.md)
- [Baseline → funded delta → acceptance matrix](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)
- [Roadmap](../ROADMAP.md)
- [Governance](../GOVERNANCE.md)
- [Current status](./STATUS.md)
- [Test report](../TEST_REPORT.md)
