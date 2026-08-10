<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: de -->
# Crystal Schnellstart

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Öffentliche Abfragen über `core.query_pipeline.query()` sind read-only. SQLite ist das normale local-first Profil; PostgreSQL/pgvector bleibt `active=false`. Import ist keine Aktivierung. RC-1/RC-2 sind bounded Reader-Grundlagen; der dedicated multi-pass Reader fehlt weiterhin.
