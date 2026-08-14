<!-- localization-index-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d1-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d1-status: CURRENT -->
<!-- d2-source: main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- d2-status: CURRENT -->
<!-- d3-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d3-status: CURRENT -->
<!-- d4-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d4-status: CURRENT -->
<!-- d5-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d5-status: CURRENT -->
<!-- rc6-localization-index-source: main@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc6-status: CURRENT -->
<!-- rc7-localization-index-source: main@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-russian-parity-source: main@9666781d390e3276a111cb5ee1735f6606a76283 -->
<!-- current-english-readme-source: main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883 -->
# 🇷🇺 Русская документация Crystal

Русский public/localized пакет обновлён с исторической RC-7 parity до текущей **post-RC-9 / post-NLI / RRTIC-v1** public architecture truth. English остаётся primary source и conflict resolver; machine/evidence truth разрешается из live GitHub, `docs/ai/**`, implementation manifest, exact tests и CI.

## 🧭 Маршрутизация

```text
👤 Human
README.ru.md
   ↓
docs/ru/README.md
   ↓
ARCHITECTURE_OVERVIEW.md
   ↓
STATUS.md + IMPLEMENTATION_STATUS.md

🤖 AI / automated auditor
docs/ai/README.md
   ↓
AGENTS.md
   ↓
docs/status/implementation-manifest.json
   ↓
English authoritative contracts / tests / exact CI
```

## 📊 Current Reader truth

```text
RC-1…RC-7            = implemented bounded layers
RC-8                  = completed architecture/research decision
RC-9                  = implemented lexical PRE-ADMISSION discovery
Comparator v1         = frozen evaluation / gate FAIL
NLI neutral-filter v1 = frozen evaluation / gate FAIL
RRTIC-v1              = frozen architecture contract only
semantic runtime      = not authorized
dedicated Reader      = not implemented
```

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
```

## 📚 Русские surfaces

| Группа | Документ | Статус |
|---|---|---|
| Root | [README.ru.md](../../README.ru.md) | current human-first presentation |
| D1 | [Quick Start](./QUICKSTART.md) | CURRENT; source semantics unchanged |
| D1 | [Status](./STATUS.md) | current post-RRTIC parity |
| D1 | [Implementation Status](./IMPLEMENTATION_STATUS.md) | current post-RRTIC parity |
| D2 | [Reviewer Guide](./REVIEWER_GUIDE.md) | CURRENT; unchanged D2 source |
| D2 | [Safety/Privacy/Failures](./SAFETY_PRIVACY_AND_FAILURES.md) | CURRENT; unchanged D2 source |
| D3 | [Architecture Overview](./ARCHITECTURE_OVERVIEW.md) | current post-RRTIC parity |
| D3 | [Storage/Authority](./STORAGE_AND_AUTHORITY_BOUNDARIES.md) | current authority/storage parity |
| D4 | [Grant Overview](./GRANT_OVERVIEW.md) | current grant-safe parity |
| D4 | [Glossary](./GLOSSARY.md) | current Reader/RRTIC terminology |
| D5 | [Extended Reference Guide](./EXTENDED_REFERENCE_GUIDE.md) | current reviewer/reference parity |

## 🛡 Authority firewall

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
physical L3 != strict Canon
```

Historical RC-7 compatibility literals remain:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite ordinary active local-first. PostgreSQL/pgvector Reader inactive `active=false`. NLnet **submitted / under review / not awarded**; ~€50,000 planning only.

## 📎 Localization provenance

RC-5 source `51c205fe048fd69d39fcd47b43e042a50de432bc`, RC-6 `ed96a88369f841bdb2ffd79ca020acef174685fc` и RC-7 `ab3ad31c437647535030e371d58f456faf14017b` сохраняются как immutable audit evidence. Они больше не означают, что текущий русский package останавливается на RC-7.

Current Russian parity refresh audit source: `main@9666781d390e3276a111cb5ee1735f6606a76283`. Human-first English README source: `main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883`.

Восемь других Reader-dependent locale packs не обновлены этим milestone и остаются `REFRESH_NEEDED` там, где это записано ledger.

## 🌍 Localization navigation

- [Localization policy](../LOCALIZATION_POLICY.md)
- [Translation status](../TRANSLATION_STATUS.md)

Эти два документа определяют source checkpoint semantics и не позволяют историческому `CURRENT` автоматически означать parity с более новым English source.
