# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 **Français** · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md)

### *Infrastructure de mémoire vérifiable, locale et open source pour une IA digne de confiance*

`v0.3.0` · 🧪 **1713 réussis / 12 ignorés** · 🎯 **100 % de couverture** · 🐍 **runtime par défaut fondé sur la bibliothèque standard** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal est une couche de mémoire vérifiable, pas un chatbot supplémentaire.
> Chaque claim conserve sa source, son état épistémique et ses métadonnées de
> provenance. L’admission automatique dans le graphe canonique reste contrôlée
> par **Guardian + TruthGate**.

> **Source normative :** le code fusionné sur GitHub `main` et les documents
> anglais font autorité pour l’implémentation et le périmètre de la subvention.
> Cette version française est une traduction maintenue pour les reviewers,
> institutions et contributeurs francophones. En cas d’écart, consulter
> [README.md](./README.md), [docs/STATUS.md](./docs/STATUS.md) et
> [TEST_REPORT.md](./TEST_REPORT.md).

---

## 🧭 Crystal en une minute

Crystal est le noyau public orienté subvention de Velantrim :

- mémoire opérationnelle locale L0/L1 ;
- backends locaux du graphe canonique L3 ;
- contrôles d’admission Guardian et TruthGate ;
- `CanonicalView` pour les réponses strictement fondées ;
- TRACE, provenance et Receipts rejouables ;
- Evidence Spans, files de revue et sessions d’import ;
- mécanismes techniques d’effacement et de limitation du traitement liés au RGPD ;
- évaluation déterministe et seuils de qualité CI ;
- interfaces FastAPI et MCP optionnelles.

Crystal n’est **pas** Titan, le Personal ExoCortex complet, un système cognitif
autonome, un projet de conscience ou un agent auto-modifiant. Les idées de
recherche peuvent nourrir de futurs RFC, mais elles ne constituent pas des
capacités runtime actuelles.

```text
GitHub Crystal main = vérité d’implémentation publique
Notion Crystal       = carte stratégique et grant synchronisée
Titan / Full         = piste de recherche séparée
```

---

## 🛡️ Frontière de confiance actuelle

### Chemin d’admission

```text
entrée / document / événement d’agent
→ classification et preuves
→ Guardian + TruthGate
→ mémoire opérationnelle L0/L1
→ graphe canonique L3 admis
```

### Chemin de requête HTTP

