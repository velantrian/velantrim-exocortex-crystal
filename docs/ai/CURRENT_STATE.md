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
reader_core_rc1_skeleton              = true
reader_core_rc2_structural_map        = true
reader_core_rc3_multi_pass_mechanics  = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core                 = false
```

RC-1 implements the bounded evidence-linked source/session skeleton. RC-2 implements the bounded caller-supplied Structural Document Map. RC-3 implements deterministic explicit multi-pass mechanics over one OPEN session and one exact-version structural map. RC-4 implements deterministic pre-admission proposition candidate registration from completed substantive RC-3 regions.

RC-3 supports `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK` and `TARGETED_REREAD`; records attempted/completed/interrupted/degraded state; requires declared structural targets and explicit per-region coverage outcomes; preserves partial progress; and exposes count-only telemetry. Cross-check/targeted reread require prior substantive processing. An unresolved structural region remains fail-visible through `NEEDS_REVIEW`.

RC-4 accepts only declared targets of a `COMPLETED` pass whose recorded outcome and current matching coverage are `PROCESSED` or `REVISITED`. It creates source-linked `EXTRACTED_PROPOSITION` SegmentCards/candidates with primary/supporting replayable locators, source owner, source-presentation category, explicit negation and qualifiers. Factual assertion, opinion, hypothesis, conditional, example, quoted speech, reported position, definition and uncertain assertion remain distinct.

RC-4 is not automatic NLP/model extraction. It does not call `core.evidence.attach_evidence()`, create a fact evidence row, set evidence sufficiency, mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, resolve contradictions or create planner/belief-update authority. `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`.

RC-1/RC-2/RC-3/RC-4 may not mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, resolve contradictions or create planner/belief-update authority. No automatic parser/OCR, Reader LLM/provider agent, embeddings/ANN/vector database or automatic cross-document reasoning runtime is present. `coverage != comprehension proof`; `pass completion != comprehension proof`.

## Localization

The RC-4 English public/source surfaces advance the Reader semantic checkpoint. The immutable localization source checkpoint for this RC-4 reconciliation is `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86`. Russian Reader-dependent public/detail documentation is refreshed in the RC-4 branch against that exact checkpoint.

D2 reviewer/safety translations remain current across all nine supported locales at `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f` because RC-4 does not change their source semantics. Russian D1/D3/D4/D5 detail pack is current against the RC-4 checkpoint. The eight other locale detail packs require Reader refresh; their prior rich translations are preserved as explicit `REFRESH_NEEDED` debt rather than shortened replacements.

The eight other localized root README files and Reader-dependent detail packs require RC-4 semantic refresh. D2 reviewer/safety and Quick Start remain current across all nine locales. The tracked Reader/root refresh debt remains 64 documents: the same eight roots plus seven Reader-dependent detail types per non-Russian locale, now lagging the RC-4 source checkpoint rather than RC-3.

The translation ledger and machine documentation manifest are the freshness authority. Old `CURRENT` markers tied to an older explicit source SHA describe that historical checkpoint only; they do not override the newer ledger.

## Grant truth

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget or payment commitment. Budget change: none. Work merged before any agreement, including Reader RC-0/RC-1/RC-2/RC-3 and RC-4 if merged pre-agreement, is existing baseline and cannot be counted again as future funded delta.

## Next Reader work

After RC-4 is merged and independently evidenced, the next Reader phase must be separately authorized. The current roadmap candidate is RC-5 exceptions / contradiction candidates, followed by long-context and cross-document work before any vector-stack commitment.
