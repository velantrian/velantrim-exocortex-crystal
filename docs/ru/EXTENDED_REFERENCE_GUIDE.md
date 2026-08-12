<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d5-locale: ru -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
<!-- d5-reader: rc5-relation-candidates-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
<!-- rc6-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
# 🇷🇺 Extended Reference Guide — Crystal / Reader RC-7

Extended reviewer/reference boundary: provenance важнее удобного нарратива, новая Reader capability не получает authority автоматически.

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import != activation
```

SQLite ordinary active local-first; PostgreSQL/pgvector inactive `active=false`.

RC-1 связывает source/session. RC-2 — caller-supplied structure. RC-3 — explicit passes. RC-4 — source-linked `EXTRACTED_PROPOSITION`. RC-5 — `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION`. RC-6 — bounded long-context working sets + caller SUMMARY. RC-7 — explicit cross-document link candidates с exact two-sided provenance.

```text
coverage != comprehension proof
pass completion != comprehension proof
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

| Kind | Symmetry | Boundary |
|---|---|---|
| SUPPORTS | directional | comparison candidate, not admitted evidence |
| CONTRADICTS | symmetric | candidate, not confirmed contradiction |
| ELABORATES | directional | elaboration candidate |
| REFERENCES | directional | reference candidate |
| DEFINES | directional | definition candidate |
| EXAMPLE_OF | directional | example candidate |
| PREREQUISITE_FOR | directional | prerequisite candidate |
| SAME_TOPIC | symmetric | same topic, not same proposition |
| POSSIBLE_SAME_CLAIM | symmetric | inspection hypothesis, not identity |

RC-7 требует different `document_id`, current registered RC-4 candidates, OPEN ReaderSession, exact SourceVersion/privacy, registered SegmentCard, completed RC-3 pass, substantive target outcome, recovered RC-2 node и current substantive coverage. Exact session/candidate/pass/node/source/locator provenance и non-empty rationale обязательны.

Optional inspection basis descriptive only; numeric similarity/confidence/identity field отсутствует. RC-7 не выполняет automatic semantic matching, entity resolution, dedupe, corroboration, embeddings/ANN/vector DB, LLM/provider/parser/OCR, evidence admission, truth/ESM/Canon mutation, contradiction winner selection, planner authority, Reader persistence/API/CLI/worker или PostgreSQL activation. `dedicated_reader_core=false`.

```text
Reader candidate/link → explicit evidence/review process (если отдельно инициирован)
→ Guardian → TruthGate → physical L3 / TrustSnapshot / strict Canon projection
```

NLnet **submitted / under review / not awarded**. Приблизительно **€50,000** planning only; **budget change: none**. Pre-agreement merged work — existing baseline.

Русская D5/Reader поверхность `CURRENT` against `main@ab3ad31c437647535030e371d58f456faf14017b`. Historical RC-5/RC-6 markers сохраняются; восемь других supported locales остаются `REFRESH_NEEDED`, 64 docs. Rich translations нельзя заменять short summaries ради статуса.

Security/legal/GDPR certification и native-speaker editorial certification не заявляются.
