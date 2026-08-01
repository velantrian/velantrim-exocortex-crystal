# 🧪 Velantrim Crystal — Test Report

**Status:** current verified runtime baseline  
**Runtime checkpoint:** `916097f049f2e71fa679571ac897e9d887957f4f`  
**Merged change:** PR #292 — targeted Ring Zero mutation gate  
**Verification date:** 2026-08-01  
**Status manifest:** [docs/status/implementation-manifest.json](./docs/status/implementation-manifest.json)

## Exact baseline

```text
Python 3.11:          1780 passed / 12 skipped
Python 3.12:          1780 passed / 12 skipped
Failed:               0
Measured statements:  6484
Coverage:              100.00% coverage
Ring Zero mutation:   7/7 declared mutants killed
```

The runtime checkpoint was verified on both supported Python versions. The
current repository CI topology contains **9 permanent CI jobs**; the
`docs-status` job was added by the documentation-hardening change after the
runtime checkpoint and validates that active public documents continue to report
this baseline consistently.

## Permanent CI jobs

| Job | Boundary checked |
|---|---|
| `test (3.11)` | full pytest suite and 100% line-coverage gate |
| `test (3.12)` | supported-version compatibility and the same coverage gate |
| `code-quality` | Ruff over production and repository tooling code |
| `security` | Gitleaks, Bandit and pip-audit |
| `docker-build` | hardened runtime image build |
| `eval-gate` | retrieval, grounding, contradiction and refusal metrics |
| `jsonl-integrity` | corpus parsing, required fields and duplicate identifiers |
| `Ring Zero mutation gate` | seven declared semantic mutations must be killed |
| `docs-status` | manifest, README, STATUS, TEST_REPORT and implementation-status consistency |

## What the verified sequence added

### PR #289 — unified public read-only query boundary

HTTP `/ask` and `/receipt`, CLI `ask` and `receipt`, and MCP search use the same
zero-durable-mutation query service.

Regression tests pin that these surfaces do not:

- create or update L0/L1 facts;
- transition ESM state;
- write L3 facts, relations, entities or mentions;
- enqueue, drain or clear the L3 outbox;
- record episodic context;
- initialize an unset embedding fingerprint;
- mutate adaptive verification state;
- store unknown retrieval candidates.

Restricted rows are excluded before claim/source content is returned by search.

### PR #290 — non-configurable LLM-origin TruthGate rule

The runtime read of `ENABLE_TRUTH_POLICY` was removed. Historical values such as
`off`, `false`, `0` and `legacy` no longer weaken the rule.

```text
LLM_OUTPUT + WORLD_FACT
        ↓
not eligible for automatic VERIFIED admission
```

This is an admission-policy invariant, not a claim that TruthGate independently
knows objective truth.

### PR #291 — immutable TrustSnapshot

Read-time reconciliation now first creates a frozen, slotted `TrustSnapshot`
from physical L3, optional deny-dominant L1 state and ranking metadata.

The dedicated tests pin:

- immutability and scalar-only retained state;
- terminal ESM dominance;
- processing-restriction dominance;
- non-terminal ESM disagreement;
- confidence, claim-type and source-status drift;
- malformed metadata failing closed;
- content-free conflict categories;
- compatibility mapping freshness.

Malformed confidence remains `None` inside the snapshot and forces a conflict;
the temporary outward mapping preserves the historical safe `0.0` sentinel for
existing mapping consumers.

### PR #292 — targeted Ring Zero mutation gate

The executable mutation harness creates isolated temporary workspaces, applies
seven fixed semantic mutations and runs the tests assigned to each mutation.

Declared mutations cover:

1. TruthGate threshold `<` changed to `<=`;
2. LLM-origin block redirected away from `LLM_OUTPUT`;
3. strict `VERIFIED` predicate inverted;
4. processing-restriction deny predicate inverted;
5. strict ESM allowlist inverted;
6. malformed-confidence conflict condition inverted;
7. Receipt digest equality inverted.

A mutation is counted as killed only when pytest exits with a normal test failure
(return code `1`). A surviving mutation, missing source fragment, duplicate source
fragment, missing test, collection failure or internal pytest error fails the CI
job.

## Reproduction

```bash
git checkout 916097f049f2e71fa679571ac897e9d887957f4f
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
```

Expected properties:

- no failed ordinary test;
- required coverage remains 100%;
- eval gate reports success;
- all seven declared mutations are killed;
- generated evaluation artifacts remain outside tracked source files;
- the checked-out source tree is not modified by the mutation harness.

For the current documentation branch or later `main`, also run:

```bash
bash scripts/check_docs_status.sh
```

## Evidence discipline

This report and the machine-readable manifest are the authoritative repository
surfaces for exact test counts, statement counts, coverage and verified
checkpoint. Other active documents may repeat the compact status line only when
the `docs-status` gate confirms consistency.

A modification timestamp alone does not prove that a translation or historical
report describes the newest implementation.

## Limits

This evidence demonstrates tested behavior at the recorded checkpoint. It does
not claim:

- absence of every defect;
- universal truth detection;
- zero hallucinations;
- legal GDPR certification;
- security certification;
- production multi-tenant readiness;
- full domain correctness of every source;
- repository-wide mutation adequacy beyond the declared Ring Zero mutations;
- Titan or Full Exo-Cortex functionality in Crystal.
