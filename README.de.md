# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### Verifizierbare, local-first Infrastruktur für Gedächtnis, Evidenz und Entscheidungen in vertrauenswürdigen KI-Systemen

`v0.3.0` · 🧪 **2078 bestanden / 13 übersprungen / 0 fehlgeschlagen** · 🎯 **9756 Statements / 100,00 % Zeilenabdeckung** · 🧬 **7/7 deklarierte Ring-Zero-Mutanten eliminiert** · ✅ **9 permanente CI-Jobs** · 🐍 **Standard-Runtime nur mit Python-Standardbibliothek** · ⚖️ **AGPL-3.0**

> Crystal ist weder ein weiterer Chatbot noch ein autonomes „Wahrheitsorakel“. Crystal ist eine Grenze für Gedächtnis, Evidenz und Entscheidungen: Sie hält fest, was eine Behauptung ist, woher sie stammt, in welchem epistemischen Zustand sie sich befindet, ob sie eine Antwort begründen darf und wie ein Widerspruch durch eine ausdrückliche, auditierbare Entscheidung behandelt wurde.

**Verifizierter Runtime-Checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — gemergter PR #337.  
**Validierter Head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 erfolgreich.  
**PostgreSQL-Integration:** `31256316532` — erfolgreich mit PostgreSQL 16 und pgvector 0.8.2.  
**Primäre Nachweise:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md) und das [maschinenlesbare Manifest](./docs/status/implementation-manifest.json).

