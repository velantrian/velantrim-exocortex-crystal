# 🔎 Reader RC-9 — Deterministic Lexical Candidate Discovery Baseline

**Status:** BOUNDED IMPLEMENTATION / PRE-ADMISSION RETRIEVAL BASELINE  
**Tracking issue:** #375  
**Live implementation baseline audited:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6`  
**Predecessor decision:** `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`  
**Documentation impact:** `GITHUB_AND_NOTION`

## 1. Purpose

RC-9 implements the first measured Reader candidate-discovery baseline authorized by RC-8. It answers only:

> Which already extracted Reader proposition candidates are lexically worth inspecting together?

It does **not** answer whether two propositions are identical, true, corroborating, contradictory, admissible evidence, or related in strict Canon.

```text
RC-4 source-linked proposition candidates
        ↓
Reader-safe lexical snapshot
        ↓
conservative normalization + stable tokens
        ↓
in-memory BM25 lexical ranking
        ↓
structured inspection candidates
        ↓
manual/downstream review only
```

No RC-7 link is auto-registered. No evidence, ESM, Guardian, TruthGate or Canon state is mutated.

## 2. Authority firewall

The RC-8 invariants remain unchanged:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

`lexical_score` is only a ranking signal. `matched_terms` are only an explanation of that lexical score. Neither field carries a truth, evidence, corroboration, contradiction, or claim-identity verdict.

## 3. Implementation

Runtime module: `core/reader_lexical_discovery.py`.

The baseline is deliberately small:

- pure Python standard library;
- in-memory only;
- deterministic `reader_rc9_bm25_lexical_v1` scoring;
- no network calls;
- no model/provider dependency;
- no embeddings or vector representation;
- no SQLite schema or durable index yet;
- no PostgreSQL/pgvector activation;
- no public API/CLI/background-worker wiring.

`ReaderLexicalRecord.from_candidate()` snapshots the public RC-4 candidate surface into a retrieval-only record containing source/session/candidate/document identity and the proposition text. The source SHA-256 is validated. Restricted/sensitivity metadata is preserved rather than discarded.

`ReaderLexicalIndex` sorts input records by a stable source/session/candidate key before building token statistics. Discovery excludes self matches and, by default, candidates from the same document identity. Ties are broken by the same stable key.

Work is explicitly bounded by:

- `MAX_READER_LEXICAL_RECORDS = 100000`;
- `MAX_READER_LEXICAL_TOP_K = 1000`.

This is an O(corpus) baseline intended to measure lexical behavior, not a claim of production-scale indexing.

## 4. Conservative normalization

`normalize_reader_lexical_text()` performs only:

- Unicode NFKC normalization;
- Unicode-aware case folding;
- whitespace collapse.

Tokenization does **not** remove stop words and does not perform stemming, synonym replacement, unit conversion, translation, entity resolution, lemmatization or semantic rewriting.

The purpose is to avoid silently erasing distinctions such as:

- `not`;
- `must` / `may`;
- `all` / `most`;
- years and dates;
- versions such as `3.11` / `3.12`;
- numeric thresholds such as `80` / `90`;
- named terms and jurisdiction markers.

Preserving a token does not mean BM25 understands its logical role. RC-9 intentionally measures that limitation instead of hiding it.

## 5. Result contract

Each `ReaderLexicalMatch` contains only auditable retrieval fields:

- query session/candidate/document identifiers;
- candidate session/candidate/document identifiers;
- candidate source URI and source SHA-256;
- lexical score;
- deterministic rank;
- retrieval method/version;
- matched lexical terms;
- restricted/sensitivity metadata.

It deliberately has no fields such as:

```text
truth_score
confidence_of_truth
corroboration_score
same_claim
confirmed_contradiction
canon_relation
```

## 6. Benchmark runner

Runner: `scripts/bench_reader_rc9_lexical.py`.

Frozen input: `eval/reader_rc8_retrieval_adversarial.jsonl` (20 synthetic cases from RC-8).

Committed machine-readable result: `eval/reader_rc9_lexical_baseline.json`.

Reproduce with:

```bash
python scripts/bench_reader_rc9_lexical.py \
  --corpus eval/reader_rc8_retrieval_adversarial.jsonl \
  --k 5 \
  --json-out /tmp/reader-rc9-lexical.json
