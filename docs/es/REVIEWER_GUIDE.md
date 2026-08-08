<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: es -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Guía para revisores — Velantrim Exo-Cortex Crystal

**Checkpoint inglés:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
Esta guía es orientación mantenida. La evidencia de implementación sigue siendo el código
en `main`, las pruebas ejecutables, el CI exacto, [TEST_REPORT.md](../../TEST_REPORT.md) y
el [manifest](../status/implementation-manifest.json).

## 1. Qué se revisa

Crystal es infraestructura pública, local-first, basada en fuentes y auditable para memoria
de sistemas de IA. La base verificada incluye claims tipados, Guardian/TruthGate, una
proyección estricta de Canon sobre L3 multiestado, consultas públicas de solo lectura,
un ingest explícito separado, Receipts y procedencia auditable.

No afirma AGI, consciencia, verdad universal, cero alucinaciones, runtime PostgreSQL activo,
switching automático, multi-tenancy productivo, certificación de seguridad/RGPD ni grant
NLnet adjudicado.

## 2. Reproducir la base

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Las métricas mutables se consultan únicamente en el informe de pruebas inglés.

## 3. Frontera de lectura y escritura

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → explícito, atribuido y auditado
```

El `ask` público usa `core.query_pipeline.query()` y no debe mutar facts, ESM, L3, outbox,
enlaces de episodios, identidad de embeddings ni candidatos desconocidos. Una negativa
acotada por grounding insuficiente es comportamiento seguro esperado.

`ingest` escribe, pero admission depende de evidence, tipo de claim, policy y TruthGate.
La salida del modelo no puede autocertificarse como hecho mundial verificado.

## 4. Storage y migración

SQLite es el perfil activo local-first ordinario. Un primer `auto` durable puede elegir
LadybugDB opcional si está instalado, o SQLite; la elección y el locator no secreto quedan
bloqueados. Está prohibido el fallback silencioso a Mock efímero.

PostgreSQL/pgvector es una ruta separada del operador: bundle verificado → preflight de
versión/TLS → schema inactivo nuevo → importación serializable → re-hash independiente
read-only → equivalencia exacta; el destino permanece `active=false`.

Import/equivalence no es activation, selection, TruthGate admission, strict Canon,
cutover, rollback, dual-write ni production readiness.

## 5. Seguridad y privacidad

La operación predeterminada no requiere cloud, LLM, telemetry ni analytics. Remote Neo4j,
Anthropic, Wikidata, Redis, migración PostgreSQL, API amplia o copias backup/export amplían
la frontera solo por decisión del operador.

`VELANTRIM_ENCRYPTION_KEY` protege campos L1 seleccionados, no automáticamente todo L3,
backup, bundle, Receipt, log o temporal. Credentials y DSN con secretos no deben entrar en
profiles, bundles, receipts, logs, issues o Notion.

El borrado del store local activo no borra automáticamente backups, exports, copias del
operador, sistemas remotos ni datos de terceros.

## 6. Fallos fail-closed

- Claims no respaldados se bloquean, etiquetan o reciben negativa acotada.
- Conflictos de profile/locator fallan antes de cachear backend.
- Fallo de importación hace rollback y mantiene `active=false`.
- Mismatch de evidence y manipulación Receipt/audit se detectan.
- Input sobredimensionado falla por límites.
- Dependencia opcional ausente no causa switch durable oculto.
- Exposición externa exige TLS, authentication, least privilege y monitoring.

## 7. Lista de revisión

- [ ] `main` y CI exacto identificados.
- [ ] Query read-only separada de ingest explícito.
- [ ] L3 físico separado de strict Canon.
- [ ] Import PostgreSQL inactivo separado de activation.
- [ ] Adaptadores de red, secrets, encryption y erasure revisados.
- [ ] No se infieren certificación, production readiness o grant award.

Fuentes inglesas: [Reviewer Guide](../REVIEWER_GUIDE.md), [Security](../../SECURITY.md),
[Privacy](../../PRIVACY.md), [Failure Modes](../FAILURE_MODES.md) y
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md).
