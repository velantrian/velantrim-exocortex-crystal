<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: zh-CN -->
# Crystal 快速开始

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

`core.query_pipeline.query()` 保持 read-only。SQLite 是普通 local-first profile；PostgreSQL/pgvector 保持 `active=false`。导入不等于 activation。RC-1/RC-2 是受限 Reader 基础，dedicated multi-pass Reader 尚未实现。
