# 🧪 Velantrim Crystal — Test Report

**Status:** current verified runtime baseline  
**Runtime checkpoint:** `b10a7446dc6c88fd319161ac983263554f93107b`  
**Merged change:** PR #300 — explicit conflict-resolution CLI and HTTP surfaces  
**Verification date:** 2026-08-01  
**Status manifest:** [docs/status/implementation-manifest.json](./docs/status/implementation-manifest.json)

## Exact baseline

```text
Python 3.11:          1838 passed / 12 skipped
Python 3.12:          1838 passed / 12 skipped
Failed:               0
Measured statements:  7051
Coverage:              100.00% coverage
Ring Zero mutation:   7/7 declared mutants killed
Permanent CI jobs:    9
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
| `docs-status` | manifest, metrics, active status surfaces and local links |

## Verified implementation sequence

- **#289:** public HTTP, CLI and MCP query surfaces share a read-only service.
- **#290:** the runtime TruthPolicy bypass was removed.
- **#291:** read reconciliation uses immutable `TrustSnapshot` objects.
- **#292:** targeted Ring Zero mutation testing was added.
- **#295:** README, documentation map, implementation manifest and docs-status gate.
- **#296:** typed `ContradictionReport` and explicit curator decisions.
- **#297:** machine-readable ESM specification derived from the runtime matrix.
- **#298:** scheduled/manual L3 benchmark history and comparable-run reporting.
- **#300:** validated CLI and authenticated FastAPI conflict-resolution surfaces.

## Reproduction

```bash
git checkout b10a7446dc6c88fd319161ac983263554f93107b
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

This evidence demonstrates tested behavior at the recorded checkpoint. It does
not claim universal truth detection, absence of every defect, zero
hallucinations, legal certification, security certification, production
multi-tenant readiness, or Titan/Full Exo-Cortex functionality.
