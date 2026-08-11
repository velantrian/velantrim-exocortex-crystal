<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d4-locale: ru -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# Crystal — обзор проекта, гранта и governance

**Дата статуса:** 11 августа 2026 года  
**Назначение:** стабильная translation-oriented D4 source summary.  
**Authority:** merged GitHub `main`, executable tests, exact CI и detailed English grant/governance documents имеют приоритет.

## 1. Позиция проекта

Velantrim Crystal — open-source, local-first runtime памяти, evidence и decision-boundary для trustworthy AI systems. Стандартная установка рассчитана на работу без mandatory cloud, telemetry, analytics, external LLM или server dependencies.

Crystal не является завершённым персональным ExoCortex, Titan runtime, AGI, системой сознания или universal truth engine. Он предоставляет bounded infrastructure для source-linked claims, evidence, read-only grounded retrieval, explicit admission, audit, portable storage operations и bounded Reader processing.

Reader Core RC-1, RC-2, RC-3, RC-4 и RC-5 входят в bounded pre-agreement baseline при merge до соглашения:

- RC-1 — minimal evidence-linked source/session skeleton;
- RC-2 — caller-supplied Structural Document Map;
- RC-3 — deterministic explicit multi-pass mechanics;
- RC-4 — deterministic source-linked proposition candidate registration из completed substantive pass regions;
- RC-5 — deterministic same-session/same-version relation candidate registration поверх valid RC-4 candidates.

Вместе они **не** образуют dedicated/full autonomous Semantic Reading runtime.

## 2. Текущий проверенный baseline

Сохранённый storage/runtime checkpoint остаётся:

```text
main@bbd816c09dd39a02e6de6c1014438490572f40f6
validated head d7af7c80722274f9217bc5545d150f92e9363f37
CI 31256316536
PostgreSQL integration 31256316532
```

Evidence этого retained checkpoint:

- Python 3.11 и 3.12: 2078 passed / 13 skipped / 0 failed;
- 9756 measured statements / 100.00% line coverage;
- 7/7 declared Ring Zero mutants killed;
- 9/9 permanent CI jobs successful;
- 1/1 real PostgreSQL/pgvector integration job successful.

Reader milestones имеют собственные exact-head/post-merge CI evidence. Documentation-only translation merges сами по себе не создают runtime capability.

## 3. Границы storage, Reader и authority

