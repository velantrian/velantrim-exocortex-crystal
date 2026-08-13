# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It is not
a replacement for Git history, issues, pull requests, `CHANGELOG.md` or Notion. Earlier detailed
entries remain available through Git history.

## 2026-08-13 — Reader Retrieval Evaluation Surface v2 (#384 / PR #385)

- Live starting point: signed `main@e824556f304143cdb8403f44a7b020a528e63291`, signature
  `verified=true` / `reason=valid`, exact push CI `31670811115` 9/9, open PRs 0 before #384.
- Scope is evaluation/research only: no `core/**`, model dependency/download, semantic/hybrid
  comparator execution, FTS/ANN/vector runtime, PostgreSQL/pgvector activation or authority change.
- Surface design remains 24 queries × 6 candidates, 12 primary strata ×2, with 144/144 explicit
  qrels and exactly 2 useful + 2 hard-negative + 2 neutral judgments per query.
- Codex review caught real pre-freeze evidence defects. They were fixed **before merge** rather
  than treated as wording issues: provisional candidate IDs leaked qrel position into deterministic
  tie-breaking; a refund-scope conflict was misjudged; Precision@5 rewarded unfilled ranks; the
  composite surface digest was not verified; machine admission requirements omitted index identity
  and privacy review.
- Final candidate identity is content-derived and **label-independent**:
  `v2-c- + first16(sha256(pool_id + NUL + proposition))`; candidate rows sort by
  `(pool_id, candidate_id)`, not qrel class.
- `v2-q04` now correctly treats “refund at any time after delivery” as a useful
  `POSSIBLE_CONTRADICTION`; a separate portal-return-label statement supplies the second
  same-topic hard negative while the 2/2/2 pool design is preserved.
- Final surface SHA-256: `7af2b1247e1c1c2590b6b2c830dd605da646989856b6c29cee18aac3e1f785e8`. Component hashes:
  queries `13dc860a364949932b23ed006eedf9416c345e1b00718c1beaa276f49fb64f47`, candidates `86d4db3bfea311e855889d4b14ac33b1b01010a773763710e387a3823d77d108`, qrels `7d774e376a793b1cbc3e735b3f9cd81d01a1d05468019e917346bcfe27c40f86`.
- Unchanged RC-9 final v2 control at K=5: 42/48 useful; Recall `0.875000`; fixed-slot Precision
  `0.350000`; fully judged precision-over-returned `0.355932`; MRR `0.857639`; hard negatives
  38/48 (`0.791667`); any-useful-query `1.000000`; all-useful-query `0.750000`.
- Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`. These are retrieval measurements,
  not semantic truth, identity, evidence or contradiction-adjudication accuracy.
- Future comparator gate is frozen before any model-backed result and remains additive to the
  unchanged historical RC-10 screen. It requires exact backend/model/dependency/index identity
  (or explicit no-index), privacy review, no `auto`, no query-time network, no external source-text
  transmission, repeatability/resource observation and zero authority violations.
- Passing both gates means only `ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY`;
  `comparison pass != runtime authorization`.
- Historical RC-8/RC-9/RC-10 artifacts remain byte-identical. Documentation impact:
  `GITHUB_AND_NOTION`; only the three existing Crystal Notion pages may be synchronized after
  guarded merge + signed main + green exact post-merge CI.
- Stop after #384 completion. A **model-backed comparator** is a separate future milestone.

## 2026-08-13 — Post-RC-10 evaluation adequacy / next-milestone reassessment (#382 / PR #383)

- Guarded squash merge produced signed
  `main@e824556f304143cdb8403f44a7b020a528e63291`; post-merge CI `31670811115` was 9/9 successful.
- Residual issue #377 was closed completed as stale RC-10 preregistration bookkeeping only.
- Decision: `measured retrieval-quality gap != measured scaling gap`; FTS/ANN/server infrastructure
  was not justified as the next mechanism.
- Selected next bounded milestone: stronger pre-frozen Reader Retrieval Evaluation Surface v2,
  with unchanged RC-9 reproduction before any model-backed comparator result.
- No runtime/model/storage/authority expansion was added.

## 2026-08-12 — Reader RC-10 existing retrieval reuse compatibility + preregistration (#377 / PR #378)

- Reuse audit found admitted-memory hashing/trigram/optional SentenceTransformer retrieval,
  bounded legacy lexical retrieval and pure stdlib RRF, but these belong to a different authority
  lifecycle from PRE-ADMISSION Reader artifacts.
- RC-10 froze a future comparison gate before results and explicitly executed no semantic/hybrid
  comparator.
- Historical screen: retain all 15 RC-9 useful hits, recover `rc8-004` to 16/16, MRR >=0.895833,
  hard-negative hits <=2/4, zero authority violations, exact backend identity, no query-time
  network and no external Reader source-text transmission.
- Passing means stronger evaluation / architecture-review eligibility only.

## 2026-08-12 — Reader RC-9 deterministic lexical candidate discovery (#375 / PR #376)

- Signed merge `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`; exact-head CI `31593097846` and
  post-merge CI `31594027040` were both 9/9 successful.
- Added stdlib-only `core/reader_lexical_discovery.py` plus benchmark runner.
- Frozen historical K=5 result: Recall `0.937500`, Precision `0.187500`, MRR `0.895833`,
  paired hard-negative rate `1.000000`, 15/16 useful hits and 4/4 hard-negative hits.
- Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.
- No semantic/vector authorization follows from the measured lexical gap.

## 2026-08-12 — Reader RC-8 post-RC-7 retrieval architecture decision (#373 / PR #374)

- Identified candidate discovery across a Reader corpus as the missing capability and separated
  discovery, identity review and downstream admission.
- Added the 20-case adversarial RC-8 fixture.
- Decision: deterministic lexical candidate discovery first; semantic/hybrid/vector work requires
  separately authorized pre-registered measured comparison.
- Authority firewall retained:
  `retrieval match != evidence`, `similarity != identity`,
  `candidate discovery != candidate adjudication`.

## Historical retained evidence

Earlier RC-0..RC-7, storage, localization and grant-reconciliation entries remain available in Git
history and their signed/CI evidence remains preserved in `docs/STATUS.md`,
`docs/IMPLEMENTATION_STATUS.md`, architecture records and pull requests.
