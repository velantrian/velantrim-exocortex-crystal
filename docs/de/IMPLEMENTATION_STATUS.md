<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: REFRESH_NEEDED -->
<!-- refresh-reason: reader-rc1-rc2-reconciliation -->
<!-- d1-locale: de -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Implementierungsstatus: Crystal und zukünftige Exo-Cortex-Arbeit

**Statusdatum:** 2026-08-08  
**Runtime-Checkpoint:** `bbd816c` / PR #337  
**Nachweise:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Maschinenlesbarer Status:** [implementation-manifest.json](../status/implementation-manifest.json)

| Komponente | Status | Aktuelle Grenze |
|---|---|---|
| Guardian / TruthGate / strikte Leseprojektion | Implementiert | Speicher und Migration können Autorität nicht umgehen |
| HTTP/CLI/MCP-Abfragen | Implementiert | gewöhnliche Abfragen verändern Canon nicht |
| SQLite Backup/Verify/inaktives Restore | Implementiert und getestet | Restore bleibt inaktiv und ist nie Zulassung |
| Begrenzter SQLite-Logikexport | Implementiert und getestet | kanonisches backend-neutrales Bundle |
| Optionale PostgreSQL-Abhängigkeit und Preflight | Implementiert und getestet | explizites Extra, lazy load, unterstützte Versionen |
| Inaktiver PostgreSQL/pgvector-Import | Implementiert und getestet | nur neues inaktives Schema; keine normalen Reads/Writes |
| Exakte Zielzustandsäquivalenz | Implementiert und getestet | unabhängiger schreibgeschützter Re-Hash |
| Aktiver PostgreSQL-Runtime-Adapter | Nicht implementiert | Ziel nicht in normaler Runtime registriert |
| Automatisches SQLite/PostgreSQL-Switching | Verboten | Verfügbarkeit und Importerfolg sind keine Auswahl |
| Exact-vs-ANN-Retrieval-Evaluation | Nicht implementiert | spätere separat geprüfte Phase |
| Cutover / Rollback / Dual-Write | Nicht implementiert | nur spätere explizite Phasen |
| PostgreSQL-Server-Lifecycle | Nicht implementiert | Backup/Restore/Upgrade/Pooling bleiben Zukunft |
| Reader Core / Semantic Reading Layer | Nicht implementiert | mögliche Schicht vor normaler Zulassung |

## Aktuelle Speichersequenz

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

Issues #331 und #332 wurden durch PR #335 und #337 umgesetzt. PostgreSQL-Unterstützung
bleibt ein optionaler Operatorpfad mit `active=false`. Erfolgreiche Äquivalenz kann
weder ein Backend aktivieren noch Guardian, TruthGate oder den strikten Canon ändern.

## Zukünftige Arbeit

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal behauptet keinen aktiven PostgreSQL-Runtime-Backend, keine automatische
Migration, kein produktives Multi-Tenancy, keine universelle Wahrheit, keine
Null-Halluzinationen, keine Rechts-/Sicherheitszertifizierung und kein Bewusstsein.
