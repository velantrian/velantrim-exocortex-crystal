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
<!-- current-italian-parity-source: main@e436577dc5ada4692e8fe399da861a44f800e2f1 -->
<!-- current-english-readme-source: main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883 -->
# 🇮🇹 Documentazione Crystal in italiano

Il pacchetto pubblico/localizzato italiano è aggiornato dalla sua presentazione Reader storica alla verità architetturale pubblica **post-RC-9 / post-NLI / RRTIC-v1**. L’inglese resta la primary source e il conflict resolver; la machine/evidence truth va risolta da GitHub live, `docs/ai/**`, implementation manifest, test eseguibili ed exact CI.

## 🧭 Routing

```text
👤 Human
README.it.md
   ↓
docs/it/README.md
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
nli_reader_runtime_filter = false
```

## 📚 Superfici italiane

| Gruppo | Documento | Stato |
|---|---|---|
| Root | [README.it.md](../../README.it.md) | current human-first presentation |
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

## 🛡 Authority Firewall

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
physical L3 != strict Canon
```

Restano preservati anche i boundary storici cross-document:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite resta ordinary active local-first. PostgreSQL/pgvector Reader resta inattivo: `active=false`. NLnet resta **submitted / under review / not awarded**; circa €50,000 è planning only.

## 📎 Provenance di localizzazione

Il checkpoint root italiano storico `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2` resta provenance. Il phased source checkpoint `main@51c205fe048fd69d39fcd47b43e042a50de432bc` continua a far parte del contratto eseguibile D1/D3/D4/D5. Nessuno di questi anchor implica che il pacchetto italiano corrente sia ancora nello stato architetturale storico.

Italian parity refresh audit source: `main@e436577dc5ada4692e8fe399da861a44f800e2f1`. Human-first English README source: `main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883`.

Dopo questo milestone italiano, quattro Reader-dependent locale packs restano `REFRESH_NEEDED`; German, Spanish, French, Italian e Russian sono i current localized detail packs.

## 🌍 Navigazione localizzazione

- [Localization policy](../LOCALIZATION_POLICY.md)
- [Translation status](../TRANSLATION_STATUS.md)

Questi documenti definiscono la semantica dei source checkpoints e impediscono che un vecchio `CURRENT` venga interpretato automaticamente come parity con una fonte inglese successiva.
