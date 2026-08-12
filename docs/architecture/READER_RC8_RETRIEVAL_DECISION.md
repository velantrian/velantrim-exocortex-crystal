# 🔎 Reader RC-8 — Post-RC-7 Candidate Discovery & Retrieval Architecture Decision

**Status:** BOUNDED ARCHITECTURE / RESEARCH DECISION — no Reader retrieval runtime implementation  
**Tracking issue:** #373  
**Live baseline audited:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`  
**RC-7 merge:** PR #372, exact validated head `b1cf79594f702194b4dce66ac2ef2546d4154f15`  
**RC-7 exact-head CI:** `31572324596` — 9/9 SUCCESS  
**RC-7 post-merge CI:** `31572918731` — 9/9 SUCCESS  
**Documentation impact:** `GITHUB_AND_NOTION`

## 1. Decision

RC-8 does **not** authorize embeddings, ANN, a vector database, automatic semantic matching, entity resolution, or automatic cross-document claim identity for Reader Core.

The post-RC-7 capability gap is real, but the missing capability is **candidate discovery with explicit identity/adjudication boundaries and measurable evaluation**, not “a vector backend” by itself.

The next implementation, if separately authorized after this milestone, should establish a deterministic lexical candidate-discovery baseline and benchmark runner first. Semantic/hybrid retrieval may be compared later against that frozen baseline. It is not justified as an ordinary Reader dependency until measured evidence shows a material recall benefit on hard semantic strata without unacceptable hard-negative, resource, reproducibility, privacy, or authority costs.

```text
RC-7 explicit caller-supplied cross-document links
                    │
                    ▼
       RC-8 architecture / research decision
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
 candidate discovery      identity/adjudication
 (find pairs to inspect)  (classify what a pair means)
          │                   │
          └─────────┬─────────┘
                    ▼
       adversarial benchmark evidence
                    │
                    ▼
 future separate authorization decision
      lexical only / hybrid / semantic
```

## 2. Why RC-7 is not enough

RC-7 (`core/reader_cross_document.py`) provides a bounded registry for **explicit caller-supplied** cross-document candidate links. It preserves exact two-sided provenance and relation/rationale metadata, but intentionally does not search a corpus for pairs.

After RC-7 Crystal can represent “these two Reader propositions may be related” when a caller already knows which pair to inspect. It cannot efficiently answer “among thousands of Reader propositions, which pairs are worth inspection?” without external enumeration.

That is the actual post-RC-7 gap.

### Capability-gap inventory

| Capability | Post-RC-7 state | RC-8 decision |
|---|---|---|
| Register explicit cross-document candidate link | Implemented in RC-7 | Preserve |
| Corpus-scale pair discovery | Not implemented | Future bounded implementation may add candidate generation |
| Same proposition / paraphrase adjudication | Not implemented | Contract defined here; no automatic authority |
| Related-claim / same-topic distinction | Not implemented as an adjudicator | Contract defined here |
| Possible contradiction candidate discovery | Not implemented cross-corpus | May be retrieval candidate only; no contradiction resolution |
| Lexical baseline benchmark | Not implemented for Reader | Required before semantic authorization |
| Semantic/vector Reader retrieval | Not implemented | Deferred pending benchmark evidence |
| Entity resolution | Not implemented | Deferred; separate contract required |
| Durable Reader corpus index | Not implemented | Deferred; storage lifecycle decision required |
| Full/dedicated autonomous Reader | `dedicated_reader_core=false` | Remains false |

## 3. Existing Crystal retrieval is a different authority domain

Crystal already contains retrieval machinery, so “semantic/vector retrieval NOT STARTED” must be read precisely as **Reader-specific pre-admission candidate discovery is not started**.

Existing modules include:

- `core/embedding.py` — pluggable vectorizer for claim/query retrieval; deterministic lexical hashing by default/fallback, optional SentenceTransformer backend;
- `core/legacy_retrieval.py` — bounded lexical fallback for legacy/uninitialised L3 stores;
- `core/retrieval_config.py` — bounded knobs for admitted-memory retrieval;
- `core/query_pipeline.py` — strict read-only querying of already admitted L3 facts;
- `core/rrf.py` — rank fusion helper with an explicit “ranking is not truth” boundary.

These modules operate around already admitted memory/query paths. Reader RC-4..RC-7 artifacts are **PRE-ADMISSION**. Reusing code may later be possible, but reusing an implementation is not permission to collapse the authority boundary.

```text
Reader source → RC-4 proposition candidates → RC-5/6/7 Reader artifacts
                         │
                         │ PRE-ADMISSION
                         ▼
             evidence/review/admission boundaries
                         │
                         ▼
                    admitted L3 facts
                         │
                         ▼
              existing query retrieval path
