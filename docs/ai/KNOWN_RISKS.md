# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-12  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**RC-8 signed merge / RC-9 audited start:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**Current bounded milestone:** RC-9 / issue #375

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted architecture contracts remain authoritative.

## P1 — Reader remains bounded, not autonomous

RC-1 through RC-7 are merged bounded Reader layers; RC-9 adds only PRE-ADMISSION lexical candidate discovery. `dedicated_reader_core=false` remains correct.

Still absent: automatic parser/OCR/multimodal reading, automatic model proposition extraction/summarization, durable Reader retrieval index, semantic/hybrid/vector retrieval, automatic entity/claim identity, public Reader retrieval API/CLI/worker, automatic evidence admission/contradiction resolution/planner authority.

## P1 — Lexical ranking creates false-identity pressure

RC-9 directly measures the RC-8 risk:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

At K=5 the frozen 20-case benchmark returns all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives, including entity/topic collisions and boilerplate overlap. High lexical overlap also ranks negation, modality, quantifier, temporal/version, numeric threshold, jurisdiction and conditional-scope changes highly.

Mitigation: RC-9 outputs inspection candidates only, preserves material tokens, exposes matched terms and carries no identity/truth/corroboration/adjudication fields.

## P1 — Lexical recall is incomplete

RC-9 Recall@5 is 0.937500 over 16 useful paired cases. The cross-lingual paraphrase is missed completely; the low-overlap paraphrase reaches rank 3 only through weak shared lexical material. This is the measured reason for `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

It is not permission to add embeddings. A future comparison must be separately authorized and pre-register success/failure thresholds before seeing comparison results.

## P1 — Benchmark misuse could overstate capability

`eval/reader_rc8_retrieval_adversarial.jsonl` is only 20 synthetic paired cases. Precision@K uses other returned corpus entries as synthetic decoys because only each left/right mate is judged. The benchmark measures baseline behavior; it does not certify production retrieval or semantic adjudication accuracy.

## P1 — In-memory O(corpus) baseline is not a scale claim

RC-9 intentionally performs bounded O(corpus) lexical scoring with at most 100000 records and top-K <= 1000. It introduces no durable index lifecycle. SQLite FTS may be evaluated later only under a separate scaling need and feature-detection/fallback contract.

## P1 — Existing retrieval machinery is a separate authority domain

`core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py` and `core/rrf.py` remain admitted-memory/query components. RC-9 does not call them. Reuse in a future Reader milestone must not blur PRE-ADMISSION discovery with strict read grounding or identity authority.

## P1 — Semantic/vector retrieval remains unauthorised for Reader

Neural embeddings/ANN may improve some recall but add model/version drift, footprint/download/privacy, non-obvious hard negatives, threshold instability, index rebuild/mismatch lifecycle and identity-pressure risk. RC-9 measured a gap but did not perform or authorize a semantic comparison.

## P1 — Storage and operational risks remain unchanged

PostgreSQL/pgvector is an inactive migration target `active=false`; no ordinary runtime adapter/cutover/dual-write/automatic switching/distributed exactly-once guarantee exists. Production identity, tenancy, distributed coordination, backup/restore operations, least privilege and supply-chain hardening remain separate work. #214 continues to track fixture/PII/supply-chain hygiene.

## P2 — Localization debt remains explicit

Russian Reader-dependent RC-7 surfaces remain current; eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, totaling 64 documents. RC-9 updates English authoritative material only.

## Open backlog isolation

- **#165**: exact normalized admitted-fact dedupe/migration; not near-duplicate/semantic matching.
- **#155**: downstream Epistemic Router/Evidence State RFC.
- **#214**: fixture/PII/supply-chain hygiene.

## Claim and grant boundaries

Physical L3 is not strict Canon. Retrieval quality cannot create claim evidence or override Guardian/TruthGate. GDPR-oriented controls are engineering controls, not legal certification. NLnet remains `submitted / under review / not awarded`; approximate €50,000 is planning only.

## Current actions

1. Complete only RC-9 issue #375 through exact-head CI, independent review, guarded merge, signed `main`, exact post-merge CI, Notion 3/3 sync/read-back, completion evidence and closure.
2. Do not automatically start semantic/hybrid retrieval, embeddings, FTS, ANN/vector DB, localization refresh, #155, #165 or #214 after RC-9.
