<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d4-locale: ru -->
<!-- rc6-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: main@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Crystal — Grant / Governance Overview

## 🎓 Funding truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

NLnet остаётся **submitted / under review / not awarded**. Приблизительно **€50,000** — planning/transparency context only, не approved budget, grant award или payment commitment.

## 🧬 Existing baseline

Любая работа, merged до grant agreement, является existing baseline и не может повторно считаться future funded delta.

Текущая existing Reader/research history включает:

- RC-1…RC-7 bounded implemented Reader layers;
- RC-8 completed retrieval architecture/research decision;
- RC-9 deterministic lexical PRE-ADMISSION candidate discovery implementation;
- Evaluation Surface v2 frozen evidence;
- Comparator v1 completed/frozen gate FAIL;
- NLI neutral-filter v1 completed/frozen gate FAIL;
- RRTIC-v1 frozen architecture contract only.

```text
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
```

## 🔬 Evidence does not become capability

RC-9 остаётся offline deterministic lexical baseline. Его frozen K=5 historical result:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Useful hits | 15/16 |
| Hard-negative hits | 4/4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator v1 восстановил useful recall, но failed hard-negative discrimination. NLI neutral-filter v1 уменьшил leakage, но failed useful-recall safety. Ни один результат не авторизует Reader semantic/hybrid runtime.

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
evaluation pass != runtime authorization
```

RRTIC-v1 фиксирует typed inspection vocabulary после relation-contract mismatch reassessment, но не даёт model/provider, reranking, identity/adjudication, evidence admission или Canon authority.

## 🛡️ Grant-safe authority boundary

```text
physical L3 != strict Canon
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
```

Historical RC-7 compatibility literals:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite ordinary active local-first. PostgreSQL/pgvector остаётся inactive `active=false`; import/equivalence не является activation или funded runtime delivery.

## 📈 Что может быть future funded delta

Только работа, которая на момент agreement действительно отсутствует и отдельно определена/измерима. Возможные категории могут включать reproducible release/audit evidence, source-span/replay improvements, larger evaluation fixtures, operational storage lifecycle proof, reviewer-facing evidence tooling, accessibility/localization или отдельно authorized retrieval experiment под preregistered gates.

Нельзя relabel уже merged RC-1…RC-9 / Comparator / NLI / RRTIC history как новую funded delivery.

## 🏛 Governance

Significant architecture/invariant changes начинаются с issue/RFC и требуют executable evidence, актуальных docs и exact CI. Presentation может становиться лучше, но не может создавать capabilities, authority или funding state.

## 🌍 Localization provenance

Historical Russian RC-7 source: `main@ab3ad31c437647535030e371d58f456faf14017b`. Current Russian refresh source: `main@9666781d390e3276a111cb5ee1735f6606a76283`. Остальные восемь languages не обновляются Issue #410.
