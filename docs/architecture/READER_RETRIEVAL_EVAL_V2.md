# 🧪 Reader Retrieval Evaluation Surface v2 — Frozen Judged Retrieval Evidence

**Status:** FROZEN / RC-9 CONTROL REPRODUCED / NO MODEL COMPARATOR EXECUTED  
**Tracking issue:** #384  
**Immutable starting checkpoint:** `main@e824556f304143cdb8403f44a7b020a528e63291`  
**Predecessor decision:** issue #382 / PR #383  
**Documentation impact:** `GITHUB_AND_NOTION`

## 1. Purpose

Evaluation Surface v2 reduces the next Reader architecture uncertainty **before** model selection.
It does not add a retrieval runtime. It freezes a stronger, fully judged synthetic evaluation
surface, reproduces the existing RC-9 BM25 control unchanged, and freezes an additional
future-comparator admission gate before any model-backed result is observed.

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

The historical RC-8 corpus, RC-9 artifact and RC-10 preregistration remain immutable.

## 2. Frozen surface identity

Machine-readable manifest: `eval/reader_retrieval_eval_v2_manifest.json`.

Surface digest:

```text
c5c134c6be6536bc27c6ea641d479777eaf617bbecfbda7a230817df000034de
```

The digest is SHA-256 over the ordered SHA-256 identities of:

- `eval/reader_retrieval_eval_v2_queries.jsonl`;
- `eval/reader_retrieval_eval_v2_candidates.jsonl`;
- `eval/reader_retrieval_eval_v2_qrels.jsonl`.

Exact component SHA-256 values:

| Artifact | Rows | SHA-256 |
|---|---:|---|
| queries | 24 | `13dc860a364949932b23ed006eedf9416c345e1b00718c1beaa276f49fb64f47` |
| candidates | 144 | `78ceff678e687f3153d59e2bcd181550a4135374cdadc84b260eabf8d370fc43` |
| qrels | 144 | `000c876d02451490e085f08e740772749f4029b63b4dd27b0a077a96f1c072cb` |

## 3. Judged design

The v2 surface has:

- 24 queries;
- 12 primary strata;
- exactly 2 queries per primary stratum;
- exactly 6 candidates per query pool;
- exactly 2 useful candidates per query;
- exactly 2 hard negatives per query;
- exactly 2 neutral decoys per query;
- 48 useful judgments;
- 48 hard-negative judgments;
- 48 neutral-decoy judgments;
- 144/144 candidate-query pool pairs explicitly judged;
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

The corpus is still synthetic and bounded. It is stronger than RC-8 for retrieval comparison,
but it is not production-distribution evidence and is not a semantic-truth benchmark.

## 4. Qrel semantics

Every candidate returned by the benchmark has an explicit judgment:

```text
USEFUL_CANDIDATE
HARD_NEGATIVE
NEUTRAL_DECOY
```

Useful candidates retain one of the Reader review classes:

- `SAME_PROPOSITION_CANDIDATE`;
- `PARAPHRASE_CANDIDATE`;
- `RELATED_CLAIM`;
- `POSSIBLE_CONTRADICTION`.

Hard negatives use:

- `SAME_TOPIC`;
- `MERELY_SIMILAR`.

A qrel is evaluation metadata only.

```text
qrel relevance != evidence
retrieval usefulness != proposition identity
hard negative != adjudicated contradiction
```

## 5. RC-9 control reproduction

Runner: `scripts/bench_reader_eval_v2_lexical.py`.  
Control artifact: `eval/reader_retrieval_eval_v2_rc9_control.json`.  
Control result is regression-tested against the frozen runner and qrels.

The runner imports the existing `core.reader_lexical_discovery.ReaderLexicalIndex` and
`RETRIEVAL_METHOD`. **`core/**` is unchanged.** The control remains
`reader_rc9_bm25_lexical_v1`, stdlib-only, local, deterministic and in-memory.

Frozen K=5 v2 result:

| Metric | Result |
|---|---:|
| Useful judgments | 48 |
| Useful hits@5 | **43 / 48** |
| Useful Recall@5 | **0.895833** |
| Returned candidates | 118 |
| Fully judged Precision@5 | **0.364407** |
| MRR | **0.829861** |
| Hard-negative judgments | 48 |
| Hard-negative hits@5 | **38 / 48** |
| Hard-negative hit rate@5 | **0.791667** |
| Any-useful-query rate@5 | **1.000000** |
| All-useful-query rate@5 | **0.791667** |
| Neutral-decoy hits | 37 |

RC-9 misses five explicit useful candidates on v2:

```text
v2-q01-c01
v2-q03-c02
v2-q04-c01
v2-q09-c01
v2-q22-c02
```

The stronger surface therefore exposes several lexical limits at once: cross-lingual mismatch,
low lexical overlap, quantifier phrasing and release-note paraphrase behavior, while hard
negatives remain frequent across multiple strata.

Classification:

```text
LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS
```

This is retrieval evidence, not semantic/adjudication accuracy.

## 6. Metric interpretation

