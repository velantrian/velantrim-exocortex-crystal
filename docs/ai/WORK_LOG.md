# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It is not a replacement for Git history, issues, pull requests, `CHANGELOG.md` or Notion. Earlier detailed entries remain available through Git history.

## 2026-08-12 — Reader RC-9 deterministic lexical candidate discovery (#375)

- Live verified starting `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6`, signature `verified=true` / `reason=valid`, open PRs 0 before the milestone.
- Reverified RC-8 exact-head CI `31581756932` on `a9a4e3b67c514c6c0eece58424c209e9693d3dd7` and post-merge push CI `31582325275` on `bd85479e...` as successful.
- Confirmed #155/#165/#214 remain separate backlog and existing embedding/legacy/query retrieval is admitted-memory authority, not PRE-ADMISSION Reader identity machinery.
- Created issue #375 and branch `feat/reader-rc9-lexical-baseline` from the exact audited main.
- Added stdlib-only `core/reader_lexical_discovery.py`: conservative NFKC/case/whitespace normalization, stable lexical tokens, deterministic in-memory BM25, cross-document default filtering, self-match exclusion, stable tie-breaks and structured inspection-only results.
- Added `scripts/bench_reader_rc9_lexical.py` and frozen result `eval/reader_rc9_lexical_baseline.json` over the unchanged 20-case RC-8 corpus.
- K=5 baseline: Recall 0.937500, Precision 0.217391, MRR 0.895833, paired hard-negative rate 1.000000. Cross-lingual paraphrase is missed; all four paired SAME_TOPIC/MERELY_SIMILAR hard negatives are surfaced in top-5.
- Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. This is not semantic/vector authorization; embeddings, hybrid retrieval, ANN/vector DB, PostgreSQL activation, automatic identity/adjudication/evidence admission remain out of scope.
- Local isolated RC-9 tests reached 100% line coverage for the new module/runner; repository exact-head CI remains the authoritative full Python 3.11/3.12 validation.
- Added `docs/architecture/READER_RC9_LEXICAL_BASELINE.md` and reconciled current English status/risk/roadmap/component surfaces. RC-8 historical decision remains intact.
- Documentation impact: `GITHUB_AND_NOTION`; the three existing Crystal Notion pages may be updated only after guarded merge, verified signed main and successful exact post-merge CI.

## 2026-08-12 — Reader RC-8 post-RC-7 retrieval architecture decision (#373)

- Live verified starting `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, signature `verified=true` / `reason=valid`, open PRs 0 before the milestone.
- Reverified RC-7 PR #372 exact validated head `b1cf79594f702194b4dce66ac2ef2546d4154f15`, exact-head CI `31572324596` 9/9 and post-merge CI `31572918731` 9/9.
- Audit found the post-RC-7 corpus candidate-discovery gap and distinguished existing admitted-memory retrieval from PRE-ADMISSION Reader artifacts.
- Added `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`, the 20-case synthetic corpus and contract tests.
- Decision: no Reader embeddings/ANN/vector DB; first establish deterministic lexical candidate discovery + benchmark runner under separate authorization.
- Authority firewall retained: `retrieval match != evidence`, `similarity != identity`, `repetition != corroboration`, `cross-document candidate != Canon relation`, `ranking != epistemic authority`, `candidate discovery != candidate adjudication`.

## 2026-08-12 — Reader Core RC-6 bounded long-context strategy (#369 / PR #370)

- Signed merge and exact CI completed; deterministic bounded working sets and caller-supplied SUMMARY preserve direct RC-4 provenance with no automatic summarization or authority gain.

## 2026-08-11 — Reader Core RC-5 relation candidates (#367 / PR #368)

- Guarded squash merge produced signed `main@af9e050e467adbf2f73a0a916a88a99918e46f38`; exact-head CI `31546290347` 9/9; post-merge CI `31546737038` 9/9.
- Added bounded same-session/same-source `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` candidates; no resolution/admission authority.

## 2026-08-10 — Post-i18n truth/backlog reconciliation (#353)

- Verified signed baseline and reconciled localization/backlog truth without merging prototype or cross-project work.

## 2026-08-08 — PR #337 inactive PostgreSQL import/equivalence merged

- Merge `bbd816c09dd39a02e6de6c1014438490572f40f6`; exact-head CI `31256316536` 9/9; Python 3.11/3.12: 2078 passed / 13 skipped; 9756 statements / 100.00% coverage.
- Implemented inactive PostgreSQL import/equivalence only; no runtime activation/cutover/automatic switching/ANN authority.
