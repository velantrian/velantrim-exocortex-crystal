<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# Crystal Project, Grant and Governance Overview

**Status date:** 2026-08-12  
**Authority:** merged GitHub `main`, executable tests, exact CI and detailed English contracts prevail.

## 1. Project position

Velantrim Crystal is open-source, local-first memory, evidence and decision-boundary infrastructure for trustworthy AI systems. It is not Titan, AGI, consciousness, a universal truth engine or a complete autonomous personal ExoCortex.

Reader Core RC-1 through RC-5 are merged bounded layers. RC-6 is the separately authorized bounded long-context milestone in issue #369 / PR #370. It adds deterministic same-session/same-version rolling working sets over valid RC-4 candidates plus caller-supplied provenance-preserving `SUMMARY` candidates. The dedicated/full autonomous Semantic Reading runtime remains not implemented.

## 2. Current retained baseline

```text
main@bbd816c09dd39a02e6de6c1014438490572f40f6
validated runtime head d7af7c80722274f9217bc5545d150f92e9363f37
CI 31256316536
PostgreSQL integration 31256316532
```

Retained evidence: Python 3.11/3.12 `2078 passed / 13 skipped / 0 failed`, 9756 measured statements / 100.00% line coverage, 7/7 Ring Zero mutants, 9/9 permanent CI and 1/1 real PostgreSQL/pgvector integration. Later Reader milestones carry separate exact-head/post-merge CI evidence.

## 3. Storage, Reader and authority boundaries

```text
physical L3             != strict Canon
retrieval score         != evidence
model output            != source truth
import success          != activation
Reader coverage         != comprehension proof
working-set coverage    != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
summary                 != source text
summary                 != evidence
summary                 != verified fact
summary                 != Canon admission
```

PostgreSQL/pgvector remains an optional inactive migration/equivalence target with `active=false`. SQLite remains ordinary active local-first.

RC-5 cannot call `core.evidence.attach_evidence()`, write fact evidence, mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, promote confidence, assert evidence sufficiency, resolve contradiction or choose a winner. It adds no LLM/provider, parser/OCR, embeddings/ANN, cross-document semantic identity, planner, API/CLI/worker, durable Reader DB or PostgreSQL activation.

RC-6 preserves that firewall. It imports only Reader layers, accepts one current RC-4 extractor / OPEN ReaderSession / exact SourceVersion, uses explicit candidate-count and source-locator budgets, keeps candidate provenance atomic, carries RC-5 relation IDs only when both sides are inside one working set, and accepts only caller-supplied `SourceFidelity.SUMMARY` text with direct RC-4 leaf provenance. It performs no automatic summarization, token-context claim, RC-7 cross-document reading, evidence admission, truth/confidence promotion, contradiction resolution or storage/backend mutation.

## 4. Grant status

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

The public funding plan discusses an **approximate €50,000 request**. It is planning/transparency, **not an approved budget or payment commitment**.

## 5. Baseline and funded-delta rule

**Anything merged before a grant agreement is existing baseline** and cannot later be billed again as future delivery. This includes storage portability work, D1-D5 documentation, Reader RC-0/RC-1/RC-2/RC-3/RC-4/RC-5 and RC-6 if RC-6 merges pre-agreement.

```text
existing verified baseline + new measurable funded delta
= independently auditable public deliverable
```

## 6. Grant-safe future work

Only new evidence beyond the merged baseline can be funded delta, for example:

- reproducible release/SBOM/audit evidence;
- exact-vs-ANN evaluation;
- explicit cutover/rollback/fencing proof;
- PostgreSQL operational lifecycle;
- reviewer-facing evidence inspection UX;
- RC-6 only while it remains unmerged pre-agreement work;
- after a pre-agreement RC-6 merge, separately authorized Reader work **after RC-6**;
- later RC-7 cross-document reading with explicit identity/authority boundaries.

The grant does not fund recreation of already merged RC-5 work, and if RC-6 merges before an agreement it cannot later be counted again as funded delta.

## 7. Governance

Significant architectural or invariant changes begin in issues/RFCs. Merges require executable evidence and current docs. Maintainer authority cannot silently weaken Ring Zero, Guardian, TruthGate, read-only query, Reader authority firewall, storage continuity or privacy contracts.

RC-6 does not authorize RC-7. Cross-document reading remains a separate milestone that requires a new bounded authorization after RC-6 completion evidence.

## 8. Contribution rules

Contributions must preserve:

- physical-L3/strict-Canon separation;
- Guardian/TruthGate ownership of admission;
- Reader artifacts as upstream non-authoritative observations/process/candidates;
- `EXTRACTED_PROPOSITION != verified fact`;
- `Reader candidate != admitted evidence`;
- `contradiction candidate != confirmed contradiction`;
- `working-set coverage != comprehension proof`;
- `summary != evidence` and `summary != verified fact`;
- read-only public query surfaces;
- stdlib-only ordinary runtime with optional dependencies explicit;
- exact grant/localization/status language.

## 9. Current non-claims

No grant award, approved budget, legal/GDPR/security certification, AGI/consciousness, active PostgreSQL runtime, automatic switching, accepted ANN profile, production multi-tenancy, dedicated/full autonomous Reader, automatic summarization, RC-7 cross-document reading or automatic semantic contradiction resolution is claimed.

## 10. Authoritative sources

- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)
- [Reader architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Roadmap](../ROADMAP.md)
- [Governance](../GOVERNANCE.md)
- [Contributing](../CONTRIBUTING.md)
- [Glossary](./GLOSSARY.md)
