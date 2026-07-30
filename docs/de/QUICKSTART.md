# 🚀 Schnellstart — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md)
>
> **Hinweis:** Befehle, Paketnamen, Umgebungsvariablen und API-Pfade werden nicht
> übersetzt. Bei Abweichungen gelten die englischen Dokumente und GitHub `main`.

## 1. Repository klonen

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
```

## 2. Virtuelle Umgebung anlegen

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Entwicklungsumgebung installieren

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Die Standard-Runtime von Crystal ist auf die Python-Standardbibliothek
beschränkt. Entwicklungs-, API- und Adapter-Abhängigkeiten sind optionale Extras.

## 4. Vollständige Prüfung ausführen

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

Die verbindliche Baseline steht in
[TEST_REPORT.md](../../TEST_REPORT.md). Der aktuelle dokumentierte Stand lautet:

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

Diese Zahlen sind kein Ersatz für einen eigenen Lauf auf einem sauberen Clone.

## 5. Grundlegende CLI verwenden

### Claim aufnehmen

```bash
velantrim ingest "Water boils at 100C at sea level"
```

Die Aufnahme ist ein Zulassungsvorgang. Neue Claims müssen die bestehenden
Klassifikations-, Guardian- und TruthGate-Grenzen durchlaufen.

### Frage stellen

```bash
velantrim ask "how does water behave"
```

⚠️ Die CLI-Befehle `ask` und `receipt` verwenden derzeit noch den historischen,
zulassungsfähigen Kompatibilitätspfad `core.pipeline.run()`. Die strikte
Null-Schreib-Garantie gilt aktuell für die migrierten HTTP-Endpunkte `/ask` und
`/receipt`, nicht pauschal für jeden Caller.

### Receipt erzeugen und prüfen

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Ein Receipt ist ein versiegelter Nachweis der verwendeten Fakten und
Provenienzbezüge. Replay prüft den Nachweis gegen den aktuellen Zustand und kann
Drift oder Manipulation sichtbar machen.

## 6. Persistenten lokalen L3-Speicher aktivieren

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Der SQLite-Pfad bleibt lokal. Crystal sendet Daten nicht automatisch an einen
Cloud- oder Modellanbieter.

## 7. Optionale FastAPI-Schnittstelle starten

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
velantrim-api
```

Standardadresse:

```text
http://127.0.0.1:8000
```

Beispiel:

```bash
curl http://127.0.0.1:8000/health
```

Wichtige Verträge:

| Methode | Pfad | Verhalten |
|---|---|---|
| `POST` | `/ingest` | Zulassung über Guardian + TruthGate |
| `POST` | `/ask` | strikt lesende Abfrage des vorhandenen Kanons |
| `GET` | `/receipt?q=...` | lesende Abfrage mit Receipt |
| `POST` | `/verify-receipt` | Receipt-Replay |

## 8. Optionalen MCP-Server starten

```bash
python -m core.mcp_server
```

MCP besitzt keine expliziten kanonischen Schreibwerkzeuge. Die Suche kann jedoch
einen noch nicht gesetzten Embedding-Fingerprint initialisieren; deshalb wird MCP
nicht als vollständig mutationsfreier Pfad beschrieben.

## 9. Nächste Dokumente

- [Reviewer-Leitfaden](./REVIEWER_GUIDE.md)
- [Aktueller Status](./STATUS.md)
- [Glossar](./GLOSSARY.md)
- [Verbindliche Architektur](../ARCHITECTURE.md)
- [Verbindliche Evaluation](../EVAL.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md)