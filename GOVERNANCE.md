# 🏛️ Governance

This document explains how decisions are made in Velantrim ExoCortex — Crystal,
how the project is maintained, and how it stays sustainable. It is deliberately
lightweight, matching the size of the project.

## 🎯 Project scope

Crystal is the **open, dependency-free core** of the broader Velantrim ExoCortex
system: a verifiable, local-first memory engine with provenance, an audited
TruthGate, GDPR machinery, and biologically-inspired memory layers. The core is
intentionally small and self-contained so that a single maintainer can sustain it
and so that third parties can audit, run, and extend it without heavy
infrastructure.

## 👤 Roles

- **Maintainer (BDFL-style, current):** the project is currently led by a single
  maintainer (**Velantrian**) who reviews and merges changes, sets direction via
  `ROADMAP.md`, and is responsible for releases and security handling.
- **Contributors:** anyone who opens issues or pull requests. Sustained,
  high-quality contributors may be invited to become maintainers (see below).

## 🗳️ Decision-making

- **Day-to-day** (bug fixes, docs, tests, scoped features): decided by the
  maintainer, ideally after discussion in an issue or PR.
- **Significant changes** (architecture, new invariants, new runtime dependencies,
  breaking changes): proposed in an issue first, discussed openly, then decided by
  the maintainer. The **project principles** in
  [CONTRIBUTING.md](./CONTRIBUTING.md) (Graph = Truth, honesty invariant,
  local-first/dependency-free, privacy by design) act as hard constraints.
- Decisions and their rationale are kept visible in issues, PRs, and the changelog.

## 🌱 Becoming a maintainer

The project actively wants to reduce its bus factor. A contributor who has made
sustained, high-quality contributions and demonstrates good judgement about the
project's principles may be invited by the current maintainer to become a
maintainer, with commit and review rights. This is how the project broadens its
stewardship over time.

## ♻️ Sustainability

- **No hosted infrastructure is required** to run or maintain the core — it is a
  stdlib-only library with optional backends, so there is no server to keep alive.
- **Reproducibility** is part of governance: CI runs the full test suite on every
  change, and the coverage gate (95%) is enforced, so the project's health is
  verifiable by anyone at any time.
- **Continuity:** documentation, tests, and the honesty invariant are maintained
  so that the project remains understandable and operable independently of any one
  person. Funding (e.g. grants — see [.github/FUNDING.yml](./.github/FUNDING.yml))
  is used to harden the core, improve documentation, and support contributors.

## 📦 Releases & versioning

- Releases are tagged from `main` once CI is green.
- The package follows semantic versioning starting at `0.1.0` (the first public
  release of the open core). The architecture has an internal lineage (the "v8"
  Crystal design line) which is documented in `ROADMAP.md`, but the **published
  package version** in `pyproject.toml` is the source of truth.

## 🔐 Security

Security vulnerabilities are handled privately under the process described in
[SECURITY.md](./SECURITY.md), not via public issues.
