# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 **Français** · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### Infrastructure local-first, vérifiable, de mémoire, de preuve et de décision pour des systèmes d’IA dignes de confiance

`v0.3.0` · 🧪 **2078 réussis / 13 ignorés / 0 échec** · 🎯 **9756 instructions / 100,00 % de couverture des lignes** · 🧬 **7/7 mutants Ring Zero éliminés** · ✅ **9 tâches CI permanentes** · 🐍 **runtime par défaut uniquement avec la bibliothèque standard Python** · ⚖️ **AGPL-3.0**

> Crystal n’est ni un chatbot supplémentaire ni un « oracle de vérité » autonome. C’est une frontière de mémoire, de preuve et de décision qui enregistre la nature d’une affirmation, sa source, son état épistémique, son droit éventuel à fonder une réponse et la manière dont une contradiction a été résolue par une décision explicite et auditable.

**Checkpoint runtime vérifié :** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337 fusionnée.  
**Head validé / CI :** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 réussies.  
**Intégration PostgreSQL :** `31256316532` — PostgreSQL 16 et pgvector 0.8.2.  
**Preuves primaires :** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md) et le [manifest machine-readable](./docs/status/implementation-manifest.json).

> **Contrat de traduction :** ce fichier vise une présentation française complète, visuelle et sémantique, et non un résumé. L’anglais reste la source de travail principale. Les autres documents sont traduits progressivement ; voir la [politique de localisation](./docs/LOCALIZATION_POLICY.md) et le [suivi des traductions](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Pourquoi Crystal existe

De nombreux systèmes d’IA mélangent documents sources, déclarations utilisateur, sorties de modèle, hypothèses, fragments retrouvés et mémoire durable dans un même contexte ou magasin vectoriel. Un texte convaincant peut alors acquérir une autorité que ses preuves ne justifient pas.

```text
Une affirmation fluide n’est pas automatiquement fiable.
Un nœud du graphe physique n’est pas automatiquement le Canon strict.
Un score de retrieval n’est pas une preuve.
Une sortie de modèle n’est pas une source factuelle indépendante.
Une contradiction ne choisit pas elle-même son gagnant.
Une étiquette thématique n’est pas un verdict de vérité.
Un import réussi n’est pas une activation du backend.
```

## 🧠 Ce que fournit Crystal

- affirmations typées et cycle de vie épistémique explicite ;
- identité de source, spans de preuve exacts et provenance ;
- frontières d’admission Guardian et TruthGate ;
- graphe physique L3 multi-statut séparé du Canon strict ;
- `TrustSnapshot` immuable et deny-dominant ;
- surfaces publiques HTTP, CLI et MCP en lecture seule ;
- TRACE et Receipts rejouables et détectant les altérations ;
- restrictions, effacement, audit et sessions d’import ;
- files de revue et sessions reprenables ;
- rapports de contradiction immuables ;
- décisions explicites `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE` ;
- capacités de curateur scoped et leases de décision locaux au processus ;
- TopicFacet consultatif sans autorité sur la vérité ;
- évaluation déterministe, couverture 100 % et mutation gate Ring Zero ;
- backup/restore SQLite et migration logique bornée vérifiés ;
- import PostgreSQL/pgvector inactif avec équivalence exacte indépendante.

## 🏛️ Architecture en trois vues

### 🧠 Carte mentale

```text
🧠 Crystal
├── 🎯 Finalité
│   ├── mémoire vérifiable pour l’IA
│   ├── infrastructure de confiance local-first
│   └── réponses et décisions liées aux preuves
├── 🏛️ Mémoire
│   ├── L0 — cache de travail rapide
│   ├── L1 — état opérationnel et cycle de vie
│   ├── L2 — frontière d’attente/revue
│   └── L3 — graphe physique multi-statut
├── 🛡️ Confiance
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Preuve
│   ├── source + span exact
│   ├── provenance
│   ├── TRACE
│   └── Receipt
├── ⚖️ Contradiction
│   ├── file et session de revue
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ Stockage
│   ├── SQLite — profil local-first ordinaire
│   └── PostgreSQL/pgvector — cible inactive
└── 📊 Vérification
    ├── Python 3.11 / 3.12
    ├── couverture 100 %
    ├── mutation / sécurité / Docker
    └── preuve CI exacte
```

### 🏗️ Flux d’information

```text
📥 ingest explicite
        ↓
🧾 type de claim + source + span de preuve exact
        ↓
🧠 état observé dans L0/L1
        ↓
🛡️ Guardian → ⚖️ TruthGate → 🚧 restrictions
        ↓                         ↓
⏳ revue L2                 🏛️ graphe physique L3
        └──────────────┬──────────┘
                       ↓
             📐 TrustSnapshot immuable
                       ↓
          🛡️ Guardian + CanonicalView STRICT
                  ↓                 ↓
          💬 réponse fondée       🚫 refus motivé
                  ↓
             🧾 Receipt rejouable
```

### 🌳 Arbre des modules

```text
🌳 Crystal
├── 🧠 Memory : L0 / L1 / L2 / L3
├── 🛡️ Trust : Guardian / TruthGate / TrustSnapshot / CanonicalView
├── 📜 Evidence : Source / Span / Provenance / TRACE / Receipt
├── ⚖️ Review : Queue / Session / ContradictionReport / Disposition
├── 🔎 Query : HTTP / CLI / MCP
├── 🗄️ Portability : SQLite lifecycle / bundle logique / import PostgreSQL inactif
└── 📊 Verification : tests / couverture / mutation / sécurité / Docker / docs-status
```

## 🧭 Distinctions essentielles

```text
graphe L3 physique    != Canon strict
query                 != ingest
confidence            != preuve indépendante
sortie LLM            != source factuelle indépendante
détection du conflit  != gagnant automatique
pertinence TopicFacet != vérité
Receipt de migration  != preuve d’une affirmation
import réussi         != activation du backend
lease local           != coordination distribuée
```

TruthGate est une passerelle de politique d’admission, pas un oracle. Le Canon strict est une projection de lecture autorisée par la politique sur les preuves, le statut, l’état ESM, la forme de confidence et les restrictions de traitement.

## 🧱 Surfaces de mémoire et de preuve

| Surface | Rôle | Limite critique |
|---|---|---|
| L0 | cache de travail en processus | rapide et reconstructible |
| L1 | mémoire opérationnelle SQLite/WAL | cycle de vie et restrictions |
| L2 | frontière logique de revue | pas automatiquement Canon |
| L3 | mémoire physique multi-statut | présence ≠ confiance |
| TrustSnapshot | réconciliation immuable | résolution deny-dominant |
| CanonicalView | projection stricte | lectures autorisées uniquement |
| TRACE / Receipt | preuve et replay | grounding, dérive, altération |
| ContradictionReport | conflit immuable | confidence ne choisit pas |
| TopicFacet | navigation | ne change ni vérité ni Canon |

## 🗄️ SQLite et PostgreSQL/pgvector

```text
SQLite
└── runtime local-first ordinaire
    ├── lectures/écritures
    ├── backup/restore
    ├── récupération des verrous
    └── export logique canonique borné

PostgreSQL 16 + pgvector
└── profil optionnel de migration/équivalence
    ├── extra optionnel [postgresql]
    ├── chargement paresseux du driver
    ├── nouveau schéma cible
    ├── active=false
    ├── import SERIALIZABLE
    └── équivalence indépendante count/byte/SHA-256
```

La cible PostgreSQL est absente de la composition runtime normale et ne sert aucune lecture ou écriture ordinaire. Un import réussi n’établit ni activation, ni sélection automatique, ni cutover, rollback, dual-write, admission TruthGate, appartenance au Canon, acceptation ANN ou multi-tenancy de production.

## 🔎 Crystal et le RAG classique

| Question | RAG classique | Crystal |
|---|---|---|
| Trouver du contenu pertinent | force principale | adaptateurs de retrieval |
| Séparer déclaration utilisateur et fait vérifié | logique applicative | frontière typée explicite |
| Suivre cycle de vie et contradictions | souvent externe | états et rapports de premier ordre |
| Empêcher le texte généré de devenir sa propre source | non inhérent | invariant Ring Zero |
| Rejouer les preuves d’une réponse | optionnel | TRACE et Receipt |
| Résoudre les contradictions de façon responsable | applicatif | dispositions autorisées |
| Fonctionner sans fournisseur cloud/modèle obligatoire | variable | base local-first pure-stdlib |

## 🛡️ Frontière publique en lecture seule

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` et `MCP search` partagent `core.query_pipeline`. Ils ne créent pas de faits, ne changent pas l’état ESM, n’écrivent pas dans L3 et ne modifient pas le Canon.

## ⚖️ Décision explicite sur une contradiction

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "les affirmations décrivent des contextes différents" \
  --expected-report-id REPORT_ID
```

Le `CuratorLeaseRegistry` ne coordonne que dans un processus. Un déploiement distribué exige un adaptateur de lease externe.

## 🚀 Démarrage rapide

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Outils PostgreSQL inactifs optionnels : `pip install -e '.[postgresql]'`.

## 📚 Navigation

- [Index français](./docs/fr/README.md)
- [Carte anglaise](./docs/DOCUMENTATION_MAP.md)
- [Rapport de tests](./TEST_REPORT.md)
- [Statut](./docs/STATUS.md)
- [Statut d’implémentation](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Sécurité](./SECURITY.md)
- [Périmètre NLnet](./docs/GRANT_NLNET_SCOPE.md)
- [Politique de localisation](./docs/LOCALIZATION_POLICY.md)
- [État des traductions](./docs/TRANSLATION_STATUS.md)

## ✅ Base vérifiée

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
Mutation: 7/7
CI: 9/9
PostgreSQL integration: PostgreSQL 16 + pgvector 0.8.2 réussie
```

## 🚧 Limite des affirmations

Crystal ne revendique ni détection universelle de la vérité, ni zéro hallucination, ni certification juridique GDPR/sécurité, ni multi-tenancy prête pour la production, ni verrouillage distribué, ni AGI ou conscience, ni runtime PostgreSQL actif, ni switching automatique, cutover/rollback, ni Reader Core dédié achevé. La proposition NLnet reste **submitted / under review / not awarded**.

## 🤝 Contribution et licence

Voir [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md), [GOVERNANCE.md](./GOVERNANCE.md) et [AGPL-3.0](./LICENSE).
