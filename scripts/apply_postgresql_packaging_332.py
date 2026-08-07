from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "pyproject.toml"
text = path.read_text()
needle = '    "requests>=2.28",         # core/adapters wikidata adapter (WP4)\n]'
replacement = '    "requests>=2.28",         # core/adapters wikidata adapter (WP4)\n    "psycopg[binary]>=3.3,<3.4", # optional PostgreSQL migration profile tests\n]'
if text.count(needle) != 1:
    raise SystemExit("dev extra marker mismatch")
text = text.replace(needle, replacement, 1)
marker = '# L3 graph backend. On first durable environment-selected startup, `auto`\n'
extra = '''# Optional institutional PostgreSQL/pgvector migration profile. The driver is
# lazy-loaded only by explicit inactive-import/verification operator commands.
# The default install remains pure standard library.
postgresql = [
    "psycopg[binary]>=3.3,<3.4",
]
'''
if text.count(marker) != 1:
    raise SystemExit("optional extra marker mismatch")
text = text.replace(marker, extra + marker, 1)
path.write_text(text)
Path(__file__).unlink()
