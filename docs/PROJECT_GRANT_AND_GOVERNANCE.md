<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# Crystal Project, Grant and Governance Overview

**Status date:** 2026-08-09  
**Purpose:** stable, translation-oriented D4 source summary.  
**Authority:** merged GitHub `main`, executable tests, exact CI and detailed English grant/governance documents prevail.

## 1. Project position

Velantrim Crystal is an open-source, local-first memory, evidence and decision-boundary runtime for trustworthy AI systems. The default installation is designed to remain usable without mandatory cloud, telemetry, analytics, external LLM or server dependencies.

Crystal is not a complete personal ExoCortex, Titan runtime, AGI, consciousness system or universal truth engine. It provides bounded infrastructure for source-linked claims, evidence, read-only grounded retrieval, explicit admission, audit and portable storage operations.

## 2. Current verified baseline

The verified runtime checkpoint remains:

```text
main@bbd816c09dd39a02e6de6c1014438490572f40f6
validated head d7af7c80722274f9217bc5545d150f92e9363f37
CI 31256316536
PostgreSQL integration 31256316532
```

Evidence:

- Python 3.11 and 3.12: 2078 passed / 13 skipped / 0 failed;
- 9756 measured statements / 100.00% line coverage;
- 7/7 declared Ring Zero mutants killed;
- 9/9 permanent CI jobs successful;
- 1/1 real PostgreSQL/pgvector integration job successful.

Documentation and translation merges after that checkpoint do not create new runtime capability.

## 3. Storage and authority boundaries

```text
physical L3      != strict Canon
retrieval score  != evidence
model output     != source truth
migration proof  != claim proof
import success   != activation
```

SQLite remains the ordinary active local-first profile. A first durable `auto` may select optional LadybugDB or SQLite and then locks the deployment identity. Explicit Mock is development/CI state.

PostgreSQL/pgvector remains an optional inactive migration/equivalence target with `active=false`, absent from ordinary runtime composition. Active PostgreSQL reads/writes, ANN acceptance, automatic switching, cutover, fencing, rollback and dual-write are not implemented.

## 4. Grant status

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

The public funding plan discusses an approximate €50,000 request. It is a planning and transparency document, not an approved budget or payment commitment.

Grant status may change only from verified external communication such as a signed agreement or Memorandum of Understanding. Private application correspondence is not public runtime or budget evidence.

## 5. Baseline and funded-delta rule

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

Anything merged before a grant agreement is existing baseline and cannot be billed again as future delivery. This includes the SQLite logical migration and inactive PostgreSQL import/equivalence phases, as well as D1–D4 documentation work merged before funding.

If `main` advances before an agreement, the baseline/funded-delta matrix must be reconciled so the funded scope remains genuinely additional, measurable and independently auditable.

## 6. Grant-safe future work

Potential future funded packages include only new evidence beyond the baseline, such as:

- reproducible release artifacts, checksums and SBOM;
- exact-vs-ANN evaluation with accepted thresholds;
- explicit source/target fencing, cutover receipts and rollback proof;
- PostgreSQL production roles, backup/restore/upgrade lifecycle and observability;
- reviewer-facing evidence and TRACE inspection UX;
- a bounded source-linked Reader Core prototype upstream of Guardian and TruthGate;
- stronger claim lint, maintenance and independent audit evidence.

A dedicated Reader Core remains not implemented. Research notes, prior art and architectural proposals are not current Crystal runtime.

## 7. Governance model

Crystal currently uses lightweight maintainer-led governance:

- one current lead maintainer reviews and merges changes;
- significant architecture, invariant, dependency and breaking changes begin in an issue or RFC;
- decisions and rationale remain visible in issues, PRs, ADRs and changelog history;
- sustained contributors may be invited to become maintainers;
- security vulnerabilities follow private responsible disclosure;
- releases are cut from green `main` and use the package version as the published version source.

The maintainer may make project decisions, but cannot override executable evidence or silently weaken Ring Zero, Guardian, TruthGate, read-only query, storage continuity, privacy or claim-discipline contracts.

## 8. Contribution rules

Contributors must preserve:

- physical-L3/strict-Canon separation;
- Guardian and TruthGate ownership of automatic admission;
- read-only public query surfaces;
- explicit admission-capable ingest;
- stdlib-only ordinary runtime, with new dependencies optional and fail-closed;
- local-first and no outbound network by default;
- exact implementation/test/status language;
- separate runtime, research, RFC, grant and translation authority.

A contribution is not complete merely because code exists. Relevant tests, 100% coverage gate, documentation, security review and exact CI evidence are required.

## 9. Sustainability and independence

The ordinary core does not require hosted infrastructure. Optional remote adapters and providers extend the trust boundary only when deliberately configured.

Sustainability mechanisms include:

- reproducible CI and public evidence;
- scoped releases and semantic versioning;
- transparent issue/PR history;
- documentation and machine-readable status manifests;
- contributor onboarding and bus-factor reduction;
- grant or contractor support tied to independently verifiable deliverables.

Funding does not transfer epistemic authority to a sponsor, provider, model or storage backend.

## 10. Current non-claims

Crystal does not claim:

- grant award or approved budget;
- legal, GDPR or security certification;
- AGI, consciousness, personhood or zero hallucinations;
- active PostgreSQL runtime, automatic switching, accepted ANN, cutover, rollback or dual-write;
- production multi-tenancy or distributed exactly-once coordination;
- completed dedicated Reader Core;
- that every physical graph record is strict Canon;
- native-speaker editorial certification for translations.

## 11. Authoritative detailed sources

- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Baseline → funded delta → acceptance matrix](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)
- [Roadmap](../ROADMAP.md)
- [Governance](../GOVERNANCE.md)
- [Contributing](../CONTRIBUTING.md)
- [Glossary](./GLOSSARY.md)
- [Current status](./STATUS.md)
- [Test report](../TEST_REPORT.md)
