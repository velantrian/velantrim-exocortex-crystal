# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It is not a replacement for Git history, issues, pull requests, `CHANGELOG.md` or Notion. Earlier detailed entries remain available through Git history.

## 2026-08-12 — Reader Core RC-6 bounded long-context strategy (#369 / PR #370)

- Live verified signed starting `main@af9e050e467adbf2f73a0a916a88a99918e46f38`, signature `verified=true` / `reason=valid`, open PRs 0 and exact post-RC-5 push CI `31546737038` 9/9.
- Live Notion read-back confirmed all three canonical Crystal pages still had RC-5 as top current truth before RC-6 work began.
- `ROADMAP.md` establishes the next order as RC-6 long-context strategy → RC-7 cross-document reading; operator separately authorized continuation, so issue #369 scopes RC-6 only.
- Branch `agent/reader-core-rc6-long-context` was created from exact starting main. Draft PR #370 was opened without `Closes #369` auto-close language so completion ordering can remain explicit.
- Initial runtime commit `97b1befa2c0db830bace2781489a164e8cfeb2c7` added only `core/reader_long_context.py` and `tests/test_reader_long_context.py`.
- Initial smoke CI `31548812403` exposed one test-design/provenance-order defect: 2148 tests passed, one failed, 13 skipped and one guard line was uncovered. The failure proved a deeper structural-provenance guard fired before the intended working-set snapshot-drift guard.
- Fix commit `83516354e20c20751c1adda79f2b57592b10ab9c` moved immutable working-set leaf-provenance comparison before deep per-leaf revalidation in `register_summary()`. This preserves fail-closed behavior and makes summary snapshot drift explicit.
- Corrected exact-head smoke CI `31549837676` is **9/9 successful** on `83516354e20c20751c1adda79f2b57592b10ab9c`, including Python 3.11/3.12, docs-status, Ring Zero, security, Ruff/code-quality, eval, JSONL integrity and Docker.
- RC-6 design: deterministic RC-2 structural order + candidate-ID tie-break, rolling working sets bounded by candidate count and direct source-locator count, candidate atomicity, optional RC-5 relation carry-through only when both sides are in-set, and caller-supplied `SUMMARY` artifacts with direct RC-4 leaf provenance.
- Authority boundary remains fail closed: no automatic summarization/model/provider/token-context claim, parser/OCR, embeddings/ANN, RC-7 cross-document reasoning, evidence admission, truth/Canon/ESM mutation, contradiction resolution, planner authority, Reader persistence/API/CLI/worker or PostgreSQL activation.
- English public/machine truth is intentionally committed before Russian refresh so the immutable English source SHA can be recorded honestly. Existing Russian `CURRENT` markers remain RC-5 checkpoint history until the follow-up RC-6 Russian parity commit pins the new exact English source SHA.
- Impact classification: `GITHUB_AND_NOTION`; Notion synchronization remains forbidden until guarded merge and exact post-merge push CI succeed.

## 2026-08-11 — Reader Core RC-5 relation candidates (#367 / PR #368)

- Guarded squash merge produced signed `main@af9e050e467adbf2f73a0a916a88a99918e46f38` with signature `verified=true`, reason `valid`.
- Final validated PR head `b4e26c9be3671e5e8049add280289c6d5fe7c798`; exact-head CI `31546290347` 9/9; exact post-merge push CI `31546737038` 9/9.
- Added bounded same-session/same-source-version `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` relation candidates over registered RC-4 proposition candidates only.
- Restored/hardened D1/D3/D4/D5 documentation validators so green CI could not be obtained by weakening inventory/link/stale-claim/storage/grant/authority checks.
- Russian Reader-dependent root + D1/D3/D4/D5 surfaces were current at RC-5 checkpoint; eight other locale packs remained rich `REFRESH_NEEDED`, 64 tracked documents.
- Notion 3/3 synchronized and read back only after post-merge CI. Completion evidence posted to #367; issue closed completed after correcting GitHub's earlier auto-close ordering.

## 2026-08-10 — Post-i18n truth/backlog reconciliation (#353)

- Verified signed starting `main@f4556e8f9775d28d4a1b2c20a28962a95e55d33e`, PR #352 exact-head CI `31340722027` 9/9 and post-merge CI `31341125405` 9/9.
- Confirmed D1–D5 current at that checkpoint and triaged stale backlog/PR state without merging prototype or cross-project work.

## 2026-08-08 — PR #337 inactive PostgreSQL import/equivalence merged

- Merge: `bbd816c09dd39a02e6de6c1014438490572f40f6`; validated head `d7af7c80722274f9217bc5545d150f92e9363f37`.
- Exact-head CI `31256316536`: 9/9; Python 3.11/3.12: 2078 passed / 13 skipped; 9756 statements / 100.00% coverage.
- Real PostgreSQL/pgvector integration `31256316532`: successful against PostgreSQL 16, pgvector 0.8.2 and Psycopg 3.3.4.
- Implemented issue #332 phase 1 only: optional lazy driver, preflight, new inactive schema, serializable import, independent exact re-hash and non-secret receipts.
- No runtime activation, cutover, rollback, dual-write, automatic switching, ANN acceptance, Guardian, TruthGate or strict Canon change.
