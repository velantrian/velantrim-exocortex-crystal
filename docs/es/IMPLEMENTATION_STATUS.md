<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: es -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Estado de implementación: Crystal y trabajo futuro

**Fecha:** 2026-08-08  
**Checkpoint:** `bbd816c` / PR #337  
**Evidencia:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Estado legible por máquina:** [manifest](../status/implementation-manifest.json)

| Componente | Estado | Frontera actual |
|---|---|---|
| Guardian / TruthGate / proyección estricta | Implementado | almacenamiento y migración no eluden autoridad |
| Consultas HTTP/CLI/MCP | Implementado | las consultas ordinarias no mutan Canon |
| Backup/verify/restore inactivo de SQLite | Implementado y probado | restore inactivo, nunca admisión |
| Exportación lógica SQLite acotada | Implementado y probado | bundle canónico neutral al backend |
| Dependencia y preflight PostgreSQL | Implementado y probado | extra explícito, carga diferida |
| Importación PostgreSQL/pgvector inactiva | Implementado y probado | esquema nuevo inactivo, sin I/O ordinario |
| Equivalencia exacta del destino | Implementado y probado | re-hash independiente de solo lectura |
| Adaptador PostgreSQL activo | No implementado | destino fuera de la composición normal |
| Switching SQLite/PostgreSQL automático | Prohibido | disponibilidad/importación no seleccionan |
| Evaluación exact-vs-ANN | No implementado | fase posterior separada |
| Cutover / rollback / dual-write | No implementado | fases posteriores explícitas |
| Ciclo de servidor PostgreSQL | No implementado | backup/restore/upgrade/pooling futuros |
| Reader Core / Semantic Reading Layer | No implementado | capa candidata antes de la admisión |

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

Los issues #331 y #332 se implementaron mediante PR #335 y #337. PostgreSQL sigue siendo
una ruta opcional del operador con `active=false`. La equivalencia correcta no activa un
backend ni modifica Guardian, TruthGate o Canon estricto.

Trabajo futuro:

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal no afirma backend PostgreSQL activo, migración automática, multi-tenancy de
producción, verdad universal, cero alucinaciones, certificación legal/de seguridad ni
conciencia.
