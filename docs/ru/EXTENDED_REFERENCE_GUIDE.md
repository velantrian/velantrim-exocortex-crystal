<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d5-locale: ru -->
<!-- translation-status: CURRENT -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
<!-- d5-reader: rc5-relation-candidates-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
# Руководство по расширенным источникам

Этот документ направляет к detailed English sources, не дублируя volatile implementation evidence, CI logs, ADR bodies, machine-readable status, legal mappings или grant evidence только ради apparent multilingual parity. English остаётся primary working/source/conflict-resolving language.

## Статусы документации

| Статус | Значение |
|---|---|
| `CURRENT` | Maintained public/routing surface, semantically reconciled с immutable source checkpoint. |
| `REFRESH_NEEDED` | Rich surface, которая известно отстаёт от governing source; status всегда explicit. |
| `RETIRED` | Preserved historical snapshot/handoff; не current authority/capability/grant evidence. |
| `ENGLISH_ONLY_BY_DESIGN` | Detailed/volatile technical, security, test, CI, machine-readable, research, RFC, ADR или grant evidence intentionally maintained only in English. |

Machine-readable inventory находится в [`../status/d5-inventory.json`](../status/d5-inventory.json). Unclassified documentation-like surface = validation failure.

После RC-5 русский root README и Reader-dependent D1/D3/D4/D5 detail pack имеют `CURRENT` к `51c205fe048fd69d39fcd47b43e042a50de432bc`. Восемь других localized root README + семь Reader-dependent detail document types на каждую locale имеют `REFRESH_NEEDED`: **64 tracked debt documents**. Их rich предыдущие переводы сохраняются; сокращённые summary replacement не считаются допустимым refresh.

D2 reviewer/safety docs и Quick Start остаются `CURRENT` во всех 9 locales, потому что RC-5 не меняет их governing source semantics.

## Reader Core boundary

Current machine truth deliberately distinguishes bounded layers from absent full capability:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

RC-1 реализует minimal evidence-linked source/session skeleton. RC-2 — caller-supplied source-version-bound Structural Document Map. RC-3 — deterministic explicit multi-pass mechanics (`ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD`), declared targets, pass state ledger, explicit coverage outcomes и count-only telemetry.

RC-4 — deterministic pre-admission proposition candidate registration из completed substantive RC-3 targets. Candidate требует pass `COMPLETED`; recorded outcome/current matching coverage = `PROCESSED` либо `REVISITED`; uses `EXTRACTED_PROPOSITION`; preserves source owner, presentation category, negation/qualifiers и replayable provenance.

RC-5 — deterministic pre-admission relation registry поверх candidates, реально registered одним RC-4 extractor, в одном OPEN ReaderSession и exact SourceVersion.

```text
POSSIBLE_CONTRADICTION = symmetric suspicion only
TENSION                = symmetric tension only
EXCEPTION              = directional exception relation
QUALIFICATION          = directional refinement relation
```

Relation keeps both exact RC-4 candidate IDs, pass/node IDs, primary/supporting source locators и explicit rationale. Symmetric pair order canonicalized; directional order preserved. Duplicate symmetric registration fail closed и не становится corroboration.

RC-5 не является automatic NLP/LLM contradiction detection. Он не вызывает `core.evidence.attach_evidence()`, не writes fact `evidence_spans`, не устанавливает evidence sufficiency, не меняет `truth_status`/ESM, не performs TruthGate admission и не invokes contradiction-resolution workflow.

RC-1..RC-5 не удерживают source body и не добавляют durable Reader DB, public Reader API/CLI/background worker, parser/OCR/layout, autonomous model-driven Reader, embeddings/ANN/vector database, semantic equivalence, cross-document identity/reasoning или planner/belief update.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
similarity != identity
repetition != corroboration
```

## Неизменные границы

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import success != activation
Reader artifact != admitted fact
Reader coverage != comprehension proof
Reader pass completion != comprehension proof
Reader structure != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

SQLite остаётся ordinary active local-first. PostgreSQL/pgvector остаётся inactive target `active=false`. Dedicated/full autonomous Reader, automatic contradiction resolution, semantic cross-document identity и active PostgreSQL runtime не реализованы.

## Грант и certification non-claims

NLnet остаётся `submitted / under review / not awarded`. Approx **€50,000** — planning only, не approved budget/payment commitment. Current grant-safe boundary: **budget change: none**. RC-0..RC-5 merged pre-agreement являются existing baseline и не могут повторно считаться funded delta.

Не заявляются legal, GDPR, security или native-speaker editorial certification.

## Retired и English-only материалы

`RETIRED` materials сохраняются для attribution/audit history, но не доказывают implementation, coverage, maturity, grant state, Canon membership или deployment readiness.

`ENGLISH_ONLY_BY_DESIGN` применяется к detailed volatile technical/evidence families, где translation каждого меняющегося artifact повышал бы stale-claim risk. Для public orientation используйте D1–D5 localized surfaces; conflict resolver — English source contracts + merged code/CI.

## Маршруты к authoritative источникам

- [D5 policy](../EXTENDED_REFERENCE_POLICY.md)
- [Карта документации](../DOCUMENTATION_MAP.md)
- [Текущий статус](./STATUS.md)
- [Статус реализации](./IMPLEMENTATION_STATUS.md)
- [Обзор архитектуры](./ARCHITECTURE_OVERVIEW.md)
- [Полная архитектура](../ARCHITECTURE.md)
- [Reader Core architecture contract](../architecture/READER_CORE_ARCHITECTURE.md)
- [ADR index](../ADR.md)
- [Security policy](../../SECURITY.md)
- [Privacy](../../PRIVACY.md)
- [GDPR technical mapping](../../GDPR.md)
- [Archive routing](../archive/README.md)

При расхождении приоритет: merged GitHub code, executable tests, exact CI, machine-readable manifests, governing English source.
