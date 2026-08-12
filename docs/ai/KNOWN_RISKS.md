# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-12  
**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 post-merge CI:** `31594027040` — 9/9 successful  
**Audited start after PR #378:** `main@430e643a2a3759da793f700617a327d419439dde`, CI `31603785427` — 9/9 successful  
**Current bounded milestone:** issue #379 — post-RC-9 grant presentation truth reconciliation

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues
and accepted architecture contracts remain authoritative.

## P1 — PostgreSQL is an inactive migration target, not active runtime

- target remains `active=false` and absent from normal runtime composition;
- no cutover, rollback, dual-write, automatic switching or distributed exactly-once behavior exists;
- endpoint/package/profile changes must never silently select another store;
- no Reader decision, RC-9 implementation, PR #378 preregistration or issue #379 docs work activates PostgreSQL/pgvector.

## P1 — Server lifecycle and operational security remain incomplete

- PostgreSQL backup/restore drill, retention and upgrade sequencing remain separate future work;
- production pooling, timeout/retry policy, least-privilege roles and distributed fencing remain future work;
- integration `trust` authentication is test-only;
- production credentials must not enter profiles, bundles, receipts, logs, issues or Notion.

## P1 — Current migration evidence remains bounded

SQLite export/verifier and PostgreSQL import evidence is bounded. It is not an institution-scale
throughput proof, production SLO or arbitrary-payload guarantee.

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

Issue #379 adds no dependency, package, network service or model download.

## P1 — Reader remains bounded, not autonomous

RC-1 through RC-7 are merged bounded runtime/domain layers. RC-8 is a completed architecture/
research decision. RC-9 is the completed PRE-ADMISSION lexical candidate-discovery
implementation baseline. PR #378 adds only retrieval-reuse compatibility plus a preregistered
future comparison gate. `dedicated_reader_core=false` remains the larger capability truth.

Remaining Reader limits include:

- no automatic parser/chunker/OCR/PDF-layout/multimodal engine;
- no automatic model/provider proposition extraction or summarization;
- no persistent Reader corpus index;
- no semantic/hybrid/vector Reader runtime;
- no automatic entity resolution or claim identity;
- no public Reader API/CLI/background worker;
- no automatic evidence admission, contradiction resolution or planner/belief authority.

## P1 — Similarity can create false identity pressure

The core retrieval risk remains epistemic category collapse:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

High lexical/vector similarity can hide decisive differences in negation, modality,
quantifiers, temporal scope, jurisdiction, attribution, units, entity identity or conditions.
Conversely, useful paraphrases can have low lexical overlap.

RC-9 directly measured this risk: at K=5 all four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard
negatives surface, including same-topic/entity collisions and boilerplate overlap. The
cross-lingual `rc8-004` pair is missed.

Mitigation remains fail-closed: Reader retrieval returns inspection candidates only;
identity/evidence/adjudication fields remain absent.

## P1 — Lexical recall is incomplete

The frozen RC-9 baseline reaches Recall@5 `0.937500` over 16 useful paired cases and MRR
`0.895833`. It misses the cross-lingual paraphrase completely. Useful paired hits are 15/16.

