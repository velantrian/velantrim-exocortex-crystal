<!-- translation-source: docs/QUICKSTART.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ar -->
# البدء السريع مع Crystal

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

المسار `core.query_pipeline.query()` للقراءة فقط. SQLite هو الملف المحلي العادي، بينما يبقى PostgreSQL/pgvector بحالة `active=false`. نجاح الاستيراد لا يعني التفعيل. RC-1 وRC-2 أساسان محدودان للـReader، أما الـReader المخصص متعدد المراحل فغير منفذ.
