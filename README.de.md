# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](./README.fr.md)  
> 📚 [Deutsche Dokumentation](./docs/de/README.md) · [Documentation française](./docs/fr/README.md)

### *Nachweisbare, lokale und quelloffene Speicherinfrastruktur für vertrauenswürdige KI*

`v0.3.0` · 🧪 **1713 bestanden / 12 übersprungen** · 🎯 **100 % Abdeckung** · 🐍 **Standardlaufzeit nur mit Python-Standardbibliothek** · ⚖️ **AGPL-3.0** · 🔒 **Local-first**

> Crystal ist eine nachweisbare Speicherschicht – kein weiterer Chatbot. Fakten
> tragen Quelle, epistemischen Zustand und Provenienzmetadaten. Die automatische
> Aufnahme in den kanonischen Graphen bleibt durch **Guardian + TruthGate**
> geregelt.

> **Verbindliche Quelle:** Der englische Stand auf GitHub `main` ist die
> Implementierungs- und Grant-Wahrheit. Diese deutsche Fassung ist eine
> gepflegte Übersetzung für deutschsprachige Prüferinnen, Prüfer und
> Mitwirkende. Bei Abweichungen gelten die englischen Dokumente und
> [TEST_REPORT.md](./TEST_REPORT.md).

---

## 🧭 Crystal in einer Minute

Crystal ist der öffentliche, grant-orientierte Kern von Velantrim:

- lokale L0/L1-Arbeitsspeicherung;
- lokale L3-Backends für den kanonischen Wissensgraphen;
- Guardian- und TruthGate-Zulassungskontrollen;
- CanonicalView für streng begründete Antworten;
- TRACE, Provenienz und reproduzierbare Receipts;
- Evidenzspannen, Review-Warteschlangen und Importsitzungen;
- technisch umgesetzte Lösch- und Verarbeitungseinschränkungen mit GDPR-Bezug;
- deterministische Evaluation und CI-Qualitätsgrenzen;
- optionale FastAPI- und lesend ausgerichtete MCP-Schnittstellen.

Crystal ist **nicht** Titan, der vollständige persönliche ExoCortex, ein autonomes
kognitives Betriebssystem, ein Bewusstseinsprojekt oder ein selbstverändernder
Agent. Forschungsideen können spätere RFCs beeinflussen, sind aber keine aktuellen
Runtime-Behauptungen.

```text
GitHub Crystal main = öffentliche Implementierungswahrheit
Notion Crystal       = synchronisierte Strategie- und Grant-Karte
Titan / Full         = getrennte Forschungslinie
```

---

## 🛡️ Vertrauensgrenze

### Zulassungspfad

```text
Eingabe / Dokument / Agentenereignis
→ Klassifikation und Evidenz
→ Guardian + TruthGate
→ operative L0/L1-Speicherung
→ zugelassener kanonischer L3-Graph
```

### HTTP-Abfragepfad