`Useful Recall@5` is explicit useful qrels retrieved divided by all explicit useful qrels.

`Fully judged Precision@5` is useful returned candidates divided by all **actually returned**
candidates. Every returned candidate is explicitly judged; there is no implicit-negative
assumption about unpaired corpus records.

`MRR` uses the first useful candidate per query.

`Hard-negative hit rate@5` counts explicit `SAME_TOPIC` / `MERELY_SIMILAR` hard-negative
judgments retrieved in top-5.

`Any-useful-query rate@5` requires at least one useful candidate per query.

`All-useful-query rate@5` requires both useful candidates for a query.

No single retrieval metric is truth, identity or evidence quality.

## 7. Work bound

The control performs 24 independent fully judged pools with six candidates each:

```text
query pools                 = 24
index records total         = 144
max record comparisons      = 144
storage                     = in_memory
network calls               = 0
mandatory third-party deps  = 0
```

This work bound is evaluation-fixture scale. It does not establish a production latency or
corpus-scaling result.

## 8. Historical evidence remains immutable

The milestone does not edit:

- `eval/reader_rc8_retrieval_adversarial.jsonl`
  - Git blob `4be317549d7a8eae9d69f9fa208d07d8855779a4`;
- `eval/reader_rc9_lexical_baseline.json`
  - Git blob `7ffbc86d713b7be89d393fe56c2d160b9dee98dc`;
- `eval/reader_rc10_retrieval_comparison_preregistration.json`
  - Git blob `70758595c220820d456a2ea4db68589289995294`.

Regression tests compute the Git blob identity from bytes so historical evidence cannot silently
change while claiming the v2 milestone is additive.

## 9. Future comparator gate is frozen before results

Machine-readable preregistration:
`eval/reader_retrieval_eval_v2_future_comparator_gate.json`.

The gate is regression-tested as pre-result, non-authorizing policy.

A future comparator must first satisfy the unchanged historical RC-10 screen. It must also pass
the v2 gate:

- retain all 43 useful candidate IDs already retrieved by RC-9 on v2;
- recover at least 3 of RC-9's 5 v2 useful misses;
- useful hits >= 46/48;
- useful Recall@5 >= `0.958333`;
- MRR >= `0.829861`;
- hard-negative hits <= 24/48;
- hard-negative hit rate@5 <= `0.500000`;
- any-useful-query rate@5 = `1.000000`;
- all-useful-query rate@5 >= `0.916667`;
- per-stratum useful Recall@5 >= `0.750000`;
- per-stratum hard-negative hit rate@5 <= `0.500000`;
- judgment coverage = `1.0`;
- zero authority violations.

Fully judged precision remains a required report, but no single global precision floor is used
as a substitute for the explicit recall + hard-negative + per-stratum requirements.

## 10. Comparator admission requirements

Any future separately authorized model-backed run must declare:

- exact comparator/backend mode;
- exact model identity if model-backed;
- immutable model revision or checksum;
- exact dependency versions;
- exact index identity if an index exists;
- no `auto` backend;
- preloaded local assets for a qualifying model run;
- zero query-time network calls;
- zero external Reader source-text transmission;
- repeatability observation;
- privacy review;
- resource observation;
- deterministic lexical fallback for any later runtime proposal.

No such comparator is executed in Evaluation Surface v2.

## 11. Authority firewall

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

No qrel, benchmark score, future gate or retrieval ranking may mutate evidence, Canon, ESM,
Guardian, TruthGate, contradiction disposition or confidence.

## 12. Storage / dependency boundary

Unchanged:

```text
SQLite ordinary active local-first
PostgreSQL/pgvector inactive active=false
Reader FTS not implemented
Reader semantic/vector runtime not implemented
ANN/vector DB not implemented
automatic backend switching absent
```

No model or dependency is added by this milestone.

## 13. Grant boundary

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning
context only.

RC-1 through RC-9, PR #378, the post-RC-10 reassessment and Evaluation Surface v2 are existing
pre-agreement repository work if completed before a funding agreement. They cannot later be
relabelled as newly funded runtime delivery.

## 14. Position after this milestone

```text
RC-1..RC-7 bounded Reader layers           implemented
RC-8 retrieval architecture decision       complete
RC-9 lexical discovery baseline            implemented / measured
RC-10 reuse + comparison preregistration   complete / no comparator
post-RC-10 reassessment                    complete
Evaluation Surface v2                      FROZEN / RC-9 reproduced
model-backed comparator execution          NOT STARTED
semantic/hybrid Reader runtime             NOT STARTED
vector Reader runtime                      NOT STARTED
dedicated_reader_core                      false
```

## 15. Stop boundary

After exact-head CI, semantic review, guarded merge, signed exact post-merge CI, Notion 3/3
synchronization/read-back, issue #384 completion evidence and final live audit: **STOP**.

Do not automatically execute a model-backed comparator, add embeddings/ANN/vector DB, implement
Reader FTS, activate PostgreSQL/pgvector, mutate authority, implement #155/#165/#214 or perform a
broad localization refresh.
