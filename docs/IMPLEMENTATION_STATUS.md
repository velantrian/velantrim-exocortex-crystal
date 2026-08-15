# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-15  
**Current signed architecture checkpoint:** `main@76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` / PR #392; post-merge CI `31771677028` — 9/9 SUCCESS  
**Historical RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372; post-merge CI `31572918731` — retained immutable cross-document Reader provenance  
**Signed RC-9 Reader implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`; retained RC-10 architecture decision #377  
**Post-RC-10 architecture reassessment:** Issue #382 / PR #383 — selected Evaluation Surface v2 before any further comparator execution  
**Latest completed model-backed evaluation:** NLI neutral-filter v1 / PR #389 — frozen gate FAIL  
**Current frozen architecture contract:** RRTIC-v1 / Issue #391 / PR #392 — no runtime authorization

## Implemented Reader capability truth

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core                  = false
```

Implemented Reader runtime/domain components:

| Capability | Status | Primary implementation |
|---|---|---|
| RC-1 source/session skeleton | **IMPLEMENTED** | `core/reader_core.py` |
| RC-2 structural map | **IMPLEMENTED** | `core/reader_structure.py` |
| RC-3 multi-pass mechanics | **IMPLEMENTED** | `core/reader_passes.py` |
| RC-4 proposition extraction contract/runtime | **IMPLEMENTED** | `core/reader_extraction.py` |
| RC-5 relation candidates | **IMPLEMENTED** | `core/reader_relations.py` |
| RC-6 bounded long-context strategy | **IMPLEMENTED** | `core/reader_long_context.py` |
| RC-7 explicit cross-document candidate links | **IMPLEMENTED** | `core/reader_cross_document.py` |
| Reader RC-9 lexical candidate discovery | **IMPLEMENTED** | `core/reader_lexical_discovery.py` |
| Dedicated/full autonomous Reader | **NOT IMPLEMENTED** | `dedicated_reader_core=false` |
| Semantic/hybrid Reader runtime | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| Reader FTS / ANN / vector DB | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| NLI runtime filter / CrossEncoder reranker | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| RRTIC runtime provider | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |

## Research/evaluation evidence is not implementation

The following repository milestones are real, completed work, but they are **not runtime features**:

| Evidence / contract | Result | Runtime meaning |
|---|---|---|
| RC-8 retrieval decision | architecture/research complete | selected deterministic lexical baseline first |
| Reader Retrieval Evaluation Surface v2 | frozen judged evaluation surface | no runtime added |
| Comparator v1 | `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` | semantic comparator rejected as runtime authorization |
| NLI neutral-filter v1 | `NLI_NEUTRAL_FILTER_GATE_FAILED` | filter rejected as Reader retrieval stage |
| RRTIC-v1 | frozen typed inspection architecture contract | no model/filter/reranker/provider added |

## RC-9 retained implementation evidence

Historical RC-9 K=5 evidence remains:

- Recall@5 `0.937500`;
- Precision@5 `0.187500`;
- MRR `0.895833`;
- paired hard-negative rate@5 `1.000000`;
- useful hits `15/16`;
- hard-negative hits `4/4`;
- classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

These are retrieval measurements, not semantic/adjudication accuracy.

## Reader Retrieval Evaluation Surface v2 — retained frozen surface

Final frozen v2 surface: 24 queries, 12 primary strata ×2, 6 candidates/query, 144/144 explicit qrels, judgment coverage `1.0`, K=5, composite SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.

Final unchanged RC-9 v2 control:

- useful hits **42 / 48**;
- Recall@5 **0.875000**;
- fixed-slot Precision@5 **0.350000**;
- judged precision-over-returned **0.355932**;
- MRR **0.857639**;
- hard-negative hits **38 / 48**;
- hard-negative rate@5 **0.791667**.

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## Comparator v1 result

Comparator v1 recovered `48/48` useful v2 candidates with Recall@5 `1.0` and MRR `1.0`, but also surfaced `41/48` hard negatives. Its historical RC-10 screen surfaced `4/4` hard negatives.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

No semantic/hybrid Reader runtime was authorized.

## NLI neutral-filter v1 result

The preregistered NLI neutral filter reduced v2 hard-negative hits to `18/48`, but useful hits regressed to `46/48`; historical useful hits regressed to `15/16`. The no-recall-loss overlay and frozen gates failed.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1 contract

RRTIC-v1 responds to the post-NLI **relation-contract mismatch** finding. It freezes six suspicion-only relation families and ten structural qualifier dimensions so a future discriminator can be evaluated against an explicit relation/qualifier contract rather than one scalar similarity score.

```text
relation families:
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN

qualifier states:
MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE
```

RRTIC-v1 does not filter, rerank, execute a model, establish identity, admit evidence, adjudicate contradictions, mutate Canon or auto-register RC-5 relations.

## Retained Reader authority firewall

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
evaluation pass != runtime authorization
```

PostgreSQL/pgvector remains `active=false`. SQLite ordinary local-first remains active.

## Current verification

Post-RRTIC CI `31771677028`: **9/9 SUCCESS**. Python 3.11: **2231 passed / 13 skipped / 0 failed**, 100% measured line coverage.

## Localization / grant / backlog

Localization parity is owned by `docs/TRANSLATION_STATUS.md`; localized checkpoint labels do not override current English implementation truth.

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning only.

Issues #155 and #165 remain separate open scopes and are not implemented by this workstream. Issue #214 was **completed and closed on 2026-08-14**; its fixture/PII/supply-chain hygiene work is retained as completed engineering history, not an open backlog item.

## Stop boundary

RRTIC-v1 is closed. No next model/discriminator/runtime milestone is implied. Any future mechanism requires separate authorization and fresh validation design. Completion of #214 grants no Reader runtime, evidence-admission or Canon authority.
