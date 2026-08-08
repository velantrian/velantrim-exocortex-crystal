<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: it -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Stato dell’implementazione: Crystal e lavoro futuro

**Data:** 2026-08-08  
**Checkpoint:** `bbd816c` / PR #337  
**Evidenza:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Stato machine-readable:** [manifest](../status/implementation-manifest.json)

| Componente | Stato | Confine attuale |
|---|---|---|
| Guardian / TruthGate / proiezione rigorosa | Implementato | storage e migrazione non aggirano l’autorità |
| Query HTTP/CLI/MCP | Implementato | le query ordinarie non mutano Canon |
| Backup/verify/restore inattivo SQLite | Implementato e testato | restore inattivo, mai ammissione |
| Export logico SQLite limitato | Implementato e testato | bundle canonico backend-neutral |
| Dipendenza e preflight PostgreSQL | Implementato e testato | extra esplicito, lazy load |
| Import PostgreSQL/pgvector inattivo | Implementato e testato | nuovo schema inattivo, nessun I/O ordinario |
| Equivalenza esatta target | Implementato e testato | re-hash indipendente read-only |
| Adapter runtime PostgreSQL attivo | Non implementato | target fuori dalla composizione normale |
| Switching SQLite/PostgreSQL automatico | Vietato | disponibilità/import non selezionano |
| Valutazione exact-vs-ANN | Non implementata | fase successiva separata |
| Cutover / rollback / dual-write | Non implementato | fasi esplicite successive |
| Ciclo server PostgreSQL | Non implementato | backup/restore/upgrade/pooling futuri |
| Reader Core / Semantic Reading Layer | Non implementato | livello candidato prima dell’ammissione |

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

Le issue #331 e #332 sono state implementate dalle PR #335 e #337. PostgreSQL rimane un
percorso operatore opzionale con `active=false`. L’equivalenza riuscita non attiva un
backend e non modifica Guardian, TruthGate o Canon rigoroso.

Lavoro futuro:

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal non dichiara backend PostgreSQL attivo, migrazione automatica, multi-tenancy
produttivo, verità universale, zero allucinazioni, certificazione legale/sicurezza o
coscienza.
