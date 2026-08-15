# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It does not replace Git history, issues, pull requests, `CHANGELOG.md` or Notion.

## 2026-08-15 — Legacy exact-normalized ingest compatibility (#165 / PR #431)

- Live starting point: signed `main@e2c557c07f23bc695bd58a70138421cccc3b5764`, `verified=true`, `reason=valid`, after audit-remediation PR #430 and post-merge CI `31902827194` SUCCESS.
- Problem: pre-normalization historical `ing:*` facts use raw-text MD5 ids. The old compatibility fallback could reuse them only when a later utterance was byte-identical, so casing/whitespace variants could create a second normalized-id fact.
- Selected design: a **persistent derived/rebuildable normalized-ingest compatibility index**, rather than a one-time historical fact-ID re-key/merge migration. This avoids coordinated rewriting of L1/L3/evidence/provenance/import-session/audit references.
- Identity contract remains exact and deterministic only: `NFC → trim → collapse internal whitespace → casefold`. `exact normalized equality != semantic identity`.
- Resolution order: an existing current normalized `fact_id` wins; otherwise an already-`Validated` historical `ing:*` row may be selected by exact normalized equality; the byte-identical raw-id fallback remains for pending/non-Validated legacy rows.
- Historical collisions are preserved rather than merged. If multiple legacy rows already share one normalized identity, future occurrence-only hits route deterministically to the oldest `created_at`, then `fact_id`.
- Explicit custom `fact_id` ingestion bypasses the compatibility resolver. Duplicate behavior remains occurrence-only: no reinforce, confidence change, ESM promotion, corroboration or Canon shortcut.
- Import dry-run uses the same resolver in read-only mode and does not create/backfill the compatibility table. Full erasure removes the derived mapping; mapping existence is not treated as proof of Canon/personal data.
- Adversarial tests cover cross-case/whitespace legacy variants, current-id precedence, preserved collisions, custom-id isolation, non-Validated isolation, pending raw fallback, dry-run/live parity, write-free preview, erasure cleanup and unchanged occurrence-only semantics.
- Documentation impact: English authoritative/current-truth surfaces only. Localized documentation is deliberately untouched and remains a separate maintainer-controlled parity task.
- Authority/non-goals: no semantic or near-duplicate matcher, Reader semantic/hybrid runtime, NLI/CrossEncoder/LLM judge, FTS/ANN/vector DB, PostgreSQL/pgvector activation, EPIS runtime, cross-project bridge or new authority owner.
- PR #431 remains subject to final exact-head CI, review/thread gate, guarded squash merge, post-merge CI and existing Notion-surface reconciliation. Independent review/approval is not claimed unless actually obtained.

## 2026-08-14 — Mentaury External Labs boundary reconciliation · DRAFT

- Live starting point: signed `main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883`, signature `verified=true` / `reason=valid`.
- Scope is documentation/research-boundary reconciliation only: no `core/**`, Canon, TruthGate, Guardian, schema, runtime wiring, grant deliverable, capability or production-authority change.
- Finding: Crystal's ecosystem map was safe but described Mentaury mainly as identity research; the External Labs Truth Ledger artifact and private External Labs history still used the older `Standalone Memory-Centered Cognitive Sandbox` framing as if it were current.
- Decision: current Mentaury cognition / digital-individuality ownership belongs to the independent `velantrim-mentaury-soul` project. Crystal retains only its evidence/trust boundary and historical research provenance.
- Public boundary: `Crystal evidence / claims / Receipts ≠ Mentaury belief / identity / M3`; `Mentaury research result ≠ Crystal Canon / evidence / runtime authority`; `shared vocabulary ≠ shared architecture`.
- Historical External Labs contracts are preserved, not deleted. The old Truth Ledger P0 candidate is explicitly marked historical and remains a failed/unaccepted candidate unless its own historical acceptance gate is independently satisfied.
- Any future Crystal ↔ Mentaury adapter requires separate ownership, interface contract, privacy/consent/erasure review, deterministic tests, read-only/shadow evaluation, rollback and explicit approval.
- Documentation impact: `GITHUB_AND_NOTION`. Notion targets synchronized in this work cycle: `📚Velantrim External Labs🔬` and `📜 Velantrim & Mentaury — Detailed Worklog / Architecture Narrative 🧠🔬`.
- GitHub candidate branch: `agent/reconcile-mentaury-external-labs-boundary`; exact PR/head and CI evidence must be recorded before merge. No green-CI or merge claim is made in this entry yet.

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