Le PR #265 a introduit un contrat HTTP de lecture strictement séparé :

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ Canon existant uniquement
→ CanonicalView
→ réponse ou refus borné
```

Pour ces surfaces HTTP, poser une question n’ingère rien dans L0/L1, ne fait pas
évoluer ESM, n’écrit ni fait ni arête L3, ne vide pas l’outbox, n’enregistre pas
de lien épisodique, n’initialise pas d’empreinte d’embedding et ne modifie pas
l’état de vérification adaptative.

### Périmètre résiduel explicitement déclaré

- les commandes CLI `ask` et `receipt` utilisent encore le chemin historique
  compatible avec l’admission ;
- `core.pipeline.run()` reste disponible ;
- MCP ne fournit aucun outil explicite d’écriture canonique, mais une recherche
  peut initialiser une empreinte d’embedding absente.

La garantie de lecture seule est donc volontairement précise, pas généralisée.
Voir la spécification normative
[read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 Modèle de mémoire

| Couche | Rôle | Frontière |
|---|---|---|
| **L0** | cache de travail en mémoire | rapide, reconstruisible |
| **L1** | mémoire opérationnelle SQLite/WAL | états, restrictions, mises à jour |
| **L2** | claims en attente et revue curatoriale | pas automatiquement canonique |
| **L3** | graphe canonique | admission automatique uniquement via TruthGate |
| **TRACE / Receipt** | couche de preuve | explique le fondement et détecte la dérive |

Le graphe physique peut contenir plusieurs statuts de vérité. Au sens strict,
le **Canon** désigne uniquement la projection vérifiée, valide selon TRACE et
autorisée par les règles — pas chaque nœud présent dans un backend de graphe.

---

## 🚀 Démarrage rapide

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

Utilisation CLI de base :

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Backend L3 SQLite persistant et local :

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Guide détaillé : [docs/fr/QUICKSTART.md](./docs/fr/QUICKSTART.md).

---

## 🔌 Interfaces optionnelles

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Méthode | Chemin | Contrat |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | admission via Guardian + TruthGate |
| `POST` | `/ask` | requête canonique strictement en lecture |
| `GET` | `/receipt?q=...` | lecture avec Receipt |
| `POST` | `/verify-receipt` | replay du Receipt contre l’état actuel |
| `GET` | `/evidence/{fact_id}` | vue publique des preuves selon la politique |

FastAPI et Uvicorn sont des extras optionnels. Le runtime par défaut ne nécessite
ni service cloud ni fournisseur de modèle tiers.

### MCP

```bash
python -m core.mcp_server
```

MCP fournit des outils d’inspection pour la recherche, les rapports mémoire,
l’historique des faits, les conflits et la vérification des Receipts. La limite
résiduelle liée à l’empreinte d’embedding reste applicable.

---

## 🧪 Évaluation

Crystal inclut déjà une baseline déterministe :

- `hit@k` et MRR pour le retrieval ;
- complétude TRACE et métadonnées ;
- couverture des Evidence Spans ;
- survie au Receipt replay ;
- précision et rappel de la détection des contradictions ;
- tests de refus aux frontières de confiance ;
- seuils et plafonds de régression CI.

L’implémentation de replay déterministe de Titan est une antériorité technique
revue, pas une runtime Crystal copiée. Toute future implémentation devra étendre
le stack d’évaluation existant, rester hors ligne, non autoritative et préserver
TruthGate ainsi que les frontières de requête.

---

## 💶 Frontière de subvention

Le projet a été soumis au **NLnet NGI0 Commons Fund** et se trouve en cours
d’évaluation. Le dépôt n’affirme pas qu’un financement a déjà été accordé.

```text
BASELINE ACTUELLE
    +
DELTA FINANCÉ MESURABLE
    =
LIVRABLE VÉRIFIABLE INDÉPENDAMMENT
```

Le travail déjà fusionné reste la baseline et n’est pas recompté comme livraison
payée. Les mécanismes cognitifs, neuromorphiques ou Titan ne sont pas ajoutés
silencieusement au périmètre Crystal.

Résumé français : [docs/fr/GRANT_OVERVIEW.md](./docs/fr/GRANT_OVERVIEW.md)  
Sources normatives :

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)

---

## ✅ Portes de vérification

| Gate | Fonction |
|---|---|
| pytest + coverage | suite complète avec seuil obligatoire de 100 % |
| Ruff | lint du code et des outils du dépôt |
| Gitleaks | détection de secrets versionnés |
| Bandit | analyse statique de sécurité Python |
| pip-audit | audit des vulnérabilités de dépendances |
| Docker build | construction reproductible de l’image durcie |
| eval-gate | contrôle des régressions retrieval, grounding et contradictions |
| JSONL integrity | structure du corpus et détection des identifiants dupliqués |

Ces contrôles réduisent le risque ; ils ne prouvent pas l’absence de tout défaut
et ne constituent ni certification juridique ni certification de sécurité.

---

## 📚 Parcours reviewer en français

1. [docs/fr/REVIEWER_GUIDE.md](./docs/fr/REVIEWER_GUIDE.md)
2. [docs/fr/QUICKSTART.md](./docs/fr/QUICKSTART.md)
3. [docs/fr/STATUS.md](./docs/fr/STATUS.md)
4. [docs/fr/GRANT_OVERVIEW.md](./docs/fr/GRANT_OVERVIEW.md)
5. [docs/fr/GLOSSARY.md](./docs/fr/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — résultats normatifs
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — architecture normative

---

## ⚖️ Licence et contribution

Crystal est distribué sous **AGPL-3.0**. Voir [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md) et [PRIVACY.md](./PRIVACY.md).

> **📊 Canon = vérité admise** · **🔗 Provenance = confiance** · **🏠 Local-first = contrôle**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 **Français** · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md)