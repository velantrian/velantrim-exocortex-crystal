<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: fr -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 Démarrage rapide de Crystal

Ce guide lance la base locale sans dépendance obligatoire, ingère une affirmation
explicite, l’interroge via la frontière en lecture seule et vérifie un Receipt.

## Prérequis

- Python 3.11 ou 3.12 ;
- Git ;
- un emplacement local pour le dépôt et les données SQLite.

Le runtime par défaut n’impose ni LLM, ni fournisseur d’embeddings, ni service cloud.
Les extras de développement et de test installent les paquets optionnels de la suite complète.

## 1. Installation

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Sous Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Vérifier le dépôt

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Le checkpoint exact et les métriques attendues sont maintenus dans
[TEST_REPORT.md](../../TEST_REPORT.md), et non dupliqués ici comme exigences changeantes.

## 3. Choisir le stockage local persistant

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell :

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite reste le profil local-first actif ordinaire. PostgreSQL/pgvector n’est qu’une voie
optionnelle d’import et d’équivalence inactive ; la cible reste `active=false`.

## 4. Ingérer explicitement une affirmation

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` est une écriture. L’affirmation entre dans l’état opérationnel et passe par le
chemin d’admission Guardian/TruthGate configuré. Cela ne signifie pas que Crystal prouve
seul la vérité objective : l’admission dépend des preuves et de la politique.

## 5. Interroger via la frontière en lecture seule

```bash
velantrim ask "how does water behave"
```

Le `ask` public utilise `core.query_pipeline.query()` et ne doit ni créer ni modifier
des faits L0/L1, changer ESM, écrire L3, opérer l’outbox, enregistrer des liens d’épisode,
initialiser une empreinte d’embeddings absente ou persister des candidats inconnus.

En l’absence d’ancrage canonique strict, un refus borné est attendu. C’est un résultat
valide de la frontière de confiance, pas nécessairement une erreur d’exécution.

## 6. Créer et vérifier un Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Un Receipt scelle la requête, la réponse et les identifiants cités sous un digest, puis
peut rejouer les citations contre l’état courant. Il rend les altérations détectables ;
la signature HMAC optionnelle exige une clé locale de provenance.

## 7. Exécuter l’API optionnelle

```bash
pip install '.[api]'
velantrim-api
```

| Méthode | Route | Frontière |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | admission/écriture explicite |
| `POST` | `/ask` | requête strictement en lecture seule |
| `GET` | `/receipt?q=...` | requête plus Receipt |
| `POST` | `/verify-receipt` | rejeu du Receipt |
| `GET` | `/evidence/{fact_id}` | vue des preuves selon la politique |

L’API utilise une base bearer-token. Ce n’est pas un modèle complet d’autorisation
multi-tenant de production.

## 8. Exécuter la surface d’inspection MCP

```bash
python -m core.mcp_server
```

MCP fournit recherche en lecture seule, rapports mémoire, historique des faits,
recherche de conflits et vérification des Receipts. Aucun outil d’écriture canonique
n’est exposé.

## Erreurs fréquentes de frontière

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- Le L3 physique n’est pas le Canon strict.
- Confidence, duplication ou similarité de retrieval ne constituent pas, seules, une preuve.
- Un import ou une équivalence réussie n’est ni activation, ni cutover, ni sélection de backend.

## Documents suivants

- [README](../../README.md)
- [Carte de la documentation](../DOCUMENTATION_MAP.md)
- [Architecture](../ARCHITECTURE.md)
- [État de l’implémentation](../IMPLEMENTATION_STATUS.md)
- [Rapport de tests](../../TEST_REPORT.md)
- [Politique de sécurité](../../SECURITY.md)
