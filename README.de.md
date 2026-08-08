# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Nachweisbare, lokale Speicherinfrastruktur für vertrauenswürdige KI-Systeme

`v0.3.0` · 🧪 **1853 bestanden / 12 übersprungen** · 🎯 **100 % Testabdeckung** · 🧬 **7/7 deklarierte Mutanten erkannt** · ✅ **9 CI-Jobs** · 🐍 **Standardlaufzeit nur mit der Python-Standardbibliothek** · ⚖️ **AGPL-3.0**

> Crystal ist kein weiterer Chatbot. Es ist eine Grenze für Speicher, Nachweise
> und Entscheidungen. Sie hält fest, was eine Aussage ist, woher sie stammt,
> welchen epistemischen Zustand sie besitzt, ob sie eine Antwort begründen darf
> und wie ein Widerspruch ausdrücklich entschieden wurde.

**Verifizierter Laufzeit-Checkpoint:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — gemergter PR #302.  
**Implementierungswahrheit:** Code und Tests auf GitHub `main`.  
**Exakte Nachweise:** [TEST_REPORT.md](./TEST_REPORT.md) und das
[maschinenlesbare Implementierungsmanifest](./docs/status/implementation-manifest.json).

> **Übersetzungsvertrag:** Diese Fassung bewahrt dieselben Funktions-, Sicherheits-
> und Statusgrenzen wie das englische README. Stabile API-Namen bleiben in ihrer
> Codeform; die Erklärungen sind idiomatisch auf Deutsch formuliert.

---

## 🎯 Warum Crystal existiert

Viele KI-Systeme vermischen Quelldokumente, Nutzerangaben, Modellausgaben,
Hypothesen, abgerufene Fragmente und dauerhaften Speicher in einem Kontext oder
Vektorspeicher. Dadurch kann flüssig formulierter Text unbemerkt Autorität
erhalten, die seine Belege nicht tragen.

```text
Eine überzeugende Aussage ist nicht automatisch vertrauenswürdig.
Ein Graphknoten ist nicht automatisch strenger Canon.
Ein Retrieval-Score ist kein Beleg.
Eine Modellausgabe ist keine unabhängige Quelle.
Ein Widerspruch bestimmt seinen Gewinner nicht selbst.
Ein Themenlabel ist kein Wahrheitsurteil.
```

## 🧠 Was Crystal bereitstellt

- typisierte Aussagen und einen ausdrücklichen epistemischen Lebenszyklus;
- Quellen-, Evidenzspannen- und Provenienzmetadaten;
- Zulassungsgrenzen durch Guardian und TruthGate;
- einen physischen L3-Graphen mit mehreren Zuständen, getrennt vom strengen Canon;
- unveränderliche, deny-dominante `TrustSnapshot`-Abstimmung beim Lesen;
- öffentliche, ausschließlich lesende HTTP-, CLI- und MCP-Abfragen;
- TRACE sowie reproduzierbare und manipulationssichtbare Receipts;
- Einschränkungs-, Lösch-, Audit- und Importsitzungsfunktionen;
- Review-Warteschlangen und fortsetzbare Review-Sitzungen;
- typisierte, unveränderliche Widerspruchsberichte;
- ausdrückliche Entscheidungen `COEXIST`, `CONTEXTUALIZE` und `SUPERSEDE`;
- CLI- und authentifizierte HTTP-Oberflächen zur Konfliktentscheidung;
- bereichsgebundene Kuratorenrollen und lokale Entscheidungs-Leases;
- beratende, mehrwertige Themenfacetten ohne Autoritätswirkung;
- eine aus den Laufzeitübergängen erzeugte maschinenlesbare ESM-Spezifikation;
- deterministische Evaluation, 100 % Zeilenabdeckung und Ring-Zero-Mutation-Gate;
- geplante/manuelle L3-Benchmark-Historie mit versionierten Artefakten.

## 🏛️ Architektur im Überblick

Die drei folgenden Karten zeigen dasselbe System aus ergänzenden Blickwinkeln:
**Zweck**, **Informationsfluss** und **Modulbeziehungen**.

### 🧠 Mindmap — Zweck und Fähigkeitsgrenzen

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 Zweck
│   ├── Nachweisbarer Speicher für KI
│   ├── Lokale Vertrauensinfrastruktur
│   └── Evidenzgestützte Antworten und Entscheidungen
│
├── 🏛️ Speichermodell
│   ├── L0 — prozessinterner Arbeitscache
│   ├── L1 — operativer Lebenszyklusspeicher
│   ├── L2 — Grenze für Pending und Review
│   └── L3 — graphbasierter Mehrzustandsspeicher
│
├── 🛡️ Vertrauensgrenze
│   ├── Guardian — Struktur- und Richtlinienprüfungen
│   ├── TruthGate — Zulassungsgrenze
│   ├── TrustSnapshot — unveränderliche Leseabstimmung
│   └── CanonicalView — strenge Vertrauensprojektion
│
├── 📜 Evidenz und Auditierbarkeit
│   ├── Provenienz und Evidenzspannen
│   ├── TRACE — Herkunft der Begründung
│   └── Receipt — Replay- und Manipulationsnachweis
│
├── ⚖️ Review und Widersprüche
│   ├── Review-Warteschlangen und fortsetzbare Sitzungen
│   ├── unveränderlicher ContradictionReport
│   ├── COEXIST
│   ├── CONTEXTUALIZE
│   └── SUPERSEDE
│
├── 🏷️ Beratende Navigation
│   └── TopicFacet — mehrwertige, nicht autoritative Metadaten
│
├── 🔐 Governance und Koordination
│   ├── bereichsgebundene Kuratorenrollen und Fähigkeiten
│   ├── Bindung an den authentifizierten Actor
│   └── prozesslokale Decision Leases
│
└── 📊 Verifikation
    ├── deterministische Tests und Evaluation
    ├── 100 % Zeilenabdeckung
    ├── Ring-Zero-Mutation-Gate
    └── versionierte Benchmark-Historie