```text
physical L3            != strict Canon
retrieval score        != evidence
model output           != source truth
migration proof        != claim proof
import success         != activation
Reader artifact        != admitted fact
Reader coverage        != comprehension proof
Reader structure       != truth/confidence authority
Reader pass complete   != comprehension or truth
EXTRACTED_PROPOSITION  != verified fact
Reader candidate       != admitted evidence
relation candidate     != admitted evidence
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

SQLite остаётся ordinary active local-first profile. Existing optional adapters не превращаются в truth authority. PostgreSQL/pgvector остаётся optional inactive migration/equivalence target с `active=false`, отсутствующим в ordinary runtime composition. Active PostgreSQL reads/writes, ANN acceptance, automatic switching, cutover, fencing, rollback и dual-write не реализованы.

Reader RC-1..RC-5 не удерживают source body, не добавляют durable Reader storage schema или public Reader API/CLI/background worker и не могут менять `truth_status`/ESM, писать strict Canon, обходить Guardian/TruthGate, присоединять fact evidence, повышать confidence, устанавливать evidence sufficiency, выбирать contradiction winner или получать planner/belief-update authority.

RC-3 не вызывает LLM/provider и не выбирает собственную objective или targets. Он записывает only explicit caller-declared pass, structural targets и legal RC-1 coverage outcomes.

RC-4 не выполняет automatic NLP/model extraction. Caller передаёт proposition, а RC-4 проверяет completed substantive pass context, exact source/session/provenance и создаёт только source-linked `EXTRACTED_PROPOSITION` candidate. Он сохраняет source owner, category, negation/qualifiers, но не вызывает `core.evidence.attach_evidence()`, не пишет fact evidence и не выполняет admission.

RC-5 принимает только candidates, реально зарегистрированные одним RC-4 extractor, внутри одного OPEN ReaderSession и exact SourceVersion. Он хранит обе стороны и rationale и различает `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`. Это relation **candidate**, не contradiction disposition.

```text
POSSIBLE_CONTRADICTION != confirmed contradiction
confirmed contradiction != resolved contradiction / winner
```

RC-5 не использует semantic similarity как proof, не создаёт cross-document identity и не invokes contradiction-resolution workflow.

## 4. Статус гранта

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

Public funding plan описывает approximate **€50,000** request. Это planning/transparency, а не approved budget или payment commitment.

Grant state может измениться только на основании verified external communication, например signed agreement или Memorandum of Understanding. Private application correspondence не является public runtime или budget evidence.

## 5. Правило baseline и funded delta

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

Всё, что merged до grant agreement, является existing baseline и не может быть повторно выставлено как future delivery. Сюда входят SQLite logical migration, inactive PostgreSQL import/equivalence, D1–D5 documentation work и Reader RC-0/RC-1/RC-2/RC-3/RC-4/RC-5, если они merged pre-agreement.

Если `main` продвигается до соглашения, baseline/funded-delta matrix должна reconciled, чтобы funded scope оставался genuinely additional, measurable и independently auditable.

## 6. Grant-safe будущая работа

Potential future funded packages включают только **новые evidence поверх реально merged RC-5 baseline**, например:

- reproducible release artifacts, checksums и SBOM;
- exact-vs-ANN evaluation с accepted thresholds;
- explicit source/target fencing, cutover receipts и rollback proof;
- PostgreSQL production roles, backup/restore/upgrade lifecycle и observability;
- reviewer-facing evidence и TRACE inspection UX;
- отдельно authorized Reader RC-6 long-context strategy;
- позднее RC-7 cross-document reading с explicit provenance/identity boundaries;
- stronger claim lint, maintenance и independent audit evidence.

RC-5 не авторизует RC-6 или RC-7 автоматически. Future Reader work не может redefining relation candidates как truth, bypass Guardian/TruthGate или use similarity as identity.

## 7. Governance model

Crystal использует lightweight maintainer-led governance:

- current lead maintainer reviews и merges changes;
- significant architecture/invariant/dependency/breaking changes начинаются с issue или RFC;
- decisions/rationale остаются видимыми в issues, PRs, ADRs и changelog history;
- sustainable contributors могут стать maintainers;
- security vulnerabilities проходят private responsible disclosure;
- releases создаются из green `main`, package version служит published version source.

Maintainer может принимать project decisions, но не может отменять executable evidence или silently weaken Ring Zero, Guardian, TruthGate, read-only query, Reader authority firewall, storage continuity, privacy или claim-discipline contracts.

## 8. Правила contribution

Contributors должны сохранять:

- physical L3 / strict Canon separation;
- Guardian/TruthGate ownership над automatic admission;
- Reader artifacts/structure/pass/proposition/relation candidates как non-authoritative upstream state;
- `EXTRACTED_PROPOSITION != verified fact`;
- `Reader candidate != admitted evidence`;
- `contradiction candidate != confirmed contradiction`;
- `similarity != identity` и `repetition != corroboration`;
- read-only public query surfaces;
- explicit admission-capable ingest;
- stdlib-only ordinary runtime, где dependencies optional и fail closed;
- local-first/no outbound network по умолчанию;
- exact implementation/test/status language;
- separate runtime, research, RFC, grant и translation authority.

Contribution не завершён только потому, что code существует. Нужны relevant tests, 100% coverage gate, docs, security review и exact CI evidence.

## 9. Sustainability и independence

Ordinary core не требует hosted infrastructure. Optional remote adapters/providers расширяют trust boundary только при deliberate configuration.

Механизмы sustainability:

- reproducible CI/public evidence;
- scoped releases/semantic versioning;
- transparent issue/PR history;
- documentation + machine-readable status manifests;
- contributor onboarding/bus-factor reduction;
- grant/contractor support, tied to independently verifiable deliverables.

Funding не передаёт epistemic authority sponsor, provider, model или storage backend.

## 10. Текущие non-claims

Crystal не заявляет:

- grant award или approved budget;
- legal, GDPR или security certification;
- AGI, consciousness, personhood или zero hallucinations;
- active PostgreSQL runtime, automatic switching, accepted ANN, cutover, rollback или dual-write;
- production multi-tenancy/distributed exactly-once coordination;
- dedicated/full autonomous Reader Core;
- automatic Reader parsing/NLP/LLM contradiction detection/resolution;
- cross-document semantic identity;
- что RC-4 candidates являются verified facts или admitted evidence;
- что RC-5 relation candidates являются confirmed/resolved contradictions;
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
