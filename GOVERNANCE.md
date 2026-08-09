<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🏛️ Governance

This document explains how decisions are made in Velantrim ExoCortex — Crystal,
how the project is maintained and how it remains independently auditable.

## 🎯 Project scope

Crystal is an open-source, local-first memory, evidence and decision-boundary runtime for
trustworthy AI systems. The ordinary runtime remains pure Python standard library; optional
adapters and providers expand the dependency or trust boundary only when explicitly selected.

Crystal is not a complete Personal ExoCortex, Titan runtime, AGI, consciousness system or
universal truth engine. It provides bounded infrastructure for source-linked claims,
evidence, explicit admission, read-only grounded retrieval, audit and portable storage
operations.

## 👤 Roles

- **Lead maintainer (current BDFL-style model):** Velantrian currently reviews and merges
  changes, coordinates releases, maintains the roadmap and handles security disclosure.
- **Contributors:** anyone who opens issues, documentation changes, tests or pull requests.
- **Future maintainers:** sustained contributors with demonstrated technical judgement and
  respect for project invariants may be invited to receive review and merge rights.

A maintainer can decide project direction but cannot make a prose claim override merged code,
executable tests, exact CI or immutable evidence.

## 🗳️ Decision-making

- **Day-to-day changes** — scoped fixes, tests and documentation are decided through review.
- **Significant changes** — architecture, Ring Zero, public contracts, dependencies, storage
  profiles, security boundaries and breaking changes begin in an issue, RFC or ADR.
- **Operator-reserved decisions** — funding agreements, production deployment policy,
  credential ownership and other explicitly reserved operator actions are not silently
  delegated to automation.
- **Visible rationale** — decisions remain traceable in issues, PRs, ADRs, release notes and
  changelog history.

## 🧱 Hard governance constraints

```text
physical L3      != strict Canon
retrieval score  != evidence
model output     != source truth
migration proof  != claim proof
import success   != activation
```

The following constraints cannot be weakened by an ordinary feature decision:

- Guardian performs structural, safety and policy checks;
- TruthGate owns automatic epistemic admission;
- public query surfaces remain read-only through `core.query_pipeline.query()`;
- explicit ingest remains the admission-capable write path;
- curator overrides are explicit, attributed and audited;
- storage profile identity is not epistemic authority;
- SQLite remains ordinary active local-first unless a separately evidenced transition is
  explicitly approved;
- PostgreSQL/pgvector remains inactive with `active=false` until separate cutover evidence;
- uncertainty fails closed rather than silently promoting a claim.

## 📚 Authority and documentation

Authority order:

```text
merged GitHub main + executable tests + exact CI
→ machine-readable implementation/status evidence
→ detailed English architecture, security, grant and governance contracts
→ checkpointed translations and Notion rationale/history
```

English is the working, source and conflict-resolving language. Translations are maintained
public product surfaces but do not create independent runtime, grant, security, TruthGate or
strict-Canon authority.

Notion stores synchronized rationale, strategy and history. It is not runtime proof.

## 🌱 Becoming a maintainer

A contributor may be invited to become a maintainer after sustained, high-quality work that
shows:

- accurate distinction between implemented, tested, planned and research states;
- preservation of Guardian, TruthGate and strict-read boundaries;
- disciplined testing, security review and documentation;
- constructive review behaviour and responsible disclosure;
- ability to maintain public evidence rather than rely on authority claims.

This invitation is a governance decision, not an automatic reward based on commit count.

## ♻️ Sustainability

- The ordinary core requires no hosted infrastructure to remain usable.
- CI provides reproducible tests, 100% line-coverage enforcement, security, mutation,
  evaluation and documentation-status gates.
- Documentation, manifests, receipts and exact checkpoints reduce dependence on one person's
  memory.
- Funding, contractor or assistant support must map to independently verifiable public
  deliverables and must not rebill already merged baseline work.
- Funding does not transfer epistemic authority to a sponsor, model provider or backend.

## 💶 Grant governance

Current public status:

```text
NLnet proposal: submitted / under review / not awarded
budget change: none
```

The approximate €50,000 funding-use plan is planning information, not an approved budget or
payment commitment. Award or budget status may change only from verified external grant
communication.

Baseline rule:

```text
verified existing baseline + new measurable funded delta
= independently verifiable public deliverable
```

Anything merged before an agreement is existing baseline and cannot be counted again as
future paid work.

## 📦 Releases and versioning

- Releases are tagged from green `main` after evidence and documentation are reconciled.
- The package version in `pyproject.toml` is the published version source.
- Internal design-line names do not replace semantic package versioning.
- A release is not evidence of production certification or support for every optional
  deployment profile.

## 🔐 Security

Security vulnerabilities follow the private responsible-disclosure process in
[SECURITY.md](./SECURITY.md), not public issues.

## Related documents

- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Glossary and claim discipline](./docs/GLOSSARY.md)
- [Contributing](./CONTRIBUTING.md)
- [Roadmap](./ROADMAP.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)