```

### 🏗️ ASCII-Architektur — wie Informationen fließen

```text
┌─────────────────────────────────────────────────────────────────────┐
│              🔱 Velantrim ExoCortex — Crystal                      │
│      Lokale, nachweisbare Speicherinfrastruktur für KI             │
└─────────────────────────────────────────────────────────────────────┘

                        📥 Ausdrückliche Aufnahme
                                  │
                                  ▼
                🧾 Aussagentyp + Quelle + Evidenzspanne
                                  │
                                  ▼
                       🧠 L0 / L1 Observed-Zustand
                                  │
                                  ▼
          🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 Einschränkungen
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ⏳ L2 Pending / Review       🏛️ Physischer L3-Graph
                    │                           │
                    │                           ▼
                    │                 📜 Provenienz / TRACE
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                      📐 Unveränderlicher TrustSnapshot
                                  │
                                  ▼
                 🛡️ Guardian + CanonicalView STRICT
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
            💬 Begründete Antwort       🚫 Begrenzte Ablehnung
                    │
                    ▼
             🧾 Reproduzierbares Receipt

⚖️ Ungelöster Widerspruch
        │
        ▼
📋 Unveränderlicher ContradictionReport
        │
        ▼
🔐 bereichsgebundener Principal + Fähigkeit + Decision Lease
        │
        ▼
🧑‍⚖️ ausdrückliches COEXIST / CONTEXTUALIZE / SUPERSEDE
        │
        ▼
📜 auditierbarer kanonischer Schreibpfad

🏷️ TopicFacet-Metadaten ──► Navigation / Filtern / Gruppieren
                           └─► niemals Autorität über Wahrheit, ESM, Evidenz oder Canon
```

### 🌳 Beziehungsbaum — wie die Module verbunden sind

```text
🌳 Crystal-Systembeziehungen
│
├── 🧠 Speicherschicht
│   ├── L0 ──► schneller, rekonstruierbarer Arbeitscache
│   ├── L1 ──► Lebenszyklus, Einschränkungen und offene Arbeit
│   ├── L2 ──► logische Review-Grenze
│   └── L3 ──► graphbasierte Mehrzustandsspeicherung
│
├── 🛡️ Vertrauensschicht
│   ├── Guardian ──► Struktur- und Richtlinienvalidierung
│   ├── TruthGate ──► Zulassungsentscheidung
│   ├── TrustSnapshot ──► deny-dominante L1/L3-Abstimmung
│   └── CanonicalView ──► strenge Begründungsprojektion
│
├── 📜 Evidenzschicht
│   ├── Quellenmetadaten
│   ├── Evidenzspannen
│   ├── Provenienz
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Review-Schicht
│   ├── Review-Warteschlange
│   ├── fortsetzbare Review-Sitzung
│   ├── ContradictionReport
│   └── ausdrückliche Disposition
│       ├── COEXIST
│       ├── CONTEXTUALIZE
│       └── SUPERSEDE
│
├── 🔐 Autorisierungsschicht
│   ├── CuratorPrincipal
│   ├── Rolle und bereichsgebundene Fähigkeit
│   ├── Übereinstimmung mit authentifiziertem Actor
│   └── prozesslokales Decision Lease
│
├── 🏷️ Beratende Schicht
│   └── TopicFacet
│       ├── mehrwertig
│       ├── Score nur für Relevanz
│       └── keine Autorität über Wahrheit oder Zulassung
│
├── 🔎 Öffentliche Abfrageschicht
│   ├── HTTP /ask und /receipt
│   ├── CLI ask und receipt
│   └── MCP search
│       └── gemeinsame Read-only-Abfragepipeline
│
└── 📊 Verifikationsschicht
    ├── Tests unter Python 3.11 / 3.12
    ├── Coverage-Gate
    ├── Ring-Zero-Mutation-Gate
    ├── Sicherheits- und Containerprüfungen
    └── Benchmark-Historie
