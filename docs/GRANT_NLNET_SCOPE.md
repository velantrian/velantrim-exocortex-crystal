<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# NLnet Scope — Crystal

**Status date:** 2026-08-12  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## Authority boundary

```text
submitted proposal        != awarded grant
planning amount           != approved budget
merged pre-agreement work != future funded delta
retrieval match           != evidence
similarity                != identity
ranking                   != epistemic authority
candidate discovery       != candidate adjudication
```

Approximate €50,000 remains planning context only. No payment commitment or approved budget is
claimed.

## Existing verified / pre-agreement baseline

Crystal already contains the trust/evidence/query/storage foundation plus the bounded Reader
line through the **RC-9 deterministic lexical candidate-discovery baseline**. Work merged before
an agreement is existing baseline and cannot later be rebilled as future funded delivery.

Reader maturity is deliberately bounded:

| Reader stage | Existing baseline | Authority boundary |
|---|---|---|
| RC-0 | normative Reader architecture contract | architecture, not runtime capability |
| RC-1 | source/version/session/provenance skeleton | no truth authority |
| RC-2 | caller-supplied Structural Document Map | structure != truth |
| RC-3 | explicit deterministic multi-pass mechanics | pass completion != comprehension proof |
| RC-4 | source-linked `EXTRACTED_PROPOSITION` candidates | proposition candidate != verified fact/evidence |
| RC-5 | same-session/same-version relation candidates | contradiction candidate != confirmed contradiction |
| RC-6 | bounded long-context working sets + caller-supplied `SUMMARY` | summary != source/evidence/Canon |
| RC-7 | explicit cross-document candidate links with two-sided provenance | cross-document candidate != Canon relation |
| RC-8 | retrieval architecture decision + frozen adversarial corpus | no semantic/vector runtime |
| RC-9 | offline stdlib-only deterministic BM25 candidate discovery + benchmark | ranking/candidate discovery only; no adjudication |

Machine Reader truth remains:

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

RC-8 and RC-9 do not turn `dedicated_reader_core` true. The subsequently merged RC-10
reuse/comparison preregistration contract (PR #378) is also pre-agreement repository history,
but it executes no comparator and adds no Reader retrieval runtime.

## RC-9 as a reviewer-verifiable proof point

Frozen artifact: `eval/reader_rc9_lexical_baseline.json`. Frozen RC-8 input: 20 paired
synthetic/adversarial cases, K=5.

| Metric | Frozen result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Paired hard-negative hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

The baseline misses the cross-lingual pair `rc8-004` and surfaces all four paired hard
negatives in top-5. These are **retrieval metrics**, not semantic accuracy, truth verification,
claim identity or evidence-admission metrics. Precision@5 follows the bounded fixed-K paired
benchmark definition documented in the RC-9 architecture note.

Reproduce with:

```bash
python scripts/bench_reader_rc9_lexical.py \
  --corpus eval/reader_rc8_retrieval_adversarial.jsonl \
  --k 5 \
  --json-out /tmp/reader-rc9-lexical.json
```

## Existing baseline vs possible future funded delta

The grant accounting boundary must follow live repository truth:

```text
verified existing pre-agreement baseline
+
new measurable work performed under an agreement
=
independently verifiable funded deliverable
```

RC-1 through RC-9 are **existing baseline**, not future paid delivery. PR #378's RC-10
preregistration contract is likewise existing pre-agreement documentation/evaluation design;
it must not be represented as a future deliverable that has not yet happened.

Possible future funded work must therefore be a genuinely new, independently measurable
delta. Examples may include deployment/release hardening, source-span/replay improvements,
larger evaluation surfaces, accessibility/localization work, operational storage lifecycle or
a separately authorized retrieval experiment **if evidence still justifies it at agreement
time**.

Semantic/vector Reader work is not a committed funded requirement. The RC-9 measured gap only
creates evidence for later research decisions; it does not prescribe embeddings, ANN, vector
DB or any specific backend.

## Reader retrieval domains must remain separate

Crystal already contains admitted-memory/query retrieval machinery (`core/embedding.py`,
`core/query_pipeline.py`, `core/legacy_retrieval.py`, `core/rrf.py` and related composition).
That infrastructure is not the same authority/data lifecycle as PRE-ADMISSION Reader
candidate discovery.

```text
PRE-ADMISSION Reader
RC-4 → RC-9 lexical candidate discovery → review/adjudication → normal admission boundary

ADMITTED MEMORY
strict read projection → existing query/retrieval machinery
```

The presence of general vector-capable admitted-memory infrastructure is **not** a claim that
Reader semantic/vector retrieval exists.

## Claim taxonomy for grant-facing text

### GREEN — safe when tied to current evidence

- local-first architecture;
- deterministic lexical Reader candidate discovery;
- offline stdlib-only RC-9 baseline;
- reproducible frozen benchmark;
- source/provenance-aware Reader pipeline;
- explicit authority separation;
- CI-backed implementation with signed/verified merge history where cited exactly.

### YELLOW — use only with explicit context

- intelligent retrieval;
- document understanding;
- cross-document reasoning;
- evidence linking.

These phrases are safe only when the text makes clear that bounded Reader candidates and
source-linked artifacts do not autonomously adjudicate truth, identity or evidence.

### RED — not current Crystal Reader capability

- semantic understanding;
- automatic claim identity;
- automatic truth verification/corroboration;
- automatic contradiction resolution;
- autonomous evidence admission;
- production-grade semantic search;
- Reader vector/ANN runtime or vector DB capability.

## Storage / privacy / security boundary

SQLite remains the ordinary active local-first storage path. PostgreSQL/pgvector is an
inactive import/equivalence target with `active=false`; successful migration/equivalence is
operation evidence, not activation.

Local-first and offline operation are useful privacy characteristics, but they do not imply
legal GDPR compliance or complete security certification. Known supply-chain/PII hardening
work remains separate under #214.

## Residual backlog kept outside this grant-truth milestone

- #155 — Epistemic Router / Evidence State RFC;
- #165 — exact normalized admitted-fact dedupe/migration;
- #214 — PII fixture / supply-chain hygiene;
- broad localization refresh;
- semantic/hybrid/vector Reader runtime or comparator execution.

## Non-claims

Crystal does not claim awarded funding, approved budget, universal truth, zero
hallucinations, legal/security/GDPR certification, active PostgreSQL/pgvector Reader runtime,
a dedicated/full autonomous Reader, semantic understanding, automatic claim identity,
automatic evidence admission or contradiction resolution.

See [baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md),
[funding use plan](./grants/funding-use-plan.md),
[RC-9 architecture/result](./architecture/READER_RC9_LEXICAL_BASELINE.md), and
[current implementation status](./IMPLEMENTATION_STATUS.md).
