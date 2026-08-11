<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
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
# Crystal — глоссарий и руководство по дисциплине claims

**Дата статуса:** 11 августа 2026 года  
**Назначение:** поддерживаемый русский D4 glossary.  
**Authority:** merged implementation, executable tests, exact CI и detailed English contracts сильнее этой сводки.

## Имена контрактов

Programmatic identifiers остаются неизменными в code, schemas, CLI, APIs и translated docs.

| Термин | Значение и граница |
|---|---|
| **claim** | Typed assertion. Claim не становится автоматически verified fact. |
| **admission** | Решение, позволяющее claim войти в более trusted state/projection. |
| **Guardian** | Structural/safety/policy checks до epistemic admission; не replacement TruthGate. |
| **TruthGate** | Controlled epistemic admission boundary; не universal truth detector. |
| **physical L3** | Multi-status graph/storage state; storage membership не strict Canon membership. |
| **strict Canon** | Deny-dominant trusted read projection, разрешённая current evidence/policy. |
| **CanonicalView** | Fail-closed read projection для grounded responses. |
| **TrustSnapshot** | Read-time trusted state view; не переписывает physical storage. |
| **TRACE** | Machine-readable grounding path, связывающий answer с admitted claims/evidence. |
| **Receipt** | Replayable, tamper-sensitive evidence операции/ответа; migration receipt не claim evidence. |
| **provenance** | Источник, path создания и lifecycle claim/artifact. |
| **evidence span** | Source-linked passage, поддерживающий candidate/admitted claim. |
| **source status** | Origin class claim, например external source, user statement, model output. |
| **epistemic state** | Typed status, определяющий допустимое обращение с claim; не просто confidence score. |
| **grounding** | Связывание ответа с admitted claims, evidence и traceable sources. |
| **FactsPack** | Bounded traceable context; не authority owner. |
| **read-only query** | Query contract, не меняющий facts, ESM, L3, outbox, links, embedder identity или candidate state. |
| **fail-closed** | Refusal/bounded failure вместо hidden admission при неопределённых evidence/policy/state. |
| **storage profile** | Durable deployment identity backend + non-secret locator; не epistemic authority. |
| **migration bundle** | Deterministic portable operation artifact approved datasets; не whole-system truth export. |
| **exact equivalence** | Equality counts/canonical bytes/hashes approved dataset; не activation/retrieval acceptance. |
| **active=false** | PostgreSQL target неактивна и не обслуживает ordinary runtime reads/writes. |
| **baseline** | Работа, уже merged/evidenced до funded agreement. |
| **funded delta** | New measurable work поверх frozen baseline, accepted via public evidence. |
| **deliverable** | Bounded public artifact с explicit acceptance evidence. |
| **local-first** | Data/ordinary operations local by default; remote services optional. |
| **provider independence** | Models/providers replaceable interfaces и не truth authority. |
| **restriction** | Technical boundary use/disclosure stored material. |
| **erasure** | Deletion через implemented active-store lifecycle; independent copies требуют separate handling. |
| **review queue** | Pending/blocked claims до explicit curator action. |
| **curator override** | Attributed audited human decision; не hidden TruthGate bypass. |
| **Reader Core RC-1** | Bounded evidence-linked source/session skeleton с exact source-version, locators, fidelity, coverage, bookmarks/open loops, stale/failure/privacy; no truth/admission authority. |
| **Reader Core RC-2** | Caller-supplied Structural Document Map с version-bound hierarchy/order/ambiguity; no parser/truth authority. |
| **Reader Core RC-3** | Deterministic explicit multi-pass mechanics: pass kinds, declared targets, pass ledger, explicit RC-1 coverage outcomes; no autonomous/comprehension authority. |
| **Reader Core RC-4** | Deterministic proposition registration из completed substantive RC-3 regions; source-linked `EXTRACTED_PROPOSITION` candidates с attribution/category/negation/qualifiers; no automatic NLP/evidence admission. |
| **Reader Core RC-5** | Deterministic same-session/same-exact-source-version relation registry поверх valid RC-4 candidates; no contradiction resolution/truth authority. |
| **EXTRACTED_PROPOSITION** | Normalized source-linked Reader representation; не verified fact/admitted evidence. |
| **source owner** | Speaker/author/entity attribution; attribution не truth. |
| **proposition presentation category** | Как source presents proposition: factual assertion, opinion, hypothesis, conditional, example, quoted speech, reported position, definition, uncertain assertion; descriptive, not admission. |
| **POSSIBLE_CONTRADICTION** | RC-5 symmetric suspicion, что two propositions могут conflict; не confirmed contradiction. |
| **TENSION** | RC-5 symmetric tension relation без assertion confirmed contradiction. |
| **EXCEPTION** | RC-5 directional relation: right candidate зарегистрирован как exception к left. |
| **QUALIFICATION** | RC-5 directional relation: right candidate narrows/refines left. |
| **relation rationale** | Explicit audit reason регистрации relation; не truth/evidence proof. |
| **dedicated/full Reader Core** | Future autonomous Semantic Reading runtime beyond bounded RC-1..RC-5; `dedicated_reader_core=false`. |
| **NLnet planning amount** | Approx **€50,000** planning magnitude, не approved budget/payment commitment. |
| **budget change** | Current grant-safe state: **budget change: none**. |

