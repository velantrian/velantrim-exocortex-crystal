<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**RC-7 signed merge:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**RC-8 signed merge / RC-9 audited start:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Current bounded milestone:** Reader RC-9 lexical candidate-discovery baseline, issue #375  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader baseline through RC-7

RC-0 is normative. RC-1 through RC-7 are merged bounded layers:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
```

### ✅ RC-1 — Minimal Evidence-Linked Reading Skeleton
Exact source/version identity, replayable locators, Reader sessions, fidelity and coverage.

### ✅ RC-2 — Structural Document Map
Caller-supplied version-bound structure; no parser/OCR authority.

### ✅ RC-3 — Explicit Multi-Pass Reading Mechanics
Deterministic explicit reading passes and auditable outcomes.

### ✅ RC-4 — Source-Linked Proposition Extraction
Source-linked `EXTRACTED_PROPOSITION` candidates; `EXTRACTED_PROPOSITION != verified fact` and `Reader candidate != admitted evidence`.

### ✅ RC-5 — Exceptions / Contradiction Candidate Detection
`core/reader_relations.py` registers PRE-ADMISSION `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`. `contradiction candidate != confirmed contradiction`.

### ✅ RC-6 — Bounded Long-Context Strategy
Bounded working sets and caller-supplied SUMMARY with direct provenance. Historical sequence remains **RC-6 long-context strategy → RC-7 cross-document reading**.

### ✅ RC-7 — Bounded Cross-Document Candidate Links
Explicit cross-document candidate links with exact two-sided provenance; no automatic semantic matching, identity, evidence admission or Canon relation.

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## ✅ RC-8 — Post-RC-7 Candidate Discovery & Retrieval Architecture Decision

Issue #373 / PR #374 completed. Decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Frozen corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

RC-8 separated PRE-ADMISSION Reader candidate discovery from admitted-memory retrieval and required a deterministic lexical baseline before any semantic/vector comparison.

## 🚧 RC-9 — Deterministic Lexical Candidate Discovery Baseline

Tracking issue: #375. Contract/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`.

Implementation scope:

```text
RC-4 propositions
→ conservative lexical normalization/tokenization
→ deterministic in-memory BM25
→ top-K inspection candidates
→ benchmark/downstream review
```

No semantic/vector machinery, PostgreSQL activation, automatic identity/adjudication, evidence admission or Canon mutation is included.

Frozen K=5 benchmark snapshot (`eval/reader_rc9_lexical_baseline.json`): Recall 0.937500, Precision 0.217391, MRR 0.895833, paired hard-negative rate 1.000000. It misses the cross-lingual pair and surfaces all four paired hard negatives.

Architecture interpretation:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

That result does not authorize the next mechanism. A future milestone may consider a pre-registered lexical-vs-hybrid/semantic comparison, but RC-9 must complete and STOP first.

## 🧩 Backlog remains separated

- #165 — exact normalized ingest dedupe/migration; no near-duplicate/semantic matching.
- #155 — downstream Epistemic Router / Evidence State RFC.
- #214 — PII fixture / reproducible supply-chain hardening.

## ✅ Storage baseline remains unchanged

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL inactive import/equivalence
→ active=false
```

## 🌍 Localization position

Russian Reader-dependent RC-7 surfaces remain current; eight other Reader-dependent locale packs remain `REFRESH_NEEDED` — 64 tracked documents. RC-9 updates authoritative English status/architecture only.

## 🎓 Grant boundary

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning only, not an approved budget/payment commitment. Anything merged before an agreement is existing baseline and cannot be counted again as future paid work. RC-9 is not an awarded/funded-delivery claim.

## ⏭️ After RC-9 — decision only, not started

Once RC-9 is fully closed, a separate future architecture milestone may assess whether measured gaps justify lexical scaling, hybrid comparison or semantic/vector comparison. It must pre-register thresholds and preserve the authority firewall before implementation. RC-10 is not started here.

## Related documents

- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [RC-8 retrieval decision](./docs/architecture/READER_RC8_RETRIEVAL_DECISION.md)
- [RC-9 lexical baseline](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
