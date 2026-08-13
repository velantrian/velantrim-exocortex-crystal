# 🧪 Reader Retrieval Evaluation Surface v2 — Frozen Judged Retrieval Evidence

**Status:** FROZEN / RC-9 CONTROL REPRODUCED / NO MODEL COMPARATOR EXECUTED  
**Tracking issue:** #384  
**Pull request:** #385  
**Immutable starting checkpoint:** `main@e824556f304143cdb8403f44a7b020a528e63291`  
**Predecessor decision:** issue #382 / PR #383  
**Documentation impact:** `GITHUB_AND_NOTION`

## 1. Purpose

Evaluation Surface v2 strengthens Reader retrieval evidence **before** model selection. It does not
add a retrieval runtime. The milestone freezes a fully judged synthetic surface, reproduces the
existing RC-9 BM25 control unchanged, and freezes an additional future-comparator admission gate
before any model-backed result is observed.

```text
RC-9 lexical baseline
        ↓
historical RC-10 frozen screen
        ↓
post-RC-10 reassessment
        ↓
Evaluation Surface v2 frozen
        ↓
RC-9 reproduced unchanged
        ↓
future comparator gate frozen
        ↓
STOP — no model comparator executed
```

Historical RC-8, RC-9 and RC-10 artifacts remain byte-identical.

## 2. Review corrections completed before freeze

The first PR drafts were **not** treated as frozen evidence. Codex review identified material
evaluation-contract defects and they were corrected before any merge:

1. provisional `c01/c02/...` IDs encoded qrel position and could influence deterministic RC-9
   tie-breaking;
2. `v2-q04` incorrectly treated an incompatible refund-scope statement as a hard negative;
3. `v2-q23` initially labelled an unconditional cache-clear rule as merely related instead of an
   incompatible-scope contradiction candidate;
4. provisional Precision@5 divided by returned candidates, allowing unfilled ranks to inflate it;
5. the runner checked component hashes but not the composite surface identity;
6. the machine gate omitted explicit index-identity and privacy-review requirements.

Final candidate IDs are label-independent and content-derived:

```text
v2-c- + first16(sha256(pool_id + NUL + proposition))
```

Candidate rows are sorted by `(pool_id, candidate_id)`, not qrel class. The qrel class is
evaluation metadata only and does not participate in retrieval identity.

For `v2-q04`, the incompatible statement “Customers may request a refund at any time after
delivery.” is `USEFUL_CANDIDATE / POSSIBLE_CONTRADICTION`. For `v2-q23`, the unconditional
statement “The cache is cleared whenever the user logs out.” is also
`USEFUL_CANDIDATE / POSSIBLE_CONTRADICTION` relative to the secure-mode condition. These review
class corrections do not change the useful/hard/neutral counts or RC-9 ranking metrics; they correct
semantic consistency of the frozen qrels. The required 2 useful / 2 hard-negative / 2 neutral
design remains intact.

## 3. Frozen surface identity

Machine-readable manifest: `eval/reader_retrieval_eval_v2_manifest.json`.

Composite surface digest:

