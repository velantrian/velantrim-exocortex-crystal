<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: es -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Límites de almacenamiento y autoridad

## Identidades separadas

```text
storage profile = identidad de despliegue
physical L3 = estado gráfico multiestado
strict Canon = proyección de lectura confiable
migration bundle = evidencia de integridad operativa
retrieval score = señal de ranking
model output = texto generado
```

Ninguna identidad concede automáticamente la autoridad de otra.

## Perfil duradero

SQLite es el perfil activo local-first ordinario. Un primer `auto` duradero puede elegir LadybugDB opcional o SQLite y bloquear backend y locator no secreto. Los conflictos posteriores fallan de forma cerrada. Mock sigue siendo únicamente un estado explícito de desarrollo/CI.

## physical L3 frente a strict Canon

physical L3 puede contener VERIFIED, USER_CLAIMED, UNVERIFIED, HYPOTHESIS, SUBJECTIVE, contested, superseded o restricted. strict Canon es una proyección deny-dominant basada en evidencia y política actuales. Almacenar, recuperar o puntuar alto no basta.

## Lectura y escritura

Las consultas públicas pasan read-only por `core.query_pipeline.query()`. `ingest` explícito es el camino con capacidad de escritura; Guardian y TruthGate aplican después los límites estructurales y epistémicos.

## Ciclo SQLite y migración

Están implementados backup, verificación independiente, inactive restore, logical export determinista acotado y verificación del bundle. Los datasets aprobados de physical L3 pueden importarse a un esquema PostgreSQL nuevo e inactivo y compararse exactamente; el objetivo permanece `active=false`.

Esto no es una migración de todo el sistema: no cubre automáticamente todo L1, audit/outbox, metadatos de cifrado, configuración o copias independientes. Tampoco hay runtime PostgreSQL activo, aceptación ANN, switching automático, cutover, fencing, rollback o dual-write.

## Secretos y copias

Contraseñas, tokens, claves privadas y DSN con credenciales no deben entrar en profiles, bundles, receipts, logs, GitHub o Notion. Backups, exports y migraciones crean copias adicionales; borrar el store activo no las elimina automáticamente. El cifrado selectivo de campos L1 no es cifrado universal.

## Evidencia operativa

| Evento | Prueba | No prueba |
|---|---|---|
| registro en L3 | persistencia física | pertenencia a strict Canon |
| resultado de retrieval | relevancia candidata | evidencia suficiente |
| backup verificado | integridad del backup | verdad de una afirmación |
| importación exitosa | integridad de importación | activation o selección runtime |
| exact equivalence | igualdad de datasets aprobados | preparación productiva o cutover |

El Reader Core dedicado no está implementado; NLnet sigue submitted / under review / not awarded.

## Contratos ingleses detallados

- [Arquitectura completa](../ARCHITECTURE.md)
- [Perfil duradero](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Contrato de migración](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Importación PostgreSQL inactiva](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
