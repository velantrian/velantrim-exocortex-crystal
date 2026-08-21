# 🌍 Crystal Translation Status

**Status date:** 2026-08-21  
**Primary/source language:** English  
**Active policy:** [LOCALIZATION_POLICY.md](./LOCALIZATION_POLICY.md)  
**Current English human-first README source:** `main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883`  
**Current Russian parity audit source:** `main@9666781d390e3276a111cb5ee1735f6606a76283`  
**Current German parity audit source:** `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`  
**Current French parity audit source:** `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`  
**Current Spanish parity audit source:** `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`  
**Current Italian parity audit source:** `main@e436577dc5ada4692e8fe399da861a44f800e2f1`  
**Current Simplified Chinese parity audit source:** `main@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8`  
**Current Japanese parity audit source:** `main@5903e90f3e0f2884f4ba257a71808d19fc439ebc`  
**Current Arabic parity audit source:** `main@9e048c21fb929f7d299e3af0ef03d76c1df899d6`  
**Current Hindi parity audit source:** `main@e1df11219ee4fc3b9c175b05c7569e568cf6f512`  
**Latest locale refresh tracking:** Issue #441 — TruthGate-v1 D1 freshness reassessment

This ledger records translation freshness. Inline `CURRENT` markers are trace metadata; current technical truth still resolves through merged implementation, executable tests, exact CI, current English contracts and the machine-readable implementation manifest.

## Current localization truth

Arabic, German, French, Spanish, Hindi, Italian, Japanese, Simplified Chinese and Russian root/public Reader-dependent documentation are refreshed to the same **post-RC-9 / post-NLI / RRTIC-v1** public architecture truth. All nine supported locale packs have `CURRENT` D1/D3/D4/D5 Reader-dependent detail surfaces under their recorded source/provenance contracts.

No supported Reader-dependent locale pack remains `REFRESH_NEEDED` after Hindi parity.

### TruthGate v1 reassessment — COMPLETE

English `docs/STATUS.md` and `docs/IMPLEMENTATION_STATUS.md` materially changed at
`main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a` to state the fixed, versioned default TruthGate policy
(`truth-gate-v1-fixed-0.05`) and the separation of process-local adaptation telemetry/research from default admission authority.

Issue #441 reassessed all nine supported locale pairs. All **18/18** affected D1 files now carry explicit `truthgate-v1-source` and `truthgate-v1-status: CURRENT` trace markers and local-language policy text covering the fixed/versioned default plus the non-authority role of process-local adaptation. The older D1/RRTIC source markers remain immutable historical provenance; they are not replaced or reinterpreted.

This completion is a documentation-parity claim only. It does not certify native-speaker editorial quality and does not authorize Reader/RAG/retrieval runtime, PostgreSQL/pgvector activation, Canon expansion, or Titan authority transfer.

D2 reviewer/safety surfaces and Quick Start remain `CURRENT` across all nine supported locales because their governing source semantics did not change in this reassessment.

## Historical phased checkpoints — immutable provenance

These checkpoints remain historical trace evidence and are **not** current repository HEAD declarations:

