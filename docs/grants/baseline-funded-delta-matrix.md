# Crystal baseline → funded delta → acceptance matrix

**Status date:** 2026-08-12  
**Grant state:** submitted / under review / not awarded — **no award/budget change**.

Anything merged before an agreement is existing pre-agreement baseline and **cannot be counted
again as future paid work**.

## Existing verified / pre-agreement baseline

| Area | Existing baseline | Authority / non-claim |
|---|---|---|
| Trust/evidence | Guardian, TruthGate, strict read projection, evidence/provenance | physical L3 != strict Canon |
| Query | HTTP/CLI/MCP read-only query pipeline | query != ingest/admission |
| SQLite | ordinary active local-first + lifecycle/export | operation evidence != truth evidence |
| PostgreSQL target | inactive import/equivalence | target remains `active=false` |
| Reader RC-1 | source/session/provenance skeleton | no truth authority |
| Reader RC-2 | caller-supplied structural map | structure != truth |
| Reader RC-3 | explicit deterministic multi-pass ledger | pass completion != comprehension proof |
| Reader RC-4 | source-linked proposition candidates | `EXTRACTED_PROPOSITION != verified fact`; candidate != evidence |
| Reader RC-5 | same-session/same-version typed relation candidates | contradiction candidate != confirmed contradiction |
| Reader RC-6 | bounded working sets + caller-supplied `SUMMARY` | summary != source/evidence/Canon |
| Reader RC-7 | explicit cross-document link candidates | candidate link != Canon relation; similarity != identity |
| Reader RC-8 | retrieval architecture decision + 20-case adversarial corpus | decision/eval design, not semantic/vector runtime |
| Reader RC-9 | deterministic offline in-memory BM25 PRE-ADMISSION candidate discovery + benchmark runner | ranking != authority; discovery != adjudication |
| Reader RC-10 preregistration | merged reuse-compatibility/future comparison contract in PR #378 | no comparison executed; no Reader runtime capability added |

Machine Reader boundary remains:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
```

RC-8/RC-9/RC-10 do not create a full autonomous Reader machine flag.

## RC-9 frozen evidence baseline

Committed result: `eval/reader_rc9_lexical_baseline.json`, K=5, 20 synthetic/adversarial
paired cases.

| Metric | Result | Safe interpretation |
|---|---:|---|
| Recall@5 | 0.937500 | 15/16 known useful paired mates surfaced |
| Precision@5 | 0.187500 | bounded fixed-K paired benchmark definition only |
| MRR | 0.895833 | ranking position of known useful paired mates |
| Paired hard-negative rate@5 | 1.000000 | all 4/4 known hard-negative mates surfaced |

Known positive miss: cross-lingual paraphrase `rc8-004`. Classification:
`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

These metrics are retrieval evidence, not “94% accuracy”, semantic equivalence accuracy,
truth accuracy, contradiction accuracy or evidence-admission quality.

## Funded-delta rule at agreement time

The matrix must be re-audited against live `main` when/if an agreement is signed. The funded
column may contain only work that is **not already present** at that time.

| Possible future delta | Minimum independent acceptance evidence | Must not be assumed in advance |
|---|---|---|
| Deploy/release hardening | clean install/run path, reproducible artifacts/checksums, CI, documented rollback/limitations | production readiness/certification |
| Source-span / receipt replay improvements | exact span identity, replay fixtures, tamper/failure tests, provenance checks | automatic truth verification |
| Larger retrieval/evaluation surface | frozen/versioned corpus, pre-registered metrics, reproducible runner, explicit failure analysis | semantic understanding or runtime authorization |
| Optional future retrieval comparison, only if still justified | exact backend/model identity, dependency/privacy/resource review, zero authority violations, benchmark evidence | embeddings/vector DB as predetermined solution |
| Storage operational lifecycle | explicit backup/restore/upgrade/cutover evidence with fencing and recovery tests | PostgreSQL activation from import equivalence alone |
| Accessibility/localization | exact English checkpoint, language review/freshness ledger, parity validation | stronger capability claims in translation |
| Security/supply-chain hardening | concrete controls, pinned/reviewed dependencies, scans, SBOM or documented acceptance artifacts as scoped | “fully secure” / GDPR certification |

This list is illustrative grant planning, not a commitment that every item will be funded or
implemented. The exact funded delta must be frozen only after live baseline reconciliation.

## Existing-vs-future Reader rule

```text
RC-0..RC-9 merged pre-agreement
        = existing Reader baseline

RC-10 preregistration merged pre-agreement
        = existing architecture/evaluation history, not Reader runtime

future Reader capability
        = separately authorized + independently measured delta only
```

A future semantic/hybrid/vector comparison is **not required by RC-9**. RC-9 measured both a
cross-lingual/low-overlap gap and hard-negative pressure; it did not select the remedy.

## Retrieval-domain separation

Existing admitted-memory retrieval (`core/embedding.py`, `core/legacy_retrieval.py`,
`core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py` and admitted-memory
composition) is distinct from Reader PRE-ADMISSION candidate discovery.

Reusing infrastructure later requires an explicit authority/data-lifecycle review. Its mere
existence does not make Reader vector retrieval an existing capability.

## Funding and security non-claims

Approximate €50,000 is planning only and does not represent an approved budget/payment
commitment. NLnet is submitted / under review / not awarded.

Local-first does not itself prove GDPR compliance or complete security. PostgreSQL/pgvector
remains inactive `active=false`. #155, #165 and #214 remain separate backlog and are not
silently folded into this matrix.
