# 🧭 Reader RC-10 — Existing Retrieval Reuse Compatibility + Comparison Pre-Registration

**Status:** ARCHITECTURE / EVALUATION CONTRACT — NO COMPARISON EXECUTED  
**Tracking issue:** #377  
**Audited starting point:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`  
**Predecessor:** `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`  
**Documentation impact:** `GITHUB_AND_NOTION`

## 1. Purpose

RC-10 exists because Crystal already contains substantial retrieval machinery outside the Reader authority domain. The safe next step after RC-9 is therefore **not to build another retrieval stack**. It is to determine what can be reused as a bounded comparison primitive, what must remain isolated from PRE-ADMISSION Reader artifacts, and what evidence must exist before any later semantic/hybrid implementation proposal is even eligible for review.

RC-10 does not run a semantic comparison and does not add Reader retrieval runtime.

```text
RC-9 measured lexical baseline
        ↓
existing-retrieval dedup / compatibility audit
        ↓
pre-register comparison modes + gates
        ↓
STOP
        ↓
future isolated comparison requires separate authorization
```

## 2. Live dedup audit

The audit found the following existing admitted-memory retrieval stack on merged `main`:

- `core/embedding.py` — deterministic `HashingEmbedder`, opt-in `TrigramHashingEmbedder`, optional `SentenceTransformerEmbedder`, embedder identity/fingerprint handling;
- `core/pipeline.py` — admitted-memory vector retrieval, graph-walk/spreading activation and RRF ordering;
- `core/query_pipeline.py` — strict read-only admitted-memory query path with trust reconciliation;
- `core/legacy_retrieval.py` — bounded lexical fallback for no-fingerprint admitted stores;
- `core/retrieval_config.py` — bounded admitted-memory retrieval knobs;
- `core/rrf.py` — pure-standard-library Reciprocal Rank Fusion ordering utility.

Closed issue #317 / merged PR #321 already solved bounded legacy no-fingerprint lexical retrieval for admitted-memory query surfaces. RC-10 must not recreate that work under a Reader name.

The audit also found that FTS/BM25 scaling is already discussed in `docs/core/DEDUP_AND_SCALE.md` and the RC-8 decision. Repository search found no Reader SQLite FTS5 virtual-table / `MATCH` runtime implementation on the audited main. FTS is therefore a documented future option, not existing Reader runtime to duplicate.

## 3. Authority-domain separation

Existing retrieval code is useful evidence and potential implementation material, but its current callers and data assumptions matter:

```text
ADMITTED MEMORY
physical L3 / trust reconciliation / strict read projection
        ↓
query + embedding + graph retrieval

PRE-ADMISSION READER
RC-4 proposition candidates
        ↓
RC-9 lexical candidate discovery
        ↓
inspection / later explicit adjudication
```

A function being pure or reusable does not erase the authority boundary around the data supplied to it.

## 4. Reuse-compatibility matrix

| Existing component | RC-10 disposition | Why |
|---|---|---|
| `core/rrf.py` | **ELIGIBLE_FOR_FUTURE_READER_COMPARISON_REUSE** | Pure stdlib rank fusion; compares rank positions, returns candidate objects unchanged; no storage/truth side effects. Any Reader use must provide a Reader candidate identity key and retain the authority firewall. |
| `HashingEmbedder` | **COMPARATOR_SIGNAL_ONLY** | Deterministic and stdlib, but its token policy differs from RC-9 and removes several words as stopwords. It is not a semantic oracle or safe identity owner. |
| `TrigramHashingEmbedder` | **COMPARATOR_SIGNAL_ONLY** | Deterministic character signal useful for morphology/typo tolerance, but can raise short/noisy false positives and has its own normalization/stopword policy. |
| `SentenceTransformerEmbedder` | **FUTURE_OPTIONAL_COMPARATOR_ONLY** | Optional third-party/model lifecycle, possible model download, drift/version/privacy/resource concerns. Requires separate execution authorization with pinned package/model identity and offline evaluation policy. |
| `get_embedder("auto")` | **FORBIDDEN_FOR_PREREGISTERED_READER_COMPARISON** | Auto selection/fallback can change the actual backend and may attempt model loading/downloading; it is not a stable experiment identity. |
| `core/pipeline.retrieve()` | **DO_NOT_REUSE_AS_READER_PIPELINE** | Coupled to admitted L3 vector search, confidence-weighted relevance, graph-walk and admitted-memory lifecycle. Direct Reader wiring would blur authority domains. |
| `core/query_pipeline.py` | **DO_NOT_REUSE_AS_READER_PIPELINE** | Coupled to strict read-only Canon/trust reconciliation and admitted-memory public query semantics. |
| `core/legacy_retrieval.py` | **DO_NOT_REUSE_AS_READER_BACKEND** | Bounded lexical logic is tied to admitted-L3 backend candidate windows. RC-9 already owns the Reader lexical baseline. |
| SQLite FTS5 | **NOT_IMPLEMENTED_FOR_READER / FUTURE_SCALING_OPTION** | May reduce O(corpus) work, but feature availability varies by SQLite build; any later backend must feature-detect and retain bounded deterministic fallback. |
| PostgreSQL/pgvector | **NOT_AUTHORIZED_FOR_READER** | Current target remains inactive `active=false`; no Reader need or ANN evidence authorizes activation. |

## 5. Important embedder-policy finding

The deterministic hashing embedders are useful comparison signals, but they are not drop-in replacements for the RC-9 tokenizer. Their normalization deliberately removes stopwords. Some of those tokens can carry Reader-relevant scope/modality information in other contexts. Therefore:

```text
existing deterministic embedder != Reader-safe semantic contract
```

A future comparison may measure such a signal, but the signal cannot silently redefine the Reader proposition representation or adjudication vocabulary.

## 6. Frozen baseline

RC-10 freezes RC-9 as the control arm:

- method: `reader_rc9_bm25_lexical_v1`;
- corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`;
- corpus Git blob: `4be317549d7a8eae9d69f9fa208d07d8855779a4`;
- result: `eval/reader_rc9_lexical_baseline.json`;
- result Git blob: `7ffbc86d713b7be89d393fe56c2d160b9dee98dc`;
- K: 5;
- useful paired hits: 15/16;
- Recall@5: 0.937500;
- Precision@5: 0.187500 under the bounded fixed-K synthetic definition;
- MRR: 0.895833;
- paired hard-negative hits: 4/4;
- paired hard-negative rate@5: 1.000000;
- known useful miss: `rc8-004` cross-lingual paraphrase.

