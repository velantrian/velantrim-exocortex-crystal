# Velantrim Crystal — Improvement Plan & Reminders

**Document role:** `PROPOSED` planning document (owner-provided roadmap, v0.3.0 → v0.4+). It is **not** implementation evidence. Live code, tests, CI and `docs/status/implementation-manifest.json` override anything written here.
**Original plan date:** 2026-07-15 · **Recorded / verified:** 2026-10-11 against `main` @ `692e05e319d1a789752fe797235798d4380e60d4` (`pyproject.toml` version `0.3.0`).

> The owner's original plan text (Russian) is preserved verbatim in section B. Section A records the verification of its claims against the repository (honesty rule: file existence ≠ wiring ≠ production readiness).

---

## A. Verification against repo (2026-10-11)

Legend: **CONFIRMED** (code/tests present as described) · **ALREADY DONE** (plan lists as TODO, baseline exists) · **PARTIAL** · **NOT FOUND**.

| Plan item | Finding | Evidence |
|---|---|---|
| TruthGate first-class module | CONFIRMED | `core/truth_gate.py`, `tests/test_truth_gate.py` (17 tests); policy `truth-gate-v1-fixed-0.05` |
| Guardian baseline `guardian_diagnose` | CONFIRMED (inline) | `core/pipeline.py` §GUARDIAN: structural `pass`/`block` only; `tests/test_guardian_contract.py` (5 tests) |
| Guardian policy as separate module/config (detect → flag → action routing) | NOT FOUND | no `core/guardian*.py`; no `flag` verdict or action routing |
| Bypass edge-case tests | PARTIAL | NaN/Infinity confidence hardening (#257) exists; no dedicated bypass test suite |
| `TRUTHGATE_BEHAVIOR.md`, `FACTSPACK_POLICY.md`, `GUARDIAN_POLICY.md` | NOT FOUND | related: `docs/CONTRADICTION_POLICY.md`, `docs/CONFLICT_RESOLUTION_SURFACES.md`, `docs/RESPONSE_POLICY_V0.md` |
| Receipt v2 | ALREADY DONE (baseline) | `core/provenance.py`: `RECEIPT_VERSION = 2` (embeds source-span evidence in citations) |
| LLM-layer fields in receipts | NOT FOUND | no model/generation fields in `core/provenance.py` |
| Provenance Chain | CONFIRMED (baseline) | `core/provenance_chain.py`, `docs/core/PROVENANCE_CHAIN_CONTRACT.md`; full lifecycle wiring not verified here |
| Span auto-extraction | PARTIAL | `core/span_extract.py` (Markdown heading-aware), `tests/test_span_extract.py`, `tests/test_wp1_spans.py`; PDF side via `core/reader_pdf_source.py` |
| L2 review: roles / multi-curator / resumable | ALREADY DONE (baseline) | `core/curator_auth.py` (`CuratorRole` REVIEWER/CURATOR/ADMIN), `core/review_decision_store.py`, `tests/test_review_resumable.py`; lease registry is process-local (not distributed) |
| NeuroCore Phase 1 | NOT FOUND | `core/neurocore.py` is Phase 0 (passive tracker, RFC0068) |
| `trace_visualize.py` / `fractal.py` | CONFIRMED | `core/trace_visualize.py`, `scripts/trace_visualize.py`, `core/fractal.py` |
| Wikidata full Q/P + RDF statements | NOT FOUND | `core/adapters/wikidata_adapter.py` = QID labels/descriptions only |
| Licence metadata in schemas | NOT FOUND | no licence fields in `core/adapters` / `schemas` |
| OAI-PMH | NOT FOUND | mentioned only in archived docs |
| Restricted facts in MCP read-path | ALREADY DONE (baseline) | `core/mcp_server.py` filters restricted hits; `get_fact` returns `RESTRICTED_BY_POLICY` |
| "GDPR-oriented", not certification | CONFIRMED | `README.md` explicitly excludes legal/GDPR certification |
| Observer action policy | NOT FOUND | `core/observe.py` is read-only observability |
| Async stores | PARTIAL | `core/aio.py` = async interface over sync stores (`asyncio.to_thread`) |
| Harness replay | RFC only | `docs/RFC_HARNESS_REPLAY_OPTIMIZATION.md` |
| Reviewer docs | CONFIRMED | `docs/IMPLEMENTATION_STATUS.md`, `docs/REVIEWER_CHECKPOINT_2026-07.md` (last checkpoint is July) |
| Tests / CI | CONFIRMED | 159 entries in `tests/`; workflows `ci.yml`, `l3-benchmark-history.yml`, `postgresql-integration.yml`. "100% coverage" claim not verified in this review |

**Context not reflected in the July plan:** since July, main has advanced on the Reader track (RC-1…RC-7 merged, RC-9 complete, RRTIC-v1 frozen contract; semantic/NLI Reader runtime NOT AUTHORIZED — see `docs/ai/CURRENT_STATE.md`). Plan priorities should be re-read against that state.

**Recommended next steps (from evidence):**
1. Guardian policy module + `GUARDIAN_POLICY.md` + dedicated TruthGate/Guardian bypass test suite (largest gap on a Ring Zero invariant; small, stdlib-only, test-first).
2. `FACTSPACK_POLICY` RFC consolidating existing contradiction/conflict docs. Receipt v2 is already shipped as a baseline — follow-up is only LLM-layer reproducibility fields, lower priority.

---

## B. Original plan (owner text, 2026-07-15)

### 1. Общая философия улучшений
Сильные стороны: инварианты Ring Zero (Graph = Truth, TruthGate — единственная автоматическая точка входа в L3); тестовое покрытие + reviewer-friendly документация; разделение Implemented / Partial / RFC / Vision; local-first + dependency-free core.
Принципы: усиливать аудитability и traceability (Receipt v2, Evidence spans, Provenance Chain); доводить baseline-фичи до production-grade (L2 review, adapters, Guardian policy); сохранять stdlib-only runtime; не нарушать инварианты.

### 2. Приоритизированный план
**2.1 TruthGate + Guardian + Pipeline (высокий)** — полноценная политика Guardian (detect → flag → action routing); `TRUTHGATE_BEHAVIOR` с жёсткими порогами; политика конфликтов на уровне FactsPack.
- [ ] Вынести Guardian policy в отдельный конфиг/модуль + тесты
- [ ] Добавить edge-case тесты на попытки bypass
- [ ] Создать RFC `FACTSPACK_POLICY`

**2.2 Память L0–L3 + bio-inspired (высокий)** — L2 multi-curator + resumable; NeuroCore Phase 1+; L0–L7 mapping + визуализация fractal anchoring.
- [ ] Усилить `core/review.py`: роли, multi-curator workflows, UI
- [ ] NeuroCore Phase 1 (активная адаптация + consolidation)
- [ ] Расширить визуализацию в `trace_visualize.py` / `fractal.py`

**2.3 Provenance, Trace, Evidence, Receipts (высокий)** — Receipt v2; Provenance Chain на весь lifecycle; авто-извлечение span offsets (PDF/Markdown).
- [ ] Receipt v2
- [ ] Расширить авто-экстракцию spans в адаптерах
- [ ] Поля для optional LLM layer в receipts

**2.4 Ingestion / Adapters (средний–высокий)** — span extraction, licence metadata, OAI-PMH, full Wikidata Q/P.
- [ ] Wikidata: полное разрешение Q/P + RDF statements
- [ ] Метаданные лицензий в схемах
- [ ] Spans в PDF/Markdown

**2.5 Privacy / GDPR-oriented (средний)**
- [ ] Restricted факты в MCP и pipeline
- [ ] Документация: «GDPR-oriented», не certification

**2.6 Evaluation / Observability / Ops (средний)**
- [ ] Observer action policy
- [ ] Async rewrite stores
- [ ] Harness replay (на базе RFC)

### 3. Документация и Reviewer Experience (высокий)
После значимых PR обновлять `REVIEWER_CHECKPOINT_*.md` и `IMPLEMENTATION_STATUS.md`; Mermaid-диаграммы; разделение Implemented / Partial / RFC. Новые документы: `TRUTHGATE_BEHAVIOR.md`, `FACTSPACK_POLICY.md`, `GUARDIAN_POLICY.md`, `IMPROVEMENT_PLAN.md`.

### 4. Roadmap 4–6 недель
| Приоритет | Система | Что делать | Срок |
|---|---|---|---|
| Высокий | Receipts + Evidence | Receipt v2 + auto span extraction | 2–3 нед. |
| Высокий | Guardian + FactsPack | Политика + тесты | 2 нед. |
| Высокий | L2 Review Queue | Multi-curator + hardening | 3 нед. |
| Средний | Adapters | Wikidata + PDF spans + licence metadata | 3–4 нед. |
| Средний | NeuroCore | Phase 1 (active) | 4 нед. |
| Средний | Documentation | Новые RFC + обновление статусов | Постоянно |

### 5. Что НЕ трогать
- Mode Layer / Imagination Mode (остаётся RFC)
- Полная L0–L7 когнитивная модель (только baseline anchoring)
- Velantrim Culture и Personal Research Mode
- Любые изменения, которые могут обойти TruthGate или Ring Zero

> Living document: пересматривать приоритеты при каждом обновлении состояния репозитория.