```

Directly wiring `core/embedding.py` or admitted-L3 retrieval into Reader candidate identity would be an architecture error unless a later milestone proves the data, lifecycle, privacy, reproducibility and authority contracts are compatible.

## 4. Authority firewall

The following are invariants, not tuning preferences:

```text
retrieval match             != evidence
similarity                  != identity
repetition                  != corroboration
cross-document candidate    != Canon relation
ranking                     != epistemic authority
candidate discovery         != candidate adjudication
same topic                  != same proposition
possible same claim         != claim identity
possible contradiction      != confirmed contradiction
```

A discovery layer may suggest **what to inspect**. It may not decide what is true, what is evidence, which claim wins, or what enters strict Canon.

No future candidate generator may:

- call `core.evidence.attach_evidence()` merely because a pair ranked highly;
- promote confidence or evidence sufficiency from similarity/rank;
- mutate `truth_status`, ESM, Canon, Guardian, TruthGate, or contradiction disposition;
- interpret repeated retrieval from multiple sources as corroboration without the evidence/admission path;
- auto-register a `POSSIBLE_SAME_CLAIM` candidate as claim identity;
- treat model/vector score as an identity proof.

## 5. Identity / adjudication taxonomy

This taxonomy defines review classes for a pair. A retrieval system may generate a pair for review but may not assign an authoritative identity relation merely from its score.

| Review class | Meaning | Required review questions | Retrieval authority |
|---|---|---|---|
| `SAME_PROPOSITION_CANDIDATE` | Both texts may assert the same proposition under materially equivalent scope | same subject/referent? same predicate? same polarity? same temporal/modal/quantifier/qualifier scope? compatible source context? | Candidate only |
| `PARAPHRASE_CANDIDATE` | Wording differs but asserted content may be semantically equivalent | are all material qualifiers preserved? is one weaker/stronger? does modality change? | Candidate only |
| `RELATED_CLAIM` | Claims are meaningfully connected but not equivalent | what explicit relation connects them? support, elaboration, dependency, example, causal/contextual relation? | Candidate only |
| `SAME_TOPIC` | Shared topic/entity/domain without enough claim-level overlap | does the pair merely mention the same subject? | Navigation signal only |
| `POSSIBLE_CONTRADICTION` | Claims may conflict if their referents and scopes are compatible | same comparand/time/context? opposite polarity or incompatible values? exception vs contradiction? | Suspicion only; no winner |
| `MERELY_SIMILAR` | Surface/embedding overlap is not a meaningful claim relation | shared boilerplate? homonym? same words, different referent? same entity, different predicate? | Reject as relation candidate |

### Adjudication safeguards

A “same proposition” review must be sensitive to at least:

- negation (`is` vs `is not`);
- modality (`is` vs `may be` / `must be`);
- quantifiers (`all` / `some` / `most` / exact counts);
- time and version (`in 2024` vs `in 2026`);
- jurisdiction/location/context;
- entity/reference resolution;
- measurement units and thresholds;
- quotation/attribution (`author says X` vs `X`);
- source presentation vs narrator/author endorsement;
- exceptions and conditional clauses.

Therefore normalization, cosine similarity, lexical overlap, translation equivalence, or a model judgment can be an **inspection signal** but is not sufficient on its own for identity.

## 6. Retrieval option assessment

| Option | Strengths | Failure modes / costs | RC-8 disposition |
|---|---|---|---|
| Deterministic normalized exact index | Reproducible, cheap, local, excellent for exact variants | Misses paraphrase and synonymy; must not be confused with #165 ingest identity | Useful baseline signal |
| Deterministic token/inverted index | Stdlib/local-first possible, explainable, bounded | Vocabulary mismatch; morphology/translation weak | **First benchmark baseline** |
| SQLite FTS | Local-first, mature lexical ranking, persistent index | FTS5 availability can vary by SQLite build; ranking still not identity | Candidate future backend with feature detection/fallback |
| Existing hashing vectors | Dependency-free and deterministic; lexical cosine | Not semantic; collision/noise/threshold sensitivity | Benchmark comparison signal only |
| Hybrid lexical + rank fusion | Better recall diversity; RRF avoids raw-score scale mixing | More complexity; can multiply false candidates | Compare only after frozen lexical baseline |
| Neural embeddings | Paraphrase/cross-lingual recall potential | model dependency, footprint, version drift, privacy/download lifecycle, hard negatives, opacity | **Deferred pending evidence** |
| ANN/vector backend | Scale for large vector corpora | index lifecycle, approximation/equivalence validation, resource and migration complexity | **Not justified in RC-8** |
| PostgreSQL/pgvector | Server-scale vector capability already researched elsewhere | violates ordinary local-first posture if made mandatory; current profile inactive | Remains `active=false`; not Reader default |

### SQLite remains ordinary active local-first

No part of this decision activates PostgreSQL or pgvector. If SQLite FTS is later evaluated, the implementation must detect capability rather than assume every embedded SQLite build exposes the same FTS features, and must retain a deterministic bounded fallback.

## 7. Adversarial benchmark contract

The frozen synthetic corpus for this decision is `eval/reader_rc8_retrieval_adversarial.jsonl`.

Its purpose is not to certify a retrieval model. It defines the minimum hard cases a future implementation must measure before a semantic/vector architecture claim is allowed.

### Required strata

1. exact text / normalized variants;
2. close paraphrase;
3. synonym/paraphrase with low lexical overlap;
4. cross-lingual paraphrase;
5. same topic but different predicate;
6. same entity but unrelated claim;
7. negation flips;
8. modality changes;
9. quantifier changes;
10. temporal/version changes;
11. attribution/quotation traps;
12. exception vs contradiction;
13. homonym/entity collision;
14. boilerplate/high lexical overlap false positives;
15. numerical/unit incompatibility.

### Evaluation outputs

A future benchmark runner must report, by stratum rather than only an aggregate:

- candidate recall at bounded `K`;
- hard-negative rate / false candidate rate;
- rank distribution for expected useful candidates;
- candidates examined and explicit work bound;
- deterministic replay result for deterministic modes;
- index/build/query resource observations for a declared local profile;
- model/embedder/index identity when a semantic mode is tested;
- failures/degradations rather than silently emptying unsupported paths.

A single “accuracy” number is insufficient because false claim-identity candidates and missed paraphrases have different safety and usability consequences.

### Semantic authorization gate

A later semantic/hybrid implementation may be authorized only after a separate issue pre-registers numeric thresholds and demonstrates all of the following on an exact frozen corpus/version:

1. a material recall improvement on semantic strata that the lexical baseline actually misses;
2. hard-negative behavior within the pre-registered bound;
3. bounded local resource cost compatible with Crystal’s local-first profile;
4. stable model/embedder/index identity and an explicit rebuild/mismatch policy;
5. deterministic lexical fallback when semantic machinery is absent or unavailable;
6. zero new evidence/truth/Canon authority from ranking;
7. privacy and dependency lifecycle are explicit;
8. exact-head CI and reproducible benchmark evidence are attached.

RC-8 deliberately does **not** invent numeric thresholds before a runnable baseline exists. Thresholds must be pre-registered before the comparison run so they cannot be tuned after seeing results.

## 8. Relationship to existing backlog

### #165 — normalized-id migration / normalized-claim index

#165 concerns **exact normalized ingest deduplication of admitted facts**, and explicitly forbids near-duplicate/semantic matching. Reader discovery may reuse vocabulary such as Unicode normalization, but it must not reuse #165’s fact identity as a semantic-equivalence oracle.

Decision: related terminology, **separate scope**.

### #155 — Epistemic Router / Evidence State Layer

#155 is downstream of retrieval/FactsPack and concerns evidence-state observability (`KNOWN/PARTIAL/UNKNOWN`) before TruthGate/Guardian. RC-8 is upstream pre-admission Reader candidate discovery.

Decision: complementary boundary, **separate scope**.

### #214 — PII fixtures / supply-chain pinning

#214 is repository/security hygiene. RC-8 adds a small synthetic benchmark corpus and no runtime dependency. Any future model/backend introduction would materially increase #214-style supply-chain/privacy concerns and therefore requires explicit security review.

Decision: no merge of scope; RC-8 must remain dependency-free.

## 9. Grant and public-positioning impact

This decision narrows overclaim risk. It does not add a funded/runtime capability and does not imply that Crystal now performs semantic corpus discovery.

Current public truth remains:

```text
reader_core_rc1_skeleton=true
reader_core_rc2_structural_map=true
reader_core_rc3_multi_pass_mechanics=true
reader_core_rc4_proposition_extraction=true
reader_core_rc5_relation_candidates=true
reader_core_rc6_long_context_strategy=true
reader_core_rc7_cross_document_links=true
dedicated_reader_core=false
```

RC-8 is an architecture/research decision layer only. NLnet status remains `submitted / under review / not awarded`; no award or budget change is implied.

## 10. Localization impact

This decision does not rewrite the existing RC-7 translated Reader packs in the implementation PR. Russian Reader-dependent RC-7 material remains `CURRENT` to its recorded immutable RC-7 English source checkpoint. The eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, totaling 64 documents.

The new RC-8 architecture document is English source material. Any broad translation is a separate documentation milestone under the localization policy.

## 11. Non-features after RC-8

After this decision merges, all of the following remain **not implemented as Reader runtime capability**:

- corpus candidate-discovery runtime;
- SQLite FTS Reader index;
- Reader embeddings;
- ANN/vector index;
- semantic model/provider integration;
- automatic claim identity;
- automatic entity resolution;
- automatic contradiction confirmation/resolution;
- durable Reader persistence/index migration;
- public Reader API/CLI/background worker;
- PostgreSQL/pgvector activation;
- dedicated/full autonomous Reader.

## 12. Authorized next decision, not automatic next work

The evidence supports a future bounded milestone for a **deterministic lexical Reader candidate-discovery baseline + benchmark runner**, with no semantic/vector dependency. That work is **not started by RC-8** and requires separate authorization after RC-8 completion evidence.

Only after measured lexical-baseline results may Crystal decide among:

```text
lexical sufficient
        OR
hybrid retrieval justified
        OR
semantic/vector retrieval justified
```

This sequencing is intentional: define the problem and evidence standard before selecting the expensive mechanism.