## Термины, требующие осторожности

### «Truth» и «canonical graph»

Не пишите, что every graph node является truth:

```text
physical L3 stores typed multi-status records
strict Canon is the evidence- and policy-allowed read projection
```

### «Implemented», «tested», «current» и «planned»

- **implemented** — merged code exists;
- **tested** — named executable evidence exists;
- **current** — reconciled against exact source checkpoint;
- **planned / research** — no runtime claim.

Open PR/RFC/issue/prototype/Notion page не являются current runtime evidence.

### «Reader Core implemented»

Не сворачивайте bounded milestones в claim full capability:

```text
RC-1 minimal evidence-linked skeleton     = implemented/tested
RC-2 Structural Document Map              = implemented/tested
RC-3 explicit multi-pass mechanics        = implemented/tested
RC-4 source-linked proposition extraction = implemented/tested
RC-5 explicit relation candidates         = implemented/tested only after exact CI/merge
dedicated/full autonomous Reader runtime  = not implemented
coverage                                  != comprehension proof
pass completion                           != comprehension proof
EXTRACTED_PROPOSITION                     != verified fact
Reader candidate                          != admitted evidence
contradiction candidate                    != confirmed contradiction
similarity                                 != identity
```

RC-3 означает process mechanics, не comprehension. RC-4 означает source-linked candidate registration, не verification. RC-5 означает explicit audited relation suspicion, не contradiction decision.

### «Factual assertion»

В RC-4 `FACTUAL_ASSERTION` означает, что **источник подаёт** proposition как factual. Crystal verification/admission остаётся во внешнем evidence/Guardian/TruthGate path.

### «Evidence extraction»

RC-4 extraction создаёт pre-admission Reader candidates. RC-5 relation registration остаётся над ними. Ни один не вызывает `core.evidence.attach_evidence()` и не пишет `evidence_spans` для admitted fact.

```text
Reader extraction candidate != fact evidence attachment
Reader relation candidate   != confirmed contradiction
source locator               != evidence sufficiency
```

### «Contradiction»

RC-5 намеренно использует `POSSIBLE_CONTRADICTION`, а не confirmed/resolved contradiction. Он не выбирает false/true side, не вызывает `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE` и не создаёт winner.

```text
contradiction candidate != confirmed contradiction
confirmed contradiction != resolved contradiction
repetition              != corroboration
```

### «Similarity»

Semantic/retrieval similarity не является identity proof. RC-5 не добавляет embeddings/ANN или semantic equivalence engine и не выполняет cross-document proposition identity.

### «GDPR compliant», «secure» и «hardened»

Предпочтительные formulations:

```text
GDPR-oriented technical controls
security-relevant checks
hardened against documented threats
```

Не заявляйте legal/GDPR/security certification без external authoritative evidence.

### «Replay»

```text
Receipt replay    = re-check existing evidence
trajectory replay = repeat execution path for evaluation
Reader reread     = explicit source-linked pass over declared regions
Reader provenance = exact locator path back to source version
relation replay   = exact candidate IDs + both-side source provenance + rationale
```

### «Grant funded» или «awarded»

Current public state:

```text
submitted / under review / not awarded
approximate planning amount: €50,000
budget change: none
```

€50,000 = planning only, not approved budget/payment commitment. RC-0..RC-5 merged pre-agreement cannot be renamed future funded delivery.

### «Default backend»

SQLite — ordinary active local-first. PostgreSQL/pgvector — inactive `active=false` import/equivalence target, not ordinary runtime. Import/equivalence != activation.

## Правила перевода

- Сохраняйте code identifiers/contract names unchanged.
- Переводите explanations, не machine identifiers.
- Сохраняйте `physical L3 != strict Canon`.
- Сохраняйте public-query read-only / explicit-ingest write separation.
- Сохраняйте SQLite ordinary runtime и PostgreSQL `active=false`.
- Сохраняйте `import/equivalence != activation`.
- Сохраняйте bounded RC-1..RC-5 vs dedicated/full Reader not implemented.
- Сохраняйте `coverage != comprehension proof`, `pass completion != comprehension proof`, `EXTRACTED_PROPOSITION != verified fact`, `Reader candidate != admitted evidence`, `contradiction candidate != confirmed contradiction`, `similarity != identity`, `repetition != corroboration`.
- Сохраняйте source owner/category/negation/qualifiers и RC-5 relation direction/rationale.
- Сохраняйте no-certification/no-award boundaries.
- Не подразумевайте native-speaker editorial certification.

NLnet: `submitted / under review / not awarded`; `budget change: none`; award: not awarded.

## Связанные authoritative документы

- [Project, grant and governance summary](../PROJECT_GRANT_AND_GOVERNANCE.md)
- [Полная архитектура](../ARCHITECTURE.md)
- [Reader Core architecture contract](../architecture/READER_CORE_ARCHITECTURE.md)
- [Reader implementation status](../IMPLEMENTATION_STATUS.md)
- [Grant scope](../GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](../grants/baseline-funded-delta-matrix.md)
- [Funding use plan](../grants/funding-use-plan.md)
- [Roadmap](../../ROADMAP.md)
- [Governance](../../GOVERNANCE.md)
- [Contributing](../../CONTRIBUTING.md)
