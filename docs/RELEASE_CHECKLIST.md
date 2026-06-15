# Velantrim Crystal — Release Checklist

Use this checklist before publishing a public release or pointing grant reviewers
to the repository.

## 1. Version and tag

- [ ] `pyproject.toml` version is correct.
- [ ] `README.md` badge/version line is correct.
- [ ] `CHANGELOG.md` has an entry for the release.
- [ ] Git tag exists, for example `v0.1.0`.
- [ ] GitHub Release notes link to the changelog and demo.

## 2. Tests and CI

- [ ] `pip install -e '.[dev]'` succeeds from a **fresh venv** (the `[dev]`
      extra and `requirements-dev.txt` must stay aligned).
- [ ] `pip install -r requirements-dev.txt` succeeds (CI path).
- [ ] `pip install -e .` succeeds (bare stdlib-only install).
- [ ] `pytest tests/ --cov=. --cov-fail-under=100` passes locally.
- [ ] `python scripts/eval_gate.py --out-dir eval-artifacts` passes and the
      working tree stays **clean** afterwards (`git status --short` is empty —
      no generated artifact is tracked).
- [ ] `python -m build` produces an sdist + wheel without errors (manual smoke
      step, not part of CI).
- [ ] GitHub Actions CI passes on Python 3.11 and 3.12.
- [ ] `TEST_REPORT.md` matches the latest test count and command.

## 3. Documentation

- [ ] `README.md` describes only implemented and tested behaviour.
- [ ] `DEMO.md` shows the verifiable memory flow.
- [ ] `docs/ARCHITECTURE.md` matches the current pipeline and backends.
- [ ] `docs/EVAL.md` states which metrics exist today and which are planned.
- [ ] `docs/GRANT_NLNET_SCOPE.md` is aligned with the current grant narrative.
- [ ] `ROADMAP.md` separates delivered work from planned work.

## 4. Privacy and security

- [ ] No databases, `.env` files, logs, secrets or personal data are committed.
- [ ] `SECURITY.md` test count and dependency wording are current.
- [ ] `PRIVACY.md` accurately describes optional external providers.
- [ ] `GDPR.md` avoids legal overclaims and stays technical.
- [ ] Optional backends remain opt-in.

## 5. Invariants

- [ ] No code path writes to L3 without Guardian/TruthGate.
- [ ] `source`, `source_status`, `claim_type` and epistemic state are preserved.
- [ ] LLM output is not promoted to world fact without evidence.
- [ ] Erasure, restriction, audit and receipt paths are covered by tests.
- [ ] Browser/PWA demos are described as demos, not as the Crystal security boundary.

## 6. Public release notes

Suggested release title:

```text
Velantrim Crystal v0.2.0 — Verifiable local-first AI memory core
```

Suggested release summary:

```text
Local-first, verifiable AI memory core. Automatic writes to the L3 canon pass a
single enforced entry — TruthGate / Guardian (an audited curator force-approve
override path is also available; see core/review.py). Answers carry TRACE
provenance; verifiable receipts are generated separately via `velantrim receipt`
and can be replayed and verified offline.

Baseline: 1168 passed / 12 skipped / 100% coverage (Python 3.11 and 3.12),
following the safe repo-hygiene / toolchain-hardening pass and the documentation
synchronisation that aligned README, TEST_REPORT and ROADMAP with the current
state. Fractal Memory is documented as the shipped multi-scale anchoring
baseline (core/fractal.py) and is explicitly distinct from the broader private
Research Mode "Fractal Memory / Fractal Attention" concept.

Scope is deliberately bounded: no production-ready, zero-hallucination, or
AGI/consciousness claims.
```
