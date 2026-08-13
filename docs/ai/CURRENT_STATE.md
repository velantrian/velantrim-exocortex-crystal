# Crystal AI Current State

**Status date:** 2026-08-13  
**Authoritative merged main at this reconciliation:** `1ca31f92dfc0818a07b6a33560799c962b6e7d9f`  
**Merge signature:** verified / valid  
**Rule:** re-resolve live GitHub before treating this dated checkpoint as evergreen truth.

GitHub merged `main`, executable tests and exact CI are authoritative for implementation truth.

## Current Reader position

```text
RC-1 through RC-7 bounded Reader layers   MERGED
RC-9 lexical discovery baseline           COMPLETE
Evaluation Surface v2                     COMPLETE / FROZEN
Comparator v1                             COMPLETE / FROZEN GATE FAIL
dedicated_reader_core                     false
semantic/hybrid Reader runtime            NOT AUTHORIZED
Reader FTS / ANN / vector DB               NOT AUTHORIZED
PostgreSQL/pgvector Reader activation      NOT AUTHORIZED
```

## Comparator v1 — current merged evidence

Tracking issue: `#386`  
Merged result: PR `#387`  
Frozen result artifact: `eval/reader_retrieval_comparator_v1_result.json`  
Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`

The pinned offline multilingual sentence-embedding comparator used:

```text
model:     sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
revision:  e8f8c211226b894fcb81acc59f3b34ba3efd5f42
device:    CPU
similarity: cosine
K:         5
index:     NO_INDEX_EXACT_POOL_SCORING
```

Qualifying execution: GitHub Actions run `31728139139`.

### Historical RC-10 screen

```text
useful hits:          16 / 16
Recall@5:             1.000000
MRR:                  1.000000
hard-negative hits:    4 / 4
hard-negative rate:    1.000000
frozen gate:          FAIL
```

### Evaluation Surface v2

RC-9 lexical control:

```text
useful hits:          42 / 48
Recall@5:             0.875000
MRR:                  0.857639
hard-negative hits:   38 / 48
hard-negative rate:    0.791667
```

Comparator v1:

```text
useful hits:          48 / 48
Recall@5:             1.000000
MRR:                  1.000000
hard-negative hits:   41 / 48
hard-negative rate:    0.854167
```

All six RC-9 v2 useful misses were recovered, but hard-negative discrimination did not improve and was worse in aggregate. Both frozen discrimination gates therefore failed. No threshold was changed after observing the result.

## Authority firewall

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

Comparator v1 is evaluation evidence only. It did not authorize Reader semantic/hybrid runtime, FTS, ANN/vector DB, PostgreSQL/pgvector activation, automatic identity/adjudication, evidence admission, Guardian/TruthGate mutation or Canon mutation.

## Current open research surface

At this reconciliation, PR `#389` is open and evaluates a separately preregistered NLI neutral-filter experiment. It is **not merged current truth** and its eventual result must not be inferred here before merge/closure evidence. Its changed files are separate from this AI documentation reconciliation.

## Machine truth

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

Machine-readable implementation truth remains in `docs/status/implementation-manifest.json`; evaluation result truth for Comparator v1 is in `eval/reader_retrieval_comparator_v1_result.json`.

## Grant / backlog boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning context only. Issues `#155`, `#165` and `#214` remain separate scopes.

## Documentation rule

Use `docs/ai/project_manifest.json` for machine navigation and `docs/ai/DOCUMENTATION_STANDARD.md` for human/AI maintenance semantics. `overview != current state != evidence != history`.
