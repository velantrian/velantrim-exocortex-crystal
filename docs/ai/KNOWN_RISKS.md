# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-12  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 post-merge CI:** `31594027040` — 9/9 successful  
**Current bounded milestone:** RC-10 architecture/evaluation preregistration under issue #377

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted architecture contracts remain authoritative.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- target remains `active=false` and absent from normal runtime composition;
- no cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior exists;
- no Reader decision or RC-10 contract activates PostgreSQL/pgvector.

## P1 — Server lifecycle and operational security remain incomplete

PostgreSQL production backup/restore sequencing, pooling, retry policy, least privilege and distributed fencing remain future work. Integration trust auth is test-only.

## P1 — Current migration evidence remains bounded

SQLite export/verifier and PostgreSQL import evidence is bounded. It is not an institution-scale throughput proof or production SLO.

## P1 — Production identity, tenancy and distributed coordination remain external

Curator leases remain process-local; no bundled production IdP or complete multi-tenant/distributed coordination proof exists.

## P1 — Supply-chain hardening is incomplete

Default runtime remains pure standard library. Psycopg is optional. Immutable action pinning, reviewed constraints/checksums, SBOM and scheduled update policy remain future work under #214. RC-10 adds no dependency or model runtime.

## P1 — Reader is bounded, not autonomous

RC-1 through RC-7 are merged bounded runtime/domain layers. RC-8 is completed architecture/research. RC-9 is a completed PRE-ADMISSION lexical candidate-discovery baseline. RC-10 adds only reuse compatibility and a pre-registered future comparison gate. `dedicated_reader_core=false` remains the larger capability truth.

Remaining Reader limits include no automatic parser/OCR/model extraction, no persistent Reader corpus index, no semantic/hybrid/vector Reader runtime, no entity/claim identity, no public Reader API/CLI/worker, and no automatic evidence admission/contradiction winner/planner authority.

## P1 — Similarity can create false identity pressure

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

High lexical/vector similarity can hide decisive differences in negation, modality, quantifiers, time, jurisdiction, attribution, units, entity identity or conditions. Useful paraphrases can also have low lexical overlap.

RC-9 measured this directly: all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard negatives surface at K=5 while cross-lingual `rc8-004` is missed. `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP` remains a retrieval finding, not authorization.

## P1 — Existing retrieval machinery is not automatically Reader-safe

Crystal already contains `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py` and admitted-memory retrieval composition in `core/pipeline.py`.

RC-10 makes the risk explicit:

- admitted-memory pipeline/query/legacy retrieval must not be wired directly into PRE-ADMISSION Reader;
- hashing/trigram embedders are comparator signals only;
- existing embedder token/stopword policy is not automatically Reader-safe semantic representation;
- `get_embedder("auto")` is not a stable experiment identity;
- pure RRF may be reused only as ordering, with Reader candidate identity and no authority promotion.

## P1 — Semantic/vector retrieval remains unauthorized for Reader

Neural embeddings may improve paraphrase/cross-lingual recall but introduce model/package footprint, model/version drift, privacy/network questions, non-obvious hard negatives, threshold instability and index lifecycle. ANN adds approximation and lifecycle complexity.

RC-10 does not run a semantic comparison. Its future gate requires simultaneous recall recovery and hard-negative improvement. Passing that gate only permits stronger evaluation/architecture review.

## P1 — SQLite FTS requires capability handling if later selected

FTS/BM25 scaling is already documented in `docs/core/DEDUP_AND_SCALE.md` and RC-8. Repository audit found no current Reader FTS5 virtual-table / `MATCH` implementation. If later selected, FTS5 availability must be feature-detected and bounded deterministic fallback retained.

## P1 — Benchmark misuse could overstate capability

The RC-8 fixture is a small synthetic 20-case paired diagnostic corpus, not fully judged all-pairs qrels and not production certification. RC-9 Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833` and paired hard-negative rate `1.000000` are bounded retrieval evidence only.

RC-10 explicitly prevents a passing future comparison from becoming runtime authorization. A stronger/larger evaluation remains required.

## P1 — In-memory O(corpus) RC-9 baseline is not a scale claim

RC-9 uses bounded in-memory O(corpus) scoring. Its frozen 20-record benchmark does not establish production corpus-scale latency or memory behavior.

## P1 — Public English README drift

The post-RC-9 audit found `README.md` still presenting an older RC-6/RC-7-in-progress checkpoint. That underclaims current implementation rather than granting unsafe authority, but it violates the desired public truth synchronization. RC-10 records the finding; broad root/localized README reconciliation remains a separate documentation milestone because the localization policy requires source-checkpoint/freshness accounting rather than a hidden English-only rewrite.

## P2 — Localization debt remains explicit

Russian Reader-dependent surfaces remain current to immutable RC-7 checkpoint `ab3ad31c437647535030e371d58f456faf14017b`; eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, 64 documents. RC-8 through RC-10 add English source meaning only.

## Open backlog isolation

- **#165**: exact normalized ingest dedupe/migration, not near-duplicate or semantic matching.
- **#155**: Epistemic Router/Evidence State RFC downstream of FactsPack.
- **#214**: fixture/PII/supply-chain hygiene.

## Claim and grant boundaries

Physical L3 is not strict Canon; retrieval/ANN quality cannot override evidence/trust policy; GDPR-oriented controls are engineering controls, not legal certification; no universal truth/AGI/consciousness claim exists. NLnet remains `submitted / under review / not awarded`; approximate €50,000 planning only.

## Next actions

1. Complete only RC-10 issue #377: preregistration/status reconciliation → exact-head CI → review → guarded merge → signed/verified main → post-merge CI → Notion sync/read-back → completion evidence → close → STOP.
2. Do **not** automatically execute semantic/hybrid comparison, implement FTS, embeddings, ANN/vector DB, localization refresh, #155, #165 or #214.
3. Preserve exact-head evidence and GitHub↔Notion synchronization for every material boundary change.
