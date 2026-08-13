# 🧭 Reader Post-RC-10 — Evaluation Adequacy & Next-Milestone Architecture Decision

**Status:** BOUNDED ARCHITECTURE / RESEARCH DECISION — NO COMPARATOR EXECUTED  
**Tracking issue:** #382  
**Audited starting point:** `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`  
**Predecessors:** RC-8 decision, RC-9 lexical baseline, PR #378 / RC-10 preregistration  
**Documentation impact:** `GITHUB_AND_NOTION`

## 1. Decision

The next justified Reader milestone is **not** semantic/vector runtime, SQLite FTS, ANN, PostgreSQL/pgvector activation, or a model download.

The smallest evidence-supported next milestone is a **stronger pre-frozen Reader retrieval evaluation surface** built before any semantic/cross-lingual comparator result is observed.

The existing RC-10 screening gate remains frozen and unchanged. A later comparator must still pass that gate on the unchanged RC-8 corpus. The stronger evaluation surface is an additional evidence layer, not a replacement or post-result threshold rewrite.

```text
RC-9 lexical baseline
        ↓
RC-10 frozen screening gate
        ↓
POST-RC-10 REASSESSMENT
        ↓
stronger evaluation surface frozen first
        ↓
future separately-authorized comparator execution
        ↓
RC-10 screen + stronger evaluation
        ↓
architecture review only
        ↓
possible later runtime decision
```

This decision does **not** start the stronger evaluation milestone and does not authorize comparator execution.

## 2. Live truth entering the reassessment

The live audit on 2026-08-13 found:

- signed current `main`: `59cf060629c25ddf0747ca46ea1fadf87fa86857`;
- merge verification: `verified=true`, reason `valid`;
- exact current-main push CI `31620098274`: 9/9 successful;
- open PRs: 0 before issue #382;
- grant-presentation issue #379: closed / completed;
- RC-10 bookkeeping issue #377: closed / completed after its missing completion-evidence step was repaired;
- PR #378 remains merged preregistration only;
- RC-9 remains the implemented Reader retrieval baseline;
- `dedicated_reader_core=false` remains correct;
- unrelated backlog #155, #165 and #214 remains separate.

The #377 closure is governance truth only. It creates no comparison or runtime authorization.

## 3. What RC-9 actually measured

The frozen RC-9 control remains `eval/reader_rc9_lexical_baseline.json` on the 20-case RC-8 diagnostic corpus at K=5:

| Metric | Frozen result |
|---|---:|
| Recall@5 | `0.937500` |
| Precision@5 | `0.187500` |
| MRR | `0.895833` |
| Useful paired hits | `15/16` |
| Paired hard-negative hits | `4/4` |
| Paired hard-negative rate@5 | `1.000000` |

Known useful miss: `rc8-004`, an English/Russian cross-lingual paraphrase.

Known hard-negative failures include same-topic/same-entity, homonym and boilerplate traps.

The correct conclusion is still:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

This is retrieval evidence. It is not semantic accuracy, identity accuracy, truth accuracy, corroboration quality or evidence-admission quality.

## 4. Two different problems must not be conflated

The live evidence exposes a **retrieval-quality gap**:

1. one cross-lingual useful pair is missed;
2. all four paired hard negatives surface at K=5.

The live evidence does **not** expose a measured Reader scale/latency blocker. RC-9 is in-memory and O(corpus), but no current benchmark demonstrates that corpus size, index-build cost, latency or memory use is the next binding limitation.

Therefore:

```text
measured retrieval-quality gap != measured scaling gap
```

Choosing FTS, ANN or a server backend now would optimize an unmeasured problem.

## 5. Option reassessment