```

### Zentrale Unterscheidungen

```text
Physischer L3-Graph ≠ strenger Canon
Abfrage ≠ Aufnahme
Konfidenz ≠ unabhängiger Beleg
LLM-Ausgabe ≠ unabhängige Faktenquelle
Widerspruch ≠ automatischer Gewinner
Themenrelevanz ≠ Wahrheit oder Belegqualität
lokales Lease ≠ Garantie verteilter Koordination
```

TruthGate ist eine Richtliniengrenze für die Zulassung, kein Orakel für objektive
Wahrheit. Der strenge Canon ist eine richtlinienkonforme Leseprojektion über
Evidenz, Status, ESM-Zustand, Konfidenzform und Verarbeitungseinschränkungen.

## 🧱 Speicher- und Evidenzoberflächen

| Oberfläche | Aufgabe | Grenze |
|---|---|---|
| L0 | prozessinterner Arbeitscache | schnell und rekonstruierbar |
| L1 | operativer SQLite/WAL-Speicher | Lebenszyklus, Einschränkungen, offene Arbeit |
| L2 | logische Review-Grenze | nicht automatisch strenger Canon |
| L3 | graphbasierter Mehrzustandsspeicher | Zulassung nur über Richtliniengrenzen |
| TrustSnapshot | unveränderliche Leseabstimmung | deny-dominante L1/L3-Auflösung |
| CanonicalView | strenge Begründungsprojektion | Graphmitgliedschaft bedeutet kein Vertrauen |
| TRACE / Receipt | Nachweis- und Replay-Schicht | Begründung, Drift und Manipulationsspuren |
| ContradictionReport | unveränderliches Konfliktobjekt | kein Gewinner allein durch Konfidenz |
| TopicFacet | Navigationsmetadaten | verändert weder Wahrheit, ESM noch Canon |
| CuratorPrincipal / Lease | Autorisierung und Koordination | bei Skalierung externe Identität und Lease nötig |

## 🛡️ Öffentliche Read-only-Abfragegrenze

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` und `MCP search` verwenden
`core.query_pipeline`. Sie erzeugen keine Fakten, ändern keinen ESM-Zustand,
schreiben nicht nach L3, bedienen keine Outbox, speichern keine Episoden und
initialisieren keinen Embedding-Fingerprint.

Siehe [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Ausdrückliche Widerspruchsentscheidungen

Eine normale Freigabe bleibt bei ungelösten Widersprüchen fail-closed. Ein
Kurator muss eine Disposition, einen Actor und eine Begründung angeben.

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "die Aussagen beschreiben unterschiedliche Kontexte" \
  --expected-report-id REPORT_ID
```

Für FastAPI wird `POST /review/resolve-conflict` mit der Authentifizierungs-
Dependency der Hostanwendung registriert. `core.curator_auth` prüft Rollen,
Faktenbereiche und Actor-Bindung. `CuratorLeaseRegistry` verhindert parallele
Entscheidungen nur innerhalb eines Prozesses; verteilte Installationen benötigen
einen externen Lease-Adapter.

Siehe [Konfliktoberflächen](./docs/CONFLICT_RESOLUTION_SURFACES.md) und
[Themenfacetten und Curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md).

## 🏷️ Beratende Themenfacetten

`core.topic_facets` ergänzt normalisierte Mehrfachlabels zur Navigation,
Filterung und Gruppierung. Der Facet-Score bedeutet ausschließlich thematische
Relevanz und verändert weder Wahrheitsstatus, Evidenz, ESM, Konfliktentscheidung
noch Zugehörigkeit zum strengen Canon.

## 🚀 Schnellstart

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Weiter mit [QUICKSTART.md](./docs/QUICKSTART.md).

## 📚 Dokumentationspfad

- [Dokumentationskarte](./docs/DOCUMENTATION_MAP.md)
- [Aktueller Status](./docs/STATUS.md)
- [Implementierungsstatus](./docs/IMPLEMENTATION_STATUS.md)
- [Architektur](./docs/ARCHITECTURE.md)
- [Read-only-Abfragegrenze](./docs/architecture/read-only-query-boundary.md)
- [Konfliktentscheidungsoberflächen](./docs/CONFLICT_RESOLUTION_SURFACES.md)
- [Themenfacetten und Curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md)
- [Testbericht](./TEST_REPORT.md)
- [Evaluation](./docs/EVAL.md)
- [Fehlermodi](./docs/FAILURE_MODES.md)
- [NLnet-Grantumfang](./docs/GRANT_NLNET_SCOPE.md)

## ✅ Verifizierte Basis

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 Grenze der Aussagen

Crystal behauptet weder universelle Wahrheitserkennung noch Halluzinationsfreiheit,
rechtliche GDPR- oder Sicherheitszertifizierung, Produktionsreife für
Multi-Tenant-Betrieb, künstliches Bewusstsein oder Titan/Full-ExoCortex-
Funktionalität. Die aktuellen Kuratoren-Leases gelten nur pro Prozess;
verteilte Koordination, externe Identity-Provider-Integration, breitere
Provenienzverdrahtung und Titan-Integration bleiben eigenständige Vorhaben.

## 🤝 Mitwirkung und Lizenz

Siehe [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) und [AGPL-3.0](./LICENSE).
