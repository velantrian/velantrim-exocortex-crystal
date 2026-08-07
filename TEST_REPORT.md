# Crystal Verification Report

**Status date:** 2026-08-07  
**Verified runtime checkpoint:** `c612c1f7de067b05ed7d01ad82d47a7bc39af23a`  
**Verified tree:** `17d65f52ac1d985fca249e6c9a183168d6116ffb`  
**Validated implementation head:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736`  
**Pull request:** #330  
**Exact-head CI:** `31213056560`

This file records the latest verified runtime checkpoint. It is evidence for the tested
repository state, not a production, legal, security or institution-scale certification.

## Result

| Gate | Result |
|---|---:|
| Python 3.11 | 2047 passed / 12 skipped / 0 failed |
| Python 3.12 | 2047 passed / 12 skipped / 0 failed |
| Measured statements | 9219 |
| Line coverage | 100.00% |
| Ring Zero declared mutants | 7/7 killed |
| Permanent CI jobs | 9/9 successful |

Successful jobs:

```text
code-quality
test (3.11)
test (3.12)
jsonl-integrity
eval-gate
security
Docker
Ring Zero mutation
docs-status
```

## Runtime delta verified in PR #330

The checkpoint adds:

- deterministic read-only logical export from a locked durable SQLite L3 profile;
- canonical JSONL datasets for nodes, vectors, edges, entities, mentions and metadata;
- completion-marker-last publication;
- independent fail-closed bundle verification;
- descriptor-bound hashing/parsing and path-swap/mutation rechecks;
- strict schema, JSON, ordering, vector and referential-integrity validation;
- an explicit bounded local-first resource contract.

Current fail-closed limits:

| Resource | Limit |
|---|---:|
| profile/control JSON | 1 MiB |
| source SQLite file | 64 MiB |
| one canonical record | 1 MiB |
| records per dataset | 200,000 |
| one dataset | 64 MiB |
| aggregate JSONL | 384 MiB |

## Authority and scale boundary

```text
physical L3 state       != strict Canon
logical bundle          != claim evidence
successful verification != backend activation
retrieval quality       != exact state equivalence
```

The current implementation is bounded for a local-first deployment envelope. It is not a
streaming or institution-scale migration engine. Issue #331 tracks cursor batching,
incremental verification and disk-backed referential checks. PostgreSQL/pgvector runtime,
inactive import, exact target equivalence, cutover and rollback remain absent and are
tracked separately in #332.

## Reproduction

```bash
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

The full repository workflow also runs Ruff, security checks, JSONL integrity, evaluation,
Docker, Ring Zero mutation and documentation-status gates.

## Evidence discipline

- `main` code and executable tests are implementation truth.
- The CI run above validates the exact implementation head merged by PR #330.
- The squash merge commit records the public main checkpoint with the same reviewed diff.
- Later changes require a fresh exact-head run before advancing these values.