- **D1/D3/D4/D5 phased source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`
- **D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`
- **Historical Russian RC-6 source:** `main@ed96a88369f841bdb2ffd79ca020acef174685fc`
- **Historical Russian RC-7 source:** `main@ab3ad31c437647535030e371d58f456faf14017b`
- **Historical German root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Historical French root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Historical Spanish root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Historical Italian root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Historical Simplified Chinese root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Historical Japanese root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Historical Arabic root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Historical Hindi root source:** `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2`
- **Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`
- **Retained historical runtime tests:** `2078 passed / 13 skipped / 0 failed`
- **Retained historical measured statements:** `9756 statements / 100.00% line coverage`

Historical compatibility literals remain visible so older evidence contracts continue to be auditable; they do not overwrite newer Reader architecture truth.

### Retained RC-5 / RC-6 / RC-7 compatibility snapshot

- **Reader RC-7 immutable English source checkpoint:** `main@ab3ad31c437647535030e371d58f456faf14017b`
- **Reader RC-7 checkpoint CI:** `31570690153` — 9/9 successful
- **Reader RC-6 immutable English source checkpoint:** `main@ed96a88369f841bdb2ffd79ca020acef174685fc`
- **Reader RC-5 immutable English source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

The later human-first / post-RRTIC locale refreshes are separate presentation layers and do not rewrite these immutable checkpoints.

At the historical RC-7 checkpoint there were **64 `REFRESH_NEEDED` localized documents** and the executable current-inventory representation for that retained compatibility layer is recorded here exactly as:

`279 total = 72 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 64 REFRESH_NEEDED + 10 RETIRED`.

The immutable RC-7 localization layer **does not claim later RC-8/RC-9 meaning** merely because current English or later refreshed locale presentation surfaces advanced.

### Retained post-German compatibility snapshot

- D1/D3/D4/D5 Reader-dependent detail translations were `CURRENT` in German and Russian; seven other supported locales were `REFRESH_NEEDED`.
- The executable D5 inventory then resolved **56 `REFRESH_NEEDED` localized documents**.
- Historical post-German inventory: **279 total = 80 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 56 REFRESH_NEEDED + 10 RETIRED**.

### Retained post-French compatibility snapshot

- D1/D3/D4/D5 Reader-dependent detail translations were `CURRENT` in German, French and Russian; six other supported locales were `REFRESH_NEEDED`.
- The executable D5 inventory then resolved **48 `REFRESH_NEEDED` localized documents**.
- Historical post-French inventory: **279 total = 88 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 48 REFRESH_NEEDED + 10 RETIRED**.

### Retained post-Spanish compatibility snapshot

- D1/D3/D4/D5 Reader-dependent detail translations were `CURRENT` in German, French, Spanish and Russian; five other supported locales were `REFRESH_NEEDED`.
- The executable D5 inventory then resolved **40 `REFRESH_NEEDED` localized documents**.
- Historical post-Spanish inventory: **279 total = 96 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 40 REFRESH_NEEDED + 10 RETIRED**.

### Retained post-Italian compatibility snapshot

- D1/D3/D4/D5 Reader-dependent detail translations were `CURRENT` in German, French, Spanish, Italian and Russian; four other supported locales were `REFRESH_NEEDED`.
- The executable D5 inventory then resolved **32 `REFRESH_NEEDED` localized documents**.
- Historical post-Italian inventory: **279 total = 104 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 32 REFRESH_NEEDED + 10 RETIRED**.

### Retained post-Simplified-Chinese compatibility snapshot

The following literals describe the closed Simplified Chinese milestone and remain historical compatibility evidence after later parity milestones. They are **not** the current inventory:

- D1 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Simplified Chinese and Russian; three other supported locales are `REFRESH_NEEDED`.
- D3 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Simplified Chinese and Russian; three other supported locales are `REFRESH_NEEDED`.
- D4 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Simplified Chinese and Russian; three other supported locales are `REFRESH_NEEDED`.
- D5 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Simplified Chinese and Russian; three other supported locales are `REFRESH_NEEDED`.
- The executable D5 inventory then resolved **24 `REFRESH_NEEDED` localized documents**.
- Historical post-Simplified-Chinese inventory: **279 total = 112 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 24 REFRESH_NEEDED + 10 RETIRED**.

### Retained post-Japanese compatibility snapshot

The following literals describe the closed Japanese milestone and remain historical evidence after later parity milestones. They are **not** the current inventory:

- D1 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian; two other supported locales are `REFRESH_NEEDED`.
- D3 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian; two other supported locales are `REFRESH_NEEDED`.
- D4 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian; two other supported locales are `REFRESH_NEEDED`.
- D5 Reader-dependent detail translations are `CURRENT` in German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian; two other supported locales are `REFRESH_NEEDED`.
- The executable D5 inventory then resolved **16 `REFRESH_NEEDED` localized documents**.
- Historical post-Japanese inventory: **279 total = 120 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 16 REFRESH_NEEDED + 10 RETIRED**.

### Retained post-Arabic compatibility snapshot

The following literals describe the closed Arabic milestone and remain historical evidence after Hindi parity. They are **not** the current inventory:

- D1/D3/D4/D5 Reader-dependent detail translations were `CURRENT` in Arabic, German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian; Hindi remained `REFRESH_NEEDED`.
- The executable D5 inventory then resolved **8 `REFRESH_NEEDED` localized documents**.
- Historical post-Arabic inventory: **279 total = 128 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 8 REFRESH_NEEDED + 10 RETIRED**.

## Root README status

| Locale | Root README | Public parity state | Current/historical source meaning |
|---|---|---|---|
| Arabic | `README.ar.md` | `CURRENT` | current human-first parity audited from `main@9e048c21…`; historical root source retained |
| German | `README.de.md` | `CURRENT` | current human-first parity audited from `main@ad8cec8…`; historical root source retained |
| French | `README.fr.md` | `CURRENT` | current human-first parity audited from `main@7d03cce2…`; historical root source retained |
| Spanish | `README.es.md` | `CURRENT` | current human-first parity audited from `main@bbe6b0d3…`; historical root source retained |
| Hindi | `README.hi.md` | `CURRENT` | current human-first parity audited from `main@e1df1121…`; historical root source retained |
| Italian | `README.it.md` | `CURRENT` | current human-first parity audited from `main@e436577d…`; historical root source retained |
| Japanese | `README.ja.md` | `CURRENT` | current human-first parity audited from `main@5903e90f…`; historical root source retained |
| Simplified Chinese | `README.zh-CN.md` | `CURRENT` | current human-first parity audited from `main@5e6301f0…`; historical root source retained |
| Russian | `README.ru.md` | `CURRENT` | current human-first parity audited from `main@9666781…`; RC-5/6/7 provenance retained |

`CURRENT` means refreshed against an explicit recorded source/parity checkpoint. It never means native-speaker editorial certification or automatic freshness after future English semantic changes.

## D1 — entry / status / implementation

**D1 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D1 Reader-dependent detail translations are `CURRENT` in all nine supported locales.

TruthGate-v1 policy freshness is separately complete for all nine supported locale pairs against `main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a` under Issue #441; historical D1 source checkpoints remain provenance rather than being rewritten.

## D2 — reviewer / safety / privacy

**D2 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

All nine supported D2 locale packs remain `CURRENT` for their recorded source semantics. Hindi `REVIEWER_GUIDE.md` and `SAFETY_PRIVACY_AND_FAILURES.md` were deliberately not rewritten by Issue #427.

D2 reviewer/safety translations remain current across all nine supported locales.

No native-speaker editorial certification is implied by `CURRENT`; CI validates objective contract markers, not independent human language certification.

## D3 — architecture / storage / authority

**D3 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D3 Reader-dependent detail translations are `CURRENT` in all nine supported locales.

Hindi D3 preserves the current architecture chain:

```text
RC-1 → RC-2 → RC-3 → RC-4 → RC-5 → RC-6 → RC-7
                                      ↓
                         RC-9 lexical PRE-ADMISSION
                                      ↓
                     RRTIC-v1 architecture contract
                                      ↓
                           evidence/admission boundary
                                      ↓
                        Guardian → TruthGate → Canon
