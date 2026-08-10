# Crystal AI Current State

**Status date:** 2026-08-10

GitHub merged `main`, executable tests, exact CI and the machine-readable implementation manifest are implementation authority. Notion records synchronized strategy/history and never overrides GitHub evidence.

## Runtime / storage truth

- verified runtime checkpoint: `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337;
- retained checkpoint evidence: Python 3.11/3.12 2078 passed / 13 skipped / 0 failed, 9756 statements / 100.00% line coverage;
- later Reader milestones carry their own exact-head and post-merge CI evidence;
- SQLite remains ordinary active local-first;
- PostgreSQL/pgvector remains an inactive target with `active=false`;
- normal PostgreSQL runtime adapter and automatic backend switching remain absent.

## Reader truth

```text
reader_core_rc1_skeleton             = true
reader_core_rc2_structural_map       = true
reader_core_rc3_multi_pass_mechanics = true
dedicated_reader_core                = false
```

RC-1 implements the bounded evidence-linked source/session skeleton. RC-2 implements the bounded caller-supplied Structural Document Map. RC-3 implements deterministic explicit multi-pass mechanics over one OPEN session and one exact-version structural map.

RC-3 supports `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK` and `TARGETED_REREAD`; records attempted/completed/interrupted/degraded state; requires declared structural targets and explicit per-region coverage outcomes; preserves partial progress; and exposes count-only telemetry. Cross-check/targeted reread require prior substantive processing. An unresolved structural region remains fail-visible through `NEEDS_REVIEW`.

RC-1/RC-2/RC-3 may not mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, resolve contradictions or create planner/belief-update authority. No automatic parser/OCR, Reader LLM/provider agent, embeddings/ANN/vector database or automatic cross-document reasoning runtime is present. `coverage != comprehension proof`; `pass completion != comprehension proof`.

## Localization

The RC-3 English public/source surfaces advance the Reader semantic checkpoint. Russian Reader-dependent public/detail documentation is refreshed in the RC-3 branch against the resulting immutable source checkpoint.

The eight other localized root README files and Reader-dependent detail packs must not be silently relabelled as current after the English RC-3 semantic change. Their prior rich translations are preserved and become explicit `REFRESH_NEEDED` debt until full semantic refresh. D2 reviewer/safety and Quick Start remain current because RC-3 does not change their source semantics.

The translation ledger and machine documentation manifest are the freshness authority. Old `CURRENT` markers tied to an older explicit source SHA describe that historical checkpoint only; they do not override the newer ledger.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget or payment commitment. Budget change: none. Work merged before any agreement, including Reader RC-0/RC-1/RC-2 and RC-3 if merged pre-agreement, is existing baseline and cannot be counted again as future funded delta.

## Next Reader work

After RC-3 is merged and independently evidenced, the next Reader phase must be separately authorized. The current roadmap candidate is RC-4 evidence extraction, followed by exceptions/contradiction candidates and long-context work before any vector-stack commitment.