| Option | What it can address | What current evidence says | Disposition |
|---|---|---|---|
| Keep RC-9 in-memory BM25 | Deterministic lexical discovery | Useful 15/16 recall, but cross-lingual miss + 4/4 hard negatives remain | Preserve as frozen control/fallback |
| SQLite FTS5 | Lexical persistence / scaling / query work | No measured scale blocker; still lexical and does not itself supply cross-lingual semantics | **Defer until scale evidence exists** |
| `core/rrf.py` | Fuse independently useful rankings without score-scale coupling | Pure ordering helper; cannot create epistemic authority and cannot substitute for a missing useful signal | Future comparison utility only |
| `HashingEmbedder` | Deterministic lexical cosine | Word hashing with stopword removal; no translation/semantic mechanism | Comparator control signal only |
| `TrigramHashingEmbedder` | Character/morphology/typo tolerance | Useful within related scripts/forms; still no semantic translation mechanism and can add noisy collisions | Comparator control signal only |
| Existing `SentenceTransformerEmbedder` | Neural semantic signal class | Optional dependency/model lifecycle; current default model identity is not an immutable evaluation pin and may load/download assets | **Do not execute as qualifying comparator yet** |
| New pinned multilingual semantic comparator | Plausible mechanism for cross-lingual recall | Not selected, pinned, privacy-reviewed or evaluated; hard-negative behavior unknown | Future separately-authorized experiment only |
| ANN / vector DB | Vector scaling | No vector Reader runtime is authorized and no scale evidence requires ANN | Not justified |
| PostgreSQL/pgvector | Institutional vector/server path | Current profile remains inactive `active=false`; unrelated to the measured next uncertainty | Not authorized for Reader |
| Stronger pre-frozen evaluation | Reduces decision uncertainty and tuning-to-20-case risk | Directly addresses the acknowledged limitation in RC-10: current corpus is small, paired and synthetic | **Selected next bounded milestone** |

## 6. Why SQLite FTS is not next

SQLite FTS is a credible local-first future scaling option, but its benefit is mostly operational:

- persistent inverted index;
- lower query work at larger corpus sizes;
- mature lexical ranking.

It does not by itself solve the demonstrated `rc8-004` cross-lingual miss, and lexical ranking can continue to surface negation, modality, homonym, boilerplate and same-topic traps.

No current Reader benchmark establishes a scale threshold that RC-9 has exceeded. Therefore FTS remains a future option whose admission requires a measured corpus-size/resource problem, feature detection and deterministic fallback.

## 7. Why existing deterministic embedders are not a semantic answer

`core/embedding.py` is useful existing code, but the current deterministic embedders remain lexical feature systems:

- `HashingEmbedder` hashes whole non-stopword tokens;
- `TrigramHashingEmbedder` hashes character trigrams after English/Russian stopword removal.

They may be useful comparison controls for morphology, typos or alternative lexical geometry. They do not implement translation or proposition-level semantic equivalence.

Their stopword policies are also a Reader risk: words carrying modality, condition or scope in some contexts can be removed. This is why PR #378 correctly classifies these components as `COMPARATOR_SIGNAL_ONLY`, not Reader identity authority.

## 8. Why RRF is reusable but insufficient by itself

`core/rrf.py` is pure ordering logic and preserves candidate objects unchanged. That makes it suitable for a future isolated Reader comparison with a Reader-specific candidate identity key.

But RRF only fuses rankings it receives. It cannot establish evidence, identity or truth, and it cannot make a missing semantic/cross-lingual signal trustworthy merely by combining it with lexical ranking.

```text
rank fusion != new semantic evidence
rank fusion != identity adjudication
```

RRF therefore remains an implementation utility for a later experiment, not the next capability milestone.

## 9. Why a semantic comparator is plausible but premature

The measured cross-lingual miss means a future comparison needs at least one signal capable of bridging lexical language mismatch if it is to satisfy the RC-10 screening requirement to recover `rc8-004`.

That observation does **not** select a particular model or authorize a semantic runtime.

A qualifying model-backed comparator would need, before execution:

- exact comparator mode;
- exact model name;
- immutable revision/checksum;
- exact dependency versions;
- preloaded local assets;
- zero query-time network calls;
- no external transmission of Reader source text;
- privacy review;
- resource observation;
- repeatability observation;
- explicit failure/degraded behavior;
- no `auto` backend selection;
- deterministic lexical fallback for any later runtime proposal.

The current optional `SentenceTransformerEmbedder` is admitted-memory infrastructure and is not, by its existence, an approved Reader comparator contract.

## 10. Evaluation adequacy finding

The RC-8 corpus is deliberately useful but deliberately limited:

- 20 cases;
- 16 paired useful cases;
- 4 paired hard negatives;
- synthetic;
- public/known;
- pair-oriented rather than a fully judged multi-candidate qrels corpus.

RC-10 itself records that passing its frozen gate cannot authorize Reader runtime adoption and requires stronger evaluation afterward.

Executing a model comparator first and only then designing the stronger evaluation would create avoidable tuning/selection pressure around a tiny known fixture. The lower-risk sequence is to freeze the stronger evaluation contract **before** seeing model-comparator results.

This does not change or bypass RC-10. It adds a second evidence surface.

## 11. Selected next bounded milestone

The next milestone, if separately started after this decision completes, should be:

