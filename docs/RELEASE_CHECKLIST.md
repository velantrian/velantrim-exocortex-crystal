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

- [ ] `pip install -r requirements-dev.txt` succeeds.
- [ ] `pip install -e .` succeeds.
- [ ] `pytest tests/ -v --cov=core --cov-fail-under=95` passes locally.
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
Velantrim Crystal v0.1.0 — Verifiable local-first AI memory core
```

Suggested release summary:

```text
This release provides a dependency-free, local-first open core for verifiable AI
memory: L0/L1 working memory, L3 canonical graph, TruthGate, source tracking,
replayable receipts, external knowledge ingestion, GDPR-relevant controls,
read-only MCP integration, and an evaluation/documentation baseline.
```
