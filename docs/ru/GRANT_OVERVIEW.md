<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d4-locale: ru -->
# Crystal — обзор проекта, гранта и governance

**Дата статуса:** 10 августа 2026 года  
**Назначение:** стабильная translation-oriented D4 source summary.  
**Authority:** merged GitHub `main`, executable tests, exact CI и подробные English grant/governance documents имеют приоритет.

## 1. Позиция проекта

Velantrim Crystal — open-source, local-first runtime памяти, evidence и decision-boundary для trustworthy AI systems. Стандартная установка рассчитана на работу без обязательных cloud, telemetry, analytics, external LLM или server dependencies.

Crystal не является завершённым персональным ExoCortex, Titan runtime, AGI, системой сознания или универсальным truth engine. Он предоставляет bounded infrastructure для source-linked claims, evidence, read-only grounded retrieval, explicit admission, audit и portable storage operations.

Reader Core RC-1 и RC-2 теперь входят в этот bounded pre-agreement baseline: RC-1 — минимальный evidence-linked source/session skeleton, RC-2 — caller-supplied Structural Document Map. Вместе они не образуют dedicated multi-pass Semantic Reading runtime.

## 2. Текущий проверенный baseline

Проверенный storage/runtime checkpoint остаётся:

```text
main@bbd816c09dd39a02e6de6c1014438490572f40f6
validated head d7af7c80722274f9217bc5545d150f92e9363f37
CI 31256316536
PostgreSQL integration 31256316532
```

Evidence:

- Python 3.11 и 3.12: 2078 passed / 13 skipped / 0 failed;
- 9756 measured statements / 100.00% line coverage;
- 7/7 declared Ring Zero mutants killed;
- 9/9 permanent CI jobs successful;
- 1/1 real PostgreSQL/pgvector integration job successful;
- Reader RC-1 и RC-2 отдельно merged/tested как bounded foundations и записаны в implementation manifest.

Documentation-only translation merges не создают новую runtime capability.

## 3. Границы storage, Reader и authority

```text
physical L3      != strict Canon
retrieval score  != evidence
model output     != source truth
migration proof  != claim proof
import success   != activation
Reader artifact  != admitted fact
Reader coverage  != comprehension proof
Reader structure != truth/confidence authority
```

SQLite остаётся ordinary active local-first profile. Первый durable `auto` может выбрать optional LadybugDB или SQLite, после чего deployment identity фиксируется. Explicit Mock — development/CI state.

PostgreSQL/pgvector остаётся optional inactive migration/equivalence target с `active=false`, отсутствующей в ordinary runtime composition. Active PostgreSQL reads/writes, ANN acceptance, automatic switching, cutover, fencing, rollback и dual-write не реализованы.

Reader RC-1/RC-2 не удерживают source body, не добавляют durable Reader storage schema или public Reader API/CLI/background worker и не могут менять `truth_status`/ESM, писать strict Canon, обходить Guardian/TruthGate, разрешать contradictions или получать planner/belief-update authority.

## 4. Статус гранта

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

Публичный funding plan описывает приблизительный запрос €50,000. Это документ планирования и прозрачности, а не approved budget или payment commitment.

Статус гранта может измениться только на основании verified external communication, например подписанного agreement или Memorandum of Understanding. Private application correspondence не является public runtime или budget evidence.

## 5. Правило baseline и funded delta

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

Всё, что merged до grant agreement, является existing baseline и не может быть повторно выставлено как future delivery. Сюда входят SQLite logical migration и inactive PostgreSQL import/equivalence phases, D1–D5 documentation work, Reader RC-0 architecture contract, RC-1 minimal skeleton и RC-2 Structural Document Map, смерженные до финансирования.

Если `main` продвигается до соглашения, baseline/funded-delta matrix должна быть reconciled, чтобы funded scope оставался действительно дополнительным, измеримым и независимо аудируемым.

## 6. Grant-safe будущая работа