The 20-case fixture is intentionally small and paired. It is useful for a preregistered diagnostic comparison, but it is not sufficient to authorize production semantic retrieval even if every RC-10 comparison gate passes.

## 7. Pre-registered comparison gate

The machine-readable contract is `eval/reader_rc10_retrieval_comparison_preregistration.json`.

A future comparator becomes **eligible for further architecture review only** when all of the following hold on the unchanged RC-8 corpus at K=5:

1. all 15 useful pairs already retrieved by RC-9 remain retrieved;
2. `rc8-004` is recovered, producing 16/16 useful paired recall / Recall@5 = 1.0;
3. MRR is at least the RC-9 baseline `0.895833`;
4. paired hard-negative hits fall from 4/4 to at most 2/4 (rate <= 0.5);
5. authority violations are exactly zero;
6. exact comparator/backend identity is recorded; `auto` mode is forbidden;
7. query-time network calls are zero and Reader source text is not sent to an external service;
8. a later runtime proposal must retain a bounded deterministic lexical fallback.

The hard-negative requirement intentionally demands a material reduction, not merely recall recovery. Added semantic complexity is not justified if it only recovers one paraphrase while continuing to surface every known identity trap.

## 8. What a passing comparison means

```text
comparison pass
    = eligible for a stronger/larger evaluation and architecture review
    != Reader runtime authorization
    != semantic identity authority
    != evidence admission
    != Canon relation
```

Because the current corpus is small and known, a passing future comparison must still be followed by a separately authorized stronger evaluation surface before any Reader runtime adoption decision.

## 9. Reproducibility and privacy rules

Any future comparison must record:

- exact code SHA;
- exact comparator class/mode;
- exact model name + immutable revision/checksum when a model is involved;
- exact dependency versions for optional third-party comparison modes;
- corpus/result identities;
- K and metric definitions;
- query-time network-call count;
- whether model assets were preloaded locally;
- repeatability/determinism observation;
- resource observations with environment caveats.

Forbidden for a qualifying comparison:

- `VELANTRIM_EMBEDDER=auto` or equivalent backend auto-selection;
- query-time model download;
- external API transmission of Reader source text;
- post-result threshold edits;
- treating similarity/rank as an adjudication label.

## 10. Authority firewall

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

RC-10 adds no TruthGate, Guardian, ESM, evidence or Canon mutation.

## 11. Explicit non-implementation

RC-10 implements no:

- semantic/hybrid comparison run;
- SentenceTransformer/model download;
- Reader embedding/vector runtime;
- SQLite FTS schema/index;
- ANN/FAISS/HNSW/vector database;
- PostgreSQL/pgvector activation;
- automatic entity resolution;
- claim identity/equivalence decision;
- contradiction adjudication/winner selection;
- evidence admission or RC-7 auto-registration;
- public Reader API/CLI/worker;
- broad localization refresh.

`dedicated_reader_core=false` remains correct.

## 12. Backlog boundary

Issues #155, #165 and #214 remain separate:

- #155 — downstream Epistemic Router / evidence-state observability;
- #165 — exact normalized admitted-fact migration/dedupe, explicitly not semantic matching;
- #214 — fixture/PII/supply-chain hardening.

A future optional model comparator would need explicit dependency/privacy treatment, but RC-10 does not implement one and therefore does not absorb #214.

## 13. Public documentation drift found by the audit

The post-RC-9 live audit found that several GitHub orientation/status surfaces still described RC-9 as in progress even though PR #376 is merged and issue #375 is completed. `README.md` also still presents an older RC-6/RC-7-in-progress public checkpoint.

RC-10 must reconcile the compact/current English truth surfaces to signed RC-9 completion. Broad localized README/detail refresh remains a separate documentation milestone under the existing localization policy; RC-10 must not falsely mark lagging translations current to RC-10.

## 14. Grant boundary

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning context only. RC-0 through RC-10 completed before any agreement are existing baseline, not evidence of awarded delivery.

## 15. Stop boundary

RC-10 ends after its architecture/evaluation contract, truth reconciliation, exact CI/review, guarded merge, signed post-merge CI, Notion synchronization/read-back and issue completion.

Do not automatically execute a semantic/hybrid comparison, implement FTS, add an embedding runtime, start ANN/vector indexing, refresh all translations or begin #155/#165/#214.