> **Reader Retrieval Evaluation Surface v2 — pre-frozen stronger corpus/qrels + unchanged RC-9 control reproduction**

It is an evaluation/research milestone, not Reader runtime.

### Minimum purpose

Create a stronger, reproducible evaluation surface that can later test lexical, deterministic-control and semantic/cross-lingual comparators without tuning the evaluation after model results.

### Required properties

The next milestone should:

1. preserve the original RC-8 corpus and RC-10 screening gate unchanged;
2. add a separate versioned evaluation corpus rather than rewriting historical fixtures;
3. include multiple cases per material identity trap rather than one exemplar;
4. include multiple cross-lingual useful and hard-negative cases;
5. include low-lexical-overlap paraphrases;
6. include negation, modality, quantifier, temporal/version, jurisdiction, attribution/quotation, conditional/scope, units/thresholds, homonym/entity collision and boilerplate traps;
7. use judged candidate pools/qrels sufficient to report precision-like behavior without treating every unpaired item as an implicit negative by construction;
8. preserve source/proposition identifiers and no-authority semantics;
9. freeze corpus identity, K/metrics and acceptance rules before any model-backed result is observed;
10. rerun RC-9 unchanged as the control on the new surface;
11. record work/resource bounds;
12. add no model dependency and execute no semantic comparator in the corpus-freeze milestone.

### Exit state

A completed Evaluation Surface v2 milestone should end with:

```text
stronger evaluation frozen
+ RC-9 control reproduced
+ future comparator admission contract explicit
+ no semantic comparator executed
+ no Reader runtime added
```

Only then should a separately authorized comparator-execution milestone be considered.

## 12. RC-10 screening gate remains immutable

Nothing in this decision changes `eval/reader_rc10_retrieval_comparison_preregistration.json`.

A future comparator must still, on the unchanged RC-8 corpus at K=5:

- retain all 15 RC-9 useful paired hits;
- recover `rc8-004`, reaching 16/16 useful paired recall;
- keep MRR >= `0.895833`;
- reduce paired hard-negative hits to <= `2/4`;
- introduce exactly zero authority violations;
- declare exact backend/model/index identity;
- use no `auto` backend;
- perform zero query-time network calls;
- send zero Reader source text to external services;
- preserve deterministic lexical fallback for any later runtime proposal.

Passing this screen remains:

```text
ELIGIBLE_FOR_STRONGER_EVALUATION_AND_ARCHITECTURE_REVIEW_ONLY
```

It remains **not runtime authorization**.

## 13. Authority firewall

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

The stronger evaluation milestone must not mutate evidence, Canon, ESM, Guardian, TruthGate or contradiction disposition.

## 14. Storage and dependency boundary

This decision changes no runtime storage or dependency state:

```text
SQLite ordinary active local-first
PostgreSQL/pgvector inactive active=false
Reader FTS not implemented
Reader semantic/vector runtime not implemented
ANN/vector DB not implemented
```

No automatic backend switching is authorized.

## 15. Backlog boundary

- #155 remains downstream Epistemic Router / Evidence State architecture scope.
- #165 remains exact normalized admitted-fact migration/dedupe and is not semantic matching.
- #214 remains fixture/PII/supply-chain hardening.

A future model-backed comparator will need explicit dependency/privacy treatment, but this decision does not absorb or implement #214.

## 16. Grant boundary

NLnet remains `submitted / under review / not awarded`. Approximate €50,000 remains planning context only.

RC-1 through RC-9, PR #378 and this architecture decision are pre-agreement existing history if completed before any funding agreement. They must not later be represented as newly funded runtime delivery.

## 17. Current Reader position after this decision

```text
RC-1..RC-7 bounded Reader layers        implemented
RC-8 retrieval architecture decision   complete
RC-9 lexical discovery baseline         implemented / measured
RC-10 reuse + comparison prereg         complete / no comparison executed
post-RC-10 reassessment                 architecture decision only
semantic comparator execution           NOT STARTED
stronger evaluation v2                  NOT STARTED
semantic/hybrid Reader runtime           NOT STARTED
vector Reader runtime                    NOT STARTED
dedicated_reader_core                    false
```

## 18. Stop boundary

After this architecture decision receives exact-head CI, semantic review, guarded merge, signed post-merge CI, Notion synchronization/read-back and completion evidence, **STOP**.

Do not automatically start Evaluation Surface v2, execute a comparator, download a model, add FTS, add ANN/vector indexing, activate PostgreSQL/pgvector, implement #155/#165/#214, or refresh localization.