This produces `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. It does not authorize semantic/vector
work. PR #378 freezes future comparison requirements before any result is observed; no
qualifying semantic/hybrid comparison has been executed.

## P1 — Hard-negative pressure is explicit

RC-9 paired hard-negative rate@5 is `1.000000`: all 4/4 known paired hard negatives are
surfaced. This is not hidden by the grant presentation. Any later comparison must treat reduced
hard-negative pressure as an explicit objective rather than optimizing recall alone.

## P1 — Existing retrieval machinery is not automatically Reader-safe

Crystal already contains admitted-memory retrieval in:

- `core/embedding.py`;
- `core/legacy_retrieval.py`;
- `core/retrieval_config.py`;
- `core/query_pipeline.py`;
- `core/rrf.py`;
- admitted vector/graph retrieval composition in `core/pipeline.py`.

Closed #317 / merged PR #321 already implemented a bounded legacy lexical fallback for admitted-
memory stores. Reimplementing or wiring that stack directly under a Reader name would create
duplicate semantics and authority confusion.

PR #378 therefore records reuse disposition without executing a comparator:

- admitted-memory pipeline/query/legacy retrieval must not be wired directly into PRE-ADMISSION Reader;
- `HashingEmbedder` / `TrigramHashingEmbedder` are comparator signals only;
- optional `SentenceTransformerEmbedder` is a future comparator only under separate pinned dependency/model/privacy authorization;
- `get_embedder("auto")` is forbidden for a qualifying preregistered Reader comparison;
- pure `core/rrf.py` may be reused only as ordering with explicit Reader candidate identity and no authority promotion.

## P1 — Semantic/vector retrieval remains unauthorized for Reader

Neural embeddings may improve paraphrase/cross-lingual recall, but introduce model/package
footprint, version drift, privacy/network questions, hard negatives, ranking instability and
index lifecycle complexity.

No semantic/hybrid comparison, ANN acceptance, vector DB or semantic Reader runtime exists.
Passing a future comparison gate would mean only eligibility for stronger evaluation and
architecture review, not runtime authorization.

## P1 — SQLite FTS needs capability handling if later selected

SQLite FTS/BM25 scaling is documented, but no current Reader FTS5 virtual-table / `MATCH`
implementation exists. A future scaling backend must feature-detect rather than assume FTS5 and
must preserve a bounded deterministic fallback.

## P1 — Benchmark misuse could overstate capability

`eval/reader_rc8_retrieval_adversarial.jsonl` is a small synthetic 20-case paired contract
corpus designed to expose failure classes, not certify production retrieval quality.

RC-9 metrics:

- Recall@5 `0.937500`;
- Precision@5 `0.187500` under the bounded fixed-K paired benchmark definition;
- MRR `0.895833`;
- paired hard-negative rate@5 `1.000000`.

These are retrieval metrics, not “94% accuracy”, semantic precision, claim-identity accuracy,
truth accuracy, contradiction accuracy or evidence-admission correctness. A stronger/larger
evaluation surface remains required before any semantic Reader runtime adoption could be
considered.

## P1 — In-memory O(corpus) RC-9 baseline is not a scale claim

RC-9 intentionally uses a bounded in-memory O(corpus) scorer. The frozen benchmark has 20 index
records and 20 queries (at most 400 record comparisons). This is a baseline measurement, not a
production-scale indexing or latency/SLO claim.

## P1 — Exact-vs-ANN / semantic comparison remains unexecuted

The repository has historical exact/vector retrieval mechanisms in admitted-memory paths, but
no qualifying Reader exact-vs-ANN or semantic/hybrid comparison has been executed. PR #378 only
freezes future comparison requirements.

## P1 — Grant/public claim drift requires executable protection

The post-RC-9 live audit found the root English README and primary grant baseline documents
still presenting RC-6/RC-7-in-progress or RC-5/RC-6-in-progress truth. It also found
`scripts/check_d4_source_contract.py` actively requiring stale RC-5 grant markers.

Issue #379 addresses this by reconciling the English public/grant surfaces and changing the D4
semantic validator so stale baseline language cannot silently return. Until #379 merges and
post-merge CI is green, the starting main remains the authoritative public state.

## P2 — Localization debt remains explicit

Russian Reader-dependent D1/D3/D4/D5 surfaces remain tied to immutable RC-7 checkpoint
`ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain
`REFRESH_NEEDED`, totaling 64 tracked detail documents.

Issue #379 advances the English root/grant presentation to post-RC-9 truth but deliberately does
not perform broad translation. Localized surfaces must not be represented as current to the new
English first-impression source until a dedicated localization refresh.

## Open backlog isolation

- **#165**: exact normalized ingest dedupe/migration, not near-duplicate or semantic matching.
- **#155**: Epistemic Router/Evidence State RFC downstream of FactsPack.
- **#214**: fixture/PII/supply-chain hygiene.
- **#377**: separate RC-10 preregistration/completion bookkeeping; #379 does not execute its future comparator.

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles/receipts are operational evidence, not claim evidence;
- retrieval quality cannot override evidence/trust policy;
- local-first/offline does not itself prove security or GDPR compliance;
- no universal truth, zero hallucinations, AGI, consciousness or production certification is claimed;
- NLnet remains `submitted / under review / not awarded`; approximate €50,000 planning only.

## Next actions

1. Complete only issue #379: public/grant reconciliation → exact-head CI → independent semantic review → guarded merge → signed main → exact post-merge CI → Notion sync/read-back → completion evidence → close → final live audit → STOP.
2. Do **not** automatically execute semantic/hybrid comparison, implement FTS, embeddings, ANN/vector DB, localization refresh, #155, #165 or #214 after #379.
3. Keep #377 and all technical backlog separate unless a future live audit plus explicit authorization changes that boundary.
