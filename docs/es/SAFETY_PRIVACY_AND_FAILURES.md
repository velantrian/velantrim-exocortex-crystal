<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: es -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Fronteras de seguridad, privacidad y fallos

**Fuente:** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

Esta vista no sustituye pruebas, revisión de seguridad ni análisis jurídico.

## Seguridad epistémica

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

Guardian y TruthGate siguen siendo fronteras de admisión. Las consultas públicas son
read-only y el ingest explícito es la escritura separada. Crystal no garantiza verdad ni
cero alucinaciones; busca que lo no respaldado sea bloqueado, etiquetado, rechazado o auditable.

## Frontera local

La instalación predeterminada no exige cloud, LLM, telemetría ni analytics. SQLite es el
perfil activo ordinario. `auto` durable puede elegir LadybugDB opcional o SQLite y bloquea
la elección; Mock es estado explícito de desarrollo/prueba. PostgreSQL/pgvector es solo un
target inactivo del operador con `active=false`.

## Datos y expansión opcional

Pueden almacenarse claims, metadata, provenance, estado epistémico, grafo, restricciones,
registros de erasure/audit, receipts, outbox, bundles, backups y exports. Los datos salen
de la frontera local únicamente al activar Anthropic, Neo4j remoto, Wikidata, Redis,
migración PostgreSQL, API amplia o copias externas.

## Cifrado y secretos

`VELANTRIM_ENCRYPTION_KEY` protege campos L1 seleccionados, no automáticamente L3, backups,
exports, receipts, logs o temporales. Se requieren cifrado de host y gestión de claves según
la sensibilidad. Las credenciales no deben entrar en profiles, bundles, receipts, logs,
issues ni Notion.

## API, privacidad y borrado

El baseline API usa authentication y loopback. Exposición externa requiere TLS,
autenticación revisada, least privilege, limits, monitoring e incident handling. Access,
rectification, restriction, erasure y processing record son controles de ingeniería, no
certificación RGPD. Borrar el store activo no borra globalmente copias independientes.

## Respuestas seguras a fallos

| Clase | Comportamiento esperado |
|---|---|
| Claim no respaldado | block, label o bounded refusal |
| Mutación read-only | reject / sin cambio de estado |
| Conflicto de profile | fallo antes de cache backend |
| Falta dependencia | error explícito, sin Mock oculto |
| Fallo import | rollback, `active=false` |
| Evidence mismatch | verification failure |
| Manipulación Receipt/audit | fallo digest/hash |
| Migración sobredimensionada | fail closed por límites |
| Exposición de red | solo explícita y autenticada |
| Copia tras erasure | inventario y borrado separados |

## No afirmaciones

Crystal no es certificación de seguridad/legal/RGPD, prueba de escala arbitraria, runtime
PostgreSQL activo, sistema de migración automática, garantía de verdad perfecta, AGI,
consciencia ni evidencia de grant NLnet adjudicado.

Detalles: [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md),
[Failure Modes](../FAILURE_MODES.md) y [resumen inglés](../SAFETY_PRIVACY_AND_FAILURES.md).
