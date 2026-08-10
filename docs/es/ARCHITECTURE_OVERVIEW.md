<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: es -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — resumen de arquitectura

Esta traducción es una capa de orientación. En caso de conflicto prevalecen el código fusionado, las pruebas ejecutables, el CI exacto y los contratos ingleses.

## Modelo central

```text
fuentes + ingest explícito
→ procedencia + normalización
→ controles Guardian
→ decisión TruthGate
→ estado operativo L1 + physical L3 multiestado
→ proyección de lectura strict Canon con denegación dominante
→ recuperación read-only / respuesta / negativa acotada
```

Un registro en physical L3 no pasa automáticamente a strict Canon. La puntuación de recuperación, la similitud vectorial y el texto de un modelo no son evidencia independiente.

## Capas de memoria y revisión

- **L0:** contexto efímero del proceso.
- **L1:** SQLite/WAL para estado operativo, evidencia, auditoría, receipts, sesiones de importación/revisión y outbox.
- **L2:** staging pendiente/de revisión para candidatos o cuarentena; no es una capa de verdad final.
- **L3:** almacenamiento gráfico multiestado; no equivale a strict Canon.
- **TrustSnapshot / CanonicalView:** superficie de lectura confiable con política deny-dominant.

## Separación lectura/escritura

`HTTP /ask`, `CLI ask` y MCP usan `core.query_pipeline.query()` en modo read-only. Una consulta no puede crear o reforzar hechos ni modificar ESM, L3, outbox, enlaces de episodios o identidad del embedder. Solo `ingest` explícito puede entrar en el camino de escritura gobernado por Guardian y TruthGate.

## Perfiles y portabilidad

SQLite es el perfil activo local-first ordinario. En el primer `auto` duradero puede seleccionarse LadybugDB opcional o SQLite y después bloquear la identidad del backend y del locator. Está prohibido caer silenciosamente en Mock efímero.

El camino verificado de PostgreSQL/pgvector termina en un objetivo inactivo:

```text
bundle SQLite verificado
→ importación transaccional PostgreSQL
→ re-hash independiente read-only
→ equivalencia exacta
→ active=false
```

Importar o demostrar equivalencia no es activation, selección de backend, admisión TruthGate, cutover, rollback ni dual-write. PostgreSQL no forma parte de la composición runtime normal.

## Lectura de documentos

Source spans, registros de documentos, sesiones de importación y flujos dry-run/review son baseline implementado. No está implementado un Reader Core dedicado de varias pasadas con mapas de cobertura, relectura consciente de contradicciones y síntesis documental.

## No afirmaciones

Crystal no afirma AGI, conciencia, cero alucinaciones, runtime PostgreSQL activo, switching automático, ANN aceptado para producción, cutover/rollback/dual-write, certificación de seguridad/legal/GDPR ni concesión NLnet.

## Fuentes inglesas

- [Arquitectura completa](../ARCHITECTURE.md)
- [Límites de almacenamiento y autoridad](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Estado de implementación](../IMPLEMENTATION_STATUS.md)
- [Importación PostgreSQL inactiva](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
