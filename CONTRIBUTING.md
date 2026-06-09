# 🤝 Contributing to Velantrim ExoCortex — Crystal

Thank you for your interest in Crystal — a verifiable, local-first memory
infrastructure for trustworthy AI. Contributions of all sizes are welcome: bug
reports, documentation, tests, and code.

## 🧭 Before you start

1. Read the **[README](./README.md)** and **[ROADMAP.md](./ROADMAP.md)**.
2. **Open an issue before large changes** so we can agree on the approach.
3. Be respectful — see the **[Code of Conduct](./CODE_OF_CONDUCT.md)**.

## 🧱 Project principles (please preserve them)

These are enforced in code, not just documented. A change that breaks one of them
will not be merged:

- **Graph = Truth** — the L3 canonical graph is the single source of truth; the
  **only** way in is through the TruthGate. Never write to L3 bypassing it.
- **Honesty invariant** — `ROADMAP.md` distinguishes *implemented & tested* from
  *designed but not coded*, and the README documents only the former. Do not
  claim, in docs or status, anything that is not actually in the code and tested.
- **Local-first & dependency-free runtime** — the default runtime uses the Python
  standard library only. New runtime dependencies must be **optional** (an extra
  in `pyproject.toml`) with a dependency-free fallback.
- **Privacy by design** — no telemetry, no outbound network calls by default.

## 💻 Development setup

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'      # editable install + pytest/coverage
pytest                       # full suite (see TEST_REPORT.md)
```

The default backends are dependency-free (`mock` L3, hashing embedder, extractive
generator), so the suite runs offline with no API keys.

## ✅ Pull request checklist

- [ ] Tests added/updated; `pytest` passes locally.
- [ ] **Coverage stays at 100%** (the gate is enforced in CI via `--cov-fail-under=100`).
- [ ] New runtime deps are optional with a stdlib fallback (or none added).
- [ ] Docs updated where relevant; `ROADMAP.md` reflects implemented vs designed.
- [ ] Commits are scoped and clearly described.

## 🌿 Branches & commits

- Branch from `main`; use a descriptive branch name.
- Conventional-style commit messages are appreciated (`feat:`, `fix:`, `docs:`, …).
- Keep PRs focused — one logical change per PR is easier to review.

## 🐛 Reporting bugs & security issues

- **Bugs / features:** open a GitHub issue with steps to reproduce.
- **Security vulnerabilities:** do **not** open a public issue — follow the
  responsible-disclosure process in **[SECURITY.md](./SECURITY.md)**.

## 📜 License of contributions

By contributing you agree that your contributions are licensed under the project's
**AGPL-3.0** license (see [LICENSE](./LICENSE)).
