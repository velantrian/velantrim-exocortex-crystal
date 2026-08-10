<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: hi -->
# Crystal त्वरित प्रारंभ

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

`core.query_pipeline.query()` read-only है। SQLite सामान्य local-first profile है; PostgreSQL/pgvector `active=false` रहता है। Import activation नहीं है। RC-1/RC-2 bounded Reader foundations हैं; dedicated multi-pass Reader अभी लागू नहीं है।
