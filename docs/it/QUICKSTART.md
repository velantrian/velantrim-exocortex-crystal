<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: it -->
# Avvio rapido Crystal

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

`core.query_pipeline.query()` è read-only. SQLite resta il profilo local-first ordinario; PostgreSQL/pgvector resta `active=false`. Import non significa activation. RC-1/RC-2 sono fondamenta Reader bounded; il Reader multi-pass dedicato non è implementato.
