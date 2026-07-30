# 📌 Velantrim Crystal — Aktueller Status

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md)

**Statusdatum:** 30. Juli 2026  
**Aktueller Repository-Stand für diese Übersetzung:** `main@2641748`  
**Letzter Runtime-verändernder Checkpoint:** PR #265 / `cd6fd44`  
**Verbindliche Testbasis:** [TEST_REPORT.md](../../TEST_REPORT.md)

> Diese Seite ist eine deutsche Statusübersetzung. Bei Abweichungen gelten
> GitHub `main`, der englische [STATUS](../STATUS.md) und
> [TEST_REPORT.md](../../TEST_REPORT.md).

---

## 🧭 Leseregel

```text
GitHub Crystal main = öffentliche Implementierungswahrheit
Notion Crystal       = synchronisierte Grant- und Strategiekarte
Titan / Full         = getrenntes Forschungslabor
```

Ein Dokument, eine Notion-Notiz, ein Prototyp-Branch oder ein Titan-Modul ist
keine aktuelle Crystal-Fähigkeit, solange es nicht in Crystal implementiert,
getestet und nach `main` gemergt wurde.

## ✅ Verifizierter Checkpoint

PR #265 führte die strikt lesende HTTP-Abfragegrenze ein:

```text
POST /ingest   → Zulassung über Guardian + TruthGate
POST /ask      → strikt lesende kanonische Abfrage
GET  /receipt  → strikt lesende Abfrage plus Receipt
```

Die HTTP-Endpunkte `/ask` und `/receipt` schreiben weder L0/L1 noch L3,
führen keine ESM-Transition aus, bedienen nicht die Outbox, speichern keine
Episodenverknüpfung, initialisieren keinen Embedding-Fingerprint und ändern
keinen adaptiven Verifikationszustand.

### Explizite Restgrenzen

- CLI `ask` und `receipt` verbleiben auf `core.pipeline.run()`;
- `core.pipeline.run()` bleibt ein zulassungsfähiger Kompatibilitätspfad;
- MCP besitzt keine expliziten kanonischen Schreibwerkzeuge, aber die Suche kann
  einen noch nicht gesetzten Embedding-Fingerprint initialisieren.

Diese Punkte sind bekannte Follow-ups und keine versteckten
Implementierungsbehauptungen.

## 🧪 Verifikationsbasis

```text
1713 bestanden
12 übersprungen
0 fehlgeschlagen
6389 gemessene Statements
100,00 % Abdeckung
```

Der vor dem Merge ausgeführte CI-Lauf `30284938992` schloss alle sieben
permanenten Jobs erfolgreich ab: Python 3.11/3.12, Ruff, Security, Docker Build,
Evaluation Gate und JSONL-Integrität.

## 🛡️ Zulässige öffentliche Beschreibung

Crystal darf beschrieben werden als:

- lokale, nachweisbare KI-Speicherinfrastruktur;
- quell- und provenienzorientierter Speicherkern;
- System mit Guardian- und TruthGate-Zulassungskontrollen, wo verdrahtet;
- System mit CanonicalView, TRACE und reproduzierbaren Receipts, wo verdrahtet;
- Standardbibliothek-basierte Default-Runtime mit optionalen Adaptern und
  Schnittstellen;
- Projekt mit technisch implementierten Lösch- und
  Verarbeitungseinschränkungsmechanismen mit GDPR-Bezug;
- unabhängig prüfbare Open-Source-Baseline auf Forschungsniveau.

Crystal darf **nicht** beschrieben werden als:

- Titan oder vollständiger persönlicher ExoCortex;
- autonomes kognitives Betriebssystem;
- bewusst, lebendig oder biologisch einem Gehirn gleichwertig;
- universell wahr oder halluzinationsfrei;
- rechtlich GDPR-zertifiziert;
- sicherheitszertifiziert oder produktionsreif für Multi-Tenant-Hosting;
- von einem verpflichtenden externen LLM oder Cloud-Anbieter abhängig.

## 💶 Grant-Status

Der Antrag beim NLnet NGI0 Commons Fund wurde eingereicht und befindet sich in
Prüfung. Das Repository behauptet nicht, dass die Förderung bewilligt wurde.

```text
HEUTIGE BASELINE
    +
MESSBARER FINANZIERTER DELTA
    =
UNABHÄNGIG PRÜFBARES DELIVERABLE
```

Bereits gemergte Arbeit bleibt Baseline und wird nicht erneut als bezahlter
Milestone gezählt. Die verbindlichen Regeln stehen in den englischen Dokumenten:

- [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

Eine deutsche Einordnung steht in [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md).

## 🧪 Evaluation-Replay

Die deterministische Replay-Implementierung aus Titan wurde als Vorarbeit
geprüft. Sie wurde nicht in die Crystal-Runtime kopiert.

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

Eine spätere Umsetzung muss den bestehenden Crystal-Evaluationsstack erweitern,
in einem separaten RFC/Issue/PR erfolgen, offline und nicht autoritativ bleiben
und die TruthGate- sowie Query-Grenzen erhalten.

## 🔬 Forschungs- und Draft-PR-Regel

Offene Forschungs- oder Branding-PRs sind keine Implementierungswahrheit. Vor
einem Merge müssen sie gegen den aktuellen `main` rebased, hinsichtlich
Grant-Sprache neu auditiert und auf Konflikte mit dem verbindlichen Status geprüft
werden.

## 📚 Reviewer-Pfad

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)
4. [GLOSSARY.md](./GLOSSARY.md)
5. [Verbindlicher englischer Status](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md)