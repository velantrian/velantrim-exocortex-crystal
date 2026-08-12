# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It is not a replacement for Git history, issues, pull requests, `CHANGELOG.md` or Notion.

## 2026-08-12 — Reader RC-10 reuse compatibility / preregistration (#377)

- Live verified starting `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`, signature `verified=true` / `reason=valid`, open PRs 0 before RC-10.
- Confirmed RC-9 PR #376 merged from exact head `1956cbd45e5a5b794852354ed2233bf1fb6e318f`; exact-head CI `31593097846` and post-merge push CI `31594027040` both 9/9; issue #375 closed completed; Notion 3/3 sync/read-back had completed.
- Per operator request, performed a dedup audit before creating any new retrieval implementation.
- Found substantial existing **admitted-memory** retrieval: deterministic hashing/trigram embedders, optional SentenceTransformer, admitted vector + graph-walk retrieval, bounded legacy lexical fallback (#317 / PR #321), bounded retrieval config and pure stdlib RRF.
- Confirmed no current Reader SQLite FTS5 virtual-table/`MATCH` runtime implementation; FTS is already a documented future scale option in `docs/core/DEDUP_AND_SCALE.md` and RC-8.
- Decision: do not build a second retrieval stack. RC-10 is architecture/evaluation only: reuse-compatibility matrix + machine-readable future comparison preregistration.
- Reuse disposition: `core/rrf.py` potentially reusable as pure ordering; hashing/trigram are comparator signals only; SentenceTransformer is future optional comparator only; `get_embedder("auto")` forbidden for a qualifying preregistered Reader experiment; admitted-memory pipeline/query/legacy retrieval are not direct PRE-ADMISSION Reader pipelines.
- Frozen future gate before results: retain 15 RC-9 useful hits, recover `rc8-004` to 16/16 / Recall@5 1.0, MRR >=0.895833, paired hard-negative hits <=2/4, zero authority violations, exact backend identity, zero query-time network calls and no external source-text transmission.
- Passing that gate means `ELIGIBLE_FOR_STRONGER_EVALUATION_AND_ARCHITECTURE_REVIEW_ONLY`, not runtime authorization.
- Audit also found GitHub truth drift: compact status surfaces still described RC-9 as in progress and root `README.md` still presented RC-6/RC-7-in-progress. RC-10 reconciles compact current English status while recording root/localized README reconciliation as separate documentation debt.
- RC-10 adds no `core/**` runtime change, no FTS/vector schema, no model download/dependency, no semantic/hybrid run, no PostgreSQL activation and no #155/#165/#214 work.
- Documentation impact: `GITHUB_AND_NOTION`; synchronize only the three existing Crystal pages after guarded merge + signed main + green post-merge CI.

## 2026-08-12 — Reader RC-9 deterministic lexical candidate discovery (#375 / PR #376) — COMPLETE

- Starting main was `bd85479e014c26ddebd0f4ae06385ce6625f5ab6`.
- Final validated PR head: `1956cbd45e5a5b794852354ed2233bf1fb6e318f`.
- Guarded squash merge: `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`; signature `verified=true`, reason `valid`.
- Exact-head CI `31593097846`: 9/9 successful; post-merge push CI `31594027040`: 9/9 successful; Python 3.11/3.12 passed the 100% coverage gate.
- Added stdlib-only `core/reader_lexical_discovery.py`, deterministic benchmark runner and frozen result over the unchanged RC-8 20-case corpus.
- Independent review corrected fail-closed string validation, a brittle historical-doc assertion and provisional Precision@K denominator semantics before final CI.
- Final K=5 baseline: Recall 0.937500, Precision 0.187500, MRR 0.895833, paired hard-negative rate 1.000000; `rc8-004` missed; 4/4 paired hard negatives surfaced.
- Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. This did not authorize semantic/vector runtime.
- Notion 3/3 synchronized/read back after green post-merge CI; completion evidence posted to #375; issue closed completed.

## 2026-08-12 — Reader RC-8 post-RC-7 retrieval architecture decision (#373 / PR #374)

- Starting signed main `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`; RC-7 post-merge CI `31572918731` 9/9.
- Audit found candidate-discovery and evaluation gaps plus existing admitted-memory retrieval in a separate authority domain.
- Added RC-8 decision and frozen 20-case synthetic adversarial corpus.
- Required deterministic lexical baseline before any semantic/vector comparison; SQLite FTS future option must feature-detect/fallback; semantic/vector remained deferred.

## 2026-08-12 — Reader Core RC-7 bounded cross-document candidate links

- Signed merge `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`; exact-head CI `31572324596` and post-merge CI `31572918731` 9/9.
- Added explicit PRE-ADMISSION cross-document candidate links with exact two-sided provenance and no automatic semantic identity/evidence authority.

## 2026-08-12 — Reader Core RC-6 bounded long-context strategy (#369 / PR #370)

- Signed merge `1f5129d3276af28608b16e369fd38d21fe38c0d5`; post-merge CI `31566408978` 9/9.
- Deterministic bounded working sets; caller-supplied SUMMARY keeps direct RC-4 leaf provenance; no automatic summarization or authority promotion.

## 2026-08-11 — Reader Core RC-5 relation candidates (#367 / PR #368)

- Signed merge `af9e050e467adbf2f73a0a916a88a99918e46f38`; exact-head/post-merge CI green.
- Added bounded same-session relation candidates and restored/hardened documentation validators.

## 2026-08-08 — PR #337 inactive PostgreSQL import/equivalence merged

- Merge `bbd816c09dd39a02e6de6c1014438490572f40f6`; exact-head CI 9/9; PostgreSQL integration successful.
- Inactive import/equivalence only; no runtime activation, cutover, rollback, dual-write, ANN acceptance or authority change.
