<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: de -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Sicherheits-, Datenschutz- und Fehlergrenzen

**Quelle:** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

Diese Übersicht ersetzt weder Tests noch Security Review oder Rechtsberatung.

## Epistemische Sicherheit

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

Guardian und TruthGate bleiben Zulassungsgrenzen. Öffentliche Queries sind read-only,
explizites Ingest ist der getrennte Schreibpfad. Crystal garantiert weder Wahrheit noch
Null-Halluzinationen; nicht gestützte Inhalte sollen blockiert, markiert, abgelehnt oder
auditierbar werden.

## Lokale Vertrauensgrenze

Die Standardinstallation hat keine Pflichtabhängigkeit von Cloud, LLM, Telemetrie oder
Analytics. SQLite ist das gewöhnliche aktive Profil. Dauerhaftes `auto` kann optional
LadybugDB oder SQLite wählen und sperrt den Gewinner; Mock bleibt expliziter Dev/Test-Zustand.
PostgreSQL/pgvector ist nur ein inaktives Operator-Target mit `active=false`.

## Daten und optionale Erweiterung

Gespeichert werden können Claims, Metadaten, Provenienz, epistemischer Zustand, Graphen,
Restrictions, Erasure-/Audit-Daten, Receipts, Outbox, Migration Bundles, Backups und Exporte.
Daten verlassen die lokale Grenze nur durch explizite Aktivierung von Anthropic, Remote
Neo4j, Wikidata, Redis, PostgreSQL-Migration, breiter HTTP-API oder kopierten Dateien.

## Encryption und Secrets

`VELANTRIM_ENCRYPTION_KEY` schützt ausgewählte L1-Felder, nicht automatisch alle L3,
Backups, Exporte, Receipts, Logs oder temporären Files. Host-Verschlüsselung und Key
Management bleiben erforderlich. Credentials dürfen nie in Profiles, Bundles, Receipts,
Logs, Issues oder Notion gespeichert werden.

## API, Privacy und Erasure

Der dokumentierte API-Baseline nutzt Authentication und Loopback. Externe Exposition braucht
TLS, geprüfte Authentifizierung, Least Privilege, Limits, Monitoring und Incident Handling.
Access, Rectification, Restriction, Erasure und Processing Record sind Engineering Controls,
keine DSGVO-Zertifizierung. Aktive Löschung ist keine globale Löschung unabhängiger Kopien.

## Sichere Fehlerreaktionen

| Klasse | Erwartetes Verhalten |
|---|---|
| Unsupported Claim | Block, Label oder bounded refusal |
| Read-only Mutation | Reject / kein State Change |
| Profile Conflict | Fehler vor Backend Cache |
| Dependency fehlt | expliziter Fehler, kein verstecktes Mock |
| Import scheitert | Rollback, `active=false` |
| Evidence mismatch | Verification failure |
| Receipt/Audit tampering | Digest-/Hash-Fehler |
| Oversized migration | Fail closed an Limits |
| Network exposure | nur explizit und authentifiziert |
| Erasure copy survives | separates Inventory und Deletion |

## Non-Claims

Crystal ist keine Security-/Legal-/DSGVO-Zertifizierung, kein Arbitrary-Scale-Beweis,
kein aktives PostgreSQL-Runtime, keine Automatic-Migration-Garantie, keine perfekte Wahrheit,
kein AGI/Bewusstsein und kein Nachweis eines bewilligten NLnet-Grants.

Details: [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md),
[Failure Modes](../FAILURE_MODES.md) und [englische Übersicht](../SAFETY_PRIVACY_AND_FAILURES.md).
