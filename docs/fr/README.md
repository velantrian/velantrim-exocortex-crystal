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
<!-- current-french-parity-source: main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2 -->
<!-- current-english-readme-source: main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883 -->
# 🇫🇷 Documentation Crystal en français

Le paquet public/localisé français a été actualisé depuis sa présentation historique RC-1/RC-2 vers la vérité d’architecture publique **post-RC-9 / post-NLI / RRTIC-v1**. L’anglais reste la primary source et le conflict resolver ; la machine/evidence truth se résout depuis GitHub live, `docs/ai/**`, l’implementation manifest, les tests exécutables et l’exact CI.

## 🧭 Routage

```text
👤 Human
README.fr.md
   ↓
docs/fr/README.md
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

## 📚 Surfaces françaises

| Groupe | Document | État |
|---|---|---|
| Root | [README.fr.md](../../README.fr.md) | current human-first presentation |
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
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
physical L3 != strict Canon
```

Les frontières historiques cross-document restent conservées :

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite reste ordinary active local-first. PostgreSQL/pgvector Reader reste inactif : `active=false`. NLnet reste **submitted / under review / not awarded** ; environ €50,000 est planning only.

## 📎 Provenance de localisation

Le checkpoint racine français historique `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2` reste une provenance. Le phased source checkpoint `main@51c205fe048fd69d39fcd47b43e042a50de432bc` reste partie du contrat exécutable D1/D3/D4/D5. Ces deux éléments ne signifient pas que le paquet français courant demeure sur cet ancien état architectural.

French parity refresh audit source: `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`. Human-first English README source: `main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883`.

Après ce milestone français, six autres Reader-dependent locale packs restent `REFRESH_NEEDED`; German et Russian restent déjà current.

## 🌍 Navigation de localisation

- [Localization policy](../LOCALIZATION_POLICY.md)
- [Translation status](../TRANSLATION_STATUS.md)

Ces documents définissent la sémantique des source checkpoints et empêchent qu’un ancien `CURRENT` soit interprété automatiquement comme une parité avec une source anglaise plus récente.