```

The benchmark treats these RC-8 review classes as useful **retrieval intent only**:

```text
SAME_PROPOSITION_CANDIDATE
PARAPHRASE_CANDIDATE
RELATED_CLAIM
POSSIBLE_CONTRADICTION
```

The paired `SAME_TOPIC` and `MERELY_SIMILAR` cases are hard negatives. This mapping is only for benchmark retrieval measurement; the ranker does not emit any RC-8 review class.

### Metric scope

The RC-8 JSONL judges only each case's left/right pair. Therefore:

- Recall@K and MRR ask whether the known useful paired right side was surfaced;
- Precision@K treats other returned corpus entries as synthetic benchmark decoys;
- paired hard-negative rate asks whether the known `SAME_TOPIC` / `MERELY_SIMILAR` mate was surfaced.

These numbers are not adjudication accuracy and do not certify semantic equivalence.

## 7. Frozen RC-9 baseline result

At `K=5` over the 20-case frozen RC-8 corpus:

| Metric | Result |
|---|---:|
| Useful paired cases | 16 |
| Hard-negative paired cases | 4 |
| Recall@5 | **0.937500** |
| Precision@5 | **0.217391** |
| MRR | **0.895833** |
| Paired hard-negative rate@5 | **1.000000** |
| Positive paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |
| Index records | 20 |
| Queries | 20 |
| Maximum record comparisons | 400 |
| Network calls | 0 |
| Mandatory third-party dependencies | 0 |

The baseline misses the cross-lingual paraphrase (`rc8-004`). The low-lexical-overlap paraphrase (`rc8-003`) is only rank 3 and is driven by the weak shared token `the`; this is not evidence of semantic understanding. All four deliberately dangerous hard-negative mates are surfaced within top-5, including same-topic/entity collisions and boilerplate overlap.

Several high-overlap scope changes also rank very highly: negation, modality, quantifier, time/version, numeric threshold, jurisdiction and conditional changes. That is expected for lexical discovery and is exactly why ranking cannot be treated as identity or truth.

## 8. Architectural interpretation

The measured RC-9 result is classified as:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

This classification means only:

1. lexical discovery is useful enough to surface most frozen useful pairs;
2. it misses at least one intentionally important semantic stratum;
3. it also surfaces all frozen hard-negative mates at K=5;
4. therefore lexical rank alone is insufficient for adjudication and leaves measurable discovery-quality gaps.

It does **not** mean embeddings, hybrid retrieval, ANN or a vector database are now authorized. Any comparison against semantic/hybrid machinery remains a separate future architecture milestone with pre-registered thresholds, dependency/privacy/resource review and exact benchmark evidence.

## 9. Relationship to existing retrieval

Existing admitted-memory retrieval remains a separate domain:

```text
PRE-ADMISSION Reader
RC-4 → RC-9 lexical discovery → review/adjudication → normal admission boundary

ADMITTED MEMORY
strict read projection → existing query/embedding/legacy retrieval
```

RC-9 does not call `core/embedding.py`, `core/legacy_retrieval.py`, `core/query_pipeline.py`, `core/rrf.py` or L3 storage. The fact that those modules already exist does not make them Reader identity authority.

## 10. Storage and dependency decision

The audited repository already has ordinary active SQLite plus inactive PostgreSQL/pgvector migration infrastructure. RC-9 needs neither.

An in-memory implementation is sufficient for the bounded 20-case evidence baseline and avoids introducing a storage/index lifecycle before a measured scale requirement exists. SQLite FTS remains an option for a future separately scoped scaling milestone, not an RC-9 dependency.

Default runtime dependencies remain unchanged: none.

## 11. Tests

RC-9 tests cover at least:

- deterministic normalization/tokenization;
- preservation of negation, modality/quantifier tokens, numbers, dates and versions;
- record/source SHA contract;
- deterministic ranking and stable tie-breaking;
- top-K bounds;
- empty lexical input;
- duplicate query terms;
- self-match exclusion;
- cross-document filtering;
- restricted/sensitivity propagation;
- absence of authority-like result fields;
- malformed/empty/duplicate benchmark fixtures;
- metric calculation;
- hard-negative behavior;
- frozen RC-8 corpus → committed snapshot reproducibility.

Repository CI remains authoritative for full Python 3.11/3.12 + 100% coverage and the other permanent gates.

## 12. Non-features after RC-9

RC-9 still does not implement:

- semantic Reader retrieval;
- embeddings or sentence-transformers for Reader;
- ANN / FAISS / HNSW / vector DB;
- PostgreSQL/pgvector Reader activation;
- automatic entity resolution;
- automatic claim identity;
- automatic contradiction adjudication or winner selection;
- automatic evidence admission or Canon linking;
- durable Reader retrieval index/schema;
- public Reader retrieval API/CLI;
- background retrieval worker;
- dedicated/full autonomous Reader runtime.

`dedicated_reader_core=false` therefore remains correct.

## 13. Backlog and localization boundary

Issues #155, #165 and #214 remain separate and are not absorbed by RC-9.

RC-9 changes authoritative English implementation/status material only. Russian Reader-dependent RC-7 material remains `CURRENT` at its recorded immutable checkpoint; the eight other Reader-dependent locale packs remain `REFRESH_NEEDED` (64 tracked documents). Broad localization is a separate milestone.

## 14. Grant boundary

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning context only. RC-9 is a pre-agreement implementation/research baseline if merged before any funding agreement; it is not evidence of an award or funded delivery.

## 15. Stop boundary

After RC-9 completion evidence, stop. Do not automatically start RC-10, hybrid/semantic retrieval, embeddings/vector indexing, localization refresh, #155, #165 or #214.
