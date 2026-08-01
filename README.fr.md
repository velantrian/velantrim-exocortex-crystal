# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 **Français** · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Infrastructure de mémoire vérifiable et locale pour des systèmes d’IA dignes de confiance

`v0.3.0` · 🧪 **1853 tests réussis / 12 ignorés** · 🎯 **couverture de 100 %** · 🧬 **7/7 mutants déclarés éliminés** · ✅ **9 tâches CI** · 🐍 **runtime par défaut limité à la bibliothèque standard Python** · ⚖️ **AGPL-3.0**

> Crystal n’est pas un chatbot de plus. C’est une frontière de mémoire, de preuve
> et de décision qui conserve la nature d’une affirmation, son origine, son état
> épistémique, son droit éventuel à fonder une réponse et la manière dont une
> contradiction a été explicitement résolue.

**Checkpoint runtime vérifié :** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — PR #302 fusionnée.  
**Preuves exactes :** [TEST_REPORT.md](./TEST_REPORT.md) et le
[manifeste d’implémentation](./docs/status/implementation-manifest.json).

> Cette traduction conserve les mêmes limites fonctionnelles et de sécurité que
> le README anglais. Les noms d’API stables restent dans leur forme de code.

---

## 🎯 Pourquoi Crystal existe

Les systèmes d’IA mélangent souvent documents sources, déclarations utilisateur,
sorties de modèle, hypothèses, fragments retrouvés et mémoire durable. Un texte
fluide peut alors recevoir une autorité que ses preuves ne justifient pas.

```text
Une affirmation convaincante n’est pas automatiquement fiable.
Un nœud du graphe n’est pas automatiquement du Canon strict.
Un score de retrieval n’est pas une preuve.
Une sortie de modèle n’est pas une source indépendante.
Une contradiction ne choisit pas elle-même son gagnant.
Une étiquette thématique n’est pas un verdict de vérité.
```

## 🧠 Capacités principales

- affirmations typées et cycle de vie épistémique explicite ;
- métadonnées de source, d’evidence span et de provenance ;
- frontières d’admission Guardian et TruthGate ;
- graphe physique L3 multi-états distinct du Canon strict ;
- réconciliation immuable et deny-dominant via `TrustSnapshot` ;
- requêtes publiques HTTP, CLI et MCP strictement en lecture ;
- TRACE et Receipts rejouables, avec détection d’altération ;
- restrictions, effacement, audit et sessions d’import ;
- files de revue et sessions reprenables ;
- rapports de contradiction typés et immuables ;
- décisions `COEXIST`, `CONTEXTUALIZE` et `SUPERSEDE` explicites ;
- résolution de conflits par CLI et HTTP authentifié ;
- rôles de curateur limités par scope et leases locaux de décision ;
- facettes thématiques consultatives qui n’accordent aucune autorité ;
- spécification ESM lisible par machine ;
- évaluation déterministe, couverture de 100 % et mutation gate Ring Zero ;
- historique versionné des benchmarks L3.

## 🏛️ Architecture

```text
ingestion explicite
→ classification + preuve
→ état Observed L0/L1
→ Guardian → TruthGate → contrôles de restriction/contradiction
→ graphe physique L3 multi-états

requête publique
→ retrieval en lecture seule
→ TrustSnapshot immuable
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ réponse / refus / Receipt

contradiction non résolue
→ ContradictionReport immuable
→ autorisation actor/rôle/scope + decision lease
→ décision explicite du curateur + justification
→ écriture canonique auditable

navigation thématique
→ TopicFacet consultative
→ filtrage/regroupement uniquement — jamais d’admission au Canon
```

```text
Graphe L3 physique ≠ Canon strict
requête ≠ ingestion
confiance ≠ preuve indépendante
sortie LLM ≠ source factuelle indépendante
pertinence thématique ≠ vérité
lease local ≠ coordination distribuée garantie
```

TruthGate est une porte de politique d’admission, pas un oracle de vérité
objective. Le Canon strict est une projection de lecture autorisée par les
règles sur la preuve, le statut, l’état ESM et les restrictions de traitement.

## 🛡️ Requêtes publiques en lecture seule

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` et `MCP search` utilisent
`core.query_pipeline`. Ils ne créent pas de faits, ne font pas évoluer ESM,
n’écrivent pas dans L3, ne traitent pas l’outbox et n’initialisent pas d’empreinte
d’embedding.

Voir [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Résolution explicite des contradictions

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "les affirmations décrivent des contextes différents" \
  --expected-report-id REPORT_ID
```

Pour FastAPI, `POST /review/resolve-conflict` doit utiliser l’authentification de
l’application hôte. `core.curator_auth` vérifie l’actor, les capacités et le
scope. `CuratorLeaseRegistry` protège uniquement un processus ; un déploiement
distribué exige un adaptateur de lease externe.

Voir [Conflict-resolution surfaces](./docs/CONFLICT_RESOLUTION_SURFACES.md) et
[Topic facets and curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md).

## 🏷️ Facettes thématiques

`core.topic_facets` fournit des étiquettes normalisées pour la navigation et le
filtrage. Leur score mesure uniquement la pertinence thématique. Il ne modifie ni
le statut de vérité, ni les preuves, ni ESM, ni le Canon strict.

## 🚀 Démarrage rapide

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 Documentation

- [Carte de la documentation](./docs/DOCUMENTATION_MAP.md)
- [Statut actuel](./docs/STATUS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Rapport de tests](./TEST_REPORT.md)
- [Évaluation](./docs/EVAL.md)
- [Périmètre NLnet](./docs/GRANT_NLNET_SCOPE.md)

## ✅ Baseline vérifiée

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 Limite des affirmations

Crystal ne prétend pas détecter universellement la vérité, éliminer toute
hallucination, fournir une certification GDPR ou de sécurité, être prêt pour un
service multi-tenant de production, réaliser une conscience artificielle ou
implémenter Titan/Full ExoCortex. Les leases actuels sont locaux au processus ;
la coordination distribuée et l’intégration d’un fournisseur d’identité restent
des travaux indépendants.

## 🤝 Contribution et licence

Voir [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) et [AGPL-3.0](./LICENSE).
