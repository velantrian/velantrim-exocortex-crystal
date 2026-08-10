<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: REFRESH_NEEDED -->
<!-- refresh-reason: reader-rc1-rc2-reconciliation -->
<!-- d3-locale: de -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Speicher- und Autoritätsgrenzen

## Getrennte Identitäten

```text
storage profile = Deployment-Identität
physical L3 = graphischer Multi-Status-Zustand
strict Canon = vertrauenswürdige Leseprojektion
migration bundle = Nachweis der Operationsintegrität
retrieval score = Ranking-Signal
model output = generierter Text
```

Keine dieser Identitäten verleiht automatisch die Autorität einer anderen.

## Dauerhaftes Profil

SQLite ist das gewöhnliche aktive local-first Profil. Ein erstes dauerhaftes `auto` kann optional LadybugDB oder SQLite auswählen und Backend plus nicht-geheime Locator-Identität sperren. Spätere Konflikte schlagen fail-closed fehl. Mock bleibt nur expliziter Entwicklungs-/CI-Zustand.

## physical L3 und strict Canon

physical L3 kann VERIFIED, USER_CLAIMED, UNVERIFIED, HYPOTHESIS, SUBJECTIVE, contested, superseded oder restricted enthalten. strict Canon ist eine deny-dominante Projektion aus aktueller Evidenz und Policy. Speicherung, Retrieval oder hoher Score reichen nicht aus.

## Lesen und Schreiben

Öffentliche Abfragen laufen read-only über `core.query_pipeline.query()`. Explizites `ingest` ist der aufnahmefähige Schreibweg; danach erzwingen Guardian und TruthGate Struktur- und Erkenntnisgrenzen.

## SQLite-Lebenszyklus und Migration

Implementiert sind Backup, unabhängige Verifikation, inactive restore, begrenzter deterministischer logical export und Bundle-Verifikation. Die zugelassenen physical-L3-Datensätze können in ein neues inaktives PostgreSQL-Schema importiert und exakt verglichen werden; das Ziel bleibt `active=false`.

Das ist keine Vollsystemmigration von L1, Audit/Outbox, Verschlüsselungsmetadaten, Konfiguration oder unabhängigen Kopien. Es gibt keine aktive PostgreSQL-Runtime, keine ANN-Abnahme, kein automatisches Switching, cutover, fencing, rollback oder dual-write.

## Geheimnisse und Kopien

Passwörter, Tokens, private Schlüssel und credential-haltige DSNs dürfen nicht in Profile, Bundles, Receipts, Logs, GitHub oder Notion gelangen. Backups, Exporte und Migrationen erzeugen weitere Kopien; Löschung im aktiven Store löscht sie nicht automatisch. Selektive L1-Feldverschlüsselung ist keine universelle Verschlüsselung.

## Operationsbelege

| Ereignis | Belegt | Belegt nicht |
|---|---|---|
| Datensatz in L3 | physische Persistenz | strict-Canon-Mitgliedschaft |
| Retrieval-Ergebnis | Kandidatenrelevanz | ausreichende Evidenz |
| verifiziertes Backup | Backup-Integrität | Wahrheit einer Behauptung |
| erfolgreicher Import | Importintegrität | activation oder Runtime-Auswahl |
| exact equivalence | Gleichheit zugelassener Datensätze | Produktionsreife oder cutover |

Der dedizierte Reader Core ist nicht implementiert; NLnet bleibt submitted / under review / not awarded.

## Detaillierte englische Verträge

- [Vollständige Architektur](../ARCHITECTURE.md)
- [Dauerhaftes Speicherprofil](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Migrationsvertrag](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inaktiver PostgreSQL-Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
