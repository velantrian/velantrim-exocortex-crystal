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
dedicated_reader_core                  = false
```

RC-5 registers explicit `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION` and `TENSION` candidates only over valid RC-4 proposition candidates in one Reader session and exact source version. It preserves exact candidate linkage/provenance and rationale.

RC-5 is pre-admission and has no truth/Canon/ESM/planner authority. It does not call `core.evidence.attach_evidence()`, create fact evidence, promote confidence, resolve contradictions, infer semantic identity, perform cross-document reading or use LLM/provider/parser/OCR/embedding/ANN dependencies.

```text
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
```

## Localization decision

Russian Reader-dependent public/detail surfaces are `CURRENT` against the immutable RC-5 English checkpoint recorded in `docs/TRANSLATION_STATUS.md`. The eight other supported Reader-dependent locale packs are `REFRESH_NEEDED`; their prior rich translations are preserved. D2 and Quick Start remain `CURRENT` across all nine locales because RC-5 does not change those source semantics.

## Storage/grant/non-claims

SQLite remains ordinary active local-first. PostgreSQL/pgvector remains an inactive target with `active=false`. NLnet remains submitted / under review / not awarded; approximate €50,000 is planning only; budget change is none. RC-5 merged pre-agreement is existing baseline, not future funded delta.

No legal/GDPR/security/native-speaker editorial certification, full autonomous Reader, automatic semantic contradiction resolution or active PostgreSQL backend is claimed.
