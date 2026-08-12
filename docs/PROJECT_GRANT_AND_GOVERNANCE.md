<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# Crystal Project, Grant and Governance Overview

**Status date:** 2026-08-12  
**Authority:** merged GitHub `main`, executable tests, exact CI and detailed English contracts prevail.

## 1. Project position

Velantrim Crystal is open-source, local-first memory, evidence and decision-boundary
infrastructure for trustworthy AI systems. It is not Titan, AGI, consciousness, a universal
truth engine or a complete autonomous personal ExoCortex.

Reader Core RC-1 through RC-7 are merged bounded Reader/domain layers. RC-8 is a completed
retrieval architecture/research decision. RC-9 is the completed deterministic lexical
PRE-ADMISSION candidate-discovery implementation baseline with a reproducible benchmark.
`dedicated_reader_core=false` remains the larger capability truth.

PR #378 later merged the RC-10 existing-retrieval reuse / future-comparison preregistration
contract only. It executes no semantic/hybrid comparator and adds no Reader retrieval runtime.

## 2. Current evidence checkpoints

Retained storage/runtime compatibility evidence remains:

```text
main@bbd816c09dd39a02e6de6c1014438490572f40f6
validated runtime head d7af7c80722274f9217bc5545d150f92e9363f37
CI 31256316536
PostgreSQL integration 31256316532
```

Current Reader retrieval implementation evidence:

```text
RC-9 signed merge      f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61
RC-9 PR                #376
RC-9 exact-head CI     31593097846 (9/9)
RC-9 post-merge CI     31594027040 (9/9)
```

The repository has later signed documentation/evaluation history. Exact current `main` and CI
must always be read from live GitHub rather than inferred from this overview.

## 3. Reader, retrieval and authority boundaries

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
cross-document candidate != Canon relation
similarity               != identity
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

RC-9 is an offline, stdlib-only, in-memory deterministic BM25 baseline over Reader proposition
snapshots. It returns inspection candidates and retrieval/provenance metadata only. It does
not write evidence, mutate ESM/Canon, auto-register RC-7 relations, decide identity or resolve
contradictions.

Existing admitted-memory vector/query retrieval (`core/embedding.py`,
`core/query_pipeline.py`, `core/legacy_retrieval.py`, `core/rrf.py` and related composition)
is a different authority/data lifecycle. Its existence does not make Reader semantic/vector
retrieval an implemented capability.

## 4. Storage boundary

SQLite remains ordinary active local-first storage. PostgreSQL/pgvector remains an optional
inactive migration/equivalence target with `active=false`.

Successful PostgreSQL import/equivalence is operational evidence, not activation or epistemic
authority. Automatic backend switching remains absent.

## 5. RC-9 measured baseline

Frozen K=5 result over the 20-case synthetic/adversarial RC-8 paired corpus:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Paired hard-negative hits | 4 / 4 |

The cross-lingual paraphrase `rc8-004` is missed and all four paired hard negatives surface
within top-5. Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

These are retrieval metrics, not semantic/adjudication accuracy. They do not authorize
embeddings, ANN/vector DB, semantic/hybrid runtime, claim identity or evidence admission.

## 6. Grant status

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

The public funding plan discusses an **approximate €50,000 request**. It remains
planning/transparency, **not an approved budget or payment commitment**.

## 7. Baseline and funded-delta rule

**Anything merged before a grant agreement is existing baseline** and cannot later be billed
again as future delivery. RC-1 through RC-9 are therefore existing pre-agreement Reader
baseline. PR #378's RC-10 preregistration is also existing pre-agreement architecture/evaluation
history, not funded delivery and not a new Reader runtime capability.

```text
existing verified baseline + new measurable funded delta
= independently auditable public deliverable
```

A possible future funded delta must be redefined against live `main` if/when an agreement is
signed. It may not relabel already merged work as unpaid/future work or assume that RC-9's
measured gap mandates semantic/vector technology.

## 8. Grant-safe future work

Examples of genuinely new work that may be considered only if still absent and justified at
agreement time include:

- reproducible release/SBOM/audit evidence;
- production-strength source-span/replay improvements;
- larger evaluation fixtures and regression gates;
- operational storage lifecycle/cutover/rollback proof;
- reviewer-facing evidence tooling;
- accessibility/localization work;
- a separately authorized retrieval experiment under pre-registered gates if evidence still
  warrants it.

No future-funded work may redefine Reader candidates as evidence/Canon, similarity as identity,
repetition as corroboration, or a benchmark/comparison pass as runtime authorization.

## 9. Governance

Significant architectural or invariant changes begin in issues/RFCs. Merges require executable
evidence and current docs. Maintainer authority cannot silently weaken Ring Zero, Guardian,
TruthGate, read-only query, Reader authority firewall, storage continuity or privacy contracts.

Grant-facing documentation may improve presentation, but it may not manufacture capabilities.

## 10. Contribution rules

Contributions must preserve:

- physical-L3/strict-Canon separation;
- Guardian/TruthGate ownership of admission;
- Reader artifacts as upstream non-authoritative observations/process/candidates;
- `EXTRACTED_PROPOSITION != verified fact`;
- `Reader candidate != admitted evidence`;
- `contradiction candidate != confirmed contradiction`;
- `working-set coverage != comprehension proof`;
- `summary != evidence` and `summary != verified fact`;
- `retrieval match != evidence`;
- `similarity != identity`;
- `ranking != epistemic authority`;
- read-only public query surfaces;
- stdlib-only ordinary runtime with optional dependencies explicit;
- exact grant/localization/status language.

## 11. Current non-claims

No grant award, approved budget, legal/GDPR/security certification, AGI/consciousness, active
PostgreSQL runtime, automatic switching, dedicated/full autonomous Reader, semantic/hybrid/vector
Reader runtime, automatic claim identity/corroboration, automatic contradiction resolution or
automatic evidence admission is claimed.

## 12. Authoritative sources

- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)
- [Reader architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [RC-9 lexical baseline](./architecture/READER_RC9_LEXICAL_BASELINE.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Roadmap](../ROADMAP.md)
- [Governance](../GOVERNANCE.md)
- [Contributing](../CONTRIBUTING.md)
- [Glossary](./GLOSSARY.md)
