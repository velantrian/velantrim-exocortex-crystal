<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: de -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 Crystal-Schnellstart

Dieser Leitfaden startet die lokale, abhängigkeitfreie Basis, nimmt einen expliziten
Claim auf, fragt ihn über die schreibgeschützte Grenze ab und prüft einen Receipt.

## Voraussetzungen

- Python 3.11 oder 3.12;
- Git;
- ein lokaler Speicherort für Repository und SQLite-Daten.

Der Standardbetrieb benötigt weder LLM noch Embedding-Anbieter oder Cloud-Dienst.
Entwicklungs- und Test-Extras installieren optionale Pakete für die vollständige Testsuite.

## 1. Installation

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Unter Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Repository prüfen

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Exakte Checkpoints und erwartete Kennzahlen stehen in
[TEST_REPORT.md](../../TEST_REPORT.md); sie werden hier nicht als veränderliche
Anforderung dupliziert.

## 3. Persistenten lokalen Speicher wählen

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite ist das gewöhnliche aktive Local-first-Profil. PostgreSQL/pgvector ist nur
ein optionaler inaktiver Import- und Äquivalenzpfad; der Zielzustand bleibt
`active=false`.

## 4. Einen Claim explizit aufnehmen

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` ist ein Schreibvorgang. Der Claim gelangt in den operativen Zustand und
durchläuft den konfigurierten Guardian/TruthGate-Zulassungspfad. Das bedeutet nicht,
dass Crystal die objektive Wahrheit der Aussage selbstständig beweist; die Zulassung
bleibt evidenz- und richtlinienabhängig.

## 5. Über die schreibgeschützte Grenze abfragen

```bash
velantrim ask "how does water behave"
```

Das öffentliche `ask` verwendet `core.query_pipeline.query()` und darf keine
L0/L1-Fakten anlegen oder ändern, ESM-Zustände wechseln, L3 schreiben, die Outbox
betreiben, Episodenbeziehungen speichern, einen nicht gesetzten Embedding-Fingerprint
initialisieren oder unbekannte Kandidaten persistieren.

Wenn strikte kanonische Fundierung fehlt, ist eine begrenzte Ablehnung erwartet.
Eine Ablehnung ist ein gültiges Ergebnis der Vertrauensgrenze und nicht automatisch
ein Laufzeitfehler.

## 6. Receipt erstellen und prüfen

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Ein Receipt versiegelt Anfrage, Antwort und zitierte Fakten-IDs unter einem Digest
und kann Zitate gegen den aktuellen Speicherzustand erneut prüfen. Er macht
Manipulationen erkennbar; optionale HMAC-Signatur benötigt einen lokal konfigurierten
Provenienzschlüssel.

## 7. Optionale API ausführen

```bash
pip install '.[api]'
velantrim-api
```

| Methode | Route | Grenze |
|---|---|---|
| `GET` | `/health` | Liveness/Readiness |
| `POST` | `/ingest` | expliziter Zulassungs-/Schreibpfad |
| `POST` | `/ask` | strikt schreibgeschützte Abfrage |
| `GET` | `/receipt?q=...` | Abfrage plus Receipt |
| `POST` | `/verify-receipt` | Receipt-Replay |
| `GET` | `/evidence/{fact_id}` | richtlinienbewusste Evidenzansicht |

Die API nutzt eine Bearer-Token-Basis. Sie ist kein vollständiges produktives
Multi-Tenant-Autorisierungsmodell.

## 8. MCP-Inspektionsoberfläche starten

```bash
python -m core.mcp_server
```

MCP bietet Inspektionswerkzeuge wie schreibgeschützte Suche, Speicherberichte,
Faktenhistorie, Konfliktsuche und Receipt-Prüfung. Es stellt kein kanonisches
Schreibwerkzeug bereit.

## Häufige Grenzfehler

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- Physisches L3 ist nicht gleich strikter Canon: ein Knoten kann einen nicht
  verifizierten oder nicht aktiven Zustand tragen.
- Hohe Confidence, Duplikathäufigkeit oder Retrieval-Ähnlichkeit sind für sich
  allein keine unabhängige Evidenz.
- Import oder erfolgreiche Äquivalenz ist keine Aktivierung, kein Cutover und
  keine Backend-Auswahl.

## Nächste Dokumente

- [README](../../README.md)
- [Dokumentationskarte](../DOCUMENTATION_MAP.md)
- [Architektur](../ARCHITECTURE.md)
- [Implementierungsstatus](../IMPLEMENTATION_STATUS.md)
- [Testbericht](../../TEST_REPORT.md)
- [Sicherheitsrichtlinie](../../SECURITY.md)
