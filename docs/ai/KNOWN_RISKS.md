# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-12  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed Reader baseline at RC-8 audit start:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**Current bounded milestone:** RC-8 architecture/research under issue #373

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted architecture contracts remain authoritative.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- target remains `active=false` and absent from normal runtime composition;
- no cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior exists;
- endpoint/package/profile changes must never silently select a backend;
- no Reader decision in RC-8 activates PostgreSQL/pgvector.

## P1 — Server lifecycle and operational security remain incomplete

- PostgreSQL backup, restore drill, retention and upgrade sequencing are not implemented;
- production pooling, timeout/retry policy, least-privilege roles and distributed fencing remain future work;
- integration `trust` authentication is test-only;
- production credentials must not enter profiles, bundles, receipts, logs, issues or Notion.

## P1 — Current migration evidence remains bounded

SQLite export/verifier and PostgreSQL import evidence is bounded. It is not an institution-scale throughput proof, production SLO or arbitrary-payload guarantee.

## P1 — Production identity, tenancy and distributed coordination remain external

- curator leases are process-local;
- no bundled production IdP;
- no complete multi-tenant isolation proof;
- network policy, credential rotation and distributed fencing remain deployment responsibilities;
- no distributed exactly-once guarantee.

## P1 — Supply-chain hardening is incomplete

- default runtime remains pure standard library;
- Psycopg is an optional extra;
- immutable action pinning, reviewed constraints/checksums, SBOM and scheduled update policy remain future work under #214;
- a green dependency audit is not supply-chain certification.

## P1 — Reader is bounded, not autonomous

RC-1 through RC-7 are merged bounded runtime/domain layers. `dedicated_reader_core=false` remains the larger capability truth.

RC-7 can register explicit caller-selected cross-document pairs, but cannot discover useful pairs across a corpus. RC-8 addresses the architecture/evaluation decision only; it does not implement discovery.

Remaining Reader limits include:

- no automatic parser/chunker/OCR/PDF-layout/multimodal engine;
- no automatic model/provider proposition extraction or summarization;
- no persistent Reader corpus index;
- no Reader candidate-discovery runtime;
- no automatic entity resolution or claim identity;
- no public Reader API/CLI/background worker;
- no automatic evidence admission, contradiction resolution or planner/belief authority.

## P1 — Similarity can create false identity pressure

The most important post-RC-7 retrieval risk is epistemic category collapse:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

High lexical/vector similarity can hide decisive differences in negation, modality, quantifiers, temporal scope, jurisdiction, attribution, units, entity identity or conditions. Conversely, useful paraphrases can have low lexical overlap.

RC-8 therefore requires an explicit adjudication taxonomy and adversarial benchmark before semantic/vector authorization.

## P1 — Existing retrieval machinery is not automatically Reader-safe

Crystal already contains admitted-memory retrieval in `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py` and `core/rrf.py`.

Risk: reusing these modules without a new boundary contract could accidentally blur admitted-L3 query retrieval with PRE-ADMISSION Reader candidate discovery.

Mitigation in RC-8: architecture decision only. Any future reuse must preserve data lifecycle, privacy, reproducibility and authority separation.

## P1 — Semantic/vector retrieval is not yet justified for Reader

Neural embeddings may improve paraphrase/cross-lingual recall, but introduce:

- model/package footprint and optional downloads;
- model/version drift and vector-space mismatch lifecycle;
- privacy/network policy questions;
- non-obvious hard negatives;
- threshold/ranking instability;
- vector index rebuild/migration requirements;
- temptation to treat similarity as identity.

ANN/vector backends additionally add approximation and index-lifecycle complexity.

RC-8 decision: first establish a deterministic lexical baseline and frozen adversarial benchmark in a separate future implementation. Semantic/hybrid work remains deferred until a separately authorized issue pre-registers numeric thresholds and shows measured benefit.

## P1 — SQLite FTS needs capability handling if later selected

SQLite FTS is attractive for local-first persistent lexical discovery, but FTS capabilities can vary by SQLite build. A future Reader backend must feature-detect rather than assume FTS5 availability and must provide a bounded deterministic fallback. RC-8 does not implement FTS.

## P1 — Benchmark misuse could overstate capability

`eval/reader_rc8_retrieval_adversarial.jsonl` is a small synthetic contract corpus. It is designed to expose failure classes, not certify production retrieval quality.

A future evaluator must report per-stratum recall/hard-negative behavior, work bounds and declared resource/model/index identity. Aggregate “accuracy” alone is insufficient.

## P2 — Localization debt remains explicit

Russian Reader-dependent RC-7 surfaces are current to immutable RC-7 English checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, totaling 64 documents. RC-8 adds English architecture/research source only; broad translation stays separate.

## Open backlog isolation

- **#165**: exact normalized ingest dedupe/migration, not near-duplicate or semantic matching. Do not turn it into Reader identity.
- **#155**: Epistemic Router/Evidence State RFC downstream of FactsPack. Do not merge with PRE-ADMISSION discovery.
- **#214**: fixture/PII/supply-chain hygiene. Any future model dependency would require explicit treatment there or in a dedicated security scope.

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles/receipts are operational evidence, not claim evidence;
- retrieval or ANN quality cannot override exact-state mismatch;
- GDPR-oriented controls are engineering controls, not legal compliance/certification;
- no universal truth, zero hallucinations, AGI, consciousness or production certification is claimed;
- NLnet remains `submitted / under review / not awarded`; approximate €50,000 planning only.

## Next actions

1. Complete only RC-8 issue #373: artifacts/tests/docs → exact-head CI → review → guarded merge → post-merge CI → Notion sync/read-back → completion evidence → close.
2. Do **not** automatically start lexical discovery, embeddings, FTS, ANN/vector DB or another Reader milestone after RC-8.
3. Keep #155, #165, #214 and PostgreSQL/cutover/ANN workstreams separate unless a future audit proves a dependency.
4. Preserve exact-head evidence and GitHub↔Notion synchronization for every material boundary change.