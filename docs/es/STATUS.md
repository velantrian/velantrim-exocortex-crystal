<!-- translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: es -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — estado actual

**Fecha:** 2026-08-08  
**Checkpoint de runtime verificado:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Árbol verificado:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Head validado:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**PR / CI:** #337 / `31256316536`  
**CI PostgreSQL:** `31256316532`

## Verificación

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** mutantes Ring Zero eliminados;
- **9/9** jobs permanentes correctos;
- **1/1** integración real PostgreSQL/pgvector correcta.

Evidencia: [TEST_REPORT.md](../../TEST_REPORT.md) y
[manifest](../status/implementation-manifest.json).

## Frontera de capacidad verificada

Crystal conserva SQLite local-first e implementa la fase 1 del issue #332:

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

El driver PostgreSQL es opcional y se carga de forma diferida solo mediante comandos del
operador. La instalación normal sigue siendo biblioteca estándar pura. El destino no se
registra en el runtime ordinario, permanece `active=false` y no sirve lecturas ni escrituras.

## Frontera de autoridad

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian, TruthGate, restrictions, TrustSnapshot y CanonicalView no cambian.

## Aún ausente

- runtime PostgreSQL activo de lectura/escritura;
- evaluación exact-vs-ANN y umbrales ANN aceptados;
- activación, cutover, fencing, rollback o dual-write;
- ciclo de backup/restore/upgrade, pooling productivo y fencing distribuido;
- IdP/multi-tenancy productivo o certificación legal, de seguridad o RGPD;
- Reader Core verificado dedicado.

## Estado de la subvención

El proyecto fue presentado y está en revisión. **No se afirma adjudicación ni cambio de
presupuesto.** PR #337 e issue #332 ya forman parte de la base y no pueden contarse otra vez
como trabajo futuro financiado.
