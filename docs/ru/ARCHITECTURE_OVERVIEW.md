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

**Назначение:** текущая русская architecture entry point.  
**Authority:** merged code, exact CI, `docs/ai/CURRENT_STATE.md` и implementation manifest остаются technical truth.

## Архитектура одним взглядом

```text
exact source/document identity
        ↓
Reader RC-1…RC-4
source/session/structure/pass/proposition artifacts
        ↓
RC-5 same-document relation candidates
        ↓
RC-6 bounded long-context working sets
        ↓
RC-7 explicit cross-document candidate links
        ↓
RC-9 deterministic lexical PRE-ADMISSION discovery
        ↓
RRTIC-v1 typed inspection contract
(architecture only; not a runtime stage)
        ↓
explicit evidence / admission boundary
        ↓
Guardian → TruthGate
        ↓
physical L3 multi-status storage
        ↓
strict Canon read projection
        ↓
read-only retrieval / answer / bounded refusal
```

Главный invariant:

```text
discovery != evidence
inspection != adjudication
similarity != identity
runtime capability != architecture research
```

## Reader capability map

| Layer | Current state | Boundary |
|---|---|---|
| RC-1 | implemented | exact SourceVersion / SourceLocator / ReaderSession foundation |
| RC-2 | implemented | caller-supplied structural map; structure metadata, not truth |
| RC-3 | implemented | deterministic explicit multi-pass mechanics; completion != comprehension proof |
| RC-4 | implemented | source-linked `EXTRACTED_PROPOSITION`; candidate != admitted evidence |
| RC-5 | implemented | same-session/same-version relation candidates |
| RC-6 | implemented | bounded working sets + caller-supplied SUMMARY; summary != evidence |
| RC-7 | implemented | explicit cross-document candidate links with exact two-sided provenance |
| RC-8 | architecture/research | retrieval decision and adversarial evaluation contract |
| RC-9 | implemented | deterministic offline BM25 PRE-ADMISSION candidate discovery |
| Comparator v1 | frozen evaluation | semantic recall recovered; discrimination gate failed |
| NLI neutral-filter v1 | frozen evaluation | discrimination improved; useful-recall safety gate failed |
| RRTIC-v1 | frozen architecture contract | typed suspicion + qualifier diagnostics; no runtime authorization |

`dedicated_reader_core=false` остаётся larger capability truth.

## RC-5 / RC-7 relation boundary

RC-5 сохраняет explicit pre-admission relations внутри одного ReaderSession / exact SourceVersion: `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION`. RRTIC-v1 не заменяет и не auto-register RC-5 relations.

RC-7 сохраняет explicit cross-document candidate links с exact two-sided provenance и caller rationale. Это comparison surface, а не identity/evidence authority.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## Post-RC-9 evaluation → RRTIC-v1

RC-9 показал полезный lexical baseline, но measured cross-lingual/hard-negative gap. Comparator v1 восстановил recall на Evaluation Surface v2, но failed hard-negative discrimination. Preregistered bidirectional NLI neutral filter уменьшил leakage, но потерял useful recall и failed frozen gates.

Post-NLI reassessment классифицировал missing capability как **relation-contract mismatch**: перед будущим discriminator нужен typed relation suspicion + explicit structural qualifier differences.

RRTIC-v1 relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

Qualifier dimensions:

```text
entity_binding
predicate_binding
argument_roles
polarity
modality_quantifier
temporal_version
jurisdiction
condition_direction
units_thresholds
attribution_causality
```

State: `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 не имеет scalar truth/confidence score, accept/reject rule, reranking, model execution, evidence admission, contradiction adjudication, Canon mutation или runtime provider.

```text
RRTIC suspicion    != adjudicated relation
qualifier mismatch != truth decision
NLI label          != proposition identity
NLI contradiction  != contradiction adjudication
evaluation pass    != runtime authorization
```

## Memory и authority layers

| Layer | Role | Authority boundary |
|---|---|---|
| Reader PRE-ADMISSION | source-linked process/proposition/relation/discovery/inspection candidates | no truth/evidence/Canon authority |
| L0 | process-local working state | ephemeral |
| L1 | SQLite operational memory | durable operational state |
| L2 | pending/review staging | candidate/quarantined before final admission |
| physical L3 | graph-oriented multi-status storage | physical storage, not strict Canon |
| strict Canon | `TrustSnapshot` / `CanonicalView` | deny-dominant trusted read projection |

Public query через `core.query_pipeline.query()` read-only. Query не должен мутировать facts, ESM, L3, outbox, episode links, embedding identity или unknown candidates. При недостаточном strict grounding ожидается bounded refusal.

## Storage / PostgreSQL boundary

SQLite — ordinary active local-first profile. PostgreSQL 16 + pgvector остаётся inactive migration/equivalence target.

```text
SQLite backup / verify / inactive restore
→ bounded deterministic logical export
→ PostgreSQL 16 + pgvector preflight
→ inactive target schema
→ serializable import
→ independent read-only re-hash
→ exact equivalence receipt
→ active=false
```

Import/equivalence — operation evidence, **не activation**, backend selection, TruthGate admission, strict Canon membership, cutover, rollback или dual-write. Reader RC-1…RC-9 и RRTIC-v1 не авторизуют PostgreSQL Reader activation.

## Current non-claims

Crystal не заявляет AGI/consciousness, universal truth/zero hallucinations, active PostgreSQL runtime, automatic switching, production multi-tenancy, completed dedicated/full Reader, automatic parser/OCR, semantic/hybrid Reader runtime, Reader FTS/ANN/vector DB, NLI/CrossEncoder runtime filter, RRTIC runtime provider, automatic identity/adjudication/evidence admission/Canon mutation, security/legal/GDPR certification или awarded NLnet funding.

NLnet остаётся **submitted / under review / not awarded**; ~€50,000 — planning context only.

## Localization provenance

Historical Russian RC-7 parity source: `main@ab3ad31c437647535030e371d58f456faf14017b`. Current Russian refresh source: `main@9666781d390e3276a111cb5ee1735f6606a76283`. Исторические markers сохранены и не переписываются задним числом.
