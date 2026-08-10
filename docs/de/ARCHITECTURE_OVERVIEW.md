<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: REFRESH_NEEDED -->
<!-- refresh-reason: reader-rc1-rc2-reconciliation -->
<!-- d3-locale: de -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — Architekturüberblick

Diese Übersetzung ist eine Orientierungsschicht. Bei Konflikten gelten gemergter Code, ausführbare Tests, exaktes CI und die englischen Verträge.

## Kernmodell

```text
Quellen + explizites ingest
→ Provenienz + Normalisierung
→ Guardian-Prüfungen
→ TruthGate-Entscheidung
→ operativer L1-Zustand + mehrstatusfähiges physical L3
→ deny-dominante strict-Canon-Leseprojektion
→ read-only Retrieval / Antwort / begrenzte Ablehnung
```

Ein Eintrag in physical L3 ist nicht automatisch strict Canon. Retrieval-Rang, Vektorähnlichkeit und Modelltext sind keine unabhängigen Belege.

## Speicher- und Review-Schichten

- **L0:** flüchtiger Prozesskontext.
- **L1:** SQLite/WAL für operativen Zustand, Belege, Audit, Receipts, Import-/Review-Sitzungen und Outbox.
- **L2:** Pending-/Review-Staging für Kandidaten oder Quarantäne; keine endgültige Wahrheitsstufe.
- **L3:** graphorientierter Multi-Status-Speicher; nicht identisch mit strict Canon.
- **TrustSnapshot / CanonicalView:** deny-dominante vertrauenswürdige Leseoberfläche.

## Read/write-Trennung

`HTTP /ask`, `CLI ask` und MCP laufen read-only über `core.query_pipeline.query()`. Eine Abfrage darf keine Fakten, ESM, L3, Outbox, Episode-Links oder Embedder-Identität verändern. Nur explizites `ingest` kann über Guardian und TruthGate in den schreibfähigen Aufnahmeweg gelangen.

## Speicherprofile und Portabilität

SQLite ist das gewöhnliche aktive local-first Profil. Beim ersten dauerhaften `auto` darf optional LadybugDB oder sonst SQLite gewählt und anschließend gesperrt werden. Ein stiller Fallback auf flüchtiges Mock ist verboten.

Der verifizierte PostgreSQL/pgvector-Pfad endet bei einem inaktiven Ziel:

```text
verifiziertes SQLite-Bundle
→ transaktionaler PostgreSQL-Import
→ unabhängiger read-only Re-Hash
→ exakte Äquivalenz
→ active=false
```

Import oder Äquivalenz sind weder activation noch Backend-Auswahl, TruthGate-Aufnahme, cutover, rollback oder dual-write. PostgreSQL gehört nicht zur normalen Runtime-Komposition.

## Dokumentverarbeitung

Source spans, Dokumentdatensätze, Import-Sitzungen und dry-run/review-Flows sind implementierter Baseline. Ein dedizierter mehrstufiger Reader Core mit Coverage-Karten, widerspruchsbewusstem Wiederlesen und Dokumentsynthese ist nicht implementiert.

## Nicht-Behauptungen

Crystal behauptet keine AGI, kein Bewusstsein, keine Null-Halluzinationen, keine aktive PostgreSQL-Runtime, kein automatisches Switching, keine akzeptierte ANN-Produktion, kein cutover/rollback/dual-write, keine Sicherheits-/Rechts-/GDPR-Zertifizierung und keine bewilligte NLnet-Förderung.

## Englische Quellen

- [Vollständige Architektur](../ARCHITECTURE.md)
- [Speicher- und Autoritätsgrenzen](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementierungsstatus](../IMPLEMENTATION_STATUS.md)
- [Inaktiver PostgreSQL-Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
