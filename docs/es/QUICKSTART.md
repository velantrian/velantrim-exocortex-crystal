<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: es -->
# Inicio rápido de Crystal

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

`core.query_pipeline.query()` es read-only. SQLite sigue siendo el perfil local-first normal; PostgreSQL/pgvector permanece `active=false`. Importar no activa el backend. RC-1/RC-2 son fundamentos Reader acotados; el Reader multi-pass dedicado no está implementado.
