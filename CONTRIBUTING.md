<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🤝 Contributing to Velantrim ExoCortex — Crystal

Thank you for contributing to Crystal, an open-source, local-first memory, evidence and
decision-boundary runtime for trustworthy AI systems.

Contributions may include bug reports, documentation, tests, tooling and code. A contribution
is accepted only when its claims match merged implementation and executable evidence.

## 🧭 Before you start

1. Read [README.md](./README.md), [AGENTS.md](./AGENTS.md) and
   [docs/ai/README.md](./docs/ai/README.md).
2. Read [ROADMAP.md](./ROADMAP.md),
   [docs/IMPLEMENTATION_STATUS.md](./docs/IMPLEMENTATION_STATUS.md) and
   [docs/GLOSSARY.md](./docs/GLOSSARY.md).
3. Open an issue before large architecture, dependency, storage, security, API or breaking
   changes.
4. Follow the [Code of Conduct](./CODE_OF_CONDUCT.md).

## 🧱 Project principles

These are implementation and review constraints, not slogans:

```text
physical L3      != strict Canon
retrieval score  != evidence
model output     != source truth
migration proof  != claim proof
import success   != activation
```

- **Guardian and TruthGate** — Guardian performs structural/safety checks; TruthGate owns
  automatic epistemic admission. Do not create an unreviewed second admission owner.
- **Read/write separation** — public query surfaces route through
  `core.query_pipeline.query()` and remain read-only. Admission-capable writes use explicit
  ingest/review paths.
- **Physical storage is not authority** — L3 may hold multiple statuses. Strict Canon is the
  deny-dominant trusted read projection.
- **Honest status** — distinguish merged, tested, current, optional, planned, research and
  unsupported states. An open issue, PR, RFC, prototype or Notion page is not runtime truth.
- **Local-first stdlib runtime** — the ordinary runtime uses Python standard library only.
  New dependencies must be optional, explicitly selected and fail closed when unavailable.
- **Privacy by default** — no telemetry, analytics, outbound model calls or remote storage is
  mandatory.
- **Portable operations are bounded** — backup, migration and exact-equivalence evidence do
  not perform TruthGate admission or activate a backend.

## 💾 Current backend boundary

| Backend | Current role |
|---|---|
| SQLite | ordinary active local-first profile |
| LadybugDB | optional embedded profile, selected explicitly or by first durable `auto` when available |
| Neo4j | explicit optional remote/server adapter; expands the trust boundary |
| Mock | explicit ephemeral development and CI backend |
| PostgreSQL/pgvector | optional inactive import/equivalence target with `active=false`; not ordinary runtime |

A durable first-run `auto` may choose optional LadybugDB or SQLite and then locks the backend
and non-secret locator identity. It must not silently accept ephemeral Mock.

## 💻 Development setup

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Use a supported Python version recorded by current CI. The authoritative tested matrix is
Python 3.11 and 3.12 at the current verified checkpoint.

Install the full `[dev]` environment before trusting a local coverage result. Optional test
modules can skip when their extras are absent. Exact GitHub CI remains the merge authority.

## ✅ Pull request requirements

- [ ] The change starts from current `main` and follows repository-local instructions.
- [ ] Tests cover success, failure and relevant fail-closed behaviour.
- [ ] The full suite passes on Python 3.11 and 3.12 in CI.
- [ ] Repository line coverage remains 100%.
- [ ] New dependencies are optional or a separately approved ordinary-runtime change.
- [ ] Security, privacy, migration and authority boundaries are updated where relevant.
- [ ] Public documentation distinguishes implementation from plan/research.
- [ ] Mutable test counts, SHAs, grant status and translation checkpoints are reconciled.
- [ ] Review threads are resolved before merge.

## 🧪 Evidence discipline

A PR description should record:

- base SHA;
- validated head SHA;
- exact CI run;
- test and coverage results;
- changed-file scope;
- remaining limitations;
- whether runtime, API, dependency, authority or grant status changed.

For storage or migration work, receipts prove operation integrity only. They do not prove a
claim or grant strict Canon membership.

## 🌍 Documentation and translations

English is the working, source and conflict-resolving language. Implement and validate the
English source contract first. Localized documents use a separate docs-only reconciliation
PR with an immutable source checkpoint.

A translation must not strengthen runtime, security, grant or authority claims. Native-speaker
editorial certification is not implied unless it occurred.

## 💶 Grant-safe contributions

Current status is `submitted / under review / not awarded` with no budget change.

Anything merged before a funding agreement is existing baseline and cannot be relabelled as
future funded delivery. Grant milestones require a new measurable delta and independently
verifiable acceptance evidence.

## 🌿 Branches and commits

- Branch from current `main`.
- Use a descriptive branch name.
- Keep each PR to one logical change.
- Conventional-style commit subjects are encouraged.
- Prefer squash merge after exact-head CI when the branch contains corrective follow-up
  commits.

## 🐛 Bugs and security issues

- Bugs and feature proposals: open a GitHub issue with reproduction or acceptance detail.
- Security vulnerabilities: do not open a public issue; follow
  [SECURITY.md](./SECURITY.md).

## 📜 License

Contributions are licensed under the project's [AGPL-3.0 license](./LICENSE).

## Related documents

- [Governance](./GOVERNANCE.md)
- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Glossary](./docs/GLOSSARY.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Test report](./TEST_REPORT.md)
