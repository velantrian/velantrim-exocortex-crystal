<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth. Resolve live GitHub and `docs/STATUS.md` before treating retained signed checkpoints below as the current repository head.

**Retained signed architecture checkpoint (architecture evidence; not live HEAD):** `main@76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — PR #392; post-merge CI `31771677028` 9/9  
**Historical signed RC-7 merge checkpoint:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — implementation PR #372; RC-7 post-merge CI `31572918731`; later Issue #373 / PR #374 documentation closure  
**Signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376; post-merge CI `31594027040`; retained RC-10 architecture decision #377  
**Grant reconciliation:** issue #379 / PR #380 / PR #381 completed  
**Comparator v1:** issue #386 / PR #387 completed — frozen gate FAIL  
**NLI neutral-filter v1:** issue #388 / PR #389 completed — frozen gate FAIL  
**RRTIC-v1:** issue #391 / PR #392 completed — architecture contract only  
**Legacy exact-normalized dedupe:** issue #165 / PR #431 completed — derived compatibility index only; no re-key or semantic matching  
**Grant status:** submitted / under review / not awarded

## ✅ Delivered Reader implementation baseline

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

- **RC-5 — relation candidates** — `core/reader_relations.py`; no admission/resolution authority.
- **RC-6 — bounded long context** — deterministic working sets + caller-supplied summaries.
- **RC-7 — bounded cross-document candidate links** — exact two-sided provenance; no automatic identity.
- **RC-8 — retrieval architecture decision** — architecture/research complete.
- **RC-9 — deterministic lexical candidate discovery + benchmark** — PRE-ADMISSION BM25 inspection baseline.

RC-1 through RC-7 and RC-9 are implemented bounded capabilities. RC-8 is architecture/research. Later Comparator/NLI/RRTIC work is evaluation/architecture evidence, not runtime feature expansion.

Historical RC-9 K=5 evidence remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15 / 16`, hard-negative hits `4 / 4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## 🔒 Retained authority vocabulary

```text
retrieval match != evidence
similarity != identity
NLI label != proposition identity
NLI contradiction != contradiction adjudication
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
repetition != corroboration
cross-document candidate != Canon relation
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
evaluation pass != runtime authorization
```

## ✅ Post-RC-10 reassessment and Evaluation Surface v2

Issue #382 / PR #383 established:

```text
measured retrieval-quality gap != measured scaling gap
```

SQLite FTS, ANN/vector DB and server infrastructure were not selected as the next Reader mechanism. RC-9 remained the deterministic control/fallback.

**Reader Retrieval Evaluation Surface v2** (#384/#385) then froze a fully judged surface:

```text
24 queries
12 strata × 2 queries
6 candidates/query
144/144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

RC-9 on v2: useful hits `42/48`, Recall@5 `0.875000`, Precision@5 `0.350000`, judged precision-over-returned `0.355932`, MRR `0.857639`, hard-negative hits `38/48`, hard-negative rate `0.791667`; classification `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## 🧪 Comparator v1 — completed / frozen FAIL

The preregistered multilingual semantic comparator recovered all useful v2 candidates (`48/48`, Recall@5 `1.0`, MRR `1.0`) but surfaced `41/48` hard negatives and all `4/4` historical RC-10 hard negatives.

```text
SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED
```

Conclusion: semantic similarity removed the measured lexical recall ceiling on this frozen surface but did not supply proposition-level discrimination. No semantic Reader runtime was authorized.

## 🧪 NLI neutral-filter v1 — completed / frozen FAIL

Bidirectional NLI filtering reduced v2 hard-negative hits to `18/48` and historical hard negatives to `1/4`, but useful recall regressed to `46/48` on v2 and `15/16` historically. The no-recall-loss overlay failed.

```text
NLI_NEUTRAL_FILTER_GATE_FAILED
```

Conclusion: the NLI signal is diagnostically useful, but the frozen filter is not admissible as the next Reader retrieval stage.

## 🧬 RRTIC-v1 — completed architecture contract

The post-NLI reassessment selected a **CONTRACT_FIRST** direction and classified the missing capability as a **relation-contract mismatch**.

RRTIC-v1 freezes:

- 6 suspicion-only relation families;
- 10 qualifier dimensions;
- qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`;
- explicit false authority flags for identity, evidence, adjudication and runtime authorization.

RRTIC-v1 has no accept/reject policy, reranking, model execution, new dependency, `core/**` runtime implementation or new performance claim. Existing RC-5 semantics remain unchanged.

```text
RRTIC diagnostic != RC-5 registered relation
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
runtime_authorization=false
```

## ⛔ Current roadmap gate

RRTIC-v1 is closed. **No next model, discriminator, reranker or Reader runtime implementation is automatically selected.**

Any future mechanism requires:

1. a separate bounded milestone;
2. explicit problem/hypothesis identity;
3. preregistration where evaluation is involved;
4. fresh validation design rather than tuning the frozen v2 surface;
5. explicit privacy/resource/dependency review;
6. authority review showing no evidence/identity/Canon shortcut.

This means “larger embedding model”, “better NLI”, CrossEncoder, LLM judge, FTS, ANN/vector DB and PostgreSQL/pgvector activation are **not roadmap commitments** merely because they are technically possible.

## 🗄️ Storage / backlog truth

```text
SQLite ordinary active local-first
PostgreSQL/pgvector inactive active=false
Reader FTS not implemented
Reader ANN/vector DB not implemented
automatic backend switching absent
legacy exact-normalized compatibility index implemented / derived / rebuildable
historical fact re-keying absent
semantic dedupe absent
```

Issue #165 is completed by the bounded compatibility-index implementation: historical `ing:*` rows can be matched by the same exact normalized claim identity used by current auto-ingest (NFC → trim → whitespace collapse → casefold), while already-current normalized IDs take precedence. Existing collisions are preserved rather than merged, future occurrences route deterministically, dry-run stays write-free, and full erasure removes the derived mapping. This is compatibility/recovery of exact identity only — not evidence, semantic identity inference or Canon authority.

The historical residual scopes #155, #165 and #214 are therefore all **CLOSED/completed** at this reconciliation checkpoint. #155 remains EPIS-001 architecture only; #214 remains bounded verification-reproducibility/security-hygiene history; #165 does not authorize semantic dedupe or historical re-keying. Their closure does not select another backlog item. Resolve live GitHub before selecting any next scope.

## 🌍 Localization boundary

The nine supported localized Reader-dependent public/detail packs are current at the starting checkpoint for this English reconciliation. This milestone intentionally changes **English authoritative/current-truth surfaces only**; it does not modify localized documentation or silently advance any locale source checkpoint. Any later translation parity update remains a separate explicit documentation task.

## 🎓 Grant boundary

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning context only. Work merged before an agreement is existing pre-agreement baseline/research history and cannot later be counted as newly funded delivery.

## Related documents

- [Reader RC-9 lexical baseline](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [Reader Retrieval Evaluation Surface v2](./docs/architecture/READER_RETRIEVAL_EVAL_V2.md)
- [RRTIC-v1 typed inspection contract](./docs/architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md)
- [Current status](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
