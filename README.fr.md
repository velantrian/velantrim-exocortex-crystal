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

## 🏛️ Architecture en un coup d’œil

Les trois cartes suivantes présentent le même système selon des angles
complémentaires : **objectif**, **flux d’information** et **relations entre modules**.

### 🧠 Mindmap — objectif et limites de capacité

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 Objectif
│   ├── Mémoire vérifiable pour l’IA
│   ├── Infrastructure de confiance locale
│   └── Réponses et décisions fondées sur des preuves
│
├── 🏛️ Modèle de mémoire
│   ├── L0 — cache de travail dans le processus
│   ├── L1 — mémoire opérationnelle du cycle de vie
│   ├── L2 — frontière pending / revue
│   └── L3 — mémoire graphée multi-états
│
├── 🛡️ Frontière de confiance
│   ├── Guardian — contrôles structurels et de politique
│   ├── TruthGate — frontière de politique d’admission
│   ├── TrustSnapshot — réconciliation de lecture immuable
│   └── CanonicalView — projection stricte de confiance
│
├── 📜 Preuve et auditabilité
│   ├── Provenance et evidence spans
│   ├── TRACE — lignée du grounding
│   └── Receipt — rejeu et détection d’altération
│
├── ⚖️ Revue et contradictions
│   ├── Files de revue et sessions reprenables
│   ├── ContradictionReport immuable
│   ├── COEXIST
│   ├── CONTEXTUALIZE
│   └── SUPERSEDE
│
├── 🏷️ Navigation consultative
│   └── TopicFacet — métadonnées multi-label non autoritatives
│
├── 🔐 Gouvernance et coordination
│   ├── Rôles et capacités de curateur limités par scope
│   ├── Liaison à l’actor authentifié
│   └── Decision leases locaux au processus
│
└── 📊 Vérification
    ├── Tests et évaluation déterministes
    ├── Couverture de lignes à 100 %
    ├── Mutation gate Ring Zero
    └── Historique versionné des benchmarks
```

### 🏗️ Architecture ASCII — circulation de l’information

```text
┌─────────────────────────────────────────────────────────────────────┐
│              🔱 Velantrim ExoCortex — Crystal                      │
│       Infrastructure locale de mémoire vérifiable pour l’IA        │
└─────────────────────────────────────────────────────────────────────┘

                         📥 Ingestion explicite
                                  │
                                  ▼
                🧾 Type d’affirmation + source + evidence span
                                  │
                                  ▼
                         🧠 État Observed L0 / L1
                                  │
                                  ▼
          🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 restrictions
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
            ⏳ L2 pending / revue       🏛️ Graphe physique L3
                    │                           │
                    │                           ▼
                    │                 📜 provenance / TRACE
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                       📐 TrustSnapshot immuable
                                  │
                                  ▼
                 🛡️ Guardian + CanonicalView STRICT
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
            💬 Réponse fondée          🚫 Refus borné
                    │
                    ▼
                 🧾 Receipt rejouable

⚖️ Contradiction non résolue
        │
        ▼
📋 ContradictionReport immuable
        │
        ▼
🔐 principal limité par scope + capacité + decision lease
        │
        ▼
🧑‍⚖️ COEXIST / CONTEXTUALIZE / SUPERSEDE explicite
        │
        ▼
📜 chemin d’écriture canonique auditable

🏷️ Métadonnées TopicFacet ──► navigation / filtrage / regroupement
                             └─► jamais d’autorité sur vérité, ESM, preuve ou Canon
```

### 🌳 Arbre des relations — connexion entre les modules

```text
🌳 Relations du système Crystal
│
├── 🧠 Couche mémoire
│   ├── L0 ──► cache de travail rapide et reconstructible
│   ├── L1 ──► cycle de vie, restrictions et travail en attente
│   ├── L2 ──► frontière logique de revue
│   └── L3 ──► stockage graphé multi-états
│
├── 🛡️ Couche de confiance
│   ├── Guardian ──► validation structurelle et de politique
│   ├── TruthGate ──► décision d’admission
│   ├── TrustSnapshot ──► réconciliation L1/L3 deny-dominant
│   └── CanonicalView ──► projection stricte de grounding
│
├── 📜 Couche de preuve
│   ├── Métadonnées de source
│   ├── Evidence spans
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Couche de revue
│   ├── File de revue
│   ├── Session de revue reprenable
│   ├── ContradictionReport
│   └── Disposition explicite
│       ├── COEXIST
│       ├── CONTEXTUALIZE
│       └── SUPERSEDE
│
├── 🔐 Couche d’autorisation
│   ├── CuratorPrincipal
│   ├── Rôle et capacité limités par scope
│   ├── Correspondance avec l’actor authentifié
│   └── Decision lease local au processus
│
├── 🏷️ Couche consultative
│   └── TopicFacet
│       ├── multi-label
│       ├── score limité à la pertinence
│       └── aucune autorité sur la vérité ou l’admission
│
├── 🔎 Couche de requête publique
│   ├── HTTP /ask et /receipt
│   ├── CLI ask et receipt
│   └── MCP search
│       └── pipeline commun de requête en lecture seule
│
└── 📊 Couche de vérification
    ├── Tests Python 3.11 / 3.12
    ├── Seuil de couverture
    ├── Mutation gate Ring Zero
    ├── Contrôles de sécurité et de conteneur
    └── Historique des benchmarks
```

### Distinctions centrales

```text
Graphe L3 physique ≠ Canon strict
requête ≠ ingestion
confiance ≠ preuve indépendante
sortie LLM ≠ source factuelle indépendante
contradiction ≠ gagnant automatique
pertinence thématique ≠ vérité ou qualité de preuve
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
