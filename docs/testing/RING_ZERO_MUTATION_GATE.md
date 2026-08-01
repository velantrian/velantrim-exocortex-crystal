# Ring Zero Mutation Gate

**Status:** implemented CI quality gate  
**Scope:** selected load-bearing invariants, not repository-wide mutation coverage

## Purpose

Line coverage proves that code executed. It does not prove that tests would
notice a semantic change. Crystal therefore runs a small deterministic mutation
gate over selected trust-boundary predicates.

The gate answers one narrow question:

```text
If this exact safety condition were inverted or weakened,
would a named behavior test fail?
```

## Execution model

`scripts/ring_zero_mutation_gate.sh`:

1. creates a fresh temporary workspace for each mutation;
2. copies `core/`, `tests/` and `adaptive_threshold_module.py`;
3. verifies that the declared source fragment occurs exactly once;
4. replaces that fragment with one deterministic semantic mutation;
5. runs only the named pytest nodes expected to detect it;
6. accepts only pytest exit code `1` as a killed mutant;
7. treats a surviving mutant, source drift, no-tests result, collection error,
   usage error or internal pytest error as a gate failure.

The checked-out repository is never modified by the harness.

## Declared mutation set

| Mutation | Safety property pinned |
|---|---|
| TruthGate `<` → `<=` | confidence equal to threshold remains admissible |
| `LLM_OUTPUT` predicate redirected | model output cannot become independent world evidence |
| CanonicalView VERIFIED predicate inverted | strict projection requires `VERIFIED` |
| restriction predicate inverted | restricted/unknown processing state fails closed |
| strict ESM allowlist inverted | only approved ESM states enter strict CanonicalView |
| malformed-confidence condition inverted | corrupt confidence creates an explicit trust conflict |
| receipt digest equality inverted | fresh receipts verify and tampered receipts fail |

## Why this is not a full mutation framework

A complete mutation run across the repository would be slower, more expensive
and more sensitive to environment variation. This gate is intentionally:

- deterministic;
- small enough for every pull request;
- dependency-light (`pytest` only);
- tied to named Ring Zero behaviors;
- fail-closed on source/test drift.

It does **not** claim a repository-wide mutation score or semantic completeness.
A broader scheduled mutation campaign may be added separately after stable
baselines and runtime budgets are measured.

## Adding a mutation

A new declaration must include:

- a unique exact source fragment;
- one syntactically valid replacement;
- one or more named pytest nodes that fail for the intended reason;
- a load-bearing invariant worth enforcing on every pull request.

Do not add mutants merely to increase a count. The mutation should represent a
credible weakening of a documented contract.

## Relationship to other gates

The mutation gate complements rather than replaces:

- the Python 3.11/3.12 full suite;
- the 100% line-coverage threshold;
- deterministic eval;
- Ruff;
- Gitleaks, Bandit and pip-audit;
- Docker build verification;
- JSONL integrity.

The current exact test/coverage baseline remains in `TEST_REPORT.md`.