```

## D4 — project / grant / glossary

**D4 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D4 Reader-dependent detail translations are `CURRENT` in all nine supported locales.

Funding truth remains identical in every current locale:

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

Approximately €50,000 remains planning/transparency context only.

## D5 — extended reference corpus

**D5 source checkpoint:** `main@51c205fe048fd69d39fcd47b43e042a50de432bc`

D5 Reader-dependent detail translations are `CURRENT` in all nine supported locales.

The executable D5 inventory now resolves **0 `REFRESH_NEEDED` localized documents**.

Resolved inventory after Hindi parity:

```text
279 total
136 CURRENT
133 ENGLISH_ONLY_BY_DESIGN
0 REFRESH_NEEDED
10 RETIRED
```

The immutable D5 source-inventory repository checkpoint remains the signed PR #350 merge `3de746e74be844c6fda55849c10faac5c3f0631a`. Hindi parity changes freshness classification, not that historical checkpoint.

## Reader RC-5 boundary — retained compatibility contract

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
nli_reader_runtime_filter = false
```

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
```

## Post-RC-9 research truth that translations must preserve

RC-9 remains the implemented deterministic lexical PRE-ADMISSION candidate discovery baseline. Retained classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator v1 is frozen evaluation evidence with classification `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`; it did not authorize semantic Reader runtime.

NLI neutral-filter v1 is frozen evaluation evidence with classification `NLI_NEUTRAL_FILTER_GATE_FAILED`; it did not authorize an NLI Reader runtime filter.

RRTIC-v1 is a frozen architecture contract for typed suspicion/qualifier inspection. It is not a model, filter, reranker, identity engine, evidence-admission authority or Canon writer.

## Storage / grant / authority invariants

```text
SQLite ordinary local-first = ACTIVE
PostgreSQL/pgvector import target = INACTIVE
active=false
physical L3 != strict Canon
successful import != backend activation
```

NLnet remains **submitted / under review / not awarded**. Translation cannot turn planning context into an award, a failed evaluation into a runtime capability, or a retrieval candidate into Evidence/Canon authority.

## Remaining localization program

The bounded Human-First documentation parity program is complete for all nine supported locales. The TruthGate-v1 D1 reassessment under Issue #441 is also complete for all 18 affected D1 documents. No Reader-dependent locale remains in the refresh backlog for the recorded semantics.

Any future localization work requires a new live audit if English source semantics change; `CURRENT` is not a permanent freshness guarantee.
