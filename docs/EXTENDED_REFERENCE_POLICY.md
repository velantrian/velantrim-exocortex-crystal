<!-- d5-source-policy: CURRENT -->
<!-- d5-inventory-scope: repository-documentation-corpus -->
# D5 extended-reference and retirement policy

## Purpose

D5 gives documentation-like repository surfaces explicit status without translating volatile evidence merely to create apparent parity. English remains primary/source and conflict-resolving language. The machine inventory is [`status/d5-inventory.json`](status/d5-inventory.json).

## States

| State | Meaning |
|---|---|
| `CURRENT` | maintained public/routing surface current against recorded source checkpoint |
| `REFRESH_NEEDED` | preserved translation known to lag its governing source |
| `RETIRED` | historical/audit material, not current authority |
| `ENGLISH_ONLY_BY_DESIGN` | detailed volatile technical/security/test/AI/RFC/ADR/grant evidence maintained only in English |

`REFRESH_NEEDED` is explicit debt, never a silent default and never permission to replace rich translations with short summaries.

## Reader Core boundary

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
dedicated_reader_core                  = false
```

RC-5 registers explicit `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION` and `TENSION` candidates only over valid RC-4 proposition candidates in one Reader session and exact source version. It preserves exact candidate linkage/provenance and rationale.

RC-5 is pre-admission and has no truth/Canon/ESM/planner authority. It does not call `core.evidence.attach_evidence()`, create fact evidence, promote confidence, resolve contradictions, infer semantic identity, perform cross-document reading or use LLM/provider/parser/OCR/embedding/ANN dependencies.

RC-6 adds a bounded long-context strategy over the current registered RC-4 candidates of one OPEN ReaderSession and exact SourceVersion. It uses RC-2 structural order plus candidate-ID tie-breaking and explicit candidate-count / direct-source-locator budgets. Candidate provenance is atomic and fails closed if one candidate cannot fit the declared locator budget.

A matching RC-5 registry is optional context only: an existing relation ID is carried into a working set only when both endpoints are already in that same set. RC-6 does not infer cross-set relations or semantic identity.

A caller may register `SourceFidelity.SUMMARY` text for a current working set. RC-6 preserves direct RC-4 leaf candidate IDs and replayable source locators, rechecks the working-set provenance snapshot before registration, and does not permit summary-only provenance chaining. Summary text is never generated automatically by RC-6.

```text
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage    != comprehension proof
summary                 != source text
summary                 != evidence
summary                 != verified fact
summary                 != Canon admission
```

RC-6 has no truth/Canon/ESM/evidence/planner authority, no contradiction resolution, no confidence/evidence-sufficiency promotion, no RC-7 cross-document reading and no LLM/provider/parser/OCR/embedding/ANN dependency.

## Localization decision

Russian Reader-dependent public/detail surfaces remain `CURRENT` against the immutable RC-5 English checkpoint recorded in `docs/TRANSLATION_STATUS.md` **until the separate RC-6 Russian refresh commit pins the new immutable English RC-6 checkpoint**. Therefore RC-5 `CURRENT` markers are historical checkpoint truth, not a claim that the existing Russian files already contain RC-6 semantics. The eight other supported Reader-dependent locale packs remain `REFRESH_NEEDED`; their prior rich translations are preserved. D2 and Quick Start remain `CURRENT` across all nine locales because RC-6 does not change those source semantics.

## Storage/grant/non-claims

SQLite remains ordinary active local-first. PostgreSQL/pgvector remains an inactive target with `active=false`. NLnet remains submitted / under review / not awarded; approximate €50,000 is planning only; budget change is none. RC-5 merged pre-agreement is existing baseline, not future funded delta. If RC-6 merges before an agreement, RC-6 also becomes existing pre-agreement baseline.

No legal/GDPR/security/native-speaker editorial certification, full autonomous Reader, automatic summarization, RC-7 cross-document reading, automatic semantic contradiction resolution or active PostgreSQL backend is claimed.
