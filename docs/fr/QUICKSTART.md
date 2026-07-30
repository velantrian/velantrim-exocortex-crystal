# 🚀 Démarrage rapide — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md)
>
> **Note :** les commandes, noms de paquets, variables d’environnement et chemins
> d’API ne sont pas traduits. En cas d’écart, GitHub `main` et les documents
> anglais font autorité.

## 1. Cloner le dépôt

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
```

## 2. Créer un environnement virtuel

Linux/macOS :

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Installer l’environnement de développement

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Le runtime par défaut de Crystal repose sur la bibliothèque standard Python.
Les dépendances de développement, d’API et d’adaptateurs sont des extras
optionnels.

## 4. Exécuter la vérification complète

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

La baseline normative se trouve dans [TEST_REPORT.md](../../TEST_REPORT.md). Le
checkpoint documenté est :

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

Ces chiffres ne remplacent pas une exécution indépendante sur un clone propre.

## 5. Utiliser la CLI

### Ingérer un claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

L’ingestion est une opération d’admission. Les nouveaux claims passent par les
frontières de classification, Guardian et TruthGate prévues.

### Poser une question

```bash
velantrim ask "how does water behave"
```

⚠️ Les commandes CLI `ask` et `receipt` utilisent encore le chemin historique
`core.pipeline.run()`, capable d’admission. La garantie stricte de zéro écriture
concerne actuellement les endpoints HTTP migrés `/ask` et `/receipt`, pas tous
les callers.

### Produire et vérifier un Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Un Receipt est une preuve scellée des faits et références de provenance utilisés.
Son replay vérifie la preuve contre l’état courant et peut révéler une dérive ou
une altération.

## 6. Activer un stockage L3 local persistant

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Le chemin SQLite reste local. Crystal n’envoie pas automatiquement les données à
un fournisseur cloud ou à un fournisseur de modèle.

## 7. Démarrer l’interface FastAPI optionnelle

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
velantrim-api
```

Adresse par défaut :

```text
http://127.0.0.1:8000
```

Exemple :

```bash
curl http://127.0.0.1:8000/health
```

| Méthode | Chemin | Comportement |
|---|---|---|
| `POST` | `/ingest` | admission via Guardian + TruthGate |
| `POST` | `/ask` | lecture stricte du Canon existant |
| `GET` | `/receipt?q=...` | lecture avec Receipt |
| `POST` | `/verify-receipt` | replay du Receipt |

## 8. Démarrer le serveur MCP optionnel

```bash
python -m core.mcp_server
```

MCP ne fournit aucun outil explicite d’écriture canonique. Une recherche peut
cependant initialiser une empreinte d’embedding absente ; MCP n’est donc pas
décrit comme un chemin entièrement sans mutation.

## 9. Documents suivants

- [Guide reviewer](./REVIEWER_GUIDE.md)
- [État actuel](./STATUS.md)
- [Vue subvention](./GRANT_OVERVIEW.md)
- [Glossaire](./GLOSSARY.md)
- [Architecture normative](../ARCHITECTURE.md)
- [Évaluation normative](../EVAL.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md)