> **Übersetzungsvertrag:** Diese Datei ist als vollständige visuelle und semantische deutsche Projektpräsentation angelegt, nicht als Kurzfassung. Englisch bleibt die primäre Arbeits- und Konfliktquelle. Weitere Dokumente werden schrittweise übersetzt; siehe [Lokalisierungsrichtlinie](./docs/LOCALIZATION_POLICY.md) und [Übersetzungsstatus](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Warum Crystal existiert

Viele KI-Systeme mischen Quelldokumente, Aussagen von Nutzern, Modellausgaben, Hypothesen, Retrieval-Fragmente und dauerhaftes Gedächtnis in einem Kontext oder Vektorspeicher. Ohne klare Grenzen kann sprachlich überzeugender Text Autorität erhalten, die seine Evidenz nicht trägt.

```text
Eine flüssige Behauptung ist nicht automatisch vertrauenswürdig.
Ein physischer Graphknoten ist nicht automatisch strikter Canon.
Ein Retrieval-Score ist keine Evidenz.
Eine Modellausgabe ist keine unabhängige Faktenquelle.
Ein Widerspruch bestimmt nicht selbst seinen Gewinner.
Ein Themenlabel ist kein Wahrheitsurteil.
Ein erfolgreicher Datenimport ist keine Backend-Aktivierung.
```

## 🧠 Was Crystal bereitstellt

- typisierte Behauptungen und einen expliziten epistemischen Lebenszyklus;
- Quellenidentität, exakte Evidenzspannen und Provenance;
- Guardian- und TruthGate-Zulassungsgrenzen;
- einen physischen Multi-Status-L3-Graphen, getrennt vom strikten Canon;
- unveränderliche, deny-dominante `TrustSnapshot`-Abstimmung;
- read-only HTTP-, CLI- und MCP-Abfrageflächen;
- TRACE und reproduzierbare, manipulationssichtbare Receipts;
- Einschränkung, Löschung, Audit und Import-Sessions;
- Review-Warteschlangen und fortsetzbare Review-Sessions;
- unveränderliche `ContradictionReport`-Objekte;
- explizite Entscheidungen `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`;
- scoped Curator-Rollen und prozesslokale Decision-Leases;
- beratende TopicFacet-Metadaten ohne Wahrheitsautorität;
- deterministische Evaluation, 100 % Coverage und Ring-Zero-Mutation-Gate;
- verifiziertes SQLite Backup/Restore und bounded logical migration;
- optionalen inaktiven PostgreSQL/pgvector-Import mit unabhängiger exakter Zustandsäquivalenz.

## 🏛️ Architektur in drei Ansichten

### 🧠 Mindmap

```text
🧠 Crystal
├── 🎯 Zweck
│   ├── verifizierbares KI-Gedächtnis
│   ├── local-first Vertrauensinfrastruktur
│   └── evidenzgebundene Antworten und Entscheidungen
├── 🏛️ Gedächtnis
│   ├── L0 — schneller Arbeitscache
│   ├── L1 — operativer Zustand und Lifecycle
│   ├── L2 — Review-/Wartegrenze
│   └── L3 — physischer Multi-Status-Graph
├── 🛡️ Vertrauen
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Evidenz
│   ├── Quelle + Evidenzspanne
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
├── ⚖️ Widerspruch
│   ├── Review-Queue
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ Speicherung
│   ├── SQLite — normaler local-first Pfad
│   └── PostgreSQL/pgvector — inaktives Migrationsziel
└── 📊 Verifikation
    ├── Python 3.11 / 3.12
    ├── 100 % Coverage
    ├── Mutation / Security / Docker
    └── exakte CI-Evidenz
```

### 🏗️ Informationsfluss

```text
📥 expliziter Ingest
        ↓
🧾 Claim-Typ + Quelle + exakte Evidenzspanne
        ↓
🧠 beobachteter Zustand in L0/L1
        ↓
🛡️ Guardian → ⚖️ TruthGate → 🚧 Restrictions
        ↓                         ↓
⏳ L2 Review                🏛️ physischer L3-Graph
        └──────────────┬──────────┘
                       ↓
             📐 immutable TrustSnapshot
                       ↓
          🛡️ Guardian + CanonicalView STRICT
                  ↓                 ↓
          💬 begründete Antwort   🚫 begründete Ablehnung
                  ↓
             🧾 replaybares Receipt
```

### 🌳 Modulbaum

```text
🌳 Crystal
├── 🧠 Memory: L0 / L1 / L2 / L3
├── 🛡️ Trust: Guardian / TruthGate / TrustSnapshot / CanonicalView
├── 📜 Evidence: Source / Span / Provenance / TRACE / Receipt
├── ⚖️ Review: Queue / Session / ContradictionReport / Disposition
├── 🔎 Query: HTTP / CLI / MCP
├── 🗄️ Portability: SQLite lifecycle / logical bundle / PostgreSQL inactive import
└── 📊 Verification: tests / coverage / mutation / security / Docker / docs-status
```

## 🧭 Zentrale Unterscheidungen

```text
physischer L3-Graph   != strikter Canon
query                 != ingest
confidence            != unabhängige Evidenz
LLM-Ausgabe           != unabhängige Faktenquelle
Widerspruchserkennung != automatischer Gewinner
TopicFacet-Relevanz   != Wahrheit
Migrations-Receipt    != Claim-Evidenz
erfolgreicher Import  != Backend-Aktivierung
prozesslokales Lease  != verteilte Koordination
```

TruthGate ist ein Policy-Gate für Zulassung, kein Orakel. Strikter Canon ist eine durch Policy erlaubte Leseprojektion über Evidenz, Status, ESM-Zustand, Confidence-Form und Verarbeitungsbeschränkungen.

## 🧱 Gedächtnis- und Evidenzflächen

| Fläche | Aufgabe | Kritische Grenze |
|---|---|---|
| L0 | In-Process-Arbeitscache | schnell und rekonstruierbar |
| L1 | SQLite/WAL-Betriebszustand | Lifecycle, Restrictions, Pending Work |
| L2 | logische Review-Grenze | nicht automatisch Canon |
| L3 | physisches Multi-Status-Gedächtnis | Existenz bedeutet nicht Vertrauen |
| TrustSnapshot | unveränderliche Abstimmung | deny-dominante L1/L3-Auflösung |
| CanonicalView | strikte Grounding-Projektion | nur Policy-erlaubtes Lesen |
| TRACE / Receipt | Nachweis und Replay | Grounding, Drift, Manipulationsnachweis |
| ContradictionReport | unveränderlicher Konflikt | Confidence entscheidet nicht |
| TopicFacet | Navigation | ändert Wahrheit und Canon nicht |

## 🗄️ SQLite und PostgreSQL/pgvector

```text
SQLite
└── normaler local-first Runtime-Pfad
    ├── Reads/Writes
    ├── Backup/Restore
    ├── Lock Recovery
    └── bounded canonical logical export

PostgreSQL 16 + pgvector
└── optionales Migrations-/Äquivalenzprofil
    ├── optionales Extra [postgresql]
    ├── lazy driver loading
    ├── neues Zielschema
    ├── active=false
    ├── SERIALIZABLE import
    └── unabhängige Count/Byte/SHA-256-Äquivalenz
```

Das PostgreSQL-Ziel ist nicht Teil der normalen Runtime-Komposition und kann keine gewöhnlichen Reads oder Writes bedienen. Importerfolg bedeutet weder Aktivierung noch automatische Auswahl, Cutover, Rollback, Dual-Write, TruthGate-Zulassung, Canon-Mitgliedschaft, ANN-Akzeptanz oder Production-Multi-Tenancy.

## 🔎 Crystal im Vergleich zu klassischem RAG

| Frage | Klassisches RAG | Crystal |
|---|---|---|
| Relevantes Material finden | Kernstärke | über Retrieval-Adapter |
| Nutzerbehauptung von verifiziertem Fakt trennen | anwendungsspezifisch | explizite typisierte Grenze |
| Lifecycle und Widersprüche verfolgen | meist externe Logik | First-Class-Zustände und Reports |
| Generierten Text als eigene Quelle verhindern | nicht inhärent | Ring-Zero-Invariante |
| Evidenz einer Antwort reproduzieren | optional | TRACE und Receipt |
| Widersprüche verantwortlich entscheiden | anwendungsspezifisch | autorisierte Dispositionen |
| Ohne Cloud-/Modellanbieter laufen | unterschiedlich | pure-stdlib local-first Basis |

## 🛡️ Öffentliche read-only Grenze

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` und `MCP search` verwenden dieselbe `core.query_pipeline`. Sie erzeugen keine Fakten, ändern keinen ESM-Zustand, schreiben nicht nach L3 und mutieren keinen Canon.

## ⚖️ Explizite Widerspruchsentscheidung

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "die Aussagen beschreiben unterschiedliche Kontexte" \
  --expected-report-id REPORT_ID
```

`CuratorLeaseRegistry` schützt nur innerhalb eines Prozesses. Verteilte Deployments benötigen einen externen Lease-Adapter.

## 🚀 Schnellstart

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optionales inaktives PostgreSQL-Migrationstooling: `pip install -e '.[postgresql]'`.

## 📚 Navigation

- [Deutscher Dokumentationsindex](./docs/de/README.md)
- [Englische Dokumentationskarte](./docs/DOCUMENTATION_MAP.md)
- [Testbericht](./TEST_REPORT.md)
- [Status](./docs/STATUS.md)
- [Implementierungsstatus](./docs/IMPLEMENTATION_STATUS.md)
- [Architektur](./docs/ARCHITECTURE.md)
- [Security](./SECURITY.md)
- [NLnet-Scope](./docs/GRANT_NLNET_SCOPE.md)
- [Lokalisierungsrichtlinie](./docs/LOCALIZATION_POLICY.md)
- [Übersetzungsstatus](./docs/TRANSLATION_STATUS.md)

## ✅ Verifizierte Basis

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
Mutation: 7/7
CI: 9/9
PostgreSQL integration: PostgreSQL 16 + pgvector 0.8.2 erfolgreich
```

## 🚧 Grenzen der Aussage

Crystal behauptet keine universelle Wahrheitserkennung, Null-Halluzinationen, rechtliche GDPR-/Security-Zertifizierung, production-ready Multi-Tenancy, verteiltes Locking, AGI oder Bewusstsein, einen aktiven PostgreSQL-Runtimepfad, automatisches Switching, Cutover/Rollback oder einen fertigen dedizierten Reader Core. Der NLnet-Antrag ist **submitted / under review / not awarded**.

## 🤝 Mitwirken und Lizenz

Siehe [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md), [GOVERNANCE.md](./GOVERNANCE.md) und [AGPL-3.0](./LICENSE).
