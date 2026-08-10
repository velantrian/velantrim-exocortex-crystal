<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->
# Быстрый старт Crystal

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Обычный runtime остаётся local-first и stdlib-only. Публичные запросы проходят через `core.query_pipeline.query()` и являются read-only; явный ingest остаётся отдельным write path.

SQLite — обычный активный local-first профиль. PostgreSQL/pgvector — только опциональная неактивная цель импорта с `active=false`. Import — не activation.

Reader RC-1/RC-2 уже существуют как bounded foundation, но dedicated multi-pass Reader не реализован.
