# 📖 Glossar — Velantrim Crystal auf Deutsch

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 [日本語](../ja/GLOSSARY.md)
>
> Dieses Glossar vereinheitlicht die deutsche Sprache, ersetzt aber keine
> englische API-, Schema- oder Codebezeichnung. Bezeichner in Codeblöcken und
> Schnittstellen bleiben unverändert.

## Grundregel

Technische Eigennamen wie `TruthGate`, `Guardian`, `CanonicalView`, `TRACE` und
`Receipt` werden nicht vollständig eingedeutscht. Beim ersten Auftreten kann
eine deutsche Erklärung ergänzt werden; der Codebegriff bleibt sichtbar.

| Englischer Begriff | Bevorzugte deutsche Form | Bedeutung / Grenze |
|---|---|---|
| **admission** | Zulassung / Aufnahmeentscheidung | Entscheidung, ob ein Claim in einen stärker vertrauten Speicherzustand gelangen darf |
| **claim** | Claim / Aussage | typisierte Behauptung; nicht automatisch eine verifizierte Tatsache |
| **Canon** | Kanon | streng zugelassene, TRACE-gültige und richtlinienkonforme Wissensprojektion |
| **canonical graph** | kanonischer Graph | L3-Graph, der zugelassene Wissensobjekte und explizite Status tragen kann |
| **Guardian** | Guardian / Struktur- und Sicherheitsprüfung | vorgelagerte Prüfung; ersetzt TruthGate nicht |
| **TruthGate** | TruthGate / epistemische Zulassungsgrenze | kontrolliert automatische Aufnahme in den Kanon anhand von Typ, Quelle, Evidenz und Richtlinie |
| **CanonicalView** | CanonicalView / kanonische Lesesicht | fail-closed Projektion für streng begründete Antworten |
| **TRACE** | TRACE / Nachweispfad | maschinenlesbare Begründungskette einer Antwort |
| **Receipt** | Receipt / versiegelter Nachweis | reproduzierbarer, manipulationssensitiver Nachweis über Fakten und Provenienz |
| **receipt replay** | Receipt-Replay | erneute Prüfung eines Receipts gegen den aktuellen Speicherzustand |
| **trajectory replay** | Trajektorien-Replay / Ablauf-Replay | Wiederholung eines Ausführungspfads zur Evaluation; nicht dasselbe wie Receipt-Replay |
| **provenance** | Provenienz / Herkunftsnachweis | Quelle, Entstehungsweg und Lebenszyklus eines Claims |
| **evidence span** | Evidenzspanne / Quellenausschnitt | referenzierter Abschnitt einer Quelle, der einen Claim stützt |
| **epistemic state** | epistemischer Zustand | Status, der ausdrückt, wie ein Claim eingeordnet ist; keine bloße Konfidenzzahl |
| **source status** | Quellenstatus | Herkunftsklasse, etwa extern, nutzergemeldet oder Modelloutput |
| **grounding** | Begründung / evidenzbasierte Verankerung | Rückführung einer Antwort auf zugelassene Claims und Quellen |
| **FactsPack** | FactsPack / kontrolliertes Faktenpaket | kompakter, nachvollziehbarer Kontext für Antworterzeugung |
| **read-only query** | lesende Abfrage | Abfragevertrag ohne die ausdrücklich ausgeschlossenen Speicher- und Zustandsmutationen |
| **fail-closed** | im Zweifel ablehnend | bei unklarer oder widersprüchlicher Vertrauenslage wird nicht stillschweigend zugelassen |
| **baseline** | Baseline / Ausgangsstand | bereits implementierter und verifizierter Stand vor finanziertem Zusatzaufwand |
| **funded delta** | finanzierter Delta | messbare zusätzliche Arbeit, die durch die Förderung geliefert werden soll |
| **deliverable** | Deliverable / prüfbares Ergebnis | öffentliches Artefakt mit definiertem Akzeptanznachweis |
| **local-first** | local-first / lokal als Standard | lokale Datenhaltung und Ausführung sind der Normalfall; externe Dienste sind optional |
| **stdlib-only runtime** | Standardlaufzeit nur mit Standardbibliothek | der Default-Pfad benötigt keine verpflichtende Drittanbieter-Runtime-Abhängigkeit |
| **restriction** | Verarbeitungseinschränkung | technische Begrenzung der Nutzung eines gespeicherten Objekts |
| **erasure** | Löschung | technisch umgesetzte Entfernung über die vorgesehenen Speicherschichten, mit Audit-/Tombstone-Regeln |
| **review queue** | Review-Warteschlange | Bereich für ausstehende oder blockierte Claims vor einer kuratierten Entscheidung |
| **curator override** | explizite Kurator-Ausnahme | attribuierte und auditierte menschliche Entscheidung; kein stiller Gate-Bypass |
| **provider independence** | Anbieterunabhängigkeit | externe Modelle sind austauschbare optionale Schnittstellen, nicht Wahrheitsautorität |

## ⚠️ Wörter mit besonderer Vorsicht

### „Verifiziert“

Nicht jeder Graphknoten ist verifizierter Kanon. „Verifiziert“ darf nur verwendet
werden, wenn Status, Evidenz, TRACE und Richtliniengrenzen dies tatsächlich
tragen.

### „GDPR-konform“

Bevorzugt:

```text
GDPR-relevante technische Kontrollen
GDPR-orientierte Architektur
```

Nicht ohne rechtliche Grundlage verwenden:

```text
GDPR-zertifiziert
vollständig rechtskonform garantiert
```

### „Sicher“ oder „gehärtet“

„Gehärtet“ bezeichnet dokumentierte technische Maßnahmen und Tests. Es ist keine
Sicherheitszertifizierung und kein Beweis, dass keine Schwachstellen existieren.

### „Wahrheit“

`TruthGate` ist kein universeller Wahrheitsdetektor. Es ist eine kontrollierte
epistemische Zulassungsgrenze innerhalb des definierten Daten- und
Richtlinienmodells.

### „Replay“

Immer unterscheiden:

```text
Receipt-Replay    = einen bestehenden Nachweis erneut prüfen
Trajectory-Replay = einen Ausführungspfad für Evaluation wiederholen
```

### „Kognitiv“, „lebendig“, „Bewusstsein“

Diese Wörter dürfen nicht zur Beschreibung aktueller Crystal-Runtime-Fähigkeiten
verwendet werden. Bio-inspirierte Modulnamen sind technische Metaphern, keine
biologischen oder personhaften Claims.

## Schreibstil für deutsche Dokumente

Bevorzugt:

- kurze, prüfbare Sätze;
- Codebezeichner unverändert in Backticks;
- klare Trennung von „implementiert“, „optional“, „geplant“ und „Forschung“;
- keine Übersetzung, die eine englische Behauptung verstärkt;
- Zahlen nur mit Link zur verbindlichen Quelle;
- „Reviewer“ oder „Prüfende“ statt unklarer Marketingadressaten.

Vermeiden:

- absolute Zuverlässigkeitsversprechen;
- Marketingformulierungen ohne Testbeleg;
- Vermischung von Titan und Crystal;
- automatische Gleichsetzung von Graphinhalt mit verifizierter Wahrheit;
- Darstellung eines offenen PRs oder RFCs als Runtime.

---

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 [日本語](../ja/GLOSSARY.md)