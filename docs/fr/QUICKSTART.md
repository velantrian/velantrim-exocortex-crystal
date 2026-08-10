<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: fr -->
# Démarrage rapide Crystal

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

`core.query_pipeline.query()` reste read-only. SQLite est le profil local-first ordinaire; PostgreSQL/pgvector reste `active=false`. L’import n’est pas une activation. RC-1/RC-2 sont des fondations Reader bornées; le Reader multi-pass dédié n’est pas implémenté.