Potential future funded packages включают только новые evidence поверх baseline, например:

- reproducible release artifacts, checksums и SBOM;
- exact-vs-ANN evaluation с accepted thresholds;
- explicit source/target fencing, cutover receipts и rollback proof;
- PostgreSQL production roles, backup/restore/upgrade lifecycle и observability;
- reviewer-facing evidence и TRACE inspection UX;
- отдельно bounded Reader work за пределами RC-1/RC-2, например explicit multi-pass mechanics после review;
- более сильные claim lint, maintenance и independent audit evidence.

Dedicated multi-pass Reader / Semantic Reading runtime не реализован. RC-1/RC-2 — bounded foundations, не automatic document comprehension. Они не добавляют parser/semantic chunker/OCR, Reader LLM/provider orchestration, embeddings/ANN/vector DB или cross-document reasoning engine.

## 7. Governance model

Сейчас Crystal использует lightweight maintainer-led governance:

- один текущий lead maintainer reviews и merges changes;
- значительные architecture, invariant, dependency и breaking changes начинаются с issue или RFC;
- решения и rationale остаются видимыми в issues, PRs, ADRs и changelog history;
- устойчивые contributors могут быть приглашены стать maintainers;
- security vulnerabilities проходят private responsible disclosure;
- releases создаются из green `main`, а package version служит published version source.

Maintainer может принимать проектные решения, но не может отменять executable evidence или тихо ослаблять Ring Zero, Guardian, TruthGate, read-only query, Reader authority, storage continuity, privacy или claim-discipline contracts.

## 8. Правила contribution

Contributors должны сохранять:

- разделение physical L3 / strict Canon;
- ownership Guardian и TruthGate над automatic admission;
- Reader artifacts/structure как non-authoritative upstream data;
- read-only public query surfaces;
- explicit admission-capable ingest;
- stdlib-only ordinary runtime, где новые dependencies optional и fail-closed;
- local-first и отсутствие outbound network по умолчанию;
- точный implementation/test/status language;
- раздельные runtime, research, RFC, grant и translation authority.

Contribution не завершён только потому, что code существует. Нужны relevant tests, 100% coverage gate, documentation, security review и exact CI evidence.

## 9. Sustainability и independence

Ordinary core не требует hosted infrastructure. Optional remote adapters и providers расширяют trust boundary только при deliberate configuration.

Механизмы sustainability включают:

- reproducible CI и public evidence;
- scoped releases и semantic versioning;
- transparent issue/PR history;
- documentation и machine-readable status manifests;
- contributor onboarding и bus-factor reduction;
- grant или contractor support, привязанный к independently verifiable deliverables.

Funding не передаёт epistemic authority sponsor, provider, model или storage backend.

## 10. Текущие non-claims

Crystal не заявляет:

- grant award или approved budget;
- legal, GDPR или security certification;
- AGI, consciousness, personhood или zero hallucinations;
- active PostgreSQL runtime, automatic switching, accepted ANN, cutover, rollback или dual-write;
- production multi-tenancy или distributed exactly-once coordination;
- завершённый dedicated multi-pass Reader Core, automatic Reader parsing или comprehension proof;
- что каждая physical graph record является strict Canon;
- native-speaker editorial certification для переводов.

## 11. Authoritative подробные источники

- [Grant scope](../GRANT_NLNET_SCOPE.md)
- [Baseline → funded delta → acceptance matrix](../grants/baseline-funded-delta-matrix.md)
- [Funding use plan](../grants/funding-use-plan.md)
- [Reader Core architecture contract](../architecture/READER_CORE_ARCHITECTURE.md)
- [Reader implementation status](../IMPLEMENTATION_STATUS.md)
- [Roadmap](../../ROADMAP.md)
- [Governance](../../GOVERNANCE.md)
- [Contributing](../../CONTRIBUTING.md)
- [Glossary](../GLOSSARY.md)
- [Current status](../STATUS.md)
- [Test report](../../TEST_REPORT.md)
