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
<!-- current-spanish-parity-source: main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb -->
<!-- current-english-readme-source: main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883 -->
# 🇪🇸 Documentación de Crystal en español

El paquete público/localizado español se ha actualizado desde su presentación histórica RC-1/RC-2 hasta la verdad arquitectónica pública **post-RC-9 / post-NLI / RRTIC-v1**. El inglés sigue siendo la primary source y el conflict resolver; la machine/evidence truth se resuelve desde GitHub live, `docs/ai/**`, el implementation manifest, los tests ejecutables y el exact CI.

## 🧭 Routing

```text
👤 Human
README.es.md
   ↓
docs/es/README.md
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

## 📚 Superficies españolas

| Grupo | Documento | Estado |
|---|---|---|
| Root | [README.es.md](../../README.es.md) | current human-first presentation |
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

Las fronteras históricas cross-document permanecen preservadas:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite sigue ordinary active local-first. PostgreSQL/pgvector Reader sigue inactivo: `active=false`. NLnet sigue **submitted / under review / not awarded**; aproximadamente €50,000 es planning only.

## 📎 Provenance de localización

El checkpoint raíz español histórico `main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2` sigue siendo provenance. El phased source checkpoint `main@51c205fe048fd69d39fcd47b43e042a50de432bc` continúa formando parte del contrato ejecutable D1/D3/D4/D5. Ninguno de esos anchors significa que el paquete español actual siga en ese antiguo estado arquitectónico.

Spanish parity refresh audit source: `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`. Human-first English README source: `main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883`.

Después de este milestone español, cinco Reader-dependent locale packs permanecen `REFRESH_NEEDED`; German, French y Russian ya estaban current.

## 🌍 Navegación de localización

- [Localization policy](../LOCALIZATION_POLICY.md)
- [Translation status](../TRANSLATION_STATUS.md)

Estos documentos definen la semántica de los source checkpoints y evitan interpretar automáticamente un `CURRENT` antiguo como paridad con una fuente inglesa posterior.