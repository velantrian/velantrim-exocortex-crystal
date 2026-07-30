# 🧪 Velantrim Crystal — Test Report

**Status:** current audited baseline  
**Implementation commit:** `cd6fd44ff4ac8c715121cae1996aa484f11ef250`  
**Merged change:** PR #265 — read-only HTTP query boundary  
**Verification date:** 2026-07-27  
**Document synchronization:** 2026-07-30

## Exact baseline

```text
Python 3.11 full suite: 1713 passed
Skipped:                12
Failed:                  0
Measured statements:    6389
Coverage:                100.00%
```

The CI matrix also completed successfully on Python 3.12. The authoritative
pre-merge GitHub Actions run for PR #265 was `30284938992`; all seven permanent
jobs passed on the reviewed head before squash merge.

## Permanent CI jobs

| Job | Result | Boundary checked |
|---|---|---|
| `test (3.11)` | success | full pytest suite and 100% coverage gate |
| `test (3.12)` | success | supported-version compatibility and coverage |
| `code-quality` | success | Ruff |
| `security` | success | Gitleaks, Bandit and pip-audit |
| `docker-build` | success | hardened image build |
| `eval-gate` | success | retrieval, grounding, contradiction and boundary metrics |
| `jsonl-integrity` | success | corpus format and duplicate-id controls |

## What PR #265 added to the verified baseline

PR #265 separated ordinary HTTP query execution from admission-capable memory
operations:

```text
/ingest         → admission path, Guardian + TruthGate
/ask, /receipt  → core.query_pipeline.query(), strict read-only Canon path
```

The regression suite verifies that the HTTP query path does not:

- ingest or update L0/L1 facts;
- transition ESM state;
- write L3 facts, edges, entities or mentions;
- enqueue or drain the L3 outbox;
- record episodic graph links;
- initialize an embedding fingerprint;
- mutate adaptive verification state;
- store unknown retrieval candidates.

The same cycle fixed two independently reviewed P1 findings:

1. unnecessary full-Canon materialization on the ordinary fingerprinted path;
2. false `STORE_STATE_CONFLICT` results caused only by equivalent float/default
   representations.

Genuine trust-metadata disagreement remains fail-closed.

## Reproduction

```bash
git checkout cd6fd44ff4ac8c715121cae1996aa484f11ef250
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

Expected properties:

- no failed test;
- required coverage remains 100%;
- eval gate prints `PASSED`;
- generated evaluation artifacts remain outside tracked source files;
- the working tree stays clean after verification.

## Evidence discipline

This report is the sole repository document that carries the exact active test,
skip, statement and coverage baseline. Other active documents should link here
rather than copying mutable counts, except for the compact README status line.

The previous long-form report is preserved byte-for-byte at:

`docs/archive/grant-sync/TEST_REPORT_PRE_SYNC_2026-07-30.md`

## Limits

This evidence demonstrates the tested repository state at the recorded commit. It
does not claim:

- absence of every defect;
- legal GDPR certification;
- security certification;
- production multi-tenant readiness;
- zero hallucinations;
- universal truth detection;
- Titan or Full Exo-Cortex functionality in Crystal.
