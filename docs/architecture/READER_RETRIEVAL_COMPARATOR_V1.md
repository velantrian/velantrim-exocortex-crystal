# Reader Retrieval Comparator Evaluation v1

Status: **COMPLETED — FROZEN GATE FAIL**  
Tracking issue: #386  
Audited start: `main@f685a0b520530e67dd3fd02dd3ac75f5d4f0bd28`  
Evaluation Surface v2 SHA-256: `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`

## 1. Decision

The post-v2 architecture reassessment selected exactly one bounded experiment: a pinned,
offline multilingual sentence-embedding comparator measured against both the historical RC-10
screen and the frozen Evaluation Surface v2 gate.

This was selected because v2 had already shown two different retrieval gaps:

- six useful lexical misses, concentrated in cross-lingual and low-overlap cases plus one
  quantifier and one boilerplate case; and
- hard-negative pressure above the future gate in ten of twelve strata.

The v2 work bound was only 144 in-memory comparisons, with no measured latency, memory or
throughput blocker. Therefore FTS, ANN and vector-database infrastructure would have addressed
an unmeasured scaling problem rather than the observed relevance/discrimination problem.
Existing hashing and trigram controls remain lexical feature systems and do not supply a
cross-lingual semantic representation.

## 2. Frozen comparator identity

The identity was preregistered before any comparator result was observed in
`eval/reader_retrieval_comparator_v1_preregistration.json`:

- backend: `sentence-transformers`;
- package: `sentence-transformers==5.7.0`;
- transformer package: `transformers==5.14.1`;
- model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`;
- immutable model revision: `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`;
- `model.safetensors` SHA-256:
  `eaa086f0ffee582aeb45b36e34cdd1fe2d6de2bef61f8a559a1bbc9bd955917b`;
- CPU cosine ranking;
- exact candidate-pool scoring, `K=5`;
- `NO_INDEX_EXACT_POOL_SCORING`;
- no `auto` backend selection.

No threshold was changed after observing the result.

## 3. Qualifying execution envelope

Qualifying GitHub Actions run: `31728139139`  
Execution head: `3edd2064a6101b0c70f4fd37f5071b10a09f8c86`  
Qualifying runner blob: `aefd8ac098501a85be5d4e58cf5a6b1fc9194017`  
Raw result SHA-256: `df3ffc693d2139ef79f151fcb09aa6bf687e78b5cb3ea616886f43df03f615e9`

The execution deliberately separated model acquisition from evaluation:

1. exact package versions were installed and the complete resolved dependency freeze was
   printed to the immutable workflow log;
2. the model snapshot was downloaded at the preregistered immutable revision;
3. the model weights SHA-256 was checked before evaluation;
4. the qualifying comparator ran under a Linux network namespace (`unshare --net`) with
   `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`;
5. only the public synthetic RC-8 and v2 evaluation fixtures were processed;
6. no Reader source text was transmitted to an external service;
7. the full ranking experiment was executed twice and both ranking fingerprints were exactly
   `d0b6d8ea7dd21d50dddfa9dce351c88a5993f4430115523c13fae55cf6da9235`.

Resolved dependency freeze SHA-256:
`9a2902d1b7d5b7ca5b5105be46d1a1151fddf683e0ed67b078a09c948b3f4bd9`.
The complete freeze remains in the qualifying workflow log. This experiment does not claim
that the unresolved repository-wide supply-chain hardening backlog in #214 is complete.

Observed two-pass wall time including model load was `15.731751 s` on the hosted runner.
Maximum RSS rose to `1,826,604 KiB`. These are bounded research observations, not production
SLOs or capacity claims.

## 4. Result

### Historical RC-10 screen

| Metric | Frozen requirement | Comparator | Result |
|---|---:|---:|---|
| useful hits | 16/16 | 16/16 | PASS |
| Recall@5 | 1.0 | 1.0 | PASS |
| recover `rc8-004` | required | recovered | PASS |
| MRR | >= 0.895833 | 1.0 | PASS |
| hard-negative hits | <= 2/4 | 4/4 | **FAIL** |
| hard-negative rate@5 | <= 0.50 | 1.0 | **FAIL** |

Historical RC-10 gate: **FAIL**.

### Evaluation Surface v2

| Metric | RC-9 lexical control | Comparator | Frozen gate |
|---|---:|---:|---:|
| useful hits | 42/48 | **48/48** | >= 46/48 |
| useful Recall@5 | 0.875000 | **1.000000** | >= 0.958333 |
| MRR | 0.857639 | **1.000000** | >= 0.857639 |
| hard-negative hits | 38/48 | **41/48** | <= 24/48 |
| hard-negative rate@5 | 0.791667 | **0.854167** | <= 0.500000 |
| any-useful-query rate | 1.000000 | 1.000000 | 1.000000 |
| all-useful-query rate | 0.750000 | **1.000000** | >= 0.916667 |
| judgment coverage | 1.0 | 1.0 | 1.0 |

All six RC-9 v2 useful misses were recovered, including both cross-lingual and both
low-lexical-overlap misses. Useful Recall@5 was `1.0` in all twelve primary strata.

However hard-negative discrimination did not improve. It became worse in aggregate:
`38/48 -> 41/48`. Eleven of twelve strata exceeded the required hard-negative rate `<= 0.50`;
only `units_thresholds` reached exactly `0.50`.

Evaluation Surface v2 gate: **FAIL**.

Overall frozen comparator gate: **FAIL**.

Machine-readable frozen evidence is in
`eval/reader_retrieval_comparator_v1_result.json`.

## 5. Architectural interpretation

Classification:

`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`

The experiment answers an important question cleanly. A generic multilingual sentence
embedding is sufficient to remove the observed lexical recall ceiling on this frozen surface,
but semantic similarity alone is not sufficient to distinguish useful candidates from
nearby hard negatives involving negation, quantifiers, modality, jurisdiction, attribution,
boilerplate, entity collision and other proposition-level distinctions.

Therefore the result does **not** support replacing RC-9 with this model, adding it as a
Reader runtime backend, or building vector infrastructure around it. It also does not justify
post-result threshold tuning or trying another model inside this milestone.

The correct information gain is narrower:

```text
lexical control                 -> broad recall, weak hard-negative discrimination
multilingual semantic similarity -> complete useful recall, still weaker discrimination

therefore:
semantic recall capability != proposition-level discrimination capability
```

A future architecture reassessment may investigate whether a separate bounded discriminator,
reranker or structured proposition-aware comparison is justified. That is a new decision and
is not authorized here.

## 6. Authority firewall

The comparator has zero epistemic authority:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

No Canon, ESM, evidence, confidence, contradiction-winner, Guardian or TruthGate state was
mutated. No Reader semantic/hybrid runtime, FTS, ANN, vector database or PostgreSQL/pgvector
activation was implemented.

## 7. Grant and scope truth

This is existing pre-agreement evaluation/research history. It is not a funded runtime
deliverable and does not imply an NLnet award, approved budget or paid implementation.

The negative gate result is useful grant evidence precisely because it prevents an unsupported
capability claim: Crystal now has direct evidence that a strong generic multilingual semantic
retriever can recover lexical misses while still failing the project's harder discrimination
contract.

## 8. Closure boundary

This milestone closes by recording the frozen FAIL result, validating the repository at the
exact PR head, completing review, guarded merge, post-merge CI and Notion synchronization.
After closure: **STOP**.

Do not automatically start another model comparator, reranker, semantic Reader runtime, FTS,
ANN/vector DB, pgvector activation, #155, #165 or #214. Any follow-up requires a fresh live
architecture reassessment and a separate bounded milestone.
