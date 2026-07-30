# 🇩🇪 Deutsche Dokumentation — Velantrim Crystal

> 🌐 [Deutscher Projektüberblick](../../README.de.md) ·
> [English documentation](../../README.md)

## 🔒 Übersetzungs- und Autoritätsregel

Diese Seiten sind eine gepflegte deutschsprachige Orientierung für Reviewer,
Institutionen und Mitwirkende. Sie ändern weder Runtime noch Grant-Scope.

```text
GitHub main + englische Kerndokumente = verbindliche Quelle
Deutsche Dokumente                  = Übersetzung und Lesehilfe
```

Bei einer Abweichung gelten:

1. der tatsächlich gemergte Code auf GitHub `main`;
2. [TEST_REPORT.md](../../TEST_REPORT.md) für Test- und Coverage-Zahlen;
3. [docs/STATUS.md](../STATUS.md) für den aktuellen Implementierungsstatus;
4. die englischen Grant-Dokumente für Umfang, Budget und Deliverables.

Eine Übersetzung darf keine Fähigkeit stärker darstellen als das englische
Original. Begriffe wie „GDPR-orientiert“, „gehärtet“, „nachweisbar“ oder
„lokal“ sind technische Beschreibungen und keine Rechts- oder
Sicherheitszertifikate.

---

## 🧭 Empfohlener Lesepfad

| Reihenfolge | Dokument | Zweck |
|---:|---|---|
| 1 | [README auf Deutsch](../../README.de.md) | Projekt, Grenzen und Architektur in komprimierter Form |
| 2 | [Reviewer-Leitfaden](./REVIEWER_GUIDE.md) | Was ein externer Reviewer prüfen sollte |
| 3 | [Schnellstart](./QUICKSTART.md) | Installation, Tests, CLI und optionale API |
| 4 | [Aktueller Status](./STATUS.md) | Implementierungs- und Behauptungsgrenzen |
| 5 | [Grant-Übersicht](./GRANT_OVERVIEW.md) | Grant-sichere deutsche Zusammenfassung |
| 6 | [Glossar](./GLOSSARY.md) | Konsistente technische Terminologie |

---

## 📚 Verbindliche englische Kerndokumente

| Dokument | Verbindlicher Inhalt |
|---|---|
| [README.md](../../README.md) | öffentlicher Einstieg und aktuelle Kernbehauptungen |
| [TEST_REPORT.md](../../TEST_REPORT.md) | reproduzierbare Test- und Coverage-Baseline |
| [docs/STATUS.md](../STATUS.md) | aktueller Implementierungsstatus |
| [docs/REVIEWER_GUIDE.md](../REVIEWER_GUIDE.md) | englischer Reviewer-Pfad |
| [docs/ARCHITECTURE.md](../ARCHITECTURE.md) | Architektur- und Speichergrenzen |
| [docs/EVAL.md](../EVAL.md) | Evaluationsmethodik |
| [docs/GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md) | eingereichter Grant-Scope |
| [Baseline-/Delta-Matrix](../grants/baseline-funded-delta-matrix.md) | Milestones und Akzeptanznachweise |
| [Funding Use Plan](../grants/funding-use-plan.md) | Budgetplanung und Priorisierung |

---

## 🛠️ Pflegekonvention

Bei Änderungen an einem übersetzten Bereich gilt:

```text
1. englische Quelle aktualisieren und mergen
2. aktuellen main-Stand prüfen
3. deutsche Übersetzung in separatem docs-only PR synchronisieren
4. keine neuen Zahlen oder Claims nur in der Übersetzung einführen
```

Der deutsche Paketstand wurde auf Basis von Crystal `main@d82abc7` erstellt.
Der letzte Runtime-verändernde Checkpoint bleibt PR #265 / `cd6fd44`; die
nachfolgende Änderung PR #266 war dokumentations- und grantbezogen.