```text
753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

The digest is SHA-256 over the ordered identities of:

| Artifact | Rows | SHA-256 |
|---|---:|---|
| queries | 24 | `13dc860a364949932b23ed006eedf9416c345e1b00718c1beaa276f49fb64f47` |
| candidates | 144 | `86d4db3bfea311e855889d4b14ac33b1b01010a773763710e387a3823d77d108` |
| qrels | 144 | `34f2a30a4b6f7cdb058537920781683819d88d908e95905c41569aef06e26a11` |

Construction:

```text
sha256(
  "queries:<sha256>\n"
  "candidates:<sha256>\n"
  "qrels:<sha256>\n"
)
```

The runner recomputes both every component SHA-256 and the composite digest and rejects any
mismatch.

## 4. Fully judged design

The final v2 surface contains:

- 24 queries;
- 12 primary strata, exactly 2 queries each;
- 6 candidates in every query pool;
- exactly 2 useful, 2 hard-negative and 2 neutral-decoy judgments per query;
- 48 useful judgments;
- 48 hard-negative judgments;
- 48 neutral-decoy judgments;
- 144/144 explicitly judged candidate-query pairs;
- judgment coverage = `1.0`;
- K = `5`.

Primary strata:

1. cross-lingual paraphrase;
2. low-lexical-overlap paraphrase;
3. negation / polarity;
4. modality / scope;
5. quantifier / scope;
6. temporal / version;
7. jurisdiction / context;
8. attribution / quotation;
9. units / thresholds;
10. homonym / entity collision;
11. boilerplate / same-topic;
12. conditional / exception.

The corpus remains bounded and synthetic. It is stronger retrieval-comparison evidence than the
RC-8 pair fixture, but it is not production-distribution evidence and is not a semantic-truth
benchmark.

## 5. Qrel semantics

Every pool candidate has exactly one explicit qrel:

```text
USEFUL_CANDIDATE
HARD_NEGATIVE
NEUTRAL_DECOY
```

Useful candidates use one of:

- `SAME_PROPOSITION_CANDIDATE`;
- `PARAPHRASE_CANDIDATE`;
- `RELATED_CLAIM`;
- `POSSIBLE_CONTRADICTION`.

Hard negatives use `SAME_TOPIC` or `MERELY_SIMILAR`.

```text
qrel relevance       != evidence
retrieval usefulness != proposition identity
possible contradiction candidate != adjudicated contradiction
hard negative         != truth verdict
```

## 6. RC-9 control reproduction

Runner: `scripts/bench_reader_eval_v2_lexical.py`.  
Control: `eval/reader_retrieval_eval_v2_rc9_control.json`.

The runner imports the existing
`core.reader_lexical_discovery.ReaderLexicalIndex` and `RETRIEVAL_METHOD`.
**`core/**` remains unchanged.** The control is still
`reader_rc9_bm25_lexical_v1`: deterministic, stdlib-only, local and in-memory.

Final K=5 result:

| Metric | Result |
|---|---:|
| Useful judgments | 48 |
| Useful hits@5 | **42 / 48** |
| Useful Recall@5 | **0.875000** |
| Precision@5, fixed K slots | **0.350000** |
| Returned candidates | 118 |
| Judged precision over returned | **0.355932** |
| MRR | **0.857639** |
| Hard-negative judgments | 48 |
| Hard-negative hits@5 | **38 / 48** |
| Hard-negative hit rate@5 | **0.791667** |
| Any-useful-query rate@5 | **1.000000** |
| All-useful-query rate@5 | **0.750000** |
| Neutral-decoy hits | 38 |

RC-9 misses six explicit useful candidates on v2:

```text
v2-c-0a8ace12cae2f46b
v2-c-276b3efe332a9a8e
v2-c-2dbbcb4d5fd9024b
v2-c-33a2bceca3914a17
v2-c-bd24e316a3f799aa
v2-c-ea4d49c11eccb857
```

Classification:

```text
LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS
```

This is retrieval evidence only.

## 7. Metric interpretation

`Useful Recall@5` = retrieved explicit useful qrels / all explicit useful qrels.

`Precision@5` uses the fixed `query_count × K` slot denominator. For v2:

```text
42 / (24 × 5) = 0.350000
```

This prevents a retriever from improving Precision@5 merely by returning fewer than K results.

`Judged precision over returned` is also reported because all returned candidates are explicitly
judged:

```text
42 / 118 = 0.355932
```

It is a diagnostic, not a replacement for fixed-slot Precision@5 and not a gate by itself.

`MRR` uses the first useful candidate per query. `Hard-negative hit rate@5` counts explicit
`SAME_TOPIC` / `MERELY_SIMILAR` qrels retrieved. `Any-useful-query` and `All-useful-query`
measure query-level useful coverage.

No retrieval metric is truth, identity, evidence or adjudication quality.

## 8. Per-stratum evidence

| Stratum | Useful recall@5 | Hard-negative rate@5 |
|---|---:|---:|
| attribution / quotation | 1.000000 | 0.750000 |
| boilerplate / same-topic | 0.750000 | 1.000000 |
| conditional / exception | 1.000000 | 0.750000 |
| cross-lingual paraphrase | 0.500000 | 0.750000 |
| homonym / entity collision | 1.000000 | 0.500000 |
| jurisdiction / context | 1.000000 | 0.750000 |
| low lexical overlap | 0.500000 | 1.000000 |
| modality / scope | 1.000000 | 0.750000 |
| negation / polarity | 1.000000 | 0.500000 |
| quantifier / scope | 0.750000 | 1.000000 |
| temporal / version | 1.000000 | 1.000000 |
| units / thresholds | 1.000000 | 0.750000 |

This makes the limitation multi-stratum and prevents one aggregate metric from hiding a
cross-lingual or low-overlap failure.

## 9. Work bound

```text
query pools                 = 24
index records total         = 144
max record comparisons      = 144
storage                     = in_memory
network calls               = 0
mandatory third-party deps  = 0
```

This is fixture-scale evaluation evidence, not a production latency/scaling result.

## 10. Historical evidence remains immutable

The milestone does not edit:

- RC-8 corpus Git blob `4be317549d7a8eae9d69f9fa208d07d8855779a4`;
- RC-9 baseline Git blob `7ffbc86d713b7be89d393fe56c2d160b9dee98dc`;
- RC-10 preregistration Git blob `70758595c220820d456a2ea4db68589289995294`.

Regression tests recompute those Git blob identities.

## 11. Future comparator gate frozen before results

Machine-readable gate:
`eval/reader_retrieval_eval_v2_future_comparator_gate.json`.

A future comparator must first pass the unchanged historical RC-10 screen and then the v2 gate.
The v2 minimum includes:

- retain all 42 useful candidate IDs already retrieved by RC-9 on v2;
- recover at least 4 of the 6 v2 useful misses;
- useful hits >= 46/48;
- Useful Recall@5 >= `0.958333`;
- MRR >= `0.857639`;
- hard-negative hits <= 24/48;
- hard-negative hit rate@5 <= `0.500000`;
- any-useful-query rate@5 = `1.000000`;
- all-useful-query rate@5 >= `0.916667`;
- per-stratum useful Recall@5 >= `0.750000`;
- per-stratum hard-negative hit rate@5 <= `0.500000`;
- judgment coverage = `1.0`;
- report fixed-slot Precision@5 and judged precision-over-returned;
- zero authority violations.

## 12. Comparator admission requirements

Any future separately authorized comparator must declare:

- exact comparator/backend identity;
- exact model identity when model-backed;
- immutable model revision or checksum;
- exact dependency versions;
- explicit no-index declaration or exact index identity;
- privacy review;
- preloaded local assets for a qualifying model run;
- no `auto` backend;
- zero query-time network calls;
- zero external Reader source-text transmission;
- repeatability observation;
- resource observation;
- deterministic lexical fallback for any later runtime proposal.

Threshold changes after future results are forbidden.

Passing both screens means only:

```text
ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY
comparison pass != runtime authorization
```

No model-backed comparator is executed in Evaluation Surface v2.

## 13. Authority firewall

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

No qrel, score, rank or gate may mutate evidence, Canon, ESM, Guardian, TruthGate, confidence or
contradiction disposition.

## 14. Storage / dependency boundary

Unchanged:

```text
SQLite ordinary active local-first
PostgreSQL/pgvector inactive active=false
Reader FTS not implemented
Reader semantic/vector runtime not implemented
ANN/vector DB not implemented
automatic backend switching absent
```

No model or runtime dependency is added.

## 15. Grant boundary

NLnet remains `submitted / under review / not awarded`; approximately €50,000 remains planning
context only. If completed before a funding agreement, Evaluation Surface v2 is existing
pre-agreement research/evaluation history and cannot later be relabelled as newly funded runtime
delivery.

## 16. Position after this milestone

```text
RC-1..RC-7 bounded Reader layers           implemented
RC-8 retrieval architecture decision       complete
RC-9 lexical discovery baseline            implemented / measured
RC-10 reuse + comparison preregistration   complete / no comparator
post-RC-10 reassessment                    complete
Evaluation Surface v2                      FROZEN / RC-9 reproduced
model-backed comparator execution          NOT STARTED
semantic/hybrid/vector Reader runtime      NOT STARTED
dedicated_reader_core                      false
```

## 17. Stop boundary

After exact-head CI, review-thread cleanup, guarded merge, signed exact post-merge CI, Notion 3/3
synchronization/read-back, issue #384 completion evidence and final live audit: **STOP**.

Do not automatically execute a model-backed comparator, add embeddings/ANN/vector DB, implement
Reader FTS, activate PostgreSQL/pgvector, mutate authority, implement #155/#165/#214 or perform a
broad localization refresh.
