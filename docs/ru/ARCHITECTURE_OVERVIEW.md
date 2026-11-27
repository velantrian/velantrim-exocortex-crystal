<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: nlnet-not-awarded -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-reader: rc4-proposition-extraction-implemented -->
<!-- d3-reader: rc5-relation-candidates-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- rc6-translation-source: docs/ARCHITECTURE_OVERVIEW.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/ARCHITECTURE_OVERVIEW.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: docs/ARCHITECTURE_OVERVIEW.md@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Crystal — Architecture Overview

**Authority:** merged code, exact CI, `docs/ai/CURRENT_STATE.md` и implementation manifest остаются technical truth.

## Архитектура

```text
exact source/document identity
→ RC-1 source/session
→ RC-2 structure
→ RC-3 passes
→ RC-4 EXTRACTED_PROPOSITION
→ RC-5 relation candidates
→ RC-6 bounded working sets / SUMMARY
→ RC-7 explicit cross-document candidate links
→ RC-9 lexical PRE-ADMISSION discovery
→ RRTIC-v1 typed inspection contract (architecture only)
→ evidence/admission boundary
→ Guardian → TruthGate
→ physical L3 → TrustSnapshot → CanonicalView
→ strict Canon read projection
```

`core.query_pipeline.query()` остаётся public read-only path.

## Reader capability map

| Layer | State | Boundary |
|---|---|---|
| RC-1 | implemented | source/session identity |
| RC-2 | implemented | structure, not truth |
| RC-3 | implemented | explicit pass mechanics |
| RC-4 | implemented | proposition candidate, not evidence |
| RC-5 | implemented | relation suspicion |
| RC-6 | implemented | bounded context + caller SUMMARY |
| RC-7 | implemented | cross-document comparison candidates |
| RC-8 | research complete | retrieval/evaluation decision |
| RC-9 | implemented | deterministic BM25 candidate discovery |
| Comparator v1 | frozen FAIL | no runtime authorization |
| NLI v1 | frozen FAIL | no runtime authorization |
| RRTIC-v1 | architecture only | no provider/filter/reranker |

`dedicated_reader_core=false`; semantic/hybrid Reader runtime не implemented/authorized.

## Retained RC-1…RC-7 compatibility boundary

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-5 сохраняет `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` как PRE-ADMISSION relation candidates. RC-7 сохраняет explicit two-sided provenance и caller rationale; automatic semantic matching отсутствует.

## Post-RC-9 evidence

RC-9 measured lexical retrieval gap. Comparator v1 recovered useful recall but failed hard-negative discrimination. NLI neutral-filter v1 improved discrimination but failed useful-recall safety. Post-NLI reassessment classified the missing capability as a **relation-contract mismatch**.

RRTIC-v1 therefore freezes typed relation suspicion and ten qualifier dimensions. It does not perform model execution, filtering, reranking, evidence admission, contradiction adjudication or Canon mutation.

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
evaluation pass != runtime authorization
```

## Storage and authority

| Surface | Role | Boundary |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable operational memory |
| L2 | pending/review | candidate staging |
| physical L3 | multi-status graph | not strict Canon |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | trusted read | policy-allowed projection |

SQLite ordinary active local-first. PostgreSQL/pgvector remains inactive `active=false`; import/equivalence is not activation, cutover, rollback or admission authority.

## Non-claims / grant

No dedicated/full autonomous Reader, semantic/hybrid Reader runtime, Reader FTS/ANN/vector DB, NLI/CrossEncoder runtime, RRTIC runtime provider, automatic identity/evidence/adjudication/Canon mutation, active PostgreSQL runtime, security/legal/GDPR certification or awarded grant is claimed.

NLnet **submitted / not selected / not awarded**; ~€50,000 planning only.

Historical RC-7 source: `main@ab3ad31c437647535030e371d58f456faf14017b`. Current Russian refresh source: `main@9666781d390e3276a111cb5ee1735f6606a76283`.
### NLnet grant-only update

> Grant-only update; the full translation checkpoint remains historical and is not being declared newly current.

```text
proposal: submitted
submitted: true
under_review: false
awarded: false
status: submitted / not selected / not awarded
review: completed
decision: NOT_SELECTED
award status: NOT_AWARDED
decision date: 2026-10-09
```

<!-- post-v1-parity-audit: 2026-11-27; code-base: 78088e029b86d8f923178d19e9cecabd650a4f61; english-doc-source: 90f423b53ffdc364680a5e49b9ffa70e853413f9 -->
## 🧩 Дополнения после V1

Reader Product Bridge v0.1 и локальные источники UTF-8 (TXT/Markdown) и PDF v0.1 реализованы (#455, #457, #458). Это ограниченные компоненты чтения до допуска: они не разрешают семантическое выполнение моделей, допуск свидетельств, запись в Canon или production.

Для обоснования публичного фактического ответа `VERIFIED` требует актуального пригодного к воспроизведению свидетельства, привязанного к точному утверждению, разрешённому `TrustSnapshot` (#464). Совпадение ID, прежний вердикт или квитанция недостаточны; потеря поддержки не доказывает ложность. Исторические решения не переписываются.

#507/#505 сверяет L0 с общей SQLite L1 при каждом `get_fact()`; #512 изолирует возвращаемые данные глубоким копированием и закрывает соединение при ошибке схемы; #513 отклоняет обычный повторный ingest уже restricted-записи до записи; #511 проверяет tombstone перед разрешением результата канонического поиска. Это ограниченные исправления: начатые ранее чтения, гонка ограничения и записи, другие пути, восстановление и независимые копии не покрыты полностью. Каскад следует только зарегистрированным `DERIVED_FROM`; полнота происхождения и прерывания остаются открытыми (#504). Завершение V1 и зелёный CI не доказывают отсутствие дефектов, юридическое соответствие или production-авторизацию.

[Английский источник](../ARCHITECTURE_OVERVIEW.md)