Der in PR #265 eingeführte HTTP-Pfad ist bewusst getrennt:

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ nur bereits vorhandener Kanon
→ CanonicalView
→ Antwort oder begrenzte Ablehnung
```

Für diese HTTP-Endpunkte führt eine Frage nicht zu einer Aufnahme in L0/L1,
keiner ESM-Transition, keinem Schreiben von L3-Fakten oder -Kanten, keinem
Outbox-Lauf, keiner Episodenverknüpfung, keiner Initialisierung eines
Embedding-Fingerprints und keiner Änderung adaptiver Verifikationszustände.

### Ehrlich ausgewiesene Restgrenzen

- CLI `ask` und `receipt` verwenden weiterhin den historischen,
  zulassungsfähigen Kompatibilitätspfad;
- `core.pipeline.run()` bleibt verfügbar;
- MCP besitzt kein explizites kanonisches Schreibwerkzeug, kann bei der Suche
  jedoch einen noch nicht gesetzten Embedding-Fingerprint initialisieren.

Technische Details stehen in der englischen, verbindlichen Spezifikation:
[read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 Speichermodell

| Ebene | Aufgabe | Grenze |
|---|---|---|
| **L0** | Prozessinterner Arbeitscache | schnell, rekonstruierbar |
| **L1** | Operativer SQLite/WAL-Speicher | Zustände, Einschränkungen, Aktualisierungen |
| **L2** | Ausstehende Claims und Kurator-Review | nicht automatisch kanonisch |
| **L3** | Kanonischer Graph | automatische Aufnahme nur über TruthGate |
| **TRACE / Receipt** | Nachweisschicht | erklärt Begründung und erkennt Drift |

Der physische Graph kann unterschiedliche Wahrheitszustände enthalten. Im
strengen Sinn bezeichnet **Kanon** nur die verifizierte, TRACE-gültige und
richtlinienkonforme Projektion – nicht jeden Knoten eines Graph-Backends.

---

## 🚀 Schnellstart

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

Grundlegende CLI-Nutzung:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Persistenter, dependency-freier L3-Speicher:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Eine schrittweise deutsche Anleitung steht in
[docs/de/QUICKSTART.md](./docs/de/QUICKSTART.md).

---

## 🔌 Optionale Schnittstellen

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Methode | Pfad | Vertrag |
|---|---|---|
| `GET` | `/health` | Liveness/Readiness |
| `POST` | `/ingest` | Zulassung über Guardian + TruthGate |
| `POST` | `/ask` | strikt lesende kanonische Abfrage |
| `GET` | `/receipt?q=...` | lesende Abfrage mit Receipt |
| `POST` | `/verify-receipt` | Receipt gegen aktuellen Zustand prüfen |
| `GET` | `/evidence/{fact_id}` | richtlinienbewusste Evidenzansicht |

FastAPI und Uvicorn sind optionale Extras. Die Standardlaufzeit benötigt weder
einen Cloud-Dienst noch einen externen Modellanbieter.

### MCP

```bash
python -m core.mcp_server
```

MCP stellt inspektionsorientierte Werkzeuge für Suche, Speicherberichte,
Faktenhistorie, Konflikte und Receipt-Prüfung bereit. Die oben genannte
Fingerprint-Restgrenze bleibt bestehen.

---

## 🧪 Evaluation

Crystal enthält bereits eine deterministische Evaluationsbasis:

- Retrieval `hit@k` und MRR;
- TRACE- und Metadatenvollständigkeit;
- Abdeckung von Evidenzspannen;
- Überlebensrate des Receipt-Replays;
- Präzision und Recall der Widerspruchserkennung;
- Tests der Vertrauensgrenzen und korrekten Ablehnung;
- CI-Regressionsgrenzen.

Der weitergehende Replay-Ansatz aus Titan ist dokumentierte Vorarbeit, aber
**keine Crystal-Runtime**. Eine spätere Umsetzung muss den vorhandenen
Crystal-Evaluationsstack erweitern, offline und nicht autoritativ bleiben und
die Grant-Regel für Baseline und finanzierten Delta bewahren.

---

## 💶 Grant-Grenze

Das Projekt wurde beim **NLnet NGI0 Commons Fund** eingereicht und befindet sich
in Prüfung. Das Repository behauptet nicht, dass eine Förderung bereits bewilligt
wurde.

```text
HEUTIGE BASELINE
    +
MESSBARER FINANZIERTER DELTA
    =
UNABHÄNGIG PRÜFBARES DELIVERABLE
```

Bereits gemergte Arbeit bleibt Baseline und wird nicht erneut als bezahltes
Deliverable gezählt. Neue kognitive, neuromorphe oder Titan-Mechanismen werden
nicht stillschweigend in den Crystal-Grant aufgenommen.

Deutsche Übersicht: [docs/de/GRANT_OVERVIEW.md](./docs/de/GRANT_OVERVIEW.md)  
Verbindliche englische Dokumente:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)

---

## ✅ Prüf- und Qualitätsgates

| Gate | Zweck |
|---|---|
| pytest + Coverage | vollständige Suite mit verpflichtenden 100 % Zeilenabdeckung |
| Ruff | Linting für Produktions- und Repository-Werkzeuge |
| Gitleaks | Erkennung eingecheckter Secrets |
| Bandit | statische Python-Sicherheitsprüfung |
| pip-audit | Meldung bekannter Dependency-Schwachstellen |
| Docker Build | reproduzierbarer gehärteter Image-Build |
| eval-gate | Kontrolle von Retrieval-, Grounding- und Widerspruchsregressionen |
| JSONL Integrity | Struktur- und Duplikatprüfung des Korpus |

Diese Kontrollen reduzieren Risiken. Sie beweisen nicht die Fehlerfreiheit und
stellen weder eine rechtliche noch eine Sicherheitszertifizierung dar.

---

## 📚 Deutscher Reviewer-Pfad

1. [docs/de/REVIEWER_GUIDE.md](./docs/de/REVIEWER_GUIDE.md)
2. [docs/de/QUICKSTART.md](./docs/de/QUICKSTART.md)
3. [docs/de/STATUS.md](./docs/de/STATUS.md)
4. [docs/de/GRANT_OVERVIEW.md](./docs/de/GRANT_OVERVIEW.md)
5. [docs/de/GLOSSARY.md](./docs/de/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — verbindliche Testergebnisse
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — verbindliche Architektur

---

## ⚖️ Lizenz und Mitwirkung

Crystal steht unter **AGPL-3.0**. Siehe [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md) und [PRIVACY.md](./PRIVACY.md).

> **📊 Kanon = zugelassene Wahrheit** · **🔗 Provenienz = Vertrauen** · **🏠 Local-first = Kontrolle**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](./README.fr.md)
