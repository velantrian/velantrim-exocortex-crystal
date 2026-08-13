# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It does not replace Git history, issues, pull requests, `CHANGELOG.md` or Notion.

## 2026-08-13 — Reader Retrieval Evaluation Surface v2 (#384 / PR #385)

- Live starting point: signed `main@e824556f304143cdb8403f44a7b020a528e63291`, signature `verified=true` / `reason=valid`, push CI `31670811115` 9/9.
- Scope is evaluation/research only: no `core/**`, model dependency/download, semantic/hybrid comparator execution, FTS/ANN/vector runtime, PostgreSQL/pgvector activation or authority change.
- Surface: 24 queries × 6 candidates; 12 primary strata ×2; 144/144 explicit qrels; exactly 2 useful + 2 hard-negative + 2 neutral judgments per query; K=5.
- Codex review found material pre-freeze defects and they were corrected before merge: qrel-position leakage through candidate IDs; incompatible refund-scope and cache-scope review-class inconsistencies; Precision@5 rewarding unfilled ranks; unverified composite surface digest; missing index-identity/privacy requirements; stale agent/status compatibility markers.
- Candidate identity is content-derived and **label-independent**: `v2-c- + first16(sha256(pool_id + NUL + proposition))`; candidate rows sort by `(pool_id, candidate_id)`, not qrel class.
- `v2-q04` “refund at any time after delivery” is `USEFUL_CANDIDATE / POSSIBLE_CONTRADICTION`.
- `v2-q23` “cache is cleared whenever the user logs out” is `USEFUL_CANDIDATE / POSSIBLE_CONTRADICTION` relative to the secure-mode condition. This second reclassification changes qrel/surface identity but not RC-9 ranking metrics.
- Final surface SHA-256: `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.
- Component SHA-256: queries `13dc860a364949932b23ed006eedf9416c345e1b00718c1beaa276f49fb64f47`; candidates `86d4db3bfea311e855889d4b14ac33b1b01010a773763710e387a3823d77d108`; qrels `34f2a30a4b6f7cdb058537920781683819d88d908e95905c41569aef06e26a11`.
- Unchanged RC-9 final v2 control at K=5: 42/48 useful; Recall `0.875000`; fixed-slot Precision `0.350000`; judged precision-over-returned `0.355932`; MRR `0.857639`; hard negatives 38/48 (`0.791667`); any-useful-query `1.000000`; all-useful-query `0.750000`.
- Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`. These are retrieval measurements, not semantic truth, identity or evidence-admission accuracy.
- Future comparator gate remains pre-result and additive to the unchanged historical RC-10 screen. It requires exact backend/model/dependency/index identity or explicit no-index, privacy review, no `auto`, no query-time network, no external source-text transmission, repeatability/resource observation and zero authority violations.
- Passing both gates means only `ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY`; `comparison pass != runtime authorization`.
- Historical RC-8/RC-9/RC-10 artifacts remain byte-identical. Documentation impact: `GITHUB_AND_NOTION`; only the three existing Crystal Notion pages may be synchronized after guarded merge + signed main + green exact post-merge CI.
- Stop after #384 completion. A **model-backed comparator** is a separate future milestone.

## 2026-08-13 — Post-RC-10 reassessment (#382 / PR #383)

- Guarded squash merge produced signed `main@e824556f304143cdb8403f44a7b020a528e63291`; post-merge CI `31670811115` was 9/9 successful.
- Issue #377 was closed completed as stale RC-10 preregistration bookkeeping only.
- Decision: `measured retrieval-quality gap != measured scaling gap`; FTS/ANN/server infrastructure was not justified as the next Reader mechanism.
- Selected next bounded milestone: stronger pre-frozen Evaluation Surface v2 with unchanged RC-9 reproduction before any model-backed comparator result.

## 2026-08-12 — Reader RC-10 preregistration (#377 / PR #378)

RC-10 froze a future comparison gate before results and explicitly executed no semantic/hybrid comparator. Passing means stronger evaluation / architecture-review eligibility only.

## 2026-08-12 — Reader RC-9 lexical discovery (#375 / PR #376)

Signed merge `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`; exact-head CI `31593097846` and post-merge CI `31594027040` were 9/9. Historical K=5 result: Recall `0.937500`, Precision `0.187500`, MRR `0.895833`, paired hard-negative rate `1.000000`, 15/16 useful hits and 4/4 hard-negative hits. Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## Historical retained evidence

Earlier RC-0..RC-8, storage, localization and grant-reconciliation entries remain available in Git history and their signed/CI evidence remains preserved in status and architecture records.
