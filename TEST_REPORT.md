# Velantrim Crystal — Test Report

**Status:** current verified runtime baseline
**Runtime checkpoint:** `b0df17a06d552ad2543b6d6e5efe8cd99877cfc0`
**Validated PR head:** `aa822c49c095039de90b92fbe4fe451c7b8f13b7`
**Validated and merged tree:** `6143d7237222935182db86a166541d0ad07887be`
**Merged change:** PR #325 — verified SQLite storage lifecycle
**Verification date:** 2026-08-07
**GitHub Actions run:** `31182471502`
**Status manifest:** [docs/status/implementation-manifest.json](./docs/status/implementation-manifest.json)

## Exact baseline

```text
Python 3.11:          2019 passed / 12 skipped
Python 3.12:          successful under the same strict coverage gate
Failed:               0
Measured statements:  8726
Coverage:              100.00% coverage
Ring Zero mutation:   7/7 declared mutants killed
CI topology:          9 permanent CI jobs
```

## Permanent CI jobs

| Job | Boundary checked |
|---|---|
| `test (3.11)` | full pytest suite and 100% coverage gate |
| `test (3.12)` | supported-version compatibility and the same gate |
| `code-quality` | Ruff over production and tooling code |
| `security` | secret, Python-security and dependency checks |
| `docker-build` | hardened runtime image build |
| `eval-gate` | retrieval, grounding, contradiction and refusal metrics |
| `jsonl-integrity` | corpus parsing and duplicate identifiers |
| `Ring Zero mutation gate` | seven declared semantic mutations must be killed |
| `docs-status` | English authoritative status, evidence, links and claim boundaries |

## Verified PR #325 behavior

PR #325 added a pure-standard-library operator surface for a locked SQLite profile:

```text
status
backup
verify
restore to a new inactive database/profile
inspect-lock
explicit guarded recover-lock
```

The bundle uses SQLite's online backup API, publishes completion last, verifies hashes,
integrity, table counts and profile identity, and never overwrites or activates the current
profile. Stale-lock recovery uses quarantine and a recovery-owned placeholder so it cannot
unlink a lock won by a new initializer.

## Authority boundary

```text
storage lifecycle = deployment continuity
physical L3      != strict Canon
backup receipt   != evidence for a claim
restore          != TruthGate admission
```

## Architecture-only next step

Issue #327 defines an English backend-neutral migration contract and a proposed
PostgreSQL/pgvector institutional profile. Those documents do not add cross-backend
runtime support.

## Reproduction

```bash
git checkout aa822c49c095039de90b92fbe4fe451c7b8f13b7
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

## Evidence boundary

This evidence demonstrates tested behavior at the recorded checkpoint. It does not claim
universal truth detection, absence of every defect, zero hallucinations, legal or security
certification, production multi-tenant readiness, distributed locking, cross-backend
migration, PostgreSQL/pgvector runtime support, or Titan/Full ExoCortex functionality.
