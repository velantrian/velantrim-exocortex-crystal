<!-- translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: de -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — aktueller Status

**Statusdatum:** 2026-08-08  
**Verifizierter Runtime-Checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Verifizierter Tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Validierter Implementierungs-Head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime-PR / CI:** #337 / `31256316536`  
**PostgreSQL-Integrations-CI:** `31256316532`

## Verifikation

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** deklarierte Ring-Zero-Mutanten beendet;
- **9/9** permanente CI-Jobs erfolgreich;
- **1/1** reale PostgreSQL/pgvector-Integration erfolgreich.

Exakte Nachweise: [TEST_REPORT.md](../../TEST_REPORT.md) und das
[maschinenlesbare Manifest](../status/implementation-manifest.json).

## Aktuelle verifizierte Fähigkeitsgrenze

Crystal behält die Local-first-SQLite-Basis und implementiert Phase 1 von Issue #332:

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

Der PostgreSQL-Treiber ist ein optionales Extra und wird nur durch explizite
Operatorbefehle lazy geladen. Die Standardinstallation bleibt reine Standardbibliothek.
Das importierte Ziel wird nicht in die gewöhnliche Runtime-Komposition aufgenommen,
bleibt `active=false` und kann keine normalen Lese- oder Schreibvorgänge bedienen.

## Autoritätsgrenze

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian, TruthGate, Restrictions, TrustSnapshot und CanonicalView bleiben unverändert.

## Noch nicht vorhanden

- aktive PostgreSQL-Lese-/Schreibauswahl;
- Exact-vs-ANN-Evaluation und akzeptierte ANN-Schwellen;
- Aktivierung, Cutover, Source/Target-Fencing, Rollback oder Dual-Write;
- PostgreSQL-Backup/Restore/Upgrade-Lifecycle, produktives Pooling und verteiltes Fencing;
- produktives IdP/Multi-Tenancy oder rechtliche, Sicherheits- bzw. DSGVO-Zertifizierung;
- dedizierter verifizierter Reader Core.

## Förderstatus

Das Projekt ist eingereicht und wird geprüft. **Es wird weder eine Bewilligung noch
eine Budgetänderung behauptet.** PR #337 und Issue #332 sind bereits gemergte Basis
und dürfen nicht erneut als zukünftiger Förderumfang gezählt werden.
