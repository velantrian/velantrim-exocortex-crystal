<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ja -->
# Crystal クイックスタート

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

`core.query_pipeline.query()` は read-only です。SQLite は通常の local-first profile、PostgreSQL/pgvector は `active=false` のままです。Import は activation ではありません。RC-1/RC-2 は bounded Reader foundation で、dedicated multi-pass Reader は未実装です。
